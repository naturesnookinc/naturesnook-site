#!/usr/bin/env python3
"""Counter QR cards (4x6 in, 300 dpi). Usage: python3 tools/qrcards.py OUTDIR
Set REVIEW_URL to the Google review link (Business Profile > Ask for reviews > Share review form)."""
import sys, io, segno
from PIL import Image, ImageDraw, ImageFont
SITE = "https://naturesnook.co"
REVIEW_URL = sys.argv[2] if len(sys.argv) > 2 else "https://www.google.com/maps?cid=4516001451929977321"
PINE = (29, 117, 66); INK = (34, 34, 34); HONEY = (201, 150, 46); BG = (251, 249, 243)
F = "/usr/share/fonts/opentype/inter/Inter-%s.otf"
def font(w, s):
    try: return ImageFont.truetype(F % w, s)
    except Exception: return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", s)
def card(url, head, sub, foot, path):
    W, H = 1200, 1800
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 28], fill=PINE)
    def center(t, y, f, fill):
        w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=fill)
    center(head[0], 150, font("Bold", 110), INK)
    center(head[1], 280, font("Bold", 110), PINE)
    d.rectangle([W/2-60, 440, W/2+60, 446], fill=HONEY)
    center(sub, 480, font("Regular", 46), INK)
    q = segno.make(url, error="m")
    buf = io.BytesIO(); q.save(buf, kind="png", scale=30, border=0, dark=INK, light=(255, 255, 255)); buf.seek(0)
    qi = Image.open(buf).convert("RGB"); qs = 760
    qi = qi.resize((qs, qs), Image.NEAREST)
    x, y = (W - qs) // 2, 640
    d.rectangle([x-50, y-50, x+qs+50, y+qs+50], fill=(255, 255, 255), outline=(222, 216, 200), width=3)
    im.paste(qi, (x, y))
    center("Point your phone camera at the code", y+qs+110, font("Medium", 44), INK)
    center(foot, 1600, font("Bold", 52), PINE)
    center("160 E Valley River Rd #2, Rexburg", 1675, font("Regular", 36), INK)
    im.save(path)
out = sys.argv[1]
card(REVIEW_URL, ("Enjoyed your visit?", "Leave us a review"), "It takes under a minute and helps a lot", "Nature's Nook", out + "/qr-google-review.png")
card(SITE, ("Shop Nature's Nook", "online"), "Browse our products, specials and hours", "naturesnook.co", out + "/qr-website.png")
for n in ("qr-google-review", "qr-website"):
    Image.open(f"{out}/{n}.png").save(f"{out}/{n}.pdf", resolution=300)
print("ok")
