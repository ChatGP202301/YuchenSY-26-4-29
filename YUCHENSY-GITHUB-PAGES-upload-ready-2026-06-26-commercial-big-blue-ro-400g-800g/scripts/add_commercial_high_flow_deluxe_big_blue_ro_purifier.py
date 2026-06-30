#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add commercial high-flow deluxe Big Blue RO purifier across language pages."""

from __future__ import annotations

import html as html_lib
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BASE = runpy.run_path(str(ROOT / "scripts" / "add_horizontal_ro_equipment_250lph.py"))
DUAL_GLOBALS = BASE["DUAL_GLOBALS"]
BASE_COPY_FOR = BASE["copy_for"]
BASE_BUILD_MAIN = BASE["build_main"]
BASE_PRODUCT_GRAPH = BASE["product_graph"]
BASE_TREATMENT_VALUES = BASE["TREATMENT_VALUES"]
FEED_WATER_VALUES = BASE["FEED_WATER_VALUES"]
UPDATE_ITEM_LIST_JSON = DUAL_GLOBALS["update_item_list_json"]
PRODUCT_CARD = DUAL_GLOBALS["product_card"]

NEW_SLUG = "product-commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g.html"
PRODUCT_ID = "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g"
MAIN_IMAGE = "commercial-high-flow-deluxe-big-blue-ro-water-purifier-800g-1600g-oem.webp"
IMAGE_WIDTH = 1046
IMAGE_HEIGHT = 644
AFTER_SLUG = "product-horizontal-reverse-osmosis-water-purification-equipment-250lph.html"
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
    "af": "Kommersiële hoëvloei luukse grootdeursnee RO-water suiweringsmasjien",
    "ar": "جهاز RO تجاري فاخر عالي التدفق بقوارير كبيرة لتنقية المياه",
    "az": "Ticarət üçün yüksək axınlı lüks böyük gövdəli RO su təmizləyicisi",
    "bg": "Луксозен търговски RO водопречиствател с висок дебит и големи колби",
    "bn": "বাণিজ্যিক উচ্চ-প্রবাহ ডিলাক্স বড় হাউজিং RO পানি বিশুদ্ধকরণ মেশিন",
    "bs": "Komercijalni luksuzni RO prečistač vode velikog protoka s velikim kućištima",
    "cs": "Komerční luxusní RO čistička vody s vysokým průtokem a velkými pouzdry",
    "da": "Kommerciel luksus RO-vandrenser med høj kapacitet og store filterhuse",
    "de": "Gewerblicher Luxus-RO-Wasserreiniger mit hohem Durchfluss und Big-Blue-Gehäusen",
    "el": "Επαγγελματικός πολυτελής καθαριστής νερού RO υψηλής ροής με μεγάλα φίλτρα",
    "en": "Commercial High-Flow Deluxe Big Blue RO Water Purifier",
    "es": "Purificador RO comercial de alto caudal con carcasas grandes de lujo",
    "et": "Kaubanduslik suure vooluhulgaga luksuslik suurte korpustega RO veepuhasti",
    "fa": "دستگاه تصفیه آب RO تجاری لوکس با دبی بالا و هوزینگ‌های بزرگ",
    "fi": "Kaupallinen suurivirtauksinen deluxe RO-vedenpuhdistin suurilla suodatinkoteloilla",
    "fr": "Purificateur d’eau RO commercial haut débit avec grands boîtiers de luxe",
    "ha": "Na'urar tace ruwa ta RO ta kasuwanci mai babban kwarara da manyan gidajen tacewa",
    "he": "מטהר מים RO מסחרי יוקרתי בספיקה גבוהה עם בתי מסנן גדולים",
    "hi": "वाणिज्यिक हाई-फ्लो डिलक्स बड़े हाउसिंग वाला RO जल शोधक",
    "hr": "Komercijalni luksuzni RO pročišćivač vode visokog protoka s velikim kućištima",
    "hu": "Kereskedelmi nagy átfolyású deluxe RO víztisztító nagy szűrőházakkal",
    "hy": "Առևտրային բարձր հոսքի լյուքս RO ջրի մաքրիչ մեծ ֆիլտրային պատյաններով",
    "id": "Pemurni air RO komersial deluxe aliran tinggi dengan housing besar",
    "it": "Purificatore RO commerciale deluxe ad alta portata con grandi alloggiamenti",
    "ja": "商業用高流量デラックス大型ハウジングRO浄水機",
    "ka": "კომერციული მაღალი ნაკადის დელუქს RO წყლის გამწმენდი დიდი კორპუსებით",
    "kk": "Жоғары ағынды коммерциялық люкс үлкен корпусты RO су тазартқышы",
    "ko": "상업용 고유량 디럭스 대형 하우징 RO 정수기",
    "ku": "Paqijkera ava RO ya bazirganî ya luks bi herikîna bilind û malên mezin",
    "ky": "Жогорку агымдуу коммерциялык люкс чоң корпустуу RO суу тазалагыч",
    "lt": "Komercinis didelio srauto prabangus RO vandens valytuvas su dideliais korpusais",
    "lv": "Komerciāls augstas plūsmas luksusa RO ūdens attīrītājs ar lieliem korpusiem",
    "ms": "Penulen air RO komersial deluxe aliran tinggi dengan perumah besar",
    "nl": "Commerciële luxe RO-waterzuiveraar met hoge doorstroming en grote behuizingen",
    "no": "Kommersiell luksus RO-vannrenser med høy kapasitet og store filterhus",
    "pl": "Komercyjny luksusowy oczyszczacz wody RO o wysokim przepływie z dużymi obudowami",
    "pt": "Purificador RO comercial de alto fluxo com carcaças grandes de luxo",
    "ro": "Purificator RO comercial deluxe cu debit mare și carcase mari",
    "ru": "Коммерческий RO-очиститель воды высокого потока с большими колбами класса люкс",
    "sk": "Komerčný luxusný RO čistič vody s vysokým prietokom a veľkými puzdrami",
    "sl": "Komercialni luksuzni RO čistilnik vode z visokim pretokom in velikimi ohišji",
    "sq": "Pastrues RO komercial luksoz me prurje të lartë dhe strehime të mëdha",
    "sr": "Комерцијални луксузни RO пречистач воде великог протока са великим кућиштима",
    "sr-me": "Komercijalni luksuzni RO prečišćivač vode velikog protoka sa velikim kućištima",
    "sv": "Kommersiell lyxig RO-vattenrenare med högt flöde och stora filterhus",
    "sw": "Kisafishaji maji cha RO cha biashara cha mtiririko mkubwa chenye makasha makubwa",
    "ta": "வணிக உயர் ஓட்ட டீலக்ஸ் பெரிய ஹவுசிங் RO நீர் சுத்திகரிப்பு இயந்திரம்",
    "tg": "Дастгоҳи тиҷоратии RO барои тозакунии об бо ҷараёни баланд ва корпусҳои калон",
    "th": "เครื่องกรองน้ำ RO เชิงพาณิชย์แบบหรูอัตราการไหลสูงพร้อมกระบอกกรองใหญ่",
    "tk": "Ýokary akymly täjirçilik derejeli uly korpusly RO suw arassalaýjy",
    "tl": "Komersiyal na deluxe RO water purifier na mataas ang daloy at may malalaking housing",
    "tr": "Yüksek debili ticari lüks büyük gövdeli RO su arıtma cihazı",
    "uk": "Комерційний RO-очисник води високого потоку з великими колбами класу люкс",
    "ur": "تجارتی ہائی فلو ڈیلکس بڑے ہاؤسنگ والا RO واٹر پیوریفائر",
    "uz": "Yuqori oqimli tijorat deluxe katta korpusli RO suv tozalagichi",
    "vi": "Máy lọc nước RO thương mại cao cấp lưu lượng lớn với cốc lọc lớn",
    "zu": "Umshini wokuhlanza amanzi we-RO webhizinisi onokugeleza okuphezulu nezindlu ezinkulu",
}


OPERATION_VALUES = {
    "af": "Voloutomatiese intelligente werking met tekort-aan-water-beskerming, outomatiese stop wanneer vol, dubbele watergehaltevertoning, werksdrukvertoning, filtervervangingsherinnering en mikrorekenaarbeheer",
    "ar": "تشغيل ذكي أوتوماتيكي كامل مع حماية من نقص المياه، توقف تلقائي عند امتلاء الخزان، عرض مزدوج لجودة المياه، عرض ضغط التشغيل، تذكير بتغيير الفلتر وتحكم بالحاسوب الدقيق",
    "az": "Su çatışmazlığından qoruma, dolu olduqda avtomatik dayanma, ikiqat su keyfiyyəti göstəricisi, iş təzyiqi göstəricisi, filtr dəyişmə xatırlatması və mikrokompüter idarəsi ilə tam avtomatik ağıllı iş",
    "bg": "Напълно автоматична интелигентна работа със защита при липса на вода, автоматично спиране при пълен резервоар, двоен дисплей за качество на водата, показване на работно налягане, напомняне за смяна на филтрите и микрокомпютърно управление",
    "bn": "পানি স্বল্পতা সুরক্ষা, পূর্ণ হলে স্বয়ংক্রিয় বন্ধ, দ্বৈত পানির মান প্রদর্শন, চলমান চাপ প্রদর্শন, ফিল্টার পরিবর্তন স্মরণ এবং মাইক্রোকম্পিউটার নিয়ন্ত্রণসহ পূর্ণ স্বয়ংক্রিয় বুদ্ধিমান অপারেশন",
    "bs": "Potpuno automatski inteligentan rad sa zaštitom od nedostatka vode, automatskim zaustavljanjem kada je rezervoar pun, dvostrukim prikazom kvaliteta vode, prikazom radnog pritiska, podsjetnikom za zamjenu filtera i mikrokompjuterskim upravljanjem",
    "cs": "Plně automatický inteligentní provoz s ochranou proti nedostatku vody, automatickým zastavením při naplnění, dvojitým zobrazením kvality vody, zobrazením provozního tlaku, připomenutím výměny filtru a mikroprocesorovým řízením",
    "da": "Fuldautomatisk intelligent drift med tørløbsbeskyttelse, automatisk stop ved fuld tank, dobbelt visning af vandkvalitet, visning af driftstryk, påmindelse om filterskift og mikrocomputerstyring",
    "de": "Vollautomatischer intelligenter Betrieb mit Wassermangelschutz, automatischem Stopp bei vollem Tank, doppelter Wasserqualitätsanzeige, Betriebsdruckanzeige, Filterwechsel-Erinnerung und Mikrocomputersteuerung",
    "el": "Πλήρως αυτόματη έξυπνη λειτουργία με προστασία έλλειψης νερού, αυτόματη διακοπή όταν γεμίσει, διπλή ένδειξη ποιότητας νερού, ένδειξη πίεσης λειτουργίας, υπενθύμιση αλλαγής φίλτρου και μικροϋπολογιστικό έλεγχο",
    "en": "Full automatic intelligent operation with water-shortage protection, auto stop when full, dual water-quality display, operating pressure display, filter replacement reminder and microcomputer control",
    "es": "Operación inteligente totalmente automática con protección por falta de agua, parada automática al llenarse, doble visualización de calidad del agua, indicación de presión de trabajo, recordatorio de cambio de filtros y control por microcomputadora",
    "et": "Täisautomaatne intelligentne töö veepuuduse kaitse, täitumisel automaatse seiskamise, kahekordse veekvaliteedi kuva, töörõhu näidu, filtrivahetuse meeldetuletuse ja mikroarvuti juhtimisega",
    "fa": "کارکرد هوشمند تمام‌خودکار با حفاظت کمبود آب، توقف خودکار هنگام پر شدن، نمایش دوگانه کیفیت آب، نمایش فشار کاری، یادآوری تعویض فیلتر و کنترل میکروکامپیوتری",
    "fi": "Täysautomaattinen älykäs käyttö, jossa on vedenpuutteen suojaus, automaattinen pysäytys täyttyessä, kaksinkertainen vedenlaadun näyttö, käyttöpainenäyttö, suodattimen vaihtomuistutus ja mikrotietokoneohjaus",
    "fr": "Fonctionnement intelligent entièrement automatique avec protection manque d’eau, arrêt automatique réservoir plein, double affichage de la qualité d’eau, affichage de la pression de service, rappel de remplacement des filtres et commande par micro-ordinateur",
    "ha": "Aiki na atomatik mai hankali tare da kariya idan ruwa ya ƙare, tsayawa ta atomatik idan ya cika, nunin ingancin ruwa biyu, nunin matsin aiki, tunatarwar sauya tacewa da sarrafa microcomputer",
    "he": "פעולה חכמה אוטומטית מלאה עם הגנה מחוסר מים, עצירה אוטומטית במילוי מלא, תצוגת איכות מים כפולה, תצוגת לחץ עבודה, תזכורת להחלפת מסננים ובקרת מיקרו-מחשב",
    "hi": "पानी की कमी सुरक्षा, भर जाने पर स्वचालित बंद, दोहरी जल गुणवत्ता डिस्प्ले, कार्य दबाव डिस्प्ले, फिल्टर बदलने की याद दिलाने और माइक्रोकंप्यूटर नियंत्रण के साथ पूर्ण स्वचालित बुद्धिमान संचालन",
    "hr": "Potpuno automatski inteligentan rad sa zaštitom od nedostatka vode, automatskim zaustavljanjem pri punom spremniku, dvostrukim prikazom kvalitete vode, prikazom radnog tlaka, podsjetnikom za zamjenu filtra i mikroprocesorskim upravljanjem",
    "hu": "Teljesen automatikus intelligens működés vízhiány-védelemmel, telítettségnél automatikus leállással, kettős vízminőség-kijelzéssel, üzemi nyomás kijelzéssel, szűrőcsere-emlékeztetővel és mikroszámítógépes vezérléssel",
    "hy": "Լիովին ավտոմատ խելացի աշխատանք՝ ջրի պակասի պաշտպանությամբ, լցվելու դեպքում ավտոմատ կանգով, ջրի որակի կրկնակի ցուցադրմամբ, աշխատանքային ճնշման ցուցադրմամբ, ֆիլտրի փոխարինման հիշեցմամբ և միկրոհամակարգչային կառավարմամբ",
    "id": "Operasi cerdas otomatis penuh dengan perlindungan kekurangan air, berhenti otomatis saat penuh, tampilan kualitas air ganda, tampilan tekanan kerja, pengingat penggantian filter dan kontrol mikrokomputer",
    "it": "Funzionamento intelligente completamente automatico con protezione mancanza acqua, arresto automatico a serbatoio pieno, doppia visualizzazione della qualità dell’acqua, indicazione della pressione di esercizio, promemoria sostituzione filtri e controllo a microcomputer",
    "ja": "水切れ保護、満水自動停止、二重水質表示、運転圧力表示、フィルター交換リマインダー、マイコン制御を備えた全自動インテリジェント運転",
    "ka": "სრულად ავტომატური გონიერი მუშაობა წყლის ნაკლებობისგან დაცვით, შევსებისას ავტომატური გაჩერებით, წყლის ხარისხის ორმაგი ჩვენებით, სამუშაო წნევის ჩვენებით, ფილტრის შეცვლის შეხსენებით და მიკროკომპიუტერული მართვით",
    "kk": "Су жетіспеуінен қорғау, толғанда автоматты тоқтау, су сапасының қос дисплейі, жұмыс қысымын көрсету, сүзгіні ауыстыру ескерткіші және микрокомпьютерлік басқаруы бар толық автоматты интеллектуалды жұмыс",
    "ko": "물 부족 보호, 만수 자동 정지, 이중 수질 표시, 운전 압력 표시, 필터 교체 알림 및 마이크로컴퓨터 제어가 포함된 완전 자동 지능 운전",
    "ku": "Xebata aqilmend a tevahî otomatîk bi parastina kêmbûna avê, sekinandina otomatîk dema tijî bibe, nîşandana cot a kalîteya avê, nîşandana zexta xebatê, bîranîna guhertina parzûnê û kontrola mikrokomputerê",
    "ky": "Суу жетишсиздигинен коргоо, толгондо автоматтык токтоо, суунун сапатын кош көрсөтүү, иш басымын көрсөтүү, чыпканы алмаштыруу эскертүүсү жана микрокомпьютердик башкаруусу бар толук автоматтык акылдуу иштөө",
    "lt": "Visiškai automatinis išmanus veikimas su apsauga nuo vandens trūkumo, automatiniu sustabdymu užsipildžius, dvigubu vandens kokybės rodymu, darbinio slėgio rodymu, filtro keitimo priminimu ir mikrokompiuteriniu valdymu",
    "lv": "Pilnībā automātiska vieda darbība ar aizsardzību pret ūdens trūkumu, automātisku apstāšanos pie pilnas tvertnes, dubultu ūdens kvalitātes rādījumu, darba spiediena rādījumu, filtra maiņas atgādinājumu un mikrodatora vadību",
    "ms": "Operasi pintar automatik penuh dengan perlindungan kekurangan air, henti automatik apabila penuh, paparan kualiti air berganda, paparan tekanan operasi, peringatan penggantian penapis dan kawalan mikrokomputer",
    "nl": "Volautomatische intelligente werking met droogloopbeveiliging, automatische stop bij volle tank, dubbele waterkwaliteitsweergave, weergave van bedrijfsdruk, herinnering voor filtervervanging en microcomputerbesturing",
    "no": "Helautomatisk intelligent drift med beskyttelse mot vannmangel, automatisk stopp når full, dobbelt visning av vannkvalitet, visning av driftstrykk, påminnelse om filterbytte og mikrocomputerstyring",
    "pl": "W pełni automatyczna inteligentna praca z ochroną przed brakiem wody, automatycznym zatrzymaniem po napełnieniu, podwójnym wskazaniem jakości wody, wskazaniem ciśnienia roboczego, przypomnieniem o wymianie filtrów i sterowaniem mikrokomputerowym",
    "pt": "Operação inteligente totalmente automática com proteção contra falta de água, parada automática ao encher, dupla visualização da qualidade da água, indicação da pressão de operação, lembrete de troca de filtros e controle por microcomputador",
    "ro": "Funcționare inteligentă complet automată cu protecție la lipsa apei, oprire automată la umplere, afișaj dublu al calității apei, afișaj presiune de lucru, memento pentru schimbarea filtrelor și control cu microcomputer",
    "ru": "Полностью автоматическая интеллектуальная работа с защитой от отсутствия воды, автоостановкой при заполнении, двойной индикацией качества воды, отображением рабочего давления, напоминанием о замене фильтров и микрокомпьютерным управлением",
    "sk": "Plne automatická inteligentná prevádzka s ochranou proti nedostatku vody, automatickým zastavením pri naplnení, dvojitým zobrazením kvality vody, zobrazením pracovného tlaku, pripomenutím výmeny filtrov a mikroprocesorovým riadením",
    "sl": "Popolnoma samodejno pametno delovanje z zaščito pred pomanjkanjem vode, samodejno ustavitvijo ob polni posodi, dvojnim prikazom kakovosti vode, prikazom delovnega tlaka, opomnikom za menjavo filtrov in mikroprocesorskim upravljanjem",
    "sq": "Funksionim inteligjent plotësisht automatik me mbrojtje nga mungesa e ujit, ndalim automatik kur mbushet, shfaqje të dyfishtë të cilësisë së ujit, shfaqje të presionit të punës, kujtesë për ndërrimin e filtrave dhe kontroll me mikrokompjuter",
    "sr": "Потпуно аутоматски интелигентан рад са заштитом од недостатка воде, аутоматским заустављањем када је пуно, двоструким приказом квалитета воде, приказом радног притиска, подсетником за замену филтера и микрокомпјутерским управљањем",
    "sr-me": "Potpuno automatski inteligentan rad sa zaštitom od nedostatka vode, automatskim zaustavljanjem kada je puno, dvostrukim prikazom kvaliteta vode, prikazom radnog pritiska, podsjetnikom za zamjenu filtera i mikrokompjuterskim upravljanjem",
    "sv": "Helautomatisk intelligent drift med skydd mot vattenbrist, automatisk stopp vid full tank, dubbel visning av vattenkvalitet, visning av drifttryck, påminnelse om filterbyte och mikrodatorstyrning",
    "sw": "Uendeshaji mahiri wa kiotomatiki kabisa wenye ulinzi wa ukosefu wa maji, kusimama kiotomatiki ikijaa, onyesho mbili la ubora wa maji, onyesho la shinikizo la kazi, ukumbusho wa kubadilisha vichujio na udhibiti wa kompyuta ndogo",
    "ta": "நீர் குறைவு பாதுகாப்பு, நிரம்பியதும் தானியங்கி நிறுத்தம், இரட்டை நீர் தரக் காட்சி, செயல்பாட்டு அழுத்தக் காட்சி, வடிகட்டி மாற்ற நினைவூட்டல் மற்றும் மைக்ரோகணினி கட்டுப்பாட்டுடன் முழு தானியங்கி அறிவார்ந்த செயல்பாடு",
    "tg": "Кори пурра автоматии зеҳнӣ бо муҳофизат аз камобӣ, қатъи худкор ҳангоми пур шудан, намоиши дугонаи сифати об, намоиши фишори корӣ, ёдрасии иваз кардани филтр ва идоракунии микрокомпютерӣ",
    "th": "การทำงานอัจฉริยะอัตโนมัติเต็มรูปแบบพร้อมป้องกันน้ำขาด หยุดอัตโนมัติเมื่อน้ำเต็ม แสดงคุณภาพน้ำสองค่า แสดงแรงดันทำงาน แจ้งเตือนเปลี่ยนไส้กรอง และควบคุมด้วยไมโครคอมพิวเตอร์",
    "tk": "Suw ýetmezçiliginden gorag, dolanda awtomatik durmak, suw hiliniň iki görkezgiji, iş basyşynyň görkezgiji, süzgüç çalyşmak ýatlatmasy we mikrokompýuter dolandyryşy bilen doly awtomatik akylly iş",
    "tl": "Ganap na awtomatikong matalinong operasyon na may proteksiyon sa kakulangan ng tubig, awtomatikong hinto kapag puno, dobleng display ng kalidad ng tubig, display ng presyon sa operasyon, paalala sa pagpapalit ng filter at kontrol ng microcomputer",
    "tr": "Susuz kalma koruması, dolunca otomatik durma, çift su kalitesi göstergesi, çalışma basıncı göstergesi, filtre değişim hatırlatması ve mikro bilgisayar kontrolü ile tam otomatik akıllı çalışma",
    "uk": "Повністю автоматична інтелектуальна робота із захистом від нестачі води, автостопом при заповненні, подвійним відображенням якості води, індикацією робочого тиску, нагадуванням про заміну фільтрів і мікрокомп’ютерним керуванням",
    "ur": "پانی کی کمی سے تحفظ، بھرنے پر خودکار بندش، دوہرا پانی معیار ڈسپلے، آپریٹنگ پریشر ڈسپلے، فلٹر تبدیلی یاد دہانی اور مائیکرو کمپیوٹر کنٹرول کے ساتھ مکمل خودکار ذہین آپریشن",
    "uz": "Suv yetishmasligidan himoya, to‘lganda avtomatik to‘xtash, ikki tomonlama suv sifati ko‘rsatkichi, ish bosimi ko‘rsatkichi, filtr almashtirish eslatmasi va mikrokompyuter boshqaruvi bilan to‘liq avtomatik aqlli ishlash",
    "vi": "Vận hành thông minh hoàn toàn tự động với bảo vệ thiếu nước, tự dừng khi đầy, hiển thị kép chất lượng nước, hiển thị áp suất vận hành, nhắc thay lõi lọc và điều khiển vi máy tính",
    "zu": "Ukusebenza okuhlakaniphile okuzenzakalelayo ngokuphelele okunokuvikelwa kokushoda kwamanzi, ukumisa ngokuzenzakalela uma kugcwele, isibonisi esiphindwe kabili sekhwalithi yamanzi, isibonisi sengcindezi yokusebenza, isikhumbuzo sokushintsha isihlungi nokulawulwa kwekhompyutha encane",
}


def clean_meta(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 260:
        text = text[:257].rsplit(" ", 1)[0] + "..."
    return text


def treatment_value(lang: str) -> str:
    value = BASE_TREATMENT_VALUES[lang].replace("20", "10")
    return re.sub(r"\+\s*RO\s*$", "+ RO×2", value)


def copy_for(lang: str) -> dict:
    base = BASE_COPY_FOR(lang)
    if lang not in PRODUCT_NAMES or lang not in OPERATION_VALUES:
        raise KeyError(f"No product translation for {lang}")
    name = f"{PRODUCT_NAMES[lang]} 800G-1600G"
    labels = base["labels"][:]
    values = base["values"][:]
    values[0] = name
    values[1] = OPERATION_VALUES[lang]
    values[2] = treatment_value(lang)
    values[3] = "800G-1600G"
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
    return text.replace(
        "Horizontal%20Reverse%20Osmosis%20Water%20Purification%20Equipment%20250Lph",
        "Commercial%20High-Flow%20Deluxe%20Big%20Blue%20RO%20Water%20Purifier%20800G-1600G",
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
            "product-simple-type-reverse-osmosis-water-purification-equipment-250-1000lph.html",
            "product-precision-filter-ro-water-purification-equipment-250-1000lph.html",
            "product-20-inch-commercial-ro-water-purifier-800g-2000g.html",
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
        (i + 1 for i, item in enumerate(products) if item.get("id") == "horizontal-reverse-osmosis-water-purification-equipment-250lph"),
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
            "800G-1600G commercial RO purifier for municipal tap water",
            "10-inch Big Blue PP and cotton-carbon composite pretreatment",
            "Dual RO membrane configuration",
            "Water-shortage protection, full-water auto stop and filter replacement reminder",
            "White or black cabinet with OEM/ODM branding options",
        ],
        "applications": "Commercial direct drinking water for offices, restaurants, cafés, schools, shops, showrooms and distributors serving municipal tap-water projects.",
        "related": [
            "horizontal-reverse-osmosis-water-purification-equipment-250lph",
            "20-inch-commercial-ro-water-purifier-800g-2000g",
            "simple-type-reverse-osmosis-water-purification-equipment-250-1000lph",
            "precision-filter-ro-water-purification-equipment-250-1000lph",
        ],
    })
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_ai_files() -> None:
    line = f"- Commercial High-Flow Deluxe Big Blue RO Water Purifier 800G-1600G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
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
        or lang not in BASE_TREATMENT_VALUES
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
