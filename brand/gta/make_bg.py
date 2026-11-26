"""Vice City-style sunset backgrounds (no text, no logos) for GTA 6 thumbnails, drawn in code."""
import math, os, sys
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
def palm(d, x, base, h, s, col):
    pts = [(x + math.sin(t / 10) * 18 * s + t * 0.9 * s, base - t * h / 60) for t in range(61)]
    for i in range(60):
        d.line([pts[i], pts[i + 1]], fill=col, width=int((22 - i * 0.22) * s))
    tx, ty = pts[-1]
    for ang in (-170, -140, -110, -70, -40, -10, 20):
        a = math.radians(ang)
        L = 230 * s
        segs = [(tx + math.cos(a) * L * k / 10, ty + math.sin(a) * L * k / 10 + (k / 10) ** 2 * 120 * s) for k in range(11)]
        for i in range(10):
            d.line([segs[i], segs[i + 1]], fill=col, width=int((26 - i * 2.2) * s))
def bg(W, H, out, sun_y, horizon):
    img = Image.new("RGB", (W, H)); d = ImageDraw.Draw(img)
    stops = [(0, (24, 6, 48)), (0.45, (120, 20, 110)), (0.75, (255, 70, 140)), (1, (255, 150, 70))]
    for y in range(horizon):
        f = y / horizon
        for i in range(len(stops) - 1):
            if stops[i][0] <= f <= stops[i + 1][0]:
                g = (f - stops[i][0]) / (stops[i + 1][0] - stops[i][0]); c0, c1 = stops[i][1], stops[i + 1][1]
                d.line([(0, y), (W, y)], fill=tuple(int(c0[k] + (c1[k] - c0[k]) * g) for k in range(3)))
    R = min(W, H) * 0.32
    sun = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sun)
    for y in range(int(sun_y - R), int(sun_y + R)):
        f = (y - (sun_y - R)) / (2 * R)
        dx = math.sqrt(max(0, R * R - (y - sun_y) ** 2))
        cut = y > sun_y and int((y - sun_y) / (R / 7)) % 2 == 1
        if not cut:
            sd.line([(W / 2 - dx, y), (W / 2 + dx, y)], fill=(255, int(220 - 120 * f), int(90 - 40 * f), 255))
    glow = sun.filter(ImageFilter.GaussianBlur(40))
    img.paste(glow, (0, 0), glow); img.paste(sun, (0, 0), sun)
    d = ImageDraw.Draw(img)
    # skyline
    import random; random.seed(6)
    x = 0
    while x < W:
        w = random.randint(int(W * 0.03), int(W * 0.07)); h = random.randint(int(H * 0.04), int(H * 0.16))
        d.rectangle([x, horizon - h, x + w, horizon], fill=(40, 10, 60)); x += w + random.randint(0, 8)
    # sea
    for y in range(horizon, H):
        f = (y - horizon) / (H - horizon)
        d.line([(0, y), (W, y)], fill=(int(30 + 20 * (1 - f)), int(10 + 30 * f), int(70 + 40 * f)))
    for k in range(18):
        yy = horizon + (k + 1) ** 1.6 * (H - horizon) / 110
        if yy < H:
            d.line([(W / 2 - R * (1 - k / 22), yy), (W / 2 + R * (1 - k / 22), yy)], fill=(255, 120, 140), width=max(2, int(k / 3)))
    s = min(W, H) / 720
    palm(d, W * 0.02, H + 10, H * 0.85, s * 1.1, (18, 4, 30))
    palm(d, W * 0.88, H + 10, H * 0.7, -s * 0.9 if False else s * 0.9, (18, 4, 30))
    img.save(os.path.join(HERE, out), quality=93)
bg(1280, 720, "gta_bg_16x9.jpg", 330, 470)
bg(1080, 1920, "gta_bg_9x16.jpg", 1050, 1300)
print("ok")
