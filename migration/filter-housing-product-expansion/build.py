from pathlib import Path
import json,re,html
from PIL import Image
ROOT=Path(__file__).resolve().parents[2]; TASK=Path(__file__).resolve().parent
A=ROOT/'assets/products/housing-expansion'; A.mkdir(exist_ok=True)
sources=sorted((TASK/'source').glob('*.png'))
by={p.name.split('clipboard-')[1][:8]:p for p in sources}
crops=[('medium-blue','c1b3930b',(942,10,1290,548)),('medium-clear','c1b3930b',(942,565,1290,1100))]
for i,(y1,y2) in enumerate([(4,140),(150,273),(283,417),(428,563),(575,740),(753,949),(964,1138),(1150,1350)]):crops.append((f'assembly-{i}','9c96fcd2',(557,y1,743,y2)))
for name,y1,y2 in [('large-blue-10',65,300),('large-blue-20',310,502),('large-clear-10',513,717),('large-clear-20',731,933),('bracket',948,1125),('screws',1140,1270)]:crops.append((name,'8cfd5766',(558,y1,743,y2)))
for name,key,box in crops:
 if key in by:Image.open(by[key]).crop(box).convert('RGB').save(A/(name+'.webp'),quality=92)
# Archived screenshots are optional for rebuilding HTML; final referenced white assets are versioned separately.
products=[]
def add(id,name,img,size,ports,pack,description,kind='single',colour='Blue',source=''):
 products.append(dict(id=id,name=name,image=img,size=size,ports=ports,pack=pack,description=description,kind=kind,colour=colour,source=source))
for colour in ['Blue','Clear']:
 add('medium-'+colour.lower(),f'10-inch medium-body {colour.lower()} filter housing','medium-'+colour.lower(),'10-inch',['Standard thread: 3/8, 1/2, 3/4, 1 inch','Brass-insert thread: 1/2, 3/4, 1 inch'],'12 sets/carton','Supplied with a mounting bracket, screws and housing wrench. Choose a white or colour inner box. Confirm cartridge diameter and installation clearance before ordering.',colour=colour,source='screenshot 1')
for size in [10,20]:
 for colour in ['Blue','Clear']:
  add(f'large-{colour.lower()}-{size}',f'{size}-inch large-body {colour.lower()} filter housing',f'large-{colour.lower()}-{size}',f'{size} × 4.5 inch',['Plastic thread: 3/4, 1, 1.5 inch','Brass-insert thread: 3/4, 1 inch'],f'{8 if size==10 else 4} sets/carton','A single large-body housing supplied with a wrench. Select the thread construction and port size together. Mounting bracket is listed separately; confirm the final accessory set.',colour=colour,source='screenshot 3')
configs=[(10,2,'wall bracket'),(10,3,'wall bracket'),(10,2,'support frame'),(10,3,'support frame'),(20,2,'wall bracket'),(20,2,'support frame'),(20,3,'wall bracket'),(20,3,'support frame')]
for i,(size,stages,mount) in enumerate(configs):
 ports=['Plastic thread: '+p+' inch' for p in (['1','1.5'] if i==0 else ['3/4','1','1.5'])]
 add(f'assembly-{i}',f'{size}-inch {"two" if stages==2 else "three"}-stage filter housing assembly — {mount}',f'assembly-{i}',f'{size} × 4.5 inch',ports,'1 assembly/carton',f'{stages} housing positions supplied with a {mount} and wrench. '+('Confirm wall strength and fixing requirements before installation.' if mount=='wall bracket' else 'Check the support surface and space beneath the bowls for cartridge removal.')+' Cartridges are purchased separately; the number of stages does not specify filtration performance.',kind='assembly',source='screenshot 2')
# Preserve published URLs before changing product terminology.
old_manifest=json.loads((TASK/'url-manifest.json').read_text())
old_urls={x['product']:x['url'].rsplit('/',1)[1] for x in old_manifest}
for item in products:
 item['slug']=old_urls[item['id']]
 if item['id'].startswith('large-'):
  item['name']=item['name'].replace('large-body','BB-style')
  item['description']=item['description'].replace('large-body','BB-style')
 elif item['kind']=='assembly':item['name']=item['name'].replace('filter housing assembly','BB-style filter housing assembly')
for size in [10,20]:
 source=next(x for x in products if x['id']==f'large-blue-{size}')
 item=dict(source,id=f'black-{size}',name=f'{size}-inch black BB-style filter housing',image=f'black-{size}',colour='Black',slug=f'{size}-inch-black-bb-filter-housing.html',source='Owner confirmation: black has same corresponding blue specifications; original black housing photo')
 item['description']='Dedicated black housing option. '+source['description']
 products.append(item)
add('bracket','Large-body housing mounting bracket','bracket','Confirm housing fit',['Confirm mounting-hole pattern'],'Not specified','Separate mounting accessory. Confirm the housing head and fixing-hole pattern before ordering.',kind='accessory',source='screenshot 3')
add('screws','Large-body housing screws','screws','Confirm screw fit',['Confirm screw specification'],'4 pieces/pack','Accessory pack containing four screws. Confirm thread and mounting compatibility; screw dimensions are not provided.',kind='accessory',source='screenshot 3')
for p in products:
 expanded=[]
 for opt in p['ports']:
  if ': ' in opt and ', ' in opt:
   label, vals=opt.split(': ',1)
   expanded.extend(label+': '+v.strip()+' inch' for v in vals.removesuffix(' inch').split(','))
  else: expanded.append(opt)
 p['ports']=expanded
(TASK/'products.json').write_text(json.dumps(products,indent=2))
esc=html.escape
cards=[]
for p in products:
 options=[]
 if p['kind']!='accessory':
  options.append('<label>Colour<select name="colour">'+''.join(f'<option>{c}</option>' for c in ([p['colour']] if p['colour']=='Black' or p['kind']=='assembly' or p['id'].startswith('medium-') else [p['colour'],'Black — confirm availability']))+'</select></label>')
 options.append('<label>Connection / construction<select name="connection">'+''.join(f'<option>{esc(x)}</option>' for x in p['ports'])+'</select></label>')
 if p['id'].startswith('medium-'):options.append('<label>Inner box<select name="box"><option>White</option><option>Colour</option></select></label>')
 cards.append(f'''<article class="fh-card" id="{p['id']}" data-product="{esc(p['name'])}"><figure><img src="../assets/products/housing-expansion-white/{p['image']}.webp" alt="{esc(p['name'])}; reference-based product visualization" width="380" height="460" loading="lazy"><figcaption>{('Illustrative 10-inch variant derived from the original black housing reference; exact geometry requires confirmation.' if p['id']=='black-10' else 'Reference-based enhanced image; confirm exact details before ordering.')}</figcaption></figure><div><p class="fh-kicker">{'Accessory' if p['kind']=='accessory' else 'Housing only · cartridges sold separately'}</p><h3>{esc(p['name'])}</h3><p>{esc(p['description'])}</p><dl><dt>{'Fit' if p['kind']=='accessory' else 'Housing size designation'}</dt><dd>{esc(p['size'])}</dd><dt>Packing quantity</dt><dd>{esc(p['pack'])}</dd></dl><div class="fh-options">{''.join(options)}</div><p class="fh-summary" aria-live="polite"></p><a class="fh-quote" href="contact.html?product={__import__('urllib.parse',fromlist=['quote']).quote(p['name'])}&amp;product_family=filter-housing">Request this configuration</a></div></article>''')
base=(TASK/'source/before.html').read_text()
main='''<main class="fh-page"><div class="fh-wrap"><nav aria-label="Breadcrumb"><a href="products.html">Products</a> / <a href="filter-housing.html">Filter housings</a> / Housing selection</nav><header class="fh-hero"><p class="fh-kicker">Water filter housings · configuration guide</p><h1>10- and 20-inch water filter housings: Big Blue-style (BB) options</h1><p>Compare medium-body single housings and Big Blue-style (BB) housings, including black, blue and clear single bottles and blue two- or three-stage assemblies. Choose 10- or 20-inch size, wall bracket or support frame, and the listed connection options; then request a quotation.</p><p><strong>Housings only. Filter cartridges are not included.</strong> Cold-water use; confirm operating limits for your project before ordering.</p><a class="fh-quote" href="#housing-products">Compare 16 products &amp; request a quote</a></header><nav class="fh-jump" aria-label="Product groups"><a href="#housing-products">Single housings</a><a href="#assemblies">Two / three stages</a><a href="#accessories">Accessories</a><a href="#selection-guide">Selection guide</a></nav><section class="fh-guide" aria-label="How to request a quotation"><h2>Choose your housing in three steps</h2><p><strong>1. Compare:</strong> choose medium-body or BB-style, then size, colour and stage count. Black BB single housings are featured first.</p><p><strong>2. Confirm:</strong> open a product to check its connections, mounting format, included accessories and packing quantity. Cartridges are sold separately.</p><p><strong>3. Inquire:</strong> select the listed configuration and use Send a product inquiry. The form carries your product and options; add quantity, destination and your contact details.</p></section><section id="housing-products"><h2>Black BB housings and single water filter housings</h2><p>BB means Big Blue-style, a housing format designation used here independently of bowl colour; it does not claim Pentair brand origin or universal compatibility. Medium-body models are listed separately from the large-body 10 × 4.5 and 20 × 4.5 inch range. These are housing size designations, not overall assembly dimensions. Confirm cartridge fit before ordering.</p>'''+''.join(cards[14:16])+''.join(cards[:6])+'''</section><section id="assemblies"><h2>Two-stage and three-stage filter housing assemblies</h2><p>Compare wall-bracket and support-frame versions in 10- and 20-inch formats. Select cartridges separately to match your water-treatment requirements.</p>'''+''.join(cards[6:14])+'''</section><section id="accessories"><h2>Mounting accessories</h2>'''+''.join(cards[16:])+'''</section><section class="fh-guide" id="selection-guide"><h2>How to select a filter housing</h2><h3>What does 10 × 4.5 or 20 × 4.5 mean?</h3><p>These are the supplier's housing size designations. They are not the external width, depth or height of a mounted assembly. Confirm cartridge dimensions, seals and head clearance for the selected housing.</p><h3>Are filter cartridges included?</h3><p>No. Buy cartridges separately. PP sediment, CTO carbon-block or PVDF options can be discussed against your dimensions and treatment requirements; compatibility and performance must be confirmed.</p><h3>Should I choose two stages or three?</h3><p>Choose the number of housing positions to suit the cartridge sequence specified for your project. More positions alone do not establish contaminant removal, capacity or water quality.</p><h3>Which connections and colours can I order?</h3><p>Available connections vary by product and by plastic-thread or brass-insert construction. Black 10-inch and 20-inch BB-style single housings have dedicated product pages with the corresponding confirmed blue-housing specifications. Thread standard is confirmed before quotation.</p><h3>What information is needed for a quotation?</h3><p>Send housing size, stage count, bracket or frame, colour, connection size and construction, quantity and packing requirements. Also provide water conditions, required operating pressure, temperature and target flow so suitability can be checked. Numerical operating ratings are not published here.</p><h3>What materials and operating conditions apply?</h3><p>The supplier identifies PP plastic construction and cold-water use. Confirm component-specific materials, seals and operating limits for the chosen configuration. Certification documents and their model coverage must be checked for your project.</p><p>Before maintenance, isolate the supply and release pressure. Allow room to remove the bowl, and inspect seals and connections before returning the housing to service.</p></section></div></main>'''
base=re.sub(r'<main\b.*?</main>',main,base,flags=re.S)
base=re.sub(r'<title>.*?</title>','<title>10 &amp; 20 Inch Filter Housings | Big Blue-style BB | Yuchen</title>',base,flags=re.S)
base=re.sub(r'(<meta name="description" content=")[^"]*',r'\g<1>Compare 10/20-inch Big Blue-style (BB) and medium-body filter housings: black, blue or clear singles and two/three-stage assemblies. Request a quotation.',base)
# Remove stale Product claims; retain non-product schema graphs.
def schema(m):
 try:
  d=json.loads(m.group(1))
  if '@graph' in d:d['@graph']=[x for x in d['@graph'] if x.get('@type') not in ['Product','FAQPage']]
  elif d.get('@type') in ['Product','FAQPage']:return ''
  return '<script type="application/ld+json">'+json.dumps(d)+'</script>'
 except ValueError:return m.group(0)
base=re.sub(r'<script type="application/ld\+json">(.*?)</script>',schema,base,flags=re.S)
base=re.sub(r'(<meta property="og:title" content=")[^"]*',r'\g<1>10/20-inch water filter housings and Big Blue-style BB options',base)
base=re.sub(r'(<meta property="og:description" content=")[^"]*',r'\g<1>Compare Big Blue-style (BB) and medium-body housings, including black singles and two/three-stage assemblies. Cartridges sold separately.',base)
base=base.replace('</head>','<link rel="stylesheet" href="../assets/housing-expansion.css">\n<script src="../assets/housing-expansion.js" defer></script>\n</head>')
(ROOT/'en/product-housing-filter.html').write_text(base)
(ROOT/'tools/templates/housing-filter-en.html').write_text(base)
print('Built',len(products),'items')

# Keep the 14 dedicated product pages and collection links deterministic.
import runpy
remote_sitemap=TASK/"source/remote-sitemap-en.xml"
if remote_sitemap.exists():
    current=ROOT/"sitemaps/sitemap-en.xml"
    import xml.etree.ElementTree as ET
    old=ET.fromstring(current.read_text()); fresh=ET.fromstring(remote_sitemap.read_text()); ns={"s":"http://www.sitemaps.org/schemas/sitemap/0.9"}
    locs={x.text for x in old.findall(".//s:loc",ns)}
    text=current.read_text()
    for node in fresh:
        loc=node.find("s:loc",ns)
        if loc is not None and loc.text not in locs:
            text=text.replace("</urlset>",ET.tostring(node,encoding="unicode")+"\n</urlset>")
    current.write_text(text)
runpy.run_path(str(TASK/"split-products.py"))
