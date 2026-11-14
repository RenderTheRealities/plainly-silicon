"""Scenes for video 07: 7 Black Friday PC Part Traps (and How to Spot a Real Deal).

Design language (retro theme): a shop-counter look. Items are hand-drawn price tags with a
string hole, a line-art shopping cart, a paper receipt that prints line by line, rubber
stamps, and a row of seven numbered trap tokens along the top that fill in as the cart
moves through the traps. Mechanism scenes use price-history charts, core grids, bus lanes,
an SSD write-speed trace, a laptop power dial and RAM channel lanes. Arrows are drawn as
shapes (Poppins has no arrow glyph).
"""
import math
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def tw(s, kind, size, x):
    return x.d.textlength(safe(s, kind), font=font(kind, size))


def arrow(x, p0, p1, c, a, w=5, head=20):
    if a <= 0:
        return
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    bx, by = p1[0] - head * math.cos(ang), p1[1] - head * math.sin(ang)
    x.line([p0, (bx, by)], c, a, w, glow=False)
    pts = [p1, (bx + head * 0.6 * math.sin(ang), by - head * 0.6 * math.cos(ang)),
           (bx - head * 0.6 * math.sin(ang), by + head * 0.6 * math.cos(ang))]
    x.d.polygon(pts, fill=col(c, a))


def tag(x, cx, cy, w, h, text, c, a, sub=None, size=40, fill=None):
    """Price tag: rectangle with a pointed left end and a string hole."""
    if a <= 0:
        return
    x0, x1, y0, y1 = cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2
    n = h * 0.45
    pts = [(x0 + n, y0), (x1, y0), (x1, y1), (x0 + n, y1), (x0, cy)]
    x.d.polygon(pts, fill=col(fill or PANEL, a), outline=col(c, a), width=4)
    x.circle(x0 + n * 0.75, cy, 9, c, a, 3, fill=NAVY)
    tx = cx + n * 0.35
    if sub:
        x.text((tx, cy - h * 0.16), text, "title", size, WHITE, a, anchor="mm")
        x.text((tx, cy + h * 0.26), sub, "semi", int(size * 0.55), c, a, anchor="mm")
    else:
        x.text((tx, cy), text, "title", size, WHITE, a, anchor="mm")


def strike(x, x0, y, x1, c, a, p=1.0, w=6):
    if a <= 0 or p <= 0:
        return
    x.line([(x0, y + 6), (x0 + (x1 - x0) * clamp(p), y - 6)], c, a, w, glow=False)


def check(x, cx, cy, s, c, a, w=7):
    if a <= 0:
        return
    x.line([(cx - s * 0.5, cy), (cx - s * 0.15, cy + s * 0.35), (cx + s * 0.55, cy - s * 0.45)], c, a, w, glow=False)


def cross(x, cx, cy, s, c, a, w=7):
    if a <= 0:
        return
    x.line([(cx - s / 2, cy - s / 2), (cx + s / 2, cy + s / 2)], c, a, w, glow=False)
    x.line([(cx - s / 2, cy + s / 2), (cx + s / 2, cy - s / 2)], c, a, w, glow=False)


def trap_row(x, cur, a, y=150):
    """Seven trap tokens across the top; tokens before `cur` are done, `cur` is lit."""
    if a <= 0:
        return
    for k in range(7):
        cx = 1290 + k * 78
        n = k + 1
        if n < cur:
            x.circle(cx, y, 26, MUTED, a, 3, fill=PANEL)
            x.text((cx, y), str(n), "semi", 26, MUTED, a, anchor="mm")
        elif n == cur:
            pulse = 1 + 0.08 * math.sin(x.t * 5)
            x.circle(cx, y, 30 * pulse, AMBER, a, 4, fill=AMBER)
            x.text((cx, y), str(n), "title", 28, NAVY, a, anchor="mm")
        else:
            x.circle(cx, y, 26, GRID, a, 3)
            x.text((cx, y), str(n), "semi", 26, GRID, a, anchor="mm")
    x.text((1250, y), "TRAP", "semi", 26, MUTED, a, anchor="rm")


def trap_title(x, n, name, a):
    x.text((150, 150), f"Trap {n}", "semi", 34, AMBER, a, anchor="lm")
    x.text((150, 215), name, "title", 62, WHITE, a, anchor="lm")


def cart(x, cx, cy, s, c, a, w=6):
    """Line-art shopping cart; basket top edge at cy - 0.55 s."""
    if a <= 0:
        return
    P = lambda u, v: (cx + u * s, cy + v * s)
    x.line([P(-1.35, -0.85), P(-1.05, -0.85), P(-0.8, 0.35), P(0.95, 0.35)], c, a, w)
    x.line([P(-0.97, -0.55), P(1.15, -0.55), P(0.95, 0.15), P(-0.84, 0.15)], c, a, w)
    for k in range(1, 5):
        u = -0.97 + k * 0.42
        x.line([P(u, -0.55), P(u - 0.04, 0.15)], c, a * 0.5, 3, glow=False)
    x.circle(*P(-0.6, 0.55), s * 0.11, c, a, w)
    x.circle(*P(0.75, 0.55), s * 0.11, c, a, w)


def chart(x, box, vals, c, a, prog=1.0, lo=None, hi=None, w=5):
    """Polyline over box from a list of values, drawn up to prog (0..1)."""
    if a <= 0:
        return []
    x0, y0, x1, y1 = box
    lo = min(vals) if lo is None else lo
    hi = max(vals) if hi is None else hi
    pts = [(x0 + (x1 - x0) * i / (len(vals) - 1), y1 - (y1 - y0) * (v - lo) / (hi - lo)) for i, v in enumerate(vals)]
    n = prog * (len(pts) - 1)
    k = int(n)
    shown = pts[:k + 1]
    if k < len(pts) - 1:
        f = n - k
        shown.append((pts[k][0] + (pts[k + 1][0] - pts[k][0]) * f, pts[k][1] + (pts[k + 1][1] - pts[k][1]) * f))
    if len(shown) > 1:
        x.line(shown, c, a, w)
    return pts


def gpu_card(x, box, c, a, name, mem):
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    x.rect(box, c, a, 4, r=14, fill=PANEL)
    for k in range(2):
        fx = x0 + (x1 - x0) * (0.3 + 0.4 * k)
        fy = (y0 + y1) / 2 + 20
        r = (y1 - y0) * 0.26
        x.circle(fx, fy, r, c, a * 0.8, 3)
        for j in range(5):
            ang = x.t * 3 + j * 2 * math.pi / 5
            x.line([(fx, fy), (fx + r * 0.85 * math.cos(ang), fy + r * 0.85 * math.sin(ang))], c, a * 0.6, 3, glow=False)
    x.text((x0 + 22, y0 + 34), name, "title", 34, WHITE, a, anchor="lm")
    x.text((x1 - 22, y0 + 34), mem, "title", 34, c, a, anchor="rm")
    # gold fingers
    for k in range(12):
        gx = x0 + 70 + k * 22
        x.d.rectangle([gx, y1, gx + 12, y1 + 16], fill=col(CYAN, a))


# ---------- scenes ----------
def s_hook(x):
    a0 = x.b(0)
    x.text((960, 150), "YOU SAVED $420", "title", 70, GREEN, a0 * (1 if x.since(0) < 4.5 else 0.35), anchor="mm")
    if a0 > 0 and x.since(0) > 2.0:
        q = ease((x.since(0) - 2.0) / 0.5)
        x.text((1290, 115), "?", "title", 90, AMBER, a0 * q, anchor="mm")
    a1 = x.b(1)
    for k in range(7):
        cx = 600 + k * 120
        p = ease((x.since(1) - k * 0.18) / 0.4) * a1
        x.circle(cx, 880, 34, AMBER, p, 4, fill=PANEL)
        x.text((cx, 880), str(k + 1), "title", 34, AMBER, p, anchor="mm")
    a3 = x.b(3)
    cart(x, 960, 560, 230, CYAN, max(x.b(1), a3))
    x.text((960, 345), "Jamie's cart", "semi", 34, MUTED, x.b(2), anchor="mm")
    items = [("GPU", 690, 400, 130), ("SSD", 840, 380, 130), ("PREBUILT", 1020, 395, 210), ("LAPTOP", 1230, 410, 180)]
    for k, (s, cx, ty, wd) in enumerate(items):
        t0 = x.since(3) - k * 0.55
        p = ease(t0 / 0.6) * a3
        if p <= 0:
            continue
        cy = ty - 200 * (1 - p) + 50
        tag(x, cx, cy, wd, 64, s, CYAN, p, size=26)
    a4 = x.b(4)
    if a4 > 0:
        x.rect([1450, 420, 1800, 640], AMBER, a4, 4, r=16, fill=PANEL)
        x.text((1625, 470), "Cart total", "semi", 30, MUTED, a4, anchor="mm")
        x.text((1625, 530), "$1,989", "title", 64, WHITE, a4, anchor="mm")
        x.d.rounded_rectangle([1475, 575, 1775, 620], radius=20, fill=col(GREEN, a4))
        x.text((1625, 598), "Saved $420!", "title", 28, NAVY, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.text((300, 520), "How much", "title", 50, WHITE, a5, anchor="mm")
        x.text((300, 585), "survives?", "title", 50, AMBER, a5, anchor="mm")


def s_was(x):
    trap_row(x, 1, x.b(0))
    trap_title(x, 1, 'The "was" price', x.b(0))
    a1 = x.b(1)
    tag(x, 420, 440, 420, 200, "", CYAN, a1)
    if a1 > 0:
        x.text((470, 395), "$399", "title", 56, MUTED, a1, anchor="mm")
        strike(x, 400, 395, 545, RED, a1, ease(x.since(1) / 0.8))
        x.text((470, 480), "$279", "title", 80, WHITE, a1, anchor="mm")
        x.text((470, 600), "the crossed-out number", "semi", 28, MUTED, a1, anchor="mm")
    # 12-month price history
    a2 = x.b(2)
    box = [820, 330, 1760, 640]
    if a2 > 0:
        x.line([(box[0], box[3]), (box[2], box[3])], MUTED, a2, 3, glow=False)
        x.line([(box[0], box[1]), (box[0], box[3])], MUTED, a2, 3, glow=False)
        for i, m in enumerate("JFMAMJJASOND"):
            x.text((box[0] + 30 + i * 78, box[3] + 30), m, "semi", 24, MUTED, a2, anchor="mm")
        vals = [289, 279, 285, 269, 279, 259, 275, 279, 265, 285, 279, 289]
        pts = chart(x, box, vals, CYAN, a2, ease(x.since(2) / 3.0), lo=240, hi=420)
        yl = box[3] - (box[3] - box[1]) * (399 - 240) / 180
        y2 = box[3] - (box[3] - box[1]) * (279 - 240) / 180
        for k in range(0, 940, 30):
            x.line([(box[0] + k, yl), (box[0] + k + 15, yl)], RED, a2 * 0.8, 3, glow=False)
            x.line([(box[0] + k, y2), (box[0] + k + 15, y2)], GREEN, a2 * 0.6, 2, glow=False)
        x.text((box[2], yl - 22), '"was" $399', "semi", 26, RED, a2, anchor="rm")
        x.text((box[2] + 10, y2), "$279", "semi", 24, GREEN, a2, anchor="lm")
        x.text((box[0] + 470, box[1] - 30), "Which: 175 products, 8 retailers, tracked a year", "semi", 26, MUTED, a2, anchor="mm")
        # dots at or below 279
        for i, v in enumerate(vals):
            if v <= 279 and ease(x.since(2) / 3.0) * 11 >= i:
                x.circle(*pts[i], 9, GREEN, a2, 3, fill=GREEN)
    a3, a4 = x.b(3), x.b(4)
    if a3 > 0:
        x.rect([160, 690, 700, 850], GREEN, a3, 4, r=18, fill=PANEL)
        x.text((300, 770), "83%", "title", 84, GREEN, a3, anchor="mm")
        x.text((560, 748), "same or cheaper", "semi", 26, WHITE, a3, anchor="mm")
        x.text((560, 793), "outside the sale", "semi", 26, WHITE, a3, anchor="mm")
    if a4 > 0:
        x.rect([740, 690, 1180, 850], AMBER, a4, 4, r=18, fill=PANEL)
        x.text((850, 770), "0", "title", 96, AMBER, a4, anchor="mm")
        x.text((1040, 748), "cheapest only", "semi", 26, WHITE, a4, anchor="mm")
        x.text((1040, 793), "on Black Friday", "semi", 26, WHITE, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.rect([1220, 690, 1760, 850], CYAN, a5, 4, r=18, fill=PANEL)
        x.text((1490, 725), "FTC pricing guide", "title", 30, CYAN, a5, anchor="mm")
        x.text((1490, 772), "former price = a real price,", "semi", 26, WHITE, a5, anchor="mm")
        x.text((1490, 812), "offered for a substantial time", "semi", 26, WHITE, a5, anchor="mm")
    a7 = x.b(6)
    if a7 > 0:
        # magnifier over the chart
        mx = 1100 + 260 * math.sin(x.since(6) * 1.2)
        x.circle(mx, 500, 80, WHITE, a7, 6)
        x.line([(mx + 57, 557), (mx + 120, 620)], WHITE, a7, 12, glow=False)
        x.text((mx, 500), "history", "semi", 26, WHITE, a7, anchor="mm")


def s_chip(x):
    trap_row(x, 2, x.b(0))
    trap_title(x, 2, "Same name, different chip", x.b(0))
    a1 = x.b(1)
    a2 = x.b(2)
    if a1 > 0:
        tag(x, 960, 340, 520, 100, "RTX 3050  $179", CYAN, a1 * (1 - a2), size=40)
    # two cards
    L, R = [180, 300, 860, 470], [1060, 300, 1740, 470]
    gpu_card(x, L, CYAN, a2, "RTX 3050", "8 GB")
    gpu_card(x, R, AMBER, a2, "RTX 3050", "6 GB")
    # cores grid (1 square = 64 cores): 40 vs 36
    a3, a4 = x.b(3), x.b(4)
    for side, (n, a, c, x0) in enumerate([(40, a3, CYAN, 180), (36, a4, AMBER, 1060)]):
        if a <= 0:
            continue
        for k in range(n):
            p = clamp((x.since(3 + side) - k * 0.03) / 0.2)
            gx, gy = x0 + (k % 20) * 34, 540 + (k // 20) * 34
            x.d.rectangle([gx, gy, gx + 26, gy + 26], fill=col(c, a * p))
        x.text((x0, 640), f"{2560 if side == 0 else 2304:,} CUDA cores", "semi", 30, WHITE, a, anchor="lm")
        # bus lanes: 128-bit = 16 lanes, 96-bit = 12 lanes
        lanes = 16 if side == 0 else 12
        for k in range(lanes):
            ly = 680 + k * 6
            x.line([(x0, ly), (x0 + 680, ly)], c, a * 0.5, 3, glow=False)
            px = x0 + ((x.t * 260 + k * 53) % 680)
            x.d.rectangle([px, ly - 2, px + 18, ly + 2], fill=col(WHITE, a))
        bw = 224 if side == 0 else 168
        x.text((x0, 795), f"{128 if side == 0 else 96}-bit bus, {bw} GB/s", "semi", 28, WHITE, a, anchor="lm")
        bar(x, x0, 850, 680, (130 if side == 0 else 70) / 140, c, a, h=24, value=f"{130 if side == 0 else 70} W power")
    a5 = x.b(5)
    if a5 > 0:
        x.text((960, 600), "=", "title", 70, MUTED, a5 * 0.6, anchor="mm")
    a6, a7 = x.b(6), x.b(7)
    if a6 > 0:
        # magnifier over the "6 GB" label
        x.circle(1640, 334, 70, WHITE, a6, 6)
        x.line([(1690, 384), (1745, 440)], WHITE, a6, 12, glow=False)
    if a7 > 0:
        x.text((1545, 262), "read the full model name", "title", 30, GREEN, a7, anchor="rm")


def s_swap(x):
    trap_row(x, 3, x.b(0))
    trap_title(x, 3, "The silent swap", x.b(0))
    a1 = x.b(1)
    # two identical M.2 sticks, labels the same
    for k, (y, lab, c) in enumerate([(330, "BEFORE", CYAN), (470, "AFTER", AMBER)]):
        a = a1 if k == 0 else x.b(2)
        if a <= 0:
            continue
        x.rect([150, y - 45, 900, y + 45], c, a, 4, r=10, fill=PANEL)
        x.d.ellipse([890, y - 12, 914, y + 12], fill=col(NAVY, a), outline=col(c, a), width=3)
        x.text((200, y), "P2", "title", 44, WHITE, a, anchor="lm")
        x.text((260, y), "same name, same number", "semi", 22, MUTED, a, anchor="lm") if k == 1 else None
        x.text((140, y), lab, "semi", 22, c, a, anchor="rm")
    # cell cutaway: TLC 3 bits vs QLC 4 bits
    a2 = x.b(2)
    for k, (bits, c, y, a) in enumerate([(3, CYAN, 330, a1), (4, AMBER, 470, a2)]):
        if a <= 0:
            continue
        for j in range(4):
            cx = 640 + j * 60
            on = j < bits
            x.rect([cx - 22, y - 30, cx + 22, y + 30], c if on else GRID, a, 3, r=6, fill=(c if on else PANEL))
            if on:
                x.text((cx, y), "1" if (j + k) % 2 else "0", "title", 26, NAVY, a, anchor="mm")
        x.text((640 + 4 * 60 - 10, y + 65), "TLC: 3 bits per cell" if k == 0 else "QLC: 4 bits per cell", "semi", 24, c, a, anchor="rm")
    # write-speed trace
    a3 = x.b(3)
    box = [1000, 300, 1760, 640]
    if a3 > 0:
        x.line([(box[0], box[3]), (box[2], box[3])], MUTED, a3, 3, glow=False)
        x.line([(box[0], box[1]), (box[0], box[3])], MUTED, a3, 3, glow=False)
        x.text((box[0], box[1] - 30), "write speed while copying a big file", "semi", 26, MUTED, a3, anchor="lm")
        p = ease(x.since(3) / 3.5)
        vals = [940] * 9 + [40] * 13
        chart(x, box, vals, AMBER, a3, p, lo=0, hi=1000)
        cx0 = box[0] + (box[2] - box[0]) * 8.5 / 21
        if p > 0.4:
            q = ease((p - 0.4) / 0.2)
            x.line([(cx0, box[1]), (cx0, box[3])], WHITE, a3 * q * 0.5, 2, glow=False)
            x.text((cx0 + 12, box[1] + 30), "fast cache full", "semi", 24, WHITE, a3 * q, anchor="lm")
            x.text((box[2], box[3] - 50), "about 40 MB/s", "title", 40, RED, a3 * q, anchor="rm")
            x.text((box[2], box[3] - 95), "USB 2 territory", "semi", 26, WHITE, a3 * q, anchor="rm")
    a4 = x.b(4)
    if a4 > 0:
        x.rect([150, 640, 900, 900], CYAN, a4, 4, r=16, fill=PANEL)
        x.text((525, 690), "launch-day review", "semi", 30, MUTED, a4, anchor="mm")
        for k in range(4):
            x.circle(360 + k * 70, 760, 22, CYAN, a4, 3, fill=CYAN)
        x.text((525, 840), "tested the BEFORE drive", "title", 34, WHITE, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.rect([1000, 700, 1760, 900], GREEN, a5, 4, r=16, fill=PANEL)
        x.text((1380, 760), "check recent reviews", "title", 36, GREEN, a5, anchor="mm")
        x.text((1380, 830), "old drive, sudden big discount = look closer", "semi", 26, WHITE, a5, anchor="mm")


def laptop(x, cx, cy, w, thick, c, a, sticker):
    if a <= 0:
        return
    h = w * 0.55
    x.rect([cx - w / 2, cy - h, cx + w / 2, cy], c, a, 5, r=10, fill=PANEL)
    x.rect([cx - w / 2 + 18, cy - h + 18, cx + w / 2 - 18, cy - 18], c, a * 0.4, 2, r=6, glow=False)
    x.d.polygon([(cx - w / 2 - 30, cy), (cx + w / 2 + 30, cy), (cx + w / 2 + 30, cy + thick),
                 (cx - w / 2 - 30, cy + thick)], fill=col(c, a))
    x.rect([cx + w / 2 - 170, cy - 80, cx + w / 2 - 30, cy - 34], AMBER, a, 3, r=8, fill=NAVY, glow=False)
    x.text((cx + w / 2 - 100, cy - 57), sticker, "title", 22, AMBER, a, anchor="mm")


def dial(x, cx, cy, r, frac, c, a, label):
    if a <= 0:
        return
    a0, a1 = math.pi * 0.85, math.pi * 2.15
    pts = [(cx + r * math.cos(a0 + (a1 - a0) * k / 40), cy + r * math.sin(a0 + (a1 - a0) * k / 40)) for k in range(41)]
    x.line(pts, GRID, a, 14, glow=False)
    n = int(40 * frac)
    if n > 0:
        x.line(pts[:n + 1], c, a, 14, glow=False)
    ang = a0 + (a1 - a0) * frac
    x.line([(cx, cy), (cx + (r - 30) * math.cos(ang), cy + (r - 30) * math.sin(ang))], WHITE, a, 6, glow=False)
    x.circle(cx, cy, 12, WHITE, a, 3, fill=WHITE)
    x.text((cx, cy + 70), label, "title", 40, c, a, anchor="mm")


def s_laptop(x):
    trap_row(x, 4, x.b(0))
    trap_title(x, 4, "Inside the laptop", x.b(0))
    a1 = x.b(1)
    laptop(x, 520, 560, 520, 18, CYAN, a1, "RTX 4060")
    a4 = x.b(4)
    laptop(x, 1400, 560, 520, 46, CYAN, a4, "RTX 4060")
    a2 = x.b(2)
    if a2 > 0:
        x.text((520, 650), "power set by the laptop maker", "semi", 28, MUTED, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        # range strip 35..115 W
        x0, x1, y = 300, 1620, 760
        x.line([(x0, y), (x1, y)], GRID, a3, 18, glow=False)
        p = ease(x.since(3) / 1.5)
        x.line([(x0, y), (x0 + (x1 - x0) * p, y)], AMBER, a3, 18, glow=False)
        x.text((x0, y + 45), "35 W", "title", 34, WHITE, a3, anchor="mm")
        x.text((x1, y + 45), "115 W", "title", 34, WHITE, a3, anchor="mm")
        x.text((960, y + 45), "+ a little Dynamic Boost from the CPU", "semi", 26, MUTED, a3, anchor="mm")
    if a4 > 0:
        q = ease(x.since(4) / 1.2)
        fl = 0.12 + 0.05 * math.sin(x.t * 3)
        fh = 0.12 + (0.88 + 0.04 * math.sin(x.t * 3.3)) * q
        x.line([(300, 700), (300 + 1320 * 0.0, 700)], WHITE, 0, 2)
        x.circle(300 + 1320 * fl, 760, 22, WHITE, a4, 4, fill=CYAN)
        x.circle(300 + 1320 * min(fh, 1), 760, 22, WHITE, a4, 4, fill=CYAN)
        x.text((520, 420), "thin", "title", 44, MUTED, a4, anchor="mm")
        x.text((1400, 420), "thick", "title", 44, MUTED, a4, anchor="mm")
        # frame counters
        x.text((520, 860), f"{int(48 + 4 * math.sin(x.t * 2))} fps", "title", 44, RED, a4, anchor="mm")
        x.text((1400, 860), f"{int(48 + 40 * q + 4 * math.sin(x.t * 2.4))} fps", "title", 44, GREEN, a4, anchor="mm")
        x.text((960, 900), "illustration", "semi", 22, MUTED, a4 * 0.8, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.rect([1170, 615, 1630, 685], GREEN, a5, 4, r=35, fill=PANEL)
        x.text((1400, 650), "compare GPU watts", "title", 34, GREEN, a5, anchor="mm")


def s_prebuilt(x):
    trap_row(x, 5, x.b(0))
    trap_title(x, 5, "Mystery parts", x.b(0))
    a1 = x.b(1)
    if a1 > 0:
        # spec card
        x.rect([150, 290, 700, 640], CYAN, a1, 4, r=16, fill=PANEL)
        x.text((425, 335), "Gaming Prebuilt", "title", 36, WHITE, a1, anchor="mm")
        for k, (s, c) in enumerate([("Fast 8-core CPU", WHITE), ("Big graphics card", WHITE),
                                   ("16 GB RAM", AMBER), ("650 W power supply", AMBER)]):
            x.text((190, 410 + k * 58), s, "semi", 32, c, a1, anchor="lm")
            if c == AMBER:
                x.text((660, 410 + k * 58), "?", "title", 36, AMBER, a1 * (0.6 + 0.4 * math.sin(x.t * 4)), anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        # CPU box with lanes to RAM
        x.rect([800, 330, 960, 490], CYAN, a2, 4, r=12, fill=PANEL)
        x.text((880, 410), "CPU", "title", 36, WHITE, a2, anchor="mm")
        for k, (y, used, lab) in enumerate([(360, True, "channel A"), (460, False, "channel B")]):
            x.line([(960, y), (1380, y)], CYAN if used else GRID, a2, 10, glow=False)
            x.text((1170, y - 25), lab, "semi", 22, MUTED, a2, anchor="mm")
            x.rect([1390, y - 30, 1720, y + 30], CYAN if used else GRID, a2, 3, r=6, fill=PANEL if used else None)
            if used:
                x.text((1555, y), "16 GB stick", "semi", 26, WHITE, a2, anchor="mm")
                for j in range(4):
                    px = 970 + ((x.t * 300 + j * 105) % 400)
                    x.d.rectangle([px, y - 6, px + 24, y + 6], fill=col(WHITE, a2))
            else:
                x.text((1555, y), "empty", "semi", 26, MUTED, a2, anchor="mm")
        x.text((1250, 540), "single channel: half the bandwidth", "title", 32, RED, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        x.rect([150, 690, 560, 900], AMBER, a3, 4, r=12, fill=PANEL)
        x.circle(270, 795, 70, AMBER, a3, 4)
        for j in range(6):
            ang = x.t * 2 + j * math.pi / 3
            x.line([(270, 795), (270 + 60 * math.cos(ang), 795 + 60 * math.sin(ang))], AMBER, a3 * 0.6, 3, glow=False)
        x.text((470, 760), "650 W", "title", 38, WHITE, a3, anchor="mm")
        x.text((470, 830), "brand: ???", "semi", 26, AMBER, a3, anchor="mm")
    a4 = x.b(4)
    if a4 > 0:
        x.text((1180, 640), "headline parts get the budget", "semi", 30, WHITE, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        tag(x, 1000, 790, 380, 110, "2 x 8 GB", GREEN, a5, sub="look for this", size=40)
        tag(x, 1460, 790, 400, 110, "PSU model #", GREEN, a5, sub="ask for this", size=36)


def s_clock(x):
    trap_row(x, 6, x.b(0))
    trap_title(x, 6, "The clock", x.b(0))
    a1 = x.b(1)
    if a1 > 0:
        rem = max(0, 14 * 60 - x.since(1) * 2)
        x.rect([150, 300, 820, 520], RED, a1, 5, r=20, fill=PANEL)
        x.text((485, 345), "deal ends in", "semi", 30, MUTED, a1, anchor="mm")
        x.text((485, 440), f"{int(rem // 60):02d}:{int(rem % 60):02d}", "monob", 110, WHITE, a1, anchor="mm")
        pulse = 0.65 + 0.35 * math.sin(x.t * 6)
        x.d.rounded_rectangle([210, 560, 760, 640], radius=40, fill=col(RED, a1 * pulse))
        x.text((485, 600), "ONLY 3 LEFT!", "title", 40, WHITE, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.rect([920, 300, 1760, 520], CYAN, a2, 4, r=16, fill=PANEL)
        x.text((1340, 350), "FTC staff report, 2022", "title", 34, CYAN, a2, anchor="mm")
        x.text((1340, 420), "called out fake countdown timers", "semi", 30, WHITE, a2, anchor="mm")
        x.text((1340, 470), "and scarcity / demand claims", "semi", 30, WHITE, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        stamp(x, 485, 790, "PRESSURE", AMBER, a3, angle=7)
    a5 = x.b(5)
    a4 = x.b(4)
    if a4 > 0:
        x.text((1340, 590), "meanwhile: the history chart", "semi", 28, MUTED, a4, anchor="mm")
    if a5 > 0:
        box = [940, 640, 1740, 900]
        vals = []
        for k in range(25):
            vals.append(279 if k % 6 == 3 else 329)
        pts = chart(x, box, vals, GREEN, a5, ease(x.since(5) / 2.5), lo=250, hi=350, w=4)
        for k, p in enumerate(pts):
            if vals[k] == 279 and ease(x.since(5) / 2.5) * 24 >= k:
                x.circle(*p, 10, GREEN, a5, 3, fill=GREEN)
        x.text((1740, 650), "it comes back", "title", 30, GREEN, a5, anchor="rm")


def s_seller(x):
    trap_row(x, 7, x.b(0))
    trap_title(x, 7, "Who's selling it?", x.b(0))
    a1 = x.b(1)
    if a1 > 0:
        # big storefront
        x.rect([150, 330, 700, 700], CYAN, a1, 5, r=8, fill=PANEL)
        for k in range(6):
            x.d.pieslice([150 + k * 92, 290, 242 + k * 92, 370], 0, 180, fill=col(AMBER if k % 2 else CYAN, a1))
        x.text((425, 450), "BIG STORE", "title", 50, WHITE, a1, anchor="mm")
        x.rect([360, 540, 490, 700], CYAN, a1, 4, r=6)
        # small seller house
        x.d.polygon([(780, 560), (900, 470), (1020, 560)], fill=col(AMBER, a1))
        x.rect([800, 560, 1000, 700], AMBER, a1, 4, r=4, fill=PANEL)
        x.text((900, 630), "seller", "semi", 28, WHITE, a1, anchor="mm")
        # box travels from seller, not the store
        p = (x.since(1) * 0.4) % 1
        bx = 900 + (1180 - 900) * p
        x.rect([bx - 30, 715, bx + 30, 760], AMBER, a1, 3, r=4, fill=AMBER, glow=False)
        x.line([(900, 738), (1180, 738)], AMBER, a1 * 0.3, 2, glow=False)
        x.text((1210, 738), "you", "title", 30, WHITE, a1, anchor="lm")
    a2 = x.b(2)
    if a2 > 0:
        cx, cy, r = 1500, 500, 170
        frac = 0.6 * ease(x.since(2) / 1.5)
        x.d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360, fill=col(GRID, a2))
        if frac > 0:
            x.d.pieslice([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=col(AMBER, a2))
        x.circle(cx, cy, 90, NAVY, a2, 0, fill=NAVY)
        x.text((cx, cy - 10), "almost", "semi", 24, MUTED, a2, anchor="mm")
        x.text((cx, cy + 25), "60%", "title", 46, WHITE, a2, anchor="mm")
        x.text((cx, cy + r + 40), "independent sellers, by value", "semi", 26, WHITE, a2, anchor="mm")
        x.text((cx, cy + r + 78), "Amazon, 2020", "semi", 24, MUTED, a2, anchor="mm")
    a3 = x.b(3)
    a4 = x.b(4)
    if a3 > 0:
        rows = [("Sold by", "SellerName"), ("Ships from", "SellerName"), ("Returns", "seller's policy")]
        for k, (l, v) in enumerate(rows):
            y = 830 + k * 0 if False else 860
        x.rect([150, 785, 1250, 870], WHITE, a3, 3, r=12, fill=PANEL)
        for k, (l, v) in enumerate(rows):
            x0 = 180 + k * 360
            x.text((x0, 811), l, "semi", 24, MUTED, a3, anchor="lm")
            x.text((x0, 845), v, "title", 26, WHITE, a3, anchor="lm")
            if a4 > 0:
                check(x, x0 + 300, 828, 34, GREEN, a4 * clamp((x.since(4) - k * 0.4) / 0.3))


def s_rerun(x):
    a0 = x.b(0)
    x.text((150, 150), "Re-running the cart", "title", 56, WHITE, a0, anchor="lm")
    # receipt
    if a0 > 0:
        x0, x1 = 300, 1100
        x.rect([x0, 210, x1, 900], WHITE, a0, 0, r=6, fill=PANEL, glow=False)
        for k in range(20):
            zx = x0 + k * 40
            x.d.polygon([(zx, 900), (zx + 20, 920), (zx + 40, 900)], fill=col(PANEL, a0))
        x.text((700, 250), "RECEIPT", "monob", 32, MUTED, a0, anchor="mm")
    rows = [("GPU  RTX 3050", "6 GB version"), ("SSD", "summer price"), ("PREBUILT", "1 stick, mystery PSU"),
            ("LAPTOP", "low-watt GPU")]
    for k, (item, why) in enumerate(rows):
        a = x.b(1 + k)
        if a <= 0:
            continue
        y = 330 + k * 110
        x.text((340, y), item, "monob", 34, WHITE, a, anchor="lm")
        x.text((340, y + 42), why, "mono", 26, AMBER, a, anchor="lm")
        label_box(x, 960, y + 20, "TRAP" if k != 1 else "NO DEAL", RED if k != 1 else AMBER, a, tsize=30)
    a5 = x.b(5)
    if a5 > 0:
        x.line([(340, 770), (1060, 770)], MUTED, a5, 2, glow=False)
        x.text((340, 820), "SAVED", "monob", 36, WHITE, a5, anchor="lm")
        x.text((1060, 820), "$420", "monob", 40, MUTED, a5, anchor="rm")
        strike(x, 940, 820, 1065, RED, a5, ease(x.since(5) / 0.6))
    # savings meter shrinking
    a6 = x.b(6)
    if a5 > 0:
        top, bot = 260, 860
        x.rect([1350, top, 1550, bot], WHITE, a5, 3, r=14)
        f = 1 - 0.8 * ease(x.since(5) / 2.5)
        if a6 > 0:
            f = 0.2
        h = (bot - top - 20) * f
        x.d.rounded_rectangle([1360, bot - 10 - h, 1540, bot - 10], radius=10, fill=col(GREEN, a5))
        x.text((1450, top - 30), "real saving", "semi", 28, WHITE, a5, anchor="mm")
        if a6 > 0:
            x.text((1600, bot - 10 - h - 10), "a fraction", "title", 34, GREEN, a6, anchor="lm")
            x.text((1600, 440), "2 items weren't", "semi", 28, WHITE, a6, anchor="lm")
            x.text((1600, 480), "what Jamie thought", "semi", 28, WHITE, a6, anchor="lm")


def s_check(x):
    a0 = x.b(0)
    x.text((960, 160), "The one-minute check", "title", 60, WHITE, a0, anchor="mm")
    steps = [("Price history", "lower than its own recent prices?"),
             ("Full model name", "the exact version reviews tested?"),
             ("Recent review", "anything changed inside?"),
             ("Hidden numbers", "RAM layout, PSU model, laptop GPU watts"),
             ("The seller", "who ships it, will they take it back?")]
    for k, (h, s) in enumerate(steps):
        a = x.b(1 + k)
        if a <= 0:
            continue
        y = 270 + k * 104
        slide = (1 - a) * 60
        x.rect([260 + slide, y - 44, 1660 + slide, y + 44], CYAN, a, 4, r=44, fill=PANEL)
        x.circle(320 + slide, y, 32, CYAN, a, 4, fill=CYAN)
        x.text((320 + slide, y), str(k + 1), "title", 32, NAVY, a, anchor="mm")
        x.text((380 + slide, y), h, "title", 36, WHITE, a, anchor="lm")
        x.text((760 + slide, y), s, "semi", 30, MUTED, a, anchor="lm")
        a6 = x.b(6)
        check(x, 1600, y, 40, GREEN, a6 * clamp((x.since(6) - k * 0.2) / 0.3))
    a7 = x.b(7)
    if a7 > 0:
        stamp(x, 960, 820, "REAL DEAL", GREEN, a7, angle=-6)


def s_outro(x):
    a0 = x.b(0)
    if a0 > 0:
        x.rect([360, 260, 1560, 640], CYAN, a0, 5, r=24, fill=PANEL)
        x.text((960, 320), "NEXT VIDEO", "semi", 30, AMBER, a0, anchor="mm")
        x.text((960, 400), "What actually raises FPS", "title", 58, WHITE, a0, anchor="mm")
        x.text((960, 470), "and 5 myths that don't", "semi", 36, MUTED, a0, anchor="mm")
        fps = int(60 + 84 * ease(x.since(0) / 4))
        x.text((960, 570), f"{fps} FPS", "monob", 60, GREEN, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.d.rounded_rectangle([760, 720, 1160, 810], radius=45, fill=col(RED, a1))
        x.text((960, 765), "SUBSCRIBE", "title", 44, WHITE, a1, anchor="mm")
        x.text((960, 870), "Best real PC deal you ever found? Tell us below.", "semi", 30, WHITE, a1, anchor="mm")


SCENES = [("One cart, seven traps", s_hook),
          ('Trap 1: the "was" price', s_was),
          ("Trap 2: same name, different chip", s_chip),
          ("Trap 3: the silent swap", s_swap),
          ("Trap 4: laptop GPU power", s_laptop),
          ("Trap 5: prebuilt mystery parts", s_prebuilt),
          ("Trap 6: countdown timers", s_clock),
          ("Trap 7: who's selling it", s_seller),
          ("Re-running the cart", s_rerun),
          ("The one-minute check", s_check),
          ("Up next", s_outro)]
