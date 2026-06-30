#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add simple type RO water purification equipment across all languages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_precision_filter_ro_equipment_250_1000lph.py"))
COMMERCIAL = runpy.run_path(str(ROOT / "scripts" / "add_commercial_central_ro_equipment_250_500lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
TREATMENT_VALUES = COMMERCIAL["TREATMENT_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-simple-type-reverse-osmosis-water-purification-equipment-250-1000lph.html"
PRODUCT_ID = "simple-type-reverse-osmosis-water-purification-equipment-250-1000lph"
MAIN_IMAGE = "simple-type-reverse-osmosis-water-purification-equipment-250l-1000l-oem.webp"
IMAGE_WIDTH = 376
IMAGE_HEIGHT = 654
AFTER_SLUG = "product-precision-filter-ro-water-purification-equipment-250-1000lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Eenvoudige tipe RO-water suiweringstoerusting",
    "ar": "معدات RO بسيطة لتنقية المياه",
    "az": "Sadə tip RO su təmizləmə avadanlığı",
    "bg": "Опростено RO оборудване за пречистване на вода",
    "bn": "সহজ ধরন RO পানি বিশুদ্ধকরণ সরঞ্জাম",
    "bs": "Jednostavna RO oprema za prečišćavanje vode",
    "cs": "Jednoduché RO zařízení na úpravu vody",
    "da": "Enkelt RO-vandrensningsanlæg",
    "de": "Einfache RO-Wasseraufbereitungsanlage",
    "el": "Απλός εξοπλισμός RO για καθαρισμό νερού",
    "en": "Simple Type Reverse Osmosis Water Purification Equipment",
    "es": "Equipo RO sencillo para purificación de agua",
    "et": "Lihtsat tüüpi RO veepuhastusseade",
    "fa": "دستگاه ساده RO برای تصفیه آب",
    "fi": "Yksinkertainen RO-vedenpuhdistuslaitteisto",
    "fr": "Équipement RO simple de purification d’eau",
    "ha": "Na'urar RO mai sauƙi ta tace ruwa",
    "he": "ציוד RO פשוט לטיהור מים",
    "hi": "सरल प्रकार RO जल शुद्धिकरण उपकरण",
    "hr": "Jednostavna RO oprema za pročišćavanje vode",
    "hu": "Egyszerű kivitelű RO víztisztító berendezés",
    "hy": "Պարզ տիպի RO ջրի մաքրման սարքավորում",
    "id": "Peralatan RO sederhana untuk pemurnian air",
    "it": "Impianto RO semplice per purificazione dell'acqua",
    "ja": "簡易型RO浄水装置",
    "ka": "მარტივი ტიპის RO წყლის გამწმენდი მოწყობილობა",
    "kk": "Қарапайым типті RO су тазарту жабдығы",
    "ko": "간편형 RO 정수 장비",
    "ku": "Amûra RO ya hêsan ji bo paqijkirina avê",
    "ky": "Жөнөкөй типтеги RO суу тазалоо жабдыгы",
    "lt": "Paprasto tipo RO vandens valymo įranga",
    "lv": "Vienkārša tipa RO ūdens attīrīšanas iekārta",
    "ms": "Peralatan RO jenis ringkas untuk penulenan air",
    "nl": "Eenvoudige RO-waterzuiveringsinstallatie",
    "no": "Enkelt RO-vannrenseanlegg",
    "pl": "Proste urządzenie RO do uzdatniania wody",
    "pt": "Equipamento RO simples de purificação de água",
    "ro": "Echipament RO simplu pentru purificarea apei",
    "ru": "RO-оборудование простой комплектации для очистки воды",
    "sk": "Jednoduché RO zariadenie na úpravu vody",
    "sl": "Enostavna RO oprema za čiščenje vode",
    "sq": "Pajisje RO e thjeshtë për pastrimin e ujit",
    "sr": "RO опрема једноставне изведбе за пречишћавање воде",
    "sr-me": "RO oprema jednostavne izvedbe za prečišćavanje vode",
    "sv": "Enkel RO-vattenreningsutrustning",
    "sw": "Kifaa rahisi cha RO cha kusafisha maji",
    "ta": "எளிய வகை RO நீர் சுத்திகரிப்பு உபகரணம்",
    "tg": "Таҷҳизоти соддаи RO барои тозакунии об",
    "th": "อุปกรณ์ RO แบบง่ายสำหรับกรองน้ำ",
    "tk": "Ýönekeý görnüşli RO suw arassalaýjy enjam",
    "tl": "Simpleng uri ng kagamitang RO para sa paglilinis ng tubig",
    "tr": "Basit tip RO su arıtma ekipmanı",
    "uk": "RO обладнання простої комплектації для очищення води",
    "ur": "سادہ قسم RO پانی صاف کرنے کا سامان",
    "uz": "Oddiy turdagi RO suv tozalash uskunasi",
    "vi": "Thiết bị RO lọc nước kiểu đơn giản",
    "zu": "Imishini elula ye-RO yokuhlanza amanzi",
}


def flow_value(lang: str) -> str:
    return f"250-1000 {FLOW_UNITS.get(lang, FLOW_UNITS['en'])}"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in NAME_PREFIXES or lang not in TREATMENT_VALUES or lang not in FEED_WATER_VALUES:
        raise KeyError(f"No product translation for {lang}")
    name = f"{NAME_PREFIXES[lang]} {flow_value(lang)}"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[2] = TREATMENT_VALUES[lang]
    values[3] = flow_value(lang)
    values[4] = FEED_WATER_VALUES[lang]
    intro = (
        f"{name}. {labels[2]}: {values[2]}. "
        f"{labels[3]}: {values[3]}. {labels[4]}: {values[4]}. "
        f"{labels[5]}: {values[5]}. {labels[6]}: {values[6]}."
    )
    card = f"{NAME_PREFIXES[lang]}: {values[2]}; {values[3]}; {values[4]}."
    copy = {
        **base,
        "name": name,
        "category": NAME_PREFIXES[lang],
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
        (f"{labels[2]}?", values[2]),
        (f"{labels[3]}?", values[3]),
        (f"{labels[4]}?", values[4]),
        (f"{labels[5]}?", values[5]),
        (f"{labels[6]}?", values[6]),
    ]
    return copy


def build_main(lang: str, copy: dict) -> str:
    text = BASE_BUILD_MAIN(lang, copy)
    return text.replace(
        "Precision%20Filter%20RO%20Water%20Purification%20Equipment%20250-1000Lph",
        "Simple%20Type%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250-1000Lph",
    )


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(BASE_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}"]
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def update_products_page(lang: str) -> None:
    path = ROOT / lang / "products.html"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG not in text:
        match = None
        for anchor in [
            AFTER_SLUG,
            "product-single-tank-integrated-ro-water-purification-supply-equipment-250-500lph.html",
            "product-commercial-central-ro-water-purification-equipment-250-500lph.html",
            "product-slim-reverse-osmosis-water-purification-equipment-250-500lph.html",
        ]:
            match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(anchor) + r'.*?</article>\s*)', text, flags=re.S)
            if match:
                break
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + PRODUCT_CARD(lang) + text[match.end():]
    text = UPDATE_ITEM_LIST_JSON(text, lang)
    path.write_text(text, encoding="utf-8")


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = copy_for("en")
    insert_at = next(
        (i + 1 for i, item in enumerate(products) if item.get("id") == "precision-filter-ro-water-purification-equipment-250-1000lph"),
        10,
    )
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
            "20-inch PP, 20-inch CTO and 20-inch PP pretreatment before RO",
            "250-1000 L/h purified water flow",
            "Designed for municipal tap water",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Simple commercial RO purification for municipal tap water in offices, stores, schools, clinics, restaurants and drinking-water supply projects.",
        "related": [
            "precision-filter-ro-water-purification-equipment-250-1000lph",
            "commercial-central-ro-water-purification-equipment-250-500lph",
            "single-tank-integrated-ro-water-purification-supply-equipment-250-500lph",
            "slim-reverse-osmosis-water-purification-equipment-250-500lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Simple Type Reverse Osmosis Water Purification Equipment 250-1000 L/h: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        article = re.sub(r'<span class="product-cat-badge">.*?</span>', f'<span class="product-cat-badge">{category}</span>', article, count=1, flags=re.S)
        article = re.sub(r'alt="[^"]*"', f'alt="{title}"', article, count=1)
        article = re.sub(r"<h3>.*?</h3>", f"<h3>{title}</h3>", article, count=1, flags=re.S)
        article = re.sub(r"<p>.*?</p>", f"<p>{body}</p>", article, count=1, flags=re.S)
        return article

    updated = re.sub(r'<article class="product-card"[\s\S]*?</article>', replace_card, text)
    if updated != text:
        path.write_text(updated, encoding="utf-8")


def main() -> None:
    missing = [
        lang for lang in DUAL_GLOBALS["dirs"]()
        if lang not in NAME_PREFIXES or lang not in TREATMENT_VALUES or lang not in FEED_WATER_VALUES
    ]
    if missing:
        raise RuntimeError(f"Missing translations: {', '.join(missing)}")
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
    for lang in DUAL_GLOBALS["dirs"]():
        fix_related_cards(lang)


if __name__ == "__main__":
    main()
