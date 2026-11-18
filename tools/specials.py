"""Set this month's coupon specials.
Usage: python3 tools/specials.py YYYY-MM-DD UPC[:dollars_off] [UPC[:dollars_off] ...]
Example: python3 tools/specials.py 2026-12-31 850029173137 788332173806:3
Clears every earlier store special first, then sets the new ones (default $2 off), runs rebuild.py, then coupon_page.py (coupon/ page + share/post images).
Each special needs a front photo in photo_lib/ (UPC-front.jpg); without one the card shows the brand's first letter."""
import sys, json, os, subprocess
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
until, specs = sys.argv[1], sys.argv[2:]
P = json.load(open(ROOT + 'data/products.json'))
for x in P: x.pop('store_off', None); x.pop('store_until', None)
by = {x['upc']: x for x in P}
for s in specs:
    u, _, off = s.partition(':')
    if u not in by: sys.exit('UPC not in catalog: ' + u)
    by[u]['store_off'] = off or '2'; by[u]['store_until'] = until
    ph = os.path.exists(ROOT + f'photo_lib/{u}-front.jpg')
    print(by[u]['brand'], by[u]['name'], '-', ('$' + (off or '2') + ' off'), '' if ph else '(no front photo yet)')
json.dump(P, open(ROOT + 'data/products.json', 'w'), indent=1)
subprocess.run([sys.executable, ROOT + 'tools/rebuild.py'], check=True)
subprocess.run([sys.executable, ROOT + 'tools/coupon_page.py'], check=True)
import urllib.parse as _u
print('\nAfter it is live, ask Google to re-fetch (Search Console > paste the address > Request indexing):')
for _p in ('https://naturesnook.co/coupon/', 'https://naturesnook.co/'):
    print('  ' + _p)
    print('    shortcut: https://search.google.com/search-console/inspect?resource_id=' + _u.quote('sc-domain:naturesnook.co', safe='') + '&id=' + _u.quote(_p, safe=''))
