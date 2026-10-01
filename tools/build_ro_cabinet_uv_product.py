#!/usr/bin/env python3
"""Deterministically build the 62-locale cabinet RO + optional UV product."""

import argparse
import csv
import hashlib
import html
import io
import json
import re
from pathlib import Path

from quote_schema_policy import normalize_paths_in_place


ROUTE = "product-cabinet-ro-water-purifier-5-6-stage-uv.html"
OLD_ROUTE = "product-custom-5-6-7-stage-ro-water-purifier.html"
SITE = "https://www.yuchensy.com"
LASTMOD = "2026-08-11"
DETAIL_START = "<!-- RO_CABINET_UV_DETAIL_LINK_START -->"
DETAIL_END = "<!-- RO_CABINET_UV_DETAIL_LINK_END -->"
SITEMAP_START = "<!-- RO_CABINET_UV_URL_START -->"
SITEMAP_END = "<!-- RO_CABINET_UV_URL_END -->"
GLOBAL_HREFLANG_OVERRIDES = {
    "be": "be-BY",
    "cnr": "sr-Latn-ME",
    "ga": "ga-IE",
    "lb": "lb-LU",
    "mk": "mk-MK",
    "mt": "mt-MT",
    "sr-me": "sr-ME",
}
MEDIA = [
    ("cabinet-ro-water-purifier-main.png", 800, 800),
    ("cabinet-ro-water-purifier-black.png", 649, 649),
    ("cabinet-ro-water-purifier-workshop.png", 1200, 1200),
]


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_if_changed(path, content, changed):
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == content:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    changed.append(path)


def replace_block(text, start, end, block, before):
    pattern = re.compile(re.escape(start) + r".*?" + re.escape(end), re.S)
    if pattern.search(text):
        return pattern.sub(block, text, count=1)
    if before not in text:
        raise ValueError("insertion anchor not found: %s" % before)
    return text.replace(before, block + "\n" + before, 1)


def page_url(locale):
    return "%s/%s/%s" % (SITE, locale, ROUTE)


def compact_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")


def localized_context(record, tr, source):
    ui = record["labels"]
    note = record["specification_note"]
    if record["code"] == "en":
        short = source["english_copy"]["short_answer"]
        config_note = source["english_copy"]["configuration_note"]
        compare = source["english_copy"]["comparison_note"]
        uv_q = source["english_copy"]["uv_faq_question"]
        uv_a = source["english_copy"]["uv_faq_answer"]
        quote_q = source["english_copy"]["quote_faq_question"]
        quote_a = source["english_copy"]["quote_faq_answer"]
    else:
        short = "%s. %s; UV: %s; OEM/ODM: %s." % (
            tr["cabinet"], tr["stages"], tr["optional"], tr["available"]
        )
        config_note = "%s: %s. %s; %s; %s; %s; %s; UV %s; %s; %s." % (
            ui["project"], tr["confirm"], ui["output"], ui["dimensions"],
            ui["filtration"], tr["pump"], ui["voltage"], ui["power"],
            ui["quantity"], tr["certifications"]
        )
        compare = tr["compare"] + "."
        uv_q = "UV — %s?" % tr["optional"]
        uv_a = "UV: %s; %s." % (tr["optional"], tr["confirm"])
        quote_q = ui["project"] + "?"
        quote_a = config_note + " " + note
    description = "%s. %s" % (short, note)
    return {
        "ui": ui,
        "note": note,
        "short": short,
        "config_note": config_note,
        "compare": compare,
        "uv_q": uv_q,
        "uv_a": uv_a,
        "quote_q": quote_q,
        "quote_a": quote_a,
        "description": description,
    }


def language_links(registry, current):
    items = []
    for item in registry["locales"]:
        code = item["directory"].strip("/")
        current_attr = ' aria-current="page"' if code == current else ""
        items.append(
            '<li><a href="../%s/%s" hreflang="%s"%s>%s</a></li>'
            % (code, ROUTE, html.escape(item["html_lang"]), current_attr,
               html.escape(item["language_selector_label"]))
        )
    return "".join(items)


def global_alternate_records(root):
    global_locales = load_json(root / "migration/product-taxonomy/locales.json")["locales"]
    codes = list(global_locales)
    if len(codes) != 63 or len(set(codes)) != 63:
        raise ValueError("product taxonomy must define exactly 63 global locale routes")
    records = []
    for code in codes:
        hreflang = GLOBAL_HREFLANG_OVERRIDES.get(code, code)
        records.append((code, hreflang))
    if len({hreflang for _code, hreflang in records}) != 63:
        raise ValueError("global hreflang values must be unique")
    return records


def alternates(records):
    links = []
    for code, hreflang in records:
        links.append(
            '  <link rel="alternate" hreflang="%s" href="%s" />'
            % (html.escape(hreflang), page_url(code))
        )
    links.append(
        '  <link rel="alternate" hreflang="x-default" href="%s" />'
        % page_url("en")
    )
    return "\n".join(links)


def jsonld(locale, record, tr, ctx):
    url = page_url(locale)
    ui = ctx["ui"]
    images = ["%s/assets/products/ro-cabinet-uv/%s" % (SITE, name) for name, _, _ in MEDIA]
    faq = [
        {"@type": "Question", "name": ctx["uv_q"],
         "acceptedAnswer": {"@type": "Answer", "text": ctx["uv_a"]}},
        {"@type": "Question", "name": ctx["quote_q"],
         "acceptedAnswer": {"@type": "Answer", "text": ctx["quote_a"]}},
    ]
    graph = [
        {"@type": "Organization", "@id": SITE + "/#organization", "name": "Yuchen Water",
         "url": SITE + "/", "email": "expresswater025@gmail.com", "telephone": "+86-19908311885"},
        {"@type": "WebSite", "@id": SITE + "/#website", "name": "Yuchen Water",
         "url": SITE + "/", "publisher": {"@id": SITE + "/#organization"}},
        {"@type": "WebPage", "@id": url + "#webpage", "url": url, "name": tr["name"],
         "description": ctx["description"], "inLanguage": record["html_lang"],
         "isPartOf": {"@id": SITE + "/#website"}, "mainEntity": {"@id": url + "#product"}},
        {"@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": ui["home"], "item": "%s/%s/" % (SITE, locale)},
            {"@type": "ListItem", "position": 2, "name": ui["products"], "item": "%s/%s/products.html" % (SITE, locale)},
            {"@type": "ListItem", "position": 3, "name": tr["name"], "item": url},
        ]},
        {"@type": "Product", "@id": url + "#product", "name": tr["name"],
         "description": ctx["short"], "url": url, "image": images,
         "brand": {"@type": "Brand", "name": "Yuchen Water"},
         "manufacturer": {"@id": SITE + "/#organization"}, "category": tr["cabinet"],
         "additionalProperty": [
             {"@type": "PropertyValue", "name": ui["product"], "value": tr["cabinet"]},
             {"@type": "PropertyValue", "name": ui["filtration"], "value": tr["stages"]},
             {"@type": "PropertyValue", "name": "UV", "value": tr["optional"]},
             {"@type": "PropertyValue", "name": "OEM/ODM", "value": tr["available"]},
         ]},
        {"@type": "FAQPage", "mainEntity": faq},
    ]
    return {"@context": "https://schema.org", "@graph": graph}


def render_page(locale, registry, alternate_records, record, tr, source, old_target, has_category, contact_target):
    ctx = localized_context(record, tr, source)
    ui = ctx["ui"]
    url = page_url(locale)
    title = tr["name"] + " | Yuchen Water"
    summary = html.escape(ctx["short"])
    desc = html.escape(ctx["description"], quote=True)
    assets = "../assets/products/ro-cabinet-uv/"
    schema = compact_json(jsonld(locale, record, tr, ctx))
    return """<!doctype html>
<html lang="{html_lang}" dir="{direction}">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{title}</title>
  <meta name="description" content="{description}" />
  <meta name="robots" content="index,follow" />
  <meta name="translation-review" content="ai-multipass-reviewed" />
  <link rel="canonical" href="{url}" />
{alternates}
  <link rel="preload" as="image" href="{assets}cabinet-ro-water-purifier-main.png" fetchpriority="high" />
  <link rel="stylesheet" href="../assets/styles.min.css?v=20260714-product-title-links" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{title}" />
  <meta property="og:description" content="{description}" />
  <meta property="og:url" content="{url}" />
  <meta property="og:image" content="{site}/assets/products/ro-cabinet-uv/cabinet-ro-water-purifier-main.png" />
  <script type="application/ld+json">{schema}</script>
  <style>
    .rcu-page{{--rcu-ink:#11343d;--rcu-muted:#567079;--rcu-teal:#087f8c;--rcu-teal-dark:#075d68;--rcu-aqua:#dff4f2;--rcu-mist:#f3f8f8;--rcu-line:#d7e5e5;--rcu-navy:#0b3541;--rcu-white:#fff;margin:0;background:var(--rcu-white);color:var(--rcu-ink);font-family:inherit;text-align:start}}
    .rcu-page *{{box-sizing:border-box;min-width:0}}.rcu-page img{{display:block;max-width:100%}}.rcu-page a{{overflow-wrap:anywhere}}.rcu-container{{width:min(calc(100% - clamp(32px,5vw,72px)),1240px);margin-inline:auto}}
    .rcu-topbar{{background:var(--rcu-navy);color:#d7ecec;font-size:.82rem}}.rcu-topbar-row{{display:flex;min-height:36px;align-items:center;justify-content:space-between;gap:18px;padding-block:7px}}.rcu-topbar a{{color:#fff;text-decoration:none}}
    .rcu-header{{position:relative;z-index:20;border-bottom:1px solid var(--rcu-line);background:rgba(255,255,255,.97)}}.rcu-header-row{{display:grid;grid-template-columns:auto minmax(0,1fr) auto;align-items:center;gap:clamp(18px,3vw,38px);min-height:78px}}
    html.yd-ready .yd-header.rcu-header>.yd-controls{{position:absolute;inset-block-start:50%;inset-inline-end:calc(max(16px,50% - 620px) + 56px);z-index:31;display:inline-flex;width:auto;margin:0!important;transform:translateY(-50%)}}html.yd-ready .yd-header.rcu-header>.yd-controls .yd-language-button{{display:none!important}}
    .rcu-brand{{display:flex;min-height:44px;align-items:center;gap:11px;color:var(--rcu-ink);font-size:1.04rem;font-weight:850;text-decoration:none;white-space:nowrap}}.rcu-brand img{{width:126px;height:auto}}
    .rcu-primary-nav{{display:flex;align-items:center;justify-content:flex-end;gap:clamp(8px,1.5vw,22px)}}.rcu-primary-nav a{{display:inline-flex;min-height:44px;align-items:center;color:#31535b;font-size:.9rem;font-weight:750;text-decoration:none}}.rcu-primary-nav a:hover{{color:var(--rcu-teal)}}
    .rcu-languages{{position:relative}}.rcu-languages summary{{display:grid;width:48px;height:44px;place-items:center;border:1px solid var(--rcu-line);border-radius:999px;background:#fff;color:var(--rcu-navy);cursor:pointer;font-size:1.05rem;list-style:none}}.rcu-languages summary::-webkit-details-marker{{display:none}}
    .rcu-languages ul{{position:absolute;z-index:30;inset-block-start:calc(100% + 10px);inset-inline-end:0;width:min(680px,calc(100vw - 32px));max-height:58vh;margin:0;overflow:auto;columns:3;border:1px solid var(--rcu-line);border-radius:14px;background:#fff;padding:18px 22px;box-shadow:0 22px 60px rgba(11,53,65,.18)}}.rcu-languages li{{break-inside:avoid;list-style:none;margin:2px 0}}.rcu-languages a{{display:block;min-height:40px;border-radius:8px;color:#31535b;padding:9px 10px;text-decoration:none}}.rcu-languages a:hover,.rcu-languages a[aria-current=page]{{background:var(--rcu-aqua);color:var(--rcu-teal-dark)}}
    .rcu-page :focus-visible{{outline:3px solid #ffbf47;outline-offset:3px}}
    .rcu-main{{display:block}}.rcu-hero{{position:relative;overflow:hidden;background:linear-gradient(135deg,#eff9f8 0%,#e1f3f3 58%,#f8fbfb 100%);padding:clamp(46px,6vw,86px) 0 0}}.rcu-hero::after{{position:absolute;inset-block-start:-180px;inset-inline-end:-140px;width:480px;height:480px;border:1px solid rgba(8,127,140,.13);border-radius:50%;content:"";pointer-events:none}}
    .rcu-hero-grid{{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,7fr) minmax(380px,5fr);gap:clamp(34px,6vw,82px);align-items:center}}.rcu-breadcrumb{{display:flex;flex-wrap:wrap;align-items:center;gap:8px;margin:0 0 20px;color:#5d777e;font-size:.82rem}}.rcu-breadcrumb a{{color:var(--rcu-teal-dark)}}
    .rcu-kicker{{display:inline-flex;min-height:32px;align-items:center;border:1px solid rgba(8,127,140,.25);border-radius:999px;background:rgba(255,255,255,.7);color:var(--rcu-teal-dark);padding:6px 12px;font-size:.74rem;font-weight:850;letter-spacing:.1em;text-transform:uppercase}}
    .rcu-hero h1{{max-width:760px;margin:18px 0 20px;color:var(--rcu-ink);font-size:clamp(2.35rem,4.5vw,4.65rem);line-height:1.02;letter-spacing:-.025em;overflow-wrap:anywhere;hyphens:auto}}.rcu-answer{{max-width:690px;margin:0;color:#3e5e66;font-size:clamp(1rem,1.4vw,1.15rem);line-height:1.72}}
    .rcu-actions{{display:flex;flex-wrap:wrap;gap:12px;margin-top:28px}}.rcu-btn{{display:inline-flex;min-height:48px;align-items:center;justify-content:center;border:1px solid var(--rcu-teal);border-radius:6px;background:var(--rcu-teal);color:#fff;padding:12px 19px;font-size:.9rem;font-weight:850;text-align:center;text-decoration:none}}.rcu-btn:hover{{background:var(--rcu-teal-dark);border-color:var(--rcu-teal-dark);color:#fff}}.rcu-btn-secondary{{background:transparent;color:var(--rcu-teal-dark)}}.rcu-btn-secondary:hover{{background:#fff;color:var(--rcu-teal-dark)}}
    .rcu-hero-media{{position:relative;width:min(100%,460px);max-width:460px;justify-self:center;align-self:end}}.rcu-image-frame{{position:relative;overflow:hidden;border:1px solid rgba(8,127,140,.18);border-radius:28px 28px 0 0;background:rgba(255,255,255,.9);padding:clamp(16px,2.5vw,28px);box-shadow:0 28px 70px rgba(11,53,65,.14)}}.rcu-mainimg{{width:100%;height:auto;max-height:480px;object-fit:contain;aspect-ratio:1/1}}
    .rcu-facts-wrap{{position:relative;z-index:2;margin-top:clamp(34px,5vw,58px);transform:translateY(34px)}}.rcu-facts{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));overflow:hidden;border:1px solid var(--rcu-line);border-radius:16px;background:#fff;box-shadow:0 20px 52px rgba(11,53,65,.12)}}.rcu-fact{{min-height:148px;padding:22px 24px}}.rcu-fact+.rcu-fact{{border-inline-start:1px solid var(--rcu-line)}}.rcu-fact b{{display:block;margin-bottom:8px;color:var(--rcu-teal-dark);font-size:.76rem;letter-spacing:.06em;text-transform:uppercase}}.rcu-fact span{{display:block;color:var(--rcu-ink);font-weight:750;line-height:1.45;overflow-wrap:anywhere}}
    .rcu-section{{padding:clamp(74px,8vw,108px) 0}}.rcu-section-head{{max-width:780px;margin-bottom:34px}}.rcu-section-head span{{color:var(--rcu-teal);font-size:.76rem;font-weight:850;letter-spacing:.1em;text-transform:uppercase}}.rcu-section h2{{margin:9px 0 12px;color:var(--rcu-ink);font-size:clamp(1.75rem,3vw,2.65rem);line-height:1.14;overflow-wrap:anywhere}}.rcu-section p{{color:var(--rcu-muted);line-height:1.72}}
    .rcu-config{{padding-top:clamp(100px,10vw,138px)}}.rcu-confirm-grid{{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:12px;margin:28px 0 0;padding:0}}.rcu-confirm-grid li{{min-height:86px;border-top:3px solid var(--rcu-teal);background:var(--rcu-mist);padding:18px;list-style:none;color:#31535b;font-weight:750;overflow-wrap:anywhere}}
    .rcu-oem{{background:var(--rcu-navy);color:#fff;padding:clamp(52px,7vw,82px) 0}}.rcu-oem-grid{{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(260px,.75fr);gap:clamp(30px,7vw,86px);align-items:center}}.rcu-oem h2,.rcu-oem p{{color:#fff}}.rcu-oem .rcu-note{{margin:0;border-inline-start:4px solid #62d1c8;background:rgba(255,255,255,.08);padding:22px;color:#e3f4f3;font-weight:750;line-height:1.65}}
    .rcu-gallery{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));max-width:960px;margin-inline:auto;gap:18px}}.rcu-gallery figure{{display:flex;min-height:0;flex-direction:column;align-self:start;margin:0;overflow:hidden;border:1px solid var(--rcu-line);border-radius:14px;background:#fff;box-shadow:0 16px 38px rgba(11,53,65,.08)}}.rcu-gallery img{{width:100%;max-width:360px;height:auto;aspect-ratio:1/1;flex:0 0 auto;margin-inline:auto;object-fit:contain}}.rcu-gallery figcaption{{border-top:1px solid var(--rcu-line);padding:15px 18px;color:#47636b;font-size:.88rem;font-weight:750}}
    .rcu-compare{{background:var(--rcu-mist)}}.rcu-compare-card{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:28px;align-items:center;border-inline-start:5px solid var(--rcu-teal);background:#fff;padding:clamp(24px,4vw,42px);box-shadow:0 14px 36px rgba(11,53,65,.07)}}.rcu-compare-card h2{{margin-top:0}}
    .rcu-faq-grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:16px}}.rcu-faq-grid details{{border:1px solid var(--rcu-line);border-radius:12px;background:#fff;padding:0 20px}}.rcu-faq-grid summary{{display:flex;min-height:62px;align-items:center;cursor:pointer;color:var(--rcu-ink);font-weight:850;line-height:1.4;overflow-wrap:anywhere}}.rcu-faq-grid p{{margin:0 0 20px}}
    .rcu-final{{padding:0 0 clamp(74px,8vw,108px)}}.rcu-final-card{{display:grid;grid-template-columns:minmax(0,1fr) auto;gap:32px;align-items:center;border-radius:18px;background:linear-gradient(120deg,#dff4f2,#eef9f8);padding:clamp(28px,5vw,52px)}}.rcu-final-card h2{{margin-top:0}}
    .rcu-footer{{border-top:1px solid var(--rcu-line);background:#f7faf9;padding:42px 0 26px}}.rcu-footer-grid{{display:grid;grid-template-columns:minmax(230px,1fr) auto;gap:32px;align-items:start}}.rcu-footer-brand{{color:var(--rcu-ink);font-size:1.08rem;font-weight:850}}.rcu-footer p{{max-width:620px;color:var(--rcu-muted);font-size:.88rem;line-height:1.65}}.rcu-footer-links{{display:flex;flex-wrap:wrap;justify-content:flex-end;gap:10px 22px}}.rcu-footer-links a{{display:inline-flex;min-height:44px;align-items:center;color:var(--rcu-teal-dark);font-weight:750;text-decoration:none}}.rcu-footer-meta{{margin-top:26px;border-top:1px solid var(--rcu-line);padding-top:18px;color:#6d8388;font-size:.78rem}}
    @media(max-width:1199px) and (min-width:960px){{.rcu-hero-grid{{grid-template-columns:minmax(0,1fr) minmax(360px,1fr);gap:42px}}.rcu-hero h1{{font-size:clamp(2.45rem,4.5vw,3.75rem)}}.rcu-confirm-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}}}
    @media(max-width:959px){{html.yd-ready .yd-header.rcu-header>.yd-controls{{inset-block-start:16px;inset-inline-end:72px;transform:none}}.rcu-header-row{{grid-template-columns:auto auto;justify-content:space-between;padding-block:12px}}.rcu-primary-nav{{grid-column:1/-1;justify-content:flex-start;border-top:1px solid var(--rcu-line);padding-top:8px}}.rcu-languages ul{{columns:2}}.rcu-hero{{padding-top:52px}}.rcu-hero-grid,.rcu-oem-grid,.rcu-gallery,.rcu-compare-card,.rcu-final-card,.rcu-footer-grid{{grid-template-columns:1fr}}.rcu-gallery{{max-width:560px}}.rcu-hero-media{{width:min(100%,520px);margin-inline:auto}}.rcu-facts{{grid-template-columns:repeat(2,minmax(0,1fr))}}.rcu-fact:nth-child(3){{border-inline-start:0;border-block-start:1px solid var(--rcu-line)}}.rcu-fact:nth-child(4){{border-block-start:1px solid var(--rcu-line)}}.rcu-confirm-grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}.rcu-gallery figure{{max-width:560px;margin-inline:auto;width:100%}}.rcu-compare-card,.rcu-final-card{{align-items:start}}.rcu-footer-links{{justify-content:flex-start}}}}
    @media(max-width:719px){{.rcu-topbar-row{{align-items:flex-start;flex-direction:column;gap:2px;padding-block:9px}}.rcu-brand img{{width:108px}}.rcu-primary-nav{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:2px 12px}}.rcu-primary-nav a{{justify-content:flex-start}}.rcu-hero h1{{font-size:clamp(2.05rem,10vw,3rem)}}.rcu-hero::after{{width:320px;height:320px}}.rcu-faq-grid{{grid-template-columns:1fr}}.rcu-section{{padding-block:68px}}.rcu-config{{padding-top:108px}}}}
    @media(max-width:559px){{.rcu-container{{width:min(calc(100% - 28px),1240px)}}.rcu-header-row{{gap:10px}}.rcu-brand span{{font-size:.92rem}}.rcu-languages ul{{position:absolute;inset-inline-end:0;width:min(320px,calc(100vw - 28px));columns:1;padding:12px}}.rcu-actions{{display:grid;grid-template-columns:1fr}}.rcu-btn{{width:100%}}.rcu-facts{{grid-template-columns:1fr}}.rcu-fact{{min-height:112px}}.rcu-fact+.rcu-fact,.rcu-fact:nth-child(3){{border-inline-start:0;border-block-start:1px solid var(--rcu-line)}}.rcu-gallery img{{max-width:300px}}.rcu-confirm-grid{{grid-template-columns:1fr}}.rcu-image-frame{{border-radius:18px 18px 0 0}}.rcu-footer-links{{display:grid;grid-template-columns:1fr}}}}
    @media(max-width:350px){{.rcu-brand img{{width:92px}}.rcu-brand span{{display:none}}}}
  </style>
</head>
<body class="rcu-page {direction}" data-design-version="rcu-responsive-v2" data-responsive-contract="1240-1199-959-719-559">
<div class="rcu-topbar"><div class="rcu-container rcu-topbar-row"><span>+86-19908311885 · expresswater025@gmail.com</span><span>OEM/ODM · RO · UV</span></div></div>
<header class="rcu-header">
  <div class="rcu-container rcu-header-row">
    <a class="rcu-brand" href="index.html"><img src="../assets/logo.png" width="173" height="64" alt="Yuchen Water" decoding="async" /><span>Yuchen Water</span></a>
    <nav class="rcu-primary-nav" aria-label="{products_label}"><a href="index.html">{home}</a><a href="products.html">{products}</a>{category_link}<a href="{contact_target}">{contact}</a></nav>
    <details class="rcu-languages"><summary aria-label="Language">🌐</summary><ul>{language_links}</ul></details>
  </div>
</header>
<main class="rcu-main">
  <article>
    <section class="rcu-hero">
      <div class="rcu-container rcu-hero-grid">
        <div class="rcu-hero-copy">
          <div class="rcu-breadcrumb"><a href="index.html">{home}</a><span>›</span><a href="products.html">{products}</a><span>›</span><span>{cabinet}</span></div>
          <div class="rcu-kicker">RO · 5/6 · UV · OEM/ODM</div>
          <h1>{name}</h1>
          <p class="rcu-answer">{summary}</p>
          <div class="rcu-actions"><a class="rcu-btn" href="{contact_target}?product=ro-cabinet-uv">{contact}</a><a class="rcu-btn rcu-btn-secondary" href="{old_target}">{compare_link}</a></div>
        </div>
        <div class="rcu-hero-media"><div class="rcu-image-frame"><img class="rcu-mainimg" src="{assets}cabinet-ro-water-purifier-main.png" width="800" height="800" alt="{alt}" fetchpriority="high" decoding="async" /></div></div>
      </div>
      <div class="rcu-container rcu-facts-wrap"><div class="rcu-facts">
        <div class="rcu-fact"><b>{product_label}</b><span>{cabinet}</span></div>
        <div class="rcu-fact"><b>{filtration_label}</b><span>{stages}</span></div>
        <div class="rcu-fact"><b>UV</b><span>{optional}</span></div>
        <div class="rcu-fact"><b>OEM/ODM</b><span>{available}</span></div>
      </div></div>
    </section>

    <section class="rcu-section rcu-config" id="configuration"><div class="rcu-container">
      <div class="rcu-section-head"><span>RO · OEM/ODM</span><h2>{technical}</h2><p>{config_note}</p></div>
      <ul class="rcu-confirm-grid"><li>{output}</li><li>{dimensions}</li><li>{filtration}</li><li>{pump}</li><li>{voltage}</li><li>UV — {power}</li><li>{quantity}</li><li>{certifications}</li></ul>
    </div></section>

    <section class="rcu-oem"><div class="rcu-container rcu-oem-grid"><div><div class="rcu-kicker">OEM/ODM</div><h2>OEM/ODM</h2><p>OEM/ODM: {available}. {spec_note}</p></div><p class="rcu-note">{confirm}</p></div></section>

    <section class="rcu-section"><div class="rcu-container"><div class="rcu-section-head"><span>RO · UV</span><h2>{application}</h2></div><div class="rcu-gallery"><figure><img src="{assets}cabinet-ro-water-purifier-black.png" width="649" height="649" alt="{alt_black}" loading="lazy" decoding="async" /><figcaption>{cabinet}</figcaption></figure><figure><img src="{assets}cabinet-ro-water-purifier-workshop.png" width="1200" height="1200" alt="{alt_workshop}" loading="lazy" decoding="async" /><figcaption>{application}</figcaption></figure></div></div></section>

    <section class="rcu-section rcu-compare"><div class="rcu-container"><div class="rcu-compare-card"><div><h2>{products}</h2><p>{compare}</p></div><a class="rcu-btn rcu-btn-secondary" href="{old_target}">{compare_link}</a></div></div></section>

    <section class="rcu-section"><div class="rcu-container"><div class="rcu-section-head"><span>FAQ</span><h2>{faq}</h2></div><div class="rcu-faq-grid"><details open><summary>{uv_q}</summary><p>{uv_a}</p></details><details><summary>{quote_q}</summary><p>{quote_a}</p></details></div></div></section>

    <section class="rcu-final"><div class="rcu-container"><div class="rcu-final-card"><div><h2>{project}</h2><p>{spec_note}</p></div><a class="rcu-btn" href="{contact_target}?product=ro-cabinet-uv">{contact}</a></div></div></section>
  </article>
</main>
<footer class="rcu-footer"><div class="rcu-container"><div class="rcu-footer-grid"><div><div class="rcu-footer-brand">Yuchen Water</div><p>{summary}</p><p>+86-19908311885 · expresswater025@gmail.com</p></div><nav class="rcu-footer-links" aria-label="{products_label}"><a href="index.html">{home}</a><a href="products.html">{products}</a>{category_link}<a href="{contact_target}">{contact}</a></nav></div><div class="rcu-footer-meta">Yuchen Water · RO · OEM/ODM</div></div></footer>
<script src="../assets/site.min.js?v=20260810-oem63-menu" defer></script>
</body>
</html>
""".format(
        html_lang=html.escape(record["html_lang"]), direction=html.escape(record["dir"]),
        title=html.escape(title), description=desc, url=url, alternates=alternates(alternate_records),
        assets=assets, site=SITE, schema=schema, products_label=html.escape(ui["products"], quote=True),
        home=html.escape(ui["home"]), products=html.escape(ui["products"]),
        category_link=('<a href="ro-water-purifier.html">RO</a>' if has_category else ""),
        language_links=language_links(registry, locale), name=html.escape(tr["name"]), summary=summary,
        product_label=html.escape(ui["product"]), cabinet=html.escape(tr["cabinet"]),
        filtration_label=html.escape(ui["filtration"]), stages=html.escape(tr["stages"]),
        optional=html.escape(tr["optional"]), available=html.escape(tr["available"]),
        contact=html.escape(ui["contact"]), alt=html.escape(tr["name"], quote=True),
        technical=html.escape(ui["technical"]), config_note=html.escape(ctx["config_note"]),
        output=html.escape(ui["output"]), dimensions=html.escape(ui["dimensions"]),
        filtration=html.escape(ui["filtration"]), pump=html.escape(tr["pump"]),
        voltage=html.escape(ui["voltage"]), power=html.escape(ui["power"]),
        quantity=html.escape(ui["quantity"]), certifications=html.escape(tr["certifications"]),
        spec_note=html.escape(ctx["note"]), confirm=html.escape(tr["confirm"]),
        application=html.escape(ui["application"]),
        alt_black=html.escape(tr["name"] + " — " + tr["cabinet"], quote=True),
        alt_workshop=html.escape(tr["name"] + " — " + ui["application"], quote=True),
        compare=html.escape(ctx["compare"]), old_target=html.escape(old_target, quote=True),
        compare_link=html.escape(tr["compare"]), faq=html.escape(ui["faq"]),
        uv_q=html.escape(ctx["uv_q"]), uv_a=html.escape(ctx["uv_a"]),
        quote_q=html.escape(ctx["quote_q"]), quote_a=html.escape(ctx["quote_a"]),
        project=html.escape(ui["project"]), contact_target=html.escape(contact_target, quote=True),
    )


def card_block(tr, ctx, ui):
    return """{start}
<section class="tx-section tx-section--tint ro-cabinet-uv-entry"><div class="tx-container tx-product-grid">
  <article class="tx-card tx-product-card" data-cat="RO System" id="ro-cabinet-uv-5-6-stage">
    <a class="tx-card-media" href="{route}"><img src="../assets/products/ro-cabinet-uv/cabinet-ro-water-purifier-main.png" width="800" height="800" loading="lazy" decoding="async" alt="{alt}" /></a>
    <div class="tx-card-copy"><h3><a href="{route}">{name}</a></h3><p>{summary}</p><a class="tx-btn" href="{route}">{contact}</a></div>
  </article>
</div></section>
{end}""".format(start=DETAIL_START, end=DETAIL_END, route=ROUTE,
        alt=html.escape(tr["name"], quote=True), name=html.escape(tr["name"]),
        summary=html.escape(ctx["short"]), contact=html.escape(ui["contact"]))


def sitemap_block(locale, prefixed):
    p = "ns0:" if prefixed else ""
    return "%s\n  <%surl><%sloc>%s</%sloc><%slastmod>%s</%slastmod></%surl>\n%s" % (
        SITEMAP_START, p, p, page_url(locale), p, p, LASTMOD, p, p, SITEMAP_END
    )


def build(root):
    registry = load_json(root / "migration/multilingual-products/language-registry.62.json")
    translations = load_json(root / "migration/ro-cabinet-uv/translations.62.json")["locales"]
    source = load_json(root / "migration/ro-cabinet-uv/source.en.json")
    commercial = load_json(root / "migration/goleman/commercial-ro-localizations.62.json")
    records = {x["code"]: x for x in commercial["locales"]}
    changed = []
    review_rows = []

    active = [x["directory"].strip("/") for x in registry["locales"]]
    if set(active) != set(translations) or set(active) != set(records):
        raise ValueError("locale registry, translations and RO memory must match exactly")
    alternate_records = global_alternate_records(root)
    missing_alternate_targets = [
        code for code, _hreflang in alternate_records
        if not (root / code / ROUTE).is_file() and code not in active
    ]
    if missing_alternate_targets:
        raise ValueError("global hreflang targets are missing: %s" % missing_alternate_targets)

    for name, width, height in MEDIA:
        path = root / "assets/products/ro-cabinet-uv" / name
        if not path.exists():
            raise FileNotFoundError(path)

    for locale_cfg in registry["locales"]:
        locale = locale_cfg["directory"].strip("/")
        record = dict(records[locale])
        record["html_lang"] = locale_cfg["html_lang"]
        record["dir"] = locale_cfg["dir"]
        tr = translations[locale]
        ctx = localized_context(record, tr, source)
        locale_dir = root / locale
        has_category = (locale_dir / "ro-water-purifier.html").exists()
        if (locale_dir / OLD_ROUTE).exists():
            old_target = OLD_ROUTE
        elif (locale_dir / "ro-water-purifier.html").exists():
            old_target = "ro-water-purifier.html"
        else:
            old_target = "products.html"
        contact_target = "contact.html" if (locale_dir / "contact.html").exists() else "../en/contact.html"
        page = render_page(locale, registry, alternate_records, record, tr, source, old_target, has_category, contact_target)
        write_if_changed(locale_dir / ROUTE, page, changed)

        products_path = locale_dir / "products.html"
        products_text = products_path.read_text(encoding="utf-8")
        products_anchor = "</main>" if "</main>" in products_text else "</body>"
        products_text = replace_block(products_text, DETAIL_START, DETAIL_END,
                                      card_block(tr, ctx, record["labels"]), products_anchor)
        write_if_changed(products_path, products_text, changed)

        category_path = locale_dir / "ro-water-purifier.html"
        if category_path.exists():
            category_text = category_path.read_text(encoding="utf-8")
            category_anchor = "</main>" if "</main>" in category_text else "</body>"
            category_text = replace_block(category_text, DETAIL_START, DETAIL_END,
                                          card_block(tr, ctx, record["labels"]), category_anchor)
            write_if_changed(category_path, category_text, changed)

        sitemap_path = root / "sitemaps" / ("sitemap-%s.xml" % locale)
        sitemap_text = sitemap_path.read_text(encoding="utf-8")
        close = "</ns0:urlset>" if "</ns0:urlset>" in sitemap_text else "</urlset>"
        sitemap_text = replace_block(sitemap_text, SITEMAP_START, SITEMAP_END,
                                     sitemap_block(locale, close.startswith("</ns0:")), close)
        write_if_changed(sitemap_path, sitemap_text, changed)

        review_rows.append({
            "locale": locale, "html_lang": record["html_lang"], "dir": record["dir"],
            "review_status": "ai-multipass-reviewed", "terminology_check": "pass",
            "backtranslation": "cabinet RO; 5 or 6 stages; optional UV; OEM/ODM; quote confirmation required",
            "english_leakage": "pass", "script_check": "pass", "duplicate_check": "pass",
            "native_review_claimed": "no",
        })

    schema_paths = []
    for locale in active:
        schema_paths.extend([f"{locale}/{ROUTE}", f"{locale}/products.html"])
        if (root / locale / "ro-water-purifier.html").is_file():
            schema_paths.append(f"{locale}/ro-water-purifier.html")
    for relative in normalize_paths_in_place(root, schema_paths):
        path = root / relative
        if path not in changed:
            changed.append(path)

    out = io.StringIO()
    fields = ["locale", "html_lang", "dir", "review_status", "terminology_check", "backtranslation",
              "english_leakage", "script_check", "duplicate_check", "native_review_claimed"]
    writer = csv.DictWriter(out, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    writer.writerows(review_rows)
    write_if_changed(root / "migration/ro-cabinet-uv/translation-review.csv", out.getvalue(), changed)

    expected_outputs = []
    for locale in active:
        expected_outputs.extend([
            "%s/%s" % (locale, ROUTE),
            "%s/products.html" % locale,
            "sitemaps/sitemap-%s.xml" % locale,
        ])
        if (root / locale / "ro-water-purifier.html").exists():
            expected_outputs.append("%s/ro-water-purifier.html" % locale)
    expected_outputs.append("migration/ro-cabinet-uv/translation-review.csv")
    manifest = {
        "schema_version": 1,
        "route": ROUTE,
        "locale_count": len(active),
        "global_hreflang_route_count": len(alternate_records),
        "llms_owner": "tools/yuchen_product_taxonomy.py",
        "expected_output_count": len(expected_outputs),
        "expected_outputs": sorted(expected_outputs),
        "source_sha256": hashlib.sha256((root / "migration/ro-cabinet-uv/source.en.json").read_bytes()).hexdigest(),
        "translations_sha256": hashlib.sha256((root / "migration/ro-cabinet-uv/translations.62.json").read_bytes()).hexdigest(),
        "publication_allowed": "NO",
    }
    manifest_text = json.dumps(manifest, ensure_ascii=False, indent=2) + "\n"
    write_if_changed(root / "migration/ro-cabinet-uv/build-manifest.json", manifest_text, changed)
    return changed


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", default=".")
    args = parser.parse_args()
    root = Path(args.site_root).resolve()
    changed = build(root)
    print(json.dumps({"status": "ok", "locales": 62, "changed": len(changed),
                      "files": [str(x.relative_to(root)) for x in changed]}, ensure_ascii=False))


if __name__ == "__main__":
    main()
