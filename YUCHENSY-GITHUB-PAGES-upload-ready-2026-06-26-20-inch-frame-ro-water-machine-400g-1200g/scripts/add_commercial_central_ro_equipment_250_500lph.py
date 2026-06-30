#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add commercial central RO water purification equipment across all languages."""

from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_single_tank_pretreatment_ro_equipment_250_500lph.py"))
DUAL_GLOBALS = BASE["main"].__globals__["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
ORIGINAL_BUILD_MAIN = DUAL_GLOBALS["build_main"]
ORIGINAL_PRODUCT_GRAPH = DUAL_GLOBALS["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]

NEW_SLUG = "product-commercial-central-ro-water-purification-equipment-250-500lph.html"
PRODUCT_ID = "commercial-central-ro-water-purification-equipment-250-500lph"
MAIN_IMAGE = "commercial-central-ro-water-purification-equipment-250l-500l-oem.webp"
IMAGE_WIDTH = 316
IMAGE_HEIGHT = 518
AFTER_SLUG = "product-slim-reverse-osmosis-water-purification-equipment-250-500lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Kommersiële sentrale RO-water suiweringstoerusting",
    "ar": "معدات RO مركزية تجارية لتنقية المياه",
    "az": "Kommersiya mərkəzi RO su təmizləmə avadanlığı",
    "bg": "Търговско централно RO оборудване за пречистване на вода",
    "bn": "বাণিজ্যিক কেন্দ্রীয় RO পানি বিশুদ্ধকরণ সরঞ্জাম",
    "bs": "Komercijalna centralna RO oprema za prečišćavanje vode",
    "cs": "Komerční centrální RO zařízení na úpravu vody",
    "da": "Kommercielt centralt RO-vandrensningsanlæg",
    "de": "Gewerbliche zentrale RO-Wasseraufbereitungsanlage",
    "el": "Εμπορικός κεντρικός εξοπλισμός καθαρισμού νερού RO",
    "en": "Commercial Central RO Water Purification Equipment",
    "es": "Equipo RO central comercial de purificación de agua",
    "et": "Kaubanduslik keskne RO veepuhastusseade",
    "fa": "دستگاه مرکزی تجاری RO برای تصفیه آب",
    "fi": "Kaupallinen keskitetty RO-vedenpuhdistuslaitteisto",
    "fr": "Équipement central commercial RO de purification d’eau",
    "ha": "Na'urar RO ta tsakiya don kasuwanci ta tace ruwa",
    "he": "ציוד RO מרכזי מסחרי לטיהור מים",
    "hi": "वाणिज्यिक केंद्रीय RO जल शुद्धिकरण उपकरण",
    "hr": "Komercijalna centralna RO oprema za pročišćavanje vode",
    "hu": "Kereskedelmi központi RO víztisztító berendezés",
    "hy": "Առևտրային կենտրոնական RO ջրի մաքրման սարքավորում",
    "id": "Peralatan RO sentral komersial untuk pemurnian air",
    "it": "Impianto centrale commerciale RO per purificazione dell'acqua",
    "ja": "業務用中央RO浄水装置",
    "ka": "კომერციული ცენტრალური RO წყლის გამწმენდი მოწყობილობა",
    "kk": "Коммерциялық орталық RO су тазарту жабдығы",
    "ko": "상업용 중앙 RO 정수 장비",
    "ku": "Amûra RO ya navendî ya bazirganî ji bo paqijkirina avê",
    "ky": "Коммерциялык борбордук RO суу тазалоо жабдыгы",
    "lt": "Komercinė centrinė RO vandens valymo įranga",
    "lv": "Komerciāla centrālā RO ūdens attīrīšanas iekārta",
    "ms": "Peralatan RO pusat komersial untuk penulenan air",
    "nl": "Commerciële centrale RO-waterzuiveringsinstallatie",
    "no": "Kommersielt sentralt RO-vannrenseanlegg",
    "pl": "Komercyjne centralne urządzenie RO do uzdatniania wody",
    "pt": "Equipamento RO central comercial de purificação de água",
    "ro": "Echipament RO central comercial pentru purificarea apei",
    "ru": "Коммерческое центральное RO-оборудование для очистки воды",
    "sk": "Komerčné centrálne RO zariadenie na úpravu vody",
    "sl": "Komercialna centralna RO oprema za čiščenje vode",
    "sq": "Pajisje qendrore komerciale RO për pastrimin e ujit",
    "sr": "Комерцијална централна RO опрема за пречишћавање воде",
    "sr-me": "Komercijalna centralna RO oprema za prečišćavanje vode",
    "sv": "Kommersiell central RO-vattenreningsutrustning",
    "sw": "Kifaa cha kati cha RO cha kibiashara cha kusafisha maji",
    "ta": "வணிக மைய RO நீர் சுத்திகரிப்பு உபகரணம்",
    "tg": "Таҷҳизоти марказии тиҷоратии RO барои тозакунии об",
    "th": "อุปกรณ์ RO ส่วนกลางเชิงพาณิชย์สำหรับกรองน้ำ",
    "tk": "Täjirçilik merkezi RO suw arassalaýjy enjam",
    "tl": "Komersyal na sentral na kagamitang RO para sa paglilinis ng tubig",
    "tr": "Ticari merkezi RO su arıtma ekipmanı",
    "uk": "Комерційне центральне RO обладнання для очищення води",
    "ur": "تجارتی مرکزی RO پانی صاف کرنے کا سامان",
    "uz": "Tijorat markaziy RO suv tozalash uskunasi",
    "vi": "Thiết bị RO trung tâm thương mại lọc nước",
    "zu": "Imishini emaphakathi yezohwebo ye-RO yokuhlanza amanzi",
}


TREATMENT_VALUES = {
    "af": "20-duim PP + 20-duim CTO + 20-duim PP + RO",
    "ar": "PP مقاس 20 بوصة + CTO مقاس 20 بوصة + PP مقاس 20 بوصة + RO",
    "az": "20 düymlük PP + 20 düymlük CTO + 20 düymlük PP + RO",
    "bg": "20-инчов PP + 20-инчов CTO + 20-инчов PP + RO",
    "bn": "20 ইঞ্চি PP + 20 ইঞ্চি CTO + 20 ইঞ্চি PP + RO",
    "bs": "20-inčni PP + 20-inčni CTO + 20-inčni PP + RO",
    "cs": "20palcový PP + 20palcový CTO + 20palcový PP + RO",
    "da": "20-tommer PP + 20-tommer CTO + 20-tommer PP + RO",
    "de": "20-Zoll PP + 20-Zoll CTO + 20-Zoll PP + RO",
    "el": "PP 20 ιντσών + CTO 20 ιντσών + PP 20 ιντσών + RO",
    "en": "20-inch PP + 20-inch CTO + 20-inch PP + RO",
    "es": "PP de 20 pulgadas + CTO de 20 pulgadas + PP de 20 pulgadas + RO",
    "et": "20-tolline PP + 20-tolline CTO + 20-tolline PP + RO",
    "fa": "PP بیست اینچ + CTO بیست اینچ + PP بیست اینچ + RO",
    "fi": "PP 20 tuumaa + CTO 20 tuumaa + PP 20 tuumaa + RO",
    "fr": "PP 20 pouces + CTO 20 pouces + PP 20 pouces + RO",
    "ha": "PP inci 20 + CTO inci 20 + PP inci 20 + RO",
    "he": "PP בגודל 20 אינץ׳ + CTO בגודל 20 אינץ׳ + PP בגודל 20 אינץ׳ + RO",
    "hi": "20 इंच PP + 20 इंच CTO + 20 इंच PP + RO",
    "hr": "20-inčni PP + 20-inčni CTO + 20-inčni PP + RO",
    "hu": "20 hüvelykes PP + 20 hüvelykes CTO + 20 hüvelykes PP + RO",
    "hy": "20 դյույմ PP + 20 դյույմ CTO + 20 դյույմ PP + RO",
    "id": "PP 20 inci + CTO 20 inci + PP 20 inci + RO",
    "it": "PP da 20 pollici + CTO da 20 pollici + PP da 20 pollici + RO",
    "ja": "20インチPP + 20インチCTO + 20インチPP + RO",
    "ka": "20 დუიმიანი PP + 20 დუიმიანი CTO + 20 დუიმიანი PP + RO",
    "kk": "20 дюймдік PP + 20 дюймдік CTO + 20 дюймдік PP + RO",
    "ko": "20인치 PP + 20인치 CTO + 20인치 PP + RO",
    "ku": "PP 20 înç + CTO 20 înç + PP 20 înç + RO",
    "ky": "20 дюймдук PP + 20 дюймдук CTO + 20 дюймдук PP + RO",
    "lt": "20 colių PP + 20 colių CTO + 20 colių PP + RO",
    "lv": "20 collu PP + 20 collu CTO + 20 collu PP + RO",
    "ms": "PP 20 inci + CTO 20 inci + PP 20 inci + RO",
    "nl": "20 inch PP + 20 inch CTO + 20 inch PP + RO",
    "no": "20-tommers PP + 20-tommers CTO + 20-tommers PP + RO",
    "pl": "PP 20 cali + CTO 20 cali + PP 20 cali + RO",
    "pt": "PP de 20 polegadas + CTO de 20 polegadas + PP de 20 polegadas + RO",
    "ro": "PP de 20 inci + CTO de 20 inci + PP de 20 inci + RO",
    "ru": "20-дюймовый PP + 20-дюймовый CTO + 20-дюймовый PP + RO",
    "sk": "20-palcový PP + 20-palcový CTO + 20-palcový PP + RO",
    "sl": "20-palčni PP + 20-palčni CTO + 20-palčni PP + RO",
    "sq": "PP 20 inç + CTO 20 inç + PP 20 inç + RO",
    "sr": "PP од 20 инча + CTO од 20 инча + PP од 20 инча + RO",
    "sr-me": "PP od 20 inča + CTO od 20 inča + PP od 20 inča + RO",
    "sv": "20-tums PP + 20-tums CTO + 20-tums PP + RO",
    "sw": "PP inchi 20 + CTO inchi 20 + PP inchi 20 + RO",
    "ta": "20 அங்குல PP + 20 அங்குல CTO + 20 அங்குல PP + RO",
    "tg": "PP-и 20 дюйм + CTO-и 20 дюйм + PP-и 20 дюйм + RO",
    "th": "PP 20 นิ้ว + CTO 20 นิ้ว + PP 20 นิ้ว + RO",
    "tk": "20 dýuým PP + 20 dýuým CTO + 20 dýuým PP + RO",
    "tl": "PP na 20 pulgada + CTO na 20 pulgada + PP na 20 pulgada + RO",
    "tr": "20 inç PP + 20 inç CTO + 20 inç PP + RO",
    "uk": "20-дюймовий PP + 20-дюймовий CTO + 20-дюймовий PP + RO",
    "ur": "20 انچ PP + 20 انچ CTO + 20 انچ PP + RO",
    "uz": "20 dyuymli PP + 20 dyuymli CTO + 20 dyuymli PP + RO",
    "vi": "PP 20 inch + CTO 20 inch + PP 20 inch + RO",
    "zu": "PP engu-20 intshi + CTO engu-20 intshi + PP engu-20 intshi + RO",
}


def flow_value(lang: str) -> str:
    return f"250-500 {FLOW_UNITS.get(lang, FLOW_UNITS['en'])}"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in NAME_PREFIXES or lang not in TREATMENT_VALUES:
        raise KeyError(f"No product translation for {lang}")
    name = f"{NAME_PREFIXES[lang]} {flow_value(lang)}"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[2] = TREATMENT_VALUES[lang]
    values[3] = flow_value(lang)
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
    text = ORIGINAL_BUILD_MAIN(lang, copy)
    encoded = "Commercial%20Central%20RO%20Water%20Purification%20Equipment%20250-500Lph"
    for old in [
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Single%20Tank%20Pretreatment%20RO%20Equipment%20250-500Lph",
        "Slim%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250-500Lph",
    ]:
        text = text.replace(old, encoded)
    return text


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(ORIGINAL_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}"]
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = copy_for("en")
    insert_at = next(
        (i + 1 for i, item in enumerate(products) if item.get("id") == "slim-reverse-osmosis-water-purification-equipment-250-500lph"),
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
            "Commercial central RO purification cabinet",
            "20-inch PP + 20-inch CTO + 20-inch PP + RO treatment",
            "250-500 L/h purified water flow",
            "Suitable for tap water and groundwater",
            "0.1-0.4 MPa feed pressure",
        ],
        "applications": "Commercial central water purification for offices, workshops, hotels, schools, kitchens and light industrial drinking-water supply.",
        "related": [
            "slim-reverse-osmosis-water-purification-equipment-250-500lph",
            "single-tank-big-blue-pp-ro-equipment-250-500lph",
            "single-tank-pretreatment-ro-equipment-250-500lph",
            "six-housing-ro-equipment-with-pure-water-tank-250-1000lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Commercial Central RO Water Purification Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    missing = [lang for lang in DUAL_GLOBALS["dirs"]() if lang not in NAME_PREFIXES or lang not in TREATMENT_VALUES]
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
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()


if __name__ == "__main__":
    main()
