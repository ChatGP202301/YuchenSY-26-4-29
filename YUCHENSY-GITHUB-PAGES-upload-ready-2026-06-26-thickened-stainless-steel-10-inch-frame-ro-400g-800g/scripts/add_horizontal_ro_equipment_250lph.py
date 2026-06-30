#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add horizontal RO water purification equipment across all languages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_simple_type_ro_equipment_250_1000lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FLOW_UNITS = BASE["FLOW_UNITS"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-horizontal-reverse-osmosis-water-purification-equipment-250lph.html"
PRODUCT_ID = "horizontal-reverse-osmosis-water-purification-equipment-250lph"
MAIN_IMAGE = "horizontal-reverse-osmosis-water-purification-equipment-250lph-oem.webp"
IMAGE_WIDTH = 932
IMAGE_HEIGHT = 440
AFTER_SLUG = "product-simple-type-reverse-osmosis-water-purification-equipment-250-1000lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Horisontale RO-water suiweringstoerusting",
    "ar": "معدات RO أفقية لتنقية المياه",
    "az": "Üfüqi RO su təmizləmə avadanlığı",
    "bg": "Хоризонтално RO оборудване за пречистване на вода",
    "bn": "অনুভূমিক RO পানি বিশুদ্ধকরণ সরঞ্জাম",
    "bs": "Horizontalna RO oprema za prečišćavanje vode",
    "cs": "Horizontální RO zařízení na úpravu vody",
    "da": "Horisontalt RO-vandrensningsanlæg",
    "de": "Horizontale RO-Wasseraufbereitungsanlage",
    "el": "Οριζόντιος εξοπλισμός RO για καθαρισμό νερού",
    "en": "Horizontal Reverse Osmosis Water Purification Equipment",
    "es": "Equipo RO horizontal para purificación de agua",
    "et": "Horisontaalne RO veepuhastusseade",
    "fa": "دستگاه افقی RO برای تصفیه آب",
    "fi": "Vaakasuuntainen RO-vedenpuhdistuslaitteisto",
    "fr": "Équipement RO horizontal de purification d’eau",
    "ha": "Na'urar RO ta kwance don tace ruwa",
    "he": "ציוד RO אופקי לטיהור מים",
    "hi": "क्षैतिज RO जल शुद्धिकरण उपकरण",
    "hr": "Horizontalna RO oprema za pročišćavanje vode",
    "hu": "Vízszintes RO víztisztító berendezés",
    "hy": "Հորիզոնական RO ջրի մաքրման սարքավորում",
    "id": "Peralatan RO horizontal untuk pemurnian air",
    "it": "Impianto RO orizzontale per purificazione dell'acqua",
    "ja": "横型RO浄水装置",
    "ka": "ჰორიზონტალური RO წყლის გამწმენდი მოწყობილობა",
    "kk": "Көлденең RO су тазарту жабдығы",
    "ko": "수평형 RO 정수 장비",
    "ku": "Amûra RO ya asoyî ji bo paqijkirina avê",
    "ky": "Горизонталдуу RO суу тазалоо жабдыгы",
    "lt": "Horizontalioji RO vandens valymo įranga",
    "lv": "Horizontāla RO ūdens attīrīšanas iekārta",
    "ms": "Peralatan RO mendatar untuk penulenan air",
    "nl": "Horizontale RO-waterzuiveringsinstallatie",
    "no": "Horisontalt RO-vannrenseanlegg",
    "pl": "Poziome urządzenie RO do uzdatniania wody",
    "pt": "Equipamento RO horizontal de purificação de água",
    "ro": "Echipament RO orizontal pentru purificarea apei",
    "ru": "Горизонтальное RO-оборудование для очистки воды",
    "sk": "Horizontálne RO zariadenie na úpravu vody",
    "sl": "Horizontalna RO oprema za čiščenje vode",
    "sq": "Pajisje RO horizontale për pastrimin e ujit",
    "sr": "Хоризонтална RO опрема за пречишћавање воде",
    "sr-me": "Horizontalna RO oprema za prečišćavanje vode",
    "sv": "Horisontell RO-vattenreningsutrustning",
    "sw": "Kifaa cha RO cha mlalo cha kusafisha maji",
    "ta": "கிடைமட்ட RO நீர் சுத்திகரிப்பு உபகரணம்",
    "tg": "Таҷҳизоти уфуқии RO барои тозакунии об",
    "th": "อุปกรณ์ RO แนวนอนสำหรับกรองน้ำ",
    "tk": "Gorizontal RO suw arassalaýjy enjam",
    "tl": "Pahalang na kagamitang RO para sa paglilinis ng tubig",
    "tr": "Yatay tip RO su arıtma ekipmanı",
    "uk": "Горизонтальне RO обладнання для очищення води",
    "ur": "افقی RO پانی صاف کرنے کا سامان",
    "uz": "Gorizontal RO suv tozalash uskunasi",
    "vi": "Thiết bị RO lọc nước dạng ngang",
    "zu": "Imishini ye-RO evundlile yokuhlanza amanzi",
}


TREATMENT_VALUES = {
    "af": "10-duim grootdeursnee PP + 20-duim grootdeursnee katoen-koolstof saamgestelde filter + RO",
    "ar": "PP كبير القطر مقاس 10 بوصات + فلتر مركب من القطن والكربون كبير القطر مقاس 20 بوصة + RO",
    "az": "10 düymlük böyük diametrli PP + 20 düymlük böyük diametrli pambıq-karbon kompozit filtr + RO",
    "bg": "10-инчов PP с голям диаметър + 20-инчов памучно-въглероден композитен филтър с голям диаметър + RO",
    "bn": "10 ইঞ্চি বড় ব্যাসের PP + 20 ইঞ্চি বড় ব্যাসের কটন-কার্বন কম্পোজিট ফিল্টার + RO",
    "bs": "10-inčni PP velikog promjera + 20-inčni kompozitni filter pamuk-karbon velikog promjera + RO",
    "cs": "10palcový PP s velkým průměrem + 20palcový bavlněno-uhlíkový kompozitní filtr s velkým průměrem + RO",
    "da": "10-tommer PP med stor diameter + 20-tommer bomuld-kul-kompositfilter med stor diameter + RO",
    "de": "10-Zoll PP mit großem Durchmesser + 20-Zoll Baumwolle-Aktivkohle-Verbundfilter mit großem Durchmesser + RO",
    "el": "PP μεγάλης διαμέτρου 10 ιντσών + σύνθετο φίλτρο βαμβακιού-άνθρακα μεγάλης διαμέτρου 20 ιντσών + RO",
    "en": "10-inch large-diameter PP + 20-inch large-diameter cotton-carbon composite filter + RO",
    "es": "PP de gran diámetro de 10 pulgadas + filtro compuesto algodón-carbón de gran diámetro de 20 pulgadas + RO",
    "et": "10-tolline suure läbimõõduga PP + 20-tolline suure läbimõõduga puuvill-süsinik komposiitfilter + RO",
    "fa": "PP ده اینچ با قطر بزرگ + فیلتر کامپوزیت پنبه-کربن بیست اینچ با قطر بزرگ + RO",
    "fi": "10 tuuman suurihalkaisijainen PP + 20 tuuman suurihalkaisijainen puuvilla-hiili-komposiittisuodatin + RO",
    "fr": "PP grand diamètre 10 pouces + filtre composite coton-charbon grand diamètre 20 pouces + RO",
    "ha": "PP mai babban diamita inci 10 + matatar hadadden auduga-da-carbon mai babban diamita inci 20 + RO",
    "he": "PP בקוטר גדול 10 אינץ׳ + מסנן מרוכב כותנה-פחם בקוטר גדול 20 אינץ׳ + RO",
    "hi": "10 इंच बड़े व्यास वाला PP + 20 इंच बड़े व्यास वाला कॉटन-कार्बन कंपोजिट फिल्टर + RO",
    "hr": "10-inčni PP velikog promjera + 20-inčni kompozitni filtar pamuk-ugljen velikog promjera + RO",
    "hu": "10 hüvelykes nagy átmérőjű PP + 20 hüvelykes nagy átmérőjű pamut-szén kompozit szűrő + RO",
    "hy": "10 դյույմ մեծ տրամագծի PP + 20 դյույմ մեծ տրամագծի բամբակ-ածխային կոմպոզիտ ֆիլտր + RO",
    "id": "PP diameter besar 10 inci + filter komposit kapas-karbon diameter besar 20 inci + RO",
    "it": "PP da 10 pollici a grande diametro + filtro composito cotone-carbone da 20 pollici a grande diametro + RO",
    "ja": "10インチ大径PP + 20インチ大径コットン・カーボン複合フィルター + RO",
    "ka": "10 დუიმიანი დიდი დიამეტრის PP + 20 დუიმიანი დიდი დიამეტრის ბამბა-ნახშირბადის კომპოზიტური ფილტრი + RO",
    "kk": "10 дюймдік үлкен диаметрлі PP + 20 дюймдік үлкен диаметрлі мақта-көмір композит сүзгісі + RO",
    "ko": "10인치 대구경 PP + 20인치 대구경 면-카본 복합 필터 + RO",
    "ku": "PP ya 10 inç bi qutri mezin + parzûna kompozît a pembû-karbonê ya 20 inç bi qutri mezin + RO",
    "ky": "10 дюймдук чоң диаметрдүү PP + 20 дюймдук чоң диаметрдүү пахта-көмүр композит чыпкасы + RO",
    "lt": "10 colių didelio skersmens PP + 20 colių didelio skersmens medvilnės-anglies kompozitinis filtras + RO",
    "lv": "10 collu liela diametra PP + 20 collu liela diametra kokvilnas-oglekļa kompozītfiltrs + RO",
    "ms": "PP diameter besar 10 inci + penapis komposit kapas-karbon diameter besar 20 inci + RO",
    "nl": "10 inch PP met grote diameter + 20 inch katoen-koolstof composietfilter met grote diameter + RO",
    "no": "10-tommers PP med stor diameter + 20-tommers bomull-karbon komposittfilter med stor diameter + RO",
    "pl": "PP 10 cali o dużej średnicy + kompozytowy filtr bawełniano-węglowy 20 cali o dużej średnicy + RO",
    "pt": "PP de grande diâmetro de 10 polegadas + filtro composto algodão-carvão de grande diâmetro de 20 polegadas + RO",
    "ro": "PP de 10 inci cu diametru mare + filtru compozit bumbac-carbon de 20 inci cu diametru mare + RO",
    "ru": "10-дюймовый PP большого диаметра + 20-дюймовый хлопково-угольный композитный фильтр большого диаметра + RO",
    "sk": "10-palcový PP s veľkým priemerom + 20-palcový bavlneno-uhlíkový kompozitný filter s veľkým priemerom + RO",
    "sl": "10-palčni PP velikega premera + 20-palčni kompozitni filter bombaž-oglje velikega premera + RO",
    "sq": "PP me diametër të madh 10 inç + filtër kompozit pambuk-karbon me diametër të madh 20 inç + RO",
    "sr": "PP великог пречника од 10 инча + композитни филтер памук-угљеник великог пречника од 20 инча + RO",
    "sr-me": "PP velikog prečnika od 10 inča + kompozitni filter pamuk-ugljenik velikog prečnika od 20 inča + RO",
    "sv": "10-tums PP med stor diameter + 20-tums bomull-kol-kompositfilter med stor diameter + RO",
    "sw": "PP ya kipenyo kikubwa inchi 10 + kichujio cha mchanganyiko wa pamba-na-kaboni kipenyo kikubwa inchi 20 + RO",
    "ta": "10 அங்குல பெரிய விட்ட PP + 20 அங்குல பெரிய விட்ட பருத்தி-கார்பன் கூட்டு வடிகட்டி + RO",
    "tg": "PP-и 10 дюймаи диаметри калон + филтри композитии пахта-карбони 20 дюймаи диаметри калон + RO",
    "th": "PP เส้นผ่านศูนย์กลางใหญ่ 10 นิ้ว + ไส้กรองคอมโพสิตฝ้าย-คาร์บอนเส้นผ่านศูนย์กลางใหญ่ 20 นิ้ว + RO",
    "tk": "10 dýuým uly diametrli PP + 20 dýuým uly diametrli pagta-karbon birleşdirilen süzgüç + RO",
    "tl": "PP na 10 pulgada na malaking diyametro + kompositong filter na bulak-karbon na 20 pulgada na malaking diyametro + RO",
    "tr": "10 inç büyük çaplı PP + 20 inç büyük çaplı pamuk-karbon kompozit filtre + RO",
    "uk": "10-дюймовий PP великого діаметра + 20-дюймовий бавовняно-вугільний композитний фільтр великого діаметра + RO",
    "ur": "10 انچ بڑے قطر والا PP + 20 انچ بڑے قطر والا کپاس-کاربن کمپوزٹ فلٹر + RO",
    "uz": "10 dyuymli katta diametrli PP + 20 dyuymli katta diametrli paxta-ko‘mir kompozit filtri + RO",
    "vi": "PP đường kính lớn 10 inch + lõi lọc composite bông-than đường kính lớn 20 inch + RO",
    "zu": "PP engu-10 intshi enobubanzi obukhulu + isihlungi esiyinhlanganisela ukotini-nekhabhoni engu-20 intshi enobubanzi obukhulu + RO",
}


def flow_value(lang: str) -> str:
    return f"250 {FLOW_UNITS.get(lang, FLOW_UNITS['en'])}"


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
    return text.replace(
        "Simple%20Type%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250-1000Lph",
        "Horizontal%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250Lph",
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
            "product-precision-filter-ro-water-purification-equipment-250-1000lph.html",
            "product-single-tank-integrated-ro-water-purification-supply-equipment-250-500lph.html",
            "product-commercial-central-ro-water-purification-equipment-250-500lph.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "simple-type-reverse-osmosis-water-purification-equipment-250-1000lph"),
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
            "Horizontal cabinet layout for compact commercial installation",
            "10-inch large-diameter PP pretreatment",
            "20-inch large-diameter cotton-carbon composite filtration before RO",
            "250 L/h purified water flow",
            "Designed for municipal tap water at 0.1-0.4 MPa",
        ],
        "applications": "Horizontal commercial RO purification for municipal tap water in shops, offices, restaurants, clinics and compact drinking-water projects.",
        "related": [
            "simple-type-reverse-osmosis-water-purification-equipment-250-1000lph",
            "precision-filter-ro-water-purification-equipment-250-1000lph",
            "commercial-central-ro-water-purification-equipment-250-500lph",
            "slim-reverse-osmosis-water-purification-equipment-250-500lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Horizontal Reverse Osmosis Water Purification Equipment 250 L/h: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
    DUAL_GLOBALS["update_products_page"] = update_products_page
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()
    for lang in DUAL_GLOBALS["dirs"]():
        fix_related_cards(lang)


if __name__ == "__main__":
    main()
