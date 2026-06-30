#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add thickened stainless steel 10-inch frame RO water machine across languages."""

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
TEN_INCH = BASE["TEN_INCH"]
POST_CARBON = BASE["POST_CARBON"]
BASE_PRODUCT_NAMES = BASE["PRODUCT_NAMES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-thickened-stainless-steel-10-inch-frame-ro-water-machine-400g-800g.html"
PRODUCT_ID = "thickened-stainless-steel-10-inch-frame-ro-water-machine-400g-800g"
MAIN_IMAGE = "thickened-stainless-steel-10-inch-frame-ro-water-machine-400g-800g-oem.webp"
IMAGE_WIDTH = 404
IMAGE_HEIGHT = 520
AFTER_SLUG = "product-10-inch-frame-ro-water-machine-400g-1200g.html"
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


STAINLESS_MODIFIER = {
    "af": "met verdikte vlekvryestaalraam",
    "ar": "بإطار سميك من الفولاذ المقاوم للصدأ",
    "az": "qalınlaşdırılmış paslanmayan polad çərçivəli",
    "bg": "с подсилена рамка от неръждаема стомана",
    "bn": "পুরু স্টেইনলেস স্টিল ফ্রেমসহ",
    "bs": "s ojačanim okvirom od nehrđajućeg čelika",
    "cs": "se zesíleným rámem z nerezové oceli",
    "da": "med forstærket ramme i rustfrit stål",
    "de": "mit verstärktem Edelstahlrahmen",
    "el": "με ενισχυμένο ανοξείδωτο πλαίσιο",
    "en": "Thickened Stainless Steel",
    "es": "con bastidor reforzado de acero inoxidable",
    "et": "tugevdatud roostevabast terasest raamiga",
    "fa": "با فریم ضخیم از فولاد ضدزنگ",
    "fi": "vahvistetulla ruostumattomalla teräsrungolla",
    "fr": "avec châssis renforcé en acier inoxydable",
    "ha": "da firam na bakin karfe mai ƙarfi",
    "he": "עם מסגרת נירוסטה מחוזקת",
    "hi": "मोटे स्टेनलेस स्टील फ्रेम वाला",
    "hr": "s ojačanim okvirom od nehrđajućeg čelika",
    "hu": "megerősített rozsdamentes acél vázzal",
    "hy": "խտացված չժանգոտվող պողպատե շրջանակով",
    "id": "dengan rangka baja tahan karat tebal",
    "it": "con telaio rinforzato in acciaio inox",
    "ja": "加厚ステンレスフレーム仕様",
    "ka": "გასქელებული უჟანგავი ფოლადის ჩარჩოთი",
    "kk": "қалыңдатылған тот баспайтын болат рамамен",
    "ko": "두꺼운 스테인리스 스틸 프레임형",
    "ku": "bi çarçoveya pola zengarnegir a xurtkirî",
    "ky": "калыңдатылган дат баспас болот рамалуу",
    "lt": "su sustiprintu nerūdijančio plieno rėmu",
    "lv": "ar pastiprinātu nerūsējošā tērauda rāmi",
    "ms": "dengan rangka keluli tahan karat tebal",
    "nl": "met versterkt roestvrijstalen frame",
    "no": "med forsterket ramme i rustfritt stål",
    "pl": "ze wzmocnioną ramą ze stali nierdzewnej",
    "pt": "com estrutura reforçada de aço inoxidável",
    "ro": "cu cadru ranforsat din oțel inoxidabil",
    "ru": "с усиленной рамой из нержавеющей стали",
    "sk": "so zosilneným rámom z nehrdzavejúcej ocele",
    "sl": "z ojačanim okvirjem iz nerjavnega jekla",
    "sq": "me kornizë të përforcuar prej çeliku inox",
    "sr": "са ојачаним рамом од нерђајућег челика",
    "sr-me": "sa ojačanim ramom od nerđajućeg čelika",
    "sv": "med förstärkt ram i rostfritt stål",
    "sw": "yenye fremu imara ya chuma cha pua",
    "ta": "தடிமனான துருப்பிடிக்காத எஃகு சட்டகத்துடன்",
    "tg": "бо чорчӯбаи мустаҳками пӯлоди зангногир",
    "th": "พร้อมโครงสแตนเลสหนาพิเศษ",
    "tk": "galyňlaşdyrylan poslamaýan polat karkasly",
    "tl": "may makapal na stainless steel frame",
    "tr": "kalınlaştırılmış paslanmaz çelik şasili",
    "uk": "з посиленою рамою з нержавіючої сталі",
    "ur": "موٹے اسٹین لیس اسٹیل فریم کے ساتھ",
    "uz": "qalinlashtirilgan zanglamas po‘lat ramali",
    "vi": "với khung inox dày",
    "zu": "enohlaka oluqinisiwe lwensimbi engagqwali",
}


PRODUCT_NAME_OVERRIDES = {
    "af": "10-duim RO-watermasjien met verdikte vlekvryestaalraam",
    "ar": "آلة مياه RO بإطار سميك من الفولاذ المقاوم للصدأ مقاس 10 بوصات",
    "az": "Qalınlaşdırılmış paslanmayan polad 10 düymlük çərçivəli RO su maşını",
    "bg": "10-инчова RO машина за вода с подсилена рамка от неръждаема стомана",
    "bn": "পুরু স্টেইনলেস স্টিল ফ্রেমসহ ১০ ইঞ্চি RO পানি মেশিন",
    "bs": "10-inčna RO mašina za vodu s ojačanim okvirom od nehrđajućeg čelika",
    "cs": "10palcový rámový RO vodní stroj se zesílenou nerezovou konstrukcí",
    "da": "10-tommer RO-vandmaskine med forstærket rustfri stålramme",
    "de": "10-Zoll-RO-Wassermaschine mit verstärktem Edelstahlrahmen",
    "el": "Μηχάνημα νερού RO 10 ιντσών με ενισχυμένο ανοξείδωτο πλαίσιο",
    "en": "Thickened Stainless Steel 10-Inch Frame RO Water Machine",
    "es": "Máquina de agua RO de 10 pulgadas con bastidor reforzado de acero inoxidable",
    "et": "10-tolline RO veemasin tugevdatud roostevabast terasest raamiga",
    "fa": "دستگاه آب RO فریم‌دار 10 اینچ با فولاد ضدزنگ ضخیم",
    "fi": "10 tuuman RO-vesikone vahvistetulla ruostumattomalla teräsrungolla",
    "fr": "Machine à eau RO 10 pouces avec châssis renforcé en acier inoxydable",
    "ha": "Na'urar ruwan RO ta inci 10 da firam na bakin karfe mai ƙarfi",
    "he": "מכונת מים RO בגודל 10 אינץ׳ עם מסגרת נירוסטה מחוזקת",
    "hi": "मोटे स्टेनलेस स्टील फ्रेम वाली 10 इंच RO वॉटर मशीन",
    "hr": "10-inčni RO uređaj za vodu s ojačanim okvirom od nehrđajućeg čelika",
    "hu": "10 hüvelykes RO vízgép megerősített rozsdamentes acél vázzal",
    "hy": "10 դյույմանոց RO ջրի սարք խտացված չժանգոտվող պողպատե շրջանակով",
    "id": "Mesin air RO rangka 10 inci dengan baja tahan karat tebal",
    "it": "Macchina per acqua RO da 10 pollici con telaio rinforzato in acciaio inox",
    "ja": "厚型ステンレスフレームRO浄水機 10インチ",
    "ka": "10-დუიმიანი RO წყლის აპარატი გასქელებული უჟანგავი ფოლადის ჩარჩოთი",
    "kk": "Қалыңдатылған тот баспайтын болат рамалы 10 дюймдік RO су машинасы",
    "ko": "두꺼운 스테인리스 스틸 프레임 10인치 RO 정수기",
    "ku": "Makîneya ava RO ya 10 înç bi çarçoveya pola zengarnegir a xurtkirî",
    "ky": "Калыңдатылган дат баспас болот рамалуу 10 дюймдук RO суу аппараты",
    "lt": "10 colių RO vandens mašina su sustiprintu nerūdijančio plieno rėmu",
    "lv": "10 collu RO ūdens iekārta ar pastiprinātu nerūsējošā tērauda rāmi",
    "ms": "Mesin air RO rangka 10 inci dengan keluli tahan karat tebal",
    "nl": "10-inch RO-watermachine met versterkt roestvrijstalen frame",
    "no": "10-tommers RO-vannmaskin med forsterket rustfri stålramme",
    "pl": "10-calowa maszyna do wody RO ze wzmocnioną ramą ze stali nierdzewnej",
    "pt": "Máquina de água RO de 10 polegadas com estrutura reforçada de aço inoxidável",
    "ro": "Mașină de apă RO de 10 inch cu cadru ranforsat din oțel inoxidabil",
    "ru": "RO-машина для воды 10 дюймов с усиленной рамой из нержавеющей стали",
    "sk": "10-palcový RO vodný stroj so zosilneným rámom z nehrdzavejúcej ocele",
    "sl": "10-palčni RO vodni aparat z ojačanim okvirjem iz nerjavnega jekla",
    "sq": "Makineri uji RO 10 inç me kornizë të përforcuar prej çeliku inox",
    "sr": "10-инчна RO машина за воду са ојачаним рамом од нерђајућег челика",
    "sr-me": "10-inčna RO mašina za vodu sa ojačanim ramom od nerđajućeg čelika",
    "sv": "10-tums RO-vattenmaskin med förstärkt ram i rostfritt stål",
    "sw": "Mashine ya maji ya RO ya inchi 10 yenye fremu imara ya chuma cha pua",
    "ta": "தடிமனான துருப்பிடிக்காத எஃகு சட்டகத்துடன் 10 அங்குல RO நீர் இயந்திரம்",
    "tg": "Мошини оби RO 10-дюймӣ бо чорчӯбаи мустаҳками пӯлоди зангногир",
    "th": "เครื่องน้ำ RO 10 นิ้วพร้อมโครงสแตนเลสหนาพิเศษ",
    "tk": "Galyňlaşdyrylan poslamaýan polat karkasly 10 dýuým RO suw enjamy",
    "tl": "10-pulgadang makinarya ng tubig na RO na may makapal na balangkas na hindi kinakalawang",
    "tr": "Kalınlaştırılmış paslanmaz çelik şasili 10 inç RO su makinesi",
    "uk": "RO-машина для води 10 дюймів з посиленою рамою з нержавіючої сталі",
    "ur": "موٹے اسٹین لیس اسٹیل فریم والی 10 انچ RO واٹر مشین",
    "uz": "Qalinlashtirilgan zanglamas po‘lat ramali 10 dyuymli RO suv mashinasi",
    "vi": "Máy nước RO khung inox dày 10 inch",
    "zu": "Umshini wamanzi we-RO wama-intshi angu-10 onohlaka oluqinisiwe lwensimbi engagqwali",
}


def product_name(lang: str) -> str:
    if lang in PRODUCT_NAME_OVERRIDES:
        return PRODUCT_NAME_OVERRIDES[lang]
    base = BASE_PRODUCT_NAMES[lang]
    modifier = STAINLESS_MODIFIER[lang]
    if lang == "en":
        return f"{modifier} {base}"
    if lang in {"ja", "ko", "th", "ta", "bn"}:
        return f"{modifier}{base}"
    return f"{base} {modifier}"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def treatment_value(lang: str) -> str:
    ten = TEN_INCH[lang]
    post = POST_CARBON[lang]
    return f"{ten} PP + {ten} UDF + {ten} PP + 3012 RO + T33 {post}"


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    missing_sources = [
        name
        for name, source in {
            "product name": BASE_PRODUCT_NAMES,
            "stainless frame": STAINLESS_MODIFIER,
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
            "400G-800G RO water machine for municipal tap water projects",
            "Thickened stainless steel frame with compact 10-inch cartridge layout",
            "10-inch PP, 10-inch UDF, 10-inch PP, 3012 RO and T33 post-carbon stages",
            "Microcomputer control with full automatic intelligent operation",
            "OEM/ODM color, logo, label, packaging and configuration support",
        ],
        "applications": "Municipal tap-water purification for offices, cafés, retail stores, schools, distributor programs and OEM private-label RO machine projects.",
        "related": [
            "10-inch-frame-ro-water-machine-400g-1200g",
            "commercial-big-blue-ro-water-purifier-400g-800g",
            "portable-custom-ro-water-purifier-400g-800g",
            "desktop-ro-water-machine-compressor-cooling-100g",
        ],
    }
    for index, item in enumerate(products):
        if item.get("id") == PRODUCT_ID:
            products[index] = entry
            break
    else:
        insert_at = next(
            (i + 1 for i, item in enumerate(products) if item.get("id") == "10-inch-frame-ro-water-machine-400g-1200g"),
            10,
        )
        products.insert(insert_at, entry)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Thickened Stainless Steel 10-Inch Frame RO Water Machine 400G-800G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        if lang not in STAINLESS_MODIFIER
        or lang not in BASE_PRODUCT_NAMES
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
