#!/usr/bin/env python3
"""Verify or repair HTML direction from the actual script used by /ku/ pages."""

from __future__ import annotations

import argparse
import re
from html.parser import HTMLParser
from pathlib import Path


HTML_TAG = re.compile(r'<html\b(?P<attrs>[^>]*)>', re.IGNORECASE)
LANG_KU = re.compile(r'\blang=["\']ku(?:-[^"\']+)?["\']', re.IGNORECASE)
DIR = re.compile(r'\bdir=["\'](?P<value>ltr|rtl)["\']', re.IGNORECASE)
ARABIC = re.compile(r'[\u0600-\u06ff]')
LATIN = re.compile(r'[A-Za-zÀ-ž]')


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.hidden = 0
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag.casefold() in {"script", "style", "noscript"}:
            self.hidden += 1

    def handle_endtag(self, tag: str) -> None:
        if tag.casefold() in {"script", "style", "noscript"} and self.hidden:
            self.hidden -= 1

    def handle_data(self, data: str) -> None:
        if not self.hidden:
            self.parts.append(data)


def expected_direction(source: str) -> tuple[str, int, int]:
    parser = VisibleText()
    parser.feed(source)
    text = " ".join(parser.parts)
    arabic = len(ARABIC.findall(text))
    latin = len(LATIN.findall(text))
    return ("rtl" if arabic > latin else "ltr", arabic, latin)


def inspect(path: Path) -> tuple[str, str, int, int] | None:
    source = path.read_text(encoding="utf-8", errors="replace")
    match = HTML_TAG.search(source)
    if not match or not LANG_KU.search(match.group("attrs")):
        return None
    direction = DIR.search(match.group("attrs"))
    actual = direction.group("value").casefold() if direction else "missing"
    expected, arabic, latin = expected_direction(source)
    return actual, expected, arabic, latin


def repair(path: Path, expected: str) -> None:
    source = path.read_text(encoding="utf-8")
    match = HTML_TAG.search(source)
    if not match:
        raise ValueError(f"missing html tag: {path}")
    tag = match.group(0)
    if DIR.search(tag):
        replacement = DIR.sub(f'dir="{expected}"', tag, count=1)
    else:
        replacement = tag[:-1] + f' dir="{expected}">'
    path.write_text(source[:match.start()] + replacement + source[match.end():], encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    pages = sorted((args.site_root / "ku").glob("*.html"))
    mismatches: list[tuple[Path, str, str, int, int]] = []
    for path in pages:
        result = inspect(path)
        if result is None:
            continue
        actual, expected, arabic, latin = result
        if actual != expected:
            mismatches.append((path, actual, expected, arabic, latin))
    if args.apply:
        for path, _actual, expected, _arabic, _latin in mismatches:
            repair(path, expected)
    print(f"checked={len(pages)} mismatches={len(mismatches)} applied={len(mismatches) if args.apply else 0}")
    for path, actual, expected, arabic, latin in mismatches[:10]:
        print(f"{path.name}: actual={actual} expected={expected} arabic={arabic} latin={latin}")
    return 0 if args.apply or not mismatches else 1


if __name__ == "__main__":
    raise SystemExit(main())
