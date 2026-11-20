"""Product photo copies. The site stores ONLY WebP files (no JPG masters), so it stays well under GitHub Pages' 1 GB limit:
  photo_lib/w/UPC-kind.webp  full-size picture, shown in the product view and on the coupon  (kind: front, back, facts)
  photo_lib/t/UPC-kind.webp  small copy for cards (front: the square the card shows, 360 px; back/facts: 192 px long side)
  photo_lib/s/UPC-kind.webp  tiny copy of the whole picture (192 px long side), for the thumbnail strip in the product view
Add a photo with tools/photo_lib.py; rebuild.py calls build() so the small copies always match the full-size one.
build() only (re)makes a small copy when it is missing or older than its full-size picture."""
import os, json
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
L = ROOT + 'photo_lib/'
def _focus(stem):
    """how far down the tall front picture the card square sits (0 = top, 1 = bottom). Default .55 suits bottles;
    boxes whose name sits higher get an entry in data/thumb_focus.json {UPC: fraction}"""
    try: return float(json.load(open(ROOT + 'data/thumb_focus.json')).get(stem[:-6], 0.55))
    except Exception: return 0.55
def small(src, stem):
    """make t/ and s/ copies of one full-size WebP (src) named stem (UPC-kind)"""
    im = Image.open(src).convert('RGB')
    s = im.copy(); s.thumbnail((192, 192), Image.LANCZOS)
    s.save(f'{L}s/{stem}.webp', 'WEBP', quality=72, method=4)
    if stem.endswith('-front'):
        W, H = im.size; t = im
        fo = _focus(stem)
        if fo != 0.55 and H > W:  # box with its name high up: cut the wide 16:9 window the card shows, top at fo of the free height
            ch = round(W * 9 / 16); top = round(fo * (H - ch)); t = im.crop((0, top, W, top + ch))
        elif H > W:  # cards show a square (object-fit: cover, 55% down), so keep only that part
            top = round(fo * (H - W)); t = im.crop((0, top, W, top + W))
        if t.width > 360: t = t.resize((360, round(t.height * 360 / t.width)), Image.LANCZOS)
    else:
        t = im.copy(); t.thumbnail((192, 192), Image.LANCZOS)
    t.save(f'{L}t/{stem}.webp', 'WEBP', quality=72, method=4)
def build():
    for d in ('w', 't', 's'): os.makedirs(L + d, exist_ok=True)
    made = 0
    for f in sorted(os.listdir(L + 'w')):
        if not f.endswith(('-front.webp', '-facts.webp', '-back.webp')): continue
        src = L + 'w/' + f; stem = f[:-5]
        if all(os.path.exists(f'{L}{d}/{f}') and os.path.getmtime(f'{L}{d}/{f}') >= os.path.getmtime(src) for d in 'ts'): continue
        small(src, stem); made += 1
    return made
if __name__ == '__main__': print('small copies made', build())
