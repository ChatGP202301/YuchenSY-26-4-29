#!/usr/bin/env python3
"""Apply and verify the bounded Quick-Change collection LCP repair."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

ROUTE = "quick-change-water-filter-cartridges.html"
ASYNC_ASSETS = ("assets/styles.min.css", "assets/commercial-ro-products.css")
LAYOUT_ASSET = "assets/sanyishui-catalog.css"
LAYOUT_VERSION = "20260921-lcp-wrap"
REMOVE_ASSETS = ("assets/products/siliphos/siliphos-product.css", "assets/pp-filter-family.css")


def transform(text: str) -> str:
    text = re.sub(
        rf'(<link rel="stylesheet" href="\.\./{re.escape(LAYOUT_ASSET)}\?v=)[^"]+("[^>]*>)',
        rf'\g<1>{LAYOUT_VERSION}\2',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'\s*<link rel="preload" href="\.\./assets/backgrounds/eco_hero1\.webp" as="image"\s*/?>',
        "",
        text,
        flags=re.I,
    )
    for asset in REMOVE_ASSETS:
        text = re.sub(
            rf'\s*<link rel="stylesheet" href="\.\./{re.escape(asset)}\?v=[^"]+"\s*/?>',
            "",
            text,
            flags=re.I,
        )
    for asset in ASYNC_ASSETS:
        # Replace the whole asset line so repeated runs collapse any older
        # nested noscript markup back to one canonical, idempotent pair.
        pattern = rf'^.*href="(\.\./{re.escape(asset)}\?v=[^"]+)".*$'
        match = re.search(pattern, text, re.I | re.M)
        if match:
            href = match.group(1)
            preserved_layout = (
                f'<link rel="stylesheet" href="../{LAYOUT_ASSET}?v={LAYOUT_VERSION}" media="all">'
                if LAYOUT_ASSET in match.group(0) else ""
            )
            replacement = (
                f'<link rel="preload" href="{href}" as="style" '
                f'onload="this.onload=null;this.rel=\'stylesheet\'">'
                f'<noscript><link rel="stylesheet" href="{href}"></noscript>{preserved_layout}'
            )
            text = text[:match.start()] + replacement + text[match.end():]
    text = re.sub(
        r'<style id="quick-change-layout-css">.*?</style>',
        f'<link rel="stylesheet" href="../{LAYOUT_ASSET}?v={LAYOUT_VERSION}" media="all">',
        text,
        count=1,
        flags=re.I | re.S,
    )
    if LAYOUT_ASSET not in text:
        text = text.replace(
            "</head>",
            f'<link rel="stylesheet" href="../{LAYOUT_ASSET}?v={LAYOUT_VERSION}" media="all">\n</head>',
            1,
        )
    text = re.sub(
        r'(<figure class="sy-bayonet-photo[^"]*"[^>]*><img\b[^>]*?)\sloading="eager"([^>]*>)',
        r'\1 loading="lazy"\2',
        text,
        flags=re.I,
    )
    text = re.sub(
        r'(<figure class="sy-bayonet-photo[^"]*"[^>]*><img\b(?![^>]*\bfetchpriority=)[^>]*)(>)',
        r'\1 fetchpriority="low"\2',
        text,
        flags=re.I,
    )
    return text


def pages(root: Path) -> list[Path]:
    return sorted(path for path in root.glob(f"*/{ROUTE}") if path.is_file())


def verify(root: Path) -> None:
    targets = pages(root)
    if len(targets) != 62:
        raise SystemExit(f"expected 62 localized pages, found {len(targets)}")
    failures: list[str] = []
    for path in targets:
        text = path.read_text(encoding="utf-8")
        if "eco_hero1.webp" in text:
            failures.append(f"{path}: stale background preload")
        for asset in REMOVE_ASSETS:
            if asset in text:
                failures.append(f"{path}: unrelated stylesheet {asset}")
        required_async_assets = ASYNC_ASSETS if path.parent.name != "en" else ASYNC_ASSETS[:1]
        for asset in required_async_assets:
            if not re.search(rf'<link rel="preload" href="\.\./{re.escape(asset)}\?v=[^"]+" as="style"', text):
                failures.append(f"{path}: missing async stylesheet preload {asset}")
            if text.count(f'../{asset}?v=') != 2:
                failures.append(f"{path}: non-canonical async stylesheet markup {asset}")
        if not re.search(rf'<link rel="stylesheet" href="\.\./{re.escape(LAYOUT_ASSET)}\?v={re.escape(LAYOUT_VERSION)}"', text):
            failures.append(f"{path}: missing current blocking page-specific stylesheet")
        if 'loading="eager"' in text:
            failures.append(f"{path}: gallery still eager")
        if text.count('class="sy-bayonet-photo') != 13:  # grid token + 12 figures
            failures.append(f"{path}: gallery structure changed")
        if text.count('fetchpriority="low"') < 12:
            failures.append(f"{path}: missing low-priority gallery hints")
        if '<h1>' not in text or '<link rel="canonical"' not in text:
            failures.append(f"{path}: required page semantics missing")
    if failures:
        raise SystemExit("\n".join(failures))
    print(f"PASS: {len(targets)} Quick-Change pages satisfy the bounded LCP contract")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, default=Path.cwd())
    parser.add_argument("mode", choices=("apply", "verify"))
    args = parser.parse_args()
    root = args.site_root.resolve()
    if args.mode == "apply":
        changed = 0
        for path in pages(root):
            before = path.read_text(encoding="utf-8")
            after = transform(before)
            if after != before:
                path.write_text(after, encoding="utf-8")
                changed += 1
        print(f"changed {changed} pages")
    verify(root)


if __name__ == "__main__":
    main()
