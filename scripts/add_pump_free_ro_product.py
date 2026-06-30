#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import re
import shutil
import zipfile
from datetime import date
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPORT_DIR = ROOT / "reports"
ASSET_DIR = ROOT / "assets" / "products"
PRODUCT_SLUG = "pump-free-five-stage-ro-water-purifier"
PRODUCT_FILE = f"product-{PRODUCT_SLUG}.html"
TODAY = date.today().isoformat()
ZIP_PATH = ROOT / f"yuchensy-github-pages-{TODAY}-pump-free-ro.zip"
REPORT_PATH = REPORT_DIR / f"pump-free-ro-product-verification-{TODAY}.txt"
CANONICAL_ROOT = "https://www.yuchensy.com"

SOURCES = [
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/221cd2ae294a3a607ef1d74ce52c4a18.jpg",
        f"{PRODUCT_SLUG}-front",
    ),
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d731e00f1ba00872bda1161199a7eaca.jpg",
        f"{PRODUCT_SLUG}-side",
    ),
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/93916567b05e102d773be16517bbcded.jpg",
        f"{PRODUCT_SLUG}-rear",
    ),
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d86e152609ff958ad8719b0888dbcb90.jpg",
        f"{PRODUCT_SLUG}-filter-housings",
    ),
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/05b8cd6ce9df259d93c6c7e54560d327.jpg",
        f"{PRODUCT_SLUG}-connection-detail",
    ),
    (
        "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/71fd19f5ccd4efb2fbdd1aeb043c3931.jpg",
        f"{PRODUCT_SLUG}-cartridge-set",
    ),
]

VIDEO_SOURCE = Path(
    "/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/video_1782469173627.mp4"
)
VIDEO_NAME = f"{PRODUCT_SLUG}-demo.mp4"

SKIP_DIRS = {
    ".git",
    ".github",
    ".codex",
    ".agents",
    "assets",
    "scripts",
    "reports",
    "node_modules",
    "__pycache__",
}

RTL_LANGS = {"ar", "fa", "he", "ku"}


CONTENT = {
    "en": {
        "lang_name": "English",
        "title": "Pump-Free Five Stage RO Water Purifier",
        "page_title": "Pump-Free Five Stage RO Water Purifier | Yuchen Water",
        "description": "Pump-free five stage RO water purifier for municipal tap water pressure, built for OEM private-label supply and compact household installation.",
        "summary": "This pump-free five stage RO water purifier works with municipal tap-water pressure, so it is suitable for markets where buyers want a quieter, lower-maintenance system without a booster pump. The filtration path combines PP sediment filtration, UDF/GAC adsorption, CTO carbon block polishing, an RO membrane and T33 post carbon for stable drinking-water purification. Yuchen Water supplies this model for distributors, importers and appliance brands that need OEM labels, packaging, faucet kits, tubing sets and market-specific configuration without keyword-heavy consumer wording.",
        "spec_title": "Technical Specifications",
        "process_title": "Filtration Process",
        "buyers_title": "Buyer Notes",
        "faq_title": "FAQ",
        "gallery_title": "Product Images and Video",
        "cta_quote": "Request OEM Quote",
        "cta_whatsapp": "WhatsApp Sales",
        "card_desc": "Pump-free five stage RO water purifier using tap-water pressure, PP/UDF/CTO/RO/T33 filtration and OEM private-label options for distributors.",
        "view": "View Product",
        "rows": {
            "Product type": "Pump-free five stage RO water purifier",
            "Working method": "Operates by municipal tap-water pressure, no booster pump",
            "Filtration stages": "PP sediment + UDF/GAC + CTO + RO membrane + T33 post carbon",
            "Pump": "No pump, lower noise and simpler service",
            "Inlet water": "Municipal tap water",
            "Installation": "Wall-mounted or under-sink according to project requirement",
            "Application": "Household drinking water, apartment projects, replacement cartridge market",
            "OEM/ODM": "Logo, label, faucet set, tubing, packaging and instruction sheet",
            "MOQ": "Discuss by specification and packaging plan",
        },
        "process": [
            "The PP sediment cartridge captures visible particles, rust and sand before the water reaches the carbon stages.",
            "The UDF/GAC and CTO carbon stages help reduce chlorine, odor and organic taste while protecting the RO membrane.",
            "The RO membrane performs fine separation for dissolved solids, and the T33 post carbon improves the final taste before dispensing.",
        ],
        "buyers": "For B2B orders, the filter sequence, cartridge label, bracket, tubing color, faucet style, carton artwork and spare-part kit can be adjusted to the target market. The model is recommended when importers want a simple RO water purifier supplier option that avoids pump noise and reduces electrical components.",
        "faq": [
            ("Does this RO purifier need a booster pump?", "No. It is designed to run by municipal tap-water pressure when the local inlet pressure is suitable."),
            ("What are the five filtration stages?", "PP sediment, UDF/GAC carbon, CTO carbon block, RO membrane and T33 post carbon."),
            ("Can the labels and carton be customized?", "Yes. OEM label, logo, user manual and export carton design can be prepared for distributors."),
            ("Which buyers is this model suitable for?", "It suits wholesalers, importers, replacement-filter sellers and household appliance brands."),
            ("Can it be supplied with different faucet or tubing kits?", "Yes. Faucet style, tubing length and connector set can be matched to the buyer's market."),
            ("How should MOQ be confirmed?", "MOQ depends on label, packaging and accessory customization, so it is confirmed by final specification."),
        ],
    },
    "ru": {
        "lang_name": "Русский",
        "title": "Пятиступенчатая RO-система без насоса",
        "page_title": "Пятиступенчатая RO-система без насоса | Yuchen Water",
        "description": "Пятиступенчатая RO-система без насоса работает от давления водопровода и подходит для OEM-поставок бытовых фильтров.",
        "summary": "Эта пятиступенчатая RO-система без насоса работает от давления городской водопроводной воды, поэтому подходит для рынков, где важны тихая работа, простое обслуживание и меньше электрических узлов. В системе используются PP-фильтр для осадка, UDF/GAC, CTO, RO-мембрана и постфильтр T33. Yuchen Water поставляет такую модель для дистрибьюторов, импортеров и брендов бытовой техники с индивидуальной этикеткой, упаковкой, комплектом крана, трубками и документацией под требования рынка.",
        "spec_title": "Технические характеристики",
        "process_title": "Процесс фильтрации",
        "buyers_title": "Информация для закупщиков",
        "faq_title": "Вопросы и ответы",
        "gallery_title": "Изображения и видео продукта",
        "cta_quote": "Запросить OEM-предложение",
        "cta_whatsapp": "Продажи в WhatsApp",
        "card_desc": "Пятиступенчатая RO-система без насоса работает от давления водопровода и поддерживает OEM-этикетки, упаковку и комплектацию.",
        "view": "Смотреть продукт",
        "rows": {
            "Тип продукта": "Пятиступенчатая RO-система без насоса",
            "Принцип работы": "Работа от давления городской водопроводной воды, без бустерного насоса",
            "Ступени фильтрации": "PP осадочный фильтр + UDF/GAC + CTO + RO-мембрана + T33",
            "Насос": "Без насоса, ниже шум и проще обслуживание",
            "Входная вода": "Городская водопроводная вода",
            "Монтаж": "Настенный или под мойку по требованию проекта",
            "Применение": "Бытовая питьевая вода, квартирные проекты, рынок сменных картриджей",
            "OEM/ODM": "Логотип, этикетка, кран, трубки, упаковка и инструкция",
            "MOQ": "Согласуется по спецификации и упаковке",
        },
        "process": [
            "PP-картридж задерживает видимые частицы, ржавчину и песок перед угольными ступенями.",
            "UDF/GAC и CTO помогают снизить хлор, запах и органический привкус, защищая RO-мембрану.",
            "RO-мембрана выполняет тонкое разделение растворенных солей, а T33 улучшает вкус готовой воды.",
        ],
        "buyers": "Для B2B-заказов можно адаптировать последовательность фильтров, этикетку картриджа, кронштейн, цвет трубок, кран, дизайн коробки и комплект запчастей. Модель подходит импортерам, которым нужна простая RO-система без шума насоса и с меньшим числом электрических компонентов.",
        "faq": [
            ("Нужен ли этой системе бустерный насос?", "Нет. Она рассчитана на работу от давления водопровода при подходящем входном давлении."),
            ("Какие пять ступеней фильтрации используются?", "PP, UDF/GAC, CTO, RO-мембрана и постфильтр T33."),
            ("Можно ли настроить этикетки и коробку?", "Да. Мы готовим OEM-этикетку, логотип, инструкцию и экспортную коробку."),
            ("Для каких покупателей подходит эта модель?", "Для оптовиков, импортеров, продавцов сменных фильтров и брендов бытовой техники."),
            ("Можно ли изменить кран или комплект трубок?", "Да. Тип крана, длина трубок и набор фитингов подбираются под рынок покупателя."),
            ("Как подтвердить MOQ?", "MOQ зависит от этикетки, упаковки и аксессуаров, поэтому подтверждается по финальной спецификации."),
        ],
    },
    "es": {
        "lang_name": "Español",
        "title": "Purificador RO de cinco etapas sin bomba",
        "page_title": "Purificador RO de cinco etapas sin bomba | Yuchen Water",
        "description": "Purificador RO de cinco etapas sin bomba para presión de agua municipal, con suministro OEM para distribuidores.",
        "summary": "Este purificador RO de cinco etapas sin bomba funciona con la presión del agua municipal, por lo que es una opción silenciosa y de bajo mantenimiento para mercados que no requieren bomba de refuerzo. La ruta de filtración combina PP para sedimentos, UDF/GAC, CTO, membrana RO y postcarbono T33. Yuchen Water lo suministra a distribuidores, importadores y marcas que necesitan etiquetas privadas, embalaje, grifo, tubos y configuración adaptada al mercado.",
        "spec_title": "Especificaciones técnicas",
        "process_title": "Proceso de filtración",
        "buyers_title": "Notas para compradores",
        "faq_title": "Preguntas frecuentes",
        "gallery_title": "Imágenes y video del producto",
        "cta_quote": "Solicitar cotización OEM",
        "cta_whatsapp": "Ventas por WhatsApp",
        "card_desc": "Purificador RO de cinco etapas sin bomba, accionado por presión de red, con filtración PP/UDF/CTO/RO/T33 y opciones OEM.",
        "view": "Ver producto",
        "rows": {
            "Tipo de producto": "Purificador RO de cinco etapas sin bomba",
            "Método de trabajo": "Funciona con presión de agua municipal, sin bomba de refuerzo",
            "Etapas de filtración": "PP sedimento + UDF/GAC + CTO + membrana RO + T33",
            "Bomba": "Sin bomba, menos ruido y mantenimiento más simple",
            "Agua de entrada": "Agua municipal",
            "Instalación": "Mural o bajo fregadero según el proyecto",
            "Aplicación": "Agua potable doméstica, proyectos de apartamentos, mercado de cartuchos",
            "OEM/ODM": "Logotipo, etiqueta, grifo, tubos, embalaje e instrucciones",
            "MOQ": "Se confirma según especificación y embalaje",
        },
        "process": [
            "El cartucho PP retiene partículas visibles, óxido y arena antes de las etapas de carbón.",
            "UDF/GAC y CTO ayudan a reducir cloro, olor y sabor orgánico, protegiendo la membrana RO.",
            "La membrana RO separa sólidos disueltos finos y el T33 mejora el sabor final del agua.",
        ],
        "buyers": "Para pedidos B2B se pueden ajustar la secuencia de filtros, etiqueta, soporte, color de tubos, grifo, diseño de caja y repuestos. Es una opción adecuada para importadores que desean un proveedor de purificadores RO sencillo, silencioso y con menos componentes eléctricos.",
        "faq": [
            ("¿Necesita bomba de refuerzo?", "No. Está diseñado para trabajar con presión municipal cuando la presión de entrada es adecuada."),
            ("¿Cuáles son las cinco etapas?", "PP, UDF/GAC, CTO, membrana RO y postcarbono T33."),
            ("¿Se puede personalizar la caja?", "Sí. Podemos preparar etiqueta OEM, logotipo, manual y caja de exportación."),
            ("¿Para qué compradores es adecuado?", "Para mayoristas, importadores, vendedores de recambios y marcas de electrodomésticos."),
            ("¿Se puede cambiar el grifo o los tubos?", "Sí. El grifo, la longitud de tubos y conectores se adaptan al mercado."),
            ("¿Cómo se confirma el MOQ?", "Depende de la etiqueta, embalaje y accesorios finales."),
        ],
    },
    "de": {
        "lang_name": "Deutsch",
        "title": "Pumpenloser fünfstufiger RO-Wasserreiniger",
        "page_title": "Pumpenloser fünfstufiger RO-Wasserreiniger | Yuchen Water",
        "description": "Pumpenloser fünfstufiger RO-Wasserreiniger für Leitungswasserdruck, geeignet für OEM-Lieferung und Privatlabel.",
        "summary": "Dieser pumpenlose fünfstufige RO-Wasserreiniger arbeitet mit dem Druck des städtischen Leitungswassers und eignet sich für Märkte, in denen leiser Betrieb, einfache Wartung und weniger elektrische Bauteile wichtig sind. Die Filtration kombiniert PP-Sediment, UDF/GAC, CTO, RO-Membran und T33-Nachkohle. Yuchen Water liefert dieses Modell für Distributoren, Importeure und Gerätemarken mit Privatlabel, Verpackung, Armatur, Schlauchset und marktspezifischer Konfiguration.",
        "spec_title": "Technische Daten",
        "process_title": "Filtrationsprozess",
        "buyers_title": "Hinweise für Käufer",
        "faq_title": "Häufige Fragen",
        "gallery_title": "Produktbilder und Video",
        "cta_quote": "OEM-Angebot anfragen",
        "cta_whatsapp": "WhatsApp-Vertrieb",
        "card_desc": "Pumpenloser fünfstufiger RO-Wasserreiniger für Leitungswasserdruck mit PP/UDF/CTO/RO/T33-Filtration und OEM-Optionen.",
        "view": "Produkt ansehen",
        "rows": {
            "Produkttyp": "Pumpenloser fünfstufiger RO-Wasserreiniger",
            "Arbeitsweise": "Betrieb über städtischen Leitungswasserdruck, ohne Boosterpumpe",
            "Filtrationsstufen": "PP-Sediment + UDF/GAC + CTO + RO-Membran + T33",
            "Pumpe": "Ohne Pumpe, geringere Geräusche und einfachere Wartung",
            "Zulaufwasser": "Städtisches Leitungswasser",
            "Installation": "Wandmontage oder Untertisch je nach Projekt",
            "Anwendung": "Trinkwasser im Haushalt, Wohnprojekte, Ersatzkartuschenmarkt",
            "OEM/ODM": "Logo, Etikett, Armatur, Schläuche, Verpackung und Anleitung",
            "MOQ": "Nach Spezifikation und Verpackung zu bestätigen",
        },
        "process": [
            "Die PP-Sedimentkartusche hält sichtbare Partikel, Rost und Sand zurück.",
            "UDF/GAC und CTO reduzieren Chlor, Geruch und organischen Geschmack und schützen die RO-Membran.",
            "Die RO-Membran trennt gelöste Stoffe fein ab, T33 verbessert den finalen Geschmack.",
        ],
        "buyers": "Für B2B-Aufträge lassen sich Filterfolge, Kartuschenetikett, Halterung, Schlauchfarbe, Armatur, Kartongestaltung und Ersatzteilset anpassen. Das Modell passt zu Importeuren, die eine einfache RO-Lösung ohne Pumpengeräusch und mit weniger elektrischen Komponenten suchen.",
        "faq": [
            ("Benötigt das Gerät eine Boosterpumpe?", "Nein. Es arbeitet bei passendem Eingangsdruck mit dem Leitungswasserdruck."),
            ("Welche fünf Stufen enthält es?", "PP, UDF/GAC, CTO, RO-Membran und T33-Nachkohle."),
            ("Sind Etikett und Karton anpassbar?", "Ja. OEM-Etikett, Logo, Anleitung und Exportkarton sind möglich."),
            ("Für welche Käufer ist es geeignet?", "Für Großhändler, Importeure, Ersatzfilteranbieter und Gerätemarken."),
            ("Können Armatur und Schläuche geändert werden?", "Ja. Armatur, Schlauchlänge und Fittings werden marktspezifisch gewählt."),
            ("Wie wird die MOQ bestätigt?", "Sie hängt von Etikett, Verpackung und Zubehör ab."),
        ],
    },
    "fr": {
        "lang_name": "Français",
        "title": "Purificateur RO cinq étapes sans pompe",
        "page_title": "Purificateur RO cinq étapes sans pompe | Yuchen Water",
        "description": "Purificateur RO cinq étapes sans pompe fonctionnant avec la pression du réseau, adapté aux commandes OEM.",
        "summary": "Ce purificateur RO cinq étapes sans pompe fonctionne avec la pression de l'eau du réseau municipal. Il convient aux marchés où les acheteurs recherchent une solution silencieuse, simple à entretenir et avec moins de composants électriques. Le circuit associe PP sédiment, UDF/GAC, CTO, membrane RO et post-charbon T33. Yuchen Water fournit ce modèle aux distributeurs, importateurs et marques avec étiquette privée, emballage, robinet, tubes et configuration adaptée au marché.",
        "spec_title": "Caractéristiques techniques",
        "process_title": "Processus de filtration",
        "buyers_title": "Notes pour acheteurs",
        "faq_title": "FAQ",
        "gallery_title": "Images et vidéo du produit",
        "cta_quote": "Demander un devis OEM",
        "cta_whatsapp": "Ventes WhatsApp",
        "card_desc": "Purificateur RO cinq étapes sans pompe, alimenté par la pression du réseau, avec filtration PP/UDF/CTO/RO/T33 et options OEM.",
        "view": "Voir le produit",
        "rows": {
            "Type de produit": "Purificateur RO cinq étapes sans pompe",
            "Mode de fonctionnement": "Fonctionne avec la pression du réseau, sans pompe booster",
            "Étapes de filtration": "PP sédiment + UDF/GAC + CTO + membrane RO + T33",
            "Pompe": "Sans pompe, moins de bruit et maintenance plus simple",
            "Eau d'entrée": "Eau du réseau municipal",
            "Installation": "Murale ou sous évier selon le projet",
            "Application": "Eau potable domestique, projets résidentiels, marché des cartouches",
            "OEM/ODM": "Logo, étiquette, robinet, tubes, emballage et notice",
            "MOQ": "À confirmer selon la spécification et l'emballage",
        },
        "process": [
            "La cartouche PP retient particules visibles, rouille et sable avant les étapes carbone.",
            "UDF/GAC et CTO réduisent chlore, odeur et goût organique tout en protégeant la membrane RO.",
            "La membrane RO sépare les solides dissous, puis T33 améliore le goût final.",
        ],
        "buyers": "Pour les commandes B2B, la séquence des filtres, l'étiquette, le support, la couleur des tubes, le robinet, le carton et le kit de pièces peuvent être adaptés. Ce modèle est recommandé aux importateurs qui veulent une solution RO simple, sans bruit de pompe et avec moins de composants électriques.",
        "faq": [
            ("Faut-il une pompe booster ?", "Non. Le système fonctionne avec la pression du réseau lorsque l'entrée est adaptée."),
            ("Quelles sont les cinq étapes ?", "PP, UDF/GAC, CTO, membrane RO et post-charbon T33."),
            ("L'emballage peut-il être personnalisé ?", "Oui. Étiquette OEM, logo, notice et carton export peuvent être préparés."),
            ("À quels acheteurs convient-il ?", "Aux grossistes, importateurs, vendeurs de recharges et marques d'électroménager."),
            ("Le robinet ou les tubes peuvent-ils changer ?", "Oui. Le robinet, la longueur des tubes et les raccords sont adaptés au marché."),
            ("Comment confirmer la MOQ ?", "Elle dépend de l'étiquette, de l'emballage et des accessoires finaux."),
        ],
    },
    "vi": {
        "lang_name": "Tiếng Việt",
        "title": "Máy lọc nước RO năm cấp không dùng bơm",
        "page_title": "Máy lọc nước RO năm cấp không dùng bơm | Yuchen Water",
        "description": "Máy lọc nước RO năm cấp không dùng bơm, vận hành bằng áp lực nước máy và phù hợp cung ứng OEM.",
        "summary": "Máy lọc nước RO năm cấp không dùng bơm này vận hành bằng áp lực nước máy đô thị, phù hợp với thị trường cần thiết bị êm, dễ bảo trì và ít linh kiện điện hơn. Hệ lọc gồm lõi PP chặn cặn, UDF/GAC, CTO, màng RO và than hậu T33. Yuchen Water cung cấp mẫu này cho nhà phân phối, nhà nhập khẩu và thương hiệu thiết bị gia dụng với nhãn riêng, bao bì, bộ vòi, ống dẫn và cấu hình theo từng thị trường.",
        "spec_title": "Thông số kỹ thuật",
        "process_title": "Quy trình lọc",
        "buyers_title": "Ghi chú cho người mua",
        "faq_title": "Câu hỏi thường gặp",
        "gallery_title": "Hình ảnh và video sản phẩm",
        "cta_quote": "Yêu cầu báo giá OEM",
        "cta_whatsapp": "Bán hàng WhatsApp",
        "card_desc": "Máy lọc nước RO năm cấp không dùng bơm, dùng áp lực nước máy, lọc PP/UDF/CTO/RO/T33 và hỗ trợ OEM.",
        "view": "Xem sản phẩm",
        "rows": {
            "Loại sản phẩm": "Máy lọc nước RO năm cấp không dùng bơm",
            "Cách vận hành": "Dùng áp lực nước máy đô thị, không cần bơm tăng áp",
            "Cấp lọc": "PP cặn + UDF/GAC + CTO + màng RO + T33",
            "Bơm": "Không bơm, ít ồn và dễ bảo trì hơn",
            "Nguồn nước": "Nước máy đô thị",
            "Lắp đặt": "Treo tường hoặc dưới bồn rửa theo dự án",
            "Ứng dụng": "Nước uống gia đình, dự án căn hộ, thị trường lõi thay thế",
            "OEM/ODM": "Logo, nhãn, vòi, ống, bao bì và hướng dẫn",
            "MOQ": "Xác nhận theo cấu hình và bao bì",
        },
        "process": [
            "Lõi PP giữ cặn nhìn thấy, rỉ sét và cát trước các cấp than.",
            "UDF/GAC và CTO giảm clo, mùi và vị hữu cơ, đồng thời bảo vệ màng RO.",
            "Màng RO tách chất rắn hòa tan, T33 cải thiện vị nước sau cùng.",
        ],
        "buyers": "Đơn hàng B2B có thể tùy chỉnh thứ tự lõi, nhãn lõi, giá đỡ, màu ống, kiểu vòi, thùng carton và bộ phụ tùng. Mẫu này phù hợp cho nhà nhập khẩu cần giải pháp RO đơn giản, ít tiếng ồn và ít linh kiện điện.",
        "faq": [
            ("Máy có cần bơm tăng áp không?", "Không. Máy dùng áp lực nước máy khi áp lực đầu vào phù hợp."),
            ("Năm cấp lọc gồm những gì?", "PP, UDF/GAC, CTO, màng RO và than hậu T33."),
            ("Có thể làm nhãn và thùng riêng không?", "Có. Có thể chuẩn bị nhãn OEM, logo, hướng dẫn và thùng xuất khẩu."),
            ("Mẫu này phù hợp với ai?", "Phù hợp nhà bán buôn, nhà nhập khẩu, nhà bán lõi thay thế và thương hiệu thiết bị gia dụng."),
            ("Có đổi vòi hoặc ống được không?", "Có. Kiểu vòi, chiều dài ống và bộ nối được chọn theo thị trường."),
            ("MOQ xác nhận thế nào?", "MOQ phụ thuộc nhãn, bao bì và phụ kiện cuối cùng."),
        ],
    },
    "ja": {
        "lang_name": "日本語",
        "title": "ポンプレス五段RO浄水器",
        "page_title": "ポンプレス五段RO浄水器 | Yuchen Water",
        "description": "水道圧で作動するポンプレス五段RO浄水器。OEM供給とプライベートラベルに対応します。",
        "summary": "このポンプレス五段RO浄水器は、水道水の圧力で作動するため、静音性、保守のしやすさ、電装部品の少なさを重視する市場に適しています。ろ過構成はPP沈殿フィルター、UDF/GAC、CTO、RO膜、T33後置カーボンです。Yuchen Waterは、販売代理店、輸入業者、家電ブランド向けに、ラベル、包装、蛇口、チューブ、取扱説明書を市場仕様に合わせて供給します。",
        "spec_title": "技術仕様",
        "process_title": "ろ過プロセス",
        "buyers_title": "バイヤー向け情報",
        "faq_title": "よくある質問",
        "gallery_title": "製品画像と動画",
        "cta_quote": "OEM見積を依頼",
        "cta_whatsapp": "WhatsAppで相談",
        "card_desc": "水道圧で作動するポンプレス五段RO浄水器。PP/UDF/CTO/RO/T33構成でOEM仕様に対応します。",
        "view": "製品を見る",
        "rows": {
            "製品タイプ": "ポンプレス五段RO浄水器",
            "作動方式": "水道圧で作動、ブースターポンプなし",
            "ろ過段数": "PP沈殿 + UDF/GAC + CTO + RO膜 + T33",
            "ポンプ": "ポンプなし、低騒音で保守が簡単",
            "原水": "市政水道水",
            "設置": "壁掛けまたはシンク下、案件仕様に対応",
            "用途": "家庭用飲料水、集合住宅案件、交換カートリッジ市場",
            "OEM/ODM": "ロゴ、ラベル、蛇口、チューブ、包装、説明書",
            "MOQ": "仕様と包装内容により確認",
        },
        "process": [
            "PPカートリッジは目に見える粒子、さび、砂を前段で捕捉します。",
            "UDF/GACとCTOは塩素、におい、有機的な味を低減し、RO膜を保護します。",
            "RO膜が溶解物質を細かく分離し、T33が最後の味を整えます。",
        ],
        "buyers": "B2B注文では、ろ過順序、カートリッジラベル、ブラケット、チューブ色、蛇口、箱デザイン、予備部品キットを調整できます。ポンプ音を避け、電装部品を減らしたい輸入業者に適したRO浄水器です。",
        "faq": [
            ("ブースターポンプは必要ですか。", "いいえ。適切な水道圧がある場合、水道圧で作動します。"),
            ("五段ろ過の内容は何ですか。", "PP、UDF/GAC、CTO、RO膜、T33後置カーボンです。"),
            ("ラベルや箱は変更できますか。", "はい。OEMラベル、ロゴ、説明書、輸出箱を準備できます。"),
            ("どのような買い手に向いていますか。", "卸売業者、輸入業者、交換フィルター販売者、家電ブランドに適しています。"),
            ("蛇口やチューブは変更できますか。", "はい。蛇口、チューブ長さ、接続部品を市場に合わせられます。"),
            ("MOQはどう決まりますか。", "ラベル、包装、付属品の最終仕様により確認します。"),
        ],
    },
    "uz": {
        "lang_name": "O'zbekcha",
        "title": "Nasossiz besh bosqichli RO suv tozalagich",
        "page_title": "Nasossiz besh bosqichli RO suv tozalagich | Yuchen Water",
        "description": "Shahar suv bosimi bilan ishlaydigan nasossiz besh bosqichli RO suv tozalagich, OEM yetkazib berish uchun.",
        "summary": "Ushbu nasossiz besh bosqichli RO suv tozalagich shahar vodoprovod bosimi bilan ishlaydi. Shu sababli u sokin ishlash, oson servis va kamroq elektr qismlarini xohlaydigan bozorlar uchun mos. Filtrlash yo‘li PP cho‘kindi filtri, UDF/GAC, CTO, RO membrana va T33 yakuniy karbon bosqichidan iborat. Yuchen Water distribyutorlar, importchilar va maishiy texnika brendlari uchun xususiy yorliq, qadoq, kran, trubka va bozor talabiga mos konfiguratsiya bilan yetkazib beradi.",
        "spec_title": "Texnik xususiyatlar",
        "process_title": "Filtrlash jarayoni",
        "buyers_title": "Xaridorlar uchun eslatma",
        "faq_title": "Savol-javob",
        "gallery_title": "Mahsulot rasmlari va video",
        "cta_quote": "OEM narx so‘rash",
        "cta_whatsapp": "WhatsApp savdo",
        "card_desc": "Shahar suv bosimida ishlaydigan nasossiz besh bosqichli RO suv tozalagich, PP/UDF/CTO/RO/T33 va OEM variantlari bilan.",
        "view": "Mahsulotni ko‘rish",
        "rows": {
            "Mahsulot turi": "Nasossiz besh bosqichli RO suv tozalagich",
            "Ishlash usuli": "Shahar suv bosimi bilan, booster nasossiz",
            "Filtrlash bosqichlari": "PP cho‘kindi + UDF/GAC + CTO + RO membrana + T33",
            "Nasos": "Nasossiz, shovqini kam va servis oson",
            "Kirish suvi": "Shahar vodoprovod suvi",
            "O‘rnatish": "Devorga yoki rakovina ostiga loyiha bo‘yicha",
            "Qo‘llanish": "Uy ichimlik suvi, kvartira loyihalari, almashtiriladigan kartrij bozori",
            "OEM/ODM": "Logo, yorliq, kran, trubka, qadoq va yo‘riqnoma",
            "MOQ": "Xususiyat va qadoq bo‘yicha kelishiladi",
        },
        "process": [
            "PP kartrij ko‘rinadigan zarra, zang va qumni ushlab qoladi.",
            "UDF/GAC va CTO xlor, hid va organik ta’mni kamaytirib, RO membranani himoya qiladi.",
            "RO membrana erigan moddalarni ajratadi, T33 esa yakuniy ta’mni yaxshilaydi.",
        ],
        "buyers": "B2B buyurtmalarda filtr ketma-ketligi, kartrij yorlig‘i, kronshteyn, trubka rangi, kran, quti dizayni va ehtiyot qismlar to‘plami moslashtiriladi. Model nasos shovqinini kamaytirishni istagan importchilar uchun qulay RO yechimidir.",
        "faq": [
            ("Booster nasos kerakmi?", "Yo‘q. Kirish bosimi mos bo‘lsa, tizim vodoprovod bosimida ishlaydi."),
            ("Besh bosqich nimalardan iborat?", "PP, UDF/GAC, CTO, RO membrana va T33."),
            ("Yorliq va quti moslashtiriladimi?", "Ha. OEM yorliq, logo, qo‘llanma va eksport qutisi tayyorlanadi."),
            ("Kimlar uchun mos?", "Ulgurji xaridorlar, importchilar, kartrij sotuvchilari va brendlar uchun."),
            ("Kran yoki trubka o‘zgaradimi?", "Ha. Kran turi, trubka uzunligi va ulagichlar bozorga moslanadi."),
            ("MOQ qanday tasdiqlanadi?", "Yakuniy yorliq, qadoq va aksessuarlarga bog‘liq."),
        ],
    },
    "kk": {
        "lang_name": "Қазақша",
        "title": "Сорғысыз бес сатылы RO су тазартқыш",
        "page_title": "Сорғысыз бес сатылы RO су тазартқыш | Yuchen Water",
        "description": "Қалалық су қысымымен жұмыс істейтін сорғысыз бес сатылы RO су тазартқыш, OEM жеткізуге қолайлы.",
        "summary": "Бұл сорғысыз бес сатылы RO су тазартқыш қалалық су құбырының қысымымен жұмыс істейді. Сондықтан ол тыныш жұмыс, жеңіл қызмет көрсету және электр тораптарының аз болуын қалайтын нарықтарға қолайлы. Жүйеде PP тұнба сүзгісі, UDF/GAC, CTO, RO мембранасы және T33 соңғы көмір сатысы бар. Yuchen Water бұл модельді дистрибьюторлар, импорттаушылар және тұрмыстық техника брендтері үшін жеке жапсырма, қаптама, кран, түтік және нарыққа бейімделген жинақпен жеткізеді.",
        "spec_title": "Техникалық сипаттамалар",
        "process_title": "Сүзу процесі",
        "buyers_title": "Сатып алушыларға ақпарат",
        "faq_title": "Жиі қойылатын сұрақтар",
        "gallery_title": "Өнім суреттері және видео",
        "cta_quote": "OEM баға сұрау",
        "cta_whatsapp": "WhatsApp сату",
        "card_desc": "Қалалық су қысымымен жұмыс істейтін сорғысыз бес сатылы RO су тазартқыш, PP/UDF/CTO/RO/T33 және OEM мүмкіндіктерімен.",
        "view": "Өнімді көру",
        "rows": {
            "Өнім түрі": "Сорғысыз бес сатылы RO су тазартқыш",
            "Жұмыс тәсілі": "Қалалық су қысымымен, бустер сорғысыз",
            "Сүзу сатылары": "PP тұнба + UDF/GAC + CTO + RO мембрана + T33",
            "Сорғы": "Сорғысыз, шу аз және қызмет көрсету оңай",
            "Кіріс су": "Қалалық су құбыры",
            "Орнату": "Қабырғаға немесе раковина астына, жоба талабына сай",
            "Қолдану": "Үй ішетін суы, пәтер жобалары, ауыстырмалы картридж нарығы",
            "OEM/ODM": "Логотип, жапсырма, кран, түтік, қаптама және нұсқаулық",
            "MOQ": "Сипаттама мен қаптама бойынша келісіледі",
        },
        "process": [
            "PP картриджі көрінетін бөлшек, тот және құмды ұстайды.",
            "UDF/GAC және CTO хлорды, иісті және органикалық дәмді азайтып, RO мембранасын қорғайды.",
            "RO мембранасы еріген заттарды бөледі, T33 соңғы дәмді жақсартады.",
        ],
        "buyers": "B2B тапсырыстарында сүзгі реті, картридж жапсырмасы, кронштейн, түтік түсі, кран, қорап дизайны және қосалқы бөлшек жиынтығы бейімделеді. Бұл модель сорғы шусыз қарапайым RO шешімін іздейтін импорттаушыларға ыңғайлы.",
        "faq": [
            ("Бустер сорғы керек пе?", "Жоқ. Кіріс қысымы жеткілікті болса, жүйе су құбыры қысымымен жұмыс істейді."),
            ("Бес саты қандай?", "PP, UDF/GAC, CTO, RO мембрана және T33."),
            ("Жапсырма мен қорапты өзгертуге бола ма?", "Иә. OEM жапсырма, логотип, нұсқаулық және экспорт қорабы дайындалады."),
            ("Қай сатып алушыларға қолайлы?", "Көтерме саудагерлерге, импорттаушыларға, картридж сатушыларға және брендтерге."),
            ("Кран немесе түтік өзгертіле ме?", "Иә. Кран түрі, түтік ұзындығы және жалғағыштар нарыққа бейімделеді."),
            ("MOQ қалай расталады?", "Соңғы жапсырма, қаптама және аксессуарларға байланысты."),
        ],
    },
    "ky": {
        "lang_name": "Кыргызча",
        "title": "Насоссуз беш баскычтуу RO суу тазалагыч",
        "page_title": "Насоссуз беш баскычтуу RO суу тазалагыч | Yuchen Water",
        "description": "Шаардык суу басымы менен иштеген насоссуз беш баскычтуу RO суу тазалагыч, OEM жеткирүүгө ылайыктуу.",
        "summary": "Бул насоссуз беш баскычтуу RO суу тазалагыч шаардык суу түтүгүнүн басымы менен иштейт. Ошондуктан ал тынч иштөө, жөнөкөй тейлөө жана электр бөлүктөрүнүн аз болушун каалаган рынокторго туура келет. Система PP чөкмө чыпкасы, UDF/GAC, CTO, RO мембранасы жана T33 акыркы көмүр баскычынан турат. Yuchen Water бул моделди дистрибьюторлорго, импортчуларга жана тиричилик техника бренддерине жеке этикетка, таңгак, кран, түтүк жана рынокко ылайык комплектация менен берет.",
        "spec_title": "Техникалык мүнөздөмөлөр",
        "process_title": "Чыпкалоо процесси",
        "buyers_title": "Сатып алуучулар үчүн маалымат",
        "faq_title": "Суроо-жооп",
        "gallery_title": "Өнүм сүрөттөрү жана видео",
        "cta_quote": "OEM баа суроо",
        "cta_whatsapp": "WhatsApp сатуу",
        "card_desc": "Шаардык суу басымы менен иштеген насоссуз беш баскычтуу RO суу тазалагыч, PP/UDF/CTO/RO/T33 жана OEM мүмкүнчүлүктөрү менен.",
        "view": "Өнүмдү көрүү",
        "rows": {
            "Өнүм түрү": "Насоссуз беш баскычтуу RO суу тазалагыч",
            "Иштөө жолу": "Шаардык суу басымы менен, бустер насос жок",
            "Чыпкалоо баскычтары": "PP чөкмө + UDF/GAC + CTO + RO мембрана + T33",
            "Насос": "Насоссуз, үнү аз жана тейлөө жеңил",
            "Кирүүчү суу": "Шаардык суу түтүгү",
            "Орнотуу": "Дубалга же раковина астына, долбоорго жараша",
            "Колдонуу": "Үй ичүүчү суусу, батир долбоорлору, алмашма картридж рыногу",
            "OEM/ODM": "Логотип, этикетка, кран, түтүк, таңгак жана нускама",
            "MOQ": "Мүнөздөмө жана таңгак боюнча макулдашылат",
        },
        "process": [
            "PP картриджи көрүнгөн бөлүкчө, дат жана кумду кармайт.",
            "UDF/GAC жана CTO хлорду, жытты жана органикалык даамды азайтып, RO мембранасын коргойт.",
            "RO мембранасы эриген заттарды бөлөт, T33 акыркы даамды жакшыртат.",
        ],
        "buyers": "B2B буйрутмаларында чыпка тартиби, картридж этикеткасы, кронштейн, түтүк түсү, кран, куту дизайны жана запастык бөлүк топтому ылайыкташтырылат. Модель насостун үнүн азайтып, жөнөкөй RO чечимин каалаган импортчуларга ылайыктуу.",
        "faq": [
            ("Бустер насос керекпи?", "Жок. Кирүүчү басым ылайыктуу болсо, система суу түтүгүнүн басымы менен иштейт."),
            ("Беш баскыч эмнелерден турат?", "PP, UDF/GAC, CTO, RO мембрана жана T33."),
            ("Этикетка жана куту өзгөрөбү?", "Ооба. OEM этикетка, логотип, нускама жана экспорт кутусу даярдалат."),
            ("Кимдерге ылайыктуу?", "Дүң сатып алуучуларга, импортчуларга, картридж сатуучуларга жана бренддерге."),
            ("Кран же түтүк өзгөрөбү?", "Ооба. Кран түрү, түтүк узундугу жана туташтыргычтар рынокко ылайыкталат."),
            ("MOQ кантип бекитилет?", "Акыркы этикетка, таңгак жана аксессуарларга жараша."),
        ],
    },
}

FALLBACKS = {
    "ar": {
        "lang_name": "العربية",
        "title": "جهاز تنقية RO بخمس مراحل بدون مضخة",
        "page_title": "جهاز تنقية RO بخمس مراحل بدون مضخة | Yuchen Water",
        "description": "جهاز RO بخمس مراحل يعمل بضغط مياه البلدية دون مضخة، مناسب لتوريد OEM.",
        "summary": "يعمل هذا الجهاز بضغط مياه البلدية دون مضخة تعزيز، لذلك يناسب الأسواق التي تحتاج إلى تشغيل هادئ وصيانة أبسط ومكونات كهربائية أقل. يجمع مسار الترشيح بين PP للرواسب و UDF/GAC و CTO وغشاء RO ومرحلة T33 النهائية. توفر Yuchen Water هذا النموذج للموزعين والمستوردين والعلامات التجارية مع ملصق خاص وتغليف وصنبور وأنابيب وتكوين مناسب للسوق.",
        "spec_title": "المواصفات الفنية",
        "process_title": "عملية الترشيح",
        "buyers_title": "ملاحظات للمشترين",
        "faq_title": "الأسئلة الشائعة",
        "gallery_title": "صور وفيديو المنتج",
        "cta_quote": "طلب عرض OEM",
        "cta_whatsapp": "مبيعات WhatsApp",
        "card_desc": "جهاز RO بخمس مراحل بدون مضخة يعمل بضغط المياه مع ترشيح PP/UDF/CTO/RO/T33 وخيارات OEM.",
        "view": "عرض المنتج",
    },
    "fa": {
        "lang_name": "فارسی",
        "title": "دستگاه تصفیه RO پنج مرحله‌ای بدون پمپ",
        "page_title": "دستگاه تصفیه RO پنج مرحله‌ای بدون پمپ | Yuchen Water",
        "description": "دستگاه RO پنج مرحله‌ای بدون پمپ که با فشار آب شهری کار می‌کند و برای تأمین OEM مناسب است.",
        "summary": "این دستگاه RO پنج مرحله‌ای بدون پمپ با فشار آب شهری کار می‌کند و برای بازارهایی مناسب است که صدای کمتر، سرویس ساده‌تر و قطعات برقی کمتر می‌خواهند. مسیر فیلتراسیون شامل PP رسوب‌گیر، UDF/GAC، CTO، ممبران RO و کربن نهایی T33 است. Yuchen Water این مدل را برای توزیع‌کنندگان، واردکنندگان و برندها با برچسب اختصاصی، بسته‌بندی، شیر، شلنگ و پیکربندی بازار هدف عرضه می‌کند.",
        "spec_title": "مشخصات فنی",
        "process_title": "فرآیند فیلتراسیون",
        "buyers_title": "نکات خرید",
        "faq_title": "پرسش‌های متداول",
        "gallery_title": "تصاویر و ویدیوی محصول",
        "cta_quote": "درخواست قیمت OEM",
        "cta_whatsapp": "فروش WhatsApp",
        "card_desc": "دستگاه RO پنج مرحله‌ای بدون پمپ با فشار آب شهری، فیلتراسیون PP/UDF/CTO/RO/T33 و گزینه‌های OEM.",
        "view": "مشاهده محصول",
    },
    "he": {
        "lang_name": "עברית",
        "title": "מטהר RO חמש שלבים ללא משאבה",
        "page_title": "מטהר RO חמש שלבים ללא משאבה | Yuchen Water",
        "description": "מטהר RO חמש שלבים ללא משאבה, פועל בלחץ מי עיר ומתאים לאספקת OEM.",
        "summary": "מטהר RO זה פועל בלחץ מי עיר ללא משאבת הגברה ומתאים לשווקים המחפשים פעולה שקטה, תחזוקה פשוטה ופחות רכיבים חשמליים. מערך הסינון כולל PP למשקעים, UDF/GAC, CTO, ממברנת RO ופחם סופי T33. Yuchen Water מספקת את הדגם למפיצים, יבואנים ומותגים עם תווית פרטית, אריזה, ברז, צנרת ותצורה לפי שוק.",
        "spec_title": "מפרט טכני",
        "process_title": "תהליך סינון",
        "buyers_title": "מידע לקונים",
        "faq_title": "שאלות נפוצות",
        "gallery_title": "תמונות וסרטון מוצר",
        "cta_quote": "בקשת הצעת OEM",
        "cta_whatsapp": "מכירות WhatsApp",
        "card_desc": "מטהר RO חמש שלבים ללא משאבה, בלחץ מים עירוני, עם PP/UDF/CTO/RO/T33 ואפשרויות OEM.",
        "view": "צפייה במוצר",
    },
}

GENERIC_ROWS = {
    "Product type": "Pump-free five stage RO water purifier",
    "Working method": "Municipal tap-water pressure, no booster pump",
    "Filtration stages": "PP sediment + UDF/GAC + CTO + RO membrane + T33",
    "Pump": "No pump",
    "Inlet water": "Municipal tap water",
    "Installation": "Wall-mounted or under-sink",
    "Application": "Household drinking water and replacement cartridge market",
    "OEM/ODM": "Logo, label, packaging and accessories",
    "MOQ": "Confirm by specification",
}

DEFAULT_PROCESS = [
    "PP sediment filtration removes visible particles, rust and sand.",
    "UDF/GAC and CTO carbon stages reduce chlorine, odor and organic taste.",
    "RO membrane separates dissolved solids, and T33 improves final taste.",
]

DEFAULT_FAQ = [
    ("Does this RO purifier need a booster pump?", "No. It works from municipal tap-water pressure when inlet pressure is suitable."),
    ("What are the filtration stages?", "PP, UDF/GAC, CTO, RO membrane and T33."),
    ("Can the product be customized?", "Yes. Labels, logo, packaging, tubing and faucet kits can be customized."),
    ("Who buys this model?", "Distributors, importers, wholesalers and appliance brands."),
    ("Can accessories be adjusted?", "Yes. Faucet, tube length and connector sets can be selected."),
    ("How is MOQ confirmed?", "MOQ depends on final label, packaging and accessory plan."),
]


def log(lines: list[str], message: str) -> None:
    lines.append(message)


def safe_read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def safe_write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def language_dirs() -> list[Path]:
    dirs: list[Path] = []
    for p in sorted(ROOT.iterdir()):
        if not p.is_dir() or p.name in SKIP_DIRS or p.name.startswith("."):
            continue
        if (p / "index.html").exists() or (p / "products.html").exists():
            dirs.append(p)
    return dirs


def content_for(lang: str) -> dict:
    base = CONTENT.get(lang) or FALLBACKS.get(lang)
    if not base:
        base = CONTENT["en"].copy()
        base["lang_name"] = lang
    merged = CONTENT["en"].copy()
    merged.update(base)
    if "rows" not in merged:
        merged["rows"] = GENERIC_ROWS
    if "process" not in merged:
        merged["process"] = DEFAULT_PROCESS
    if "buyers" not in merged:
        merged["buyers"] = CONTENT["en"]["buyers"]
    if "faq" not in merged:
        merged["faq"] = DEFAULT_FAQ
    return merged


def convert_assets(lines: list[str]) -> tuple[list[dict], dict | None]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    assets: list[dict] = []
    try:
        from PIL import Image

        pil_available = True
    except Exception:
        Image = None
        pil_available = False
        log(lines, "WARNING: Pillow not available; images copied as JPG fallback.")

    for src_str, stem in SOURCES:
        src = Path(src_str)
        if not src.exists():
            log(lines, f"WARNING: missing source image: {src}")
            continue
        width = height = 0
        if pil_available:
            out = ASSET_DIR / f"{stem}.webp"
            try:
                with Image.open(src) as im:
                    im = im.convert("RGB")
                    im.thumbnail((1600, 1600))
                    width, height = im.size
                    im.save(out, "WEBP", quality=82, method=6)
                assets.append({"path": out, "name": out.name, "width": width, "height": height})
                log(lines, f"OK image: {out.relative_to(ROOT)} {width}x{height}")
                continue
            except Exception as exc:
                log(lines, f"WARNING: webp conversion failed for {src.name}: {exc}")
        out = ASSET_DIR / f"{stem}.jpg"
        shutil.copy2(src, out)
        assets.append({"path": out, "name": out.name, "width": width or 1200, "height": height or 1200})
        log(lines, f"OK image fallback: {out.relative_to(ROOT)}")

    video_info = None
    if VIDEO_SOURCE.exists():
        out_video = ASSET_DIR / VIDEO_NAME
        shutil.copy2(VIDEO_SOURCE, out_video)
        video_info = {"path": out_video, "name": out_video.name}
        log(lines, f"OK video: {out_video.relative_to(ROOT)}")
    else:
        log(lines, f"WARNING: missing source video: {VIDEO_SOURCE}")
    return assets, video_info


def rel_from_lang(lang_dir: Path, target: Path) -> str:
    return Path(os.path.relpath(target, lang_dir)).as_posix()


def find_sample(lang_dir: Path) -> Path | None:
    preferred = [
        "product-built-in-pressure-tank-ro.html",
        "product-custom-5-6-7-stage-ro-water-purifier.html",
        "product-ro-seawater-desalination-machine.html",
        "product-ro-water-purifier.html",
    ]
    for name in preferred:
        p = lang_dir / name
        if p.exists():
            return p
    products = sorted(lang_dir.glob("product-*.html"))
    return products[0] if products else None


def strip_ld_json(text: str) -> str:
    return re.sub(
        r"<script\b[^>]*type=[\"']application/ld\+json[\"'][^>]*>[\s\S]*?</script>",
        "",
        text,
        flags=re.I,
    )


def replace_or_add_meta(head: str, pattern: str, replacement: str, before: str = "</head>") -> str:
    if re.search(pattern, head, flags=re.I):
        return re.sub(pattern, replacement, head, count=1, flags=re.I)
    return head.replace(before, replacement + "\n" + before)


def rewrite_shell(prefix: str, suffix: str, lang: str, lang_dir: Path, c: dict, assets: list[dict]) -> tuple[str, str]:
    canonical = f"{CANONICAL_ROOT}/{lang}/{PRODUCT_FILE}"
    img_rel = rel_from_lang(lang_dir, assets[0]["path"]) if assets else "../assets/products/pump-free-five-stage-ro-water-purifier-front.webp"
    prefix = strip_ld_json(prefix)
    suffix = strip_ld_json(suffix)
    if "<html" in prefix[:500].lower():
        dir_attr = ' dir="rtl"' if lang in RTL_LANGS and "dir=" not in prefix[:500].lower() else ""
        prefix = re.sub(r"<html\b[^>]*>", f'<html lang="{escape(lang)}"{dir_attr}>', prefix, count=1, flags=re.I)
    prefix = replace_or_add_meta(prefix, r"<title>[\s\S]*?</title>", f"<title>{escape(c['page_title'])}</title>")
    prefix = replace_or_add_meta(
        prefix,
        r"<meta\s+name=[\"']description[\"'][^>]*>",
        f'<meta name="description" content="{escape(c["description"], quote=True)}">',
    )
    prefix = re.sub(r"<meta\s+name=[\"']keywords[\"'][^>]*>\s*", "", prefix, flags=re.I)
    prefix = re.sub(r"<meta\s+name=[\"']revisit-after[\"'][^>]*>\s*", "", prefix, flags=re.I)
    prefix = replace_or_add_meta(
        prefix,
        r"<link\s+rel=[\"']canonical[\"'][^>]*>",
        f'<link rel="canonical" href="{canonical}">',
    )
    prefix = replace_or_add_meta(
        prefix,
        r"<meta\s+property=[\"']og:title[\"'][^>]*>",
        f'<meta property="og:title" content="{escape(c["page_title"], quote=True)}">',
    )
    prefix = replace_or_add_meta(
        prefix,
        r"<meta\s+property=[\"']og:description[\"'][^>]*>",
        f'<meta property="og:description" content="{escape(c["description"], quote=True)}">',
    )
    prefix = replace_or_add_meta(
        prefix,
        r"<meta\s+property=[\"']og:image[\"'][^>]*>",
        f'<meta property="og:image" content="{CANONICAL_ROOT}/{img_rel.lstrip("../")}">',
    )
    return prefix, suffix


def extract_shell(lang_dir: Path, lang: str, c: dict, assets: list[dict]) -> tuple[str, str]:
    sample = find_sample(lang_dir)
    if sample and sample.exists():
        html = safe_read(sample)
        main_open = re.search(r"<main\b[^>]*>", html, flags=re.I)
        main_close = html.lower().rfind("</main>")
        if main_open and main_close != -1 and main_close > main_open.end():
            prefix = html[: main_open.start()]
            suffix = html[main_close + len("</main>") :]
            return rewrite_shell(prefix, suffix, lang, lang_dir, c, assets)
    dir_attr = ' dir="rtl"' if lang in RTL_LANGS else ""
    first_img = rel_from_lang(lang_dir, assets[0]["path"]) if assets else "../assets/products/pump-free-five-stage-ro-water-purifier-front.webp"
    prefix = f"""<!doctype html>
<html lang="{escape(lang)}"{dir_attr}>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(c['page_title'])}</title>
  <meta name="description" content="{escape(c['description'], quote=True)}">
  <link rel="canonical" href="{CANONICAL_ROOT}/{lang}/{PRODUCT_FILE}">
  <meta property="og:title" content="{escape(c['page_title'], quote=True)}">
  <meta property="og:description" content="{escape(c['description'], quote=True)}">
  <meta property="og:image" content="{CANONICAL_ROOT}/{first_img.lstrip('../')}">
  <style>
    body{{margin:0;font-family:Arial,sans-serif;color:#17343b;background:#f7faf9;line-height:1.65}}
    a{{color:#0b6b78;text-decoration:none}} .container{{max-width:1180px;margin:auto;padding:24px}}
    header,footer{{background:#fff;padding:18px 24px;border-bottom:1px solid #dbe8e6}}
    .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:18px}}
    .card{{background:#fff;border:1px solid #dbe8e6;border-radius:10px;padding:18px}}
    img,video{{max-width:100%;height:auto;border-radius:10px;background:#fff}}
    table{{width:100%;border-collapse:collapse;background:#fff}}td{{padding:12px;border-bottom:1px solid #dbe8e6}}
    .btn{{display:inline-block;margin:8px 8px 8px 0;padding:12px 18px;border-radius:8px;background:#0b6b78;color:#fff;font-weight:700}}
  </style>
</head>
<body>
<header><a href="index.html">Yuchen Water</a> · <a href="products.html">Products</a> · <a href="contact.html">Contact</a></header>
"""
    suffix = "\n<footer>Yuchen Water · expresswater025@gmail.com · +86-19908311885</footer>\n</body>\n</html>\n"
    return prefix, suffix


def img_alt(c: dict, index: int) -> str:
    details = [
        "front view",
        "side connection detail",
        "rear view",
        "filter housing detail",
        "water port detail",
        "cartridge set view",
    ]
    if c["lang_name"] == "English":
        return f"{c['title']} {details[index] if index < len(details) else 'product image'}"
    return f"{c['title']} - {c['lang_name']}"


def json_ld(lang: str, c: dict, assets: list[dict], video: dict | None) -> str:
    product_url = f"{CANONICAL_ROOT}/{lang}/{PRODUCT_FILE}"
    image_urls = [f"{CANONICAL_ROOT}/assets/products/{a['name']}" for a in assets]
    graph = [
        {
            "@context": "https://schema.org",
            "@type": "Product",
            "name": c["title"],
            "brand": {"@type": "Brand", "name": "Yuchen Water"},
            "manufacturer": {"@type": "Organization", "name": "Yuchen Water"},
            "description": c["description"],
            "image": image_urls,
            "url": product_url,
            "category": "RO water purifier",
        },
        {
            "@context": "https://schema.org",
            "@type": "FAQPage",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": q,
                    "acceptedAnswer": {"@type": "Answer", "text": a},
                }
                for q, a in c["faq"]
            ],
        },
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{CANONICAL_ROOT}/{lang}/"},
                {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{CANONICAL_ROOT}/{lang}/products.html"},
                {"@type": "ListItem", "position": 3, "name": c["title"], "item": product_url},
            ],
        },
    ]
    if video:
        graph.append(
            {
                "@context": "https://schema.org",
                "@type": "VideoObject",
                "name": c["title"],
                "description": c["description"],
                "thumbnailUrl": image_urls[:1],
                "contentUrl": f"{CANONICAL_ROOT}/assets/products/{video['name']}",
                "uploadDate": TODAY,
            }
        )
    return '<script type="application/ld+json">\n' + json.dumps(graph, ensure_ascii=False, indent=2) + "\n</script>"


def build_main(lang_dir: Path, lang: str, c: dict, assets: list[dict], video: dict | None) -> str:
    quote_href = "contact.html"
    wa_href = "https://wa.me/8619908311885"
    gallery = []
    for i, a in enumerate(assets):
        gallery.append(
            f'''<figure class="product-gallery-item">
  <img src="{escape(rel_from_lang(lang_dir, a["path"]))}" width="{a["width"]}" height="{a["height"]}" loading="{'eager' if i == 0 else 'lazy'}" alt="{escape(img_alt(c, i), quote=True)}">
</figure>'''
        )
    if video:
        gallery.append(
            f'''<figure class="product-gallery-item">
  <video controls preload="metadata" playsinline>
    <source src="{escape(rel_from_lang(lang_dir, video["path"]))}" type="video/mp4">
  </video>
</figure>'''
        )
    rows = "\n".join(
        f"<tr><td>{escape(str(k))}</td><td>{escape(str(v))}</td></tr>" for k, v in c["rows"].items()
    )
    process = "\n".join(f"<p>{escape(p)}</p>" for p in c["process"])
    faq = "\n".join(
        f"<details><summary>{escape(q)}</summary><p>{escape(a)}</p></details>" for q, a in c["faq"]
    )
    return f"""
<main class="product-detail pump-free-ro-product" data-product-slug="{PRODUCT_SLUG}">
  <section class="product-hero container">
    <nav class="breadcrumb"><a href="index.html">Home</a> &gt; <a href="products.html">Products</a> &gt; {escape(c['title'])}</nav>
    <h1>{escape(c['title'])}</h1>
    <p class="lead">{escape(c['summary'])}</p>
    <p>
      <a class="btn primary" href="{quote_href}">{escape(c['cta_quote'])}</a>
      <a class="btn secondary" href="{wa_href}">{escape(c['cta_whatsapp'])}</a>
    </p>
  </section>

  <section class="container">
    <h2>{escape(c['gallery_title'])}</h2>
    <div class="grid product-gallery">
      {''.join(gallery)}
    </div>
  </section>

  <section class="container">
    <h2>{escape(c['spec_title'])}</h2>
    <table class="spec-table"><tbody>{rows}</tbody></table>
  </section>

  <section class="container">
    <h2>{escape(c['process_title'])}</h2>
    {process}
  </section>

  <section class="container">
    <h2>{escape(c['buyers_title'])}</h2>
    <p>{escape(c['buyers'])}</p>
  </section>

  <section class="container">
    <h2>{escape(c['faq_title'])}</h2>
    <div class="faq-list">{faq}</div>
  </section>

  <section class="container product-cta">
    <p>
      <a class="btn primary" href="{quote_href}">{escape(c['cta_quote'])}</a>
      <a class="btn secondary" href="{wa_href}">{escape(c['cta_whatsapp'])}</a>
    </p>
  </section>
  {json_ld(lang, c, assets, video)}
</main>
"""


def generate_product_pages(lang_dirs: list[Path], assets: list[dict], video: dict | None, lines: list[str]) -> list[str]:
    generated: list[str] = []
    for lang_dir in lang_dirs:
        lang = lang_dir.name
        c = content_for(lang)
        prefix, suffix = extract_shell(lang_dir, lang, c, assets)
        page = prefix + build_main(lang_dir, lang, c, assets, video) + suffix
        out = lang_dir / PRODUCT_FILE
        safe_write(out, page)
        generated.append(str(out.relative_to(ROOT)))
        log(lines, f"OK page: {out.relative_to(ROOT)}")
    return generated


def product_card(lang_dir: Path, c: dict, assets: list[dict]) -> str:
    image = rel_from_lang(lang_dir, assets[0]["path"]) if assets else "../assets/products/pump-free-five-stage-ro-water-purifier-front.webp"
    return f"""
<!-- product-card:{PRODUCT_SLUG} -->
<article class="product-card" data-category="ro-water-purifier ro-system" data-product-slug="{PRODUCT_SLUG}">
  <a href="{PRODUCT_FILE}">
    <img src="{escape(image)}" width="{assets[0]['width'] if assets else 1200}" height="{assets[0]['height'] if assets else 1200}" loading="lazy" alt="{escape(c['title'], quote=True)}">
    <h3>{escape(c['title'])}</h3>
  </a>
  <p>{escape(c['card_desc'])}</p>
  <a class="product-link" href="{PRODUCT_FILE}">{escape(c['view'])}</a>
</article>
"""


def update_products_pages(lang_dirs: list[Path], assets: list[dict], lines: list[str]) -> list[str]:
    updated: list[str] = []
    marker = f"product-card:{PRODUCT_SLUG}"
    for lang_dir in lang_dirs:
        page = lang_dir / "products.html"
        if not page.exists():
            log(lines, f"WARNING: missing products.html in {lang_dir.name}")
            continue
        html = safe_read(page)
        if marker in html:
            log(lines, f"OK products card already present: {page.relative_to(ROOT)}")
            continue
        c = content_for(lang_dir.name)
        card = product_card(lang_dir, c, assets)
        lower = html.lower()
        inserted = False
        for token in ["</main>", "</section>", "</body>"]:
            pos = lower.rfind(token)
            if pos != -1:
                html = html[:pos] + card + "\n" + html[pos:]
                inserted = True
                break
        if not inserted:
            html += card
        safe_write(page, html)
        updated.append(str(page.relative_to(ROOT)))
        log(lines, f"OK products card inserted: {page.relative_to(ROOT)}")
    return updated


def update_sitemap(lang_dirs: list[Path], lines: list[str]) -> None:
    sitemap = ROOT / "sitemap.xml"
    if not sitemap.exists():
        log(lines, "WARNING: sitemap.xml missing; skipped sitemap update.")
        return
    text = safe_read(sitemap)
    added = 0
    urls = []
    for lang_dir in lang_dirs:
        url = f"{CANONICAL_ROOT}/{lang_dir.name}/{PRODUCT_FILE}"
        if url not in text:
            urls.append(f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>")
    if urls:
        if "</urlset>" in text:
            text = text.replace("</urlset>", "\n" + "\n".join(urls) + "\n</urlset>")
        else:
            text += "\n".join(urls)
        safe_write(sitemap, text)
        added = len(urls)
    log(lines, f"OK sitemap updated, new URLs: {added}")


def visible_new_content(lang: str, c: dict) -> str:
    parts = [c["title"], c["description"], c["summary"], c["spec_title"], c["process_title"], c["buyers_title"], c["faq_title"], c["gallery_title"], c["card_desc"], c["view"], c["buyers"]]
    for k, v in c["rows"].items():
        parts.extend([str(k), str(v)])
    for p in c["process"]:
        parts.append(p)
    for q, a in c["faq"]:
        parts.extend([q, a])
    return "\n".join(parts)


def check_language_mix(lang_dirs: list[Path], lines: list[str]) -> None:
    allowed = {
        "ro",
        "pp",
        "cto",
        "udf",
        "gac",
        "t33",
        "oem",
        "odm",
        "moq",
        "mpa",
        "whatsapp",
        "yuchen",
        "water",
    }
    common_words = re.compile(r"\b(the|and|with|for|water|filter|product|stage|stages|pump|without|municipal|pressure|custom|packaging|quote|view)\b", re.I)
    for lang_dir in lang_dirs:
        lang = lang_dir.name
        if lang == "en":
            continue
        content = visible_new_content(lang, content_for(lang))
        matches = [m.group(0) for m in common_words.finditer(content) if m.group(0).lower() not in allowed]
        if matches:
            log(lines, f"CHECK: possible English terms in generated {lang} content: {', '.join(sorted(set(matches))[:12])}")
        else:
            log(lines, f"OK language check: {lang} generated product text has no obvious English filler.")


def validate_pages(lang_dirs: list[Path], assets: list[dict], video: dict | None, lines: list[str]) -> None:
    for lang_dir in lang_dirs:
        page = lang_dir / PRODUCT_FILE
        products = lang_dir / "products.html"
        if not page.exists():
            log(lines, f"FAIL missing product page: {lang_dir.name}")
            continue
        html = safe_read(page)
        c = content_for(lang_dir.name)
        checks = [
            (c["title"] in html, "title"),
            ("Product" in html or '"@type": "Product"' in html, "Product JSON-LD"),
            ('"@type": "FAQPage"' in html, "FAQ JSON-LD"),
            ('"@type": "BreadcrumbList"' in html, "Breadcrumb JSON-LD"),
            (all(a["name"] in html for a in assets), "images"),
            ((not video) or video["name"] in html, "video"),
        ]
        bad = [label for ok, label in checks if not ok]
        if bad:
            log(lines, f"FAIL page validation {page.relative_to(ROOT)}: {', '.join(bad)}")
        else:
            log(lines, f"OK page validation: {page.relative_to(ROOT)}")
        if products.exists():
            ph = safe_read(products)
            if PRODUCT_FILE in ph and f"product-card:{PRODUCT_SLUG}" in ph:
                log(lines, f"OK products link validation: {products.relative_to(ROOT)}")
            else:
                log(lines, f"FAIL products link missing: {products.relative_to(ROOT)}")


def make_zip(lines: list[str]) -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    excluded_dirs = {".git", "reports", "scripts", "__pycache__", "node_modules"}
    with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in ROOT.rglob("*"):
            rel = path.relative_to(ROOT)
            if path.is_dir():
                continue
            if rel.parts and rel.parts[0] in excluded_dirs:
                continue
            if path.suffix == ".zip":
                continue
            zf.write(path, rel.as_posix())
    log(lines, f"OK zip package: {ZIP_PATH}")


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    lines: list[str] = []
    log(lines, f"Pump-free RO product build started: {TODAY}")
    try:
        langs = language_dirs()
        log(lines, "Languages detected: " + ", ".join(p.name for p in langs))
        assets, video = convert_assets(lines)
        if not assets:
            raise RuntimeError("No product images were prepared.")
        pages = generate_product_pages(langs, assets, video, lines)
        cards = update_products_pages(langs, assets, lines)
        update_sitemap(langs, lines)
        check_language_mix(langs, lines)
        validate_pages(langs, assets, video, lines)
        make_zip(lines)
        log(lines, "")
        log(lines, "SUMMARY")
        log(lines, f"Product slug: {PRODUCT_SLUG}")
        log(lines, f"Product pages generated: {len(pages)}")
        log(lines, f"Products pages updated: {len(cards)}")
        log(lines, f"Assets prepared: {len(assets)} images, {'1 video' if video else '0 video'}")
        log(lines, f"Upload package: {ZIP_PATH}")
    except Exception as exc:
        log(lines, f"ERROR: {type(exc).__name__}: {exc}")
        raise
    finally:
        safe_write(REPORT_PATH, "\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
