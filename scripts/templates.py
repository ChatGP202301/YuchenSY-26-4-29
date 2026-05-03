"""HTML page templates for Express Water multi-language B2B website.

Forest Green / Champagne Gold theme. Produces semantic, SEO-rich HTML.
"""

# Forest Green #485342, Champagne Gold #B5A48B, Light BG #F9F9F7
PALETTE = {
    "fg": "#485342",       # Forest Green
    "gd": "#B5A48B",       # Champagne Gold
    "bg": "#F9F9F7",       # Light cream background
    "fgd": "#3a4536",      # Dark green
    "txt": "#2c3329",      # Body text
    "muted": "#6b7368",
}

GEO = {
    "lat": "30.4398",
    "lon": "120.6974",
    "city": "Haining",
    "region": "Zhejiang",
    "country": "CN",
    "address": "Yuanhua Town, Haining City, Zhejiang Province, China",
    "phone": "+86-19908311885",
    "email": "expresswater025@gmail.com",
    "wa": "8619908311885",
}

LANGS = ['en','es','fr','de','pt','ru','ar','ja','ko','it','tr','hi','bn','id','vi','th','pl','nl','fa','ur','ms','tl','he','el','cs','hu','ro','sv','da','fi','no','uk','bg','hr','sr','sk','sl','lt','et','lv','sw','ha','zu','ta','kk']

LANG_LABELS = {
    "en": "English", "es": "Español", "fr": "Français", "de": "Deutsch", "pt": "Português",
    "ru": "Русский", "ar": "العربية", "ja": "日本語", "ko": "한국어", "it": "Italiano",
    "tr": "Türkçe", "hi": "हिन्दी", "bn": "বাংলা", "id": "Bahasa Indonesia", "vi": "Tiếng Việt",
    "th": "ไทย", "pl": "Polski", "nl": "Nederlands", "fa": "فارسی", "ur": "اردو",
    "ms": "Bahasa Melayu", "tl": "Tagalog", "he": "עברית", "el": "Ελληνικά", "cs": "Čeština",
    "hu": "Magyar", "ro": "Română", "sv": "Svenska", "da": "Dansk", "fi": "Suomi",
    "no": "Norsk", "uk": "Українська", "bg": "Български", "hr": "Hrvatski", "sr": "Српски",
    "sk": "Slovenčina", "sl": "Slovenščina", "lt": "Lietuvių", "et": "Eesti", "lv": "Latviešu",
    "sw": "Kiswahili", "ha": "Hausa", "zu": "isiZulu", "ta": "தமிழ்", "kk": "Қазақша",
}

RTL_LANGS = {"ar", "fa", "he", "ur", "ps", "prs"}

NAV_KEYS = [
    ("nav_home", "index.html"),
    ("nav_about", "about.html"),
    ("nav_products", "products.html"),
    ("nav_workshop", "workshop.html"),
    ("nav_faq", "faq.html"),
    ("nav_contact", "contact.html"),
]


def head(title, description, lang, page_path, alt_langs):
    """SEO+GEO head with hreflang, JSON-LD, OG, GEO tags."""
    is_rtl = lang in RTL_LANGS
    dir_attr = ' dir="rtl"' if is_rtl else ' dir="ltr"'
    canonical = f"https://expresswater.cn/{lang}/{page_path}"
    hreflang = "\n".join(
        f'  <link rel="alternate" hreflang="{l}" href="https://expresswater.cn/{l}/{page_path}" />'
        for l in alt_langs
    )
    hreflang += f'\n  <link rel="alternate" hreflang="x-default" href="https://expresswater.cn/en/{page_path}" />'

    jsonld = f'''
{{
  "@context": "https://schema.org",
  "@type": "IndustrialBusiness",
  "name": "Express Water",
  "alternateName": "Eco Express Water",
  "url": "{canonical}",
  "logo": "https://expresswater.cn/assets/logo.png",
  "image": "https://expresswater.cn/assets/backgrounds/eco_hero1.jpg",
  "description": "{description}",
  "telephone": "{GEO['phone']}",
  "email": "{GEO['email']}",
  "foundingDate": "1998",
  "address": {{
    "@type": "PostalAddress",
    "streetAddress": "Yuanhua Town",
    "addressLocality": "{GEO['city']}",
    "addressRegion": "{GEO['region']}",
    "addressCountry": "{GEO['country']}"
  }},
  "geo": {{
    "@type": "GeoCoordinates",
    "latitude": {GEO['lat']},
    "longitude": {GEO['lon']}
  }},
  "areaServed": ["United States","Germany","France","Russia","Brazil","Mexico","UK","Italy","Spain","Japan","Korea","Saudi Arabia","UAE","Egypt","India","Indonesia","Malaysia","Vietnam","Thailand","Turkey"],
  "knowsAbout": ["NSF certified water filter","RO Membrane manufacturer","OEM water purifier","Industrial filtration","PP melt-blown filter","CTO carbon block","GAC filter","UF membrane","T33 post-carbon","reverse osmosis","Halal water filter","ISO 9001:2015","SGS test report","CE certification"]
}}'''.strip()

    return f'''<!DOCTYPE html>
<html lang="{lang}"{dir_attr}>
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="keywords" content="water filter manufacturer, NSF certified, RO membrane, OEM water purifier, PP melt-blown filter, CTO carbon block, GAC filter, UF membrane, T33 post-carbon, reverse osmosis system, industrial filtration, halal water filter, China water dispenser factory, ISO 9001 water filter, wholesale water purifier, Express Water" />
  <meta name="robots" content="index, follow" />
  <meta name="author" content="Express Water" />

  <!-- Geo tags -->
  <meta name="geo.region" content="CN-ZJ" />
  <meta name="geo.placename" content="{GEO['city']}, {GEO['region']}" />
  <meta name="geo.position" content="{GEO['lat']};{GEO['lon']}" />
  <meta name="ICBM" content="{GEO['lat']}, {GEO['lon']}" />

  <!-- Open Graph -->
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{canonical}" />
  <meta property="og:image" content="https://expresswater.cn/assets/backgrounds/eco_hero1.jpg" />
  <meta property="og:locale" content="{lang}" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{title}" />
  <meta name="twitter:description" content="{description}" />

  <link rel="canonical" href="{canonical}" />
{hreflang}

  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@500;600;700&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet" />

  <link rel="stylesheet" href="../assets/styles.css" />

  <script type="application/ld+json">{jsonld}</script>
</head>
<body class="{'rtl' if is_rtl else 'ltr'}">
'''


def topbar_html(t, lang):
    return f'''
<div class="topbar">
  <div class="container topbar-row">
    <div class="topbar-left">{t.get('topbar_phone', '📞 +86-19908311885')} &nbsp;·&nbsp; {t.get('topbar_email', '✉ expresswater025@gmail.com')}</div>
    <div class="topbar-right">{t.get('topbar_tag', 'Global Bulk Wholesale · OEM/ODM Specialist · Since 1998')}</div>
  </div>
</div>
'''


def lang_switcher_dropdown(current_lang, page_path="index.html"):
    """Inline language picker between Contact and WhatsApp."""
    options = "\n".join(
        f'    <a href="../{l}/{page_path}" class="lang-option {"active" if l == current_lang else ""}" lang="{l}">{LANG_LABELS[l]}</a>'
        for l in LANGS
    )
    return f'''
<div class="lang-switcher">
  <button class="lang-btn" onclick="toggleLangMenu()">🌐 <span>{LANG_LABELS.get(current_lang, current_lang.upper())}</span> ▾</button>
  <div class="lang-menu" id="langMenu">
{options}
  </div>
</div>
'''


def navbar_html(t, lang, current_page="index.html"):
    nav_labels = {
        "nav_home": t.get("nav_home", "Home"),
        "nav_about": t.get("nav_about", "About Us"),
        "nav_products": t.get("nav_products", "Products"),
        "nav_workshop": t.get("nav_workshop", "Workshop"),
        "nav_faq": t.get("nav_faq", "FAQ"),
        "nav_contact": t.get("nav_contact", "Contact"),
    }
    items = ""
    for key, href in NAV_KEYS:
        active = " active" if href == current_page else ""
        items += f'<a href="{href}" class="nav-link{active}">{nav_labels[key]}</a>\n      '
    wa_label = t.get("cta_whatsapp", "WhatsApp Us")
    return f'''
<header class="header">
  <div class="container header-row">
    <a href="index.html" class="brand">
      <img src="../assets/logo.png" alt="Express Water" class="logo-img" onerror="this.style.display='none'" />
      <span class="brand-name">Express Water</span>
    </a>
    <nav class="nav">
      {items}
    </nav>
    <div class="header-actions">
      {lang_switcher_dropdown(lang, current_page)}
      <a href="https://wa.me/{GEO['wa']}" target="_blank" rel="noopener" class="cta-wa">📱 {wa_label}</a>
      <button class="mobile-menu-toggle" onclick="document.querySelector('.nav').classList.toggle('open')">☰</button>
    </div>
  </div>
</header>
'''


def footer_html(t, lang):
    nav_labels = {
        "nav_home": t.get("nav_home", "Home"),
        "nav_about": t.get("nav_about", "About Us"),
        "nav_products": t.get("nav_products", "Products"),
        "nav_workshop": t.get("nav_workshop", "Workshop"),
        "nav_faq": t.get("nav_faq", "FAQ"),
        "nav_contact": t.get("nav_contact", "Contact"),
    }
    return f'''
<footer class="footer">
  <div class="container footer-grid">
    <div class="footer-col footer-brand">
      <div class="footer-logo">Express Water</div>
      <p>{t.get("footer_brand_desc", "Leading China manufacturer of industrial water filtration products since 1998. NSF, ISO 9001 and SGS certified factory specializing in OEM/ODM solutions for global wholesale distributors.")}</p>
    </div>
    <div class="footer-col">
      <h4>{t.get("footer_company", "Company")}</h4>
      <a href="index.html">{nav_labels["nav_home"]}</a>
      <a href="about.html">{nav_labels["nav_about"]}</a>
      <a href="workshop.html">{nav_labels["nav_workshop"]}</a>
      <a href="faq.html">{nav_labels["nav_faq"]}</a>
    </div>
    <div class="footer-col">
      <h4>{t.get("footer_products", "Products")}</h4>
      <a href="products.html">PP Melt-Blown Filter</a>
      <a href="products.html">CTO Carbon Block</a>
      <a href="products.html">GAC Filter</a>
      <a href="products.html">RO Membrane</a>
      <a href="products.html">UF Membrane</a>
      <a href="products.html">Water Dispenser</a>
    </div>
    <div class="footer-col">
      <h4>{t.get("footer_contact", "Contact")}</h4>
      <p>📍 {GEO['address']}</p>
      <p>📞 <a href="tel:{GEO['phone']}">{GEO['phone']}</a></p>
      <p>✉ <a href="mailto:{GEO['email']}">{GEO['email']}</a></p>
      <p>📱 <a href="https://wa.me/{GEO['wa']}" target="_blank">WhatsApp</a></p>
    </div>
  </div>
  <div class="footer-bottom">
    <div class="container">
      © 2026 Express Water · Eco Express Water Co., Ltd. · {t.get("footer_rights", "All Rights Reserved")} · NSF · ISO 9001:2015 · CE · SGS · 3C · Halal Certified
    </div>
  </div>
</footer>
<script src="../assets/site.js"></script>
</body>
</html>'''
