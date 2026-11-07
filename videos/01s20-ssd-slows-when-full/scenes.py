"""Short 01s20: why an SSD slows down when it's nearly full (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def gauge(x, cx, cy, r, frac, a, c):
    """Half-circle speedometer with a needle at frac (0..1)."""
    pts = [(cx + r * math.cos(math.pi + math.pi * k / 40), cy + r * math.sin(math.pi + math.pi * k / 40)) for k in range(41)]
    x.line(pts, MUTED, a, 18, glow=False)
    n = max(2, int(41 * clamp(frac)))
    x.line(pts[:n], c, a, 18)
    ang = math.pi + math.pi * clamp(frac)
    x.line([(cx, cy), (cx + (r - 40) * math.cos(ang), cy + (r - 40) * math.sin(ang))], WHITE, a, 10, glow=False)
    x.circle(cx, cy, 20, WHITE, a, 0, fill=WHITE)


def s_hook(x):
    a = x.b(0)
    p = ease(x.since(0) / 3.5)
    fill = 0.15 + 0.8 * p
    # the drive as a long capacity bar
    x.text((CX, 450), "drive space used", "semi", 40, MUTED, a, anchor="mm")
    x.rect([120, 500, 960, 610], WHITE, a, 5, r=20, glow=False)
    c = AMBER if fill < 0.75 else RED
    x.d.rounded_rectangle([132, 512, 132 + 816 * fill, 598], radius=14, fill=col(c, a))
    x.text((CX, 555), f"{int(fill * 100)}%", "title", 60, NAVY if fill > 0.3 else WHITE, a, anchor="mm")
    # write speed gauge falls as space runs out
    spd = 1 - max(0.0, (fill - 0.55) / 0.4) * 0.85
    gauge(x, CX, 1050, 300, spd, a, AMBER if spd > 0.5 else RED)
    x.text((CX, 1150), "write speed", "semi", 42, WHITE, a, anchor="mm")
    label_box(x, CX, 1230, "it's real", CYAN, x.b(1), 44)


def cell(x, cx, cy, s, bits, c, a, lit=1.0):
    x.rect([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], c, a, 4, r=12, fill=PANEL + (255,), glow=False)
    for k in range(bits):
        oy = (k - (bits - 1) / 2) * s * 0.26
        x.circle(cx, cy + oy, s * 0.09, c, a * lit, 0, fill=c)


def s_cache(x):
    a = x.b(0)
    a1 = x.b(1)
    a2 = x.b(2)
    # flash cells: left two columns switch to 1-bit (SLC) mode
    s, gap = 120, 30
    cols, rows = 6, 3
    x0 = CX - (cols * s + (cols - 1) * gap) / 2 + s / 2
    y0 = 720
    for i in range(cols):
        for j in range(rows):
            cx, cy = x0 + i * (s + gap), y0 + j * (s + gap)
            slc = i < 2 and a1 > 0
            cell(x, cx, cy, s, 1 if slc else 3, CYAN if slc else MUTED, a)
    if a1 > 0:
        x.rect([x0 - s / 2 - 16, y0 - s / 2 - 16, x0 + s + gap + s / 2 + 16, y0 + 2 * (s + gap) + s / 2 + 16],
               CYAN, a1, 5, r=20)
        x.text((x0 + (s + gap) / 2, 1135), "1 bit / cell", "title", 40, CYAN, a1, anchor="mm")
        x.text((x0 + 3.5 * (s + gap), 1135), "3 bits / cell", "semi", 36, MUTED, a1, anchor="mm")
    if a2 > 0:
        label_box(x, x0 + (s + gap) / 2, 1215, "SLC cache", CYAN, a2, 44)
        # incoming write packets drop into the cache
        for k in range(3):
            u = (x.since(2) * 0.8 + k / 3) % 1
            px = x0 + (s + gap) / 2 + (k - 1) * 60
            py = 430 + 190 * u
            x.d.rounded_rectangle([px - 24, py - 24, px + 24, py + 24], radius=8, fill=col(AMBER, a2 * (1 - u * 0.6)))
        x.text((x0 + 3.5 * (s + gap), 520), "new writes", "semi", 36, AMBER, a2, anchor="mm")


def s_shrink(x):
    a = x.b(0)
    # strip of blocks: data (muted) eats the free space; cache (cyan) is what free space is left
    n = 10
    s = 78
    x0 = CX - (n * s + (n - 1) * 8) / 2
    fillp = ease(x.since(1) / 1.6) if x.b(1) > 0 else 0.0
    used = int(3 + 5 * fillp + 0.5)
    for i in range(n):
        bx = x0 + i * (s + 8)
        c = MUTED if i < used else CYAN
        x.d.rounded_rectangle([bx, 460, bx + s, 560], radius=10, fill=col(c, a))
    x.text((x0, 610), "your files", "semi", 34, MUTED, a, anchor="lm")
    x.text((x0 + n * (s + 8) - 8, 610), "cache", "semi", 34, CYAN, a, anchor="rm")
    # speed over a big copy: plateau then cliff
    a2 = x.b(2)
    gx, gy, gw, gh = 140, 720, 800, 400
    x.line([(gx, gy), (gx, gy + gh), (gx + gw, gy + gh)], WHITE, a2, 4, glow=False)
    x.text((gx + 10, gy - 20), "speed", "semi", 32, MUTED, a2, anchor="ls")
    x.text((gx + gw, gy + gh + 40), "GB copied", "semi", 32, MUTED, a2, anchor="rm")
    p = ease(x.since(2) / 2.5)

    def curve(edge, c, w):
        pts = []
        for k in range(61):
            u = k / 60
            yv = gy + 40 if u < edge else gy + gh - 90
            pts.append((gx + gw * u, yv))
            if abs(u - edge) < 1 / 120:
                pts.append((gx + gw * u, gy + gh - 90))
        m = max(2, int(len(pts) * p))
        x.line(pts[:m], c, a2, w)
    curve(0.62, MUTED, 4)
    curve(0.2, RED, 9)
    x.text((gx + gw * 0.62 + 12, gy + 70), "empty drive", "semi", 30, MUTED, a2 * p, anchor="lm")
    label_box(x, CX, gy + gh + 105, "nearly full: native speed", RED, a2 * ease(x.since(2) / 0.6 - 3), 34)


def s_tidy(x):
    a = x.b(0)
    # two blocks: a messy one with stale pages, and an empty one the controller copies good pages into
    def block(bx, by, pages, aa, title):
        x.rect([bx, by, bx + 340, by + 340], WHITE, aa, 4, r=16, fill=PANEL + (255,), glow=False)
        x.text((bx + 170, by - 34), title, "semi", 34, MUTED, aa, anchor="mm")
        for k, kind in enumerate(pages):
            px, py = bx + 30 + (k % 3) * 100, by + 30 + (k // 3) * 100
            if kind == "ok":
                x.d.rounded_rectangle([px, py, px + 80, py + 80], radius=10, fill=col(AMBER, aa))
            elif kind == "old":
                x.d.rounded_rectangle([px, py, px + 80, py + 80], radius=10, outline=col(RED, aa), width=4)
                x.line([(px + 18, py + 18), (px + 62, py + 62)], RED, aa, 5, glow=False)
                x.line([(px + 62, py + 18), (px + 18, py + 62)], RED, aa, 5, glow=False)
    p = ease(x.since(0) / 3.0 - 0.4)
    cleared = p >= 1
    messy = ["ok", "old", "old", "old", "ok", "old", "ok", "old", "old"]
    a1 = x.b(1)
    if a1 > 0:
        p, cleared = 0.0, False
    left = ["empty"] * 9 if cleared else [("empty" if (m == "ok" and p > 0.5) else m) for m in messy]
    block(90, 500, left, a, "full drive" if a1 > 0 else ("erased" if cleared else "old block"))
    right = (["ok"] * 3 + ["empty"] * 6) if p > 0.5 else ["empty"] * 9
    block(650, 500, right, a, "free block")
    if 0 < p < 1:
        x.line([(450, 670), (630, 670)], CYAN, a, 8)
        x.d.polygon([(640, 670), (610, 650), (610, 690)], fill=col(CYAN, a))
    # full drive: no free block, the writes queue up
    if a1 > 0:
        x.rect([650, 500, 990, 840], RED, a1, 8, r=16, fill=PANEL + (255,), glow=False)
        x.text((820, 670), "no room", "title", 50, RED, a1, anchor="mm")
        for k in range(5):
            qx = 160 + k * 160 + 20 * math.sin(x.t * 3 + k)
            x.d.rounded_rectangle([qx, 990, qx + 110, 1080], radius=12, fill=col(MUTED, a1))
        label_box(x, CX, 1180, "writes wait", RED, a1, 42)
    else:
        label_box(x, CX, 1060, "wear leveling + garbage collection", CYAN, a, 34)


def s_room(x):
    a = x.b(0)
    cx, cy, r = CX, 820, 300
    used = 0.85
    x.circle(cx, cy, r, MUTED, a, 0, fill=GRID)
    p = ease(x.since(0) / 1.4)
    # pie: used (muted) + free slice (green) pulsing
    x.d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * used * p, fill=col(MUTED, a))
    pulse = 0.75 + 0.25 * math.sin(x.t * 4)
    x.d.pieslice([cx - r - 10, cy - r - 10, cx + r + 10, cy + r + 10], -90 + 360 * used, 270,
                 fill=col(AMBER, a * p * pulse))
    x.circle(cx, cy, r * 0.64, NAVY, a, 0, fill=NAVY)
    a1 = x.b(1)
    x.text((cx, cy - 30), "keep free", "semi", 44, WHITE, a1, anchor="mm")
    x.text((cx, cy + 50), "10-20%", "title", 76, AMBER, a1, anchor="mm")
    label_box(x, CX, 1210, "common rule of thumb", CYAN, a1, 40)


def s_end(x):
    a = x.b(0)
    # an M.2 SSD stick
    x0, y0, w, h = 160, 600, 760, 200
    x.rect([x0, y0, x0 + w, y0 + h], WHITE, a, 5, r=14, fill=PANEL + (255,), glow=False)
    x.d.rectangle([x0 + 60, y0 + 40, x0 + 220, y0 + 160], fill=col(CYAN, a))
    for k in range(3):
        bx = x0 + 270 + k * 150
        x.d.rectangle([bx, y0 + 40, bx + 120, y0 + 160], fill=col(MUTED, a))
    for k in range(0, 50, 9):
        x.d.rectangle([x0 + w - 6 + 0 * k, y0 + 20 + k * 3, x0 + w + 20, y0 + 30 + k * 3], fill=col(AMBER, a))
    x.text((CX, 900), "space = speed", "title", 70, AMBER, a, anchor="mm")
    label_box(x, CX, 1100, "More PC hardware on the channel", CYAN, a, 38)


SCENES = [("Full SSD, slow SSD?", s_hook), ("The fast lane", s_cache), ("The cache shrinks", s_shrink),
          ("No room to tidy", s_tidy), ("Leave some space", s_room), ("Plainly Silicon", s_end)]
