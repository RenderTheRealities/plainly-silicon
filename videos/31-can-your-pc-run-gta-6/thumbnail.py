"""Draft thumbnail for video 31 (Canva credits out): 1280x720, crimson theme, one big red-hot CPU chip,
words "STUCK AT 30" (don't repeat the title). Logo added top-right by brand_thumb.py; bottom-right kept clear."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from render import BRAND_TITLE_FONT, THEMES
T = THEMES["crimson"]; BG, PANEL, YEL, PINK, WHITE, RED = T["NAVY"], T["PANEL"], T["CYAN"], T["AMBER"], T["WHITE"], T["RED"]
W, H, K = 1280, 720, 2
img = Image.new("RGB", (W * K, H * K), BG)
g = Image.new("RGBA", img.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
gd.ellipse([780 * K, 60 * K, 1300 * K, 640 * K], fill=(255, 70, 40, 170))
img.paste(g.filter(ImageFilter.GaussianBlur(90 * K)), (0, 0), g.filter(ImageFilter.GaussianBlur(90 * K)))
d = ImageDraw.Draw(img)
cx, cy, s = 960, 360, 360
h = s / 2
d.rounded_rectangle([(cx - h) * K, (cy - h) * K, (cx + h) * K, (cy + h) * K], radius=30 * K, fill=(40, 6, 12), outline=(255, 90, 60), width=10 * K)
for i in range(1, 8):
    o = -h + s / 8 * i
    for a, b in [((cx + o, cy - h), (cx + o, cy - h - 50)), ((cx + o, cy + h), (cx + o, cy + h + 50)),
                 ((cx - h, cy + o), (cx - h - 50, cy + o)), ((cx + h, cy + o), (cx + h + 50, cy + o))]:
        d.line([(a[0] * K, a[1] * K), (b[0] * K, b[1] * K)], fill=(255, 120, 80), width=10 * K)
d.rounded_rectangle([(cx - 110) * K, (cy - 110) * K, (cx + 110) * K, (cy + 110) * K], radius=16 * K, fill=(255, 90, 60))
d.text((cx * K, cy * K), "CPU", font=ImageFont.truetype(BRAND_TITLE_FONT, 92 * K), fill=(40, 6, 12), anchor="mm")
F = lambda n: ImageFont.truetype(BRAND_TITLE_FONT, n * K)
d.text((60 * K, 70 * K), "STUCK", font=F(170), fill=WHITE, stroke_width=6 * K, stroke_fill=BG)
d.text((60 * K, 260 * K), "AT", font=F(170), fill=WHITE, stroke_width=6 * K, stroke_fill=BG)
d.text((300 * K, 230 * K), "30", font=F(300), fill=YEL, stroke_width=8 * K, stroke_fill=BG)
img.resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail_raw.jpg"), quality=92)
print("ok")
