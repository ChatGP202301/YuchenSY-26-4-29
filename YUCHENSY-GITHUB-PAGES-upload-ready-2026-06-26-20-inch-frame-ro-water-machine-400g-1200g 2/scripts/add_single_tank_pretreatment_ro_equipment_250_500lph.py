#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add single-tank pretreatment RO equipment across all language pages."""

from __future__ import annotations

import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_dual_tank_pretreatment_ro_equipment_250_1000lph.py"))
DUAL_GLOBALS = BASE["main"].__globals__["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
ORIGINAL_BUILD_MAIN = DUAL_GLOBALS["build_main"]
ORIGINAL_PRODUCT_GRAPH = DUAL_GLOBALS["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]

NEW_SLUG = "product-single-tank-pretreatment-ro-equipment-250-500lph.html"
PRODUCT_ID = "single-tank-pretreatment-ro-equipment-250-500lph"
MAIN_IMAGE = "single-tank-pretreatment-ro-water-purification-equipment-250l-500l-oem.webp"
IMAGE_WIDTH = 324
IMAGE_HEIGHT = 520
AFTER_SLUG = "product-six-housing-ro-equipment-with-pure-water-tank-250-1000lph.html"
TODAY = "2026-06-21"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Enkeltenk-voorbehandeling RO-toerusting",
    "ar": "معدات RO بمعالجة أولية بخزان واحد",
    "az": "Tək çənli əvvəlcədən təmizləməli RO avadanlığı",
    "bg": "RO оборудване с едноколонна предварителна обработка",
    "bn": "এক ট্যাংক প্রি-ট্রিটমেন্ট RO সরঞ্জাম",
    "bs": "RO oprema s jednotankovskim predtretmanom",
    "cs": "RO zařízení s jednonádobovou předúpravou",
    "da": "RO-anlæg med enkelt forbehandlingstank",
    "de": "RO-Anlage mit Eintank-Vorbehandlung",
    "el": "Εξοπλισμός RO με προεπεξεργασία μίας δεξαμενής",
    "en": "Single-Tank Pretreatment Reverse Osmosis Water Purification Equipment",
    "es": "Equipo RO con pretratamiento de un tanque",
    "et": "Ühe paagiga eeltöötlusega RO seade",
    "fa": "دستگاه RO با پیش‌تصفیه تک‌مخزن",
    "fi": "Yhden säiliön esikäsittelyllä varustettu RO-laitteisto",
    "fr": "Équipement RO avec prétraitement à une cuve",
    "ha": "Na'urar RO mai tanki ɗaya na kafin tacewa",
    "he": "ציוד RO עם טיפול מקדים במכל יחיד",
    "hi": "एकल टैंक प्री-ट्रीटमेंट RO उपकरण",
    "hr": "RO oprema s jednotankovskom predobradom",
    "hu": "Egytartályos előkezelésű RO berendezés",
    "hy": "Մեկ բաքով նախամշակմամբ RO սարքավորում",
    "id": "Peralatan RO pretreatment satu tangki",
    "it": "Impianto RO con pretrattamento a serbatoio singolo",
    "ja": "単槽前処理RO浄水装置",
    "ka": "ერთავზიანი წინასწარი დამუშავების RO მოწყობილობა",
    "kk": "Бір бакты алдын ала тазарту RO жабдығы",
    "ko": "단일 탱크 전처리 RO 정수 장비",
    "ku": "Amûra RO ya pêşparastina yek tankî",
    "ky": "Бир бактуу алдын ала тазалоо RO жабдыгы",
    "lt": "Vienos talpos pirminio valymo RO įranga",
    "lv": "Vienas tvertnes priekšattīrīšanas RO iekārta",
    "ms": "Peralatan RO pra-rawatan satu tangki",
    "nl": "RO-installatie met enkele voorbehandelingstank",
    "no": "RO-anlegg med én forbehandlingstank",
    "pl": "Urządzenie RO z jednostopniowym zbiornikiem wstępnym",
    "pt": "Equipamento RO com pré-tratamento de um tanque",
    "ro": "Echipament RO cu pretratare într-un singur rezervor",
    "ru": "RO-оборудование с одноколонной предварительной очисткой",
    "sk": "RO zariadenie s jednonádobovou predúpravou",
    "sl": "RO oprema z enorezervoarsko predobdelavo",
    "sq": "Pajisje RO me paratrajtim me një rezervuar",
    "sr": "RO опрема са једнорезервоарском предобрадом",
    "sr-me": "RO oprema sa jednim rezervoarom za predtretman",
    "sv": "RO-utrustning med enkel förbehandlingstank",
    "sw": "Kifaa cha RO chenye tanki moja la maandalizi ya awali",
    "ta": "ஒற்றை தொட்டி முன்சிகிச்சையுடன் RO உபகரணம்",
    "tg": "Таҷҳизоти RO бо пештозакунии якзарфа",
    "th": "อุปกรณ์ RO พร้อมถังปรับสภาพน้ำหนึ่งถัง",
    "tk": "Bir bakly öňünden arassalaýjy RO enjamy",
    "tl": "Kagamitang RO na may isang tangke ng paunang pagsala",
    "tr": "Tek tank ön arıtmalı RO ekipmanı",
    "uk": "RO обладнання з одноколонною попередньою очисткою",
    "ur": "ایک ٹینک پری ٹریٹمنٹ RO سامان",
    "uz": "Bir bakli oldindan tozalash RO uskunasi",
    "vi": "Thiết bị RO tiền xử lý một bồn",
    "zu": "Imishini ye-RO enethangi elilodwa lokulungiselela amanzi",
}


TREATMENT_VALUES = {
    "af": "Outomatiese sand-koolstoftenk + 20″ PP + 20″ PP + RO",
    "ar": "خزان رمل وكربون أوتوماتيكي + PP مقاس 20 بوصة + PP مقاس 20 بوصة + RO",
    "az": "Avtomatik qum-karbon çəni + 20 düymlük PP + 20 düymlük PP + RO",
    "bg": "Автоматичен пясъчно-въглероден съд + 20-инчов PP + 20-инчов PP + RO",
    "bn": "স্বয়ংক্রিয় বালু-কার্বন ট্যাংক + 20 ইঞ্চি PP + 20 ইঞ্চি PP + RO",
    "bs": "Automatski pješčano-karbonski tank + 20-inčni PP + 20-inčni PP + RO",
    "cs": "Automatická pískovo-uhlíková nádoba + 20palcový PP + 20palcový PP + RO",
    "da": "Automatisk sand-kultank + 20-tommer PP + 20-tommer PP + RO",
    "de": "Automatischer Sand-Aktivkohlebehälter + 20-Zoll PP + 20-Zoll PP + RO",
    "el": "Αυτόματη δεξαμενή άμμου-άνθρακα + PP 20 ιντσών + PP 20 ιντσών + RO",
    "en": "Automatic sand-carbon tank + 20-inch PP + 20-inch PP + RO",
    "es": "Tanque automático de arena y carbón + PP de 20 pulgadas + PP de 20 pulgadas + RO",
    "et": "Automaatne liiva-söepaak + 20-tolline PP + 20-tolline PP + RO",
    "fa": "مخزن شنی-کربنی خودکار + PP بیست اینچ + PP بیست اینچ + RO",
    "fi": "Automaattinen hiekka-hiilisäiliö + PP 20 tuumaa + PP 20 tuumaa + RO",
    "fr": "Cuve automatique sable-charbon + PP 20 pouces + PP 20 pouces + RO",
    "ha": "Tankin yashi-da-carbon na atomatik + PP inci 20 + PP inci 20 + RO",
    "he": "מכל חול-פחם אוטומטי + PP בגודל 20 אינץ׳ + PP בגודל 20 אינץ׳ + RO",
    "hi": "स्वचालित रेत-कार्बन टैंक + 20 इंच PP + 20 इंच PP + RO",
    "hr": "Automatski pješčano-ugljični spremnik + 20-inčni PP + 20-inčni PP + RO",
    "hu": "Automata homok-aktívszén tartály + 20 hüvelykes PP + 20 hüvelykes PP + RO",
    "hy": "Ավտոմատ ավազ-ածխային բաք + 20 դյույմ PP + 20 դյույմ PP + RO",
    "id": "Tangki pasir-karbon otomatis + PP 20 inci + PP 20 inci + RO",
    "it": "Serbatoio automatico sabbia-carbone + PP da 20 pollici + PP da 20 pollici + RO",
    "ja": "自動砂・活性炭タンク + 20インチPP + 20インチPP + RO",
    "ka": "ავტომატური ქვიშა-ნახშირის ავზი + 20 დუიმიანი PP + 20 დუიმიანი PP + RO",
    "kk": "Автоматты құм-көмір багы + 20 дюймдік PP + 20 дюймдік PP + RO",
    "ko": "자동 모래-카본 탱크 + 20인치 PP + 20인치 PP + RO",
    "ku": "Tankera xwelî-karbonê ya xweber + PP 20 inç + PP 20 inç + RO",
    "ky": "Автоматтык кум-көмүр багы + 20 дюймдук PP + 20 дюймдук PP + RO",
    "lt": "Automatinė smėlio-anglies talpa + 20 colių PP + 20 colių PP + RO",
    "lv": "Automātiska smilšu-oglekļa tvertne + 20 collu PP + 20 collu PP + RO",
    "ms": "Tangki pasir-karbon automatik + PP 20 inci + PP 20 inci + RO",
    "nl": "Automatische zand-koolstoftank + 20-inch PP + 20-inch PP + RO",
    "no": "Automatisk sand-karbontank + 20-tommers PP + 20-tommers PP + RO",
    "pl": "Automatyczny zbiornik piaskowo-węglowy + PP 20 cali + PP 20 cali + RO",
    "pt": "Tanque automático de areia e carvão + PP de 20 polegadas + PP de 20 polegadas + RO",
    "ro": "Rezervor automat nisip-carbon + PP de 20 inci + PP de 20 inci + RO",
    "ru": "Автоматическая песчано-угольная колонна + 20-дюймовый PP + 20-дюймовый PP + RO",
    "sk": "Automatická pieskovo-uhlíková nádoba + 20-palcový PP + 20-palcový PP + RO",
    "sl": "Samodejni peščeno-ogljikov rezervoar + 20-palčni PP + 20-palčni PP + RO",
    "sq": "Rezervuar automatik rërë-karbon + PP 20 inç + PP 20 inç + RO",
    "sr": "Аутоматски песковито-угљени резервоар + PP од 20 инча + PP од 20 инча + RO",
    "sr-me": "Automatski pješčano-ugljični rezervoar + PP od 20 inča + PP od 20 inča + RO",
    "sv": "Automatisk sand-koltank + 20-tums PP + 20-tums PP + RO",
    "sw": "Tanki ya mchanga-na-kaboni ya kiotomatiki + PP inchi 20 + PP inchi 20 + RO",
    "ta": "தானியங்கி மணல்-கார்பன் தொட்டி + 20 அங்குல PP + 20 அங்குல PP + RO",
    "tg": "Зарфи худкори қум-карбон + PP-и 20 дюйм + PP-и 20 дюйм + RO",
    "th": "ถังกรองทราย-คาร์บอนอัตโนมัติ + PP 20 นิ้ว + PP 20 นิ้ว + RO",
    "tk": "Awtomatiki gum-karbon baky + 20 dýuým PP + 20 dýuým PP + RO",
    "tl": "Awtomatikong tangke ng buhangin-karbon + PP na 20 pulgada + PP na 20 pulgada + RO",
    "tr": "Otomatik kum-karbon tankı + 20 inç PP + 20 inç PP + RO",
    "uk": "Автоматична піщано-вугільна колона + 20-дюймовий PP + 20-дюймовий PP + RO",
    "ur": "خودکار ریت-کاربن ٹینک + 20 انچ PP + 20 انچ PP + RO",
    "uz": "Avtomatik qum-ko‘mir baki + 20 dyuymli PP + 20 dyuymli PP + RO",
    "vi": "Bồn cát-than tự động + PP 20 inch + PP 20 inch + RO",
    "zu": "Ithangi lesihlabathi-nekhabhoni elizenzakalelayo + PP engu-20 intshi + PP engu-20 intshi + RO",
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
    custom_sentence = values[6]
    intro = (
        f"{name}. {labels[2]}: {values[2]}. "
        f"{labels[3]}: {values[3]}. {labels[4]}: {values[4]}. "
        f"{labels[5]}: {values[5]}. {labels[6]}: {custom_sentence}."
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
        (f"{labels[5]}?", values[5]),
        (f"{labels[6]}?", values[6]),
    ]
    return copy


def build_main(lang: str, copy: dict) -> str:
    text = ORIGINAL_BUILD_MAIN(lang, copy)
    return text.replace(
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Single%20Tank%20Pretreatment%20RO%20Equipment%20250-500Lph",
    ).replace(
        "Dual%20Tank%20Pretreatment%20RO%20Equipment%20250-1000Lph",
        "Single%20Tank%20Pretreatment%20RO%20Equipment%20250-500Lph",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "six-housing-ro-equipment-with-pure-water-tank-250-1000lph"),
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
            "Automatic sand-carbon pretreatment tank",
            "20-inch PP + 20-inch PP + RO purification",
            "250-500 L/h purified water flow",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Tap-water and groundwater purification for commercial drinking water, offices, workshops, schools and light industrial projects.",
        "related": [
            "six-housing-ro-equipment-with-pure-water-tank-250-1000lph",
            "dual-tank-pretreatment-ro-equipment-250-1000lph",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
            "dual-tank-pretreatment-integrated-skid-ro-equipment",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Single-Tank Pretreatment Reverse Osmosis Water Purification Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
