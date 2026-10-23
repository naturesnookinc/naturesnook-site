import os
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))+'/'
INVDIR=os.environ.get('NN_INV','/home/claude/inv')  # register export: kept private, NOT in this repo
import json,sys,importlib.util
P=json.load(open(ROOT+'data/products.json'))
idx={p['upc'].lstrip('0'):i for i,p in enumerate(P)}
for f in sys.argv[1:]:
  spec=importlib.util.spec_from_file_location('m',f); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
  dept=getattr(m,'V'); src=m.SRC
  for r in m.ROWS:
    upc,price,msrp,off,brand,name,var,form,pos=r[:9]
    d=r[9] if len(r)>9 else dept
    k=upc.lstrip('0')
    if k in idx:
      p=P[idx[k]]; ch=[]
      if p['shelf_price']!=price: ch.append(f"price {p['shelf_price']}->{price}"); p['shelf_price']=p['price']=price
      if msrp and p.get('msrp')!=msrp: ch.append(f"msrp {p.get('msrp')}->{msrp}"); p['msrp']=msrp
      p.pop('msrp_est',None) if msrp else None
      if off and p.get('member_off')!=f'{float(off):.2f}': ch.append(f'member {off}'); p['member_off']=f'{float(off):.2f}'; p['member_until']='2026-12-29'
      print('UPD',p['name'],p.get('variant'),ch)
    else:
      assert name, upc
      p=dict(name=name,variant=var,form=form,brand=brand,dept=d,price=price,shelf_price=price,upc=upc,pos=pos,source=src)
      if msrp: p['msrp']=msrp
      if off: p['member_off']=f'{float(off):.2f}'; p['member_until']='2026-12-29'
      P.append(p); idx[k]=len(P)-1; print('ADD',brand,name,var)
json.dump(P,open(ROOT+'data/products.json','w'),indent=1,ensure_ascii=False)
from collections import Counter
c=Counter(p['upc'].lstrip('0') for p in P); print('total',len(P),'dups',[u for u,n in c.items() if n>1])
