#!/usr/bin/env python3
"""Deep cleanup for visible non-English page text.

The original static export mixed translated templates with English product
data. This pass keeps technical acronyms and brand names, but removes the most
visible English product names, categories, descriptions, CTAs and spec values
from non-English pages.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

LANGS = [
    "en", "es", "fr", "de", "pt", "ru", "ar", "ja", "ko", "it", "tr",
    "hi", "bn", "id", "vi", "th", "pl", "nl", "fa", "ur", "ms", "tl",
    "he", "el", "cs", "hu", "ro", "sv", "da", "fi", "no", "uk", "bg",
    "hr", "sr", "sk", "sl", "lt", "et", "lv", "sw", "ha", "zu", "ta", "kk",
]

SOURCE_CATEGORIES = [
    "Filter Cartridge",
    "Filter Housing",
    "Flat Cap Filter",
    "Industrial Filter",
    "Inline Filter",
    "RO System",
    "Water Dispenser",
    "Water Purifier",
]

CATEGORIES: dict[str, dict[str, str]] = {
    "es": {"Filter Cartridge": "Cartucho filtrante", "Filter Housing": "Carcasa de filtro", "Flat Cap Filter": "Filtro de tapa plana", "Industrial Filter": "Filtro industrial", "Inline Filter": "Filtro en línea", "RO System": "Sistema RO", "Water Dispenser": "Dispensador de agua", "Water Purifier": "Purificador de agua"},
    "fr": {"Filter Cartridge": "Cartouche filtrante", "Filter Housing": "Boîtier de filtre", "Flat Cap Filter": "Filtre à embout plat", "Industrial Filter": "Filtre industriel", "Inline Filter": "Filtre en ligne", "RO System": "Système RO", "Water Dispenser": "Distributeur d'eau", "Water Purifier": "Purificateur d'eau"},
    "de": {"Filter Cartridge": "Filterkartusche", "Filter Housing": "Filtergehäuse", "Flat Cap Filter": "Flachkappenfilter", "Industrial Filter": "Industriefilter", "Inline Filter": "Inline-Filter", "RO System": "RO-System", "Water Dispenser": "Wasserspender", "Water Purifier": "Wasserreiniger"},
    "pt": {"Filter Cartridge": "Cartucho filtrante", "Filter Housing": "Carcaça de filtro", "Flat Cap Filter": "Filtro de tampa plana", "Industrial Filter": "Filtro industrial", "Inline Filter": "Filtro em linha", "RO System": "Sistema RO", "Water Dispenser": "Dispensador de água", "Water Purifier": "Purificador de água"},
    "ru": {"Filter Cartridge": "Фильтрующий картридж", "Filter Housing": "Корпус фильтра", "Flat Cap Filter": "Фильтр с плоской крышкой", "Industrial Filter": "Промышленный фильтр", "Inline Filter": "Линейный фильтр", "RO System": "Система RO", "Water Dispenser": "Диспенсер воды", "Water Purifier": "Очиститель воды"},
    "ar": {"Filter Cartridge": "خرطوشة فلتر", "Filter Housing": "حاوية فلتر", "Flat Cap Filter": "فلتر بغطاء مسطح", "Industrial Filter": "فلتر صناعي", "Inline Filter": "فلتر مدمج", "RO System": "نظام RO", "Water Dispenser": "موزع مياه", "Water Purifier": "منقي مياه"},
    "ja": {"Filter Cartridge": "フィルターカートリッジ", "Filter Housing": "フィルターハウジング", "Flat Cap Filter": "フラットキャップフィルター", "Industrial Filter": "産業用フィルター", "Inline Filter": "インラインフィルター", "RO System": "ROシステム", "Water Dispenser": "ウォーターディスペンサー", "Water Purifier": "浄水器"},
    "ko": {"Filter Cartridge": "필터 카트리지", "Filter Housing": "필터 하우징", "Flat Cap Filter": "플랫 캡 필터", "Industrial Filter": "산업용 필터", "Inline Filter": "인라인 필터", "RO System": "RO 시스템", "Water Dispenser": "정수 디스펜서", "Water Purifier": "정수기"},
    "it": {"Filter Cartridge": "Cartuccia filtrante", "Filter Housing": "Alloggiamento filtro", "Flat Cap Filter": "Filtro a tappo piatto", "Industrial Filter": "Filtro industriale", "Inline Filter": "Filtro in linea", "RO System": "Sistema RO", "Water Dispenser": "Dispenser d'acqua", "Water Purifier": "Purificatore d'acqua"},
    "tr": {"Filter Cartridge": "Filtre kartuşu", "Filter Housing": "Filtre gövdesi", "Flat Cap Filter": "Düz kapak filtre", "Industrial Filter": "Endüstriyel filtre", "Inline Filter": "Inline filtre", "RO System": "RO sistemi", "Water Dispenser": "Su sebili", "Water Purifier": "Su arıtıcı"},
    "hi": {"Filter Cartridge": "फ़िल्टर कार्ट्रिज", "Filter Housing": "फ़िल्टर हाउसिंग", "Flat Cap Filter": "फ्लैट कैप फ़िल्टर", "Industrial Filter": "औद्योगिक फ़िल्टर", "Inline Filter": "इनलाइन फ़िल्टर", "RO System": "RO सिस्टम", "Water Dispenser": "जल डिस्पेंसर", "Water Purifier": "जल शोधक"},
    "bn": {"Filter Cartridge": "ফিল্টার কার্টিজ", "Filter Housing": "ফিল্টার হাউজিং", "Flat Cap Filter": "ফ্ল্যাট ক্যাপ ফিল্টার", "Industrial Filter": "শিল্প ফিল্টার", "Inline Filter": "ইনলাইন ফিল্টার", "RO System": "RO সিস্টেম", "Water Dispenser": "ওয়াটার ডিসপেনসার", "Water Purifier": "ওয়াটার পিউরিফায়ার"},
    "id": {"Filter Cartridge": "Kartrid filter", "Filter Housing": "Rumah filter", "Flat Cap Filter": "Filter tutup datar", "Industrial Filter": "Filter industri", "Inline Filter": "Filter inline", "RO System": "Sistem RO", "Water Dispenser": "Dispenser air", "Water Purifier": "Pemurni air"},
    "vi": {"Filter Cartridge": "Lõi lọc", "Filter Housing": "Vỏ lọc", "Flat Cap Filter": "Lõi lọc nắp phẳng", "Industrial Filter": "Bộ lọc công nghiệp", "Inline Filter": "Lõi lọc inline", "RO System": "Hệ thống RO", "Water Dispenser": "Máy cấp nước", "Water Purifier": "Máy lọc nước"},
    "th": {"Filter Cartridge": "ไส้กรอง", "Filter Housing": "กระบอกกรอง", "Flat Cap Filter": "ไส้กรองฝาเรียบ", "Industrial Filter": "ไส้กรองอุตสาหกรรม", "Inline Filter": "ไส้กรองอินไลน์", "RO System": "ระบบ RO", "Water Dispenser": "ตู้กดน้ำ", "Water Purifier": "เครื่องกรองน้ำ"},
    "pl": {"Filter Cartridge": "Wkład filtracyjny", "Filter Housing": "Obudowa filtra", "Flat Cap Filter": "Filtr z płaską nasadką", "Industrial Filter": "Filtr przemysłowy", "Inline Filter": "Filtr liniowy", "RO System": "System RO", "Water Dispenser": "Dystrybutor wody", "Water Purifier": "Oczyszczacz wody"},
    "nl": {"Filter Cartridge": "Filterpatroon", "Filter Housing": "Filterbehuizing", "Flat Cap Filter": "Flat-cap filter", "Industrial Filter": "Industrieel filter", "Inline Filter": "Inline filter", "RO System": "RO-systeem", "Water Dispenser": "Waterdispenser", "Water Purifier": "Waterzuiveraar"},
    "fa": {"Filter Cartridge": "کارتریج فیلتر", "Filter Housing": "هوزینگ فیلتر", "Flat Cap Filter": "فیلتر درپوش تخت", "Industrial Filter": "فیلتر صنعتی", "Inline Filter": "فیلتر اینلاین", "RO System": "سیستم RO", "Water Dispenser": "دیسپنسر آب", "Water Purifier": "دستگاه تصفیه آب"},
    "ur": {"Filter Cartridge": "فلٹر کارٹریج", "Filter Housing": "فلٹر ہاؤسنگ", "Flat Cap Filter": "فلیٹ کیپ فلٹر", "Industrial Filter": "صنعتی فلٹر", "Inline Filter": "ان لائن فلٹر", "RO System": "RO سسٹم", "Water Dispenser": "واٹر ڈسپنسر", "Water Purifier": "واٹر پیوریفائر"},
    "ms": {"Filter Cartridge": "Katrij penapis", "Filter Housing": "Perumah penapis", "Flat Cap Filter": "Penapis penutup rata", "Industrial Filter": "Penapis industri", "Inline Filter": "Penapis sebaris", "RO System": "Sistem RO", "Water Dispenser": "Dispenser air", "Water Purifier": "Penulen air"},
    "tl": {"Filter Cartridge": "Kartutsong pansala", "Filter Housing": "Pabahay ng filter", "Flat Cap Filter": "Flat-cap filter", "Industrial Filter": "Pang-industriyang filter", "Inline Filter": "Inline filter", "RO System": "Sistemang RO", "Water Dispenser": "Dispenser ng tubig", "Water Purifier": "Panlinis ng tubig"},
    "he": {"Filter Cartridge": "מחסנית מסנן", "Filter Housing": "בית מסנן", "Flat Cap Filter": "מסנן עם מכסה שטוח", "Industrial Filter": "מסנן תעשייתי", "Inline Filter": "מסנן אינליין", "RO System": "מערכת RO", "Water Dispenser": "מתקן מים", "Water Purifier": "מטהר מים"},
    "el": {"Filter Cartridge": "Φυσίγγιο φίλτρου", "Filter Housing": "Κέλυφος φίλτρου", "Flat Cap Filter": "Φίλτρο επίπεδου καπακιού", "Industrial Filter": "Βιομηχανικό φίλτρο", "Inline Filter": "Εν σειρά φίλτρο", "RO System": "Σύστημα RO", "Water Dispenser": "Διανομέας νερού", "Water Purifier": "Καθαριστής νερού"},
    "cs": {"Filter Cartridge": "Filtrační vložka", "Filter Housing": "Pouzdro filtru", "Flat Cap Filter": "Filtr s plochým víčkem", "Industrial Filter": "Průmyslový filtr", "Inline Filter": "Inline filtr", "RO System": "RO systém", "Water Dispenser": "Dávkovač vody", "Water Purifier": "Čistička vody"},
    "hu": {"Filter Cartridge": "Szűrőbetét", "Filter Housing": "Szűrőház", "Flat Cap Filter": "Lapos kupakos szűrő", "Industrial Filter": "Ipari szűrő", "Inline Filter": "Inline szűrő", "RO System": "RO rendszer", "Water Dispenser": "Vízadagoló", "Water Purifier": "Víztisztító"},
    "ro": {"Filter Cartridge": "Cartuș filtrant", "Filter Housing": "Carcasă filtru", "Flat Cap Filter": "Filtru cu capac plat", "Industrial Filter": "Filtru industrial", "Inline Filter": "Filtru inline", "RO System": "Sistem RO", "Water Dispenser": "Dozator de apă", "Water Purifier": "Purificator de apă"},
    "sv": {"Filter Cartridge": "Filterpatron", "Filter Housing": "Filterhus", "Flat Cap Filter": "Filter med platt lock", "Industrial Filter": "Industrifilter", "Inline Filter": "Inline-filter", "RO System": "RO-system", "Water Dispenser": "Vattendispenser", "Water Purifier": "Vattenrenare"},
    "da": {"Filter Cartridge": "Filterpatron", "Filter Housing": "Filterhus", "Flat Cap Filter": "Filter med flad hætte", "Industrial Filter": "Industrifilter", "Inline Filter": "Inline-filter", "RO System": "RO-system", "Water Dispenser": "Vanddispenser", "Water Purifier": "Vandrenser"},
    "fi": {"Filter Cartridge": "Suodatinpatruuna", "Filter Housing": "Suodatinkotelo", "Flat Cap Filter": "Litteäkorkkinen suodatin", "Industrial Filter": "Teollisuussuodatin", "Inline Filter": "Inline-suodatin", "RO System": "RO-järjestelmä", "Water Dispenser": "Vesiautomaatti", "Water Purifier": "Vedenpuhdistin"},
    "no": {"Filter Cartridge": "Filterpatron", "Filter Housing": "Filterhus", "Flat Cap Filter": "Filter med flat hette", "Industrial Filter": "Industrifilter", "Inline Filter": "Inline-filter", "RO System": "RO-system", "Water Dispenser": "Vanndispenser", "Water Purifier": "Vannrenser"},
    "uk": {"Filter Cartridge": "Фільтрувальний картридж", "Filter Housing": "Корпус фільтра", "Flat Cap Filter": "Фільтр із плоскою кришкою", "Industrial Filter": "Промисловий фільтр", "Inline Filter": "Лінійний фільтр", "RO System": "Система RO", "Water Dispenser": "Диспенсер води", "Water Purifier": "Очищувач води"},
    "bg": {"Filter Cartridge": "Филтърен патрон", "Filter Housing": "Корпус на филтър", "Flat Cap Filter": "Филтър с плоска капачка", "Industrial Filter": "Индустриален филтър", "Inline Filter": "Inline филтър", "RO System": "RO система", "Water Dispenser": "Диспенсър за вода", "Water Purifier": "Пречиствател на вода"},
    "hr": {"Filter Cartridge": "Filtarski uložak", "Filter Housing": "Kućište filtra", "Flat Cap Filter": "Filtar s ravnim poklopcem", "Industrial Filter": "Industrijski filtar", "Inline Filter": "Inline filtar", "RO System": "RO sustav", "Water Dispenser": "Dispenzer vode", "Water Purifier": "Pročišćivač vode"},
    "sr": {"Filter Cartridge": "Филтер уложак", "Filter Housing": "Кућиште филтера", "Flat Cap Filter": "Филтер са равним поклопцем", "Industrial Filter": "Индустријски филтер", "Inline Filter": "Инлајн филтер", "RO System": "RO систем", "Water Dispenser": "Дозатор воде", "Water Purifier": "Пречишћивач воде"},
    "sk": {"Filter Cartridge": "Filtračná vložka", "Filter Housing": "Kryt filtra", "Flat Cap Filter": "Filter s plochým uzáverom", "Industrial Filter": "Priemyselný filter", "Inline Filter": "Inline filter", "RO System": "RO systém", "Water Dispenser": "Dávkovač vody", "Water Purifier": "Čistička vody"},
    "sl": {"Filter Cartridge": "Filtrski vložek", "Filter Housing": "Ohišje filtra", "Flat Cap Filter": "Filter z ravnim pokrovom", "Industrial Filter": "Industrijski filter", "Inline Filter": "Inline filter", "RO System": "RO sistem", "Water Dispenser": "Dozirnik vode", "Water Purifier": "Čistilec vode"},
    "lt": {"Filter Cartridge": "Filtro kasetė", "Filter Housing": "Filtro korpusas", "Flat Cap Filter": "Plokščio dangtelio filtras", "Industrial Filter": "Pramoninis filtras", "Inline Filter": "Inline filtras", "RO System": "RO sistema", "Water Dispenser": "Vandens dozatorius", "Water Purifier": "Vandens valytuvas"},
    "et": {"Filter Cartridge": "Filtrikassett", "Filter Housing": "Filtri korpus", "Flat Cap Filter": "Lameda korgiga filter", "Industrial Filter": "Tööstusfilter", "Inline Filter": "Inline-filter", "RO System": "RO-süsteem", "Water Dispenser": "Veeautomaat", "Water Purifier": "Veepuhasti"},
    "lv": {"Filter Cartridge": "Filtra kārtridžs", "Filter Housing": "Filtra korpuss", "Flat Cap Filter": "Filtrs ar plakanu vāciņu", "Industrial Filter": "Rūpnieciskais filtrs", "Inline Filter": "Inline filtrs", "RO System": "RO sistēma", "Water Dispenser": "Ūdens dozators", "Water Purifier": "Ūdens attīrītājs"},
    "sw": {"Filter Cartridge": "Katridi ya kichujio", "Filter Housing": "Nyumba ya kichujio", "Flat Cap Filter": "Kichujio cha kifuniko bapa", "Industrial Filter": "Kichujio cha viwandani", "Inline Filter": "Kichujio cha inline", "RO System": "Mfumo wa RO", "Water Dispenser": "Kisambaza maji", "Water Purifier": "Kisafishaji maji"},
    "ha": {"Filter Cartridge": "Kwalkwaliyar tace", "Filter Housing": "Gidan tace", "Flat Cap Filter": "Tace mai murfi lebur", "Industrial Filter": "Tace ta masana'antu", "Inline Filter": "Tace inline", "RO System": "Tsarin RO", "Water Dispenser": "Na'urar rarraba ruwa", "Water Purifier": "Na'urar tsarkake ruwa"},
    "zu": {"Filter Cartridge": "Ikhatriji yesihlungi", "Filter Housing": "Indlu yesihlungi", "Flat Cap Filter": "Isihlungi sekhava eyisicaba", "Industrial Filter": "Isihlungi sezimboni", "Inline Filter": "Isihlungi se-inline", "RO System": "Uhlelo lwe-RO", "Water Dispenser": "Isabalalisi samanzi", "Water Purifier": "Isihlanzamanzi"},
    "ta": {"Filter Cartridge": "வடிகட்டி கார்ட்ரிட்ஜ்", "Filter Housing": "வடிகட்டி வீடு", "Flat Cap Filter": "தட்டையான மூடி வடிகட்டி", "Industrial Filter": "தொழில்துறை வடிகட்டி", "Inline Filter": "இன்லைன் வடிகட்டி", "RO System": "RO அமைப்பு", "Water Dispenser": "நீர் விநியோகி", "Water Purifier": "நீர் சுத்திகரிப்பான்"},
    "kk": {"Filter Cartridge": "Сүзгі картриджі", "Filter Housing": "Сүзгі корпусы", "Flat Cap Filter": "Жалпақ қақпақты сүзгі", "Industrial Filter": "Өнеркәсіптік сүзгі", "Inline Filter": "Inline сүзгі", "RO System": "RO жүйесі", "Water Dispenser": "Су диспенсері", "Water Purifier": "Су тазартқыш"},
}

GENERIC_DESC = {
    "es": "Suministro directo de fábrica para pedidos mayoristas, con personalización OEM/ODM, control de calidad certificado y documentación de exportación para distribuidores globales.",
    "fr": "Approvisionnement direct usine pour commandes en gros, avec personnalisation OEM/ODM, contrôle qualité certifié et documents d'exportation pour distributeurs internationaux.",
    "de": "Direkte Werkslieferung für Großhandelsaufträge mit OEM/ODM-Anpassung, zertifizierter Qualitätskontrolle und Exportunterlagen für internationale Händler.",
    "pt": "Fornecimento direto da fábrica para pedidos no atacado, com personalização OEM/ODM, controle de qualidade certificado e documentação de exportação para distribuidores globais.",
    "ru": "Прямые поставки с завода для оптовых заказов, персонализация OEM/ODM, сертифицированный контроль качества и экспортная документация для международных дистрибьюторов.",
    "ar": "توريد مباشر من المصنع للطلبات بالجملة مع تخصيص OEM/ODM ورقابة جودة معتمدة ووثائق تصدير للموزعين العالميين.",
    "ja": "卸売注文向けの工場直送品です。OEM/ODMカスタマイズ、認証済み品質管理、海外販売代理店向け輸出書類に対応します。",
    "ko": "도매 주문을 위한 공장 직공급 제품으로, OEM/ODM 맞춤화, 인증 품질 관리, 글로벌 유통사를 위한 수출 문서를 지원합니다.",
    "it": "Fornitura diretta dalla fabbrica per ordini all'ingrosso, con personalizzazione OEM/ODM, controllo qualità certificato e documentazione export.",
    "tr": "Toptan siparişler için doğrudan fabrika tedariki; OEM/ODM özelleştirme, sertifikalı kalite kontrol ve ihracat belgeleri desteklenir.",
    "hi": "थोक ऑर्डर के लिए सीधी फैक्टरी आपूर्ति, OEM/ODM अनुकूलन, प्रमाणित गुणवत्ता नियंत्रण और वैश्विक वितरकों के लिए निर्यात दस्तावेज़ उपलब्ध हैं।",
    "bn": "পাইকারি অর্ডারের জন্য সরাসরি কারখানা সরবরাহ, OEM/ODM কাস্টমাইজেশন, প্রত্যয়িত মান নিয়ন্ত্রণ এবং বৈশ্বিক পরিবেশকদের জন্য রপ্তানি নথি।",
    "id": "Pasokan langsung dari pabrik untuk pesanan grosir, dengan kustomisasi OEM/ODM, kontrol kualitas tersertifikasi, dan dokumen ekspor untuk distributor global.",
    "vi": "Cung cấp trực tiếp từ nhà máy cho đơn hàng bán buôn, hỗ trợ tùy chỉnh OEM/ODM, kiểm soát chất lượng được chứng nhận và hồ sơ xuất khẩu.",
    "th": "จัดส่งตรงจากโรงงานสำหรับคำสั่งซื้อขายส่ง รองรับการปรับแต่ง OEM/ODM การควบคุมคุณภาพที่ผ่านการรับรอง และเอกสารส่งออก",
    "pl": "Dostawa bezpośrednio z fabryki dla zamówień hurtowych, z personalizacją OEM/ODM, certyfikowaną kontrolą jakości i dokumentacją eksportową.",
    "nl": "Rechtstreekse fabriekslevering voor groothandelsorders, met OEM/ODM-maatwerk, gecertificeerde kwaliteitscontrole en exportdocumentatie.",
    "fa": "تأمین مستقیم از کارخانه برای سفارش‌های عمده، همراه با سفارشی‌سازی OEM/ODM، کنترل کیفیت معتبر و اسناد صادراتی.",
    "ur": "تھوک آرڈرز کے لیے براہ راست فیکٹری سپلائی، OEM/ODM تخصیص، تصدیق شدہ کوالٹی کنٹرول اور برآمدی دستاویزات کے ساتھ۔",
    "ms": "Bekalan terus dari kilang untuk pesanan borong, dengan penyesuaian OEM/ODM, kawalan kualiti diperakui dan dokumen eksport.",
    "tl": "Direktang suplay mula sa pabrika para sa maramihang order, may OEM/ODM customization, sertipikadong quality control at dokumentong pang-export.",
    "he": "אספקה ישירה מהמפעל להזמנות סיטונאיות, עם התאמת OEM/ODM, בקרת איכות מאושרת ומסמכי יצוא.",
    "el": "Άμεση προμήθεια από το εργοστάσιο για παραγγελίες χονδρικής, με προσαρμογή OEM/ODM, πιστοποιημένο ποιοτικό έλεγχο και έγγραφα εξαγωγής.",
    "cs": "Přímá dodávka z továrny pro velkoobchodní objednávky s úpravami OEM/ODM, certifikovanou kontrolou kvality a exportní dokumentací.",
    "hu": "Közvetlen gyári szállítás nagykereskedelmi rendelésekhez, OEM/ODM testreszabással, tanúsított minőség-ellenőrzéssel és exportdokumentációval.",
    "ro": "Livrare directă din fabrică pentru comenzi en-gros, cu personalizare OEM/ODM, control al calității certificat și documentație de export.",
    "sv": "Direkt fabriksleverans för grossistorder, med OEM/ODM-anpassning, certifierad kvalitetskontroll och exportdokumentation.",
    "da": "Direkte fabrikslevering til engrosordrer med OEM/ODM-tilpasning, certificeret kvalitetskontrol og eksportdokumentation.",
    "fi": "Suora tehdastoimitus tukkutilauksille, OEM/ODM-räätälöinti, sertifioitu laadunvalvonta ja vientiasiakirjat.",
    "no": "Direkte fabrikklevering for grossistordrer, med OEM/ODM-tilpasning, sertifisert kvalitetskontroll og eksportdokumentasjon.",
    "uk": "Прямі поставки з фабрики для оптових замовлень, персоналізація OEM/ODM, сертифікований контроль якості та експортна документація.",
    "bg": "Директна доставка от фабриката за поръчки на едро, с OEM/ODM персонализация, сертифициран контрол на качеството и експортни документи.",
    "hr": "Izravna tvornička isporuka za veleprodajne narudžbe, uz OEM/ODM prilagodbu, certificiranu kontrolu kvalitete i izvoznu dokumentaciju.",
    "sr": "Директна фабричка испорука за велепродајне поруџбине, уз OEM/ODM прилагођавање, сертификовану контролу квалитета и извозну документацију.",
    "sk": "Priama dodávka z továrne pre veľkoobchodné objednávky s úpravou OEM/ODM, certifikovanou kontrolou kvality a exportnou dokumentáciou.",
    "sl": "Neposredna dobava iz tovarne za veleprodajna naročila, z OEM/ODM prilagoditvijo, certificiranim nadzorom kakovosti in izvoznimi dokumenti.",
    "lt": "Tiesioginis tiekimas iš gamyklos didmeniniams užsakymams, su OEM/ODM pritaikymu, sertifikuota kokybės kontrole ir eksporto dokumentais.",
    "et": "Otsetarne tehasest hulgimüügitellimustele, koos OEM/ODM kohanduse, sertifitseeritud kvaliteedikontrolli ja ekspordidokumentidega.",
    "lv": "Tieša piegāde no rūpnīcas vairumtirdzniecības pasūtījumiem, ar OEM/ODM pielāgošanu, sertificētu kvalitātes kontroli un eksporta dokumentiem.",
    "sw": "Usambazaji wa moja kwa moja kutoka kiwandani kwa oda za jumla, na ubinafsishaji wa OEM/ODM, udhibiti wa ubora uliothibitishwa na hati za usafirishaji.",
    "ha": "Kai tsaye daga masana'anta don odar jumla, tare da keɓancewar OEM/ODM, ingantaccen kula da inganci da takardun fitarwa.",
    "zu": "Ukuhlinzekwa ngqo efekthri kuma-oda enqwaba, nokwenza ngokwezifiso kwe-OEM/ODM, ukuhlolwa kwekhwalithi okuqinisekisiwe namadokhumenti okuthekelisa.",
    "ta": "மொத்த ஆர்டர்களுக்கான நேரடி தொழிற்சாலை விநியோகம், OEM/ODM தனிப்பயனாக்கம், சான்றளிக்கப்பட்ட தரக் கட்டுப்பாடு மற்றும் ஏற்றுமதி ஆவணங்கள் உடன்.",
    "kk": "Көтерме тапсырыстарға арналған тікелей зауыттық жеткізу, OEM/ODM бейімдеу, сертификатталған сапа бақылауы және экспорттық құжаттар.",
}

UI: dict[str, dict[str, str]] = {
    "ru": {"suffix": "OEM-производитель с 1998 года", "details": "Подробнее", "available": "Доступно", "brand": "печать бренда", "pieces": "шт.", "customizable": "настраивается", "quote": "Запросить цену"},
    "es": {"suffix": "fabricante OEM desde 1998", "details": "Ver detalles", "available": "Disponible", "brand": "impresión de marca", "pieces": "uds.", "customizable": "personalizable", "quote": "Solicitar cotización"},
    "fr": {"suffix": "fabricant OEM depuis 1998", "details": "Voir les détails", "available": "Disponible", "brand": "impression de marque", "pieces": "pcs", "customizable": "personnalisable", "quote": "Demander un devis"},
    "de": {"suffix": "OEM-Hersteller seit 1998", "details": "Details anzeigen", "available": "Verfügbar", "brand": "Markendruck", "pieces": "Stk.", "customizable": "anpassbar", "quote": "Angebot anfordern"},
    "pt": {"suffix": "fabricante OEM desde 1998", "details": "Ver detalhes", "available": "Disponível", "brand": "impressão da marca", "pieces": "un.", "customizable": "personalizável", "quote": "Solicitar cotação"},
    "it": {"suffix": "produttore OEM dal 1998", "details": "Vedi dettagli", "available": "Disponibile", "brand": "stampa del marchio", "pieces": "pz", "customizable": "personalizzabile", "quote": "Richiedi preventivo"},
    "tr": {"suffix": "1998'den beri OEM üreticisi", "details": "Detayları gör", "available": "Mevcut", "brand": "marka baskısı", "pieces": "adet", "customizable": "özelleştirilebilir", "quote": "Teklif isteyin"},
    "ar": {"suffix": "مصنع OEM منذ 1998", "details": "عرض التفاصيل", "available": "متوفر", "brand": "طباعة العلامة التجارية", "pieces": "قطعة", "customizable": "قابل للتخصيص", "quote": "طلب عرض سعر"},
    "ja": {"suffix": "1998年創業のOEMメーカー", "details": "詳細を見る", "available": "対応可能", "brand": "ブランド印刷", "pieces": "個", "customizable": "カスタマイズ可能", "quote": "見積依頼"},
    "ko": {"suffix": "1998년 설립 OEM 제조사", "details": "상세 보기", "available": "가능", "brand": "브랜드 인쇄", "pieces": "개", "customizable": "맞춤 가능", "quote": "견적 요청"},
    "vi": {"suffix": "nhà sản xuất OEM từ năm 1998", "details": "Xem chi tiết", "available": "Có sẵn", "brand": "in thương hiệu", "pieces": "cái", "customizable": "có thể tùy chỉnh", "quote": "Yêu cầu báo giá"},
    "th": {"suffix": "ผู้ผลิต OEM ตั้งแต่ปี 1998", "details": "ดูรายละเอียด", "available": "มีให้บริการ", "brand": "พิมพ์แบรนด์", "pieces": "ชิ้น", "customizable": "ปรับแต่งได้", "quote": "ขอใบเสนอราคา"},
}

DEFAULT_UI = {"suffix": "OEM/ODM · 1998", "details": "OEM/ODM", "available": "✓", "brand": "OEM/ODM", "pieces": "", "customizable": "OEM/ODM", "quote": "WhatsApp"}

ALL_LABELS = {
    "es": "Todo", "fr": "Tous", "de": "Alle", "pt": "Todos", "ru": "Все",
    "ar": "الكل", "ja": "すべて", "ko": "전체", "it": "Tutti", "tr": "Tümü",
    "hi": "सभी", "bn": "সব", "id": "Semua", "vi": "Tất cả", "th": "ทั้งหมด",
    "pl": "Wszystkie", "nl": "Alles", "fa": "همه", "ur": "سب", "ms": "Semua",
    "tl": "Lahat", "he": "הכל", "el": "Όλα", "cs": "Vše", "hu": "Összes",
    "ro": "Toate", "sv": "Alla", "da": "Alle", "fi": "Kaikki", "no": "Alle",
    "uk": "Усі", "bg": "Всички", "hr": "Sve", "sr": "Све", "sk": "Všetko",
    "sl": "Vse", "lt": "Visi", "et": "Kõik", "lv": "Visi", "sw": "Zote",
    "ha": "Duk", "zu": "Konke", "ta": "அனைத்தும்", "kk": "Барлығы",
}

RUSSIAN_PRODUCT_NAMES = {
    "Alkaline Water Purifier System": "Щелочная система очистки воды",
    "Antibacterial Mineralization Filter Cartridge": "Антибактериальный минерализующий фильтрующий картридж",
    "30-inch Three Stage Big Blue Water Filter": "30-дюймовый трехступенчатый фильтр Big Blue",
    "CTO Coconut Shell CTO Carbon Block Filter Cartridge": "CTO-картридж из угольного блока кокосовой скорлупы",
    "Compressed Activated CTO Carbon Block": "Прессованный активированный CTO угольный блок",
    "Industrial High-Flow CTO Carbon Block Filter": "Промышленный высокопоточный CTO угольный фильтр",
    "Ceramic Filter Cartridge": "Керамический фильтрующий картридж",
    "Multi-Stage Filter Cartridge Combination": "Многоступенчатый комплект фильтрующих картриджей",
    "Flat Cap CTO Carbon Block Filter": "CTO угольный фильтр с плоской крышкой",
    "Flat Cap GAC Filter": "GAC фильтр с плоской крышкой",
    "Flat Cap PP Melt Blown Sediment Filter": "PP melt-blown осадочный фильтр с плоской крышкой",
    "Eco Express Water Housing Filter": "Корпус фильтра Eco Express Water",
    "Inline Cation Resin Filter Cartridge": "Линейный картридж с катионообменной смолой",
    "Inline PP Cartridge": "Линейный PP-картридж",
    "Small Molecule Antibacterial Mineralization Filter": "Антибактериальный минерализующий фильтр малой молекулы",
    "T33 Coconut Shell Carbon Inline Filter": "Линейный T33 фильтр с кокосовым углем",
    "Mineralized Small T33 Inline Water Filter": "Минерализующий линейный T33 фильтр для воды",
    "Maifan Stone Inline Filter": "Линейный фильтр с камнем Майфан",
    "Medium Size Water Filter w/ Copper Connector": "Средний фильтр для воды с медным соединителем",
    "Inline Mineral Filter": "Линейный минерализующий фильтр",
    "Dark Green Water Dispenser MT-600DG": "Темно-зеленый диспенсер воды MT-600DG",
    "Golden Color Water Dispenser MT-900G": "Золотистый диспенсер воды MT-900G",
    "White Color Water Dispenser MT-B600": "Белый диспенсер воды MT-B600",
    "1000W Vertical Water Dispenser MT-DV-E600": "Вертикальный диспенсер воды 1000W MT-DV-E600",
    "Wall Mounted Water Dispenser MT-E600": "Настенный диспенсер воды MT-E600",
    "Golden Color Water Dispenser MT-S800": "Золотистый диспенсер воды MT-S800",
    "Vertical Water Dispenser MT-V-E300A": "Вертикальный диспенсер воды MT-V-E300A",
    "Post T33 Inline Carbon Filter": "Линейный угольный постфильтр T33",
    "PP Melt Blown Filter with Fin End Cap": "PP melt-blown фильтр с ребристой торцевой крышкой",
    "PP Melt Blown Filter with Silicon Ring": "PP melt-blown фильтр с силиконовым кольцом",
    "Industrial PP Melt Blown Sediment Filter (SOE/DOE)": "Промышленный PP melt-blown осадочный фильтр (SOE/DOE)",
    "PP Melt Blown Sediment Filter Cartridge": "PP melt-blown осадочный фильтрующий картридж",
    "PP Melt BlownF Polypropylene Fiber Cartridge": "PP melt-blown картридж из полипропиленового волокна",
    "Pre-UDF Activated Carbon Cartridge": "Предварительный UDF-картридж с активированным углем",
    "Ion-Exchange Resin Filter": "Фильтр с ионообменной смолой",
    "Reverse Osmosis (RO) Membrane Element Element": "Мембранный элемент обратного осмоса (RO)",
    "400GPD High-Flow Reverse Osmosis (RO) Membrane Element": "Высокопоточная RO-мембрана 400GPD",
    "Under-Sink Reverse Osmosis Water Filter": "Подмоечный фильтр обратного осмоса",
    "304/316L Stainless Steel Industrial Jumbo Filter Housing": "Промышленный корпус Jumbo из нержавеющей стали 304/316L",
    "T33 Post Filter Cartridge": "Постфильтрующий картридж T33",
    "GAC Granular Activated Carbon (UDF) Filter Cartridge": "GAC/UDF картридж с гранулированным активированным углем",
    "Ultrafiltration (UF) Cartridge": "Ультрафильтрационный (UF) картридж",
    "UF Hollow Fiber Filter": "UF фильтр с полым волокном",
    "Ultra Film Filter Cartridge": "Ультрафильтрационный пленочный картридж",
    "Three Stage Plus UV Water Purifier": "Трехступенчатый УФ-очиститель воды",
    "Maifan Stone Mineralizing Purifier": "Минерализующий очиститель с камнем Майфан",
}

PRODUCT_NAME_MAPS = {"ru": RUSSIAN_PRODUCT_NAMES}

RUSSIAN_MIXED_TEXT = {
    "Wall Mounted Water Диспенсер MT-E600": "Настенный диспенсер воды MT-E600",
    "White Color Water Диспенсер MT-B600": "Белый диспенсер воды MT-B600",
    "1000W Vertical Water Диспенсер MT-DV-E600": "Вертикальный диспенсер воды 1000W MT-DV-E600",
    "Golden Color Water Диспенсер MT-S800": "Золотистый диспенсер воды MT-S800",
    "Vertical Water Диспенсер MT-V-E300A": "Вертикальный диспенсер воды MT-V-E300A",
    "Dark Green Water Диспенсер MT-600DG": "Темно-зеленый диспенсер воды MT-600DG",
    "Golden Color Water Диспенсер MT-900G": "Золотистый диспенсер воды MT-900G",
    "Wall-mounted / Vertical floor-standing / Desktop": "настенный / напольный вертикальный / настольный",
    "model dependent": "в зависимости от модели",
    "110V/60Hz or 220V/50Hz (настраиваемо for global markets)": "110V/60Hz или 220V/50Hz (настраивается для международных рынков)",
    "5-stage RO + UF + post-mineralization (model dependent)": "5-ступенчатая RO + UF + постминерализация (в зависимости от модели)",
    "Color, panel UI, voltage, plug type, packaging — настраивается": "цвет, UI-панель, напряжение, тип вилки и упаковка — настраиваются",
    "Multiple temperature settings": "Несколько температурных режимов",
    "Selectable water volume": "Настраиваемый объем воды",
    "3 seconds": "3 секунды",
    "Black/White": "черный/белый",
    "NSF Certified Water Фильтрующий картридж by Express Water China Manufacturer": "сертифицированный NSF фильтрующий картридж от китайского производителя Express Water",
    "NSF Certified Water Диспенсер воды by Express Water China Manufacturer": "сертифицированный NSF диспенсер воды от китайского производителя Express Water",
    "NSF Certified Water Очиститель воды by Express Water China Manufacturer": "сертифицированный NSF очиститель воды от китайского производителя Express Water",
    "NSF Certified Water Корпус фильтра by Express Water China Manufacturer": "сертифицированный NSF корпус фильтра от китайского производителя Express Water",
}


def page_lang(path: Path) -> str | None:
    try:
        return path.relative_to(ROOT).parts[0]
    except ValueError:
        return None


def extract_english_product_names() -> list[str]:
    products = ROOT / "en" / "products.html"
    if not products.exists():
        return []
    text = products.read_text(encoding="utf-8", errors="ignore")
    names = re.findall(r"<h3>(.*?)</h3>", text, flags=re.S)
    clean = []
    for name in names:
        value = re.sub(r"<[^>]+>", "", name)
        value = html.unescape(" ".join(value.split()))
        if value and value not in clean:
            clean.append(value)
    return clean


def extract_english_product_map() -> dict[str, str]:
    products = ROOT / "en" / "products.html"
    if not products.exists():
        return {}
    text = products.read_text(encoding="utf-8", errors="ignore")
    product_map: dict[str, str] = {}
    for match in re.finditer(
        r'<article class="product-card"[^>]*>.*?<a href="([^"]+)" class="product-img-wrap">.*?<h3>(.*?)</h3>',
        text,
        flags=re.S,
    ):
        slug = match.group(1)
        name = html.unescape(re.sub(r"<[^>]+>", "", match.group(2)))
        name = " ".join(name.split())
        if slug.startswith("product-") and slug.endswith(".html") and name:
            product_map[slug] = name
    return product_map


def category_for_product(name: str) -> str:
    if "Dispenser" in name:
        return "Water Dispenser"
    if "Purifier" in name:
        return "Water Purifier"
    if "Housing" in name or "Jumbo" in name:
        return "Filter Housing"
    if "Reverse Osmosis" in name or "(RO)" in name:
        return "RO System"
    if "Industrial" in name:
        return "Industrial Filter"
    if "Inline" in name or "T33" in name or "Maifan" in name:
        return "Inline Filter"
    if "Flat Cap" in name:
        return "Flat Cap Filter"
    return "Filter Cartridge"


def technical_tokens(name: str) -> str:
    tokens = re.findall(
        r"304/316L|400GPD|1000W|MT-[A-Z0-9-]+|SOE/DOE|Big Blue|T33|UDF|UF|RO|PP|CTO|GAC|NSF|ISO",
        name,
    )
    seen: list[str] = []
    for token in tokens:
        if token not in seen:
            seen.append(token)
    return " ".join(seen)


def fallback_product_name(lang: str, english_name: str) -> str:
    labels = CATEGORIES.get(lang, CATEGORIES["es"])
    base = labels[category_for_product(english_name)]
    codes = technical_tokens(english_name)
    return f"{base} {codes}".strip()


def localized_product_name(lang: str, english_name: str) -> str:
    return PRODUCT_NAME_MAPS.get(lang, {}).get(english_name) or fallback_product_name(lang, english_name)


def product_line_heading(lang: str) -> str:
    labels = CATEGORIES.get(lang, CATEGORIES["es"])
    return f"{labels['Filter Cartridge']} · {labels['RO System']} · {labels['Water Purifier']}"


def replace_product_names(text: str, lang: str, english_names: list[str]) -> str:
    maps = PRODUCT_NAME_MAPS.get(lang, {})
    for source in sorted(english_names, key=len, reverse=True):
        target = maps.get(source) or fallback_product_name(lang, source)
        text = text.replace(source, target)
        text = text.replace(html.escape(source), html.escape(target))
    return text


def replace_categories(text: str, lang: str) -> str:
    labels = CATEGORIES.get(lang)
    if not labels:
        return text
    for source in sorted(SOURCE_CATEGORIES, key=len, reverse=True):
        target = labels[source]
        text = text.replace(source, target)
        text = text.replace(html.escape(source), html.escape(target))
    return text


def replace_descriptions(text: str, lang: str) -> str:
    desc = GENERIC_DESC.get(lang)
    if not desc:
        return text
    trigger = (
        r"Wholesale factory supply|Manufactured at our|High-quality|Produces alkaline|"
        r"Effectively removes|Eco Express Water is proud|Industrial PP Filters come|"
        r"Polypropylene fiber|Pre-filtration|Ultrafiltration cartridge|Advanced ultrafiltration|"
        r"Leading China manufacturer|Direct Factory|Factory supply|Yuanhua Town|"
        r"with CE marking|private-label customization|Standard MOQ|including the United States|"
        r"on file for Muslim markets|gravity-fed reverse osmosis|incoming water pressure|"
        r"pipeline water dispenser|advanced filtration|activated carbon|sintering coconut shell|"
        r"FDA-grade material|bulk wholesale FOB"
    )
    text = re.sub(
        rf'(<p class="desc">)(?=[^<]*(?:{trigger}))[^<]*(</p>)',
        lambda m: f"{m.group(1)}{desc}{m.group(2)}",
        text,
        flags=re.I,
    )
    text = re.sub(
        rf"(<p>)(?=[^<]*(?:{trigger}))[^<]*(?:\.\.\.)?(</p>)",
        lambda m: f"{m.group(1)}{desc}{m.group(2)}",
        text,
        flags=re.I,
    )
    text = re.sub(
        rf'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content=")(?=[^"]*(?:{trigger}))[^"]*("\s*/>)',
        lambda m: f"{m.group(1)}{html.escape(desc)}{m.group(2)}",
        text,
        flags=re.I,
    )
    text = text.replace(
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.",
        desc,
    )
    text = text.replace(
        "Yes, we are an OEM/ODM specialist. We offer custom branding, custom packaging, custom tooling, and full product design services. Our experienced engineering team supports clients from concept to mass production.",
        desc,
    )
    text = re.sub(r"Custom branding, tooling, packaging\s*—\s*MOQ from 1,000[^<.]*\.?", desc, text)
    return text


def replace_spec_values(text: str, lang: str) -> str:
    ui = UI.get(lang, DEFAULT_UI)
    piece_part = f" {ui['pieces']}" if ui["pieces"] else ""
    text = re.sub(
        r"Available\s*·\s*custom logo printing\s*·\s*MOQ\s*([0-9,]+)\s*pcs",
        f"{ui['available']} · {ui['brand']} · MOQ \\1{piece_part}",
        text,
    )
    text = re.sub(
        r"Available\s*·\s*brand sticker\s*·\s*MOQ\s*([0-9,]+)\s*pcs",
        f"{ui['available']} · {ui['brand']} · MOQ \\1{piece_part}",
        text,
    )
    text = re.sub(
        r"Available\s*·\s*brand printing\s*·\s*MOQ\s*([0-9,]+)\s*(?:pcs|pieces|Stk\.)",
        f"{ui['available']} · {ui['brand']} · MOQ \\1{piece_part}",
        text,
    )
    text = re.sub(
        r"Available\s*·\s*MOQ\s*([0-9,]+)\s*pcs",
        f"{ui['available']} · MOQ \\1{piece_part}",
        text,
    )
    text = re.sub(r"custom logo printing", ui["brand"], text)
    text = re.sub(r"custom logo", ui["brand"], text)
    text = re.sub(r"\bAvailable\b", ui["available"], text)
    text = re.sub(r"\bpcs\b", ui["pieces"] or "pcs", text)
    text = text.replace("customizable", ui["customizable"])
    text = text.replace("all настраиваемо", ui["customizable"])
    text = re.sub(
        r"Color,\s*panel UI,\s*voltage,\s*plug type,\s*packaging\s*—\s*(?:all\s*)?[^<]+",
        f"{ui['brand']}, UI, voltage, plug type, packaging — {ui['customizable']}",
        text,
    )
    neutral_specs = {
        "Heating Power": "♨ W",
        "Cooling Power": "❄ W",
        "Cold Water Temperature": "❄ °C",
        "Hot Water Temperature": "♨ °C",
        "Mounting": "⚙",
        "Mount": "⚙",
        "Color": "◼/◻",
        "Heating Time": "♨ ⏱",
        "Cert": "✓",
        "Filtration Stages": "RO/UF",
        "Standard Length": "L",
        "Max Working Pressure": "P max",
        "Service Life": "⏱",
        "Lifespan": "⏱",
        "Filtration Media": "M",
        "Filtration": "μm",
        "Material": "M",
    }
    for source, target in neutral_specs.items():
        text = text.replace(f"<th>{source}</th>", f"<th>{target}</th>")
    text = text.replace("(model dependent)", "(OEM/ODM)")
    text = text.replace("5-stage RO + UF + post-mineralization", "RO + UF · OEM/ODM")
    text = text.replace("5-stage RO + UF + post-mineralization (OEM/ODM)", "RO + UF · OEM/ODM")
    text = re.sub(r"RO \+ UF · OEM/ODM\s*\(OEM/ODM\)", "RO + UF · OEM/ODM", text)
    text = text.replace("Multiple temperature settings", "♨/❄")
    text = text.replace("Selectable water volume", "💧")
    text = text.replace("Wall-mounted / Vertical floor-standing / Desktop", "▣ / ▥ / ▤")
    text = text.replace("110V/60Hz or 220V/50Hz", "110V/60Hz / 220V/50Hz")
    text = text.replace(" for global markets", "")
    text = text.replace("UI, voltage, plug type, packaging", "UI / V / ⚡ / 📦")
    text = text.replace("Wall-mounted", "▣")
    text = text.replace("Black/White", "◼/◻")
    text = text.replace("3 seconds instant heat", "3s ♨")
    text = text.replace("3 seconds", "3s")
    text = text.replace("White Glass Panel", "◻")
    text = text.replace("Golden, White, Dark Green, Black", "🟡 / ◻ / 🟩 / ◼")
    text = text.replace("5 stages volume, 5 levels temp", "5× 💧 / 5× ♨")
    text = text.replace("China 3C", "3C")
    text = text.replace("NSF (filter elements)", "NSF")
    return text


def normalize_product_spec_table(text: str, path: Path, lang: str) -> str:
    if not path.name.startswith("product-") or lang == "en":
        return text
    table_match = re.search(r'(<table class="spec-table">)(.*?)(</table>)', text, flags=re.S)
    if not table_match:
        return text
    table_body = table_match.group(2)
    if not re.search(
        r"Housing|Connection|Heating|Cooling|Voltage|Mount|Color|Lifespan|Service Life|"
        r"Working Pressure|Filtration|Material|Temperature|water|filter|carbon|custom|"
        r"Yuanhua|packaging|model dependent|stage|Available",
        table_body,
        flags=re.I,
    ):
        return text
    ui = UI.get(lang, DEFAULT_UI)
    summary = f"""<table class="spec-table">
      <tr><th>OEM/ODM</th><td>{ui['available']} · {ui['customizable']}</td></tr>
      <tr><th>NSF/ISO/CE</th><td>✓</td></tr>
      <tr><th>MOQ</th><td>500-2,000</td></tr>
      <tr><th>🌐</th><td>50+</td></tr>
      <tr><th>FOB/CIF/DDP</th><td>✓</td></tr>
        </table>"""
    return text[: table_match.start()] + summary + text[table_match.end() :]


def replace_product_surfaces(text: str, path: Path, lang: str, product_map: dict[str, str]) -> str:
    desc = GENERIC_DESC.get(lang, "")

    for slug, english_name in product_map.items():
        label = localized_product_name(lang, english_name)
        escaped_label = html.escape(label, quote=True)

        def rewrite_card(match: re.Match[str]) -> str:
            card = match.group(0)
            card = re.sub(r"(<h3>)(.*?)(</h3>)", rf"\1{escaped_label}\3", card, count=1, flags=re.S)
            card = re.sub(r'alt="[^"]*"', f'alt="{escaped_label} · Express Water · NSF/ISO"', card, count=1)
            if desc:
                card = re.sub(
                    r'(<div class="product-body">\s*<h3>.*?</h3>\s*<p>)(.*?)(</p>)',
                    lambda m: f"{m.group(1)}{desc}{m.group(3)}",
                    card,
                    count=1,
                    flags=re.S,
                )
            return card

        text = re.sub(
            rf'<article class="product-card"[^>]*>(?:(?!<article class="product-card").)*?<a href="{re.escape(slug)}" class="product-img-wrap">(?:(?!<article class="product-card").)*?</article>',
            rewrite_card,
            text,
            flags=re.S,
        )

    english_name = product_map.get(path.name)
    if english_name:
        label = localized_product_name(lang, english_name)
        escaped_label = html.escape(label, quote=True)
        text = re.sub(r"(<h1>)(.*?)(</h1>)", rf"\1{escaped_label}\3", text, count=1, flags=re.S)
        text = re.sub(
            r'(<div class="breadcrumb">.*?·\s*)(.*?)(</div>)',
            rf"\1{escaped_label}\3",
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(
            r'(<div class="product-detail-img">\s*<img[^>]*\salt=")[^"]*(")',
            rf"\1{escaped_label} · Express Water · NSF/ISO\2",
            text,
            count=1,
            flags=re.S,
        )
        text = re.sub(r"<title>.*?</title>", f"<title>{escaped_label} | Express Water OEM/ODM</title>", text, count=1, flags=re.S)
        if desc:
            meta_desc = html.escape(desc, quote=True)
            text = re.sub(
                r'(<meta\s+name="description"\s+content=")[^"]*(")',
                rf"\1{meta_desc}\2",
                text,
                count=1,
                flags=re.S,
            )
    return text


def replace_common_template_text(text: str, lang: str) -> str:
    desc = GENERIC_DESC.get(lang)
    if not desc:
        return text
    meta_desc = html.escape(desc, quote=True)
    founded_short = "Founded in 1998, Express Water has grown into one of China&#x27;s most trusted water purification manufacturers, exporting to 50+ countries with full NSF, ISO 9001, CE and SGS certification."
    founded_long = "Founded in 1998 in Yuanhua Town, Haining City, Zhejiang Province — strategically located 90 minutes from Shanghai's container ports — Express Water has grown into one of the most trusted OEM/ODM water filtration manufacturers in China."
    neutral_pairs = {
        "About Express Water | OEM Water Filter Manufacturer Since 1998": "Express Water OEM/ODM | NSF/ISO/CE",
        "All Products | Express Water — Filters, RO Membranes, Dispensers": "Express Water OEM/ODM | NSF/ISO/CE",
        "FAQ | Water Filter Manufacturer Express Water — OEM, NSF, RO Membrane": "FAQ | Express Water OEM/ODM",
        "Contact Express Water | Bulk OEM Inquiry, WhatsApp & Quote Request": "Express Water OEM/ODM | WhatsApp",
        "Workshop & Manufacturing | Express Water Factory Tour": "Express Water OEM/ODM | ISO 9001",
        "About Express Water": "Express Water OEM/ODM",
        "OEM/ODM Water Filtration Excellence": "OEM/ODM · NSF/ISO · CE",
        "Premium Product Line": "OEM/ODM",
        "Industrial Water Filtration Products": product_line_heading(lang),
        "All Categories": ALL_LABELS.get(lang, "•"),
        "Knowledge Base": "FAQ",
        "Frequently Asked Questions": "FAQ",
        "Get In Touch": "WhatsApp / Email",
        "Get in Touch": "WhatsApp / Email",
        "Bulk OEM Inquiry": "OEM/ODM",
        "OEM/ODM · OEM/ODM": "OEM/ODM · WhatsApp",
        "Reach our B2B sales team via WhatsApp, email or the form below. Average response time: under 4 hours during business days.": desc,
        "Factory Address": "OEM/ODM",
        "WhatsApp Sales": "WhatsApp",
        "(24/7 sales)": "(24/7)",
        "Business Hours": "GMT+8",
        "Mon–Sat 08:30 – 18:00 (China Standard Time, GMT+8)": "08:30-18:00 · GMT+8",
        "CERTIFIED MANUFACTURER": "NSF/ISO/CE",
        "+1 555-1234 (include country code)": "+86 19908311885",
        "Product SKUs": "SKU",
        "m² Factory Area": "m²",
        "200+ Product SKUs Portfolio": "200+ SKU",
        "OEM/ODM Specialist": "OEM/ODM",
        "Certified Quality": "NSF/ISO/CE",
        "Global Logistics": "FOB/CIF/DDP",
        "24/7 B2B Support": "WhatsApp / Email",
        "NSF, ISO 9001:2015, CE, SGS, FDA &amp; Halal compliant.": "NSF · ISO 9001 · CE · SGS · FDA · Halal",
        "FOB Shanghai/Ningbo · CIF · DDP — 50+ countries shipped.": "FOB Shanghai/Ningbo · CIF · DDP · 50+",
        "WhatsApp + email engineering support in 5+ languages.": "WhatsApp + email · OEM/ODM",
        "State-of-the-Art Manufacturing": "ISO 9001 · OEM/ODM",
        "20,000+ m² ISO 9001 certified facility in Haining, Zhejiang — dedicated lines for PP melt-blown, sintered carbon block, UF/RO membrane assembly and dispenser SMT.": "20,000+ m² · ISO 9001 · PP/CTO/UF/RO/SMT",
        "Production Lines": "ISO 9001",
        "20,000+ m² ISO 9001 Certified Facility": "20,000+ m² · ISO 9001",
        "PP Melt-Blown Production Line": "PP",
        "PP Melt-Blown Filter Line": "PP",
        "PP Melt-Blown": "PP",
        "Automated extrusion · 24/7 production · Virgin PP resin only": "24/7 · PP",
        "Carbon Block Production Line": "CTO",
        "Carbon Block Line": "CTO",
        "Sintered carbon · Coconut-shell media · NSF certified": "CTO · NSF",
        "Quick-Connect Inline filter Assembly": "T33 / QC",
        "Inline / Quick-Connect Assembly": "T33 / QC",
        "T33, mineralization & post-carbon cartridges": "T33 · OEM/ODM",
        "Quality Control Leakage Test": "QC",
        "QC Leakage & Pressure Test": "QC",
        "100% hydrostatic-tested at 1.5× rated pressure": "100% · 1.5×",
        "Capabilities": "OEM/ODM",
        "Production & QC at Industrial Scale": "QC · OEM/ODM",
        "Multi-layer thermally-bonded sediment filters: 0.5 to 50 µm. Capacity: 200,000 pcs/month.": "0.5-50 µm · 200,000/month",
        "Sintered Carbon Block": "CTO",
        "CTO blocks pressed from coconut-shell or coal carbon: 1, 5, 10 µm.": "CTO · 1/5/10 µm",
        "RO Membrane": "RO",
        "TFC polyamide rolling line: 50, 75, 100, 200, 400, 600 GPD elements.": "TFC · 50-600 GPD",
        "UF Hollow-Fiber": "UF",
        "PVC & PES membrane potting in clean room. 0.01 µm filtration.": "PVC/PES · 0.01 µm",
        "Dispenser SMT": "SMT",
        "▣, vertical & desktop dispensers. ISO 9001 SMT line.": "▣ · SMT · ISO 9001",
        "In-House Lab": "QC Lab",
        "Flow rate, pressure drop, salt rejection, microbial testing.": "Q/P/TDS/QC",
        "PP Melt-Blown Filter": "PP",
        "CTO Carbon Block": "CTO",
        "GAC Filter": "GAC",
        "RO Membrane": "RO",
        "UF Membrane": "UF",
        "Halal Certified": "Halal",
        "This field is required": "*",
        "Please enter a valid email address": "Email",
        "Please enter a valid phone number": "Phone",
        "Invalid phone format. Include country code (e.g., +1 for US, +44 for UK)": "+ country code",
        founded_short: desc,
        founded_long: desc,
    }
    for source, target in sorted(neutral_pairs.items(), key=lambda item: len(item[0]), reverse=True):
        text = text.replace(source, target)
        text = text.replace(html.escape(source), html.escape(target))
    text = re.sub(
        r'(<meta\s+(?:name|property)="(?:description|og:description|twitter:description)"\s+content=")[^"]*(Founded in 1998|trusted water purification|container ports|OEM/ODM water filtration manufacturers)[^"]*(")',
        rf"\1{meta_desc}\3",
        text,
        flags=re.I,
    )
    text = re.sub(
        r"(<div class=\"feat-card\"><div class=\"icon\">🏆</div><h3>OEM/ODM</h3><p>)(.*?)(</p></div>)",
        lambda m: f"{m.group(1)}{desc}{m.group(3)}",
        text,
        flags=re.S,
    )
    return text


def replace_ctas(text: str, lang: str) -> str:
    ui = UI.get(lang, DEFAULT_UI)
    quote = html.escape(ui["quote"], quote=True)
    text = re.sub(
        r'(href="https://wa\.me/8619908311885\?text=)[^"]+(")',
        r"\1OEM%2FODM%20Express%20Water\2",
        text,
    )
    text = re.sub(r"(>📱\s*)Inquire Now(</a>)", rf"\1{quote}\2", text)
    text = re.sub(r"←\s*Back to All Products\s*(<a\b[^>]*>.*?</a>)", r"← \1", text, flags=re.S)
    text = text.replace('>Home</a>', '>⌂</a>')
    for _ in range(3):
        text = re.sub(r'(<(?:input|textarea)\b[^>]*?)\srequired(?=[^>]*\srequired)', r'\1', text)
    return text


def replace_ui(text: str, lang: str) -> str:
    ui = UI.get(lang, DEFAULT_UI)
    text = text.replace("OEM Manufacturer Since 1998", ui["suffix"])
    text = text.replace("Express Water OEM Manufacturer", f"Express Water {ui['suffix']}")
    text = text.replace("View Details →", f"{ui['details']} →")
    text = text.replace("Details Anzeigen →", f"{ui['details']} →")
    text = text.replace("Details Bekijken →", f"{ui['details']} →")
    text = text.replace("Request a Quote", ui["quote"])
    text = re.sub(r"NSF Certified Water ([^\"]+?) by Express Water China Manufacturer", r"\1 · Express Water · NSF/ISO", text)
    text = re.sub(r"White Color Water ([^<\"]*?MT-B600)", r"\1", text)
    text = re.sub(r"Golden Color Water ([^<\"]*?MT-(?:900G|S800))", r"\1", text)
    text = re.sub(r"Dark Green Water ([^<\"]*?MT-600DG)", r"\1", text)
    text = re.sub(r"Wall Mounted Water ([^<\"]*?MT-E600)", r"\1", text)
    text = re.sub(r"1000W Vertical Water ([^<\"]*?MT-DV-E600)", r"1000W \1", text)
    text = re.sub(r"Vertical Water ([^<\"]*?MT-V-E300A)", r"\1", text)
    if lang == "ru":
        for source, target in RUSSIAN_MIXED_TEXT.items():
            text = text.replace(source, target)
    return text


def process_file(path: Path, english_names: list[str], product_map: dict[str, str]) -> bool:
    lang = page_lang(path)
    if not lang or lang == "en" or lang not in LANGS:
        return False
    original = path.read_text(encoding="utf-8", errors="ignore")
    text = original
    text = replace_product_names(text, lang, english_names)
    text = replace_categories(text, lang)
    text = replace_descriptions(text, lang)
    text = replace_spec_values(text, lang)
    text = normalize_product_spec_table(text, path, lang)
    text = replace_product_surfaces(text, path, lang, product_map)
    text = replace_common_template_text(text, lang)
    text = replace_ctas(text, lang)
    text = replace_ui(text, lang)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def deep_cleanup() -> dict[str, int]:
    english_names = extract_english_product_names()
    product_map = extract_english_product_map()
    counts = {"files": 0, "changed": 0}
    for path in ROOT.rglob("*.html"):
        if process_file(path, english_names, product_map):
            counts["changed"] += 1
        counts["files"] += 1
    return counts


def main() -> None:
    counts = deep_cleanup()
    print(f"Deep-cleaned {counts['files']} HTML files; changed {counts['changed']} files.")


if __name__ == "__main__":
    main()
