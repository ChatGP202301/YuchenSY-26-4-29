#!/usr/bin/env python3
"""Post-process the generated static site.

The generated pages are numerous, so this script fixes repeatable issues in one
pass: valid Schema.org types, escaped category filters, malformed image tags,
placeholder reCAPTCHA, language meta consistency, and common untranslated UI.
"""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MODIFIED_DATE = "2026-05-11"

LANGS = [
    "en", "es", "fr", "de", "pt", "ru", "ar", "ja", "ko", "it", "tr",
    "hi", "bn", "id", "vi", "th", "pl", "nl", "fa", "ur", "ms", "tl",
    "he", "el", "cs", "hu", "ro", "sv", "da", "fi", "no", "uk", "bg",
    "hr", "sr", "sk", "sl", "lt", "et", "lv", "sw", "ha", "zu", "ta", "kk",
]

RTL_LANGS = {"ar", "fa", "he", "ur"}

LANG_META = {
    "en": ("en", "English"),
    "es": ("es", "Spanish"),
    "fr": ("fr", "French"),
    "de": ("de", "German"),
    "pt": ("pt", "Portuguese"),
    "ru": ("ru", "Russian"),
    "ar": ("ar", "Arabic"),
    "ja": ("ja", "Japanese"),
    "ko": ("ko", "Korean"),
    "it": ("it", "Italian"),
    "tr": ("tr", "Turkish"),
    "hi": ("hi", "Hindi"),
    "bn": ("bn", "Bengali"),
    "id": ("id", "Indonesian"),
    "vi": ("vi", "Vietnamese"),
    "th": ("th", "Thai"),
    "pl": ("pl", "Polish"),
    "nl": ("nl", "Dutch"),
    "fa": ("fa", "Persian"),
    "ur": ("ur", "Urdu"),
    "ms": ("ms", "Malay"),
    "tl": ("tl", "Tagalog"),
    "he": ("he", "Hebrew"),
    "el": ("el", "Greek"),
    "cs": ("cs", "Czech"),
    "hu": ("hu", "Hungarian"),
    "ro": ("ro", "Romanian"),
    "sv": ("sv", "Swedish"),
    "da": ("da", "Danish"),
    "fi": ("fi", "Finnish"),
    "no": ("no", "Norwegian"),
    "uk": ("uk", "Ukrainian"),
    "bg": ("bg", "Bulgarian"),
    "hr": ("hr", "Croatian"),
    "sr": ("sr", "Serbian"),
    "sk": ("sk", "Slovak"),
    "sl": ("sl", "Slovenian"),
    "lt": ("lt", "Lithuanian"),
    "et": ("et", "Estonian"),
    "lv": ("lv", "Latvian"),
    "sw": ("sw", "Swahili"),
    "ha": ("ha", "Hausa"),
    "zu": ("zu", "Zulu"),
    "ta": ("ta", "Tamil"),
    "kk": ("kk", "Kazakh"),
}

# High-impact repeated UI strings. Product model names remain technical terms,
# but fixed navigation, CTA, workshop and contact copy should match the page.
REPLACEMENTS: dict[str, dict[str, str]] = {
    "ru": {
        "View Product Catalog": "Смотреть каталог продукции",
        "Product SKUs": "Артикулов продукции",
        "m² Factory Area": "м² площадь фабрики",
        "OEM/ODM Water Filtration Excellence": "Экспертиза OEM/ODM в фильтрации воды",
        "Founded in 1998, Express Water has grown into one of China&#x27;s most trusted water purification manufacturers, exporting to 50+ countries with full NSF, ISO 9001, CE and SGS certification.": "Основанная в 1998 году, Express Water стала одним из надежных китайских производителей систем водоочистки и экспортирует продукцию в 50+ стран с сертификациями NSF, ISO 9001, CE и SGS.",
        "Custom branding, tooling, packaging — MOQ from 1,000 pcs.": "Индивидуальный брендинг, оснастка и упаковка — MOQ от 1 000 шт.",
        "NSF, ISO 9001:2015, CE, SGS, FDA &amp; Halal compliant.": "Соответствие NSF, ISO 9001:2015, CE, SGS, FDA и Halal.",
        "FOB Shanghai/Ningbo · CIF · DDP — 50+ countries shipped.": "FOB Шанхай/Нинбо · CIF · DDP — поставки в 50+ стран.",
        "WhatsApp + email engineering support in 5+ languages.": "Инженерная поддержка по WhatsApp и email на 5+ языках.",
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.": "Полная линейка OEM/ODM: фильтрующие картриджи, RO-мембраны, диспенсеры, корпуса и системы водоочистки для бытовых, коммерческих и промышленных задач.",
        "State-of-the-Art Manufacturing": "Современное производство",
        "Our Production Lines": "Наши производственные линии",
        "20,000+ m² ISO 9001 certified facility in Haining, Zhejiang — dedicated lines for PP melt-blown, sintered carbon block, UF/RO membrane assembly and dispenser SMT.": "Завод 20 000+ м² в Хайнине, Чжэцзян, сертифицированный по ISO 9001: отдельные линии для PP melt-blown, спеченного угольного блока, сборки UF/RO-мембран и SMT для диспенсеров.",
        "PP Melt-Blown Filter Line": "Линия PP melt-blown фильтров",
        "Carbon Block Line": "Линия угольных блоков",
        "Inline Filter Line": "Линия inline-фильтров",
        "QC Leakage Test": "QC тест на протечки",
        "Automated extrusion · 24/7 operation": "Автоматизированная экструзия · работа 24/7",
        "Sintered CTO · Coconut-shell media": "Спеченный CTO · кокосовый активированный уголь",
        "Quick-connect assembly": "Сборка quick-connect",
        "100% pressure-tested before shipment": "100% проверка давлением перед отгрузкой",
        "Request a Quote · Bulk OEM Inquiry": "Запрос цены · Оптовый OEM-запрос",
        "Inquire Now": "Отправить запрос",
        "Request a Quote": "Запросить цену",
        "← Back to All Products": "← Назад ко всем продуктам",
        "Get In Touch": "Связаться",
        "Reach our B2B sales team via WhatsApp, email or the form below. Average response time: under 4 hours during business days.": "Свяжитесь с нашей B2B-командой продаж через WhatsApp, email или форму ниже. Среднее время ответа в рабочие дни — до 4 часов.",
        "Get in Touch": "Контактная информация",
        "Factory Address": "Адрес фабрики",
        "WhatsApp Sales": "Продажи в WhatsApp",
        "Mon–Sat 08:30 – 18:00 (China Standard Time, GMT+8)": "Пн-Сб 08:30-18:00 (китайское время, GMT+8)",
        "27+ Years Producing Premium Water Filtration": "27+ лет производства премиальных решений для фильтрации воды",
        "Production Lines": "Производственные линии",
        "Capabilities": "Возможности",
        "Production & QC at Industrial Scale": "Производство и контроль качества в промышленном масштабе",
        "Our state-of-the-art manufacturing center in Yuanhua Town, Haining, Zhejiang Province operates dedicated lines for every product family — ensuring traceability, quality and on-time delivery for global wholesale orders.": "Наш современный производственный центр в Юаньхуа, Хайнин, провинция Чжэцзян, имеет отдельные линии для каждой категории продукции, обеспечивая прослеживаемость, качество и своевременную поставку оптовых заказов.",
        "All Products | Express Water — Filters, RO Membranes, Dispensers": "Вся продукция | Express Water — фильтры, RO-мембраны, диспенсеры",
        "Contact Express Water | Bulk OEM Inquiry, WhatsApp & Quote Request": "Контакты Express Water | Оптовый OEM-запрос, WhatsApp и расчет цены",
        "About Express Water | OEM Water Filter Manufacturer Since 1998": "О Express Water | OEM-производитель фильтров для воды с 1998 года",
        "NSF Certified Water Filter Cartridge by Express Water China Manufacturer": "сертифицированный NSF фильтрующий картридж от китайского производителя Express Water",
    },
    "es": {
        "View Product Catalog": "Ver catálogo de productos",
        "Product SKUs": "Referencias de producto",
        "m² Factory Area": "m² de fábrica",
        "OEM/ODM Water Filtration Excellence": "Excelencia OEM/ODM en filtración de agua",
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.": "Gama completa OEM/ODM de cartuchos filtrantes, membranas RO, dispensadores, carcasas y sistemas completos de purificación para usos residenciales, comerciales e industriales.",
        "State-of-the-Art Manufacturing": "Fabricación avanzada",
        "Our Production Lines": "Nuestras líneas de producción",
        "Request a Quote · Bulk OEM Inquiry": "Solicitar cotización · Consulta OEM mayorista",
        "Product SKUs Portfolio": "portafolio de referencias de producto",
        "← Back to All Products": "← Volver a todos los productos",
        "Inquire Now": "Consultar ahora",
        "Request a Quote": "Solicitar cotización",
    },
    "fr": {
        "View Product Catalog": "Voir le catalogue produits",
        "Product SKUs": "Références produit",
        "m² Factory Area": "m² de surface d'usine",
        "OEM/ODM Water Filtration Excellence": "Excellence OEM/ODM en filtration de l'eau",
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.": "Gamme complète OEM/ODM de cartouches filtrantes, membranes RO, distributeurs, boîtiers et systèmes complets de purification pour applications résidentielles, commerciales et industrielles.",
        "State-of-the-Art Manufacturing": "Fabrication de pointe",
        "Our Production Lines": "Nos lignes de production",
        "Request a Quote · Bulk OEM Inquiry": "Demande de devis · Projet OEM en volume",
        "Product SKUs Portfolio": "portefeuille de références produit",
        "← Back to All Products": "← Retour à tous les produits",
        "Inquire Now": "Demander maintenant",
        "Request a Quote": "Demander un devis",
    },
    "de": {
        "View Product Catalog": "Produktkatalog ansehen",
        "Product SKUs": "Produkt-SKUs",
        "m² Factory Area": "m² Werksfläche",
        "OEM/ODM Water Filtration Excellence": "OEM/ODM-Kompetenz in der Wasserfiltration",
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.": "Vollständiges OEM/ODM-Sortiment mit Filterkartuschen, RO-Membranen, Spendern, Gehäusen und kompletten Wasseraufbereitungssystemen für private, gewerbliche und industrielle Anwendungen.",
        "State-of-the-Art Manufacturing": "Moderne Fertigung",
        "Our Production Lines": "Unsere Produktionslinien",
        "Request a Quote · Bulk OEM Inquiry": "Angebot anfordern · OEM-Großmengenanfrage",
        "Product SKUs Portfolio": "Produkt-SKU-Portfolio",
        "← Back to All Products": "← Zurück zu allen Produkten",
        "Inquire Now": "Jetzt anfragen",
        "Request a Quote": "Angebot anfordern",
    },
    "pt": {
        "View Product Catalog": "Ver catálogo de produtos",
        "Product SKUs": "SKUs de produto",
        "m² Factory Area": "m² de área fabril",
        "OEM/ODM Water Filtration Excellence": "Excelência OEM/ODM em filtragem de água",
        "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.": "Linha completa OEM/ODM com cartuchos filtrantes, membranas RO, dispensadores, carcaças e sistemas completos de purificação para aplicações residenciais, comerciais e industriais.",
        "State-of-the-Art Manufacturing": "Fabricação avançada",
        "Our Production Lines": "Nossas linhas de produção",
        "Request a Quote · Bulk OEM Inquiry": "Solicitar cotação · Consulta OEM em volume",
        "Product SKUs Portfolio": "portfólio de SKUs de produto",
        "← Back to All Products": "← Voltar a todos os produtos",
        "Inquire Now": "Consultar agora",
        "Request a Quote": "Solicitar cotação",
    },
    "it": {
        "View Product Catalog": "Vedi catalogo prodotti",
        "Product SKUs": "SKU prodotto",
        "m² Factory Area": "m² di area produttiva",
        "OEM/ODM Water Filtration Excellence": "Eccellenza OEM/ODM nella filtrazione dell'acqua",
        "State-of-the-Art Manufacturing": "Produzione all'avanguardia",
        "Our Production Lines": "Le nostre linee di produzione",
        "Request a Quote · Bulk OEM Inquiry": "Richiedi preventivo · Richiesta OEM all'ingrosso",
        "← Back to All Products": "← Torna a tutti i prodotti",
        "Inquire Now": "Richiedi informazioni",
        "Request a Quote": "Richiedi preventivo",
    },
    "tr": {
        "View Product Catalog": "Ürün kataloğunu görüntüle",
        "Product SKUs": "Ürün SKU'ları",
        "m² Factory Area": "m² fabrika alanı",
        "OEM/ODM Water Filtration Excellence": "OEM/ODM su filtrasyonu uzmanlığı",
        "State-of-the-Art Manufacturing": "Modern üretim",
        "Our Production Lines": "Üretim hatlarımız",
        "Request a Quote · Bulk OEM Inquiry": "Teklif isteyin · Toplu OEM talebi",
        "← Back to All Products": "← Tüm ürünlere dön",
        "Inquire Now": "Hemen sor",
        "Request a Quote": "Teklif isteyin",
    },
    "ar": {
        "View Product Catalog": "عرض كتالوج المنتجات",
        "Product SKUs": "رموز المنتجات",
        "m² Factory Area": "م² مساحة المصنع",
        "OEM/ODM Water Filtration Excellence": "خبرة OEM/ODM في تنقية المياه",
        "State-of-the-Art Manufacturing": "تصنيع متقدم",
        "Our Production Lines": "خطوط الإنتاج لدينا",
        "Request a Quote · Bulk OEM Inquiry": "طلب عرض سعر · استفسار OEM بالجملة",
        "← Back to All Products": "← العودة إلى جميع المنتجات",
        "Inquire Now": "استفسر الآن",
        "Request a Quote": "طلب عرض سعر",
    },
    "ja": {
        "View Product Catalog": "製品カタログを見る",
        "Product SKUs": "製品SKU",
        "m² Factory Area": "m² 工場面積",
        "OEM/ODM Water Filtration Excellence": "OEM/ODM水ろ過ソリューション",
        "State-of-the-Art Manufacturing": "先進的な製造体制",
        "Our Production Lines": "生産ライン",
        "Request a Quote · Bulk OEM Inquiry": "見積依頼 · 大量OEMお問い合わせ",
        "← Back to All Products": "← すべての製品に戻る",
        "Inquire Now": "今すぐ問い合わせ",
        "Request a Quote": "見積依頼",
    },
    "ko": {
        "View Product Catalog": "제품 카탈로그 보기",
        "Product SKUs": "제품 SKU",
        "m² Factory Area": "m² 공장 면적",
        "OEM/ODM Water Filtration Excellence": "OEM/ODM 정수 필터 전문성",
        "State-of-the-Art Manufacturing": "첨단 제조",
        "Our Production Lines": "생산 라인",
        "Request a Quote · Bulk OEM Inquiry": "견적 요청 · 대량 OEM 문의",
        "← Back to All Products": "← 전체 제품으로 돌아가기",
        "Inquire Now": "지금 문의",
        "Request a Quote": "견적 요청",
    },
    "vi": {
        "View Product Catalog": "Xem danh mục sản phẩm",
        "Product SKUs": "Mã sản phẩm",
        "m² Factory Area": "m² diện tích nhà máy",
        "State-of-the-Art Manufacturing": "Sản xuất hiện đại",
        "Our Production Lines": "Dây chuyền sản xuất",
        "Request a Quote · Bulk OEM Inquiry": "Yêu cầu báo giá · Đơn OEM số lượng lớn",
        "← Back to All Products": "← Quay lại tất cả sản phẩm",
        "Inquire Now": "Gửi yêu cầu",
        "Request a Quote": "Yêu cầu báo giá",
    },
    "th": {
        "View Product Catalog": "ดูแค็ตตาล็อกผลิตภัณฑ์",
        "Product SKUs": "รหัสสินค้า",
        "m² Factory Area": "ม² พื้นที่โรงงาน",
        "State-of-the-Art Manufacturing": "การผลิตสมัยใหม่",
        "Our Production Lines": "สายการผลิตของเรา",
        "Request a Quote · Bulk OEM Inquiry": "ขอใบเสนอราคา · สอบถาม OEM จำนวนมาก",
        "← Back to All Products": "← กลับไปยังผลิตภัณฑ์ทั้งหมด",
        "Inquire Now": "สอบถามตอนนี้",
        "Request a Quote": "ขอใบเสนอราคา",
    },
}

RUSSIAN_GLOSSARY = {
    "Щелочной Water Очиститель Система": "Щелочная система очистки воды",
    "Antibacterial Mineralization Фильтр Картридж": "Антибактериальный минерализующий фильтрующий картридж",
    "30-inch Three Stage Big Blue Water Фильтр": "30-дюймовый трехступенчатый фильтр Big Blue",
    "CTO кокосовая скорлупа CTO Угольный Block Фильтр Картридж": "CTO фильтр-картридж из угольного блока кокосовой скорлупы",
    "Compressed Activated CTO Угольный Block": "Прессованный активированный CTO угольный блок",
    "Industrial High-Flow CTO Угольный Block Фильтр": "Промышленный высокопоточный CTO угольный фильтр",
    "Ceramic Фильтр Картридж": "Керамический фильтрующий картридж",
    "Multi-Stage Фильтр Картридж Combination": "Многоступенчатый комплект фильтрующих картриджей",
    "Flat Cap CTO Угольный Block Фильтр": "CTO угольный фильтр с плоской крышкой",
    "Flat Cap GAC Фильтр": "GAC фильтр с плоской крышкой",
    "Flat Cap PP Melt Blown Осадочный Фильтр": "PP melt-blown осадочный фильтр с плоской крышкой",
    "Alkaline Water Purifier System": "Щелочная система очистки воды",
    "Antibacterial Mineralization Filter Cartridge": "Антибактериальный минерализующий фильтрующий картридж",
    "30-inch Three Stage Big Blue Water Filter": "30-дюймовый трехступенчатый фильтр Big Blue",
    "CTO Coconut Shell CTO Carbon Block Filter Cartridge": "CTO фильтр-картридж из угольного блока кокосовой скорлупы",
    "Compressed Activated CTO Carbon Block": "Прессованный активированный CTO угольный блок",
    "Industrial High-Flow CTO Carbon Block Filter": "Промышленный высокопоточный CTO угольный фильтр",
    "Ceramic Filter Cartridge": "Керамический фильтрующий картридж",
    "Multi-Stage Filter Cartridge Combination": "Многоступенчатый комплект фильтрующих картриджей",
    "Flat Cap CTO Carbon Block Filter": "CTO угольный фильтр с плоской крышкой",
    "Flat Cap GAC Filter": "GAC фильтр с плоской крышкой",
    "Flat Cap PP Melt Blown Sediment Filter": "PP melt-blown осадочный фильтр с плоской крышкой",
    "PP Melt Blown Sediment Filter Cartridge": "PP melt-blown осадочный фильтрующий картридж",
    "RO Membrane": "RO-мембрана",
    "Water Dispenser": "Диспенсер воды",
    "Water Purifier": "Очиститель воды",
    "Filter Cartridge": "Фильтрующий картридж",
    "Filter Housing": "Корпус фильтра",
    "Carbon Block": "угольный блок",
    "Coconut Shell": "кокосовая скорлупа",
    "Quick-Connect": "быстросъемная сборка",
}


def page_lang(path: Path) -> str | None:
    try:
        return path.relative_to(ROOT).parts[0]
    except ValueError:
        return None


def fix_schema(text: str) -> str:
    text = re.sub(r'"@type"\s*:\s*"(?!FAQPage|WebPage)[^"]+Page"', '"@type": "FAQPage"', text)
    text = re.sub(
        r'itemtype="https://schema.org/(?!FAQPage|WebPage)[^"]+Page"',
        'itemtype="https://schema.org/FAQPage"',
        text,
    )
    return text


def fix_language_meta(text: str, lang: str) -> str:
    code, language_name = LANG_META.get(lang, (lang, lang))
    direction = "rtl" if lang in RTL_LANGS else "ltr"
    text = re.sub(r'<html lang="[^"]+" dir="[^"]+">', f'<html lang="{code}" dir="{direction}">', text, count=1)
    text = re.sub(r'<body class="(?:ltr|rtl)">', f'<body class="{direction}">', text, count=1)
    text = re.sub(r'<meta name="content-language" content="[^"]*" />', f'<meta name="content-language" content="{code}" />', text)
    text = re.sub(r'<meta name="dcterms.language" content="[^"]*" />', f'<meta name="dcterms.language" content="{language_name}" />', text)
    text = re.sub(
        r'<meta name="article:modified_time" content="[^"]*" />',
        f'<meta name="article:modified_time" content="{MODIFIED_DATE}T00:00:00+08:00" />',
        text,
    )
    text = re.sub(
        r'<meta name="last-modified" content="[^"]*" />',
        f'<meta name="last-modified" content="{MODIFIED_DATE}" />',
        text,
    )
    return text


def fix_html_syntax(text: str) -> str:
    text = re.sub(
        r'onclick="filterCat\("([^"]+)", this\)"',
        lambda match: f'onclick="filterCat(\'{match.group(1)}\', this)"',
        text,
    )
    text = text.replace(' required required', ' required')
    for _ in range(3):
        text = re.sub(r'(<(?:input|textarea)\b[^>]*?)\srequired(?=[^>]*\srequired)', r'\1', text)
    text = text.replace(' loading="lazy" / loading="lazy"', ' loading="lazy" decoding="async"')
    text = text.replace('  loading="lazy" / loading="lazy"', ' loading="lazy" decoding="async"')
    text = re.sub(r'(<img\b(?=[^>]*\sloading="lazy")(?![^>]*\sdecoding=)[^>]*?)\s*/?>', r'\1 decoding="async">', text)
    text = re.sub(r'<script src="https://www\.google\.com/recaptcha/api\.js\?render=YOUR_RECAPTCHA_SITE_KEY"></script>\n?', '', text)
    text = text.replace("grecaptcha.execute('YOUR_RECAPTCHA_SITE_KEY', {action: 'submit'})", "grecaptcha.execute('REPLACE_WITH_RECAPTCHA_SITE_KEY', {action: 'submit'})")
    return text


def add_image_dimensions_hint(text: str) -> str:
    # Avoid layout shift for repeated product/workshop thumbnails without
    # hard-coding actual pixels on every asset.
    text = text.replace(" / width=", " width=")
    return re.sub(
        r'(<img\b(?=[^>]*\ssrc="(?:\.\./)?assets/(?:products|workshop)/)(?![^>]*\swidth=)(?![^>]*\sheight=)[^>]*?)>',
        lambda match: f'{match.group(1).rstrip().removesuffix("/").rstrip()} width="640" height="480">',
        text,
    )


def localize_common_text(text: str, lang: str) -> str:
    for source, target in REPLACEMENTS.get(lang, {}).items():
        text = text.replace(source, target)
        text = text.replace(html.escape(source), html.escape(target))

    if lang == "ru":
        # Long product names are visible on cards, breadcrumbs, alt text and
        # JSON-LD names. Prefer specific phrases first, then leave technical
        # acronyms such as CTO, GAC, RO intact.
        for source, target in RUSSIAN_GLOSSARY.items():
            text = text.replace(source, target)
    return text


def rewrite_root_index() -> None:
    alternates = "\n".join(
        f'  <link rel="alternate" hreflang="{lang}" href="https://expresswater.cn/{lang}/index.html" />'
        for lang in LANGS
    )
    (ROOT / "index.html").write_text(
        f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Express Water | Water Filter Manufacturer & OEM/ODM Supplier</title>
  <meta name="description" content="Express Water is a China-based water filter manufacturer offering OEM/ODM filter cartridges, RO membranes, dispensers and industrial water purification solutions since 1998." />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://expresswater.cn/en/index.html" />
{alternates}
  <link rel="alternate" hreflang="x-default" href="https://expresswater.cn/en/index.html" />
  <meta http-equiv="refresh" content="2; url=en/index.html" />
  <script>
    (function() {{
      var supported = {LANGS!r};
      var preferred = (navigator.language || navigator.userLanguage || "en").slice(0, 2).toLowerCase();
      var lang = supported.indexOf(preferred) >= 0 ? preferred : "en";
      window.location.replace(lang + "/index.html");
    }})();
  </script>
</head>
<body>
  <main>
    <h1>Express Water</h1>
    <p>Global OEM/ODM water filtration manufacturer since 1998.</p>
    <p><a href="en/index.html">Continue to English site</a></p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )


def rewrite_legacy_root_pages() -> None:
    legacy_targets = {
        "homepage.html": ("en/index.html", "Express Water Home"),
        "product_page.html": ("en/products.html", "Express Water Products"),
        "inline.html": ("en/products.html", "Express Water Inline Filters"),
        "flat_cap.html": ("en/products.html", "Express Water Flat Cap Filters"),
    }
    for filename, (target, title) in legacy_targets.items():
        path = ROOT / filename
        if not path.exists():
            continue
        path.write_text(
            f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title} | Redirect</title>
  <meta name="robots" content="noindex, follow" />
  <link rel="canonical" href="https://expresswater.cn/{target}" />
  <meta http-equiv="refresh" content="0; url={target}" />
  <script>window.location.replace("{target}");</script>
</head>
<body>
  <main>
    <h1>{title}</h1>
    <p>This legacy page has moved to <a href="{target}">{target}</a>.</p>
  </main>
</body>
</html>
""",
            encoding="utf-8",
        )


def process_html() -> dict[str, int]:
    counts = {"files": 0, "changed": 0}
    for path in ROOT.rglob("*.html"):
        if path.name == "index.html" and path.parent == ROOT:
            continue
        lang = page_lang(path)
        original = path.read_text(encoding="utf-8", errors="ignore")
        text = original
        text = fix_schema(text)
        if lang in LANGS:
            text = fix_language_meta(text, lang)
            text = localize_common_text(text, lang)
        text = fix_html_syntax(text)
        text = add_image_dimensions_hint(text)
        if text != original:
            path.write_text(text, encoding="utf-8")
            counts["changed"] += 1
        counts["files"] += 1
    return counts


def update_sitemap_dates() -> None:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        return
    text = sitemap.read_text(encoding="utf-8")
    text = re.sub(r"<lastmod>[^<]+</lastmod>", f"<lastmod>{MODIFIED_DATE}</lastmod>", text)
    sitemap.write_text(text, encoding="utf-8")


def main() -> None:
    rewrite_root_index()
    rewrite_legacy_root_pages()
    counts = process_html()
    try:
        from deep_language_cleanup import deep_cleanup

        deep_counts = deep_cleanup()
    except Exception as exc:
        deep_counts = {"files": 0, "changed": 0}
        print(f"Deep language cleanup skipped: {exc}")
    update_sitemap_dates()
    print(f"Processed {counts['files']} HTML files; changed {counts['changed']} files.")
    print(f"Deep-cleaned {deep_counts['files']} HTML files; changed {deep_counts['changed']} files.")


if __name__ == "__main__":
    main()
