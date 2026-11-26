"""Original GTA-6-style art for video 31 thumbnails: a giant "30" styled like the GTA VI logo
(sunset gradient fill with palm silhouettes, purple outer outline, white inner edge) on a transparent
background, plus a dark Vice City night background. Assembled in Canva."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT)
from render import BRAND_TITLE_FONT

def grad(w, h):
    stops = [(0, (64, 70, 230)), (0.35, (170, 70, 210)), (0.62, (255, 80, 150)), (1, (255, 190, 80))]
    g = Image.new("RGB", (w, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        f = y / h
        for i in range(3):
            if stops[i][0] <= f <= stops[i + 1][0]:
                t = (f - stops[i][0]) / (stops[i + 1][0] - stops[i][0]); a, b = stops[i][1], stops[i + 1][1]
                d.line([(0, y), (w, y)], fill=tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3)))
    return g

def palm(d, x, base, h, s, col, w=1.0):
    pts = [(x + math.sin(t / 10) * 18 * s + t * 0.9 * s, base - t * h / 60) for t in range(61)]
    for i in range(60):
        d.line([pts[i], pts[i + 1]], fill=col, width=max(1, int((22 - i * 0.22) * s * w)))
    tx, ty = pts[-1]
    for ang in (-170, -140, -110, -70, -40, -10, 20):
        a = math.radians(ang); L = 230 * s
        seg = [(tx + math.cos(a) * L * k / 10, ty + math.sin(a) * L * k / 10 + (k / 10) ** 2 * 120 * s) for k in range(11)]
        for i in range(10):
            d.line([seg[i], seg[i + 1]], fill=col, width=max(1, int((26 - i * 2.2) * s * w)))

def number(text, size, out):
    f = ImageFont.truetype(BRAND_TITLE_FONT, size)
    pad = int(size * 0.2)
    tmp = ImageDraw.Draw(Image.new("L", (1, 1)))
    l, t, r, b = tmp.textbbox((0, 0), text, font=f)
    W, H = r - l + 2 * pad, b - t + 2 * pad
    org = (pad - l, pad - t)
    def mask(stroke):
        m = Image.new("L", (W, H), 0)
        ImageDraw.Draw(m).text(org, text, font=f, fill=255, stroke_width=stroke, stroke_fill=255)
        return m
    outer, white, inner = mask(int(size * 0.075)), mask(int(size * 0.045)), mask(0)
    fill = grad(W, H).convert("RGBA")
    # faint palm leaves inside the fill, like the VI logo
    pl = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(pl)
    palm(pd, W * 0.08, H * 1.05, H * 0.9, size / 900, (255, 255, 255, 46), 1.4)
    palm(pd, W * 0.55, H * 1.1, H * 1.0, size / 800, (255, 255, 255, 40), 1.4)
    fill = Image.alpha_composite(fill, pl)
    out_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow = Image.new("RGBA", (W, H), (255, 70, 160, 0)); glow.putalpha(outer.filter(ImageFilter.GaussianBlur(size * 0.05)).point(lambda v: int(v * 0.8)))
    out_img = Image.alpha_composite(out_img, glow)
    purple = Image.new("RGBA", (W, H), (46, 8, 72, 255)); purple.putalpha(outer)
    out_img = Image.alpha_composite(out_img, purple)
    wht = Image.new("RGBA", (W, H), (255, 255, 255, 255)); wht.putalpha(white)
    out_img = Image.alpha_composite(out_img, wht)
    fill.putalpha(inner)
    out_img = Image.alpha_composite(out_img, fill)
    out_img.save(os.path.join(HERE, out))
    return out_img.size

def night(W, H, out, glow_y):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    for y in range(H):
        f = y / H
        d.line([(0, y), (W, y)], fill=(int(14 + 20 * f), int(4 + 6 * f), int(30 + 30 * f)))
    g = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    R = max(W, H) * 0.42
    gd.ellipse([W / 2 - R, glow_y - R * 0.7, W / 2 + R, glow_y + R * 0.7], fill=(255, 60, 140, 150))
    gd.ellipse([W / 2 - R * 0.55, glow_y - R * 0.3, W / 2 + R * 0.55, glow_y + R * 0.5], fill=(255, 150, 60, 140))
    g = g.filter(ImageFilter.GaussianBlur(R * 0.35))
    img.paste(g, (0, 0), g)
    p = Image.new("RGBA", (W, H), (0, 0, 0, 0)); pd = ImageDraw.Draw(p)
    s = min(W, H) / 720
    palm(pd, -W * 0.03, H + 20, H * 0.9, s * 1.25, (10, 2, 20, 255))
    palm(pd, W * 0.86, H + 20, H * 0.75, s * 1.0, (10, 2, 20, 255))
    img.paste(p, (0, 0), p)
    # subtle scanlines for a night-city screen feel
    d = ImageDraw.Draw(img, "RGBA")
    for y in range(0, H, 6):
        d.line([(0, y), (W, y)], fill=(0, 0, 0, 28))
    img.save(os.path.join(HERE, out), quality=93)

if __name__ == "__main__":
    print(number("30", 900, "gta_30.png"))
    night(1280, 720, "gta_night_16x9.jpg", 420)
    night(1080, 1920, "gta_night_9x16.jpg", 1000)
