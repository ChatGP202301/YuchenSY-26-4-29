from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = "https://www.yuchensy.com"
TODAY = date.today().isoformat()


ORG = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "Organization",
            "@id": f"{SITE}/#organization",
            "name": "Yuchen Water",
            "legalName": "Yuchen Water",
            "alternateName": ["Yuchen Water", "Yuchen Water China", "雨晨三溢"],
            "url": f"{SITE}/",
            "logo": f"{SITE}/assets/logo.png",
            "address": {
                "@type": "PostalAddress",
                "streetAddress": "Yuanhua Town",
                "addressLocality": "Haining City",
                "addressRegion": "Zhejiang Province",
                "addressCountry": "CN",
            },
            "telephone": "+86-19908311885",
            "email": "expresswater025@gmail.com",
            "industry": "Water filtration products manufacturer",
            "description": (
                "Yuchen Water is a China water filtration products manufacturer supplying "
                "PP melt blown filters, CTO carbon block filters, GAC filters, T33 inline "
                "filters, UF membranes, RO membranes, water purifiers, water dispensers, "
                "filter housings and OEM/ODM water treatment equipment for global B2B buyers."
            ),
            "knowsAbout": [
                "PP melt blown filter cartridge manufacturing",
                "CTO carbon block filter manufacturing",
                "GAC and UDF filter cartridges",
                "T33 inline post carbon filters",
                "RO membrane elements",
                "UF hollow fiber filters",
                "residential RO water purifier OEM",
                "commercial RO water purification equipment",
                "industrial reverse osmosis systems",
                "seawater desalination equipment",
                "water dispenser OEM manufacturing",
                "filter housing supply",
            ],
            "contactPoint": {
                "@type": "ContactPoint",
                "telephone": "+86-19908311885",
                "email": "expresswater025@gmail.com",
                "contactType": "sales engineering",
                "areaServed": "Worldwide",
            },
        },
        {
            "@type": "WebSite",
            "@id": f"{SITE}/#website",
            "name": "Yuchen Water",
            "url": f"{SITE}/",
            "publisher": {"@id": f"{SITE}/#organization"},
        },
    ],
}


GUIDE_HTML = """<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Water Filter OEM Buyer Guide | RO, PP, CTO and GAC Selection</title>
  <meta name="description" content="A practical B2B buyer guide from Yuchen Water covering OEM water filter selection, PP, CTO, GAC, T33, UF, RO membrane, commercial RO systems and supplier qualification." />
  <meta name="robots" content="index, follow" />
  <meta name="author" content="Yuchen Water" />
  <meta name="copyright" content="© 2026 Yuchen Water. All rights reserved." />
  <link rel="canonical" href="https://www.yuchensy.com/en/water-filter-oem-buyer-guide.html" />
  <link rel="stylesheet" href="../assets/styles.min.css?v=20260612-mobile-lang-polished" />
  <meta property="og:type" content="article" />
  <meta property="og:title" content="Water Filter OEM Buyer Guide | Yuchen Water" />
  <meta property="og:description" content="How B2B buyers select OEM water filtration products, supplier capability, quality documents and export packaging." />
  <meta property="og:url" content="https://www.yuchensy.com/en/water-filter-oem-buyer-guide.html" />
  <meta property="og:image" content="https://www.yuchensy.com/assets/backgrounds/eco_hero1.webp" />
  <meta name="twitter:card" content="summary_large_image" />
  <script type="application/ld+json">__SCHEMA__</script>
</head>
<body class="ltr">
<div class="topbar">
  <div class="container topbar-row">
    <div class="topbar-left">+86-19908311885 &middot; expresswater025@gmail.com</div>
    <div class="topbar-right">Global OEM/ODM water filtration supplier</div>
  </div>
</div>
<header class="header">
  <div class="container header-row">
    <a href="index.html" class="brand">
      <img src="../assets/logo.png" alt="Yuchen Sanyi logo" class="logo-img" width="173" height="64" decoding="async" />
      <span class="brand-name">Yuchen Water</span>
    </a>
    <nav class="nav">
      <a href="index.html" class="nav-link">Home</a>
      <a href="about.html" class="nav-link">About</a>
      <a href="products.html" class="nav-link">Products</a>
      <a href="workshop.html" class="nav-link">Workshop</a>
      <a href="faq.html" class="nav-link">FAQ</a>
      <a href="contact.html" class="nav-link">Contact</a>
    </nav>
    <div class="header-actions">
      <a class="btn btn-primary btn-small" href="contact.html">Request OEM Quote</a>
      <button class="mobile-menu-toggle" type="button" aria-label="Open menu">☰</button>
    </div>
  </div>
</header>
<main>
  <section class="hero">
    <div class="container hero-inner">
      <div class="hero-copy">
        <span class="eyebrow">Buyer Guide</span>
        <h1>Water Filter OEM Buyer Guide for Importers and Distributors</h1>
        <p class="hero-desc">This guide helps B2B buyers compare filter cartridges, RO water purifiers, commercial reverse osmosis systems and supplier qualification points before placing OEM or ODM orders with a China water filtration manufacturer.</p>
        <div class="hero-actions">
          <a class="btn btn-primary" href="contact.html">Request OEM Quote</a>
          <a class="btn btn-secondary" href="products.html">View Products</a>
        </div>
      </div>
    </div>
  </section>
  <section class="section">
    <div class="container prose">
      <h2>How to Define the Product Scope</h2>
      <p>For private-label water filtration projects, buyers should start with the target application, water source and replacement cycle. A PP melt blown filter cartridge is normally selected for sediment removal, while CTO carbon block and GAC filters are used for chlorine, taste and odor reduction. T33 inline carbon filters are common as the final taste-polishing stage in RO water purifier programs.</p>
      <p>Residential and light-commercial RO water purifier projects usually require capacity selection, filter-stage matching, housing size, label artwork, carton design and spare filter kits. Industrial reverse osmosis equipment should be defined by feed water quality, pretreatment design, membrane configuration, operating pressure, automation level and expected permeate flow.</p>
      <h2>Supplier Qualification Checklist</h2>
      <p>A reliable OEM water filtration supplier should provide clear specifications, production capability, batch inspection process and export packaging support. Buyers can ask for material declarations, applicable test reports, factory photos, sample approval records and shipping carton information before confirming a purchase order.</p>
      <p>Certification wording should be checked carefully. Selected products can be supplied or tested according to NSF/ANSI 42, 53 and 58 requirements. ISO 9001, CE, SGS and Halal-related documents are available upon request where applicable, but buyers should confirm which document applies to the exact product and market.</p>
      <h2>Technical Details Buyers Should Compare</h2>
      <p>For cartridges, compare size, micron rating, filter media, end cap type, gasket material, flow rate, service life and packaging method. For RO systems, compare membrane model, pump selection, pressure switch, solenoid valve, controller, voltage, tank option, filter replacement design and after-sales spare parts list.</p>
      <p>For commercial RO and industrial RO systems, key items include pretreatment tanks, sand filter, activated carbon filter, softening tank, precision filter, high-pressure pump, membrane housing, conductivity meter, automatic control valve, CIP cleaning option and electrical protection. The correct configuration depends on raw water, site conditions and local maintenance capability.</p>
      <h2>OEM/ODM and Export Packaging</h2>
      <p>Yuchen Water supports OEM labels, custom colors, logo printing, filter label design, carton artwork, user manuals, private-label packaging and project-specific configuration. For export orders, buyers should confirm carton size, pallet loading, wooden crate requirement, destination port and document support before production starts.</p>
      <div class="cta-band">
        <h2>Need help selecting a water filtration product?</h2>
        <p>Send the target product, quantity, destination country and customization requirements. Our engineering team will help match a practical OEM/ODM configuration.</p>
        <a class="btn btn-primary" href="contact.html">Send Inquiry</a>
      </div>
    </div>
  </section>
</main>
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-col">
      <div class="footer-brand"><img src="../assets/logo.png" alt="Yuchen Sanyi logo" class="footer-logo" width="173" height="64" loading="lazy" decoding="async" /><strong>Yuchen Water</strong></div>
      <p>China manufacturer of PP, CTO, GAC, T33, UF, RO membrane, RO Water Machine, water dispenser and filter housing products for OEM/ODM buyers.</p>
    </div>
    <div class="footer-col">
      <h4>Company</h4>
      <p>Yuanhua Town, Haining City, Zhejiang Province, China</p>
      <p><a href="tel:+86-19908311885">+86-19908311885</a></p>
      <p><a href="mailto:expresswater025@gmail.com">expresswater025@gmail.com</a></p>
      <p><a href="https://wa.me/8619908311885" target="_blank" rel="noopener">WhatsApp</a></p>
    </div>
  </div>
  <div class="footer-bottom"><div class="container">Yuchen Water &middot; ISO 9001, CE, SGS and selected NSF/ANSI test documents available upon request. · <a href="privacy-policy.html">Privacy Policy</a></div></div>
</footer>
<script src="../assets/site.min.js?v=20260612-mobile-lang-polished" defer></script>
</body>
</html>
"""


def is_site_file(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    return not (rel.parts and rel.parts[0].startswith("YUCHENSY-GITHUB-PAGES-upload-ready"))


def page_url(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{SITE}/"
    return f"{SITE}/{rel}"


def has_schema(text: str, schema_type: str) -> bool:
    escaped = re.escape(schema_type)
    pattern = rf'"@type"\s*:\s*(?:"{escaped}"|\[[^\]]*"{escaped}"[^\]]*\])'
    return re.search(pattern, text) is not None


def compact_json(data: dict) -> str:
    return json.dumps(data, ensure_ascii=False, separators=(",", ":"))


def support_schema_for(path: Path) -> str:
    schema = json.loads(json.dumps(ORG))
    rel = path.relative_to(ROOT)
    schema["@graph"][1]["inLanguage"] = rel.parts[0] if len(rel.parts) > 1 else "en"
    schema["@graph"].append(
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                {"@type": "ListItem", "position": 2, "name": path.stem.replace("-", " ").title(), "item": page_url(path)},
            ],
        }
    )
    return compact_json(schema)


def clean_and_patch_html() -> tuple[int, int, int]:
    changed = 0
    schema_added = 0
    keywords_removed = 0
    for path in ROOT.rglob("*.html"):
        if not is_site_file(path):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        new = text

        for old in [
            "Eco Express Water Equipment Co., Ltd.",
            "Eco Express Water Co., Ltd.",
            "Eco Express Water",
            "Express Water",
        ]:
            new = new.replace(old, "Yuchen Water")

        before_keywords = new
        new = re.sub(r"\n?\s*<meta\s+name=[\"']keywords[\"'][^>]*>\s*", "\n", new, flags=re.I)
        if new != before_keywords:
            keywords_removed += 1

        if re.search(r"<meta\s+name=[\"']author[\"']", new, flags=re.I):
            new = re.sub(
                r"<meta\s+name=[\"']author[\"'][^>]*>",
                '<meta name="author" content="Yuchen Water" />',
                new,
                count=1,
                flags=re.I,
            )
        elif "<head" in new.lower():
            new = re.sub(r"(<head[^>]*>)", r'\1\n  <meta name="author" content="Yuchen Water" />', new, count=1, flags=re.I)

        if re.search(r"<meta\s+name=[\"']copyright[\"']", new, flags=re.I):
            new = re.sub(
                r"<meta\s+name=[\"']copyright[\"'][^>]*>",
                '<meta name="copyright" content="© 2026 Yuchen Water. All rights reserved." />',
                new,
                count=1,
                flags=re.I,
            )

        needs_org = not has_schema(new, "Organization")
        needs_web = not has_schema(new, "WebSite")
        if (needs_org or needs_web) and re.search(r"</head>", new, flags=re.I):
            schema = f'  <script type="application/ld+json">{support_schema_for(path)}</script>\n'
            new = re.sub(r"</head>", schema + "</head>", new, count=1, flags=re.I)
            schema_added += 1

        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1

    return changed, schema_added, keywords_removed


def write_buyer_guide() -> None:
    article_schema = json.loads(json.dumps(ORG))
    article_schema["@graph"].extend(
        [
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "Home", "item": f"{SITE}/"},
                    {
                        "@type": "ListItem",
                        "position": 2,
                        "name": "Water Filter OEM Buyer Guide",
                        "item": f"{SITE}/en/water-filter-oem-buyer-guide.html",
                    },
                ],
            },
            {
                "@type": "Article",
                "@id": f"{SITE}/en/water-filter-oem-buyer-guide.html#article",
                "headline": "Water Filter OEM Buyer Guide for Importers and Distributors",
                "description": "A practical B2B guide for choosing OEM water filtration products, supplier capability and export packaging.",
                "author": {"@id": f"{SITE}/#organization"},
                "publisher": {"@id": f"{SITE}/#organization"},
                "datePublished": TODAY,
                "dateModified": TODAY,
                "mainEntityOfPage": f"{SITE}/en/water-filter-oem-buyer-guide.html",
            },
            {
                "@type": "FAQPage",
                "mainEntity": [
                    {
                        "@type": "Question",
                        "name": "What should buyers confirm before ordering OEM water filter cartridges?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Confirm the application, cartridge size, micron rating, filter media, service life, label artwork, packaging and destination market requirements.",
                        },
                    },
                    {
                        "@type": "Question",
                        "name": "How should buyers evaluate a China RO water purifier supplier?",
                        "acceptedAnswer": {
                            "@type": "Answer",
                            "text": "Check production capability, specification clarity, sample approval, quality inspection, export packaging and applicable product documents.",
                        },
                    },
                ],
            },
        ]
    )
    html_text = GUIDE_HTML.replace("__SCHEMA__", html.escape(compact_json(article_schema), quote=False))
    (ROOT / "en" / "water-filter-oem-buyer-guide.html").write_text(html_text, encoding="utf-8")


def add_url_to_sitemap() -> bool:
    sitemap = ROOT / "sitemap.xml"
    text = sitemap.read_text(encoding="utf-8")
    loc = f"{SITE}/en/water-filter-oem-buyer-guide.html"
    if loc in text:
        return False
    entry = f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{TODAY}</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.7</priority>
  </url>
"""
    text = text.replace("</urlset>", entry + "</urlset>")
    sitemap.write_text(text, encoding="utf-8")
    return True


def add_url_to_llms() -> bool:
    path = ROOT / "llms.txt"
    text = path.read_text(encoding="utf-8")
    line = f"- Water Filter OEM Buyer Guide: {SITE}/en/water-filter-oem-buyer-guide.html"
    if line in text:
        return False
    marker = "## Important URLs\n"
    text = text.replace(marker, marker + "\n" + line + "\n", 1)
    path.write_text(text, encoding="utf-8")
    return True


def main() -> None:
    changed, schema_added, keywords_removed = clean_and_patch_html()
    write_buyer_guide()
    sitemap_added = add_url_to_sitemap()
    llms_added = add_url_to_llms()
    print(
        json.dumps(
            {
                "html_changed": changed,
                "schema_added": schema_added,
                "meta_keywords_removed": keywords_removed,
                "buyer_guide": "en/water-filter-oem-buyer-guide.html",
                "sitemap_added": sitemap_added,
                "llms_added": llms_added,
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
