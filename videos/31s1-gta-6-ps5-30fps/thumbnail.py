"""Draft Shorts cover for 31s1 (Canva credits out Nov 26): 1080x1920, full-bleed sunset gradient,
all text and art inside y 190-1760 (YouTube's 2:3 crop). Logo added by brand_thumb.py."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from render import BRAND_TITLE_FONT
W, H = 1080, 1920
top, bot = (30, 14, 48), (244, 114, 182)
img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
for y in range(H):
    f = (y / H) ** 1.6
    d.line([(0, y), (W, y)], fill=tuple(int(top[i] + (bot[i] - top[i]) * f) for i in range(3)))
# sun + horizon stripes (full-bleed decoration)
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
gd.ellipse([140, 1150, 940, 1950], fill=(251, 146, 60, 200))
img.paste(glow.filter(ImageFilter.GaussianBlur(60)), (0, 0), glow.filter(ImageFilter.GaussianBlur(60)))
for k, yy in enumerate(range(1500, 1920, 46)):
    d.rectangle([0, yy, W, yy + 10 + k * 2], fill=(30, 14, 48))
F = lambda n: ImageFont.truetype(BRAND_TITLE_FONT, n)
def ctext(y, s, n, fill, stroke=8):
    d.text((W / 2, y), s, font=F(n), fill=fill, anchor="mm", stroke_width=stroke, stroke_fill=(20, 8, 32))
ctext(340, "GTA 6", 195, (255, 255, 255))
ctext(545, "ONLY 30?", 150, (251, 146, 60))
# FPS counter panel
d.rounded_rectangle([170, 700, 910, 1250], radius=44, fill=(20, 10, 34), outline=(255, 255, 255), width=8)
d.text((W / 2, 770), "FPS", font=F(56), fill=(190, 150, 190), anchor="mm")
d.text((W / 2, 1000), "60", font=F(300), fill=(110, 231, 183, 80), anchor="mm")
d.line([(240, 1160), (840, 800)], fill=(255, 80, 80), width=22)
d.text((W / 2 + 150, 1130), "30", font=F(170), fill=(251, 146, 60), anchor="mm", stroke_width=6, stroke_fill=(20, 8, 32))
ctext(1420, "Can your PC run it?", 76, (255, 255, 255), stroke=6)
img.save(os.path.join(HERE, "thumbnail_raw.jpg"), quality=92)
print("ok")
