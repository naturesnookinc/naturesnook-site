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

## Important
index.html must keep its first lines (`<!doctype html>`, `<meta charset="utf-8">`, `<meta name="viewport" ...>`). Without them phones show the desktop layout zoomed out.

## Policies, claims and accessibility (added November 2026)
- Policy pages live in `returns/`, `privacy/`, `cookies/`, `terms/`, `accessibility/` (plain HTML, linked from the footer). Update the "Last updated" date when one changes.
- The privacy and cookie pages say the site has **no forms, no analytics, no cookies and no trackers**. Before adding any of those (pickup ordering, sign-up form, analytics, embeds), update those pages first and add consent wording to the form.
- Return policy: 30 days with receipt for a refund; store credit without a receipt, within 30 days.
- No health claims in our own words: never tie a product to a disease or to replacing a medicine (search notes, section labels, banners). Label wording copied from the package is fine. Keep the FDA disclaimer in the footer and product view.
- Reviews must be real Google reviews quoted as written, labeled as a selection.
- Accessibility: keep text contrast at 4.5:1 or better (`--pine` is `#1d7542` for this reason), keep alt text, visible focus outlines, the skip link, the dialog focus trap and the slideshow Pause buttons.
