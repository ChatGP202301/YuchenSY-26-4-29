#!/usr/bin/env python3
"""Focused SEO and conversion patch for the Yuchen/Express Water static site.

The current project is a generated static site. This script intentionally keeps
the patch surface focused on public SEO assets and English B2B pages rather than
regenerating every translated page.
"""

from __future__ import annotations

import html
import json
import re
import shutil
from pathlib import Path
from urllib.parse import quote

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.yuchensy.com"
CORE_LANGS = ["en", "ru", "es", "ar", "fr", "de", "id", "vi"]
NON_CORE_LANGS = [
    "bg", "bn", "cs", "da", "el", "et", "fa", "fi", "ha", "he", "hi",
    "hr", "hu", "it", "ja", "kk", "ko", "lt", "lv", "ms", "nl", "no",
    "pl", "pt", "ro", "sk", "sl", "sr", "sv", "sw", "ta", "th", "tl",
    "tr", "uk", "ur", "zu",
]

ORG_NAME = "Yuchen Water"
PHONE = "+86-19908311885"
WA = "8619908311885"
EMAIL = "expresswater025@gmail.com"
ADDRESS = "Yuanhua Town, Haining City, Zhejiang Province, China"
SAFE_CERT = (
    "Selected products can be supplied or tested according to NSF/ANSI 42, 53 "
    "and 58 requirements. ISO 9001, CE, SGS and Halal-related documents are "
    "available upon request."
)

HOME_TITLE = "Water Filter Manufacturer China | RO, PP, CTO, GAC OEM Supplier"
HOME_DESC = (
    "Express Water is a China water filter manufacturer supplying PP melt blown "
    "filters, CTO carbon block, GAC, T33, UF, RO membranes and OEM/ODM water "
    "purification systems for global distributors."
)
HOME_H1 = "China Water Filter Manufacturer & OEM/ODM Water Filtration Supplier"


def esc(value: str) -> str:
    return html.escape(value or "", quote=True)


def slugify(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-+", "-", value).strip("-")
    return value or "water-filter"


def read_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def convert_primary_images(products: list[dict]) -> dict[str, str]:
    """Create keyword WebP images for English product pages and product cards."""
    mapping: dict[str, str] = {}
    products_dir = ROOT / "assets" / "products"
    for p in products:
        src_rel = p.get("image_local") or (p.get("image", "").replace("../", ""))
        if not src_rel:
            continue
        src = ROOT / src_rel
        if not src.exists():
            continue
        base = slugify(f"{p['name']} OEM")
        dst = products_dir / f"{base}.webp"
        if not dst.exists():
            try:
                with Image.open(src) as im:
                    if im.mode not in ("RGB", "RGBA"):
                        im = im.convert("RGBA" if "A" in im.mode else "RGB")
                    im.save(dst, "WEBP", quality=82, method=6)
            except Exception:
                continue
        old_page_ref = "../" + src_rel
        new_page_ref = "../assets/products/" + dst.name
        mapping[old_page_ref] = new_page_ref
        mapping[src_rel] = "assets/products/" + dst.name
        p["image"] = new_page_ref
        p["image_local"] = "assets/products/" + dst.name
        p["image_orig"] = old_page_ref
    return mapping


def org_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "@id": f"{SITE}/#organization",
        "name": ORG_NAME,
        "alternateName": ["Yuchen Water", "Express Water"],
        "url": SITE + "/",
        "logo": f"{SITE}/assets/logo.png",
        "address": {
            "@type": "PostalAddress",
            "streetAddress": "Yuanhua Town",
            "addressLocality": "Haining City",
            "addressRegion": "Zhejiang Province",
            "addressCountry": "CN",
        },
        "telephone": PHONE,
        "email": EMAIL,
        "industry": "Water filtration products manufacturer",
        "description": (
            "Yuchen Water is a China water filtration products manufacturer for "
            "global B2B OEM and ODM buyers."
        ),
        "makesOffer": [
            {"@type": "Offer", "itemOffered": {"@type": "Product", "name": item}}
            for item in [
                "PP melt blown filter",
                "CTO carbon block filter",
                "GAC filter",
                "T33 inline filter",
                "UF membrane",
                "RO membrane",
                "water purifier",
                "water dispenser",
                "filter housing",
            ]
        ],
        "contactPoint": {
            "@type": "ContactPoint",
            "telephone": PHONE,
            "email": EMAIL,
            "contactType": "sales engineering",
            "availableLanguage": ["en", "ru", "es", "ar", "fr", "de", "id", "vi"],
            "areaServed": "Worldwide",
        },
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "@id": f"{SITE}/#website",
        "name": "Yuchen Water",
        "url": SITE + "/",
        "publisher": {"@id": f"{SITE}/#organization"},
        "inLanguage": "en",
    }


def breadcrumb_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {
                "@type": "ListItem",
                "position": i + 1,
                "name": name,
                "item": url,
            }
            for i, (name, url) in enumerate(items)
        ],
    }


def faq_schema(faqs: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in faqs
        ],
    }


def product_schema(p: dict, page: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "@id": f"{SITE}/en/{page}#product",
        "name": p["name"],
        "description": p["summary"],
        "image": f"{SITE}/{p['image'].replace('../', '')}",
        "brand": {"@type": "Brand", "name": "Yuchen Water"},
        "manufacturer": {"@id": f"{SITE}/#organization"},
        "category": p["category"],
        "additionalProperty": [
            {"@type": "PropertyValue", "name": k, "value": v}
            for k, v in p["specs"].items()
        ],
        "offers": {
            "@type": "Offer",
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
            "url": f"{SITE}/en/{page}",
            "priceValidUntil": "2027-12-31",
        },
    }


def hreflang(page: str, lang: str = "en", homepage_root: bool = False) -> str:
    links = []
    for l in CORE_LANGS:
        href = f"{SITE}/{l}/{page}"
        links.append(f'  <link rel="alternate" hreflang="{l}" href="{href}" />')
    default = f"{SITE}/en/index.html" if homepage_root or page == "index.html" else f"{SITE}/en/{page}"
    links.append(f'  <link rel="alternate" hreflang="x-default" href="{default}" />')
    return "\n".join(links)


def head(title: str, desc: str, canonical: str, page: str, *, root_home: bool = False,
         image: str = "/assets/backgrounds/eco_hero1.webp", extra_json: list[dict] | None = None,
         preload: str | None = None) -> str:
    extras = [org_schema(), website_schema()]
    if extra_json:
        extras.extend(extra_json)
    preload_tag = f'  <link rel="preload" as="image" href="{preload}" fetchpriority="high" />\n' if preload else ""
    return f'''<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{esc(title)}</title>
  <meta name="description" content="{esc(desc)}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{canonical}" />
{hreflang(page, homepage_root=root_home)}
{preload_tag}  <link rel="dns-prefetch" href="https://wa.me" />
  <link rel="stylesheet" href="{'assets/styles.css' if root_home else '../assets/styles.css'}?v=20260531-seo" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{esc(title)}" />
  <meta property="og:description" content="{esc(desc)}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="{SITE}{image}" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@graph":extras}, ensure_ascii=False)}</script>
  <link rel="icon" href="{'assets/logo.png' if root_home else '../assets/logo.png'}" type="image/png" />
</head>
'''


def header(root_home: bool = False, active: str = "home") -> str:
    prefix = "en/" if root_home else ""
    asset = "" if root_home else "../"
    nav = [
        ("home", "index.html", "Home"),
        ("about", "about.html", "About"),
        ("products", "products.html", "Products"),
        ("workshop", "workshop.html", "Workshop"),
        ("faq", "faq.html", "FAQ"),
        ("contact", "contact.html", "Contact"),
    ]
    nav_html = "\n".join(
        f'<a href="{prefix}{href}" class="nav-link{" active" if key == active else ""}">{label}</a>'
        for key, href, label in nav
    )
    lang_options = "\n".join(
        f'<a href="{"" if root_home else "../"}{l}/index.html" class="lang-option{" active" if l == "en" else ""}" lang="{l}">{l.upper()}</a>'
        for l in CORE_LANGS
    )
    return f'''
<body class="ltr">
<div class="topbar">
  <div class="container topbar-row">
    <div class="topbar-left">{PHONE} &middot; {EMAIL}</div>
    <div class="topbar-right">Global OEM/ODM water filtration supplier</div>
  </div>
</div>
<header class="header">
  <div class="container header-row">
    <a href="{prefix}index.html" class="brand">
      <img src="{asset}assets/logo.png" alt="Yuchen Water filtration products manufacturer logo" class="logo-img" width="64" height="64" decoding="async" />
      <span class="brand-name">Yuchen Water</span>
    </a>
    <nav class="nav">
      {nav_html}
    </nav>
    <div class="header-actions">
      <div class="lang-switcher">
        <button class="lang-btn" onclick="toggleLangMenu()" type="button">EN</button>
        <div class="lang-menu" id="langMenu">{lang_options}</div>
      </div>
      <a href="{prefix}contact.html" class="btn btn-gold">Request OEM Quote</a>
      <a href="https://wa.me/{WA}" target="_blank" rel="noopener" class="cta-wa">Contact Engineer</a>
      <button class="mobile-menu-toggle" onclick="document.querySelector('.nav').classList.toggle('open')" type="button" aria-label="Open menu">Menu</button>
    </div>
  </div>
</header>
'''


def footer(root_home: bool = False) -> str:
    prefix = "en/" if root_home else ""
    asset = "" if root_home else "../"
    return f'''
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-col">
      <div class="footer-brand"><img src="{asset}assets/logo.png" alt="Yuchen Water logo" class="footer-logo" width="48" height="48" loading="lazy" decoding="async"><strong>Yuchen Water</strong></div>
      <p>China manufacturer of PP, CTO, GAC, T33, UF, RO membrane, water purifier, water dispenser and filter housing products for OEM/ODM buyers.</p>
      <p>{SAFE_CERT}</p>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <a href="{prefix}index.html">Home</a>
      <a href="{prefix}about.html">About</a>
      <a href="{prefix}products.html">Products</a>
      <a href="{prefix}workshop.html">Workshop</a>
      <a href="{prefix}faq.html">FAQ</a>
      <a href="{prefix}contact.html">Contact</a>
    </div>
    <div class="footer-col">
      <h4>Products</h4>
      <a href="{prefix}pp-melt-blown-filter-cartridge.html">PP Melt Blown Filter</a>
      <a href="{prefix}cto-carbon-block-filter.html">CTO Carbon Block</a>
      <a href="{prefix}ro-membrane.html">RO Membrane</a>
      <a href="{prefix}water-dispenser.html">Water Dispenser</a>
    </div>
    <div class="footer-col">
      <h4>Contact</h4>
      <p>{ADDRESS}</p>
      <p><a href="tel:{PHONE}">{PHONE}</a></p>
      <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><a href="https://wa.me/{WA}" target="_blank" rel="noopener">WhatsApp</a></p>
    </div>
  </div>
  <div class="footer-bottom"><div class="container">Yuchen Water &middot; ISO 9001, CE, SGS and selected NSF/ANSI test documents available upon request.</div></div>
</footer>
<a class="mobile-whatsapp-bar" href="https://wa.me/{WA}" target="_blank" rel="noopener">Contact Engineer on WhatsApp</a>
<script src="{asset}assets/site.js?v=20260531-seo" defer></script>
</body>
</html>
'''


TARGET_PRODUCTS = {
    "built-in-pressure-tank-ro": {
        "name": "Built-In Pressure Tank RO Water Purifier 100G/200G",
        "category": "RO Water Purifier",
        "summary": (
            "This built-in pressure tank RO water purifier is designed for distributors "
            "and OEM appliance brands that need a compact under-sink system with stable "
            "storage pressure and clean cabinet integration. The unit supports 100G and "
            "200G configurations, 5-stage or 6-stage filtration, private-label front "
            "panels, filter labels and carton design. It is suitable for household, "
            "apartment, office pantry and light commercial drinking water programs where "
            "buyers need reliable reverse osmosis performance, repeatable assembly and "
            "export-ready packaging from a China factory."
        ),
        "specs": {
            "Product Type": "Built-in tank reverse osmosis water purifier",
            "Flow Options": "100G / 200G",
            "Filtration Stages": "5-stage or 6-stage",
            "Tank": "Integrated pressure tank",
            "Applications": "Home, apartment, office pantry, private-label appliance programs",
            "OEM/ODM": "Front panel, label, faucet, filter set, packaging and manual",
        },
        "features": [
            "Compact cabinet design with integrated pressure tank",
            "Configurable 5-stage or 6-stage filtration layout",
            "RO membrane, PP, CTO, GAC and post-carbon filter matching",
            "Private-label appearance and packaging for distributor brands",
            "Factory assembly, leakage testing and export carton support",
        ],
        "applications": "Under-sink drinking water projects, residential kitchen programs, office pantry installations, regional distributor portfolios and OEM appliance brand lines.",
        "image_hint": "built-in-pressure-tank-ro",
        "related": ["ro-membrane", "pp-spun", "carbon-block", "udf-cartridge"],
    },
    "pp-spun": {
        "name": "PP Melt Blown Sediment Filter Cartridge",
        "category": "PP Melt Blown Filter",
        "summary": (
            "The PP melt blown sediment filter cartridge is a cost-efficient prefilter "
            "for removing sand, rust, silt and suspended particles before carbon, UF or "
            "RO stages. It is made from thermally bonded polypropylene without adhesives "
            "and can be supplied in common 10 inch and 20 inch lengths with micron "
            "ratings from 1 to 50 micron. OEM buyers can specify length, diameter, end "
            "cap style, label, flow target and carton design for residential, commercial "
            "and light industrial water treatment systems."
        ),
        "specs": {
            "Material": "Food-grade polypropylene",
            "Micron Rating": "1, 3, 5, 10, 20, 50 micron",
            "Length": "10 inch, 20 inch, 30 inch, 40 inch on request",
            "Outer Diameter": "2.5 inch standard; jumbo sizes available",
            "Function": "Sediment, sand, rust and suspended solids reduction",
            "OEM/ODM": "Micron, length, end cap, label and packaging",
        },
        "features": [
            "Gradient density structure for longer dirt holding capacity",
            "No adhesive or surfactant in the melt blown process",
            "Fits common residential and commercial filter housings",
            "Stable prefiltration for RO systems and water dispensers",
            "Low MOQ private-label packaging available for distributors",
        ],
        "applications": "RO system prefiltration, whole house prefilters, water dispenser inlet protection, commercial drinking water systems and replacement cartridge programs.",
        "image_hint": "pp-spun",
        "related": ["carbon-block", "udf-cartridge", "ro-membrane", "big-blue-3stage"],
    },
    "carbon-block": {
        "name": "CTO Coconut Shell Carbon Block Filter",
        "category": "CTO Carbon Block Filter",
        "summary": (
            "The CTO coconut shell carbon block filter is designed for chlorine, taste, "
            "odor and fine particle reduction in residential and commercial water "
            "systems. The compressed carbon block uses selected coconut shell activated "
            "carbon and a controlled pore structure for consistent flow and adsorption. "
            "It can be supplied in 10 inch, 20 inch and custom sizes with 1, 5 or 10 "
            "micron ratings. OEM/ODM options include carbon formula, end caps, gasket "
            "color, printed label, shrink wrap and export carton layout."
        ),
        "specs": {
            "Media": "Coconut shell activated carbon block",
            "Micron Rating": "1, 5 or 10 micron",
            "Length": "10 inch / 20 inch / custom",
            "Function": "Chlorine, taste, odor and organic compound reduction",
            "Compatibility": "RO systems, countertop filters, whole house housings",
            "OEM/ODM": "Formula, label, end cap, color and packaging",
        },
        "features": [
            "Compressed block structure for uniform water contact",
            "Coconut shell carbon for high adsorption performance",
            "Low fines release after proper flushing",
            "Common sizes for distributor replacement cartridge programs",
            "Private-label labels and retail packaging supported",
        ],
        "applications": "Second-stage RO filtration, drinking water purifiers, countertop systems, commercial prefilters and replacement cartridge kits.",
        "image_hint": "carbon-block",
        "related": ["pp-spun", "udf-cartridge", "inline-t33-coconut", "ro-membrane"],
    },
    "udf-cartridge": {
        "name": "GAC / UDF Filter Cartridge",
        "category": "GAC UDF Filter",
        "summary": (
            "The GAC / UDF filter cartridge uses granular activated carbon to reduce "
            "chlorine, odor and unpleasant taste before or after fine filtration stages. "
            "It is commonly installed in RO systems, water purifiers, dispensers and "
            "multi-stage cartridge sets. The cartridge can be built with coconut shell "
            "carbon, PP shell, non-woven pads and optional mesh or sponge protection. "
            "OEM buyers can customize carbon grade, cartridge length, cap design, label, "
            "bag, color box and master carton for wholesale replacement programs."
        ),
        "specs": {
            "Media": "Granular activated carbon",
            "Shell": "Food-grade PP",
            "Length": "10 inch / 20 inch",
            "Function": "Chlorine, odor and taste reduction",
            "Use Position": "Pre-carbon or post-carbon stage",
            "OEM/ODM": "Carbon media, shell color, label and carton",
        },
        "features": [
            "Granular carbon bed for broad contact area",
            "Suitable for pre-carbon and polishing stages",
            "Custom carbon iodine value and fill weight available",
            "Compatible with standard filter housings and RO sets",
            "Distributor-ready private-label packaging",
        ],
        "applications": "RO prefiltration, dispenser filtration, countertop purifier cartridges, domestic replacement sets and light commercial drinking water systems.",
        "image_hint": "udf-cartridge",
        "related": ["carbon-block", "inline-t33-coconut", "pp-spun", "ro-membrane"],
    },
    "inline-t33-coconut": {
        "name": "T33 Inline Carbon Filter",
        "category": "T33 Inline Filter",
        "summary": (
            "The T33 inline carbon filter is a compact polishing cartridge for RO water "
            "purifiers, direct drinking systems and water dispensers. It uses activated "
            "carbon media to improve final taste and reduce residual odor after storage "
            "or membrane filtration. The inline body can be supplied with quick-connect "
            "or threaded fittings, different lengths, coconut shell carbon, mineral "
            "media options, printed labels and private-label cartons. It is a practical "
            "OEM component for replacement filter sets and appliance manufacturing."
        ),
        "specs": {
            "Product Type": "Inline post-carbon filter",
            "Media": "Coconut shell activated carbon",
            "Connection": "1/4 inch quick-connect or threaded options",
            "Function": "Final taste and odor polishing",
            "Applications": "RO systems, water dispensers, direct drinking machines",
            "OEM/ODM": "Fitting, media, label, cap color and packaging",
        },
        "features": [
            "Compact inline shape for cabinet and dispenser installation",
            "Post-carbon polishing after RO membrane filtration",
            "Quick-connect options for faster assembly",
            "Mineral, alkaline or antibacterial media can be quoted",
            "Private-label filter label and carton available",
        ],
        "applications": "RO post-filter stage, direct drinking systems, water dispensers, refrigerator water lines and replacement filter kits.",
        "image_hint": "inline-t33-coconut",
        "related": ["ro-membrane", "udf-cartridge", "carbon-block", "built-in-pressure-tank-ro"],
    },
    "ro-membrane": {
        "name": "RO Membrane Element",
        "category": "RO Membrane",
        "summary": (
            "The RO membrane element is the core separation component for reverse "
            "osmosis water purification systems. It is not an under-sink purifier by "
            "itself; it is a replaceable membrane cartridge installed inside RO systems "
            "to reduce dissolved solids, heavy metals and salts. Yuchen Water supplies "
            "residential and light commercial membrane elements in common GPD ratings "
            "with OEM labeling, dry or wet preservation, batch traceability and export "
            "packing for system manufacturers and replacement filter distributors."
        ),
        "specs": {
            "Membrane Type": "TFC polyamide RO membrane",
            "Capacity": "50, 75, 100, 200, 400 GPD options",
            "Function": "TDS, salts and heavy metal reduction",
            "Use": "Replacement element for RO systems",
            "Packaging": "Individual sealed bag and export carton",
            "OEM/ODM": "Label, flow rating, private brand and carton",
        },
        "features": [
            "True membrane element description, not a complete RO system",
            "Multiple GPD ratings for residential and light commercial use",
            "Stable salt rejection and flow after standard prefiltration",
            "Private-label membrane sleeve and carton support",
            "Batch traceability and sampling inspection before shipment",
        ],
        "applications": "Under-sink RO systems, countertop RO purifiers, commercial drinking water machines and replacement membrane distribution.",
        "image_hint": "ro-membrane",
        "related": ["built-in-pressure-tank-ro", "pp-spun", "carbon-block", "inline-t33-coconut"],
    },
    "uf-filter-2": {
        "name": "UF Hollow Fiber Filter",
        "category": "UF Membrane Filter",
        "summary": (
            "The UF hollow fiber filter is a membrane cartridge for reducing suspended "
            "solids, colloids and microorganisms while keeping beneficial dissolved "
            "minerals in the water. It is commonly used in gravity purifiers, kitchen "
            "water filters, dispensers and multi-stage drinking water systems where "
            "electric pressure pumps are not required. OEM/ODM buyers can specify "
            "membrane material, pore size, housing shape, connector type, flow rate, "
            "label and packaging for local distribution or appliance integration."
        ),
        "specs": {
            "Membrane": "Hollow fiber UF membrane",
            "Nominal Pore Size": "0.01 micron class",
            "Function": "Colloid, turbidity and microorganism reduction",
            "Operation": "Pressure or gravity assisted, depending on design",
            "Applications": "Purifier cartridge, dispenser, kitchen filter",
            "OEM/ODM": "Housing, connector, membrane area, label and carton",
        },
        "features": [
            "Hollow fiber membrane filtration without RO wastewater",
            "Retains dissolved minerals while improving turbidity",
            "Suitable for low-pressure drinking water devices",
            "Custom housing and connector integration available",
            "Private-label replacement cartridge programs supported",
        ],
        "applications": "Gravity purifiers, kitchen drinking water filters, water dispensers, pre-RO protection and compact household filtration systems.",
        "image_hint": "uf-filter-2",
        "related": ["pp-spun", "carbon-block", "udf-cartridge", "ss-jumbo-housing"],
    },
    "ss-jumbo-housing": {
        "name": "304/316L Stainless Steel Filter Housing",
        "category": "Filter Housing",
        "summary": (
            "The 304/316L stainless steel filter housing is built for higher-pressure "
            "commercial and industrial water treatment applications where plastic "
            "housings may not be preferred. It can be configured for PP sediment, "
            "carbon block, UF or specialty cartridges in 10 inch, 20 inch and jumbo "
            "formats. Buyers can specify material grade, inlet/outlet size, surface "
            "finish, clamp or threaded closure, pressure rating, private nameplate and "
            "export packaging for OEM projects and engineering distributors."
        ),
        "specs": {
            "Material": "SUS 304 or SUS 316L stainless steel",
            "Length": "10 inch, 20 inch, jumbo and custom",
            "Connection": "NPT/BSP threaded options",
            "Cartridge Fit": "PP, CTO, GAC, UF and specialty cartridges",
            "Applications": "Commercial, industrial and high-flow filtration",
            "OEM/ODM": "Nameplate, finish, port size and packaging",
        },
        "features": [
            "Corrosion-resistant 304/316L stainless steel body",
            "Higher pressure capability than standard plastic housings",
            "Compatible with common cartridge families",
            "Custom port, bracket and surface finish available",
            "Suitable for engineering distributors and project orders",
        ],
        "applications": "Commercial prefiltration, industrial process water, food service systems, RO pretreatment skids and high-flow cartridge installations.",
        "image_hint": "ss-jumbo-housing",
        "related": ["big-blue-3stage", "pp-spun", "carbon-block", "uf-filter-2"],
    },
    "mt-e600": {
        "name": "Wall Mounted Water Dispenser",
        "category": "Water Dispenser",
        "summary": (
            "The wall mounted water dispenser is designed for compact drinking water "
            "installations in offices, schools, clinics, apartments and public service "
            "areas. It can be matched with PP, CTO, GAC, UF or RO filtration modules "
            "depending on the required water quality and market positioning. OEM/ODM "
            "options include shell color, control panel, tap layout, heating or cooling "
            "configuration, filter set, brand badge, carton artwork and user manual for "
            "regional distributors and appliance brands."
        ),
        "specs": {
            "Product Type": "Wall mounted drinking water dispenser",
            "Installation": "Wall mounted",
            "Filtration": "PP, CTO, GAC, UF or RO module options",
            "Functions": "Ambient, hot or cold configurations by model",
            "Applications": "Office, school, clinic, apartment, public area",
            "OEM/ODM": "Color, panel, badge, filter set and packaging",
        },
        "features": [
            "Space-saving wall mounted dispenser format",
            "Configurable filtration module for different markets",
            "Private-label shell, panel and user manual options",
            "Factory assembly and functional testing before shipment",
            "Distributor-ready carton and spare filter program",
        ],
        "applications": "Office hydration points, school drinking water, clinic waiting areas, apartment corridors, retail facilities and regional dispenser brands.",
        "image_hint": "mt-e600",
        "related": ["built-in-pressure-tank-ro", "uf-filter-2", "inline-t33-coconut", "pp-spun"],
    },
    "big-blue-3stage": {
        "name": "30-inch Three Stage Big Blue Water Filter",
        "category": "Big Blue Water Filter",
        "summary": (
            "The 30-inch three stage Big Blue water filter is a high-capacity filtration "
            "set for villas, commercial kitchens, light industrial prefiltration and "
            "project water treatment. It can combine sediment, carbon and fine filtration "
            "stages according to inlet water conditions and buyer requirements. The large "
            "housing format supports stronger flow than standard small cartridges. OEM "
            "buyers can specify cartridge sequence, housing color, bracket, pressure "
            "gauge, inlet/outlet size, logo label, carton design and spare cartridge kits."
        ),
        "specs": {
            "System Type": "Three stage Big Blue filter set",
            "Size": "30 inch housing class",
            "Stages": "Sediment, carbon and fine filtration options",
            "Connection": "Custom inlet/outlet options",
            "Applications": "Villa, commercial kitchen, light industrial prefiltration",
            "OEM/ODM": "Housing color, bracket, gauge, label and packaging",
        },
        "features": [
            "Large housing format for higher flow requirements",
            "Flexible three-stage cartridge configuration",
            "Can be matched with PP, CTO, GAC or specialty media",
            "Project-friendly brackets, gauges and connection options",
            "Private-label system and spare cartridge kit packaging",
        ],
        "applications": "Whole house prefiltration, commercial kitchens, light industrial water pretreatment, villas, farms and distributor project packages.",
        "image_hint": "big-blue-3stage",
        "related": ["ss-jumbo-housing", "pp-spun", "carbon-block", "udf-cartridge"],
    },
}


CATEGORY_PAGES = {
    "pp-melt-blown-filter-cartridge.html": {
        "h1": "PP Melt Blown Filter Cartridge Manufacturer",
        "title": "PP Melt Blown Filter Cartridge Manufacturer China | OEM Supplier",
        "desc": "China PP melt blown sediment filter cartridge manufacturer for OEM/ODM buyers. Custom micron, length, end cap, label and packaging for global distributors.",
        "product_ids": ["pp-spun", "pp-fin-cap", "pp-silicon-ring", "pp-soe-doe", "inline-pp"],
        "intro": "PP melt blown filter cartridges are the standard first-stage sediment filter for water purifiers, RO systems, dispensers and whole house filtration. Yuchen Water manufactures polypropylene cartridges from food-grade PP resin with a thermally bonded gradient-density structure, helping reduce sand, rust, silt and suspended particles before the water reaches carbon or membrane stages.",
        "applications": "Typical applications include household RO prefilters, commercial drinking water machines, dispenser inlet protection, prefiltration for UF and RO membranes, and replacement cartridge programs for regional distributors. Buyers can select 1, 3, 5, 10, 20 or 50 micron ratings depending on local water turbidity and service-life targets.",
        "oem": "OEM/ODM support covers cartridge length, diameter, micron rating, end cap format, private label, printed bag, color box, carton mark and pallet packing. The factory can quote standard 10 inch and 20 inch cartridges as well as jumbo sizes for commercial housings.",
        "table": [
            ("Material", "Food-grade polypropylene"),
            ("Micron Options", "1, 3, 5, 10, 20, 50 micron"),
            ("Lengths", "10 inch, 20 inch, 30 inch, 40 inch"),
            ("Use", "Sediment prefiltration before CTO, GAC, UF or RO"),
            ("OEM Options", "Label, bag, box, end cap, size and carton"),
        ],
    },
    "cto-carbon-block-filter.html": {
        "h1": "CTO Carbon Block Filter Manufacturer",
        "title": "CTO Carbon Block Filter Manufacturer | Coconut Shell OEM Supplier",
        "desc": "OEM CTO coconut shell carbon block filter cartridges for chlorine, taste and odor reduction. China factory supply with custom size, micron, label and packaging.",
        "product_ids": ["carbon-block", "carbon-block-2", "carbon-block-industrial", "flat-cap-cto"],
        "intro": "CTO carbon block filters use compressed activated carbon to reduce chlorine, unpleasant taste, odor and selected organic compounds in drinking water systems. Yuchen Water supplies coconut shell carbon block cartridges for RO systems, countertop filters, whole house housings and commercial prefiltration.",
        "applications": "The product is commonly used as a second or third stage cartridge after PP sediment filtration and before RO membrane protection. It also works as a standalone taste-and-odor cartridge in countertop purifiers and commercial water machines where compact size and repeatable flow are important.",
        "oem": "OEM/ODM choices include carbon source, iodine value, micron rating, block density, gasket, end cap, shrink wrap, label, retail box and master carton. Private-label buyers can request sampling and test documentation for selected models according to project requirements.",
        "table": [
            ("Media", "Coconut shell activated carbon block"),
            ("Micron Options", "1, 5, 10 micron"),
            ("Lengths", "10 inch, 20 inch and custom"),
            ("Function", "Chlorine, taste, odor and organic reduction"),
            ("OEM Options", "Formula, end cap, label, shrink wrap and carton"),
        ],
    },
    "gac-udf-filter-cartridge.html": {
        "h1": "GAC UDF Filter Cartridge Manufacturer",
        "title": "GAC UDF Filter Cartridge Manufacturer China | OEM Water Filter",
        "desc": "GAC and UDF activated carbon filter cartridges for RO systems, dispensers and water purifiers. OEM media, shell, label and packaging support.",
        "product_ids": ["udf-cartridge", "pre-udf", "flat-cap-gac", "filter-combo"],
        "intro": "GAC and UDF filter cartridges use granular activated carbon to improve water taste and reduce chlorine and odor in multi-stage drinking water systems. They are a flexible choice for pre-carbon and polishing stages in RO purifiers, dispensers and countertop devices.",
        "applications": "Distributors use GAC/UDF cartridges in replacement filter sets, direct drinking systems, water dispenser filter modules and commercial prefiltration. The granular bed can be configured by fill weight, carbon iodine value, shell design and end pad layout to suit flow and service-life targets.",
        "oem": "Yuchen Water supports private-label UDF cartridges with custom shell color, label, sealed bag, color box and export carton. Buyers can also specify coconut shell carbon, coal-based carbon, mesh, sponge, non-woven pad or silicon ring configurations.",
        "table": [
            ("Media", "Granular activated carbon"),
            ("Shell", "Food-grade PP"),
            ("Sizes", "10 inch, 20 inch and inline formats"),
            ("Function", "Chlorine, odor and taste reduction"),
            ("OEM Options", "Carbon grade, shell color, label and packaging"),
        ],
    },
    "t33-inline-filter.html": {
        "h1": "T33 Inline Carbon Filter Manufacturer",
        "title": "T33 Inline Carbon Filter Manufacturer | OEM Post Carbon Cartridge",
        "desc": "T33 inline carbon filters for RO post-filtration, water dispensers and direct drinking systems. OEM quick-connect fittings, media, label and cartons.",
        "product_ids": ["inline-t33-coconut", "post-t33", "t33-post", "inline-t33-mineral"],
        "intro": "T33 inline filters are compact post-carbon cartridges used after RO membranes or storage tanks to polish taste before drinking. Yuchen Water manufactures T33 inline carbon filters with coconut shell activated carbon, optional mineral media and multiple connector choices.",
        "applications": "The cartridge is suitable for under-sink RO purifiers, wall mounted dispensers, refrigerator water lines, direct drinking appliances and replacement filter kits. It helps distributors build complete filter sets with PP, CTO, GAC, RO and final polishing stages.",
        "oem": "OEM/ODM service includes body length, diameter, fitting type, cap color, media formula, filter label, flow direction mark, polybag, color box and carton design. Engineering samples can be quoted for appliance integration projects.",
        "table": [
            ("Media", "Coconut shell activated carbon"),
            ("Connection", "1/4 inch quick-connect or threaded"),
            ("Use Position", "Final post-carbon polishing"),
            ("Applications", "RO purifier, dispenser, direct drinking system"),
            ("OEM Options", "Fitting, media, label, cap and packaging"),
        ],
    },
    "ro-membrane.html": {
        "h1": "RO Membrane Element Manufacturer",
        "title": "RO Membrane Element Manufacturer China | OEM Reverse Osmosis",
        "desc": "Reverse osmosis membrane elements for residential and light commercial RO systems. OEM GPD rating, sleeve label, bag and carton options.",
        "product_ids": ["ro-membrane", "ro-membrane-400g", "built-in-pressure-tank-ro", "ro-undersink"],
        "intro": "An RO membrane element is the replaceable separation cartridge inside a reverse osmosis system. It is not the complete under-sink system; it is the membrane component that reduces dissolved solids, salts and heavy metals after proper sediment and carbon prefiltration.",
        "applications": "Yuchen Water supplies residential and light commercial RO membrane elements for system manufacturers, replacement cartridge distributors and private-label water purifier brands. Common applications include under-sink RO systems, countertop RO purifiers and commercial drinking water machines.",
        "oem": "OEM service covers GPD rating, membrane sleeve, private label, sealed bag, model code, carton, user instructions and batch traceability. Buyers can request performance data and selected test documentation according to target market requirements.",
        "table": [
            ("Membrane", "TFC polyamide RO membrane"),
            ("Capacity", "50, 75, 100, 200, 400 GPD options"),
            ("Function", "TDS, salt and heavy metal reduction"),
            ("Use", "Replacement membrane for RO systems"),
            ("OEM Options", "Sleeve, label, bag, model code and carton"),
        ],
    },
    "uf-membrane-filter.html": {
        "h1": "UF Hollow Fiber Membrane Filter Manufacturer",
        "title": "UF Membrane Filter Manufacturer | Hollow Fiber OEM Cartridge",
        "desc": "UF hollow fiber membrane filters for gravity purifiers, dispensers and kitchen systems. Custom housing, connector, flow and private label options.",
        "product_ids": ["uf-filter-2", "uf-cartridge", "ultra-film"],
        "intro": "UF membrane filters use hollow fiber membrane bundles to reduce turbidity, suspended solids, colloids and microorganisms while retaining dissolved minerals. They are often selected for low-pressure drinking water devices and systems that do not require RO wastewater discharge.",
        "applications": "Applications include gravity purifiers, wall mounted dispensers, kitchen water filters, pre-RO protection and compact household filtration systems. Buyers can specify membrane area and flow rate to match local appliance designs or replacement cartridge standards.",
        "oem": "OEM/ODM options include membrane material, housing shape, connector, cap color, label, individual bag, color box and master carton. The factory can support private-label programs and appliance integration projects.",
        "table": [
            ("Membrane", "Hollow fiber UF membrane"),
            ("Pore Class", "0.01 micron class"),
            ("Function", "Turbidity, colloid and microorganism reduction"),
            ("Operation", "Low-pressure or gravity assisted design"),
            ("OEM Options", "Housing, connector, membrane area and carton"),
        ],
    },
    "water-dispenser.html": {
        "h1": "Water Dispenser Manufacturer for OEM/ODM Buyers",
        "title": "Water Dispenser Manufacturer China | Wall Mounted OEM Supplier",
        "desc": "China water dispenser manufacturer for wall mounted, desktop and vertical models. OEM shell color, filter set, panel, badge and carton support.",
        "product_ids": ["mt-e600", "mt-b600", "mt-600dg", "mt-900g", "mt-dv-e600", "mt-s800", "mt-v-e300a"],
        "intro": "Yuchen Water supplies wall mounted, desktop and vertical water dispensers for B2B distributors, appliance brands and project buyers. Dispenser models can be paired with PP, CTO, GAC, UF or RO filtration modules depending on water quality, budget and market positioning.",
        "applications": "Typical uses include offices, schools, clinics, apartments, retail stores and public service areas. Distributors can select ambient, hot, cold or combined configurations and build recurring revenue through replacement filter sets.",
        "oem": "OEM/ODM options include shell color, front panel, control layout, tap design, filter module, brand badge, printed manual, carton artwork and spare filter kit. Sampling and pilot production are available for private-label appliance projects.",
        "table": [
            ("Models", "Wall mounted, desktop and vertical"),
            ("Filtration", "PP, CTO, GAC, UF or RO options"),
            ("Functions", "Ambient, hot or cold by model"),
            ("Applications", "Office, school, clinic, apartment and public area"),
            ("OEM Options", "Shell, panel, badge, filter set and packaging"),
        ],
    },
    "ro-water-purifier.html": {
        "h1": "RO Water Purifier Manufacturer China",
        "title": "RO Water Purifier Manufacturer China | OEM/ODM Supplier",
        "desc": "OEM/ODM RO water purifiers including built-in tank and under-sink systems. Custom stages, membrane, front panel, filters, faucet and packaging.",
        "product_ids": ["built-in-pressure-tank-ro", "ro-undersink", "ro-membrane", "inline-t33-coconut"],
        "intro": "RO water purifiers combine sediment, carbon, reverse osmosis membrane and polishing stages to deliver drinking water systems for residential and light commercial use. Yuchen Water manufactures compact RO systems and matching replacement filters for OEM/ODM buyers.",
        "applications": "The category fits under-sink kitchen systems, apartments, office pantries, appliance brand portfolios and distributor replacement programs. Buyers can choose built-in tank designs, classic under-sink layouts or customized filter combinations.",
        "oem": "OEM support includes cabinet shape, front panel, stages, filter sequence, faucet, pump, membrane GPD rating, user manual, label and carton artwork. Engineering discussion is available for new mold or local compliance projects.",
        "table": [
            ("System Types", "Built-in tank and under-sink RO"),
            ("Stages", "5-stage or 6-stage options"),
            ("Membrane", "50 to 400 GPD options by model"),
            ("Applications", "Home, apartment, office and appliance brand lines"),
            ("OEM Options", "Panel, faucet, filter set, label and carton"),
        ],
    },
    "filter-housing.html": {
        "h1": "Water Filter Housing Manufacturer",
        "title": "Water Filter Housing Manufacturer China | PP and Stainless Steel",
        "desc": "Water filter housing manufacturer for PP, Big Blue and 304/316L stainless steel housings. OEM port size, color, bracket, label and packaging.",
        "product_ids": ["ss-jumbo-housing", "big-blue-3stage", "housing-filter"],
        "intro": "Water filter housings hold sediment, carbon, UF and specialty cartridges in residential, commercial and industrial filtration systems. Yuchen Water supplies PP housings, Big Blue housings and 304/316L stainless steel housings for distributors and project buyers.",
        "applications": "Applications include whole house filtration, commercial kitchens, RO pretreatment, industrial process water, villas and replacement cartridge programs. Housing selection depends on flow, pressure, installation space, cartridge size and required material grade.",
        "oem": "OEM/ODM choices include material, port size, color, bracket, wrench, pressure gauge, label, nameplate, carton and pallet packing. Stainless steel models can be quoted with surface finish and port configuration options.",
        "table": [
            ("Materials", "PP, reinforced PP, SUS 304, SUS 316L"),
            ("Sizes", "10 inch, 20 inch, Big Blue, jumbo and custom"),
            ("Ports", "NPT/BSP options"),
            ("Applications", "Whole house, commercial and industrial filtration"),
            ("OEM Options", "Port, color, bracket, gauge, label and carton"),
        ],
    },
}


def product_lookup(products: list[dict]) -> dict[str, dict]:
    lookup = {p["id"]: p for p in products}
    for pid, detail in TARGET_PRODUCTS.items():
        if pid in lookup:
            lookup[pid].update(detail)
    for p in products:
        p.setdefault("summary", p.get("desc", ""))
        p.setdefault("features", [
            "OEM/ODM private-label support for global distributors",
            "Batch production and export packaging available",
            "Suitable for residential, commercial or light industrial water filtration",
        ])
        p.setdefault("applications", p.get("desc", ""))
        p.setdefault("related", [])
    return lookup


def product_card(p: dict) -> str:
    desc = p.get("summary") or p.get("desc", "")
    desc = re.sub(r"\s+", " ", desc).strip()
    if len(desc) > 190:
        desc = desc[:187].rsplit(" ", 1)[0] + "..."
    return f'''
<article class="product-card" data-cat="{esc(p.get('category', ''))}">
  <a href="product-{esc(p['id'])}.html" class="product-img-wrap">
    <span class="product-cat-badge">{esc(p.get('category', ''))}</span>
    <img src="{esc(p.get('image', '../assets/products/1.png'))}" alt="{esc(p['name'])} for OEM/ODM water filtration projects" loading="lazy" decoding="async" width="640" height="480" />
  </a>
  <div class="product-body">
    <h3>{esc(p['name'])}</h3>
    <p>{esc(desc)}</p>
    <a href="product-{esc(p['id'])}.html" class="product-link">Send Inquiry</a>
  </div>
</article>'''


def render_home(root_home: bool = False, products: list[dict] | None = None) -> str:
    products = products or []
    canonical = SITE + "/" if root_home else SITE + "/en/index.html"
    page = "index.html"
    preload = "assets/backgrounds/eco_hero1.webp" if root_home else "../assets/backgrounds/eco_hero1.webp"
    page_title = "Yuchen Water | China Water Filter Manufacturer & OEM/ODM Supplier" if root_home else HOME_TITLE
    page_desc = (
        "Yuchen Water is the English root homepage for a China OEM/ODM water filter "
        "manufacturer supplying PP, CTO, GAC, T33, UF, RO membrane, purifier, "
        "dispenser and housing products."
    ) if root_home else HOME_DESC
    json_extra = [
        breadcrumb_schema([("Home", canonical)]),
        faq_schema([
            ("Can Yuchen Water manufacture private-label water filters?", "Yes. We support OEM/ODM labels, packaging, cartridge sizes, filter sets and selected tooling projects for distributors and appliance brands."),
            ("Are all products NSF certified?", SAFE_CERT),
            ("What products can be supplied for a complete RO system?", "We can supply PP sediment filters, CTO carbon block, GAC/UDF, T33 inline filters, UF membranes, RO membrane elements, housings and complete RO purifier assemblies."),
        ]),
    ]
    out = head(page_title, page_desc, canonical, page, root_home=root_home, extra_json=json_extra, preload=preload)
    out += header(root_home=root_home, active="home")
    prefix = "en/" if root_home else ""
    asset = "" if root_home else "../"
    cats = [
        ("PP Melt Blown Filters", "pp-melt-blown-filter-cartridge.html", "Sediment cartridges for RO systems, dispensers and whole-house prefilters."),
        ("CTO Carbon Block", "cto-carbon-block-filter.html", "Coconut shell carbon block filters for chlorine, taste and odor reduction."),
        ("GAC / UDF Filters", "gac-udf-filter-cartridge.html", "Granular activated carbon cartridges for pre-carbon and polishing stages."),
        ("T33 Inline Filters", "t33-inline-filter.html", "Compact post-carbon filters for RO purifiers and water dispensers."),
        ("RO Membranes", "ro-membrane.html", "Replacement RO membrane elements for residential and light commercial systems."),
        ("UF Membranes", "uf-membrane-filter.html", "Hollow fiber UF cartridges for low-pressure drinking water filtration."),
        ("Water Dispensers", "water-dispenser.html", "Wall mounted, desktop and vertical dispensers with OEM options."),
        ("Filter Housings", "filter-housing.html", "PP, Big Blue and stainless steel housings for cartridge systems."),
    ]
    hot_ids = ["built-in-pressure-tank-ro", "pp-spun", "carbon-block", "udf-cartridge", "inline-t33-coconut", "ro-membrane", "uf-filter-2", "big-blue-3stage"]
    lookup = {p["id"]: p for p in products}
    out += f'''
<main>
<section class="hero seo-hero" style="min-height:56vh;background-image:linear-gradient(rgba(20,45,55,.72),rgba(20,45,55,.58)),url('{asset}assets/backgrounds/eco_hero1.webp');background-size:cover;background-position:center;">
  <div class="container hero-content">
    <div class="hero-eyebrow">China OEM/ODM Water Filtration Manufacturer</div>
    <h1>{HOME_H1}</h1>
    <p class="hero-desc">{HOME_DESC}</p>
    <div class="hero-actions">
      <a href="{prefix}contact.html" class="btn btn-gold">Request OEM Quote</a>
      <a href="https://wa.me/{WA}" target="_blank" rel="noopener" class="btn">Contact Engineer</a>
    </div>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Product Categories</span><h2>Water Filter Product Categories</h2><p>Focused OEM/ODM product families for global distributors, wholesalers and appliance brands.</p></div>
    <div class="category-grid">
      {''.join(f'<a class="category-card" href="{prefix}{href}"><h3>{esc(name)}</h3><p>{esc(desc)}</p></a>' for name, href, desc in cats)}
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="container seo-grid two-col">
    <div>
      <span class="eyebrow">OEM/ODM Manufacturing Capabilities</span>
      <h2>Private-label water filtration products from a China factory</h2>
      <p>Yuchen Water supports B2B buyers with product selection, filter-stage matching, label design, color box artwork, carton marks, spare filter sets and sampling. Programs can cover individual cartridges, complete RO systems, dispensers, filter housings and bundled replacement kits.</p>
      <p>{SAFE_CERT}</p>
      <div class="hero-actions"><a href="{prefix}contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}" class="btn" target="_blank" rel="noopener">Contact Engineer</a></div>
    </div>
    <div class="capability-list">
      <p><strong>Custom products:</strong> PP, CTO, GAC, T33, UF, RO membrane, dispenser, housing and purifier systems.</p>
      <p><strong>Custom branding:</strong> filter labels, logo printing, retail box, instruction manual and export carton.</p>
      <p><strong>Buyer support:</strong> product matching, sample preparation, batch inspection and shipment coordination.</p>
    </div>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Factory & Production Lines</span><h2>Factory and production line overview</h2><p>Dedicated production for sediment filters, carbon blocks, inline cartridges, membrane products and water dispenser assembly.</p></div>
    <div class="workshop-grid">
      <div class="workshop-card"><img src="{asset}assets/workshop/line1-optimized.jpg" alt="PP melt blown filter cartridge production line" loading="lazy" decoding="async" width="640" height="480"><div class="label"><h3>PP Melt Blown Line</h3><p>Gradient-density sediment cartridge production.</p></div></div>
      <div class="workshop-card"><img src="{asset}assets/workshop/2_carbon_block_line.jpg" alt="CTO carbon block filter production line" loading="lazy" decoding="async" width="640" height="480"><div class="label"><h3>Carbon Block Line</h3><p>Coconut shell CTO carbon block processing.</p></div></div>
      <div class="workshop-card"><img src="{asset}assets/workshop/3_quick_connect_line.png" alt="T33 inline water filter assembly line" loading="lazy" decoding="async" width="640" height="480"><div class="label"><h3>Inline Filter Assembly</h3><p>T33, mineral and quick-connect filter assembly.</p></div></div>
      <div class="workshop-card"><img src="{asset}assets/workshop/4_leak_test.png" alt="Water filter quality leakage test station" loading="lazy" decoding="async" width="640" height="480"><div class="label"><h3>Quality Control</h3><p>Leakage, flow and packaging checks before shipment.</p></div></div>
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="container seo-grid two-col">
    <div>
      <span class="eyebrow">Quality Control & Certifications</span>
      <h2>Practical compliance support for importers</h2>
      <p>For global distributors, compliance language must be precise. We avoid claiming that every SKU carries the same certificate. Instead, Yuchen Water can provide ISO 9001 quality-system documents, CE and SGS-related files, Halal-related documents, and selected NSF/ANSI 42, 53 and 58 testing or supply options depending on the product and order requirement.</p>
    </div>
    <table class="spec-table">
      <tr><th>Incoming materials</th><td>PP resin, activated carbon, membrane and housing material checks</td></tr>
      <tr><th>In-process QC</th><td>Dimension, flow, pressure drop and assembly inspection</td></tr>
      <tr><th>Final inspection</th><td>Appearance, leakage, labeling, carton and random sampling</td></tr>
      <tr><th>Documents</th><td>{SAFE_CERT}</td></tr>
    </table>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Hot Products</span><h2>Hot OEM water filtration products</h2></div>
    <div class="product-grid">{''.join(product_card(lookup[i]) for i in hot_ids if i in lookup)}</div>
  </div>
</section>

<section class="section section-cream" itemscope itemtype="https://schema.org/FAQPage">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>Common B2B buyer questions</h2></div>
    <div class="faq-wrap">
      <div class="faq-item open" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><button class="faq-q" itemprop="name">Can you make OEM/ODM water filters for our brand?</button><div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">Yes. We support private labels, cartridge dimensions, filter stages, color boxes, instruction manuals, export cartons and selected new mold projects.</p></div></div>
      <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><button class="faq-q" itemprop="name">Which products are suitable for distributors?</button><div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">Common distributor programs include PP sediment filters, CTO carbon block, GAC/UDF, T33 inline filters, RO membranes, UF filters, dispensers and filter housings.</p></div></div>
      <div class="faq-item" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><button class="faq-q" itemprop="name">What certification documents are available?</button><div class="faq-a" itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><p itemprop="text">{SAFE_CERT}</p></div></div>
    </div>
  </div>
</section>

<section class="section section-dark quote-strip">
  <div class="container">
    <h2>Request a quote for your OEM/ODM water filtration project</h2>
    <p>Send product type, quantity, target market and destination port. A sales engineer will help match filters, packaging and documentation.</p>
    <div class="hero-actions"><a href="{prefix}contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}" target="_blank" rel="noopener" class="btn">Send Inquiry</a></div>
  </div>
</section>
</main>
'''
    out += footer(root_home=root_home)
    return out


def render_category(page: str, data: dict, lookup: dict[str, dict]) -> str:
    faqs = [
        ("Can this category be supplied with private-label packaging?", "Yes. Yuchen Water supports product labels, sealed bags, color boxes, instruction sheets, master cartons and pallet marks for OEM/ODM orders."),
        ("What information is needed for a quotation?", "Please send product type, target size, specification, estimated quantity, destination port and any branding or compliance requirements."),
        ("Are certification documents available?", SAFE_CERT),
    ]
    breadcrumb = [("Home", f"{SITE}/en/index.html"), ("Products", f"{SITE}/en/products.html"), (data["h1"], f"{SITE}/en/{page}")]
    out = head(
        data["title"],
        data["desc"],
        f"{SITE}/en/{page}",
        page,
        extra_json=[breadcrumb_schema(breadcrumb), faq_schema(faqs)],
    )
    out += header(active="products")
    product_ids = [pid for pid in data["product_ids"] if pid in lookup]
    words = (
        f"{data['intro']} {data['applications']} {data['oem']} "
        "For international B2B buyers, the correct filter category should be selected by inlet water quality, target flow rate, housing size, service interval, retail price point and replacement filter strategy. Yuchen Water can help distributors compare standard cartridge dimensions, choose practical filtration stages and prepare packaging that is easier for local dealers to sell. The goal is not to over-specify every product, but to create a reliable range that can be replenished consistently, documented clearly and shipped efficiently by carton or container. "
        "Each quotation can include product photos, specification confirmation, sampling lead time, MOQ, carton quantity, gross weight, carton size, loading estimate and recommended spare parts. This makes the category suitable for importers building a catalog, appliance brands sourcing matched cartridges, and project buyers that need stable supply from a China water filtration manufacturer."
    )
    out += f'''
<main>
<section class="section section-cream page-hero">
  <div class="container">
    <nav class="breadcrumb"><a href="index.html">Home</a><span>·</span><a href="products.html">Products</a><span>·</span><span>{esc(data['h1'])}</span></nav>
    <h1>{esc(data['h1'])}</h1>
    <p class="desc">{esc(data['desc'])}</p>
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}" class="btn" target="_blank" rel="noopener">Contact Engineer</a></div>
  </div>
</section>
<section class="section section-light">
  <div class="container seo-content">
    <h2>Product Introduction</h2>
    <p>{esc(data['intro'])}</p>
    <h2>Applications</h2>
    <p>{esc(data['applications'])}</p>
    <h2>Specifications and Selection Guide</h2>
    <table class="spec-table">{''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in data['table'])}</table>
    <h2>OEM/ODM Capabilities</h2>
    <p>{esc(data['oem'])}</p>
    <p>{esc(words)}</p>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Related Products</span><h2>Products in this category</h2></div>
    <div class="product-grid">{''.join(product_card(lookup[pid]) for pid in product_ids)}</div>
  </div>
</section>
<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>{esc(data['h1'])} FAQ</h2></div>
    <div class="faq-wrap">{''.join(f'<div class="faq-item"><button class="faq-q">{esc(q)}</button><div class="faq-a"><p>{esc(a)}</p></div></div>' for q, a in faqs)}</div>
  </div>
</section>
<section class="section section-dark quote-strip"><div class="container"><h2>Request an OEM quote for {esc(data['h1'])}</h2><p>Share your target specification, quantity and destination port for a practical factory quotation.</p><div class="hero-actions"><a href="contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}" class="btn" target="_blank" rel="noopener">Send Inquiry</a></div></div></section>
</main>
'''
    out += footer()
    return out


def render_product_page(p: dict, lookup: dict[str, dict]) -> str:
    page = f"product-{p['id']}.html"
    title = f"{p['name']} | China OEM/ODM Water Filter Manufacturer"
    if len(re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?", p["summary"])) < 80:
        p["summary"] += " This page is written for B2B buyers comparing factory supply, repeat orders and private-label water filtration programs."
    desc = re.sub(r"\s+", " ", p["summary"]).strip()
    meta = desc[:155].rsplit(" ", 1)[0]
    faqs = [
        (f"Can {p['name']} be customized for OEM orders?", "Yes. Yuchen Water can quote private-label options such as label, packaging, color, connector, size or matched filter set depending on this product type."),
        ("What information should I send for a quotation?", "Please send product specification, target quantity, private-label requirements, destination port and any compliance documents required in your market."),
        ("What certification documents can be supplied?", SAFE_CERT),
    ]
    breadcrumb = [("Home", f"{SITE}/en/index.html"), ("Products", f"{SITE}/en/products.html"), (p["name"], f"{SITE}/en/{page}")]
    out = head(
        title,
        meta,
        f"{SITE}/en/{page}",
        page,
        extra_json=[breadcrumb_schema(breadcrumb), faq_schema(faqs), product_schema(p, page)],
        image="/" + p["image"].replace("../", ""),
        preload=p["image"],
    )
    out += header(active="products")
    related = [lookup[r] for r in p.get("related", []) if r in lookup]
    if not related:
        related = [x for x in lookup.values() if x["id"] != p["id"] and x.get("category") == p.get("category")][:4]
    out += f'''
<main>
<section class="section section-cream product-hero">
  <div class="container product-detail">
    <div class="product-detail-img">
      <img src="{esc(p['image'])}" alt="{esc(p['name'])} for OEM ODM water filtration supply" loading="eager" fetchpriority="high" decoding="async" width="800" height="800" class="product-main-image" />
    </div>
    <div class="product-detail-info">
      <nav class="breadcrumb"><a href="index.html">Home</a><span>·</span><a href="products.html">Products</a><span>·</span><span>{esc(p['name'])}</span></nav>
      <h1>{esc(p['name'])}</h1>
      <span class="cat-badge">{esc(p.get('category', 'Water Filter Product'))}</span>
      <p class="desc">{esc(p['summary'])}</p>
      <div class="product-actions"><a href="contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}?text={quote('Inquiry about ' + p['name'])}" class="btn" target="_blank" rel="noopener">Contact Engineer</a></div>
    </div>
  </div>
</section>
<section class="section section-light">
  <div class="container seo-grid two-col">
    <div>
      <h2>Technical Specifications</h2>
      <table class="spec-table">{''.join(f'<tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>' for k, v in p['specs'].items())}</table>
    </div>
    <div>
      <h2>Key Features</h2>
      <ul class="benefits-list">{''.join(f'<li>{esc(item)}</li>' for item in p['features'])}</ul>
    </div>
  </div>
</section>
<section class="section section-cream">
  <div class="container seo-grid three-col">
    <div><h2>Applications</h2><p>{esc(p['applications'])}</p></div>
    <div><h2>OEM/ODM Options</h2><p>Private label, product label, matched filter set, color box, master carton, user instructions and market-specific documentation can be quoted according to your order plan.</p></div>
    <div><h2>Packaging & Shipping</h2><p>Standard export cartons, inner bags, color boxes, pallet packing and FOB Shanghai or Ningbo shipping support are available. Send quantity and destination port for loading estimates.</p></div>
  </div>
</section>
<section class="section section-light">
  <div class="container">
    <div class="section-head"><span class="eyebrow">FAQ</span><h2>{esc(p['name'])} FAQ</h2></div>
    <div class="faq-wrap">{''.join(f'<div class="faq-item"><button class="faq-q">{esc(q)}</button><div class="faq-a"><p>{esc(a)}</p></div></div>' for q, a in faqs)}</div>
  </div>
</section>
<section class="section section-cream">
  <div class="container">
    <div class="section-head"><span class="eyebrow">Related Products</span><h2>Related Products</h2></div>
    <div class="product-grid">{''.join(product_card(r) for r in related[:4])}</div>
  </div>
</section>
<section class="section section-dark quote-strip"><div class="container"><h2>Request a quote for {esc(p['name'])}</h2><p>Send target specification, quantity, destination port and branding needs. A sales engineer will reply with a practical OEM/ODM quotation.</p><div class="hero-actions"><a href="contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/{WA}?text={quote('Inquiry about ' + p['name'])}" class="btn" target="_blank" rel="noopener">Send Inquiry</a></div></div></section>
</main>
'''
    out += footer()
    return out


def render_products_index(products: list[dict]) -> str:
    cats = sorted({p.get("category", "Water Filter") for p in products})
    out = head(
        "Water Filter Products | OEM PP CTO GAC RO UF Supplier",
        "Browse OEM/ODM water filtration products including PP melt blown filters, CTO carbon block, GAC, T33, UF, RO membrane, dispensers and housings.",
        f"{SITE}/en/products.html",
        "products.html",
        extra_json=[breadcrumb_schema([("Home", f"{SITE}/en/index.html"), ("Products", f"{SITE}/en/products.html")])],
    )
    out += header(active="products")
    out += '''
<main>
<section class="section section-cream page-hero">
  <div class="container">
    <nav class="breadcrumb"><a href="index.html">Home</a><span>·</span><span>Products</span></nav>
    <h1>Water Filter Products for OEM/ODM Buyers</h1>
    <p class="desc">Explore China factory supply for PP melt blown filters, CTO carbon block, GAC/UDF, T33 inline filters, UF membrane, RO membrane, water purifiers, water dispensers and filter housings.</p>
    <div class="hero-actions"><a href="contact.html" class="btn btn-gold">Request OEM Quote</a><a href="https://wa.me/''' + WA + '''" class="btn" target="_blank" rel="noopener">Contact Engineer</a></div>
  </div>
</section>
<section class="section section-light"><div class="container"><div class="section-head"><span class="eyebrow">Categories</span><h2>SEO product category pages</h2></div><div class="category-grid">
'''
    for page, data in CATEGORY_PAGES.items():
        out += f'<a class="category-card" href="{page}"><h3>{esc(data["h1"])}</h3><p>{esc(data["desc"])}</p></a>'
    out += '</div></div></section><section class="section section-cream"><div class="container"><div class="cat-filter">'
    out += '<button class="cat-btn active" onclick="filterCat(\'all\', this)" type="button">All Categories</button>'
    for cat in cats:
        out += f'<button class="cat-btn" onclick="filterCat({json.dumps(cat)}, this)" type="button">{esc(cat)}</button>'
    out += f'</div><div class="product-grid">{"".join(product_card(p) for p in products)}</div></div></section></main>'
    out += footer()
    return out


def render_contact() -> str:
    out = head(
        "Contact Yuchen Water | Request OEM Quote for Water Filters",
        "Send an OEM/ODM water filter inquiry with product, quantity, WhatsApp, country and destination port. Yuchen Water sales engineers reply to global B2B buyers.",
        f"{SITE}/en/contact.html",
        "contact.html",
        extra_json=[breadcrumb_schema([("Home", f"{SITE}/en/index.html"), ("Contact", f"{SITE}/en/contact.html")])],
    )
    out += header(active="contact")
    out += f'''
<main>
<section class="section section-cream page-hero">
  <div class="container">
    <nav class="breadcrumb"><a href="index.html">Home</a><span>·</span><span>Contact</span></nav>
    <h1>Request OEM Quote</h1>
    <p class="desc">Send product type, quantity, destination port and private-label requirements. A sales engineer will help confirm specification, packaging and shipping details.</p>
  </div>
</section>
<section class="section section-light">
  <div class="container contact-grid">
    <div class="contact-info">
      <h2>Contact Engineer</h2>
      <p><strong>Phone:</strong> <a href="tel:{PHONE}">{PHONE}</a></p>
      <p><strong>WhatsApp:</strong> <a href="https://wa.me/{WA}" target="_blank" rel="noopener">{PHONE}</a></p>
      <p><strong>Email:</strong> <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p><strong>Factory:</strong> {ADDRESS}</p>
      <p>{SAFE_CERT}</p>
    </div>
    <form class="contact-form" id="quoteForm" action="mailto:{EMAIL}" method="post" enctype="text/plain">
      <h2>Send Inquiry</h2>
      <div class="form-row"><label for="name">Name</label><input id="name" name="Name" type="text" required></div>
      <div class="form-row"><label for="company">Company</label><input id="company" name="Company" type="text" required></div>
      <div class="form-row"><label for="email">Email</label><input id="email" name="Email" type="email" required></div>
      <div class="form-row"><label for="whatsapp">WhatsApp</label><input id="whatsapp" name="WhatsApp" type="text"></div>
      <div class="form-row"><label for="country">Country</label><input id="country" name="Country" type="text" required></div>
      <div class="form-row"><label for="product">Product</label><input id="product" name="Product" type="text" required></div>
      <div class="form-row"><label for="quantity">Quantity</label><input id="quantity" name="Quantity" type="text" required></div>
      <div class="form-row"><label for="port">Destination Port</label><input id="port" name="Destination Port" type="text"></div>
      <div class="form-row"><label for="message">Message</label><textarea id="message" name="Message" rows="6" required></textarea></div>
      <button type="submit" class="btn btn-gold">Send Inquiry</button>
      <p id="formSuccess" class="form-success" hidden>Thank you. Your inquiry is ready to send, and our engineer will reply as soon as possible.</p>
    </form>
  </div>
</section>
</main>
'''
    out += footer()
    return out


def replace_hreflang_and_canonical(path: Path) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    rel = path.relative_to(ROOT).as_posix()
    parts = rel.split("/")
    if len(parts) < 2 or parts[0] not in CORE_LANGS + NON_CORE_LANGS or not rel.endswith(".html"):
        return
    lang = parts[0]
    page = "/".join(parts[1:])
    canonical = f"{SITE}/{lang}/{page}"
    text = re.sub(r'<link rel="canonical" href="[^"]+"\s*/>', f'<link rel="canonical" href="{canonical}" />', text)
    alt_block = "\n".join(
        f'  <link rel="alternate" hreflang="{l}" href="{SITE}/{l}/{page}" />'
        for l in CORE_LANGS
        if (ROOT / l / page).exists()
    )
    default_page = page if (ROOT / "en" / page).exists() else "index.html"
    alt_block += f'\n  <link rel="alternate" hreflang="x-default" href="{SITE}/en/{default_page}" />'
    text = re.sub(r'(?:\s*<link rel="alternate" hreflang="[^"]+" href="[^"]+"\s*/>)+', "\n" + alt_block, text, count=1)
    robots = "index, follow" if lang in CORE_LANGS else "noindex, follow"
    if '<meta name="robots"' in text:
        text = re.sub(r'<meta name="robots" content="[^"]+"\s*/>', f'<meta name="robots" content="{robots}" />', text)
    else:
        text = text.replace("</head>", f'  <meta name="robots" content="{robots}" />\n</head>', 1)
    write(path, text)


def safe_cert_replacements() -> None:
    replacements = {
        "All our products are certified by NSF International, ISO 9001:2015, CE (European Conformity), SGS, FDA, and Halal (JAKIM). Selected products also have 3C and additional regional certifications.": SAFE_CERT,
        "All Express Water products are certified by NSF International, ISO 9001:2015, CE (European Conformity), SGS, FDA, and Halal (JAKIM). Selected products also have 3C and regional certifications.": SAFE_CERT,
        "NSF, ISO 9001:2015, CE, SGS, FDA &amp; Halal compliant.": SAFE_CERT,
        "NSF/ISO certified for industrial and commercial water treatment.": "Manufactured under ISO-managed processes, with selected NSF/ANSI test options available for qualified orders.",
        "NSF Certified": "NSF/ANSI Test Options",
        "full NSF, ISO 9001, CE and SGS certification": "ISO 9001, CE, SGS and selected NSF/ANSI documentation",
        "NSF · ISO 9001:2015 · CE · SGS · 3C · Halal Certified": "NSF/ANSI options · ISO 9001 · CE · SGS · Halal documents on request",
        "NSF International Certification": "NSF/ANSI 42, 53 and 58 testing available for selected products",
        "FDA Compliance": "Food-contact material declarations available on request",
        "Halal JAKIM Certification": "Halal-related documents available on request",
    }
    for path in ROOT.rglob("*.html"):
        if any(part.startswith(".") for part in path.relative_to(ROOT).parts):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = re.sub(
            r"NSF/ISO certified(?: for)?(?: [^.<\"\n]+)?(?:\.\.\.|\.)?",
            "Selected NSF/ANSI test options and ISO/CE/SGS documents are available on request.",
            text,
        )
        text = text.replace("WhatsApp Us", "Contact Engineer")
        text = text.replace("Request a Quote", "Request OEM Quote")
        text = text.replace("Inquire Now", "Send Inquiry")
        if text != original:
            write(path, text)


def generate_sitemap() -> None:
    pages = sorted((ROOT / "en").glob("*.html"))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">',
        "  <url>",
        f"    <loc>{SITE}/</loc>",
        f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}/en/index.html"/>',
        f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}/en/index.html"/>',
        "    <lastmod>2026-05-31</lastmod>",
        "    <changefreq>weekly</changefreq>",
        "    <priority>1.0</priority>",
        "  </url>",
    ]
    for page in pages:
        name = page.name
        if name == "index.html":
            loc = f"{SITE}/en/index.html"
            priority = "0.9"
        elif name.startswith("product-"):
            loc = f"{SITE}/en/{name}"
            priority = "0.7"
        elif name in CATEGORY_PAGES:
            loc = f"{SITE}/en/{name}"
            priority = "0.8"
        else:
            loc = f"{SITE}/en/{name}"
            priority = "0.6"
        lines.extend([
            "  <url>",
            f"    <loc>{loc}</loc>",
            f'    <xhtml:link rel="alternate" hreflang="en" href="{loc}"/>',
            f'    <xhtml:link rel="alternate" hreflang="x-default" href="{loc}"/>',
            "    <lastmod>2026-05-31</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ])
    lines.append("</urlset>")
    write(ROOT / "sitemap.xml", "\n".join(lines) + "\n")


def generate_robots() -> None:
    write(
        ROOT / "robots.txt",
        "\n".join([
            "# Yuchen Water robots.txt",
            "User-agent: *",
            "Allow: /",
            "Disallow: /thank-you.html",
            "",
            "# Non-core language pages are controlled by page-level noindex tags.",
            f"Sitemap: {SITE}/sitemap.xml",
            "",
        ]),
    )


def patch_htaccess() -> None:
    path = ROOT / ".htaccess"
    text = path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""
    additions = """

# SEO root handling and modern image MIME types
<IfModule mod_rewrite.c>
    RewriteEngine On
    RewriteRule ^$ /en/ [R=301,L]
</IfModule>

<IfModule mod_mime.c>
    AddType image/webp .webp
</IfModule>
"""
    if "RewriteRule ^$ /en/ [R=301,L]" not in text:
        text += additions
    text = text.replace("expresswater\\.cn", "yuchensy\\.com")
    write(path, text)


def patch_support_files() -> None:
    # Keep generator constants aligned with the public SEO decision.
    templates = ROOT / "scripts" / "templates.py"
    if templates.exists():
        text = templates.read_text(encoding="utf-8", errors="ignore")
        text = re.sub(r"LANGS = \[[^\]]+\]", f"LANGS = {CORE_LANGS!r}", text, count=1)
        text = text.replace("NSF, ISO 9001:2015, CE, SGS, FDA & Halal compliant.", SAFE_CERT)
        write(templates, text)

    site_js = ROOT / "assets" / "site.js"
    text = site_js.read_text(encoding="utf-8", errors="ignore")
    if "quoteForm" not in text:
        text += """

document.addEventListener('submit', function(e) {
    const form = e.target;
    if (!form || form.id !== 'quoteForm') return;
    const success = document.getElementById('formSuccess');
    if (success) {
        success.hidden = false;
        success.setAttribute('role', 'status');
    }
});
"""
    write(site_js, text)


def patch_language_pages() -> None:
    for lang in CORE_LANGS + NON_CORE_LANGS:
        lang_dir = ROOT / lang
        if not lang_dir.exists():
            continue
        for path in lang_dir.glob("*.html"):
            replace_hreflang_and_canonical(path)


def main() -> None:
    data = read_json(ROOT / "scripts" / "products.json")
    products = data["products"]
    image_mapping = convert_primary_images(products)
    lookup = product_lookup(products)

    # Persist the product image cleanup for future generated output.
    write(ROOT / "scripts" / "products.json", json.dumps(data, indent=2, ensure_ascii=False) + "\n")

    # Replace old primary image references in existing HTML and JSON-like pages.
    for path in list(ROOT.rglob("*.html")) + [ROOT / "scripts" / "products.json"]:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        original = text
        for old, new in image_mapping.items():
            text = text.replace(old, new)
        if text != original:
            write(path, text)

    # Generate high-priority English pages.
    write(ROOT / "index.html", render_home(root_home=True, products=products))
    write(ROOT / "en" / "index.html", render_home(root_home=False, products=products))
    write(ROOT / "en" / "products.html", render_products_index(products))
    write(ROOT / "en" / "contact.html", render_contact())

    for page, cat_data in CATEGORY_PAGES.items():
        write(ROOT / "en" / page, render_category(page, cat_data, lookup))

    for p in products:
        # Render all English product detail pages so product cards and images are consistent.
        write(ROOT / "en" / f"product-{p['id']}.html", render_product_page(p, lookup))

    safe_cert_replacements()
    patch_language_pages()
    patch_support_files()
    patch_htaccess()
    generate_sitemap()
    generate_robots()

    print("SEO B2B OEM patch complete")
    print(f"Generated/updated {len(products)} English product pages")
    print(f"Generated {len(CATEGORY_PAGES)} category pages")
    print(f"Created {len({v for v in image_mapping.values() if v.endswith('.webp')})} WebP image references")


if __name__ == "__main__":
    main()
