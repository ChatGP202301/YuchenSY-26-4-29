from pathlib import Path
import json,copy,xml.etree.ElementTree as ET,re,hashlib,runpy
T=Path(__file__).resolve().parent;R=T.parents[1]
def check(rows):
 assert len(rows)==18
 ids={p['id']:p for p in rows}
 for size in [10,20]:
  b=ids[f'black-{size}'];blue=ids[f'large-blue-{size}']
  assert b['colour']=='Black' and b['image']==f'black-{size}'
  assert b['ports']==blue['ports'] and b['pack']==blue['pack'] and b['size']==blue['size']
  assert b['slug']==f'{size}-inch-black-bb-filter-housing.html'
 for p in rows:
  if p['id'].startswith('medium-'):assert 'BB' not in p['name']
  elif p['kind']!='accessory':assert 'BB-style' in p['name']
 assert ids['assembly-0']['ports']==['Plastic thread: 1 inch','Plastic thread: 1.5 inch']
rows=json.loads((T/'products.json').read_text());check(rows)
for name,mutate in [('missing black',lambda a:a.pop(14)),('wrong colour',lambda a:a[14].update(colour='Blue')),('wrong port',lambda a:a[14].update(ports=['Plastic thread: 2 inch']))]:
 bad=copy.deepcopy(rows);mutate(bad)
 try:check(bad)
 except AssertionError:print('RED detected:',name)
 else:raise AssertionError('Negative case accepted: '+name)
check(rows);print('GREEN restored canonical data')
manifest=json.loads((T/'url-manifest.json').read_text());assert len(manifest)==16
sitemap=(R/'sitemaps/sitemap-en.xml').read_text()
for x in manifest:
 p=next(p for p in rows if p['id']==x['product']);s=(R/'en'/p['slug']).read_text()
 assert x['url'] in sitemap and f'rel="canonical" href="{x["url"]}"' in s
 assert s.count('<h1>')==1 and 'data-fh-inquiry' in s
 assert 'NSF certified' not in s
 for raw in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S):
  d=json.loads(raw);assert d['name']==p['name']
 if p['id'].startswith('large-'):assert 'large-body' in p['slug']
 if p['id'].startswith('assembly-'):assert 'bb-style' not in p['slug']
 if 'BB-style' in p['name']:assert 'BB means Big Blue-style' in s
print('PASS 16 page contracts, preserved old URL forms, sitemap, Product JSON-LD and terminology')
paths=[R/'en'/p['slug'] for p in rows if p['kind']!='accessory']+[R/'en/product-housing-filter.html',R/'sitemaps/sitemap-en.xml'];before=[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths];runpy.run_path(str(T/'build.py'));assert before==[hashlib.sha256(p.read_bytes()).hexdigest() for p in paths];print('PASS deterministic rebuild: zero changes')
