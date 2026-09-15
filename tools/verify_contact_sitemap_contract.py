#!/usr/bin/env python3
"""Verify indexable localized contact pages are present once in their sitemap."""

from __future__ import annotations

import re
import sys
from pathlib import Path
from xml.etree import ElementTree as ET


SITE_ROOT = Path(__file__).resolve().parents[1]
ORIGIN = "https://www.yuchensy.com"


def sitemap_urls(path: Path) -> list[str]:
    return [
        element.text.strip()
        for element in ET.parse(path).getroot().iter()
        if element.tag.endswith("loc") and element.text
    ]


def main() -> int:
    errors: list[str] = []
    checked = 0
    for sitemap in sorted((SITE_ROOT / "sitemaps").glob("sitemap-*.xml")):
        locale = sitemap.stem.removeprefix("sitemap-")
        if locale == "root":
            continue
        contact = SITE_ROOT / locale / "contact.html"
        if not contact.is_file():
            continue
        html = contact.read_text(encoding="utf-8-sig")
        robots = re.search(
            r'<meta\b[^>]*\bname=["\']robots["\'][^>]*\bcontent=["\']([^"\']+)',
            html,
            re.I,
        )
        if not robots or "noindex" in robots.group(1).lower():
            continue
        checked += 1
        expected = f"{ORIGIN}/{locale}/contact.html"
        count = sitemap_urls(sitemap).count(expected)
        if count != 1:
            errors.append(f"{sitemap.relative_to(SITE_ROOT)}: {expected} count={count}")

    if errors:
        print("FAIL contact sitemap contract")
        for error in errors:
            print(error)
        return 1
    print(f"PASS contact sitemap contract: {checked} indexable localized contact pages")
    return 0


if __name__ == "__main__":
    sys.exit(main())
