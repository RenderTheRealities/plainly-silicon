"""Thumbnail for video 05: terminal-green load bars racing (HDD crawling vs SSD done) + big text."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
# THEMES["terminal"] colors
NAVY = (6, 10, 7); PANEL = (10, 20, 12); GRID = (16, 32, 20); GREEN = (74, 222, 128)
AMBER = (250, 204, 21); WHITE = (214, 240, 220); MUTED = (110, 150, 120); RED = (248, 113, 113)
DV = "/usr/share/fonts/truetype/dejavu/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
d0 = ImageDraw.Draw(img)
for gy in range(0, h, 4 * K):  # scanlines
    d0.line([(0, gy), (w, gy)], fill=GRID + (140,), width=K)
glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(glow).ellipse([w * 0.40, h * 0.05, w * 1.15, h * 1.05], fill=(20, 60, 30, 255))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(170)))

layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
d = ImageDraw.Draw(layer)
mono = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 44 * K)
small = ImageFont.truetype(DV + "DejaVuSansMono.ttf", 30 * K)

# terminal window on the right with two race bars
x0, y0, x1, y1 = 660 * K, 150 * K, 1235 * K, 600 * K
d.rounded_rectangle([x0, y0, x1, y1], radius=14 * K, fill=PANEL + (255,), outline=GREEN + (255,), width=4 * K)
d.line([(x0, y0 + 56 * K), (x1, y0 + 56 * K)], fill=GREEN + (160,), width=3 * K)
for k in range(3):
    cx = x0 + 32 * K + k * 34 * K
    d.ellipse([cx - 9 * K, y0 + 19 * K, cx + 9 * K, y0 + 37 * K], outline=GREEN + (255,), width=3 * K)
d.text((x0 + 140 * K, y0 + 28 * K), "load_level", font=small, fill=MUTED + (255,), anchor="lm")

rows = [("SSD", 1.0, AMBER, "6s READY"), ("HDD", 0.1, WHITE, "63s ...")]
for i, (nm, frac, c, tag) in enumerate(rows):
    yy = y0 + 120 * K + i * 160 * K
    d.text((x0 + 36 * K, yy), nm, font=mono, fill=c + (255,), anchor="lm")
    bx0, bx1 = x0 + 170 * K, x1 - 40 * K
    d.rectangle([bx0, yy - 30 * K, bx1, yy + 30 * K], outline=c + (120,), width=3 * K)
    d.rectangle([bx0 + 8 * K, yy - 22 * K, bx0 + 8 * K + (bx1 - bx0 - 16 * K) * frac, yy + 22 * K], fill=c + (255,))
    d.text((bx1, yy + 62 * K), tag, font=mono, fill=c + (255,), anchor="rm")
g = layer.filter(ImageFilter.GaussianBlur(12 * K))
img.alpha_composite(g); img.alpha_composite(layer)

# big text left
t1 = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 150 * K)
t2 = ImageFont.truetype(DV + "DejaVuSansMono-Bold.ttf", 96 * K)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
lines = [((56 * K, 110 * K), "63s", t1, WHITE), ((56 * K, 290 * K), "vs", t2, MUTED), ((56 * K, 410 * K), "6s", t1, AMBER)]
for (xy, s, f, c) in lines:
    sd.text((xy[0] + 6 * K, xy[1] + 6 * K), s, font=f, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(14 * K)))
dd = ImageDraw.Draw(img)
for (xy, s, f, c) in lines:
    dd.text(xy, s, font=f, fill=c + (255,))

logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))

img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
