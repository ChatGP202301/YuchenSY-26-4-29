#!/usr/bin/env python3
"""
Render the entire Express Water multi-language website:
  /{lang}/index.html
  /{lang}/about.html
  /{lang}/products.html
  /{lang}/workshop.html
  /{lang}/faq.html
  /{lang}/contact.html
  /{lang}/product-{id}.html  (one per product)

Plus root: /index.html (redirect), /sitemap.xml, /robots.txt
"""
import json, os, sys, html, glob, shutil

ROOT = "/Users/jet/.accio/accounts/1661502182/agents/DID-F456DA-2B0D4C/project"
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from templates import (
    LANGS, LANG_LABELS, RTL_LANGS, GEO, head, topbar_html,
    navbar_html, footer_html
)

I18N_DIR = os.path.join(ROOT, "assets/i18n")
FAQ_DIR = os.path.join(ROOT, "scripts/faq_i18n")

UI_DEFAULTS = {
    "topbar_phone": "📞 +86-19908311885",
    "topbar_email": "✉ expresswater025@gmail.com",
    "topbar_tag": "Global Bulk Wholesale · OEM/ODM Specialist · Since 1998",
    "nav_home": "Home", "nav_about": "About Us", "nav_products": "Products",
    "nav_workshop": "Workshop", "nav_faq": "FAQ", "nav_contact": "Contact",
    "cta_whatsapp": "WhatsApp Us", "cta_request_quote": "Request a Quote",
    "cta_view_catalog": "View Product Catalog", "cta_view_details": "View Details",
    "cta_inquire_now": "Inquire Now", "cta_send_message": "Send Inquiry",
    "hero_eyebrow": "Trusted Global Manufacturer · Since 1998",
    "hero_title": "Industrial Water Filtration Solutions for Global Distributors",
    "hero_desc": "Express Water is a leading China-based manufacturer of NSF-certified water filtration products — RO membranes, PP melt-blown filters, CTO carbon blocks, UF membranes, T33 post-carbon and OEM/ODM water dispensers. We supply 50+ countries with bulk wholesale, halal certification, and full ISO 9001:2015 quality assurance.",
    "stats_years": "Years of Excellence", "stats_products": "Product SKUs",
    "stats_countries": "Countries Served", "stats_factory_m2": "m² Factory Area",
    "section_products_eyebrow": "Premium Product Line",
    "section_products_title": "Industrial Water Filtration Products",
    "section_products_desc": "Complete OEM/ODM range covering filter cartridges, RO membranes, dispensers, housings and full water purification systems for residential, commercial and industrial applications.",
    "section_workshop_eyebrow": "State-of-the-Art Manufacturing",
    "section_workshop_title": "Our Production Lines",
    "section_workshop_desc": "20,000+ m² ISO 9001 certified facility in Haining, Zhejiang — dedicated lines for PP melt-blown, sintered carbon block, UF/RO membrane assembly and dispenser SMT.",
    "section_about_eyebrow": "About Express Water",
    "section_about_title": "OEM/ODM Water Filtration Excellence",
    "section_about_desc": "Founded in 1998, Express Water has grown into one of China's most trusted water purification manufacturers, exporting to 50+ countries with full NSF, ISO 9001, CE and SGS certification.",
    "section_faq_eyebrow": "Knowledge Base",
    "section_faq_title": "Frequently Asked Questions",
    "section_contact_eyebrow": "Get In Touch",
    "section_contact_title": "Request a Quote · Bulk OEM Inquiry",
    "feat_oem": "OEM/ODM Specialist",
    "feat_oem_desc": "Custom branding, tooling, packaging — MOQ from 1,000 pcs.",
    "feat_certified": "Certified Quality",
    "feat_certified_desc": "NSF, ISO 9001:2015, CE, SGS, FDA & Halal compliant.",
    "feat_global": "Global Logistics",
    "feat_global_desc": "FOB Shanghai/Ningbo · CIF · DDP — 50+ countries shipped.",
    "feat_support": "24/7 B2B Support",
    "feat_support_desc": "WhatsApp + email engineering support in 5+ languages.",
    "form_name": "Full Name", "form_company": "Company Name", "form_email": "Email Address",
    "form_country": "Country", "form_phone": "Phone / WhatsApp", "form_message": "Your Inquiry — please specify product, quantity, destination",
    "contact_addr_label": "Factory Address", "contact_phone_label": "Phone",
    "contact_email_label": "Email", "contact_wa_label": "WhatsApp Sales",
    "contact_hours_label": "Business Hours",
    "contact_hours": "Mon–Sat 08:30 – 18:00 (China Standard Time, GMT+8)",
    "products_filter_all": "All Categories",
    "products_breadcrumb": "Products",
    "spec_table_title": "Technical Specifications",
    "features_title": "Key Features",
    "related_products": "Related Products",
    "back_to_products": "← Back to All Products",
    "footer_brand_desc": "Leading China manufacturer of industrial water filtration products since 1998. NSF, ISO 9001 and SGS certified factory specializing in OEM/ODM solutions for global wholesale distributors.",
    "footer_company": "Company", "footer_products": "Products", "footer_contact": "Contact",
    "footer_rights": "All Rights Reserved",
}

# ---------- Load all language data ----------
print("Loading i18n data...")
LANG_DATA = {}
for lang in LANGS:
    fp = os.path.join(I18N_DIR, f"{lang}.json")
    if os.path.exists(fp):
        with open(fp, encoding="utf-8") as f:
            LANG_DATA[lang] = json.load(f)
    else:
        # Fallback to English
        with open(os.path.join(I18N_DIR, "en.json"), encoding="utf-8") as f:
            LANG_DATA[lang] = json.load(f)
        print(f"  ! {lang}.json missing, using en fallback")

FAQ_DATA = {}
for lang in LANGS:
    fp = os.path.join(FAQ_DIR, f"{lang}.json")
    if os.path.exists(fp):
        with open(fp, encoding="utf-8") as f:
            FAQ_DATA[lang] = json.load(f)
    else:
        with open(os.path.join(FAQ_DIR, "en.json"), encoding="utf-8") as f:
            FAQ_DATA[lang] = json.load(f)


def get_t(lang):
    """Build text dict with UI defaults + lang-specific overrides."""
    d = LANG_DATA[lang]
    ui = d.get("ui", {})
    t = dict(UI_DEFAULTS)
    t.update(ui)
    return t


def get_products(lang):
    return LANG_DATA[lang].get("products", [])


def get_categories(lang):
    return LANG_DATA[lang].get("categories", {})


def esc(s):
    return html.escape(str(s)) if s else ""


# ============================================================
# PAGE: Home
# ============================================================
def render_home(lang):
    t = get_t(lang)
    products = get_products(lang)
    title = f"Express Water | {t['hero_title']} - OEM Manufacturer Since 1998"
    desc = t['hero_desc'][:155]
    body = head(title, desc, lang, "index.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "index.html")

    # Hero
    body += f'''
<section class="hero">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['hero_eyebrow'])}</div>
    <h1>{esc(t['hero_title'])}</h1>
    <p class="hero-desc">{esc(t['hero_desc'])}</p>
    <div class="hero-actions">
      <a href="products.html" class="btn btn-gold">{esc(t['cta_view_catalog'])}</a>
      <a href="https://wa.me/{GEO['wa']}" target="_blank" class="btn btn-outline">📱 {esc(t['cta_whatsapp'])}</a>
    </div>
  </div>
</section>

<section class="stats">
  <div class="container">
    <div class="stats-grid">
      <div><div class="stat-num">27+</div><div class="stat-label">{esc(t['stats_years'])}</div></div>
      <div><div class="stat-num">200+</div><div class="stat-label">{esc(t['stats_products'])}</div></div>
      <div><div class="stat-num">50+</div><div class="stat-label">{esc(t['stats_countries'])}</div></div>
      <div><div class="stat-num">20,000</div><div class="stat-label">{esc(t['stats_factory_m2'])}</div></div>
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">{esc(t['section_about_eyebrow'])}</div>
      <h2>{esc(t['section_about_title'])}</h2>
      <p>{esc(t['section_about_desc'])}</p>
    </div>
    <div class="feat-grid">
      <div class="feat-card"><div class="icon">🏆</div><h3>{esc(t['feat_oem'])}</h3><p>{esc(t['feat_oem_desc'])}</p></div>
      <div class="feat-card"><div class="icon">✅</div><h3>{esc(t['feat_certified'])}</h3><p>{esc(t['feat_certified_desc'])}</p></div>
      <div class="feat-card"><div class="icon">🌍</div><h3>{esc(t['feat_global'])}</h3><p>{esc(t['feat_global_desc'])}</p></div>
      <div class="feat-card"><div class="icon">💬</div><h3>{esc(t['feat_support'])}</h3><p>{esc(t['feat_support_desc'])}</p></div>
    </div>
  </div>
</section>
'''

    # Featured products (first 8)
    body += f'''
<section class="section section-light">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">{esc(t['section_products_eyebrow'])}</div>
      <h2>{esc(t['section_products_title'])}</h2>
      <p>{esc(t['section_products_desc'])}</p>
    </div>
    <div class="product-grid">
'''
    for p in products[:8]:
        body += render_product_card(p, t)
    body += f'''    </div>
    <div style="text-align:center; margin-top:50px;">
      <a href="products.html" class="btn btn-gold">{esc(t['cta_view_catalog'])} →</a>
    </div>
  </div>
</section>
'''

    # Workshop preview
    body += f'''
<section class="section section-dark" style="background-image:linear-gradient(rgba(58,69,54,0.92), rgba(58,69,54,0.92)), url('../assets/backgrounds/eco_hero1.jpg'); background-size:cover; background-position:center;">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow" style="color:var(--gd-light);">{esc(t['section_workshop_eyebrow'])}</div>
      <h2 style="color:var(--gd-light);">{esc(t['section_workshop_title'])}</h2>
      <p style="color:rgba(255,255,255,0.85);">{esc(t['section_workshop_desc'])}</p>
    </div>
    <div class="workshop-grid">
      <div class="workshop-card"><img src="../assets/workshop/line1.png" alt="PP Melt-Blown Production Line" /><div class="label"><h3>PP Melt-Blown Filter Line</h3><p>Automated extrusion · 24/7 operation</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/2_carbon_block_line.jpg" alt="Carbon Block Production Line" /><div class="label"><h3>Carbon Block Line</h3><p>Sintered CTO · Coconut-shell media</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/3_quick_connect_line.png" alt="Quick Connect Assembly Line" /><div class="label"><h3>Inline Filter Line</h3><p>Quick-connect assembly</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/4_leak_test.png" alt="Quality Leakage Test" /><div class="label"><h3>QC Leakage Test</h3><p>100% pressure-tested before shipment</p></div></div>
    </div>
    <div style="text-align:center; margin-top:40px;">
      <a href="workshop.html" class="btn btn-gold">{esc(t['nav_workshop'])} →</a>
    </div>
  </div>
</section>
'''

    # CTA
    body += f'''
<section class="section section-cream">
  <div class="container" style="text-align:center; max-width:760px;">
    <h2 style="margin-bottom:20px;">{esc(t['section_contact_title'])}</h2>
    <p style="font-size:17px; color:var(--muted); margin-bottom:32px;">{esc(t['hero_desc'][:200])}</p>
    <div class="hero-actions" style="justify-content:center;">
      <a href="contact.html" class="btn btn-gold">{esc(t['cta_request_quote'])}</a>
      <a href="https://wa.me/{GEO['wa']}" target="_blank" class="btn" style="background:#25D366;color:#fff !important;">📱 {esc(t['cta_whatsapp'])}</a>
    </div>
  </div>
</section>
'''

    body += footer_html(t, lang)
    return body


def render_product_card(p, t):
    img = p.get("image", "../assets/products/1.png")
    name = esc(p.get("name", ""))
    cat = esc(p.get("category", ""))
    desc_short = esc((p.get("desc", "") or "")[:130]) + "..."
    pid = p["id"]
    return f'''      <article class="product-card" data-cat="{cat}">
        <a href="product-{pid}.html" class="product-img-wrap">
          <span class="product-cat-badge">{cat}</span>
          <img src="{img}" alt="{name}" loading="lazy" onerror="this.src='../assets/products/1.png'" />
        </a>
        <div class="product-body">
          <h3>{name}</h3>
          <p>{desc_short}</p>
          <a href="product-{pid}.html" class="product-link">{esc(t['cta_view_details'])} →</a>
        </div>
      </article>
'''


# ============================================================
# PAGE: About Us
# ============================================================
def render_about(lang):
    t = get_t(lang)
    title = f"About Express Water | OEM Water Filter Manufacturer Since 1998"
    desc = "Express Water is a leading China-based OEM water filtration manufacturer with 27+ years of experience, ISO 9001 certified, exporting to 50+ countries."
    body = head(title, desc, lang, "about.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "about.html")

    body += f'''
<section class="hero" style="min-height:42vh; background-image:linear-gradient(rgba(58,69,54,0.82), rgba(58,69,54,0.7)), url('../assets/backgrounds/eco_hero1.jpg');">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['section_about_eyebrow'])}</div>
    <h1>{esc(t['nav_about'])}</h1>
    <p class="hero-desc">{esc(t['section_about_desc'])}</p>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;">
      <div>
        <div class="eyebrow">Our Story</div>
        <h2 style="margin-bottom:20px;">27+ Years Producing Premium Water Filtration</h2>
        <p style="font-size:16px;line-height:1.85;color:var(--muted);margin-bottom:18px;">Founded in 1998 in Yuanhua Town, Haining City, Zhejiang Province — strategically located 90 minutes from Shanghai's container ports — Express Water has grown into one of the most trusted OEM/ODM water filtration manufacturers in China.</p>
        <p style="font-size:16px;line-height:1.85;color:var(--muted);margin-bottom:18px;">Our 20,000+ m² ISO 9001:2015 certified facility houses dedicated production lines for PP melt-blown sediment filters, sintered CTO carbon block filters, GAC granular carbon, T33 post-carbon, UF hollow-fiber membranes, and the full RO membrane element family from 50 GPD residential to 600 GPD commercial.</p>
        <p style="font-size:16px;line-height:1.85;color:var(--muted);">Today we proudly supply over 50 countries with NSF/ANSI 42, 53 and 58 compliant products, holding CE, SGS, FDA, China 3C and JAKIM Halal certifications for international compliance.</p>
      </div>
      <div>
        <img src="../assets/workshop/line1.png" alt="Express Water Factory" style="width:100%;border-radius:6px;box-shadow:var(--shadow-md);" onerror="this.src='../assets/backgrounds/eco_hero1.jpg'" />
      </div>
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Why Choose Express Water</div>
      <h2>Built for Global B2B Distributors</h2>
    </div>
    <div class="feat-grid">
      <div class="feat-card"><div class="icon">🏆</div><h3>{esc(t['feat_oem'])}</h3><p>{esc(t['feat_oem_desc'])}</p></div>
      <div class="feat-card"><div class="icon">✅</div><h3>{esc(t['feat_certified'])}</h3><p>{esc(t['feat_certified_desc'])}</p></div>
      <div class="feat-card"><div class="icon">🌍</div><h3>{esc(t['feat_global'])}</h3><p>{esc(t['feat_global_desc'])}</p></div>
      <div class="feat-card"><div class="icon">💬</div><h3>{esc(t['feat_support'])}</h3><p>{esc(t['feat_support_desc'])}</p></div>
      <div class="feat-card"><div class="icon">🧪</div><h3>R&D & Testing</h3><p>In-house lab tests every batch for flow rate, pressure drop, contaminant rejection.</p></div>
      <div class="feat-card"><div class="icon">🚚</div><h3>Container-Ready</h3><p>1×20'GP ≈ 80,000 cartridges. FOB SHA/NGB · CIF · DDP terms.</p></div>
      <div class="feat-card"><div class="icon">📋</div><h3>Halal Certified</h3><p>JAKIM Malaysia certified for Muslim markets — full documentation.</p></div>
      <div class="feat-card"><div class="icon">🔧</div><h3>Tooling & R&D</h3><p>Custom injection-mold tooling — refundable on volume orders.</p></div>
    </div>
  </div>
</section>

<section class="section section-dark" style="background-image:linear-gradient(rgba(58,69,54,0.92),rgba(58,69,54,0.92)),url('../assets/backgrounds/eco_hero1.jpg');background-size:cover;">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow" style="color:var(--gd-light);">Certifications & Compliance</div>
      <h2 style="color:var(--gd-light);">Globally Recognized Quality Standards</h2>
    </div>
    <div class="feat-grid">
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">🏅</div><h3 style="color:var(--gd-light);">NSF/ANSI 42, 53 & 58</h3><p style="color:rgba(255,255,255,0.8);">Aesthetic, health and reverse osmosis water treatment.</p></div>
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">📜</div><h3 style="color:var(--gd-light);">ISO 9001:2015</h3><p style="color:rgba(255,255,255,0.8);">Quality management system certified.</p></div>
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">🇪🇺</div><h3 style="color:var(--gd-light);">CE Marking</h3><p style="color:rgba(255,255,255,0.8);">European import compliance.</p></div>
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">🔬</div><h3 style="color:var(--gd-light);">SGS Test Reports</h3><p style="color:rgba(255,255,255,0.8);">Heavy-metal & VOC removal validated.</p></div>
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">🇨🇳</div><h3 style="color:var(--gd-light);">China 3C</h3><p style="color:rgba(255,255,255,0.8);">Compulsory certification for dispensers.</p></div>
      <div class="feat-card" style="background:rgba(255,255,255,0.08);border-color:rgba(255,255,255,0.1);"><div class="icon">☪️</div><h3 style="color:var(--gd-light);">JAKIM Halal</h3><p style="color:rgba(255,255,255,0.8);">For Muslim-market distribution.</p></div>
    </div>
  </div>
</section>
'''

    body += footer_html(t, lang)
    return body


# ============================================================
# PAGE: Products list
# ============================================================
def render_products(lang):
    t = get_t(lang)
    products = get_products(lang)
    cats = sorted({p.get("category", "Other") for p in products})
    title = f"All Products | Express Water — Filters, RO Membranes, Dispensers"
    desc = "Browse Express Water's complete OEM/ODM product catalog: PP melt-blown filters, CTO carbon blocks, GAC, UF, T33, RO membranes, and water dispensers."
    body = head(title, desc, lang, "products.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "products.html")

    body += f'''
<section class="hero" style="min-height:38vh; background-image:linear-gradient(rgba(58,69,54,0.85),rgba(58,69,54,0.7)), url('../assets/backgrounds/eco_hero1.jpg');">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['section_products_eyebrow'])}</div>
    <h1>{esc(t['section_products_title'])}</h1>
    <p class="hero-desc">{esc(t['section_products_desc'])}</p>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div class="cat-filter">
      <button class="cat-btn active" onclick="filterCat('all', this)">{esc(t['products_filter_all'])}</button>
'''
    for c in cats:
        body += f'      <button class="cat-btn" onclick="filterCat({json.dumps(c)}, this)">{esc(c)}</button>\n'
    body += '    </div>\n    <div class="product-grid">\n'
    for p in products:
        body += render_product_card(p, t)
    body += '''    </div>
  </div>
</section>
'''
    body += footer_html(t, lang)
    return body


# ============================================================
# PAGE: Single product detail
# ============================================================
def render_product_detail(p, lang, all_products):
    t = get_t(lang)
    pid = p["id"]
    img = p.get("image", "../assets/products/1.png")
    name = esc(p.get("name", ""))
    cat = esc(p.get("category", ""))
    desc = p.get("desc", "")
    specs = p.get("specs", {}) or {}
    features = p.get("features", []) or []
    title = f"{name} | Express Water OEM Manufacturer"
    meta_desc = (desc[:155]).replace('"', "'")
    body = head(title, meta_desc, lang, f"product-{pid}.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "products.html")

    # Spec table
    spec_rows = ""
    for k, v in specs.items():
        spec_rows += f"      <tr><th>{esc(k)}</th><td>{esc(v)}</td></tr>\n"

    feat_html = ""
    if features:
        feat_html = f'''
    <h3 style="margin-top:36px;margin-bottom:14px;color:var(--fg);">{esc(t['features_title'])}</h3>
    <ul class="benefits-list">
'''
        for f in features:
            feat_html += f"      <li>{esc(f)}</li>\n"
        feat_html += "    </ul>\n"

    body += f'''
<section class="section section-cream" style="padding-top:50px;">
  <div class="container">
    <div class="product-detail">
      <div class="product-detail-img">
        <img src="{img}" alt="{name}" onerror="this.src='../assets/products/1.png'" />
      </div>
      <div class="product-detail-info">
        <div class="breadcrumb"><a href="index.html">{esc(t['nav_home'])}</a> · <a href="products.html">{esc(t['products_breadcrumb'])}</a> · {name}</div>
        <h1>{name}</h1>
        <span class="cat-badge">{cat}</span>
        <p class="desc">{esc(desc)}</p>
        <h3 style="color:var(--fg);font-size:1.2rem;margin-bottom:8px;">{esc(t['spec_table_title'])}</h3>
        <table class="spec-table">
{spec_rows}        </table>
        {feat_html}
        <div class="product-actions">
          <a href="https://wa.me/{GEO['wa']}?text=Inquiry%20about%20{esc(name).replace(' ', '%20')}" target="_blank" class="btn" style="background:#25D366;color:white !important;">📱 {esc(t['cta_inquire_now'])}</a>
          <a href="contact.html" class="btn btn-gold">✉ {esc(t['cta_request_quote'])}</a>
        </div>
        <p style="margin-top:24px;font-size:13px;color:var(--muted);">
          {esc(t['back_to_products'])} <a href="products.html" style="color:var(--gd-dark);font-weight:500;">{esc(t['nav_products'])}</a>
        </p>
      </div>
    </div>
  </div>
</section>

<!-- Related Products -->
<section class="section section-light">
  <div class="container">
    <div class="section-head"><h2>{esc(t['related_products'])}</h2></div>
    <div class="product-grid">
'''
    related = [x for x in all_products if x.get("category") == p.get("category") and x["id"] != pid][:4]
    for rp in related:
        body += render_product_card(rp, t)
    body += '''    </div>
  </div>
</section>
'''
    body += footer_html(t, lang)
    return body


# ============================================================
# PAGE: Workshop
# ============================================================
def render_workshop(lang):
    t = get_t(lang)
    title = "Workshop & Manufacturing | Express Water Factory Tour"
    desc = "Tour our 20,000+ m² ISO 9001 certified water filter factory in Haining, Zhejiang. PP melt-blown, carbon block, RO/UF membrane production lines."
    body = head(title, desc, lang, "workshop.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "workshop.html")

    body += f'''
<section class="hero" style="min-height:38vh; background-image:linear-gradient(rgba(58,69,54,0.85),rgba(58,69,54,0.7)), url('../assets/workshop/line1.png');background-size:cover;background-position:center;">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['section_workshop_eyebrow'])}</div>
    <h1>{esc(t['nav_workshop'])}</h1>
    <p class="hero-desc">{esc(t['section_workshop_desc'])}</p>
  </div>
</section>

<section class="section section-light">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Production Lines</div>
      <h2>20,000+ m² ISO 9001 Certified Facility</h2>
      <p>Our state-of-the-art manufacturing center in Yuanhua Town, Haining, Zhejiang Province operates dedicated lines for every product family — ensuring traceability, quality and on-time delivery for global wholesale orders.</p>
    </div>
    <div class="workshop-grid">
      <div class="workshop-card"><img src="../assets/workshop/line1.png" alt="PP Melt-Blown Production Line" /><div class="label"><h3>PP Melt-Blown Filter Line</h3><p>Automated extrusion · 24/7 production · Virgin PP resin only</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/2_carbon_block_line.jpg" alt="Carbon Block Production Line" /><div class="label"><h3>Carbon Block Line</h3><p>Sintered carbon · Coconut-shell media · NSF certified</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/3_quick_connect_line.png" alt="Quick-Connect Inline Filter Assembly" /><div class="label"><h3>Inline / Quick-Connect Assembly</h3><p>T33, mineralization & post-carbon cartridges</p></div></div>
      <div class="workshop-card"><img src="../assets/workshop/4_leak_test.png" alt="Quality Control Leakage Test" /><div class="label"><h3>QC Leakage & Pressure Test</h3><p>100% hydrostatic-tested at 1.5× rated pressure</p></div></div>
    </div>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="section-head">
      <div class="eyebrow">Capabilities</div>
      <h2>Production & QC at Industrial Scale</h2>
    </div>
    <div class="feat-grid">
      <div class="feat-card"><div class="icon">⚙️</div><h3>PP Melt-Blown</h3><p>Multi-layer thermally-bonded sediment filters: 0.5 to 50 µm. Capacity: 200,000 pcs/month.</p></div>
      <div class="feat-card"><div class="icon">🪨</div><h3>Sintered Carbon Block</h3><p>CTO blocks pressed from coconut-shell or coal carbon: 1, 5, 10 µm.</p></div>
      <div class="feat-card"><div class="icon">💧</div><h3>RO Membrane</h3><p>TFC polyamide rolling line: 50, 75, 100, 200, 400, 600 GPD elements.</p></div>
      <div class="feat-card"><div class="icon">🧬</div><h3>UF Hollow-Fiber</h3><p>PVC & PES membrane potting in clean room. 0.01 µm filtration.</p></div>
      <div class="feat-card"><div class="icon">🔥</div><h3>Dispenser SMT</h3><p>Wall-mounted, vertical & desktop dispensers. ISO 9001 SMT line.</p></div>
      <div class="feat-card"><div class="icon">🔍</div><h3>In-House Lab</h3><p>Flow rate, pressure drop, salt rejection, microbial testing.</p></div>
    </div>
  </div>
</section>
'''
    body += footer_html(t, lang)
    return body


# ============================================================
# PAGE: FAQ (with FAQPage JSON-LD)
# ============================================================
def render_faq(lang):
    t = get_t(lang)
    faq = FAQ_DATA.get(lang, FAQ_DATA["en"])
    title = "FAQ | Water Filter Manufacturer Express Water — OEM, NSF, RO Membrane"
    desc = "Common questions about NSF certified water filters, OEM manufacturing, ISO 9001 quality, RO membrane wholesale, halal certification & global shipping."
    body = head(title, desc, lang, "faq.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "faq.html")

    body += f'''
<section class="hero" style="min-height:34vh; background-image:linear-gradient(rgba(58,69,54,0.85),rgba(58,69,54,0.72)), url('../assets/backgrounds/eco_hero1.jpg');">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['section_faq_eyebrow'])}</div>
    <h1>{esc(t['section_faq_title'])}</h1>
    <p class="hero-desc">{esc(faq.get('faq_intro', ''))[:200]}</p>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="faq-wrap">
'''
    for i, item in enumerate(faq.get("faqs", [])):
        q = esc(item.get("q", ""))
        a = esc(item.get("a", ""))
        body += f'''      <div class="faq-item{' open' if i==0 else ''}">
        <button class="faq-q">{q}</button>
        <div class="faq-a"><p>{a}</p></div>
      </div>
'''
    body += '''    </div>
  </div>
</section>
'''
    # Inject FAQPage JSON-LD for Google rich snippet & GEO
    faq_jsonld = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": item["q"], "acceptedAnswer": {"@type": "Answer", "text": item["a"]}}
            for item in faq.get("faqs", [])
        ],
    }
    body += f'<script type="application/ld+json">{json.dumps(faq_jsonld, ensure_ascii=False)}</script>\n'
    body += footer_html(t, lang)
    return body


# ============================================================
# PAGE: Contact
# ============================================================
def render_contact(lang):
    t = get_t(lang)
    title = "Contact Express Water | Bulk OEM Inquiry, WhatsApp & Quote Request"
    desc = "Contact Express Water for bulk OEM water filter quotes. WhatsApp +86-19908311885 · expresswater025@gmail.com · Factory: Haining, Zhejiang, China."
    body = head(title, desc, lang, "contact.html", LANGS)
    body += topbar_html(t, lang)
    body += navbar_html(t, lang, "contact.html")

    body += f'''
<section class="hero" style="min-height:36vh; background-image:linear-gradient(rgba(58,69,54,0.85),rgba(58,69,54,0.7)), url('../assets/backgrounds/eco_hero1.jpg');">
  <div class="container hero-content">
    <div class="hero-eyebrow">{esc(t['section_contact_eyebrow'])}</div>
    <h1>{esc(t['section_contact_title'])}</h1>
    <p class="hero-desc">Reach our B2B sales team via WhatsApp, email or the form below. Average response time: under 4 hours during business days.</p>
  </div>
</section>

<section class="section section-cream">
  <div class="container">
    <div class="contact-grid">
      <div class="contact-info">
        <h3>Get in Touch</h3>
        <div class="contact-info-item">
          <div class="icon">📍</div>
          <div>
            <div class="label">{esc(t['contact_addr_label'])}</div>
            <p>{GEO['address']}</p>
          </div>
        </div>
        <div class="contact-info-item">
          <div class="icon">📞</div>
          <div>
            <div class="label">{esc(t['contact_phone_label'])}</div>
            <p><a href="tel:{GEO['phone']}">{GEO['phone']}</a></p>
          </div>
        </div>
        <div class="contact-info-item">
          <div class="icon">📱</div>
          <div>
            <div class="label">{esc(t['contact_wa_label'])}</div>
            <p><a href="https://wa.me/{GEO['wa']}" target="_blank">+86 19908311885 (24/7 sales)</a></p>
          </div>
        </div>
        <div class="contact-info-item">
          <div class="icon">✉</div>
          <div>
            <div class="label">{esc(t['contact_email_label'])}</div>
            <p><a href="mailto:{GEO['email']}">{GEO['email']}</a></p>
          </div>
        </div>
        <div class="contact-info-item">
          <div class="icon">🕐</div>
          <div>
            <div class="label">{esc(t['contact_hours_label'])}</div>
            <p>{esc(t['contact_hours'])}</p>
          </div>
        </div>

        <div style="margin-top:36px;padding-top:30px;border-top:1px solid rgba(255,255,255,0.15);">
          <p style="font-size:13px;color:var(--gd-light);margin-bottom:8px;">CERTIFIED MANUFACTURER</p>
          <p style="font-size:13px;color:rgba(255,255,255,0.75);">NSF · ISO 9001:2015 · CE · SGS · 3C · Halal (JAKIM)</p>
        </div>
      </div>

      <form class="contact-form" onsubmit="event.preventDefault(); window.open('https://wa.me/{GEO['wa']}?text=Inquiry from ' + this.elements.name.value, '_blank');">
        <h3 style="color:var(--fg);margin-bottom:24px;font-size:1.5rem;">{esc(t['cta_request_quote'])}</h3>
        <div class="form-row"><label>{esc(t['form_name'])}</label><input type="text" name="name" required></div>
        <div class="form-row"><label>{esc(t['form_company'])}</label><input type="text" name="company"></div>
        <div class="form-row"><label>{esc(t['form_email'])}</label><input type="email" name="email" required></div>
        <div class="form-row"><label>{esc(t['form_phone'])}</label><input type="text" name="phone"></div>
        <div class="form-row"><label>{esc(t['form_country'])}</label><input type="text" name="country"></div>
        <div class="form-row"><label>{esc(t['form_message'])}</label><textarea name="message" required></textarea></div>
        <button type="submit" class="btn">{esc(t['cta_send_message'])} →</button>
      </form>
    </div>
  </div>
</section>

<section class="section section-light" style="padding:0;">
  <iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3471.123!2d{GEO['lon']}!3d{GEO['lat']}!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1sHaining%20Zhejiang!5e0!3m2!1sen!2scn!4v1730000000" width="100%" height="380" style="border:0;display:block;" loading="lazy"></iframe>
</section>
'''
    body += footer_html(t, lang)
    return body


# ============================================================
# DRIVER
# ============================================================
def main():
    print(f"Rendering site for {len(LANGS)} languages...")
    total_files = 0
    for lang in LANGS:
        out_dir = os.path.join(ROOT, lang)
        os.makedirs(out_dir, exist_ok=True)
        # Core pages
        with open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8") as f:
            f.write(render_home(lang))
        with open(os.path.join(out_dir, "about.html"), "w", encoding="utf-8") as f:
            f.write(render_about(lang))
        with open(os.path.join(out_dir, "products.html"), "w", encoding="utf-8") as f:
            f.write(render_products(lang))
        with open(os.path.join(out_dir, "workshop.html"), "w", encoding="utf-8") as f:
            f.write(render_workshop(lang))
        with open(os.path.join(out_dir, "faq.html"), "w", encoding="utf-8") as f:
            f.write(render_faq(lang))
        with open(os.path.join(out_dir, "contact.html"), "w", encoding="utf-8") as f:
            f.write(render_contact(lang))
        total_files += 6
        # Product detail pages
        products = get_products(lang)
        for p in products:
            with open(os.path.join(out_dir, f"product-{p['id']}.html"), "w", encoding="utf-8") as f:
                f.write(render_product_detail(p, lang, products))
            total_files += 1
        print(f"  ✓ {lang}: 6 core + {len(products)} product pages")

    # Root redirect
    redirect_html = '''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
<title>Express Water — Industrial Water Filtration OEM Manufacturer</title>
<meta http-equiv="refresh" content="0; url=en/index.html">
<script>
(function(){
  var langs = ''' + json.dumps(LANGS) + ''';
  var browser = (navigator.language || 'en').slice(0,2).toLowerCase();
  if (langs.indexOf(browser) >= 0) {
    location.replace(browser + '/index.html');
  } else {
    location.replace('en/index.html');
  }
})();
</script>
</head>
<body>
<p style="font-family:sans-serif;text-align:center;padding:40px;">Redirecting to <a href="en/index.html">Express Water</a>...</p>
</body></html>'''
    with open(os.path.join(ROOT, "index.html"), "w", encoding="utf-8") as f:
        f.write(redirect_html)

    # Sitemap
    sitemap_lines = ['<?xml version="1.0" encoding="UTF-8"?>',
                     '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">']
    for lang in LANGS:
        for page in ["index.html", "about.html", "products.html", "workshop.html", "faq.html", "contact.html"]:
            sitemap_lines.append(f'  <url>')
            sitemap_lines.append(f'    <loc>https://expresswater.cn/{lang}/{page}</loc>')
            for alt in LANGS:
                sitemap_lines.append(f'    <xhtml:link rel="alternate" hreflang="{alt}" href="https://expresswater.cn/{alt}/{page}"/>')
            sitemap_lines.append(f'    <changefreq>weekly</changefreq>')
            sitemap_lines.append(f'    <priority>0.8</priority>')
            sitemap_lines.append(f'  </url>')
        for p in get_products(lang):
            sitemap_lines.append(f'  <url><loc>https://expresswater.cn/{lang}/product-{p["id"]}.html</loc><priority>0.7</priority></url>')
    sitemap_lines.append('</urlset>')
    with open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write("\n".join(sitemap_lines))

    # Robots
    with open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8") as f:
        f.write("User-agent: *\nAllow: /\nSitemap: https://expresswater.cn/sitemap.xml\n")

    print(f"\n✓ Total files generated: {total_files} HTML pages across {len(LANGS)} languages")
    print(f"✓ Root redirect, sitemap.xml, robots.txt written")


if __name__ == "__main__":
    main()
