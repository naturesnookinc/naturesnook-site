"""Rebuild the catalog block in index.html from data/products.json.
Usage: python3 tools/rebuild.py  [brand colors added via NEW_BRANDS dict below]"""
import re,json,sys
import os as _os; ROOT=_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))+'/'
h=open(ROOT+'index.html').read()
p=json.load(open(ROOT+'data/products.json'))
def num(s):
    m=re.search(r'(\d[\d,]*(?:\.\d+)?)',s or '')
    return float(m.group(1).replace(',','')) if m else 0
def key(x):
    return (x['name'].lower(), x['brand']!="Nature's Nook", x['brand'].lower(), num(x['variant']), x['variant'].lower(), num(x['form'].split('·')[-1]), float(x.get('shelf_price') or x['price'] or 0))
p.sort(key=key)
rows=[[x['dept'],x['brand'],x['name'],x['variant'],x['form'],x.get('shelf_price') or x['price'],x['upc'],x.get('msrp') or '',x.get('member_off') or '',x.get('member_until') or '',x.get('fav') or ''] for x in p]
data=json.dumps(rows,ensure_ascii=False,separators=(',',':'))
h=re.sub(r'(<script id="catalog-data" type="application/json">).*?(</script>)',lambda m:m.group(1)+data+m.group(2),h,count=1,flags=re.S)
h=re.sub(r'<strong>Preview:</strong> [\d,]+ products',f'<strong>Preview:</strong> {len(rows):,} products',h)
NEW=json.loads(sys.argv[1]) if len(sys.argv)>1 else {}
new={k:v for k,v in NEW.items() if f'.b-{k}{{' not in h}
if new:
    css=''.join(f'.b-{k}{{--b1:{a};--b2:{b}}}' for k,(a,b,d) in new.items())
    dk1=''.join(f':root[data-theme="dark"] .b-{k}{{--b1:{d}}}' for k,(a,b,d) in new.items())
    dk2='@media (prefers-color-scheme: dark){'+''.join(f':root:not([data-theme="light"]) .b-{k}{{--b1:{d}}}' for k,(a,b,d) in new.items())+'}'
    assert h.count('\n/* Our own line */')==1
    h=h.replace('\n/* Our own line */','\n'+css+'\n'+dk1+'\n'+dk2+'\n/* Our own line */')
open(ROOT+'index.html','w').write(h)
json.dump(p,open(ROOT+'data/products.json','w'),indent=1)
print(len(rows),'products; new brand colors:',list(new))
# --- attach photo library (photo_lib/UPC-front|back|facts.jpg) to products on the site ---
import os
h=open(ROOT+'index.html').read()
m=re.search(r'(<script id="photo-data" type="application/json">)(.*?)(</script>)',h,re.S)
ph=json.loads(m.group(2)); ph.setdefault('_facts',{})
lib=set(os.listdir(ROOT+'photo_lib')) if os.path.isdir(ROOT+'photo_lib') else set()
onsite={x['upc'] for x in p}; n=0
for u in onsite:
    if f'{u}-front.jpg' in lib:
        ph[u]=[f'photo_lib/{u}-{k}.jpg' for k in ('front','back') if f'{u}-{k}.jpg' in lib]
        if f'{u}-facts.jpg' in lib: ph['_facts'][u]=f'photo_lib/{u}-facts.jpg'
        n+=1
h=h[:m.start(2)]+json.dumps(ph,separators=(',',':'))+h[m.end(2):]
open(ROOT+'index.html','w').write(h)
print('photo library attached to',n,'products')
# --- clean facts tables (data/facts.json) ---
if os.path.exists(ROOT+'data/facts.json'):
    h=open(ROOT+'index.html').read()
    m=re.search(r'(<script id="photo-data" type="application/json">)(.*?)(</script>)',h,re.S)
    ph=json.loads(m.group(2)); fd=ph.setdefault('_factsData',{})
    fx=json.load(open(ROOT+'data/facts.json')); fd.update({u:v for u,v in fx.items() if u in onsite})
    h=h[:m.start(2)]+json.dumps(ph,separators=(',',':'),ensure_ascii=False).replace('</','<\\/')+h[m.end(2):]
    open(ROOT+'index.html','w').write(h)
    print('clean facts tables:',len(fd))
