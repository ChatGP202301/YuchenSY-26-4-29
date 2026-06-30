#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add desktop RO water machine with compressor cooling across all languages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_simple_type_ro_equipment_250_1000lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-desktop-ro-water-machine-compressor-cooling-100g.html"
PRODUCT_ID = "desktop-ro-water-machine-compressor-cooling-100g"
MAIN_IMAGE = "desktop-ro-water-machine-compressor-cooling-100g-black-front-oem.webp"
SECOND_IMAGE = "desktop-ro-water-machine-compressor-cooling-100g-filter-compartment-oem.webp"
IMAGE_WIDTH = 1086
IMAGE_HEIGHT = 1448
AFTER_SLUG = "product-built-in-pressure-tank-ro.html"
TODAY = "2026-06-22"
BRAND = "Yuchen Water"


NAME_PREFIXES = {
    "af": "Tafelblad RO-watermasjien met kompressorkoeling",
    "ar": "جهاز RO مكتبي للمياه مع تبريد بالضاغط",
    "az": "Kompressor soyutmalı masaüstü RO su aparatı",
    "bg": "Настолна RO машина за вода с компресорно охлаждане",
    "bn": "কম্প্রেসর কুলিংসহ ডেস্কটপ RO পানি মেশিন",
    "bs": "Stolna RO mašina za vodu s kompresorskim hlađenjem",
    "cs": "Stolní RO přístroj na vodu s kompresorovým chlazením",
    "da": "Bordmodel RO-vandmaskine med kompressorkøling",
    "de": "Tisch-RO-Wassermaschine mit Kompressorkühlung",
    "el": "Επιτραπέζια μηχανή νερού RO με ψύξη συμπιεστή",
    "en": "Desktop RO Water Machine with Compressor Cooling",
    "es": "Máquina de agua RO de sobremesa con enfriamiento por compresor",
    "et": "Kompressorjahutusega lauapealne RO veemasin",
    "fa": "دستگاه آب RO رومیزی با خنک‌سازی کمپرسوری",
    "fi": "Pöytämallinen RO-vesikone kompressorijäähdytyksellä",
    "fr": "Machine à eau RO de comptoir avec refroidissement par compresseur",
    "ha": "Na'urar ruwan RO ta kan tebur mai sanyaya komfreso",
    "he": "מכונת מים RO שולחנית עם קירור מדחס",
    "hi": "कंप्रेसर कूलिंग वाली डेस्कटॉप RO वाटर मशीन",
    "hr": "Stolni RO aparat za vodu s kompresorskim hlađenjem",
    "hu": "Asztali RO vízgép kompresszoros hűtéssel",
    "hy": "Սեղանի RO ջրի սարք կոմպրեսորային սառեցմամբ",
    "id": "Mesin air RO meja dengan pendingin kompresor",
    "it": "Macchina acqua RO da banco con raffreddamento a compressore",
    "ja": "コンプレッサー冷却付き卓上ROウォーターマシン",
    "ka": "სამაგიდო RO წყლის აპარატი კომპრესორული გაგრილებით",
    "kk": "Компрессорлық салқындатуы бар үстел үсті RO су аппараты",
    "ko": "컴프레서 냉각 방식 탁상형 RO 정수기",
    "ku": "Makîneya ava RO ya ser maseyê bi sarbûna kompresorê",
    "ky": "Компрессордук муздатуусу бар үстөл үстү RO суу аппараты",
    "lt": "Stalinis RO vandens aparatas su kompresoriniu aušinimu",
    "lv": "Galda RO ūdens aparāts ar kompresora dzesēšanu",
    "ms": "Mesin air RO atas meja dengan penyejukan pemampat",
    "nl": "RO-watermachine voor op het werkblad met compressorkoeling",
    "no": "Bordmodell RO-vannmaskin med kompressorkjøling",
    "pl": "Nablatowa maszyna RO do wody z chłodzeniem kompresorowym",
    "pt": "Máquina de água RO de bancada com refrigeração por compressor",
    "ro": "Aparat de apă RO de masă cu răcire prin compresor",
    "ru": "Настольный RO-аппарат для воды с компрессорным охлаждением",
    "sk": "Stolový RO prístroj na vodu s kompresorovým chladením",
    "sl": "Namizni RO aparat za vodo s kompresorskim hlajenjem",
    "sq": "Pajisje uji RO për tavolinë me ftohje me kompresor",
    "sr": "Стони RO апарат за воду са компресорским хлађењем",
    "sr-me": "Stoni RO aparat za vodu sa kompresorskim hlađenjem",
    "sv": "Bordsmodell RO-vattenmaskin med kompressorkylning",
    "sw": "Mashine ya maji ya RO ya mezani yenye upoozaji wa kompresor",
    "ta": "கம்பிரசர் குளிரூட்டலுடன் மேசை RO நீர் இயந்திரம்",
    "tg": "Дастгоҳи мизии оби RO бо хунуккунии компрессорӣ",
    "th": "เครื่องทำน้ำ RO ตั้งโต๊ะพร้อมระบบทำความเย็นแบบคอมเพรสเซอร์",
    "tk": "Kompressor sowadyjyly stol üstü RO suw enjamy",
    "tl": "Pangpatong na makinang RO para sa tubig na may paglamig ng kompresor",
    "tr": "Kompresör soğutmalı masaüstü RO su makinesi",
    "uk": "Настільний RO апарат для води з компресорним охолодженням",
    "ur": "کمپریسر کولنگ والی ڈیسک ٹاپ RO واٹر مشین",
    "uz": "Kompressorli sovitishga ega stol usti RO suv apparati",
    "vi": "Máy nước RO để bàn có làm lạnh bằng máy nén",
    "zu": "Umshini wamanzi we-RO wedeski onokupholisa nge-compressor",
}


COOLING_VALUES = {
    "af": "Kompressorkoeling vir verkoelde drinkwater en stabiele tafeldiens",
    "ar": "تبريد بالضاغط لتوفير مياه شرب مبردة وخدمة مكتبية مستقرة",
    "az": "Soyudulmuş içməli su və sabit masaüstü istifadə üçün kompressor soyutması",
    "bg": "Компресорно охлаждане за охладена питейна вода и стабилна настолна работа",
    "bn": "ঠান্ডা পানীয় জল ও স্থিতিশীল ডেস্কটপ ব্যবহারের জন্য কম্প্রেসর কুলিং",
    "bs": "Kompresorsko hlađenje za rashlađenu pitku vodu i stabilan rad na stolu",
    "cs": "Kompresorové chlazení pro chlazenou pitnou vodu a stabilní stolní provoz",
    "da": "Kompressorkøling til kølet drikkevand og stabil borddrift",
    "de": "Kompressorkühlung für gekühltes Trinkwasser und stabilen Tischbetrieb",
    "el": "Ψύξη συμπιεστή για δροσερό πόσιμο νερό και σταθερή επιτραπέζια χρήση",
    "en": "Compressor cooling for chilled drinking water and stable countertop service",
    "es": "Enfriamiento por compresor para agua potable fría y uso estable de sobremesa",
    "et": "Kompressorjahutus jahutatud joogivee ja stabiilse lauakasutuse jaoks",
    "fa": "خنک‌سازی کمپرسوری برای آب آشامیدنی سرد و کارکرد پایدار رومیزی",
    "fi": "Kompressorijäähdytys viileälle juomavedelle ja vakaaseen pöytäkäyttöön",
    "fr": "Refroidissement par compresseur pour eau potable fraîche et service stable sur comptoir",
    "ha": "Sanyaya komfreso don ruwan sha mai sanyi da aiki mai karko a kan tebur",
    "he": "קירור מדחס למי שתייה קרים ולפעולה יציבה על משטח עבודה",
    "hi": "ठंडे पेयजल और स्थिर काउंटरटॉप उपयोग के लिए कंप्रेसर कूलिंग",
    "hr": "Kompresorsko hlađenje za rashlađenu pitku vodu i stabilan rad na pultu",
    "hu": "Kompresszoros hűtés hűtött ivóvízhez és stabil asztali használathoz",
    "hy": "Կոմպրեսորային սառեցում սառը խմելու ջրի և կայուն սեղանի աշխատանքի համար",
    "id": "Pendingin kompresor untuk air minum dingin dan penggunaan meja yang stabil",
    "it": "Raffreddamento a compressore per acqua potabile fresca e servizio stabile da banco",
    "ja": "冷水飲用と安定した卓上使用に対応するコンプレッサー冷却",
    "ka": "კომპრესორული გაგრილება ცივი სასმელი წყლისა და სტაბილური სამაგიდო მუშაობისთვის",
    "kk": "Салқын ауыз су және тұрақты үстел үсті жұмыс үшін компрессорлық салқындату",
    "ko": "냉수 음용과 안정적인 탁상 사용을 위한 컴프레서 냉각",
    "ku": "Sarbûna kompresorê ji bo ava vexwarinê ya sar û karûbarê sekinî yê ser maseyê",
    "ky": "Муздак ичүүчү суу жана туруктуу үстөл үстү колдонуу үчүн компрессордук муздатуу",
    "lt": "Kompresorinis aušinimas vėsiam geriamajam vandeniui ir stabiliam staliniam darbui",
    "lv": "Kompresora dzesēšana atdzesētam dzeramajam ūdenim un stabilai galda lietošanai",
    "ms": "Penyejukan pemampat untuk air minuman sejuk dan penggunaan atas meja yang stabil",
    "nl": "Compressorkoeling voor gekoeld drinkwater en stabiel gebruik op het werkblad",
    "no": "Kompressorkjøling for kaldt drikkevann og stabil bruk på benk",
    "pl": "Chłodzenie kompresorowe dla schłodzonej wody pitnej i stabilnej pracy nablatowej",
    "pt": "Refrigeração por compressor para água potável fria e uso estável em bancada",
    "ro": "Răcire prin compresor pentru apă potabilă rece și funcționare stabilă pe blat",
    "ru": "Компрессорное охлаждение для холодной питьевой воды и стабильной настольной работы",
    "sk": "Kompresorové chladenie pre chladenú pitnú vodu a stabilnú stolovú prevádzku",
    "sl": "Kompresorsko hlajenje za ohlajeno pitno vodo in stabilno namizno delovanje",
    "sq": "Ftohje me kompresor për ujë të pijshëm të ftohtë dhe përdorim të qëndrueshëm në tavolinë",
    "sr": "Компресорско хлађење за расхлађену питку воду и стабилан рад на пулту",
    "sr-me": "Kompresorsko hlađenje za rashlađenu pitku vodu i stabilan rad na pultu",
    "sv": "Kompressorkylning för kylt dricksvatten och stabil bordsdrift",
    "sw": "Upoozaji wa kompresor kwa maji ya kunywa yaliyopozwa na matumizi thabiti mezani",
    "ta": "குளிர்ந்த குடிநீர் மற்றும் நிலையான மேசை பயன்பாட்டிற்கான கம்பிரசர் குளிரூட்டல்",
    "tg": "Хунуккунии компрессорӣ барои оби нӯшокии хунук ва кори устувори рӯимизӣ",
    "th": "ระบบทำความเย็นแบบคอมเพรสเซอร์สำหรับน้ำดื่มเย็นและการใช้งานตั้งโต๊ะที่เสถียร",
    "tk": "Sowadylan agyz suwy we durnukly stol üstü iş üçin kompressor sowadyşy",
    "tl": "Paglamig ng kompresor para sa malamig na inuming tubig at matatag na paggamit sa patungan",
    "tr": "Soğuk içme suyu ve dengeli tezgah üstü kullanım için kompresör soğutma",
    "uk": "Компресорне охолодження для холодної питної води та стабільної настільної роботи",
    "ur": "ٹھنڈے پینے کے پانی اور مستحکم کاؤنٹر ٹاپ استعمال کے لیے کمپریسر کولنگ",
    "uz": "Sovutilgan ichimlik suvi va barqaror stol usti ishlashi uchun kompressorli sovitish",
    "vi": "Làm lạnh bằng máy nén cho nước uống lạnh và vận hành ổn định trên bàn",
    "zu": "Ukupholisa nge-compressor kwamanzi okuphuza abandayo nokusebenza okuzinzile etafuleni",
}


TREATMENT_VALUES = {
    "af": "Vierstadiumfiltrasie: PP + CTO + T33 + RO, met 100G RO-kapasiteit",
    "ar": "ترشيح من أربع مراحل: PP + CTO + T33 + RO، مع قدرة RO مقدارها 100G",
    "az": "Dörd mərhələli filtrasiya: PP + CTO + T33 + RO, 100G RO tutumu ilə",
    "bg": "Четиристепенна филтрация: PP + CTO + T33 + RO, с RO капацитет 100G",
    "bn": "চার ধাপের ফিল্টারেশন: PP + CTO + T33 + RO, 100G RO ক্ষমতা সহ",
    "bs": "Četverostepena filtracija: PP + CTO + T33 + RO, s RO kapacitetom 100G",
    "cs": "Čtyřstupňová filtrace: PP + CTO + T33 + RO, s kapacitou RO 100G",
    "da": "Firetrinsfiltrering: PP + CTO + T33 + RO, med 100G RO-kapacitet",
    "de": "Vierstufige Filtration: PP + CTO + T33 + RO, mit 100G RO-Leistung",
    "el": "Φιλτράρισμα τεσσάρων σταδίων: PP + CTO + T33 + RO, με ικανότητα RO 100G",
    "en": "Four-stage filtration: PP + CTO + T33 + RO, with 100G RO capacity",
    "es": "Filtración de cuatro etapas: PP + CTO + T33 + RO, con capacidad RO 100G",
    "et": "Neljaastmeline filtreerimine: PP + CTO + T33 + RO, 100G RO võimsusega",
    "fa": "فیلتراسیون چهارمرحله‌ای: PP + CTO + T33 + RO، با ظرفیت RO 100G",
    "fi": "Nelivaiheinen suodatus: PP + CTO + T33 + RO, 100G RO-kapasiteetilla",
    "fr": "Filtration en quatre étapes : PP + CTO + T33 + RO, avec capacité RO 100G",
    "ha": "Tacewa matakai huɗu: PP + CTO + T33 + RO, tare da ƙarfin RO 100G",
    "he": "סינון בארבעה שלבים: PP + CTO + T33 + RO, עם קיבולת RO של 100G",
    "hi": "चार-चरण निस्पंदन: PP + CTO + T33 + RO, 100G RO क्षमता के साथ",
    "hr": "Četverostupanjska filtracija: PP + CTO + T33 + RO, s RO kapacitetom 100G",
    "hu": "Négyfokozatú szűrés: PP + CTO + T33 + RO, 100G RO kapacitással",
    "hy": "Չորս աստիճանի ֆիլտրում՝ PP + CTO + T33 + RO, 100G RO հզորությամբ",
    "id": "Filtrasi empat tahap: PP + CTO + T33 + RO, dengan kapasitas RO 100G",
    "it": "Filtrazione a quattro stadi: PP + CTO + T33 + RO, con capacità RO 100G",
    "ja": "4段階ろ過：PP + CTO + T33 + RO、100G RO能力",
    "ka": "ოთხსაფეხურიანი ფილტრაცია: PP + CTO + T33 + RO, 100G RO წარმადობით",
    "kk": "Төрт сатылы сүзу: PP + CTO + T33 + RO, 100G RO өнімділігімен",
    "ko": "4단계 여과: PP + CTO + T33 + RO, 100G RO 용량",
    "ku": "Parzûnkirina çar qonaxî: PP + CTO + T33 + RO, bi kapasîteya RO 100G",
    "ky": "Төрт баскычтуу чыпкалоо: PP + CTO + T33 + RO, 100G RO кубаттуулугу менен",
    "lt": "Keturių pakopų filtravimas: PP + CTO + T33 + RO, su 100G RO našumu",
    "lv": "Četru pakāpju filtrācija: PP + CTO + T33 + RO, ar 100G RO jaudu",
    "ms": "Penapisan empat peringkat: PP + CTO + T33 + RO, dengan kapasiti RO 100G",
    "nl": "Viertraps filtratie: PP + CTO + T33 + RO, met 100G RO-capaciteit",
    "no": "Firetrinns filtrering: PP + CTO + T33 + RO, med 100G RO-kapasitet",
    "pl": "Czterostopniowa filtracja: PP + CTO + T33 + RO, z wydajnością RO 100G",
    "pt": "Filtração em quatro estágios: PP + CTO + T33 + RO, com capacidade RO 100G",
    "ro": "Filtrare în patru trepte: PP + CTO + T33 + RO, cu capacitate RO 100G",
    "ru": "Четырехступенчатая фильтрация: PP + CTO + T33 + RO, производительность RO 100G",
    "sk": "Štvorstupňová filtrácia: PP + CTO + T33 + RO, s kapacitou RO 100G",
    "sl": "Štiristopenjska filtracija: PP + CTO + T33 + RO, z zmogljivostjo RO 100G",
    "sq": "Filtrim me katër faza: PP + CTO + T33 + RO, me kapacitet RO 100G",
    "sr": "Четворостепена филтрација: PP + CTO + T33 + RO, са RO капацитетом 100G",
    "sr-me": "Četvorostepena filtracija: PP + CTO + T33 + RO, sa RO kapacitetom 100G",
    "sv": "Fyrstegsfiltrering: PP + CTO + T33 + RO, med 100G RO-kapacitet",
    "sw": "Uchujaji wa hatua nne: PP + CTO + T33 + RO, wenye uwezo wa RO 100G",
    "ta": "நான்கு நிலை வடிகட்டல்: PP + CTO + T33 + RO, 100G RO திறனுடன்",
    "tg": "Филтратсияи чорзинагӣ: PP + CTO + T33 + RO, бо иқтидори RO 100G",
    "th": "การกรองสี่ขั้นตอน: PP + CTO + T33 + RO พร้อมกำลัง RO 100G",
    "tk": "Dört basgançakly süzgüç: PP + CTO + T33 + RO, 100G RO kuwwaty bilen",
    "tl": "Apat na yugto ng pagsasala: PP + CTO + T33 + RO, na may kapasidad na RO 100G",
    "tr": "Dört aşamalı filtrasyon: PP + CTO + T33 + RO, 100G RO kapasitesiyle",
    "uk": "Чотириступенева фільтрація: PP + CTO + T33 + RO, продуктивність RO 100G",
    "ur": "چار مرحلوں کی فلٹریشن: PP + CTO + T33 + RO، 100G RO صلاحیت کے ساتھ",
    "uz": "To‘rt bosqichli filtrlash: PP + CTO + T33 + RO, 100G RO quvvati bilan",
    "vi": "Lọc bốn cấp: PP + CTO + T33 + RO, công suất RO 100G",
    "zu": "Ukuhlunga kwezigaba ezine: PP + CTO + T33 + RO, ngomthamo we-RO 100G",
}


CUSTOMIZATION_VALUES = {
    "af": "Swart behuising standaard; ander kleure, logo, paneeltaal en verpakking kan vir OEM/ODM aangepas word; kinderslot beskikbaar",
    "ar": "هيكل أسود قياسي؛ يمكن تخصيص الألوان الأخرى والشعار ولغة اللوحة والتغليف لخدمات OEM/ODM؛ يتوفر قفل للأطفال",
    "az": "Standart qara korpus; digər rənglər, loqo, panel dili və qablaşdırma OEM/ODM üçün fərdiləşdirilə bilər; uşaq kilidi mövcuddur",
    "bg": "Стандартен черен корпус; други цветове, лого, език на панела и опаковка могат да се персонализират за OEM/ODM; налична е детска защита",
    "bn": "স্ট্যান্ডার্ড কালো হাউজিং; OEM/ODM এর জন্য অন্যান্য রং, লোগো, প্যানেল ভাষা ও প্যাকেজিং কাস্টমাইজ করা যায়; চাইল্ড লক উপলভ্য",
    "bs": "Standardno crno kućište; druge boje, logo, jezik panela i pakovanje mogu se prilagoditi za OEM/ODM; dostupna dječja brava",
    "cs": "Standardní černé provedení; jiné barvy, logo, jazyk panelu a balení lze upravit pro OEM/ODM; dětský zámek je k dispozici",
    "da": "Sort kabinet som standard; andre farver, logo, panelsprog og emballage kan tilpasses til OEM/ODM; børnesikring er tilgængelig",
    "de": "Schwarzes Gehäuse als Standard; weitere Farben, Logo, Panelsprache und Verpackung sind für OEM/ODM anpassbar; Kindersicherung verfügbar",
    "el": "Μαύρο περίβλημα ως στάνταρ· άλλα χρώματα, λογότυπο, γλώσσα πάνελ και συσκευασία προσαρμόζονται για OEM/ODM· διαθέτει κλείδωμα παιδιών",
    "en": "Black housing standard; other colors, logo, panel language and packaging can be customized for OEM/ODM; child lock available",
    "es": "Carcasa negra estándar; otros colores, logotipo, idioma del panel y embalaje personalizables para OEM/ODM; bloqueo infantil disponible",
    "et": "Standardne must korpus; muud värvid, logo, paneeli keel ja pakend on OEM/ODM jaoks kohandatavad; lapselukk olemas",
    "fa": "بدنه مشکی استاندارد؛ رنگ‌های دیگر، لوگو، زبان پنل و بسته‌بندی برای OEM/ODM قابل سفارشی‌سازی است؛ قفل کودک موجود است",
    "fi": "Musta runko vakiona; muut värit, logo, paneelin kieli ja pakkaus voidaan mukauttaa OEM/ODM-toimituksiin; lapsilukko saatavilla",
    "fr": "Boîtier noir standard ; autres couleurs, logo, langue du panneau et emballage personnalisables pour OEM/ODM ; verrouillage enfant disponible",
    "ha": "Jiki baƙi na asali; ana iya keɓance wasu launuka, tambari, harshen panel da marufi don OEM/ODM; akwai makullin yara",
    "he": "גוף שחור כסטנדרט; צבעים אחרים, לוגו, שפת לוח ואריזה ניתנים להתאמה עבור OEM/ODM; נעילת ילדים זמינה",
    "hi": "मानक काला हाउसिंग; OEM/ODM के लिए अन्य रंग, लोगो, पैनल भाषा और पैकेजिंग अनुकूलित की जा सकती है; चाइल्ड लॉक उपलब्ध",
    "hr": "Standardno crno kućište; druge boje, logotip, jezik panela i pakiranje mogu se prilagoditi za OEM/ODM; dostupna dječja zaštita",
    "hu": "Alapértelmezett fekete ház; más színek, logó, panelnyelv és csomagolás OEM/ODM szerint testreszabható; gyermekzár elérhető",
    "hy": "Ստանդարտ սև կորպուս․ այլ գույներ, լոգո, վահանակի լեզու և փաթեթավորում կարող են հարմարեցվել OEM/ODM-ի համար․ առկա է մանկական կողպում",
    "id": "Bodi hitam standar; warna lain, logo, bahasa panel, dan kemasan dapat disesuaikan untuk OEM/ODM; tersedia kunci anak",
    "it": "Corpo nero standard; altri colori, logo, lingua del pannello e imballo personalizzabili per OEM/ODM; blocco bambini disponibile",
    "ja": "標準は黒色ボディ。OEM/ODM向けに他色、ロゴ、パネル言語、梱包をカスタム可能。チャイルドロック対応",
    "ka": "სტანდარტული შავი კორპუსი; სხვა ფერები, ლოგო, პანელის ენა და შეფუთვა OEM/ODM-ისთვის მორგებადია; ხელმისაწვდომია ბავშვებისგან დაცვა",
    "kk": "Стандартты қара корпус; OEM/ODM үшін басқа түстер, логотип, панель тілі және қаптама бапталады; балалардан қорғау құлпы бар",
    "ko": "기본 검정 본체; OEM/ODM용 다른 색상, 로고, 패널 언어와 포장 맞춤 가능; 어린이 잠금 기능 제공",
    "ku": "Qalikê reş wek standard; rengên din, logo, zimanê panelê û pakêt ji bo OEM/ODM dikarin bên xwestin; qefila zarokan heye",
    "ky": "Стандарттуу кара корпус; OEM/ODM үчүн башка түстөр, логотип, панелдин тили жана таңгак ыңгайлаштырылат; балдар кулпусу бар",
    "lt": "Standartinis juodas korpusas; kitos spalvos, logotipas, skydelio kalba ir pakuotė pritaikomi OEM/ODM; yra vaikų užraktas",
    "lv": "Standarta melns korpuss; citas krāsas, logotipu, paneļa valodu un iepakojumu var pielāgot OEM/ODM; pieejama bērnu drošības bloķēšana",
    "ms": "Perumah hitam standard; warna lain, logo, bahasa panel dan pembungkusan boleh disesuaikan untuk OEM/ODM; kunci kanak-kanak tersedia",
    "nl": "Zwarte behuizing standaard; andere kleuren, logo, paneeltaal en verpakking aanpasbaar voor OEM/ODM; kinderslot beschikbaar",
    "no": "Svart kabinett som standard; andre farger, logo, panelspråk og emballasje kan tilpasses for OEM/ODM; barnesikring tilgjengelig",
    "pl": "Standardowa czarna obudowa; inne kolory, logo, język panelu i opakowanie można dostosować dla OEM/ODM; dostępna blokada dziecięca",
    "pt": "Gabinete preto padrão; outras cores, logotipo, idioma do painel e embalagem podem ser personalizados para OEM/ODM; trava infantil disponível",
    "ro": "Carcasă neagră standard; alte culori, logo, limba panoului și ambalajul pot fi personalizate pentru OEM/ODM; blocare pentru copii disponibilă",
    "ru": "Стандартный черный корпус; другие цвета, логотип, язык панели и упаковка настраиваются для OEM/ODM; доступна защита от детей",
    "sk": "Štandardné čierne telo; iné farby, logo, jazyk panelu a balenie možno prispôsobiť pre OEM/ODM; detská poistka k dispozícii",
    "sl": "Standardno črno ohišje; druge barve, logotip, jezik plošče in embalaža so prilagodljivi za OEM/ODM; na voljo je otroška ključavnica",
    "sq": "Trup i zi standard; ngjyra të tjera, logoja, gjuha e panelit dhe paketimi mund të përshtaten për OEM/ODM; ka bllokim për fëmijë",
    "sr": "Стандардно црно кућиште; друге боје, лого, језик панела и паковање могу се прилагодити за OEM/ODM; доступна је дечја брава",
    "sr-me": "Standardno crno kućište; druge boje, logo, jezik panela i pakovanje mogu se prilagoditi za OEM/ODM; dostupna je dječja brava",
    "sv": "Svart hölje som standard; andra färger, logotyp, panelspråk och förpackning kan anpassas för OEM/ODM; barnlås finns",
    "sw": "Mwili mweusi wa kawaida; rangi nyingine, nembo, lugha ya paneli na kifungashio vinaweza kubadilishwa kwa OEM/ODM; kufuli ya watoto ipo",
    "ta": "நிலையான கருப்பு உடல்; OEM/ODM க்காக பிற நிறங்கள், லோகோ, பலகை மொழி மற்றும் பேக்கேஜிங் தனிப்பயனாக்கலாம்; குழந்தை பூட்டு உள்ளது",
    "tg": "Корпуси сиёҳи стандартӣ; рангҳои дигар, логотип, забони панел ва бастабандӣ барои OEM/ODM танзимшавандаанд; қулфи кӯдакон мавҷуд аст",
    "th": "ตัวเครื่องสีดำเป็นมาตรฐาน สามารถปรับสีอื่น โลโก้ ภาษาหน้าจอ และบรรจุภัณฑ์สำหรับ OEM/ODM ได้ มีระบบล็อกป้องกันเด็ก",
    "tk": "Standart gara korpus; beýleki reňkler, logo, panel dili we gaplama OEM/ODM üçin sazlanýar; çaga gulpy bar",
    "tl": "Karaniwang itim ang kaha; maaaring iangkop ang ibang kulay, logo, wika ng panel at pakete para sa OEM/ODM; may kandado para sa bata",
    "tr": "Standart siyah gövde; diğer renkler, logo, panel dili ve ambalaj OEM/ODM için özelleştirilebilir; çocuk kilidi mevcuttur",
    "uk": "Стандартний чорний корпус; інші кольори, логотип, мова панелі та пакування налаштовуються для OEM/ODM; доступний дитячий замок",
    "ur": "معیاری سیاہ باڈی؛ OEM/ODM کے لیے دیگر رنگ، لوگو، پینل زبان اور پیکنگ حسب ضرورت بن سکتی ہے؛ چائلڈ لاک دستیاب ہے",
    "uz": "Standart qora korpus; OEM/ODM uchun boshqa ranglar, logo, panel tili va qadoqlash moslashtiriladi; bolalar qulfi mavjud",
    "vi": "Thân máy màu đen tiêu chuẩn; có thể tùy chỉnh màu khác, logo, ngôn ngữ bảng điều khiển và bao bì cho OEM/ODM; có khóa trẻ em",
    "zu": "Umzimba omnyama ojwayelekile; eminye imibala, ilogo, ulimi lwephaneli nokupakisha kungenziwa ngokwezifiso ze-OEM/ODM; ikhiyi yezingane ikhona",
}


APPLICATION_VALUES = {
    "af": "Kantore, vertoonlokale, woonstelle, klein kombuise, spense en handelsmerk-tafeltoestelprogramme",
    "ar": "المكاتب وصالات العرض والشقق والمطابخ الصغيرة وغرف الخدمة وبرامج الأجهزة المكتبية ذات العلامة الخاصة",
    "az": "Ofislər, sərgi salonları, mənzillər, kiçik mətbəxlər, çay otaqları və marka masaüstü cihaz proqramları",
    "bg": "Офиси, шоуруми, апартаменти, малки кухни, сервизни зони и програми за брандирани настолни уреди",
    "bn": "অফিস, শোরুম, অ্যাপার্টমেন্ট, ছোট রান্নাঘর, প্যান্ট্রি এবং ব্র্যান্ডেড ডেস্কটপ যন্ত্র প্রকল্প",
    "bs": "Uredi, izložbeni prostori, stanovi, male kuhinje, čajne kuhinje i programi stolnih uređaja pod brendom",
    "cs": "Kanceláře, showroomy, byty, malé kuchyně, kuchyňky a programy značkových stolních spotřebičů",
    "da": "Kontorer, showrooms, lejligheder, små køkkener, tekøkkener og programmer for brandede bordapparater",
    "de": "Büros, Ausstellungsräume, Wohnungen, kleine Küchen, Teeküchen und Programme für Marken-Tischgeräte",
    "el": "Γραφεία, εκθεσιακοί χώροι, διαμερίσματα, μικρές κουζίνες, χώροι ροφημάτων και προγράμματα επώνυμων επιτραπέζιων συσκευών",
    "en": "Offices, showrooms, apartments, small kitchens, pantries and branded countertop appliance programs",
    "es": "Oficinas, salas de exposición, apartamentos, cocinas pequeñas, áreas de servicio y programas de equipos de sobremesa de marca",
    "et": "Kontorid, näidistesaalid, korterid, väikesed köögid, puhkenurgad ja kaubamärgiga lauaseadmete programmid",
    "fa": "دفترها، نمایشگاه‌ها، آپارتمان‌ها، آشپزخانه‌های کوچک، آبدارخانه‌ها و برنامه‌های دستگاه رومیزی با برند اختصاصی",
    "fi": "Toimistot, näyttelytilat, asunnot, pienet keittiöt, taukotilat ja brändättyjen pöytälaitteiden ohjelmat",
    "fr": "Bureaux, showrooms, appartements, petites cuisines, espaces de pause et programmes d’appareils de comptoir de marque",
    "ha": "Ofisoshi, wuraren nuni, gidaje, ƙananan girki, ɗakunan shayi da shirye-shiryen na'urar tebur mai tambari",
    "he": "משרדים, אולמות תצוגה, דירות, מטבחים קטנים, מטבחונים ותוכניות למכשירי שולחן ממותגים",
    "hi": "कार्यालय, शोरूम, अपार्टमेंट, छोटे किचन, पैंट्री और ब्रांडेड काउंटरटॉप उपकरण कार्यक्रम",
    "hr": "Uredi, izložbeni prostori, apartmani, male kuhinje, čajne kuhinje i programi brendiranih pultnih uređaja",
    "hu": "Irodák, bemutatótermek, lakások, kis konyhák, teakonyhák és márkázott asztali készülékprogramok",
    "hy": "Գրասենյակներ, ցուցասրահներ, բնակարաններ, փոքր խոհանոցներ, սպասարկման սենյակներ և բրենդավորված սեղանի սարքերի ծրագրեր",
    "id": "Kantor, ruang pamer, apartemen, dapur kecil, pantry, dan program perangkat meja bermerek",
    "it": "Uffici, showroom, appartamenti, piccole cucine, aree break e programmi di apparecchi da banco con marchio",
    "ja": "オフィス、ショールーム、集合住宅、小型キッチン、給湯室、ブランド卓上機器プログラム",
    "ka": "ოფისები, შოურუმები, ბინები, მცირე სამზარეულოები, ჩაის კუთხეები და ბრენდირებული სამაგიდო აპარატების პროგრამები",
    "kk": "Кеңселер, шоурумдар, пәтерлер, шағын асүйлер, қызмет бөлмелері және брендтік үстел үсті құрылғы бағдарламалары",
    "ko": "사무실, 전시장, 아파트, 소형 주방, 탕비실 및 브랜드 탁상형 기기 프로그램",
    "ku": "Ofîs, salona pêşandanê, apartman, metbexên biçûk, odeyên xizmetê û bernameyên amûrên ser maseyê yên bi marke",
    "ky": "Кеңселер, көргөзмө залдары, батирлер, чакан ашканалар, чай бөлмөлөрү жана бренддик үстөл үстү жабдык программалары",
    "lt": "Biurai, ekspozicijų salės, butai, mažos virtuvės, poilsio zonos ir firminių stalinių prietaisų programos",
    "lv": "Biroji, izstāžu zāles, dzīvokļi, nelielas virtuves, atpūtas zonas un zīmola galda ierīču programmas",
    "ms": "Pejabat, bilik pameran, apartmen, dapur kecil, pantri dan program peralatan atas meja berjenama",
    "nl": "Kantoren, showrooms, appartementen, kleine keukens, pantry’s en programma’s voor merkgebonden werkbladapparaten",
    "no": "Kontorer, utstillingsrom, leiligheter, små kjøkken, tekjøkken og programmer for merkevarebaserte benkapparater",
    "pl": "Biura, salony ekspozycyjne, mieszkania, małe kuchnie, aneksy socjalne i programy markowych urządzeń nablatowych",
    "pt": "Escritórios, showrooms, apartamentos, cozinhas pequenas, copas e programas de aparelhos de bancada de marca",
    "ro": "Birouri, showroomuri, apartamente, bucătării mici, oficii și programe de aparate de masă cu marcă proprie",
    "ru": "Офисы, шоурумы, квартиры, небольшие кухни, сервисные зоны и программы настольной техники под брендом клиента",
    "sk": "Kancelárie, showroomy, byty, malé kuchyne, kuchynky a programy značkových stolových spotrebičov",
    "sl": "Pisarne, razstavni prostori, stanovanja, majhne kuhinje, čajne kuhinje in programi namiznih naprav z blagovno znamko",
    "sq": "Zyra, sallone ekspozimi, apartamente, kuzhina të vogla, kënde shërbimi dhe programe pajisjesh tavoline me markë",
    "sr": "Канцеларије, изложбени простори, станови, мале кухиње, чајне кухиње и програми брендираних стоних уређаја",
    "sr-me": "Kancelarije, izložbeni prostori, stanovi, male kuhinje, čajne kuhinje i programi brendiranih stonih uređaja",
    "sv": "Kontor, utställningsrum, lägenheter, små kök, pentryn och program för varumärkesanpassade bordsapparater",
    "sw": "Ofisi, vyumba vya maonyesho, apartimenti, jikoni ndogo, maeneo ya huduma na programu za vifaa vya mezani vyenye chapa",
    "ta": "அலுவலகங்கள், காட்சியறைகள், குடியிருப்புகள், சிறிய சமையலறைகள், பாண்ட்ரிகள் மற்றும் பிராண்டு மேசை சாதன திட்டங்கள்",
    "tg": "Дафтарҳо, толорҳои намоишӣ, хонаҳо, ошхонаҳои хурд, утоқҳои хизматӣ ва барномаҳои дастгоҳҳои рӯимизии брендӣ",
    "th": "สำนักงาน โชว์รูม อพาร์ตเมนต์ ครัวขนาดเล็ก มุมเตรียมเครื่องดื่ม และโครงการเครื่องใช้ตั้งโต๊ะแบรนด์ลูกค้า",
    "tk": "Ofisler, görkezme zallary, öýler, kiçi aşhanalar, hyzmat burçlary we brendli stol üstü enjam maksatnamalary",
    "tl": "Mga opisina, showroom, apartment, maliliit na kusina, pantry at mga programang pang-aparatong may sariling tatak",
    "tr": "Ofisler, showroomlar, daireler, küçük mutfaklar, servis alanları ve markalı tezgah üstü cihaz programları",
    "uk": "Офіси, шоуруми, квартири, невеликі кухні, сервісні зони та програми настільної техніки під брендом клієнта",
    "ur": "دفاتر، شو رومز، اپارٹمنٹس، چھوٹے کچن، پینٹریاں اور برانڈڈ کاؤنٹر ٹاپ آلات کے پروگرام",
    "uz": "Ofislar, ko‘rgazma zallari, xonadonlar, kichik oshxonalar, xizmat burchaklari va mijoz brendidagi stol usti apparat dasturlari",
    "vi": "Văn phòng, phòng trưng bày, căn hộ, bếp nhỏ, khu pantry và chương trình thiết bị để bàn theo thương hiệu",
    "zu": "Amahhovisi, amagumbi okubukisa, amafulethi, amakhishi amancane, amapentri nezinhlelo zemishini yedeski enophawu",
}


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    required = [NAME_PREFIXES, COOLING_VALUES, TREATMENT_VALUES, CUSTOMIZATION_VALUES, APPLICATION_VALUES, FEED_WATER_VALUES]
    if any(lang not in mapping for mapping in required):
        raise KeyError(f"No product translation for {lang}")
    name = f"{NAME_PREFIXES[lang]} 100G"
    labels = base["labels"][:]
    if lang == "fr":
        labels[7] = "Utilisation"
    values = base["values"][:]
    values[0] = name
    values[1] = COOLING_VALUES[lang]
    values[2] = TREATMENT_VALUES[lang]
    values[3] = "100G"
    values[4] = FEED_WATER_VALUES[lang]
    values[6] = CUSTOMIZATION_VALUES[lang]
    values[7] = APPLICATION_VALUES[lang]
    values[8] = CUSTOMIZATION_VALUES[lang]
    intro = (
        f"{name}. {labels[1]}: {values[1]}. "
        f"{labels[2]}: {values[2]}. {labels[3]}: {values[3]}. "
        f"{labels[4]}: {values[4]}. {labels[6]}: {values[6]}. "
        f"{labels[7]}: {values[7]}."
    )
    card = f"{NAME_PREFIXES[lang]}: {values[2]}; {values[1]}; {values[6]}."
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
        (f"{labels[1]}?", values[1]),
        (f"{labels[2]}?", values[2]),
        (f"{labels[3]}?", values[3]),
        (f"{labels[6]}?", values[6]),
        (f"{labels[7]}?", values[7]),
    ]
    return copy


def gallery_html(copy: dict) -> str:
    name = html_lib.escape(copy["name"], quote=True)
    return f'''
      <div class="product-gallery">
        <a href="../assets/products/{MAIN_IMAGE}"><img src="../assets/products/{MAIN_IMAGE}" alt="{name}" loading="lazy" decoding="async" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}"></a>
        <a href="../assets/products/{SECOND_IMAGE}"><img src="../assets/products/{SECOND_IMAGE}" alt="{name}" loading="lazy" decoding="async" width="{IMAGE_WIDTH}" height="{IMAGE_HEIGHT}"></a>
      </div>'''


def build_main(lang: str, copy: dict) -> str:
    text = BASE_BUILD_MAIN(lang, copy)
    text = text.replace(
        "Simple%20Type%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250-1000Lph",
        "Desktop%20RO%20Water%20Machine%20Compressor%20Cooling%20100G",
    )
    text = text.replace(
        "Inquiry%20about%20Desktop%20RO%20Water%20Machine%20Compressor%20Cooling%20100G",
        quote(f"{copy['request']}: {copy['name']}", safe=""),
    )
    if "product-gallery" not in text:
        text = re.sub(
            r'(<img src="../assets/products/' + re.escape(MAIN_IMAGE) + r'"[^>]*class="product-main-image" />)',
            r"\1" + gallery_html(copy),
            text,
            count=1,
        )
    return text


def product_graph(lang: str, copy: dict) -> str:
    graph = json.loads(BASE_PRODUCT_GRAPH(lang, copy))
    for node in graph.get("@graph", []):
        if isinstance(node, dict) and node.get("@type") == "Product":
            node["image"] = [
                f"https://www.yuchensy.com/assets/products/{MAIN_IMAGE}",
                f"https://www.yuchensy.com/assets/products/{SECOND_IMAGE}",
            ]
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
            "product-custom-5-6-7-stage-ro-water-purifier.html",
            "product-commercial-ro-water-purifier-800g-2000g.html",
            "product-simple-type-reverse-osmosis-water-purification-equipment-250-1000lph.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "built-in-pressure-tank-ro"),
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
            "Desktop RO water machine with compressor cooling",
            "Four-stage PP + CTO + T33 + RO filtration",
            "100G RO capacity",
            "Black cabinet with custom color options",
            "Child lock and custom logo options",
        ],
        "applications": "Desktop RO drinking water machine for offices, showrooms, apartments, small kitchens, pantries and OEM appliance programs.",
        "related": [
            "built-in-pressure-tank-ro",
            "custom-5-6-7-stage-ro-water-purifier",
            "commercial-ro-water-purifier-800g-2000g",
            "ro-water-purifier",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Desktop RO Water Machine with Compressor Cooling 100G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        if lang not in NAME_PREFIXES
        or lang not in COOLING_VALUES
        or lang not in TREATMENT_VALUES
        or lang not in CUSTOMIZATION_VALUES
        or lang not in APPLICATION_VALUES
        or lang not in FEED_WATER_VALUES
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
