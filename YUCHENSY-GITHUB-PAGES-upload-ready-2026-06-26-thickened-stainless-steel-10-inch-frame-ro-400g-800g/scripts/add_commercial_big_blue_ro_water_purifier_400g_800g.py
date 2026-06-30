#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add commercial Big Blue RO water purifier 400G-800G across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_portable_custom_ro_water_purifier_400g_800g.py"))
BIG_PP_BASE = runpy.run_path(str(ROOT / "scripts" / "add_single_tank_big_blue_pp_ro_equipment_250_500lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["BASE_COPY_FOR"]
BASE_BUILD_MAIN = BASE["BASE_BUILD_MAIN"]
BASE_PRODUCT_GRAPH = BASE["BASE_PRODUCT_GRAPH"]
OPERATION_VALUES = BASE["OPERATION_VALUES"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
BIG_PP_TREATMENT_VALUES = BIG_PP_BASE["TREATMENT_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-commercial-big-blue-ro-water-purifier-400g-800g.html"
PRODUCT_ID = "commercial-big-blue-ro-water-purifier-400g-800g"
MAIN_IMAGE = "commercial-big-blue-ro-water-purifier-400g-800g-oem.webp"
IMAGE_WIDTH = 412
IMAGE_HEIGHT = 476
AFTER_SLUG = "product-commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g.html"
TODAY = "2026-06-26"
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
    "af": "Kommersiële grootdeursnee RO-waterreiniger",
    "ar": "جهاز تنقية مياه RO تجاري بقارورة كبيرة",
    "az": "Ticarət üçün böyük korpuslu RO su təmizləyicisi",
    "bg": "Търговски RO водопречиствател с голяма колба",
    "bn": "বাণিজ্যিক বড় হাউজিং RO পানি বিশুদ্ধকরণ মেশিন",
    "bs": "Komercijalni RO prečistač vode s velikim kućištem",
    "cs": "Komerční RO čistička vody s velkým pouzdrem",
    "da": "Kommerciel RO-vandrenser med stort filterhus",
    "de": "Gewerblicher RO-Wasserreiniger mit großem Filtergehäuse",
    "el": "Επαγγελματικός καθαριστής νερού RO με μεγάλο περίβλημα",
    "en": "Commercial Big Blue RO Water Purifier",
    "es": "Purificador de agua RO comercial con carcasa grande",
    "et": "Kaubanduslik suure korpusega RO veepuhasti",
    "fa": "دستگاه تصفیه آب RO تجاری با هوزینگ بزرگ",
    "fi": "Kaupallinen RO-vedenpuhdistin suurella suodatinkotelolla",
    "fr": "Purificateur d’eau RO commercial avec grand boîtier",
    "ha": "Na'urar tace ruwan RO ta kasuwanci mai babban gida",
    "he": "מטהר מים RO מסחרי עם בית מסנן גדול",
    "hi": "वाणिज्यिक बड़े हाउसिंग वाला RO जल शोधक",
    "hr": "Komercijalni RO pročišćivač vode s velikim kućištem",
    "hu": "Kereskedelmi RO víztisztító nagy szűrőházzal",
    "hy": "Առևտրային RO ջրի մաքրիչ մեծ ֆիլտրային պատյանով",
    "id": "Pemurni air RO komersial dengan housing besar",
    "it": "Purificatore d’acqua RO commerciale con grande alloggiamento",
    "ja": "商業用大型ハウジングRO浄水機",
    "ka": "კომერციული RO წყლის გამწმენდი დიდი კორპუსით",
    "kk": "Коммерциялық үлкен корпусты RO су тазартқышы",
    "ko": "상업용 대형 하우징 RO 정수기",
    "ku": "Paqijkera ava RO ya bazirganî bi mala mezin",
    "ky": "Коммерциялык чоң корпустуу RO суу тазалагыч",
    "lt": "Komercinis RO vandens valytuvas su dideliu korpusu",
    "lv": "Komerciāls RO ūdens attīrītājs ar lielu korpusu",
    "ms": "Penulen air RO komersial dengan perumah besar",
    "nl": "Commerciële RO-waterzuiveraar met grote behuizing",
    "no": "Kommersiell RO-vannrenser med stort filterhus",
    "pl": "Komercyjny oczyszczacz wody RO z dużą obudową",
    "pt": "Purificador de água RO comercial com carcaça grande",
    "ro": "Purificator de apă RO comercial cu carcasă mare",
    "ru": "Коммерческий RO-очиститель воды с большой колбой",
    "sk": "Komerčný RO čistič vody s veľkým puzdrom",
    "sl": "Komercialni RO čistilnik vode z velikim ohišjem",
    "sq": "Pastrues uji RO komercial me strehim të madh",
    "sr": "Комерцијални RO пречистач воде са великим кућиштем",
    "sr-me": "Komercijalni RO prečišćivač vode sa velikim kućištem",
    "sv": "Kommersiell RO-vattenrenare med stort filterhus",
    "sw": "Kisafishaji maji cha RO cha biashara chenye kasha kubwa",
    "ta": "வணிக பெரிய ஹவுசிங் RO நீர் சுத்திகரிப்பான்",
    "tg": "Тозакунандаи оби RO-и тиҷоратӣ бо корпуси калон",
    "th": "เครื่องกรองน้ำ RO เชิงพาณิชย์พร้อมกระบอกกรองขนาดใหญ่",
    "tk": "Uly korpusly täjirçilik RO suw arassalaýjy",
    "tl": "Komersiyal na RO water purifier na may malaking housing",
    "tr": "Büyük gövdeli ticari RO su arıtma cihazı",
    "uk": "Комерційний RO-очисник води з великою колбою",
    "ur": "تجارتی بڑے ہاؤسنگ والا RO واٹر پیوریفائر",
    "uz": "Katta korpusli tijorat RO suv tozalagichi",
    "vi": "Máy lọc nước RO thương mại với cốc lọc lớn",
    "zu": "Umshini wokuhlanza amanzi we-RO webhizinisi onezindlu ezinkulu",
}


def treatment_value(lang: str) -> str:
    value = BIG_PP_TREATMENT_VALUES[lang]
    value = value.replace("20", "10").replace("بیست", "ده")
    if value.endswith(" + RO"):
        value = value[:-5]
    return f"{value} + RO + T33"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if (
        lang not in PRODUCT_NAMES
        or lang not in OPERATION_VALUES
        or lang not in BIG_PP_TREATMENT_VALUES
        or lang not in FEED_WATER_VALUES
    ):
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 400G-800G"
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
    card = f"{PRODUCT_NAMES[lang]}: {values[2]}; {values[3]}; {values[4]}."
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
            "product-portable-custom-ro-water-purifier-400g-800g.html",
            "product-desktop-ro-water-machine-compressor-cooling-100g.html",
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
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = copy_for("en")
    insert_at = next(
        (i + 1 for i, item in enumerate(products) if item.get("id") == "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g"),
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
            "400G-800G commercial RO water purifier for municipal tap water",
            "10-inch Big Blue PP prefilter, RO membrane and T33 post-carbon polishing",
            "Microcomputer control with automatic intelligent operation",
            "Compact open-frame structure for commercial drinking water projects",
            "OEM/ODM label, color, packaging and configuration options",
        ],
        "applications": "Commercial direct drinking water for offices, cafés, restaurants, stores, schools, distributors and OEM private-label municipal tap-water projects.",
        "related": [
            "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g",
            "portable-custom-ro-water-purifier-400g-800g",
            "desktop-ro-water-machine-compressor-cooling-100g",
            "built-in-pressure-tank-ro",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Commercial Big Blue RO Water Purifier 400G-800G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        or lang not in OPERATION_VALUES
        or lang not in BIG_PP_TREATMENT_VALUES
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
