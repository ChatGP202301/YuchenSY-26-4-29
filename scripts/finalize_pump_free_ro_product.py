#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SLUG = "product-pump-free-five-stage-ro-water-purifier.html"
PRODUCT_KEY = "pump-free-five-stage-ro-water-purifier"
SITE = "https://www.yuchensy.com"
ASSET_DIR = ROOT / "assets" / "products"
REPORT_DIR = ROOT / "reports"
ZIP_PATH = ROOT / "yuchensy-github-pages-2026-06-29-pump-free-ro.zip"

IMAGE_SOURCES = [
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/221cd2ae294a3a607ef1d74ce52c4a18.jpg", "front"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/93916567b05e102d773be16517bbcded.jpg", "main"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d731e00f1ba00872bda1161199a7eaca.jpg", "side"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/05b8cd6ce9df259d93c6c7e54560d327.jpg", "connection"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d86e152609ff958ad8719b0888dbcb90.jpg", "housing"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/71fd19f5ccd4efb2fbdd1aeb043c3931.jpg", "cartridges"),
]
VIDEO_SOURCE = Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/video_1782469173627.mp4")

RTL_LANGS = {"ar", "fa", "he", "ku"}
LANG_NAMES = {
    "en": "English", "ru": "Русский", "es": "Español", "de": "Deutsch", "fr": "Français",
    "vi": "Tiếng Việt", "ja": "日本語", "uz": "O'zbek", "kk": "Қазақша", "ky": "Кыргызча",
    "ar": "العربية", "fa": "فارسی", "he": "עברית", "tr": "Türkçe", "it": "Italiano",
    "nl": "Nederlands", "pt": "Português", "id": "Indonesia", "ko": "한국어", "pl": "Polski",
    "cs": "Čeština", "sk": "Slovenčina", "hu": "Magyar", "ro": "Română", "bg": "Български",
    "hr": "Hrvatski", "sr": "Српски", "sl": "Slovenščina", "bs": "Bosanski", "sq": "Shqip",
    "el": "Ελληνικά", "lt": "Lietuvių", "lv": "Latviešu", "et": "Eesti", "uk": "Українська",
    "th": "ไทย", "ms": "Melayu", "tl": "Filipino", "bn": "বাংলা", "sw": "Kiswahili",
    "af": "Afrikaans", "da": "Dansk", "no": "Norsk", "fi": "Suomi", "sv": "Svenska",
    "zh": "中文",
}


def pack(name, summary, detail, card, headings, labels, faq, quote, contact, meta=None):
    return {
        "name": name,
        "summary": summary,
        "detail": detail,
        "card": card,
        "headings": headings,
        "labels": labels,
        "faq": faq,
        "quote": quote,
        "contact": contact,
        "meta": meta or summary,
    }


TEXT = {
    "en": pack(
        "Pump-Free Five Stage RO Water Purifier",
        "This pump-free RO water purifier works from municipal tap water pressure, so it is suitable for markets where buyers prefer a quieter, simpler system without a booster pump. The five-stage configuration combines PP sediment filtration, UDF/GAC carbon, CTO carbon block, RO membrane separation and T33 post carbon polishing for household and light commercial drinking water projects. Yuchen Water can support OEM branding, label design, packaging and component selection for distributors and appliance brands.",
        "The system is designed for stable city-water-pressure operation. It reduces installation complexity, keeps power demand low and gives buyers a compact reverse osmosis option for apartments, rental homes, small offices and replacement system programs. Filter sequence, connector style, bracket, faucet, tubing color and carton layout can be adjusted for OEM or ODM orders.",
        "Pump-free five-stage RO purifier for municipal tap water pressure, with PP, carbon, RO membrane and T33 filtration for OEM drinking water projects.",
        ("Product Gallery", "Technical Specifications", "System Description", "Product Video", "Questions from Buyers", "Related Products"),
        ("Product type", "Filtration stages", "Working method", "Water source", "Pressure requirement", "Installation", "OEM/ODM options", "Typical buyers"),
        [
            ("Does this model need a booster pump?", "No. It is designed to work with municipal tap water pressure when the local inlet pressure is suitable."),
            ("Can the filter labels and carton be customized?", "Yes. Logo, label, manual, color accessories and export carton design can be discussed for OEM orders."),
            ("Which filters are included?", "The standard system uses PP, UDF/GAC, CTO, RO membrane and T33 post carbon filtration."),
        ],
        "Request OEM Quote",
        "Contact Engineer",
        "Pump-free five-stage RO water purifier for tap-water-pressure OEM projects, with PP, carbon, RO membrane and T33 filtration.",
    ),
    "ru": pack(
        "Пятиступенчатый RO-фильтр без насоса",
        "Этот RO-очиститель работает от давления городского водопровода и не требует повышающего насоса. Пятиступенчатая схема включает PP-фильтр осадка, уголь UDF/GAC, угольный блок CTO, мембрану RO и постфильтр T33. Модель подходит дистрибьюторам, брендам бытовых фильтров и проектам замены картриджных систем, где важны тихая работа, простая установка и OEM-оформление.",
        "Конструкция упрощает монтаж и снижает зависимость от электропитания. По заказу можно адаптировать последовательность фильтров, кронштейн, фитинги, кран, цвет трубок, маркировку картриджей, инструкцию и экспортную упаковку.",
        "RO-система без насоса для работы от давления водопровода, с PP, угольными фильтрами, мембраной RO и T33 для OEM-поставок.",
        ("Фотографии продукта", "Технические характеристики", "Описание системы", "Видео продукта", "Вопросы покупателей", "Связанные продукты"),
        ("Тип продукта", "Ступени фильтрации", "Принцип работы", "Источник воды", "Требование к давлению", "Монтаж", "Варианты OEM/ODM", "Основные покупатели"),
        [
            ("Нужен ли повышающий насос?", "Нет, модель рассчитана на подходящее давление городского водопровода."),
            ("Можно ли изменить этикетку и коробку?", "Да, логотип, этикетка, инструкция и экспортная коробка настраиваются для OEM-заказов."),
            ("Какие фильтры входят в систему?", "Стандартная схема: PP, UDF/GAC, CTO, мембрана RO и постфильтр T33."),
        ],
        "Запросить OEM-предложение",
        "Связаться с инженером",
    ),
    "es": pack(
        "Purificador RO de cinco etapas sin bomba",
        "Este purificador RO funciona con la presión del agua municipal y no necesita bomba de refuerzo. La configuración de cinco etapas integra filtro PP de sedimentos, carbón UDF/GAC, bloque CTO, membrana RO y postfiltro T33. Es una opción silenciosa y sencilla para distribuidores, marcas de purificadores y proyectos de reposición que buscan suministro OEM estable.",
        "El diseño reduce la complejidad de instalación y el consumo eléctrico. Yuchen Water puede adaptar la secuencia de filtros, soporte, conectores, grifo, color de tubos, etiquetas, manual y embalaje de exportación según el pedido.",
        "Purificador RO sin bomba para presión de red municipal, con PP, carbón, membrana RO y T33 para proyectos OEM.",
        ("Galería del producto", "Especificaciones técnicas", "Descripción del sistema", "Vídeo del producto", "Preguntas de compradores", "Productos relacionados"),
        ("Tipo de producto", "Etapas de filtración", "Modo de trabajo", "Fuente de agua", "Presión requerida", "Instalación", "Opciones OEM/ODM", "Compradores típicos"),
        [
            ("¿Necesita bomba de refuerzo?", "No. Está diseñado para trabajar con presión municipal adecuada."),
            ("¿Se pueden personalizar etiquetas y cajas?", "Sí. Logotipo, etiqueta, manual y caja de exportación se pueden preparar para pedidos OEM."),
            ("¿Qué filtros incluye?", "La configuración estándar utiliza PP, UDF/GAC, CTO, membrana RO y T33."),
        ],
        "Solicitar cotización OEM",
        "Contactar con ingeniería",
    ),
    "de": pack(
        "Fünfstufiger RO-Wasserfilter ohne Pumpe",
        "Dieser RO-Wasserfilter arbeitet mit dem Druck der kommunalen Wasserversorgung und benötigt keine Druckerhöhungspumpe. Die fünfstufige Filtration kombiniert PP-Sedimentfilter, UDF/GAC-Aktivkohle, CTO-Kohleblock, RO-Membran und T33-Nachfilter. Das Modell eignet sich für Händler, Markenanbieter und Austauschprogramme, die eine leise, einfache und OEM-fähige Lösung suchen.",
        "Die Anlage vereinfacht die Installation und reduziert den Strombedarf. Filterfolge, Halterung, Anschlüsse, Wasserhahn, Schlauchfarbe, Etiketten, Anleitung und Exportverpackung können projektbezogen angepasst werden.",
        "RO-Wasserfilter ohne Pumpe für Leitungswasserdruck, mit PP, Aktivkohle, RO-Membran und T33 für OEM-Projekte.",
        ("Produktbilder", "Technische Daten", "Systembeschreibung", "Produktvideo", "Fragen von Käufern", "Ähnliche Produkte"),
        ("Produkttyp", "Filtrationsstufen", "Arbeitsweise", "Wasserquelle", "Druckanforderung", "Installation", "OEM/ODM-Optionen", "Typische Käufer"),
        [
            ("Benötigt das Modell eine Pumpe?", "Nein. Es ist für geeigneten kommunalen Leitungswasserdruck ausgelegt."),
            ("Sind Etiketten und Kartons anpassbar?", "Ja. Logo, Etikett, Anleitung und Exportkarton können für OEM-Aufträge angepasst werden."),
            ("Welche Filter sind enthalten?", "Standardmäßig PP, UDF/GAC, CTO, RO-Membran und T33-Nachfilter."),
        ],
        "OEM-Angebot anfragen",
        "Ingenieur kontaktieren",
    ),
    "fr": pack(
        "Purificateur RO cinq étapes sans pompe",
        "Ce purificateur RO fonctionne avec la pression du réseau municipal et ne nécessite pas de pompe de surpression. La filtration en cinq étapes associe un filtre PP à sédiments, du charbon UDF/GAC, un bloc CTO, une membrane RO et un post-filtre T33. Il convient aux distributeurs, marques et programmes de remplacement recherchant une solution silencieuse, simple et personnalisable en OEM.",
        "La conception réduit la complexité d'installation et la dépendance à l'alimentation électrique. La séquence de filtres, le support, les raccords, le robinet, la couleur des tubes, les étiquettes, la notice et l'emballage export peuvent être adaptés.",
        "Purificateur RO sans pompe pour pression d'eau municipale, avec PP, charbon, membrane RO et T33 pour projets OEM.",
        ("Galerie produit", "Spécifications techniques", "Description du système", "Vidéo du produit", "Questions des acheteurs", "Produits associés"),
        ("Type de produit", "Étapes de filtration", "Mode de fonctionnement", "Source d'eau", "Pression requise", "Installation", "Options OEM/ODM", "Acheteurs typiques"),
        [
            ("Faut-il une pompe de surpression ?", "Non. Le modèle fonctionne avec une pression de réseau adaptée."),
            ("Les étiquettes et cartons sont-ils personnalisables ?", "Oui. Logo, étiquette, notice et carton export peuvent être préparés pour les commandes OEM."),
            ("Quels filtres sont inclus ?", "La configuration standard utilise PP, UDF/GAC, CTO, membrane RO et T33."),
        ],
        "Demander un devis OEM",
        "Contacter l'ingénieur",
    ),
    "vi": pack(
        "Máy lọc RO năm cấp không dùng bơm",
        "Máy lọc RO này vận hành bằng áp lực nước máy đô thị, không cần bơm tăng áp. Hệ lọc năm cấp gồm lõi PP giữ cặn, than UDF/GAC, than khối CTO, màng RO và lõi T33 sau lọc. Sản phẩm phù hợp cho nhà phân phối, thương hiệu máy lọc nước và dự án thay thế cần giải pháp êm, dễ lắp và hỗ trợ OEM.",
        "Thiết kế giúp giảm phụ thuộc vào điện và đơn giản hóa lắp đặt. Có thể tùy chỉnh thứ tự lõi lọc, giá treo, đầu nối, vòi, màu ống, nhãn lõi, hướng dẫn và thùng xuất khẩu theo yêu cầu.",
        "Máy lọc RO không dùng bơm, chạy bằng áp lực nước máy, có PP, than, màng RO và T33 cho dự án OEM.",
        ("Hình ảnh sản phẩm", "Thông số kỹ thuật", "Mô tả hệ thống", "Video sản phẩm", "Câu hỏi của khách mua", "Sản phẩm liên quan"),
        ("Loại sản phẩm", "Cấp lọc", "Cách vận hành", "Nguồn nước", "Yêu cầu áp lực", "Lắp đặt", "Tùy chọn OEM/ODM", "Khách mua phù hợp"),
        [
            ("Có cần bơm tăng áp không?", "Không. Máy được thiết kế cho áp lực nước máy phù hợp."),
            ("Có thể tùy chỉnh nhãn và thùng không?", "Có. Logo, nhãn, hướng dẫn và thùng xuất khẩu có thể làm theo đơn OEM."),
            ("Bao gồm những lõi lọc nào?", "Cấu hình tiêu chuẩn gồm PP, UDF/GAC, CTO, màng RO và T33."),
        ],
        "Yêu cầu báo giá OEM",
        "Liên hệ kỹ sư",
    ),
    "ja": pack(
        "ポンプ不要の5段RO浄水器",
        "このRO浄水器は水道圧で作動し、加圧ポンプを必要としません。5段ろ過はPP沈殿フィルター、UDF/GAC活性炭、CTOカーボンブロック、RO膜、T33後置きカーボンで構成されます。静音性、簡単な設置、OEM対応を重視する販売代理店や浄水器ブランドに適したモデルです。",
        "電源への依存を抑え、設置作業を簡素化できます。フィルター構成、ブラケット、継手、蛇口、チューブ色、ラベル、取扱説明書、輸出用梱包は注文仕様に合わせて調整できます。",
        "水道圧で作動するポンプ不要RO浄水器。PP、活性炭、RO膜、T33を組み合わせたOEM向けモデルです。",
        ("製品写真", "技術仕様", "システム説明", "製品動画", "購入者からの質問", "関連製品"),
        ("製品タイプ", "ろ過段数", "作動方式", "原水", "必要水圧", "設置方式", "OEM/ODM対応", "主な購入者"),
        [
            ("加圧ポンプは必要ですか。", "いいえ。適切な水道圧で作動するように設計されています。"),
            ("ラベルや箱は変更できますか。", "はい。ロゴ、ラベル、説明書、輸出用箱をOEM仕様で対応できます。"),
            ("どのフィルターを使用しますか。", "標準構成はPP、UDF/GAC、CTO、RO膜、T33です。"),
        ],
        "OEM見積もりを依頼",
        "技術者に相談",
    ),
    "uz": pack(
        "Nasossiz besh bosqichli RO suv tozalagich",
        "Ushbu RO suv tozalagich shahar vodoprovod bosimi bilan ishlaydi va kuchaytiruvchi nasos talab qilmaydi. Besh bosqichli tizim PP cho'kindi filtri, UDF/GAC ko'mir, CTO ko'mir bloki, RO membrana va T33 yakuniy ko'mir filtridan iborat. Model distribyutorlar va OEM brendlar uchun sokin, sodda va moslashtiriladigan yechimdir.",
        "Qurilma o'rnatishni soddalashtiradi va elektrga bog'liqlikni kamaytiradi. Filtr ketma-ketligi, kronshteyn, ulagich, kran, quvur rangi, yorliq, qo'llanma va eksport qutisi buyurtmaga ko'ra moslashtiriladi.",
        "Vodoprovod bosimi bilan ishlaydigan nasossiz RO tozalagich, PP, ko'mir, RO membrana va T33 bilan OEM loyihalar uchun.",
        ("Mahsulot rasmlari", "Texnik xususiyatlar", "Tizim tavsifi", "Mahsulot videosi", "Xaridor savollari", "Tegishli mahsulotlar"),
        ("Mahsulot turi", "Filtrlash bosqichlari", "Ishlash usuli", "Suv manbai", "Bosim talabi", "O'rnatish", "OEM/ODM imkoniyatlari", "Asosiy xaridorlar"),
        [
            ("Kuchaytiruvchi nasos kerakmi?", "Yo'q. Model mos vodoprovod bosimi bilan ishlashga mo'ljallangan."),
            ("Yorliq va quti moslashtiriladimi?", "Ha. Logo, yorliq, qo'llanma va eksport qutisi OEM buyurtmasiga moslanadi."),
            ("Qaysi filtrlar bor?", "Standart tizim PP, UDF/GAC, CTO, RO membrana va T33 dan iborat."),
        ],
        "OEM narxini so'rash",
        "Muhandis bilan bog'lanish",
    ),
    "kk": pack(
        "Сорғысыз бес сатылы RO су тазартқыш",
        "Бұл RO су тазартқыш қалалық су қысымымен жұмыс істейді және күшейткіш сорғыны қажет етпейді. Бес сатылы сүзу PP тұнба сүзгісін, UDF/GAC көмірін, CTO көмір блогын, RO мембранасын және T33 соңғы көмір сүзгісін біріктіреді. Үлгі тыныш жұмыс, жеңіл орнату және OEM бейімдеу қажет дистрибьюторларға жарайды.",
        "Жүйе орнатуды жеңілдетіп, электрге тәуелділікті азайтады. Сүзгі реті, кронштейн, қосқыштар, кран, түтік түсі, жапсырма, нұсқаулық және экспорт қорабы тапсырысқа сай өзгертіледі.",
        "Қалалық су қысымымен жұмыс істейтін сорғысыз RO жүйе, PP, көмір, RO мембрана және T33 сүзуімен OEM жобаларға арналған.",
        ("Өнім суреттері", "Техникалық сипаттамалар", "Жүйе сипаттамасы", "Өнім видеосы", "Сатып алушы сұрақтары", "Ұқсас өнімдер"),
        ("Өнім түрі", "Сүзу сатылары", "Жұмыс тәсілі", "Су көзі", "Қысым талабы", "Орнату", "OEM/ODM нұсқалары", "Негізгі сатып алушылар"),
        [
            ("Күшейткіш сорғы керек пе?", "Жоқ. Үлгі қолайлы қалалық су қысымымен жұмыс істеуге арналған."),
            ("Жапсырма мен қорапты өзгертуге бола ма?", "Иә. Логотип, жапсырма, нұсқаулық және экспорт қорабы OEM тапсырысына бейімделеді."),
            ("Қандай сүзгілер қолданылады?", "Стандартты жүйе PP, UDF/GAC, CTO, RO мембрана және T33 қамтиды."),
        ],
        "OEM бағасын сұрау",
        "Инженермен байланысу",
    ),
    "ky": pack(
        "Насоссуз беш баскычтуу RO суу тазалагыч",
        "Бул RO суу тазалагыч шаардык суу басымы менен иштейт жана күчөтүүчү насос талап кылбайт. Беш баскычтуу чыпкалоо PP чөкмө чыпкасын, UDF/GAC көмүрүн, CTO көмүр блогун, RO мембранасын жана T33 соңку көмүр чыпкасын камтыйт. Модель тынч иштөө, жеңил орнотуу жана OEM ылайыкташтыруу керек болгон сатып алуучуларга ылайыктуу.",
        "Түзүлүш орнотууну жөнөкөйлөтүп, электрге көз карандылыкты азайтат. Чыпка ирети, кронштейн, туташтыргычтар, кран, түтүк түсү, этикетка, нускама жана экспорт кутусу заказ боюнча өзгөртүлөт.",
        "Шаардык суу басымы менен иштеген насоссуз RO система, PP, көмүр, RO мембрана жана T33 менен OEM долбоорлорго ылайыктуу.",
        ("Продукт сүрөттөрү", "Техникалык мүнөздөмөлөр", "Системанын сүрөттөлүшү", "Продукт видеосу", "Сатып алуучу суроолору", "Окшош продуктылар"),
        ("Продукт түрү", "Чыпкалоо баскычтары", "Иштөө ыкмасы", "Суу булагы", "Басым талабы", "Орнотуу", "OEM/ODM варианттары", "Негизги сатып алуучулар"),
        [
            ("Күчөтүүчү насос керекпи?", "Жок. Модель ылайыктуу шаардык суу басымы менен иштөөгө арналган."),
            ("Этикетка жана куту өзгөрөбү?", "Ооба. Логотип, этикетка, нускама жана экспорт кутусу OEM заказга ылайыкталат."),
            ("Кайсы чыпкалар колдонулат?", "Стандарттуу система PP, UDF/GAC, CTO, RO мембрана жана T33 камтыйт."),
        ],
        "OEM баасын суроо",
        "Инженер менен байланышуу",
    ),
}

EXTRA = {
    "ar": ("جهاز تنقية RO بخمس مراحل بدون مضخة", "يعمل هذا الجهاز بضغط مياه الشبكة البلدية دون مضخة تعزيز. يجمع نظام الترشيح بين PP والكربون UDF/GAC وCTO وغشاء RO وفلتر T33، وهو مناسب للتوزيع ومشاريع OEM الهادئة وسهلة التركيب."),
    "fa": ("تصفیه‌کننده RO پنج‌مرحله‌ای بدون پمپ", "این دستگاه با فشار آب شهری کار می‌کند و به پمپ تقویت‌کننده نیاز ندارد. مسیر تصفیه شامل PP، کربن UDF/GAC، بلوک CTO، غشای RO و فیلتر نهایی T33 است و برای پروژه‌های OEM مناسب است."),
    "he": ("מטהר RO חמש-שלבי ללא משאבה", "המערכת פועלת בלחץ מי רשת עירונית ללא משאבת הגברה. חמשת השלבים כוללים PP, פחם UDF/GAC, CTO, ממברנת RO ומסנן T33, ומתאימים למותגי OEM."),
    "tr": ("Pompasız beş aşamalı RO su arıtma cihazı", "Bu RO cihazı şehir şebekesi basıncıyla çalışır ve takviye pompası gerektirmez. PP, UDF/GAC karbon, CTO, RO membran ve T33 son karbon filtresiyle OEM projeleri için sessiz ve sade bir çözümdür."),
    "it": ("Purificatore RO a cinque stadi senza pompa", "Il purificatore funziona con la pressione dell'acqua di rete e non richiede pompa booster. La filtrazione integra PP, carbone UDF/GAC, CTO, membrana RO e T33 per forniture OEM silenziose e semplici da installare."),
    "nl": ("Vijftraps RO-waterfilter zonder pomp", "Dit RO-systeem werkt op gemeentelijke waterdruk en heeft geen boosterpomp nodig. De opbouw met PP, UDF/GAC-kool, CTO, RO-membraan en T33 is geschikt voor stille OEM-projecten."),
    "pt": ("Purificador RO de cinco etapas sem bomba", "O purificador funciona com a pressão da rede municipal e não exige bomba de reforço. A filtragem combina PP, carvão UDF/GAC, CTO, membrana RO e T33 para projetos OEM."),
    "id": ("Pemurni RO lima tahap tanpa pompa", "Pemurni ini bekerja dengan tekanan air kota tanpa pompa pendorong. Tahap PP, karbon UDF/GAC, CTO, membran RO dan T33 cocok untuk proyek OEM yang tenang dan mudah dipasang."),
    "ko": ("펌프 없는 5단 RO 정수기", "이 RO 정수기는 수돗물 압력으로 작동하며 가압 펌프가 필요하지 않습니다. PP, UDF/GAC 탄소, CTO, RO 멤브레인, T33 구성으로 OEM 공급에 적합합니다."),
    "pl": ("Pięciostopniowy filtr RO bez pompy", "Urządzenie działa na ciśnieniu wody miejskiej bez pompy wzmacniającej. Układ PP, węgiel UDF/GAC, CTO, membrana RO i T33 sprawdza się w projektach OEM."),
    "cs": ("Pětistupňový RO čistič bez čerpadla", "Zařízení pracuje s tlakem městské vody bez posilovacího čerpadla. Sestava PP, uhlík UDF/GAC, CTO, membrána RO a T33 je vhodná pro OEM dodávky."),
    "sk": ("Päťstupňový RO čistič bez čerpadla", "Zariadenie pracuje s tlakom mestskej vody bez posilňovacieho čerpadla. PP, UDF/GAC uhlík, CTO, RO membrána a T33 sú vhodné pre OEM projekty."),
    "hu": ("Szivattyú nélküli ötlépcsős RO víztisztító", "A készülék városi víznyomással működik, nyomásfokozó szivattyú nélkül. A PP, UDF/GAC szén, CTO, RO membrán és T33 felépítés OEM projektekhez illik."),
    "ro": ("Purificator RO în cinci trepte fără pompă", "Purificatorul funcționează cu presiunea apei municipale, fără pompă de ridicare. Filtrarea PP, carbon UDF/GAC, CTO, membrană RO și T33 este potrivită pentru OEM."),
    "bg": ("Петстепенен RO пречиствател без помпа", "Уредът работи с налягане от градската мрежа без усилваща помпа. PP, UDF/GAC въглен, CTO, RO мембрана и T33 са подходящи за OEM проекти."),
    "hr": ("Petostupanjski RO pročišćivač bez pumpe", "Uređaj radi na tlaku gradske vode bez pojačavajuće pumpe. PP, UDF/GAC ugljen, CTO, RO membrana i T33 prikladni su za OEM isporuke."),
    "sr": ("Петостепени RO пречистач без пумпе", "Уређај ради на притиску градске воде без појачавајуће пумпе. PP, UDF/GAC угљен, CTO, RO мембрана и T33 погодни су за OEM пројекте."),
    "sl": ("Petstopenjski RO čistilec brez črpalke", "Naprava deluje s tlakom mestne vode brez ojačevalne črpalke. PP, UDF/GAC oglje, CTO, RO membrana in T33 so primerni za OEM naročila."),
    "bs": ("Petostepeni RO prečistač bez pumpe", "Uređaj radi na pritisku gradske vode bez pojačavajuće pumpe. PP, UDF/GAC ugljen, CTO, RO membrana i T33 pogodni su za OEM projekte."),
    "sq": ("Pastrues RO me pesë faza pa pompë", "Pajisja punon me presionin e ujit të rrjetit pa pompë përforcuese. PP, karbon UDF/GAC, CTO, membranë RO dhe T33 janë të përshtatshme për OEM."),
    "el": ("Πενταβάθμιο φίλτρο RO χωρίς αντλία", "Η συσκευή λειτουργεί με πίεση δημοτικού νερού χωρίς αντλία ενίσχυσης. Τα στάδια PP, άνθρακας UDF/GAC, CTO, μεμβράνη RO και T33 είναι κατάλληλα για OEM."),
    "lt": ("Penkių pakopų RO filtras be siurblio", "Įrenginys veikia nuo miesto vandens slėgio be stiprinimo siurblio. PP, UDF/GAC anglis, CTO, RO membrana ir T33 tinka OEM tiekimui."),
    "lv": ("Piecu pakāpju RO filtrs bez sūkņa", "Ierīce darbojas ar pilsētas ūdens spiedienu bez pastiprinātāja sūkņa. PP, UDF/GAC ogle, CTO, RO membrāna un T33 ir piemēroti OEM projektiem."),
    "et": ("Viieastmeline pumbata RO veepuhasti", "Seade töötab linna veesurvega ilma rõhutõstepumbata. PP, UDF/GAC süsi, CTO, RO membraan ja T33 sobivad OEM-tarneteks."),
    "uk": ("П'ятиступеневий RO-очисник без насоса", "Пристрій працює від тиску міської води без підвищувального насоса. PP, UDF/GAC вугілля, CTO, RO мембрана і T33 підходять для OEM."),
    "th": ("เครื่องกรอง RO ห้าขั้นตอนไม่ใช้ปั๊ม", "เครื่องนี้ทำงานด้วยแรงดันน้ำประปา ไม่ต้องใช้ปั๊มเพิ่มแรงดัน มี PP, คาร์บอน UDF/GAC, CTO, เมมเบรน RO และ T33 เหมาะกับงาน OEM."),
    "ms": ("Penapis RO lima peringkat tanpa pam", "Sistem ini beroperasi dengan tekanan air bandar tanpa pam penguat. PP, karbon UDF/GAC, CTO, membran RO dan T33 sesuai untuk projek OEM."),
    "tl": ("Limang yugto na RO purifier na walang bomba", "Gumagana ito sa presyon ng tubig sa lungsod nang walang booster pump. Ang PP, UDF/GAC carbon, CTO, RO membrane at T33 ay angkop sa OEM."),
    "bn": ("পাম্পবিহীন পাঁচ ধাপের RO পানি পরিশোধক", "এই RO পরিশোধক পৌর পানির চাপেই চলে, অতিরিক্ত পাম্প লাগে না। PP, UDF/GAC কার্বন, CTO, RO মেমব্রেন ও T33 OEM প্রকল্পের জন্য উপযোগী।"),
    "sw": ("Kisafishaji cha RO hatua tano bila pampu", "Kifaa hufanya kazi kwa shinikizo la maji ya mjini bila pampu ya kuongeza nguvu. PP, kaboni UDF/GAC, CTO, utando RO na T33 vinafaa kwa OEM."),
    "af": ("Vyfstadium RO-waterfilter sonder pomp", "Die toestel werk met munisipale waterdruk sonder versterkerpomp. PP, UDF/GAC-koolstof, CTO, RO-membraan en T33 pas by OEM-projekte."),
    "da": ("Femtrins RO-vandfilter uden pumpe", "Enheden arbejder med kommunalt vandtryk uden boosterpumpe. PP, UDF/GAC-kul, CTO, RO-membran og T33 passer til OEM-projekter."),
    "no": ("Femtrinns RO-vannfilter uten pumpe", "Enheten bruker kommunalt vanntrykk uten boosterpumpe. PP, UDF/GAC-karbon, CTO, RO-membran og T33 passer for OEM-prosjekter."),
    "fi": ("Viisivaiheinen RO-puhdistin ilman pumppua", "Laite toimii kunnallisella vedenpaineella ilman paineenkorotuspumppua. PP, UDF/GAC-hiili, CTO, RO-kalvo ja T33 sopivat OEM-toimituksiin."),
    "sv": ("Femstegs RO-vattenrenare utan pump", "Enheten arbetar med kommunalt vattentryck utan tryckhöjningspump. PP, UDF/GAC-kol, CTO, RO-membran och T33 passar OEM-projekt."),
    "zh": ("无泵五级RO净水机", "这款RO净水机依靠市政自来水压力运行，不需要增压泵。五级过滤包含PP、UDF/GAC、CTO、RO膜和T33，适合经销商、品牌商和OEM项目。"),
}


def add_extra_languages() -> None:
    headings = ("产品图片", "技术参数", "系统说明", "产品视频", "买家常见问题", "相关产品")
    labels = ("产品类型", "过滤级数", "运行方式", "适用水源", "压力要求", "安装方式", "OEM/ODM选项", "适合客户")
    faq = [("是否需要增压泵？", "不需要，适合在进水压力合适的市政自来水环境中使用。"), ("是否可以定制？", "可以定制标识、标签、说明书和出口包装。"), ("过滤配置是什么？", "标准配置为PP、UDF/GAC、CTO、RO膜和T33。")]
    for code, (name, summary) in EXTRA.items():
        TEXT[code] = pack(name, summary, summary, summary, headings, labels, faq, "咨询OEM报价", "联系工程师")


def language_dirs() -> list[Path]:
    dirs = []
    for path in ROOT.iterdir():
        if path.is_dir() and len(path.name) <= 5 and (path / "index.html").exists():
            dirs.append(path)
    if not (ROOT / "en").exists() and (ROOT / "index.html").exists():
        dirs.append(ROOT)
    return sorted(dirs, key=lambda p: p.name)


def lang_from_dir(path: Path) -> str:
    return "en" if path == ROOT else path.name


def web_path(lang: str, filename: str = SLUG) -> str:
    return f"/{filename}" if lang == "root" else f"/{lang}/{filename}"


def canonical(lang: str) -> str:
    if lang == "root":
        return f"{SITE}/{SLUG}"
    return f"{SITE}/{lang}/{SLUG}"


def image_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image
        with Image.open(path) as img:
            return img.size
    except Exception:
        return (900, 1200)


def prepare_assets() -> tuple[list[dict], str | None]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    images = []
    try:
        from PIL import Image
        pil_ok = True
    except Exception:
        pil_ok = False
        Image = None
    for source, suffix in IMAGE_SOURCES:
        src = Path(source)
        if not src.exists():
            continue
        if pil_ok:
            out = ASSET_DIR / f"{PRODUCT_KEY}-{suffix}.webp"
            with Image.open(src) as im:
                im = im.convert("RGB")
                im.thumbnail((1400, 1400))
                im.save(out, "WEBP", quality=84, method=6)
        else:
            out = ASSET_DIR / f"{PRODUCT_KEY}-{suffix}{src.suffix.lower()}"
            shutil.copy2(src, out)
        width, height = image_size(out)
        images.append({"src": f"../assets/products/{out.name}", "file": out, "width": width, "height": height})
    video = None
    if VIDEO_SOURCE.exists():
        video_out = ASSET_DIR / f"{PRODUCT_KEY}-demo.mp4"
        shutil.copy2(VIDEO_SOURCE, video_out)
        video = f"../assets/products/{video_out.name}"
    return images, video


def strip_managed_blocks(text: str) -> str:
    text = re.sub(r"\s*<!-- PUMP_FREE_RO_HEAD_START -->.*?<!-- PUMP_FREE_RO_HEAD_END -->", "", text, flags=re.S)
    text = re.sub(r"\s*<!-- PUMP_FREE_RO_CARD_START -->.*?<!-- PUMP_FREE_RO_CARD_END -->", "", text, flags=re.S)
    return text


def update_html_tag(page: str, lang: str) -> str:
    direction = " dir=\"rtl\"" if lang in RTL_LANGS else ""
    if re.search(r"<html\b[^>]*>", page, flags=re.I):
        return re.sub(r"<html\b[^>]*>", f"<html lang=\"{html.escape(lang)}\"{direction}>", page, count=1, flags=re.I)
    return page


def update_head(page: str, lang: str, t: dict, image: str | None) -> str:
    page = re.sub(r"<title>.*?</title>", "", page, flags=re.I | re.S)
    page = re.sub(r"\s*<meta\s+name=[\"']description[\"'][^>]*>", "", page, flags=re.I)
    page = re.sub(r"\s*<meta\s+name=[\"']keywords[\"'][^>]*>", "", page, flags=re.I)
    page = re.sub(r"\s*<meta\s+name=[\"']author[\"'][^>]*>", "", page, flags=re.I)
    page = re.sub(r"\s*<link\s+rel=[\"']canonical[\"'][^>]*>", "", page, flags=re.I)
    image_url = f"{SITE}/{image.replace('../', '')}" if image else f"{SITE}/assets/images/yuchen-water-logo-transparent.webp"
    head = f"""
<!-- PUMP_FREE_RO_HEAD_START -->
<title>{html.escape(t['name'])} | Yuchen Water</title>
<meta name="description" content="{html.escape(t['meta'][:155])}">
<meta name="author" content="Yuchen Water">
<link rel="canonical" href="{canonical(lang)}">
<meta property="og:title" content="{html.escape(t['name'])} | Yuchen Water">
<meta property="og:description" content="{html.escape(t['meta'][:180])}">
<meta property="og:image" content="{html.escape(image_url)}">
<!-- PUMP_FREE_RO_HEAD_END -->
"""
    if "</head>" in page:
        return page.replace("</head>", head + "\n</head>", 1)
    return head + page


def spec_values(lang: str) -> list[str]:
    return [
        "RO",
        "PP + UDF/GAC + CTO + RO + T33",
        {
            "en": "No booster pump, municipal tap water pressure",
            "ru": "Без насоса, давление городского водопровода",
            "es": "Sin bomba, presión de red municipal",
            "de": "Ohne Pumpe, kommunaler Leitungswasserdruck",
            "fr": "Sans pompe, pression du réseau municipal",
            "vi": "Không dùng bơm, áp lực nước máy",
            "ja": "ポンプ不要、水道圧で作動",
            "uz": "Nasossiz, shahar vodoprovod bosimi",
            "kk": "Сорғысыз, қалалық су қысымы",
            "ky": "Насоссуз, шаардык суу басымы",
            "zh": "无增压泵，依靠市政自来水压力",
        }.get(lang, "RO"),
        {
            "en": "Municipal tap water", "ru": "Городская водопроводная вода", "es": "Agua de red municipal",
            "de": "Kommunales Leitungswasser", "fr": "Eau du réseau municipal", "vi": "Nước máy đô thị",
            "ja": "市水", "uz": "Shahar vodoprovod suvi", "kk": "Қалалық су", "ky": "Шаардык суу", "zh": "市政自来水",
        }.get(lang, "H2O"),
        "0.1-0.4 MPa",
        {
            "en": "Wall-mounted or under-sink installation", "ru": "Настенный или подмоечный монтаж", "es": "Instalación mural o bajo fregadero",
            "de": "Wandmontage oder Untertischmontage", "fr": "Installation murale ou sous évier", "vi": "Lắp treo tường hoặc dưới bồn",
            "ja": "壁掛けまたはシンク下設置", "uz": "Devorga yoki rakovina ostiga o'rnatish", "kk": "Қабырғаға немесе раковина астына орнату", "ky": "Дубалга же раковина астына орнотуу", "zh": "壁挂或厨下安装",
        }.get(lang, "RO"),
        {
            "en": "Logo, label, manual, carton, fittings", "ru": "Логотип, этикетка, инструкция, коробка, фитинги", "es": "Logotipo, etiqueta, manual, caja y conectores",
            "de": "Logo, Etikett, Anleitung, Karton und Anschlüsse", "fr": "Logo, étiquette, notice, carton et raccords", "vi": "Logo, nhãn, hướng dẫn, thùng và đầu nối",
            "ja": "ロゴ、ラベル、説明書、箱、継手", "uz": "Logo, yorliq, qo'llanma, quti, ulagich", "kk": "Логотип, жапсырма, нұсқаулық, қорап, фитинг", "ky": "Логотип, этикетка, нускама, куту, туташтыргыч", "zh": "Logo、标签、说明书、纸箱、接头",
        }.get(lang, "OEM/ODM"),
        {
            "en": "Distributors, water purifier brands, importers", "ru": "Дистрибьюторы, бренды фильтров, импортеры", "es": "Distribuidores, marcas e importadores",
            "de": "Händler, Markenanbieter, Importeure", "fr": "Distributeurs, marques, importateurs", "vi": "Nhà phân phối, thương hiệu, nhà nhập khẩu",
            "ja": "販売代理店、浄水器ブランド、輸入業者", "uz": "Distribyutorlar, brendlar, importyorlar", "kk": "Дистрибьюторлар, брендтер, импорттаушылар", "ky": "Дистрибьюторлор, бренддер, импортчулар", "zh": "经销商、品牌商、进口商",
        }.get(lang, "B2B"),
    ]


def body(lang: str, t: dict, images: list[dict], video: str | None, all_langs: list[str]) -> str:
    labels = t["labels"]
    values = spec_values(lang)
    gallery = "\n".join(
        f'<figure class="product-gallery-item"><img src="{html.escape(img["src"])}" width="{img["width"]}" height="{img["height"]}" loading="lazy" alt="{html.escape(t["name"])} - {i + 1}"></figure>'
        for i, img in enumerate(images)
    )
    main_img = images[0]["src"] if images else ""
    specs = "\n".join(f"<tr><th>{html.escape(label)}</th><td>{html.escape(value)}</td></tr>" for label, value in zip(labels, values))
    faqs = "\n".join(f"<details><summary>{html.escape(q)}</summary><p>{html.escape(a)}</p></details>" for q, a in t["faq"])
    video_html = ""
    if video:
        video_html = f"""
<section class="section product-video-section">
  <div class="container">
    <h2>{html.escape(t['headings'][3])}</h2>
    <video controls preload="metadata" playsinline poster="{html.escape(main_img)}" style="width:100%;max-width:900px;border-radius:8px;">
      <source src="{html.escape(video)}" type="video/mp4">
    </video>
  </div>
</section>"""
    hreflang = "\n".join(
        f'<link rel="alternate" hreflang="{html.escape(code)}" href="{canonical(code)}">'
        for code in all_langs if code != "root"
    )
    product_schema = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": t["name"],
        "description": t["meta"],
        "brand": {"@type": "Brand", "name": "Yuchen Water"},
        "manufacturer": {"@type": "Organization", "name": "Yuchen Water"},
        "image": [f"{SITE}/{img['src'].replace('../', '')}" for img in images],
        "category": "RO water purifier",
    }
    faq_schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in t["faq"]],
    }
    breadcrumb_schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/{lang}/index.html"},
            {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{SITE}/{lang}/products.html"},
            {"@type": "ListItem", "position": 3, "name": t["name"], "item": canonical(lang)},
        ],
    }
    return f"""
<!-- PUMP_FREE_RO_START -->
<section class="section product-hero-section">
  <div class="container">
    <nav class="breadcrumb"><a href="index.html">Home</a> / <a href="products.html">Products</a> / <span>{html.escape(t['name'])}</span></nav>
    <div class="product-detail-layout">
      <div class="product-detail-media">
        <img src="{html.escape(main_img)}" width="{images[0]['width'] if images else 900}" height="{images[0]['height'] if images else 1200}" alt="{html.escape(t['name'])}" loading="eager">
      </div>
      <div class="product-detail-summary">
        <h1>{html.escape(t['name'])}</h1>
        <p>{html.escape(t['summary'])}</p>
        <p>{html.escape(t['detail'])}</p>
        <div class="cta-row">
          <a class="btn btn-primary" href="contact.html">{html.escape(t['quote'])}</a>
          <a class="btn btn-secondary" href="https://wa.me/8619908311885">{html.escape(t['contact'])}</a>
        </div>
      </div>
    </div>
  </div>
</section>
<section class="section product-gallery-section">
  <div class="container">
    <h2>{html.escape(t['headings'][0])}</h2>
    <div class="product-gallery-grid">{gallery}</div>
  </div>
</section>
<section class="section product-spec-section">
  <div class="container">
    <h2>{html.escape(t['headings'][1])}</h2>
    <table class="spec-table"><tbody>{specs}</tbody></table>
  </div>
</section>
<section class="section product-description-section">
  <div class="container">
    <h2>{html.escape(t['headings'][2])}</h2>
    <p>{html.escape(t['detail'])}</p>
  </div>
</section>
{video_html}
<section class="section faq-section">
  <div class="container">
    <h2>{html.escape(t['headings'][4])}</h2>
    <div class="faq-list">{faqs}</div>
  </div>
</section>
<section class="section related-products-section">
  <div class="container">
    <h2>{html.escape(t['headings'][5])}</h2>
    <p><a href="ro-water-purifier.html">RO</a> · <a href="product-built-in-pressure-tank-ro.html">100G/200G</a> · <a href="products.html">Yuchen Water</a></p>
    <div class="cta-row"><a class="btn btn-primary" href="contact.html">{html.escape(t['quote'])}</a></div>
  </div>
</section>
<script type="application/ld+json">{json.dumps(product_schema, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(faq_schema, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(breadcrumb_schema, ensure_ascii=False)}</script>
<!-- PUMP_FREE_RO_END -->
"""


def base_page_for(lang_dir: Path) -> str:
    for name in ["product-built-in-pressure-tank-ro.html", "product-ro-seawater-desalination-machine.html", "index.html"]:
        path = lang_dir / name
        if path.exists():
            return path.read_text(encoding="utf-8", errors="ignore")
    return "<!doctype html><html><head></head><body><main></main></body></html>"


def replace_main(page: str, content: str) -> str:
    page = strip_managed_blocks(page)
    m = re.search(r"<main\b[^>]*>.*?</main>", page, flags=re.S | re.I)
    if m:
        return page[:m.start()] + "<main>\n" + content + "\n</main>" + page[m.end():]
    if "</body>" in page:
        return page.replace("</body>", "<main>\n" + content + "\n</main>\n</body>", 1)
    return page + "<main>\n" + content + "\n</main>"


def product_card(lang: str, t: dict, image: str | None) -> str:
    img_html = ""
    if image:
        img_html = f'<img src="{html.escape(image)}" alt="{html.escape(t["name"])}" loading="lazy" width="900" height="1200">'
    return f"""
<!-- PUMP_FREE_RO_CARD_START -->
<article class="product-card" data-category="ro-water-purifier">
  <a href="{SLUG}">{img_html}<h3>{html.escape(t['name'])}</h3></a>
  <p>{html.escape(t['card'])}</p>
  <a class="btn btn-secondary" href="{SLUG}">{html.escape(t['contact'])}</a>
</article>
<!-- PUMP_FREE_RO_CARD_END -->
"""


def insert_card(products: Path, card: str) -> None:
    if not products.exists():
        return
    text = strip_managed_blocks(products.read_text(encoding="utf-8", errors="ignore"))
    if PRODUCT_KEY in text or SLUG in text:
        text = re.sub(r"\s*<!-- PUMP_FREE_RO_CARD_START -->.*?<!-- PUMP_FREE_RO_CARD_END -->", "", text, flags=re.S)
    if "</main>" in text:
        text = text.replace("</main>", card + "\n</main>", 1)
    else:
        text += "\n" + card
    products.write_text(text, encoding="utf-8")


def update_sitemap(langs: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    urls = "\n".join(f"  <url><loc>{canonical(lang)}</loc></url>" for lang in langs if lang != "root")
    if sitemap.exists():
        text = sitemap.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"\s*<url><loc>[^<]*" + re.escape(SLUG) + r"</loc></url>", "", text)
        if "</urlset>" in text:
            text = text.replace("</urlset>", urls + "\n</urlset>", 1)
        else:
            text += "\n" + urls
    else:
        text = f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{urls}\n</urlset>\n'
    sitemap.write_text(text, encoding="utf-8")


def visible_generated_text(page: str) -> str:
    m = re.search(r"<!-- PUMP_FREE_RO_START -->(.*?)<!-- PUMP_FREE_RO_END -->", page, flags=re.S)
    snippet = m.group(1) if m else page
    snippet = re.sub(r"<script\b[^>]*>.*?</script>", "", snippet, flags=re.S | re.I)
    snippet = re.sub(r"<[^>]+>", " ", snippet)
    return html.unescape(snippet)


def check_english(lang: str, text: str) -> list[str]:
    if lang == "en":
        return []
    allowed = {"RO", "PP", "CTO", "UDF", "GAC", "T33", "OEM", "ODM", "MPa", "Yuchen", "Water", "WhatsApp"}
    problems = []
    phrases = ["municipal tap water", "booster pump", "five-stage", "Product Gallery", "Technical Specifications", "System Description", "Product Video", "Questions from Buyers", "Related Products", "Request OEM Quote", "Contact Engineer"]
    lower = text.lower()
    for phrase in phrases:
        if phrase.lower() in lower:
            problems.append(phrase)
    words = re.findall(r"\b[A-Za-z][A-Za-z-]{3,}\b", text)
    for word in words:
        if word not in allowed and word.upper() not in allowed:
            if word not in problems:
                problems.append(word)
            if len(problems) >= 12:
                break
    return problems


def write_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in ROOT.rglob("*"):
            if path.is_dir():
                continue
            rel = path.relative_to(ROOT)
            if rel.parts[0] in {".git", "__pycache__"}:
                continue
            if path == ZIP_PATH:
                continue
            zf.write(path, rel.as_posix())


def main() -> None:
    add_extra_languages()
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    images, video = prepare_assets()
    langs = []
    checks = []
    lang_dirs = language_dirs()
    all_langs = [lang_from_dir(d) for d in lang_dirs]
    for lang_dir in lang_dirs:
        lang = lang_from_dir(lang_dir)
        t = TEXT.get(lang, TEXT["en"])
        langs.append(lang)
        page = base_page_for(lang_dir)
        page = update_html_tag(page, lang)
        content = body(lang, t, images, video, all_langs)
        page = replace_main(page, content)
        page = update_head(page, lang, t, images[0]["src"] if images else None)
        out = lang_dir / SLUG
        out.write_text(page, encoding="utf-8")
        card = product_card(lang, t, images[0]["src"] if images else None)
        insert_card(lang_dir / "products.html", card)
        visible = visible_generated_text(page)
        problems = check_english(lang, visible)
        checks.append((lang, out.exists(), (lang_dir / "products.html").exists(), not problems, ", ".join(problems[:8])))
    update_sitemap(langs)
    write_zip()
    report = REPORT_DIR / "pump-free-ro-product-verification-2026-06-29.txt"
    lines = [
        "Pump-free five-stage RO water purifier verification",
        f"Product page: {SLUG}",
        f"Images created: {len(images)}",
        f"Video included: {'yes' if video else 'no'}",
        f"Package: {ZIP_PATH.name}",
        "",
        "Language checks:",
    ]
    for lang, page_ok, list_ok, text_ok, notes in checks:
        lines.append(f"- {lang}: page={'ok' if page_ok else 'missing'}, products={'ok' if list_ok else 'missing'}, localized_text={'ok' if text_ok else 'review'}, notes={notes or '-'}")
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(report)


if __name__ == "__main__":
    main()
