#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add three-tank pretreatment integrated skid RO equipment across all language pages."""

from __future__ import annotations

import json
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DUAL = runpy.run_path(str(ROOT / "scripts" / "add_dual_tank_pretreatment_integrated_skid_ro_product.py"))
DUAL_GLOBALS = DUAL["main"].__globals__
ORIGINAL_BUILD_MAIN = DUAL_GLOBALS["build_main"]

NEW_SLUG = "product-three-tank-pretreatment-integrated-skid-ro-equipment.html"
PRODUCT_ID = "three-tank-pretreatment-integrated-skid-ro-equipment"
MAIN_IMAGE = "three-tank-pretreatment-integrated-skid-ro-equipment-1000l-3000l-oem.webp"
IMAGE_WIDTH = 958
IMAGE_HEIGHT = 724
AFTER_SLUG = "product-dual-tank-pretreatment-integrated-skid-ro-equipment.html"
TODAY = "2026-06-21"


COUNT_REPLACEMENTS = {
    "af": [("Dubbeltenk", "Drietenk"), ("dubbeltenk", "drietenk")],
    "ar": [("بخزانين", "بثلاثة خزانات")],
    "az": [("İki çənli", "Üç çənli"), ("iki çənli", "üç çənli")],
    "bg": [("двуколонна", "триколонна"), ("двуколонной", "триколонной")],
    "bn": [("দুই ট্যাংক", "তিন ট্যাংক")],
    "bs": [("dvotankovskim predtretmanom", "predtretmanom s tri tanka")],
    "cs": [("dvounádobovou", "třínádobovou")],
    "da": [("to-tanks", "tre-tanks")],
    "de": [("Zweitank", "Dreitank")],
    "el": [("δύο δεξαμενών", "τριών δεξαμενών")],
    "en": [("Dual-Tank", "Three-Tank"), ("Dual-tank", "Three-tank"), ("dual-tank", "three-tank"), ("two tanks", "three tanks")],
    "es": [("dos tanques", "tres tanques")],
    "et": [("Kahe paagiga", "Kolme paagiga"), ("kahe paagiga", "kolme paagiga")],
    "fa": [("دو مخزن", "سه مخزن")],
    "fi": [("Kahden säiliön", "Kolmen säiliön"), ("kahden säiliön", "kolmen säiliön")],
    "fr": [("deux cuves", "trois cuves")],
    "ha": [("tankuna biyu", "tankuna uku"), ("tankuna biyu", "tankuna uku")],
    "he": [("בשני מכלים", "בשלושה מכלים")],
    "hi": [("दो टैंक", "तीन टैंक")],
    "hr": [("dvospremničkom predobradom", "predobradom s tri spremnika")],
    "hu": [("Két tartályos", "Három tartályos"), ("két tartályos", "három tartályos")],
    "hy": [("Երկու տարայով", "Երեք տարայով"), ("երկու տարայով", "երեք տարայով")],
    "id": [("dua tangki", "tiga tangki")],
    "it": [("due serbatoi", "tre serbatoi")],
    "ja": [("二槽式", "三槽式")],
    "ka": [("ორი ავზის", "სამი ავზის")],
    "kk": [("Екі бакты", "Үш бакты"), ("екі бакты", "үш бакты")],
    "ko": [("이중 탱크", "삼중 탱크")],
    "ku": [("du tankan", "sê tankan")],
    "ky": [("Эки бактуу", "Үч бактуу"), ("эки бактуу", "үч бактуу")],
    "lt": [("dviejų talpų", "trijų talpų")],
    "lv": [("divu tvertņu", "trīs tvertņu")],
    "ms": [("dua tangki", "tiga tangki")],
    "nl": [("tweetanks", "drietanks")],
    "no": [("to-tanks", "tre-tanks")],
    "pl": [("dwuzbiornikowym", "trójzbiornikowym")],
    "pt": [("dois tanques", "três tanques")],
    "ro": [("două tancuri", "trei tancuri")],
    "ru": [("Двухколонная", "Трехколонная"), ("двухколонной", "трехколонной")],
    "sk": [("dvojtankovou", "trojtankovou")],
    "sl": [("dvorezervoarsko predobdelavo", "predobdelavo s tremi rezervoarji")],
    "sq": [("dy depozita", "tri depozita")],
    "sr": [("двотанковским предтретманом", "предтретманом са три танка")],
    "sr-me": [("dvotankovskim predtretmanom", "predtretmanom sa tri tanka")],
    "sv": [("tvåtanks", "tretanks")],
    "sw": [("matenki mawili", "matenki matatu")],
    "ta": [("இரண்டு தொட்டி", "மூன்று தொட்டி")],
    "tg": [("ду бак", "се бак")],
    "th": [("สองถัง", "สามถัง")],
    "tk": [("Iki bakly", "Üç bakly"), ("iki bakly", "üç bakly")],
    "tl": [("dalawang tangke", "tatlong tangke")],
    "tr": [("İki tank", "Üç tank"), ("iki tank", "üç tank")],
    "uk": [("двобаковою", "трибаковою")],
    "ur": [("دو ٹینک", "تین ٹینک")],
    "uz": [("Ikki bakli", "Uch bakli"), ("ikki bakli", "uch bakli")],
    "vi": [("hai bồn", "ba bồn")],
    "zu": [("amathangi amabili", "amathangi amathathu")],
}


SOFTENERS = {
    "af": "outomatiese versagtingstenk",
    "ar": "وحدة تليين أوتوماتيكية",
    "az": "avtomatik yumşaltma çəni",
    "bg": "автоматичен омекотител",
    "bn": "স্বয়ংক্রিয় সফটেনিং ইউনিট",
    "bs": "automatski omekšivač",
    "cs": "automatický změkčovač",
    "da": "automatisk blødgøringstank",
    "de": "automatischer Enthärter",
    "el": "αυτόματος αποσκληρυντής",
    "en": "automatic softening tank",
    "es": "ablandador automático",
    "et": "automaatne pehmenduspaak",
    "fa": "مخزن سختی‌گیر خودکار",
    "fi": "automaattinen pehmennyssäiliö",
    "fr": "adoucisseur automatique",
    "ha": "tankin laushi na atomatik",
    "he": "מרכך מים אוטומטי",
    "hi": "ऑटोमैटिक सॉफ्टनर",
    "hr": "automatski omekšivač",
    "hu": "automatikus lágyító tartály",
    "hy": "ավտոմատ փափկեցման տարա",
    "id": "tangki pelembut otomatis",
    "it": "addolcitore automatico",
    "ja": "自動軟水化槽",
    "ka": "ავტომატური დამარბილებელი ავზი",
    "kk": "автоматты жұмсарту багы",
    "ko": "자동 연수 탱크",
    "ku": "tankê nermkirinê yê otomatîk",
    "ky": "автоматтык жумшартуу багы",
    "lt": "automatinė minkštinimo talpa",
    "lv": "automātiska mīkstināšanas tvertne",
    "ms": "tangki pelembut automatik",
    "nl": "automatische onthardingstank",
    "no": "automatisk bløtgjøringstank",
    "pl": "automatyczny zmiękczacz",
    "pt": "abrandador automático",
    "ro": "tanc automat de dedurizare",
    "ru": "автоматическая колонна умягчения",
    "sk": "automatická zmäkčovacia nádoba",
    "sl": "avtomatski mehčalni rezervoar",
    "sq": "zbutës automatik",
    "sr": "аутоматски омекшивач",
    "sr-me": "automatski omekšivač",
    "sv": "automatisk avhärdningstank",
    "sw": "tenki la kulainisha la moja kwa moja",
    "ta": "தானியங்கி மென்மைப்படுத்தும் தொட்டி",
    "tg": "баки нармкунии автоматӣ",
    "th": "ถังปรับน้ำอ่อนอัตโนมัติ",
    "tk": "awtomatik ýumşadyjy bak",
    "tl": "awtomatikong tangke ng pampalambot",
    "tr": "otomatik yumuşatma tankı",
    "uk": "автоматичний бак пом'якшення",
    "ur": "خودکار سافٹننگ ٹینک",
    "uz": "avtomatik yumshatish baki",
    "vi": "bồn làm mềm tự động",
    "zu": "ithangi lokuthambisa elizenzakalelayo",
}


def apply_replacements(lang: str, text: str) -> str:
    for old, new in COUNT_REPLACEMENTS.get(lang, []):
        text = text.replace(old, new)
    return text


def add_softener(treatment: str, lang: str) -> str:
    parts = [part.strip() for part in treatment.split("+")]
    if len(parts) >= 3:
        parts.insert(2, SOFTENERS[lang])
        return " + ".join(parts)
    return f"{treatment} + {SOFTENERS[lang]}"


def build_terms() -> dict[str, dict[str, str]]:
    terms: dict[str, dict[str, str]] = {}
    for lang, values in DUAL_GLOBALS["TERMS"].items():
        item = {key: apply_replacements(lang, value) for key, value in values.items()}
        item["treatment"] = add_softener(item["treatment"], lang)
        item["intro"] = item["intro"].replace(values["treatment"].replace(" + ", ", "), item["treatment"].replace(" + ", ", "))
        item["card"] = item["card"].replace(values["treatment"].replace(" + ", ", "), item["treatment"].replace(" + ", ", "))
        terms[lang] = item
    return terms


TERMS = build_terms()


def build_main(lang: str, copy: dict) -> str:
    html = ORIGINAL_BUILD_MAIN(lang, copy)
    return html.replace(
        "Dual%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
        "Three%20Tank%20Pretreatment%20Integrated%20Skid%20RO%20Equipment",
    )


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if any(item.get("id") == PRODUCT_ID for item in products):
        return
    copy = DUAL_GLOBALS["copy_for"]("en")
    insert_at = next((i + 1 for i, item in enumerate(products) if item.get("id") == "dual-tank-pretreatment-integrated-skid-ro-equipment"), 5)
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
            "Automatic sand, carbon and softening tanks",
            "Precision filter plus RO purification",
            "1000-3000 L/h purified water flow",
            "0.1-0.4 MPa feed pressure",
            "Customized frame, process and control functions",
        ],
        "applications": "Hotels, factories, schools, communities, commercial kitchens and groundwater treatment projects.",
        "related": [
            "dual-tank-pretreatment-integrated-skid-ro-equipment",
            "large-industrial-reverse-osmosis-water-treatment-equipment",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Three-Tank Pretreatment Integrated Skid RO Equipment: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    DUAL_GLOBALS["NEW_SLUG"] = NEW_SLUG
    DUAL_GLOBALS["PRODUCT_ID"] = PRODUCT_ID
    DUAL_GLOBALS["MAIN_IMAGE"] = MAIN_IMAGE
    DUAL_GLOBALS["IMAGE_WIDTH"] = IMAGE_WIDTH
    DUAL_GLOBALS["IMAGE_HEIGHT"] = IMAGE_HEIGHT
    DUAL_GLOBALS["AFTER_SLUG"] = AFTER_SLUG
    DUAL_GLOBALS["TODAY"] = TODAY
    DUAL_GLOBALS["TERMS"] = TERMS
    DUAL_GLOBALS["build_main"] = build_main
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()


if __name__ == "__main__":
    main()
