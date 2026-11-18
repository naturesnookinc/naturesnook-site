"""Build the Rexburg department pages, sitemap.xml and robots.txt.
Usage: python3 tools/seo.py   (run after rebuild.py whenever the catalog changes)
Pages describe what the store carries (brands and product names from data/products.json).
No health claims: nothing here says what a product does."""
import json, os, collections, html, datetime, re
SKIP = re.compile(r'parasit|paracide|bronch|blood sugar|thyroid|adrenal rx|diabet|cancer|arthrit|inflamm|\bpain\b|\bcold\b|\bflu\b|anxiety|depress|\bcure|detox|cleanse|cramp|immun', re.I)  # keep disease-implying names out of the sample lists

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
SITE = 'https://naturesnook.co'
P = json.load(open(ROOT + 'data/products.json'))
TODAY = datetime.date.today().isoformat()
e = html.escape

PAGES = [
 dict(slug='vitamins-supplements-rexburg', dept='Vitamins & Supplements', q='', short='Vitamins & Supplements',
      title="Vitamins & Supplements in Rexburg, Idaho | Nature's Nook",
      desc="Shop vitamins and supplements in Rexburg, Idaho at Nature's Nook: Solaray, NOW Foods, Natural Factors, Garden of Life, Nature's Way, Terry Naturally and our own line.",
      h1='Vitamins & supplements in Rexburg',
      intro="Nature's Nook is a local health food store at 160 E Valley River Rd #2 in Rexburg, Idaho. We carry a wide selection of vitamins, minerals, herbs, probiotics, protein and specialty supplements from well-known brands, plus our own Nature's Nook line made in glass bottles.",
      more="Stop in and our staff can point you to what we carry, or search the full online list to see if we have a brand or product on the shelf. Stock changes, so call ahead if you are making a special trip.",
      fda=True),
 dict(slug='herbs-tinctures-rexburg', dept='Herbs & Tinctures', q='', short='Herbs & Tinctures',
      title="Herbs & Tinctures in Rexburg, Idaho | Nature's Nook",
      desc="Herbs, liquid extracts, capsules and powders in Rexburg, Idaho. Nature's Nook carries Herb Pharm, Starwest Botanicals, Frontier Co-op and our own label herbs.",
      h1='Herbs & tinctures in Rexburg',
      intro="Nature's Nook carries single herbs and herbal blends in liquid extract, capsule and powder form, including our own Nature's Nook line, packaged in glass bottles and sealed for your protection.",
      more="Ask our staff about a specific herb, or search the online list by name to see if it is on the shelf.",
      fda=True),
 dict(slug='essential-oils-rexburg', dept='Essential Oils', q='', short='Essential Oils',
      title="Essential Oils in Rexburg, Idaho | Nature's Nook",
      desc="Essential oils, diffusers and carrier oils in Rexburg, Idaho. Nature's Nook carries NOW Essential Oils, Pranarôm, Garden Essence and our own label oils.",
      h1='Essential oils in Rexburg',
      intro="Nature's Nook stocks single essential oils and blends, carrier oils and diffusers from several brands, including our own Nature's Nook oils.",
      more="Come in to smell the oils in person, or search the online list for a favorite scent or brand.",
      fda=True),
 dict(slug='gluten-free-natural-groceries-rexburg', dept='Grocery', q='', short='Gluten-Free & Natural Groceries',
      title="Gluten-Free & Natural Groceries in Rexburg, Idaho | Nature's Nook",
      desc="Gluten-free breads, baking supplies, snacks and natural pantry staples in Rexburg, Idaho. Bulk herbs, flours, sweeteners and more at Nature's Nook.",
      h1='Gluten-free & natural groceries in Rexburg',
      intro="Besides vitamins and herbs, Nature's Nook is a natural grocer. Our gluten-free section has breads, baking supplies, snacks and meals, and our shelves carry grains and flours, natural sweeteners, nuts and dried fruit, spices, bulk herbs and healthy snacks. We also fill your jugs with distilled water made in the store.",
      more="Always read the package for ingredients and allergens before you buy. If a product you want isn't on the shelf, ask and we'll do our best to order it.",
      fda=False),
 dict(slug='teas-rexburg', dept='Teas', q='', short='Teas',
      title="Herbal Teas in Rexburg, Idaho | Nature's Nook",
      desc="Loose-leaf and bagged teas in Rexburg, Idaho: Traditional Medicinals, Buddha Teas, Triple Leaf, Celestial Seasonings and more at Nature's Nook.",
      h1='Herbal & specialty teas in Rexburg',
      intro="Nature's Nook carries bagged herbal teas, herbal blends and specialty teas from several brands, along with bulk herbs for making your own.",
      more="Ask our staff what we have in stock, or search the online list by brand or tea name.",
      fda=True),
 dict(slug='natural-beauty-personal-care-rexburg', dept='Beauty & Personal Care', q='', short='Beauty & Personal Care',
      title="Natural Beauty & Personal Care in Rexburg, Idaho | Nature's Nook",
      desc="Natural soaps, lotions, hair care, lip balm and body care in Rexburg, Idaho. Dr. Bronner's, Burt's Bees, NOW Solutions and more at Nature's Nook.",
      h1='Natural beauty & personal care in Rexburg',
      intro="Nature's Nook carries cleaner skin care, hair care, soaps, lotions, lip care and everyday personal care products from brands like Dr. Bronner's, Burt's Bees, NOW Solutions and Heritage Store.",
      more="Search the online list for a brand or product, or stop in to see what is on the shelf.",
      fda=False),
 dict(slug='protein-powder-rexburg', dept=('protein|whey|collagen|bone broth', ('Vitamins & Supplements','Grocery')), q='Protein', short='Protein & Protein Powder',
      title="Protein Powder & Protein Products in Rexburg, Idaho | Nature's Nook",
      desc="Protein powder in Rexburg, Idaho: plant-based, whey, collagen and bone broth protein, bars and shakes from Garden of Life, Ancient Nutrition, NOW Sports, Sunwarrior and more at Nature's Nook.",
      h1='Protein powder & protein products in Rexburg',
      intro="Nature's Nook carries protein powders, collagen and bone broth protein, ready-to-drink shakes and protein bars. Plant-based, whey and egg-white options come from brands like Garden of Life, Ancient Nutrition, NOW Sports, Sunwarrior, Biochem, Natural Factors and Nature's Plus.",
      more="Ingredients and allergens differ by flavor and size, so read the package before you buy. Ask our staff what is on the shelf today, or search the online list by brand or flavor.",
      fda=True),
 dict(slug='electrolytes-rexburg', dept=('electrolyte|re-lyte|zerolyte|hydro[ -]?(pak|fuel|magnesium)|rapid hydration|coconut water|super fruit water', ('Vitamins & Supplements','Grocery')), q='Electrolyte', short='Electrolyte Drink Mixes',
      title="Electrolyte Drink Mixes in Rexburg, Idaho | Nature's Nook",
      desc="Electrolyte powders, stick packs and drink mixes in Rexburg, Idaho: Re-Lyte, Trace Minerals, Zhou, Ancient Nutrition, Superieur and coconut water at Nature's Nook.",
      h1='Electrolyte drink mixes in Rexburg',
      intro="Nature's Nook carries electrolyte powders, stick packs and drink mixes in many flavors, including Redmond Re-Lyte, Trace Minerals, Zhou, Ancient Nutrition, Superieur and KAL, plus coconut waters and fruit waters in the cooler.",
      more="Flavors and sizes change, so ask our staff what is on the shelf, or search the online list by brand or flavor.",
      fda=True),
]

DEPTS = {p['dept'] for p in PAGES if isinstance(p['dept'], str)}


DENY = re.compile(r'proline|burrito|ramen|biscuit|gravy|beauty|bromelain|big stick|smoothie|hydrangea', re.I)


def pool(key):
    """products for a page: a department name, or a (regex, depts) filter"""
    if isinstance(key, tuple):
        rx, depts = key
        r = re.compile(rx, re.I)
        return [x for x in P if x['dept'] in depts and r.search(x['name']) and not DENY.search(x['name'])]
    return [x for x in P if x['dept'] == key]


def brands_for(dept):
    c = collections.Counter(x['brand'] for x in pool(dept))
    out = [b for b, n in c.most_common()]
    own = "Nature's Nook"
    if own in out:
        out.remove(own); out.insert(0, own)
    return out


def examples_for(dept, n=24):
    seen, out = set(), []
    # one product name per brand first, round-robin, so the list is varied
    by = collections.defaultdict(list)
    for x in pool(dept):
        if not SKIP.search(x['name']):
            by[x['brand']].append(x['name'])
    order = brands_for(dept)
    i = 0
    while len(out) < n and any(by[b] for b in order):
        for b in order:
            while by[b]:
                nm = by[b].pop(0)
                key = (b, nm.lower())
                if key not in seen:
                    seen.add(key); out.append((b, nm)); break
            if len(out) >= n:
                break
    return out


CSS = """:root{color-scheme:light;--pine:#1d7542;--ink:#1b1f1c;--muted:#4c584f;--line:#d4e1d7;--bg:#f2f6f2;--surface:#fff;--gold:#e8a33d;--gold-soft:#fdf1d8}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--ink);font-family:system-ui,-apple-system,"Segoe UI",Roboto,Arial,sans-serif;font-size:1.0625rem;line-height:1.65}
a{color:var(--pine);font-weight:600}
a:focus-visible,.btn:focus-visible{outline:3px solid #8a4a1f;outline-offset:3px;border-radius:4px}
.skip{position:absolute;left:8px;top:-80px;background:#fff;color:var(--ink);padding:.7rem 1rem;border:2px solid var(--ink);border-radius:8px;z-index:5}
.skip:focus{top:8px}
header{background:#1d4a31;border-bottom:3px solid var(--gold)}
header .in{max-width:860px;margin:0 auto;padding:14px 16px;display:flex;align-items:center;justify-content:space-between;gap:1rem}
header a{color:#fff;text-decoration:none;display:inline-block;padding:.4rem 0}
header a:focus-visible{outline-color:#fff}
header .logo{background:#fff;border-radius:10px;padding:6px 10px;display:block}
header .logo img{display:block;height:44px;width:auto}
main{max-width:860px;margin:0 auto;padding:28px 16px 40px}
main:focus{outline:none}
h1{font-size:clamp(1.8rem,5vw,2.5rem);line-height:1.12;margin:0 0 .6rem}
h1::after{content:"";display:block;width:72px;height:5px;border-radius:2px;background:var(--gold);margin-top:.6rem}
h2{font-size:1.3rem;line-height:1.3;margin:2rem 0 .5rem}
p,ul{margin:.6rem 0}
.btn{display:inline-block;background:var(--pine);color:#fff;text-decoration:none;font-weight:700;padding:.8rem 1.3rem;border-radius:999px;box-shadow:0 3px 0 var(--gold);margin:.4rem .6rem .4rem 0}
.btn.ghost{background:#fff;color:var(--pine);border:1.5px solid var(--pine);box-shadow:none}
.box{background:var(--surface);border:1px solid var(--line);border-radius:14px;padding:1rem 1.2rem;margin:1.2rem 0}
.box.visit{border-top:5px solid var(--gold)}
.brands{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:.4rem .5rem}
.brands li{background:var(--surface);border:1px solid var(--line);border-radius:999px;padding:.15rem .75rem;font-size:.95rem}
.ex{columns:2;column-gap:2rem;padding-left:1.1rem}
.ex li{break-inside:avoid;margin:.25rem 0}
.ex span{color:var(--muted);font-size:.9rem}
.cats{list-style:none;padding:0;display:flex;flex-wrap:wrap;gap:.3rem 1.2rem}
.fda{color:var(--muted);font-size:.9rem;border-top:1px solid var(--line);padding-top:.8rem;margin-top:1.6rem}
footer{border-top:3px solid var(--gold);background:var(--surface);color:var(--muted);font-size:.92rem}
footer .in{max-width:860px;margin:0 auto;padding:20px 16px 28px}
footer ul{list-style:none;margin:0 0 .8rem;padding:0;display:flex;flex-wrap:wrap;gap:.2rem 1.2rem}
footer a{display:inline-block;padding:.3rem 0}
@media (max-width:600px){.ex{columns:1}}
@media print{header,footer ul,.skip{display:none}body{background:#fff}}"""

FOOT = """<footer><div class="in"><ul>
<li><a href="/returns/">Returns &amp; refunds</a></li><li><a href="/privacy/">Privacy policy</a></li><li><a href="/cookies/">Cookie policy</a></li><li><a href="/terms/">Terms of use</a></li><li><a href="/accessibility/">Accessibility</a></li></ul>
<p>&copy; Nature's Nook &middot; 160 E Valley River Rd #2, Rexburg, ID 83440 &middot; <a href="tel:+12083565284">(208) 356-5284</a></p>
</div></footer>"""

FDA = '<p class="fda">Statements about dietary supplements on this site have not been evaluated by the Food and Drug Administration. These products are not intended to diagnose, treat, cure, or prevent any disease. Talk with your health care provider about what is right for you.</p>'


def link(page):
    from urllib.parse import quote
    qs = []
    if page.get('q'):
        qs.append('q=' + quote(page['q']))
    elif page['dept'] != 'Grocery':
        qs.append('dept=' + quote(page['dept']))
    else:
        qs.append('q=' + quote('Gluten Free'))
    return '/?' + '&'.join(qs) + '#find'


def build(page):
    brands = brands_for(page['dept'])
    shown = brands[:40]
    ex = examples_for(page['dept'])
    n = len(pool(page['dept']))
    url = f"{SITE}/{page['slug']}/"
    ld = {
      "@context": "https://schema.org",
      "@graph": [
        {"@type": "BreadcrumbList", "itemListElement": [
          {"@type": "ListItem", "position": 1, "name": "Nature's Nook", "item": SITE + "/"},
          {"@type": "ListItem", "position": 2, "name": page['short'], "item": url}]},
        {"@type": "CollectionPage", "@id": url + "#page", "url": url, "name": page['title'], "description": page['desc'],
         "about": {"@id": SITE + "/#store"}, "isPartOf": {"@id": SITE + "/#website"}}
      ]}
    others = ''.join(f'<li><a href="/{p["slug"]}/">{e(p["short"])}</a></li>' for p in PAGES if p is not page)
    ex_html = ''.join(f'<li>{e(nm)} <span>({e(b)})</span></li>' for b, nm in ex)
    out = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="color-scheme" content="light">
<title>{e(page['title'])}</title>
<meta name="description" content="{e(page['desc'])}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nature's Nook">
<meta property="og:title" content="{e(page['title'])}">
<meta property="og:description" content="{e(page['desc'])}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/img/og-storefront.jpg">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="icon" type="image/png" sizes="192x192" href="/img/icon-192.png">
<link rel="icon" href="/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="48x48" href="/favicon-48.png">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script>
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<header><div class="in"><a class="logo" href="/"><img src="/img/logo.svg" alt="Nature's Nook home" width="72" height="44"></a><a href="/">&larr; Back to naturesnook.co</a></div></header>
<main id="main" tabindex="-1">
<h1>{e(page['h1'])}</h1>
<p>{e(page['intro'])}</p>
<p>{e(page['more'])}</p>
<p><a class="btn" href="{link(page)}">Search these products ({n:,} listed)</a><a class="btn ghost" href="tel:+12083565284">Call (208) 356-5284</a></p>
<h2>Brands we carry</h2>
<ul class="brands">{''.join(f'<li>{e(b)}</li>' for b in shown)}</ul>
<h2>A few things on our shelves</h2>
<ul class="ex">{ex_html}</ul>
<p>This is a small sample. Prices and stock change, so the price in store applies.</p>
<div class="box visit">
<h2 style="margin-top:0">Visit Nature's Nook</h2>
<p><strong>160 E Valley River Rd #2, Rexburg, ID 83440</strong><br>Monday&ndash;Friday 9:00 AM&ndash;6:00 PM &middot; Saturday 9:00 AM&ndash;5:00 PM &middot; Sunday closed<br><a href="tel:+12083565284">(208) 356-5284</a> &middot; <a href="https://www.google.com/maps/place/Nature's+Nook/@43.8328504,-111.7814928,17z/data=!3m1!4b1!4m5!3m4!1s0x53540a4f81e4cd11:0x3eac0f64cb6f41e9!8m2!3d43.8328504!4d-111.7793041" rel="noopener">Directions</a></p>
</div>
<h2>More from Nature's Nook</h2>
<ul class="cats">{others}<li><a href="/">Home</a></li></ul>
{FDA if page['fda'] else ''}
</main>
{FOOT}
</body>
</html>
"""
    d = ROOT + page['slug']
    os.makedirs(d, exist_ok=True)
    open(d + '/index.html', 'w').write(out)


for pg in PAGES:
    build(pg)

urls = [('/', '1.0', 'weekly')] + [(f"/{p['slug']}/", '0.8', 'weekly') for p in PAGES] + \
       [(f'/{s}/', '0.3', 'yearly') for s in ('returns', 'privacy', 'cookies', 'terms', 'accessibility')]
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
for u, pr, fr in urls:
    sm += f'  <url><loc>{SITE}{u}</loc><lastmod>{TODAY}</lastmod><changefreq>{fr}</changefreq><priority>{pr}</priority></url>\n'
sm += '</urlset>\n'
open(ROOT + 'sitemap.xml', 'w').write(sm)
open(ROOT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print('pages:', len(PAGES), '| sitemap urls:', len(urls))
