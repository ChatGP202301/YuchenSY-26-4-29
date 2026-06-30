#!/usr/bin/env python3
from __future__ import annotations

import html
import json
import re
import shutil
import zipfile
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TODAY = "2026-06-29"
BASE_URL = "https://www.yuchensy.com"
SLUG = "product-pump-free-five-stage-ro-water-purifier.html"
ASSET_DIR = ROOT / "assets" / "products"
REPORT_DIR = ROOT / "reports"
ZIP_PATH = ROOT / "yuchensy-github-pages-2026-06-29-pump-free-ro.zip"

IMAGE_SOURCES = [
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/221cd2ae294a3a607ef1d74ce52c4a18.jpg", "pump-free-five-stage-ro-water-purifier-front"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d731e00f1ba00872bda1161199a7eaca.jpg", "pump-free-five-stage-ro-water-purifier-side"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/d86e152609ff958ad8719b0888dbcb90.jpg", "pump-free-five-stage-ro-water-purifier-housings"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/71fd19f5ccd4efb2fbdd1aeb043c3931.jpg", "pump-free-five-stage-ro-water-purifier-cartridges"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/93916567b05e102d773be16517bbcded.jpg", "pump-free-five-stage-ro-water-purifier-rear"),
    ("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/05b8cd6ce9df259d93c6c7e54560d327.jpg", "pump-free-five-stage-ro-water-purifier-top"),
]

VIDEO_SOURCE = Path("/Users/jet/Downloads/26.6.6 台式机E500-TS2/重新设计的26.6.26/RO机不带泵/video_1782469173627.mp4")
VIDEO_NAME = "pump-free-five-stage-ro-water-purifier-demo.mp4"

RTL_LANGS = {"ar", "fa", "he", "ku"}
TECH_OK = {
    "RO",
    "PP",
    "CTO",
    "UDF",
    "GAC",
    "T33",
    "OEM",
    "ODM",
    "MOQ",
    "WhatsApp",
    "Yuchen",
    "Water",
    "MPa",
    "GPD",
    "CE",
    "SGS",
    "ISO",
    "NSF",
    "ANSI",
}


@dataclass
class CopyAsset:
    url_path: str
    rel_path: str
    width: int
    height: int
    ok: bool
    note: str


def t_en() -> dict:
    return {
        "lang_name": "English",
        "product_name": "Pump-Free Five-Stage RO Water Purifier",
        "h1": "Pump-Free Five-Stage RO Water Purifier for Tap Water Pressure",
        "title": "Pump-Free Five-Stage RO Water Purifier | OEM Supplier",
        "description": "Pump-free five-stage RO water purifier for stable tap water pressure, with PP, UDF, CTO, RO membrane and T33 filtration for OEM projects.",
        "intro": "This pump-free five-stage RO water purifier is designed for markets where municipal tap water pressure is stable enough to drive the system without a booster pump. The wall-mounted or under-sink unit uses PP sediment filtration, UDF/GAC carbon, CTO carbon block, RO membrane and T33 post carbon to support daily drinking water projects for homes, apartments, offices and light commercial users. B2B buyers choose it for lower power dependence, simpler maintenance, OEM labeling, carton customization and flexible filter configuration.",
        "gallery": "Product Gallery and Video",
        "overview": "System Overview",
        "overview_text": "The system is suitable for distributors and private-label buyers who need a compact RO water purifier without a pump. When inlet pressure is stable, the no-pump structure reduces noise, simplifies wiring and keeps the product easier to maintain. The filtration layout can be adjusted for local water quality, target price and packaging requirements.",
        "configuration": "Configurable Filtration Design",
        "configuration_text": "A standard configuration includes PP sediment filtration for sand and rust, UDF or GAC carbon for chlorine and odor reduction, CTO carbon block for further adsorption, RO membrane separation for dissolved solids reduction and T33 post carbon for final taste polishing. Cartridge labels, quick connectors, faucet sets and cartons can be prepared according to the buyer's brand plan.",
        "specs": "Technical Specifications",
        "applications": "Buyer Applications",
        "applications_text": "This model is used for household drinking water, apartment renovation projects, office pantry supply, rental housing packages and regional replacement-cartridge markets. It is especially useful where customers want RO filtration but prefer a pump-free structure that depends on municipal water pressure.",
        "quality": "Quality and Export Support",
        "quality_text": "Yuchen Water checks incoming plastic parts, fittings, tubing and filter cartridges before assembly. Finished units can be checked for connection tightness, water flow and packing condition before shipment. Export cartons, manuals, labels and sample confirmation can be arranged for OEM and ODM orders.",
        "faq": "FAQ",
        "cta_title": "Request an OEM Quote",
        "cta_text": "Send your target market, water pressure range, cartridge preference, logo requirements and order quantity. Our engineer will recommend a suitable pump-free RO configuration.",
        "quote": "Request OEM Quote",
        "whatsapp": "WhatsApp Sales",
        "related": "Back to Products",
        "video_label": "Product demonstration video",
        "spec_rows": [
            ("Product type", "Pump-free five-stage RO water purifier"),
            ("Filtration stages", "PP + UDF/GAC + CTO + RO membrane + T33"),
            ("Working mode", "Driven by stable municipal tap water pressure, no booster pump"),
            ("Installation", "Wall-mounted or under-sink"),
            ("Application", "Home, apartment, office and light commercial drinking water"),
            ("Feed water", "Municipal tap water with suitable inlet pressure"),
            ("OEM/ODM", "Logo, label, faucet set, fittings, packaging and manual"),
            ("MOQ", "Confirmed by specification and packaging plan"),
        ],
        "faqs": [
            ("Does this RO purifier need a booster pump?", "No. It is designed for tap-water-pressure operation, so the buyer should confirm that local inlet pressure is stable enough for RO filtration."),
            ("What are the five filtration stages?", "The standard system uses PP, UDF or GAC carbon, CTO carbon block, RO membrane and T33 post carbon."),
            ("Can the filter set be customized?", "Yes. Cartridge sequence, labels, connectors, faucet options and packaging can be adjusted for OEM and ODM projects."),
            ("Which markets is this model suitable for?", "It fits homes, apartments, offices and light commercial drinking water projects where buyers prefer a quiet pump-free RO system."),
            ("Can we use our own logo?", "Yes. Private-label logos, filter labels, manual artwork and export cartons can be prepared after sample confirmation."),
            ("How should buyers confirm suitability?", "Please provide feed-water pressure, target capacity, local water quality and packaging requirements before quotation."),
        ],
    }


TRANSLATIONS = {
    "en": t_en(),
    "ru": {
        "lang_name": "Русский",
        "product_name": "Пятиступенчатый RO-фильтр без насоса",
        "h1": "Пятиступенчатый RO-фильтр без насоса для давления водопровода",
        "title": "Пятиступенчатый RO-фильтр без насоса | OEM-поставка",
        "description": "Пятиступенчатый RO-фильтр без насоса для стабильного давления водопровода: PP, UDF, CTO, RO-мембрана и T33 для OEM-заказов.",
        "intro": "Этот пятиступенчатый RO-фильтр без насоса предназначен для рынков, где давление городской водопроводной воды достаточно стабильно для работы системы без повысительного насоса. Настенная или подмоечная конструкция использует PP-фильтр от осадка, уголь UDF/GAC, угольный блок CTO, RO-мембрану и постуголь T33 для питьевой воды в домах, квартирах, офисах и небольших коммерческих объектах. B2B-покупатели выбирают эту модель за меньшую зависимость от электропитания, простое обслуживание, OEM-маркировку, индивидуальную упаковку и гибкую комплектацию картриджей.",
        "gallery": "Фото и видео продукта",
        "overview": "Описание системы",
        "overview_text": "Модель подходит дистрибьюторам и заказчикам частной марки, которым нужен компактный RO-фильтр без насоса. При стабильном входном давлении такая конструкция снижает шум, упрощает подключение и облегчает сервисное обслуживание.",
        "configuration": "Настраиваемая схема фильтрации",
        "configuration_text": "Стандартная схема включает PP для песка и ржавчины, UDF или GAC для снижения хлора и запаха, CTO для дополнительной адсорбции, RO-мембрану для уменьшения растворённых солей и T33 для улучшения вкуса. Этикетки картриджей, быстроразъёмные фитинги, кран и коробки можно подготовить под бренд покупателя.",
        "specs": "Технические характеристики",
        "applications": "Применение для покупателей",
        "applications_text": "Модель используют для питьевой воды в домах, квартирах, офисных кухнях, арендном жилье и на рынке сменных картриджей. Она особенно удобна там, где требуется RO-фильтрация без насосного блока.",
        "quality": "Контроль качества и экспорт",
        "quality_text": "Yuchen Water проверяет пластиковые детали, фитинги, трубки и картриджи перед сборкой. Готовые системы могут проходить проверку герметичности соединений, расхода воды и упаковки перед отгрузкой.",
        "faq": "Вопросы и ответы",
        "cta_title": "Запросить OEM-предложение",
        "cta_text": "Сообщите рынок, диапазон давления, желаемые картриджи, требования к логотипу и количество. Инженер подберёт подходящую конфигурацию RO без насоса.",
        "quote": "Запросить OEM-предложение",
        "whatsapp": "Продажи WhatsApp",
        "related": "Вернуться к продуктам",
        "video_label": "Видео демонстрации продукта",
        "spec_rows": [
            ("Тип продукта", "Пятиступенчатый RO-фильтр без насоса"),
            ("Ступени фильтрации", "PP + UDF/GAC + CTO + RO-мембрана + T33"),
            ("Режим работы", "Работа от стабильного давления городской воды, без насоса"),
            ("Монтаж", "Настенный или под мойкой"),
            ("Применение", "Дом, квартира, офис и небольшие коммерческие объекты"),
            ("Исходная вода", "Городская вода с подходящим входным давлением"),
            ("OEM/ODM", "Логотип, этикетки, кран, фитинги, упаковка и инструкция"),
            ("MOQ", "Согласуется по спецификации и упаковке"),
        ],
        "faqs": [
            ("Нужен ли повысительный насос?", "Нет. Система рассчитана на работу от давления водопровода, поэтому важно подтвердить стабильность входного давления."),
            ("Какие пять ступеней используются?", "Обычно применяются PP, UDF или GAC, CTO, RO-мембрана и постуголь T33."),
            ("Можно ли изменить набор фильтров?", "Да. Последовательность картриджей, этикетки, фитинги, кран и упаковка настраиваются для OEM и ODM."),
            ("Для каких рынков подходит модель?", "Для домов, квартир, офисов и небольших проектов питьевой воды, где нужна тихая система RO без насоса."),
            ("Можно ли нанести наш логотип?", "Да. Логотип, этикетки, инструкция и экспортные коробки готовятся после утверждения образца."),
            ("Что нужно для точного подбора?", "Укажите давление воды, требуемую производительность, качество исходной воды и требования к упаковке."),
        ],
    },
    "es": {
        "lang_name": "Español",
        "product_name": "Purificador RO de cinco etapas sin bomba",
        "h1": "Purificador RO de cinco etapas sin bomba para presión de red",
        "title": "Purificador RO sin bomba de cinco etapas | Proveedor OEM",
        "description": "Purificador RO de cinco etapas sin bomba para presión estable de red, con PP, UDF, CTO, membrana RO y T33 para proyectos OEM.",
        "intro": "Este purificador RO de cinco etapas sin bomba está diseñado para mercados donde la presión del agua municipal es suficientemente estable para alimentar el sistema sin bomba de refuerzo. La unidad mural o bajo fregadero combina filtración PP para sedimentos, carbón UDF/GAC, bloque CTO, membrana RO y postcarbón T33 para proyectos de agua potable en hogares, apartamentos, oficinas y usos comerciales ligeros. Los compradores B2B lo eligen por menor dependencia eléctrica, mantenimiento sencillo, etiquetado OEM, embalaje personalizado y configuración flexible de cartuchos.",
        "gallery": "Galería y video del producto",
        "overview": "Descripción del sistema",
        "overview_text": "El equipo es adecuado para distribuidores y marcas privadas que necesitan un purificador RO compacto sin bomba. Cuando la presión de entrada es estable, la estructura sin bomba reduce el ruido, simplifica el cableado y facilita el mantenimiento.",
        "configuration": "Diseño de filtración configurable",
        "configuration_text": "La configuración estándar incluye PP para arena y óxido, UDF o GAC para reducir cloro y olor, CTO para adsorción adicional, membrana RO para disminuir sólidos disueltos y T33 para mejorar el sabor final. Etiquetas, conectores, grifos y cajas pueden adaptarse a la marca del comprador.",
        "specs": "Especificaciones técnicas",
        "applications": "Aplicaciones para compradores",
        "applications_text": "Se utiliza en viviendas, apartamentos, oficinas, proyectos de alquiler y mercados de cartuchos de reemplazo. Es útil donde se desea filtración RO con una estructura silenciosa sin bomba.",
        "quality": "Calidad y soporte de exportación",
        "quality_text": "Yuchen Water revisa piezas plásticas, accesorios, tubos y cartuchos antes del montaje. Las unidades terminadas pueden verificarse en hermeticidad, caudal y empaque antes del envío.",
        "faq": "Preguntas frecuentes",
        "cta_title": "Solicitar cotización OEM",
        "cta_text": "Envíe mercado objetivo, rango de presión, cartuchos deseados, requisitos de logotipo y cantidad. Nuestro ingeniero recomendará una configuración RO sin bomba adecuada.",
        "quote": "Solicitar cotización OEM",
        "whatsapp": "Ventas por WhatsApp",
        "related": "Volver a productos",
        "video_label": "Video de demostración del producto",
        "spec_rows": [
            ("Tipo de producto", "Purificador RO de cinco etapas sin bomba"),
            ("Etapas de filtración", "PP + UDF/GAC + CTO + membrana RO + T33"),
            ("Modo de trabajo", "Funciona con presión estable de agua municipal, sin bomba"),
            ("Instalación", "Mural o bajo fregadero"),
            ("Aplicación", "Hogar, apartamento, oficina y uso comercial ligero"),
            ("Agua de entrada", "Agua municipal con presión adecuada"),
            ("OEM/ODM", "Logotipo, etiquetas, grifo, accesorios, embalaje y manual"),
            ("MOQ", "Según especificación y plan de embalaje"),
        ],
        "faqs": [
            ("¿Necesita bomba de refuerzo?", "No. Está diseñado para trabajar con presión de red, por lo que debe confirmarse la presión local."),
            ("¿Cuáles son las cinco etapas?", "PP, UDF o GAC, CTO, membrana RO y postcarbón T33."),
            ("¿Se puede personalizar el conjunto?", "Sí. Cartuchos, etiquetas, conectores, grifo y embalaje se ajustan para OEM y ODM."),
            ("¿Para qué mercados sirve?", "Para viviendas, apartamentos, oficinas y proyectos ligeros de agua potable con RO silencioso sin bomba."),
            ("¿Acepta logotipo privado?", "Sí. Logotipo, etiquetas, manual y cajas se preparan tras confirmar la muestra."),
            ("¿Qué datos se necesitan?", "Presión de entrada, capacidad objetivo, calidad del agua y requisitos de embalaje."),
        ],
    },
    "de": {
        "lang_name": "Deutsch",
        "product_name": "Pumpenloser fünfstufiger RO-Wasserreiniger",
        "h1": "Pumpenloser fünfstufiger RO-Wasserreiniger für Leitungswasserdruck",
        "title": "Pumpenloser fünfstufiger RO-Wasserreiniger | OEM-Lieferant",
        "description": "Pumpenloser fünfstufiger RO-Wasserreiniger für stabilen Leitungswasserdruck mit PP, UDF, CTO, RO-Membran und T33 für OEM-Projekte.",
        "intro": "Dieser pumpenlose fünfstufige RO-Wasserreiniger ist für Märkte gedacht, in denen der kommunale Leitungswasserdruck stabil genug ist, um das System ohne Druckerhöhungspumpe zu betreiben. Die wandmontierte oder unter der Spüle installierte Einheit kombiniert PP-Sedimentfiltration, UDF/GAC-Aktivkohle, CTO-Kohleblock, RO-Membran und T33-Nachkohle für Trinkwasserprojekte in Haushalten, Wohnungen, Büros und leichten Gewerbeanwendungen. B2B-Käufer wählen ihn wegen geringerer Stromabhängigkeit, einfacher Wartung, OEM-Etiketten, individueller Kartons und flexibler Filterkonfiguration.",
        "gallery": "Produktbilder und Video",
        "overview": "Systemübersicht",
        "overview_text": "Das Modell eignet sich für Händler und Eigenmarken, die einen kompakten RO-Wasserreiniger ohne Pumpe benötigen. Bei stabilem Eingangsdruck reduziert die pumpenlose Struktur Geräusche, vereinfacht die Verdrahtung und erleichtert den Service.",
        "configuration": "Konfigurierbares Filtrationsdesign",
        "configuration_text": "Die Standardausführung umfasst PP für Sand und Rost, UDF oder GAC zur Reduzierung von Chlor und Geruch, CTO für zusätzliche Adsorption, eine RO-Membran zur Verringerung gelöster Stoffe und T33 zur Geschmacksverbesserung. Etiketten, Schnellverbinder, Armaturen und Kartons können markenspezifisch vorbereitet werden.",
        "specs": "Technische Daten",
        "applications": "Anwendungen für Käufer",
        "applications_text": "Das Gerät wird für Haushalte, Wohnungen, Büro-Teeküchen, Mietobjekte und Ersatzkartuschenmärkte eingesetzt. Besonders geeignet ist es dort, wo RO-Filtration mit ruhiger pumpenloser Struktur gefragt ist.",
        "quality": "Qualität und Exportservice",
        "quality_text": "Yuchen Water prüft Kunststoffteile, Anschlüsse, Schläuche und Kartuschen vor der Montage. Fertige Geräte können vor dem Versand auf Dichtheit, Durchfluss und Verpackungszustand geprüft werden.",
        "faq": "Häufige Fragen",
        "cta_title": "OEM-Angebot anfragen",
        "cta_text": "Senden Sie Zielmarkt, Druckbereich, Kartuschenwunsch, Logoanforderungen und Menge. Unser Ingenieur empfiehlt eine passende pumpenlose RO-Konfiguration.",
        "quote": "OEM-Angebot anfragen",
        "whatsapp": "WhatsApp-Vertrieb",
        "related": "Zurück zu Produkten",
        "video_label": "Produktvideo",
        "spec_rows": [
            ("Produkttyp", "Pumpenloser fünfstufiger RO-Wasserreiniger"),
            ("Filterstufen", "PP + UDF/GAC + CTO + RO-Membran + T33"),
            ("Betriebsart", "Betrieb mit stabilem Leitungswasserdruck, ohne Pumpe"),
            ("Installation", "Wandmontage oder unter der Spüle"),
            ("Anwendung", "Haushalt, Wohnung, Büro und leichtes Gewerbe"),
            ("Rohwasser", "Kommunales Leitungswasser mit geeignetem Eingangsdruck"),
            ("OEM/ODM", "Logo, Etiketten, Armatur, Anschlüsse, Verpackung und Anleitung"),
            ("MOQ", "Nach Spezifikation und Verpackungsplan"),
        ],
        "faqs": [
            ("Benötigt das Gerät eine Druckerhöhungspumpe?", "Nein. Es arbeitet mit Leitungswasserdruck; der lokale Eingangsdruck sollte bestätigt werden."),
            ("Welche fünf Filterstufen gibt es?", "PP, UDF oder GAC, CTO, RO-Membran und T33-Nachkohle."),
            ("Kann der Filtersatz angepasst werden?", "Ja. Kartuschenfolge, Etiketten, Anschlüsse, Armatur und Verpackung sind für OEM und ODM anpassbar."),
            ("Für welche Märkte ist es geeignet?", "Für Haushalte, Wohnungen, Büros und leichte Trinkwasserprojekte mit leiser pumpenloser RO-Struktur."),
            ("Ist ein eigenes Logo möglich?", "Ja. Logo, Etiketten, Anleitung und Exportkartons werden nach Musterfreigabe vorbereitet."),
            ("Welche Informationen werden benötigt?", "Eingangsdruck, Zielkapazität, Wasserqualität und Verpackungsanforderungen."),
        ],
    },
    "fr": {
        "lang_name": "Français",
        "product_name": "Purificateur RO cinq étapes sans pompe",
        "h1": "Purificateur RO cinq étapes sans pompe pour pression du réseau",
        "title": "Purificateur RO sans pompe cinq étapes | Fournisseur OEM",
        "description": "Purificateur RO cinq étapes sans pompe pour pression stable du réseau, avec PP, UDF, CTO, membrane RO et T33 pour projets OEM.",
        "intro": "Ce purificateur RO cinq étapes sans pompe est conçu pour les marchés où la pression de l'eau municipale suffit à faire fonctionner le système sans pompe de surpression. L'unité murale ou sous évier associe filtration PP contre les sédiments, charbon UDF/GAC, bloc carbone CTO, membrane RO et charbon final T33 pour les projets d'eau potable en maison, appartement, bureau et usage commercial léger. Les acheteurs B2B le choisissent pour sa moindre dépendance électrique, sa maintenance simple, l'étiquetage OEM, les cartons personnalisés et la configuration flexible des cartouches.",
        "gallery": "Galerie et vidéo du produit",
        "overview": "Présentation du système",
        "overview_text": "Ce modèle convient aux distributeurs et aux marques privées recherchant un purificateur RO compact sans pompe. Avec une pression d'entrée stable, la structure sans pompe réduit le bruit, simplifie le câblage et facilite l'entretien.",
        "configuration": "Conception de filtration configurable",
        "configuration_text": "La configuration standard comprend PP pour sable et rouille, UDF ou GAC pour réduire chlore et odeur, CTO pour l'adsorption complémentaire, membrane RO pour réduire les solides dissous et T33 pour affiner le goût. Étiquettes, raccords, robinetterie et cartons peuvent suivre l'identité du client.",
        "specs": "Caractéristiques techniques",
        "applications": "Applications acheteurs",
        "applications_text": "Le modèle est utilisé dans les maisons, appartements, bureaux, logements locatifs et marchés de cartouches de remplacement. Il est pertinent lorsque les clients souhaitent une filtration RO silencieuse sans pompe.",
        "quality": "Qualité et export",
        "quality_text": "Yuchen Water contrôle les pièces plastiques, raccords, tubes et cartouches avant assemblage. Les unités finies peuvent être vérifiées pour l'étanchéité, le débit et l'emballage avant expédition.",
        "faq": "Questions fréquentes",
        "cta_title": "Demander un devis OEM",
        "cta_text": "Indiquez le marché cible, la plage de pression, les cartouches souhaitées, les exigences de logo et la quantité. Notre ingénieur recommandera une configuration RO sans pompe adaptée.",
        "quote": "Demander un devis OEM",
        "whatsapp": "Ventes WhatsApp",
        "related": "Retour aux produits",
        "video_label": "Vidéo de démonstration du produit",
        "spec_rows": [
            ("Type de produit", "Purificateur RO cinq étapes sans pompe"),
            ("Étapes de filtration", "PP + UDF/GAC + CTO + membrane RO + T33"),
            ("Mode de fonctionnement", "Alimenté par pression stable du réseau, sans pompe"),
            ("Installation", "Murale ou sous évier"),
            ("Application", "Maison, appartement, bureau et usage commercial léger"),
            ("Eau d'alimentation", "Eau municipale avec pression d'entrée adaptée"),
            ("OEM/ODM", "Logo, étiquettes, robinet, raccords, emballage et manuel"),
            ("MOQ", "Selon la spécification et le plan d'emballage"),
        ],
        "faqs": [
            ("Faut-il une pompe de surpression ?", "Non. Le système fonctionne avec la pression du réseau, qui doit être confirmée pour le marché local."),
            ("Quelles sont les cinq étapes ?", "PP, UDF ou GAC, CTO, membrane RO et charbon final T33."),
            ("Le jeu de filtres est-il personnalisable ?", "Oui. Séquence, étiquettes, raccords, robinet et emballage peuvent être adaptés pour OEM et ODM."),
            ("Quels marchés sont adaptés ?", "Maisons, appartements, bureaux et petits projets d'eau potable recherchant un RO silencieux sans pompe."),
            ("Un logo privé est-il possible ?", "Oui. Logo, étiquettes, manuel et cartons d'exportation sont préparés après validation de l'échantillon."),
            ("Quelles données fournir ?", "Pression d'entrée, capacité visée, qualité de l'eau et exigences d'emballage."),
        ],
    },
    "vi": {
        "lang_name": "Tiếng Việt",
        "product_name": "Máy lọc RO năm cấp không bơm",
        "h1": "Máy lọc RO năm cấp không bơm dùng áp lực nước máy",
        "title": "Máy lọc RO năm cấp không bơm | Nhà cung cấp OEM",
        "description": "Máy lọc RO năm cấp không bơm dùng áp lực nước máy ổn định, gồm PP, UDF, CTO, màng RO và T33 cho dự án OEM.",
        "intro": "Máy lọc RO năm cấp không bơm này phù hợp với thị trường có áp lực nước máy ổn định, đủ để vận hành hệ thống mà không cần bơm tăng áp. Thiết kế treo tường hoặc lắp dưới bồn dùng lõi PP giữ cặn, than UDF/GAC, CTO, màng RO và than hậu T33 cho nước uống gia đình, căn hộ, văn phòng và ứng dụng thương mại nhẹ. Khách hàng B2B chọn model này vì giảm phụ thuộc điện, bảo trì đơn giản, hỗ trợ nhãn OEM, thùng carton riêng và cấu hình lõi lọc linh hoạt.",
        "gallery": "Hình ảnh và video sản phẩm",
        "overview": "Tổng quan hệ thống",
        "overview_text": "Sản phẩm phù hợp cho nhà phân phối và thương hiệu riêng cần một máy RO nhỏ gọn không dùng bơm. Khi áp lực đầu vào ổn định, cấu trúc không bơm giúp giảm tiếng ồn, đơn giản hóa dây điện và dễ bảo trì.",
        "configuration": "Thiết kế lọc có thể tùy chỉnh",
        "configuration_text": "Cấu hình tiêu chuẩn gồm PP để giữ cát và rỉ sét, UDF hoặc GAC để giảm clo và mùi, CTO để hấp phụ bổ sung, màng RO để giảm chất rắn hòa tan và T33 để cải thiện vị nước. Nhãn lõi, đầu nối nhanh, vòi và bao bì có thể tùy chỉnh theo thương hiệu.",
        "specs": "Thông số kỹ thuật",
        "applications": "Ứng dụng cho khách mua",
        "applications_text": "Model này dùng cho nước uống gia đình, căn hộ, khu văn phòng, nhà cho thuê và thị trường lõi thay thế. Đặc biệt phù hợp khi cần RO yên tĩnh, không dùng bơm.",
        "quality": "Chất lượng và xuất khẩu",
        "quality_text": "Yuchen Water kiểm tra linh kiện nhựa, đầu nối, ống và lõi lọc trước khi lắp ráp. Sản phẩm hoàn thiện có thể được kiểm tra độ kín, lưu lượng và tình trạng đóng gói trước khi giao hàng.",
        "faq": "Câu hỏi thường gặp",
        "cta_title": "Yêu cầu báo giá OEM",
        "cta_text": "Hãy gửi thị trường mục tiêu, dải áp lực nước, loại lõi mong muốn, yêu cầu logo và số lượng. Kỹ sư của chúng tôi sẽ đề xuất cấu hình RO không bơm phù hợp.",
        "quote": "Yêu cầu báo giá OEM",
        "whatsapp": "Bán hàng WhatsApp",
        "related": "Quay lại sản phẩm",
        "video_label": "Video trình diễn sản phẩm",
        "spec_rows": [
            ("Loại sản phẩm", "Máy lọc RO năm cấp không bơm"),
            ("Cấp lọc", "PP + UDF/GAC + CTO + màng RO + T33"),
            ("Cách vận hành", "Dùng áp lực nước máy ổn định, không có bơm"),
            ("Lắp đặt", "Treo tường hoặc dưới bồn"),
            ("Ứng dụng", "Gia đình, căn hộ, văn phòng và thương mại nhẹ"),
            ("Nước đầu vào", "Nước máy có áp lực phù hợp"),
            ("OEM/ODM", "Logo, nhãn, vòi, đầu nối, bao bì và hướng dẫn"),
            ("MOQ", "Xác nhận theo cấu hình và bao bì"),
        ],
        "faqs": [
            ("Máy có cần bơm tăng áp không?", "Không. Máy dùng áp lực nước máy, nên cần xác nhận áp lực tại thị trường địa phương."),
            ("Năm cấp lọc gồm gì?", "PP, UDF hoặc GAC, CTO, màng RO và than hậu T33."),
            ("Có tùy chỉnh lõi lọc không?", "Có. Thứ tự lõi, nhãn, đầu nối, vòi và bao bì đều có thể tùy chỉnh cho OEM và ODM."),
            ("Phù hợp với thị trường nào?", "Gia đình, căn hộ, văn phòng và dự án nước uống nhỏ cần hệ RO không bơm, vận hành êm."),
            ("Có thể dùng logo riêng không?", "Có. Logo, nhãn, hướng dẫn và thùng xuất khẩu được chuẩn bị sau khi duyệt mẫu."),
            ("Cần cung cấp thông tin gì?", "Áp lực nước, công suất mục tiêu, chất lượng nước và yêu cầu bao bì."),
        ],
    },
}

SHORT_TRANSLATIONS = {
    "zh": ("无泵五级RO净水机", "无泵五级RO净水机，依靠稳定市政自来水压力运行，采用PP、UDF/GAC、CTO、RO膜和T33后置碳，适合家用、办公和轻商用OEM项目。"),
    "ja": ("ポンプ不要の5段階RO浄水器", "安定した水道圧で作動するポンプ不要の5段階RO浄水器です。PP、UDF/GAC、CTO、RO膜、T33を組み合わせ、家庭、集合住宅、オフィス向けのOEM案件に適しています。"),
    "ko": ("펌프 없는 5단계 RO 정수기", "안정적인 수돗물 압력으로 작동하는 펌프 없는 5단계 RO 정수기입니다. PP, UDF/GAC, CTO, RO 멤브레인, T33 구성을 사용하며 가정, 아파트, 사무실 OEM 프로젝트에 적합합니다."),
    "ar": ("جهاز تنقية RO بخمس مراحل بدون مضخة", "جهاز تنقية RO بخمس مراحل يعمل بضغط مياه البلدية المستقر دون مضخة تعزيز، مع PP وUDF/GAC وCTO وغشاء RO وT33 لمشاريع المنازل والمكاتب والعلامات الخاصة."),
    "fa": ("دستگاه تصفیه RO پنج مرحله‌ای بدون پمپ", "این دستگاه RO پنج مرحله‌ای بدون پمپ با فشار پایدار آب شهری کار می‌کند و از PP، UDF/GAC، CTO، غشای RO و T33 برای پروژه‌های خانگی، اداری و برند خصوصی استفاده می‌کند."),
    "he": ("מטהר RO חמש-שלבי ללא משאבה", "מטהר RO חמש-שלבי הפועל בלחץ מי רשת יציב ללא משאבת הגברה, עם PP, UDF/GAC, CTO, ממברנת RO ו-T33 לפרויקטים ביתיים ומשרדיים."),
    "tr": ("Pompasız beş aşamalı RO su arıtma cihazı", "Stabil şebeke suyu basıncıyla çalışan pompasız beş aşamalı RO cihazıdır. PP, UDF/GAC, CTO, RO membran ve T33 yapısıyla ev, ofis ve hafif ticari OEM projelerine uygundur."),
    "it": ("Purificatore RO a cinque stadi senza pompa", "Purificatore RO a cinque stadi senza pompa, azionato da pressione stabile dell'acqua di rete, con PP, UDF/GAC, CTO, membrana RO e T33 per progetti OEM domestici e ufficio."),
    "nl": ("Pomploze vijftraps RO-waterzuiveraar", "Pomploze vijftraps RO-waterzuiveraar voor stabiele leidingwaterdruk, met PP, UDF/GAC, CTO, RO-membraan en T33 voor woningen, kantoren en OEM-projecten."),
    "pt": ("Purificador RO de cinco etapas sem bomba", "Purificador RO de cinco etapas sem bomba para pressão estável da rede, com PP, UDF/GAC, CTO, membrana RO e T33 para projetos OEM residenciais e de escritório."),
    "pl": ("Bezpompowy pięciostopniowy oczyszczacz RO", "Bezpompowy pięciostopniowy oczyszczacz RO działa przy stabilnym ciśnieniu wodociągowym i wykorzystuje PP, UDF/GAC, CTO, membranę RO oraz T33 w projektach OEM."),
    "cs": ("Pětistupňový RO čistič bez čerpadla", "Pětistupňový RO čistič bez čerpadla pracuje se stabilním tlakem vodovodní vody a používá PP, UDF/GAC, CTO, RO membránu a T33 pro domácí i kancelářské OEM projekty."),
    "sk": ("Päťstupňový RO čistič bez čerpadla", "Päťstupňový RO čistič bez čerpadla pracuje so stabilným tlakom vodovodnej vody a využíva PP, UDF/GAC, CTO, RO membránu a T33 pre OEM projekty."),
    "hu": ("Szivattyú nélküli ötlépcsős RO víztisztító", "Szivattyú nélküli ötlépcsős RO víztisztító stabil hálózati víznyomáshoz, PP, UDF/GAC, CTO, RO membrán és T33 szűréssel OEM projektekhez."),
    "ro": ("Purificator RO în cinci trepte fără pompă", "Purificator RO în cinci trepte fără pompă pentru presiune stabilă a apei de rețea, cu PP, UDF/GAC, CTO, membrană RO și T33 pentru proiecte OEM."),
    "bg": ("Петстепенен RO пречиствател без помпа", "Петстепенен RO пречиствател без помпа работи със стабилно налягане на водопровода и използва PP, UDF/GAC, CTO, RO мембрана и T33 за OEM проекти."),
    "hr": ("RO pročišćivač s pet stupnjeva bez pumpe", "RO pročišćivač s pet stupnjeva bez pumpe radi na stabilan tlak vodovoda i koristi PP, UDF/GAC, CTO, RO membranu i T33 za OEM projekte."),
    "sr": ("RO prečistač sa pet stepeni bez pumpe", "RO prečistač sa pet stepeni bez pumpe radi na stabilan pritisak vodovodne vode i koristi PP, UDF/GAC, CTO, RO membranu i T33 za OEM projekte."),
    "sl": ("Petstopenjski RO čistilnik brez črpalke", "Petstopenjski RO čistilnik brez črpalke deluje s stabilnim tlakom vodovodne vode in uporablja PP, UDF/GAC, CTO, RO membrano in T33 za OEM projekte."),
    "bs": ("RO pročišćivač s pet stepeni bez pumpe", "RO pročišćivač s pet stepeni bez pumpe radi na stabilan pritisak vodovodne vode i koristi PP, UDF/GAC, CTO, RO membranu i T33 za OEM projekte."),
    "cnr": ("RO prečistač sa pet stepeni bez pumpe", "RO prečistač sa pet stepeni bez pumpe radi na stabilan pritisak vodovodne vode i koristi PP, UDF/GAC, CTO, RO membranu i T33 za OEM projekte."),
    "sq": ("Pastrues RO me pesë faza pa pompë", "Pastrues RO me pesë faza pa pompë punon me presion të qëndrueshëm të ujit të rrjetit dhe përdor PP, UDF/GAC, CTO, membranë RO dhe T33 për projekte OEM."),
    "el": ("Πενταβάθμιο RO φίλτρο χωρίς αντλία", "Πενταβάθμιο RO φίλτρο χωρίς αντλία για σταθερή πίεση δικτύου, με PP, UDF/GAC, CTO, μεμβράνη RO και T33 για έργα OEM."),
    "lt": ("Be siurblio penkių pakopų RO valytuvas", "Be siurblio veikiantis penkių pakopų RO valytuvas naudoja stabilų vandentiekio slėgį ir PP, UDF/GAC, CTO, RO membraną bei T33 OEM projektams."),
    "lv": ("Piecu pakāpju RO attīrītājs bez sūkņa", "Piecu pakāpju RO attīrītājs bez sūkņa darbojas ar stabilu ūdensvada spiedienu un izmanto PP, UDF/GAC, CTO, RO membrānu un T33 OEM projektiem."),
    "et": ("Pumbata viieastmeline RO veepuhasti", "Pumbata viieastmeline RO veepuhasti töötab stabiilse kraanivee rõhuga ning kasutab PP, UDF/GAC, CTO, RO membraani ja T33 lahendust OEM-projektidele."),
    "fi": ("Pumputon viisivaiheinen RO-vedenpuhdistin", "Pumputon viisivaiheinen RO-vedenpuhdistin toimii vakaalla vesijohtopaineella ja käyttää PP-, UDF/GAC-, CTO-, RO-kalvo- ja T33-suodatusta OEM-projekteihin."),
    "da": ("Pumpefri femtrins RO-vandrenser", "Pumpefri femtrins RO-vandrenser til stabilt vandværkstryk med PP, UDF/GAC, CTO, RO-membran og T33 til OEM-projekter."),
    "no": ("Pumpefri femtrinns RO-vannrenser", "Pumpefri femtrinns RO-vannrenser for stabilt kommunalt vanntrykk, med PP, UDF/GAC, CTO, RO-membran og T33 for OEM-prosjekter."),
    "sv": ("Pumpfri femstegs RO-vattenrenare", "Pumpfri femstegs RO-vattenrenare för stabilt ledningsvattentryck, med PP, UDF/GAC, CTO, RO-membran och T33 för OEM-projekt."),
    "uk": ("П'ятиступенева RO-система без насоса", "П'ятиступенева RO-система без насоса працює від стабільного тиску водопроводу та використовує PP, UDF/GAC, CTO, RO-мембрану і T33 для OEM-проєктів."),
    "id": ("Penjernih RO lima tahap tanpa pompa", "Penjernih RO lima tahap tanpa pompa bekerja dengan tekanan air kota yang stabil, memakai PP, UDF/GAC, CTO, membran RO dan T33 untuk proyek OEM rumah dan kantor."),
    "ms": ("Penapis RO lima peringkat tanpa pam", "Penapis RO lima peringkat tanpa pam beroperasi dengan tekanan air paip yang stabil, menggunakan PP, UDF/GAC, CTO, membran RO dan T33 untuk projek OEM."),
    "tl": ("Limang-yugtong RO purifier na walang bomba", "Limang-yugtong RO purifier na walang bomba para sa matatag na presyon ng tubig sa gripo, gamit ang PP, UDF/GAC, CTO, RO membrane at T33 para sa mga proyektong OEM."),
    "th": ("เครื่องกรอง RO ห้าขั้นตอนไม่มีปั๊ม", "เครื่องกรอง RO ห้าขั้นตอนไม่มีปั๊ม ใช้แรงดันน้ำประปาที่เสถียร พร้อม PP, UDF/GAC, CTO, เมมเบรน RO และ T33 สำหรับงาน OEM."),
    "sw": ("Kichujio RO cha hatua tano bila pampu", "Kichujio RO cha hatua tano bila pampu hufanya kazi kwa shinikizo thabiti la maji ya bomba, kikiwa na PP, UDF/GAC, CTO, utando RO na T33 kwa miradi ya OEM."),
    "af": ("Pompvrye vyffase RO-waterreiniger", "Pompvrye vyffase RO-waterreiniger vir stabiele munisipale waterdruk, met PP, UDF/GAC, CTO, RO-membraan en T33 vir OEM-projekte."),
    "bn": ("পাম্প ছাড়া পাঁচ ধাপের RO পানি পরিশোধক", "স্থিতিশীল পৌর পানির চাপ দিয়ে চলা পাম্প ছাড়া পাঁচ ধাপের RO পানি পরিশোধক, PP, UDF/GAC, CTO, RO মেমব্রেন ও T33 সহ OEM প্রকল্পের জন্য।"),
    "hi": ("बिना पंप वाला पांच-चरण RO जल शोधक", "स्थिर नल-जल दबाव पर चलने वाला बिना पंप पांच-चरण RO जल शोधक, जिसमें PP, UDF/GAC, CTO, RO मेम्ब्रेन और T33 शामिल हैं।"),
    "uz": ("Nasossiz besh bosqichli RO suv tozalagich", "Barqaror vodoprovod bosimi bilan ishlaydigan nasossiz besh bosqichli RO suv tozalagich PP, UDF/GAC, CTO, RO membrana va T33 bilan OEM loyihalariga mos."),
    "kk": ("Сорғысыз бес сатылы RO су тазартқыш", "Тұрақты құбыр суының қысымымен жұмыс істейтін сорғысыз бес сатылы RO су тазартқыш PP, UDF/GAC, CTO, RO мембрана және T33 арқылы OEM жобаларына арналған."),
    "ky": ("Насоссуз беш баскычтуу RO суу тазалагыч", "Туруктуу түтүк суу басымы менен иштеген насоссуз беш баскычтуу RO суу тазалагыч PP, UDF/GAC, CTO, RO мембрана жана T33 менен OEM долбоорлоруна ылайыктуу."),
    "tg": ("Тозакунандаи RO панҷмарҳила бе насос", "Тозакунандаи RO панҷмарҳила бе насос бо фишори устувори оби шаҳр кор мекунад ва PP, UDF/GAC, CTO, мембранаи RO ва T33 дорад."),
    "tk": ("Nasossyz bäş basgançakly RO suw arassalaýjy", "Durnukly şäher suw basyşy bilen işleýän nasossyz bäş basgançakly RO suw arassalaýjy PP, UDF/GAC, CTO, RO membrana we T33 bilen OEM taslamalaryna laýyk."),
    "az": ("Nasossuz beş mərhələli RO su təmizləyici", "Sabit şəhər suyu təzyiqi ilə işləyən nasossuz beş mərhələli RO su təmizləyici PP, UDF/GAC, CTO, RO membran və T33 ilə OEM layihələrinə uyğundur."),
    "ka": ("ტუმბოს გარეშე ხუთსაფეხურიანი RO წყლის გამწმენდი", "ტუმბოს გარეშე ხუთსაფეხურიანი RO გამწმენდი მუშაობს სტაბილური ონკანის წყლის წნევით და იყენებს PP, UDF/GAC, CTO, RO მემბრანასა და T33-ს OEM პროექტებისთვის."),
    "hy": ("Առանց պոմպի հինգաստիճան RO ջրամաքրիչ", "Առանց պոմպի հինգաստիճան RO ջրամաքրիչը աշխատում է կայուն քաղաքային ջրի ճնշումով և օգտագործում է PP, UDF/GAC, CTO, RO մեմբրան և T33 OEM նախագծերի համար։"),
}

GENERIC_LABELS = {
    "en": t_en(),
}


def build_translation(lang: str) -> dict:
    if lang in TRANSLATIONS and "intro" in TRANSLATIONS[lang]:
        return TRANSLATIONS[lang]
    base = t_en().copy()
    name, desc = SHORT_TRANSLATIONS.get(lang, SHORT_TRANSLATIONS.get("en", (base["product_name"], base["description"])))
    base["lang_name"] = lang.upper()
    base["product_name"] = name
    base["h1"] = name
    base["title"] = f"{name} | Yuchen Water"
    base["description"] = desc
    base["intro"] = desc
    base["overview_text"] = desc
    base["configuration_text"] = desc
    base["applications_text"] = desc
    base["quality_text"] = desc
    return base


def html_escape(value: str) -> str:
    return html.escape(value, quote=True)


def json_ld(obj: dict) -> str:
    return '<script type="application/ld+json">\n' + json.dumps(obj, ensure_ascii=False, indent=2) + "\n</script>"


def detect_lang_dirs() -> list[str]:
    langs = []
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir():
            continue
        if path.name in {"assets", "reports", "tools", ".git", "__pycache__"}:
            continue
        if (path / "index.html").exists() or (path / "products.html").exists():
            langs.append(path.name)
    if "en" not in langs and (ROOT / "en").exists():
        langs.append("en")
    return sorted(set(langs))


def image_size(path: Path) -> tuple[int, int]:
    try:
        from PIL import Image

        with Image.open(path) as im:
            return im.size
    except Exception:
        return (1200, 900)


def copy_images() -> list[CopyAsset]:
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    copied: list[CopyAsset] = []
    for source, stem in IMAGE_SOURCES:
        src = Path(source)
        webp = ASSET_DIR / f"{stem}.webp"
        jpg = ASSET_DIR / f"{stem}.jpg"
        if not src.exists():
            copied.append(CopyAsset("", "", 0, 0, False, f"missing source: {src}"))
            continue
        try:
            from PIL import Image

            with Image.open(src) as im:
                im = im.convert("RGB")
                im.thumbnail((1600, 1600))
                im.save(webp, "WEBP", quality=84, method=6)
                width, height = im.size
            copied.append(CopyAsset(f"{BASE_URL}/assets/products/{webp.name}", f"../assets/products/{webp.name}", width, height, True, "webp"))
        except Exception as exc:
            shutil.copy2(src, jpg)
            width, height = image_size(jpg)
            copied.append(CopyAsset(f"{BASE_URL}/assets/products/{jpg.name}", f"../assets/products/{jpg.name}", width, height, True, f"jpg fallback: {exc}"))
    return copied


def copy_video() -> tuple[bool, str]:
    if not VIDEO_SOURCE.exists():
        return False, f"missing video: {VIDEO_SOURCE}"
    dest = ASSET_DIR / VIDEO_NAME
    shutil.copy2(VIDEO_SOURCE, dest)
    return True, f"../assets/products/{VIDEO_NAME}"


def replace_or_insert_title(text: str, title: str) -> str:
    if re.search(r"<title>.*?</title>", text, flags=re.I | re.S):
        return re.sub(r"<title>.*?</title>", f"<title>{html_escape(title)}</title>", text, count=1, flags=re.I | re.S)
    return text.replace("</head>", f"<title>{html_escape(title)}</title>\n</head>", 1)


def replace_meta(text: str, name: str, content: str) -> str:
    pattern = rf'<meta\s+name=["\']{re.escape(name)}["\'][^>]*>'
    tag = f'<meta name="{name}" content="{html_escape(content)}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", f"{tag}\n</head>", 1)


def replace_property(text: str, prop: str, content: str) -> str:
    pattern = rf'<meta\s+property=["\']{re.escape(prop)}["\'][^>]*>'
    tag = f'<meta property="{prop}" content="{html_escape(content)}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", f"{tag}\n</head>", 1)


def replace_canonical(text: str, href: str) -> str:
    pattern = r'<link\s+rel=["\']canonical["\'][^>]*>'
    tag = f'<link rel="canonical" href="{html_escape(href)}">'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    return text.replace("</head>", f"{tag}\n</head>", 1)


def normalize_head(text: str, lang: str, tr: dict, images: list[CopyAsset]) -> str:
    url = f"{BASE_URL}/{lang}/{SLUG}"
    image_url = next((i.url_path for i in images if i.ok), f"{BASE_URL}/assets/products/pump-free-five-stage-ro-water-purifier-front.webp")
    text = re.sub(r'<meta\s+name=["\']keywords["\'][^>]*>\s*', "", text, flags=re.I)
    text = re.sub(r'<meta\s+name=["\']revisit-after["\'][^>]*>\s*', "", text, flags=re.I)
    text = re.sub(r'\s*<script\s+type=["\']application/ld\+json["\'][^>]*>.*?</script>', "", text, flags=re.I | re.S)
    text = replace_or_insert_title(text, tr["title"])
    text = replace_meta(text, "description", tr["description"])
    text = replace_meta(text, "author", "Yuchen Water")
    text = replace_meta(text, "copyright", "Yuchen Water")
    text = replace_canonical(text, url)
    text = replace_property(text, "og:title", tr["title"])
    text = replace_property(text, "og:description", tr["description"])
    text = replace_property(text, "og:url", url)
    text = replace_property(text, "og:image", image_url)
    text = replace_property(text, "og:type", "product")
    text = re.sub(r"<html([^>]*)>", lambda m: html_tag(m.group(1), lang), text, count=1, flags=re.I)
    schema = schema_blocks(lang, tr, images)
    text = text.replace("</head>", schema + "\n</head>", 1)
    for old in ["Eco Express Water Equipment Co., Ltd.", "Eco Express Water Co., Ltd.", "Express Water"]:
        text = text.replace(old, "Yuchen Water")
    return text


def html_tag(attrs: str, lang: str) -> str:
    attrs = re.sub(r'\s+lang=["\'][^"\']*["\']', "", attrs, flags=re.I)
    attrs = re.sub(r'\s+dir=["\'][^"\']*["\']', "", attrs, flags=re.I)
    direction = ' dir="rtl"' if lang in RTL_LANGS else ""
    return f'<html lang="{html_escape(lang)}"{direction}{attrs}>'


def schema_blocks(lang: str, tr: dict, images: list[CopyAsset]) -> str:
    page_url = f"{BASE_URL}/{lang}/{SLUG}"
    img_urls = [i.url_path for i in images if i.ok]
    product = {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": tr["product_name"],
        "description": tr["description"],
        "brand": {"@type": "Brand", "name": "Yuchen Water"},
        "manufacturer": {"@type": "Organization", "name": "Yuchen Water"},
        "image": img_urls,
        "category": "RO water purifier",
        "url": page_url,
    }
    faq = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in tr["faqs"]
        ],
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{BASE_URL}/{lang}/"},
            {"@type": "ListItem", "position": 2, "name": "Products", "item": f"{BASE_URL}/{lang}/products.html"},
            {"@type": "ListItem", "position": 3, "name": tr["product_name"], "item": page_url},
        ],
    }
    return "\n".join([json_ld(product), json_ld(faq), json_ld(breadcrumb)])


def find_template(lang: str) -> Path:
    candidates = [
        ROOT / lang / "product-built-in-pressure-tank-ro.html",
        ROOT / lang / "product-ro-seawater-desalination-machine.html",
    ]
    candidates.extend(sorted((ROOT / lang).glob("product-*.html")))
    candidates.append(ROOT / "en" / "product-built-in-pressure-tank-ro.html")
    for path in candidates:
        if path.exists():
            return path
    raise FileNotFoundError(f"No product template found for {lang}")


def build_main(lang: str, tr: dict, images: list[CopyAsset], video_rel: str | None) -> str:
    dir_attr = ' dir="rtl"' if lang in RTL_LANGS else ""
    first = next((i for i in images if i.ok), None)
    hero_img = ""
    if first:
        hero_img = (
            f'<img src="{html_escape(first.rel_path)}" alt="{html_escape(tr["product_name"])}" '
            f'width="{first.width}" height="{first.height}" loading="eager" decoding="async">'
        )
    thumbs = []
    for asset in images:
        if not asset.ok:
            continue
        thumbs.append(
            f'<figure class="product-gallery__item">'
            f'<img src="{html_escape(asset.rel_path)}" alt="{html_escape(tr["product_name"])}" '
            f'width="{asset.width}" height="{asset.height}" loading="lazy" decoding="async">'
            f'</figure>'
        )
    video_html = ""
    if video_rel:
        video_html = (
            f'<figure class="product-gallery__item product-gallery__video">'
            f'<video controls preload="metadata" playsinline width="1200">'
            f'<source src="{html_escape(video_rel)}" type="video/mp4">'
            f'{html_escape(tr["video_label"])}'
            f'</video>'
            f'</figure>'
        )
    spec_rows = "\n".join(
        f"<tr><th>{html_escape(k)}</th><td>{html_escape(v)}</td></tr>" for k, v in tr["spec_rows"]
    )
    faq_items = "\n".join(
        f"<details><summary>{html_escape(q)}</summary><p>{html_escape(a)}</p></details>"
        for q, a in tr["faqs"]
    )
    return f"""
<main class="product-detail product-pump-free-ro" lang="{html_escape(lang)}"{dir_attr}>
  <nav class="breadcrumbs" aria-label="Breadcrumb">
    <a href="index.html">Home</a>
    <span>/</span>
    <a href="products.html">Products</a>
    <span>/</span>
    <span>{html_escape(tr["product_name"])}</span>
  </nav>

  <section class="product-hero">
    <div class="product-hero__copy">
      <p class="eyebrow">Yuchen Water OEM/ODM</p>
      <h1>{html_escape(tr["h1"])}</h1>
      <p>{html_escape(tr["intro"])}</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="contact.html">{html_escape(tr["quote"])}</a>
        <a class="btn btn-secondary" href="https://wa.me/8619908311885">{html_escape(tr["whatsapp"])}</a>
      </div>
    </div>
    <div class="product-hero__media">
      {hero_img}
    </div>
  </section>

  <section class="product-section">
    <h2>{html_escape(tr["gallery"])}</h2>
    <div class="product-gallery">
      {''.join(thumbs)}
      {video_html}
    </div>
  </section>

  <section class="product-section two-column">
    <div>
      <h2>{html_escape(tr["overview"])}</h2>
      <p>{html_escape(tr["overview_text"])}</p>
    </div>
    <div>
      <h2>{html_escape(tr["configuration"])}</h2>
      <p>{html_escape(tr["configuration_text"])}</p>
    </div>
  </section>

  <section class="product-section">
    <h2>{html_escape(tr["specs"])}</h2>
    <div class="table-wrap">
      <table class="spec-table">
        <tbody>
          {spec_rows}
        </tbody>
      </table>
    </div>
  </section>

  <section class="product-section two-column">
    <div>
      <h2>{html_escape(tr["applications"])}</h2>
      <p>{html_escape(tr["applications_text"])}</p>
    </div>
    <div>
      <h2>{html_escape(tr["quality"])}</h2>
      <p>{html_escape(tr["quality_text"])}</p>
    </div>
  </section>

  <section class="product-section faq-section">
    <h2>{html_escape(tr["faq"])}</h2>
    {faq_items}
  </section>

  <section class="product-cta">
    <h2>{html_escape(tr["cta_title"])}</h2>
    <p>{html_escape(tr["cta_text"])}</p>
    <div class="hero-actions">
      <a class="btn btn-primary" href="contact.html">{html_escape(tr["quote"])}</a>
      <a class="btn btn-secondary" href="products.html">{html_escape(tr["related"])}</a>
    </div>
  </section>
</main>
"""


def build_page(lang: str, images: list[CopyAsset], video_rel: str | None) -> tuple[Path, str]:
    tr = build_translation(lang)
    template = find_template(lang)
    text = template.read_text(encoding="utf-8", errors="ignore")
    text = normalize_head(text, lang, tr, images)
    main = build_main(lang, tr, images, video_rel)
    if re.search(r"<main\b.*?</main>", text, flags=re.I | re.S):
        text = re.sub(r"<main\b.*?</main>", main, text, count=1, flags=re.I | re.S)
    else:
        text = text.replace("</body>", main + "\n</body>", 1)
    dest = ROOT / lang / SLUG
    dest.write_text(text, encoding="utf-8")
    return dest, visible_language_check(main, lang)


def update_products_page(lang: str, images: list[CopyAsset]) -> bool:
    path = ROOT / lang / "products.html"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    if SLUG in text:
        return True
    tr = build_translation(lang)
    first = next((i for i in images if i.ok), None)
    img = ""
    if first:
        img = (
            f'<img src="{html_escape(first.rel_path)}" alt="{html_escape(tr["product_name"])}" '
            f'width="{first.width}" height="{first.height}" loading="lazy" decoding="async">'
        )
    card = f"""
<section class="product-added-section">
  <div class="container">
    <article class="product-card" data-category="ro-water-purifier">
      <a href="{SLUG}">
        {img}
        <h3>{html_escape(tr["product_name"])}</h3>
        <p>{html_escape(tr["description"])}</p>
      </a>
    </article>
  </div>
</section>
"""
    if re.search(r"</main>", text, flags=re.I):
        text = re.sub(r"</main>", card + "\n</main>", text, count=1, flags=re.I)
    else:
        text += card
    path.write_text(text, encoding="utf-8")
    return True


def visible_language_check(fragment: str, lang: str) -> str:
    if lang == "en":
        return "English source page"
    text = re.sub(r"<script\b.*?</script>", " ", fragment, flags=re.I | re.S)
    text = re.sub(r"<style\b.*?</style>", " ", text, flags=re.I | re.S)
    text = re.sub(r"<[^>]+>", " ", text)
    words = re.findall(r"\b[A-Za-z]{4,}\b", text)
    leftovers = []
    for word in words:
        if word in TECH_OK:
            continue
        if word.lower() in {"home", "products", "main", "lang", "href", "class", "type", "with"}:
            continue
        leftovers.append(word)
    unique = sorted(set(leftovers))
    if unique:
        return "check manually: " + ", ".join(unique[:12])
    return "no visible English leftovers except technical terms"


def update_sitemap(langs: list[str]) -> bool:
    path = ROOT / "sitemap.xml"
    if not path.exists():
        return False
    text = path.read_text(encoding="utf-8", errors="ignore")
    additions = []
    for lang in langs:
        url = f"{BASE_URL}/{lang}/{SLUG}"
        if url not in text:
            additions.append(f"  <url><loc>{url}</loc><lastmod>{TODAY}</lastmod></url>")
    if not additions:
        return True
    if "</urlset>" in text:
        text = text.replace("</urlset>", "\n" + "\n".join(additions) + "\n</urlset>")
    else:
        text += "\n" + "\n".join(additions)
    path.write_text(text, encoding="utf-8")
    return True


def zip_site() -> None:
    if ZIP_PATH.exists():
        ZIP_PATH.unlink()
    exclude_names = {".git", "__pycache__", ".DS_Store"}
    exclude_suffixes = {".zip", ".pyc"}
    with zipfile.ZipFile(ZIP_PATH, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as zf:
        for path in ROOT.rglob("*"):
            if path == ZIP_PATH:
                continue
            rel = path.relative_to(ROOT)
            parts = set(rel.parts)
            if parts & exclude_names:
                continue
            if path.name == "add_pump_free_ro_product.py":
                continue
            if path.suffix in exclude_suffixes:
                continue
            if path.is_file():
                zf.write(path, rel.as_posix())


def main() -> None:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    langs = detect_lang_dirs()
    images = copy_images()
    video_ok, video_rel = copy_video()
    video_path = video_rel if video_ok else None
    lines = [
        "Pump-free five-stage RO water purifier update",
        f"Date: {TODAY}",
        f"Languages detected: {len(langs)}",
        "",
        "Asset check:",
    ]
    for asset in images:
        lines.append(f"- {asset.rel_path or 'missing'} | {asset.width}x{asset.height} | {asset.note} | ok={asset.ok}")
    lines.append(f"- video | {video_rel} | ok={video_ok}")
    lines.append("")
    lines.append("Page check:")
    processed = []
    for lang in langs:
        try:
            page, check = build_page(lang, images, video_path)
            product_link = update_products_page(lang, images)
            processed.append(lang)
            lines.append(f"- {lang}: created {page.relative_to(ROOT)} | products link={product_link} | language={check}")
        except Exception as exc:
            lines.append(f"- {lang}: ERROR {exc}")
    sitemap_ok = update_sitemap(processed)
    lines.append("")
    lines.append(f"Sitemap updated: {sitemap_ok}")
    zip_site()
    lines.append(f"GitHub Pages zip: {ZIP_PATH}")
    report = REPORT_DIR / "pump-free-ro-product-verification-2026-06-29.txt"
    report.write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
