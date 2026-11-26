"""Original PS5 vs PC face-off art for the GTA 6 thumbnails: split background (PlayStation blue vs
Vice City pink/orange), neon line-art PS5 and gaming PC, VS badge, and a GTA-VI-style "60?".
Text and the GTA VI logo are added in Canva."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../.."))
sys.path.insert(0, ROOT); sys.path.insert(0, HERE)
from render import BRAND_TITLE_FONT
import make_art

def glow_layer(size, draw_fn, color, width, blur):
    L = Image.new("RGBA", size, (0, 0, 0, 0)); d = ImageDraw.Draw(L); draw_fn(d, color + (255,), width)
    G = L.filter(ImageFilter.GaussianBlur(blur))
    out = Image.new("RGBA", size, (0, 0, 0, 0)); out = Image.alpha_composite(out, G); out = Image.alpha_composite(out, G)
    core = Image.new("RGBA", size, (0, 0, 0, 0)); cd = ImageDraw.Draw(core); draw_fn(cd, (255, 255, 255, 255), max(2, width // 3))
    return Image.alpha_composite(Image.alpha_composite(out, L), core)

def ps5(d, c, w, x, y, h):
    s = h / 470
    # left and right curved white plates with the black core between
    for side in (-1, 1):
        pts = []
        for k in range(41):
            t = k / 40
            yy = y + t * h
            bulge = math.sin(t * math.pi) * 30 * s
            pts.append((x + side * (60 * s + bulge + 20 * s * (1 - t)), yy))
        pts += [(x + side * 24 * s, y + h - 10 * s), (x + side * 24 * s, y + 20 * s)]
        d.line(pts + [pts[0]], fill=c, width=w, joint="curve")
    d.rounded_rectangle([x - 22 * s, y + 30 * s, x + 22 * s, y + h - 20 * s], radius=10 * s, outline=c, width=w)
    d.line([(x - 24 * s, y + 40 * s), (x - 24 * s, y + 160 * s)], fill=(120, 200, 255, 255), width=w + 2)  # light bar
    d.rounded_rectangle([x - 110 * s, y + h + 6 * s, x + 110 * s, y + h + 26 * s], radius=10 * s, outline=c, width=w)  # stand

def pc(d, c, w, x, y, h):
    s = h / 460; W = 300 * s
    d.rounded_rectangle([x - W / 2, y, x + W / 2, y + h], radius=18 * s, outline=c, width=w)
    d.line([(x - W / 2 + 20 * s, y + 20 * s), (x - W / 2 + 20 * s, y + h - 20 * s)], fill=c, width=max(2, w // 2))
    for k in range(3):
        cy = y + 85 * s + k * 120 * s
        d.ellipse([x + 10 * s - 48 * s, cy - 48 * s, x + 10 * s + 48 * s, cy + 48 * s], outline=c, width=w)
        for a in range(6):
            ang = a * math.pi / 3
            d.line([(x + 10 * s, cy), (x + 10 * s + 40 * s * math.cos(ang), cy + 40 * s * math.sin(ang))], fill=c, width=max(2, w // 2))
    d.rounded_rectangle([x - W / 2 + 40 * s, y + h - 70 * s, x + W / 2 - 30 * s, y + h - 40 * s], radius=8 * s, outline=c, width=w)  # GPU
    for fx in (-W / 2 + 30 * s, W / 2 - 30 * s):
        d.line([(x + fx, y + h), (x + fx, y + h + 18 * s)], fill=c, width=w)

def split_bg(W, H, horizontal):
    img = Image.new("RGB", (W, H)); px = img.load()
    for yy in range(H):
        for xx in range(0, W, 2):
            if horizontal:
                left = yy < H * 0.5 + (xx - W / 2) * 0.12
                f = yy / H
            else:
                left = xx < W * 0.5 + (H / 2 - yy) * 0.17
                f = xx / W
            if left:
                col = (int(6 + 20 * f), int(16 + 30 * f), int(60 + 70 * f))
            else:
                col = (int(70 + 60 * f), int(10 + 20 * f), int(60 + 10 * f))
            px[xx, yy] = col
            if xx + 1 < W: px[xx + 1, yy] = col
    return img.convert("RGBA")

def vs_badge(img, cx, cy, r):
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.ellipse([cx - r * 1.3, cy - r * 1.3, cx + r * 1.3, cy + r * 1.3], fill=(255, 255, 255, 120))
    L = L.filter(ImageFilter.GaussianBlur(r * 0.4)); img.alpha_composite(L)
    d = ImageDraw.Draw(img)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(20, 6, 34), outline=(255, 255, 255), width=int(r * 0.12))
    f = ImageFont.truetype(BRAND_TITLE_FONT, int(r * 0.95))
    d.text((cx, cy + r * 0.04), "VS", font=f, fill=(255, 210, 63), anchor="mm")

def divider(img, p0, p1, w):
    L = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.line([p0, p1], fill=(255, 255, 255, 255), width=w)
    G = L.filter(ImageFilter.GaussianBlur(w * 2)); img.alpha_composite(G); img.alpha_composite(G); img.alpha_composite(L)

def long():
    W, H = 1280, 720
    img = split_bg(W, H, False)
    img.alpha_composite(glow_layer(img.size, lambda d, c, w: ps5(d, c, w, 190, 170, 430), (60, 160, 255), 7, 10))
    img.alpha_composite(glow_layer(img.size, lambda d, c, w: pc(d, c, w, 1070, 170, 430), (255, 70, 170), 7, 10))
    divider(img, (W * 0.5 + H * 0.5 * 0.17, 0), (W * 0.5 - H * 0.5 * 0.17, H), 6)
    vs_badge(img, W // 2, 470, 70)
    img.convert("RGB").save(os.path.join(HERE, "gta_vs_16x9.jpg"), quality=93)

def short():
    W, H = 1080, 1920
    img = split_bg(W, H, True)
    img.alpha_composite(glow_layer(img.size, lambda d, c, w: ps5(d, c, w, 250, 360, 540), (60, 160, 255), 8, 12))
    img.alpha_composite(glow_layer(img.size, lambda d, c, w: pc(d, c, w, 800, 1090, 560), (255, 70, 170), 8, 12))
    divider(img, (0, H * 0.5 - W * 0.5 * 0.12), (W, H * 0.5 + W * 0.5 * 0.12), 7)
    vs_badge(img, W // 2, H // 2, 95)
    img.convert("RGB").save(os.path.join(HERE, "gta_vs_9x16.jpg"), quality=93)

long(); short()
print(make_art.number("60?", 900, "gta_60.png"))
