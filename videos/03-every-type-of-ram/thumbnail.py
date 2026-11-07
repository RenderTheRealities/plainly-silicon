"""Thumbnail for video 3: three RAM generations fanned out, notches glowing, big two-line text (mint theme)."""
import os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "../.."))
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H, K = 1280, 720, 2
# mint theme colors (THEMES["mint"] in render.py)
NAVY = (5, 38, 35); PANEL = (10, 56, 51); GRID = (14, 66, 60); CYAN = (45, 212, 191)
AMBER = (253, 230, 138); WHITE = (236, 253, 245); MUTED = (130, 180, 170); GREEN = (190, 242, 100)
GF = "/usr/share/fonts/truetype/google-fonts/"
w, h = W * K, H * K
img = Image.new("RGBA", (w, h), NAVY + (255,))
d0 = ImageDraw.Draw(img)
for k in range(-h, w, 48 * K):
    d0.line([(k, 0), (k + h, h)], fill=GRID + (255,), width=2 * K)
bg = Image.new("RGBA", (w, h), (0, 0, 0, 0))
ImageDraw.Draw(bg).ellipse([w * 0.40, -h * 0.25, w * 1.25, h * 1.15], fill=(16, 90, 80, 200))
img.alpha_composite(bg.filter(ImageFilter.GaussianBlur(170)))


def stick(layer, x0, y0, L, Hh, notch, edge, label, angle):
    """Draw one module on its own layer, rotate, return it with its paste offset."""
    pad = 40 * K
    m = Image.new("RGBA", (int(L + 2 * pad), int(Hh + 2 * pad)), (0, 0, 0, 0))
    d = ImageDraw.Draw(m)
    bx0, by0 = pad, pad
    d.rounded_rectangle([bx0, by0, bx0 + L, by0 + Hh], radius=8 * K, fill=PANEL + (255,), outline=edge + (255,), width=6 * K)
    cw = (L - 60 * K) / 8
    for i in range(8):
        cx = bx0 + 30 * K + i * cw
        d.rectangle([cx + cw * 0.12, by0 + Hh * 0.15, cx + cw * 0.88, by0 + Hh * 0.56], fill=(14, 20, 20, 255))
    nx = bx0 + L * notch
    n = 46
    pitch = (L - 24 * K) / n
    for i in range(n):
        px = bx0 + 12 * K + i * pitch
        if abs(px + pitch / 2 - nx) < L * 0.022:
            continue
        d.rectangle([px + pitch * 0.18, by0 + Hh * 0.82, px + pitch * 0.82, by0 + Hh - 6 * K], fill=AMBER + (255,))
    d.rectangle([nx - L * 0.012, by0 + Hh * 0.80, nx + L * 0.012, by0 + Hh + 4], fill=(0, 0, 0, 0))
    # glowing ring on the notch
    d.ellipse([nx - 34 * K, by0 + Hh - 40 * K, nx + 34 * K, by0 + Hh + 28 * K], outline=GREEN + (255,), width=6 * K)
    f = ImageFont.truetype(GF + "Poppins-Bold.ttf", int(Hh * 0.2))
    tw = d.textlength(label, font=f)
    lx, ly = bx0 + L - 36 * K - tw, by0 + Hh * 0.58
    d.rectangle([lx - 12 * K, ly, lx + tw + 12 * K, ly + Hh * 0.22], fill=WHITE + (255,))
    d.text((lx, ly + Hh * 0.11), label, font=f, fill=NAVY + (255,), anchor="lm")
    m = m.rotate(angle, expand=True, resample=Image.BICUBIC)
    glow = m.filter(ImageFilter.GaussianBlur(16 * K))
    layer.alpha_composite(glow, (int(x0 - pad), int(y0 - pad)))
    layer.alpha_composite(m, (int(x0 - pad), int(y0 - pad)))


layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
L, Hh = 560 * K, 150 * K
stick(layer, 640 * K, 70 * K, L, Hh, 0.40, MUTED, "DDR3", 8)
stick(layer, 650 * K, 270 * K, L, Hh, 0.49, WHITE, "DDR4", 4)
stick(layer, 660 * K, 470 * K, L, Hh, 0.545, CYAN, "DDR5", 0)
img.alpha_composite(layer)

# text
t1 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 170 * K)
t2 = ImageFont.truetype(GF + "Poppins-Bold.ttf", 120 * K)
shadow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
sd = ImageDraw.Draw(shadow)
sd.text((54 * K, 90 * K), "EVERY", font=t2, fill=(0, 0, 0, 230))
sd.text((54 * K, 215 * K), "RAM", font=t1, fill=(0, 0, 0, 230))
sd.text((54 * K, 420 * K), "TYPE", font=t2, fill=(0, 0, 0, 230))
img.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(16 * K)))
dd = ImageDraw.Draw(img)
dd.text((50 * K, 84 * K), "EVERY", font=t2, fill=WHITE)
dd.text((50 * K, 208 * K), "RAM", font=t1, fill=AMBER)
dd.text((50 * K, 414 * K), "TYPE", font=t2, fill=WHITE)

logo = Image.open(os.path.join(ROOT, "brand/plainly-silicon-logo.png")).convert("RGBA").resize((80 * K, 80 * K))
img.alpha_composite(logo, (56 * K, 606 * K))

img.convert("RGB").resize((W, H), Image.LANCZOS).save(os.path.join(HERE, "thumbnail.jpg"), quality=92)
print("ok")
