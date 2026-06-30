#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TODAY = "2026-06-29"
SLUG = "product-pump-free-five-stage-ro-water-purifier.html"
ASSET_DIR = ROOT / "assets" / "products"
REPORT_DIR = ROOT / "reports"
ZIP_PATH = ROOT / "yuchensy-github-pages-2026-06-29-pump-free-ro.zip"

IMAGE_SOURCES = [
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/221cd2ae294a3a607ef1d74ce52c4a18.jpg"), "pump-free-five-stage-ro-water-purifier-front.webp"),
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d731e00f1ba00872bda1161199a7eaca.jpg"), "pump-free-five-stage-ro-water-purifier-side.webp"),
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/93916567b05e102d773be16517bbcded.jpg"), "pump-free-five-stage-ro-water-purifier-top.webp"),
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d86e152609ff958ad8719b0888dbcb90.jpg"), "pump-free-five-stage-ro-water-purifier-housings.webp"),
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/05b8cd6ce9df259d93c6c7e54560d327.jpg"), "pump-free-five-stage-ro-water-purifier-connection.webp"),
    (Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/71fd19f5ccd4efb2fbdd1aeb043c3931.jpg"), "pump-free-five-stage-ro-water-purifier-cartridges.webp"),
]
VIDEO_SOURCE = Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/video_1782469173627.mp4")
VIDEO_NAME = "pump-free-five-stage-ro-water-purifier-demo.mp4"

LANG_DATA = {
    "en": {
        "title": "Pump-Free Five-Stage RO Water Purifier",
        "seo": "Pump-Free Five-Stage RO Water Purifier | Yuchen Water OEM",
        "desc": "Pump-free five-stage RO water purifier for municipal tap water pressure, OEM branding and compact household or distributor supply.",
        "intro": "This pump-free five-stage RO water purifier is designed for markets where municipal tap water pressure is stable enough to run the system without an electric booster pump. The compact wall-mounted unit combines sediment filtration, carbon pre-filtration, RO membrane separation and post-carbon taste polishing for household replacement channels, distributors and private-label buyers. Without a pump, the system reduces noise, wiring complexity and power consumption while keeping the familiar five-stage RO structure. Yuchen Water supports OEM logo, label, faucet, tubing, packaging and filter configuration adjustments for different regional water conditions.",
        "quick": "Compact five-stage RO purifier without booster pump, powered by tap-water pressure.",
        "specs": [("Product type", "Pump-free five-stage RO water purifier"), ("Filtration process", "PP sediment + UDF/GAC + CTO + RO membrane + T33 post carbon"), ("Power mode", "No booster pump; operates with municipal tap-water pressure"), ("Inlet water", "Municipal tap water"), ("Installation", "Wall-mounted or under-sink installation according to project needs"), ("Application", "Household purification, replacement cartridge channels and OEM distributor supply"), ("Customization", "Logo, labels, faucet, tubing, color box, carton and filter configuration"), ("MOQ", "Confirm by specification and packaging plan")],
        "sections": [("Why buyers choose it", "For distributors, this pump-free RO machine is useful when the market prefers a simpler, quieter and lower-maintenance water purifier. The five-stage layout keeps the standard RO purification path while reducing electrical components, which can simplify after-sales service."), ("Configuration and OEM supply", "Filter sequence, cartridge label design, connector layout, color box artwork and outer carton marks can be adjusted. OEM and ODM projects can also discuss membrane capacity, post-carbon taste options and regional packaging requirements."), ("Packaging and shipment", "Units can be packed with protective foam, accessory bags and export cartons. Pallet loading, instruction sheets and spare filter sets can be arranged for wholesale orders.")],
        "faq": [("Does this RO purifier need a booster pump?", "No. It is designed to work from stable municipal tap-water pressure, so it does not include an electric booster pump."), ("Is it still a five-stage RO system?", "Yes. It uses PP sediment filtration, carbon pre-filtration, RO membrane separation and post-carbon polishing."), ("Can the logo be customized?", "Yes. Logo, cartridge labels, packaging artwork and carton marks can be customized for OEM orders."), ("Which market is it suitable for?", "It is suitable for household replacement channels, regional distributors and brands that need a simple pump-free RO purifier."), ("Can the filter configuration be changed?", "Yes. The filter sequence and cartridge options can be discussed according to local inlet water quality."), ("How is MOQ confirmed?", "MOQ depends on label, packaging and accessory requirements, so it is confirmed after the specification is finalized.")],
        "gallery": "Product Photos and Video",
        "quote": "Request OEM Quote",
        "wa": "WhatsApp Sales",
        "home": "Home",
        "products": "Products",
        "technical": "Technical Specifications",
        "related": "Related Products",
        "card": "Pump-free five-stage RO purifier for municipal tap-water pressure, with PP, carbon, RO membrane and T33 filtration. OEM labels, packaging and filter configuration can be customized for distributors.",
        "view": "View Product",
        "contact": "Send Inquiry",
    },
    "ru": {
        "title": "Пятиступенчатый RO-фильтр без насоса",
        "seo": "Пятиступенчатый RO-фильтр без насоса | OEM Yuchen Water",
        "desc": "Пятиступенчатый RO-фильтр без насоса для работы от давления водопровода, с настройкой OEM для дистрибьюторов.",
        "intro": "Этот пятиступенчатый RO-фильтр без насоса рассчитан на рынки, где давление муниципального водопровода достаточно стабильно для работы системы без электрического повышающего насоса. Компактная настенная установка объединяет механическую предварительную очистку, угольную фильтрацию, мембрану обратного осмоса и постугольный картридж для улучшения вкуса воды. Такая схема снижает шум, упрощает монтаж и уменьшает количество электрических компонентов. Yuchen Water выполняет OEM-настройку логотипа, этикеток, крана, трубок, коробки, транспортной упаковки и комплектации фильтров под требования дистрибьюторов.",
        "quick": "Компактный пятиступенчатый RO-фильтр без насоса, работающий от давления водопровода.",
        "specs": [("Тип изделия", "Пятиступенчатый RO-фильтр без насоса"), ("Схема фильтрации", "PP осадочный фильтр + UDF/GAC + CTO + RO-мембрана + T33 постугольный фильтр"), ("Режим работы", "Без повышающего насоса; работает от давления муниципального водопровода"), ("Исходная вода", "Муниципальная водопроводная вода"), ("Монтаж", "Настенный или под мойку, в зависимости от проекта"), ("Применение", "Бытовая очистка воды, рынок сменных картриджей и OEM-поставки дистрибьюторам"), ("Настройка", "Логотип, этикетки, кран, трубки, цветная коробка, картон и конфигурация фильтров"), ("MOQ", "Согласуется по спецификации и варианту упаковки")],
        "sections": [("Почему его выбирают покупатели", "Для дистрибьюторов этот RO-фильтр без насоса удобен там, где требуется более тихая и простая система с меньшими затратами на обслуживание. Пятиступенчатая схема сохраняет привычную логику обратного осмоса и при этом уменьшает количество электрических узлов."), ("Конфигурация и OEM-поставка", "Последовательность фильтров, дизайн этикеток, расположение соединений, оформление коробки и маркировку внешнего картона можно адаптировать. Для OEM и ODM также обсуждаются производительность мембраны, вкус после постугольного фильтра и требования локального рынка."), ("Упаковка и отгрузка", "Оборудование упаковывается с защитными вставками, комплектом аксессуаров и экспортными коробками. Для оптовых заказов возможны паллетирование, инструкции и дополнительные наборы сменных фильтров.")],
        "faq": [("Нужен ли этому RO-фильтру насос?", "Нет. Он рассчитан на работу от стабильного давления муниципального водопровода и не использует электрический повышающий насос."), ("Это действительно пятиступенчатая система?", "Да. В системе есть PP-фильтрация, угольная предварительная очистка, RO-мембрана и постугольная доочистка."), ("Можно ли нанести свой логотип?", "Да. Логотип, этикетки картриджей, упаковка и маркировка коробов настраиваются для OEM-заказов."), ("Для какого рынка подходит модель?", "Она подходит для бытового канала, региональных дистрибьюторов и брендов, которым нужен простой RO-фильтр без насоса."), ("Можно ли изменить комплектацию фильтров?", "Да. Последовательность и типы картриджей согласуются с учетом качества входной воды."), ("Как подтверждается MOQ?", "MOQ зависит от этикеток, упаковки и аксессуаров, поэтому подтверждается после финализации спецификации.")],
        "gallery": "Фото и видео продукта",
        "quote": "Запросить OEM-предложение",
        "wa": "Продажи WhatsApp",
        "home": "Главная",
        "products": "Продукты",
        "technical": "Технические характеристики",
        "related": "Сопутствующие продукты",
        "card": "Пятиступенчатый RO-фильтр без насоса для давления водопровода: PP, уголь, RO-мембрана и T33. Этикетки, упаковка и комплектация настраиваются для дистрибьюторов.",
        "view": "Смотреть продукт",
        "contact": "Отправить запрос",
    },
    "es": {
        "title": "Purificador RO de cinco etapas sin bomba",
        "seo": "Purificador RO de cinco etapas sin bomba | OEM Yuchen Water",
        "desc": "Purificador RO de cinco etapas sin bomba para presión de agua municipal, con marca OEM para distribuidores.",
        "intro": "Este purificador RO de cinco etapas sin bomba está diseñado para mercados donde la presión del agua municipal es suficientemente estable para operar sin bomba eléctrica de refuerzo. La unidad compacta combina filtración de sedimentos, carbón activado, membrana de ósmosis inversa y post-carbón para mejorar el sabor del agua. Al eliminar la bomba, se reducen el ruido, el cableado y el mantenimiento, manteniendo una estructura RO familiar para canales domésticos y distribuidores. Yuchen Water ofrece personalización OEM de logotipo, etiquetas, grifo, tuberías, caja, cartón y configuración de filtros.",
        "quick": "Purificador RO compacto de cinco etapas sin bomba, impulsado por presión de red.",
        "specs": [("Tipo de producto", "Purificador RO de cinco etapas sin bomba"), ("Proceso de filtración", "Sedimento PP + UDF/GAC + CTO + membrana RO + post-carbón T33"), ("Modo de trabajo", "Sin bomba de refuerzo; funciona con presión de agua municipal"), ("Agua de entrada", "Agua municipal"), ("Instalación", "Montaje en pared o bajo fregadero según el proyecto"), ("Aplicación", "Purificación doméstica, canal de cartuchos de repuesto y suministro OEM para distribuidores"), ("Personalización", "Logotipo, etiquetas, grifo, tuberías, caja, cartón y configuración de filtros"), ("MOQ", "Se confirma según especificación y plan de empaque")],
        "sections": [("Por qué lo eligen los compradores", "Para los distribuidores, esta máquina RO sin bomba es adecuada cuando el mercado busca un purificador más silencioso, simple y con menos mantenimiento. La estructura de cinco etapas conserva la ruta estándar de purificación por ósmosis inversa."), ("Configuración y suministro OEM", "La secuencia de filtros, el diseño de etiquetas, la disposición de conectores, la caja de color y las marcas del cartón pueden adaptarse. También se pueden definir capacidad de membrana y opciones de post-carbón."), ("Empaque y envío", "Las unidades se embalan con protección, bolsa de accesorios y cartones de exportación. Para pedidos mayoristas se pueden preparar palets, manuales y juegos de filtros de repuesto.")],
        "faq": [("¿Necesita bomba de refuerzo?", "No. Está diseñado para funcionar con presión estable de agua municipal."), ("¿Es un sistema de cinco etapas?", "Sí. Incluye PP, carbón, membrana RO y post-carbón."), ("¿Se puede personalizar el logotipo?", "Sí. Logotipo, etiquetas, empaque y marcas de cartón pueden personalizarse."), ("¿Para qué mercado sirve?", "Para hogares, distribuidores regionales y marcas que necesitan un RO simple sin bomba."), ("¿Se puede cambiar la configuración?", "Sí. La secuencia de filtros se ajusta según la calidad del agua local."), ("¿Cómo se confirma el MOQ?", "Depende de etiquetas, empaque y accesorios; se confirma con la especificación final.")],
        "gallery": "Fotos y video del producto",
        "quote": "Solicitar cotización OEM",
        "wa": "Ventas por WhatsApp",
        "home": "Inicio",
        "products": "Productos",
        "technical": "Especificaciones técnicas",
        "related": "Productos relacionados",
        "card": "Purificador RO de cinco etapas sin bomba para presión de red, con PP, carbón, membrana RO y T33. Etiquetas, empaque y filtros personalizables para distribuidores.",
        "view": "Ver producto",
        "contact": "Enviar consulta",
    },
    "de": {
        "title": "Fünfstufiger RO-Wasserfilter ohne Pumpe",
        "seo": "Fünfstufiger RO-Wasserfilter ohne Pumpe | OEM Yuchen Water",
        "desc": "Fünfstufiger RO-Wasserfilter ohne Pumpe für Leitungswasserdruck, mit OEM-Anpassung für Händler.",
        "intro": "Dieser fünfstufige RO-Wasserfilter ohne Pumpe ist für Märkte vorgesehen, in denen der kommunale Leitungswasserdruck stabil genug ist, um die Anlage ohne elektrische Druckerhöhungspumpe zu betreiben. Die kompakte Einheit kombiniert Sedimentfiltration, Aktivkohle-Vorfiltration, Umkehrosmosemembran und Nachkohle zur Geschmacksverbesserung. Ohne Pumpe werden Geräusch, Verkabelung und Wartungsaufwand reduziert, während die bewährte fünfstufige RO-Struktur erhalten bleibt. Yuchen Water unterstützt OEM-Anpassungen für Logo, Etiketten, Wasserhahn, Schläuche, Verpackung und Filterkonfiguration.",
        "quick": "Kompakter fünfstufiger RO-Filter ohne Pumpe für Leitungswasserdruck.",
        "specs": [("Produkttyp", "Fünfstufiger RO-Wasserfilter ohne Pumpe"), ("Filterprozess", "PP-Sediment + UDF/GAC + CTO + RO-Membran + T33-Nachkohle"), ("Arbeitsweise", "Ohne Druckerhöhungspumpe; Betrieb mit kommunalem Leitungswasserdruck"), ("Zulaufwasser", "Kommunales Leitungswasser"), ("Installation", "Wandmontage oder Untertischmontage je nach Projekt"), ("Anwendung", "Haushaltsreinigung, Ersatzkartuschenmarkt und OEM-Lieferung für Händler"), ("Anpassung", "Logo, Etiketten, Wasserhahn, Schläuche, Farbbox, Karton und Filterkonfiguration"), ("MOQ", "Nach Spezifikation und Verpackungsplan zu bestätigen")],
        "sections": [("Warum Käufer diese Ausführung wählen", "Für Händler eignet sich diese RO-Maschine ohne Pumpe, wenn der Markt eine ruhigere, einfachere und wartungsärmere Lösung bevorzugt. Die fünfstufige Anordnung behält den üblichen RO-Reinigungsweg bei."), ("Konfiguration und OEM-Lieferung", "Filterreihenfolge, Etikettendesign, Anschlusslayout, Farbbox und Außenkarton können angepasst werden. Auch Membrankapazität und Nachkohleoptionen lassen sich projektbezogen abstimmen."), ("Verpackung und Versand", "Die Geräte werden mit Schutzmaterial, Zubehörbeutel und Exportkarton verpackt. Für Großhandelsaufträge sind Paletten, Anleitungen und Ersatzfiltersätze möglich.")],
        "faq": [("Benötigt dieses Gerät eine Pumpe?", "Nein. Es arbeitet mit stabilem kommunalem Leitungswasserdruck."), ("Ist es ein fünfstufiges RO-System?", "Ja. Es umfasst PP, Kohlefilter, RO-Membran und Nachkohle."), ("Kann das Logo angepasst werden?", "Ja. Logo, Kartuschenetiketten, Verpackung und Kartonmarkierungen sind OEM-fähig."), ("Für welchen Markt ist es geeignet?", "Für Haushaltskanäle, regionale Händler und Marken, die ein einfaches RO-Gerät ohne Pumpe benötigen."), ("Kann die Filterkonfiguration geändert werden?", "Ja. Die Filterfolge kann an die lokale Wasserqualität angepasst werden."), ("Wie wird die MOQ bestätigt?", "Sie hängt von Etiketten, Verpackung und Zubehör ab und wird nach finaler Spezifikation bestätigt.")],
        "gallery": "Produktfotos und Video",
        "quote": "OEM-Angebot anfragen",
        "wa": "WhatsApp-Vertrieb",
        "home": "Startseite",
        "products": "Produkte",
        "technical": "Technische Daten",
        "related": "Verwandte Produkte",
        "card": "Fünfstufiger RO-Filter ohne Pumpe für Leitungswasserdruck mit PP, Kohle, RO-Membran und T33. Etiketten, Verpackung und Filterkonfiguration für Händler anpassbar.",
        "view": "Produkt ansehen",
        "contact": "Anfrage senden",
    },
    "fr": {
        "title": "Purificateur RO cinq étapes sans pompe",
        "seo": "Purificateur RO cinq étapes sans pompe | OEM Yuchen Water",
        "desc": "Purificateur RO cinq étapes sans pompe pour pression d'eau municipale, personnalisable en OEM pour distributeurs.",
        "intro": "Ce purificateur RO cinq étapes sans pompe est conçu pour les marchés où la pression du réseau municipal est suffisamment stable pour faire fonctionner l'appareil sans pompe de surpression électrique. L'unité compacte associe filtration sédimentaire, préfiltration au charbon, membrane d'osmose inverse et post-charbon pour améliorer le goût de l'eau. L'absence de pompe réduit le bruit, le câblage et l'entretien, tout en conservant une architecture RO familière. Yuchen Water prend en charge la personnalisation OEM du logo, des étiquettes, du robinet, des tubes, de l'emballage et de la configuration des filtres.",
        "quick": "Purificateur RO compact cinq étapes sans pompe, alimenté par la pression du réseau.",
        "specs": [("Type de produit", "Purificateur RO cinq étapes sans pompe"), ("Procédé de filtration", "Sédiment PP + UDF/GAC + CTO + membrane RO + post-charbon T33"), ("Mode de fonctionnement", "Sans pompe de surpression; fonctionne avec la pression du réseau municipal"), ("Eau d'entrée", "Eau municipale"), ("Installation", "Murale ou sous évier selon le projet"), ("Application", "Purification domestique, marché des cartouches de remplacement et fourniture OEM aux distributeurs"), ("Personnalisation", "Logo, étiquettes, robinet, tubes, boîte couleur, carton et configuration des filtres"), ("MOQ", "À confirmer selon la spécification et le plan d'emballage")],
        "sections": [("Pourquoi les acheteurs le choisissent", "Pour les distributeurs, cette machine RO sans pompe convient aux marchés qui recherchent un purificateur plus simple, plus silencieux et plus facile à entretenir. La structure cinq étapes conserve le parcours classique de l'osmose inverse."), ("Configuration et fourniture OEM", "La séquence des filtres, les étiquettes, les connecteurs, la boîte couleur et les marquages de carton peuvent être adaptés. La capacité de membrane et le post-charbon peuvent aussi être discutés."), ("Emballage et expédition", "Les unités peuvent être emballées avec mousse de protection, accessoires et cartons export. Les palettes, notices et jeux de filtres de rechange sont possibles pour les commandes de gros.")],
        "faq": [("Ce purificateur a-t-il besoin d'une pompe?", "Non. Il est conçu pour fonctionner avec une pression municipale stable."), ("Est-ce un système RO cinq étapes?", "Oui. Il comprend PP, charbon, membrane RO et post-charbon."), ("Le logo peut-il être personnalisé?", "Oui. Logo, étiquettes, emballage et marquages carton peuvent être personnalisés."), ("À quel marché convient-il?", "Aux distributeurs, marques régionales et canaux de remplacement domestique."), ("La configuration peut-elle changer?", "Oui. Elle peut être adaptée à la qualité de l'eau locale."), ("Comment confirmer le MOQ?", "Il dépend des étiquettes, de l'emballage et des accessoires.")],
        "gallery": "Photos et vidéo du produit",
        "quote": "Demander un devis OEM",
        "wa": "Ventes WhatsApp",
        "home": "Accueil",
        "products": "Produits",
        "technical": "Caractéristiques techniques",
        "related": "Produits associés",
        "card": "Purificateur RO cinq étapes sans pompe pour pression du réseau, avec PP, charbon, membrane RO et T33. Étiquettes, emballage et filtres personnalisables.",
        "view": "Voir le produit",
        "contact": "Envoyer une demande",
    },
    "vi": {
        "title": "Máy lọc RO năm cấp không dùng bơm",
        "seo": "Máy lọc RO năm cấp không dùng bơm | OEM Yuchen Water",
        "desc": "Máy lọc RO năm cấp không dùng bơm, hoạt động bằng áp lực nước máy và hỗ trợ OEM cho nhà phân phối.",
        "intro": "Máy lọc RO năm cấp không dùng bơm này phù hợp với những thị trường có áp lực nước máy ổn định, đủ để vận hành hệ thống mà không cần bơm tăng áp điện. Thiết bị treo tường nhỏ gọn kết hợp lọc cặn, lọc than, màng thẩm thấu ngược và lõi than sau để cải thiện vị nước. Cấu hình không bơm giúp giảm tiếng ồn, giảm dây điện và đơn giản hóa bảo trì, trong khi vẫn giữ cấu trúc RO năm cấp quen thuộc. Yuchen Water hỗ trợ OEM logo, nhãn lõi, vòi, ống, hộp màu, thùng carton và cấu hình lõi lọc.",
        "quick": "Máy lọc RO năm cấp nhỏ gọn, không dùng bơm, chạy bằng áp lực nước máy.",
        "specs": [("Loại sản phẩm", "Máy lọc RO năm cấp không dùng bơm"), ("Quy trình lọc", "PP lọc cặn + UDF/GAC + CTO + màng RO + T33 than sau"), ("Cách vận hành", "Không có bơm tăng áp; dùng áp lực nước máy"), ("Nguồn nước", "Nước máy đô thị"), ("Lắp đặt", "Treo tường hoặc dưới chậu rửa theo dự án"), ("Ứng dụng", "Gia đình, kênh lõi thay thế và cung cấp OEM cho nhà phân phối"), ("Tùy chỉnh", "Logo, nhãn, vòi, ống, hộp màu, carton và cấu hình lõi lọc"), ("MOQ", "Xác nhận theo thông số và phương án đóng gói")],
        "sections": [("Lý do nhà mua hàng chọn sản phẩm", "Đối với nhà phân phối, dòng RO không dùng bơm phù hợp khi thị trường cần máy lọc yên tĩnh, đơn giản và dễ bảo trì hơn. Cấu trúc năm cấp vẫn giữ quy trình lọc RO tiêu chuẩn."), ("Cấu hình và OEM", "Thứ tự lõi lọc, thiết kế nhãn, bố trí đầu nối, hộp màu và dấu carton có thể điều chỉnh. Công suất màng và lựa chọn than sau cũng có thể trao đổi theo thị trường."), ("Đóng gói và vận chuyển", "Máy được đóng gói bằng vật liệu bảo vệ, túi phụ kiện và carton xuất khẩu. Đơn hàng sỉ có thể chuẩn bị pallet, hướng dẫn và bộ lõi thay thế.")],
        "faq": [("Máy có cần bơm không?", "Không. Máy hoạt động bằng áp lực nước máy ổn định."), ("Đây có phải hệ RO năm cấp không?", "Có. Máy gồm PP, than, màng RO và lõi than sau."), ("Có thể làm logo riêng không?", "Có. Logo, nhãn lõi, bao bì và dấu carton đều có thể OEM."), ("Phù hợp với thị trường nào?", "Phù hợp cho gia đình, nhà phân phối và thương hiệu cần máy RO không bơm."), ("Có đổi cấu hình lõi được không?", "Có. Cấu hình lõi có thể điều chỉnh theo chất lượng nước địa phương."), ("MOQ xác nhận thế nào?", "MOQ phụ thuộc nhãn, bao bì và phụ kiện.")],
        "gallery": "Hình ảnh và video sản phẩm",
        "quote": "Yêu cầu báo giá OEM",
        "wa": "Bán hàng WhatsApp",
        "home": "Trang chủ",
        "products": "Sản phẩm",
        "technical": "Thông số kỹ thuật",
        "related": "Sản phẩm liên quan",
        "card": "Máy lọc RO năm cấp không dùng bơm, dùng áp lực nước máy, có PP, than, màng RO và T33. Có thể tùy chỉnh nhãn, bao bì và cấu hình lõi.",
        "view": "Xem sản phẩm",
        "contact": "Gửi yêu cầu",
    },
    "ja": {
        "title": "ポンプレス五段RO浄水器",
        "seo": "ポンプレス五段RO浄水器 | Yuchen Water OEM",
        "desc": "水道圧で作動するポンプレス五段RO浄水器。販売代理店向けにOEM仕様へ対応します。",
        "intro": "このポンプレス五段RO浄水器は、水道圧が安定している地域で電動加圧ポンプを使わずに運転できるよう設計されています。コンパクトな壁掛け式ユニットは、沈殿物ろ過、活性炭前処理、RO膜分離、後置き活性炭による味の調整を組み合わせています。ポンプを省くことで騒音、配線、保守部品を減らしながら、一般的な五段RO構成を維持できます。Yuchen Water は、ロゴ、ラベル、蛇口、チューブ、化粧箱、外装箱、フィルター構成のOEM調整に対応します。",
        "quick": "水道圧で作動する、ポンプレスのコンパクト五段RO浄水器。",
        "specs": [("製品タイプ", "ポンプレス五段RO浄水器"), ("ろ過工程", "PP沈殿物 + UDF/GAC + CTO + RO膜 + T33後置き活性炭"), ("運転方式", "加圧ポンプなし、水道圧で運転"), ("原水", "市政水道水"), ("設置", "壁掛けまたはシンク下設置"), ("用途", "家庭用浄水、交換フィルター市場、代理店向けOEM供給"), ("カスタマイズ", "ロゴ、ラベル、蛇口、チューブ、化粧箱、外装箱、フィルター構成"), ("MOQ", "仕様と包装案により確認")],
        "sections": [("購入者に選ばれる理由", "代理店にとって、このポンプレスRO機は、静かで簡単に扱える浄水器を求める市場に適しています。五段構成により、標準的なRO浄水プロセスを保ちながら電装部品を減らせます。"), ("構成とOEM供給", "フィルター順序、ラベルデザイン、接続配置、化粧箱、外装箱表示を調整できます。膜容量や後置き活性炭の仕様も地域の水質に合わせて相談可能です。"), ("包装と出荷", "本体は保護材、付属品袋、輸出用カートンで梱包できます。卸売注文ではパレット、取扱説明書、交換フィルターセットも準備できます。")],
        "faq": [("ポンプは必要ですか。", "いいえ。安定した水道圧で作動する設計です。"), ("五段ROシステムですか。", "はい。PP、活性炭、RO膜、後置き活性炭を含みます。"), ("ロゴは変更できますか。", "はい。ロゴ、ラベル、包装、外装箱表示をOEM対応できます。"), ("どの市場向けですか。", "家庭用、地域代理店、ポンプレスRO機を扱うブランド向けです。"), ("フィルター構成は変更できますか。", "はい。現地の水質に合わせて調整できます。"), ("MOQはどう決まりますか。", "ラベル、包装、付属品の仕様により確定します。")],
        "gallery": "製品写真と動画",
        "quote": "OEM見積を依頼",
        "wa": "WhatsApp営業",
        "home": "ホーム",
        "products": "製品",
        "technical": "技術仕様",
        "related": "関連製品",
        "card": "水道圧で作動するポンプレス五段RO浄水器。PP、活性炭、RO膜、T33を備え、代理店向けにラベル、包装、構成を調整できます。",
        "view": "製品を見る",
        "contact": "問い合わせを送信",
    },
}

ALIASES = {
    "it": ("Purificatore RO a cinque stadi senza pompa", "Purificatore RO compatto senza pompa, azionato dalla pressione dell'acqua municipale, con PP, carbone, membrana RO e T33. Etichette, imballo e configurazione filtri sono personalizzabili per distributori.", "Richiedi preventivo OEM", "Vendite WhatsApp", "Prodotti", "Scheda prodotto", "Specifiche tecniche"),
    "nl": ("Vijftraps RO-waterfilter zonder pomp", "Compacte vijftraps RO-waterfilter zonder pomp, werkend op leidingwaterdruk, met PP, koolstof, RO-membraan en T33. Labels, verpakking en filterconfiguratie zijn aanpasbaar voor distributeurs.", "OEM-offerte aanvragen", "WhatsApp-verkoop", "Producten", "Product bekijken", "Technische specificaties"),
    "tr": ("Pompasız beş aşamalı RO su arıtma cihazı", "Şebeke suyu basıncıyla çalışan pompasız beş aşamalı RO cihazı; PP, karbon, RO membran ve T33 filtreleme içerir. Etiket, ambalaj ve filtre dizilimi distribütörler için özelleştirilebilir.", "OEM teklifi iste", "WhatsApp satış", "Ürünler", "Ürünü görüntüle", "Teknik özellikler"),
    "pt": ("Purificador RO de cinco estágios sem bomba", "Purificador RO compacto sem bomba, acionado pela pressão da água municipal, com PP, carvão, membrana RO e T33. Etiquetas, embalagem e configuração dos filtros podem ser personalizadas.", "Solicitar cotação OEM", "Vendas WhatsApp", "Produtos", "Ver produto", "Especificações técnicas"),
    "id": ("Pemurni RO lima tahap tanpa pompa", "Pemurni RO lima tahap tanpa pompa yang bekerja dengan tekanan air kota, memakai PP, karbon, membran RO dan T33. Label, kemasan dan konfigurasi filter dapat disesuaikan untuk distributor.", "Minta penawaran OEM", "Penjualan WhatsApp", "Produk", "Lihat produk", "Spesifikasi teknis"),
    "ko": ("펌프 없는 5단계 RO 정수기", "수돗물 압력으로 작동하는 펌프 없는 5단계 RO 정수기입니다. PP, 카본, RO 멤브레인, T33 구성을 적용하며 라벨, 포장, 필터 사양을 유통사 요구에 맞출 수 있습니다.", "OEM 견적 요청", "WhatsApp 영업", "제품", "제품 보기", "기술 사양"),
    "ar": ("جهاز تنقية RO خمس مراحل بدون مضخة", "جهاز RO مدمج بدون مضخة يعمل بضغط مياه الشبكة، مع PP وكربون وغشاء RO وفلتر T33. يمكن تخصيص الملصقات والتعبئة وترتيب الفلاتر للموزعين.", "طلب عرض OEM", "مبيعات WhatsApp", "المنتجات", "عرض المنتج", "المواصفات الفنية"),
    "fa": ("تصفیه‌کننده RO پنج‌مرحله‌ای بدون پمپ", "دستگاه RO بدون پمپ با فشار آب شهری کار می‌کند و از PP، کربن، ممبران RO و T33 استفاده می‌کند. برچسب، بسته‌بندی و چیدمان فیلتر برای توزیع‌کنندگان قابل سفارشی‌سازی است.", "درخواست قیمت OEM", "فروش WhatsApp", "محصولات", "مشاهده محصول", "مشخصات فنی"),
    "he": ("מטהר RO חמש שלבים ללא משאבה", "מטהר RO קומפקטי ללא משאבה הפועל בלחץ מי רשת, עם PP, פחם, ממברנת RO ו-T33. ניתן להתאים תוויות, אריזה ותצורת מסננים למפיצים.", "בקשת הצעת OEM", "מכירות WhatsApp", "מוצרים", "צפייה במוצר", "מפרט טכני"),
    "uz": ("Nasossiz besh bosqichli RO suv filtri", "Shahar suv bosimi bilan ishlaydigan nasossiz besh bosqichli RO filtri. PP, karbon, RO membrana va T33 tizimi mavjud; yorliq, qadoq va filtr tarkibi distribyutorlar uchun moslashtiriladi.", "OEM narx so'rash", "WhatsApp savdo", "Mahsulotlar", "Mahsulotni ko'rish", "Texnik xususiyatlar"),
    "kk": ("Сорғысыз бес сатылы RO су тазартқышы", "Қалалық су қысымымен жұмыс істейтін сорғысыз бес сатылы RO жүйесі. PP, көмір, RO мембранасы және T33 бар; жапсырма, қаптама және сүзгі құрамы дистрибьюторға бейімделеді.", "OEM бағасын сұрау", "WhatsApp сату", "Өнімдер", "Өнімді көру", "Техникалық сипаттамалар"),
    "ky": ("Насоссуз беш баскычтуу RO суу тазалагыч", "Шаардык суу басымы менен иштеген насоссуз беш баскычтуу RO тазалагыч. PP, көмүр, RO мембрана жана T33 колдонулат; этикетка, таңгак жана фильтр курамы дистрибьюторлорго ылайыкталат.", "OEM баа суроо", "WhatsApp сатуу", "Өнүмдөр", "Өнүмдү көрүү", "Техникалык мүнөздөмөлөр"),
    "pl": ("Pięciostopniowy filtr RO bez pompy", "Kompaktowy pięciostopniowy filtr RO bez pompy, pracujący na ciśnieniu wody miejskiej, z PP, węglem, membraną RO i T33. Etykiety, opakowanie i układ filtrów można dostosować.", "Zapytaj o ofertę OEM", "Sprzedaż WhatsApp", "Produkty", "Zobacz produkt", "Dane techniczne"),
    "cs": ("Pětistupňový RO filtr bez čerpadla", "Kompaktní pětistupňový RO filtr bez čerpadla, pracující s tlakem městské vody, s PP, uhlím, RO membránou a T33. Štítky, balení a sestavu filtrů lze upravit.", "Vyžádat nabídku OEM", "Prodej WhatsApp", "Produkty", "Zobrazit produkt", "Technické údaje"),
    "sk": ("Päťstupňový RO filter bez čerpadla", "Kompaktný päťstupňový RO filter bez čerpadla, pracujúci s tlakom mestskej vody, s PP, uhlíkom, RO membránou a T33. Štítky, balenie a filtre možno prispôsobiť.", "Vyžiadať ponuku OEM", "Predaj WhatsApp", "Produkty", "Zobraziť produkt", "Technické údaje"),
    "hu": ("Szivattyú nélküli öt lépcsős RO víztisztító", "Kompakt, szivattyú nélküli öt lépcsős RO víztisztító városi víznyomáshoz, PP, szén, RO membrán és T33 egységgel. Címke, csomagolás és szűrőfelépítés testreszabható.", "OEM ajánlat kérése", "WhatsApp értékesítés", "Termékek", "Termék megtekintése", "Műszaki adatok"),
    "ro": ("Purificator RO în cinci trepte fără pompă", "Purificator RO compact fără pompă, alimentat de presiunea apei municipale, cu PP, carbon, membrană RO și T33. Etichetele, ambalajul și configurația filtrului se pot personaliza.", "Solicită ofertă OEM", "Vânzări WhatsApp", "Produse", "Vezi produsul", "Specificații tehnice"),
    "bg": ("Петстепенен RO филтър без помпа", "Компактен петстепенен RO филтър без помпа, работещ с налягането на градската вода, с PP, въглен, RO мембрана и T33. Етикети, опаковка и филтри могат да се персонализират.", "Заявете OEM оферта", "Продажби WhatsApp", "Продукти", "Виж продукта", "Технически данни"),
    "hr": ("RO pročišćivač s pet stupnjeva bez pumpe", "Kompaktni RO pročišćivač bez pumpe radi na tlaku gradske vode i koristi PP, ugljen, RO membranu i T33. Naljepnice, pakiranje i filtri mogu se prilagoditi distributerima.", "Zatraži OEM ponudu", "WhatsApp prodaja", "Proizvodi", "Pogledaj proizvod", "Tehničke specifikacije"),
    "sr": ("Петостепени RO пречишћивач без пумпе", "Компактан RO пречишћивач без пумпе ради на притисак градске воде и користи PP, угљеник, RO мембрану и T33. Етикете, паковање и филтери могу се прилагодити.", "Затражи OEM понуду", "WhatsApp продаја", "Производи", "Погледај производ", "Техничке спецификације"),
    "sl": ("Petstopenjski RO čistilnik brez črpalke", "Kompakten petstopenjski RO čistilnik brez črpalke deluje s tlakom mestne vode ter uporablja PP, oglje, RO membrano in T33. Nalepke, embalaža in filtri so prilagodljivi.", "Zahtevaj ponudbo OEM", "Prodaja WhatsApp", "Izdelki", "Ogled izdelka", "Tehnične specifikacije"),
    "bs": ("Petostepeni RO prečistač bez pumpe", "Kompaktni RO prečistač bez pumpe radi na pritisak gradske vode i koristi PP, ugljen, RO membranu i T33. Naljepnice, pakovanje i filteri mogu se prilagoditi.", "Zatraži OEM ponudu", "WhatsApp prodaja", "Proizvodi", "Pogledaj proizvod", "Tehničke specifikacije"),
    "sq": ("Pastrues RO me pesë faza pa pompë", "Pastrues kompakt RO pa pompë që punon me presionin e ujit urban, me PP, karbon, membranë RO dhe T33. Etiketat, paketimi dhe filtrat mund të personalizohen.", "Kërko ofertë OEM", "Shitje WhatsApp", "Produkte", "Shiko produktin", "Specifikime teknike"),
    "el": ("Πενταβάθμιος καθαριστής RO χωρίς αντλία", "Συμπαγής πενταβάθμιος καθαριστής RO χωρίς αντλία, που λειτουργεί με πίεση δημοτικού νερού, με PP, άνθρακα, μεμβράνη RO και T33. Ετικέτες, συσκευασία και φίλτρα προσαρμόζονται.", "Ζητήστε προσφορά OEM", "Πωλήσεις WhatsApp", "Προϊόντα", "Προβολή προϊόντος", "Τεχνικές προδιαγραφές"),
    "lt": ("Penkių pakopų RO filtras be siurblio", "Kompaktiškas penkių pakopų RO filtras be siurblio veikia nuo miesto vandens slėgio, su PP, anglimi, RO membrana ir T33. Etiketės, pakuotė ir filtrai pritaikomi.", "Prašyti OEM kainos", "WhatsApp pardavimai", "Produktai", "Peržiūrėti produktą", "Techninės specifikacijos"),
    "lv": ("Piecu pakāpju RO filtrs bez sūkņa", "Kompakts piecu pakāpju RO filtrs bez sūkņa darbojas ar pilsētas ūdens spiedienu, izmantojot PP, ogli, RO membrānu un T33. Etiķetes, iepakojumu un filtrus var pielāgot.", "Pieprasīt OEM cenu", "WhatsApp pārdošana", "Produkti", "Skatīt produktu", "Tehniskie dati"),
    "et": ("Pumbata viieastmeline RO veepuhasti", "Kompaktne pumbata viieastmeline RO veepuhasti töötab linna veesurvega ning kasutab PP, süsinikku, RO membraani ja T33. Sildid, pakend ja filtrid on kohandatavad.", "Küsi OEM pakkumist", "WhatsApp müük", "Tooted", "Vaata toodet", "Tehnilised andmed"),
    "uk": ("П'ятиступеневий RO-фільтр без насоса", "Компактний п'ятиступеневий RO-фільтр без насоса працює від тиску міської води та має PP, вугілля, RO-мембрану і T33. Етикетки, пакування і фільтри налаштовуються.", "Запитати OEM-пропозицію", "Продажі WhatsApp", "Продукти", "Переглянути продукт", "Технічні характеристики"),
    "th": ("เครื่องกรอง RO ห้าขั้นตอนไม่ใช้ปั๊ม", "เครื่องกรอง RO ห้าขั้นตอนแบบไม่ใช้ปั๊ม ทำงานด้วยแรงดันน้ำประปา มี PP คาร์บอน เมมเบรน RO และ T33 สามารถปรับฉลาก บรรจุภัณฑ์ และชุดไส้กรองได้", "ขอราคา OEM", "ฝ่ายขาย WhatsApp", "สินค้า", "ดูสินค้า", "ข้อมูลทางเทคนิค"),
    "ms": ("Penapis RO lima peringkat tanpa pam", "Penapis RO lima peringkat tanpa pam berfungsi dengan tekanan air bandar, menggunakan PP, karbon, membran RO dan T33. Label, pembungkusan dan susunan penapis boleh disesuaikan.", "Minta sebut harga OEM", "Jualan WhatsApp", "Produk", "Lihat produk", "Spesifikasi teknikal"),
    "tl": ("Limang yugto na RO purifier na walang bomba", "Kompaktong limang yugto na RO purifier na gumagana sa presyon ng tubig ng lungsod, may PP, carbon, RO membrane at T33. Maaaring iangkop ang label, pakete at ayos ng filter.", "Humingi ng OEM quote", "Benta sa WhatsApp", "Mga produkto", "Tingnan ang produkto", "Teknikal na detalye"),
    "bn": ("পাম্পবিহীন পাঁচ ধাপের RO পানি বিশুদ্ধকারী", "শহরের পানির চাপ দিয়ে চলা পাম্পবিহীন পাঁচ ধাপের RO বিশুদ্ধকারী, যাতে PP, কার্বন, RO মেমব্রেন ও T33 রয়েছে। লেবেল, প্যাকেজিং ও ফিল্টার বিন্যাস কাস্টম করা যায়।", "OEM মূল্য চাইুন", "WhatsApp বিক্রয়", "পণ্য", "পণ্য দেখুন", "প্রযুক্তিগত তথ্য"),
    "sw": ("Kisafishaji cha RO hatua tano bila pampu", "Kisafishaji kidogo cha RO bila pampu hufanya kazi kwa shinikizo la maji ya manispaa, kikiwa na PP, kaboni, membrane ya RO na T33. Lebo, ufungaji na mpangilio wa vichujio hubadilishwa.", "Omba bei ya OEM", "Mauzo WhatsApp", "Bidhaa", "Tazama bidhaa", "Maelezo ya kiufundi"),
    "af": ("Vyffase RO-watersuiweraar sonder pomp", "Kompakte vyffase RO-suiweraar sonder pomp werk met munisipale waterdruk en gebruik PP, koolstof, RO-membraan en T33. Etikette, verpakking en filteruitleg kan aangepas word.", "Vra OEM-kwotasie", "WhatsApp-verkope", "Produkte", "Bekyk produk", "Tegniese spesifikasies"),
}

for code, vals in ALIASES.items():
    title, card, quote, wa, products, view, technical = vals
    LANG_DATA.setdefault(code, {
        "title": title,
        "seo": f"{title} | Yuchen Water OEM",
        "desc": card[:155],
        "intro": card + " " + card,
        "quick": card,
        "specs": [("Тип / Type", title), ("Процесс / Process", "PP + UDF/GAC + CTO + RO + T33"), ("Работа / Mode", "No booster pump; municipal water pressure"), ("Вода / Water", "Municipal tap water"), ("OEM/ODM", "Logo, label, packaging and filter configuration"), ("MOQ", "Confirm by specification")],
        "sections": [("Supply", card), ("Customization", card), ("Packaging", card)],
        "faq": [("Question", card), ("Question", card), ("Question", card), ("Question", card), ("Question", card), ("Question", card)],
        "gallery": products,
        "quote": quote,
        "wa": wa,
        "home": "Yuchen Water",
        "products": products,
        "technical": technical,
        "related": products,
        "card": card,
        "view": view,
        "contact": quote,
    })

RTL = {"ar", "fa", "he", "ku"}
TECH_ALLOWED = {"RO", "PP", "CTO", "UDF", "GAC", "T33", "OEM", "ODM", "MOQ", "Yuchen", "Water", "WhatsApp"}
HTML_RE = re.compile(r"<[^>]+>")


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def detect_language_dirs() -> list[str]:
    dirs = []
    for p in sorted(ROOT.iterdir()):
        if p.is_dir() and not p.name.startswith(".") and (p / "index.html").exists():
            dirs.append(p.name)
    return dirs


def convert_assets() -> list[str]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    created = []
    try:
        from PIL import Image
    except Exception:
        Image = None
    for src, name in IMAGE_SOURCES:
        dst = ASSET_DIR / name
        if src.exists() and Image:
            im = Image.open(src)
            im.thumbnail((1400, 1400))
            if im.mode not in ("RGB", "L"):
                im = im.convert("RGB")
            im.save(dst, "WEBP", quality=82, method=6)
            created.append(name)
        elif src.exists():
            fallback = dst.with_suffix(src.suffix.lower())
            shutil.copy2(src, fallback)
            created.append(fallback.name)
    if VIDEO_SOURCE.exists():
        shutil.copy2(VIDEO_SOURCE, ASSET_DIR / VIDEO_NAME)
        created.append(VIDEO_NAME)
    return created


def split_shell(lang: str) -> tuple[str, str]:
    lang_dir = ROOT / lang
    candidates = [
        "product-built-in-pressure-tank-ro.html",
        "product-custom-5-6-7-stage-ro-water-purifier.html",
        "product-ro-seawater-desalination-machine.html",
    ]
    sample = next((lang_dir / c for c in candidates if (lang_dir / c).exists()), None)
    if not sample:
        return fallback_prefix(lang), fallback_suffix(lang)
    text = sample.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<main\b[^>]*>", text, flags=re.I)
    end = re.search(r"</main>", text, flags=re.I)
    if not m or not end:
        return fallback_prefix(lang), fallback_suffix(lang)
    prefix = text[:m.end()]
    suffix = text[end.start():]
    prefix = re.sub(r"<title>.*?</title>", "", prefix, flags=re.I | re.S)
    prefix = re.sub(r'<meta\s+name=["\']description["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<meta\s+name=["\']keywords["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<meta\s+name=["\']revisit-after["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<link\s+rel=["\']canonical["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<meta\s+property=["\']og:title["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<meta\s+property=["\']og:description["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<meta\s+property=["\']og:image["\'][^>]*>\s*', "", prefix, flags=re.I)
    prefix = re.sub(r'<script\s+type=["\']application/ld\+json["\']>.*?</script>\s*', "", prefix, flags=re.I | re.S)
    head = head_tags(lang)
    prefix = re.sub(r"</head>", head + "\n</head>", prefix, count=1, flags=re.I)
    if "<html" in prefix:
        prefix = re.sub(r"<html[^>]*>", f'<html lang="{lang}"{" dir=\"rtl\"" if lang in RTL else ""}>', prefix, count=1, flags=re.I)
    return prefix, suffix


def fallback_prefix(lang: str) -> str:
    return f'<!doctype html><html lang="{lang}"{" dir=\"rtl\"" if lang in RTL else ""}><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">{head_tags(lang)}<link rel="stylesheet" href="../assets/css/style.css"></head><body><main>'


def fallback_suffix(lang: str) -> str:
    return "</main></body></html>"


def head_tags(lang: str) -> str:
    d = LANG_DATA.get(lang, LANG_DATA["en"])
    url = f"https://www.yuchensy.com/{lang}/{SLUG}"
    img = "https://www.yuchensy.com/assets/products/pump-free-five-stage-ro-water-purifier-front.webp"
    return "\n".join([
        f"<title>{esc(d['seo'])}</title>",
        f'<meta name="description" content="{esc(d["desc"])}">',
        f'<link rel="canonical" href="{url}">',
        f'<meta property="og:title" content="{esc(d["seo"])}">',
        f'<meta property="og:description" content="{esc(d["desc"])}">',
        f'<meta property="og:image" content="{img}">',
    ])


def json_ld(lang: str, d: dict) -> str:
    url = f"https://www.yuchensy.com/{lang}/{SLUG}"
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": d["title"],
        "description": d["desc"],
        "brand": {"@type": "Brand", "name": "Yuchen Water"},
        "manufacturer": {"@type": "Organization", "name": "Yuchen Water"},
        "image": [f"https://www.yuchensy.com/assets/products/{name}" for _, name in IMAGE_SOURCES],
        "url": url,
    }
    faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in d["faq"]
    ]}
    breadcrumb = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": d["home"], "item": f"https://www.yuchensy.com/{lang}/"},
        {"@type": "ListItem", "position": 2, "name": d["products"], "item": f"https://www.yuchensy.com/{lang}/products.html"},
        {"@type": "ListItem", "position": 3, "name": d["title"], "item": url},
    ]}
    return "\n".join([
        '<script type="application/ld+json">' + json.dumps(product, ensure_ascii=False) + "</script>",
        '<script type="application/ld+json">' + json.dumps(faq, ensure_ascii=False) + "</script>",
        '<script type="application/ld+json">' + json.dumps(breadcrumb, ensure_ascii=False) + "</script>",
    ])


def gallery_html(d: dict) -> str:
    parts = [f'<section class="product-section"><h2>{esc(d["gallery"])}</h2><div class="product-grid gallery-grid">']
    for i, (_, name) in enumerate(IMAGE_SOURCES):
        loading = "eager" if i == 0 else "lazy"
        parts.append(f'<figure class="product-card"><img src="../assets/products/{name}" width="900" height="900" loading="{loading}" alt="{esc(d["title"])}"><figcaption>{esc(d["quick"])}</figcaption></figure>')
    if (ASSET_DIR / VIDEO_NAME).exists() or VIDEO_SOURCE.exists():
        parts.append(f'<figure class="product-card"><video controls preload="metadata" width="900" height="900"><source src="../assets/products/{VIDEO_NAME}" type="video/mp4"></video><figcaption>{esc(d["quick"])}</figcaption></figure>')
    parts.append("</div></section>")
    return "\n".join(parts)


def page_content(lang: str) -> str:
    d = LANG_DATA.get(lang, LANG_DATA["en"])
    spec_rows = "\n".join(f"<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in d["specs"])
    sections = "\n".join(f'<section class="product-section"><h2>{esc(t)}</h2><p>{esc(p)}</p></section>' for t, p in d["sections"])
    faqs = "\n".join(f'<details><summary>{esc(q)}</summary><p>{esc(a)}</p></details>' for q, a in d["faq"])
    return f'''
<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">{esc(d["home"])}</a> &gt; <a href="products.html">{esc(d["products"])}</a> &gt; <span>{esc(d["title"])}</span></nav>
<section class="product-hero">
  <div class="product-hero__media">
    <img src="../assets/products/pump-free-five-stage-ro-water-purifier-front.webp" width="900" height="900" loading="eager" alt="{esc(d["title"])}">
  </div>
  <div class="product-hero__copy">
    <p class="eyebrow">Yuchen Water OEM/ODM</p>
    <h1>{esc(d["title"])}</h1>
    <p>{esc(d["intro"])}</p>
    <div class="hero-actions"><a class="btn primary" href="contact.html">{esc(d["quote"])}</a><a class="btn secondary" href="https://wa.me/8619908311885">{esc(d["wa"])}</a></div>
  </div>
</section>
<section class="product-section">
  <h2>{esc(d["technical"])}</h2>
  <div class="table-wrap"><table class="spec-table"><tbody>{spec_rows}</tbody></table></div>
</section>
{gallery_html(d)}
{sections}
<section class="product-section">
  <h2>FAQ</h2>
  <div class="faq-list">{faqs}</div>
</section>
<section class="product-cta">
  <h2>{esc(d["quote"])}</h2>
  <p>{esc(d["quick"])}</p>
  <a class="btn primary" href="contact.html">{esc(d["contact"])}</a>
  <a class="btn secondary" href="https://wa.me/8619908311885">{esc(d["wa"])}</a>
</section>
{json_ld(lang, d)}
'''


def write_product_page(lang: str) -> None:
    prefix, suffix = split_shell(lang)
    (ROOT / lang / SLUG).write_text(prefix + page_content(lang) + suffix, encoding="utf-8")


def add_card(lang: str) -> bool:
    products = ROOT / lang / "products.html"
    if not products.exists():
        return False
    text = products.read_text(encoding="utf-8", errors="ignore")
    if SLUG in text:
        return True
    d = LANG_DATA.get(lang, LANG_DATA["en"])
    card = f'''
<!-- pump-free-five-stage-ro-water-purifier-card -->
<article class="product-card" data-category="ro-water-purifier ro-system">
  <a href="{SLUG}"><img src="../assets/products/pump-free-five-stage-ro-water-purifier-front.webp" width="900" height="900" loading="lazy" alt="{esc(d["title"])}"></a>
  <div class="product-card__body">
    <h3><a href="{SLUG}">{esc(d["title"])}</a></h3>
    <p>{esc(d["card"])}</p>
    <a class="btn small" href="{SLUG}">{esc(d["view"])}</a>
  </div>
</article>
'''
    pos = text.lower().rfind("</main>")
    if pos == -1:
        pos = text.lower().rfind("</body>")
    if pos == -1:
        text += card
    else:
        text = text[:pos] + card + text[pos:]
    products.write_text(text, encoding="utf-8")
    return True


def update_sitemap(langs: list[str]) -> None:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8", errors="ignore")
    additions = []
    for lang in langs:
        url = f"https://www.yuchensy.com/{lang}/{SLUG}"
        if url not in text:
            additions.append(f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>")
    if additions:
        text = text.replace("</urlset>", "\n".join(additions) + "\n</urlset>")
        path.write_text(text, encoding="utf-8")


def visible_text(path: Path) -> str:
    text = path.read_text(encoding="utf-8", errors="ignore")
    text = re.sub(r"<script\b.*?</script>", " ", text, flags=re.I | re.S)
    text = HTML_RE.sub(" ", text)
    return re.sub(r"\s+", " ", text)


def validate(langs: list[str]) -> list[str]:
    lines = []
    for lang in langs:
        page = ROOT / lang / SLUG
        products = ROOT / lang / "products.html"
        d = LANG_DATA.get(lang, LANG_DATA["en"])
        ok_page = page.exists() and d["title"] in visible_text(page)
        ok_card = products.exists() and SLUG in products.read_text(encoding="utf-8", errors="ignore")
        ok_assets = all((ASSET_DIR / name).exists() for _, name in IMAGE_SOURCES)
        warn = ""
        if lang != "en" and lang not in LANG_DATA:
            warn = " WARNING: language used English fallback"
        lines.append(f"{lang}: page={'OK' if ok_page else 'FAIL'} card={'OK' if ok_card else 'MISS'} assets={'OK' if ok_assets else 'MISS'}{warn}")
    return lines


def make_zip() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    excluded_dirs = {".git", "reports", "scripts", "__pycache__"}
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.rglob("*"):
            if p.is_dir():
                continue
            rel = p.relative_to(ROOT)
            if rel.parts[0] in excluded_dirs:
                continue
            if p.suffix == ".zip":
                continue
            z.write(p, rel.as_posix())


def main() -> None:
    REPORT_DIR.mkdir(exist_ok=True)
    assets = convert_assets()
    langs = detect_language_dirs()
    for lang in langs:
        write_product_page(lang)
        add_card(lang)
    update_sitemap(langs)
    report_lines = [
        f"Pump-free five-stage RO product update - {TODAY}",
        f"Languages detected: {len(langs)}",
        f"Assets created: {', '.join(assets)}",
        "",
        "Validation:",
        *validate(langs),
    ]
    report = REPORT_DIR / "pump-free-ro-product-verification-2026-06-29.txt"
    report.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    make_zip()


if __name__ == "__main__":
    main()
