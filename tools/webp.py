"""Make the fast copies of every product photo (rebuild.py calls this; run by hand if you like).
photo_lib/UPC-kind.jpg stays the master (coupon page and share images use it).
  photo_lib/w/UPC-kind.webp  full-size WebP, shown in the product view
  photo_lib/t/UPC-kind.webp  small WebP (front 480 px wide, back/facts 240), shown on cards and thumbnails
Only (re)makes a file when the master is newer."""
import os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
L = ROOT + 'photo_lib/'
def build():
    for d in ('w', 't'): os.makedirs(L + d, exist_ok=True)
    made = 0
    for f in sorted(os.listdir(L)):
        if not f.endswith(('-front.jpg', '-facts.jpg', '-back.jpg')): continue
        src = L + f; stem = f[:-4]
        for d, width, q in (('w', None, 78), ('t', 480 if f.endswith('-front.jpg') else 240, 74)):
            out = f'{L}{d}/{stem}.webp'
            if os.path.exists(out) and os.path.getmtime(out) >= os.path.getmtime(src): continue
            im = Image.open(src).convert('RGB')
            if width and im.width > width: im = im.resize((width, round(im.height * width / im.width)), Image.LANCZOS)
            im.save(out, 'WEBP', quality=q, method=6); made += 1
    return made
if __name__ == '__main__': print('webp files made', build())
