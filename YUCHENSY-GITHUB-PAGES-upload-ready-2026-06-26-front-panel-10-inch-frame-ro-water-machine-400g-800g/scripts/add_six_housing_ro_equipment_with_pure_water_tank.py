#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add six-housing RO equipment with pure water tank across all language pages."""

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

NEW_SLUG = "product-six-housing-ro-equipment-with-pure-water-tank-250-1000lph.html"
PRODUCT_ID = "six-housing-ro-equipment-with-pure-water-tank-250-1000lph"
MAIN_IMAGE = "six-housing-ro-equipment-with-pure-water-tank-250l-1000l-open-oem.webp"
SECOND_IMAGE = "six-housing-ro-equipment-with-pure-water-tank-250l-1000l-stainless-cabinet-oem.webp"
IMAGE_WIDTH = 526
IMAGE_HEIGHT = 702
SECOND_IMAGE_WIDTH = 540
SECOND_IMAGE_HEIGHT = 744
AFTER_SLUG = "product-dual-tank-pretreatment-ro-equipment-250-1000lph.html"
TODAY = "2026-06-21"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Sesbehuizing-RO-toerusting met skoonwatertenk",
    "ar": "معدات RO بستة هياكل فلتر مع خزان مياه نقية",
    "az": "Təmiz su çəni olan altı korpuslu RO avadanlığı",
    "bg": "RO оборудване с шест корпуса и резервоар за чиста вода",
    "bn": "বিশুদ্ধ পানির ট্যাংকসহ ছয়-হাউজিং RO সরঞ্জাম",
    "bs": "RO oprema sa šest kućišta i rezervoarom čiste vode",
    "cs": "RO zařízení se šesti pouzdry a nádrží na čistou vodu",
    "da": "RO-anlæg med seks filterhuse og rentvandstank",
    "de": "RO-Anlage mit sechs Filtergehäusen und Reinwassertank",
    "el": "Εξοπλισμός RO έξι κελυφών με δεξαμενή καθαρού νερού",
    "en": "Six-Housing Reverse Osmosis Equipment with Pure Water Tank",
    "es": "Equipo RO de seis carcasas con tanque de agua pura",
    "et": "Kuue korpusega RO seade puhta vee paagiga",
    "fa": "دستگاه RO شش محفظه‌ای با مخزن آب خالص",
    "fi": "Kuusikoteloisen RO-laitteisto puhdasvesisäiliöllä",
    "fr": "Équipement RO à six carters avec réservoir d'eau pure",
    "ha": "Na'urar RO mai gidajen tacewa shida da tankin ruwa mai tsabta",
    "he": "ציוד RO עם שישה בתי מסנן ומכל מים טהורים",
    "hi": "शुद्ध जल टैंक वाला छह-हाउसिंग RO उपकरण",
    "hr": "RO oprema sa šest kućišta i spremnikom čiste vode",
    "hu": "Hat szűrőházas RO berendezés tisztavíz-tartállyal",
    "hy": "Վեց պատյանով RO սարքավորում մաքուր ջրի բաքով",
    "id": "Peralatan RO enam rumah filter dengan tangki air murni",
    "it": "Impianto RO a sei alloggiamenti con serbatoio acqua pura",
    "ja": "純水タンク付き6本フィルターハウジングRO装置",
    "ka": "ექვსკორპუსიანი RO მოწყობილობა სუფთა წყლის ავზით",
    "kk": "Таза су багы бар алты корпусты RO жабдығы",
    "ko": "순수 탱크가 있는 6하우징 RO 장비",
    "ku": "Amûra RO ya şeş malperên fîltreyê bi tankera ava paqij",
    "ky": "Таза суу багы бар алты корпуслуу RO жабдыгы",
    "lt": "Šešių korpusų RO įranga su švaraus vandens talpa",
    "lv": "Sešu korpusu RO iekārta ar tīra ūdens tvertni",
    "ms": "Peralatan RO enam perumah dengan tangki air tulen",
    "nl": "RO-installatie met zes filterhuizen en schoonwatertank",
    "no": "RO-anlegg med seks filterhus og rentvannstank",
    "pl": "Urządzenie RO z sześcioma obudowami i zbiornikiem wody czystej",
    "pt": "Equipamento RO de seis carcaças com tanque de água pura",
    "ro": "Echipament RO cu șase carcase și rezervor de apă pură",
    "ru": "RO-оборудование с шестью корпусами и баком чистой воды",
    "sk": "RO zariadenie so šiestimi puzdrami a nádržou na čistú vodu",
    "sl": "RO oprema s šestimi ohišji in rezervoarjem čiste vode",
    "sq": "Pajisje RO me gjashtë strehë filtri dhe rezervuar uji të pastër",
    "sr": "RO опрема са шест кућишта и резервоаром чисте воде",
    "sr-me": "RO oprema sa šest kućišta i rezervoarom čiste vode",
    "sv": "RO-utrustning med sex filterhus och rentvattentank",
    "sw": "Kifaa cha RO chenye nyumba sita za vichujio na tanki la maji safi",
    "ta": "தூய நீர் தொட்டியுடன் ஆறு ஹவுசிங் கொண்ட RO உபகரணம்",
    "tg": "Таҷҳизоти RO бо шаш корпус ва зарфи оби тоза",
    "th": "อุปกรณ์ RO หกกระบอกพร้อมถังน้ำบริสุทธิ์",
    "tk": "Arassa suw baky bolan alty korpusly RO enjamy",
    "tl": "Kagamitang RO na may anim na sisidlan ng filter at tangke ng purong tubig",
    "tr": "Saf su tanklı altı filtre yuvalı RO ekipmanı",
    "uk": "RO обладнання з шістьма корпусами та баком чистої води",
    "ur": "خالص پانی کے ٹینک کے ساتھ چھ ہاؤسنگ RO سامان",
    "uz": "Toza suv baki bilan olti korpusli RO uskunasi",
    "vi": "Thiết bị RO sáu cốc lọc với bồn nước tinh khiết",
    "zu": "Imishini ye-RO enezindlu eziyisithupha nezitsha zamanzi ahlanzekile",
}


TREATMENT_VALUE = "20″ PP + 20″ CTO + 20″ PP + RO"


def flow_value(lang: str) -> str:
    return f"250-1000 {FLOW_UNITS.get(lang, FLOW_UNITS['en'])}"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in NAME_PREFIXES:
        raise KeyError(f"No product name translation for {lang}")
    name = f"{NAME_PREFIXES[lang]} {flow_value(lang)}"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[2] = TREATMENT_VALUE
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
    text = text.replace(
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Six%20Housing%20RO%20Equipment%20with%20Pure%20Water%20Tank",
    )
    text = text.replace(
        "Dual%20Tank%20Pretreatment%20RO%20Equipment%20250-1000Lph",
        "Six%20Housing%20RO%20Equipment%20with%20Pure%20Water%20Tank",
    )
    gallery = (
        f'<div class="product-gallery">'
        f'<a href="../assets/products/{SECOND_IMAGE}">'
        f'<img src="../assets/products/{SECOND_IMAGE}" alt="{DUAL_GLOBALS["esc"](copy["name"])}" '
        f'loading="lazy" decoding="async" width="{SECOND_IMAGE_WIDTH}" height="{SECOND_IMAGE_HEIGHT}" />'
        f'</a></div>'
    )
    text = re.sub(
        r'(<img src="\.\./assets/products/' + re.escape(MAIN_IMAGE) + r'"[^>]*class="product-main-image" />)',
        r"\1" + gallery,
        text,
        count=1,
    )
    return text


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(ORIGINAL_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [
                f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}",
                f"https://www.yuchensy.com/assets/products/{SECOND_IMAGE}",
            ]
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = copy_for("en")
    insert_at = next(
        (i + 1 for i, item in enumerate(products) if item.get("id") == "dual-tank-pretreatment-ro-equipment-250-1000lph"),
        8,
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
            "20-inch PP + CTO + PP pretreatment",
            "RO purification with pure water tank",
            "250-1000 L/h purified water flow",
            "0.1-0.4 MPa feed pressure",
            "Custom appearance, process, configuration and functions",
        ],
        "applications": "Tap-water and groundwater purification for commercial drinking water, factories, schools, workshops and light industrial projects.",
        "related": [
            "dual-tank-pretreatment-ro-equipment-250-1000lph",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
            "dual-tank-pretreatment-integrated-skid-ro-equipment",
            "three-tank-pretreatment-integrated-skid-ro-equipment",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Six-Housing Reverse Osmosis Equipment with Pure Water Tank: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    missing = [lang for lang in DUAL_GLOBALS["dirs"]() if lang not in NAME_PREFIXES]
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
