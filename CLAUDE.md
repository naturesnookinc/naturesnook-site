# Nature's Nook website

Live at **naturesnook.co** via GitHub Pages (this repo's `main` branch, root folder).

## What's here
- `index.html` – the whole site (catalog data is embedded; rebuilt by `tools/rebuild.py`)
- `img/` – storefront and in-store photos
- `photo_lib/` – product photos, WebP only (no JPG masters, to stay under GitHub Pages' 1 GB limit): `w/` full-size (`UPC-front.webp`, `UPC-back.webp`, `UPC-facts.webp`), `t/` small copies for cards, `s/` tiny copies for the thumbnail strip. Add photos with `python3 tools/photo_lib.py UPC kind file` (it makes all three copies); `rebuild.py` attaches them and refreshes any missing small copies
- `data/products.json` – the product catalog (source of truth for prices, names, member deals, staff picks)
- `data/thumb_focus.json` – optional per-UPC card-thumbnail position for tall box pictures whose name sits high up (`{UPC: 0-1}`). Listed products get a wide 16:9 card crop starting that fraction down the picture, so the product name and subtitle show on the search card; everything else keeps the bottle default (square at .55). Delete the product's `t/UPC-front.webp` and run `rebuild.py` after changing it
- `data/photo_ver.json` – `{UPC: n}`; when a product's picture is REPLACED (same file name), set or bump its number so browsers fetch the new picture instead of the cached old one (adds `?v=n` to that product's photo links)
- `data/facts.json` – clean Supplement Facts / essential-oil Label Details tables, keyed by UPC
- `tools/` – `rebuild.py` (rebuild index.html from data + photos), `photo_lib.py` (add product photos),
  `apply.py` (apply a batch of shelf-tag rows), `look.py` (look a UPC/name up on the site and in the register export)

## Catalog rules
- Use the package label name; price always from the shelf tag.
- Never double-add (dedupe by UPC); every variant is its own product.
- Everyday Savings: show the regular price crossed out (`msrp`). Member deals: only blue SaveNaturally tags.
- Monthly coupon specials (bring in / show at the register, not SaveNaturally): run `python3 tools/specials.py YYYY-MM-DD UPC[:dollars_off] ...` (clears last month's, sets the new ones, default $2 off, runs rebuild). Standard card: gold badge, front photo (`photo_lib/w/UPC-front.webp`, already on the site, so coupons never need new pictures), name, brand and size, was/now price. 4 to 8 items looks best. They show on the member coupon only, never on product cards.

**Coupon layout standard (Nov 2026):** the coupon is for everyone, member or not, so no "member" wording inside it (headline, footer, print, share text). Big "Specials this month" headline on top, one line under it ("$X off each item below. Bring this in or show us at the register. No membership needed."), then the product cards (photo, name, brand and size, was/now price) in one row on desktop and two across on phones. The "More savings for members" block (SaveNaturally deals, free signup, loyalty points, brands, See all member deals) sits below the coupon box, never inside it, and does not print. The standalone `coupon/` page must match this standard.

**Coupon photos always show the full bottle or box** (the full-size front picture in `photo_lib/w/`, never the cropped card thumbnail from `photo_lib/t/`), on the site coupon, the `coupon/` page and the share/post images.

**Updating the coupon updates everything that goes with it.** `tools/specials.py` now also runs `tools/coupon_page.py`, which rebuilds `coupon/index.html` (the shareable page, with its title, description, link-preview tags and expiry date), `img/coupon-share.jpg` (link preview) and `img/coupon-post.jpg` (social post image). Then check by hand: the "This month" banner in `index.html`, and the Search Console / Bing request to re-fetch /coupon/ if it changed a lot. Run `python3 tools/seo.py` only if the catalog itself changed.
- Discontinued brands: set `notice` on the product in `data/products.json` (shown as a plain line under the price in the product view). Biochem has it (Nov 2026). Remove the product when it sells out.
- Never add manufacturer/brand coupons. Yellow staff-pick tags go in `fav`.
- The register (Catapult) inventory export is private and is **not** stored in this public repo.

## Update workflow
Edit `data/*.json` or add photos, run `python3 tools/rebuild.py`, commit, push. Pages redeploys in ~1 minute.

## Important
index.html must keep its first lines (`<!doctype html>`, `<meta charset="utf-8">`, `<meta name="viewport" ...>`). Without them phones show the desktop layout zoomed out.

The site is light-only: keep `<html lang="en" data-theme="light">` and `<meta name="color-scheme" content="light">`. Removing them lets phones in dark mode turn the text light on the light background (unreadable).

## Policies, claims and accessibility (added November 2026)
- Policy pages live in `returns/`, `privacy/`, `cookies/`, `terms/`, `accessibility/` (plain HTML, linked from the footer). Update the "Last updated" date when one changes.
- The privacy and cookie pages say the site has **no forms, no analytics, no cookies and no trackers**. Before adding any of those (pickup ordering, sign-up form, analytics, embeds), update those pages first and add consent wording to the form. Pickup ordering is built but dormant: see `tools/pickup/README.md`; `tools/pickup/golive.py <Apps Script URL>` switches it on and updates the privacy, cookie and terms pages together.
- Return policy: 30 days with receipt for a refund; store credit without a receipt, within 30 days.
- No health claims in our own words: never tie a product to a disease or to replacing a medicine (search notes, section labels, banners). Label wording copied from the package is fine. Keep the FDA disclaimer in the footer and product view.
- Reviews must be real Google reviews quoted as written, labeled as a selection.
- Accessibility: keep text contrast at 4.5:1 or better (`--pine` is `#1d7542` for this reason), keep alt text, visible focus outlines, the skip link, the dialog focus trap and the slideshow Pause buttons.

## Product photo standard (added November 2026)
- Each product has two photos: **front** = the full-body product picture, and **facts** = the full-body side/back picture with the clean Supplement Facts panel (never crop the facts picture down to just the panel).
- **Every product with photos also gets its clean Supplement Facts table in `data/facts.json`** (typed from the label, easy to read), never just the facts photo. All the photos (front, back, side panels) stay in the picture gallery. Where print is too small or smudged to read with confidence (e.g. probiotic strain codes), leave that detail out and say "printed on the label photos" rather than guess.
- Only use the good product pictures the owner uploads for this. **Never crop pictures out of shelf/tag photos** used to add or update products; add the product data from the tag and leave the photo empty until good pictures arrive.
- Each picture is its own product on its own: no edges of neighboring containers.

## SEO (added November 2026)
- `tools/seo.py` builds the Rexburg department pages (six departments plus protein-powder and electrolytes pages, which are product-filtered by regex in PAGES), `sitemap.xml` and `robots.txt`. Run it after `rebuild.py` whenever the catalog changes, then commit the generated folders.
- `index.html` carries HealthFoodStore JSON-LD (address, phone, hours, map). If hours, phone or address change, update the JSON-LD, the hours table, and `tools/seo.py` together.
- Never add aggregateRating/review markup unless it comes from real Google reviews.
- Department pages describe what we carry only (brands, product names). No health claims; `seo.py` skips disease-implying product names in sample lists.
- `?dept=` and `?q=` links open the product search pre-filtered.
- Kids: the **Kids** chip (`?dept=Kids`) and the search words "kids"/"children" use `KIDRX`/`KIDEX` in `index.html`; `tools/seo.py` mirrors them in `is_kid()` and builds `kids-products-rexburg`, `kids-vitamins-rexburg`, `kids-herbs-homeopathics-rexburg`, `kids-toothpaste-baby-care-rexburg`. Keep the two regexes in step. Baby: the **Baby** chip (`?dept=Baby`) and the search words "baby"/"babies"/"infant"/"newborn" use `BABYRX` in `index.html`, mirrored by `BABYRX`/`is_baby()` in `tools/seo.py`, which builds `baby-products-rexburg`. New kids products are picked up automatically; rerun `seo.py` after catalog changes.
