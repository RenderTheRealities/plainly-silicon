"""Short 09s2: why CPU reviews test at 1080p with the fastest GPU (vertical, ocean theme).
Visual language: a two-lane relay track (CPU lane hands a frame baton to the GPU lane),
tall rising fps columns under a movable horizontal "ceiling" bar, and a sliding GPU card."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def gpu_card(x, cx, cy, w, a, c=None):
    """Side view of a big graphics card: shroud, three fans, bracket."""
    if a <= 0:
        return
    c = c or CYAN
    h = w * 0.36
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 5, r=18, fill=PANEL + (255,))
    for k in range(3):
        fx = cx - w / 3 + k * w / 3
        r = h * 0.36
        x.circle(fx, cy, r, WHITE, a, 4)
        for b in range(5):
            ang = x.t * 4 + b * 2 * math.pi / 5
            x.line([(fx, cy), (fx + r * 0.85 * math.cos(ang), cy + r * 0.85 * math.sin(ang))], MUTED, a, 5, glow=False)
    x.rect([cx - w / 2 - 26, cy - h / 2 - 10, cx - w / 2 - 6, cy + h / 2 + 30], MUTED, a, 3, r=4, fill=MUTED, glow=False)


def column(x, cx, base, hpx, c, a, label, val, w=230):
    if a <= 0:
        return
    if hpx > 2:
        x.rect([cx - w / 2, base - hpx, cx + w / 2, base], c, a, 4, r=16, fill=c + (255,))
    x.text((cx, base + 50), label, "title", 52, WHITE, a, anchor="mm")
    if val:
        x.text((cx, base - hpx - 50), val, "title", 56, c, a, anchor="mm")


# ---------- scene 1: the odd test setup ----------
def s_hook(x):
    a = x.b(0)
    # monitor showing 1080p
    x.rect([200, 430, 880, 820], WHITE, a, 6, r=20, fill=PANEL + (255,))
    x.line([(540, 820), (540, 880)], WHITE, a, 10, glow=False)
    x.line([(420, 885), (660, 885)], WHITE, a, 10, glow=False)
    pulse = 1 + 0.04 * math.sin(x.t * 4)
    x.text((540, 625), "1080p", "title", int(130 * pulse), AMBER, a, anchor="mm")
    gpu_card(x, 540, 1060, 620, x.b(0) * ease(x.since(0) / 0.8))
    x.text((540, 1210), "fastest GPU available", "semi", 38, MUTED, a, anchor="mm")
    a2 = x.b(1)
    if a2 > 0:
        stamp(x, 790, 520, "ON PURPOSE", GREEN, a2, angle=-10)


# ---------- scene 2: the relay ----------
def s_relay(x):
    a = x.b(0)
    lanes = [("CPU", 560, AMBER, 0.42), ("GPU", 860, CYAN, 0.58)]
    for name, y, c, frac in lanes:
        x.text((110, y), name, "title", 60, c, a, anchor="lm")
        x.rect([290, y - 50, 970, y + 50], c, a, 4, r=50, glow=False)
    # baton: a frame square travels CPU lane then GPU lane, cycle 2.4 s
    cyc = (x.since(0) % 2.4) / 2.4
    if cyc < 0.42:
        p, y, c = cyc / 0.42, 560, AMBER
    else:
        p, y, c = (cyc - 0.42) / 0.58, 860, CYAN
    bx = 330 + 600 * p
    x.rect([bx - 34, y - 34, bx + 34, y + 34], c, a, 4, r=8, fill=c + (255,))
    x.line([(930, 610), (930, 810)], MUTED, a * 0.6, 4, glow=False)
    a1 = x.b(1)
    if a1 > 0:
        # time per frame bars
        q = ease(x.since(1) / 0.8)
        for k, (nm, frac, c) in enumerate((("CPU time", 0.55, AMBER), ("GPU time", 0.85, CYAN))):
            y = 1010 + k * 130
            x.text((150, y - 20), nm, "semi", 40, WHITE, a1, anchor="ld")
            x.d.rounded_rectangle([150, y, 930, y + 60], radius=30, fill=col(GRID, a1))
            x.d.rounded_rectangle([150, y, 150 + 780 * frac * q, y + 60], radius=30, fill=col(c, a1))
        if q > 0.9:
            label_box(x, 790, 1225, "slower = sets fps", CYAN, a1, 38)


# ---------- scene 3: RTX 3060, GPU is the wall ----------
def s_3060(x):
    a = x.b(0)
    base = 1100
    ceil_y = 600
    g = ease(x.since(0) / 1.0)
    h3 = (base - ceil_y) * g * 0.97
    h9 = (base - ceil_y) * g
    column(x, 330, base, h3, MUTED, a, "Core i3", "")
    column(x, 750, base, h9, AMBER, a, "Core i9", "")
    x.line([(150, ceil_y), (930, ceil_y)], RED, a, 10)
    label_box(x, 540, ceil_y - 70, "RTX 3060 limit", RED, a, 40)
    a1 = x.b(0)
    if g > 0.95:
        x.text((540, 420), "+3%", "title", 110, WHITE, a1, anchor="mm")
    a2 = x.b(1)
    if a2 > 0:
        for k, cx in enumerate((330, 750)):
            for j in range(3):
                on = int(x.t * 3 + j) % 3 == 0
                x.circle(cx - 40 + j * 40, ceil_y + 70, 12, WHITE, a2, 3, fill=WHITE if on else None)
        x.text((540, 1250), "both processors wait", "semi", 40, MUTED, a2, anchor="mm")


# ---------- scene 4: RTX 4090, the ceiling lifts ----------
def s_4090(x):
    a = x.b(0)
    base = 1150
    scale = 3.5  # px per fps
    g = ease(x.since(0) / 1.4)
    ceil_y = 640 - (640 - 470) * g
    v3 = 102 * g + 99 * 0
    v9 = 102 + (186 - 102) * g
    h3 = 102 * scale * min(1, g * 3)
    h9 = v9 * scale
    column(x, 330, base, h3, MUTED, a, "Core i3", f"{int(102 * min(1, g * 3))}")
    column(x, 750, base, min(h9, base - ceil_y - 10), AMBER, a, "Core i9", f"{int(v9)}")
    x.line([(150, ceil_y), (930, ceil_y)], CYAN, a * (1 - g * 0.7), 8)
    if g < 0.5:
        label_box(x, 540, ceil_y - 60, "RTX 4090", CYAN, a, 40)
    a1 = x.b(1)
    if a1 > 0:
        x.text((540, 1262), "frames per second, 1080p", "semi", 36, MUTED, a1, anchor="mm")
    if g > 0.95:
        label_box(x, 330, 560, "+82%", GREEN, a, 64)


# ---------- scene 5: GPU out of the way, the real ceiling ----------
def s_ceiling(x):
    a = x.b(0)
    p = ease(x.since(0) / 1.2)
    gpu_card(x, 540 + 700 * p, 1020, 520, a * (1 - p))
    if p > 0.2:
        x.text((540, 1020), "GPU out of the way", "semi", 44, MUTED, a * p, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        y = 620
        x.rect([120, y - 70, 960, y + 70], AMBER, a1, 6, r=24, fill=PANEL + (255,))
        x.text((540, y), "CPU's real ceiling", "title", 64, AMBER, a1, anchor="mm")
        # a future GPU rising up to meet the ceiling
        q = ease(x.since(1) / 1.6)
        gy = 1200 - (1200 - 800) * q
        gpu_card(x, 540, gy, 380, a1 * 0.9, GREEN)
        if q > 0.9:
            x.text((540, 470), "your next GPU upgrade hits this", "semi", 38, WHITE, a1, anchor="mm")


# ---------- scene 6: the long video ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 560, 940, 1060], CYAN, a, 6, r=30, fill=PANEL + (255,))
    x.text((CX, 650), "FULL VIDEO", "semi", 38, MUTED, a, anchor="mm")
    x.text((CX, 790), "Bottlenecks", "title", 96, WHITE, a, anchor="mm")
    x.text((CX, 920), "Explained", "title", 96, AMBER, a, anchor="mm")


SCENES = [
    ("Why test at 1080p?", s_hook),
    ("The slower part sets fps", s_relay),
    ("RTX 3060: the GPU is the wall", s_3060),
    ("RTX 4090: the gap appears", s_4090),
    ("The CPU's real ceiling", s_ceiling),
    ("Watch the full video", s_end),
]
