# usage: python3 tools/photo_lib.py UPC kind imagefile [UPC kind imagefile ...]   (kind: front|facts|back)
# Saves the full-size WebP in photo_lib/w/UPC-kind.webp and its small copies (t/ for cards, s/ for thumbnails);
# rebuild.py attaches them to the product on the site. No JPG is kept (see tools/webp.py).
import sys, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
sys.path.insert(0, ROOT + 'tools'); import webp
for d in ('w', 't', 's'): os.makedirs(ROOT + f'photo_lib/{d}', exist_ok=True)
args = sys.argv[1:]
for i in range(0, len(args), 3):
    upc, kind, f = args[i:i+3]
    im = Image.open(f).convert('RGBA')
    bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3])
    w = {'front': 900, 'facts': 1400, 'back': 1400}[kind]  # larger so the click-to-enlarge view stays sharp (never upscales)
    bg.thumbnail((w, w * 3))
    out = ROOT + f'photo_lib/w/{upc}-{kind}.webp'
    bg.save(out, 'WEBP', quality=78, method=6)
    webp.small(out, f'{upc}-{kind}')
    print(upc, kind, bg.size)
