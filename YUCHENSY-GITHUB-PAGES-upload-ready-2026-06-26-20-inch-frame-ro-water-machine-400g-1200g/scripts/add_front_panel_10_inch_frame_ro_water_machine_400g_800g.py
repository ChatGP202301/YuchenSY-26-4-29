#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add front-panel 10-inch frame RO water machine 400G-800G across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_10_inch_frame_ro_water_machine_400g_1200g.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["BASE_COPY_FOR"]
BASE_BUILD_MAIN = BASE["BASE_BUILD_MAIN"]
BASE_PRODUCT_GRAPH = BASE["BASE_PRODUCT_GRAPH"]
OPERATION_VALUES = BASE["OPERATION_VALUES"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
PRODUCT_NAMES = BASE["PRODUCT_NAMES"]
TEN_INCH = BASE["TEN_INCH"]
POST_CARBON = BASE["POST_CARBON"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-front-panel-10-inch-frame-ro-water-machine-400g-800g.html"
PRODUCT_ID = "front-panel-10-inch-frame-ro-water-machine-400g-800g"
MAIN_IMAGE = "front-panel-10-inch-frame-ro-water-machine-400g-800g-oem.webp"
IMAGE_WIDTH = 420
IMAGE_HEIGHT = 508
AFTER_SLUG = "product-10-inch-frame-ro-water-machine-400g-800g.html"
TODAY = "2026-06-26"
BRAND = "Yuchen Water"


FRONT_PANEL_MODIFIER = {
    "af": "met voorpaneel",
    "ar": "بواجهة أمامية",
    "az": "ön panelli",
    "bg": "с преден панел",
    "bn": "সামনের প্যানেলসহ",
    "bs": "s prednjim panelom",
    "cs": "s předním panelem",
    "da": "med frontpanel",
    "de": "mit Frontblende",
    "el": "με μπροστινό πάνελ",
    "en": "Front Panel",
    "es": "con panel frontal",
    "et": "esipaneeliga",
    "fa": "با پنل جلو",
    "fi": "etupaneelilla",
    "fr": "avec panneau avant",
    "ha": "mai panel na gaba",
    "he": "עם לוח קדמי",
    "hi": "फ्रंट पैनल के साथ",
    "hr": "s prednjom pločom",
    "hu": "előlappal",
    "hy": "առջևի վահանակով",
    "id": "dengan panel depan",
    "it": "con pannello frontale",
    "ja": "前面パネル付き",
    "ka": "წინა პანელით",
    "kk": "алдыңғы панельмен",
    "ko": "전면 패널형",
    "ku": "bi panela pêşîn",
    "ky": "алдыңкы панелдүү",
    "lt": "su priekiniu skydeliu",
    "lv": "ar priekšējo paneli",
    "ms": "dengan panel hadapan",
    "nl": "met frontpaneel",
    "no": "med frontpanel",
    "pl": "z panelem przednim",
    "pt": "com painel frontal",
    "ro": "cu panou frontal",
    "ru": "с передней панелью",
    "sk": "s predným panelom",
    "sl": "s sprednjo ploščo",
    "sq": "me panel të përparmë",
    "sr": "са предњим панелом",
    "sr-me": "sa prednjim panelom",
    "sv": "med frontpanel",
    "sw": "yenye paneli ya mbele",
    "ta": "முன்புற பலகையுடன்",
    "tg": "бо панели пеш",
    "th": "พร้อมแผงด้านหน้า",
    "tk": "öň panel bilen",
    "tl": "may harapang panel",
    "tr": "ön panelli",
    "uk": "з передньою панеллю",
    "ur": "سامنے والے پینل کے ساتھ",
    "uz": "old panel bilan",
    "vi": "có mặt trước",
    "zu": "enephaneli yangaphambili",
}


def dirs() -> list[str]:
    return sorted(
        p.name
        for p in ROOT.iterdir()
        if p.is_dir()
        and (p / "index.html").exists()
        and re.fullmatch(r"[a-z]{2}(?:-[a-z]{2})?", p.name)
    )


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def product_name(lang: str) -> str:
    base = PRODUCT_NAMES[lang]
    modifier = FRONT_PANEL_MODIFIER[lang]
    if lang == "en":
        return f"{modifier} {base}"
    if lang in {"bn", "hi", "ja", "ko", "ta", "th", "ur"}:
        return f"{modifier} {base}"
    return f"{base} {modifier}"


def treatment_value(lang: str) -> str:
    ten = TEN_INCH[lang]
    post = POST_CARBON[lang]
    return f"{ten} PP + {ten} UDF + {ten} PP + 3012 RO + T33 {post}"


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    missing_sources = [
        name
        for name, source in {
            "product name": PRODUCT_NAMES,
            "front panel": FRONT_PANEL_MODIFIER,
            "10-inch": TEN_INCH,
            "post carbon": POST_CARBON,
            "operation": OPERATION_VALUES,
            "feed water": FEED_WATER_VALUES,
        }.items()
        if lang not in source
    ]
    if missing_sources:
        raise KeyError(f"No {', '.join(missing_sources)} translation for {lang}")

    raw_name = product_name(lang)
    name = f"{raw_name} 400G-800G"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = treatment_value(lang)
    values[3] = "400G-800G"
    values[4] = FEED_WATER_VALUES[lang]
    values[5] = "0.1-0.4 MPa"
    intro = (
        f"{name}. {labels[1]}: {values[1]}. "
        f"{labels[2]}: {values[2]}. {labels[3]}: {values[3]}. "
        f"{labels[4]}: {values[4]}. {labels[5]}: {values[5]}. "
        f"{labels[6]}: {values[6]}."
    )
    card = f"{raw_name}: {values[2]}; {values[3]}; {values[4]}."
    copy = {
        **base,
        "name": name,
        "category": raw_name,
        "intro": intro,
        "card": card,
        "labels": labels,
        "values": values,
    }
    copy["title"] = f"{name} | {BRAND}"
    copy["meta"] = clean_meta(intro)
    copy["quote"] = f"{copy['request']}: {name}"
    copy["quote_desc"] = intro
    copy["faq_pairs"] = [
        (f"{labels[1]}?", values[1]),
        (f"{labels[2]}?", values[2]),
        (f"{labels[3]}?", values[3]),
        (f"{labels[4]}?", values[4]),
        (f"{labels[5]}?", values[5]),
        (f"{labels[6]}?", values[6]),
    ]
    return copy


def build_main(lang: str, copy: dict) -> str:
    text = BASE_BUILD_MAIN(lang, copy)
    text = text.replace(
        "Horizontal%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250Lph",
        quote(f"{copy['request']}: {copy['name']}", safe=""),
    )
    return text


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(BASE_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}"]
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def update_products_page(lang: str) -> None:
    path = ROOT / lang / "products.html"
    text = path.read_text(encoding="utf-8")
    card = PRODUCT_CARD(lang)
    main_start = text.find("<main")
    scope_start = main_start if main_start >= 0 else 0
    scoped_text = text[scope_start:]
    pattern = (
        r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>'
        r'(?:(?!</article>).)*?'
        + re.escape(NEW_SLUG)
        + r'(?:(?!</article>).)*?</article>)'
    )
    if re.search(pattern, text, flags=re.S):
        text = re.sub(pattern, card, text, count=1, flags=re.S)
    else:
        match = None
        for anchor in [
            AFTER_SLUG,
            "product-10-inch-frame-ro-water-machine-400g-1200g.html",
            "product-commercial-big-blue-ro-water-purifier-400g-800g.html",
            "product-portable-custom-ro-water-purifier-400g-800g.html",
            "product-built-in-pressure-tank-ro.html",
        ]:
            match = re.search(
                r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?'
                + re.escape(anchor)
                + r".*?</article>\s*)",
                scoped_text,
                flags=re.S,
            )
            if match:
                break
        if not match:
            cards = list(
                re.finditer(
                    r'<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?</article>\s*',
                    scoped_text,
                    flags=re.S,
                )
            )
            if not cards:
                raise RuntimeError(f"Could not find insertion point in {path}")
            insert_pos = scope_start + cards[-1].end()
        else:
            insert_pos = scope_start + match.end()
        text = text[:insert_pos] + "\n" + card + text[insert_pos:]
    text = UPDATE_ITEM_LIST_JSON(text, lang)
    path.write_text(text, encoding="utf-8")


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    copy = copy_for("en")
    entry = {
        "id": PRODUCT_ID,
        "name": copy["name"],
        "category": "RO Water Machine",
        "desc": copy["card"],
        "specs": dict(zip(copy["labels"], copy["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": copy["intro"],
        "features": [
            "400G-800G front-panel 10-inch frame RO water machine for municipal tap water",
            "10-inch PP, 10-inch UDF, 10-inch PP, 3012 RO membrane and T33 post-carbon stages",
            "Microcomputer control with full automatic intelligent operation",
            "Front-panel frame layout for commercial drinking water and distributor projects",
            "OEM/ODM color, logo, label, packaging and configuration support",
        ],
        "applications": "Municipal tap-water purification for offices, cafés, retail stores, schools, distributors and OEM private-label front-panel RO machine projects.",
        "related": [
            "10-inch-frame-ro-water-machine-400g-800g",
            "thickened-stainless-steel-10-inch-frame-ro-water-machine-400g-800g",
            "10-inch-frame-ro-water-machine-400g-1200g",
            "commercial-big-blue-ro-water-purifier-400g-800g",
        ],
    }
    for index, item in enumerate(products):
        if item.get("id") == PRODUCT_ID:
            products[index] = entry
            break
    else:
        insert_at = next(
            (
                i + 1
                for i, item in enumerate(products)
                if item.get("id") == "10-inch-frame-ro-water-machine-400g-800g"
            ),
            10,
        )
        products.insert(insert_at, entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Front Panel 10-Inch Frame RO Water Machine 400G-800G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def extract_target_card_copy(lang: str, slug: str) -> tuple[str, str, str] | None:
    path = ROOT / lang / slug
    if not path.exists():
        return None
    text = path.read_text(encoding="utf-8")
    h1 = re.search(r"<h1>(.*?)</h1>", text, flags=re.S)
    desc = re.search(r'<p class="desc">(.*?)</p>', text, flags=re.S)
    cat = re.search(r'<span class="cat-badge">(.*?)</span>', text, flags=re.S)
    if not h1 or not desc:
        return None

    def clean(fragment: str) -> str:
        fragment = re.sub(r"<[^>]+>", " ", fragment)
        fragment = html_lib.unescape(fragment)
        return re.sub(r"\s+", " ", fragment).strip()

    title = clean(h1.group(1))
    body = clean(desc.group(1))
    category = clean(cat.group(1)) if cat else title
    return title, body, category


def fix_related_cards(lang: str) -> None:
    path = ROOT / lang / NEW_SLUG
    text = path.read_text(encoding="utf-8")

    def replace_card(match: re.Match) -> str:
        article = match.group(0)
        href = re.search(r'href="([^"]+\.html)"', article)
        if not href or href.group(1) == NEW_SLUG:
            return article
        card_copy = extract_target_card_copy(lang, href.group(1))
        if not card_copy:
            return article
        title, body, category = [html_lib.escape(part, quote=True) for part in card_copy]
        article = re.sub(r'data-cat="[^"]*"', f'data-cat="{category}"', article, count=1)
        article = re.sub(
            r'<span class="product-cat-badge">.*?</span>',
            f'<span class="product-cat-badge">{category}</span>',
            article,
            count=1,
            flags=re.S,
        )
        article = re.sub(r'alt="[^"]*"', f'alt="{title}"', article, count=1)
        article = re.sub(r"<h3>.*?</h3>", f"<h3>{title}</h3>", article, count=1, flags=re.S)
        article = re.sub(r"<p>.*?</p>", f"<p>{body}</p>", article, count=1, flags=re.S)
        return article

    updated = re.sub(r'<article class="product-card"[\s\S]*?</article>', replace_card, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def main() -> None:
    languages = dirs()
    missing = [
        lang
        for lang in languages
        if lang not in PRODUCT_NAMES
        or lang not in FRONT_PANEL_MODIFIER
        or lang not in TEN_INCH
        or lang not in POST_CARBON
        or lang not in OPERATION_VALUES
        or lang not in FEED_WATER_VALUES
    ]
    if missing:
        raise RuntimeError(f"Missing translations: {', '.join(missing)}")
    DUAL_GLOBALS["dirs"] = dirs
    DUAL_GLOBALS["NEW_SLUG"] = NEW_SLUG
    DUAL_GLOBALS["PRODUCT_ID"] = PRODUCT_ID
    DUAL_GLOBALS["MAIN_IMAGE"] = MAIN_IMAGE
    DUAL_GLOBALS["IMAGE_WIDTH"] = IMAGE_WIDTH
    DUAL_GLOBALS["IMAGE_HEIGHT"] = IMAGE_HEIGHT
    DUAL_GLOBALS["AFTER_SLUG"] = AFTER_SLUG
    DUAL_GLOBALS["TODAY"] = TODAY
    DUAL_GLOBALS["copy_for"] = copy_for
    DUAL_GLOBALS["build_main"] = build_main
    DUAL_GLOBALS["product_graph"] = product_graph
    DUAL_GLOBALS["update_products_page"] = update_products_page
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()
    for lang in languages:
        fix_related_cards(lang)


if __name__ == "__main__":
    main()
