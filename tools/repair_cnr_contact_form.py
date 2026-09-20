#!/usr/bin/env python3
"""Restore the established localized quote form on the CNR contact page.

The six later-generated locale contact pages were emitted as contact-card-only
shells.  CNR already loads the shared form CSS and JavaScript, so this bounded
repair reuses the reviewed sr-me localized form contract while changing only
the locale-specific IDs, page URL, and submitted-language value.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


FORM_RE = re.compile(r'(<form class="contact-form"(?:\s|>).*?</form>)', re.DOTALL)
MAIN_END = "</main>"


def transform(target: str, source: str) -> str:
    if FORM_RE.search(target):
        return target

    match = FORM_RE.search(source)
    if match is None:
        raise ValueError("reviewed sr-me contact form is missing")
    if target.count(MAIN_END) != 1:
        raise ValueError("CNR contact page must contain exactly one main end tag")

    form = match.group(1)
    form = form.replace("-sr-me", "-cnr")
    form = form.replace("/sr-me/contact.html", "/cnr/contact.html")
    form = form.replace('value="sr-me" data-submitted-language',
                        'value="cnr" data-submitted-language')

    section = (
        '<section class="tx-section"><div class="tx-container">'
        + form
        + "</div></section>"
    )
    return target.replace(MAIN_END, section + MAIN_END)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    target_path = args.site_root / "cnr" / "contact.html"
    source_path = args.site_root / "sr-me" / "contact.html"
    target = target_path.read_text(encoding="utf-8")
    source = source_path.read_text(encoding="utf-8")
    repaired = transform(target, source)
    changed = repaired != target

    if args.apply and changed:
        target_path.write_text(repaired, encoding="utf-8")

    fields = len(re.findall(r"<(?:input|textarea|select|button)\b", repaired))
    print(
        f"route=cnr/contact.html forms={len(FORM_RE.findall(repaired))} "
        f"fields={fields} changed={str(changed).lower()} "
        f"applied={str(args.apply and changed).lower()}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
