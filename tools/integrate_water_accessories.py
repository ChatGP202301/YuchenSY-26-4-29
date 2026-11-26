"""Build localized accessory details and bidirectional selection cards in the local site."""
import argparse
import csv
import json
import re
import shutil
from urllib.parse import quote, urlencode
from html import escape, unescape
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--english-only", action="store_true")
ENGLISH_ONLY = parser.parse_args().english_only

SITE = Path(__file__).resolve().parents[1]
DATA = SITE / "migration/water-accessories"
FACTS = json.loads((DATA / "facts.json").read_text())
COPY = list(csv.reader((DATA / "copy.psv").read_text().splitlines(), delimiter="|"))
RO = "product-commercial-mid-cabinet-ro-water-purifier-built-in-pressure-tank-400g-1600g.html"
RO_SELECTION = (
    "product-built-in-pressure-tank-ro.html",
    "product-pump-free-five-stage-ro-water-purifier.html",
    "product-smart-ro-water-purifier-400g-1200g.html",
)
GROUP = "product-housing-filter.html"
GUIDE = "water-accessory-selection-guide.html"
INDEX = "water-accessories.html"
ASSETS = SITE / "assets/water-accessories"
ASSETS.mkdir(exist_ok=True)
for image in (DATA / "preview/images").glob("*.webp"):
    shutil.copyfile(image, ASSETS / image.name)

CSS = """<style>.wa-wrap{max-width:1120px;margin:auto;padding:32px 20px;overflow-wrap:anywhere}.wa-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,210px),1fr));gap:1.25rem}.wa-card{padding:1rem;background:#fff;border:1px solid #d5dfde;border-radius:12px}.wa-card a{display:grid;gap:.7rem}.wa-card img{width:100%;height:145px;object-fit:contain}.wa-card p{font-size:.95rem}.wa-wrap figure{margin:1rem 0}.wa-wrap figure img{max-width:100%;max-height:460px;object-fit:contain}.wa-wrap textarea{width:100%;min-height:7em}.wa-wrap td,.wa-wrap th{padding:.4rem}.wa-wrap section{margin-block:2rem}</style>"""
ENGLISH = json.loads((DATA / "product-copy.en.json").read_text())
def clean_marks(value):
    for original, replacement in (("1寸外丝","1″ ♂"),("1寸","1″"),("4分","1/2″"),("3分","3/8″"),("2分","1/4″")):
        value=value.replace(original,replacement)
    return value

CSS=CSS.replace("</style>", """
.wa-wrap .wa-hero{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:center;gap:clamp(20px,4vw,60px);margin:28px 0 42px}
.wa-hero figure{margin:0;padding:16px;background:#f5f6f4;border-radius:12px}.wa-hero figure img{display:block;width:100%;height:clamp(220px,28vw,360px);object-fit:contain}.wa-hero figcaption{font-size:.85rem;color:#515d59;margin-top:12px}
.wa-hero dl{margin:20px 0}.wa-hero dl div{border-top:1px solid #d9dfda;padding:8px 0;display:grid;grid-template-columns:40% 1fr;gap:8px}.wa-hero dt{font-weight:bold}.wa-hero dd{margin:0;min-inline-size:0}.wa-hero dt{min-inline-size:0}.wa-wrap bdi{direction:ltr;unicode-bidi:isolate}.wa-wrap .product-card{min-inline-size:0;overflow-wrap:anywhere}.wa-wrap .wa-copy{max-width:78ch}.wa-wrap .wa-family{font-size:.9rem;color:#526d63;margin-bottom:8px}
.wa-related-compact{max-inline-size:420px}.wa-related-compact .product-grid{grid-template-columns:minmax(0,1fr)!important}.wa-related-compact .product-card{display:block!important;min-height:0}.wa-related-compact .product-img-wrap{height:clamp(120px,38vw,168px)!important;min-height:0;aspect-ratio:auto!important;border-right:0}.wa-related-compact .product-img-wrap img{padding:10px!important}
@media(max-width:720px){.wa-wrap .wa-hero{grid-template-columns:1fr}.wa-hero figure img{height:240px}} </style>""")

def title(source):
    return re.sub("<[^>]*>", "", re.search(r"<h1\b[^>]*>(.*?)</h1>", source, re.S)[1]).strip()

def card(route, name, image, note=""):
    return (f'<article class="product-card"><a href="{route}" class="product-img-wrap">'
            f'<img loading="lazy" decoding="async" src="{image}" alt="{name}"></a>'
            f'<div class="product-body"><h3><a href="{route}" class="product-title-link">{name}</a></h3>'
            f'<p>{note}</p></div></article>')

def section(cards):
    return '<div class="product-grid">' + ''.join(cards) + '</div>'


def inject(path, block):
    source = path.read_text()
    source = re.sub(r'<section id="housing-union-accessory".*?</section>', '', source, flags=re.S)
    source = re.sub(r'<!-- water-accessories:start -->.*?<!-- water-accessories:end -->','',source,flags=re.S)
    assert '</main>' in source
    path.write_text(source.replace('</main>', '<!-- water-accessories:start -->'+CSS+'<section class="wa-wrap">'+block+'</section><!-- water-accessories:end --></main>',1))

labels={row[0]:row[1:] for row in csv.reader((DATA/"relation-labels.psv").read_text().splitlines(),delimiter="|")}
extra_copy={}
extra_path=DATA/'product-copy.extra.psv'
if extra_path.exists():
    for code,category,intro,*fields in csv.reader(extra_path.read_text().splitlines(),delimiter='|'):
        first,second,third,heading,detail,photo=fields
        spec=dict(item.split(': ',1) for item in (first,second,third))
        extra_copy.setdefault(code,[]).append(dict(category=category,intro=intro,spec=spec,heading=heading,detail=detail,photo=photo))
confirmed=set()  # Add a model pair only after its interfaces and operating conditions are documented.
matrix=[]
accessory_languages = ['en'] if ENGLISH_ONLY else sorted({row[0] for row in COPY})
for row in sorted(COPY, key=lambda row: row[0]!='en'):
    lang,*v=row
    if ENGLISH_ONLY and lang != 'en':
        continue
    v=list(map(clean_marks,v))
    copy_path=DATA/f'product-copy.{lang}.json'
    detailed=copy_path.is_file() or lang in extra_copy
    content=json.loads(copy_path.read_text()) if copy_path.is_file() else extra_copy.get(lang,ENGLISH)
    folder=SITE/lang
    template=(folder/'product-built-in-pressure-tank-ro.html').read_text()
    tag=re.search(r'<html[^>]*>',template)[0]
    header=re.search(r'<header\b.*?</header>',template,re.S)[0]
    footer_match = re.search(r'<footer\b.*?</footer>', template, re.S)
    if footer_match is None:
        footer_match = re.search(r'<footer\b.*?</footer>', (folder / 'products.html').read_text(), re.S)
    footer = footer_match[0]
    def render(route,name,description,body,kind,image_url=None):
        url=f'https://www.yuchensy.com/{lang}/{route}'
        alternate = ''.join(
            f'<link rel="alternate" hreflang="{code}" href="https://www.yuchensy.com/{code}/{route}">'
            for code in accessory_languages
        )
        alternate += f'<link rel="alternate" hreflang="x-default" href="https://www.yuchensy.com/en/{route}">'
        schema_type = 'WebPage' if lang == 'en' and kind == 'Product' else kind
        schema_data = {'@context':'https://schema.org','@type':schema_type,'name':unescape(name),'description':description,'url':url}
        image_meta = ''
        if image_url:
            schema_data['image'] = image_url
            image_meta = f'<meta property="og:image" content="{escape(image_url)}"><meta name="twitter:image" content="{escape(image_url)}">'
        schema = json.dumps(schema_data, ensure_ascii=False)
        nav=header.replace('product-built-in-pressure-tank-ro.html',route)
        if ENGLISH_ONLY:
            nav = re.sub(r'<div class="lang-switcher">.*?(?=<a href="contact.html" class="btn btn-gold">)',
                         '', nav, count=1, flags=re.S)
        crumb=f'<nav><a href="products.html">{catalog}</a> › <a href="{INDEX}">{v[5]}</a></nav>'
        measurement = ''
        site_script = '../assets/site.min.js'
        tracking = ''
        if lang == 'en' and kind == 'Product':
            product_id = escape(route.removesuffix('.html'))
            item = {'item_id': product_id, 'item_name': unescape(name), 'item_category': 'water-accessories'}
            context = json.dumps({'detail': item}).replace('<', r'\u003c')
            measurement = f'<script>window.YUCHEN_PRODUCT_MEASUREMENT = {context};</script>'
            site_script += '?v=20261126-accessories'
            tracking = f' data-product-id="{product_id}" data-product-slug="{product_id}" data-product-family="water-accessories"'
        html=f'<!doctype html>{tag}<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,follow"><title>{name} | Yuchen Water</title><meta name="description" content="{escape(description)}"><link rel="canonical" href="{url}">{alternate}{image_meta}<link rel="stylesheet" href="../assets/styles.min.css">{CSS}<script type="application/ld+json">{schema}</script>{measurement}</head><body{tracking}>{nav}<main class="wa-wrap">{crumb}<h1>{name}</h1>{body}</main>{footer}<script defer src="{site_script}"></script></body></html>'
        (folder/route).write_text(clean_marks(html))
    catalog=title((folder/'products.html').read_text())
    cards=[card(f['id']+'.html',v[i],f'../assets/water-accessories/{i+1}-480.webp') for i,f in enumerate(FACTS)]
    by_device={}
    for i,f in enumerate(FACTS):
        route=f['id']+'.html'
        source=(DATA/'preview'/lang/route).read_text()
        body=re.search(r'</h1>(.*?)</main>',source,re.S)[1].split('<nav>')[0].replace('../images/','../assets/water-accessories/').replace('guide.html#',GUIDE+'#')
        routes=[]
        if i in (0,1):
            for size in (10,20):
                routes.extend([f'{size}-inch-large-body-{color}-filter-housing.html' for color in ('blue','clear')])
                routes.append(f'{size}-inch-black-bb-filter-housing.html')
            routes=[r for r in routes if (folder/r).exists()]
        if i==2:
            routes=[RO]
        if lang == "en" and i in (3, 4):
            routes = RO_SELECTION
        devices=[]
        for target in routes:
            text=(folder/target).read_text()
            main=re.search(r'<main\b.*?</main>',text,re.S)[0]
            image=re.search(r'<img\b[^>]*?\bsrc="([^"]+)"',main)[1]
            if lang == "en" and target == "product-smart-ro-water-purifier-400g-1200g.html":
                # Use the reference exterior published on the English Smart RO detail.
                image = "https://www.yuchensy.com/assets/products/under-sink-ro-800g-reference-exterior.jpg"
            else:
                assert (folder/image).is_file(),image
            evidence = ('0.1–0.4 MPa' if i == 2 else '1″' if i in (0, 1) else 'Model-specific circuit drawing' if i == 3 else 'Feed-line layout and outside diameter')
            status=labels[lang][int((route,target) in confirmed)]
            note=status+' · '+evidence+' · '+v[6+i]
            if lang == "en":
                reason = [
                    "Compare the housing head’s 1-inch port option with the union’s male thread before choosing a pipe-side connection.",
                    "The elbow turns the feed tube through 90°. Select the housing’s 1-inch port option, then match the 1/2″ or 3/8″ tube end.",
                    "This RO unit specifies 0.1–0.4 MPa at its inlet. Compare the valve’s outlet setting with that range and size both connections.",
                    "For this RO machine, request its configuration-specific water circuit diagram. Verify the four tube destinations and switching conditions before choosing a replacement valve.",
                    "For this RO machine, identify the feed tube and measure its outside diameter. Confirm the shutoff location, trigger clearance and reset procedure before ordering."
                ][i]
                note = status + ". " + reason
            devices.append(card(target,(labels[lang][2]+" · " if target==GROUP else "")+title(text),image,note))
            by_device.setdefault(target,[]).append(card(route,v[i],f'../assets/water-accessories/{i+1}-480.webp',note))
            matrix.append((lang,route,target,evidence))
        product=content[i]
        src=f'../assets/water-accessories/{i+1}'
        intro=product["intro"] if detailed else v[6+i]
        caption=product["photo"] if detailed else v[i]
        height = (601, 444, 521, 596, 430)[i]
        dimensions = f' width="960" height="{height}"' if lang == "en" else ""
        picture=f'<figure><img src="{src}-960.webp"{dimensions} srcset="{src}-480.webp 480w, {src}-960.webp 960w" sizes="(max-width:720px) 95vw, 520px" alt="{escape(caption)}"><figcaption>{caption}</figcaption></figure>'
        spec = {k: re.sub(r'(\d+/\d+″)',r'<bdi dir="ltr">\1</bdi>',escape(value)) for k,value in product['spec'].items()}
        rows=''.join(f'<div><dt>{key}</dt><dd>{val}</dd></div>' for key,val in spec.items())
        facts_html=f'<dl>{rows}</dl>' if detailed else f'<p><bdi>{clean_marks(f["label"])}</bdi></p>'
        family=f'<p class="wa-family">{product["category"]}</p>' if detailed else ''
        cta=f'<a class="btn btn-gold" href="mailto:expresswater025@gmail.com?subject={quote(v[i])}&amp;body={quote(v[12])}">{v[11]}</a>'
        if lang == "en":
            query = urlencode({"product": v[i], "product_family": "water-accessories",
                               "product_slug": f["id"], "source_page": route,
                               "product_id": f["id"], "cta_location": "product_hero"})
            cta = f'<a class="btn btn-gold" data-primary-cta data-cta-location="product_hero" href="contact.html?{escape(query)}#quoteForm">{v[11]}</a>'
        body=f'<section class="wa-hero">{picture}<div>{family}<p>{intro}</p>{facts_html}{cta}</div></section>'
        if detailed:
            body+=f'<section class="wa-copy"><h2>{product["heading"]}</h2><p>{product["detail"]}</p></section>'
        if lang == "en":
            body += f'<section class="wa-copy"><h2>What to send for a quote</h2><p>{escape(product["inquiry_checklist"])}</p></section>'
        body+=f'<p><a href="{GUIDE}#{f["id"]}">{v[5]}</a></p>'
        if devices:
            related = ({'en':'<h2>Related equipment</h2>','fr':'<h2>Équipements associés</h2>','es':'<h2>Equipos relacionados</h2>','de':'<h2>Verwandte Geräte</h2>','ar':'<h2>الأجهزة ذات الصلة</h2>','ja':'<h2>関連機器</h2>','ru':'<h2>Связанное оборудование</h2>'}.get(lang,''))+section(devices)
            body += f'<section class="wa-related-compact">{related}</section>' if i == 2 and lang == "en" else related
        image_url = f'https://www.yuchensy.com/assets/water-accessories/{i+1}-960.webp' if lang == 'en' else None
        render(route,v[i],intro,body,'Product',image_url)
    for target,items in by_device.items():
        inject(folder/target,section(items))
    if GROUP not in by_device:
        inject(folder/GROUP,section(cards[:2]))
    directory_title = 'Water Treatment Accessories' if lang == 'en' else v[5]
    inject(folder/'products.html',f'<h2><a href="{INDEX}">{directory_title}</a></h2>'+section(cards))
    guide=(DATA/'preview'/lang/'guide.html').read_text()
    render(GUIDE,v[5],v[12],re.search(r'</h1>(.*?)</main>',guide,re.S)[1],'Article')
    render(INDEX,directory_title,v[12],section(cards)+f'<p><a href="{GUIDE}">{v[5]}</a></p>','CollectionPage')
if ENGLISH_ONLY:
    print(f'{len(matrix)} English selection relationships')
    raise SystemExit(0)

entries=''.join(f'<tr><td>{l}</td><td><a href="../../{l}/{a}">{a}</a></td><td><a href="../../{l}/{b}">{b}</a></td><td>{e}</td><td>选型相关，订购前核对</td></tr>' for l,a,b,e in matrix)
(DATA/'equipment-links.html').write_text('<meta charset="utf-8"><title>配件与设备关系</title><h1>配件与设备关系</h1><p>四接口阀待原厂回路与端口图。漏水保护器待整机进水接管与断水位置资料。</p><table>'+entries+'</table>')
print(len(matrix),'localized selection relationships')

# Local language review index links directly to the integrated catalog and product routes.
names = dict(re.findall(r'<a href="../([^/]+)/[^"]+" class="lang-option"[^>]*>([^<]+)', (SITE/'en/products.html').read_text()))
language_rows=[]
for code,*terms in sorted(COPY):
    links=' · '.join(f'<a href="{code}/{fact["id"]}.html">{escape(terms[i])}</a>' for i,fact in enumerate(FACTS))
    language_rows.append(f'<section><h2><a href="{code}/{INDEX}">{names.get(code,code)} ({code})</a></h2><p>{links}</p></section>')
(SITE/'en/accessory-language-review.html').write_text('<!doctype html><html lang="zh"><head><base href="../"><meta charset="utf-8"><meta name="robots" content="noindex"><meta name="viewport" content="width=device-width,initial-scale=1"><title>配件多语言预览</title><style>body{max-width:900px;margin:auto;padding:24px;font:16px/1.7 system-ui}section{border-bottom:1px solid #ddd}a{color:#18575b}</style></head><body><h1>配件多语言预览</h1><p>点击语言进入目录，或点击产品名称直接查看详情。</p>'+''.join(language_rows)+'</body></html>')
