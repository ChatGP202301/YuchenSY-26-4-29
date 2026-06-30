#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add portable custom RO water purifier 400G-800G across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_horizontal_ro_equipment_250lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-portable-custom-ro-water-purifier-400g-800g.html"
PRODUCT_ID = "portable-custom-ro-water-purifier-400g-800g"
MAIN_IMAGE = "portable-custom-ro-water-purifier-400g-800g-oem.webp"
IMAGE_WIDTH = 520
IMAGE_HEIGHT = 522
AFTER_SLUG = "product-desktop-ro-water-machine-compressor-cooling-100g.html"
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
    "af": "Draagbare pasgemaakte RO-waterreiniger",
    "ar": "جهاز تنقية مياه RO محمول قابل للتخصيص",
    "az": "Portativ fərdiləşdirilə bilən RO su təmizləyicisi",
    "bg": "Преносим персонализиран RO водопречиствател",
    "bn": "বহনযোগ্য কাস্টম RO পানি বিশুদ্ধকরণ মেশিন",
    "bs": "Prenosivi prilagodljivi RO prečistač vode",
    "cs": "Přenosná zakázková RO čistička vody",
    "da": "Bærbar specialtilpasset RO-vandrenser",
    "de": "Tragbarer kundenspezifischer RO-Wasserreiniger",
    "el": "Φορητός προσαρμοσμένος καθαριστής νερού RO",
    "en": "Portable Custom RO Water Purifier",
    "es": "Purificador de agua RO portátil personalizable",
    "et": "Kaasaskantav kohandatav RO veepuhasti",
    "fa": "دستگاه تصفیه آب RO قابل‌حمل و سفارشی",
    "fi": "Kannettava räätälöitävä RO-vedenpuhdistin",
    "fr": "Purificateur d’eau RO portable personnalisable",
    "ha": "Na'urar tace ruwan RO mai ɗaukuwa da ake keɓancewa",
    "he": "מטהר מים RO נייד בהתאמה אישית",
    "hi": "पोर्टेबल कस्टम RO जल शोधक",
    "hr": "Prijenosni prilagodljivi RO pročišćivač vode",
    "hu": "Hordozható egyedi RO víztisztító",
    "hy": "Դյուրակիր պատվերով RO ջրի մաքրիչ",
    "id": "Pemurni air RO portabel yang dapat disesuaikan",
    "it": "Purificatore d’acqua RO portatile personalizzabile",
    "ja": "ポータブルカスタムRO浄水機",
    "ka": "პორტატული მორგებადი RO წყლის გამწმენდი",
    "kk": "Портативті тапсырыстық RO су тазартқышы",
    "ko": "휴대형 맞춤 RO 정수기",
    "ku": "Paqijkera ava RO ya hilgirtinbar û xwestekî",
    "ky": "Портативдүү ыңгайлаштырылуучу RO суу тазалагыч",
    "lt": "Nešiojamas pritaikomas RO vandens valytuvas",
    "lv": "Pārnēsājams pielāgojams RO ūdens attīrītājs",
    "ms": "Penulen air RO mudah alih yang boleh disesuaikan",
    "nl": "Draagbare maatwerk RO-waterzuiveraar",
    "no": "Bærbar tilpasset RO-vannrenser",
    "pl": "Przenośny konfigurowalny oczyszczacz wody RO",
    "pt": "Purificador de água RO portátil personalizável",
    "ro": "Purificator de apă RO portabil personalizabil",
    "ru": "Портативный RO-очиститель воды под заказ",
    "sk": "Prenosný prispôsobiteľný RO čistič vody",
    "sl": "Prenosni prilagodljivi RO čistilnik vode",
    "sq": "Pastrues uji RO portativ i personalizueshëm",
    "sr": "Преносиви прилагодљиви RO пречистач воде",
    "sr-me": "Prenosivi prilagodljivi RO prečišćivač vode",
    "sv": "Bärbar anpassad RO-vattenrenare",
    "sw": "Kisafishaji maji cha RO cha kubebeka kinachoweza kubinafsishwa",
    "ta": "எடுத்துச் செல்லக்கூடிய தனிப்பயன் RO நீர் சுத்திகரிப்பான்",
    "tg": "Тозакунандаи оби RO-и сайёри фармоишӣ",
    "th": "เครื่องกรองน้ำ RO แบบพกพาปรับแต่งได้",
    "tk": "Göterilýän ýöriteleşdirilýän RO suw arassalaýjy",
    "tl": "Nadadalang pasadyang RO water purifier",
    "tr": "Taşınabilir özelleştirilebilir RO su arıtma cihazı",
    "uk": "Портативний RO-очисник води під замовлення",
    "ur": "پورٹیبل حسب ضرورت RO واٹر پیوریفائر",
    "uz": "Ko‘chma moslashtiriladigan RO suv tozalagichi",
    "vi": "Máy lọc nước RO di động tùy chỉnh",
    "zu": "Umshini we-RO wokuhlanza amanzi ophathekayo nowenziwa ngokwezifiso",
}


OPERATION_VALUES = {
    "af": "Voloutomatiese intelligente werking met mikrorekenaarbeheer",
    "ar": "تشغيل ذكي أوتوماتيكي كامل مع تحكم بالحاسوب الدقيق",
    "az": "Mikrokompüter idarəsi ilə tam avtomatik ağıllı iş",
    "bg": "Напълно автоматична интелигентна работа с микрокомпютърно управление",
    "bn": "মাইক্রোকম্পিউটার নিয়ন্ত্রণসহ পূর্ণ স্বয়ংক্রিয় বুদ্ধিমান অপারেশন",
    "bs": "Potpuno automatski inteligentan rad s mikrokompjuterskim upravljanjem",
    "cs": "Plně automatický inteligentní provoz s mikroprocesorovým řízením",
    "da": "Fuldautomatisk intelligent drift med mikrocomputerstyring",
    "de": "Vollautomatischer intelligenter Betrieb mit Mikrocomputersteuerung",
    "el": "Πλήρως αυτόματη έξυπνη λειτουργία με μικροϋπολογιστικό έλεγχο",
    "en": "Full automatic intelligent operation with microcomputer control",
    "es": "Operación inteligente totalmente automática con control por microcomputadora",
    "et": "Täisautomaatne intelligentne töö mikroarvuti juhtimisega",
    "fa": "کارکرد هوشمند تمام‌خودکار با کنترل میکروکامپیوتری",
    "fi": "Täysautomaattinen älykäs käyttö mikrotietokoneohjauksella",
    "fr": "Fonctionnement intelligent entièrement automatique avec commande par micro-ordinateur",
    "ha": "Aiki na atomatik mai hankali tare da sarrafa microcomputer",
    "he": "פעולה חכמה אוטומטית מלאה עם בקרת מיקרו-מחשב",
    "hi": "माइक्रोकंप्यूटर नियंत्रण के साथ पूर्ण स्वचालित बुद्धिमान संचालन",
    "hr": "Potpuno automatski inteligentan rad s mikroprocesorskim upravljanjem",
    "hu": "Teljesen automatikus intelligens működés mikroszámítógépes vezérléssel",
    "hy": "Լիովին ավտոմատ խելացի աշխատանք՝ միկրոհամակարգչային կառավարմամբ",
    "id": "Operasi cerdas otomatis penuh dengan kontrol mikrokomputer",
    "it": "Funzionamento intelligente completamente automatico con controllo a microcomputer",
    "ja": "マイコン制御による全自動インテリジェント運転",
    "ka": "სრულად ავტომატური გონიერი მუშაობა მიკროკომპიუტერული მართვით",
    "kk": "Микрокомпьютерлік басқаруы бар толық автоматты интеллектуалды жұмыс",
    "ko": "마이크로컴퓨터 제어를 갖춘 완전 자동 지능 운전",
    "ku": "Xebata aqilmend a tevahî otomatîk bi kontrola mikrokomputerê",
    "ky": "Микрокомпьютердик башкаруусу бар толук автоматтык акылдуу иштөө",
    "lt": "Visiškai automatinis išmanus veikimas su mikrokompiuteriniu valdymu",
    "lv": "Pilnībā automātiska vieda darbība ar mikrodatora vadību",
    "ms": "Operasi pintar automatik penuh dengan kawalan mikrokomputer",
    "nl": "Volautomatische intelligente werking met microcomputerbesturing",
    "no": "Helautomatisk intelligent drift med mikrocomputerstyring",
    "pl": "W pełni automatyczna inteligentna praca ze sterowaniem mikrokomputerowym",
    "pt": "Operação inteligente totalmente automática com controle por microcomputador",
    "ro": "Funcționare inteligentă complet automată cu control prin microcomputer",
    "ru": "Полностью автоматическая интеллектуальная работа с микрокомпьютерным управлением",
    "sk": "Plne automatická inteligentná prevádzka s mikroprocesorovým riadením",
    "sl": "Popolnoma samodejno pametno delovanje z mikroprocesorskim upravljanjem",
    "sq": "Funksionim inteligjent plotësisht automatik me kontroll me mikrokompjuter",
    "sr": "Потпуно аутоматски интелигентан рад са микрокомпјутерским управљањем",
    "sr-me": "Potpuno automatski inteligentan rad sa mikrokompjuterskim upravljanjem",
    "sv": "Helautomatisk intelligent drift med mikrodatorstyrning",
    "sw": "Uendeshaji mahiri wa kiotomatiki kabisa kwa udhibiti wa kompyuta ndogo",
    "ta": "மைக்ரோகணினி கட்டுப்பாட்டுடன் முழு தானியங்கி அறிவார்ந்த செயல்பாடு",
    "tg": "Кори пурра автоматии зеҳнӣ бо идоракунии микрокомпютерӣ",
    "th": "การทำงานอัจฉริยะอัตโนมัติเต็มรูปแบบด้วยการควบคุมไมโครคอมพิวเตอร์",
    "tk": "Mikrokompýuter dolandyryşy bilen doly awtomatik akylly iş",
    "tl": "Ganap na awtomatikong matalinong operasyon na may kontrol ng microcomputer",
    "tr": "Mikro bilgisayar kontrolü ile tam otomatik akıllı çalışma",
    "uk": "Повністю автоматична інтелектуальна робота з мікрокомп’ютерним керуванням",
    "ur": "مائیکرو کمپیوٹر کنٹرول کے ساتھ مکمل خودکار ذہین آپریشن",
    "uz": "Mikrokompyuter boshqaruvi bilan to‘liq avtomatik aqlli ishlash",
    "vi": "Vận hành thông minh hoàn toàn tự động với điều khiển vi máy tính",
    "zu": "Ukusebenza okuhlakaniphile okuzenzakalelayo ngokuphelele ngokulawulwa kwekhompyutha encane",
}


TREATMENT_VALUES = {
    "af": "Geïntegreerde vinnigkoppeling PP-sedimentfilter + RO-membraan 3013",
    "ar": "فلتر رواسب PP سريع التوصيل مدمج + غشاء RO 3013",
    "az": "İnteqrasiya olunmuş tez qoşulan PP çöküntü filtri + RO membranı 3013",
    "bg": "Интегриран бързосменяем PP седиментен филтър + RO мембрана 3013",
    "bn": "একীভূত দ্রুত-সংযোগ PP সেডিমেন্ট ফিল্টার + RO মেমব্রেন 3013",
    "bs": "Integrisani brzspojni PP sedimentni filter + RO membrana 3013",
    "cs": "Integrovaný rychlospojovací PP sedimentační filtr + RO membrána 3013",
    "da": "Integreret hurtigkoblet PP-sedimentfilter + RO-membran 3013",
    "de": "Integrierter Schnellanschluss-PP-Sedimentfilter + RO-Membran 3013",
    "el": "Ενσωματωμένο φίλτρο ιζημάτων PP ταχείας σύνδεσης + μεμβράνη RO 3013",
    "en": "Integrated quick-connect PP sediment filter + RO membrane 3013",
    "es": "Filtro de sedimentos PP integrado de conexión rápida + membrana RO 3013",
    "et": "Integreeritud kiirühendusega PP setefilter + RO membraan 3013",
    "fa": "فیلتر رسوب‌گیر PP یکپارچه با اتصال سریع + ممبران RO 3013",
    "fi": "Integroitu pikaliitäntäinen PP-sedimenttisuodatin + RO-kalvo 3013",
    "fr": "Filtre sédiments PP intégré à raccord rapide + membrane RO 3013",
    "ha": "Hadadden matatar laka ta PP mai haɗin sauri + membrane RO 3013",
    "he": "מסנן משקעים PP משולב בחיבור מהיר + ממברנת RO 3013",
    "hi": "इंटीग्रेटेड क्विक-कनेक्ट PP सेडिमेंट फिल्टर + RO मेम्ब्रेन 3013",
    "hr": "Integrirani PP sedimentni filtar s brzim spojem + RO membrana 3013",
    "hu": "Integrált gyorscsatlakozós PP üledékszűrő + RO membrán 3013",
    "hy": "Ինտեգրված արագ միացման PP նստվածքային ֆիլտր + RO թաղանթ 3013",
    "id": "Filter sedimen PP terintegrasi sambungan cepat + membran RO 3013",
    "it": "Filtro sedimenti PP integrato a innesto rapido + membrana RO 3013",
    "ja": "一体型クイック接続PP沈殿フィルター + ROメンブレン3013",
    "ka": "ინტეგრირებული სწრაფი შეერთების PP ნალექის ფილტრი + RO მემბრანა 3013",
    "kk": "Кіріктірілген жылдам қосылатын PP тұнба сүзгісі + RO мембранасы 3013",
    "ko": "일체형 퀵 커넥트 PP 침전 필터 + RO 멤브레인 3013",
    "ku": "Parzûna sedîmentê ya PP ya yekgirtî bi girêdana bilez + membrana RO 3013",
    "ky": "Интеграцияланган тез туташтырылуучу PP чөкмө чыпкасы + RO мембранасы 3013",
    "lt": "Integruotas greito jungimo PP nuosėdų filtras + RO membrana 3013",
    "lv": "Integrēts ātrā savienojuma PP nogulšņu filtrs + RO membrāna 3013",
    "ms": "Penapis sedimen PP bersepadu sambungan pantas + membran RO 3013",
    "nl": "Geïntegreerd snelkoppelbaar PP-sedimentfilter + RO-membraan 3013",
    "no": "Integrert hurtigkoblet PP-sedimentfilter + RO-membran 3013",
    "pl": "Zintegrowany szybkozłączny filtr sedymentacyjny PP + membrana RO 3013",
    "pt": "Filtro de sedimentos PP integrado de conexão rápida + membrana RO 3013",
    "ro": "Filtru de sedimente PP integrat cu conectare rapidă + membrană RO 3013",
    "ru": "Интегрированный быстросъемный PP-фильтр осадка + RO-мембрана 3013",
    "sk": "Integrovaný rýchlospojkový PP sedimentačný filter + RO membrána 3013",
    "sl": "Integriran hitrospojni PP sedimentni filter + RO membrana 3013",
    "sq": "Filtër sedimenti PP i integruar me lidhje të shpejtë + membranë RO 3013",
    "sr": "Интегрисани брзоспојни PP седиментни филтер + RO мембрана 3013",
    "sr-me": "Integrisani brzspojni PP sedimentni filter + RO membrana 3013",
    "sv": "Integrerat snabbkopplat PP-sedimentfilter + RO-membran 3013",
    "sw": "Kichujio cha mashapo cha PP kilichounganishwa kwa haraka + utando wa RO 3013",
    "ta": "ஒருங்கிணைந்த விரைவு இணைப்பு PP கழிவு வடிகட்டி + RO மெம்பிரேன் 3013",
    "tg": "Филтри таҳшинии PP-и ҳамгирошуда бо пайвасти зуд + мембранаи RO 3013",
    "th": "ไส้กรองตะกอน PP แบบควิกคอนเนกต์ในตัว + เมมเบรน RO 3013",
    "tk": "Birleşdirilen çalt birikdirilýän PP çökündi süzgüji + RO membranasy 3013",
    "tl": "Pinagsamang quick-connect PP sediment filter + RO membrane 3013",
    "tr": "Entegre hızlı bağlantılı PP tortu filtresi + RO membran 3013",
    "uk": "Інтегрований швидкознімний PP-фільтр осаду + RO-мембрана 3013",
    "ur": "انٹیگریٹڈ کوئیک کنیکٹ PP سیڈمنٹ فلٹر + RO میمبرین 3013",
    "uz": "Integratsiyalashgan tez ulanuvchi PP cho‘kindi filtri + RO membranasi 3013",
    "vi": "Lõi lọc cặn PP tích hợp kết nối nhanh + màng RO 3013",
    "zu": "Isihlungi se-PP sediment esihlanganisiwe esixhuma ngokushesha + ulwelwesi lwe-RO 3013",
}


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in PRODUCT_NAMES or lang not in OPERATION_VALUES or lang not in TREATMENT_VALUES:
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 400G-800G"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = TREATMENT_VALUES[lang]
    values[3] = "400G-800G"
    values[4] = FEED_WATER_VALUES[lang]
    values[5] = "0.1-0.4 MPa"
    intro = (
        f"{name}. {labels[1]}: {values[1]}. "
        f"{labels[2]}: {values[2]}. {labels[3]}: {values[3]}. "
        f"{labels[4]}: {values[4]}. {labels[5]}: {values[5]}. "
        f"{labels[6]}: {values[6]}."
    )
    card = f"{PRODUCT_NAMES[lang]}: {values[2]}; {values[3]}; {values[4]}."
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
            "product-built-in-pressure-tank-ro.html",
            "product-custom-5-6-7-stage-ro-water-purifier.html",
            "product-commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g.html",
        ]:
            match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(anchor) + r'.*?</article>\s*)', text, flags=re.S)
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "desktop-ro-water-machine-compressor-cooling-100g"),
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
            "Portable custom RO purifier for municipal tap water",
            "Integrated quick-connect PP sediment filter and 3013 RO membrane",
            "400G-800G purified water flow range",
            "Microcomputer control with automatic intelligent operation",
            "OEM/ODM color, label, logo and packaging options",
        ],
        "applications": "Portable custom RO water purifier for distributors, rental projects, offices, apartments, small stores, exhibitions and OEM private-label programs.",
        "related": [
            "desktop-ro-water-machine-compressor-cooling-100g",
            "built-in-pressure-tank-ro",
            "custom-5-6-7-stage-ro-water-purifier",
            "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Portable Custom RO Water Purifier 400G-800G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        or lang not in OPERATION_VALUES
        or lang not in TREATMENT_VALUES
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
