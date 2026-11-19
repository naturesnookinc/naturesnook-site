"""Rebuild everything that goes with the monthly coupon, from the store specials in data/products.json:
  coupon/index.html (shareable page), img/coupon-share.jpg (1200x630 link preview), img/coupon-post.jpg (1080x1350 social post).
Run by tools/specials.py. Standalone: python3 tools/coupon_page.py"""
import json, os, html, datetime, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
P = json.load(open(ROOT + 'data/products.json'))
S = [x for x in P if x.get('store_off')]
if not S: raise SystemExit('no store specials set')
e = html.escape
d = datetime.date.fromisoformat(min(x['store_until'] for x in S))
until = d.strftime('%B ') + str(d.day) + d.strftime(', %Y')
offs = sorted({float(x['store_off']) for x in S})
amt = lambda v: '$' + (('%.2f' % v) if v % 1 else str(int(v)))
line = (amt(offs[0]) + ' off' if len(offs) == 1 else 'Up to ' + amt(offs[-1]) + ' off') + ' each item below'
def photo(x, pre=''):
    f = f'photo_lib/w/{x["upc"]}-front.webp'
    return f'<img src="{pre}{f}" alt="">' if os.path.exists(ROOT + f) else f'<span class="ph">{e(x["brand"][:1])}</span>'
def size(x): return (x.get('form') or '').split(' · ')[-1]
def cards(pre='', link=True):
    out = []
    for x in S:
        off = float(x['store_off']); pr = float(x['price'])
        inner = (f'<b class="off">{amt(off)} OFF</b><span class="pic">{photo(x, pre)}</span><span class="nm">{e(x["name"])}</span>'
                 f'<span class="mt">{e(x["brand"])} · {e(size(x))}</span><span class="pr"><s>${pr:.2f}</s> <b>${pr-off:.2f}</b></span>')
        out.append(f'<li><a href="/#p{x["upc"]}">{inner}</a></li>' if link else f'<li><div>{inner}</div></li>')
    return '\n'.join(out)
FONTS = lambda pre: f'@font-face{{font-family:"Archivo";font-weight:100 900;src:url({pre}fonts/archivo-latin-wght-normal.woff2) format("woff2")}}@font-face{{font-family:"Figtree";font-weight:100 900;src:url({pre}fonts/figtree-latin-wght-normal.woff2) format("woff2")}}'
CARD_CSS = '''.grid{list-style:none;margin:0;padding:0;display:grid;gap:10px}
.grid li{min-width:0}.grid a,.grid div{display:flex;flex-direction:column;align-items:center;text-align:center;height:100%;padding:12px 8px 14px;background:#fff;border:1px solid #d4e1d7;border-top:4px solid #e8a33d;color:inherit;text-decoration:none}
.off{background:#e8a33d;color:#1b1f1c;font-family:Archivo,Arial,sans-serif;font-weight:800;letter-spacing:.02em;padding:.25rem .75rem;border-radius:2px;font-size:1.15rem}
.pic{display:flex;align-items:center;justify-content:center;height:130px;margin:10px 0 8px}.pic img{max-height:130px;max-width:100%;width:auto}
.ph{font:800 2.4rem Archivo,sans-serif;color:#1d7542}
.nm{font-weight:700;font-size:.92rem;line-height:1.25}.mt{font-size:.76rem;color:#56635a;margin-top:3px}
.pr{margin-top:auto;padding-top:8px;display:flex;align-items:baseline;gap:6px;flex-wrap:wrap;justify-content:center}.pr s{color:#56635a;font-size:.85rem}.pr b{font:800 1.5rem Archivo,sans-serif;color:#1d7542}'''
page = f'''<!doctype html>
<html lang="en" data-theme="light">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Specials This Month | Nature's Nook, Rexburg</title>
<meta name="description" content="{line.capitalize()} at Nature's Nook. Bring this in or show it at the register. No membership needed. Through {until}.">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nature's Nook">
<meta property="og:url" content="https://naturesnook.co/coupon/">
<meta property="og:title" content="Specials this month | Nature's Nook">
<meta property="og:description" content="{line.capitalize()}. Bring this in or show it at the register. No membership needed. 160 E Valley River Rd #2, Rexburg.">
<meta property="og:image" content="https://naturesnook.co/img/coupon-share.jpg?v={d.isoformat()}">
<meta property="og:image:secure_url" content="https://naturesnook.co/img/coupon-share.jpg?v={d.isoformat()}">
<meta property="og:image:type" content="image/jpeg">
<meta property="og:image:alt" content="Nature's Nook specials this month: {e(', '.join(x['name'] for x in S))}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:image" content="https://naturesnook.co/img/coupon-share.jpg?v={d.isoformat()}">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png">
<link rel="icon" href="/favicon.ico">
<link rel="canonical" href="https://naturesnook.co/coupon/">
<meta name="color-scheme" content="light">
<style>
{FONTS('/')}
:root{{--pine:#1d7542;--ink:#1b1f1c;--cream:#fcf3df;color-scheme:light}}
*{{box-sizing:border-box}}
body{{margin:0;font-family:Figtree,system-ui,-apple-system,"Segoe UI",sans-serif;color:var(--ink);background:var(--cream)}}
.wrap{{max-width:980px;margin:0 auto;padding:16px 16px 40px}}
.top{{display:flex;align-items:center;justify-content:space-between;padding:6px 0 14px}}.top img{{height:54px;width:auto}}
.top a.home{{color:var(--pine);font-weight:700;text-decoration:none}}
.coupon{{background:#fff;border:2px dashed var(--pine);padding:clamp(18px,4vw,32px) clamp(12px,3vw,28px) 18px;text-align:center}}
h1{{font:800 clamp(2.3rem,7vw,4rem)/1 Archivo,Arial,sans-serif;text-transform:uppercase;letter-spacing:-.01em;margin:0}}
.sub{{font-size:1.05rem;margin:.7rem auto 1.2rem;max-width:40rem}}
{CARD_CSS}
.grid{{grid-template-columns:repeat(2,minmax(0,1fr))}}
@media(min-width:760px){{.grid{{grid-template-columns:repeat(auto-fit,minmax(125px,1fr))}}}}
.foot{{font-size:.85rem;color:#56635a;margin:1.2rem 0 0}}
.btns{{display:grid;gap:10px;margin:18px auto 0;max-width:560px}}
.btn{{display:flex;justify-content:center;align-items:center;padding:14px 18px;border-radius:2px;font-weight:700;text-decoration:none;font-size:1.05rem;border:2px solid var(--pine);color:var(--pine);background:#fff;cursor:pointer;font-family:inherit}}
.btn.main{{background:var(--pine);color:#fff}}
.mem{{text-align:center;margin:26px auto 0;max-width:560px;color:#56635a;font-size:.95rem;line-height:1.5}}.mem a{{color:var(--pine);font-weight:700}}
.mem h2{{font:700 1.3rem Archivo,sans-serif;color:var(--ink);margin:0 0 .3rem}}
p.note{{text-align:center;color:#56635a;font-size:.92rem;margin-top:16px;line-height:1.45}}
@media print{{@page{{size:letter;margin:.4in}}body{{background:#fff}}.top,.btns,.mem,p.note{{display:none}}.wrap{{max-width:none;padding:0}}.grid{{grid-template-columns:repeat(3,1fr)}}}}
</style>
</head>
<body>
<div class="wrap">
  <div class="top"><a href="/"><img src="/img/logo.svg" alt="Nature's Nook"></a><a class="home" href="/">naturesnook.co</a></div>
  <div class="coupon">
    <h1>Specials this month</h1>
    <p class="sub">{line}. <strong>Bring this in</strong> or show us at the register. No membership needed.</p>
    <ul class="grid">
{cards('/')}
    </ul>
    <p class="foot">Valid at Nature's Nook, 160 E Valley River Rd #2, Rexburg. Through {until}.</p>
  </div>
  <div class="btns">
    <button class="btn main" type="button" onclick="window.print()">Print coupon</button>
    <a class="btn" id="dir" href="https://www.google.com/maps/dir/?api=1&destination=Nature%27s+Nook+160+E+Valley+River+Rd+%232+Rexburg+ID">Get directions</a>
    <a class="btn" href="tel:+12083565284">Call (208) 356-5284</a>
  </div>
  <div class="mem"><h2>More savings for members</h2>Members save on hundreds of products with a blue SaveNaturally tag. Membership is free and we can sign you up at the register. <a href="/#members">See member deals</a></div>
  <p class="note"><a href="/returns/">Returns</a> &middot; <a href="/privacy/">Privacy</a> &middot; <a href="/terms/">Terms</a> &middot; <a href="/accessibility/">Accessibility</a></p>
</div>
<script>
(function(){{var a=document.getElementById('dir');if(/iPhone|iPad|iPod|Macintosh/.test(navigator.userAgent)&&('ontouchend' in document||/iPhone|iPad|iPod/.test(navigator.userAgent))){{a.href='https://maps.apple.com/?daddr=160+E+Valley+River+Rd+%232,+Rexburg,+ID&q=Nature%27s+Nook';}}}})();
</script>
</body>
</html>
'''
open(ROOT + 'coupon/index.html', 'w').write(page)
# social images
def img_page(w, h, cols):
    return f'''<!doctype html><meta charset="utf-8"><style>{FONTS('file://'+ROOT)}
*{{box-sizing:border-box}}body{{margin:0;width:{w}px;height:{h}px;background:#fcf3df;font-family:Figtree,sans-serif;color:#1b1f1c;padding:{28 if h<700 else 40}px;display:flex;flex-direction:column}}
.in{{flex:1;background:#fff;border:3px dashed #1d7542;padding:{18 if h<700 else 28}px;text-align:center;display:flex;flex-direction:column;justify-content:center}}
h1{{font:800 {54 if h<700 else 84}px/1 Archivo,sans-serif;text-transform:uppercase;margin:0}}
.sub{{font-size:{20 if h<700 else 34}px;margin:{8 if h<700 else 18}px 0 {12 if h<700 else 28}px}}
{CARD_CSS}
.grid{{grid-template-columns:repeat({cols},1fr);flex:none;gap:{8 if h<700 else 18}px}}
.pic{{height:{130 if h<700 else 170}px}}.pic img{{max-height:{130 if h<700 else 170}px}}
.nm{{font-size:{12 if h<700 else 22}px}}.mt{{display:{'none' if h<700 else 'block'};font-size:17px}}.off{{font-size:{14 if h<700 else 24}px}}.pr b{{font-size:{22 if h<700 else 40}px}}.pr s{{font-size:{13 if h<700 else 20}px}}
.foot{{font-size:{15 if h<700 else 24}px;margin:{8 if h<700 else 20}px 0 0;color:#56635a}}</style>
<div class="in"><h1>Specials this month</h1><p class="sub"><b>{line}.</b> Bring this in. No membership needed.</p><ul class="grid">{cards('file://'+ROOT, False)}</ul><p class="foot">Nature's Nook · 160 E Valley River Rd #2, Rexburg · Through {until}</p></div>'''
from playwright.sync_api import sync_playwright
n = len(S)
with sync_playwright() as pw:
    b = pw.chromium.launch(); tmp = tempfile.mkdtemp()
    for name, w, h, cols in (('coupon-share', 1200, 630, n), ('coupon-post', 1080, 1350, 3 if n > 4 else 2)):
        f = f'{tmp}/{name}.html'; open(f, 'w').write(img_page(w, h, cols))
        pg = b.new_page(viewport={'width': w, 'height': h}); pg.goto('file://' + f); pg.wait_for_timeout(600)
        pg.screenshot(path=ROOT + f'img/{name}.jpg', type='jpeg', quality=88); pg.close()
    b.close()
print('coupon page + share images rebuilt:', n, 'specials, through', until)
