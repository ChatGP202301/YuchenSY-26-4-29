#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add single-tank 20-inch large PP prefilter RO equipment across all languages."""

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

NEW_SLUG = "product-single-tank-big-blue-pp-ro-equipment-250-500lph.html"
PRODUCT_ID = "single-tank-big-blue-pp-ro-equipment-250-500lph"
MAIN_IMAGE = "single-tank-20-inch-big-blue-pp-ro-water-purification-equipment-250l-500l-oem.webp"
IMAGE_WIDTH = 396
IMAGE_HEIGHT = 640
AFTER_SLUG = "product-single-tank-pretreatment-ro-equipment-250-500lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "RO-toerusting met enkeltenk en 20-duim grootformaat PP-voorfilter",
    "ar": "معدات RO بخزان واحد مع مرشح PP كبير مقاس 20 بوصة",
    "az": "Tək çənli 20 düymlük iri PP ön filtrli RO avadanlığı",
    "bg": "RO оборудване с един съд и 20-инчов голям PP предфилтър",
    "bn": "এক ট্যাংক 20 ইঞ্চি বড় PP প্রি-ফিল্টার RO সরঞ্জাম",
    "bs": "RO oprema s jednim tankom i velikim PP predfilterom od 20 inča",
    "cs": "RO zařízení s jednou nádobou a velkým 20palcovým PP předfiltrem",
    "da": "RO-anlæg med én tank og 20-tommer stor PP-forfilter",
    "de": "RO-Anlage mit einem Tank und großem 20-Zoll-PP-Vorfilter",
    "el": "Εξοπλισμός RO μίας δεξαμενής με μεγάλο προφίλτρο PP 20 ιντσών",
    "en": "Single-Tank 20-Inch Big Blue PP Reverse Osmosis Water Purification Equipment",
    "es": "Equipo RO de un tanque con prefiltro PP grande de 20 pulgadas",
    "et": "Ühe paagiga RO seade suure 20-tollise PP eelfiltriga",
    "fa": "دستگاه RO تک‌مخزن با پیش‌فیلتر بزرگ PP بیست اینچ",
    "fi": "Yhden säiliön RO-laitteisto suurella 20 tuuman PP-esisuodattimella",
    "fr": "Équipement RO à une cuve avec grand préfiltre PP 20 pouces",
    "ha": "Na'urar RO mai tanki ɗaya da babban PP na farko inci 20",
    "he": "ציוד RO במכל יחיד עם מסנן מקדים PP גדול בגודל 20 אינץ׳",
    "hi": "एकल टैंक 20 इंच बड़े PP प्री-फिल्टर वाला RO उपकरण",
    "hr": "RO oprema s jednim spremnikom i velikim PP predfiltrom od 20 inča",
    "hu": "Egytartályos RO berendezés nagy 20 hüvelykes PP előszűrővel",
    "hy": "Մեկ բաքով RO սարքավորում 20 դյույմ մեծ PP նախաֆիլտրով",
    "id": "Peralatan RO satu tangki dengan pra-filter PP besar 20 inci",
    "it": "Impianto RO a serbatoio singolo con grande prefiltro PP da 20 pollici",
    "ja": "単槽20インチ大型PP前置フィルターRO浄水装置",
    "ka": "ერთავზიანი RO მოწყობილობა დიდი 20 დუიმიანი PP წინასწარი ფილტრით",
    "kk": "Бір бакты 20 дюймдік үлкен PP алдын ала сүзгісі бар RO жабдығы",
    "ko": "단일 탱크 20인치 대형 PP 전처리 필터 RO 장비",
    "ku": "Amûra RO ya yek tankî bi pêşfîltera PP ya mezin a 20 înç",
    "ky": "Бир бактуу 20 дюймдук чоң PP алдын ала чыпкалуу RO жабдыгы",
    "lt": "Vienos talpos RO įranga su dideliu 20 colių PP pirminiu filtru",
    "lv": "Vienas tvertnes RO iekārta ar lielu 20 collu PP priekšfiltru",
    "ms": "Peralatan RO satu tangki dengan pra-penapis PP besar 20 inci",
    "nl": "RO-installatie met één tank en groot 20-inch PP-voorfilter",
    "no": "RO-anlegg med én tank og stort 20-tommers PP-forfilter",
    "pl": "Urządzenie RO z jednym zbiornikiem i dużym 20-calowym filtrem wstępnym PP",
    "pt": "Equipamento RO de um tanque com pré-filtro PP grande de 20 polegadas",
    "ro": "Echipament RO cu un rezervor și prefiltru PP mare de 20 inci",
    "ru": "RO-оборудование с одной колонной и большим 20-дюймовым PP-предфильтром",
    "sk": "RO zariadenie s jednou nádobou a veľkým 20-palcovým PP predfiltrom",
    "sl": "RO oprema z enim rezervoarjem in velikim 20-palčnim PP predfiltrom",
    "sq": "Pajisje RO me një rezervuar dhe parafiltër të madh PP 20 inç",
    "sr": "RO опрема са једним резервоаром и великим PP предфилтером од 20 инча",
    "sr-me": "RO oprema sa jednim rezervoarom i velikim PP predfilterom od 20 inča",
    "sv": "RO-utrustning med en tank och stort 20-tums PP-förfilter",
    "sw": "Kifaa cha RO chenye tanki moja na kichujio cha awali cha PP kikubwa cha inchi 20",
    "ta": "ஒற்றை தொட்டி 20 அங்குல பெரிய PP முன் வடிகட்டி RO உபகரணம்",
    "tg": "Таҷҳизоти RO бо як зарф ва пешфилтри калони PP-и 20 дюйм",
    "th": "อุปกรณ์ RO ถังเดียวพร้อมไส้กรอง PP ขนาดใหญ่ 20 นิ้ว",
    "tk": "Bir bakly 20 dýuým uly PP öň süzgüçli RO enjamy",
    "tl": "Kagamitang RO na may isang tangke at malaking paunang PP na pansala na 20 pulgada",
    "tr": "Tek tanklı, 20 inç büyük PP ön filtreli RO ekipmanı",
    "uk": "RO обладнання з однією колоною та великим 20-дюймовим PP передфільтром",
    "ur": "ایک ٹینک والا 20 انچ بڑا PP پری فلٹر RO سامان",
    "uz": "Bir bakli 20 dyuymli katta PP old filtrli RO uskunasi",
    "vi": "Thiết bị RO một bồn với lõi lọc PP cỡ lớn 20 inch",
    "zu": "Imishini ye-RO enethangi elilodwa nesihlungi sangaphambili se-PP esikhulu esingu-20 intshi",
}


TREATMENT_VALUES = {
    "af": "20-duim grootformaat PP-voorfilter + RO",
    "ar": "مرشح PP كبير مقاس 20 بوصة + RO",
    "az": "20 düymlük iri PP ön filtri + RO",
    "bg": "20-инчов голям PP предфилтър + RO",
    "bn": "20 ইঞ্চি বড় PP প্রি-ফিল্টার + RO",
    "bs": "Veliki PP predfilter od 20 inča + RO",
    "cs": "Velký 20palcový PP předfiltr + RO",
    "da": "20-tommer stor PP-forfilter + RO",
    "de": "Großer 20-Zoll-PP-Vorfilter + RO",
    "el": "Μεγάλο προφίλτρο PP 20 ιντσών + RO",
    "en": "20-inch Big Blue PP prefilter + RO",
    "es": "Prefiltro PP grande de 20 pulgadas + RO",
    "et": "Suur 20-tolline PP eelfilter + RO",
    "fa": "پیش‌فیلتر بزرگ PP بیست اینچ + RO",
    "fi": "Suuri 20 tuuman PP-esisuodatin + RO",
    "fr": "Grand préfiltre PP 20 pouces + RO",
    "ha": "Babban PP na farko inci 20 + RO",
    "he": "מסנן מקדים PP גדול בגודל 20 אינץ׳ + RO",
    "hi": "20 इंच बड़ा PP प्री-फिल्टर + RO",
    "hr": "Veliki PP predfilter od 20 inča + RO",
    "hu": "Nagy 20 hüvelykes PP előszűrő + RO",
    "hy": "20 դյույմ մեծ PP նախաֆիլտր + RO",
    "id": "Pra-filter PP besar 20 inci + RO",
    "it": "Grande prefiltro PP da 20 pollici + RO",
    "ja": "20インチ大型PP前置フィルター + RO",
    "ka": "დიდი 20 დუიმიანი PP წინასწარი ფილტრი + RO",
    "kk": "20 дюймдік үлкен PP алдын ала сүзгісі + RO",
    "ko": "20인치 대형 PP 전처리 필터 + RO",
    "ku": "Pêşfîltera PP ya mezin a 20 înç + RO",
    "ky": "20 дюймдук чоң PP алдын ала чыпкасы + RO",
    "lt": "Didelis 20 colių PP pirminis filtras + RO",
    "lv": "Liels 20 collu PP priekšfiltrs + RO",
    "ms": "Pra-penapis PP besar 20 inci + RO",
    "nl": "Groot 20-inch PP-voorfilter + RO",
    "no": "Stort 20-tommers PP-forfilter + RO",
    "pl": "Duży 20-calowy filtr wstępny PP + RO",
    "pt": "Pré-filtro PP grande de 20 polegadas + RO",
    "ro": "Prefiltru PP mare de 20 inci + RO",
    "ru": "Большой 20-дюймовый PP-предфильтр + RO",
    "sk": "Veľký 20-palcový PP predfilter + RO",
    "sl": "Velik 20-palčni PP predfilter + RO",
    "sq": "Parafiltër i madh PP 20 inç + RO",
    "sr": "Велики PP предфилтер од 20 инча + RO",
    "sr-me": "Veliki PP predfilter od 20 inča + RO",
    "sv": "Stort 20-tums PP-förfilter + RO",
    "sw": "Kichujio cha awali cha PP kikubwa cha inchi 20 + RO",
    "ta": "20 அங்குல பெரிய PP முன் வடிகட்டி + RO",
    "tg": "Пешфилтри калони PP-и 20 дюйм + RO",
    "th": "ไส้กรอง PP ขนาดใหญ่ 20 นิ้ว + RO",
    "tk": "20 dýuým uly PP öň süzgüji + RO",
    "tl": "Malaking paunang PP na pansala na 20 pulgada + RO",
    "tr": "20 inç büyük PP ön filtre + RO",
    "uk": "Великий 20-дюймовий PP передфільтр + RO",
    "ur": "20 انچ بڑا PP پری فلٹر + RO",
    "uz": "20 dyuymli katta PP old filtri + RO",
    "vi": "Lõi lọc PP cỡ lớn 20 inch + RO",
    "zu": "Isihlungi sangaphambili se-PP esikhulu esingu-20 intshi + RO",
}


FEED_WATER_VALUES = {
    "af": "Munisipale kraanwater",
    "ar": "مياه الصنبور البلدية",
    "az": "Bələdiyyə şəbəkə suyu",
    "bg": "Общинска чешмяна вода",
    "bn": "পৌর কলের পানি",
    "bs": "Gradska voda iz vodovoda",
    "cs": "Městská vodovodní voda",
    "da": "Kommunalt vandværksvand",
    "de": "Kommunales Leitungswasser",
    "el": "Δημοτικό νερό βρύσης",
    "en": "Municipal tap water",
    "es": "Agua municipal de red",
    "et": "Munitsipaalne kraanivesi",
    "fa": "آب شهری",
    "fi": "Kunnallinen vesijohtovesi",
    "fr": "Eau de ville",
    "ha": "Ruwan famfo na birni",
    "he": "מי ברז עירוניים",
    "hi": "नगरपालिका नल का पानी",
    "hr": "Gradska vodovodna voda",
    "hu": "Városi vezetékes víz",
    "hy": "Քաղաքային ծորակի ջուր",
    "id": "Air PDAM",
    "it": "Acqua di rete municipale",
    "ja": "市政水道水",
    "ka": "მუნიციპალური ონკანის წყალი",
    "kk": "Қалалық су құбыры суы",
    "ko": "시 상수도",
    "ku": "Ava şemiyê ya bajêr",
    "ky": "Шаардык суу түтүк суусу",
    "lt": "Municipalinis vandentiekio vanduo",
    "lv": "Pašvaldības krāna ūdens",
    "ms": "Air paip perbandaran",
    "nl": "Gemeentelijk leidingwater",
    "no": "Kommunalt springvann",
    "pl": "Miejska woda wodociągowa",
    "pt": "Água municipal da rede",
    "ro": "Apă de la rețeaua municipală",
    "ru": "Муниципальная водопроводная вода",
    "sk": "Mestská voda z vodovodu",
    "sl": "Mestna vodovodna voda",
    "sq": "Ujë rubineti bashkiak",
    "sr": "Градска водоводна вода",
    "sr-me": "Gradska vodovodna voda",
    "sv": "Kommunalt kranvatten",
    "sw": "Maji ya bomba ya manispaa",
    "ta": "நகராட்சி குழாய் நீர்",
    "tg": "Оби қубурии шаҳрӣ",
    "th": "น้ำประปาเทศบาล",
    "tk": "Şäher suw geçirijisiniň suwy",
    "tl": "Tubig-gripo ng munisipyo",
    "tr": "Belediye şebeke suyu",
    "uk": "Муніципальна водопровідна вода",
    "ur": "بلدیاتی نل کا پانی",
    "uz": "Shahar vodoprovod suvi",
    "vi": "Nước máy đô thị",
    "zu": "Amanzi kampompi kamasipala",
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
    text = ORIGINAL_BUILD_MAIN(lang, copy)
    return text.replace(
        "Single%20Tank%20Pretreatment%20RO%20Equipment%20250-500Lph",
        "Single%20Tank%20Big%20Blue%20PP%20RO%20Equipment%20250-500Lph",
    )


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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "single-tank-pretreatment-ro-equipment-250-500lph"),
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
            "20-inch Big Blue PP prefilter with RO purification",
            "250-500 L/h purified water flow",
            "Designed for municipal tap water projects",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Municipal tap-water purification for commercial drinking water, offices, workshops, schools and light industrial water supply.",
        "related": [
            "single-tank-pretreatment-ro-equipment-250-500lph",
            "dual-tank-pretreatment-ro-equipment-250-1000lph",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
            "six-housing-ro-equipment-with-pure-water-tank-250-1000lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Single-Tank 20-Inch Big Blue PP Reverse Osmosis Water Purification Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


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
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()


if __name__ == "__main__":
    main()
