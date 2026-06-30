#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add commercial small-cabinet RO purifier across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
MID = runpy.run_path(str(ROOT / "scripts" / "add_commercial_mid_cabinet_ro_purifier_built_in_pressure_tank.py"))

DUAL_GLOBALS = MID["DUAL_GLOBALS"]
BASE_COPY_FOR = MID["BASE_COPY_FOR"]
BASE_BUILD_MAIN = MID["BASE_BUILD_MAIN"]
BASE_PRODUCT_GRAPH = MID["BASE_PRODUCT_GRAPH"]
FEED_WATER_VALUES = MID["FEED_WATER_VALUES"]
OPERATION_VALUES = MID["OPERATION_VALUES"]
CENTRAL_TREATMENT_VALUES = MID["CENTRAL_TREATMENT_VALUES"]
SIZE_LABELS = MID["SIZE_LABELS"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-commercial-small-cabinet-ro-water-purifier-400g-1600g.html"
PRODUCT_ID = "commercial-small-cabinet-ro-water-purifier-400g-1600g"
MAIN_IMAGE = "commercial-small-cabinet-ro-water-purifier-400g-1600g-oem.webp"
IMAGE_WIDTH = 360
IMAGE_HEIGHT = 482
AFTER_SLUG = "product-commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g.html"
TODAY = "2026-06-25"
BRAND = "Yuchen Water"


def dirs() -> list[str]:
    return sorted(
        p.name
        for p in ROOT.iterdir()
        if p.is_dir()
        and (p / "index.html").exists()
        and re.fullmatch(r"[a-z]{2}(?:-[a-z]{2})?", p.name)
    )


PRODUCT_NAMES = {
    "af": "Kommersiële kleinkas RO-waterreiniger",
    "ar": "جهاز تنقية مياه RO تجاري بخزانة صغيرة",
    "az": "Kommersiya kiçik şkaflı RO su təmizləyicisi",
    "bg": "Търговски RO водопречиствател малък шкаф",
    "bn": "বাণিজ্যিক ছোট ক্যাবিনেট RO পানি বিশুদ্ধকরণ মেশিন",
    "bs": "Komercijalni RO prečistač vode u malom kabinetu",
    "cs": "Komerční RO čistička vody v malé skříni",
    "da": "Kommerciel RO-vandrenser i lille kabinet",
    "de": "Gewerblicher RO-Wasserreiniger im Kleinschrank",
    "el": "Επαγγελματικός καθαριστής νερού RO μικρού ερμαρίου",
    "en": "Commercial Small-Cabinet RO Water Purifier",
    "es": "Purificador de agua RO comercial de gabinete pequeño",
    "et": "Kaubanduslik väikese kapiga RO veepuhasti",
    "fa": "دستگاه تصفیه آب RO تجاری کابینت کوچک",
    "fi": "Kaupallinen pienkaappinen RO-vedenpuhdistin",
    "fr": "Purificateur d’eau RO commercial à petite armoire",
    "ha": "Na'urar tace ruwan RO ta kasuwanci a ƙaramin kabad",
    "he": "מטהר מים RO מסחרי בארון קטן",
    "hi": "वाणिज्यिक छोटे कैबिनेट RO जल शोधक",
    "hr": "Komercijalni RO pročišćivač vode u malom ormariću",
    "hu": "Kereskedelmi kis szekrényes RO víztisztító",
    "hy": "Առևտրային փոքր պահարանով RO ջրի մաքրիչ",
    "id": "Pemurni air RO komersial kabinet kecil",
    "it": "Purificatore d’acqua RO commerciale a mobile piccolo",
    "ja": "業務用小型キャビネットRO浄水機",
    "ka": "კომერციული მცირე კაბინეტის RO წყლის გამწმენდი",
    "kk": "Коммерциялық шағын шкафты RO су тазартқышы",
    "ko": "상업용 소형 캐비닛 RO 정수기",
    "ku": "Paqijkera ava RO ya bazirganî ya kabîneya biçûk",
    "ky": "Коммерциялык чакан шкафтуу RO суу тазалагыч",
    "lt": "Komercinis mažos spintos RO vandens valytuvas",
    "lv": "Komerciāls maza skapja RO ūdens attīrītājs",
    "ms": "Penulen air RO komersial kabinet kecil",
    "nl": "Commerciële kleine kast RO-waterzuiveraar",
    "no": "Kommersiell liten skap RO-vannrenser",
    "pl": "Komercyjny mały szafkowy oczyszczacz wody RO",
    "pt": "Purificador de água RO comercial de gabinete pequeno",
    "ro": "Purificator de apă RO comercial cu dulap mic",
    "ru": "Коммерческий RO-очиститель воды в малом шкафу",
    "sk": "Komerčný RO čistič vody v malej skrini",
    "sl": "Komercialni RO čistilnik vode v majhni omari",
    "sq": "Pastrues uji RO komercial me kabinet të vogël",
    "sr": "Комерцијални RO пречистач воде у малом ормару",
    "sr-me": "Komercijalni RO prečišćivač vode u malom ormaru",
    "sv": "Kommersiell RO-vattenrenare i litet skåp",
    "sw": "Kisafishaji maji cha RO cha biashara cha kabati ndogo",
    "ta": "வணிக சிறிய கேபினெட் RO நீர் சுத்திகரிப்பான்",
    "tg": "Тозакунандаи оби RO-и тиҷоратии ҷевони хурд",
    "th": "เครื่องกรองน้ำ RO เชิงพาณิชย์แบบตู้เล็ก",
    "tk": "Täjirçilik kiçi şkafly RO suw arassalaýjy",
    "tl": "Komersiyal na RO water purifier sa maliit na kabinet",
    "tr": "Ticari küçük kabin RO su arıtma cihazı",
    "uk": "Комерційний RO-очисник води в малій шафі",
    "ur": "تجارتی چھوٹی کابینہ والا RO پانی صاف کرنے والا آلہ",
    "uz": "Tijorat kichik shkafli RO suv tozalagichi",
    "vi": "Máy lọc nước RO tủ nhỏ thương mại",
    "zu": "Umshini we-RO wokuhlanza amanzi webhizinisi wekhabhinethi encane",
}


def treatment_value(lang: str) -> str:
    return f"{CENTRAL_TREATMENT_VALUES[lang]} + T33"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in PRODUCT_NAMES or lang not in SIZE_LABELS:
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 400G-1600G"
    labels = base["labels"][:]
    values = base["values"][:]
    size_label = SIZE_LABELS[lang]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = treatment_value(lang)
    values[3] = "400G-1600G"
    values[4] = FEED_WATER_VALUES[lang]
    values[5] = "0.1-0.4 MPa"
    labels.insert(7, size_label)
    values.insert(7, "55*35*96 cm")
    intro = (
        f"{name}. {labels[1]}: {values[1]}. "
        f"{labels[2]}: {values[2]}. {labels[3]}: {values[3]}. "
        f"{labels[4]}: {values[4]}. {labels[5]}: {values[5]}. "
        f"{size_label}: 55*35*96 cm. {labels[8]}: {values[8]}."
    )
    card = f"{PRODUCT_NAMES[lang]}: {values[2]}; {values[3]}; {values[4]}; 55*35*96 cm."
    copy = {
        **base,
        "name": name,
        "category": PRODUCT_NAMES[lang],
        "intro": intro,
        "card": card,
        "labels": labels,
        "values": values,
    }
    copy["title"] = f"{name} | {BRAND}"
    meta_text = f"{name}. {values[3]}; {values[4]}; {size_label}: 55*35*96 cm."
    copy["meta"] = clean_meta(meta_text)
    copy["quote"] = f"{copy['request']}: {name}"
    copy["quote_desc"] = intro
    copy["faq_pairs"] = [
        (f"{labels[1]}?", values[1]),
        (f"{labels[2]}?", values[2]),
        (f"{labels[3]}?", values[3]),
        (f"{labels[4]}?", values[4]),
        (f"{labels[5]}?", values[5]),
        (f"{size_label}?", "55*35*96 cm"),
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
    existing_card = re.search(
        r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?'
        + re.escape(NEW_SLUG)
        + r'.*?</article>\s*)',
        text,
        flags=re.S,
    )
    if existing_card:
        text = text[:existing_card.start()] + card + text[existing_card.end():]
    else:
        match = None
        for anchor in [
            AFTER_SLUG,
            "product-commercial-central-ro-water-purification-equipment-250-500lph.html",
            "product-commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g.html",
            "product-portable-custom-ro-water-purifier-400g-800g.html",
        ]:
            match = re.search(
                r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?'
                + re.escape(anchor)
                + r'.*?</article>\s*)',
                text,
                flags=re.S,
            )
            if match:
                break
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + card + text[match.end():]
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g"),
        10,
    )
    products.insert(insert_at, {
        "id": PRODUCT_ID,
        "name": copy["name"],
        "category": "RO Water Purifier",
        "desc": copy["card"],
        "specs": dict(zip(copy["labels"], copy["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": copy["intro"],
        "features": [
            "Commercial small-cabinet RO purifier for direct drinking water",
            "20-inch PP, 20-inch CTO, 20-inch PP, RO and T33 filtration",
            "400G-1600G purified water flow range",
            "Microcomputer control for automatic intelligent operation",
            "Compact 55*35*96 cm cabinet with OEM/ODM logo and color options",
        ],
        "applications": "Commercial small-cabinet RO water purifier for offices, stores, tea shops, restaurants, municipal tap water projects and B2B private-label distribution.",
        "related": [
            "commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g",
            "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g",
            "portable-custom-ro-water-purifier-400g-800g",
            "built-in-pressure-tank-ro",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Commercial Small-Cabinet RO Water Purifier 400G-1600G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
    languages = dirs()
    missing = [
        lang for lang in languages
        if lang not in PRODUCT_NAMES
        or lang not in SIZE_LABELS
        or lang not in OPERATION_VALUES
        or lang not in CENTRAL_TREATMENT_VALUES
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
