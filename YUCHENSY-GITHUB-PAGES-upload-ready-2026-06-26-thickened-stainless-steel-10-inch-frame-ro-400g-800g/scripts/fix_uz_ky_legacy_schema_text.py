#!/usr/bin/env python3
"""Localize legacy JSON-LD text left in priority language pages."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from fix_priority_language_mixed_english import COPY, EXTRA, QUALITY_LABEL, ROOT, clean_name, product_name


LANGS = ["ru", "es", "de", "fr", "vi", "ja", "uz", "kk", "ky"]

ORG_COPY = {
    "ru": {
        "industry": "Производитель продукции для фильтрации воды",
        "description": "Yuchen Water — китайский производитель продукции для фильтрации воды, поставляющий PP, CTO, GAC, T33, UF, RO-мембраны, очистители воды, диспенсеры и корпуса фильтров для глобальных B2B покупателей OEM/ODM.",
        "awards": ["27+ лет опыта производства фильтров для воды", "50+ экспортных рынков", "200+ SKU продукции для водоочистки"],
        "home": "Главная",
        "products": "Продукты",
    },
    "es": {
        "industry": "Fabricante de productos de filtración de agua",
        "description": "Yuchen Water es un fabricante chino de productos de filtración de agua que suministra PP, CTO, GAC, T33, UF, membranas RO, purificadores, dispensadores y carcasas de filtro para compradores B2B OEM/ODM globales.",
        "awards": ["27+ años de experiencia en fabricación de filtración de agua", "50+ mercados de exportación", "200+ referencias de productos de filtración de agua"],
        "home": "Inicio",
        "products": "Productos",
    },
    "de": {
        "industry": "Hersteller von Wasserfiltrationsprodukten",
        "description": "Yuchen Water ist ein chinesischer Hersteller von Wasserfiltrationsprodukten und liefert PP, CTO, GAC, T33, UF, RO-Membranen, Wasserreiniger, Wasserspender und Filtergehäuse für globale B2B-OEM/ODM-Käufer.",
        "awards": ["27+ Jahre Erfahrung in der Wasserfiltration", "50+ Exportmärkte", "200+ SKU für Wasserfiltrationsprodukte"],
        "home": "Startseite",
        "products": "Produkte",
    },
    "fr": {
        "industry": "Fabricant de produits de filtration d'eau",
        "description": "Yuchen Water est un fabricant chinois de produits de filtration d'eau fournissant PP, CTO, GAC, T33, UF, membranes RO, purificateurs, distributeurs et boîtiers de filtre pour les acheteurs B2B OEM/ODM mondiaux.",
        "awards": ["27+ ans d'expérience en fabrication de filtration d'eau", "50+ marchés d'exportation", "200+ références de produits de filtration d'eau"],
        "home": "Accueil",
        "products": "Produits",
    },
    "vi": {
        "industry": "Nhà sản xuất sản phẩm lọc nước",
        "description": "Yuchen Water là nhà sản xuất sản phẩm lọc nước tại Trung Quốc, cung cấp PP, CTO, GAC, T33, UF, màng RO, máy lọc nước, cây nước và vỏ lọc cho khách hàng B2B OEM/ODM toàn cầu.",
        "awards": ["27+ năm kinh nghiệm sản xuất lọc nước", "50+ thị trường xuất khẩu", "200+ mã sản phẩm lọc nước"],
        "home": "Trang chủ",
        "products": "Sản phẩm",
    },
    "ja": {
        "industry": "水処理製品メーカー",
        "description": "Yuchen Water は中国の水処理製品メーカーとして、PP、CTO、GAC、T33、UF、RO膜、浄水器、ウォーターディスペンサー、フィルターケースを世界のB2B OEM/ODMバイヤー向けに供給しています。",
        "awards": ["27年以上の水処理製品製造経験", "50以上の輸出市場", "200以上の水処理製品SKU"],
        "home": "ホーム",
        "products": "製品",
    },
    "uz": {
        "industry": "Suv filtrlash mahsulotlari ishlab chiqaruvchisi",
        "description": "Yuchen Water Xitoydagi suv filtrlash mahsulotlari ishlab chiqaruvchisi bo‘lib, global B2B OEM/ODM xaridorlari uchun PP, CTO, GAC, T33, UF, RO membrana, suv tozalagich, dispenser va filtr korpuslarini yetkazib beradi.",
        "awards": ["27+ yillik suv filtrlash ishlab chiqarish tajribasi", "50+ eksport bozori", "200+ turdagi suv filtrlash mahsuloti"],
        "home": "Bosh sahifa",
        "products": "Mahsulotlar",
        "faq": [
            ("{name} OEM buyurtmalari uchun moslashtiriladimi?", "Ha. Yuchen Water mahsulot turiga qarab yorliq, qadoqlash, rang, ulagich, o‘lcham yoki mos filtr to‘plami kabi private-label variantlarini taklif qilishi mumkin."),
            ("Narx olish uchun qanday ma'lumot yuborishim kerak?", "Mahsulot spetsifikatsiyasi, maqsadli miqdor, private-label talablari, boradigan port va bozoringizda kerak bo‘ladigan muvofiqlik hujjatlarini yuboring."),
            ("Qanday sifat hujjatlari taqdim etiladi?", COPY["uz"]["quality"]),
        ],
    },
    "kk": {
        "industry": "Су сүзу өнімдерін өндіруші",
        "description": "Yuchen Water Қытайдағы су сүзу өнімдерін өндіруші болып, жаһандық B2B OEM/ODM сатып алушылары үшін PP, CTO, GAC, T33, UF, RO мембрана, су тазартқыш, диспенсер және сүзгі корпусын жеткізеді.",
        "awards": ["27+ жыл су сүзу өндірісі тәжірибесі", "50+ экспорт нарығы", "200+ су сүзу өнімдерінің ассортименті"],
        "home": "Басты бет",
        "products": "Өнімдер",
        "faq": [
            ("{name} OEM тапсырыстары үшін бейімделе ме?", "Иә. Yuchen Water өнім түріне қарай жапсырма, қаптама, түс, қосқыш, өлшем немесе сәйкес сүзгі жиынтығы сияқты private-label нұсқаларын ұсына алады."),
            ("Баға алу үшін қандай ақпарат жіберу керек?", "Өнім сипаттамасын, мақсатты мөлшерді, private-label талаптарын, жеткізу портын және нарығыңызда қажет сәйкестік құжаттарын жіберіңіз."),
            ("Қандай сапа құжаттары беріледі?", COPY["kk"]["quality"]),
        ],
    },
    "ky": {
        "industry": "Суу чыпкалоо продукциясын өндүрүүчү",
        "description": "Yuchen Water Кытайдагы суу чыпкалоо продукциясын өндүрүүчү болуп, дүйнөлүк B2B OEM/ODM сатып алуучулар үчүн PP, CTO, GAC, T33, UF, RO мембрана, суу тазалагыч, диспенсер жана чыпка корпустарын жеткирет.",
        "awards": ["27+ жыл суу чыпкалоо өндүрүш тажрыйбасы", "50+ экспорт рыногу", "200+ суу чыпкалоо продукциясынын ассортименти"],
        "home": "Башкы бет",
        "products": "Өнүмдөр",
        "faq": [
            ("{name} OEM буйрутмалары үчүн ыңгайлаштырылабы?", "Ооба. Yuchen Water өнүм түрүнө жараша этикетка, таңгак, түс, туташтыргыч, өлчөм же ылайык чыпка топтому сыяктуу private-label варианттарын сунуштай алат."),
            ("Бааны алуу үчүн кандай маалымат жөнөтүшүм керек?", "Өнүм спецификациясын, керектүү санды, private-label талаптарын, жеткирүү портун жана базарыңыз талап кылган шайкештик документтерин жөнөтүңүз."),
            ("Кандай сапат документтери берилет?", COPY["ky"]["quality"]),
        ],
    },
}

PROPERTY_NAME = {
    "uz": {
        "Applications": "Qo‘llanishi",
        "Function": "Vazifasi",
        "Connector": "Ulagich",
        "Material": "Material",
        "Length": "Uzunlik",
        "Connection": "Ulanish",
        "Type": "Turi",
        "Industry": "Sanoat",
        "Size": "O‘lcham",
        "Stages": "Bosqichlar",
        "Sterilization": "Sterilizatsiya",
        "Product Type": "Mahsulot turi",
        "Installation": "O‘rnatish",
        "Filtration": "Filtrlash",
        "Functions": "Funksiyalar",
        "Color": "Rang",
        "Mount": "O‘rnatish",
        "Power": "Quvvat",
        "Position": "Joylashuv",
        "Combination": "Kombinatsiya",
        "Membrane": "Membrana",
        "System Type": "Tizim turi",
        "Cartridge Fit": "Kartrij mosligi",
        "Adds": "Qo‘shimcha minerallar",
        "Quality documents": QUALITY_LABEL["uz"],
    },
    "kk": {
        "Applications": "Қолданылуы",
        "Function": "Функциясы",
        "Connector": "Қосқыш",
        "Material": "Материал",
        "Length": "Ұзындығы",
        "Connection": "Қосылу",
        "Type": "Түрі",
        "Industry": "Өнеркәсіп",
        "Size": "Өлшемі",
        "Stages": "Кезеңдер",
        "Sterilization": "Стерилизация",
        "Product Type": "Өнім түрі",
        "Installation": "Орнату",
        "Filtration": "Сүзу",
        "Functions": "Функциялар",
        "Color": "Түсі",
        "Mount": "Орнату",
        "Power": "Қуаты",
        "Position": "Орналасуы",
        "Combination": "Комбинация",
        "Membrane": "Мембрана",
        "System Type": "Жүйе түрі",
        "Cartridge Fit": "Картридж сәйкестігі",
        "Adds": "Қосымша минералдар",
        "Quality documents": QUALITY_LABEL["kk"],
    },
    "ky": {
        "Applications": "Колдонулушу",
        "Function": "Функциясы",
        "Connector": "Туташтыргыч",
        "Material": "Материал",
        "Length": "Узундук",
        "Connection": "Туташуу",
        "Type": "Түрү",
        "Industry": "Өнөр жай",
        "Size": "Өлчөм",
        "Stages": "Баскычтар",
        "Sterilization": "Стерилизация",
        "Product Type": "Өнүм түрү",
        "Installation": "Орнотуу",
        "Filtration": "Чыпкалоо",
        "Functions": "Функциялар",
        "Color": "Түс",
        "Mount": "Орнотуу",
        "Power": "Кубат",
        "Position": "Орду",
        "Combination": "Комбинация",
        "Membrane": "Мембрана",
        "System Type": "Система түрү",
        "Cartridge Fit": "Картридж шайкештиги",
        "Adds": "Кошумча минералдар",
        "Quality documents": QUALITY_LABEL["ky"],
    },
}

VALUE_REPLACE = {
    "uz": {
        "Wholesale factory supply, OEM/ODM for OEM/ODM.": "Zavoddan ulgurji ta'minot va OEM/ODM moslashtirish.",
        "Selected NSF/ANSI test options and ISO/SGS documents are available on request.": COPY["uz"]["quality"],
        "This page is written for B2B buyers comparing factory supply, repeat orders and private-label water filtration programs.": "Ushbu sahifa zavod ta'minoti, takroriy buyurtmalar va private-label suv filtrlash dasturlarini solishtirayotgan B2B xaridorlar uchun tayyorlangan.",
        "Yes. Yuchen Water can quote private-label options such as label, packaging, color, connector, size or matched filter set depending on this product type.": ORG_COPY["uz"]["faq"][0][1],
        "Please send product specification, target quantity, private-label requirements, destination port and any compliance documents required in your market.": ORG_COPY["uz"]["faq"][1][1],
        "Water filtration products manufacturer": ORG_COPY["uz"]["industry"],
        "Global water filter and reverse osmosis system manufacturer for OEM/ODM wholesale buyers": "OEM/ODM ulgurji xaridorlari uchun suv filtri va teskari osmos tizimlari ishlab chiqaruvchisi",
    },
    "kk": {
        "Wholesale factory supply, OEM/ODM for OEM/ODM.": "Зауыттан көтерме жеткізу және OEM/ODM бейімдеу.",
        "Selected NSF/ANSI test options and ISO/SGS documents are available on request.": COPY["kk"]["quality"],
        "This page is written for B2B buyers comparing factory supply, repeat orders and private-label water filtration programs.": "Бұл бет зауыттық жеткізуді, қайталама тапсырыстарды және private-label су сүзу бағдарламаларын салыстыратын B2B сатып алушыларға арналған.",
        "Yes. Yuchen Water can quote private-label options such as label, packaging, color, connector, size or matched filter set depending on this product type.": ORG_COPY["kk"]["faq"][0][1],
        "Please send product specification, target quantity, private-label requirements, destination port and any compliance documents required in your market.": ORG_COPY["kk"]["faq"][1][1],
        "Water filtration products manufacturer": ORG_COPY["kk"]["industry"],
        "Global water filter and reverse osmosis system manufacturer for OEM/ODM wholesale buyers": "OEM/ODM көтерме сатып алушыларына арналған су сүзгісі және кері осмос жүйелері өндірушісі",
    },
    "ky": {
        "Wholesale factory supply, OEM/ODM for OEM/ODM.": "Заводдон дүң камсыздоо жана OEM/ODM ыңгайлаштыруу.",
        "Selected NSF/ANSI test options and ISO/SGS documents are available on request.": COPY["ky"]["quality"],
        "This page is written for B2B buyers comparing factory supply, repeat orders and private-label water filtration programs.": "Бул барак заводдук камсыздоону, кайталап буйрутмаларды жана private-label суу чыпкалоо программаларын салыштырган B2B сатып алуучулар үчүн даярдалган.",
        "Yes. Yuchen Water can quote private-label options such as label, packaging, color, connector, size or matched filter set depending on this product type.": ORG_COPY["ky"]["faq"][0][1],
        "Please send product specification, target quantity, private-label requirements, destination port and any compliance documents required in your market.": ORG_COPY["ky"]["faq"][1][1],
        "Water filtration products manufacturer": ORG_COPY["ky"]["industry"],
        "Global water filter and reverse osmosis system manufacturer for OEM/ODM wholesale buyers": "OEM/ODM дүң сатып алуучулары үчүн суу сүзгү жана тескери осмос системаларын өндүрүүчү",
    },
}

STANDARD_PRODUCT_PROPS = {
    "uz": [
        ("Mahsulot turi", "{name}"),
        ("Qo‘llanishi", "RO tizimlari, suv dispenserlari, oldindan filtrlash, tijorat suv tozalash yoki almashtirish kartriji dasturlariga mos konfiguratsiya."),
        ("OEM/ODM", "Logo, yorliq, rang, o‘lcham, filtr materiali, qadoqlash va eksport kartoni buyurtma talabiga ko‘ra moslashtiriladi."),
        (QUALITY_LABEL["uz"], COPY["uz"]["quality"]),
        ("MOQ", "Mahsulot spetsifikatsiyasi va moslashtirish darajasiga qarab tasdiqlanadi."),
    ],
    "kk": [
        ("Өнім түрі", "{name}"),
        ("Қолданылуы", "RO жүйелері, су диспенсерлері, алдын ала сүзу, коммерциялық су тазарту немесе ауыстырмалы картридж бағдарламаларына сай конфигурация."),
        ("OEM/ODM", "Логотип, жапсырма, түс, өлшем, сүзгі материалы, қаптама және экспорттық картон тапсырыс талабына қарай бейімделеді."),
        (QUALITY_LABEL["kk"], COPY["kk"]["quality"]),
        ("MOQ", "Өнім сипаттамасы мен бейімдеу деңгейіне қарай расталады."),
    ],
    "ky": [
        ("Өнүм түрү", "{name}"),
        ("Колдонулушу", "RO системалары, суу диспенсерлери, алдын ала чыпкалоо, коммерциялык суу тазалоо же алмаштыруучу картридж программалары үчүн ылайык конфигурация."),
        ("OEM/ODM", "Логотип, этикетка, түс, өлчөм, чыпка материалы, таңгак жана экспорттук картон буйрутма талабына жараша ыңгайлаштырылат."),
        (QUALITY_LABEL["ky"], COPY["ky"]["quality"]),
        ("MOQ", "Өнүм спецификациясына жана ыңгайлаштыруу деңгээлине жараша такталат."),
    ],
}

ENGLISH_PRODUCT_TEXT_RE = re.compile(
    r"\b(The|Custom|Industrial|Alkaline|Inline|Flat cap|Plastic|RO seawater|"
    r"PP Melt|Under-sink|Three stage|Wall mounted|Maifan|Post T33|"
    r"400GPD high-flow|Ion-exchange|UF hollow)\b"
)

SCHEMA_TERMS = {
    "ru": {
        "slogan": "Промышленная водоочистка и OEM-решения",
        "about": "О компании",
        "location": "Хайнин, Чжэцзян, Китай",
        "worldwide": "По всему миру",
        "terms": {
            "PP melt blown filter": "PP фильтр расплавного выдува",
            "CTO carbon block filter": "CTO угольный блок-фильтр",
            "GAC filter": "GAC фильтр",
            "T33 inline filter": "Линейный фильтр T33",
            "UF membrane": "UF мембрана",
            "RO membrane": "RO мембрана",
            "water purifier": "Очиститель воды",
            "water dispenser": "Диспенсер воды",
            "filter housing": "Корпус фильтра",
            "OEM manufacturing service": "OEM производственная услуга",
            "ODM design service": "ODM услуга разработки",
            "built-in pressure tank RO water purifier": "RO очиститель воды со встроенным баком",
            "compact reverse osmosis water purifier": "Компактный очиститель воды обратного осмоса",
            "100G and 200G RO systems": "RO системы 100G и 200G",
            "5-stage and 6-stage RO filtration": "5- и 6-ступенчатая RO фильтрация",
            "OEM/ODM water purifier manufacturing": "OEM/ODM производство очистителей воды",
            "private-label water filtration products": "Продукция водоочистки под частной маркой",
            "PP melt-blown filter cartridge": "PP melt-blown фильтрующий картридж",
            "GAC activated carbon filter": "GAC фильтр с активированным углем",
            "UF membrane filtration": "UF мембранная фильтрация",
            "RO membrane element": "RO мембранный элемент",
            "water dispenser manufacturing": "Производство диспенсеров воды",
        },
    },
    "es": {
        "slogan": "Purificación de agua industrial y soluciones OEM",
        "about": "Sobre nosotros",
        "location": "Haining, Zhejiang, China",
        "worldwide": "Todo el mundo",
        "terms": {
            "PP melt blown filter": "Filtro PP melt blown",
            "CTO carbon block filter": "Filtro CTO de bloque de carbón",
            "GAC filter": "Filtro GAC",
            "T33 inline filter": "Filtro en línea T33",
            "UF membrane": "Membrana UF",
            "RO membrane": "Membrana RO",
            "water purifier": "Purificador de agua",
            "water dispenser": "Dispensador de agua",
            "filter housing": "Carcasa de filtro",
            "OEM manufacturing service": "Servicio de fabricación OEM",
            "ODM design service": "Servicio de diseño ODM",
            "built-in pressure tank RO water purifier": "Purificador RO con tanque integrado",
            "compact reverse osmosis water purifier": "Purificador compacto de ósmosis inversa",
            "100G and 200G RO systems": "Sistemas RO 100G y 200G",
            "5-stage and 6-stage RO filtration": "Filtración RO de 5 y 6 etapas",
            "OEM/ODM water purifier manufacturing": "Fabricación OEM/ODM de purificadores de agua",
            "private-label water filtration products": "Productos de filtración de agua de marca privada",
            "PP melt-blown filter cartridge": "Cartucho filtrante PP melt blown",
            "GAC activated carbon filter": "Filtro GAC de carbón activado",
            "UF membrane filtration": "Filtración por membrana UF",
            "RO membrane element": "Elemento de membrana RO",
            "water dispenser manufacturing": "Fabricación de dispensadores de agua",
        },
    },
    "de": {
        "slogan": "Industrielle Wasseraufbereitung und OEM-Lösungen",
        "about": "Über uns",
        "location": "Haining, Zhejiang, China",
        "worldwide": "Weltweit",
        "terms": {
            "PP melt blown filter": "PP-Melt-Blown-Filter",
            "CTO carbon block filter": "CTO-Kohlenstoffblockfilter",
            "GAC filter": "GAC-Filter",
            "T33 inline filter": "T33-Inline-Filter",
            "UF membrane": "UF-Membran",
            "RO membrane": "RO-Membran",
            "water purifier": "Wasserreiniger",
            "water dispenser": "Wasserspender",
            "filter housing": "Filtergehäuse",
            "OEM manufacturing service": "OEM-Fertigungsservice",
            "ODM design service": "ODM-Designservice",
            "built-in pressure tank RO water purifier": "RO-Wasserreiniger mit integriertem Drucktank",
            "compact reverse osmosis water purifier": "Kompakter Umkehrosmose-Wasserreiniger",
            "100G and 200G RO systems": "RO-Systeme 100G und 200G",
            "5-stage and 6-stage RO filtration": "5- und 6-stufige RO-Filtration",
            "OEM/ODM water purifier manufacturing": "OEM/ODM-Fertigung von Wasserreinigern",
            "private-label water filtration products": "Wasserfiltrationsprodukte als Eigenmarke",
            "PP melt-blown filter cartridge": "PP-Melt-Blown-Filterkartusche",
            "GAC activated carbon filter": "GAC-Aktivkohlefilter",
            "UF membrane filtration": "UF-Membranfiltration",
            "RO membrane element": "RO-Membranelement",
            "water dispenser manufacturing": "Fertigung von Wasserspendern",
        },
    },
    "fr": {
        "slogan": "Traitement d'eau industriel et solutions OEM",
        "about": "À propos",
        "location": "Haining, Zhejiang, Chine",
        "worldwide": "Monde entier",
        "terms": {
            "PP melt blown filter": "Filtre PP melt blown",
            "CTO carbon block filter": "Filtre bloc de charbon CTO",
            "GAC filter": "Filtre GAC",
            "T33 inline filter": "Filtre en ligne T33",
            "UF membrane": "Membrane UF",
            "RO membrane": "Membrane RO",
            "water purifier": "Purificateur d'eau",
            "water dispenser": "Distributeur d'eau",
            "filter housing": "Boîtier de filtre",
            "OEM manufacturing service": "Service de fabrication OEM",
            "ODM design service": "Service de conception ODM",
            "built-in pressure tank RO water purifier": "Purificateur RO avec réservoir intégré",
            "compact reverse osmosis water purifier": "Purificateur compact par osmose inverse",
            "100G and 200G RO systems": "Systèmes RO 100G et 200G",
            "5-stage and 6-stage RO filtration": "Filtration RO à 5 et 6 étapes",
            "OEM/ODM water purifier manufacturing": "Fabrication OEM/ODM de purificateurs d'eau",
            "private-label water filtration products": "Produits de filtration d'eau en marque privée",
            "PP melt-blown filter cartridge": "Cartouche filtrante PP melt blown",
            "GAC activated carbon filter": "Filtre GAC à charbon actif",
            "UF membrane filtration": "Filtration par membrane UF",
            "RO membrane element": "Élément de membrane RO",
            "water dispenser manufacturing": "Fabrication de distributeurs d'eau",
        },
    },
    "vi": {
        "slogan": "Xử lý nước công nghiệp và giải pháp OEM",
        "about": "Giới thiệu",
        "location": "Haining, Zhejiang, Trung Quốc",
        "worldwide": "Toàn cầu",
        "terms": {
            "PP melt blown filter": "Lõi lọc PP melt blown",
            "CTO carbon block filter": "Lõi lọc CTO carbon block",
            "GAC filter": "Lõi lọc GAC",
            "T33 inline filter": "Lõi lọc inline T33",
            "UF membrane": "Màng UF",
            "RO membrane": "Màng RO",
            "water purifier": "Máy lọc nước",
            "water dispenser": "Cây nước",
            "filter housing": "Vỏ lọc",
            "OEM manufacturing service": "Dịch vụ sản xuất OEM",
            "ODM design service": "Dịch vụ thiết kế ODM",
            "built-in pressure tank RO water purifier": "Máy lọc RO bình áp tích hợp",
            "compact reverse osmosis water purifier": "Máy lọc nước RO nhỏ gọn",
            "100G and 200G RO systems": "Hệ thống RO 100G và 200G",
            "5-stage and 6-stage RO filtration": "Lọc RO 5 cấp và 6 cấp",
            "OEM/ODM water purifier manufacturing": "Sản xuất máy lọc nước OEM/ODM",
            "private-label water filtration products": "Sản phẩm lọc nước nhãn riêng",
            "PP melt-blown filter cartridge": "Lõi lọc PP melt blown",
            "GAC activated carbon filter": "Lõi lọc GAC than hoạt tính",
            "UF membrane filtration": "Lọc màng UF",
            "RO membrane element": "Phần tử màng RO",
            "water dispenser manufacturing": "Sản xuất cây nước",
        },
    },
    "ja": {
        "slogan": "産業用水処理とOEMソリューション",
        "about": "会社概要",
        "location": "中国浙江省海寧市",
        "worldwide": "世界各地",
        "terms": {
            "PP melt blown filter": "PPメルトブローンフィルター",
            "CTO carbon block filter": "CTOカーボンブロックフィルター",
            "GAC filter": "GACフィルター",
            "T33 inline filter": "T33インラインフィルター",
            "UF membrane": "UF膜",
            "RO membrane": "RO膜",
            "water purifier": "浄水器",
            "water dispenser": "ウォーターディスペンサー",
            "filter housing": "フィルターハウジング",
            "OEM manufacturing service": "OEM製造サービス",
            "ODM design service": "ODM設計サービス",
            "built-in pressure tank RO water purifier": "内蔵圧力タンク式RO浄水器",
            "compact reverse osmosis water purifier": "コンパクトRO浄水器",
            "100G and 200G RO systems": "100G・200G ROシステム",
            "5-stage and 6-stage RO filtration": "5段・6段ROろ過",
            "OEM/ODM water purifier manufacturing": "OEM/ODM浄水器製造",
            "private-label water filtration products": "プライベートラベル水処理製品",
            "PP melt-blown filter cartridge": "PPメルトブローンフィルターカートリッジ",
            "GAC activated carbon filter": "GAC活性炭フィルター",
            "UF membrane filtration": "UF膜ろ過",
            "RO membrane element": "RO膜エレメント",
            "water dispenser manufacturing": "ウォーターディスペンサー製造",
        },
    },
    "uz": {
        "slogan": "Sanoat suv tozalash va OEM yechimlari",
        "about": "Kompaniya haqida",
        "location": "Haining, Zhejiang, Xitoy",
        "worldwide": "Butun dunyo",
        "terms": {
            "PP melt blown filter": "PP melt blown filtr",
            "CTO carbon block filter": "CTO karbon blok filtri",
            "GAC filter": "GAC filtri",
            "T33 inline filter": "T33 inline filtr",
            "UF membrane": "UF membrana",
            "RO membrane": "RO membrana",
            "water purifier": "Suv tozalagich",
            "water dispenser": "Suv dispenseri",
            "filter housing": "Filtr korpusi",
            "OEM manufacturing service": "OEM ishlab chiqarish xizmati",
            "ODM design service": "ODM dizayn xizmati",
            "built-in pressure tank RO water purifier": "Ichki bosim bakli RO suv tozalagich",
            "compact reverse osmosis water purifier": "Ixcham teskari osmos suv tozalagich",
            "100G and 200G RO systems": "100G va 200G RO tizimlari",
            "5-stage and 6-stage RO filtration": "5 va 6 bosqichli RO filtrlash",
            "OEM/ODM water purifier manufacturing": "OEM/ODM suv tozalagich ishlab chiqarish",
            "private-label water filtration products": "Private-label suv filtrlash mahsulotlari",
            "PP melt-blown filter cartridge": "PP melt blown filtr kartriji",
            "GAC activated carbon filter": "GAC faollashtirilgan karbon filtri",
            "UF membrane filtration": "UF membrana filtrlash",
            "RO membrane element": "RO membrana elementi",
            "water dispenser manufacturing": "Suv dispenseri ishlab chiqarish",
        },
    },
    "kk": {
        "slogan": "Өнеркәсіптік су тазарту және OEM шешімдері",
        "about": "Компания туралы",
        "location": "Хайнин, Чжэцзян, Қытай",
        "worldwide": "Бүкіл әлем",
        "terms": {
            "PP melt blown filter": "PP melt blown сүзгісі",
            "CTO carbon block filter": "CTO көмір блок сүзгісі",
            "GAC filter": "GAC сүзгісі",
            "T33 inline filter": "T33 inline сүзгісі",
            "UF membrane": "UF мембранасы",
            "RO membrane": "RO мембранасы",
            "water purifier": "Су тазартқыш",
            "water dispenser": "Су диспенсері",
            "filter housing": "Сүзгі корпусы",
            "OEM manufacturing service": "OEM өндіріс қызметі",
            "ODM design service": "ODM дизайн қызметі",
            "built-in pressure tank RO water purifier": "Кіріктірілген қысым багы бар RO су тазартқыш",
            "compact reverse osmosis water purifier": "Ықшам кері осмос су тазартқышы",
            "100G and 200G RO systems": "100G және 200G RO жүйелері",
            "5-stage and 6-stage RO filtration": "5 және 6 сатылы RO сүзу",
            "OEM/ODM water purifier manufacturing": "OEM/ODM су тазартқыш өндірісі",
            "private-label water filtration products": "Private-label су сүзу өнімдері",
            "PP melt-blown filter cartridge": "PP melt blown сүзгі картриджі",
            "GAC activated carbon filter": "GAC белсендірілген көмір сүзгісі",
            "UF membrane filtration": "UF мембраналық сүзу",
            "RO membrane element": "RO мембрана элементі",
            "water dispenser manufacturing": "Су диспенсерін өндіру",
        },
    },
    "ky": {
        "slogan": "Өнөр жай суу тазалоо жана OEM чечимдери",
        "about": "Компания жөнүндө",
        "location": "Хайнин, Чжэцзян, Кытай",
        "worldwide": "Бүткүл дүйнө",
        "terms": {
            "PP melt blown filter": "PP melt blown сүзгү",
            "CTO carbon block filter": "CTO көмүр блок сүзгү",
            "GAC filter": "GAC сүзгү",
            "T33 inline filter": "T33 inline сүзгү",
            "UF membrane": "UF мембрана",
            "RO membrane": "RO мембрана",
            "water purifier": "Суу тазалагыч",
            "water dispenser": "Суу диспенсери",
            "filter housing": "Сүзгү корпусу",
            "OEM manufacturing service": "OEM өндүрүш кызматы",
            "ODM design service": "ODM дизайн кызматы",
            "built-in pressure tank RO water purifier": "Ички басым багы бар RO суу тазалагыч",
            "compact reverse osmosis water purifier": "Ыкчам тескери осмос суу тазалагыч",
            "100G and 200G RO systems": "100G жана 200G RO системалары",
            "5-stage and 6-stage RO filtration": "5 жана 6 баскычтуу RO чыпкалоо",
            "OEM/ODM water purifier manufacturing": "OEM/ODM суу тазалагыч өндүрүшү",
            "private-label water filtration products": "Private-label суу чыпкалоо продукциялары",
            "PP melt-blown filter cartridge": "PP melt blown сүзгү картриджи",
            "GAC activated carbon filter": "GAC активдештирилген көмүр сүзгү",
            "UF membrane filtration": "UF мембрана чыпкалоо",
            "RO membrane element": "RO мембрана элементи",
            "water dispenser manufacturing": "Суу диспенсерин өндүрүү",
        },
    },
}


def schema_type(obj: dict) -> set[str]:
    value = obj.get("@type")
    if isinstance(value, list):
        return {str(item) for item in value}
    if value:
        return {str(value)}
    return set()


def localize_url(value: str, lang: str) -> str:
    return value.replace("https://www.yuchensy.com/en/", f"https://www.yuchensy.com/{lang}/")


def replace_text(value: str, lang: str) -> str:
    if value == "Global water filter and reverse osmosis system manufacturer for OEM/ODM wholesale buyers":
        return ORG_COPY[lang]["description"]
    if value == "Industrial-Grade Water Purification & OEM Solutions":
        return SCHEMA_TERMS[lang]["slogan"]
    if value == "Home":
        return ORG_COPY[lang]["home"]
    if value == "Products":
        return ORG_COPY[lang]["products"]
    if value == "About Us":
        return SCHEMA_TERMS[lang]["about"]
    if value == "Haining, Zhejiang, China":
        return SCHEMA_TERMS[lang]["location"]
    if value == "Worldwide":
        return SCHEMA_TERMS[lang]["worldwide"]
    if value in SCHEMA_TERMS[lang]["terms"]:
        return SCHEMA_TERMS[lang]["terms"][value]
    for source, target in VALUE_REPLACE.get(lang, {}).items():
        value = value.replace(source, target)
    return value


def localize_schema(obj, lang: str, fallback_name: str):
    if isinstance(obj, list):
        for index, item in enumerate(obj):
            if isinstance(item, str):
                obj[index] = replace_text(item, lang)
            else:
                localize_schema(item, lang, fallback_name)
        return obj
    if not isinstance(obj, dict):
        return obj

    types = schema_type(obj)
    for key in ("@id", "url", "item", "urlTemplate"):
        if isinstance(obj.get(key), str):
            obj[key] = localize_url(obj[key], lang)

    if "Organization" in types:
        obj["industry"] = ORG_COPY[lang]["industry"]
        obj["description"] = ORG_COPY[lang]["description"]
        obj["slogan"] = SCHEMA_TERMS[lang]["slogan"]
        obj["award"] = ORG_COPY[lang]["awards"]
        if isinstance(obj.get("foundingLocation"), dict):
            obj["foundingLocation"]["name"] = SCHEMA_TERMS[lang]["location"]
        if isinstance(obj.get("areaServed"), dict):
            obj["areaServed"]["name"] = SCHEMA_TERMS[lang]["worldwide"]
        if isinstance(obj.get("hasCredential"), list):
            obj["hasCredential"] = [
                {
                    "@type": "EducationalOccupationalCredential",
                    "name": COPY[lang]["quality"],
                    "credentialCategory": QUALITY_LABEL[lang],
                }
            ]

    if "BreadcrumbList" in types and isinstance(obj.get("itemListElement"), list):
        for item in obj["itemListElement"]:
            if not isinstance(item, dict):
                continue
            if item.get("name") == "Home":
                item["name"] = ORG_COPY[lang]["home"]
            if item.get("name") == "Products":
                item["name"] = ORG_COPY[lang]["products"]
            if item.get("name") == "About Us":
                item["name"] = SCHEMA_TERMS[lang]["about"]

    if "FAQPage" in types:
        name = fallback_name
        questions = []
        faq_items = ORG_COPY[lang].get("faq") or COPY[lang]["q"][:6]
        for q, a in faq_items:
            questions.append(
                {
                    "@type": "Question",
                    "name": q.format(name=name),
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
            )
        obj["mainEntity"] = questions

    if "ItemList" in types and isinstance(obj.get("itemListElement"), list):
        for item in obj["itemListElement"]:
            if not isinstance(item, dict):
                continue
            item_name = clean_name(str(item.get("name") or fallback_name))
            if isinstance(item.get("description"), str):
                item["description"] = COPY[lang]["card"].format(name=item_name)

    if "Product" in types:
        name = clean_name(str(obj.get("name") or fallback_name))
        description = str(obj.get("description") or "")
        if (
            "This page is written for B2B buyers" in description
            or "Wholesale factory supply" in description
            or ENGLISH_PRODUCT_TEXT_RE.search(description)
        ):
            obj["description"] = COPY[lang]["intro"].format(name=name)
        if lang in STANDARD_PRODUCT_PROPS:
            obj["additionalProperty"] = [
                {"@type": "PropertyValue", "name": prop_name, "value": prop_value.format(name=name)}
                for prop_name, prop_value in STANDARD_PRODUCT_PROPS[lang]
            ]
        if lang in STANDARD_PRODUCT_PROPS and isinstance(obj.get("category"), str) and ENGLISH_PRODUCT_TEXT_RE.search(obj["category"]):
            obj["category"] = name
        if isinstance(obj.get("additionalProperty"), list):
            for prop in obj["additionalProperty"]:
                if not isinstance(prop, dict):
                    continue
                prop_names = PROPERTY_NAME.get(lang, {})
                if prop.get("name") in prop_names:
                    prop["name"] = prop_names[prop["name"]]
                if isinstance(prop.get("value"), str):
                    prop["value"] = replace_text(prop["value"], lang)

    for key, value in list(obj.items()):
        if isinstance(value, str):
            obj[key] = replace_text(value, lang)
        else:
            localize_schema(value, lang, fallback_name)
    return obj


SCRIPT_RE = re.compile(r'(<script type="application/ld\+json">)(.*?)(</script>)', re.S)


def fix_jsonld(page: str, lang: str) -> str:
    fallback_name = product_name(page)

    def repl(match: re.Match[str]) -> str:
        prefix, payload, suffix = match.groups()
        try:
            data = json.loads(payload)
        except json.JSONDecodeError:
            payload = replace_text(payload, lang)
            return f"{prefix}{payload}{suffix}"
        localize_schema(data, lang, fallback_name)
        return f"{prefix}{json.dumps(data, ensure_ascii=False, separators=(',', ':'))}{suffix}"

    return SCRIPT_RE.sub(repl, page)


def fix_plain_text(page: str, lang: str) -> str:
    options = {
        "ru": "варианты испытаний NSF/ANSI",
        "es": "opciones de ensayo NSF/ANSI",
        "de": "NSF/ANSI-Prüfoptionen",
        "fr": "options d'essai NSF/ANSI",
        "vi": "tùy chọn thử nghiệm NSF/ANSI",
        "ja": "NSF/ANSI試験オプション",
        "uz": "NSF/ANSI sinov variantlari",
        "kk": "NSF/ANSI сынақ нұсқалары",
        "ky": "NSF/ANSI сыноо варианттары",
    }
    page = page.replace("NSF/ANSI options", options[lang])
    return page


def main() -> None:
    changed = 0
    scanned = 0
    for lang in LANGS:
        for path in (ROOT / lang).glob("*.html"):
            scanned += 1
            original = path.read_text(encoding="utf-8", errors="ignore")
            page = fix_plain_text(fix_jsonld(original, lang), lang)
            if page != original:
                path.write_text(page, encoding="utf-8")
                changed += 1

    for path in (ROOT / "fr").glob("*.html"):
        original = path.read_text(encoding="utf-8", errors="ignore")
        page = original.replace("Applications du produit", "Domaines d'utilisation du produit")
        if page != original:
            path.write_text(page, encoding="utf-8")
            changed += 1
    print(f"Scanned {scanned} priority-language HTML files; changed {changed} files.")


if __name__ == "__main__":
    main()
