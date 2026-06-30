#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add the 20-inch commercial RO water purifier product across language pages."""

from __future__ import annotations

import html
import json
import re
import runpy
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OLD_SLUG = "product-ro-seawater-desalination-machine.html"
NEW_SLUG = "product-20-inch-commercial-ro-water-purifier-800g-2000g.html"
PRODUCT_ID = "20-inch-commercial-ro-water-purifier-800g-2000g"
TODAY = "2026-06-14"

MAIN_IMAGE = "20-inch-commercial-ro-water-purifier-800g-2000g-front-full-frame-oem.webp"
IMAGES = [
    (MAIN_IMAGE, 1024, 1024, "front full frame"),
    ("20-inch-commercial-ro-water-purifier-800g-2000g-side-angle-oem.webp", 1024, 1024, "side angle"),
    ("20-inch-commercial-ro-water-purifier-800g-2000g-rear-plumbing-oem.webp", 1728, 2304, "rear plumbing"),
    ("20-inch-commercial-ro-water-purifier-800g-2000g-front-20-inch-blue-housings-oem.webp", 1728, 2304, "20-inch blue housings"),
    ("20-inch-commercial-ro-water-purifier-800g-2000g-front-angle-oem.webp", 1024, 1024, "front angle"),
    ("20-inch-commercial-ro-water-purifier-800g-2000g-front-close-up-oem.webp", 1728, 2304, "front close-up"),
]

RTL_LANGS = {"ar", "fa", "he", "ur"}

PRIORITY_COPY = runpy.run_path(str(ROOT / "scripts" / "fix_priority_language_mixed_english.py"))["COPY"]
THIRD_COPY = runpy.run_path(str(ROOT / "scripts" / "fix_third_language_ui_residuals.py"))["T"]

LANG_NAMES = {
    "af": "20-duim kommersiële RO-waterreiniger 800G/1200G/1600G/2000G",
    "ar": "جهاز تنقية مياه RO تجاري 20 بوصة 800G/1200G/1600G/2000G",
    "az": "20 düymlük kommersiya RO su təmizləyicisi 800G/1200G/1600G/2000G",
    "bg": "20-инчова търговска RO машина за пречистена питейна вода 800G/1200G/1600G/2000G",
    "bn": "20 ইঞ্চি বাণিজ্যিক RO বিশুদ্ধ পানির মেশিন 800G/1200G/1600G/2000G",
    "bs": "20-inčni komercijalni RO prečistač vode 800G/1200G/1600G/2000G",
    "cs": "20palcový komerční RO čistič vody 800G/1200G/1600G/2000G",
    "da": "20-tommer kommerciel RO-vandrenser 800G/1200G/1600G/2000G",
    "de": "20-Zoll kommerzielle RO-Trinkwasseranlage 800G/1200G/1600G/2000G",
    "el": "Επαγγελματική μηχανή καθαρού νερού RO 20 ιντσών 800G/1200G/1600G/2000G",
    "en": "20-inch Commercial RO Water Purifier 800G/1200G/1600G/2000G",
    "es": "Purificador comercial de agua RO de 20 pulgadas 800G/1200G/1600G/2000G",
    "et": "20-tolline kaubanduslik RO veepuhasti 800G/1200G/1600G/2000G",
    "fa": "دستگاه تصفیه آب RO تجاری 20 اینچ 800G/1200G/1600G/2000G",
    "fi": "20 tuuman kaupallinen RO-vedenpuhdistin 800G/1200G/1600G/2000G",
    "fr": "Purificateur d'eau RO commercial 20 pouces 800G/1200G/1600G/2000G",
    "ha": "Na'urar tace ruwan RO ta kasuwanci inci 20 800G/1200G/1600G/2000G",
    "he": "מטהר מים RO מסחרי 20 אינץ' 800G/1200G/1600G/2000G",
    "hi": "20 इंच वाणिज्यिक RO शुद्ध पेयजल मशीन 800G/1200G/1600G/2000G",
    "hr": "20-inčni komercijalni RO pročišćivač vode 800G/1200G/1600G/2000G",
    "hu": "20 hüvelykes kereskedelmi RO víztisztító 800G/1200G/1600G/2000G",
    "hy": "20 դյույմանոց առևտրային RO ջրի մաքրիչ 800G/1200G/1600G/2000G",
    "id": "Pemurni air RO komersial 20 inci 800G/1200G/1600G/2000G",
    "it": "Depuratore d'acqua RO commerciale da 20 pollici 800G/1200G/1600G/2000G",
    "ja": "20インチ業務用RO純水直飲浄水機 800G/1200G/1600G/2000G",
    "ka": "20 დიუმიანი კომერციული RO წყლის გამწმენდი 800G/1200G/1600G/2000G",
    "kk": "20 дюймдік коммерциялық RO таза ауыз су жүйесі 800G/1200G/1600G/2000G",
    "ko": "20인치 상업용 RO 정수 직수형 정수기 800G/1200G/1600G/2000G",
    "ku": "Paqijkera ava RO ya bazirganî 20 înç 800G/1200G/1600G/2000G",
    "ky": "20 дюймдук коммерциялык RO таза ичүүчү суу аппараты 800G/1200G/1600G/2000G",
    "lt": "20 colių komercinis RO vandens valytuvas 800G/1200G/1600G/2000G",
    "lv": "20 collu komerciāls RO ūdens attīrītājs 800G/1200G/1600G/2000G",
    "ms": "Penapis air RO komersial 20 inci 800G/1200G/1600G/2000G",
    "nl": "20-inch commerciële RO-waterzuiveraar 800G/1200G/1600G/2000G",
    "no": "20-tommers kommersiell RO-vannrenser 800G/1200G/1600G/2000G",
    "pl": "20-calowy komercyjny oczyszczacz wody RO 800G/1200G/1600G/2000G",
    "pt": "Purificador comercial de água RO de 20 polegadas 800G/1200G/1600G/2000G",
    "ro": "Purificator comercial de apă RO de 20 inch 800G/1200G/1600G/2000G",
    "ru": "20-дюймовая коммерческая RO-система питьевой воды 800G/1200G/1600G/2000G",
    "sk": "20-palcový komerčný RO čistič vody 800G/1200G/1600G/2000G",
    "sl": "20-palčni komercialni RO čistilnik vode 800G/1200G/1600G/2000G",
    "sq": "Pastrues komercial uji RO 20 inç 800G/1200G/1600G/2000G",
    "sr": "20-инчни комерцијални RO пречишћивач воде 800G/1200G/1600G/2000G",
    "sr-me": "20-inčni komercijalni RO prečišćivač vode 800G/1200G/1600G/2000G",
    "sv": "20-tums kommersiell RO-vattenrenare 800G/1200G/1600G/2000G",
    "sw": "Kisafishaji maji cha RO cha biashara inchi 20 800G/1200G/1600G/2000G",
    "ta": "20 அங்குல வர்த்தக RO தூய குடிநீர் இயந்திரம் 800G/1200G/1600G/2000G",
    "tg": "Дастгоҳи тиҷоратии RO барои оби нӯшокӣ 20 дюйм 800G/1200G/1600G/2000G",
    "th": "เครื่องกรองน้ำ RO เชิงพาณิชย์ 20 นิ้ว 800G/1200G/1600G/2000G",
    "tk": "20 dýuým täjirçilik RO suw arassalaýjy 800G/1200G/1600G/2000G",
    "tl": "20-pulgadang commercial RO water purifier 800G/1200G/1600G/2000G",
    "tr": "20 inç ticari RO saf içme suyu makinesi 800G/1200G/1600G/2000G",
    "uk": "20-дюймова комерційна RO система питної води 800G/1200G/1600G/2000G",
    "ur": "20 انچ کمرشل RO واٹر پیوریفائر 800G/1200G/1600G/2000G",
    "uz": "20 dyuymli tijorat RO toza ichimlik suvi mashinasi 800G/1200G/1600G/2000G",
    "vi": "Máy lọc nước tinh khiết RO thương mại 20 inch 800G/1200G/1600G/2000G",
    "zu": "Isihlanzi samanzi se-RO sokuhweba esingu-20 intshi 800G/1200G/1600G/2000G",
}

UI = {
    "en": {
        "home": "Home", "products": "Products", "category": "Commercial RO Water Purifier",
        "specs": "Technical Specifications", "spec_h": "Commercial RO purifier specification guide",
        "options": "Configuration Options", "options_h": "Tankless or pressure-tank commercial RO supply",
        "faq": "FAQ", "faq_h": "Commercial RO water purifier FAQ",
        "related": "Related Products", "quote": "Request a quote for the 20-inch commercial RO purifier",
        "quote_desc": "Send capacity, tank option, quantity, logo needs and destination port. A Yuchen Water engineer will confirm the OEM/ODM configuration.",
        "request": "Request OEM Quote", "whatsapp": "WhatsApp Sales", "send": "Send Inquiry",
        "item": "Item", "spec": "Specification",
        "labels": ["Product Type", "Capacity", "Filtration Stages", "Pressure Tank", "Rated Power", "Product Weight", "Dimensions", "Installation", "Application", "OEM/ODM", "MOQ"],
    },
    "ru": {"home": "Главная", "products": "Продукция", "category": "Коммерческая RO-система", "specs": "Технические характеристики", "spec_h": "Спецификация коммерческой RO-системы", "options": "Варианты конфигурации", "options_h": "Поставка без бака или с напорным баком", "faq": "FAQ", "faq_h": "Вопросы по коммерческой RO-системе", "related": "Похожие продукты", "quote": "Запросить цену на 20-дюймовую коммерческую RO-систему", "quote_desc": "Отправьте требуемую производительность, вариант бака, количество, требования к логотипу и порт назначения. Инженер Yuchen Water подтвердит OEM/ODM конфигурацию.", "request": "Запросить OEM-предложение", "whatsapp": "Продажи WhatsApp", "send": "Отправить запрос", "item": "Параметр", "spec": "Спецификация", "labels": ["Тип продукта", "Производительность", "Ступени фильтрации", "Напорный бак", "Номинальная мощность", "Вес продукта", "Размеры", "Установка", "Применение", "OEM/ODM", "MOQ"]},
    "es": {"home": "Inicio", "products": "Productos", "category": "Purificador RO comercial", "specs": "Especificaciones técnicas", "spec_h": "Guía de especificación del purificador RO comercial", "options": "Opciones de configuración", "options_h": "Suministro comercial RO sin tanque o con tanque de presión", "faq": "FAQ", "faq_h": "Preguntas sobre el purificador comercial RO", "related": "Productos relacionados", "quote": "Solicitar cotización del purificador RO comercial de 20 pulgadas", "quote_desc": "Envíe capacidad, opción de tanque, cantidad, requisitos de logo y puerto de destino. Un ingeniero de Yuchen Water confirmará la configuración OEM/ODM.", "request": "Solicitar cotización OEM", "whatsapp": "Ventas por WhatsApp", "send": "Enviar consulta", "item": "Ítem", "spec": "Especificación", "labels": ["Tipo de producto", "Capacidad", "Etapas de filtración", "Tanque de presión", "Potencia nominal", "Peso del producto", "Dimensiones", "Instalación", "Aplicación", "OEM/ODM", "MOQ"]},
    "de": {"home": "Startseite", "products": "Produkte", "category": "Kommerzielle RO-Anlage", "specs": "Technische Daten", "spec_h": "Spezifikation der kommerziellen RO-Anlage", "options": "Konfigurationsoptionen", "options_h": "Tanklose Ausführung oder mit Drucktank", "faq": "FAQ", "faq_h": "Fragen zur kommerziellen RO-Anlage", "related": "Ähnliche Produkte", "quote": "Angebot für die 20-Zoll kommerzielle RO-Anlage anfordern", "quote_desc": "Senden Sie Leistung, Tankoption, Menge, Logoanforderungen und Zielhafen. Ein Yuchen Water Ingenieur bestätigt die OEM/ODM-Konfiguration.", "request": "OEM-Angebot anfordern", "whatsapp": "WhatsApp-Vertrieb", "send": "Anfrage senden", "item": "Punkt", "spec": "Spezifikation", "labels": ["Produkttyp", "Leistung", "Filterstufen", "Drucktank", "Nennleistung", "Produktgewicht", "Abmessungen", "Installation", "Anwendung", "OEM/ODM", "MOQ"]},
    "fr": {"home": "Accueil", "products": "Produits", "category": "Purificateur RO commercial", "specs": "Spécifications techniques", "spec_h": "Guide de spécification du purificateur RO commercial", "options": "Options de configuration", "options_h": "Fourniture RO commerciale sans réservoir ou avec réservoir sous pression", "faq": "FAQ", "faq_h": "Questions sur le purificateur RO commercial", "related": "Produits associés", "quote": "Demander un devis pour le purificateur RO commercial 20 pouces", "quote_desc": "Envoyez la capacité, l'option de réservoir, la quantité, les besoins de logo et le port de destination. Un ingénieur Yuchen Water confirmera la configuration OEM/ODM.", "request": "Demander un devis OEM", "whatsapp": "Ventes WhatsApp", "send": "Envoyer une demande", "item": "Élément", "spec": "Spécification", "labels": ["Type de produit", "Capacité", "Étapes de filtration", "Réservoir sous pression", "Puissance nominale", "Poids du produit", "Dimensions", "Installation", "Application", "OEM/ODM", "MOQ"]},
    "vi": {"home": "Trang chủ", "products": "Sản phẩm", "category": "Máy RO thương mại", "specs": "Thông số kỹ thuật", "spec_h": "Hướng dẫn thông số máy RO thương mại", "options": "Tùy chọn cấu hình", "options_h": "Cung cấp máy RO không bình áp hoặc có bình áp", "faq": "FAQ", "faq_h": "Câu hỏi về máy lọc nước RO thương mại", "related": "Sản phẩm liên quan", "quote": "Yêu cầu báo giá máy RO thương mại 20 inch", "quote_desc": "Gửi công suất, lựa chọn bình áp, số lượng, yêu cầu logo và cảng đến. Kỹ sư Yuchen Water sẽ xác nhận cấu hình OEM/ODM.", "request": "Yêu cầu báo giá OEM", "whatsapp": "Bán hàng WhatsApp", "send": "Gửi yêu cầu", "item": "Hạng mục", "spec": "Thông số", "labels": ["Loại sản phẩm", "Công suất", "Cấp lọc", "Bình áp", "Công suất điện định mức", "Trọng lượng sản phẩm", "Kích thước", "Lắp đặt", "Ứng dụng", "OEM/ODM", "MOQ"]},
    "ja": {"home": "ホーム", "products": "製品", "category": "業務用RO浄水機", "specs": "技術仕様", "spec_h": "業務用RO浄水機の仕様ガイド", "options": "構成オプション", "options_h": "タンクレスまたは圧力タンク付きで供給可能", "faq": "FAQ", "faq_h": "業務用RO浄水機FAQ", "related": "関連製品", "quote": "20インチ業務用RO浄水機の見積依頼", "quote_desc": "能力、タンク有無、数量、ロゴ要件、仕向港をお送りください。Yuchen Water の技術担当が OEM/ODM 仕様を確認します。", "request": "OEM見積を依頼", "whatsapp": "WhatsApp営業", "send": "問い合わせを送信", "item": "項目", "spec": "仕様", "labels": ["製品タイプ", "処理能力", "ろ過段数", "圧力タンク", "定格電力", "製品重量", "外形寸法", "設置方式", "用途", "OEM/ODM", "MOQ"]},
    "uz": {"home": "Bosh sahifa", "products": "Mahsulotlar", "category": "Tijorat RO suv tozalagichi", "specs": "Texnik xususiyatlar", "spec_h": "Tijorat RO qurilmasi uchun spetsifikatsiya", "options": "Konfiguratsiya variantlari", "options_h": "Baksiz yoki bosim baki bilan RO ta'minoti", "faq": "FAQ", "faq_h": "Tijorat RO suv tozalagichi bo‘yicha savollar", "related": "Tegishli mahsulotlar", "quote": "20 dyuymli tijorat RO qurilmasi uchun narx so‘rash", "quote_desc": "Quvvat, bak varianti, miqdor, logo talabi va yetkazib berish portini yuboring. Yuchen Water muhandisi OEM/ODM konfiguratsiyasini tasdiqlaydi.", "request": "OEM narx so‘rash", "whatsapp": "WhatsApp savdo", "send": "So‘rov yuborish", "item": "Band", "spec": "Spetsifikatsiya", "labels": ["Mahsulot turi", "Quvvat", "Filtrlash bosqichlari", "Bosim baki", "Nominal quvvat", "Mahsulot vazni", "O‘lchamlar", "O‘rnatish", "Qo‘llanish", "OEM/ODM", "MOQ"]},
    "kk": {"home": "Басты бет", "products": "Өнімдер", "category": "Коммерциялық RO су тазартқыш", "specs": "Техникалық сипаттамалар", "spec_h": "Коммерциялық RO жүйесінің сипаттамасы", "options": "Конфигурация нұсқалары", "options_h": "Баксыз немесе қысым багымен жеткізу", "faq": "FAQ", "faq_h": "Коммерциялық RO жүйесі бойынша сұрақтар", "related": "Ұқсас өнімдер", "quote": "20 дюймдік коммерциялық RO жүйесіне баға сұрау", "quote_desc": "Қажетті өнімділік, бак нұсқасы, саны, логотип талабы және жеткізу портын жіберіңіз. Yuchen Water инженері OEM/ODM конфигурациясын растайды.", "request": "OEM ұсынысын сұрау", "whatsapp": "WhatsApp сату", "send": "Сұрау жіберу", "item": "Параметр", "spec": "Сипаттама", "labels": ["Өнім түрі", "Өнімділік", "Сүзу сатылары", "Қысым багы", "Номиналды қуат", "Өнім салмағы", "Өлшемдер", "Орнату", "Қолданылуы", "OEM/ODM", "MOQ"]},
    "ky": {"home": "Башкы бет", "products": "Өнүмдөр", "category": "Коммерциялык RO суу тазалагыч", "specs": "Техникалык мүнөздөмөлөр", "spec_h": "Коммерциялык RO системасынын спецификациясы", "options": "Конфигурация варианттары", "options_h": "Баксыз же басым багы менен жеткирүү", "faq": "FAQ", "faq_h": "Коммерциялык RO системасы боюнча суроолор", "related": "Окшош өнүмдөр", "quote": "20 дюймдук коммерциялык RO системасына баа суроо", "quote_desc": "Кубаттуулук, бак варианты, көлөм, логотип талабы жана жеткирүү портун жөнөтүңүз. Yuchen Water инженери OEM/ODM конфигурациясын тактайт.", "request": "OEM баасын суроо", "whatsapp": "WhatsApp сатуу", "send": "Суроо жөнөтүү", "item": "Параметр", "spec": "Спецификация", "labels": ["Өнүм түрү", "Кубаттуулук", "Чыпкалоо баскычтары", "Басым багы", "Номиналдык кубат", "Өнүм салмагы", "Өлчөмдөр", "Орнотуу", "Колдонуу", "OEM/ODM", "MOQ"]},
}

QUALITY_LABELS = {
    "en": "Quality documents", "ru": "Документы качества", "es": "Documentos de calidad",
    "de": "Qualitätsunterlagen", "fr": "Documents qualité", "vi": "Tài liệu chất lượng",
    "ja": "品質書類", "uz": "Sifat hujjatlari", "kk": "Сапа құжаттары",
    "ky": "Сапат документтери",
}

LOCAL_TERMS = {
    "af": {"home": "Tuis", "products": "Produkte", "specs": "Tegniese spesifikasies", "options": "Konfigurasie-opsies", "related": "Verwante produkte", "request": "Vra OEM-kwotasie", "send": "Stuur navraag", "item": "Item", "spec": "Spesifikasie", "quality": "Kwaliteitsdokumente", "labels": ["Produksoort", "Kapasiteit", "Filtrasiestappe", "Druktenk", "Aangeslane krag", "Produkgewig", "Afmetings", "Installasie", "Toepassing", "OEM/ODM", "MOQ"], "stage": "Vyf-stap RO-filtrasie met PP sediment, vooraf-koolstof, RO-membraan en na-koolstof volgens bestelling", "tank": "Standaard sonder tenk; druktenk kan volgens klantvereiste bygevoeg word", "frame": "Houtraam 47 x 33 x 90 cm", "install": "Vloerstaande kommersiële installasie vir direkte drinkwater", "app": "Kantore, restaurante, skole, kafees, klein fabrieke en verspreiderprojekte", "oem": "Logo, paneel, etiket, filtervolgorde, tenkopsie, verpakking en handleiding", "moq": "Bevestig volgens spesifikasie en handelsmerkvlak", "body": "Vir B2B-verspreiders en handelsmerke, met 800G, 1200G, 1600G en 2000G kapasiteite, vyf-stap RO-filtrasie, 160W krag, 28 kg gewig en keuse van druktenk of tenklose toevoer.", "card": "Kommersiële direkte-drinkwater RO-masjien met 800G-2000G opsies, vyf-stap filtrasie en OEM/ODM-handelsmerkondersteuning."},
    "ar": {"home": "الرئيسية", "products": "المنتجات", "specs": "المواصفات الفنية", "options": "خيارات التكوين", "related": "منتجات ذات صلة", "request": "طلب عرض OEM", "send": "إرسال استفسار", "item": "البند", "spec": "المواصفة", "quality": "وثائق الجودة", "labels": ["نوع المنتج", "السعة", "مراحل الترشيح", "خزان الضغط", "القدرة الاسمية", "وزن المنتج", "الأبعاد", "التركيب", "الاستخدام", "OEM/ODM", "MOQ"], "stage": "ترشيح RO من خمس مراحل مع فلتر رواسب PP وكربون أولي وغشاء RO وكربون نهائي حسب الطلب", "tank": "التكوين القياسي بدون خزان، ويمكن إضافة خزان ضغط حسب طلب العميل", "frame": "إطار خشبي 47 x 33 x 90 cm", "install": "تركيب تجاري قائم على الأرض لمياه الشرب المباشرة", "app": "المكاتب والمطاعم والمدارس والمقاهي والمصانع الصغيرة ومشاريع الموزعين", "oem": "الشعار واللوحة والملصق وتسلسل الفلاتر وخيار الخزان والتغليف والدليل", "moq": "يتم التأكيد حسب المواصفات ومستوى العلامة", "body": "مناسب للموزعين والعلامات التجارية في B2B، ويدعم سعات 800G و1200G و1600G و2000G مع ترشيح RO من خمس مراحل، قدرة 160W، وزن 28 kg، وخيار بدون خزان أو مع خزان ضغط.", "card": "جهاز RO تجاري لمياه الشرب المباشرة بسعات 800G-2000G وترشيح من خمس مراحل ودعم OEM/ODM."},
    "az": {"home": "Ana səhifə", "products": "Məhsullar", "specs": "Texniki xüsusiyyətlər", "options": "Konfiqurasiya seçimləri", "related": "Əlaqəli məhsullar", "request": "OEM qiymət sorğusu", "send": "Sorğu göndər", "item": "Bənd", "spec": "Spesifikasiya", "quality": "Keyfiyyət sənədləri", "labels": ["Məhsul növü", "Tutum", "Filtrasiya mərhələləri", "Təzyiq çəni", "Nominal güc", "Məhsul çəkisi", "Ölçülər", "Quraşdırma", "Tətbiq", "OEM/ODM", "MOQ"], "stage": "PP çöküntü filtri, ilkin karbon, RO membran və sifarişə uyğun son karbon ilə beş mərhələli RO filtrasiya", "tank": "Standart çənsizdir; müştəri tələbinə görə təzyiq çəni əlavə edilə bilər", "frame": "Taxta çərçivə 47 x 33 x 90 cm", "install": "Birbaşa içməli su üçün döşəmə tipli kommersiya quraşdırması", "app": "Ofislər, restoranlar, məktəblər, kafelər, kiçik müəssisələr və distribyutor layihələri", "oem": "Loqo, panel, etiket, filtr ardıcıllığı, çən seçimi, qablaşdırma və təlimat", "moq": "Spesifikasiya və brendləşmə səviyyəsinə görə təsdiqlənir", "body": "B2B distribyutorları və markaları üçün hazırlanmışdır; 800G, 1200G, 1600G və 2000G tutumları, beş mərhələli RO filtrasiya, 160W güc, 28 kg çəki və çənsiz və ya təzyiq çənli seçimləri dəstəkləyir.", "card": "800G-2000G kommersiya RO içməli su qurğusu, beş mərhələli filtrasiya və OEM/ODM brendləşmə dəstəyi."},
    "bg": {"home": "Начало", "products": "Продукти", "specs": "Технически характеристики", "options": "Опции за конфигурация", "related": "Свързани продукти", "request": "Заявка за OEM оферта", "send": "Изпрати запитване", "item": "Параметър", "spec": "Спецификация", "quality": "Документи за качество", "labels": ["Тип продукт", "Капацитет", "Степени на филтрация", "Резервоар под налягане", "Номинална мощност", "Тегло на продукта", "Размери", "Инсталация", "Приложение", "OEM/ODM", "MOQ"], "stage": "Петстепенна RO филтрация с PP седиментен филтър, предварителен въглен, RO мембрана и последващ въглен според поръчката", "tank": "Стандартно без резервоар; резервоар под налягане може да се добави по изискване на клиента", "frame": "Дървена рамка 47 x 33 x 90 cm", "install": "Подова търговска инсталация за директна питейна вода", "app": "Офиси, ресторанти, училища, кафенета, малки производства и дистрибуторски проекти", "oem": "Лого, панел, етикет, последователност на филтрите, опция за резервоар, опаковка и инструкция", "moq": "Потвърждава се според спецификацията и нивото на брандиране", "body": "Създадена за B2B дистрибутори и марки, машината поддържа 800G, 1200G, 1600G и 2000G, петстепенна RO филтрация, 160W мощност, 28 kg тегло и конфигурация без резервоар или с резервоар под налягане.", "card": "Търговска RO машина за директна питейна вода с 800G-2000G опции, петстепенна филтрация и OEM/ODM брандиране."},
    "bn": {"home": "হোম", "products": "পণ্য", "specs": "প্রযুক্তিগত স্পেসিফিকেশন", "options": "কনফিগারেশন অপশন", "related": "সম্পর্কিত পণ্য", "request": "OEM কোটেশন চাইুন", "send": "অনুসন্ধান পাঠান", "item": "আইটেম", "spec": "স্পেসিফিকেশন", "quality": "গুণমান নথি", "labels": ["পণ্যের ধরন", "ক্ষমতা", "ফিল্টার ধাপ", "প্রেশার ট্যাঙ্ক", "রেটেড পাওয়ার", "পণ্যের ওজন", "মাত্রা", "ইনস্টলেশন", "ব্যবহার", "OEM/ODM", "MOQ"], "stage": "PP সেডিমেন্ট, প্রি-কার্বন, RO মেমব্রেন এবং অর্ডার অনুযায়ী পোস্ট-কার্বনসহ পাঁচ ধাপের RO ফিল্টারেশন", "tank": "স্ট্যান্ডার্ডভাবে ট্যাঙ্কবিহীন; গ্রাহকের চাহিদা অনুযায়ী প্রেশার ট্যাঙ্ক যোগ করা যায়", "frame": "কাঠের ফ্রেম 47 x 33 x 90 cm", "install": "সরাসরি পানযোগ্য পানির জন্য ফ্লোর-স্ট্যান্ডিং বাণিজ্যিক ইনস্টলেশন", "app": "অফিস, রেস্টুরেন্ট, স্কুল, ক্যাফে, ছোট কারখানা এবং ডিস্ট্রিবিউটর প্রকল্প", "oem": "লোগো, প্যানেল, লেবেল, ফিল্টার ক্রম, ট্যাঙ্ক অপশন, প্যাকেজিং এবং ম্যানুয়াল", "moq": "স্পেসিফিকেশন ও ব্র্যান্ডিং স্তর অনুযায়ী নিশ্চিত করা হবে", "body": "B2B ডিস্ট্রিবিউটর ও ব্র্যান্ডের জন্য তৈরি; 800G, 1200G, 1600G ও 2000G ক্ষমতা, পাঁচ ধাপের RO ফিল্টারেশন, 160W পাওয়ার, 28 kg ওজন এবং ট্যাঙ্কবিহীন বা প্রেশার ট্যাঙ্ক কনফিগারেশন সমর্থন করে।", "card": "800G-2000G বাণিজ্যিক RO সরাসরি পানীয় জলের মেশিন, পাঁচ ধাপের ফিল্টারেশন ও OEM/ODM সহায়তা।"},
    "bs": {"home": "Početna", "products": "Proizvodi", "specs": "Tehničke specifikacije", "options": "Opcije konfiguracije", "related": "Povezani proizvodi", "request": "Zatraži OEM ponudu", "send": "Pošalji upit", "item": "Stavka", "spec": "Specifikacija", "quality": "Dokumenti kvaliteta", "labels": ["Tip proizvoda", "Kapacitet", "Faze filtracije", "Tlačni rezervoar", "Nazivna snaga", "Težina proizvoda", "Dimenzije", "Instalacija", "Primjena", "OEM/ODM", "MOQ"], "stage": "Petostepena RO filtracija sa PP sedimentom, predkarbonom, RO membranom i završnim karbonom prema narudžbi", "tank": "Standardno bez rezervoara; tlačni rezervoar se može dodati prema zahtjevu kupca", "frame": "Drveni okvir 47 x 33 x 90 cm", "install": "Podna komercijalna instalacija za direktnu pitku vodu", "app": "Uredi, restorani, škole, kafići, male fabrike i distributerski projekti", "oem": "Logo, panel, etiketa, redoslijed filtera, opcija rezervoara, pakovanje i uputstvo", "moq": "Potvrđuje se prema specifikaciji i nivou brendiranja", "body": "Namijenjen B2B distributerima i brendovima, podržava kapacitete 800G, 1200G, 1600G i 2000G, petostepenu RO filtraciju, snagu 160W, težinu 28 kg i opciju bez rezervoara ili sa tlačnim rezervoarom.", "card": "Komercijalna RO mašina za direktnu pitku vodu sa 800G-2000G opcijama, petostepenom filtracijom i OEM/ODM podrškom."},
    "cs": {"home": "Domů", "products": "Produkty", "specs": "Technické specifikace", "options": "Možnosti konfigurace", "related": "Související produkty", "request": "Vyžádat OEM nabídku", "send": "Odeslat poptávku", "item": "Položka", "spec": "Specifikace", "quality": "Dokumenty kvality", "labels": ["Typ produktu", "Kapacita", "Stupně filtrace", "Tlaková nádoba", "Jmenovitý výkon", "Hmotnost produktu", "Rozměry", "Instalace", "Použití", "OEM/ODM", "MOQ"], "stage": "Pětistupňová RO filtrace s PP sedimentem, předuhlím, RO membránou a douhlím podle objednávky", "tank": "Standardně bez nádrže; tlakovou nádobu lze přidat podle požadavku zákazníka", "frame": "Dřevěný rám 47 x 33 x 90 cm", "install": "Volně stojící komerční instalace pro přímou pitnou vodu", "app": "Kanceláře, restaurace, školy, kavárny, malé provozy a distribuční projekty", "oem": "Logo, panel, štítek, pořadí filtrů, varianta nádrže, balení a manuál", "moq": "Potvrzuje se podle specifikace a úrovně brandingu", "body": "Pro B2B distributory a značky, s kapacitami 800G, 1200G, 1600G a 2000G, pětistupňovou RO filtrací, výkonem 160W, hmotností 28 kg a provedením bez nádrže nebo s tlakovou nádobou.", "card": "Komerční RO zařízení pro přímou pitnou vodu s možnostmi 800G-2000G, pětistupňovou filtrací a OEM/ODM podporou."},
    "da": {"home": "Forside", "products": "Produkter", "specs": "Tekniske specifikationer", "options": "Konfigurationsmuligheder", "related": "Relaterede produkter", "request": "Anmod om OEM-tilbud", "send": "Send forespørgsel", "item": "Punkt", "spec": "Specifikation", "quality": "Kvalitetsdokumenter", "labels": ["Produkttype", "Kapacitet", "Filtreringstrin", "Tryktank", "Nominel effekt", "Produktvægt", "Dimensioner", "Installation", "Anvendelse", "OEM/ODM", "MOQ"], "stage": "Femtrins RO-filtrering med PP-sediment, forkul, RO-membran og efterkul efter ordre", "tank": "Standard uden tank; tryktank kan tilføjes efter kundens krav", "frame": "Træramme 47 x 33 x 90 cm", "install": "Gulvstående kommerciel installation til direkte drikkevand", "app": "Kontorer, restauranter, skoler, caféer, små fabrikker og distributørprojekter", "oem": "Logo, panel, etiket, filterrækkefølge, tankvalg, emballage og manual", "moq": "Bekræftes efter specifikation og brandingniveau", "body": "Udviklet til B2B-distributører og brands med 800G, 1200G, 1600G og 2000G kapaciteter, femtrins RO-filtrering, 160W effekt, 28 kg vægt og valg mellem tankløs drift eller tryktank.", "card": "Kommerciel RO-maskine til direkte drikkevand med 800G-2000G muligheder, femtrins filtrering og OEM/ODM-branding."},
    "el": {"home": "Αρχική", "products": "Προϊόντα", "specs": "Τεχνικές προδιαγραφές", "options": "Επιλογές διαμόρφωσης", "related": "Σχετικά προϊόντα", "request": "Ζητήστε προσφορά OEM", "send": "Αποστολή ερωτήματος", "item": "Στοιχείο", "spec": "Προδιαγραφή", "quality": "Έγγραφα ποιότητας", "labels": ["Τύπος προϊόντος", "Δυναμικότητα", "Στάδια φιλτραρίσματος", "Δεξαμενή πίεσης", "Ονομαστική ισχύς", "Βάρος προϊόντος", "Διαστάσεις", "Εγκατάσταση", "Εφαρμογή", "OEM/ODM", "MOQ"], "stage": "Πενταβάθμια φίλτρανση RO με φίλτρο PP, προ-άνθρακα, μεμβράνη RO και μετα-άνθρακα σύμφωνα με την παραγγελία", "tank": "Τυπικά χωρίς δεξαμενή· μπορεί να προστεθεί δεξαμενή πίεσης σύμφωνα με την απαίτηση του πελάτη", "frame": "Ξύλινο πλαίσιο 47 x 33 x 90 cm", "install": "Επιδαπέδια εμπορική εγκατάσταση για άμεσο πόσιμο νερό", "app": "Γραφεία, εστιατόρια, σχολεία, καφέ, μικρές μονάδες και έργα διανομέων", "oem": "Λογότυπο, πάνελ, ετικέτα, σειρά φίλτρων, επιλογή δεξαμενής, συσκευασία και εγχειρίδιο", "moq": "Επιβεβαιώνεται ανάλογα με τις προδιαγραφές και το επίπεδο branding", "body": "Σχεδιασμένο για B2B διανομείς και brands, υποστηρίζει 800G, 1200G, 1600G και 2000G, πενταβάθμια RO φίλτρανση, ισχύ 160W, βάρος 28 kg και διαμόρφωση χωρίς δεξαμενή ή με δεξαμενή πίεσης.", "card": "Εμπορική μηχανή RO για άμεσο πόσιμο νερό με επιλογές 800G-2000G, πενταβάθμια φίλτρανση και υποστήριξη OEM/ODM."},
    "et": {"home": "Avaleht", "products": "Tooted", "specs": "Tehnilised andmed", "options": "Konfiguratsiooni valikud", "related": "Seotud tooted", "request": "Küsi OEM pakkumist", "send": "Saada päring", "item": "Üksus", "spec": "Spetsifikatsioon", "quality": "Kvaliteedidokumendid", "labels": ["Toote tüüp", "Võimsus", "Filtreerimisetapid", "Survepaak", "Nimivõimsus", "Toote kaal", "Mõõtmed", "Paigaldus", "Kasutus", "OEM/ODM", "MOQ"], "stage": "Viieastmeline RO-filtreerimine PP-settefiltri, eelsöe, RO-membraani ja järelsöega vastavalt tellimusele", "tank": "Standardina paagita; survepaagi saab lisada kliendi nõude järgi", "frame": "Puitraam 47 x 33 x 90 cm", "install": "Põrandal seisev ärikasutuse paigaldus otse joogiveele", "app": "Kontorid, restoranid, koolid, kohvikud, väiketootmine ja edasimüüjate projektid", "oem": "Logo, paneel, etikett, filtrijärjestus, paagivalik, pakend ja juhend", "moq": "Kinnitatakse spetsifikatsiooni ja kaubamärgi taseme järgi", "body": "Mõeldud B2B edasimüüjatele ja brändidele, toetades 800G, 1200G, 1600G ja 2000G võimsusi, viieastmelist RO-filtreerimist, 160W võimsust, 28 kg kaalu ning paagita või survepaagiga konfiguratsiooni.", "card": "Ärikasutuse RO-joogiveeseade 800G-2000G valikutega, viieastmelise filtreerimise ja OEM/ODM-toega."},
    "fa": {"home": "خانه", "products": "محصولات", "specs": "مشخصات فنی", "options": "گزینه‌های پیکربندی", "related": "محصولات مرتبط", "request": "درخواست قیمت OEM", "send": "ارسال استعلام", "item": "مورد", "spec": "مشخصات", "quality": "اسناد کیفیت", "labels": ["نوع محصول", "ظرفیت", "مراحل فیلتراسیون", "مخزن تحت فشار", "توان نامی", "وزن محصول", "ابعاد", "نصب", "کاربرد", "OEM/ODM", "MOQ"], "stage": "فیلتراسیون RO پنج مرحله‌ای با فیلتر رسوب PP، کربن اولیه، ممبران RO و کربن نهایی مطابق سفارش", "tank": "به صورت استاندارد بدون مخزن؛ مخزن تحت فشار بر اساس نیاز مشتری قابل افزودن است", "frame": "فریم چوبی 47 x 33 x 90 cm", "install": "نصب ایستاده تجاری برای آب آشامیدنی مستقیم", "app": "دفاتر، رستوران‌ها، مدارس، کافه‌ها، کارخانه‌های کوچک و پروژه‌های توزیع‌کنندگان", "oem": "لوگو، پنل، برچسب، ترتیب فیلترها، گزینه مخزن، بسته‌بندی و دفترچه راهنما", "moq": "بر اساس مشخصات و سطح برندینگ تأیید می‌شود", "body": "برای توزیع‌کنندگان و برندهای B2B طراحی شده و ظرفیت‌های 800G، 1200G، 1600G و 2000G، فیلتراسیون RO پنج مرحله‌ای، توان 160W، وزن 28 kg و پیکربندی بدون مخزن یا با مخزن فشار را پشتیبانی می‌کند.", "card": "دستگاه RO تجاری آب آشامیدنی مستقیم با گزینه‌های 800G-2000G، فیلتراسیون پنج مرحله‌ای و پشتیبانی OEM/ODM."},
    "fi": {"home": "Etusivu", "products": "Tuotteet", "specs": "Tekniset tiedot", "options": "Kokoonpanovaihtoehdot", "related": "Aiheeseen liittyvät tuotteet", "request": "Pyydä OEM-tarjous", "send": "Lähetä kysely", "item": "Kohta", "spec": "Erittely", "quality": "Laatuasiakirjat", "labels": ["Tuotetyyppi", "Kapasiteetti", "Suodatusvaiheet", "Painesäiliö", "Nimellisteho", "Tuotteen paino", "Mitat", "Asennus", "Käyttökohde", "OEM/ODM", "MOQ"], "stage": "Viisivaiheinen RO-suodatus PP-sedimentillä, esihiilellä, RO-kalvolla ja jälkihiilellä tilauksen mukaan", "tank": "Vakiona ilman säiliötä; painesäiliö voidaan lisätä asiakkaan vaatimuksen mukaan", "frame": "Puurunko 47 x 33 x 90 cm", "install": "Lattialle asennettava kaupallinen ratkaisu suoralle juomavedelle", "app": "Toimistot, ravintolat, koulut, kahvilat, pienet tuotantotilat ja jälleenmyyjäprojektit", "oem": "Logo, paneeli, etiketti, suodatinjärjestys, säiliövaihtoehto, pakkaus ja käyttöohje", "moq": "Vahvistetaan erittelyn ja brändäystason mukaan", "body": "Suunniteltu B2B-jakelijoille ja brändeille; tukee 800G, 1200G, 1600G ja 2000G kapasiteetteja, viisivaiheista RO-suodatusta, 160W tehoa, 28 kg painoa sekä säiliötöntä tai painesäiliöllistä kokoonpanoa.", "card": "Kaupallinen RO-suorajuomavesilaite 800G-2000G vaihtoehdoilla, viisivaiheisella suodatuksella ja OEM/ODM-tuella."},
    "ha": {"home": "Gida", "products": "Kayayyaki", "specs": "Bayanan fasaha", "options": "Zaɓuɓɓukan tsari", "related": "Kayayyaki masu alaƙa", "request": "Nemi farashin OEM", "send": "Aika tambaya", "item": "Abu", "spec": "Bayani", "quality": "Takardun inganci", "labels": ["Nau'in samfur", "Ƙarfi", "Matakan tacewa", "Tankin matsa lamba", "Ƙarfin lantarki", "Nauyin samfur", "Girma", "Shigarwa", "Amfani", "OEM/ODM", "MOQ"], "stage": "Tacewar RO matakai biyar tare da PP sediment, carbon na farko, membrane RO da carbon na ƙarshe bisa odar abokin ciniki", "tank": "Ba tare da tanki a matsayin daidaito ba; ana iya ƙara tankin matsa lamba idan abokin ciniki ya buƙata", "frame": "Firam na itace 47 x 33 x 90 cm", "install": "Shigarwa ta kasuwanci a ƙasa don ruwan sha kai tsaye", "app": "Ofisoshi, gidajen abinci, makarantu, kafetoci, ƙananan masana'antu da ayyukan dillalai", "oem": "Tambari, panel, lakabi, jerin filter, zaɓin tanki, marufi da littafin amfani", "moq": "A tabbatar bisa ƙayyadaddun bayanai da matakin alama", "body": "An tsara shi don dillalan B2B da alamomi, yana tallafawa 800G, 1200G, 1600G da 2000G, tacewar RO matakai biyar, ƙarfin 160W, nauyi 28 kg da zaɓin ba tare da tanki ko tare da tankin matsa lamba ba.", "card": "Na'urar RO ta kasuwanci don ruwan sha kai tsaye, 800G-2000G, tacewa matakai biyar da tallafin OEM/ODM."},
    "he": {"home": "בית", "products": "מוצרים", "specs": "מפרט טכני", "options": "אפשרויות תצורה", "related": "מוצרים קשורים", "request": "בקשת הצעת OEM", "send": "שלח פנייה", "item": "פריט", "spec": "מפרט", "quality": "מסמכי איכות", "labels": ["סוג מוצר", "קיבולת", "שלבי סינון", "מכל לחץ", "הספק נקוב", "משקל מוצר", "מידות", "התקנה", "יישום", "OEM/ODM", "MOQ"], "stage": "סינון RO בן חמישה שלבים עם מסנן משקעים PP, פחם מקדים, ממברנת RO ופחם סופי לפי הזמנה", "tank": "סטנדרט ללא מכל; ניתן להוסיף מכל לחץ לפי דרישת הלקוח", "frame": "מסגרת עץ 47 x 33 x 90 cm", "install": "התקנה מסחרית עומדת לרצפה עבור מי שתייה ישירים", "app": "משרדים, מסעדות, בתי ספר, בתי קפה, מפעלים קטנים ופרויקטים של מפיצים", "oem": "לוגו, פאנל, תווית, סדר מסננים, אפשרות מכל, אריזה ומדריך", "moq": "יאושר לפי המפרט ורמת המיתוג", "body": "מיועד למפיצים ולמותגים B2B, עם קיבולות 800G, 1200G, 1600G ו-2000G, סינון RO בחמישה שלבים, הספק 160W, משקל 28 kg ותצורה ללא מכל או עם מכל לחץ.", "card": "מכונת RO מסחרית למי שתייה ישירים עם אפשרויות 800G-2000G, סינון חמישה שלבים ותמיכת OEM/ODM."},
    "hi": {"home": "होम", "products": "उत्पाद", "specs": "तकनीकी विनिर्देश", "options": "कॉन्फ़िगरेशन विकल्प", "related": "संबंधित उत्पाद", "request": "OEM कोटेशन माँगें", "send": "पूछताछ भेजें", "item": "आइटम", "spec": "विनिर्देश", "quality": "गुणवत्ता दस्तावेज", "labels": ["उत्पाद प्रकार", "क्षमता", "फिल्ट्रेशन चरण", "प्रेशर टैंक", "रेटेड पावर", "उत्पाद वजन", "आकार", "स्थापना", "उपयोग", "OEM/ODM", "MOQ"], "stage": "PP सेडिमेंट, प्री-कार्बन, RO मेम्ब्रेन और ऑर्डर के अनुसार पोस्ट-कार्बन के साथ पाँच चरण RO फिल्ट्रेशन", "tank": "मानक रूप से बिना टैंक; ग्राहक की आवश्यकता अनुसार प्रेशर टैंक जोड़ा जा सकता है", "frame": "लकड़ी का फ्रेम 47 x 33 x 90 cm", "install": "सीधे पेयजल के लिए फ्लोर-स्टैंडिंग वाणिज्यिक स्थापना", "app": "कार्यालय, रेस्टोरेंट, स्कूल, कैफे, छोटे कारखाने और वितरक प्रोजेक्ट", "oem": "लोगो, पैनल, लेबल, फिल्टर क्रम, टैंक विकल्प, पैकेजिंग और मैनुअल", "moq": "विनिर्देश और ब्रांडिंग स्तर के अनुसार पुष्टि", "body": "B2B वितरकों और ब्रांडों के लिए बनाया गया; 800G, 1200G, 1600G और 2000G क्षमता, पाँच चरण RO फिल्ट्रेशन, 160W पावर, 28 kg वजन और बिना टैंक या प्रेशर टैंक कॉन्फ़िगरेशन उपलब्ध है.", "card": "800G-2000G वाणिज्यिक RO डायरेक्ट ड्रिंकिंग मशीन, पाँच चरण फिल्ट्रेशन और OEM/ODM समर्थन।"},
    "hr": {"home": "Početna", "products": "Proizvodi", "specs": "Tehničke specifikacije", "options": "Opcije konfiguracije", "related": "Povezani proizvodi", "request": "Zatraži OEM ponudu", "send": "Pošalji upit", "item": "Stavka", "spec": "Specifikacija", "quality": "Dokumenti kvalitete", "labels": ["Vrsta proizvoda", "Kapacitet", "Faze filtracije", "Tlačni spremnik", "Nazivna snaga", "Težina proizvoda", "Dimenzije", "Instalacija", "Primjena", "OEM/ODM", "MOQ"], "stage": "Petostupanjska RO filtracija s PP sedimentom, predkarbonom, RO membranom i završnim karbonom prema narudžbi", "tank": "Standardno bez spremnika; tlačni spremnik može se dodati prema zahtjevu kupca", "frame": "Drveni okvir 47 x 33 x 90 cm", "install": "Podna komercijalna instalacija za izravnu pitku vodu", "app": "Uredi, restorani, škole, kafići, male tvornice i distribucijski projekti", "oem": "Logo, panel, etiketa, redoslijed filtera, opcija spremnika, pakiranje i priručnik", "moq": "Potvrđuje se prema specifikaciji i razini brendiranja", "body": "Za B2B distributere i brendove, podržava kapacitete 800G, 1200G, 1600G i 2000G, petostupanjsku RO filtraciju, snagu 160W, težinu 28 kg i konfiguraciju bez spremnika ili s tlačnim spremnikom.", "card": "Komercijalna RO mašina za izravnu pitku vodu s 800G-2000G opcijama, petostupanjskom filtracijom i OEM/ODM podrškom."},
    "hu": {"home": "Kezdőlap", "products": "Termékek", "specs": "Műszaki adatok", "options": "Konfigurációs lehetőségek", "related": "Kapcsolódó termékek", "request": "OEM ajánlat kérése", "send": "Érdeklődés küldése", "item": "Tétel", "spec": "Specifikáció", "quality": "Minőségi dokumentumok", "labels": ["Terméktípus", "Kapacitás", "Szűrési fokozatok", "Nyomástartály", "Névleges teljesítmény", "Terméktömeg", "Méretek", "Telepítés", "Alkalmazás", "OEM/ODM", "MOQ"], "stage": "Ötfokozatú RO szűrés PP üledékszűrővel, előszénnel, RO membránnal és utószénnel rendelés szerint", "tank": "Alapesetben tartály nélkül; nyomástartály a vevő igénye szerint hozzáadható", "frame": "Fa keret 47 x 33 x 90 cm", "install": "Padlón álló kereskedelmi telepítés közvetlen ivóvízhez", "app": "Irodák, éttermek, iskolák, kávézók, kisebb üzemek és disztribútori projektek", "oem": "Logó, panel, címke, szűrősorrend, tartályopció, csomagolás és kézikönyv", "moq": "Specifikáció és márkázási szint szerint megerősítendő", "body": "B2B forgalmazók és márkák számára készült, 800G, 1200G, 1600G és 2000G kapacitással, ötfokozatú RO szűréssel, 160W teljesítménnyel, 28 kg tömeggel, tartály nélküli vagy nyomástartályos kivitelben.", "card": "Kereskedelmi RO közvetlen ivóvízgép 800G-2000G opciókkal, ötfokozatú szűréssel és OEM/ODM támogatással."},
    "hy": {"home": "Գլխավոր", "products": "Ապրանքներ", "specs": "Տեխնիկական բնութագրեր", "options": "Կոնֆիգուրացիայի տարբերակներ", "related": "Առնչվող ապրանքներ", "request": "Պահանջել OEM գնառաջարկ", "send": "Ուղարկել հարցում", "item": "Կետ", "spec": "Բնութագիր", "quality": "Որակի փաստաթղթեր", "labels": ["Ապրանքի տեսակ", "Հզորություն", "Ֆիլտրացման փուլեր", "Ճնշման բաք", "Անվանական հզորություն", "Ապրանքի քաշ", "Չափսեր", "Տեղադրում", "Կիրառում", "OEM/ODM", "MOQ"], "stage": "Հինգ փուլ RO ֆիլտրացում՝ PP նստվածքային ֆիլտրով, նախնական ածխով, RO մեմբրանով և վերջնական ածխով ըստ պատվերի", "tank": "Ստանդարտ՝ առանց բաքի, ճնշման բաքը կարող է ավելացվել ըստ հաճախորդի պահանջի", "frame": "Փայտե շրջանակ 47 x 33 x 90 cm", "install": "Հատակին տեղադրվող կոմերցիոն համակարգ ուղղակի խմելու ջրի համար", "app": "Գրասենյակներ, ռեստորաններ, դպրոցներ, սրճարաններ, փոքր արտադրամասեր և դիստրիբյուտորային նախագծեր", "oem": "Լոգո, վահանակ, պիտակ, ֆիլտրերի հերթականություն, բաքի տարբերակ, փաթեթավորում և ձեռնարկ", "moq": "Հաստատվում է ըստ բնութագրի և բրենդավորման մակարդակի", "body": "Նախատեսված է B2B դիստրիբյուտորների և բրենդների համար՝ 800G, 1200G, 1600G և 2000G հզորություններով, հինգ փուլ RO ֆիլտրացմամբ, 160W հզորությամբ, 28 kg քաշով և առանց բաքի կամ ճնշման բաքով տարբերակով.", "card": "Կոմերցիոն RO ուղղակի խմելու ջրի մեքենա՝ 800G-2000G տարբերակներով, հինգ փուլ ֆիլտրացմամբ և OEM/ODM աջակցությամբ."},
    "id": {"home": "Beranda", "products": "Produk", "specs": "Spesifikasi Teknis", "options": "Opsi Konfigurasi", "related": "Produk Terkait", "request": "Minta Penawaran OEM", "send": "Kirim Pertanyaan", "item": "Item", "spec": "Spesifikasi", "quality": "Dokumen kualitas", "labels": ["Tipe produk", "Kapasitas", "Tahap filtrasi", "Tangki tekanan", "Daya terukur", "Berat produk", "Dimensi", "Instalasi", "Aplikasi", "OEM/ODM", "MOQ"], "stage": "Filtrasi RO lima tahap dengan sedimen PP, karbon awal, membran RO dan karbon akhir sesuai pesanan", "tank": "Standar tanpa tangki; tangki tekanan dapat ditambahkan sesuai kebutuhan pelanggan", "frame": "Rangka kayu 47 x 33 x 90 cm", "install": "Instalasi komersial berdiri untuk air minum langsung", "app": "Kantor, restoran, sekolah, kafe, pabrik kecil dan proyek distributor", "oem": "Logo, panel, label, urutan filter, opsi tangki, kemasan dan manual", "moq": "Dikonfirmasi sesuai spesifikasi dan tingkat branding", "body": "Dirancang untuk distributor dan merek B2B, mendukung kapasitas 800G, 1200G, 1600G dan 2000G, filtrasi RO lima tahap, daya 160W, berat 28 kg, serta konfigurasi tanpa tangki atau dengan tangki tekanan.", "card": "Mesin RO komersial untuk air minum langsung dengan opsi 800G-2000G, filtrasi lima tahap dan dukungan OEM/ODM."},
    "it": {"home": "Home", "products": "Prodotti", "specs": "Specifiche tecniche", "options": "Opzioni di configurazione", "related": "Prodotti correlati", "request": "Richiedi preventivo OEM", "send": "Invia richiesta", "item": "Voce", "spec": "Specificazione", "quality": "Documenti qualità", "labels": ["Tipo di prodotto", "Capacità", "Stadi di filtrazione", "Serbatoio a pressione", "Potenza nominale", "Peso prodotto", "Dimensioni", "Installazione", "Applicazione", "OEM/ODM", "MOQ"], "stage": "Filtrazione RO a cinque stadi con sedimento PP, carbone iniziale, membrana RO e post-carbone secondo ordine", "tank": "Standard senza serbatoio; serbatoio a pressione disponibile su richiesta del cliente", "frame": "Telaio in legno 47 x 33 x 90 cm", "install": "Installazione commerciale a pavimento per acqua potabile diretta", "app": "Uffici, ristoranti, scuole, bar, piccoli stabilimenti e progetti distributori", "oem": "Logo, pannello, etichetta, sequenza filtri, opzione serbatoio, imballaggio e manuale", "moq": "Da confermare in base a specifica e livello di branding", "body": "Pensato per distributori e marchi B2B, supporta capacità 800G, 1200G, 1600G e 2000G, filtrazione RO a cinque stadi, potenza 160W, peso 28 kg e configurazione senza serbatoio o con serbatoio a pressione.", "card": "Macchina RO commerciale per acqua potabile diretta con opzioni 800G-2000G, filtrazione a cinque stadi e supporto OEM/ODM."},
    "ka": {"home": "მთავარი", "products": "პროდუქტები", "specs": "ტექნიკური მახასიათებლები", "options": "კონფიგურაციის ვარიანტები", "related": "დაკავშირებული პროდუქტები", "request": "OEM ფასის მოთხოვნა", "send": "გაგზავნეთ მოთხოვნა", "item": "პუნქტი", "spec": "სპეციფიკაცია", "quality": "ხარისხის დოკუმენტები", "labels": ["პროდუქტის ტიპი", "წარმადობა", "ფილტრაციის ეტაპები", "წნევის ავზი", "ნომინალური სიმძლავრე", "პროდუქტის წონა", "ზომები", "ინსტალაცია", "გამოყენება", "OEM/ODM", "MOQ"], "stage": "ხუთეტაპიანი RO ფილტრაცია PP ნალექის ფილტრით, წინასწარი ნახშირით, RO მემბრანით და საბოლოო ნახშირით შეკვეთის მიხედვით", "tank": "სტანდარტულად ავზის გარეშე; წნევის ავზი ემატება მომხმარებლის მოთხოვნით", "frame": "ხის ჩარჩო 47 x 33 x 90 cm", "install": "იატაკზე მდგომი კომერციული ინსტალაცია პირდაპირი სასმელი წყლისთვის", "app": "ოფისები, რესტორნები, სკოლები, კაფეები, მცირე საწარმოები და დისტრიბუტორის პროექტები", "oem": "ლოგო, პანელი, ეტიკეტი, ფილტრების თანმიმდევრობა, ავზის ვარიანტი, შეფუთვა და სახელმძღვანელო", "moq": "დასტურდება სპეციფიკაციისა და ბრენდინგის დონის მიხედვით", "body": "შექმნილია B2B დისტრიბუტორებისა და ბრენდებისთვის; მხარს უჭერს 800G, 1200G, 1600G და 2000G წარმადობას, ხუთეტაპიან RO ფილტრაციას, 160W სიმძლავრეს, 28 kg წონას და ავზის გარეშე ან წნევის ავზით კონფიგურაციას.", "card": "კომერციული RO სასმელი წყლის მანქანა 800G-2000G ვარიანტებით, ხუთეტაპიანი ფილტრაციით და OEM/ODM მხარდაჭერით."},
    "ko": {"home": "홈", "products": "제품", "specs": "기술 사양", "options": "구성 옵션", "related": "관련 제품", "request": "OEM 견적 요청", "send": "문의 보내기", "item": "항목", "spec": "사양", "quality": "품질 문서", "labels": ["제품 유형", "용량", "여과 단계", "압력 탱크", "정격 전력", "제품 중량", "크기", "설치", "적용", "OEM/ODM", "MOQ"], "stage": "PP 침전, 전처리 카본, RO 멤브레인 및 주문형 후처리 카본을 포함한 5단 RO 여과", "tank": "기본은 탱크리스이며 고객 요구에 따라 압력 탱크 추가 가능", "frame": "목재 프레임 47 x 33 x 90 cm", "install": "직음수 공급을 위한 바닥 설치형 상업용 구성", "app": "사무실, 식당, 학교, 카페, 소규모 공장 및 유통 프로젝트", "oem": "로고, 패널, 라벨, 필터 순서, 탱크 옵션, 포장 및 설명서", "moq": "사양 및 브랜딩 수준에 따라 확인", "body": "B2B 유통업체와 브랜드를 위해 설계되었으며 800G, 1200G, 1600G, 2000G 용량, 5단 RO 여과, 160W 전력, 28 kg 중량, 탱크리스 또는 압력 탱크 구성을 지원합니다.", "card": "800G-2000G 상업용 직음수 RO 장비, 5단 여과 및 OEM/ODM 브랜딩 지원."},
    "ku": {"home": "Mal", "products": "Berhem", "specs": "Taybetmendiyên teknîkî", "options": "Vebijarkên sazkarî", "related": "Berhemên têkildar", "request": "Daxwaza bihayê OEM", "send": "Pirsiyar bişîne", "item": "Xal", "spec": "Taybetmendî", "quality": "Belgeyên kalîteyê", "labels": ["Cureyê berhemê", "Kapasîte", "Qonaxên parzûnkirinê", "Tankê zextê", "Hêza navdar", "Giraniya berhemê", "Mezinahî", "Sazkirin", "Bikaranîn", "OEM/ODM", "MOQ"], "stage": "Parzûnkirina RO ya pênc qonaxî bi PP sediment, karbonê pêşîn, membrana RO û karbonê dawî li gorî fermanê", "tank": "Standard bê tank e; tankê zextê dikare li gorî daxwaza xerîdar zêde bibe", "frame": "Çarçoveya darîn 47 x 33 x 90 cm", "install": "Sazkirina bazirganî ya li erdê ji bo ava vexwarinê ya rasterast", "app": "Ofîs, xwaringeh, dibistan, kafe, kargehên biçûk û projeyên belavkaran", "oem": "Logo, panel, etîket, rêza filteran, vebijarka tankê, pakêt û rêbername", "moq": "Li gorî taybetmendî û asta markeyê tê piştrastkirin", "body": "Ji bo belavkar û markeyên B2B hatî amadekirin; kapasîteyên 800G, 1200G, 1600G û 2000G, parzûnkirina RO ya pênc qonaxî, hêza 160W, giraniya 28 kg û sazkarî bê tank an bi tankê zextê piştgirî dike.", "card": "Makîneya RO ya bazirganî ji bo ava vexwarinê ya rasterast, 800G-2000G, pênc qonax parzûnkirin û piştgiriya OEM/ODM."},
    "lt": {"home": "Pagrindinis", "products": "Produktai", "specs": "Techninės specifikacijos", "options": "Konfigūracijos parinktys", "related": "Susiję produktai", "request": "Prašyti OEM pasiūlymo", "send": "Siųsti užklausą", "item": "Pozicija", "spec": "Specifikacija", "quality": "Kokybės dokumentai", "labels": ["Produkto tipas", "Našumas", "Filtravimo etapai", "Slėginis bakas", "Nominali galia", "Produkto svoris", "Matmenys", "Montavimas", "Pritaikymas", "OEM/ODM", "MOQ"], "stage": "Penkių etapų RO filtravimas su PP nuosėdų filtru, pirminiu anglimi, RO membrana ir galutiniu anglimi pagal užsakymą", "tank": "Standartiškai be bako; slėginį baką galima pridėti pagal kliento poreikį", "frame": "Medinis rėmas 47 x 33 x 90 cm", "install": "Ant grindų statomas komercinis montavimas tiesioginiam geriamajam vandeniui", "app": "Biurai, restoranai, mokyklos, kavinės, mažos gamyklos ir platintojų projektai", "oem": "Logotipas, skydelis, etiketė, filtrų seka, bako parinktis, pakuotė ir instrukcija", "moq": "Patvirtinama pagal specifikaciją ir prekės ženklo lygį", "body": "Skirta B2B platintojams ir prekių ženklams, palaiko 800G, 1200G, 1600G ir 2000G našumą, penkių etapų RO filtravimą, 160W galią, 28 kg svorį ir be bako arba su slėginiu baku konfigūraciją.", "card": "Komercinis RO tiesioginio geriamojo vandens įrenginys su 800G-2000G parinktimis, penkių etapų filtravimu ir OEM/ODM palaikymu."},
    "lv": {"home": "Sākums", "products": "Produkti", "specs": "Tehniskās specifikācijas", "options": "Konfigurācijas iespējas", "related": "Saistītie produkti", "request": "Pieprasīt OEM piedāvājumu", "send": "Nosūtīt pieprasījumu", "item": "Pozīcija", "spec": "Specifikācija", "quality": "Kvalitātes dokumenti", "labels": ["Produkta tips", "Jauda", "Filtrēšanas posmi", "Spiediena tvertne", "Nominālā jauda", "Produkta svars", "Izmēri", "Uzstādīšana", "Lietojums", "OEM/ODM", "MOQ"], "stage": "Piecu posmu RO filtrācija ar PP nogulšņu filtru, priekšoglekli, RO membrānu un pēcoglekli pēc pasūtījuma", "tank": "Standartā bez tvertnes; spiediena tvertni var pievienot pēc klienta prasības", "frame": "Koka rāmis 47 x 33 x 90 cm", "install": "Uz grīdas novietojama komerciāla uzstādīšana tiešam dzeramajam ūdenim", "app": "Biroji, restorāni, skolas, kafejnīcas, mazas ražotnes un izplatītāju projekti", "oem": "Logotips, panelis, etiķete, filtru secība, tvertnes opcija, iepakojums un rokasgrāmata", "moq": "Apstiprina pēc specifikācijas un zīmola līmeņa", "body": "Paredzēts B2B izplatītājiem un zīmoliem, atbalsta 800G, 1200G, 1600G un 2000G jaudu, piecu posmu RO filtrāciju, 160W jaudu, 28 kg svaru un konfigurāciju bez tvertnes vai ar spiediena tvertni.", "card": "Komerciāla RO tiešā dzeramā ūdens iekārta ar 800G-2000G opcijām, piecu posmu filtrāciju un OEM/ODM atbalstu."},
    "ms": {"home": "Laman Utama", "products": "Produk", "specs": "Spesifikasi Teknikal", "options": "Pilihan konfigurasi", "related": "Produk berkaitan", "request": "Minta sebut harga OEM", "send": "Hantar pertanyaan", "item": "Item", "spec": "Spesifikasi", "quality": "Dokumen kualiti", "labels": ["Jenis produk", "Kapasiti", "Tahap penapisan", "Tangki tekanan", "Kuasa berkadar", "Berat produk", "Dimensi", "Pemasangan", "Aplikasi", "OEM/ODM", "MOQ"], "stage": "Penapisan RO lima tahap dengan sedimen PP, karbon awal, membran RO dan karbon akhir mengikut pesanan", "tank": "Standard tanpa tangki; tangki tekanan boleh ditambah mengikut keperluan pelanggan", "frame": "Rangka kayu 47 x 33 x 90 cm", "install": "Pemasangan komersial berdiri untuk air minuman terus", "app": "Pejabat, restoran, sekolah, kafe, kilang kecil dan projek pengedar", "oem": "Logo, panel, label, urutan penapis, pilihan tangki, pembungkusan dan manual", "moq": "Disahkan mengikut spesifikasi dan tahap penjenamaan", "body": "Direka untuk pengedar dan jenama B2B, menyokong kapasiti 800G, 1200G, 1600G dan 2000G, penapisan RO lima tahap, kuasa 160W, berat 28 kg serta konfigurasi tanpa tangki atau dengan tangki tekanan.", "card": "Mesin RO komersial air minuman terus dengan pilihan 800G-2000G, penapisan lima tahap dan sokongan OEM/ODM."},
    "nl": {"home": "Home", "products": "Producten", "specs": "Technische specificaties", "options": "Configuratieopties", "related": "Gerelateerde producten", "request": "OEM-offerte aanvragen", "send": "Aanvraag verzenden", "item": "Item", "spec": "Specificatie", "quality": "Kwaliteitsdocumenten", "labels": ["Producttype", "Capaciteit", "Filtratiestappen", "Druktank", "Nominaal vermogen", "Productgewicht", "Afmetingen", "Installatie", "Toepassing", "OEM/ODM", "MOQ"], "stage": "Vijftraps RO-filtratie met PP-sediment, voorkool, RO-membraan en nakool volgens bestelling", "tank": "Standaard zonder tank; druktank kan volgens klantwens worden toegevoegd", "frame": "Houten frame 47 x 33 x 90 cm", "install": "Vrijstaande commerciële installatie voor direct drinkwater", "app": "Kantoren, restaurants, scholen, cafés, kleine fabrieken en distributeursprojecten", "oem": "Logo, paneel, label, filtervolgorde, tankoptie, verpakking en handleiding", "moq": "Te bevestigen volgens specificatie en brandingniveau", "body": "Ontworpen voor B2B-distributeurs en merken, met 800G, 1200G, 1600G en 2000G capaciteit, vijftraps RO-filtratie, 160W vermogen, 28 kg gewicht en configuratie zonder tank of met druktank.", "card": "Commerciële RO-machine voor direct drinkwater met 800G-2000G opties, vijftraps filtratie en OEM/ODM-ondersteuning."},
    "no": {"home": "Hjem", "products": "Produkter", "specs": "Tekniske spesifikasjoner", "options": "Konfigurasjonsvalg", "related": "Relaterte produkter", "request": "Be om OEM-tilbud", "send": "Send forespørsel", "item": "Punkt", "spec": "Spesifikasjon", "quality": "Kvalitetsdokumenter", "labels": ["Produkttype", "Kapasitet", "Filtreringstrinn", "Trykktank", "Nominell effekt", "Produktvekt", "Dimensjoner", "Installasjon", "Bruk", "OEM/ODM", "MOQ"], "stage": "Femtrinns RO-filtrering med PP-sediment, forkull, RO-membran og etterkull etter ordre", "tank": "Standard uten tank; trykktank kan legges til etter kundens krav", "frame": "Treramme 47 x 33 x 90 cm", "install": "Gulvstående kommersiell installasjon for direkte drikkevann", "app": "Kontorer, restauranter, skoler, kafeer, små fabrikker og distributørprosjekter", "oem": "Logo, panel, etikett, filterrekkefølge, tankvalg, emballasje og manual", "moq": "Bekreftes etter spesifikasjon og merkevarenivå", "body": "Utviklet for B2B-distributører og merkevarer, med 800G, 1200G, 1600G og 2000G kapasitet, femtrinns RO-filtrering, 160W effekt, 28 kg vekt og tankløs eller trykktankkonfigurasjon.", "card": "Kommersiell RO-maskin for direkte drikkevann med 800G-2000G alternativer, femtrinns filtrering og OEM/ODM-støtte."},
    "pl": {"home": "Strona główna", "products": "Produkty", "specs": "Specyfikacja techniczna", "options": "Opcje konfiguracji", "related": "Produkty powiązane", "request": "Poproś o wycenę OEM", "send": "Wyślij zapytanie", "item": "Pozycja", "spec": "Specyfikacja", "quality": "Dokumenty jakości", "labels": ["Typ produktu", "Wydajność", "Etapy filtracji", "Zbiornik ciśnieniowy", "Moc znamionowa", "Waga produktu", "Wymiary", "Instalacja", "Zastosowanie", "OEM/ODM", "MOQ"], "stage": "Pięciostopniowa filtracja RO z filtrem PP, węglem wstępnym, membraną RO i węglem końcowym według zamówienia", "tank": "Standardowo bez zbiornika; zbiornik ciśnieniowy może być dodany według wymagań klienta", "frame": "Rama drewniana 47 x 33 x 90 cm", "install": "Wolnostojąca instalacja komercyjna do bezpośredniej wody pitnej", "app": "Biura, restauracje, szkoły, kawiarnie, małe zakłady i projekty dystrybutorów", "oem": "Logo, panel, etykieta, kolejność filtrów, opcja zbiornika, opakowanie i instrukcja", "moq": "Potwierdzane według specyfikacji i poziomu brandingu", "body": "Dla dystrybutorów i marek B2B, obsługuje wydajności 800G, 1200G, 1600G i 2000G, pięciostopniową filtrację RO, moc 160W, wagę 28 kg oraz konfigurację bez zbiornika lub ze zbiornikiem ciśnieniowym.", "card": "Komercyjna maszyna RO do bezpośredniej wody pitnej z opcjami 800G-2000G, pięciostopniową filtracją i wsparciem OEM/ODM."},
    "pt": {"home": "Início", "products": "Produtos", "specs": "Especificações técnicas", "options": "Opções de configuração", "related": "Produtos relacionados", "request": "Solicitar cotação OEM", "send": "Enviar consulta", "item": "Item", "spec": "Especificação", "quality": "Documentos de qualidade", "labels": ["Tipo de produto", "Capacidade", "Etapas de filtração", "Tanque de pressão", "Potência nominal", "Peso do produto", "Dimensões", "Instalação", "Aplicação", "OEM/ODM", "MOQ"], "stage": "Filtração RO em cinco etapas com sedimento PP, carvão inicial, membrana RO e pós-carvão conforme pedido", "tank": "Padrão sem tanque; tanque de pressão pode ser adicionado conforme a necessidade do cliente", "frame": "Estrutura de madeira 47 x 33 x 90 cm", "install": "Instalação comercial de piso para água potável direta", "app": "Escritórios, restaurantes, escolas, cafés, pequenas fábricas e projetos de distribuidores", "oem": "Logo, painel, etiqueta, sequência de filtros, opção de tanque, embalagem e manual", "moq": "Confirmado conforme especificação e nível de marca", "body": "Projetado para distribuidores e marcas B2B, suporta capacidades 800G, 1200G, 1600G e 2000G, filtração RO em cinco etapas, potência 160W, peso 28 kg e configuração sem tanque ou com tanque de pressão.", "card": "Máquina RO comercial para água potável direta com opções 800G-2000G, filtração em cinco etapas e suporte OEM/ODM."},
    "ro": {"home": "Acasă", "products": "Produse", "specs": "Specificații tehnice", "options": "Opțiuni de configurare", "related": "Produse conexe", "request": "Solicită ofertă OEM", "send": "Trimite cerere", "item": "Element", "spec": "Specificație", "quality": "Documente de calitate", "labels": ["Tip produs", "Capacitate", "Etape de filtrare", "Rezervor sub presiune", "Putere nominală", "Greutate produs", "Dimensiuni", "Instalare", "Aplicație", "OEM/ODM", "MOQ"], "stage": "Filtrare RO în cinci etape cu sediment PP, carbon preliminar, membrană RO și post-carbon conform comenzii", "tank": "Standard fără rezervor; rezervorul sub presiune poate fi adăugat la cererea clientului", "frame": "Cadru din lemn 47 x 33 x 90 cm", "install": "Instalare comercială pe podea pentru apă potabilă directă", "app": "Birouri, restaurante, școli, cafenele, fabrici mici și proiecte de distribuitori", "oem": "Logo, panou, etichetă, secvență filtre, opțiune rezervor, ambalaj și manual", "moq": "Confirmat în funcție de specificație și nivelul de branding", "body": "Proiectat pentru distribuitori și branduri B2B, acceptă capacități 800G, 1200G, 1600G și 2000G, filtrare RO în cinci etape, putere 160W, greutate 28 kg și configurație fără rezervor sau cu rezervor sub presiune.", "card": "Mașină RO comercială pentru apă potabilă directă cu opțiuni 800G-2000G, filtrare în cinci etape și suport OEM/ODM."},
    "sk": {"home": "Domov", "products": "Produkty", "specs": "Technické špecifikácie", "options": "Možnosti konfigurácie", "related": "Súvisiace produkty", "request": "Požiadať o OEM ponuku", "send": "Odoslať dopyt", "item": "Položka", "spec": "Špecifikácia", "quality": "Dokumenty kvality", "labels": ["Typ produktu", "Kapacita", "Stupne filtrácie", "Tlaková nádoba", "Menovitý výkon", "Hmotnosť produktu", "Rozmery", "Inštalácia", "Použitie", "OEM/ODM", "MOQ"], "stage": "Päťstupňová RO filtrácia s PP sedimentom, pred-uhlíkom, RO membránou a do-uhlíkom podľa objednávky", "tank": "Štandardne bez nádoby; tlaková nádoba môže byť pridaná podľa požiadavky zákazníka", "frame": "Drevený rám 47 x 33 x 90 cm", "install": "Voľne stojaca komerčná inštalácia pre priamu pitnú vodu", "app": "Kancelárie, reštaurácie, školy, kaviarne, malé prevádzky a distribútorské projekty", "oem": "Logo, panel, etiketa, poradie filtrov, možnosť nádoby, balenie a manuál", "moq": "Potvrdzuje sa podľa špecifikácie a úrovne brandingu", "body": "Pre B2B distribútorov a značky, podporuje kapacity 800G, 1200G, 1600G a 2000G, päťstupňovú RO filtráciu, výkon 160W, hmotnosť 28 kg a konfiguráciu bez nádoby alebo s tlakovou nádobou.", "card": "Komerčné RO zariadenie na priamu pitnú vodu s možnosťami 800G-2000G, päťstupňovou filtráciou a OEM/ODM podporou."},
    "sl": {"home": "Domov", "products": "Izdelki", "specs": "Tehnične specifikacije", "options": "Možnosti konfiguracije", "related": "Povezani izdelki", "request": "Zahtevaj OEM ponudbo", "send": "Pošlji povpraševanje", "item": "Postavka", "spec": "Specifikacija", "quality": "Dokumenti kakovosti", "labels": ["Vrsta izdelka", "Kapaciteta", "Stopnje filtracije", "Tlačni rezervoar", "Nazivna moč", "Teža izdelka", "Dimenzije", "Namestitev", "Uporaba", "OEM/ODM", "MOQ"], "stage": "Petstopenjska RO filtracija s PP sedimentom, predogljem, RO membrano in končnim ogljem po naročilu", "tank": "Standardno brez rezervoarja; tlačni rezervoar se lahko doda po zahtevi kupca", "frame": "Leseni okvir 47 x 33 x 90 cm", "install": "Talna komercialna namestitev za neposredno pitno vodo", "app": "Pisarne, restavracije, šole, kavarne, manjše tovarne in projekti distributerjev", "oem": "Logotip, panel, etiketa, zaporedje filtrov, možnost rezervoarja, embalaža in priročnik", "moq": "Potrdi se glede na specifikacijo in raven blagovne znamke", "body": "Za B2B distributerje in blagovne znamke podpira kapacitete 800G, 1200G, 1600G in 2000G, petstopenjsko RO filtracijo, moč 160W, težo 28 kg ter konfiguracijo brez rezervoarja ali s tlačnim rezervoarjem.", "card": "Komercialna RO naprava za neposredno pitno vodo z možnostmi 800G-2000G, petstopenjsko filtracijo in podporo OEM/ODM."},
    "sq": {"home": "Kryefaqja", "products": "Produkte", "specs": "Specifikime teknike", "options": "Opsione konfigurimi", "related": "Produkte të lidhura", "request": "Kërko ofertë OEM", "send": "Dërgo kërkesë", "item": "Artikull", "spec": "Specifikim", "quality": "Dokumente cilësie", "labels": ["Lloji i produktit", "Kapaciteti", "Fazat e filtrimit", "Depozita e presionit", "Fuqia nominale", "Pesha e produktit", "Përmasat", "Instalimi", "Aplikimi", "OEM/ODM", "MOQ"], "stage": "Filtrim RO me pesë faza me sediment PP, karbon fillestar, membranë RO dhe karbon përfundimtar sipas porosisë", "tank": "Standard pa depozitë; depozita e presionit mund të shtohet sipas kërkesës së klientit", "frame": "Kornizë druri 47 x 33 x 90 cm", "install": "Instalim komercial në dysheme për ujë të pijshëm direkt", "app": "Zyra, restorante, shkolla, kafene, fabrika të vogla dhe projekte distributorësh", "oem": "Logo, panel, etiketë, renditje filtrash, opsion depozite, paketim dhe manual", "moq": "Konfirmohet sipas specifikimit dhe nivelit të markimit", "body": "I projektuar për distributorë dhe marka B2B, mbështet kapacitete 800G, 1200G, 1600G dhe 2000G, filtrim RO me pesë faza, fuqi 160W, peshë 28 kg dhe konfigurim pa depozitë ose me depozitë presioni.", "card": "Makineri RO komerciale për ujë të pijshëm direkt me opsione 800G-2000G, filtrim me pesë faza dhe mbështetje OEM/ODM."},
    "sr": {"home": "Почетна", "products": "Производи", "specs": "Техничке спецификације", "options": "Опције конфигурације", "related": "Повезани производи", "request": "Затражи OEM понуду", "send": "Пошаљи упит", "item": "Ставка", "spec": "Спецификација", "quality": "Документи квалитета", "labels": ["Тип производа", "Капацитет", "Фазе филтрације", "Резервоар под притиском", "Номинална снага", "Тежина производа", "Димензије", "Инсталација", "Примена", "OEM/ODM", "MOQ"], "stage": "Петостепена RO филтрација са PP седиментом, предугљем, RO мембраном и завршним угљем према наруџбини", "tank": "Стандардно без резервоара; резервоар под притиском може се додати по захтеву купца", "frame": "Дрвени оквир 47 x 33 x 90 cm", "install": "Подна комерцијална инсталација за директну питку воду", "app": "Канцеларије, ресторани, школе, кафићи, мале фабрике и дистрибутерски пројекти", "oem": "Лого, панел, етикета, редослед филтера, опција резервоара, паковање и упутство", "moq": "Потврђује се према спецификацији и нивоу брендирања", "body": "За B2B дистрибутере и брендове, подржава капацитете 800G, 1200G, 1600G и 2000G, петостепену RO филтрацију, снагу 160W, тежину 28 kg и конфигурацију без резервоара или са резервоаром под притиском.", "card": "Комерцијална RO машина за директну питку воду са 800G-2000G опцијама, петостепеном филтрацијом и OEM/ODM подршком."},
    "sr-me": {"home": "Početna", "products": "Proizvodi", "specs": "Tehničke specifikacije", "options": "Opcije konfiguracije", "related": "Povezani proizvodi", "request": "Zatraži OEM ponudu", "send": "Pošalji upit", "item": "Stavka", "spec": "Specifikacija", "quality": "Dokumenti kvaliteta", "labels": ["Tip proizvoda", "Kapacitet", "Faze filtracije", "Tlačni rezervoar", "Nazivna snaga", "Težina proizvoda", "Dimenzije", "Instalacija", "Primjena", "OEM/ODM", "MOQ"], "stage": "Petostepena RO filtracija sa PP sedimentom, predkarbonom, RO membranom i završnim karbonom prema narudžbi", "tank": "Standardno bez rezervoara; tlačni rezervoar može se dodati prema zahtjevu kupca", "frame": "Drveni okvir 47 x 33 x 90 cm", "install": "Podna komercijalna instalacija za direktnu pitku vodu", "app": "Kancelarije, restorani, škole, kafići, male fabrike i distributerski projekti", "oem": "Logo, panel, etiketa, redosljed filtera, opcija rezervoara, pakovanje i uputstvo", "moq": "Potvrđuje se prema specifikaciji i nivou brendiranja", "body": "Za B2B distributere i brendove, podržava kapacitete 800G, 1200G, 1600G i 2000G, petostepenu RO filtraciju, snagu 160W, težinu 28 kg i konfiguraciju bez rezervoara ili sa tlačnim rezervoarom.", "card": "Komercijalna RO mašina za direktnu pitku vodu sa 800G-2000G opcijama, petostepenom filtracijom i OEM/ODM podrškom."},
    "sv": {"home": "Hem", "products": "Produkter", "specs": "Tekniska specifikationer", "options": "Konfigurationsalternativ", "related": "Relaterade produkter", "request": "Begär OEM-offert", "send": "Skicka förfrågan", "item": "Post", "spec": "Specifikation", "quality": "Kvalitetsdokument", "labels": ["Produkttyp", "Kapacitet", "Filtreringssteg", "Trycktank", "Märkeffekt", "Produktvikt", "Mått", "Installation", "Användning", "OEM/ODM", "MOQ"], "stage": "Femstegs RO-filtrering med PP-sediment, förkol, RO-membran och efterkol enligt order", "tank": "Standard utan tank; trycktank kan läggas till enligt kundens krav", "frame": "Träram 47 x 33 x 90 cm", "install": "Golvstående kommersiell installation för direkt dricksvatten", "app": "Kontor, restauranger, skolor, kaféer, små fabriker och distributörsprojekt", "oem": "Logotyp, panel, etikett, filtersekvens, tankalternativ, förpackning och manual", "moq": "Bekräftas enligt specifikation och varumärkesnivå", "body": "Utformad för B2B-distributörer och varumärken, med 800G, 1200G, 1600G och 2000G kapacitet, femstegs RO-filtrering, 160W effekt, 28 kg vikt och tanklös eller trycktankskonfiguration.", "card": "Kommersiell RO-maskin för direkt dricksvatten med 800G-2000G alternativ, femstegs filtrering och OEM/ODM-stöd."},
    "sw": {"home": "Nyumbani", "products": "Bidhaa", "specs": "Maelezo ya kiufundi", "options": "Chaguo za usanidi", "related": "Bidhaa zinazohusiana", "request": "Omba nukuu ya OEM", "send": "Tuma ombi", "item": "Kipengee", "spec": "Maelezo", "quality": "Nyaraka za ubora", "labels": ["Aina ya bidhaa", "Uwezo", "Hatua za uchujaji", "Tanki la shinikizo", "Nguvu iliyokadiriwa", "Uzito wa bidhaa", "Vipimo", "Ufungaji", "Matumizi", "OEM/ODM", "MOQ"], "stage": "Uchujaji wa RO wa hatua tano wenye PP sediment, kaboni ya awali, membrane ya RO na kaboni ya mwisho kulingana na oda", "tank": "Kawaida bila tanki; tanki la shinikizo linaweza kuongezwa kulingana na mahitaji ya mteja", "frame": "Fremu ya mbao 47 x 33 x 90 cm", "install": "Ufungaji wa kibiashara unaosimama sakafuni kwa maji ya kunywa moja kwa moja", "app": "Ofisi, migahawa, shule, mikahawa, viwanda vidogo na miradi ya wasambazaji", "oem": "Nembo, paneli, lebo, mpangilio wa vichujio, chaguo la tanki, ufungaji na mwongozo", "moq": "Huthibitishwa kulingana na vipimo na kiwango cha chapa", "body": "Imeundwa kwa wasambazaji na chapa za B2B, ikisaidia uwezo wa 800G, 1200G, 1600G na 2000G, uchujaji wa RO wa hatua tano, nguvu 160W, uzito 28 kg na usanidi bila tanki au kwa tanki la shinikizo.", "card": "Mashine ya RO ya kibiashara kwa maji ya kunywa moja kwa moja, 800G-2000G, uchujaji hatua tano na usaidizi wa OEM/ODM."},
    "ta": {"home": "முகப்பு", "products": "தயாரிப்புகள்", "specs": "தொழில்நுட்ப விவரங்கள்", "options": "கட்டமைப்பு விருப்பங்கள்", "related": "தொடர்புடைய தயாரிப்புகள்", "request": "OEM மேற்கோள் கேளுங்கள்", "send": "விசாரணை அனுப்பவும்", "item": "உருப்படி", "spec": "விவரம்", "quality": "தர ஆவணங்கள்", "labels": ["தயாரிப்பு வகை", "திறன்", "வடிகட்டி நிலைகள்", "அழுத்தத் தொட்டி", "மதிப்பிடப்பட்ட சக்தி", "தயாரிப்பு எடை", "அளவுகள்", "நிறுவல்", "பயன்பாடு", "OEM/ODM", "MOQ"], "stage": "PP sediment, முன் கார்பன், RO membrane மற்றும் ஆர்டர் படி பின் கார்பன் உடன் ஐந்து நிலை RO வடிகட்டி", "tank": "நிலையானது தொட்டி இல்லாமல்; வாடிக்கையாளர் தேவைக்கு ஏற்ப அழுத்தத் தொட்டி சேர்க்கலாம்", "frame": "மர சட்டம் 47 x 33 x 90 cm", "install": "நேரடி குடிநீருக்கான தரையில் நிற்கும் வர்த்தக நிறுவல்", "app": "அலுவலகங்கள், உணவகங்கள், பள்ளிகள், கஃபேக்கள், சிறு தொழிற்சாலைகள் மற்றும் விநியோகஸ்தர் திட்டங்கள்", "oem": "லோகோ, பேனல், லேபிள், வடிகட்டி வரிசை, தொட்டி விருப்பம், பேக்கிங் மற்றும் கையேடு", "moq": "விவரம் மற்றும் பிராண்டிங் நிலைக்கு ஏற்ப உறுதி செய்யப்படும்", "body": "B2B விநியோகஸ்தர்கள் மற்றும் பிராண்டுகளுக்காக வடிவமைக்கப்பட்டது; 800G, 1200G, 1600G, 2000G திறன், ஐந்து நிலை RO வடிகட்டி, 160W சக்தி, 28 kg எடை, தொட்டி இல்லா அல்லது அழுத்தத் தொட்டி அமைப்பை ஆதரிக்கிறது.", "card": "800G-2000G வர்த்தக RO நேரடி குடிநீர் இயந்திரம், ஐந்து நிலை வடிகட்டி மற்றும் OEM/ODM ஆதரவு."},
    "tg": {"home": "Асосӣ", "products": "Маҳсулот", "specs": "Хусусиятҳои техникӣ", "options": "Имконоти конфигуратсия", "related": "Маҳсулоти марбут", "request": "Дархости нархи OEM", "send": "Ирсоли дархост", "item": "Банд", "spec": "Спецификатсия", "quality": "Ҳуҷҷатҳои сифат", "labels": ["Навъи маҳсулот", "Иқтидор", "Марҳилаҳои филтр", "Зарфи фишор", "Қувваи номиналӣ", "Вазни маҳсулот", "Андозаҳо", "Насб", "Истифода", "OEM/ODM", "MOQ"], "stage": "Филтратсияи RO панҷмарҳила бо PP sediment, карбони пешакӣ, мембранаи RO ва карбони ниҳоӣ мувофиқи фармоиш", "tank": "Стандартӣ бе зарф; зарфи фишор мувофиқи талаботи муштарӣ илова мешавад", "frame": "Чорчӯбаи чӯбӣ 47 x 33 x 90 cm", "install": "Насби тиҷоратии рӯизаминӣ барои оби нӯшокии мустақим", "app": "Идораҳо, тарабхонаҳо, мактабҳо, қаҳвахонаҳо, корхонаҳои хурд ва лоиҳаҳои дистрибюторӣ", "oem": "Лого, панел, тамға, тартиби филтрҳо, интихоби зарф, бастабандӣ ва дастур", "moq": "Мувофиқи спецификатсия ва сатҳи бренд тасдиқ мешавад", "body": "Барои дистрибюторҳо ва брендҳои B2B таҳия шудааст; иқтидорҳои 800G, 1200G, 1600G ва 2000G, филтратсияи RO панҷмарҳила, қувваи 160W, вазни 28 kg ва конфигуратсияи бе зарф ё бо зарфи фишорро дастгирӣ мекунад.", "card": "Дастгоҳи тиҷоратии RO барои оби нӯшокии мустақим бо имконоти 800G-2000G, филтратсияи панҷмарҳила ва дастгирии OEM/ODM."},
    "th": {"home": "หน้าแรก", "products": "ผลิตภัณฑ์", "specs": "ข้อมูลจำเพาะทางเทคนิค", "options": "ตัวเลือกการกำหนดค่า", "related": "ผลิตภัณฑ์ที่เกี่ยวข้อง", "request": "ขอใบเสนอราคา OEM", "send": "ส่งคำถาม", "item": "รายการ", "spec": "ข้อมูลจำเพาะ", "quality": "เอกสารคุณภาพ", "labels": ["ประเภทสินค้า", "กำลังการผลิต", "ขั้นตอนการกรอง", "ถังแรงดัน", "กำลังไฟพิกัด", "น้ำหนักสินค้า", "ขนาด", "การติดตั้ง", "การใช้งาน", "OEM/ODM", "MOQ"], "stage": "การกรอง RO 5 ขั้นตอน พร้อม PP sediment, คาร์บอนก่อนกรอง, เมมเบรน RO และคาร์บอนหลังกรองตามคำสั่งซื้อ", "tank": "มาตรฐานเป็นแบบไม่มีถัง สามารถเพิ่มถังแรงดันตามความต้องการของลูกค้า", "frame": "โครงไม้ 47 x 33 x 90 cm", "install": "ติดตั้งเชิงพาณิชย์แบบตั้งพื้นสำหรับน้ำดื่มโดยตรง", "app": "สำนักงาน ร้านอาหาร โรงเรียน คาเฟ่ โรงงานขนาดเล็ก และโครงการผู้จัดจำหน่าย", "oem": "โลโก้ แผงหน้า ฉลาก ลำดับไส้กรอง ตัวเลือกถัง บรรจุภัณฑ์ และคู่มือ", "moq": "ยืนยันตามสเปกและระดับการทำแบรนด์", "body": "ออกแบบสำหรับผู้จัดจำหน่ายและแบรนด์ B2B รองรับกำลังผลิต 800G, 1200G, 1600G และ 2000G การกรอง RO 5 ขั้นตอน กำลังไฟ 160W น้ำหนัก 28 kg และเลือกได้ทั้งแบบไม่มีถังหรือมีถังแรงดัน", "card": "เครื่อง RO เชิงพาณิชย์สำหรับน้ำดื่มโดยตรง 800G-2000G พร้อมการกรอง 5 ขั้นตอนและรองรับ OEM/ODM"},
    "tk": {"home": "Baş sahypa", "products": "Önümler", "specs": "Tehniki aýratynlyklar", "options": "Konfigurasiýa görnüşleri", "related": "Degişli önümler", "request": "OEM baha soramak", "send": "Sorag iber", "item": "Bölüm", "spec": "Spesifikasiýa", "quality": "Hil resminamalary", "labels": ["Önüm görnüşi", "Kuwwat", "Süzgüç tapgyrlary", "Basyş baky", "Nominal kuwwat", "Önümiň agramy", "Ölçegler", "Gurnama", "Ulanylyş", "OEM/ODM", "MOQ"], "stage": "PP sediment, başlangyç karbon, RO membrana we sargy boýunça soňky karbon bilen bäş tapgyrly RO süzgüç", "tank": "Standart baksyz; müşderiniň talaby boýunça basyş baky goşulyp bilner", "frame": "Agaç rama 47 x 33 x 90 cm", "install": "Göni içimlik suw üçin ýerde goýulýan täjirçilik gurnamasy", "app": "Ofisler, restoranlar, mekdepler, kafeler, kiçi zawodlar we distribýutor taslamalary", "oem": "Logo, panel, etiketka, süzgüç yzygiderligi, bak görnüşi, gaplama we gollanma", "moq": "Spesifikasiýa we brend derejesi boýunça tassyklanýar", "body": "B2B distribýutorlary we markalary üçin niýetlenen; 800G, 1200G, 1600G we 2000G kuwwatlary, bäş tapgyrly RO süzgüç, 160W güýç, 28 kg agram we baksyz ýa-da basyş bakly konfigurasiýa goldaw berýär.", "card": "800G-2000G täjirçilik RO göni içimlik suw enjamy, bäş tapgyrly süzgüç we OEM/ODM goldawy."},
    "tl": {"home": "Pangunahing pahina", "products": "Mga Produkto", "specs": "Teknikal na espesipikasyon", "options": "Mga pagpipilian sa pagsasaayos", "related": "Kaugnay na produkto", "request": "Humiling ng presyong OEM", "send": "Ipadala ang tanong", "item": "Aytem", "spec": "Espesipikasyon", "quality": "Mga dokumento ng kalidad", "labels": ["Uri ng produkto", "Kapasidad", "Mga yugto ng pagsasala", "Tangke ng presyon", "Nakatakdang lakas", "Bigat ng produkto", "Sukat", "Pag-install", "Gamit", "OEM/ODM", "MOQ"], "stage": "Limang yugto ng pagsasala ng RO na may PP sediment, paunang karbon, RO membrane at panghuling karbon ayon sa order", "tank": "Karaniwang walang tangke; maaaring magdagdag ng tangke ng presyon ayon sa kailangan ng customer", "frame": "Kahoy na frame 47 x 33 x 90 cm", "install": "Nakatayong komersyal na pag-install para sa direktang inuming tubig", "app": "Opisina, restawran, paaralan, kapihan, maliit na pabrika at proyekto ng distributor", "oem": "Logo, panel, etiketa, pagkakasunod ng filter, opsyon ng tangke, pakete at manwal", "moq": "Kukumpirmahin ayon sa espesipikasyon at antas ng pagba-brand", "body": "Ginawa para sa mga distributor at brand na B2B, sumusuporta sa kapasidad na 800G, 1200G, 1600G at 2000G, limang yugto ng pagsasala ng RO, lakas na 160W, bigat na 28 kg at pagsasaayos na walang tangke o may tangke ng presyon.", "card": "Komersyal na RO machine para sa direktang inuming tubig na may 800G-2000G na opsyon, limang yugto ng pagsasala at suporta sa OEM/ODM."},
    "tr": {"home": "Ana sayfa", "products": "Ürünler", "specs": "Teknik özellikler", "options": "Konfigürasyon seçenekleri", "related": "İlgili ürünler", "request": "OEM teklifi isteyin", "send": "Sorgu gönder", "item": "Kalem", "spec": "Özellik", "quality": "Kalite belgeleri", "labels": ["Ürün tipi", "Kapasite", "Filtrasyon aşamaları", "Basınç tankı", "Nominal güç", "Ürün ağırlığı", "Ölçüler", "Kurulum", "Uygulama", "OEM/ODM", "MOQ"], "stage": "PP sediment, ön karbon, RO membran ve siparişe göre son karbon ile beş aşamalı RO filtrasyon", "tank": "Standart olarak tanksızdır; müşteri ihtiyacına göre basınç tankı eklenebilir", "frame": "Ahşap çerçeve 47 x 33 x 90 cm", "install": "Doğrudan içme suyu için yere kurulan ticari sistem", "app": "Ofisler, restoranlar, okullar, kafeler, küçük işletmeler ve distribütör projeleri", "oem": "Logo, panel, etiket, filtre sıralaması, tank seçeneği, ambalaj ve kılavuz", "moq": "Spesifikasyon ve marka seviyesine göre onaylanır", "body": "B2B distribütörler ve markalar için tasarlanmıştır; 800G, 1200G, 1600G ve 2000G kapasite, beş aşamalı RO filtrasyon, 160W güç, 28 kg ağırlık ve tanksız ya da basınç tanklı konfigürasyon sunar.", "card": "800G-2000G ticari doğrudan içme suyu RO makinesi, beş aşamalı filtrasyon ve OEM/ODM desteği."},
    "uk": {"home": "Головна", "products": "Продукція", "specs": "Технічні характеристики", "options": "Варіанти конфігурації", "related": "Схожі продукти", "request": "Запит OEM-ціни", "send": "Надіслати запит", "item": "Параметр", "spec": "Специфікація", "quality": "Документи якості", "labels": ["Тип продукту", "Продуктивність", "Ступені фільтрації", "Бак під тиском", "Номінальна потужність", "Вага продукту", "Розміри", "Встановлення", "Застосування", "OEM/ODM", "MOQ"], "stage": "П'ятиступенева RO фільтрація з PP осадовим фільтром, попереднім вугіллям, RO мембраною та пост-вугіллям за замовленням", "tank": "Стандартно без бака; бак під тиском може бути доданий за вимогою клієнта", "frame": "Дерев'яна рама 47 x 33 x 90 cm", "install": "Підлогове комерційне встановлення для прямої питної води", "app": "Офіси, ресторани, школи, кафе, малі виробництва та проекти дистриб'юторів", "oem": "Логотип, панель, етикетка, послідовність фільтрів, варіант бака, пакування та інструкція", "moq": "Підтверджується за специфікацією та рівнем брендування", "body": "Для B2B дистриб'юторів і брендів, підтримує 800G, 1200G, 1600G і 2000G, п'ятиступеневу RO фільтрацію, потужність 160W, вагу 28 kg і конфігурацію без бака або з баком під тиском.", "card": "Комерційна RO машина для прямої питної води з опціями 800G-2000G, п'ятиступеневою фільтрацією та підтримкою OEM/ODM."},
    "ur": {"home": "ہوم", "products": "مصنوعات", "specs": "تکنیکی وضاحتیں", "options": "کنفیگریشن کے اختیارات", "related": "متعلقہ مصنوعات", "request": "OEM کوٹیشن طلب کریں", "send": "انکوائری بھیجیں", "item": "آئٹم", "spec": "وضاحت", "quality": "معیار کی دستاویزات", "labels": ["مصنوعات کی قسم", "صلاحیت", "فلٹریشن مراحل", "پریشر ٹینک", "ریٹڈ پاور", "مصنوعات کا وزن", "ابعاد", "تنصیب", "استعمال", "OEM/ODM", "MOQ"], "stage": "PP sediment، pre-carbon، RO membrane اور آرڈر کے مطابق post-carbon کے ساتھ پانچ مرحلوں والی RO فلٹریشن", "tank": "معیاری طور پر بغیر ٹینک؛ کسٹمر کی ضرورت کے مطابق پریشر ٹینک شامل کیا جا سکتا ہے", "frame": "لکڑی کا فریم 47 x 33 x 90 cm", "install": "براہ راست پینے کے پانی کے لیے فرش پر نصب کمرشل تنصیب", "app": "دفاتر، ریستوران، اسکول، کیفے، چھوٹے کارخانے اور ڈسٹری بیوٹر پروجیکٹس", "oem": "لوگو، پینل، لیبل، فلٹر ترتیب، ٹینک آپشن، پیکیجنگ اور دستی", "moq": "تفصیلات اور برانڈنگ کی سطح کے مطابق تصدیق", "body": "B2B ڈسٹری بیوٹرز اور برانڈز کے لیے تیار، 800G، 1200G، 1600G اور 2000G صلاحیت، پانچ مرحلوں والی RO فلٹریشن، 160W پاور، 28 kg وزن اور بغیر ٹینک یا پریشر ٹینک کنفیگریشن کی حمایت کرتا ہے۔", "card": "800G-2000G کمرشل RO براہ راست پینے کے پانی کی مشین، پانچ مرحلوں کی فلٹریشن اور OEM/ODM سپورٹ۔"},
    "zu": {"home": "Ikhaya", "products": "Imikhiqizo", "specs": "Imininingwane yobuchwepheshe", "options": "Izinketho zokuhlelwa", "related": "Imikhiqizo ehlobene", "request": "Cela ikhotheshini ye-OEM", "send": "Thumela umbuzo", "item": "Into", "spec": "Imininingwane", "quality": "Amadokhumenti ekhwalithi", "labels": ["Uhlobo lomkhiqizo", "Umthamo", "Izigaba zokuhlunga", "Ithangi lengcindezi", "Amandla alinganisiwe", "Isisindo somkhiqizo", "Ubukhulu", "Ukufakwa", "Ukusetshenziswa", "OEM/ODM", "MOQ"], "stage": "Ukuhlunga kwe-RO kwezigaba ezinhlanu nge-PP sediment, ikhabhoni yokuqala, i-RO membrane nekhabhoni yokugcina ngokwe-oda", "tank": "Okuvamile akunathangi; ithangi lengcindezi lingangezwa ngokwesidingo sekhasimende", "frame": "Uhlaka lokhuni 47 x 33 x 90 cm", "install": "Ukufakwa kwezentengiselwano okumile phansi kwamanzi okuphuza aqondile", "app": "Amahhovisi, izindawo zokudlela, izikole, amakhofi, amafekthri amancane namaphrojekthi abasabalalisi", "oem": "Ilogo, iphaneli, ilebula, ukuhleleka kwefilter, inketho yethangi, ukupakisha nencwadi", "moq": "Kuqinisekiswa ngokwespecification nezinga le-branding", "body": "Yenzelwe abasabalalisi be-B2B namabrendi, isekela 800G, 1200G, 1600G no-2000G, ukuhlunga kwe-RO kwezigaba ezinhlanu, amandla 160W, isisindo 28 kg nokuhlelwa okungenathangi noma okunethangi lengcindezi.", "card": "Umshini we-RO wezentengiselwano wamanzi okuphuza aqondile, 800G-2000G, ukuhlunga kwezigaba ezinhlanu nokusekelwa kwe-OEM/ODM."},
}

RELATED_TITLES = {
    "ha": {
        "product-built-in-pressure-tank-ro.html": "Na'urar tace ruwan RO mai tankin matsa lamba 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Na'urar RO mai matakai 5/6/7 bisa bukatar abokin ciniki",
        "product-ro-seawater-desalination-machine.html": "Na'urar RO ta cire gishirin ruwan teku",
    },
    "hi": {
        "product-built-in-pressure-tank-ro.html": "बिल्ट-इन प्रेशर टैंक RO वाटर प्यूरीफायर 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "कस्टम 5/6/7 स्टेज RO वाटर प्यूरीफायर",
        "product-ro-seawater-desalination-machine.html": "RO समुद्री जल विलवणीकरण उपकरण",
    },
    "ta": {
        "product-built-in-pressure-tank-ro.html": "உள்ளமைந்த அழுத்தத் தொட்டி RO நீர் சுத்திகரிப்பு இயந்திரம் 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "தனிப்பயன் 5/6/7 நிலை RO நீர் சுத்திகரிப்பு இயந்திரம்",
        "product-ro-seawater-desalination-machine.html": "RO கடல் நீர் உப்பு நீக்கம் சாதனம்",
    },
    "ur": {
        "product-built-in-pressure-tank-ro.html": "بلٹ اِن پریشر ٹینک RO واٹر پیوریفائر 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "کسٹم 5/6/7 مرحلوں والا RO واٹر پیوریفائر",
        "product-ro-seawater-desalination-machine.html": "RO سمندری پانی ڈی سیلینیشن مشین",
    },
    "zu": {
        "product-built-in-pressure-tank-ro.html": "Isihlanzi samanzi se-RO esinethangi lengcindezi 100G/200G",
        "product-custom-5-6-7-stage-ro-water-purifier.html": "Isihlanzi samanzi se-RO sezinyathelo 5/6/7 ngokwezifiso",
        "product-ro-seawater-desalination-machine.html": "Imishini ye-RO yokususa usawoti emanzini olwandle",
    },
}


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def dirs() -> list[str]:
    return sorted(p.name for p in ROOT.iterdir() if p.is_dir() and (p / "index.html").exists())


def localized_ui(lang: str, name: str) -> dict:
    ui = UI["en"].copy()
    ui.update(UI.get(lang, {}))
    if lang in LOCAL_TERMS:
        t = LOCAL_TERMS[lang]
        ui.update({
            "home": t["home"],
            "products": t["products"],
            "category": name,
            "specs": t["specs"],
            "spec_h": f"{name} · {t['specs']}",
            "options": t["options"],
            "options_h": f"{name} · {t['options']}",
            "faq": "FAQ",
            "faq_h": f"{name} · FAQ",
            "related": t["related"],
            "quote": f"{t['request']}: {name}",
            "quote_desc": t["body"],
            "request": t["request"],
            "send": t["send"],
            "item": t["item"],
            "spec": t["spec"],
            "labels": t["labels"],
        })
    ui["quality_label"] = QUALITY_LABELS.get(lang, LOCAL_TERMS.get(lang, {}).get("quality", "Quality documents"))
    return ui


def copy_for(lang: str) -> dict:
    name = LANG_NAMES.get(lang, LANG_NAMES["en"])
    ui = localized_ui(lang, name)
    if lang in PRIORITY_COPY:
        intro = PRIORITY_COPY[lang]["intro"].format(name=name)
        card = PRIORITY_COPY[lang]["card"].format(name=name)
        quality = PRIORITY_COPY[lang]["quality"]
        faq_pairs = PRIORITY_COPY[lang]["q"]
        cta = PRIORITY_COPY[lang]["cta"]
        ui["request"] = cta.get("Request OEM Quote", ui["request"])
        ui["send"] = cta.get("Send Inquiry", ui["send"])
    elif lang in LOCAL_TERMS:
        t = LOCAL_TERMS[lang]
        intro = f"{name}. {t['body']}"
        card = f"{name}. {t['card']}"
        quality = THIRD_COPY.get(lang, {}).get("cert_tail", t["quality"])
        values = spec_values(lang)
        faq_pairs = [
            (t["labels"][1], values[1]),
            (t["labels"][3], values[3]),
            (t["labels"][9], values[9]),
        ]
    elif lang in THIRD_COPY:
        t = THIRD_COPY[lang]
        intro = f"{name} — {t['cat_a2']} {t['cat_a1']}"
        card = f"{name} — {t['cat_a2']} {t['quality_plain']}."
        quality = t["cert_tail"]
        faq_pairs = [
            (t["cat_q2"], t["cat_a2"]),
            (t["cat_q1"], t["cat_a1"]),
            (t["cat_q3"], t["cert_tail"]),
        ]
    else:
        intro = (
            f"{name} is supplied by Yuchen Water for B2B distributors, importers and OEM/ODM brands. "
            "The unit supports 800G, 1200G, 1600G and 2000G capacity options, five-stage filtration, tankless supply or optional pressure tank configuration, private-label appearance and export packaging."
        )
        card = (
            f"{name} for commercial direct drinking water projects, with 800G-2000G options, five-stage filtration, optional pressure tank and OEM/ODM branding support."
        )
        quality = "Selected products can be supplied or tested according to NSF/ANSI 42, 53 and 58 requirements. ISO 9001, CE, SGS and Halal-related documents are available upon request."
        faq_pairs = [
            ("Can this machine be supplied as 800G, 1200G, 1600G or 2000G?", "Yes. Capacity is confirmed according to membrane selection, inlet water quality, pump configuration and target application."),
            ("Can it be supplied without a pressure tank?", "Yes. Tankless configuration is standard for many commercial direct drinking water projects, and an optional pressure tank can be added if the buyer requires storage."),
            ("What OEM/ODM information should be sent?", "Please send capacity, quantity, logo, panel language, pressure tank choice, packaging needs and destination port."),
        ]
    title = f"{name} | Yuchen Water OEM"
    meta = re.sub(r"\s+", " ", intro).strip()
    if len(meta) > 260:
        meta = meta[:257].rsplit(" ", 1)[0] + "..."
    return {
        "name": name,
        "title": title,
        "meta": meta,
        "intro": intro,
        "card": card,
        "quality": quality,
        "faq_pairs": faq_pairs,
        **ui,
    }


def spec_values(lang: str) -> list[str]:
    if lang in LOCAL_TERMS:
        t = LOCAL_TERMS[lang]
        return [
            LANG_NAMES.get(lang, LANG_NAMES["en"]),
            "800G / 1200G / 1600G / 2000G",
            t["stage"],
            t["tank"],
            "160W", "28 kg", t["frame"],
            t["install"],
            t["app"],
            t["oem"],
            t["moq"],
        ]
    if lang == "ru":
        return [
            "20-дюймовая коммерческая система обратного осмоса для чистой питьевой воды",
            "800G / 1200G / 1600G / 2000G",
            "Пять ступеней: PP осадочный фильтр, предварительный уголь, RO мембрана, постугольный или дополнительный картридж по заказу",
            "Стандартно без бака; напорный бак может быть добавлен по требованию клиента",
            "160W", "28 kg", "Деревянная рама 47 x 33 x 90 cm",
            "Напольная коммерческая установка для прямого питьевого водоснабжения",
            "Офисы, рестораны, школы, кафе, небольшие производства и проекты дистрибьюторов",
            "Логотип, панель, этикетки, последовательность фильтров, вариант бака, упаковка и инструкция",
            "Подтверждается по спецификации и уровню брендирования",
        ]
    if lang == "es":
        return [
            "Sistema comercial de ósmosis inversa de 20 pulgadas para agua potable directa",
            "800G / 1200G / 1600G / 2000G",
            "Cinco etapas: PP sedimentos, carbón previo, membrana RO, post-carbón o cartucho adicional según pedido",
            "Sin tanque como estándar; se puede añadir tanque de presión si el cliente lo requiere",
            "160W", "28 kg", "Estructura de madera 47 x 33 x 90 cm",
            "Instalación comercial de pie para suministro directo de agua potable",
            "Oficinas, restaurantes, escuelas, cafeterías, pequeñas fábricas y proyectos de distribuidores",
            "Logo, panel, etiquetas, secuencia de filtros, opción de tanque, embalaje y manual",
            "Se confirma según especificación y nivel de marca",
        ]
    if lang == "de":
        return [
            "20-Zoll kommerzielle Umkehrosmoseanlage für direktes Trinkwasser",
            "800G / 1200G / 1600G / 2000G",
            "Fünf Stufen: PP-Sediment, Voraktivkohle, RO-Membran, Nachkohle oder Zusatzkartusche nach Auftrag",
            "Standardmäßig tanklos; Drucktank kann auf Kundenwunsch ergänzt werden",
            "160W", "28 kg", "Holzrahmen 47 x 33 x 90 cm",
            "Freistehende kommerzielle Installation für direktes Trinkwasser",
            "Büros, Restaurants, Schulen, Cafés, kleine Betriebe und Distributionsprojekte",
            "Logo, Frontpanel, Etiketten, Filterfolge, Tankoption, Verpackung und Anleitung",
            "Nach Spezifikation und Branding-Anforderungen zu bestätigen",
        ]
    if lang == "fr":
        return [
            "Système commercial d'osmose inverse 20 pouces pour eau potable directe",
            "800G / 1200G / 1600G / 2000G",
            "Cinq étapes : PP sédiments, charbon amont, membrane RO, post-charbon ou cartouche supplémentaire selon commande",
            "Sans réservoir en standard; réservoir sous pression possible selon demande client",
            "160W", "28 kg", "Châssis bois 47 x 33 x 90 cm",
            "Installation commerciale au sol pour eau potable directe",
            "Bureaux, restaurants, écoles, cafés, petites usines et projets de distributeurs",
            "Logo, panneau, étiquettes, séquence de filtres, option réservoir, emballage et manuel",
            "À confirmer selon la spécification et le niveau de marquage",
        ]
    if lang == "vi":
        return [
            "Hệ thống thẩm thấu ngược thương mại 20 inch cho nước uống trực tiếp",
            "800G / 1200G / 1600G / 2000G",
            "Năm cấp lọc: PP cặn bẩn, than hoạt tính trước, màng RO, than sau hoặc lõi bổ sung theo đơn hàng",
            "Tiêu chuẩn không bình áp; có thể thêm bình áp theo yêu cầu khách hàng",
            "160W", "28 kg", "Khung gỗ 47 x 33 x 90 cm",
            "Lắp đặt dạng đứng cho cấp nước uống trực tiếp thương mại",
            "Văn phòng, nhà hàng, trường học, quán cà phê, xưởng nhỏ và dự án nhà phân phối",
            "Logo, mặt panel, nhãn, thứ tự lõi lọc, lựa chọn bình áp, bao bì và hướng dẫn",
            "Xác nhận theo thông số và mức độ thương hiệu",
        ]
    if lang == "ja":
        return [
            "20インチ業務用逆浸透膜システム、直飲用純水向け",
            "800G / 1200G / 1600G / 2000G",
            "5段ろ過：PP沈殿、前処理カーボン、RO膜、後置カーボンまたは追加カートリッジを注文仕様で設定",
            "標準はタンクレス。必要に応じて圧力タンクを追加可能",
            "160W", "28 kg", "木枠寸法 47 x 33 x 90 cm",
            "直飲水供給向けの床置き業務用設置",
            "オフィス、飲食店、学校、カフェ、小規模工場、販売代理店プロジェクト",
            "ロゴ、パネル、ラベル、フィルター順序、タンク有無、梱包、説明書",
            "仕様とブランド要求により確認",
        ]
    if lang == "uz":
        return [
            "20 dyuymli tijorat teskari osmos tizimi, toza ichimlik suvi uchun",
            "800G / 1200G / 1600G / 2000G",
            "Besh bosqich: PP cho‘kindi filtri, old karbon, RO membrana, post-karbon yoki buyurtma bo‘yicha qo‘shimcha kartrij",
            "Standart baksiz; mijoz talab qilsa bosim baki qo‘shilishi mumkin",
            "160W", "28 kg", "Yog‘och ramka 47 x 33 x 90 cm",
            "Tijorat to‘g‘ridan-to‘g‘ri ichimlik suvi uchun polga o‘rnatish",
            "Ofis, restoran, maktab, kafe, kichik zavod va distribyutor loyihalari",
            "Logo, panel, yorliq, filtr ketma-ketligi, bak varianti, qadoqlash va qo‘llanma",
            "Spetsifikatsiya va brendlash darajasiga qarab tasdiqlanadi",
        ]
    if lang == "kk":
        return [
            "20 дюймдік коммерциялық кері осмос жүйесі, тікелей ішетін таза суға арналған",
            "800G / 1200G / 1600G / 2000G",
            "Бес саты: PP тұнба сүзгісі, алдынғы көмір, RO мембранасы, кейінгі көмір немесе тапсырыс бойынша қосымша картридж",
            "Стандартты түрде баксыз; клиент қажет етсе қысым багы қосылады",
            "160W", "28 kg", "Ағаш қаңқа 47 x 33 x 90 cm",
            "Коммерциялық тікелей ауыз су үшін еденге орнату",
            "Офистер, мейрамханалар, мектептер, кафелер, шағын зауыттар және дистрибьютор жобалары",
            "Логотип, панель, жапсырмалар, сүзгі реті, бак нұсқасы, қаптама және нұсқаулық",
            "Сипаттама мен брендтеу деңгейіне қарай расталады",
        ]
    if lang == "ky":
        return [
            "20 дюймдук коммерциялык тескери осмос системасы, түз ичүүчү таза суу үчүн",
            "800G / 1200G / 1600G / 2000G",
            "Беш баскыч: PP чөкмө чыпкасы, алдынкы көмүр, RO мембрана, кийинки көмүр же буйрутма боюнча кошумча картридж",
            "Стандартта баксыз; кардар талап кылса басым багы кошулат",
            "160W", "28 kg", "Жыгач рама 47 x 33 x 90 cm",
            "Коммерциялык түз ичүүчү суу үчүн полго орнотуу",
            "Офистер, ресторандар, мектептер, кафелер, чакан өндүрүштөр жана дистрибьютор долбоорлору",
            "Логотип, панель, этикетка, чыпка тартиби, бак варианты, таңгак жана колдонмо",
            "Спецификация жана бренддөө деңгээли боюнча такталат",
        ]
    return [
        "20-inch commercial reverse osmosis direct drinking water purifier",
        "800G / 1200G / 1600G / 2000G",
        "Five-stage filtration with PP sediment, pre-carbon, RO membrane, post carbon or custom cartridge sequence",
        "Tankless as standard; optional pressure tank can be configured according to customer requirements",
        "160W", "28 kg", "Wooden frame 47 x 33 x 90 cm",
        "Floor-standing commercial direct drinking water installation",
        "Offices, restaurants, schools, cafés, small factories and distributor projects",
        "Logo, panel, label, filter sequence, pressure tank option, packaging and manual",
        "Confirm by specification and branding level",
    ]


def product_graph(lang: str, c: dict) -> str:
    img_urls = [f"https://www.yuchensy.com/assets/products/{name}" for name, _, _, _ in IMAGES]
    faq_entities = [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
        for q, a in c["faq_pairs"]
    ]
    labels = c["labels"]
    values = spec_values(lang)
    props = [{"@type": "PropertyValue", "name": labels[i], "value": values[i]} for i in range(len(labels))]
    graph = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@context": "https://schema.org",
                "@type": "Organization",
                "@id": "https://www.yuchensy.com/#organization",
                "name": "Yuchen Water",
                "url": "https://www.yuchensy.com/",
                "logo": "https://www.yuchensy.com/assets/logo.png",
                "telephone": "+86-19908311885",
                "email": "expresswater025@gmail.com",
                "address": {
                    "@type": "PostalAddress",
                    "streetAddress": "Yuanhua Town",
                    "addressLocality": "Haining City",
                    "addressRegion": "Zhejiang Province",
                    "addressCountry": "CN",
                },
            },
            {"@context": "https://schema.org", "@type": "WebSite", "@id": "https://www.yuchensy.com/#website", "name": "Yuchen Water", "url": "https://www.yuchensy.com/", "publisher": {"@id": "https://www.yuchensy.com/#organization"}, "inLanguage": lang},
            {
                "@context": "https://schema.org",
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": c["home"], "item": f"https://www.yuchensy.com/{lang}/index.html"},
                    {"@type": "ListItem", "position": 2, "name": c["products"], "item": f"https://www.yuchensy.com/{lang}/products.html"},
                    {"@type": "ListItem", "position": 3, "name": c["name"], "item": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}"},
                ],
            },
            {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_entities},
            {
                "@context": "https://schema.org",
                "@type": "Product",
                "@id": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}#product",
                "name": c["name"],
                "description": c["intro"],
                "image": img_urls,
                "brand": {"@type": "Brand", "name": "Yuchen Water"},
                "manufacturer": {"@id": "https://www.yuchensy.com/#organization"},
                "category": c["category"],
                "additionalProperty": props,
                "offers": {
                    "@type": "Offer",
                    "priceCurrency": "USD",
                    "availability": "https://schema.org/InStock",
                    "url": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}",
                    "priceValidUntil": "2027-12-31",
                },
            },
        ],
    }
    return json.dumps(graph, ensure_ascii=False, separators=(",", ":"))


def page_h1(lang: str, href: str, fallback: str) -> str:
    if lang in RELATED_TITLES and href in RELATED_TITLES[lang]:
        return RELATED_TITLES[lang][href]
    path = ROOT / lang / href
    if not path.exists():
        return fallback
    text = path.read_text(encoding="utf-8", errors="ignore")
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, flags=re.S)
    if not match:
        return fallback
    title = re.sub(r"<.*?>", "", match.group(1)).strip()
    return title or fallback


def build_main(lang: str, c: dict) -> str:
    labels = c["labels"]
    values = spec_values(lang)
    rows = "\n".join(f"      <tr><th>{esc(labels[i])}</th><td>{esc(values[i])}</td></tr>" for i in range(len(labels)))
    gallery = "\n".join(
        f'        <a href="../assets/products/{img}"><img src="../assets/products/{img}" alt="{esc(c["name"] + " - " + view)}" loading="lazy" decoding="async" width="{w}" height="{h}" /></a>'
        for img, w, h, view in IMAGES[1:]
    )
    faq = "\n".join(
        f'      <div class="faq-item"><button class="faq-q">{esc(q)}</button><div class="faq-a"><p>{esc(a)}</p></div></div>'
        for q, a in c["faq_pairs"]
    )
    related = [
        ("product-built-in-pressure-tank-ro.html", page_h1(lang, "product-built-in-pressure-tank-ro.html", "Built-In Pressure Tank RO Water Purifier 100G/200G"), "built-in-pressure-tank-ro-water-purifier-100g-200g-oem.webp", "RO Water Purifier"),
        ("product-custom-5-6-7-stage-ro-water-purifier.html", page_h1(lang, "product-custom-5-6-7-stage-ro-water-purifier.html", "Custom 5/6/7 Stage RO Water Purifier"), "custom-5-6-7-stage-ro-water-purifier-orange-bracket-single-gauge-oem.jpg", "RO Water Purifier"),
        ("product-ro-seawater-desalination-machine.html", page_h1(lang, "product-ro-seawater-desalination-machine.html", "RO Seawater Desalination Equipment"), "ro-seawater-desalination-equipment-complete-system-oem.jpg", "RO System"),
    ]
    related_html = "\n".join(
        f'''      <article class="product-card" data-cat="{esc(cat)}">
        <a href="{href}" class="product-img-wrap">
          <span class="product-cat-badge">{esc(cat)}</span>
          <img src="../assets/products/{img}" alt="{esc(title)}" loading="lazy" decoding="async" width="640" height="480" />
        </a>
        <div class="product-body">
          <h3>{esc(title)}</h3>
          <p>{esc(c["card"])}</p>
          <a href="{href}" class="product-link">{esc(c["send"])}</a>
        </div>
      </article>'''
        for href, title, img, cat in related
    )
    return f'''<main>
<section class="section section-cream product-hero">
  <div class="container product-detail">
    <div class="product-detail-img">
      <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="eager" fetchpriority="high" decoding="async" width="1024" height="1024" class="product-main-image" />
      <div class="product-gallery">
{gallery}
      </div>
    </div>
    <div class="product-detail-info">
      <nav class="breadcrumb"><a href="index.html">{esc(c["home"])}</a><span>·</span><a href="products.html">{esc(c["products"])}</a><span>·</span><span>{esc(c["name"])}</span></nav>
      <h1>{esc(c["name"])}</h1>
      <span class="cat-badge">{esc(c["category"])}</span>
      <p class="desc">{esc(c["intro"])}</p>
      <div class="product-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%2020-inch%20Commercial%20RO%20Water%20Purifier%20800G%202000G" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
    </div>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["specs"])}</span><h2>{esc(c["spec_h"])}</h2></div>
    <table class="spec-table">
      <tr><th>{esc(c["item"])}</th><td>{esc(c["spec"])}</td></tr>
{rows}
    </table>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["options"])}</span><h2>{esc(c["options_h"])}</h2></div>
    <table class="spec-table">
      <tr><th>800G-2000G</th><td>{esc(values[1])}</td></tr>
      <tr><th>{esc(labels[3])}</th><td>{esc(values[3])}</td></tr>
      <tr><th>{esc(labels[9])}</th><td>{esc(values[9])}</td></tr>
      <tr><th>{esc(labels[10])}</th><td>{esc(values[10])}</td></tr>
      <tr><th>{esc(c["quality_label"])}</th><td>{esc(c["quality"])}</td></tr>
    </table>
  </div>
</section>
<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["faq"])}</span><h2>{esc(c["faq_h"])}</h2></div>
    <div class="faq-wrap">
{faq}
    </div>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">{esc(c["related"])}</span><h2>{esc(c["related"])}</h2></div>
    <div class="product-grid">
{related_html}
    </div>
  </div>
</section>
<section class="section section-dark quote-strip">
  <div class="container">
    <h2>{esc(c["quote"])}</h2>
    <p>{esc(c["quote_desc"])}</p>
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">{esc(c["request"])}</a><a href="https://wa.me/8619908311885?text=Inquiry%20about%2020-inch%20Commercial%20RO%20Water%20Purifier%20800G%202000G" class="btn" target="_blank" rel="noopener">{esc(c["whatsapp"])}</a></div>
  </div>
</section>
</main>'''


def update_head(text: str, lang: str, c: dict) -> str:
    direction = "rtl" if lang in RTL_LANGS else "ltr"
    text = text.replace(OLD_SLUG, NEW_SLUG)
    text = re.sub(r'<html lang="[^"]+" dir="[^"]+">', f'<html lang="{lang}" dir="{direction}">', text, count=1)
    text = re.sub(r'<title>.*?</title>', f'<title>{esc(c["title"])}</title>', text, count=1, flags=re.S)
    text = re.sub(r'<meta name="description" content="[^"]*" />', f'<meta name="description" content="{esc(c["meta"])}" />', text, count=1)
    text = re.sub(r'<link rel="canonical" href="[^"]+" />', f'<link rel="canonical" href="https://www.yuchensy.com/{lang}/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<link rel="alternate" hreflang="x-default" href="[^"]+" />', f'<link rel="alternate" hreflang="x-default" href="https://www.yuchensy.com/en/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<link rel="preload" as="image" href="[^"]+" fetchpriority="high" />', f'<link rel="preload" as="image" href="../assets/products/{MAIN_IMAGE}" fetchpriority="high" />', text, count=1)
    text = re.sub(r'<meta property="og:title" content="[^"]*" />', f'<meta property="og:title" content="{esc(c["title"])}" />', text, count=1)
    text = re.sub(r'<meta property="og:description" content="[^"]*" />', f'<meta property="og:description" content="{esc(c["meta"])}" />', text, count=1)
    text = re.sub(r'<meta property="og:url" content="[^"]*" />', f'<meta property="og:url" content="https://www.yuchensy.com/{lang}/{NEW_SLUG}" />', text, count=1)
    text = re.sub(r'<meta property="og:image" content="[^"]*" />', f'<meta property="og:image" content="https://www.yuchensy.com/assets/products/{MAIN_IMAGE}" />', text, count=1)
    text = re.sub(r'<script type="application/ld\+json">.*?</script>', f'<script type="application/ld+json">{product_graph(lang, c)}</script>', text, count=1, flags=re.S)
    return text


def make_page(lang: str) -> None:
    template = (ROOT / lang / OLD_SLUG).read_text(encoding="utf-8")
    c = copy_for(lang)
    text = update_head(template, lang, c)
    text = re.sub(r'<main>.*?</main>', build_main(lang, c), text, count=1, flags=re.S)
    (ROOT / lang / NEW_SLUG).write_text(text, encoding="utf-8")


def product_card(lang: str) -> str:
    c = copy_for(lang)
    return f'''<article class="product-card" data-cat="RO System">
  <a href="{NEW_SLUG}" class="product-img-wrap">
    <span class="product-cat-badge">{esc(c["category"])}</span>
    <img src="../assets/products/{MAIN_IMAGE}" alt="{esc(c["name"])}" loading="lazy" decoding="async" width="1024" height="1024" />
  </a>
  <div class="product-body">
    <h3>{esc(c["name"])}</h3>
    <p>{esc(c["card"])}</p>
    <a href="{NEW_SLUG}" class="product-link">{esc(c["send"])}</a>
  </div>
</article>
'''


def update_item_list_json(text: str, lang: str) -> str:
    scripts = list(re.finditer(r'<script type="application/ld\+json">(.*?)</script>', text, flags=re.S))
    c = copy_for(lang)
    for m in scripts:
        try:
            data = json.loads(m.group(1))
        except json.JSONDecodeError:
            continue
        graph = data.get("@graph") if isinstance(data, dict) else None
        if not isinstance(graph, list):
            continue
        changed = False
        for node in graph:
            if node.get("@type") == "ItemList":
                elements = node.setdefault("itemListElement", [])
                if any(NEW_SLUG in item.get("url", "") for item in elements if isinstance(item, dict)):
                    return text
                insert_at = 3
                for i, item in enumerate(elements):
                    if OLD_SLUG in item.get("url", ""):
                        insert_at = i + 1
                        break
                elements.insert(insert_at, {
                    "@type": "ListItem",
                    "position": insert_at + 1,
                    "url": f"https://www.yuchensy.com/{lang}/{NEW_SLUG}",
                    "name": c["name"],
                    "description": c["card"],
                })
                for pos, item in enumerate(elements, 1):
                    if isinstance(item, dict):
                        item["position"] = pos
                node["numberOfItems"] = len(elements)
                changed = True
        if changed:
            new_script = f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False, separators=(",", ":"))}</script>'
            return text[:m.start()] + new_script + text[m.end():]
    return text


def update_products_page(lang: str) -> None:
    path = ROOT / lang / "products.html"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG not in text:
        match = re.search(r'(<article class="[^"]*\bproduct-card\b[^"]*"[^>]*>.*?' + re.escape(OLD_SLUG) + r'.*?</article>\s*)', text, flags=re.S)
        if not match:
            raise RuntimeError(f"Could not find insertion point in {path}")
        text = text[:match.end()] + "\n" + product_card(lang) + text[match.end():]
    text = update_item_list_json(text, lang)
    path.write_text(text, encoding="utf-8")


def update_products_json() -> None:
    path = ROOT / "scripts" / "products.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    products = data.setdefault("products", [])
    if not any(item.get("id") == PRODUCT_ID for item in products):
        products.insert(3, {
            "id": PRODUCT_ID,
            "name": LANG_NAMES["en"],
            "category": "RO System",
            "desc": "20-inch commercial RO direct drinking water purifier with 800G, 1200G, 1600G and 2000G capacity options, five-stage filtration, 160W rated power, 28 kg weight and tankless or optional pressure-tank configuration for OEM/ODM projects.",
            "specs": {
                "Product Type": "20-inch commercial reverse osmosis direct drinking water purifier",
                "Capacity": "800G / 1200G / 1600G / 2000G",
                "Filtration Stages": "Five-stage filtration",
                "Pressure Tank": "Tankless standard; optional pressure tank",
                "Rated Power": "160W",
                "Product Weight": "28 kg",
                "Dimensions": "Wooden frame 47 x 33 x 90 cm",
                "OEM/ODM": "Logo, panel, filter sequence, label, packaging and manual",
            },
            "image": f"../assets/products/{MAIN_IMAGE}",
            "image_local": f"assets/products/{MAIN_IMAGE}",
            "image_orig": f"../assets/products/{MAIN_IMAGE}",
            "summary": "This 20-inch commercial RO water purifier is built for offices, restaurants, schools, cafés and distributor direct drinking water projects. It supports 800G, 1200G, 1600G and 2000G output options, five-stage filtration, tankless supply or optional pressure tank configuration, and OEM/ODM branding for global B2B buyers.",
            "features": ["800G/1200G/1600G/2000G capacity options", "Five-stage reverse osmosis filtration", "Tankless or optional pressure-tank configuration", "160W rated power and 28 kg product weight", "OEM/ODM logo, label, panel and export packaging support"],
            "applications": "Commercial direct drinking water, office pantry, restaurant, school, café, small factory and distributor water purifier projects.",
            "related": ["built-in-pressure-tank-ro", "custom-5-6-7-stage-ro-water-purifier", "ro-seawater-desalination-machine"],
        })
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def update_sitemap(langs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    text = path.read_text(encoding="utf-8")
    if NEW_SLUG in text:
        return
    urls = []
    for lang in langs:
        urls.append(
            f"  <url>\n"
            f"    <loc>https://www.yuchensy.com/{lang}/{NEW_SLUG}</loc>\n"
            f"    <lastmod>{TODAY}</lastmod>\n"
            f"    <changefreq>monthly</changefreq>\n"
            f"    <priority>0.8</priority>\n"
            f"  </url>\n"
        )
    text = text.replace("</urlset>", "".join(urls) + "</urlset>")
    path.write_text(text, encoding="utf-8")


def update_ai_files() -> None:
    line = f"- 20-inch Commercial RO Water Purifier 800G/1200G/1600G/2000G: https://www.yuchensy.com/en/{NEW_SLUG}\n"
    for name in ["llms.txt", "llms-full.txt"]:
        path = ROOT / name
        if path.exists():
            text = path.read_text(encoding="utf-8")
            if NEW_SLUG not in text:
                path.write_text(text.rstrip() + "\n" + line, encoding="utf-8")


def main() -> None:
    languages = dirs()
    for lang in languages:
        make_page(lang)
        update_products_page(lang)
    update_products_json()
    update_sitemap(languages)
    update_ai_files()
    print(f"generated_pages={len(languages)}")


if __name__ == "__main__":
    main()
