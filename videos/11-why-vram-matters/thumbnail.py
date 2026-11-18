"""Thumbnail for video 11: an overfull VRAM suitcase spilling tiles, graphite palette."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
BG = (28, 30, 34); PANEL = (40, 43, 48); DOT = (52, 55, 62); WHITE = (241, 245, 249)
RED = (239, 68, 68); MUTED = (148, 155, 165); GREEN = (74, 222, 128)
GF = "/usr/share/fonts/truetype/google-fonts/"
FD = "/usr/share/fonts/opentype/inter/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), BG + (255,))
d = ImageDraw.Draw(img)
for gx in range(20, W, 40):
    for gy in range(20, H, 40):
        d.ellipse([(gx - 2) * K, (gy - 2) * K, (gx + 2) * K, (gy + 2) * K], fill=DOT)


def S(*v):
    return [p * K for p in v]


def lora(size):
    f = ImageFont.truetype(GF + "Lora-Variable.ttf", size * K)
    f.set_variation_by_name(b"Bold")
    return f


# glow behind the suitcase
gl = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(gl).rounded_rectangle(S(760, 150, 1180, 570), radius=30 * K, outline=RED + (150,), width=30 * K)
img.alpha_composite(gl.filter(ImageFilter.GaussianBlur(22 * K)))
d = ImageDraw.Draw(img)
# suitcase
d.rounded_rectangle(S(900, 100, 1040, 150), radius=16 * K, outline=WHITE, width=7 * K)
d.rounded_rectangle(S(760, 140, 1180, 570), radius=24 * K, fill=PANEL, outline=WHITE, width=8 * K)
cell = 48
for r in range(8):
    for c in range(8):
        x0, y0 = 782 + c * cell, 162 + r * cell
        fill = RED if (r * 8 + c) >= 52 else WHITE
        d.rectangle(S(x0 + 4, y0 + 4, x0 + cell - 4, y0 + cell - 4), fill=fill)
# spilled tiles flying out to the left
for i, (sx, sy, rot) in enumerate([(700, 240, 12), (680, 330, -18), (705, 420, 25), (660, 480, -8), (690, 560, 15)]):
    t = Image.new("RGBA", (44 * K, 44 * K), (0, 0, 0, 0))
    ImageDraw.Draw(t).rectangle([0, 0, 44 * K - 1, 44 * K - 1], fill=RED)
    t = t.rotate(rot, expand=True, resample=Image.BICUBIC)
    img.alpha_composite(t, (sx * K, sy * K))
d = ImageDraw.Draw(img)

d.text((60 * K, 40 * K), "8 GB", font=lora(190), fill=WHITE)
d.text((60 * K, 275 * K), "ENOUGH?", font=lora(112), fill=RED)
d.rounded_rectangle(S(60, 520, 600, 600), radius=40 * K, fill=WHITE)
d.text((330 * K, 560 * K), "Why VRAM matters now", font=ImageFont.truetype(FD + "Inter-Bold.otf", 38 * K), fill=BG, anchor="mm")
logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (1170 * K, 620 * K))
img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
