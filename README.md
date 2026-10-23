# Nature's Nook website

Live at **naturesnook.co** via GitHub Pages (this repo's `main` branch, root folder).

## What's here
- `index.html` – the whole site (catalog data is embedded; rebuilt by `tools/rebuild.py`)
- `img/` – storefront and in-store photos
- `photo_lib/` – product photos: `UPC-front.jpg`, `UPC-back.jpg`, `UPC-facts.jpg`
- `data/products.json` – the product catalog (source of truth for prices, names, member deals, staff picks)
- `data/facts.json` – clean Supplement Facts / essential-oil Label Details tables, keyed by UPC
- `tools/` – `rebuild.py` (rebuild index.html from data + photos), `photo_lib.py` (add product photos),
  `apply.py` (apply a batch of shelf-tag rows), `look.py` (look a UPC/name up on the site and in the register export)

## Catalog rules
- Use the package label name; price always from the shelf tag.
- Never double-add (dedupe by UPC); every variant is its own product.
- Everyday Savings: show the regular price crossed out (`msrp`). Member deals: only blue SaveNaturally tags.
- Never add manufacturer/brand coupons. Yellow staff-pick tags go in `fav`.
- The register (Catapult) inventory export is private and is **not** stored in this public repo.

## Update workflow
Edit `data/*.json` or add photos, run `python3 tools/rebuild.py`, commit, push. Pages redeploys in ~1 minute.
