import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
INVDIR=os.environ.get('NN_INV','/home/claude/inv')  # register export: kept private, NOT in this repo
import json,re,sys
INV=[]
for f in ['raw1','raw2','raw3']: INV+=json.load(open(os.path.join(INVDIR,f'{f}.json')))
P=json.load(open(ROOT+'data/products.json'))
def norm(u): return u.lstrip('0')
byp={norm(p['upc']):p for p in P}
byi={}
for r in INV:
  u=re.match(r'\d*',r['id']).group()
  if u: byi.setdefault(norm(u),r)
for u in sys.argv[1:]:
  if not u[0].isdigit():
    q=u.upper().split('+')
    for r in INV:
      s=(r['brand']+' '+r['name']).upper()
      if all(x in s for x in q) and r['disc']!='TRUE': print('  INV?',r['id'],r['brand'],r['name'],r['size'],r['price'])
    for p in P:
      s=(p['brand']+' '+p['name']+' '+p.get('variant','')).upper()
      if all(x in s for x in q): print('  SITE?',p['upc'],p['brand'],p['name'],p.get('variant'),p['shelf_price'])
    continue
  n=norm(u); hit=None
  for cand in [n,n[:-1]]:
    if cand in byp: print(u,'SITE',byp[cand]['name'],byp[cand].get('variant'),byp[cand]['shelf_price'],byp[cand].get('msrp'),byp[cand].get('member_off')); hit=1;break
  if hit: continue
  for cand in [n,n[:-1]]:
    if cand in byi: r=byi[cand]; print(u,'INV',r['id'],r['brand'],'|',r['name'],'|',r['size'],r['price'],r['dept']); hit=1;break
  if not hit: print(u,'NONE')
