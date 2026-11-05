from pathlib import Path
import json,re,html
from urllib.parse import quote
R=Path(__file__).resolve().parents[2];T=Path(__file__).resolve().parent
products=json.loads((T/'products.json').read_text())[:14]
base=(R/'en/product-housing-filter.html').read_text()
slugs=[]
for p in products:
 slug=re.sub('[^a-z0-9]+','-',p['name'].lower()).strip('-')+'.html';slugs.append(slug)
for i,(p,slug) in enumerate(zip(products,slugs)):
 card=re.search(r'<article class="fh-card" id="'+p['id']+r'".*?</article>',base,re.S).group()
 card=card.replace('<h3>'+html.escape(p['name'])+'</h3>','<h2>Specifications and configuration</h2>')
 other=[(products[j],slugs[j]) for j in range(len(products)) if j!=i and products[j]['kind']==p['kind']][:3]
 related=''.join(f'<li><a href="{s}">{html.escape(x["name"])}</a></li>' for x,s in other)
 guide=f'<section class="fh-guide"><h2>Buying and installation questions</h2><h3>Which connections are listed for this configuration?</h3><p>{html.escape("; ".join(p["ports"]))}. Confirm the mating connection and thread standard before ordering; size alone does not establish compatibility.</p><h3>What is the packing quantity?</h3><p>This {html.escape(p["name"])} is listed as {html.escape(p["pack"])}. This is a packing quantity, not a minimum order quantity. Confirm carton dimensions, weight and order quantity with your quotation.</p><h3>Are cartridges included?</h3><p>No. Cartridges are purchased separately. Discuss PP sediment, CTO carbon-block or PVDF cartridges against the housing fit and your treatment requirements. Stage count alone does not establish filtration performance.</p><h3>What should I confirm before installation?</h3><p>The {html.escape(p["size"])} designation describes the housing size, not overall assembly dimensions. Confirm cartridge fit, component materials, operating pressure, cold-water temperature, required flow and service clearance. Isolate the supply and release pressure before maintenance. Black is an alternative colour subject to configuration availability; the reference photograph stays unchanged.</p></section>' 
 intro=f'Compare the available connections and packing for this {p["size"]} configuration. '+p['description']
 main=f'''<main class="fh-page"><div class="fh-wrap"><nav aria-label="Breadcrumb"><a href="products.html">Products</a> / <a href="product-housing-filter.html">Housing configurations</a> / {html.escape(p['name'])}</nav><header class="fh-hero"><p class="fh-kicker">Cold-water filter housing · cartridges sold separately</p><h1>{html.escape(p['name'])}</h1><p>{html.escape(intro)}</p></header>{card}<section><h2>Compare related configurations</h2><ul>{related}</ul><a href="product-housing-filter.html">Compare all 14 housing configurations</a></section>{guide}</div></main>'''
 page=re.sub(r'<main\b.*?</main>',lambda _:main,base,flags=re.S)
 title=p['name']+' | Yuchen Water';desc=f'{p["name"]}. {p["size"]}; {p["pack"]}. Compare connection options and request a quotation. Filter cartridges sold separately.'
 page=re.sub(r'<title>.*?</title>','<title>'+html.escape(title)+'</title>',page,flags=re.S)
 page=re.sub(r'(<meta name="description" content=")[^"]*',lambda m:m[1]+html.escape(desc,quote=True),page)
 page=re.sub(r'(<link rel="canonical" href=")[^"]*',lambda m:m[1]+'https://www.yuchensy.com/en/'+slug,page)
 page=re.sub(r'(<meta property="og:image" content=")[^"]*',lambda m:m[1]+'https://www.yuchensy.com/assets/products/housing-expansion-white/'+p['image']+'.webp',page)
 page=re.sub(r'<link\b[^>]*hreflang=[^>]*>','',page)
 page=re.sub(r'(<meta property="og:(?:url|title|description)" content=")[^"]*',lambda m:m[1]+html.escape(('https://www.yuchensy.com/en/'+slug if 'url' in m[1] else title if 'title' in m[1] else desc),quote=True),page)
 page=re.sub(r'<script type="application/ld\+json">.*?</script>','',page,flags=re.S)
 schema={'@context':'https://schema.org','@type':'Product','name':p['name'],'url':'https://www.yuchensy.com/en/'+slug,'image':'https://www.yuchensy.com/assets/products/housing-expansion-white/'+p['image']+'.webp','description':desc,'additionalProperty':[{'@type':'PropertyValue','name':'Housing size designation','value':p['size']},{'@type':'PropertyValue','name':'Packing quantity','value':p['pack']}]}
 page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(schema)+'</script></head>')
 (R/'en'/slug).write_text(page)
# Add static discovery links and a progressive search input; preserve full text without JS.
for p,slug in zip(products,slugs):
 needle='<h3>'+html.escape(p['name'])+'</h3>'
 base=base.replace(needle,needle+f'<p><a href="{slug}">View full product details →</a></p>')
# Collection displays product entries; full descriptions belong on each dedicated URL.
for p,slug in zip(products,slugs):
 card=f'<article class="fh-card fh-directory-card" id="{p["id"]}"><a class="fh-product-link" href="{slug}"><img src="../assets/products/housing-expansion-white/{p["image"]}.webp" alt="{html.escape(p["name"])}" width="1254" height="1254" loading="lazy"><h3>{html.escape(p["name"])}</h3></a><p>{html.escape(p["size"])} · {html.escape(p["pack"])}</p><a class="fh-quote" href="{slug}">View this product</a></article>'
 base=re.sub(r'<article class="fh-card" id="'+p['id']+r'".*?</article>',lambda _:card,base,flags=re.S)
base=base.replace('<section id="housing-products">','<div class="fh-search"><label for="fh-search">Search housings by size, colour, stages or mounting style</label><input id="fh-search" type="search" placeholder="Try: 20-inch, clear, support frame" aria-describedby="fh-search-count"><p id="fh-search-count" aria-live="polite">14 housings and 2 accessories</p></div><section id="housing-products">')
(R/'en/product-housing-filter.html').write_text(base);(R/'tools/templates/housing-filter-en.html').write_text(base)
(T/'url-manifest.json').write_text(json.dumps([dict(product=p['id'],name=p['name'],url='https://www.yuchensy.com/en/'+s,keyword=p['name'],intent='Compare specifications, select configuration and request quotation') for p,s in zip(products,slugs)],indent=2))
import xml.etree.ElementTree as ET
site=R/'sitemaps/sitemap-en.xml'; tree=ET.fromstring(site.read_text()); ns='http://www.sitemaps.org/schemas/sitemap/0.9'; existing={n.text for n in tree.iter() if n.tag=='{'+ns+'}loc'}
for slug in slugs:
 url='https://www.yuchensy.com/en/'+slug
 if url not in existing:
  node=ET.SubElement(tree,'{'+ns+'}url');ET.SubElement(node,'{'+ns+'}loc').text=url
site.write_text(ET.tostring(tree,encoding='unicode'))
print('Generated',len(slugs),'product URLs; updated collection, template and English sitemap')
