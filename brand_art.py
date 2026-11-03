"""Plainly Silicon brand kit: logo (800x800) and banner (2560x1440)."""
import math, random
from PIL import Image, ImageDraw, ImageFilter, ImageFont

NAVY = (11, 18, 32)
NAVY2 = (17, 27, 46)
CYAN = (34, 211, 238)
AMBER = (245, 158, 11)
WHITE = (229, 231, 235)
MUTED = (120, 135, 160)
FD = "/usr/share/fonts/opentype/inter/"
TITLE = FD + "InterDisplay-Bold.otf"
SEMI = FD + "Inter-SemiBold.otf"
REG = FD + "Inter-Regular.otf"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"


def glow(base, layer, radius, strength=1.0):
    """Composite a blurred copy of layer under the sharp layer."""
    g = layer.filter(ImageFilter.GaussianBlur(radius))
    if strength != 1.0:
        a = g.getchannel("A").point(lambda v: min(255, int(v * strength)))
        g.putalpha(a)
    base.alpha_composite(g)
    base.alpha_composite(layer)


def chip(d, cx, cy, size, w, color, pins=6, pin_len=None):
    """Square chip outline with pins on all four sides."""
    h = size / 2
    pin_len = pin_len or size * 0.16
    r = size * 0.08
    d.rounded_rectangle([cx - h, cy - h, cx + h, cy + h], radius=r, outline=color, width=w)
    gap = size / (pins + 1)
    for i in range(1, pins + 1):
        o = -h + gap * i
        for (x0, y0, x1, y1) in [
            (cx + o, cy - h, cx + o, cy - h - pin_len),
            (cx + o, cy + h, cx + o, cy + h + pin_len),
            (cx - h, cy + o, cx - h - pin_len, cy + o),
            (cx + h, cy + o, cx + h + pin_len, cy + o),
        ]:
            d.line([x0, y0, x1, y1], fill=color, width=w)


def trace_p(d, cx, cy, size, w, color, node_r):
    """A 'P' drawn as circuit traces with round solder nodes at the ends."""
    s = size
    x0 = cx - s * 0.22        # stem x
    top = cy - s * 0.30
    bot = cy + s * 0.32
    mid = cy + s * 0.02
    bx = cx + s * 0.12        # where the bowl curve starts
    rad = (mid - top) / 2
    # stem
    d.line([x0, bot, x0, top], fill=color, width=w)
    # top bar, bowl, middle bar
    d.line([x0, top, bx, top], fill=color, width=w)
    d.arc([bx - rad, top, bx + rad, mid], start=-90, end=90, fill=color, width=w)
    d.line([bx, mid, x0, mid], fill=color, width=w)
    for (nx, ny) in [(x0, bot)]:
        d.ellipse([nx - node_r, ny - node_r, nx + node_r, ny + node_r], fill=color)
    # small inner node on the middle bar (circuit feel)
    nr = node_r * 0.7
    d.ellipse([x0 - nr, mid - nr, x0 + nr, mid + nr], fill=NAVY, outline=color, width=max(2, w // 2))


def make_logo(path, S=800):
    K = 3  # supersample
    W = S * K
    img = Image.new("RGBA", (W, W), NAVY + (255,))
    # subtle radial lift in the center
    bg = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    bd = ImageDraw.Draw(bg)
    bd.ellipse([W * 0.15, W * 0.15, W * 0.85, W * 0.85], fill=NAVY2 + (255,))
    img.alpha_composite(bg.filter(ImageFilter.GaussianBlur(W * 0.12)))

    layer = Image.new("RGBA", (W, W), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cs = W * 0.46
    chip(d, W / 2, W / 2, cs, int(W * 0.018), CYAN + (255,), pins=5, pin_len=cs * 0.15)
    trace_p(d, W / 2, W / 2, cs, int(W * 0.026), CYAN + (255,), node_r=W * 0.026)
    glow(img, layer, W * 0.02, 1.4)
    img = img.convert("RGB").resize((S, S), Image.LANCZOS)
    img.save(path)


def iso(x, y, z, ox, oy, s):
    """Isometric projection."""
    return (ox + (x - y) * s * 0.866, oy + (x + y) * s * 0.5 - z * s)


def iso_box(d, ox, oy, s, x, y, z, w, l, h, color, width):
    P = lambda a, b, c: iso(a, b, c, ox, oy, s)
    top = [P(x, y, z + h), P(x + w, y, z + h), P(x + w, y + l, z + h), P(x, y + l, z + h)]
    d.line(top + [top[0]], fill=color, width=width)
    for (a, b) in [(x + w, y), (x + w, y + l), (x, y + l)]:
        d.line([P(a, b, z), P(a, b, z + h)], fill=color, width=width)
    d.line([P(x + w, y, z), P(x + w, y + l, z), P(x, y + l, z)], fill=color, width=width)


def make_banner(path, W=2560, H=1440):
    K = 2
    w, h = W * K, H * K
    img = Image.new("RGBA", (w, h), NAVY + (255,))
    d = ImageDraw.Draw(img)

    # faint circuit traces across the full canvas (only seen on TV)
    rnd = random.Random(7)
    faint = (30, 48, 74, 255)
    for _ in range(70):
        x, y = rnd.randrange(0, w), rnd.randrange(0, h)
        pts = [(x, y)]
        for _ in range(rnd.randint(2, 4)):
            if rnd.random() < 0.5:
                x += rnd.choice([-1, 1]) * rnd.randint(80, 400) * K
            else:
                y += rnd.choice([-1, 1]) * rnd.randint(60, 300) * K
            pts.append((x, y))
        d.line(pts, fill=faint, width=3 * K)
        ex, ey = pts[-1]
        d.ellipse([ex - 8 * K, ey - 8 * K, ex + 8 * K, ey + 8 * K], outline=faint, width=3 * K)

    # darken behind the safe area so text stays crisp on every device
    veil = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    vd = ImageDraw.Draw(veil)
    vd.rounded_rectangle([420 * K, 470 * K, 2140 * K, 970 * K], radius=60 * K, fill=NAVY + (235,))
    img.alpha_composite(veil.filter(ImageFilter.GaussianBlur(50 * K)))

    # safe area: x 507-2053, y 508-931
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)

    # left: logo mark
    cx, cy, cs = 640 * K, 720 * K, 170 * K
    chip(ld, cx, cy, cs, int(6 * K), CYAN + (255,), pins=4, pin_len=cs * 0.15)
    trace_p(ld, cx, cy, cs, int(9 * K), CYAN + (255,), node_r=9 * K)

    # right: exploded isometric board with chip, RAM, GPU
    ox, oy, s = 1790 * K, 600 * K, 24 * K
    lw = int(3 * K)
    iso_box(ld, ox, oy, s, -5, -5, 0, 10, 10, 0.4, CYAN + (255,), lw)           # board
    iso_box(ld, ox, oy, s, -1.5, -1.5, 1.6, 3, 3, 0.6, CYAN + (255,), lw)       # CPU (floating)
    for i in range(2):
        iso_box(ld, ox, oy, s, 2.3 + i * 0.9, -3.5, 2.4, 0.35, 4, 1.4, AMBER + (255,), lw)  # RAM sticks
    # guide lines showing the "exploded" offsets
    dash = (34, 211, 238, 110)
    for (a, b, z0, z1) in [(0, 0, 0.4, 1.6), (2.7, -1.5, 0.4, 2.4), (3.6, -1.5, 0.4, 2.4)]:
        p0, p1 = iso(a, b, z0, ox, oy, s), iso(a, b, z1, ox, oy, s)
        n = 8
        for i in range(n):
            if i % 2 == 0:
                t0, t1 = i / n, (i + 1) / n
                ld.line([(p0[0] + (p1[0] - p0[0]) * t0, p0[1] + (p1[1] - p0[1]) * t0),
                         (p0[0] + (p1[0] - p0[0]) * t1, p0[1] + (p1[1] - p0[1]) * t1)],
                        fill=dash, width=lw)
    glow(img, layer, 10 * K, 1.3)

    # text
    td = ImageDraw.Draw(img)
    f_title = ImageFont.truetype(TITLE, 112 * K)
    f_tag = ImageFont.truetype(REG, 42 * K)
    f_sched = ImageFont.truetype(MONO, 30 * K)
    tx = 790 * K
    td.text((tx, 610 * K), "Plainly Silicon", font=f_title, fill=WHITE)
    td.text((tx, 752 * K), "How your PC actually works — animated", font=f_tag, fill=(170, 185, 205))
    td.text((tx, 830 * K), "NEW VIDEOS  MON · WED · FRI", font=f_sched, fill=CYAN)

    img = img.convert("RGB").resize((W, H), Image.LANCZOS)
    img.save(path)


if __name__ == "__main__":
    make_logo(os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand/plainly-silicon-logo.png"))
    make_banner(os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand/plainly-silicon-banner.png"))
    print("ok")
