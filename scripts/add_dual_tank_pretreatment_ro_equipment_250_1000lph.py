#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 250-1000 L/h dual-tank pretreatment RO equipment across all language pages."""

from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DUAL = runpy.run_path(str(ROOT / "scripts" / "add_dual_tank_pretreatment_integrated_skid_ro_product.py"))
DUAL_GLOBALS = DUAL["main"].__globals__
ORIGINAL_BUILD_MAIN = DUAL_GLOBALS["build_main"]
ORIGINAL_COPY_FOR = DUAL_GLOBALS["copy_for"]
ORIGINAL_PRODUCT_GRAPH = DUAL_GLOBALS["product_graph"]
ORIGINAL_TERMS = DUAL_GLOBALS["TERMS"]

NEW_SLUG = "product-dual-tank-pretreatment-ro-equipment-250-1000lph.html"
PRODUCT_ID = "dual-tank-pretreatment-ro-equipment-250-1000lph"
MAIN_IMAGE = "dual-tank-pretreatment-ro-equipment-250l-1000l-blue-frp-tanks-oem.webp"
SECOND_IMAGE = "dual-tank-pretreatment-ro-equipment-250l-1000l-stainless-tanks-oem.webp"
IMAGE_WIDTH = 540
IMAGE_HEIGHT = 714
SECOND_IMAGE_WIDTH = 540
SECOND_IMAGE_HEIGHT = 662
AFTER_SLUG = "product-three-tank-pretreatment-integrated-skid-ro-equipment.html"
TODAY = "2026-06-21"
FLOW_UNITS = {
    "af": "L/uur", "ar": "لتر/ساعة", "az": "L/saat", "bg": "л/ч", "bn": "লিটার/ঘণ্টা",
    "bs": "L/h", "cs": "l/h", "da": "L/time", "de": "L/h", "el": "L/h", "en": "L/h",
    "es": "L/h", "et": "L/h", "fa": "لیتر/ساعت", "fi": "L/h", "fr": "L/h",
    "ha": "L/sa'a", "he": "ליטר/שעה", "hi": "लि/घंटा", "hr": "L/h", "hu": "L/óra",
    "hy": "լ/ժ", "id": "L/jam", "it": "L/h", "ja": "L/時", "ka": "ლ/სთ",
    "kk": "л/сағ", "ko": "L/시간", "ku": "L/saet", "ky": "л/саат", "lt": "L/val.",
    "lv": "L/h", "ms": "L/jam", "nl": "L/uur", "no": "L/time", "pl": "l/h",
    "pt": "L/h", "ro": "L/h", "ru": "л/ч", "sk": "l/h", "sl": "L/h",
    "sq": "L/orë", "sr": "л/ч", "sr-me": "L/h", "sv": "L/h", "sw": "L/saa",
    "ta": "லி/மணி", "tg": "л/соат", "th": "ลิตร/ชม.", "tk": "L/sagat",
    "tl": "L/oras", "tr": "L/saat", "uk": "л/год", "ur": "لیٹر/گھنٹہ",
    "uz": "L/soat", "vi": "L/giờ", "zu": "L/ihora",
}
FLOW_PATTERNS = (
    "250-1000 L/h", "250-1000 L/saat", "250-1000 L/jam", "250-1000 L/soat",
    "250-1000 L/giờ", "250-1000 लि/घंटा", "250-1000 லி/மணி",
    "250-1000 л/ч", "250-1000 لتر/ساعة", "250-1000 لیتر/ساعت",
    "250-1000 ליטר/שעה",
)


def flow_value(lang: str) -> str:
    return f"250-1000 {FLOW_UNITS.get(lang, FLOW_UNITS['en'])}"


def localize_flow_units(lang: str, text: str) -> str:
    value = flow_value(lang)
    for pattern in FLOW_PATTERNS:
        text = text.replace(pattern, value)
    return text


def replace_flow(text: str) -> str:
    return (
        text.replace("1000-3000 L/h", "250-1000 L/h")
        .replace("1000-3000 L/saat", "250-1000 L/saat")
        .replace("1000-3000 L/jam", "250-1000 L/jam")
        .replace("1000-3000 L/soat", "250-1000 L/soat")
        .replace("1000-3000 L/giờ", "250-1000 L/giờ")
        .replace("1000-3000 लि/घंटा", "250-1000 लि/घंटा")
        .replace("1000-3000 லி/மணி", "250-1000 லி/மணி")
        .replace("1000-3000 л/ч", "250-1000 л/ч")
        .replace("1000-3000 لتر/ساعة", "250-1000 لتر/ساعة")
        .replace("1000-3000 لیتر/ساعت", "250-1000 لیتر/ساعت")
        .replace("1000-3000 ליטר/שעה", "250-1000 ליטר/שעה")
    )


def build_terms() -> dict[str, dict[str, str]]:
    terms: dict[str, dict[str, str]] = {}
    for lang, values in ORIGINAL_TERMS.items():
        item = {key: localize_flow_units(lang, replace_flow(value)) for key, value in values.items()}
        terms[lang] = item

    terms["en"].update({
        "name": "Dual-Tank Pretreatment Reverse Osmosis Equipment 250-1000 L/h",
        "category": "Dual-tank pretreatment RO equipment",
        "intro": "Yuchen Water dual-tank pretreatment reverse osmosis equipment is designed for B2B projects that need 250-1000 L/h purified water from tap water or groundwater. The system combines an automatic sand tank, automatic carbon tank, precision filter and RO purification in a compact frame, with 0.1-0.4 MPa feed pressure. Appearance, process flow, component configuration and control functions can be customized according to water analysis, installation space and buyer requirements.",
        "card": "Dual-tank pretreatment RO equipment with automatic sand and carbon tanks, precision filtration and 250-1000 L/h purified water output for customized OEM projects.",
        "category": "Dual-tank pretreatment RO equipment",
        "app_value": "Hotels, workshops, schools, clinics, commercial kitchens, groundwater pretreatment and compact water purification projects",
    })
    return terms


TERMS = build_terms()


def copy_for(lang: str) -> dict:
    copy = ORIGINAL_COPY_FOR(lang)
    copy["values"][3] = flow_value(lang)
    copy["meta"] = localize_flow_units(lang, replace_flow(copy["meta"]))
    copy["quote"] = f"{copy['request']}: {copy['name']}"
    copy["quote_desc"] = copy["intro"]
    copy["faq_pairs"] = [
        (f"{copy['labels'][2]}?", copy["values"][2]),
        (f"{copy['labels'][3]}?", copy["values"][3]),
        (f"{copy['labels'][5]}?", copy["values"][5]),
        (f"{copy['labels'][6]}?", copy["values"][6]),
    ]
    return copy


def build_main(lang: str, copy: dict) -> str:
    text = ORIGINAL_BUILD_MAIN(lang, copy)
    text = text.replace(
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Dual%20Tank%20Pretreatment%20RO%20Equipment%20250-1000Lph",
    )
    gallery = (
        f'<div class="product-gallery">'
        f'<a href="../assets/products/{SECOND_IMAGE}">'
        f'<img src="../assets/products/{SECOND_IMAGE}" alt="{DUAL_GLOBALS["esc"](copy["name"])}" loading="lazy" decoding="async" width="{SECOND_IMAGE_WIDTH}" height="{SECOND_IMAGE_HEIGHT}" />'
        f'</a></div>'
    )
    text = re.sub(
        r'(<img src="\.\./assets/products/' + re.escape(MAIN_IMAGE) + r'"[^>]*class="product-main-image" />)',
        r"\1" + gallery,
        text,
        count=1,
    )
    return text


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(ORIGINAL_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [
                f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}",
                f"https://www.yuchensy.com/assets/products/{SECOND_IMAGE}",
            ]
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = copy_for("en")
    insert_at = next((i + 1 for i, item in enumerate(products) if item.get("id") == "three-tank-pretreatment-integrated-skid-ro-equipment"), 6)
    products.insert(insert_at, {
        "id": PRODUCT_ID,
        "name": copy["name"],
        "category": "RO System",
        "desc": copy["card"],
        "specs": dict(zip(copy["labels"], copy["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": copy["intro"],
        "features": [
            "Automatic sand tank and carbon tank",
            "Precision filter plus RO purification",
            "250-1000 L/h purified water flow",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Hotels, workshops, schools, clinics, commercial kitchens, groundwater pretreatment and compact water purification projects.",
        "related": [
            "dual-tank-pretreatment-integrated-skid-ro-equipment",
            "three-tank-pretreatment-integrated-skid-ro-equipment",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Dual-Tank Pretreatment Reverse Osmosis Equipment 250-1000 L/h: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    DUAL_GLOBALS["NEW_SLUG"] = NEW_SLUG
    DUAL_GLOBALS["PRODUCT_ID"] = PRODUCT_ID
    DUAL_GLOBALS["MAIN_IMAGE"] = MAIN_IMAGE
    DUAL_GLOBALS["IMAGE_WIDTH"] = IMAGE_WIDTH
    DUAL_GLOBALS["IMAGE_HEIGHT"] = IMAGE_HEIGHT
    DUAL_GLOBALS["AFTER_SLUG"] = AFTER_SLUG
    DUAL_GLOBALS["TODAY"] = TODAY
    DUAL_GLOBALS["TERMS"] = TERMS
    DUAL_GLOBALS["copy_for"] = copy_for
    DUAL_GLOBALS["build_main"] = build_main
    DUAL_GLOBALS["product_graph"] = product_graph
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()


if __name__ == "__main__":
    main()
