#!/usr/bin/env python3
"""Align sitemap URL membership with the static deployment output tree."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import unquote, urlparse
from xml.etree import ElementTree as ET


EXPECTED_INITIAL_MISSING = 1108


def output_path(site: Path, url: str) -> Path:
    path = unquote(urlparse(url).path)
    if path == "/":
        return site / "index.html"
    if path.endswith("/"):
        return site / path.lstrip("/") / "index.html"
    return site / path.lstrip("/")


def sitemap_urls(path: Path) -> list[str]:
    return [
        node.text.strip()
        for node in ET.parse(path).getroot().iter()
        if node.tag.endswith("loc") and node.text
    ]


def inventory(site: Path) -> dict[Path, list[str]]:
    missing: dict[Path, list[str]] = {}
    for sitemap in sorted((site / "sitemaps").glob("sitemap-*.xml")):
        absent = [url for url in sitemap_urls(sitemap) if not output_path(site, url).is_file()]
        if absent:
            missing[sitemap] = absent
    return missing


def remove_urls(text: str, urls: set[str]) -> tuple[str, int]:
    pattern = re.compile(r"[ \t]*<(?:\w+:)?url>.*?</(?:\w+:)?url>[ \t]*\n?", re.S)
    removed = 0

    def keep_or_remove(match: re.Match[str]) -> str:
        nonlocal removed
        block = match.group(0)
        loc = re.search(r"<(?:\w+:)?loc>(.*?)</(?:\w+:)?loc>", block)
        if loc and loc.group(1).strip() in urls:
            removed += 1
            return ""
        return block

    return pattern.sub(keep_or_remove, text), removed


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=Path("."))
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    site = args.site_root.resolve()
    missing = inventory(site)
    count = sum(map(len, missing.values()))
    result = {
        "mode": "apply" if args.apply else "audit",
        "missing_output_urls": count,
        "affected_sitemaps": len(missing),
        "by_sitemap": {path.name: len(urls) for path, urls in missing.items()},
    }
    if not args.apply:
        result["status"] = "PASS" if count == 0 else "FAIL"
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if count == 0 else 1
    if count != EXPECTED_INITIAL_MISSING:
        raise SystemExit(
            f"refusing scope drift: expected {EXPECTED_INITIAL_MISSING} missing outputs, found {count}"
        )
    removed = 0
    for sitemap, urls in missing.items():
        original = sitemap.read_text(encoding="utf-8-sig")
        updated, removed_here = remove_urls(original, set(urls))
        if removed_here != len(urls):
            raise SystemExit(f"{sitemap}: expected {len(urls)} removals, found {removed_here}")
        sitemap.write_text(updated, encoding="utf-8")
        removed += removed_here
    remaining = inventory(site)
    result.update(
        {
            "removed_urls": removed,
            "remaining_missing_output_urls": sum(map(len, remaining.values())),
            "status": "PASS" if not remaining else "FAIL",
        }
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if not remaining else 1


if __name__ == "__main__":
    raise SystemExit(main())
