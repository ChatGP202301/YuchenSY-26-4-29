#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add slim RO water purification equipment across all language pages."""

from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_single_tank_big_blue_pp_ro_equipment_250_500lph.py"))
DUAL_GLOBALS = BASE["main"].__globals__["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
ORIGINAL_BUILD_MAIN = DUAL_GLOBALS["build_main"]
ORIGINAL_PRODUCT_GRAPH = DUAL_GLOBALS["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]

NEW_SLUG = "product-slim-reverse-osmosis-water-purification-equipment-250-500lph.html"
PRODUCT_ID = "slim-reverse-osmosis-water-purification-equipment-250-500lph"
MAIN_IMAGE = "slim-reverse-osmosis-water-purification-equipment-250l-500l-oem.webp"
IMAGE_WIDTH = 392
IMAGE_HEIGHT = 640
AFTER_SLUG = "product-single-tank-big-blue-pp-ro-equipment-250-500lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Smal RO-water suiweringstoerusting",
    "ar": "معدات RO ضيقة لتنقية المياه",
    "az": "Dar gövdəli RO su təmizləmə avadanlığı",
    "bg": "Тясно RO оборудване за пречистване на вода",
    "bn": "সরু RO পানি বিশুদ্ধকরণ সরঞ্জাম",
    "bs": "Uska RO oprema za prečišćavanje vode",
    "cs": "Úzké RO zařízení na úpravu vody",
    "da": "Smal RO-vandrensningsenhed",
    "de": "Schmale RO-Wasseraufbereitungsanlage",
    "el": "Στενός εξοπλισμός καθαρισμού νερού RO",
    "en": "Slim Reverse Osmosis Water Purification Equipment",
    "es": "Equipo RO estrecho de purificación de agua",
    "et": "Kitsas RO veepuhastusseade",
    "fa": "دستگاه باریک RO برای تصفیه آب",
    "fi": "Kapea RO-vedenpuhdistuslaitteisto",
    "fr": "Équipement RO étroit de purification d’eau",
    "ha": "Na'urar RO mai siriri don tace ruwa",
    "he": "ציוד RO צר לטיהור מים",
    "hi": "स्लिम RO जल शुद्धिकरण उपकरण",
    "hr": "Uska RO oprema za pročišćavanje vode",
    "hu": "Keskeny RO víztisztító berendezés",
    "hy": "Նեղ RO ջրի մաքրման սարքավորում",
    "id": "Peralatan RO ramping untuk pemurnian air",
    "it": "Impianto RO stretto per purificazione dell'acqua",
    "ja": "スリム型RO浄水装置",
    "ka": "ვიწრო RO წყლის გამწმენდი მოწყობილობა",
    "kk": "Жіңішке RO су тазарту жабдығы",
    "ko": "슬림형 RO 정수 장비",
    "ku": "Amûra RO ya zirav ji bo paqijkirina avê",
    "ky": "Ичке RO суу тазалоо жабдыгы",
    "lt": "Siaura RO vandens valymo įranga",
    "lv": "Šaura RO ūdens attīrīšanas iekārta",
    "ms": "Peralatan RO reka bentuk sempit untuk penulenan air",
    "nl": "Smalle RO-waterzuiveringsinstallatie",
    "no": "Smal RO-vannrenseenhet",
    "pl": "Wąskie urządzenie RO do uzdatniania wody",
    "pt": "Equipamento RO estreito de purificação de água",
    "ro": "Echipament RO îngust pentru purificarea apei",
    "ru": "Узкое RO-оборудование для очистки воды",
    "sk": "Úzke RO zariadenie na úpravu vody",
    "sl": "Ozka RO oprema za čiščenje vode",
    "sq": "Pajisje RO i ngushtë për pastrimin e ujit",
    "sr": "Уска RO опрема за пречишћавање воде",
    "sr-me": "Uska RO oprema za prečišćavanje vode",
    "sv": "Smal RO-vattenreningsutrustning",
    "sw": "Kifaa chembamba cha RO cha kusafisha maji",
    "ta": "மெலிந்த RO நீர் சுத்திகரிப்பு உபகரணம்",
    "tg": "Таҷҳизоти борики RO барои тозакунии об",
    "th": "อุปกรณ์ RO แบบแคบสำหรับกรองน้ำ",
    "tk": "Inçe görnüşli RO suw arassalaýjy enjam",
    "tl": "Makitid na kagamitang RO para sa paglilinis ng tubig",
    "tr": "Dar tip RO su arıtma ekipmanı",
    "uk": "Вузьке RO обладнання для очищення води",
    "ur": "پتلا RO پانی صاف کرنے کا سامان",
    "uz": "Ixcham RO suv tozalash uskunasi",
    "vi": "Thiết bị RO dạng hẹp lọc nước",
    "zu": "Imishini encane ye-RO yokuhlanza amanzi",
}


TREATMENT_VALUES = {
    "af": "PP-katoenfilterpatroon + geaktiveerdekoolfilterpatroon + RO",
    "ar": "خرطوشة PP قطنية + خرطوشة كربون نشط + RO",
    "az": "PP pambıq filtr kartrici + aktivləşdirilmiş karbon kartrici + RO",
    "bg": "PP памучен филтърен патрон + патрон с активен въглен + RO",
    "bn": "PP কটন ফিল্টার কার্টিজ + অ্যাক্টিভেটেড কার্বন কার্টিজ + RO",
    "bs": "PP pamučni filterski uložak + uložak od aktivnog uglja + RO",
    "cs": "PP bavlněná filtrační vložka + vložka s aktivním uhlím + RO",
    "da": "PP-bomuldsfilterpatron + aktivt kulfilterpatron + RO",
    "de": "PP-Sedimentfilterpatrone + Aktivkohlefilterpatrone + RO",
    "el": "Φυσίγγιο φίλτρου PP για ιζήματα + φυσίγγιο ενεργού άνθρακα + RO",
    "en": "PP cotton filter cartridge + activated carbon cartridge + RO",
    "es": "Cartucho filtrante PP de sedimentos + cartucho de carbón activado + RO",
    "et": "PP-settefiltri padrun + aktiivsöe padrun + RO",
    "fa": "کارتریج PP الیافی + کارتریج کربن فعال + RO",
    "fi": "PP-sedimenttisuodatinpatruuna + aktiivihiilisuodatinpatruuna + RO",
    "fr": "Cartouche PP sédiments + cartouche charbon actif + RO",
    "ha": "Kartirij ɗin PP na laka + kartirij ɗin carbon mai aiki + RO",
    "he": "מחסנית סינון משקעים PP + מחסנית פחם פעיל + RO",
    "hi": "PP सेडिमेंट फिल्टर कार्ट्रिज + सक्रिय कार्बन कार्ट्रिज + RO",
    "hr": "PP sedimentni filterski uložak + uložak od aktivnog ugljena + RO",
    "hu": "PP üledékszűrő betét + aktívszenes szűrőbetét + RO",
    "hy": "PP նստվածքային ֆիլտրի քարթրիջ + ակտիվացված ածխային քարթրիջ + RO",
    "id": "Kartrid filter sedimen PP + kartrid karbon aktif + RO",
    "it": "Cartuccia filtrante PP per sedimenti + cartuccia a carbone attivo + RO",
    "ja": "PP沈殿物フィルターカートリッジ + 活性炭カートリッジ + RO",
    "ka": "PP ნალექის ფილტრის კარტრიჯი + აქტივირებული ნახშირის კარტრიჯი + RO",
    "kk": "PP тұнба сүзгі картриджі + белсендірілген көмір картриджі + RO",
    "ko": "PP 침전물 필터 카트리지 + 활성탄 카트리지 + RO",
    "ku": "Karterîca fîltera sedîmentê ya PP + karterîca karbonê çalak + RO",
    "ky": "PP чөкмө чыпка картриджи + активдештирилген көмүр картриджи + RO",
    "lt": "PP nuosėdų filtro kasetė + aktyvintos anglies kasetė + RO",
    "lv": "PP nogulšņu filtra kasetne + aktīvās ogles kasetne + RO",
    "ms": "Kartrij penapis sedimen PP + kartrij karbon aktif + RO",
    "nl": "PP-sedimentfilterpatroon + actiefkoolfilterpatroon + RO",
    "no": "PP-sedimentfilterpatron + aktivt karbonfilterpatron + RO",
    "pl": "Wkład osadowy PP + wkład z węglem aktywnym + RO",
    "pt": "Cartucho PP de sedimentos + cartucho de carvão ativado + RO",
    "ro": "Cartuș filtrant PP pentru sedimente + cartuș cu carbon activ + RO",
    "ru": "PP-картридж механической очистки + картридж с активированным углем + RO",
    "sk": "PP sedimentačná filtračná vložka + vložka s aktívnym uhlím + RO",
    "sl": "PP sedimentni filtrski vložek + vložek z aktivnim ogljem + RO",
    "sq": "Fishek filtri PP për sedimente + fishek karboni aktiv + RO",
    "sr": "PP уложак за механичке нечистоће + уложак са активним угљем + RO",
    "sr-me": "PP uložak za sediment + uložak sa aktivnim ugljem + RO",
    "sv": "PP-sedimentfilterpatron + patron med aktivt kol + RO",
    "sw": "Katriji ya PP ya kuondoa mashapo + katriji ya kaboni amilifu + RO",
    "ta": "PP கழிவு வடிகட்டி கார்ட்ரிட்ஜ் + செயற்படுத்தப்பட்ட கார்பன் கார்ட்ரிட்ஜ் + RO",
    "tg": "Картриҷи филтри таҳшинии PP + картриҷи карбони фаъол + RO",
    "th": "ไส้กรองตะกอน PP + ไส้กรองคาร์บอนกัมมันต์ + RO",
    "tk": "PP çökündi süzgüç kartriji + işjeňleşdirilen karbon kartriji + RO",
    "tl": "PP na kartutso para sa latak + kartutso ng activated carbon + RO",
    "tr": "PP tortu filtre kartuşu + aktif karbon kartuşu + RO",
    "uk": "PP-картридж механічного очищення + картридж з активованим вугіллям + RO",
    "ur": "PP سیڈمنٹ فلٹر کارٹریج + فعال کاربن کارٹریج + RO",
    "uz": "PP cho‘kindi filtr kartriji + faollashtirilgan ko‘mir kartriji + RO",
    "vi": "Lõi lọc cặn PP + lõi than hoạt tính + RO",
    "zu": "Ikhatriji yesihlungi se-PP sokubamba izinhlayiya + ikhatriji yekhabhoni esebenzayo + RO",
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
    encoded = "Slim%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250-500Lph"
    for old in [
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Single%20Tank%20Pretreatment%20RO%20Equipment%20250-500Lph",
        "Single%20Tank%20Big%20Blue%20PP%20RO%20Equipment%20250-500Lph",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "single-tank-big-blue-pp-ro-equipment-250-500lph"),
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
            "Slim frame reverse osmosis equipment",
            "PP cotton cartridge, activated carbon cartridge and RO treatment",
            "250-500 L/h purified water flow",
            "Designed for municipal tap water",
            "0.1-0.4 MPa feed pressure",
        ],
        "applications": "Municipal tap-water purification for compact commercial drinking water, offices, workshops, schools and light industrial supply.",
        "related": [
            "single-tank-big-blue-pp-ro-equipment-250-500lph",
            "single-tank-pretreatment-ro-equipment-250-500lph",
            "dual-tank-pretreatment-ro-equipment-250-1000lph",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Slim Reverse Osmosis Water Purification Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
