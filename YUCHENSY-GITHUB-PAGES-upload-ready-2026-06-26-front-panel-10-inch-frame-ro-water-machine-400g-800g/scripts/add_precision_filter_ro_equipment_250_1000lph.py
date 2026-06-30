#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add precision-filter RO water purification equipment across all languages."""

from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_commercial_central_ro_equipment_250_500lph.py"))
DUAL_GLOBALS = BASE["main"].__globals__["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-precision-filter-ro-water-purification-equipment-250-1000lph.html"
PRODUCT_ID = "precision-filter-ro-water-purification-equipment-250-1000lph"
MAIN_IMAGE = "precision-filter-ro-water-purification-equipment-250l-1000l-oem.webp"
IMAGE_WIDTH = 382
IMAGE_HEIGHT = 636
AFTER_SLUG = "product-commercial-central-ro-water-purification-equipment-250-500lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Presisiefilter RO-water suiweringstoerusting",
    "ar": "معدات RO لتنقية المياه بفلتر دقيق",
    "az": "Dəqiq filtrli RO su təmizləmə avadanlığı",
    "bg": "RO оборудване за пречистване на вода с прецизен филтър",
    "bn": "প্রিসিশন ফিল্টার RO পানি বিশুদ্ধকরণ সরঞ্জাম",
    "bs": "RO oprema za prečišćavanje vode s preciznim filterom",
    "cs": "RO zařízení na úpravu vody s jemným filtrem",
    "da": "RO-vandrensningsanlæg med præcisionsfilter",
    "de": "RO-Wasseraufbereitungsanlage mit Feinfilter",
    "el": "Εξοπλισμός καθαρισμού νερού RO με φίλτρο ακριβείας",
    "en": "Precision Filter RO Water Purification Equipment",
    "es": "Equipo RO de purificación de agua con filtro de precisión",
    "et": "Täppisfiltriga RO veepuhastusseade",
    "fa": "دستگاه RO تصفیه آب با فیلتر دقیق",
    "fi": "Tarkkuussuodattimella varustettu RO-vedenpuhdistuslaitteisto",
    "fr": "Équipement RO de purification d’eau avec filtre de précision",
    "ha": "Na'urar RO ta tace ruwa mai matatar daidaito",
    "he": "ציוד RO לטיהור מים עם מסנן מדויק",
    "hi": "प्रिसिजन फिल्टर RO जल शुद्धिकरण उपकरण",
    "hr": "RO oprema za pročišćavanje vode s preciznim filtrom",
    "hu": "Finomszűrős RO víztisztító berendezés",
    "hy": "Ճշգրիտ ֆիլտրով RO ջրի մաքրման սարքավորում",
    "id": "Peralatan RO pemurnian air dengan filter presisi",
    "it": "Impianto RO per purificazione dell'acqua con filtro di precisione",
    "ja": "精密フィルター付きRO浄水装置",
    "ka": "ზუსტი ფილტრით RO წყლის გამწმენდი მოწყობილობა",
    "kk": "Дәл сүзгілі RO су тазарту жабдығы",
    "ko": "정밀 필터 RO 정수 장비",
    "ku": "Amûra RO ya paqijkirina avê bi parzûna hûr",
    "ky": "Так чыпкалуу RO суу тазалоо жабдыгы",
    "lt": "RO vandens valymo įranga su tiksliuoju filtru",
    "lv": "RO ūdens attīrīšanas iekārta ar precīzo filtru",
    "ms": "Peralatan RO penulenan air dengan penapis ketepatan",
    "nl": "RO-waterzuiveringsinstallatie met precisiefilter",
    "no": "RO-vannrenseanlegg med presisjonsfilter",
    "pl": "Urządzenie RO do uzdatniania wody z filtrem dokładnym",
    "pt": "Equipamento RO de purificação de água com filtro de precisão",
    "ro": "Echipament RO de purificare a apei cu filtru de precizie",
    "ru": "RO-оборудование для очистки воды с прецизионным фильтром",
    "sk": "RO zariadenie na úpravu vody s jemným filtrom",
    "sl": "RO oprema za čiščenje vode s finim filtrom",
    "sq": "Pajisje RO për pastrimin e ujit me filtër preciz",
    "sr": "RO опрема за пречишћавање воде са прецизним филтером",
    "sr-me": "RO oprema za prečišćavanje vode sa preciznim filterom",
    "sv": "RO-vattenreningsutrustning med precisionsfilter",
    "sw": "Kifaa cha RO cha kusafisha maji chenye kichujio sahihi",
    "ta": "துல்லிய வடிகட்டியுடன் RO நீர் சுத்திகரிப்பு உபகரணம்",
    "tg": "Таҷҳизоти RO барои тозакунии об бо филтри дақиқ",
    "th": "อุปกรณ์ RO กรองน้ำพร้อมไส้กรองละเอียด",
    "tk": "Takyk süzgüçli RO suw arassalaýjy enjam",
    "tl": "Kagamitang RO na panlinis ng tubig na may presisyong filter",
    "tr": "Hassas filtreli RO su arıtma ekipmanı",
    "uk": "RO обладнання для очищення води з прецизійним фільтром",
    "ur": "پریسیژن فلٹر RO پانی صاف کرنے کا سامان",
    "uz": "Aniq filtrli RO suv tozalash uskunasi",
    "vi": "Thiết bị RO lọc nước với bộ lọc tinh",
    "zu": "Imishini ye-RO yokuhlanza amanzi enesihlungi esinembayo",
}


TREATMENT_VALUES = {
    "af": "Presisiefilter + RO",
    "ar": "فلتر دقيق + RO",
    "az": "Dəqiq filtr + RO",
    "bg": "Прецизен филтър + RO",
    "bn": "প্রিসিশন ফিল্টার + RO",
    "bs": "Precizni filter + RO",
    "cs": "Jemný filtr + RO",
    "da": "Præcisionsfilter + RO",
    "de": "Feinfilter + RO",
    "el": "Φίλτρο ακριβείας + RO",
    "en": "Precision filter + RO",
    "es": "Filtro de precisión + RO",
    "et": "Täppisfilter + RO",
    "fa": "فیلتر دقیق + RO",
    "fi": "Tarkkuussuodatin + RO",
    "fr": "Filtre de précision + RO",
    "ha": "Matatar daidaito + RO",
    "he": "מסנן מדויק + RO",
    "hi": "प्रिसिजन फिल्टर + RO",
    "hr": "Precizni filtar + RO",
    "hu": "Finomszűrő + RO",
    "hy": "Ճշգրիտ ֆիլտր + RO",
    "id": "Filter presisi + RO",
    "it": "Filtro di precisione + RO",
    "ja": "精密フィルター + RO",
    "ka": "ზუსტი ფილტრი + RO",
    "kk": "Дәл сүзгі + RO",
    "ko": "정밀 필터 + RO",
    "ku": "Parzûna hûr + RO",
    "ky": "Так чыпка + RO",
    "lt": "Tikslusis filtras + RO",
    "lv": "Precīzais filtrs + RO",
    "ms": "Penapis ketepatan + RO",
    "nl": "Precisiefilter + RO",
    "no": "Presisjonsfilter + RO",
    "pl": "Filtr dokładny + RO",
    "pt": "Filtro de precisão + RO",
    "ro": "Filtru de precizie + RO",
    "ru": "Прецизионный фильтр + RO",
    "sk": "Jemný filter + RO",
    "sl": "Fini filter + RO",
    "sq": "Filtër preciz + RO",
    "sr": "Прецизни филтер + RO",
    "sr-me": "Precizni filter + RO",
    "sv": "Precisionsfilter + RO",
    "sw": "Kichujio sahihi + RO",
    "ta": "துல்லிய வடிகட்டி + RO",
    "tg": "Филтри дақиқ + RO",
    "th": "ไส้กรองละเอียด + RO",
    "tk": "Takyk süzgüç + RO",
    "tl": "Presisyong filter + RO",
    "tr": "Hassas filtre + RO",
    "uk": "Прецизійний фільтр + RO",
    "ur": "پریسیژن فلٹر + RO",
    "uz": "Aniq filtr + RO",
    "vi": "Bộ lọc tinh + RO",
    "zu": "Isihlungi esinembayo + RO",
}


FEED_WATER_VALUES = {
    "af": "Munisipale kraanwater",
    "ar": "مياه الصنبور البلدية",
    "az": "Bələdiyyə kran suyu",
    "bg": "Общинска водопроводна вода",
    "bn": "পৌরসভার কলের পানি",
    "bs": "Gradska voda iz vodovoda",
    "cs": "Městská vodovodní voda",
    "da": "Kommunalt ledningsvand",
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
    "hi": "नगरपालिका नल जल",
    "hr": "Gradska vodovodna voda",
    "hu": "Települési vezetékes víz",
    "hy": "Քաղաքային ծորակի ջուր",
    "id": "Air PDAM",
    "it": "Acqua di rete municipale",
    "ja": "市政水道水",
    "ka": "მუნიციპალური ონკანის წყალი",
    "kk": "Қалалық су құбыры суы",
    "ko": "시 상수도 수돗물",
    "ku": "Ava şaredariyê ya kranê",
    "ky": "Муниципалдык кран суусу",
    "lt": "Savivaldybės vandentiekio vanduo",
    "lv": "Pašvaldības krāna ūdens",
    "ms": "Air paip perbandaran",
    "nl": "Gemeentelijk leidingwater",
    "no": "Kommunalt springvann",
    "pl": "Woda wodociągowa miejska",
    "pt": "Água municipal da rede",
    "ro": "Apă municipală de la rețea",
    "ru": "Муниципальная водопроводная вода",
    "sk": "Mestská vodovodná voda",
    "sl": "Mestna vodovodna voda",
    "sq": "Ujë rubineti komunal",
    "sr": "Градска водоводна вода",
    "sr-me": "Gradska vodovodna voda",
    "sv": "Kommunalt kranvatten",
    "sw": "Maji ya bomba ya manispaa",
    "ta": "நகராட்சி குழாய் நீர்",
    "tg": "Оби лӯлаи шаҳрӣ",
    "th": "น้ำประปาเทศบาล",
    "tk": "Şäher kran suwy",
    "tl": "Tubig sa gripo ng munisipyo",
    "tr": "Belediye şebeke suyu",
    "uk": "Муніципальна водопровідна вода",
    "ur": "میونسپل نل کا پانی",
    "uz": "Shahar vodoprovod suvi",
    "vi": "Nước máy đô thị",
    "zu": "Amanzi kampompi kamasipala",
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
    encoded = "Precision%20Filter%20RO%20Water%20Purification%20Equipment%20250-1000Lph"
    return text.replace(
        "Commercial%20Central%20RO%20Water%20Purification%20Equipment%20250-500Lph",
        encoded,
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
            "product-slim-reverse-osmosis-water-purification-equipment-250-500lph.html",
            "product-single-tank-big-blue-pp-ro-equipment-250-500lph.html",
            "product-single-tank-pretreatment-ro-equipment-250-500lph.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "commercial-central-ro-water-purification-equipment-250-500lph"),
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
            "Precision filter plus RO purification",
            "250-1000 L/h purified water flow",
            "Designed for municipal tap water",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Municipal tap-water purification for offices, shops, schools, clinics, commercial kitchens and compact drinking-water projects.",
        "related": [
            "commercial-central-ro-water-purification-equipment-250-500lph",
            "slim-reverse-osmosis-water-purification-equipment-250-500lph",
            "single-tank-big-blue-pp-ro-equipment-250-500lph",
            "six-housing-ro-equipment-with-pure-water-tank-250-1000lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Precision Filter RO Water Purification Equipment 250-1000 L/h: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    missing = [lang for lang in DUAL_GLOBALS["dirs"]() if lang not in NAME_PREFIXES or lang not in TREATMENT_VALUES or lang not in FEED_WATER_VALUES]
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


if __name__ == "__main__":
    main()
