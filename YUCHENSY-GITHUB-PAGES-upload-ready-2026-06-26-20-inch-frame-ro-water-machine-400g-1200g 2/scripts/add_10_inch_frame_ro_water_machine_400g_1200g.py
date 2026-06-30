#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add 10-inch frame RO water machine 400G-1200G across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_commercial_big_blue_ro_water_purifier_400g_800g.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["BASE_COPY_FOR"]
BASE_BUILD_MAIN = BASE["BASE_BUILD_MAIN"]
BASE_PRODUCT_GRAPH = BASE["BASE_PRODUCT_GRAPH"]
OPERATION_VALUES = BASE["OPERATION_VALUES"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-10-inch-frame-ro-water-machine-400g-1200g.html"
PRODUCT_ID = "10-inch-frame-ro-water-machine-400g-1200g"
MAIN_IMAGE = "10-inch-frame-ro-water-machine-400g-1200g-oem.webp"
IMAGE_WIDTH = 374
IMAGE_HEIGHT = 462
AFTER_SLUG = "product-commercial-big-blue-ro-water-purifier-400g-800g.html"
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
    "af": "10-duim raam-RO-watermasjien",
    "ar": "آلة مياه RO بإطار 10 بوصات",
    "az": "10 düymlük çərçivəli RO su maşını",
    "bg": "10-инчова рамкова RO машина за вода",
    "bn": "১০ ইঞ্চি ফ্রেম RO পানি মেশিন",
    "bs": "10-inčna okvirna RO mašina za vodu",
    "cs": "10palcový rámový RO vodní stroj",
    "da": "10-tommer rammebaseret RO-vandmaskine",
    "de": "10-Zoll-Rahmen-RO-Wassermaschine",
    "el": "Μηχάνημα νερού RO με πλαίσιο 10 ιντσών",
    "en": "10-Inch Frame RO Water Machine",
    "es": "Máquina de agua RO con bastidor de 10 pulgadas",
    "et": "10-tolline raamiga RO veemasin",
    "fa": "دستگاه آب RO فریم‌دار 10 اینچ",
    "fi": "10 tuuman runkorakenteinen RO-vesikone",
    "fr": "Machine à eau RO à châssis 10 pouces",
    "ha": "Na'urar ruwan RO mai firam inci 10",
    "he": "מכונת מים RO עם מסגרת 10 אינץ׳",
    "hi": "10 इंच फ्रेम RO वॉटर मशीन",
    "hr": "10-inčni okvirni RO uređaj za vodu",
    "hu": "10 hüvelykes keretes RO vízgép",
    "hy": "10 դյույմանոց շրջանակով RO ջրի սարք",
    "id": "Mesin air RO rangka 10 inci",
    "it": "Macchina per acqua RO con telaio da 10 pollici",
    "ja": "10インチフレームRO浄水機",
    "ka": "10-დუიმიანი ჩარჩოს RO წყლის აპარატი",
    "kk": "10 дюймдік рамалы RO су машинасы",
    "ko": "10인치 프레임 RO 정수기",
    "ku": "Makîneya ava RO bi çarçoveya 10 înç",
    "ky": "10 дюймдук рамалуу RO суу аппараты",
    "lt": "10 colių rėminė RO vandens mašina",
    "lv": "10 collu rāmja RO ūdens iekārta",
    "ms": "Mesin air RO rangka 10 inci",
    "nl": "10-inch frame RO-watermachine",
    "no": "10-tommers rammebasert RO-vannmaskin",
    "pl": "10-calowa ramowa maszyna do wody RO",
    "pt": "Máquina de água RO com estrutura de 10 polegadas",
    "ro": "Mașină de apă RO cu cadru de 10 inch",
    "ru": "RO-машина для воды на 10-дюймовой раме",
    "sk": "10-palcový rámový RO vodný stroj",
    "sl": "10-palčni okvirni RO vodni aparat",
    "sq": "Makineri uji RO me kornizë 10 inç",
    "sr": "10-инчна рамска RO машина за воду",
    "sr-me": "10-inčna ramovska RO mašina za vodu",
    "sv": "10-tums rambaserad RO-vattenmaskin",
    "sw": "Mashine ya maji ya RO yenye fremu ya inchi 10",
    "ta": "10 அங்குல சட்டக RO நீர் இயந்திரம்",
    "tg": "Мошини оби RO бо чорчӯбаи 10-дюймӣ",
    "th": "เครื่องน้ำ RO แบบโครง 10 นิ้ว",
    "tk": "10 dýuým karkasly RO suw enjamy",
    "tl": "10-pulgadang frame RO water machine",
    "tr": "10 inç şasili RO su makinesi",
    "uk": "RO-машина для води на 10-дюймовій рамі",
    "ur": "10 انچ فریم والا RO واٹر مشین",
    "uz": "10 dyuymli ramali RO suv mashinasi",
    "vi": "Máy nước RO khung 10 inch",
    "zu": "Umshini wamanzi we-RO onohlaka lwama-intshi angu-10",
}


TEN_INCH = {
    "af": "10-duim",
    "ar": "10 بوصات",
    "az": "10 düymlük",
    "bg": "10-инчов",
    "bn": "১০ ইঞ্চি",
    "bs": "10-inčni",
    "cs": "10palcový",
    "da": "10-tommer",
    "de": "10-Zoll",
    "el": "10 ιντσών",
    "en": "10-inch",
    "es": "10 pulgadas",
    "et": "10-tolline",
    "fa": "10 اینچ",
    "fi": "10 tuuman",
    "fr": "10 pouces",
    "ha": "inci 10",
    "he": "10 אינץ׳",
    "hi": "10 इंच",
    "hr": "10-inčni",
    "hu": "10 hüvelykes",
    "hy": "10 դյույմանոց",
    "id": "10 inci",
    "it": "10 pollici",
    "ja": "10インチ",
    "ka": "10-დუიმიანი",
    "kk": "10 дюймдік",
    "ko": "10인치",
    "ku": "10 înç",
    "ky": "10 дюймдук",
    "lt": "10 colių",
    "lv": "10 collu",
    "ms": "10 inci",
    "nl": "10-inch",
    "no": "10-tommers",
    "pl": "10-calowy",
    "pt": "10 polegadas",
    "ro": "10 inch",
    "ru": "10-дюймовый",
    "sk": "10-palcový",
    "sl": "10-palčni",
    "sq": "10 inç",
    "sr": "10-инчни",
    "sr-me": "10-inčni",
    "sv": "10-tums",
    "sw": "inchi 10",
    "ta": "10 அங்குல",
    "tg": "10-дюймӣ",
    "th": "10 นิ้ว",
    "tk": "10 dýuým",
    "tl": "10-pulgada",
    "tr": "10 inç",
    "uk": "10-дюймовий",
    "ur": "10 انچ",
    "uz": "10 dyuymli",
    "vi": "10 inch",
    "zu": "ama-intshi angu-10",
}


POST_CARBON = {
    "af": "nakoolstof",
    "ar": "كربون لاحق",
    "az": "son karbon",
    "bg": "последващ въглен",
    "bn": "পরবর্তী কার্বন",
    "bs": "završni ugljen",
    "cs": "dočišťovací uhlík",
    "da": "efterkul",
    "de": "Nachkohle",
    "el": "τελικό ανθρακικό φίλτρο",
    "en": "post carbon",
    "es": "post-carbón",
    "et": "järelaktiivsüsi",
    "fa": "کربن نهایی",
    "fi": "jälkihiili",
    "fr": "post-carbone",
    "ha": "carbon na ƙarshe",
    "he": "פחם סופי",
    "hi": "पोस्ट कार्बन",
    "hr": "završni ugljen",
    "hu": "utószén",
    "hy": "վերջնական ածխածին",
    "id": "karbon akhir",
    "it": "post-carbone",
    "ja": "後置カーボン",
    "ka": "საბოლოო ნახშირბადი",
    "kk": "соңғы көмір сүзгісі",
    "ko": "후단 카본",
    "ku": "karbona dawîn",
    "ky": "акыркы көмүр",
    "lt": "baigiamasis anglies filtras",
    "lv": "pēckarbona filtrs",
    "ms": "karbon akhir",
    "nl": "nakoolstof",
    "no": "etterkarbon",
    "pl": "węgiel końcowy",
    "pt": "pós-carvão",
    "ro": "carbon final",
    "ru": "постугольный фильтр",
    "sk": "dočisťovací uhlík",
    "sl": "zaključni ogljik",
    "sq": "karbon përfundimtar",
    "sr": "завршни угљеник",
    "sr-me": "završni ugljenik",
    "sv": "efterkol",
    "sw": "kaboni ya mwisho",
    "ta": "இறுதி கார்பன்",
    "tg": "карбони ниҳоӣ",
    "th": "คาร์บอนขั้นสุดท้าย",
    "tk": "soňky karbon",
    "tl": "panghuling carbon",
    "tr": "son karbon",
    "uk": "поствугільний фільтр",
    "ur": "آخری کاربن",
    "uz": "yakuniy karbon",
    "vi": "than hoạt tính sau lọc",
    "zu": "ikhabhoni yokugcina",
}


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def treatment_value(lang: str) -> str:
    ten = TEN_INCH[lang]
    post = POST_CARBON[lang]
    return f"{ten} PP + {ten} UDF + {ten} PP + RO + T33 {post}"


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if (
        lang not in PRODUCT_NAMES
        or lang not in TEN_INCH
        or lang not in POST_CARBON
        or lang not in OPERATION_VALUES
        or lang not in FEED_WATER_VALUES
    ):
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 400G-1200G"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = treatment_value(lang)
    values[3] = "400G-1200G"
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
            "product-commercial-big-blue-ro-water-purifier-400g-800g.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "commercial-big-blue-ro-water-purifier-400g-800g"),
        10,
    )
    products.insert(insert_at, {
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
            "400G-1200G open-frame RO water machine for municipal tap water",
            "10-inch PP, 10-inch UDF, 10-inch PP, RO membrane and T33 post-carbon stages",
            "Microcomputer control with full automatic intelligent operation",
            "Frame structure for commercial drinking water and OEM distributor projects",
            "OEM/ODM label, color, packaging and configuration options",
        ],
        "applications": "Commercial direct drinking water for offices, cafés, restaurants, stores, schools, distributors and OEM private-label municipal tap-water projects.",
        "related": [
            "commercial-big-blue-ro-water-purifier-400g-800g",
            "portable-custom-ro-water-purifier-400g-800g",
            "desktop-ro-water-machine-compressor-cooling-100g",
            "built-in-pressure-tank-ro",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- 10-Inch Frame RO Water Machine 400G-1200G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
