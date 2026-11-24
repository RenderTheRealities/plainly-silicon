"""Thumbnail for video 23: one big neon graphics card with an S-tier badge + 2 words."""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT)
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from render import BRAND_TITLE_FONT, THEMES

T = THEMES["neon"]
BG, PANEL, MAG, CY, WHITE, GREEN = T["NAVY"], T["PANEL"], T["CYAN"], T["AMBER"], T["WHITE"], T["GREEN"]
W, H, K = 1280, 720, 2
S = lambda *v: [p * K for p in v]
img = Image.new("RGBA", (W * K, H * K), BG + (255,))

# glow blobs behind the card
glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
gd = ImageDraw.Draw(glow)
gd.ellipse(S(560, 60, 1300, 700), fill=MAG + (150,))
gd.ellipse(S(820, 300, 1340, 760), fill=CY + (110,))
img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(120 * K)))

# the card, drawn flat then given a slight perspective tilt
cw, ch = 900, 400
card = Image.new("RGBA", (cw * K, ch * K), (0, 0, 0, 0))
c = ImageDraw.Draw(card)
c.rounded_rectangle(S(10, 30, cw - 10, ch - 60), radius=36 * K, fill=PANEL + (255,), outline=MAG + (255,), width=8 * K)
for fx in (250, 640):
    cx, cy, r = fx, 185, 140
    c.ellipse(S(cx - r, cy - r, cx + r, cy + r), outline=CY + (255,), width=8 * K, fill=(10, 8, 22, 255))
    for k in range(9):
        a = k * 2 * math.pi / 9
        c.line(S(cx, cy, cx + r * 0.9 * math.cos(a + 0.4), cy + r * 0.9 * math.sin(a + 0.4)), fill=CY + (200,), width=6 * K)
    c.ellipse(S(cx - 34, cy - 34, cx + 34, cy + 34), fill=MAG + (255,))
for k in range(22):  # gold fingers
    gx = 300 + k * 16
    c.rectangle(S(gx, ch - 60, gx + 10, ch - 22), fill=(250, 204, 21, 255))
card = card.transform(card.size, Image.PERSPECTIVE,
                      (1.06, 0.10, -40 * K, 0.0, 1.0, 0, 0.00012 / K, 0.0), resample=Image.BICUBIC)
img.alpha_composite(card, (400 * K, 190 * K))

d = ImageDraw.Draw(img)
# S-tier badge on the card
d.rounded_rectangle(S(1040, 120, 1220, 300), radius=28 * K, fill=GREEN + (255,))
f = ImageFont.truetype(BRAND_TITLE_FONT, 150 * K)
d.text(S(1130, 212), "S", font=f, fill=BG, anchor="mm")

# words: brand title font, max 3, not repeating the title
f1 = ImageFont.truetype(BRAND_TITLE_FONT, 150 * K)
d.text(S(50, 40), "NOT", font=f1, fill=WHITE, stroke_width=6 * K, stroke_fill=BG)
d.text(S(50, 200), "NVIDIA.", font=f1, fill=CY, stroke_width=6 * K, stroke_fill=BG)

logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((72 * K, 72 * K))
img.alpha_composite(logo, (1188 * K, 628 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
img.convert("RGB").resize((320, 180), Image.LANCZOS).save(os.path.join(HERE, "preview_thumb_small.png"))
print("ok")
