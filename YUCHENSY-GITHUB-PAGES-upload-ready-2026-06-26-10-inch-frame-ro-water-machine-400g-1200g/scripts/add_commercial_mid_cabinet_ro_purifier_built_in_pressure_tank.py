#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add commercial mid-cabinet RO purifier with built-in pressure tank."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_horizontal_ro_equipment_250lph.py"))
PORTABLE = runpy.run_path(str(ROOT / "scripts" / "add_portable_custom_ro_water_purifier_400g_800g.py"))
CENTRAL = runpy.run_path(str(ROOT / "scripts" / "add_commercial_central_ro_equipment_250_500lph.py"))

DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
OPERATION_VALUES = PORTABLE["OPERATION_VALUES"]
CENTRAL_TREATMENT_VALUES = CENTRAL["TREATMENT_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g.html"
PRODUCT_ID = "commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g"
MAIN_IMAGE = "commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g-oem.webp"
IMAGE_WIDTH = 350
IMAGE_HEIGHT = 544
AFTER_SLUG = "product-commercial-central-ro-water-purification-equipment-250-500lph.html"
TODAY = "2026-06-25"
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
    "af": "Kommersiële middelkas RO-waterreiniger met ingeboude druktenk",
    "ar": "جهاز تنقية مياه RO تجاري بخزانة متوسطة مع خزان ضغط مدمج",
    "az": "Daxili təzyiq çəni olan kommersiya orta şkaflı RO su təmizləyicisi",
    "bg": "Търговски RO водопречиствател среден шкаф с вграден резервоар под налягане",
    "bn": "অন্তর্নির্মিত চাপ ট্যাংকসহ বাণিজ্যিক মাঝারি ক্যাবিনেট RO পানি বিশুদ্ধকরণ মেশিন",
    "bs": "Komercijalni RO prečistač vode u srednjem kabinetu s ugrađenim tlačnim rezervoarom",
    "cs": "Komerční RO čistička vody ve střední skříni s vestavěnou tlakovou nádrží",
    "da": "Kommerciel RO-vandrenser i mellemstort kabinet med indbygget tryktank",
    "de": "Gewerblicher RO-Wasserreiniger im Mittelschrank mit integriertem Drucktank",
    "el": "Επαγγελματικός καθαριστής νερού RO μεσαίου ερμαρίου με ενσωματωμένη δεξαμενή πίεσης",
    "en": "Commercial Mid-Cabinet RO Water Purifier with Built-In Pressure Tank",
    "es": "Purificador de agua RO comercial de gabinete mediano con tanque de presión integrado",
    "et": "Kaubanduslik keskmise kapiga RO veepuhasti sisseehitatud survepaagiga",
    "fa": "دستگاه تصفیه آب RO تجاری کابینت متوسط با مخزن فشار داخلی",
    "fi": "Kaupallinen keskikaappinen RO-vedenpuhdistin sisäänrakennetulla painesäiliöllä",
    "fr": "Purificateur d’eau RO commercial à armoire moyenne avec réservoir sous pression intégré",
    "ha": "Na'urar tace ruwan RO ta kasuwanci a matsakaicin kabad tare da tankin matsa lamba na ciki",
    "he": "מטהר מים RO מסחרי בארון בינוני עם מיכל לחץ מובנה",
    "hi": "अंतर्निर्मित प्रेशर टैंक वाला वाणिज्यिक मध्यम कैबिनेट RO जल शोधक",
    "hr": "Komercijalni RO pročišćivač vode u srednjem ormariću s ugrađenim tlačnim spremnikom",
    "hu": "Kereskedelmi közepes szekrényes RO víztisztító beépített nyomástartállyal",
    "hy": "Առևտրային միջին պահարանով RO ջրի մաքրիչ՝ ներկառուցված ճնշման բաքով",
    "id": "Pemurni air RO komersial kabinet sedang dengan tangki tekanan bawaan",
    "it": "Purificatore d’acqua RO commerciale a mobile medio con serbatoio pressurizzato integrato",
    "ja": "内蔵圧力タンク付き業務用中型キャビネットRO浄水機",
    "ka": "კომერციული საშუალო კაბინეტის RO წყლის გამწმენდი ჩაშენებული წნევის ავზით",
    "kk": "Кіріктірілген қысым багы бар коммерциялық орта шкафты RO су тазартқышы",
    "ko": "내장 압력 탱크가 있는 상업용 중형 캐비닛 RO 정수기",
    "ku": "Paqijkera ava RO ya bazirganî ya kabîneya navîn bi tanka zextê ya hundurîn",
    "ky": "Ичине орнотулган басым багы бар коммерциялык орто шкафтуу RO суу тазалагыч",
    "lt": "Komercinis vidutinės spintos RO vandens valytuvas su įmontuotu slėginiu baku",
    "lv": "Komerciāls vidēja skapja RO ūdens attīrītājs ar iebūvētu spiediena tvertni",
    "ms": "Penulen air RO komersial kabinet sederhana dengan tangki tekanan terbina dalam",
    "nl": "Commerciële middelgrote kast RO-waterzuiveraar met ingebouwde druktank",
    "no": "Kommersiell mellomskap RO-vannrenser med innebygd trykktank",
    "pl": "Komercyjny średni szafkowy oczyszczacz wody RO z wbudowanym zbiornikiem ciśnieniowym",
    "pt": "Purificador de água RO comercial de gabinete médio com tanque de pressão integrado",
    "ro": "Purificator de apă RO comercial cu dulap mediu și rezervor sub presiune integrat",
    "ru": "Коммерческий RO-очиститель воды в среднем шкафу со встроенным напорным баком",
    "sk": "Komerčný RO čistič vody v strednej skrini so zabudovanou tlakovou nádržou",
    "sl": "Komercialni RO čistilnik vode v srednji omari z vgrajenim tlačnim rezervoarjem",
    "sq": "Pastrues uji RO komercial me kabinet të mesëm dhe rezervuar presioni të integruar",
    "sr": "Комерцијални RO пречистач воде у средњем ормару са уграђеним резервоаром под притиском",
    "sr-me": "Komercijalni RO prečišćivač vode u srednjem ormaru sa ugrađenim rezervoarom pod pritiskom",
    "sv": "Kommersiell RO-vattenrenare i mellanskåp med inbyggd trycktank",
    "sw": "Kisafishaji maji cha RO cha biashara cha kabati la kati chenye tanki la shinikizo lililojengwa ndani",
    "ta": "உட்புற அழுத்த தொட்டியுடன் வணிக நடுத்தர கேபினெட் RO நீர் சுத்திகரிப்பான்",
    "tg": "Тозакунандаи оби RO-и тиҷоратии ҷевони миёна бо зарфи фишори дарунсохт",
    "th": "เครื่องกรองน้ำ RO เชิงพาณิชย์แบบตู้กลางพร้อมถังแรงดันในตัว",
    "tk": "Içindäki basyş baky bolan täjirçilik orta şkafly RO suw arassalaýjy",
    "tl": "Komersiyal na tagalinis ng tubig na RO sa katamtamang kabinet na may nakapaloob na tangke ng presyon",
    "tr": "Dahili basınç tanklı ticari orta kabin RO su arıtma cihazı",
    "uk": "Комерційний RO-очисник води в середній шафі з вбудованим напірним баком",
    "ur": "تجارتی درمیانی کابینہ والا RO پانی صاف کرنے والا آلہ، اندرونی دباؤ ٹینک کے ساتھ",
    "uz": "Ichki bosim baki bor tijorat o‘rta shkafli RO suv tozalagichi",
    "vi": "Máy lọc nước RO tủ trung thương mại có bình áp tích hợp",
    "zu": "Umshini we-RO wokuhlanza amanzi webhizinisi wekhabhinethi ephakathi onethangi lengcindezi elakhelwe ngaphakathi",
}

SIZE_LABELS = {
    "af": "Produkafmeting", "ar": "أبعاد المنتج", "az": "Məhsul ölçüsü",
    "bg": "Размер на продукта", "bn": "পণ্যের আকার", "bs": "Dimenzije proizvoda",
    "cs": "Rozměry produktu", "da": "Produktmål", "de": "Produktabmessungen",
    "el": "Διαστάσεις προϊόντος", "en": "Product Size", "es": "Dimensiones del producto",
    "et": "Toote mõõtmed", "fa": "ابعاد محصول", "fi": "Tuotteen mitat",
    "fr": "Dimensions du produit", "ha": "Girman samfur", "he": "מידות המוצר",
    "hi": "उत्पाद आयाम", "hr": "Dimenzije proizvoda", "hu": "Termék mérete",
    "hy": "Ապրանքի չափսեր", "id": "Dimensi produk", "it": "Dimensioni del prodotto",
    "ja": "製品寸法", "ka": "პროდუქტის ზომები", "kk": "Өнім өлшемі",
    "ko": "제품 크기", "ku": "Mezinahiya hilberê", "ky": "Продукт өлчөмү",
    "lt": "Produkto matmenys", "lv": "Produkta izmēri", "ms": "Dimensi produk",
    "nl": "Productafmetingen", "no": "Produktmål", "pl": "Wymiary produktu",
    "pt": "Dimensões do produto", "ro": "Dimensiuni produs", "ru": "Размер изделия",
    "sk": "Rozmery produktu", "sl": "Mere izdelka", "sq": "Përmasat e produktit",
    "sr": "Димензије производа", "sr-me": "Dimenzije proizvoda", "sv": "Produktmått",
    "sw": "Vipimo vya bidhaa", "ta": "தயாரிப்பு பரிமாணம்", "tg": "Андозаи маҳсулот",
    "th": "ขนาดสินค้า", "tk": "Önümiň ölçegi", "tl": "Sukat ng produkto",
    "tr": "Ürün ölçüleri", "uk": "Розмір виробу", "ur": "مصنوعات کا سائز",
    "uz": "Mahsulot o‘lchami", "vi": "Kích thước sản phẩm", "zu": "Usayizi womkhiqizo",
}


def treatment_value(lang: str) -> str:
    return f"{CENTRAL_TREATMENT_VALUES[lang]} + T33"


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in PRODUCT_NAMES or lang not in SIZE_LABELS:
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 400G-1600G"
    labels = base["labels"][:]
    values = base["values"][:]
    size_label = SIZE_LABELS[lang]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = treatment_value(lang)
    values[3] = "400G-1600G"
    values[4] = FEED_WATER_VALUES[lang]
    values[5] = "0.1-0.4 MPa"
    labels.insert(7, size_label)
    values.insert(7, "65*55*126 cm")
    intro = (
        f"{name}. {labels[1]}: {values[1]}. "
        f"{labels[2]}: {values[2]}. {labels[3]}: {values[3]}. "
        f"{labels[4]}: {values[4]}. {labels[5]}: {values[5]}. "
        f"{size_label}: 65*55*126 cm. {labels[8]}: {values[8]}."
    )
    card = f"{PRODUCT_NAMES[lang]}: {values[2]}; {values[3]}; {values[4]}; 65*55*126 cm."
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
        (f"{size_label}?", "65*55*126 cm"),
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
    if NEW_SLUG in text:
        link_at = text.find(NEW_SLUG)
        start = text.rfind("<article", 0, link_at)
        end = text.find("</article>", link_at)
        if start < 0 or end < 0:
            raise RuntimeError(f"Could not refresh existing card in {path}")
        text = text[:start] + card + text[end + len("</article>"):]
    else:
        match = None
        for anchor in [
            AFTER_SLUG,
            "product-commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g.html",
            "product-portable-custom-ro-water-purifier-400g-800g.html",
            "product-built-in-pressure-tank-ro.html",
        ]:
            match = re.search(
                r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?'
                + re.escape(anchor)
                + r'.*?</article>\s*)',
                text,
                flags=re.S,
            )
            if match:
                break
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + card + text[match.end():]
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
        "category": "RO Water Purifier",
        "desc": copy["card"],
        "specs": dict(zip(copy["labels"], copy["values"])),
        "image": f"../assets/products/{MAIN_IMAGE}",
        "image_local": f"assets/products/{MAIN_IMAGE}",
        "image_orig": f"../assets/products/{MAIN_IMAGE}",
        "summary": copy["intro"],
        "features": [
            "Commercial cabinet RO purifier with built-in pressure tank",
            "20-inch PP, 20-inch CTO, 20-inch PP, RO and T33 filtration",
            "400G-1600G purified water flow range",
            "Microcomputer control for automatic intelligent operation",
            "OEM/ODM cabinet color, logo, label and packaging options",
        ],
        "applications": "Commercial mid-cabinet RO water purifier for offices, stores, tea shops, restaurants, municipal tap water projects and B2B private-label distribution.",
        "related": [
            "commercial-central-ro-water-purification-equipment-250-500lph",
            "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g",
            "portable-custom-ro-water-purifier-400g-800g",
            "built-in-pressure-tank-ro",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Commercial Mid-Cabinet RO Water Purifier with Built-In Pressure Tank 400G-1600G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        or lang not in SIZE_LABELS
        or lang not in OPERATION_VALUES
        or lang not in CENTRAL_TREATMENT_VALUES
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
