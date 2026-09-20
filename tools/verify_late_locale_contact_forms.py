#!/usr/bin/env python3
"""Verify quote-form contracts for the six later-generated locale pages."""

from __future__ import annotations

import sys
from pathlib import Path

from bs4 import BeautifulSoup


SITE_ROOT = Path(__file__).resolve().parents[1]
LOCALES = ("be", "cnr", "ga", "lb", "mk", "mt")
ACTION = "https://formsubmit.co/expresswater025@gmail.com"


def main() -> int:
    errors: list[str] = []
    for locale in LOCALES:
        path = SITE_ROOT / locale / "contact.html"
        soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
        form = soup.select_one("form.contact-form#quoteForm")
        if form is None:
            errors.append(f"{locale}: missing quoteForm")
            continue
        checks = {
            "action": form.get("action") == ACTION,
            "method": form.get("method") == "POST",
            "anti-spam": form.get("data-form-protection") == "required-anti-spam",
            "honeypot": form.select_one("[data-spam-trap]") is not None,
            "token": form.select_one("[data-form-token]") is not None,
            "source-check": form.select_one("[data-form-source-check]") is not None,
            "locale": (
                form.select_one("[data-submitted-language]") is not None
                and form.select_one("[data-submitted-language]").get("value") == locale
            ),
            "page": (
                form.select_one("[data-current-page]") is not None
                and form.select_one("[data-current-page]").get("value")
                == f"https://www.yuchensy.com/{locale}/contact.html"
            ),
            "required-fields": len(form.select("[required]")) == 9,
        }
        for name, passed in checks.items():
            if not passed:
                errors.append(f"{locale}: failed {name}")

    if errors:
        print("FAIL late-locale contact form contract")
        for error in errors:
            print(error)
        return 1
    print(f"PASS late-locale contact form contract: {len(LOCALES)} locales")
    return 0


if __name__ == "__main__":
    sys.exit(main())
