"""Scenes for video 23: The Only Budget GPUs Worth Buying Right Now (tier list).

Design language (neon theme): an arcade scoreboard. Cards are glowing cartridge tiles with a
VRAM badge. The recurring element is the "price meter", a horizontal gauge from $3 to $8 per
point with green / amber / red zones and a needle, so every card is judged on the same dial.
The tier board (S / A / B / SKIP rows) fills up over the video and is complete in the verdict.
"""
import math
from render import *  # noqa: F401,F403

S_C, A_C, B_C, X_C = GREEN, AMBER, CYAN, RED          # tier colors
TIERS = [("S", S_C), ("A", A_C), ("B", B_C), ("SKIP", X_C)]


def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def tile(x, cx, cy, name, vram, a, c=None, w=330, h=104, glow=1.0, ns=34):
    """A cartridge tile: card name + VRAM badge."""
    if a <= 0:
        return
    c = c or CYAN
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=18, fill=PANEL + (255,), glow=glow > 0)
    # notch on the left like a cartridge
    x.d.rectangle([cx - w / 2 + 14, cy - 18, cx - w / 2 + 24, cy + 18], fill=col(c, a))
    x.text((cx - w / 2 + 44, cy), name, "title", ns, WHITE, a, anchor="lm")
    if vram:
        bx = cx + w / 2 - 22
        x.rect([bx - 74, cy - 22, bx, cy + 22], c, a, 2, r=10, fill=NAVY + (255,), glow=False)
        x.text((bx - 37, cy), f"{vram} GB", "semi", 22, c, a, anchor="mm")


def meter(x, x0, y, w, val, a, prog=1.0, label=True):
    """$/point gauge from 3 to 8 with zones; needle eases to val."""
    if a <= 0:
        return
    lo, hi = 3.0, 8.0
    X = lambda v: x0 + w * (v - lo) / (hi - lo)
    for z0, z1, c in [(3, 4, GREEN), (4, 5, AMBER), (5, 8, RED)]:
        x.d.rounded_rectangle([X(z0), y, X(z1), y + 26], radius=6, fill=col(c, a * 0.85))
    for v in range(3, 9):
        x.line([(X(v), y + 30), (X(v), y + 44)], MUTED, a, 2, glow=False)
        x.text((X(v), y + 50), f"${v}", "mono", 24, MUTED, a, anchor="ma")
    cur = lerp(lo, val, ease(prog))
    nx = X(cur)
    x.d.polygon([(nx, y - 6), (nx - 16, y - 34), (nx + 16, y - 34)], fill=col(WHITE, a))
    if label:
        c = GREEN if val <= 4 else AMBER if val <= 5 else RED
        x.text((nx, y - 44), f"${cur:.2f} / point", "monob", 34, c, a, anchor="md")


def score_bar(x, x0, y, w, score, a, c, label, prog=1.0):
    """Speed score bar, 0..110 scale, with a dashed 100 line."""
    if a <= 0:
        return
    x.d.rounded_rectangle([x0, y, x0 + w, y + 40], radius=20, fill=col(GRID, a))
    fw = w * min(score, 110) / 110 * ease(prog)
    if fw > 2:
        x.d.rounded_rectangle([x0, y, x0 + max(40, fw), y + 40], radius=20, fill=col(c, a))
    x100 = x0 + w * 100 / 110
    for k in range(0, 60, 12):
        x.line([(x100, y - 10 + k), (x100, y - 4 + k)], WHITE, a * 0.7, 2, glow=False)
    x.text((x0, y - 12), label, "semi", 30, WHITE, a, anchor="ld")
    x.text((x0 + w, y - 12), f"{int(round(score * ease(prog)))}", "monob", 34, c, a, anchor="rd")


def tag(x, cx, cy, txt, a, c, size=56, strike=0.0):
    """Price tag with a hole; strike draws a line through it."""
    if a <= 0:
        return
    f = font("title", size)
    tw = x.d.textlength(safe(txt, "title"), font=f)
    x0, x1 = cx - tw / 2 - 34, cx + tw / 2 + 30
    y0, y1 = cy - size * 0.75, cy + size * 0.75
    x.d.polygon([(x0 - 30, cy), (x0, y0), (x1, y0), (x1, y1), (x0, y1)], fill=col(PANEL, a), outline=col(c, a))
    x.circle(x0 - 6, cy, 7, c, a, 3)
    x.text((cx + 4, cy), txt, "title", size, c, a, anchor="mm")
    if strike > 0:
        x.line([(x0 - 10, cy + 8), (x0 - 10 + (x1 - x0 + 20) * ease(strike), cy - 8)], RED, a, 6)


def board(x, x0, y0, w, rows, a, rh=118):
    """Tier board. rows: {tier: [(name, vram, alpha), ...]}"""
    if a <= 0:
        return
    for i, (t, c) in enumerate(TIERS):
        y = y0 + i * rh
        x.d.rounded_rectangle([x0, y, x0 + 130, y + rh - 14], radius=14, fill=col(c, a))
        x.text((x0 + 65, y + (rh - 14) / 2), t, "title", 44 if len(t) == 1 else 32, NAVY, a, anchor="mm")
        x.d.rounded_rectangle([x0 + 142, y, x0 + w, y + rh - 14], radius=14, fill=col(PANEL, a * 0.9))
        for k, (name, vram, ta) in enumerate(rows.get(t, [])):
            tile(x, x0 + 142 + 20 + 200 + k * 420, y + (rh - 14) / 2, name, vram, a * ta, c, w=400, h=84, glow=0, ns=32)


def stamp_at(x, cx, cy, s, c, i, angle=-10):
    stamp(x, cx, cy, s, c, x.b(i, 0.35), angle)


# ---------------- scenes ----------------
def s_hook(x):
    a0 = x.b(0)
    x.text((150, 300), "BEST VALUE GPU", "title", 64, WHITE, a0)
    x.text((150, 380), "this Black Friday", "semi", 40, MUTED, a0)
    # S slot with a pulsing question mark
    p = 0.5 + 0.5 * math.sin(x.t * 4)
    x.rect([150, 470, 760, 600], GREEN, a0, 5, r=20, fill=PANEL + (255,))
    x.text((210, 535), "S", "title", 70, GREEN, a0, anchor="mm")
    x.text((470, 535), "?", "title", 90, GREEN, a0 * (0.6 + 0.4 * p), anchor="mm")
    x.text((455, 650), "not Nvidia.  not AMD.", "semi", 36, AMBER, x.b(0), anchor="ma")
    # skip row with a deal-banner card
    a1 = x.b(1)
    x.rect([1000, 470, 1760, 600], RED, a1, 5, r=20, fill=PANEL + (255,))
    x.text((1080, 535), "SKIP", "title", 44, RED, a1, anchor="mm")
    x.text((1450, 535), "BLACK FRIDAY DEAL!", "title", 40, WHITE, a1 * (0.5 + 0.5 * p), anchor="mm")
    # the one number
    a2 = x.b(2)
    x.text((960, 800), "$  per frame", "title", 96, CYAN, a2, anchor="mm")
    x.text((960, 880), "buy price  +  walk-away price", "semi", 34, MUTED, x.b(3), anchor="mm")


def s_prices(x):
    data = [("Arc B570", 219, 289), ("Arc B580", 249, 390), ("RTX 5050", 249, 400),
            ("RTX 5060", 299, 500), ("RX 9060 XT 16GB", 349, 750)]
    a0 = x.b(0)
    x.text((150, 170), "Launch price  vs  mid-November 2026 (US listings)", "semi", 34, MUTED, a0)
    sc = 1.2
    for i, (n, msrp, now) in enumerate(data):
        y = 250 + i * 104
        x.text((150, y + 22), n, "semi", 32, WHITE, a0, anchor="lm")
        x0 = 520
        x.d.rounded_rectangle([x0, y, x0 + msrp * sc, y + 22], radius=8, fill=col(MUTED, a0))
        x.text((x0 + msrp * sc + 14, y + 11), f"${msrp}", "mono", 24, MUTED, a0, anchor="lm")
        p = clamp(x.since(0) / 2.5 - i * 0.15)
        w_ = msrp * sc + (now - msrp) * sc * ease(p)
        x.d.rounded_rectangle([x0, y + 30, x0 + w_, y + 56], radius=8, fill=col(RED, a0))
        x.text((x0 + w_ + 14, y + 43), f"${int(msrp + (now - msrp) * ease(p))}", "monob", 28, RED, a0, anchor="lm")
    # memory being pulled to AI servers
    a2 = x.b(2)
    x.text((150, 810), "memory", "semi", 30, AMBER, a2, anchor="lm")
    for k in range(7):
        t = (x.since(2) * 0.35 + k / 7) % 1
        chip_icon(x, 330 + t * 1000, 810, 40, AMBER, a2 * min(1, 4 * (1 - t)), 3, pins=3)
    x.rect([1380, 772, 1700, 848], CYAN, a2, 3, r=12, fill=PANEL + (255,))
    x.text((1540, 810), "AI servers", "title", 36, CYAN, a2, anchor="mm")
    label_box(x, 1540, 250, "AMD: about +10% in Q4", AMBER, x.b(4), 28)
    label_box(x, 1540, 330, "Nvidia: several raises", AMBER, x.b(4), 28)


def s_method(x):
    a0 = x.b(0)
    score_bar(x, 300, 300, 1300, 100, a0, CYAN, "RTX 5060  =  100  (1080p)", prog=x.since(0) / 1.2)
    x.text((960, 410), "averaged from several independent reviews, rounded", "semi", 28, MUTED, x.b(2), anchor="ma")
    a2 = x.b(3)
    x.text((960, 560), "price  ÷  score  =  $ per point", "title", 70, WHITE, a2, anchor="mm")
    meter(x, 460, 760, 1000, 5.0, x.b(4), prog=x.since(4) / 1.2)
    x.text((960, 650), "lower is better", "semi", 30, GREEN, x.b(4), anchor="mm")


def s_lineup(x):
    rows = [(0, "Arc B570", 10, AMBER), (0, "Arc B580", 12, AMBER),
            (1, "RTX 5050", 8, GREEN), (1, "RTX 5060", 8, GREEN),
            (2, "RX 9060 XT", 8, RED), (2, "RX 9060 XT", 16, RED),
            (3, "RTX 3050", 6, MUTED)]
    pos = [(560, 300), (1360, 300), (560, 470), (1360, 470), (560, 640), (1360, 640), (960, 820)]
    heads = [("INTEL", AMBER, 300), ("NVIDIA", GREEN, 470), ("AMD", RED, 640)]
    for k, (n, c, y) in enumerate(heads):
        x.text((960, y), n, "semi", 26, c, x.b(k + 1), anchor="mm")
    for (i, n, v, c), (cx, cy) in zip(rows, pos):
        tile(x, cx, cy, n, v, x.b(i + 1), c if i < 3 else RED, w=440)
    x.text((960, 900), "keeps showing up in deals", "semi", 26, RED, x.b(4), anchor="mm")


def s_3050(x):
    a0 = x.b(0)
    tile(x, 960, 200, "RTX 3050  6 GB", 6, a0, RED, w=520)
    rows = [("CUDA cores", 2560, 2304, ""), ("Bandwidth", 224, 168, " GB/s"), ("Power", 130, 70, " W")]
    for i, (n, big, small, u) in enumerate(rows):
        y = 360 + i * 150
        a = x.b(min(i + 1, 2))
        x.text((300, y), n, "semi", 32, WHITE, a, anchor="lm")
        mx = max(big, small)
        x.d.rounded_rectangle([600, y - 34, 600 + 900 * big / mx, y - 6], radius=8, fill=col(MUTED, a))
        x.text((600 + 900 * big / mx + 14, y - 20), f"8 GB: {big}{u}", "mono", 24, MUTED, a, anchor="lm")
        x.d.rounded_rectangle([600, y + 4, 600 + 900 * small / mx * ease(x.since(1) / 1.0), y + 32], radius=8, fill=col(RED, a))
        x.text((600 + 900 * small / mx + 14, y + 18), f"6 GB: {small}{u}", "monob", 24, RED, a, anchor="lm")
    x.text((960, 820), "about 20% slower than the 8 GB card", "title", 40, WHITE, x.b(2), anchor="mm")
    stamp_at(x, 1600, 820, "SKIP", RED, 3)


def s_5050(x):
    a0 = x.b(0)
    tile(x, 560, 200, "RTX 5050", 8, a0, GREEN)
    tile(x, 1360, 200, "Arc B570", 10, x.b(2), AMBER)
    score_bar(x, 360, 340, 400, 78, x.b(2), GREEN, "score", prog=x.since(2))
    score_bar(x, 1160, 340, 400, 78, x.b(2), AMBER, "score", prog=x.since(2))
    tag(x, 560, 520, "$249", x.b(3), MUTED, 44, strike=x.since(4) / 0.6)
    tag(x, 560, 640, "$400", x.b(4), RED, 64)
    tag(x, 1360, 580, "$289", x.b(4), GREEN, 64)
    meter(x, 360, 840, 600, 5.13, x.b(5), prog=x.since(5) / 1.2)
    x.text((1360, 690), "same speed, +2 GB, $111 less", "semi", 32, GREEN, x.b(6), anchor="mm")
    stamp_at(x, 1360, 810, "SKIP AT $400", RED, 6, angle=-6)


def s_btier(x):
    a0 = x.b(0)
    tile(x, 560, 190, "RTX 5060", 8, a0, CYAN, w=420)
    tile(x, 1360, 190, "RX 9060 XT", 8, a0, CYAN, w=420)
    score_bar(x, 340, 320, 440, 100, x.b(1), CYAN, "score", prog=x.since(1))
    score_bar(x, 1140, 320, 440, 98, x.b(1), CYAN, "score", prog=x.since(1))
    label_box(x, 960, 340, "TIE", WHITE, x.b(2), 40)
    tag(x, 560, 500, "$299", x.b(3), MUTED, 40, strike=x.since(3) / 0.6)
    tag(x, 860, 500, "$500", x.b(3), AMBER, 54)
    meter(x, 360, 700, 600, 5.00, x.b(4), prog=x.since(4) / 1.2)
    a5 = x.b(5)
    x.text((1200, 470), "8 GB", "title", 56, WHITE, a5)
    x.text((1200, 560), "1080p: fine", "semi", 32, GREEN, a5)
    x.text((1200, 610), "1440p ultra: costs frames", "semi", 32, RED, a5)
    label_box(x, 1400, 840, "walk away above $400", AMBER, x.b(6), 34)


def s_16gb(x):
    a0 = x.b(0)
    tile(x, 960, 180, "RX 9060 XT", 16, a0, CYAN, w=520, h=120)
    score_bar(x, 560, 330, 800, 105, x.b(1), CYAN, "fastest card here", prog=x.since(0))
    p = ease(x.since(3) / 1.5)
    tag(x, 600, 520, f"${int(349 + (750 - 349) * p)}", x.b(2), RED if p > 0.5 else WHITE, 72)
    x.text((600, 620), "launch $349", "semi", 28, MUTED, x.b(2), anchor="mm")
    meter(x, 960, 560, 760, 7.14, x.b(4), prog=x.since(4) / 1.2)
    x.text((1340, 700), "great card, terrible price", "semi", 34, RED, x.b(5), anchor="mm")
    a6 = x.b(6)
    x.rect([560, 780, 1360, 880], GREEN, a6, 4, r=18, fill=PANEL + (255,))
    x.text((960, 830), "walk-away price  $420", "title", 52, GREEN, a6, anchor="mm")


def s_b580(x):
    a0 = x.b(0)
    x.d.rounded_rectangle([160, 160, 300, 300], radius=18, fill=col(A_C, a0))
    x.text((230, 230), "A", "title", 80, NAVY, a0, anchor="mm")
    tile(x, 720, 230, "Arc B580", 12, a0, AMBER, w=560, h=120)
    score_bar(x, 300, 420, 900, 88, x.b(1), AMBER, "score vs RTX 5060 = 100", prog=x.since(1))
    x.text((1380, 440), "12 GB", "title", 80, AMBER, x.b(1), anchor="lm")
    tag(x, 600, 600, "$249", x.b(2), MUTED, 40, strike=x.since(2) / 0.6)
    tag(x, 900, 600, "~$390", x.b(2), AMBER, 54)
    meter(x, 460, 830, 1000, 4.43, x.b(3), prog=x.since(3) / 1.2)


def s_b570(x):
    a0 = x.b(0)
    pulse = 0.75 + 0.25 * math.sin(x.t * 3)
    x.d.rounded_rectangle([160, 160, 300, 300], radius=18, fill=col(S_C, a0 * pulse))
    x.text((230, 230), "S", "title", 80, NAVY, a0, anchor="mm")
    tile(x, 720, 230, "Arc B570", 10, a0, GREEN, w=560, h=120)
    score_bar(x, 300, 400, 700, 78, x.b(1), GREEN, "Arc B570", prog=x.since(1))
    score_bar(x, 300, 500, 700, 84, x.b(1), MUTED, "RTX 4060  (~7% ahead)", prog=x.since(1))
    tag(x, 1350, 430, "$219", x.b(3), MUTED, 40, strike=x.since(3) / 0.6)
    tag(x, 1600, 430, "$289", x.b(3), GREEN, 60)
    x.text((1480, 520), "Newegg, Nov 18", "semi", 26, MUTED, x.b(3), anchor="mm")
    meter(x, 460, 760, 1000, 3.71, x.b(4), prog=x.since(4) / 1.2)
    label_box(x, 960, 900, "$111 less than an RTX 5050, same speed", GREEN, x.b(5), 32)


def s_catch(x):
    a0 = x.b(1)
    # BIOS toggle
    x.rect([160, 180, 900, 470], WHITE, x.b(0), 3, r=8, fill=(0, 0, 0, 255), glow=False)
    x.text((190, 200), "BIOS  >  Advanced  >  PCI Subsystem", "mono", 26, MUTED, x.b(0))
    x.text((190, 290), "Resizable BAR", "mono", 34, WHITE, a0)
    on = x.since(1) > 1.2
    sx = 720
    x.rect([sx, 280, sx + 130, 340], GREEN if on else MUTED, a0, 3, r=30, fill=PANEL + (255,), glow=False)
    kx = sx + (96 if on else 34)
    x.circle(kx, 310, 22, GREEN if on else MUTED, a0, 3, fill=GREEN if on else MUTED)
    x.text((190, 400), "must be ON for Arc", "semi", 30, GREEN if on else AMBER, a0)
    # old CPU overhead
    a2 = x.b(2)
    x.text((1040, 200), "Arc B580, same games", "semi", 32, WHITE, a2)
    score_bar(x, 1040, 300, 700, 100, a2, AMBER, "modern CPU", prog=x.since(2))
    score_bar(x, 1040, 420, 700, 80, x.b(3), RED, "Ryzen 5 2600 (TechSpot)", prog=x.since(3))
    x.text((1040, 520), "about 20% slower", "title", 40, RED, x.b(3))
    x.text((1040, 580), "newer drivers: better, not fixed everywhere", "semi", 26, MUTED, x.b(4))
    a5 = x.b(5)
    x.rect([160, 700, 1760, 880], AMBER, a5, 4, r=20, fill=PANEL + (255,))
    x.text((960, 760), "Old PC, or no Resizable BAR?", "title", 46, AMBER, a5, anchor="mm")
    x.text((960, 830), "pick the RX 9060 XT or RTX 5060 instead", "semi", 36, WHITE, a5, anchor="mm")


def s_rule(x):
    a0 = x.b(0)
    x.text((960, 190), "$4 per point or less", "title", 80, GREEN, x.b(1), anchor="mm")
    rows = [("Arc B570", 10, "under $310"), ("Arc B580", 12, "under $350"),
            ("RTX 5060 / RX 9060 XT 8 GB", 8, "under $400"), ("RX 9060 XT 16 GB", 16, "under $420")]
    for i, (n, v, p) in enumerate(rows):
        y = 320 + i * 120
        a = x.b(min(i + 2, 5))
        x.rect([300, y, 1620, y + 96], CYAN, a, 3, r=16, fill=PANEL + (255,), glow=False)
        x.text((340, y + 48), n, "semi", 36, WHITE, a, anchor="lm")
        x.text((1580, y + 48), p, "monob", 40, GREEN, a, anchor="rm")
    x.text((960, 850), "miss the number = not a deal", "title", 44, RED, x.b(6), anchor="mm")


def s_verdict(x):
    rows = {"S": [("Arc B570", 10, x.b(1))],
            "A": [("Arc B580", 12, x.b(2)), ("RX 9060 XT", 16, x.b(4))],
            "B": [("RTX 5060", 8, x.b(0)), ("RX 9060 XT", 8, x.b(0))],
            "SKIP": [("RTX 5050", 8, x.b(3)), ("RTX 3050", 6, x.b(3))]}
    board(x, 160, 170, 1600, rows, 1.0, rh=150)
    label_box(x, 1500, 170 + 150 + 66, "under $350", AMBER, x.b(2), 26)
    label_box(x, 1500, 170 + 150 + 120, "16 GB: only near $420", AMBER, x.b(4), 22)


def s_outro(x):
    a0 = x.b(0)
    x.text((160, 400), "NEXT UP: MONDAY", "semi", 34, MUTED, a0)
    x.text((160, 470), "DDR4 or DDR5", "title", 84, CYAN, a0)
    x.text((160, 570), "in 2026?", "title", 84, CYAN, a0)
    x.line([(160, 670), (160 + 500 * ease(x.since(0) / 1.5), 670)], AMBER, a0, 6)


SCENES = [
    ("The best value isn't Nvidia or AMD", s_hook),
    ("Why every card costs more", s_prices),
    ("Dollars per point", s_method),
    ("The six-card lineup", s_lineup),
    ("Skip: RTX 3050 6 GB", s_3050),
    ("Skip: RTX 5050", s_5050),
    ("B tier: RTX 5060 and RX 9060 XT 8 GB", s_btier),
    ("RX 9060 XT 16 GB: great card, bad price", s_16gb),
    ("A tier: Arc B580", s_b580),
    ("S tier: Arc B570", s_b570),
    ("The Arc catch", s_catch),
    ("Judge any deal in 10 seconds", s_rule),
    ("The verdict", s_verdict),
    ("Next up: Monday", s_outro),
]
