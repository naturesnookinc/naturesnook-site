"""Make the fast copies of every product photo (rebuild.py calls this; run by hand if you like).
photo_lib/UPC-kind.jpg stays the master (coupon page and share images use it).
  photo_lib/w/UPC-kind.webp  full-size WebP, shown in the product view
  photo_lib/t/UPC-kind.webp  small WebP for cards and thumbnails (front: the square the card shows, 360 px; back/facts: 192 px on the long side)
  photo_lib/s/UPC-kind.webp  tiny WebP of the whole picture (192 px long side), for the thumbnail strip in the product view
Only (re)makes a file when the master is newer."""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
L = ROOT + 'photo_lib/'
def build():
    for d in ('w', 't', 's'): os.makedirs(L + d, exist_ok=True)
    made = 0
    for f in sorted(os.listdir(L)):
        if not f.endswith(('-front.jpg', '-facts.jpg', '-back.jpg')): continue
        src = L + f; stem = f[:-4]
        for d, q in (('w', 78), ('t', 72), ('s', 72)):
            out = f'{L}{d}/{stem}.webp'
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src): continue
            im = Image.open(src).convert('RGB')
            if d == 's':
                im.thumbnail((192, 192), Image.LANCZOS)
            elif d == 't':
                if f.endswith('-front.jpg'):
                    W, H = im.size
                    if H > W:  # cards show a square (object-fit: cover, 55% down), so keep only that part
                        top = round(0.55 * (H - W)); im = im.crop((0, top, W, top + W))
                    if im.width > 360: im = im.resize((360, round(im.height * 360 / im.width)), Image.LANCZOS)
                else:
                    im.thumbnail((192, 192), Image.LANCZOS)
            im.save(out, 'WEBP', quality=q, method=4); made += 1
    return made
if __name__ == '__main__': print('webp files made', build())
