"""Fallback thumbnail for Short 10s2 (Canva credits ran out Nov 26, 2026): a gold 80 Plus-style
badge with a red crack, and 2 words in the brand title font. Logo added by brand_thumb.py."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from render import BRAND_TITLE_FONT
W, H, K = 1280, 720, 2
BG, NAVY, RED, GOLD, GOLD2 = (250, 250, 250), (17, 24, 39), (220, 38, 38), (212, 160, 23), (245, 205, 80)
img = Image.new("RGB", (W * K, H * K), BG); d = ImageDraw.Draw(img)
for x in range(40, W, 80):
    for y in range(40, H, 80):
        d.line([((x - 7) * K, y * K), ((x + 7) * K, y * K)], fill=(225, 225, 228), width=2 * K)
        d.line([(x * K, (y - 7) * K), (x * K, (y + 7) * K)], fill=(225, 225, 228), width=2 * K)
cx, cy, R = 930, 380, 250
sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); ImageDraw.Draw(sh).ellipse([(cx - R + 14) * K, (cy - R + 24) * K, (cx + R + 14) * K, (cy + R + 24) * K], fill=(0, 0, 0, 90))
img.paste(sh.filter(ImageFilter.GaussianBlur(30 * K)), (0, 0), sh.filter(ImageFilter.GaussianBlur(30 * K)))
pts = [(cx + (R if k % 2 == 0 else R * 0.9) * math.cos(math.pi * k / 24) , cy + (R if k % 2 == 0 else R * 0.9) * math.sin(math.pi * k / 24)) for k in range(48)]
d.polygon([(x * K, y * K) for x, y in pts], fill=GOLD)
d.ellipse([(cx - R * 0.78) * K, (cy - R * 0.78) * K, (cx + R * 0.78) * K, (cy + R * 0.78) * K], fill=GOLD2, outline=(255, 255, 255), width=6 * K)
f1 = ImageFont.truetype(BRAND_TITLE_FONT, 74 * K); f2 = ImageFont.truetype(BRAND_TITLE_FONT, 92 * K)
d.text((cx * K, (cy - 50) * K), "80 PLUS", font=f1, fill=NAVY, anchor="mm"); d.text((cx * K, (cy + 45) * K), "GOLD", font=f2, fill=(140, 95, 0), anchor="mm")
crack = [(cx - 40, cy - R - 10), (cx + 10, cy - 120), (cx - 30, cy - 40), (cx + 35, cy + 30), (cx - 10, cy + 120), (cx + 30, cy + R + 10)]
d.line([(x * K, y * K) for x, y in crack], fill=RED, width=16 * K, joint="curve")
ft = ImageFont.truetype(BRAND_TITLE_FONT, 150 * K)
d.text((50 * K, 150 * K), "NOT", font=ft, fill=NAVY, stroke_width=4 * K, stroke_fill=BG)
d.text((50 * K, 330 * K), "QUALITY", font=ImageFont.truetype(BRAND_TITLE_FONT, 120 * K), fill=RED, stroke_width=4 * K, stroke_fill=BG)
img.resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail_raw.jpg"), quality=92)
print("ok")
