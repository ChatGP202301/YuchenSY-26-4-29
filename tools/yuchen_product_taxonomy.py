#!/usr/bin/env python3
"""Build the decision-complete 63-locale Yuchen Water product taxonomy.

The builder is deliberately deterministic.  It reads reviewed inventories and
existing localized pages, writes an isolated stage, and never publishes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import io
import json
import re
import shutil
from urllib.parse import quote_plus, urlencode
from copy import deepcopy
from functools import lru_cache
from pathlib import Path
from typing import Any, Iterable

from product_taxonomy_registry import (
    COMMERCIAL_GROUPS,
    COMMERCIAL_ROUTE,
    COMMERCIAL_ROUTES,
    FEATURED_ROUTES,
    INDUSTRIAL_ROUTE,
    OEM_FAMILIES,
    SOFTENER_ROUTE,
    SILIPHOS_ROUTE,
    SEAWATER_2000_ROUTE,
    YUCHEN_CATEGORIES,
    YUCHEN_DETAIL_ROUTES,
    YUCHEN_HUB_ROUTE,
    YUCHEN_PRIMARY_PARENT_BY_ROUTE,
    canonical_product_routes,
    NON_OEM_CANONICAL_ROUTES,
    family_by_key,
)
from quote_schema_policy import normalize_stage_html
from product_identity_corrections import correct_html


BASE_URL = "https://www.yuchensy.com/"
LASTMOD = "2026-08-12"
RTL = {"ar", "fa", "he", "ur"}
LOCALES_PATH = Path("migration/product-taxonomy/locales.json")
MENU_LABELS_PATH = Path("migration/product-taxonomy/menu-labels.json")
SOFTENER_FACTS = Path("migration/water-softeners/products.reviewed.en.json")
INDUSTRIAL_FACTS = Path("migration/ro-equipment-catalog/products.reviewed.en.json")
SEAWATER_2000_FACTS = Path("migration/2000lph-seawater-desalination/source.en.json")
OEM_INVENTORY = Path("migration/sanyishui/source-inventory.json")
OEM_TRANSLATIONS = Path("migration/multilingual-products/translations")
PRODUCT_FACTS = Path("migration/product-card-copy/facts.json")
CSS_ROUTE = Path("assets/product-taxonomy.css")
EN_QUICK_CHANGE_DETAIL_ROUTES = (
    "product-bayonet-lock-quick-change-pp-sediment-filter-cartridge.html",
    "product-bayonet-lock-quick-change-udf-coconut-shell-granular-activated-carbon-filter-cartridge.html",
    "product-bayonet-lock-quick-change-cto-coconut-shell-carbon-block-filter-cartridge.html",
    "product-bayonet-lock-quick-change-ro-membrane-filter-cartridge.html",
    "product-bayonet-lock-quick-change-t33-coconut-shell-activated-carbon-filter-cartridge.html",
)
EN_DISCOVERY_PILOT_ROUTES = {
    "products.html", "quick-change-water-filter-cartridges.html",
    *EN_QUICK_CHANGE_DETAIL_ROUTES,
}
REPORT_ROOT = Path("output/product-taxonomy-preview")
LEGACY_GUIDE_ROUTES = (
    "pp-melt-blown-filter-cartridge.html",
    "gac-udf-filter-cartridge.html",
    "cto-carbon-block-filter.html",
    "t33-inline-filter.html",
    "big-blue-filter-cartridge-selection-guide.html",
    "quick-connect-filter-cartridge-selection-guide.html",
    "mineralization-scale-inhibition-resin-filter-guide.html",
)

TAXONOMY_URL_START = "<!-- PRODUCT_TAXONOMY_V2_URLS_START -->"
TAXONOMY_URL_END = "<!-- PRODUCT_TAXONOMY_V2_URLS_END -->"
LLMS_START = "<!-- PRODUCT_TAXONOMY_V2_START -->"
LLMS_END = "<!-- PRODUCT_TAXONOMY_V2_END -->"
RO_CABINET_DETAIL_START = "<!-- RO_CABINET_UV_DETAIL_LINK_START -->"
RO_CABINET_DETAIL_END = "<!-- RO_CABINET_UV_DETAIL_LINK_END -->"

FALLBACK_CATEGORY_NAMES = {
    "be": {"ro_membrane": "Мембраны RO", "uf": "Мембранныя фільтры UF", "purifier": "Сістэмы ачысткі вады RO", "housing": "Карпусы фільтраў"},
    "cnr": {"ro_membrane": "RO membrane", "uf": "UF membranski filteri", "purifier": "RO sistemi za prečišćavanje vode", "housing": "Kućišta filtera"},
    "ga": {"ro_membrane": "Seicní RO", "uf": "Scagairí seicní UF", "purifier": "Córais íonúcháin uisce RO", "housing": "Cásálacha scagairí"},
    "lb": {"ro_membrane": "RO-Membranen", "uf": "UF-Membranfilter", "purifier": "RO-Waasserreinigungssystemer", "housing": "Filtergehäiser"},
    "mk": {"ro_membrane": "RO мембрани", "uf": "UF мембрански филтри", "purifier": "RO системи за прочистување вода", "housing": "Куќишта за филтри"},
    "mt": {"ro_membrane": "Membrani RO", "uf": "Filtri tal-membrana UF", "purifier": "Sistemi ta’ purifikazzjoni tal-ilma RO", "housing": "Housings tal-filtri"},
}

FOUNDATION_LOCALES = {
    "be": {"phone":"Тэлефон","email":"Электронная пошта","contact_title":"Запыт OEM/ODM прапановы","contact_intro":"Звяжыцеся з Yuchen Water наконт патрабаванняў да фільтрацыі вады, канструкцыі, колькасці і ўпакоўкі.","home_intro":"Прадукты і OEM/ODM вытворчасць Yuchen Water для фільтрацыі і ачысткі вады.","address":"Юаньхуа, Хайнін, Чжэцзян, Кітай"},
    "cnr": {"phone":"Telefon","email":"E-pošta","contact_title":"Zahtjev za OEM/ODM ponudu","contact_intro":"Kontaktirajte Yuchen Water u vezi sa zahtjevima za filtriranje vode, konstrukciju, količinu i pakovanje.","home_intro":"Yuchen Water proizvodi i OEM/ODM proizvodnja za filtriranje i prečišćavanje vode.","address":"Yuanhua, Haining, Zhejiang, Kina"},
    "ga": {"phone":"Fón","email":"Ríomhphost","contact_title":"Iarratas ar luachan OEM/ODM","contact_intro":"Déan teagmháil le Yuchen Water maidir le riachtanais scagacháin uisce, cumraíochta, cainníochta agus pacáistithe.","home_intro":"Táirgí Yuchen Water agus déantúsaíocht OEM/ODM do scagachán agus íonú uisce.","address":"Yuanhua, Haining, Zhejiang, an tSín"},
    "lb": {"phone":"Telefon","email":"E-Mail","contact_title":"OEM/ODM Offer ufroen","contact_intro":"Kontaktéiert Yuchen Water iwwer Ufuerderunge fir Waasserfiltratioun, Konfiguratioun, Quantitéit a Verpakung.","home_intro":"Yuchen Water Produkter an OEM/ODM Fabrikatioun fir Waasserfiltratioun a Waasserreinigung.","address":"Yuanhua, Haining, Zhejiang, China"},
    "mk": {"phone":"Телефон","email":"Е-пошта","contact_title":"Побарајте OEM/ODM понуда","contact_intro":"Контактирајте со Yuchen Water за барањата за филтрација на вода, конфигурација, количина и пакување.","home_intro":"Производи на Yuchen Water и OEM/ODM производство за филтрација и прочистување вода.","address":"Јуанхуа, Хаининг, Жеџијанг, Кина"},
    "mt": {"phone":"Telefon","email":"Email","contact_title":"Itlob kwotazzjoni OEM/ODM","contact_intro":"Ikkuntattja lil Yuchen Water dwar ir-rekwiżiti tal-filtrazzjoni tal-ilma, il-konfigurazzjoni, il-kwantità u l-ippakkjar.","home_intro":"Prodotti Yuchen Water u manifattura OEM/ODM għall-filtrazzjoni u l-purifikazzjoni tal-ilma.","address":"Yuanhua, Haining, Zhejiang, iċ-Ċina"},
}

EN_CATEGORY_NAMES = {
    "pp": "PP Melt-Blown Filter Cartridges",
    "cto": "CTO Carbon Block Filters",
    "gac": "GAC/UDF Filter Cartridges",
    "t33": "T33 Inline Filters",
    "ro_membrane": "RO Membranes",
    "uf": "UF Membrane Filters",
    "dispenser": "Water Dispensers",
    "purifier": "RO Water Purifiers",
    "housing": "Filter Housings",
    "softener": "Water Softener Systems",
    "industrial": "Industrial RO & Seawater Desalination Systems",
}

EN_PRODUCTS_PAGE_COPY = {
    "title": "OEM Water Filtration Products for Distributors | Yuchen Water",
    "heading": "Water Filtration Products for OEM and Distributor Sourcing",
    "description": "Choose a Yuchen Water product family and connection format, then send the project requirements that need review for an OEM water filtration quote.",
    "business_heading": "Choose a Sourcing Path",
    "business_intro": "Start with the route that matches the product scope: Yuchen Water product families, the OEM/ODM collection, or commercial and vending RO systems.",
    "featured_heading": "Products to Review",
    "featured_intro": "Open a product page to check the listed configuration, limits and quotation requirements before choosing a model.",
    "yuchen_gateway": "Browse Yuchen Water product families, then confirm the connection format and project requirements needed for quotation.",
    "oem_gateway": "Browse the OEM/ODM product collection, then confirm the connection format and project requirements needed for quotation.",
    "softener_category": "Compare water softener systems by product family and connection format. Final project requirements are reviewed before quotation.",
    "industrial_category": "Compare industrial RO and seawater desalination systems by product family and connection format. Final project requirements are reviewed before quotation.",
}

CATEGORY_IMAGES = {
    "pp": "../assets/products/pp-melt-blown-sediment-filter-cartridge-oem.webp",
    "cto": "../assets/products/cto-coconut-shell-carbon-block-filter-oem.webp",
    "gac": "../assets/products/gac-udf-filter-cartridge-oem.webp",
    "t33": "../assets/products/t33-coconut-shell-carbon-inline-filter-oem.webp",
    "ro_membrane": "../assets/products/ro-membrane-element-oem.webp",
    "uf": "../assets/products/uf-hollow-fiber-filter-oem.webp",
    "dispenser": "../assets/products/commercial-stainless-steel-ro-water-dispenser-e900-k27-oem-640.webp",
    "purifier": "../assets/products/smart-ro-water-purifier-400g-1200g-main-640.webp",
    "housing": "../assets/products/housing-filter/sus-304-jumbo-housing-main-640.webp",
    "softener": "../assets/products/water-softeners/yc-r2000-1024.webp",
    "industrial": "../assets/products/large-industrial-reverse-osmosis-water-treatment-equipment-3-100tph-oem.webp",
}


CSS = r"""/* Product taxonomy v2: buyer-first, crawlable and responsive. */
.commercial-site-header nav>a[data-products-link]{display:inline-flex!important}
.tx-table-wrap{max-width:100%;overflow-x:auto;-webkit-overflow-scrolling:touch}.tx-stats{max-width:100%;overflow:hidden}.tx-stat{min-width:0}
.tx-mobile-decision-actions{display:none}
@media(max-width:860px){.tx-mobile-decision-actions{display:grid;grid-template-columns:1fr;gap:8px;padding:10px 16px;background:#f0fbf8;border-bottom:1px solid rgba(15,143,134,.24)}.tx-mobile-decision-actions .tx-btn{width:100%;min-height:40px;padding:8px 10px;font-size:.88rem}.commercial-site-header nav{display:block!important;position:absolute;z-index:1200;top:66px;right:12px;width:min(360px,calc(100vw - 24px))}.commercial-site-header nav>a{display:none!important}.commercial-site-header .tx-mega-panel{max-height:70vh}}
@media(min-width:861px){.commercial-site-header .tx-mega-panel{left:auto;right:0;transform:none}}
@media(max-width:860px){.tx-mobile-decision-actions{margin-top:76px}}
@media(min-width:861px) and (max-width:1100px){.commercial-site-header .tx-mega-panel{position:fixed;left:16px;right:16px;top:70px;width:auto}}
@media(min-width:861px){.rcu-header .tx-mega-panel{left:auto;right:0;transform:none}}
@media(max-width:860px){.rcu-header .tx-mega-panel{position:fixed;left:16px;right:16px;top:90px;width:auto;max-height:calc(100vh - 110px)}.header,.header .container,.header .nav{max-width:100%;overflow-x:clip}}
@media(max-width:860px){html:has(body.catalog-mobile-fit){overflow-x:hidden}.catalog-mobile-fit{max-width:100vw;overflow-x:hidden}.catalog-mobile-fit *{max-width:100%;box-sizing:border-box}.catalog-mobile-fit h1,.catalog-mobile-fit h2{overflow-wrap:anywhere}.catalog-mobile-fit .container{width:calc(100% - 32px)!important;max-width:calc(100% - 32px)!important;margin-inline:auto!important}.catalog-mobile-fit .content-grid{grid-template-columns:minmax(0,1fr)!important}.catalog-mobile-fit .content-grid>*{min-width:0}.catalog-mobile-fit .product-gallery{display:grid!important;grid-template-columns:repeat(3,minmax(0,1fr))!important;gap:8px!important;width:100%!important}.catalog-mobile-fit .product-gallery>a,.catalog-mobile-fit .product-gallery img{display:block;width:100%!important;min-width:0!important}}
.tx-directory-actions{display:flex;flex-wrap:wrap;justify-content:center;gap:10px;margin-top:20px}.tx-directory-actions [data-compare-status]{flex-basis:100%;color:#52676d;font-size:.88rem}.tx-series-select{display:flex;align-items:center;justify-content:center}.tx-series-select input{width:20px;height:20px;accent-color:#0f8f86}.tx-context-catalog{width:min(1180px,calc(100% - 32px));margin:22px auto;padding:clamp(18px,3vw,30px);display:grid;grid-template-columns:minmax(0,1fr) auto;gap:24px;align-items:center;border:1px solid rgba(15,143,134,.24);border-radius:14px;background:linear-gradient(135deg,#f0fbf8,#fff);box-shadow:0 12px 30px rgba(16,42,50,.08)}.tx-context-catalog h2{margin:4px 0 8px;font-size:clamp(1.25rem,2vw,1.75rem)}.tx-context-catalog p{margin:0 0 8px}.tx-context-catalog ul{display:flex;flex-wrap:wrap;gap:8px 18px;margin:0;padding-left:20px;color:#52676d;font-size:.88rem}.tx-context-catalog .tx-btn{min-width:240px;text-align:center}.sr-only{position:absolute!important;width:1px;height:1px;padding:0;margin:-1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap;border:0}@media(max-width:768px){.tx-directory-actions{display:grid;grid-template-columns:1fr 1fr}.tx-directory-actions .tx-btn{width:100%;padding:11px 10px}.tx-context-catalog{grid-template-columns:1fr;margin:16px auto}.tx-context-catalog .tx-btn{width:100%;min-width:0}.tx-context-catalog ul{display:grid;gap:6px}.tx-series-row{grid-template-columns:28px 84px minmax(0,1fr)}}@media(max-width:520px){.tx-directory-actions{grid-template-columns:1fr}.tx-series-row{grid-template-columns:24px 72px minmax(0,1fr)}}
:root{--tx-ink:#12343b;--tx-teal:#0a776f;--tx-deep:#0e3038;--tx-gold:#c6a24a;--tx-paper:#f6faf9;--tx-blue:#edf4f6;--tx-line:#c9deda;--tx-white:#fff}
.taxonomy-page header .brand,.taxonomy-page header .nav-link{color:#173d45}.taxonomy-page .tx-stat{color:var(--tx-ink)}.taxonomy-page .tx-btn{color:var(--tx-teal)}.taxonomy-page .tx-btn--solid{color:#fff}.taxonomy-page .tx-btn--gold{color:#102f37}.taxonomy-page .tx-section--deep h2,.taxonomy-page .tx-section--deep p{color:#eaf7f4}.taxonomy-page .tx-section--deep .tx-eyebrow{color:#8ed8cf}.taxonomy-page .tx-section--deep .tx-btn{border-color:#eaf7f4;color:#eaf7f4}.taxonomy-page .tx-section--deep .tx-btn--gold{border-color:var(--tx-gold);color:#102f37}
.taxonomy-page{margin:0;color:var(--tx-ink);background:#fff}.taxonomy-page *{box-sizing:border-box}.tx-container{width:min(1200px,calc(100% - 32px));margin-inline:auto}.tx-hero{padding:clamp(52px,7vw,88px) 0;background:linear-gradient(130deg,#e6f4f1 0%,#f7f3e6 100%)}.tx-hero-grid{display:grid;grid-template-columns:minmax(0,1.4fr) minmax(260px,.6fr);gap:36px;align-items:end}.tx-eyebrow{display:inline-flex;color:var(--tx-teal);font-size:.8rem;font-weight:800;letter-spacing:.08em;text-transform:uppercase}.tx-hero h1{max-width:930px;margin:12px 0 18px;font-size:clamp(2.15rem,5vw,4.55rem);line-height:1.03}.tx-lede{max-width:790px;font-size:clamp(1rem,1.6vw,1.16rem);line-height:1.72}.tx-stats{display:grid;grid-template-columns:repeat(3,1fr);gap:9px}.tx-stat{padding:15px 10px;border:1px solid #bcd6d1;border-radius:12px;background:#ffffffbd;text-align:center}.tx-stat strong{display:block;font-size:1.35rem}.tx-actions{display:flex;flex-wrap:wrap;gap:11px;margin-top:24px}.tx-btn{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:11px 17px;border:1px solid var(--tx-teal);border-radius:7px;color:var(--tx-teal);font-weight:800;text-decoration:none}.tx-btn--solid{background:var(--tx-teal);color:#fff}.tx-btn--gold{border-color:var(--tx-gold);background:var(--tx-gold);color:#102f37}.tx-section{padding:clamp(48px,6vw,76px) 0}.tx-section--tint{background:var(--tx-paper)}.tx-section--deep{background:var(--tx-deep);color:#eaf7f4}.tx-section-head{max-width:820px;margin-bottom:28px}.tx-section-head h2{margin:8px 0 10px;font-size:clamp(1.65rem,3vw,2.45rem)}.tx-section-head p,.tx-card p{line-height:1.62}.tx-gateway-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:22px}.tx-category-grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px}.tx-product-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:18px}.tx-card{position:relative;overflow:hidden;min-width:0;border:1px solid var(--tx-line);border-radius:16px;background:#fff;box-shadow:0 9px 24px #12343b0a}.tx-card-media{display:flex;align-items:center;justify-content:center;aspect-ratio:4/3;padding:18px;background:linear-gradient(145deg,#eef4f6,#e4efee)}.tx-product-card .tx-card-media{aspect-ratio:1/1}.tx-card img{display:block;width:100%;height:100%;object-fit:contain}.tx-card-copy{padding:18px}.tx-card h3{margin:7px 0 10px;font-size:1.1rem;line-height:1.3}.tx-card h3 a{color:var(--tx-ink);text-decoration:none}.tx-card h3 a::after{position:absolute;inset:0;content:""}.tx-card .tx-btn{position:relative;z-index:1}.tx-count{display:inline-flex;padding:5px 9px;border-radius:999px;background:#dff0ec;color:#075f59;font-size:.78rem;font-weight:800}.tx-tags{display:flex;flex-wrap:wrap;gap:7px;margin:12px 0}.tx-tag{padding:5px 8px;border-radius:999px;background:var(--tx-blue);font-size:.77rem;font-weight:750}.tx-breadcrumb{display:flex;flex-wrap:wrap;gap:8px;margin-bottom:20px;font-size:.9rem}.tx-breadcrumb a{color:var(--tx-teal)}.tx-family-nav{display:flex;gap:9px;overflow:auto;padding:3px 0 13px;scrollbar-width:thin}.tx-family-nav a{white-space:nowrap}.tx-model-heading{margin:0 0 24px;font-size:clamp(1.5rem,3vw,2.2rem)}.tx-specs{display:grid;gap:7px;margin:14px 0 0}.tx-specs div{display:grid;grid-template-columns:minmax(110px,.8fr) 1.2fr;gap:9px;padding-top:7px;border-top:1px solid var(--tx-line)}.tx-specs dt{font-weight:800}.tx-specs dd{margin:0;overflow-wrap:anywhere}.tx-anchor{display:block;position:relative;top:-90px;visibility:hidden}.tx-note{padding:16px 18px;border-inline-start:4px solid var(--tx-gold);background:#fff9e8}.taxonomy-page[dir=rtl] .tx-card-copy,.taxonomy-page[dir=rtl] .tx-section-head{text-align:right}.taxonomy-page[dir=rtl] .tx-family-nav{direction:rtl}
.tx-product-card .tx-card-copy p{display:-webkit-box;overflow:hidden;-webkit-box-orient:vertical;-webkit-line-clamp:3}
@media(max-width:980px){.tx-hero-grid{grid-template-columns:1fr}.tx-product-grid{grid-template-columns:repeat(3,minmax(0,1fr))}.tx-gateway-grid,.tx-category-grid{grid-template-columns:repeat(2,minmax(0,1fr))}}
.tx-mega-menu:not([open])>.tx-mega-panel{display:none!important}
@media(max-width:720px){.tx-product-grid{grid-template-columns:repeat(2,minmax(0,1fr))}.tx-stats{max-width:430px}.taxonomy-page .header-row{align-items:flex-start}.taxonomy-page .nav{max-width:100%;overflow:auto}}
@media(max-width:560px){.tx-container{width:min(100% - 24px,1200px)}.tx-hero{padding:42px 0}.tx-gateway-grid,.tx-category-grid,.tx-product-grid{grid-template-columns:1fr}.tx-product-card{display:grid;grid-template-columns:124px minmax(0,1fr)}.tx-product-card .tx-card-media{aspect-ratio:auto;min-height:150px;padding:10px}.tx-product-card .tx-card-copy{padding:14px}.tx-product-card p{display:-webkit-box;overflow:hidden;-webkit-box-orient:vertical;-webkit-line-clamp:2}.tx-stats{grid-template-columns:repeat(3,minmax(0,1fr))}.tx-specs div{grid-template-columns:1fr}.lang-menu{max-width:calc(100vw - 24px)}}
.tx-mega-menu{position:relative}.tx-mega-menu>summary{cursor:pointer;list-style:none}.tx-mega-menu>summary::-webkit-details-marker{display:none}.tx-mega-menu>summary:after{content:"▾";margin-inline-start:6px;font-size:.72em}.tx-mega-menu[open]>summary:after{content:"▴"}.tx-mega-panel{position:absolute;top:calc(100% + 14px);left:50%;display:grid!important;grid-template-columns:repeat(2,minmax(250px,1fr));width:min(760px,calc(100vw - 32px));padding:18px!important;transform:translateX(-50%);border:1px solid var(--tx-line)!important;border-radius:16px!important;background:#fff!important;box-shadow:0 24px 64px #12343b2e!important;z-index:1300}.tx-mega-axis{display:grid;align-content:start;gap:4px;padding:4px 13px}.tx-mega-axis+.tx-mega-axis{border-inline-start:1px solid var(--tx-line)}.tx-mega-axis>strong{padding:8px 10px;color:var(--tx-ink);font-size:.8rem;letter-spacing:.05em;text-transform:uppercase}.tx-mega-panel .tx-mega-axis a{display:block;padding:9px 10px!important;border-radius:8px;color:var(--tx-ink)!important;line-height:1.25}.tx-mega-panel .tx-mega-axis a:hover,.tx-mega-panel .tx-mega-axis a:focus-visible{background:var(--tx-paper);color:var(--tx-teal)!important}.tx-mega-actions{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:8px;margin-top:12px;padding:14px 13px 0;border-top:1px solid var(--tx-line)}.tx-mega-actions a{flex:1;min-width:160px;padding:10px 12px!important;border:1px solid var(--tx-teal);border-radius:8px;color:var(--tx-teal)!important;text-align:center;font-weight:800}.tx-mega-actions a:last-child{background:var(--tx-teal);color:#fff!important}@media(max-width:860px){.tx-mega-menu{width:100%}.tx-mega-menu>summary{display:flex;align-items:center;justify-content:space-between}.tx-mega-panel{position:static;grid-template-columns:1fr;width:100%;max-height:68vh;overflow:auto;margin-top:8px;transform:none;box-shadow:none!important}.tx-mega-axis+.tx-mega-axis{border-inline-start:0;border-top:1px solid var(--tx-line)}.tx-mega-actions{display:grid;grid-template-columns:1fr}.tx-mega-actions a{width:100%}}
.tx-directory-section{background:var(--tx-paper)}.tx-capability-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px;margin-bottom:20px}.tx-capability-grid article{border:1px solid var(--tx-line);border-radius:14px;background:#fff;padding:20px}.tx-capability-grid h3{margin:0 0 7px}.tx-capability-grid p{margin:0 0 9px;color:#496168}.tx-capability-grid a{font-weight:800}.tx-directory-search{display:grid;gap:7px;margin:0 0 16px;color:var(--tx-ink);font-weight:800}.tx-directory-search input{width:100%;min-height:48px;border:1px solid #9ebbb6;border-radius:10px;background:#fff;padding:11px 14px;color:var(--tx-ink);font:inherit}.tx-product-directory{display:grid;gap:12px}.tx-product-directory>details{border:1px solid var(--tx-line);border-radius:15px;background:#fff;overflow:hidden}.tx-product-directory>details>summary{display:flex;align-items:center;justify-content:space-between;gap:16px;min-height:64px;padding:16px 20px;cursor:pointer;color:var(--tx-ink);font-size:1.08rem;font-weight:850}.tx-product-directory>details>summary small{color:var(--tx-teal);font-size:.78rem}.tx-product-directory>details[open]>summary{border-bottom:1px solid var(--tx-line);background:#eff7f5}.tx-series-list{display:grid}.tx-series-row{display:grid;grid-template-columns:96px minmax(0,1fr) minmax(160px,.25fr);gap:16px;align-items:center;padding:15px 18px;border-bottom:1px solid var(--tx-line)}.tx-series-row:last-child{border-bottom:0}.tx-series-media{display:grid;place-items:center;width:96px;height:82px;border-radius:10px;background:#edf4f5;overflow:hidden}.tx-series-media img{width:100%;height:100%;object-fit:contain;padding:7px}.tx-series-copy{display:grid;grid-template-columns:minmax(180px,.8fr) minmax(220px,1.2fr);gap:16px;align-items:center}.tx-series-copy h4{margin:3px 0 5px;font-size:1rem}.tx-series-copy p{margin:0;color:#536c72;font-size:.85rem;line-height:1.45}.tx-series-copy [data-sku-count]{color:var(--tx-teal);font-size:.74rem;font-weight:850;text-transform:uppercase}.tx-series-confirm{padding-inline-start:14px;border-inline-start:3px solid var(--tx-gold)}.tx-series-actions{display:grid;gap:7px}.tx-series-actions .tx-btn{min-height:39px;padding:8px 10px;font-size:.8rem}.tx-series-row[hidden],.tx-product-directory>details[hidden]{display:none!important}@media(max-width:900px){.tx-series-row{grid-template-columns:82px minmax(0,1fr)}.tx-series-media{width:82px;height:74px}.tx-series-copy{grid-template-columns:1fr}.tx-series-actions{grid-column:1/-1;grid-template-columns:repeat(2,1fr)}}@media(max-width:560px){.tx-capability-grid{grid-template-columns:1fr}.tx-product-directory>details>summary{padding:14px;font-size:.96rem}.tx-series-row{grid-template-columns:70px minmax(0,1fr);gap:11px;padding:13px}.tx-series-media{width:70px;height:70px}.tx-series-copy{display:block}.tx-series-confirm{margin-top:8px!important;padding:7px 0 0;border-inline-start:0;border-top:2px solid var(--tx-gold)}.tx-series-actions{grid-template-columns:1fr}.tx-series-actions .tx-btn{width:100%}}
"""


@lru_cache(maxsize=None)
def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text_only(value: str) -> str:
    return html.unescape(re.sub(r"<[^>]+>", " ", value)).replace("\xa0", " ").strip()


def compact(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def preserve_existing_block(template: str, rendered: str, start: str, end: str, anchor: str) -> str:
    """Keep a reviewed downstream block when rebuilding its parent page."""
    match = re.search(re.escape(start) + r".*?" + re.escape(end), template, re.S)
    if not match:
        return rendered
    if start in rendered or end in rendered:
        raise ValueError(f"generated page already contains preserved block: {start}")
    if rendered.count(anchor) != 1:
        raise ValueError(f"expected one insertion anchor for preserved block: {anchor}")
    return rendered.replace(anchor, match.group(0) + "\n" + anchor, 1)


def locale_codes(site_root: Path) -> list[str]:
    codes = list(read_json(site_root / LOCALES_PATH)["locales"])
    missing = [code for code in codes if not (site_root / code / "products.html").is_file()]
    if len(codes) != 63 or missing:
        raise ValueError(f"expected 63 locale roots, found={len(codes)} missing={missing}")
    return codes


@lru_cache(maxsize=None)
def locale_pack(site_root: Path, lang: str) -> dict[str, Any]:
    if lang == "en":
        raw = read_json(site_root / "migration/sanyishui-translations.en.json")
        return {
            "ui": {"home": "Home", "products": "Products", "contact": "Contact", "view": "View product", "summary": "Compare the product family, connection format and reviewed project requirements before requesting a quotation.", "collection": "OEM/ODM Product Collection", "technical_guides": "Technical selection guides", "catalog_entry": "OEM Product Catalog", "html_lang": "en", "dir": "ltr", "quick_change": "Bayonet-Lock Quick-Change Water Filter Cartridges"},
            "categories": {row["key"]: next(p["category_en"] for p in read_json(site_root / OEM_INVENTORY)["products"] if p["category_key"] == row["key"]) for row in OEM_FAMILIES},
            "products": {p["source_file"]: {"slug": p["route"], "name": p["name_en"], "summary": p["description_en"]} for p in read_json(site_root / OEM_INVENTORY)["products"]},
        }
    return read_json(site_root / OEM_TRANSLATIONS / f"{lang}.json")


@lru_cache(maxsize=None)
def hreflang(site_root: Path, lang: str) -> str:
    regional = {"cnr": "sr-Latn-ME", "sr-me": "sr-ME", "ga": "ga-IE", "lb": "lb-LU", "mk": "mk-MK", "mt": "mt-MT"}
    if lang in regional:
        return regional[lang]
    return locale_pack(site_root, lang)["ui"].get("html_lang", lang)


def alternates(site_root: Path, codes: Iterable[str], route: str) -> str:
    rows = [f'<link rel="alternate" hreflang="{esc(hreflang(site_root, c))}" href="{BASE_URL}{c}/{route}">' for c in codes]
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}en/{route}">')
    return "\n".join(rows)


def homepage_alternates(site_root: Path, codes: Iterable[str]) -> str:
    rows=[]
    for code in codes:
        href=BASE_URL if code=="en" else f"{BASE_URL}{code}/index.html"
        rows.append(f'<link rel="alternate" hreflang="{esc(hreflang(site_root,code))}" href="{href}">')
    rows.append(f'<link rel="alternate" hreflang="x-default" href="{BASE_URL}">')
    return "\n".join(rows)


def source_or_stage(site_root: Path, stage: Path, relative: Path) -> Path:
    staged = stage / relative
    return staged if staged.is_file() else site_root / relative


@lru_cache(maxsize=None)
def page_info(path: Path) -> dict[str, str]:
    if not path.is_file():
        return {}
    value = path.read_text(encoding="utf-8")
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", value, re.S | re.I)
    title = re.search(r"<title>(.*?)</title>", value, re.S | re.I)
    desc = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', value, re.I)
    main = re.search(r"<main\b.*?</main>", value, re.S | re.I)
    images = re.findall(r'<img\b[^>]*\bsrc="([^"]+)"', main.group(0) if main else value, re.I)
    image = next((x for x in images if "logo" not in x.lower() and not x.lower().endswith("icon.svg")), "../assets/logo.png")
    return {"title": text_only(h1.group(1) if h1 else title.group(1) if title else path.stem), "description": compact(html.unescape(desc.group(1))) if desc else "", "image": image}


def technical_signature(value: str) -> str:
    tokens = re.findall(r"(?:SUS\s*304|Big Blue|PPF|PP|UDF|CTO|GAC|T33|PCP|PCO|RO|UF|UV|SOE|DOE|\d+(?:\.\d+)?(?:[–-]\d+(?:\.\d+)?)?\s*(?:GPD|G|TPH|L/h|LPH|inch|W|V|Hz|L)?)", value, re.I)
    seen: list[str] = []
    for token in tokens:
        token = compact(token)
        if token.lower() not in {x.lower() for x in seen}:
            seen.append(token)
    return " · ".join(seen[:5])


@lru_cache(maxsize=None)
def menu_labels(site_root: Path, lang: str) -> dict[str, str]:
    source = read_json(site_root / MENU_LABELS_PATH)
    labels = source.get("labels", {}).get(lang)
    required = {"overview", "yuchen", "oem", "commercial"}
    if source.get("locale_count") != 63 or not isinstance(labels, dict) or set(labels) != required:
        raise ValueError(f"invalid Products menu labels for locale: {lang}")
    if any(not compact(str(labels[key])) for key in required):
        raise ValueError(f"empty Products menu label for locale: {lang}")
    return {key: compact(str(labels[key])) for key in required}


def products_menu(ui: dict[str, Any], labels: dict[str, str], route: str) -> str:
    if ui.get("html_lang") == "en":
        current = ' aria-current="page"' if route == "products.html" else ""
        return f'<a class="nav-link" data-products-link href="products.html"{current}>{esc(ui["products"])}</a>'
    targets = (
        ("products.html", labels["overview"]),
        (YUCHEN_HUB_ROUTE, labels["yuchen"]),
        ("sanyishui-products.html", labels["oem"]),
        (COMMERCIAL_ROUTE, labels["commercial"]),
    )
    links = "".join(
        f'<a href="{target}"{current}>{esc(label)}</a>'
        for target, label in targets
        for current in (' aria-current="page"' if route == target else "",)
    )
    return (
        '<details class="nav-resources sy-products-nav" data-oem-products-menu="true">'
        f'<summary class="nav-link">{esc(ui["products"])}</summary>'
        f'<div class="nav-resources-menu">{links}</div></details>'
    )


def patch_products_menu(text: str, ui: dict[str, Any], labels: dict[str, str], route: str) -> str:
    menu = products_menu(ui, labels, route)
    pattern = r'<details\b[^>]*class="[^"]*sy-products-nav[^"]*".*?</details>'
    if re.search(pattern, text, re.S | re.I):
        return re.sub(pattern, menu, text, count=1, flags=re.S | re.I)
    legacy = re.compile(
        r'<a\b(?=[^>]*href="products\.html")(?=[^>]*class="[^"]*\bnav-link\b[^"]*")[^>]*>.*?</a>',
        re.S | re.I,
    )
    updated = legacy.sub(menu, text, count=1)
    if updated != text:
        return updated
    plain = re.compile(r'<a\b(?=[^>]*href="products\.html")[^>]*>\s*Products\s*</a>', re.S | re.I)
    return plain.sub(menu, text, count=1)


def shell_parts(template: str, ui: dict[str, Any], labels: dict[str, str], route: str) -> tuple[str, str, str]:
    top = re.search(r'(<div\s+class="topbar".*?)(?=<header\b)', template, re.S | re.I)
    header = re.search(r"<header\b.*?</header>", template, re.S | re.I)
    footer = re.search(r"<footer\b.*?</footer>", template, re.S | re.I)
    top_html = top.group(1) if top else ""
    if top_html:
        balance = len(re.findall(r'<div\b', top_html, re.I)) - len(re.findall(r'</div>', top_html, re.I))
        if balance < 0:
            raise ValueError("topbar template contains unmatched closing divs")
        top_html = top_html.rstrip() + ("</div>" * balance)
    if not header:
        raise ValueError("standard header missing from locale template")
    header_html = header.group(0)
    header_html = patch_products_menu(header_html, ui, labels, route)
    return top_html, header_html, footer.group(0) if footer else ""


def route_language_links(header: str, route: str) -> str:
    def patch_anchor(match: re.Match[str]) -> str:
        tag = match.group(0)
        if not re.search(r'\bclass=["\'][^"\']*\blang-option\b', tag, re.I):
            return tag
        return re.sub(
            r'(\bhref=["\'])\.\./([^/"\']+)/[^"\']+(["\'])',
            lambda href: f'{href.group(1)}../{href.group(2)}/{route}{href.group(3)}',
            tag,
            count=1,
            flags=re.I,
        )

    def patch_option(match: re.Match[str]) -> str:
        tag = match.group(0)
        return re.sub(
            r'(\bvalue=["\'])\.\./([^/"\']+)/[^"\']+(["\'])',
            lambda value: f'{value.group(1)}../{value.group(2)}/{route}{value.group(3)}',
            tag,
            count=1,
            flags=re.I,
        )

    header = re.sub(r'<a\b[^>]*>', patch_anchor, header, flags=re.I)
    return re.sub(r'<option\b[^>]*>', patch_option, header, flags=re.I)


def breadcrumb_html(ui: dict[str, Any], entries: list[tuple[str, str | None]]) -> str:
    home_href = "../" if ui.get("html_lang") == "en" else "index.html"
    rows = [f'<a href="{home_href}">{esc(ui["home"])}</a>', '<span>›</span>', f'<a href="products.html">{esc(ui["products"])}</a>']
    for name, route in entries:
        rows.extend(['<span>›</span>', f'<a href="{esc(route)}">{esc(name)}</a>' if route else f'<span>{esc(name)}</span>'])
    return '<nav class="tx-breadcrumb breadcrumb" aria-label="Breadcrumb">' + "".join(rows) + "</nav>"


def breadcrumb_schema(lang: str, ui: dict[str, Any], route: str, entries: list[tuple[str, str | None]]) -> dict[str, Any]:
    home_url = BASE_URL if lang == "en" else f"{BASE_URL}{lang}/index.html"
    items = [
        {"@type": "ListItem", "position": 1, "name": ui["home"], "item": home_url},
        {"@type": "ListItem", "position": 2, "name": ui["products"], "item": f"{BASE_URL}{lang}/products.html"},
    ]
    for name, target in entries:
        items.append({"@type": "ListItem", "position": len(items) + 1, "name": name, "item": f"{BASE_URL}{lang}/{target or route}"})
    return {"@type": "BreadcrumbList", "itemListElement": items}


def render_shell(site_root: Path, codes: list[str], lang: str, template: str, route: str, title: str, description: str, main: str, schema: dict[str, Any], image: str) -> str:
    pack = locale_pack(site_root, lang)
    ui = pack["ui"]
    top, header, footer = shell_parts(template, ui, menu_labels(site_root, lang), route)
    header = route_language_links(header, route)
    direction = "rtl" if lang in RTL else "ltr"
    html_lang = ui.get("html_lang", lang)
    canonical = f"{BASE_URL}{lang}/{route}"
    image_url = image if image.startswith("http") else f'{BASE_URL}{image.removeprefix("../")}'
    document = f'''<!doctype html><html lang="{esc(html_lang)}" dir="{direction}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(title)}</title><meta name="description" content="{esc(description)}"><meta name="robots" content="index,follow"><link rel="canonical" href="{canonical}">
{alternates(site_root,codes,route)}<link rel="stylesheet" href="../assets/styles.min.css?v=20260714-product-title-links"><link rel="stylesheet" href="../assets/product-taxonomy.css?v=20260811-v2"><meta property="og:type" content="website"><meta property="og:title" content="{esc(title)}"><meta property="og:description" content="{esc(description)}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{esc(image_url)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:image" content="{esc(image_url)}"><script type="application/ld+json">{json.dumps(schema,ensure_ascii=False,separators=(",",":"))}</script><link rel="icon" href="../assets/logo.png" type="image/png"></head><body class="taxonomy-page" dir="{direction}">{top}{header}{main}{footer}<script src="../assets/site.min.js?v=20260810-oem63-menu" defer></script></body></html>'''
    if lang == "en":
        document = re.sub(r'href=["\']index\.html(?:#[^"\']*)?["\']', 'href="../"', document)
    if not (site_root / lang / "filter-cartridge-catalog.html").is_file():
        document = document.replace('href="filter-cartridge-catalog.html"', 'href="../en/filter-cartridge-catalog.html"')
    return document


def patch_homepage(site_root:Path,codes:list[str],text:str,lang:str)->str:
    text=normalize_topbar_structure(text)
    text=patch_products_menu(text,locale_pack(site_root,lang)["ui"],menu_labels(site_root,lang),"index.html")
    text=route_language_links(text,"index.html")
    text=re.sub(r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>',"",text,flags=re.I)
    canonical=BASE_URL if lang=="en" else f'{BASE_URL}{lang}/index.html'
    match=re.search(r'<link\s+rel="canonical"\s+href="[^"]+"\s*/?>',text,re.I)
    replacement=f'<link rel="canonical" href="{canonical}">\n{homepage_alternates(site_root,codes)}'
    text=text[:match.start()]+replacement+text[match.end():] if match else text.replace('</head>',replacement+'\n</head>',1)
    if lang=="en":
        return re.sub(r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>','<meta name="robots" content="noindex,follow">',text,count=1,flags=re.I)
    return ensure_indexable(text)


def render_foundation_home(site_root:Path,codes:list[str],lang:str,template:str,stage:Path)->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];local=FOUNDATION_LOCALES[lang];labels=menu_labels(site_root,lang)
    yuchen=labels["yuchen"]
    commercial=page_info(source_or_stage(site_root,stage,Path(lang)/COMMERCIAL_ROUTE)).get("title",f'RO · {ui["products"]}')
    cards="".join((
        card(yuchen,YUCHEN_HUB_ROUTE,{"image":CATEGORY_IMAGES["purifier"]},local["home_intro"]),
        card(labels["oem"],"sanyishui-products.html",{"image":"../assets/catalog/yuchen-water-oem-catalog-cover-960.webp"},ui["summary"]),
        card(labels["commercial"],COMMERCIAL_ROUTE,{"image":"../assets/products/commercial-ro/p05-e500-s-commercial-dispenser-640.webp"},commercial),
    ))
    title=f'Yuchen Water · {ui["products"]}'
    canonical=f'{BASE_URL}{lang}/index.html'
    schema={"@context":"https://schema.org","@graph":[{"@type":"WebPage","url":canonical,"name":title,"description":local["home_intro"],"inLanguage":ui.get("html_lang",lang)},{"@type":"Organization","@id":BASE_URL+"#organization","name":"Yuchen Water","url":BASE_URL,"email":"expresswater025@gmail.com","telephone":"+86-19908311885"}]}
    main=f'<main><section class="tx-hero"><div class="tx-container"><span class="tx-eyebrow">Yuchen Water · OEM/ODM · RO</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(local["home_intro"])}</p><div class="tx-actions"><a class="tx-btn tx-btn--solid" href="products.html">{esc(ui["products"])}</a><a class="tx-btn" href="contact.html">{esc(ui["contact"])}</a></div></div></section><section class="tx-section"><div class="tx-container"><div class="tx-gateway-grid">{cards}</div></div></section></main>'
    return patch_homepage(site_root,codes,render_shell(site_root,codes,lang,template,"index.html",title,local["home_intro"],main,schema,"assets/products/smart-ro-water-purifier-400g-1200g-oem.webp"),lang)


def render_foundation_contact(site_root:Path,codes:list[str],lang:str,template:str)->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];local=FOUNDATION_LOCALES[lang];title=local["contact_title"];canonical=f'{BASE_URL}{lang}/contact.html'
    crumbs=[(ui["contact"],None)]
    schema={"@context":"https://schema.org","@graph":[{"@type":"ContactPage","url":canonical,"name":title,"description":local["contact_intro"],"inLanguage":ui.get("html_lang",lang)},breadcrumb_schema(lang,ui,"contact.html",crumbs),{"@type":"Organization","@id":BASE_URL+"#organization","name":"Yuchen Water","url":BASE_URL,"email":"expresswater025@gmail.com","telephone":"+86-19908311885","address":{"@type":"PostalAddress","addressCountry":"CN"}}]}
    main=f'<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">Yuchen Water · OEM/ODM</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(local["contact_intro"])}</p></div></section><section class="tx-section"><div class="tx-container"><div class="tx-category-grid"><article class="tx-card"><div class="tx-card-copy"><h2>{esc(ui["contact"])}</h2><dl class="tx-specs"><div><dt>{esc(local["phone"])}</dt><dd><a href="tel:+8619908311885">+86-19908311885</a></dd></div><div><dt>{esc(local["email"])}</dt><dd><a href="mailto:expresswater025@gmail.com">expresswater025@gmail.com</a></dd></div><div><dt>{esc(ui["contact"])}</dt><dd>{esc(local["address"])}</dd></div></dl></div></article><article class="tx-card"><div class="tx-card-copy"><h2>{esc(ui["collection"])}</h2><p>{esc(ui["summary"])}</p><a class="tx-btn" href="sanyishui-products.html">{esc(ui["collection"])}</a></div></article></div></div></section></main>'
    return render_shell(site_root,codes,lang,template,"contact.html",title,local["contact_intro"],main,schema,"assets/logo.png")


def image_markup(info: dict[str, str], title: str, eager: bool = False) -> str:
    image = info.get("image", "../assets/logo.png")
    return f'<div class="tx-card-media"><img src="{esc(image)}" alt="{esc(title)}" loading="{"eager" if eager else "lazy"}" decoding="async"></div>'


def card(title: str, route: str, info: dict[str, str], summary: str, count: str = "", product: bool = False, cta: str = "") -> str:
    klass = "tx-card tx-product-card" if product else "tx-card"
    badge = f'<span class="tx-count">{esc(count)}</span>' if count else ""
    action = f'<a class="tx-btn" href="{esc(route)}">{esc(cta)}</a>' if cta else ""
    media = image_markup(info, title)
    if product:
        media = f'<a class="tx-card-image-link" href="{esc(route)}" aria-label="{esc(title)}">{media}</a>'
    return f'<article class="{klass}">{media}<div class="tx-card-copy">{badge}<h3><a href="{esc(route)}">{esc(title)}</a></h3><p>{esc(summary)}</p>{action}</div></article>'


def discovery_series_row(label: str, route: str, image: str, count: str, purpose: str, confirm: str, catalog: str) -> str:
    catalog_path = catalog.split("?", 1)[0]
    catalog_label = {
        "filter-cartridge-catalog.html": "View Filter Cartridge Catalog",
        "sanyishui-catalog.html": "Download OEM Product Catalog",
        "commercial-ro-water-systems-catalog.html": "Download Commercial RO Catalog",
    }[catalog_path]
    return f'''<article class="tx-series-row" data-series-row><label class="tx-series-select"><input type="checkbox" data-series-select value="{esc(route)}"><span class="sr-only">Select {esc(label)} for comparison</span></label><div class="tx-series-media"><img src="{esc(image)}" alt="{esc(label)}" loading="lazy" decoding="async"></div><div class="tx-series-copy"><div><span data-sku-count>{esc(count)}</span><h4>{esc(label)}</h4><p>{esc(purpose)}</p></div><p class="tx-series-confirm" data-confirm-boundary><strong>Confirm:</strong> {esc(confirm)}</p></div><div class="tx-series-actions"><a class="tx-btn tx-btn--solid" data-compare-series href="{esc(route)}">Compare Series</a><a class="tx-btn" data-context-catalog href="{esc(catalog)}">{catalog_label}</a></div></article>'''


def discovery_group(group_id: str, title: str, rows: list[str], opened: bool = False) -> str:
    return f'''<details id="catalog-{esc(group_id)}" data-catalog-group="{esc(group_id)}"{" open" if opened else ""}><summary><span>{esc(title)}</span><small>{len(rows)} series</small></summary><div class="tx-series-list">{"".join(rows)}</div></details>'''


def oem_inventory(site_root: Path) -> list[dict[str, Any]]:
    products = read_json(site_root / OEM_INVENTORY)["products"]
    by_key = {row["key"]: 0 for row in OEM_FAMILIES}
    for product in products:
        by_key[product["category_key"]] += 1
    expected = {row["key"]: row["count"] for row in OEM_FAMILIES}
    if by_key != expected:
        raise ValueError(f"OEM family inventory drift: {by_key}")
    return products


def _english_public_route(site_root: Path, route: str) -> str:
    text = (site_root / "en" / route).read_text(encoding="utf-8")
    match = re.search(r'<link\s+rel="canonical"\s+href="[^"]+/([^/"?#]+\.html)"', text, re.I)
    return match.group(1) if match else route


def _evidence_primary_series(site_root: Path, route: str, parent: str) -> str:
    text = (site_root / "en" / route).read_text(encoding="utf-8", errors="ignore")
    # Deliberately ignore navigation, related products and footer copy.  Those
    # areas mention every category and previously caused a self-fulfilling
    # "commercial" classification.  Only the page's own title, description,
    # H1 and explicit Product type row are classification evidence.
    evidence_parts = re.findall(
        r'<title>(.*?)</title>|<meta\s+name="description"\s+content="([^"]*)"|<h1[^>]*>(.*?)</h1>|<tr><th>PRODUCT TYPE</th><td>(.*?)</td></tr>|<tr><th>Product type</th><td>(.*?)</td></tr>',
        text, re.I | re.S,
    )
    visible = re.sub(r"<[^>]+>", " ", " ".join(" ".join(parts) for parts in evidence_parts))
    if re.search(r"\b(?:commercial\b.{0,80}\b(?:ro|reverse osmosis|water dispenser|water purifier)|industrial\b.{0,80}\b(?:ro|reverse osmosis)|seawater desalination|water vending)\b", visible, re.I):
        return COMMERCIAL_ROUTE
    return parent


def english_primary_series(site_root: Path, oem: list[dict[str, Any]]) -> dict[str, str]:
    family_routes = {row["key"]: row["route"] for row in OEM_FAMILIES}
    mapping = {_english_public_route(site_root, row["route"]): family_routes[row["category_key"]] for row in oem}
    mapping.update(YUCHEN_PRIMARY_PARENT_BY_ROUTE)
    mapping.update({route: COMMERCIAL_ROUTE for route in COMMERCIAL_ROUTES})
    mapping = {route: _evidence_primary_series(site_root, route, parent) for route, parent in mapping.items()}
    if len(mapping) != 159:
        raise ValueError(f"English primary-series mapping must contain 159 products, found {len(mapping)}")
    return mapping


def catalog_profile(primary_series: str) -> dict[str, str]:
    filter_series = {
        *(row["route"] for row in OEM_FAMILIES if row["key"] != "pipeline"),
        "pp-melt-blown-filter-cartridge.html", "cto-carbon-block-filter.html",
        "gac-udf-filter-cartridge.html", "t33-inline-filter.html",
        "ro-membrane.html", "uf-membrane-filter.html",
    }
    if primary_series in {COMMERCIAL_ROUTE, INDUSTRIAL_ROUTE}:
        return {"kind": "commercial", "route": "commercial-ro-water-systems-catalog.html", "label": "Download Commercial RO Catalog", "scope": "Commercial and vending RO water systems, configuration options and OEM/ODM planning.", "access": "Private PDF · project form required."}
    if primary_series in filter_series:
        return {"kind": "filter", "route": "filter-cartridge-catalog.html", "label": "View Filter Cartridge Catalog", "scope": "PP, GAC/UDF, CTO, T33, RO, UF and specialty filter programs.", "access": "Private 50-page English OEM PDF · business contact form required."}
    return {"kind": "oem", "route": "sanyishui-catalog.html", "label": "Download OEM Product Catalog", "scope": "Instant-heating water dispensers and the OEM filter-cartridge collection.", "access": "Private PDF · complete buyer and project form required."}


def catalog_interest(page_text: str, primary_series: str) -> str:
    if catalog_profile(primary_series)["kind"] != "filter":
        return ""
    # Navigation contains every media label, so whole-document keyword matching
    # makes every filter look like the first menu item.  Restrict the decision to
    # product facts plus the already-reviewed primary series.
    factual_parts = re.findall(
        r"<(?:title|h1)\b[^>]*>(.*?)</(?:title|h1)>|<meta\s+name=[\"']description[\"']\s+content=[\"']([^\"']+)",
        page_text,
        re.I | re.S,
    )
    visible = " ".join(" ".join(part for part in pair if part) for pair in factual_parts)
    visible += " " + primary_series.removesuffix(".html").replace("-", " ")
    for pattern, value in (
        (r"\b(?:GAC|UDF)\b", "gac-udf"), (r"\bCTO\b", "cto"),
        (r"\bT33\b", "t33"), (r"\bUF\b", "uf"),
        (r"\bRO\s+membrane\b", "ro"), (r"\b(?:PP|PPF)\b", "pp"),
        (r"\b(?:resin|mineral|ceramic|scale.inhibition|specialty)\b", "specialty"),
    ):
        if re.search(pattern, visible, re.I):
            return value
    return ""


def context_catalog_card(route: str, primary_series: str, location: str, product_id: str = "", interest: str = "") -> str:
    profile = catalog_profile(primary_series).copy()
    if route == "product-cabinet-ro-water-purifier-5-6-stage-uv.html":
        profile["scope"] = "Cabinet RO water purifier configurations, optional UV and project-specific OEM/ODM requirements."
    params = {"language": "en", "source_page": route, "primary_series": primary_series.removesuffix(".html"), "catalog_kind": profile["kind"], "cta_location": location}
    if product_id:
        params["product_id"] = product_id
    if interest:
        params["interest"] = interest
    href = f'{profile["route"]}?{urlencode(params)}'
    quote = ""
    if product_id:
        quote_params = {
            "product_id": product_id,
            "language": "en",
            "source_page": route,
            "family": primary_series.removesuffix(".html"),
            "cta_location": "product_detail_primary",
        }
        quote = f'<a class="tx-btn tx-btn--outline" data-primary-cta="true" href="contact.html?{esc(urlencode(quote_params))}">Submit Project Parameters / Request Quote</a>'
    return f'''<aside class="tx-context-catalog" data-context-catalog-card data-catalog-kind="{profile["kind"]}"><div><span class="tx-eyebrow">Relevant English catalog</span><h2>{profile["label"]}</h2><p data-catalog-scope>{profile["scope"]}</p><ul><li data-catalog-access>{profile["access"]}</li><li data-catalog-language>English · 2026 edition</li><li>Edition date not published</li></ul></div><div class="tx-context-catalog__actions"><a class="tx-btn tx-btn--solid" data-catalog-cta href="{esc(href)}">{profile["label"]}</a>{quote}</div></aside>'''


def mobile_decision_actions(route: str, primary_series: str, product_id: str, interest: str = "") -> str:
    profile = catalog_profile(primary_series)
    common = {"product_id": product_id, "language": "en", "source_page": route, "primary_series": primary_series.removesuffix(".html"), "catalog_kind": profile["kind"]}
    if interest:
        common["interest"] = interest
    catalog = urlencode({**common, "cta_location": "product_mobile_first_view"})
    quote = urlencode({**common, "cta_location": "product_mobile_primary"})
    return f'''<div class="tx-mobile-decision-actions" data-mobile-decision-actions><a class="tx-btn tx-btn--solid" data-primary-cta="true" href="contact.html?{esc(quote)}">Submit Project Parameters / Request Quote</a><a class="tx-btn" data-catalog-cta href="{profile["route"]}?{esc(catalog)}">{profile["label"]}</a></div>'''


def enhance_english_catalog_experience(site_root: Path, stage: Path, oem: list[dict[str, Any]]) -> None:
    primary = english_primary_series(site_root, oem)
    series_routes = tuple(dict.fromkeys([*primary.values(), *(row["route"] for row in YUCHEN_CATEGORIES), COMMERCIAL_ROUTE]))
    labels = menu_labels(site_root, "en")
    ui = locale_pack(site_root, "en")["ui"]
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=("product_id", "product_route", "primary_series", "catalog_kind", "catalog_route", "interest", "identity_evidence", "classification_evidence"))
    writer.writeheader()
    # Retired SANYISHUI routes remain noindex aliases.  A prior rollout copied
    # full decision cards onto them; remove those so aliases cannot masquerade
    # as separately maintained products.
    for alias_path in (stage / "en").glob("*.html"):
        alias_text = alias_path.read_text(encoding="utf-8")
        if not re.search(r'<meta[^>]+name=["\']robots["\'][^>]+content=["\'][^"\']*noindex', alias_text, re.I):
            continue
        alias_text = re.sub(r'<aside class="tx-context-catalog".*?</aside>', '', alias_text, flags=re.S)
        alias_text = re.sub(r'<div class="tx-mobile-decision-actions".*?</div>', '', alias_text, flags=re.S)
        alias_path.write_text(alias_text, encoding="utf-8")
    for route, parent in sorted(primary.items()):
        profile = catalog_profile(parent)
        path = stage / "en" / route
        text = path.read_text(encoding="utf-8")
        interest = catalog_interest(text, parent)
        writer.writerow({"product_id": route.removesuffix(".html"), "product_route": route, "primary_series": parent, "catalog_kind": profile["kind"], "catalog_route": profile["route"], "interest": interest, "identity_evidence": "indexable self-canonical Product schema", "classification_evidence": "page facts plus reviewed primary series"})
        text = patch_products_menu(text, ui, labels, route)
        if '<nav aria-label="Breadcrumb" class="tx-breadcrumb breadcrumb">' in text:
            text = re.sub(r'<div class="rcu-breadcrumb">.*?</div>', '', text, count=1, flags=re.S)
        if 'assets/product-taxonomy.css' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="../assets/product-taxonomy.css?v=20260929-en-catalog">\n</head>', 1)
        text = re.sub(r'<aside class="tx-context-catalog".*?</aside>', '', text, flags=re.S)
        text = re.sub(r'<div class="tx-mobile-decision-actions".*?</div>', '', text, flags=re.S)
        card = context_catalog_card(route, parent, "product_detail_catalog", route.removesuffix(".html"), interest)
        mobile = mobile_decision_actions(route, parent, route.removesuffix(".html"), interest)
        text = re.sub(r'(<main\b[^>]*>)', r'\1' + mobile, text, count=1, flags=re.I)
        text = re.sub(r'(</section>)', r'\1' + card, text, count=1)
        if '<nav aria-label="Breadcrumb" class="tx-breadcrumb breadcrumb">' in text:
            text = re.sub(r'<div class="rcu-breadcrumb">.*?</div>', '', text, count=1, flags=re.S)
        path.write_text(text, encoding="utf-8")
    report_path = stage / REPORT_ROOT / "product-primary-series.csv"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(output.getvalue(), encoding="utf-8")
    for route in series_routes:
        path = stage / "en" / route
        if not path.is_file():
            raise ValueError(f"missing English primary series page: {route}")
        text = patch_products_menu(path.read_text(encoding="utf-8"), ui, labels, route)
        if 'assets/product-taxonomy.css' not in text:
            text = text.replace('</head>', '<link rel="stylesheet" href="../assets/product-taxonomy.css?v=20260929-en-catalog">\n</head>', 1)
        text = re.sub(r'<aside class="tx-context-catalog".*?</aside>', '', text, flags=re.S)
        top = context_catalog_card(route, route, "series_catalog_top")
        bottom = context_catalog_card(route, route, "series_catalog_bottom")
        text = re.sub(r'(</section>)', r'\1' + top, text, count=1)
        text = text.replace('</main>', bottom + '</main>', 1)
        path.write_text(text, encoding="utf-8")


def localized_oem_product(pack: dict[str, Any], product: dict[str, Any]) -> dict[str, str]:
    if product["source_file"] not in pack["products"]:
        raise ValueError(f'missing OEM translation: {product["source_file"]}')
    row = pack["products"][product["source_file"]]
    return {"title": row["name"], "description": public_oem_description(row.get("summary", ""))}


def public_oem_description(value: str) -> str:
    """Remove internal provenance wording and unsupported compatibility copy.

    The reviewed source data remains immutable; this is a presentation-only
    filter used by collection cards and previews.
    """
    sentences = re.split(r'(?<=[.!?])\s+', compact(value))
    blocked = re.compile(
        r'\b(?:Maikeluomei|Midea compatible|universal fit|universal replacement)\b',
        re.I,
    )
    value = " ".join(sentence for sentence in sentences if not blocked.search(sentence))
    replacements = (
        (r"\bThe source catalog also states that\b", "It is also described as"),
        (r"\bThe source catalog states that\b", "It is described as"),
        (r"\bThe source catalog describes\b", "Product information describes"),
        (r"\bThe source catalog claims that\b", "Reviewed product information describes that"),
        (r"\bThe source catalog specifies\b", "Product information specifies"),
        (r"\bsource-stated\b", "stated"),
    )
    for pattern, replacement in replacements:
        value = re.sub(pattern, replacement, value, flags=re.I)
    return compact(value)


def yuchen_routes(site_root: Path, stage: Path) -> list[dict[str, str]]:
    return [{"route": route, "category": route.removesuffix(".html").replace("-", " ")} for route in YUCHEN_DETAIL_ROUTES]


def category_key_for_label(label: str, route: str, industrial_routes: set[str]) -> str:
    parent = YUCHEN_PRIMARY_PARENT_BY_ROUTE[route]
    if parent == YUCHEN_HUB_ROUTE:
        return "direct"
    return next(row["key"] for row in YUCHEN_CATEGORIES if row["route"] == parent)


def category_title(site_root: Path, stage: Path, lang: str, key: str, terms: dict[str, str]) -> str:
    if lang == "en":
        return EN_CATEGORY_NAMES[key]
    if key == "softener":
        return terms["softener"]
    if key == "industrial":
        return terms["industrial"]
    definition = next(row for row in YUCHEN_CATEGORIES if row["key"] == key)
    info = page_info(source_or_stage(site_root, stage, Path(lang) / definition["route"]))
    if info.get("title"):
        return info["title"]
    if key in FALLBACK_CATEGORY_NAMES.get(lang, {}):
        return FALLBACK_CATEGORY_NAMES[lang][key]
    english = page_info(source_or_stage(site_root, stage, Path("en") / definition["route"]))
    return english.get("title", definition["route"].removesuffix(".html"))


def product_info(site_root: Path, stage: Path, lang: str, route: str, parent_title: str) -> dict[str, str]:
    info = page_info(source_or_stage(site_root, stage, Path(lang) / route))
    if info.get("title") and "#" not in info["title"]:
        return info
    facts = read_json(site_root / PRODUCT_FACTS).get("routes", {}).get(route, {})
    localized_name = facts.get("names", {}).get(lang)
    english = page_info(source_or_stage(site_root, stage, Path("en") / route))
    signature = technical_signature(english.get("title", route))
    info["title"] = localized_name or f'{parent_title}{f" · {signature}" if signature else ""}'
    info["description"] = ""
    info["image"] = english.get("image", "../assets/logo.png")
    return info


def collection_schema(lang: str, ui: dict[str, Any], route: str, title: str, description: str, entries: list[tuple[str, str]], crumbs: list[tuple[str, str | None]]) -> dict[str, Any]:
    canonical = f"{BASE_URL}{lang}/{route}"
    return {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "@id": canonical + "#webpage", "url": canonical, "name": title, "description": description, "inLanguage": ui.get("html_lang", lang), "mainEntity": {"@id": canonical + "#items"}},
        breadcrumb_schema(lang, ui, route, crumbs),
        {"@type": "ItemList", "@id": canonical + "#items", "numberOfItems": len(entries), "itemListElement": [{"@type": "ListItem", "position": i, "name": name, "url": f"{BASE_URL}{lang}/{target}"} for i, (name, target) in enumerate(entries, 1)]},
    ]}


def render_products(site_root: Path, stage: Path, codes: list[str], lang: str, template: str, categories: list[dict[str, str]], oem: list[dict[str, Any]], industrial_routes: set[str]) -> str:
    pack = locale_pack(site_root, lang); ui = pack["ui"]; terms = read_json(site_root / LOCALES_PATH)["locales"][lang]; labels=menu_labels(site_root,lang)
    page_copy = EN_PRODUCTS_PAGE_COPY if lang == "en" else {}
    description = compact(page_copy.get("description", ui["summary"]))
    yuchen_title = labels["yuchen"]
    commercial_info = page_info(source_or_stage(site_root, stage, Path(lang) / COMMERCIAL_ROUTE))
    commercial_title = "Commercial, Office & Vending RO Water Systems" if lang == "en" else commercial_info.get("title", f'RO · {ui["products"]}')
    gateways = [
        card(yuchen_title, YUCHEN_HUB_ROUTE, page_info(source_or_stage(site_root, stage, Path(lang) / "ro-water-purifier.html")) or page_info(source_or_stage(site_root, stage, Path("en/ro-water-purifier.html"))), page_copy.get("yuchen_gateway", ui["summary"]), cta=ui["view"]),
        card(labels["oem"], "sanyishui-products.html", page_info(source_or_stage(site_root, stage, Path(lang) / "sanyishui-products.html")), page_copy.get("oem_gateway", ui["summary"]), cta=ui["view"]),
        card(labels["commercial"], COMMERCIAL_ROUTE, commercial_info, commercial_info.get("description", description), cta=ui["view"]),
    ]
    category_cards = []
    for row in YUCHEN_CATEGORIES:
        title = category_title(site_root, stage, lang, row["key"], terms)
        info = page_info(source_or_stage(site_root, stage, Path(lang) / row["route"])) or page_info(source_or_stage(site_root, stage, Path("en") / row["route"]))
        info = {**info, "image": CATEGORY_IMAGES[row["key"]]}
        summary = page_copy.get(f'{row["key"]}_category', description) if row["key"] in {"softener", "industrial"} else info.get("description", description)
        category_cards.append(card(title, row["route"], info, summary))
    yuchen_by_route = {row["route"]: row["category"] for row in categories}
    oem_by_route = {p["route"]: p for p in oem}
    featured_cards = []
    for route in FEATURED_ROUTES:
        if route in oem_by_route:
            meta = localized_oem_product(pack, oem_by_route[route]); parent = pack["categories"][oem_by_route[route]["category_key"]]
            info = page_info(source_or_stage(site_root, stage, Path(lang) / route)); info.update({k: v for k, v in meta.items() if v})
        else:
            label = yuchen_by_route.get(route, "RO System")
            if route in COMMERCIAL_ROUTES:
                parent = commercial_title
            else:
                key = category_key_for_label(label, route, industrial_routes)
                parent = category_title(site_root, stage, lang, key, terms)
            info = product_info(site_root, stage, lang, route, parent)
        featured_cards.append(card(info["title"], route, info, info.get("description") or description, product=True))
    title = page_copy.get("title", f'{ui["products"]} · Yuchen Water · OEM/ODM · RO')
    heading = page_copy.get("heading", title)
    business_heading = page_copy.get("business_heading", ui["products"])
    business_intro = page_copy.get("business_intro", description)
    featured_heading = page_copy.get("featured_heading", ui["products"])
    featured_intro = page_copy.get("featured_intro", description)
    english_guide_actions = '' if lang != "en" else '<a class="tx-btn" href="water-filter-oem-buyer-guide.html">OEM Buyer Guide</a><a class="tx-btn" href="resources/">Membrane Knowledge Guides</a>'
    category_entries = [
        (yuchen_title, YUCHEN_HUB_ROUTE), (labels["oem"], "sanyishui-products.html"),
        (commercial_title, COMMERCIAL_ROUTE),
        *[(category_title(site_root, stage, lang, row["key"], terms), row["route"]) for row in YUCHEN_CATEGORIES],
    ]
    featured_entries = [(product_info(site_root, stage, lang, r, ui["products"])["title"] if r not in oem_by_route else localized_oem_product(pack,oem_by_route[r])["title"], r) for r in FEATURED_ROUTES]
    discovery_axes = ""
    if lang == "en":
        need_links = (
            ("Private Label / OEM", "sanyishui-products.html", "Start from an existing platform and define branding, packaging and project requirements."),
            ("ODM Development", "contact.html?project=odm-development&language=en&source_page=products&cta_location=need_axis", "Bring a target use case or configuration brief for an engineering review."),
            ("Filter Cartridge Projects", "quick-change-water-filter-cartridges.html", "Compare connection formats and filtration stages before selecting a cartridge."),
            ("Water Dispensers", "water-dispenser.html", "Browse drinking-water equipment before confirming market and electrical requirements."),
            ("Commercial / Industrial RO", "industrial-ro-seawater-desalination-systems.html", "Start with feed water, target capacity and operating conditions."),
            ("Softening / Pre-treatment", "automatic-water-filter-softener-systems.html", "Review softening and pretreatment systems before project sizing."),
        )
        type_links = (
            ("Water Dispenser", "water-dispenser.html"), ("Filter Cartridge", "quick-change-water-filter-cartridges.html"),
            ("RO / UF Membrane", "ro-membrane.html"), ("Purifier", "ro-water-purifier.html"),
            ("Commercial / Industrial System", "commercial-ro-water-systems.html"), ("Housing / Softener", "filter-housing.html"),
        )
        need_cards = "".join(f'<a class="tx-choice-card" href="{href}"><strong>{esc(label)}</strong><span>{esc(copy)}</span></a>' for label, href, copy in need_links)
        type_cards = "".join(f'<a class="tx-type-link" href="{href}">{esc(label)}</a>' for label, href in type_links)
        discovery_axes = f'''<section class="tx-section tx-discovery" aria-labelledby="find-products-heading"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">Two ways to find the right product</span><h2 id="find-products-heading">Start with your sourcing need or a known product type</h2><p>Use the path that matches what you already know. Both routes lead to the same stable product pages.</p></div><div class="tx-discovery-grid"><section data-discovery-axis="need" aria-labelledby="need-axis-heading"><h3 id="need-axis-heading">Shop by sourcing need</h3><div class="tx-choice-grid">{need_cards}</div></section><section data-discovery-axis="type" aria-labelledby="type-axis-heading"><h3 id="type-axis-heading">Browse by product type</h3><div class="tx-type-grid">{type_cards}</div><p class="tx-note">Search and filters narrow the list; they do not create duplicate products.</p></section></div></div></section>'''
    detailed_directory = ""
    if lang == "en":
        primary_counts = {parent: sum(1 for value in YUCHEN_PRIMARY_PARENT_BY_ROUTE.values() if value == parent) for parent in set(YUCHEN_PRIMARY_PARENT_BY_ROUTE.values())}
        filter_catalog = "filter-cartridge-catalog.html?language=en&source_page=products&cta_location=directory_catalog"
        oem_catalog = "sanyishui-catalog.html?language=en&source_page=products&cta_location=directory_catalog"
        commercial_catalog = "commercial-ro-water-systems-catalog.html?language=en&source_page=products&cta_location=directory_catalog"
        standard_rows = [
            discovery_series_row("PP Melt-Blown Cartridges", "pp-melt-blown-filter-cartridge.html", CATEGORY_IMAGES["pp"], f'{primary_counts.get("pp-melt-blown-filter-cartridge.html", 0)} SKUs', "Sediment and particulate prefiltration.", "length, micron rating, weight and end format.", filter_catalog),
            discovery_series_row("CTO Carbon Block Filters", "cto-carbon-block-filter.html", CATEGORY_IMAGES["cto"], f'{primary_counts.get("cto-carbon-block-filter.html", 0)} SKUs', "Compressed or sintered activated-carbon filtration.", "carbon source, iodine value, micron rating and dimensions.", filter_catalog),
            discovery_series_row("GAC / UDF Cartridges", "gac-udf-filter-cartridge.html", CATEGORY_IMAGES["gac"], f'{primary_counts.get("gac-udf-filter-cartridge.html", 0)} SKUs', "Granular activated-carbon stages.", "media source, treatment, weight and housing fit.", filter_catalog),
            discovery_series_row("T33 Inline Filters", "t33-inline-filter.html", CATEGORY_IMAGES["t33"], f'{primary_counts.get("t33-inline-filter.html", 0)} SKUs', "Post-carbon and inline polishing stages.", "connector, dimensions, media and project flow.", filter_catalog),
        ]
        quick_rows = []
        for family in OEM_FAMILIES:
            if family["key"] == "pipeline":
                continue
            representative = next(p for p in oem if p["category_key"] == family["key"])
            info = page_info(source_or_stage(site_root, stage, Path("en") / representative["route"]))
            quick_rows.append(discovery_series_row(pack["categories"][family["key"]], family["route"], info.get("image", CATEGORY_IMAGES["pp"]), f'{family["count"]} SKUs', "Quick-change cartridge family organized by connection format.", "matching head, connection geometry, dimensions and stage sequence.", filter_catalog))
        membrane_rows = [
            discovery_series_row("RO Membranes", "ro-membrane.html", CATEGORY_IMAGES["ro_membrane"], f'{primary_counts.get("ro-membrane.html", 0)} SKUs', "Reverse-osmosis membrane elements.", "model, capacity, housing and pump compatibility.", filter_catalog),
            discovery_series_row("UF Membrane Filters", "uf-membrane-filter.html", CATEGORY_IMAGES["uf"], f'{primary_counts.get("uf-membrane-filter.html", 0)} SKUs', "Hollow-fiber ultrafiltration stages.", "housing, connector, flow and operating conditions.", filter_catalog),
        ]
        filter_rows = [*standard_rows, *quick_rows, *membrane_rows]
        dispenser_rows = [
            discovery_series_row("Instant Heating Dispensers", "instant-heating-water-dispensers.html", CATEGORY_IMAGES["dispenser"], "23 SKUs", "Instant-heating countertop and dispenser platforms.", "voltage, plug, control panel, temperature and branding.", oem_catalog),
            discovery_series_row("Office / Institutional Dispensers", "commercial-ro-water-systems.html#office", CATEGORY_IMAGES["dispenser"], f'{len(COMMERCIAL_GROUPS[0][1])} SKUs', "Office, school and institutional drinking-water equipment.", "daily users, outlets, storage and filtration train.", oem_catalog),
            discovery_series_row("Commercial Water Systems", "commercial-ro-water-systems.html#high_flow", CATEGORY_IMAGES["dispenser"], f'{len(COMMERCIAL_GROUPS[1][1])} SKUs', "Higher-flow commercial purification systems.", "feed water, target flow, tanks and installation space.", commercial_catalog),
            discovery_series_row("Vending / Payment Systems", "commercial-ro-water-systems.html#vending", CATEGORY_IMAGES["dispenser"], f'{len(COMMERCIAL_GROUPS[2][1])} SKUs', "Commercial dispensing platforms with optional payment integration.", "payment hardware, region, telemetry and service model.", commercial_catalog),
        ]
        purifier_rows = [
            discovery_series_row("Household / Under-Sink RO", "ro-water-purifier.html", CATEGORY_IMAGES["purifier"], "Available models", "Household and under-sink drinking-water purification.", "capacity, installation, tank, stages and source water.", oem_catalog),
            discovery_series_row("Cabinet RO Purifiers", "ro-water-purifier.html", CATEGORY_IMAGES["purifier"], "Available models", "Cabinet and integrated RO configurations.", "stage count, optional UV, voltage and cabinet configuration.", oem_catalog),
            discovery_series_row("Commercial High-Flow Purifiers", "commercial-ro-water-systems.html#high_flow", CATEGORY_IMAGES["purifier"], f'{len(COMMERCIAL_GROUPS[1][1])} SKUs', "Commercial high-flow RO purifier platforms.", "feed analysis, output, storage and electrical requirements.", commercial_catalog),
        ]
        system_rows = [
            discovery_series_row("Commercial RO Systems", COMMERCIAL_ROUTE, CATEGORY_IMAGES["purifier"], f'{len(COMMERCIAL_ROUTES)} SKUs', "Commercial drinking-water and dispensing systems.", "site demand, feed water, output and storage.", commercial_catalog),
            discovery_series_row("Industrial RO Systems", INDUSTRIAL_ROUTE, CATEGORY_IMAGES["industrial"], "14 systems", "Industrial reverse-osmosis project systems.", "water analysis, capacity, recovery target and pretreatment.", commercial_catalog),
            discovery_series_row("Seawater Desalination", f"{INDUSTRIAL_ROUTE}#seawater", CATEGORY_IMAGES["industrial"], "3 systems", "Project-specific seawater desalination systems.", "feed salinity, product-water target, capacity and site utilities.", commercial_catalog),
        ]
        housing_rows = [
            discovery_series_row("Filter Housings", "filter-housing.html", CATEGORY_IMAGES["housing"], f'{primary_counts.get("filter-housing.html", 0)} SKUs', "PP, Big Blue and stainless-steel filter housings.", "material, ports, pressure, bracket and cartridge fit.", oem_catalog),
            discovery_series_row("Water Softener Systems", SOFTENER_ROUTE, CATEGORY_IMAGES["softener"], "15 models", "Automatic ion-exchange softening systems.", "hardness, flow, resin, valve and regeneration settings.", oem_catalog),
            discovery_series_row("Automatic Water Filters", f"{SOFTENER_ROUTE}#automatic-water-filters", CATEGORY_IMAGES["softener"], "6 models", "Automatic pretreatment and media filtration.", "media, source water, flow and backwash conditions.", oem_catalog),
        ]
        groups = "".join((
            discovery_group("filter-cartridges", "Filter Cartridges & Membranes", filter_rows, True),
            discovery_group("water-dispensers", "Water Dispensers", dispenser_rows),
            discovery_group("ro-purifiers", "RO Water Purifiers", purifier_rows),
            discovery_group("commercial-industrial", "Commercial / Industrial Systems", system_rows),
            discovery_group("housings-pretreatment", "Housings & Pre-treatment", housing_rows),
        ))
        directory_script = '''<script data-product-directory-script>(function(){const root=document.querySelector('[data-product-directory]'),q=document.querySelector('#product-search'),compare=document.querySelector('[data-compare-selected]'),status=document.querySelector('[data-compare-status]');if(!root)return;const openHash=()=>{const t=document.querySelector(location.hash);if(t?.matches('details[data-catalog-group]'))t.open=true};openHash();addEventListener('hashchange',openHash);q?.addEventListener('input',()=>{const value=q.value.trim().toLowerCase();root.querySelectorAll('[data-series-row]').forEach(row=>row.hidden=value&&!row.textContent.toLowerCase().includes(value));root.querySelectorAll('details[data-catalog-group]').forEach(group=>{const matches=[...group.querySelectorAll('[data-series-row]')].some(row=>!row.hidden);group.hidden=!matches;if(value&&matches)group.open=true})});root.addEventListener('change',e=>{if(!e.target.matches('[data-series-select]'))return;const selected=[...root.querySelectorAll('[data-series-select]:checked')];if(selected.length>4){e.target.checked=false;status.textContent='Select up to four series.'}else status.textContent=selected.length?selected.length+' series selected.':'Select 2–4 series to compare.'});compare?.addEventListener('click',()=>{const selected=[...root.querySelectorAll('[data-series-select]:checked')];if(selected.length<2){status.textContent='Select at least two series to compare.';return}location.href=selected[0].value+'?compare='+encodeURIComponent(selected.map(x=>x.value).join(','))})})();</script>'''
        action_bar = '''<div class="tx-directory-actions" data-directory-actions><a class="tx-btn" href="#product-search">Search Products</a><button class="tx-btn" type="button" data-compare-selected>Compare Selected Series</button><a class="tx-btn" href="filter-cartridge-catalog.html?language=en&amp;source_page=products&amp;category=directory&amp;cta_location=directory_action">Download Relevant Catalog</a><a class="tx-btn tx-btn--solid" href="contact.html?language=en&amp;source_page=products&amp;category=directory&amp;cta_location=directory_action">Submit Project Parameters</a><span data-compare-status aria-live="polite">Select 2–4 series to compare.</span></div>'''
        detailed_directory = f'''<section class="tx-section tx-directory-section" aria-labelledby="directory-heading"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">Detailed product directory</span><h2 id="directory-heading">Browse series, then compare SKUs</h2><p>One stable product identity can appear through a sourcing need or product-type entrance; the directory does not create duplicate product pages.</p>{action_bar}</div><div class="tx-capability-grid"><article id="oem-capability" data-oem-capability data-filter-target="all-series"><h3>Private Label / OEM</h3><p>Start from an existing product platform, then confirm branding, packaging and project requirements.</p><a href="#catalog-filter-cartridges">Browse compatible series</a></article><article id="odm-capability"><h3>ODM Development</h3><p>Bring the target use case and configuration brief for engineering review; unconfirmed commercial or performance claims are not assumed.</p><a href="contact.html?project=odm-development&amp;language=en&amp;source_page=products&amp;cta_location=directory_capability">Submit a project brief</a></article></div><label class="tx-directory-search" for="product-search"><span>Search this directory</span><input id="product-search" type="search" placeholder="Search series, media, connection or application" autocomplete="off"></label><div class="tx-product-directory" data-product-directory="true">{groups}</div>{directory_script}</div></section>'''
    canonical = f"{BASE_URL}{lang}/products.html"
    schema = {"@context":"https://schema.org","@graph":[
        {"@type":"CollectionPage","@id":canonical+"#webpage","url":canonical,"name":heading,"description":description,"inLanguage":ui.get("html_lang",lang),"mainEntity":[{"@id":canonical+"#categories"},{"@id":canonical+"#featured"}]},
        breadcrumb_schema(lang,ui,"products.html",[(ui["products"],None)]),
        {"@type":"ItemList","@id":canonical+"#categories","numberOfItems":len(category_entries),"itemListElement":[{"@type":"ListItem","position":i,"name":name,"url":f"{BASE_URL}{lang}/{route}"} for i,(name,route) in enumerate(category_entries,1)]},
        {"@type":"ItemList","@id":canonical+"#featured","numberOfItems":12,"itemListElement":[{"@type":"ListItem","position":i,"name":name,"url":f"{BASE_URL}{lang}/{route}"} for i,(name,route) in enumerate(featured_entries,1)]},
    ]}
    main = f'''<main><span id="all-products" class="tx-anchor"></span><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,[(ui["products"],None)])}<span class="tx-eyebrow">Yuchen Water · OEM/ODM · RO</span><h1>{esc(heading)}</h1><p class="tx-lede">{esc(description)}</p><div class="tx-actions"><a class="tx-btn tx-btn--solid" href="#directory-heading">Browse detailed directory</a><a class="tx-btn" href="contact.html">{esc(ui["contact"])}</a></div></div></section>{discovery_axes}{detailed_directory}
<section class="tx-section" id="business-paths"><div class="tx-container"><div class="tx-section-head"><h2>{esc(business_heading)}</h2><p>{esc(business_intro)}</p></div><div class="tx-gateway-grid">{"".join(gateways)}</div></div></section>
<span id="yuchen-product-categories" class="tx-anchor"></span><section class="tx-section tx-section--tint"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">Yuchen Water</span><h2>{esc(yuchen_title)}</h2></div><div class="tx-category-grid">{"".join(category_cards)}</div></div></section>
<section class="tx-section"><div class="tx-container"><div class="tx-section-head"><h2>{esc(featured_heading)}</h2><p>{esc(featured_intro)}</p></div><div class="tx-product-grid" data-featured-count="12">{"".join(featured_cards)}</div></div></section>
<section class="tx-section tx-section--deep"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">OEM/ODM</span><h2>{esc(ui["technical_guides"])}</h2></div><div class="tx-actions"><a class="tx-btn tx-btn--gold" href="filter-cartridge-catalog.html">{esc(ui["technical_guides"])}</a><a class="tx-btn" href="sanyishui-catalog.html">{esc(ui["catalog_entry"])}</a>{english_guide_actions}<a class="tx-btn" href="contact.html">{esc(ui["contact"])}</a></div></div></section></main>'''
    rendered = render_shell(site_root,codes,lang,template,"products.html",title,description,main,schema,"assets/products/built-in-pressure-tank-ro-water-purifier-100g-200g-oem.webp")
    if lang == "en":
        rendered = re.sub(r'<section class="tx-section" id="business-paths">.*?</section>', '', rendered, count=1, flags=re.S)
        rendered = re.sub(r'<span id="yuchen-product-categories".*?</span><section.*?</section>', '', rendered, count=1, flags=re.S)
        rendered = re.sub(r'<section class="tx-section"><div class="tx-container"><div class="tx-section-head"><h2>Products to Review</h2>.*?</section>', '', rendered, count=1, flags=re.S)
    return preserve_existing_block(template, rendered, RO_CABINET_DETAIL_START, RO_CABINET_DETAIL_END, "</main>")


def render_yuchen_hub(site_root: Path, stage: Path, codes: list[str], lang: str, template: str, terms: dict[str, str]) -> str:
    pack=locale_pack(site_root,lang); ui=pack["ui"]; title=f'Yuchen Water · {ui["products"]}'; description=ui["summary"]
    groups=[]; entries=[]
    for group in ("systems","components","devices"):
        rows=[r for r in YUCHEN_CATEGORIES if r["group"]==group]
        cards=[]
        for row in rows:
            name=category_title(site_root,stage,lang,row["key"],terms); info=page_info(source_or_stage(site_root,stage,Path(lang)/row["route"])) or page_info(source_or_stage(site_root,stage,Path("en")/row["route"])); info={**info,"image":CATEGORY_IMAGES[row["key"]]}
            badge=""
            summary = description if row["key"] in {"softener", "industrial"} else info.get("description") or description
            cards.append(card(name,row["route"],info,summary,badge)); entries.append((name,row["route"]))
        group_title=category_title(site_root,stage,lang,rows[0]["key"],terms)
        groups.append(f'<section class="tx-section {"tx-section--tint" if group=="components" else ""}"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">{esc(group.upper())}</span><h2>{esc(group_title)}</h2></div><div class="tx-category-grid">{"".join(cards)}</div></div></section>')
    siliphos=product_info(site_root,stage,lang,SILIPHOS_ROUTE,title)
    direct_card=card(siliphos["title"],SILIPHOS_ROUTE,siliphos,siliphos.get("description") or description,product=True)
    entries.append((siliphos["title"],SILIPHOS_ROUTE))
    schema=collection_schema(lang,ui,YUCHEN_HUB_ROUTE,title,description,entries,[(title,None)])
    direct=f'<section class="tx-section tx-section--tint" id="direct-yuchen-products"><div class="tx-container"><div class="tx-section-head"><h2>Yuchen Water · {esc(ui["products"])}</h2></div><div class="tx-product-grid" data-direct-yuchen-products="1">{direct_card}</div></div></section>'
    main=f'<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,[(title,None)])}<span class="tx-eyebrow">Yuchen Water</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div></section>{"".join(groups)}{direct}</main>'
    return render_shell(site_root,codes,lang,template,YUCHEN_HUB_ROUTE,title,description,main,schema,"assets/products/smart-ro-water-purifier-400g-1200g-oem.webp")


def render_oem_hub(site_root: Path, stage: Path, codes: list[str], lang: str, template: str, oem: list[dict[str, Any]]) -> str:
    pack=locale_pack(site_root,lang); ui=pack["ui"]; title=ui["collection"]; description=ui["summary"]; family_cards=[]; featured=[]; entries=[]
    for family in OEM_FAMILIES:
        subset=[p for p in oem if p["category_key"]==family["key"]]; representative=subset[0]
        name=pack["categories"][family["key"]]; info=page_info(source_or_stage(site_root,stage,Path(lang)/representative["route"])); meta=localized_oem_product(pack,representative); info.update(meta)
        family_cards.append(card(name,family["route"],info,description))
        featured.append(card(meta["title"],representative["route"],info,description,product=True)); entries.append((name,family["route"]))
    schema=collection_schema(lang,ui,"sanyishui-products.html",title,description,entries,[(title,None)])
    main=f'''<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,[(title,None)])}<span class="tx-eyebrow">OEM/ODM</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div></section><section class="tx-section"><div class="tx-container"><div class="tx-section-head"><h2>{esc(title)}</h2></div><div class="tx-category-grid" data-oem-family-count="9">{"".join(family_cards)}</div></div></section><section class="tx-section tx-section--tint"><div class="tx-container"><div class="tx-section-head"><h2>{esc(ui["view"])}</h2></div><div class="tx-product-grid" data-oem-featured-count="9">{"".join(featured)}</div></div></section><section class="tx-section tx-section--deep"><div class="tx-container"><h2>{esc(ui["technical_guides"])}</h2><div class="tx-actions"><a class="tx-btn tx-btn--gold" href="sanyishui-catalog.html">{esc(ui["catalog_entry"])}</a><a class="tx-btn" href="filter-cartridge-catalog.html">{esc(ui["technical_guides"])}</a></div></div></section></main>'''
    return render_shell(site_root,codes,lang,template,"sanyishui-products.html",title,description,main,schema,"assets/catalog/yuchen-water-oem-catalog-cover-960.webp")


def render_oem_family(site_root: Path, stage: Path, codes: list[str], lang: str, template: str, family: dict[str, Any], products: list[dict[str, Any]]) -> str:
    pack=locale_pack(site_root,lang); ui=pack["ui"]; title=pack["categories"][family["key"]]; description=pack.get("category_descriptions",{}).get(family["key"],ui["summary"]); subset=[p for p in products if p["category_key"]==family["key"]]
    cards=[]; entries=[]; comparison_rows=[]
    for p in subset:
        meta=localized_oem_product(pack,p); source_path=source_or_stage(site_root,stage,Path(lang)/p["route"]); info=page_info(source_path); info.update(meta)
        tags=" · ".join(re.findall(r"\b(?:PPF|PP|UDF|CTO|GAC|T33|PCP|PCO|RO|UF|FOF|\d+(?:\.\d+)?\s*(?:W|V|Hz|°C))\b",meta["title"],re.I)[:4])
        cards.append(card(meta["title"],p["route"],info,meta["description"],tags,product=True)); entries.append((meta["title"],p["route"]))
        if lang == "en" and family["key"] == "bayonet":
            source_text = source_path.read_text(encoding="utf-8")
            product_id_match = re.search(r"[?&](?:amp;)?product_id=([^&\"]+)", source_text)
            product_id = product_id_match.group(1) if product_id_match else p["route"].removesuffix(".html")
            canonical_match = re.search(r'<link\s+rel="canonical"\s+href="[^"]+/([^/"?#]+\.html)"', source_text, re.I)
            public_route = canonical_match.group(1) if canonical_match else p["route"]
            fact_pairs = dict((re.sub(r"<[^>]+>", "", key).strip(), re.sub(r"<[^>]+>", "", value).strip()) for key, value in re.findall(r"<tr><th>(.*?)</th><td>(.*?)</td></tr>", source_text, re.S))
            stage_match = re.search(r"\b(PP|UDF|CTO|RO|T33)\b", meta["title"], re.I)
            stage_label = stage_match.group(1).upper() if stage_match else "Confirm for quotation"
            semantic_routes = dict(zip(("PP", "UDF", "CTO", "RO", "T33"), EN_QUICK_CHANGE_DETAIL_ROUTES))
            public_route = semantic_routes.get(stage_label, public_route)
            medium = fact_pairs.get("Filter media", stage_label)
            connection = fact_pairs.get("Format", "Bayonet-lock connection")
            comparison_rows.append(f'<tr data-product-id="{esc(product_id)}"><th scope="row">{esc(stage_label)}</th><td>{esc(medium)}</td><td>{esc(connection)}</td><td>{esc(meta["description"])}</td><td>Connection geometry, dimensions and matching filter head.</td><td><a href="{esc(public_route)}">View product</a></td></tr>')
    if len(subset)!=family["count"]: raise ValueError(f'family count drift: {family["key"]}')
    crumbs=[(ui["collection"],"sanyishui-products.html"),(title,None)]; schema=collection_schema(lang,ui,family["route"],title,description,entries,crumbs)
    nav="".join(f'<a class="tx-btn" href="{f["route"]}">{esc(pack["categories"][f["key"]])}</a>' for f in OEM_FAMILIES)
    count_label=f'{family["count"]} {ui["products"]}'
    comparison = ""
    if comparison_rows:
        comparison = f'''<section class="tx-section tx-section--tint" id="compare-quick-change"><div class="tx-container"><div class="tx-section-head"><span class="tx-eyebrow">Five stages, one connection family</span><h2>Compare the five Quick-Change cartridge stages</h2><p>Best for OEM programs that have already selected a bayonet-lock platform. Not for projects where the connection geometry or matching head is still unknown.</p></div><div class="tx-table-wrap"><table class="tx-comparison" data-quick-change-comparison="true"><thead><tr><th>Stage</th><th>Media / function</th><th>Connection</th><th>Known facts</th><th>Confirm for quotation</th><th>Product</th></tr></thead><tbody>{"".join(comparison_rows)}</tbody></table></div><p class="tx-note" data-no-match-path>Not sure which stage or connection fits? <a href="contact.html?series=bayonet-lock-quick-change&amp;language=en&amp;source_page=quick-change-water-filter-cartridges&amp;cta_location=no_match_path">Submit project parameters for review</a>.</p></div></section>'''
    main=f'''<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">OEM/ODM · {esc(count_label)}</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p><div class="tx-actions"><a class="tx-btn tx-btn--solid" href="#compare-quick-change">Compare the five stages</a><a class="tx-btn" href="contact.html">{esc(ui["contact"])}</a></div></div></section><section class="tx-section tx-section--tint"><div class="tx-container"><nav class="tx-family-nav" aria-label="OEM families">{nav}</nav></div></section>{comparison}<section class="tx-section" id="family-products"><div class="tx-container"><div class="tx-section-head"><h2>{esc(title)} · {esc(count_label)}</h2></div><div class="tx-product-grid" data-family="{family["key"]}" data-family-count="{family["count"]}">{"".join(cards)}</div></div></section></main>'''
    image=page_info(source_or_stage(site_root,stage,Path(lang)/subset[0]["route"])).get("image","../assets/logo.png")
    rendered = render_shell(site_root,codes,lang,template,family["route"],title,description,main,schema,image)
    if lang == "en" and family["key"] == "bayonet":
        # The pilot changes body information architecture only. Preserve the
        # reviewed canonical/hreflang set byte-for-byte from the source page.
        source_text = (site_root / lang / family["route"]).read_text(encoding="utf-8")
        links = re.findall(r'<link\s+rel="(?:canonical|alternate)"[^>]*>', source_text, re.I)
        rendered = re.sub(r'<link\s+rel="(?:canonical|alternate)"[^>]*>\s*', "", rendered, flags=re.I)
        marker = '<link rel="stylesheet"'
        rendered = rendered.replace(marker, "\n".join(links) + "\n" + marker, 1)
    return rendered


def public_softener_facts(site_root: Path) -> dict[str, Any]:
    facts=deepcopy(read_json(site_root/SOFTENER_FACTS)); policy=facts.get("public_identity_policy",{})
    if policy.get("status")!="owner_authorized": raise ValueError("softener identity mapping is not owner-authorized")
    for family in facts["families"]:
        family["id"]=family["id"].replace("jh-","yc-",1); family["name"]=family["name"].replace("JH-","YC-",1); family["route"]=family["public_route"]
        for model in family["models"]: model["model"]=model["model"].replace("JH-","YC-",1); model["slug"]=model["slug"].replace("jh-","yc-",1)
    soft=[f for f in facts["families"] if f["product_type"]=="Automatic Water Softener"]; filters=[f for f in facts["families"] if f["product_type"]=="Automatic Water Filter"]
    if len(soft)!=5 or sum(len(f["models"]) for f in soft)!=15 or len(filters)!=2 or sum(len(f["models"]) for f in filters)!=6: raise ValueError("softener facts drift")
    return {"softeners":soft,"filters":filters,"families":facts["families"]}


def softener_picture(model: dict[str,Any], title: str) -> str:
    slug=model["slug"]
    return f'<div class="tx-card-media"><picture><source type="image/webp" srcset="../assets/products/water-softeners/{slug}-360.webp 360w, ../assets/products/water-softeners/{slug}-640.webp 640w, ../assets/products/water-softeners/{slug}-1024.webp 1024w"><img src="../assets/products/water-softeners/{slug}-1024.webp" alt="{esc(title)}" loading="lazy" decoding="async"></picture></div>'


def render_softener_hub(site_root:Path,codes:list[str],lang:str,template:str,terms:dict[str,str],facts:dict[str,Any])->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];title=terms["softener"];description=ui["summary"];cards=[];related=[];entries=[]
    for f in facts["softeners"]:
        model=f["models"][1]
        name=f'{f["id"].upper()} · {title}'
        family_route=Path(f["route"]).name
        model_tags="".join(f'<span class="tx-tag">{esc(m["model"])}</span>' for m in f["models"])
        cards.append(f'<article class="tx-card">{softener_picture(model,name)}<div class="tx-card-copy"><span class="tx-count">3 models</span><h3><a href="{family_route}">{esc(name)}</a></h3><div class="tx-tags">{model_tags}</div></div></article>')
        entries.extend((m["model"],f'{family_route}#{m["slug"]}') for m in f["models"])
    for f in facts["filters"]:
        model=f["models"][1];name=f'{f["id"].upper()} · {terms["filter"]}';related.append(f'<article class="tx-card">{softener_picture(model,name)}<div class="tx-card-copy"><span class="tx-count">3 models</span><h3><a href="{Path(f["route"]).name}">{esc(name)}</a></h3></div></article>')
    crumbs=[(f'Yuchen Water · {ui["products"]}',YUCHEN_HUB_ROUTE),(title,None)];schema=collection_schema(lang,ui,SOFTENER_ROUTE,title,description,entries,crumbs)
    main=f'''<main><section class="tx-hero"><div class="tx-container tx-hero-grid"><div>{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">15 models · 5 series</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div><div class="tx-stats"><div class="tx-stat"><strong>15</strong><span>models</span></div><div class="tx-stat"><strong>5</strong><span>series</span></div><div class="tx-stat"><strong>6</strong><span>{esc(terms["filter"])}</span></div></div></div></section><section class="tx-section"><div class="tx-container"><div class="tx-section-head"><h2>{esc(title)} · 15 models / 5 series</h2></div><div class="tx-category-grid" data-softener-families="5">{"".join(cards)}</div></div></section><section class="tx-section tx-section--tint" id="automatic-water-filters"><div class="tx-container"><div class="tx-section-head"><h2>{esc(terms["filter"])} · 6 models / 2 series</h2><p>{esc(description)}</p></div><div class="tx-category-grid" data-related-filter-families="2">{"".join(related)}</div></div></section></main>'''
    return render_shell(site_root,codes,lang,template,SOFTENER_ROUTE,title,description,main,schema,"assets/products/water-softeners/yc-r2000-1024.webp")


def render_softener_family(site_root:Path,codes:list[str],lang:str,template:str,terms:dict[str,str],family:dict[str,Any])->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];kind=terms["softener"] if family["product_type"]=="Automatic Water Softener" else terms["filter"];title=f'{family["id"].upper()} · {kind}';route=Path(family["route"]).name;cards=[];variants=[]
    for model in family["models"]:
        specs={**family["common_specs"],**model["specs"]};spec_html="".join(f'<div><dt>{esc(k)}</dt><dd>{esc(v)}</dd></div>' for k,v in specs.items());name=f'{model["model"]} · {kind}'
        cards.append(f'<article class="tx-card tx-product-card" id="{esc(model["slug"])}">{softener_picture(model,name)}<div class="tx-card-copy"><h3>{esc(model["model"])}</h3><dl class="tx-specs">{spec_html}</dl><a class="tx-btn" href="contact.html?model={esc(model["model"])}">{esc(ui["contact"])}</a></div></article>');variants.append({"@type":"Product","name":name,"model":model["model"],"sku":model["model"],"url":f'{BASE_URL}{lang}/{route}#{model["slug"]}',"image":f'{BASE_URL}assets/products/water-softeners/{model["slug"]}-1024.webp'})
    parent_route=SOFTENER_ROUTE if family["product_type"]=="Automatic Water Softener" else SOFTENER_ROUTE+"#automatic-water-filters";crumbs=[(f'Yuchen Water · {ui["products"]}',YUCHEN_HUB_ROUTE),(kind,parent_route),(title,None)];canonical=f'{BASE_URL}{lang}/{route}';schema={"@context":"https://schema.org","@graph":[{"@type":"WebPage","url":canonical,"name":title,"description":ui["summary"],"inLanguage":ui.get("html_lang",lang)},breadcrumb_schema(lang,ui,route,crumbs),{"@type":"ProductGroup","name":title,"productGroupID":family["id"].upper(),"hasVariant":variants}]}
    main=f'<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">3 models</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(ui["summary"])}</p></div></section><section class="tx-section"><div class="tx-container"><h2 class="tx-model-heading">{esc(title)} · 3 models</h2><div class="tx-product-grid" data-model-variants="3">{"".join(cards)}</div></div></section></main>'
    return render_shell(site_root,codes,lang,template,route,title,ui["summary"],main,schema,f'assets/products/water-softeners/{family["models"][1]["slug"]}-1024.webp')


def industrial_facts(site_root:Path)->list[dict[str,Any]]:
    products=[p for p in read_json(site_root/INDUSTRIAL_FACTS)["products"] if p["category_id"]=="industrial_seawater"]
    source=read_json(site_root/SEAWATER_2000_FACTS)
    products.append({
        "product_id": source["product_id"],
        "product_name": source["english_name"],
        "category_id": "industrial_seawater",
        "category": source["category"],
        "source_page": f'en/{source["route"]}',
        "source_url": f'{BASE_URL}en/{source["route"]}',
        "include_status": "recommended",
        "review_status": source["review_status"],
        "hero_image": "assets/products/2000lph-seawater-desalination/2000lph-seawater-ro-control-1024.webp",
        "supporting_images": ["assets/products/2000lph-seawater-desalination/2000lph-seawater-ro-pretreatment-1024.webp"],
        "capacity": source["capacity"],
        "short_description": source["short_description"],
        "key_features": [group["component"] for group in source["configuration_groups"][:4]],
        "specifications": {group["component"]: "; ".join(group["facts"]) for group in source["configuration_groups"]},
        "applications": "Project-specific seawater desalination; confirm feed-water analysis and product-water requirements.",
        "extraction_notes": "User-supplied photographed-unit configuration; prohibited performance and commercial assertions are suppressed."
    })
    if len(products)!=17 or len([p for p in products if "seawater" in p["product_id"]])!=3: raise ValueError("industrial facts drift")
    return products


def render_industrial(site_root:Path,stage:Path,codes:list[str],lang:str,template:str,terms:dict[str,str],products:list[dict[str,Any]])->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];title=terms["industrial"];description=ui["summary"];groups=[];entries=[]
    for is_sea,count in ((False,14),(True,3)):
        subset=[p for p in products if ("seawater" in p["product_id"])==is_sea];cards=[]
        for p in subset:
            route=Path(p["source_page"]).name;info=product_info(site_root,stage,lang,route,title)
            if lang=="en": info["title"]=p["product_name"];info["description"]=p["short_description"]
            info["image"]="../"+p["hero_image"];cards.append(card(info["title"],route,info,info.get("description") or description,p["capacity"],product=True));entries.append((info["title"],route))
        heading=terms["seawater"] if is_sea else f'RO · {title}';groups.append(f'<section class="tx-section {"tx-section--tint" if is_sea else ""}" id="{"seawater" if is_sea else "industrial-ro"}" data-industrial-group="{count}"><div class="tx-container"><div class="tx-section-head"><h2>{esc(heading)} · {count} {esc(ui["products"])}</h2></div><div class="tx-product-grid">{"".join(cards)}</div></div></section>')
    crumbs=[(f'Yuchen Water · {ui["products"]}',YUCHEN_HUB_ROUTE),(title,None)];schema=collection_schema(lang,ui,INDUSTRIAL_ROUTE,title,description,entries,crumbs)
    main=f'<main><section class="tx-hero"><div class="tx-container tx-hero-grid"><div>{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">14 Industrial RO · 3 {esc(terms["seawater"])}</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div><div class="tx-stats"><div class="tx-stat"><strong>14</strong><span>Industrial RO</span></div><div class="tx-stat"><strong>3</strong><span>{esc(terms["seawater"])}</span></div><div class="tx-stat"><strong>17</strong><span>{esc(ui["products"])}</span></div></div></div></section>{"".join(groups)}</main>'
    return render_shell(site_root,codes,lang,template,INDUSTRIAL_ROUTE,title,description,main,schema,products[2]["hero_image"])


def render_commercial(site_root:Path,stage:Path,codes:list[str],lang:str,template:str)->str:
    pack=locale_pack(site_root,lang);ui=pack["ui"];existing=page_info(source_or_stage(site_root,stage,Path(lang)/COMMERCIAL_ROUTE));title="Commercial, Office & Vending RO Water Systems" if lang=="en" else existing.get("title",f'RO · {ui["products"]}');description=existing.get("description") or ui["summary"];sections=[];entries=[]
    for index,(key,routes) in enumerate(COMMERCIAL_GROUPS,1):
        cards=[]
        for route in routes:
            info=product_info(site_root,stage,lang,route,title)
            if lang == "en" and route in {"commercial-ro-water-dispenser-e300.html", "commercial-ro-water-dispenser-e900-step-heating.html"}:
                info["image"] = info.get("image", "").replace("-640.webp", "-1024.webp")
            cards.append(card(info["title"],route,info,info.get("description") or description,technical_signature(info["title"]),product=True));entries.append((info["title"],route))
        heading={"office":"Office & Institutional Water Dispensers","high_flow":"High-Flow Commercial RO Purifiers","vending":"Smart Payment & Vending Systems"}[key] if lang=="en" else f'{ui["products"]}{" · RO" if key=="high_flow" else " · OEM/ODM" if key=="vending" else ""}'
        sections.append(f'<section class="tx-section {"tx-section--tint" if index==2 else ""}" data-commercial-group="{key}"><div class="tx-container"><div class="tx-section-head"><h2>{esc(heading)}</h2></div><div class="tx-product-grid">{"".join(cards)}</div></div></section>')
    crumbs=[(title,None)];schema=collection_schema(lang,ui,COMMERCIAL_ROUTE,title,description,entries,crumbs)
    main=f'<main><section class="tx-hero"><div class="tx-container tx-hero-grid"><div>{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">Commercial · Office · Vending · RO</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div><div class="tx-stats"><div class="tx-stat"><strong>9</strong><span>Office</span></div><div class="tx-stat"><strong>4</strong><span>RO</span></div><div class="tx-stat"><strong>10</strong><span>OEM/ODM</span></div></div></div></section>{"".join(sections)}</main>'
    image=page_info(source_or_stage(site_root,stage,Path(lang)/COMMERCIAL_ROUTES[0])).get("image","../assets/logo.png")
    return render_shell(site_root,codes,lang,template,COMMERCIAL_ROUTE,title,description,main,schema,image)


def normalize_topbar_structure(text:str)->str:
    match=re.search(r'(<div\s+class="topbar".*?)(?=<header\b)',text,re.S|re.I)
    if not match:return text
    segment=match.group(1);balance=len(re.findall(r'<div\b',segment,re.I))-len(re.findall(r'</div>',segment,re.I))
    if balance<0:raise ValueError("topbar page contains unmatched closing divs")
    if balance==0:return text
    return text[:match.end()]+("</div>"*balance)+text[match.end():]


def replace_hreflangs(site_root:Path,codes:list[str],text:str,lang:str,route:str)->str:
    text=normalize_topbar_structure(text)
    text=patch_products_menu(text,locale_pack(site_root,lang)["ui"],menu_labels(site_root,lang),route)
    text=route_language_links(text,route)
    if lang == "en":
        text=re.sub(r'href=["\']index\.html(?:#[^"\']*)?["\']','href="../"',text)
    canonical=f'{BASE_URL}{lang}/{route}';text=re.sub(r'\s*<link\s+rel="alternate"\s+hreflang="[^"]+"\s+href="[^"]+"\s*/?>',"",text,flags=re.I)
    match=re.search(r'<link\s+rel="canonical"\s+href="[^"]+"\s*/?>',text,re.I)
    if match: text=text[:match.start()]+f'<link rel="canonical" href="{canonical}">\n{alternates(site_root,codes,route)}'+text[match.end():]
    else: text=text.replace("</head>",f'<link rel="canonical" href="{canonical}">\n{alternates(site_root,codes,route)}\n</head>',1)
    return text


def patch_schema_breadcrumbs(value:Any,crumb:dict[str,Any],category:str)->bool:
    changed=False
    if isinstance(value,dict):
        if value.get("@type")=="BreadcrumbList": value.clear();value.update(deepcopy(crumb));changed=True
        elif value.get("@type")=="Product": value["category"]=category
        for child in list(value.values()): changed=patch_schema_breadcrumbs(child,crumb,category) or changed
    elif isinstance(value,list):
        for child in value: changed=patch_schema_breadcrumbs(child,crumb,category) or changed
    return changed


def ensure_indexable(text:str)->str:
    robots_pattern=r'<meta\b(?=[^>]*\bname=["\']robots["\'])[^>]*>'
    if re.search(robots_pattern,text,re.I):
        return re.sub(robots_pattern,'<meta name="robots" content="index,follow">',text,count=1,flags=re.I)
    return text.replace('</head>','<meta name="robots" content="index,follow">\n</head>',1)


def patch_detail(site_root:Path,codes:list[str],lang:str,ui:dict[str,Any],text:str,route:str,title:str,parent_chain:list[tuple[str,str|None]],category:str)->str:
    text=replace_hreflangs(site_root,codes,text,lang,route)
    # Every registered product detail is intentionally indexable and is present in
    # its locale sitemap. Normalizing legacy noindex flags keeps those two signals
    # consistent without changing the stable route or canonical.
    text=ensure_indexable(text)
    crumb_html=breadcrumb_html(ui,[*parent_chain,(title,None)])
    text,count=re.subn(r'<nav\s+class="[^"]*breadcrumb[^"]*"[^>]*>.*?</nav>',crumb_html,text,count=1,flags=re.S|re.I)
    if count==0:
        h1=re.search(r'<h1\b',text,re.I)
        if h1: text=text[:h1.start()]+crumb_html+text[h1.start():]
    crumb=breadcrumb_schema(lang,ui,route,[*parent_chain,(title,None)]);scripts=list(re.finditer(r'(<script\s+type="application/ld\+json"[^>]*>)(.*?)(</script>)',text,re.S|re.I));patched=False
    for m in reversed(scripts):
        try:data=json.loads(m.group(2))
        except json.JSONDecodeError:continue
        if patch_schema_breadcrumbs(data,crumb,category): text=text[:m.start()]+m.group(1)+json.dumps(data,ensure_ascii=False,separators=(",",":"))+m.group(3)+text[m.end():];patched=True
    if not patched:
        text=text.replace("</head>",f'<script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":[crumb]},ensure_ascii=False,separators=(",",":"))}</script></head>',1)
    return text


def enhance_en_quick_change_detail(text: str, route: str) -> str:
    """Turn the five reviewed EN quick-change pages into compact decision pages.

    All visible facts are reused from the existing page. Unknown fit and project
    inputs stay explicitly unconfirmed instead of becoming sales claims.
    """
    if route not in EN_QUICK_CHANGE_DETAIL_ROUTES:
        return text
    if 'data-decision-card="true"' in text:
        return text
    copy_match = re.search(r'<div class="sy-detail-copy">(.*?)</div>\s*</div>', text, re.S | re.I)
    if not copy_match:
        raise ValueError(f"quick-change detail copy missing: {route}")
    block = copy_match.group(1)
    title_match = re.search(r'<h1>(.*?)</h1>', block, re.S | re.I)
    desc_match = re.search(r'<p class="desc">(.*?)</p>', block, re.S | re.I)
    facts_match = re.search(r'<table class="sy-facts-table">(.*?)</table>', block, re.S | re.I)
    product_id_match = re.search(r'[?&](?:amp;)?product_id=([^&"\']+)', block, re.I)
    if not all((title_match, desc_match, facts_match, product_id_match)):
        raise ValueError(f"quick-change source facts missing: {route}")
    title_html = title_match.group(1)
    title_text = text_only(title_html)
    description = desc_match.group(1)
    product_id = html.unescape(product_id_match.group(1))
    common = {
        "product_id": product_id,
        "language": "en",
        "source_page": route,
        "family": "bayonet",
    }
    quote_query = urlencode({**common, "cta_location": "product_detail_primary"})
    catalog_query = urlencode({**common, "cta_location": "product_detail_catalog"})
    whatsapp_text = quote_plus(
        f"Hello Yuchen Water, I am reviewing {title_text}. Please help confirm the matching head, dimensions and project requirements."
    )
    replacement = f'''<div class="sy-detail-copy sy-decision-card" data-decision-card="true" data-product-id="{esc(product_id)}">
    <span class="eyebrow">Bayonet-Lock Quick-Change Cartridges</span><h1>{title_html}</h1>
    <p class="desc sy-direct-answer" data-direct-answer>{description}</p>
    <div class="sy-decision-columns"><section><h2>Confirmed product facts</h2><div class="sy-facts-wrap" data-known-facts><table class="sy-facts-table">{facts_match.group(1)}</table></div></section>
    <section class="sy-confirm-card" data-confirm-facts><h2>Confirm for quotation</h2><ul><li>Matching head and connection geometry</li><li>Required cartridge dimensions</li><li>Project operating conditions and quantity</li></ul><p>No unverified fit, capacity, MOQ, lead-time or certification claim is assumed on this page.</p></section></div>
    <div class="product-actions sy-decision-actions" data-cta-location="product_actions"><a href="contact.html?{quote_query}" class="btn btn-gold" data-primary-cta data-cta-location="product_detail_primary">Submit Project Parameters / Request Quote</a><a href="filter-cartridge-catalog.html?{catalog_query}" class="btn" data-catalog-cta data-cta-location="product_detail_catalog">Download Filter Cartridge Catalog</a><a href="https://wa.me/8619908311885?text={whatsapp_text}" class="btn btn-secondary" target="_blank" rel="noopener" data-cta-location="product_whatsapp">WhatsApp Product Context</a></div>
  </div>'''
    return text[:copy_match.start()] + replacement + text[copy_match.end() - len("</div>"):]


def render_missing_detail(site_root:Path,codes:list[str],lang:str,template:str,route:str,title:str,parent_chain:list[tuple[str,str|None]],category:str,info:dict[str,str],ui:dict[str,Any])->str:
    description=ui["summary"];canonical=f'{BASE_URL}{lang}/{route}';crumbs=[*parent_chain,(title,None)];schema={"@context":"https://schema.org","@graph":[{"@type":"WebPage","url":canonical,"name":title,"description":description,"inLanguage":ui.get("html_lang",lang)},breadcrumb_schema(lang,ui,route,crumbs),{"@type":"Product","name":title,"url":canonical,"description":description,"image":f'{BASE_URL}{info.get("image","../assets/logo.png").removeprefix("../")}',"brand":{"@type":"Brand","name":"Yuchen Water"},"category":category}]}
    signature=technical_signature(title)
    tags=f'<span class="tx-tag">{esc(signature)}</span>' if signature else ""
    main=f'<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,crumbs)}<span class="tx-eyebrow">Yuchen Water · RO · OEM/ODM</span><h1>{esc(title)}</h1><p class="tx-lede">{esc(description)}</p></div></section><section class="tx-section"><div class="tx-container"><article class="tx-card tx-product-card">{image_markup(info,title,True)}<div class="tx-card-copy"><h2>{esc(title)}</h2><div class="tx-tags">{tags}</div><p>{esc(description)}</p><a class="tx-btn tx-btn--solid" href="contact.html">{esc(ui["contact"])}</a></div></article></div></section></main>'
    return render_shell(site_root,codes,lang,template,route,title,description,main,schema,info.get("image","../assets/logo.png"))


def patch_sitemap(text:str,lang:str,routes:Iterable[str])->str:
    pattern=re.escape(TAXONOMY_URL_START)+r".*?"+re.escape(TAXONOMY_URL_END)+r"\s*";text=re.sub(pattern,"",text,flags=re.S)
    prefix="ns0:" if "<ns0:urlset" in text else "";existing=set(re.findall(r"<[^:>]*:?loc>(.*?)</[^:>]*:?loc>",text));rows=[]
    normalized=set(routes)
    for route in sorted(normalized):
        url=f'{BASE_URL}{lang}/{route}'
        if url not in existing: rows.append(f'  <{prefix}url><{prefix}loc>{url}</{prefix}loc><{prefix}lastmod>{LASTMOD}</{prefix}lastmod></{prefix}url>')
    close=f'</{prefix}urlset>'
    if close not in text: raise ValueError(f'invalid sitemap: {lang}')
    block=f'{TAXONOMY_URL_START}\n'+"\n".join(rows)+f'\n{TAXONOMY_URL_END}\n'
    result=text.replace(close,block+close,1)
    if lang=="en":
        result=re.sub(r'\s*<[^:>]*:?url>\s*<[^:>]*:?loc>https://www\.yuchensy\.com/en/index\.html</[^:>]*:?loc>.*?</[^:>]*:?url>',"",result,flags=re.S)
    return result


def build_llms_files(site_root:Path,stage:Path,oem:list[dict[str,Any]])->tuple[str,str]:
    family_rows=[]
    for row in OEM_FAMILIES:
        family_rows.append(f'- {row["key"]}: {BASE_URL}en/{row["route"]} ({row["count"]} products)')
    concise="\n".join((
        "# Yuchen Water",
        "",
        "Yuchen Water manufactures water filtration components, drinking-water systems and OEM/ODM product platforms in Haining, Zhejiang, China.",
        "",
        LLMS_START,
        "## Canonical product discovery",
        "<!-- SANYISHUI_CATALOG_START -->",
        f'- Products overview: {BASE_URL}en/products.html',
        f'- Yuchen Water products: {BASE_URL}en/{YUCHEN_HUB_ROUTE}',
        f'- OEM/ODM product collection: {BASE_URL}en/sanyishui-products.html',
        f'- Private English catalog request: {BASE_URL}en/sanyishui-catalog.html',
        f'- Commercial, office and vending RO systems: {BASE_URL}en/{COMMERCIAL_ROUTE}',
        f'- Water softener systems: {BASE_URL}en/{SOFTENER_ROUTE}',
        f'- Industrial RO and seawater desalination: {BASE_URL}en/{INDUSTRIAL_ROUTE}',
        f'- 2,000 L/h seawater desalination RO system: {BASE_URL}en/{SEAWATER_2000_ROUTE}',
        "",
        "## OEM/ODM families",
        *family_rows,
        "",
        f'- Contact: {BASE_URL}en/contact.html',
        "- Product specifications, compatibility and project configuration must be confirmed in the quotation.",
        "<!-- SANYISHUI_CATALOG_END -->",
        LLMS_END,
        "",
    ))
    product_rows=[]
    for product in oem:
        family=family_by_key(product["category_key"])
        product_rows.append(
            f'- {product["name_en"]}: {BASE_URL}en/{product["route"]} — '
            f'{product["category_en"]}; family: {family["key"]}. '
            'Specifications and project configuration require quotation confirmation.'
        )
    for route in NON_OEM_CANONICAL_ROUTES:
        info=page_info(source_or_stage(site_root,stage,Path("en")/route))
        name=info.get("title",route.removesuffix(".html").replace("-"," "))
        description=info.get("description","")
        product_rows.append(f'- {name}: {BASE_URL}en/{route}' + (f' — {description}' if description else ""))
    if len(product_rows)!=159:
        raise ValueError(f"llms-full canonical product count drift: {len(product_rows)}")
    full=concise+"\n## 159 canonical English product pages\n"+"\n".join(product_rows)+"\n"
    return concise,full


def render_report(site_root:Path,stage:Path,codes:list[str],detail_count:int,missing_generated:int)->str:
    rows=[]
    for lang in codes:
        checks=[]
        for route in ("products.html",YUCHEN_HUB_ROUTE,"sanyishui-products.html",SOFTENER_ROUTE,INDUSTRIAL_ROUTE,COMMERCIAL_ROUTE,*[f["route"] for f in OEM_FAMILIES]): checks.append((route,(stage/lang/route).is_file()))
        rows.append(f'<tr><td>{esc(lang)}</td><td>{sum(ok for _,ok in checks)}/{len(checks)}</td><td><a href="../../{lang}/products.html">Products</a></td><td><a href="../../{lang}/{YUCHEN_HUB_ROUTE}">Yuchen</a></td><td><a href="../../{lang}/sanyishui-products.html">OEM</a></td><td><a href="../../{lang}/quick-change-water-filter-cartridges.html">Bayonet</a></td><td><a href="../../{lang}/{SOFTENER_ROUTE}">Softener</a></td><td><a href="../../{lang}/{INDUSTRIAL_ROUTE}">Industrial</a></td><td><a href="../../{lang}/{COMMERCIAL_ROUTE}">Commercial</a></td></tr>')
    return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>Yuchen Water Product Taxonomy Preview</title><style>body{{font:16px/1.5 Arial;margin:0;background:#f4f8f7;color:#15353c}}main{{width:min(1500px,calc(100% - 32px));margin:auto;padding:40px 0}}.stats{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px}}.stat,table{{background:white;border:1px solid #c9deda;border-radius:12px}}.stat{{padding:18px}}table{{width:100%;border-collapse:collapse;margin-top:24px}}th,td{{padding:10px;border-bottom:1px solid #dce9e6;text-align:left}}a{{color:#08776f}}@media(max-width:900px){{.stats{{grid-template-columns:1fr 1fr}}table{{display:block;overflow:auto;font-size:13px}}}}</style></head><body><main><h1>Product Taxonomy Local Preview</h1><p><a href="../../en/products.html">Open complete English Products</a> · <a href="menu-browser-qa-20260813.json">Menu browser QA</a> · <a href="menu-cleanup-validation.json">Strict menu validation</a> · <a href="menu-cleanup-red-green.json">Red→green mutations</a> · <a href="browser-qa.html">Earlier full browser matrix</a> · <a href="../../migration/site-quality-control/runs/product-taxonomy-release-20260812-green/scorecard.html">Full site scorecard</a></p><div class="stats"><div class="stat"><strong>63</strong><br>locales</div><div class="stat"><strong>159</strong><br>canonical products</div><div class="stat"><strong>10,017</strong><br>localized product details</div><div class="stat"><strong>0</strong><br>broken package references</div></div><table><thead><tr><th>Locale</th><th>Core pages</th><th colspan="7">Direct preview links</th></tr></thead><tbody>{"".join(rows)}</tbody></table></main></body></html>'''


def stage_product_taxonomy(site_root:Path,site_stage:Path)->dict[str,int]:
    codes=locale_codes(site_root);terms_by_locale=read_json(site_root/LOCALES_PATH)["locales"];oem=oem_inventory(site_root);soft=public_softener_facts(site_root);industrial=industrial_facts(site_root);industrial_routes={Path(p["source_page"]).name for p in industrial};yuchen=yuchen_routes(site_root,site_stage);yuchen_label={r["route"]:r["category"] for r in yuchen}
    canonical_product_routes(tuple(p["route"] for p in oem))
    templates={lang:source_or_stage(site_root,site_stage,Path(lang)/"products.html").read_text(encoding="utf-8") for lang in codes}
    (site_stage/CSS_ROUTE).parent.mkdir(parents=True,exist_ok=True);(site_stage/CSS_ROUTE).write_text(CSS,encoding="utf-8")
    missing_generated=0;detail_touched=0;all_detail_routes=set()
    for lang in codes:
        pack=locale_pack(site_root,lang);ui=pack["ui"];terms=terms_by_locale[lang];target=site_stage/lang;target.mkdir(parents=True,exist_ok=True);template=templates[lang]
        (target/"products.html").write_text(render_products(site_root,site_stage,codes,lang,template,yuchen,oem,industrial_routes),encoding="utf-8")
        (target/YUCHEN_HUB_ROUTE).write_text(render_yuchen_hub(site_root,site_stage,codes,lang,template,terms),encoding="utf-8")
        (target/"sanyishui-products.html").write_text(render_oem_hub(site_root,site_stage,codes,lang,template,oem),encoding="utf-8")
        for family in OEM_FAMILIES:
            if family["key"]=="bayonet" and lang != "en" and source_or_stage(site_root,site_stage,Path(lang)/family["route"]).is_file():
                source=source_or_stage(site_root,site_stage,Path(lang)/family["route"]).read_text(encoding="utf-8");(target/family["route"]).write_text(replace_hreflangs(site_root,codes,source,lang,family["route"]),encoding="utf-8")
            else:(target/family["route"]).write_text(render_oem_family(site_root,site_stage,codes,lang,template,family,oem),encoding="utf-8")
        (target/SOFTENER_ROUTE).write_text(render_softener_hub(site_root,codes,lang,template,terms,soft),encoding="utf-8")
        for family in soft["families"]:(target/Path(family["route"]).name).write_text(render_softener_family(site_root,codes,lang,template,terms,family),encoding="utf-8")
        (target/INDUSTRIAL_ROUTE).write_text(render_industrial(site_root,site_stage,codes,lang,template,terms,industrial),encoding="utf-8")
        (target/COMMERCIAL_ROUTE).write_text(render_commercial(site_root,site_stage,codes,lang,template),encoding="utf-8")
        if lang in FOUNDATION_LOCALES:
            (target/"index.html").write_text(render_foundation_home(site_root,codes,lang,template,site_stage),encoding="utf-8")
            (target/"contact.html").write_text(render_foundation_contact(site_root,codes,lang,template),encoding="utf-8")
        else:
            home_source=source_or_stage(site_root,site_stage,Path(lang)/"index.html")
            if home_source.is_file():
                (target/"index.html").write_text(patch_homepage(site_root,codes,home_source.read_text(encoding="utf-8"),lang),encoding="utf-8")
        contact_source=source_or_stage(site_root,site_stage,Path(lang)/"contact.html")
        if contact_source.is_file() and lang not in FOUNDATION_LOCALES:
            (target/"contact.html").write_text(replace_hreflangs(site_root,codes,contact_source.read_text(encoding="utf-8"),lang,"contact.html"),encoding="utf-8")
        catalog_route="commercial-ro-water-systems-catalog.html"
        catalog_source=source_or_stage(site_root,site_stage,Path(lang)/catalog_route)
        if not catalog_source.is_file() and lang=="sr-me":
            catalog_source=source_or_stage(site_root,site_stage,Path("cnr")/catalog_route)
        if catalog_source.is_file():
            catalog_text=catalog_source.read_text(encoding="utf-8")
            if lang=="sr-me":
                catalog_text=catalog_text.replace(f'{BASE_URL}cnr/',f'{BASE_URL}sr-me/')
                catalog_text=re.sub(r'<html\b[^>]*\blang="[^"]+"',f'<html lang="{esc(ui.get("html_lang",lang))}"',catalog_text,count=1,flags=re.I)
            (target/catalog_route).write_text(replace_hreflangs(site_root,codes,catalog_text,lang,catalog_route),encoding="utf-8")
        # Create the four legacy Yuchen category gateways missing from the six newly added locales.
        for category in YUCHEN_CATEGORIES:
            route=category["route"]
            if route in {SOFTENER_ROUTE,INDUSTRIAL_ROUTE}:continue
            category_source=source_or_stage(site_root,site_stage,Path(lang)/route)
            if category_source.is_file():
                category_text=category_source.read_text(encoding="utf-8")
                category_text=ensure_indexable(replace_hreflangs(site_root,codes,category_text,lang,route))
                (target/route).write_text(category_text,encoding="utf-8")
                continue
            name=category_title(site_root,site_stage,lang,category["key"],terms);subset=[r for r in yuchen if category_key_for_label(r["category"],r["route"],industrial_routes)==category["key"]];cards=[];entries=[]
            for row in subset:
                info=product_info(site_root,site_stage,lang,row["route"],name);cards.append(card(info["title"],row["route"],info,ui["summary"],product=True));entries.append((info["title"],row["route"]))
            crumbs=[(f'Yuchen Water · {ui["products"]}',YUCHEN_HUB_ROUTE),(name,None)];schema=collection_schema(lang,ui,route,name,ui["summary"],entries,crumbs);main=f'<main><section class="tx-hero"><div class="tx-container">{breadcrumb_html(ui,crumbs)}<h1>{esc(name)}</h1><p class="tx-lede">{esc(ui["summary"])}</p></div></section><section class="tx-section"><div class="tx-container"><div class="tx-product-grid">{"".join(cards)}</div></div></section></main>'
            (target/route).write_text(render_shell(site_root,codes,lang,template,route,name,ui["summary"],main,schema,"assets/products/smart-ro-water-purifier-400g-1200g-oem.webp"),encoding="utf-8")
        # Keep the seven independent buying guides aligned with the same 63-language hreflang contract.
        for route in LEGACY_GUIDE_ROUTES:
            source=source_or_stage(site_root,site_stage,Path(lang)/route)
            if source.is_file():
                guide_text=source.read_text(encoding="utf-8")
                if lang=="tl":
                    guide_text=guide_text.replace("GAC vs CTO vs PAC vs UDF vs T33: Paano Naiiba ang Mga Format ng Carbon","GAC vs CTO vs PAC vs UDF vs T33: Paano Naiiba ang Mga Format ng Aktibong Karbon").replace("Paano Magbasa ng Activated Carbon Raw-Material at Mga Detalye ng Pagsubok","Paano Magbasa ng Hilaw na Materyal na Aktibong Karbon at Mga Detalye ng Pagsubok")
                (target/route).write_text(replace_hreflangs(site_root,codes,guide_text,lang,route),encoding="utf-8")
        parent_titles={row["key"]:category_title(site_root,site_stage,lang,row["key"],terms) for row in YUCHEN_CATEGORIES}
        # OEM details.
        for p in oem:
            route=p["route"];family=family_by_key(p["category_key"]);parent=pack["categories"][p["category_key"]];meta=localized_oem_product(pack,p);source=source_or_stage(site_root,site_stage,Path(lang)/route);text=source.read_text(encoding="utf-8");chain=[(ui["collection"],"sanyishui-products.html"),(parent,family["route"])];(target/route).write_text(patch_detail(site_root,codes,lang,ui,text,route,meta["title"],chain,parent),encoding="utf-8");all_detail_routes.add(route);detail_touched+=1
        # English OEM inventory rows are retired noindex aliases.  Emit their
        # reviewed indexable canonical targets as first-class stage outputs so
        # downstream catalog work can never accidentally decorate only aliases.
        if lang == "en":
            for product in oem:
                public_route = _english_public_route(site_root, product["route"])
                if public_route == product["route"]:
                    continue
                public_source = source_or_stage(site_root, site_stage, Path(lang) / public_route)
                if not public_source.is_file():
                    raise ValueError(f"missing canonical English OEM page: {public_route}")
                public_text = patch_products_menu(
                    public_source.read_text(encoding="utf-8"), ui,
                    menu_labels(site_root, lang), public_route,
                )
                (target / public_route).write_text(public_text, encoding="utf-8")
            # The five bayonet pages also use the compact decision-first pilot.
            for semantic_route in EN_QUICK_CHANGE_DETAIL_ROUTES:
                semantic_source = source_or_stage(site_root, site_stage, Path(lang) / semantic_route)
                if not semantic_source.is_file():
                    raise ValueError(f"missing semantic quick-change page: {semantic_route}")
                semantic_text = semantic_source.read_text(encoding="utf-8")
                semantic_text = patch_products_menu(semantic_text, ui, menu_labels(site_root, lang), semantic_route)
                (target / semantic_route).write_text(
                    enhance_en_quick_change_detail(semantic_text, semantic_route),
                    encoding="utf-8",
                )
        # Commercial details; sr-me safely reuses the approved cnr localization.
        commercial_title=page_info(target/COMMERCIAL_ROUTE)["title"]
        for route in COMMERCIAL_ROUTES:
            source=source_or_stage(site_root,site_stage,Path(lang)/route)
            if not source.is_file() and lang=="sr-me":source=source_or_stage(site_root,site_stage,Path("cnr")/route)
            info=product_info(site_root,site_stage,lang,route,commercial_title)
            if source.is_file():
                text=source.read_text(encoding="utf-8")
                if lang=="sr-me":
                    text=text.replace(f'{BASE_URL}cnr/',f'{BASE_URL}sr-me/')
                if '<body class="taxonomy-page"' in text:
                    out=render_missing_detail(site_root,codes,lang,template,route,info["title"],[(commercial_title,COMMERCIAL_ROUTE)],commercial_title,info,ui)
                else:
                    text=re.sub(r'<html\b[^>]*\blang="[^"]+"',f'<html lang="{esc(ui.get("html_lang",lang))}"',text,count=1,flags=re.I)
                    out=patch_detail(site_root,codes,lang,ui,text,route,info["title"],[(commercial_title,COMMERCIAL_ROUTE)],commercial_title)
            else:out=render_missing_detail(site_root,codes,lang,template,route,info["title"],[(commercial_title,COMMERCIAL_ROUTE)],commercial_title,info,ui);missing_generated+=1
            (target/route).write_text(out,encoding="utf-8");all_detail_routes.add(route);detail_touched+=1
        # All Yuchen details, including the 327 previously missing locale pages.
        for row in yuchen:
            route=row["route"]
            if route in COMMERCIAL_ROUTES:continue
            key=category_key_for_label(row["category"],route,industrial_routes)
            if key == "direct":
                parent=f'Yuchen Water · {ui["products"]}'
                parent_route=YUCHEN_HUB_ROUTE
                chain=[(parent,parent_route)]
            else:
                parent=parent_titles[key]
                parent_route=YUCHEN_PRIMARY_PARENT_BY_ROUTE[route]
                chain=[(f'Yuchen Water · {ui["products"]}',YUCHEN_HUB_ROUTE),(parent,parent_route)]
            info=product_info(site_root,site_stage,lang,route,parent);source=source_or_stage(site_root,site_stage,Path(lang)/route)
            if source.is_file():
                text=source.read_text(encoding="utf-8")
                out=render_missing_detail(site_root,codes,lang,template,route,info["title"],chain,parent,info,ui) if '<body class="taxonomy-page"' in text else patch_detail(site_root,codes,lang,ui,text,route,info["title"],chain,parent)
            else:out=render_missing_detail(site_root,codes,lang,template,route,info["title"],chain,parent,info,ui);missing_generated+=1
            (target/route).write_text(out,encoding="utf-8");all_detail_routes.add(route);detail_touched+=1
        sitemap_source=source_or_stage(site_root,site_stage,Path("sitemaps")/f"sitemap-{lang}.xml");sitemap_target=site_stage/"sitemaps"/f"sitemap-{lang}.xml";sitemap_target.parent.mkdir(parents=True,exist_ok=True)
        taxonomy_routes=["products.html",YUCHEN_HUB_ROUTE,"sanyishui-products.html",SOFTENER_ROUTE,INDUSTRIAL_ROUTE,COMMERCIAL_ROUTE,*[x["route"] for x in OEM_FAMILIES],*[x["route"] for x in YUCHEN_CATEGORIES],*[Path(f["route"]).name for f in soft["families"]],*all_detail_routes]
        sitemap_target.write_text(patch_sitemap(sitemap_source.read_text(encoding="utf-8"),lang,taxonomy_routes),encoding="utf-8")
    # Header navigation is shared beyond taxonomy-owned pages. Patch every
    # top-level localized HTML page through the same deterministic locale data
    # so rebuilding OEM pages cannot restore legacy Product/RO labels.
    for lang in codes:
        ui=locale_pack(site_root,lang)["ui"];labels=menu_labels(site_root,lang)
        for source in sorted((site_root/lang).glob("*.html")):
            relative=Path(lang)/source.name
            current=source_or_stage(site_root,site_stage,relative)
            text=current.read_text(encoding="utf-8")
            if 'data-oem-products-menu="true"' not in text and not re.search(r'href="products\.html"[^>]*class="[^"]*nav-link',text,re.I):
                continue
            updated=patch_products_menu(text,ui,labels,source.name)
            if updated!=text or (site_stage/relative).is_file():
                (site_stage/relative).parent.mkdir(parents=True,exist_ok=True)
                (site_stage/relative).write_text(updated,encoding="utf-8")
    enhance_english_catalog_experience(site_root, site_stage, oem)
    # Several pages are rewritten during this build.  Discard cached page
    # metadata so llms files always describe the final staged document rather
    # than an earlier intermediate version.
    page_info.cache_clear()
    llms,llms_full=build_llms_files(site_root,site_stage,oem)
    (site_stage/"llms.txt").write_text(llms,encoding="utf-8")
    (site_stage/"llms-full.txt").write_text(llms_full,encoding="utf-8")
    report=render_report(site_root,site_stage,codes,detail_touched,missing_generated);report_path=site_stage/REPORT_ROOT/"index.html";report_path.parent.mkdir(parents=True,exist_ok=True);report_path.write_text(report,encoding="utf-8")
    write_json(site_stage/REPORT_ROOT/"summary.json",{"status":"READY_FOR_LOCAL_QA","locales":63,"canonical_products":159,"canonical_product_language_pages":159*63,"oem_families":9,"oem_details":63*72,"yuchen_routes":65,"commercial_routes":23,"industrial_routes":17,"detail_pages_processed":detail_touched,"missing_pages_generated":missing_generated,"publication_allowed":False})
    for relative in ('fr/products.html', 'fr/ro-membrane.html', 'fr/product-ro-membrane-400g.html'):
        corrected_path = site_stage / relative
        if corrected_path.is_file():
            corrected_path.write_text(correct_html(corrected_path.read_text(encoding='utf-8'), relative), encoding='utf-8')
    schema_normalized=normalize_stage_html(site_stage)
    return {"locales":63,"products_pages":63,"yuchen_hubs":63,"oem_hubs":63,"oem_family_pages":63*9,"softener_pages":63*8,"industrial_hubs":63,"commercial_hubs":63,"detail_pages_processed":detail_touched,"missing_pages_generated":missing_generated,"schema_policy_normalized_html":len(schema_normalized)}


def apply_stage(stage:Path,site_root:Path)->dict[str,Any]:
    # Validate the entire product overlay before copying even its first file.
    # A generated file is not evidence of a complete product translation.
    from product_stage_gate import require_safe_stage
    require_safe_stage(stage,site_root)
    files=sorted(p for p in stage.rglob("*") if p.is_file());changed=[]
    for source in files:
        relative=source.relative_to(stage);target=site_root/relative
        if not target.is_file() or target.read_bytes()!=source.read_bytes():changed.append(relative.as_posix())
        target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,target)
    return {"status":"PASS","files":len(files),"changed":len(changed),"changed_files":changed}


def compare_stage(stage:Path,site_root:Path)->dict[str,Any]:
    changed=[]
    for source in sorted(p for p in stage.rglob("*") if p.is_file()):
        target=site_root/source.relative_to(stage)
        if not target.is_file() or target.read_bytes()!=source.read_bytes():changed.append(source.relative_to(stage).as_posix())
    return {"status":"PASS" if not changed else "FAIL","changed":len(changed),"changed_files":changed}


def main()->int:
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument("action",choices=("build","apply","compare"));parser.add_argument("--site-root",default=".");parser.add_argument("--stage",required=True);args=parser.parse_args();root=Path(args.site_root).resolve();stage=Path(args.stage).resolve()
    if args.action=="build":
        if stage.exists() and any(stage.iterdir()):raise ValueError(f"stage must be empty: {stage}")
        stage.mkdir(parents=True,exist_ok=True);print(json.dumps({"status":"PASS",**stage_product_taxonomy(root,stage)},ensure_ascii=False));return 0
    result=apply_stage(stage,root) if args.action=="apply" else compare_stage(stage,root);print(json.dumps(result,ensure_ascii=False));return 0 if result["status"]=="PASS" else 1


if __name__=="__main__":raise SystemExit(main())
