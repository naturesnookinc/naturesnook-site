# usage: python3 tools/photo_lib.py UPC kind imagefile [UPC kind imagefile ...]   (kind: front|facts|back)
# Stores a compressed JPEG in photo_lib/UPC-kind.jpg; rebuild.py attaches it to the product on the site.
import sys, os
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/'
args = sys.argv[1:]
for i in range(0, len(args), 3):
    upc, kind, f = args[i:i+3]
    im = Image.open(f).convert('RGBA')
    bg = Image.new('RGB', im.size, 'white'); bg.paste(im, mask=im.split()[3])
    w = {'front': 420, 'facts': 700, 'back': 700}[kind]
    bg.thumbnail((w, w * 3))
    bg.save(ROOT + f'photo_lib/{upc}-{kind}.jpg', quality=78, optimize=True)
    print(upc, kind, bg.size)
