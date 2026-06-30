#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add single-tank integrated RO purification and water supply equipment."""

from __future__ import annotations

import json
import re
import html as html_lib
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

NEW_SLUG = "product-single-tank-integrated-ro-water-purification-supply-equipment-250-500lph.html"
PRODUCT_ID = "single-tank-integrated-ro-water-purification-supply-equipment-250-500lph"
MAIN_IMAGE = "single-tank-integrated-ro-water-purification-supply-equipment-250l-500l-oem.webp"
IMAGE_WIDTH = 308
IMAGE_HEIGHT = 536
AFTER_SLUG = "product-precision-filter-ro-water-purification-equipment-250-1000lph.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Enkeltenk geïntegreerde RO-water suiwering- en toevoertoerusting",
    "ar": "معدات RO متكاملة بخزان واحد لتنقية المياه وتزويدها",
    "az": "Bir çənli inteqrə olunmuş RO su təmizləmə və təchizat avadanlığı",
    "bg": "Интегрирано RO оборудване с един съд за пречистване и водоснабдяване",
    "bn": "এক ট্যাংক ইন্টিগ্রেটেড RO পানি বিশুদ্ধকরণ ও সরবরাহ সরঞ্জাম",
    "bs": "Integrisana RO oprema s jednim tankom za prečišćavanje i dovod vode",
    "cs": "Integrované RO zařízení s jednou nádobou pro úpravu a dodávku vody",
    "da": "Integreret RO-anlæg med én tank til vandrensning og forsyning",
    "de": "Integrierte RO-Wasseraufbereitungs- und Versorgungsanlage mit einem Tank",
    "el": "Ολοκληρωμένος εξοπλισμός RO μίας δεξαμενής για καθαρισμό και παροχή νερού",
    "en": "Single-Tank Integrated RO Water Purification and Supply Equipment",
    "es": "Equipo RO integrado de un tanque para purificación y suministro de agua",
    "et": "Ühe paagiga integreeritud RO veepuhastus- ja varustusseade",
    "fa": "دستگاه یک‌مخزنه یکپارچه RO برای تصفیه و تأمین آب",
    "fi": "Yhden säiliön integroitu RO-vedenpuhdistus- ja syöttölaitteisto",
    "fr": "Équipement RO intégré à une cuve pour purification et alimentation en eau",
    "ha": "Na'urar RO mai tanki ɗaya haɗaɗɗe don tacewa da samar da ruwa",
    "he": "ציוד RO משולב במכל יחיד לטיהור ואספקת מים",
    "hi": "एकल टैंक एकीकृत RO जल शुद्धिकरण और आपूर्ति उपकरण",
    "hr": "Integrirana RO oprema s jednim spremnikom za pročišćavanje i opskrbu vodom",
    "hu": "Egytartályos integrált RO víztisztító és vízellátó berendezés",
    "hy": "Մեկ բաքով ինտեգրված RO ջրի մաքրման և մատակարարման սարքավորում",
    "id": "Peralatan RO terintegrasi satu tangki untuk pemurnian dan suplai air",
    "it": "Impianto RO integrato a serbatoio singolo per purificazione e alimentazione acqua",
    "ja": "単槽一体型RO浄水・給水装置",
    "ka": "ერთავზიანი ინტეგრირებული RO წყლის გამწმენდი და მიწოდების მოწყობილობა",
    "kk": "Бір бакты біріктірілген RO су тазарту және сумен жабдықтау жабдығы",
    "ko": "단일 탱크 일체형 RO 정수 및 급수 장비",
    "ku": "Amûra RO ya yek tankî ya yekbûyî ji bo paqijkirin û dabînkirina avê",
    "ky": "Бир бактуу интеграцияланган RO суу тазалоо жана суу берүү жабдыгы",
    "lt": "Vienos talpos integruota RO vandens valymo ir tiekimo įranga",
    "lv": "Vienas tvertnes integrēta RO ūdens attīrīšanas un padeves iekārta",
    "ms": "Peralatan RO bersepadu satu tangki untuk penulenan dan bekalan air",
    "nl": "Geïntegreerde RO-waterzuiverings- en toevoerinstallatie met één tank",
    "no": "Integrert RO-vannrense- og forsyningsanlegg med én tank",
    "pl": "Zintegrowane urządzenie RO z jednym zbiornikiem do uzdatniania i zasilania wodą",
    "pt": "Equipamento RO integrado de um tanque para purificação e abastecimento de água",
    "ro": "Echipament RO integrat cu un singur rezervor pentru purificarea și alimentarea cu apă",
    "ru": "Интегрированное RO-оборудование с одной колонной для очистки и подачи воды",
    "sk": "Integrované RO zariadenie s jednou nádobou na úpravu a dodávku vody",
    "sl": "Integrirana RO oprema z enim rezervoarjem za čiščenje in dovod vode",
    "sq": "Pajisje RO e integruar me një rezervuar për pastrimin dhe furnizimin e ujit",
    "sr": "Интегрисана RO опрема са једним резервоаром за пречишћавање и довод воде",
    "sr-me": "Integrisana RO oprema sa jednim rezervoarom za prečišćavanje i dovod vode",
    "sv": "Integrerad RO-vattenrenings- och försörjningsutrustning med en tank",
    "sw": "Kifaa jumuishi cha RO chenye tanki moja kwa kusafisha na kusambaza maji",
    "ta": "ஒற்றை தொட்டி ஒருங்கிணைந்த RO நீர் சுத்திகரிப்பு மற்றும் வழங்கல் உபகரணம்",
    "tg": "Таҷҳизоти якзарфаи ҳамгирошудаи RO барои тозакунӣ ва таъмини об",
    "th": "อุปกรณ์ RO แบบถังเดียวครบชุดสำหรับกรองและจ่ายน้ำ",
    "tk": "Bir bakly birleşdirilen RO suw arassalaýjy we üpjün ediji enjam",
    "tl": "Pinagsamang RO na kagamitang may isang tangke para sa paglilinis at suplay ng tubig",
    "tr": "Tek tank entegre RO su arıtma ve besleme ekipmanı",
    "uk": "Інтегроване RO обладнання з однією колоною для очищення та подачі води",
    "ur": "ایک ٹینک مربوط RO پانی صاف کرنے اور فراہمی کا سامان",
    "uz": "Bir bakli integratsiyalashgan RO suv tozalash va ta’minot uskunasi",
    "vi": "Thiết bị RO tích hợp một bồn cho lọc và cấp nước",
    "zu": "Imishini ye-RO ehlanganisiwe enethangi elilodwa yokuhlanza nokuhlinzeka ngamanzi",
}


TREATMENT_VALUES = {
    "af": "Rouwaterpomp + outomatiese sand-koolstoftenk + 20-duim PP + RO + vlekvryestaal skoonwatertenk + frekwensie-beheerde toevoerpomp",
    "ar": "مضخة مياه خام + خزان رمل وكربون أوتوماتيكي + PP مقاس 20 بوصة + RO + خزان مياه نقية من الفولاذ المقاوم للصدأ + مضخة تزويد مياه بتردد متغير",
    "az": "Xam su nasosu + avtomatik qum-karbon çəni + 20 düymlük PP + RO + paslanmayan polad təmiz su çəni + dəyişən tezlikli su təchizat nasosu",
    "bg": "Помпа за сурова вода + автоматичен пясъчно-въглероден съд + 20-инчов PP + RO + резервоар за чиста вода от неръждаема стомана + честотно управлявана помпа за водоснабдяване",
    "bn": "কাঁচা পানির পাম্প + স্বয়ংক্রিয় বালু-কার্বন ট্যাংক + 20 ইঞ্চি PP + RO + স্টেইনলেস স্টিল বিশুদ্ধ পানির ট্যাংক + ভ্যারিয়েবল-ফ্রিকোয়েন্সি পানি সরবরাহ পাম্প",
    "bs": "Pumpa sirove vode + automatski pješčano-karbonski tank + 20-inčni PP + RO + spremnik čiste vode od nehrđajućeg čelika + pumpa za dovod vode s regulacijom frekvencije",
    "cs": "Čerpadlo surové vody + automatická pískovo-uhlíková nádoba + 20palcový PP + RO + nerezová nádrž na čistou vodu + frekvenčně řízené zásobovací čerpadlo",
    "da": "Råvandspumpe + automatisk sand-kultank + 20-tommer PP + RO + rentvandstank i rustfrit stål + frekvensstyret forsyningspumpe",
    "de": "Rohwasserpumpe + automatischer Sand-Aktivkohlebehälter + 20-Zoll PP + RO + Reinwassertank aus Edelstahl + frequenzgeregelte Förderpumpe",
    "el": "Αντλία ακατέργαστου νερού + αυτόματη δεξαμενή άμμου-άνθρακα + PP 20 ιντσών + RO + ανοξείδωτη δεξαμενή καθαρού νερού + αντλία παροχής νερού μεταβλητής συχνότητας",
    "en": "Raw water pump + automatic sand-carbon tank + 20-inch PP + RO + stainless steel pure water tank + variable-frequency water supply pump",
    "es": "Bomba de agua cruda + tanque automático de arena y carbón + PP de 20 pulgadas + RO + tanque de agua pura de acero inoxidable + bomba de suministro con frecuencia variable",
    "et": "Toorveepump + automaatne liiva-söepaak + 20-tolline PP + RO + roostevabast terasest puhta vee paak + sagedusmuunduriga varustuspump",
    "fa": "پمپ آب خام + مخزن شنی-کربنی خودکار + PP بیست اینچ + RO + مخزن آب خالص استیل ضدزنگ + پمپ تأمین آب با فرکانس متغیر",
    "fi": "Raakavesipumppu + automaattinen hiekka-hiilisäiliö + PP 20 tuumaa + RO + ruostumattomasta teräksestä valmistettu puhdasvesisäiliö + taajuusohjattu syöttöpumppu",
    "fr": "Pompe d’eau brute + cuve automatique sable-charbon + PP 20 pouces + RO + réservoir d’eau pure en acier inoxydable + pompe d’alimentation à fréquence variable",
    "ha": "Famfon ruwan danye + tankin yashi-da-carbon na atomatik + PP inci 20 + RO + tankin ruwan tsabta na bakin karfe + famfon samar da ruwa mai sauya mitar aiki",
    "he": "משאבת מים גולמיים + מכל חול-פחם אוטומטי + PP בגודל 20 אינץ׳ + RO + מכל מים טהורים מנירוסטה + משאבת אספקת מים בתדר משתנה",
    "hi": "कच्चे पानी का पंप + स्वचालित रेत-कार्बन टैंक + 20 इंच PP + RO + स्टेनलेस स्टील शुद्ध पानी टैंक + परिवर्ती आवृत्ति जल आपूर्ति पंप",
    "hr": "Pumpa sirove vode + automatski pješčano-ugljični spremnik + 20-inčni PP + RO + spremnik čiste vode od nehrđajućeg čelika + frekvencijski regulirana dovodna pumpa",
    "hu": "Nyersvíz-szivattyú + automata homok-aktívszén tartály + 20 hüvelykes PP + RO + rozsdamentes acél tisztavíz-tartály + frekvenciavezérelt vízellátó szivattyú",
    "hy": "Հում ջրի պոմպ + ավտոմատ ավազ-ածխային բաք + 20 դյույմ PP + RO + չժանգոտվող պողպատից մաքուր ջրի բաք + փոփոխական հաճախականության ջրամատակարարման պոմպ",
    "id": "Pompa air baku + tangki pasir-karbon otomatis + PP 20 inci + RO + tangki air murni baja tahan karat + pompa suplai air frekuensi variabel",
    "it": "Pompa acqua grezza + serbatoio automatico sabbia-carbone + PP da 20 pollici + RO + serbatoio acqua pura in acciaio inox + pompa di alimentazione a frequenza variabile",
    "ja": "原水ポンプ + 自動砂・活性炭タンク + 20インチPP + RO + ステンレス純水タンク + インバーター給水ポンプ",
    "ka": "ნედლი წყლის ტუმბო + ავტომატური ქვიშა-ნახშირის ავზი + 20 დუიმიანი PP + RO + უჟანგავი ფოლადის სუფთა წყლის ავზი + ცვლადი სიხშირის მიწოდების ტუმბო",
    "kk": "Шикі су сорғысы + автоматты құм-көмір багы + 20 дюймдік PP + RO + тот баспайтын болаттан таза су багы + жиілікпен басқарылатын су беру сорғысы",
    "ko": "원수 펌프 + 자동 모래-카본 탱크 + 20인치 PP + RO + 스테인리스 순수 탱크 + 인버터 급수 펌프",
    "ku": "Pompa ava xav + tankera xwelî-karbonê ya xweber + PP 20 inç + RO + tankera ava paqij a pola zengarnegir + pompa dabînkirina avê ya frekansa guherbar",
    "ky": "Чийки суу насосу + автоматтык кум-көмүр багы + 20 дюймдук PP + RO + дат баспас болоттон таза суу багы + жыштык менен башкарылуучу суу берүү насосу",
    "lt": "Žaliavinio vandens siurblys + automatinė smėlio-anglies talpa + 20 colių PP + RO + nerūdijančio plieno švaraus vandens talpa + dažniu valdoma tiekimo pompa",
    "lv": "Neapstrādāta ūdens sūknis + automātiska smilšu-oglekļa tvertne + 20 collu PP + RO + nerūsējošā tērauda tīrā ūdens tvertne + frekvences vadības padeves sūknis",
    "ms": "Pam air mentah + tangki pasir-karbon automatik + PP 20 inci + RO + tangki air tulen keluli tahan karat + pam bekalan air frekuensi berubah",
    "nl": "Ruwwaterpomp + automatische zand-koolstoftank + 20 inch PP + RO + roestvrijstalen zuiverwatertank + frequentiegeregelde toevoerpomp",
    "no": "Råvannspumpe + automatisk sand-karbontank + 20-tommers PP + RO + rentvannstank i rustfritt stål + frekvensstyrt forsyningspumpe",
    "pl": "Pompa wody surowej + automatyczny zbiornik piaskowo-węglowy + PP 20 cali + RO + zbiornik czystej wody ze stali nierdzewnej + pompa zasilająca z regulacją częstotliwości",
    "pt": "Bomba de água bruta + tanque automático de areia e carvão + PP de 20 polegadas + RO + tanque de água pura em aço inoxidável + bomba de abastecimento com frequência variável",
    "ro": "Pompă de apă brută + rezervor automat nisip-carbon + PP de 20 inci + RO + rezervor de apă pură din oțel inoxidabil + pompă de alimentare cu frecvență variabilă",
    "ru": "Насос сырой воды + автоматическая песчано-угольная колонна + 20-дюймовый PP + RO + бак чистой воды из нержавеющей стали + насос подачи воды с частотным управлением",
    "sk": "Čerpadlo surovej vody + automatická pieskovo-uhlíková nádoba + 20-palcový PP + RO + nerezová nádrž na čistú vodu + frekvenčne riadené zásobovacie čerpadlo",
    "sl": "Črpalka surove vode + samodejni peščeno-ogljikov rezervoar + 20-palčni PP + RO + rezervoar čiste vode iz nerjavnega jekla + frekvenčno krmiljena dovodna črpalka",
    "sq": "Pompë e ujit të papërpunuar + rezervuar automatik rërë-karbon + PP 20 inç + RO + rezervuar uji të pastër prej çeliku inox + pompë furnizimi me frekuencë të ndryshueshme",
    "sr": "Пумпа сирове воде + аутоматски песковито-угљени резервоар + PP од 20 инча + RO + резервоар чисте воде од нерђајућег челика + пумпа за довод воде са фреквентном регулацијом",
    "sr-me": "Pumpa sirove vode + automatski pješčano-ugljični rezervoar + PP od 20 inča + RO + rezervoar čiste vode od nerđajućeg čelika + pumpa za dovod vode sa frekventnom regulacijom",
    "sv": "Råvattenpump + automatisk sand-koltank + 20-tums PP + RO + renvattentank i rostfritt stål + frekvensstyrd matarpump",
    "sw": "Pampu ya maji ghafi + tanki ya mchanga-na-kaboni ya kiotomatiki + PP inchi 20 + RO + tanki ya maji safi ya chuma cha pua + pampu ya kusambaza maji yenye udhibiti wa masafa",
    "ta": "மூலநீர் பம்ப் + தானியங்கி மணல்-கார்பன் தொட்டி + 20 அங்குல PP + RO + துருப்பிடிக்காத எஃகு தூயநீர் தொட்டி + மாறும் அதிர்வெண் நீர்வழங்கல் பம்ப்",
    "tg": "Насоси оби хом + зарфи худкори қум-карбон + PP-и 20 дюйм + RO + зарфи оби тозаи пӯлоди зангногир + насоси таъмини об бо идоракунии басомад",
    "th": "ปั๊มน้ำดิบ + ถังกรองทราย-คาร์บอนอัตโนมัติ + PP 20 นิ้ว + RO + ถังน้ำบริสุทธิ์สแตนเลส + ปั๊มจ่ายน้ำแบบปรับความถี่",
    "tk": "Çig suw nasosy + awtomatiki gum-karbon baky + 20 dýuým PP + RO + poslamaýan polatdan arassa suw baky + üýtgeýän ýygylykly suw üpjünçilik nasosy",
    "tl": "Pumpa ng hilaw na tubig + awtomatikong tangke ng buhangin-karbon + PP na 20 pulgada + RO + tangke ng purong tubig na hindi kinakalawang na asero + pumpang suplay ng tubig na may nagbabagong dalas",
    "tr": "Ham su pompası + otomatik kum-karbon tankı + 20 inç PP + RO + paslanmaz çelik saf su tankı + değişken frekanslı su besleme pompası",
    "uk": "Насос сирої води + автоматична піщано-вугільна колона + 20-дюймовий PP + RO + бак чистої води з нержавіючої сталі + насос подачі води з частотним керуванням",
    "ur": "خام پانی پمپ + خودکار ریت-کاربن ٹینک + 20 انچ PP + RO + سٹینلیس سٹیل صاف پانی ٹینک + متغیر فریکوئنسی پانی سپلائی پمپ",
    "uz": "Xom suv nasosi + avtomatik qum-ko‘mir baki + 20 dyuymli PP + RO + zanglamaydigan po‘lat toza suv baki + o‘zgaruvchan chastotali suv ta’minoti nasosi",
    "vi": "Bơm nước thô + bồn cát-than tự động + PP 20 inch + RO + bồn nước tinh khiết inox + bơm cấp nước biến tần",
    "zu": "Iphampu lamanzi angahluziwe + ithangi lesihlabathi-nekhabhoni elizenzakalelayo + PP engu-20 intshi + RO + ithangi lamanzi ahlanzekile lensimbi engagqwali + iphampu yokuphakela amanzi elawulwa imvamisa",
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
    text = BASE_BUILD_MAIN(lang, copy)
    encoded = "Single%20Tank%20Integrated%20RO%20Water%20Purification%20Supply%20Equipment%20250-500Lph"
    for old in [
        "Commercial%20Central%20RO%20Water%20Purification%20Equipment%20250-500Lph",
        "Precision%20Filter%20RO%20Water%20Purification%20Equipment%20250-1000Lph",
    ]:
        text = text.replace(old, encoded)
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
    if NEW_SLUG not in text:
        match = None
        for anchor in [
            AFTER_SLUG,
            "product-commercial-central-ro-water-purification-equipment-250-500lph.html",
            "product-slim-reverse-osmosis-water-purification-equipment-250-500lph.html",
            "product-single-tank-big-blue-pp-ro-equipment-250-500lph.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "precision-filter-ro-water-purification-equipment-250-1000lph"),
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
            "Raw water pump, automatic sand-carbon tank and 20-inch PP pretreatment",
            "RO purification with stainless steel pure water tank",
            "Variable-frequency water supply pump",
            "250-500 L/h purified water flow",
            "Suitable for tap water and groundwater",
        ],
        "applications": "Integrated RO purification and pressure water supply for offices, schools, clinics, hotels, kitchens and commercial drinking-water projects.",
        "related": [
            "precision-filter-ro-water-purification-equipment-250-1000lph",
            "commercial-central-ro-water-purification-equipment-250-500lph",
            "single-tank-pretreatment-ro-equipment-250-500lph",
            "single-tank-big-blue-pp-ro-equipment-250-500lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Single-Tank Integrated RO Water Purification and Supply Equipment 250-500 L/h: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
    DUAL_GLOBALS["update_products_page"] = update_products_page
    DUAL_GLOBALS["update_products_json"] = update_products_json
    DUAL_GLOBALS["update_ai_files"] = update_ai_files
    DUAL_GLOBALS["main"]()
    for lang in DUAL_GLOBALS["dirs"]():
        fix_related_cards(lang)


if __name__ == "__main__":
    main()
