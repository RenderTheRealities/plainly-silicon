"""Short 04s2: Windows' standby cache, and why "no free memory" is usually fine (vertical, sakura theme).
Shelf style: RAM drawn as a row of shelf cubbies that get stocked with app boxes, a donut of
memory composition, boxes being swept off for a new app, and two upright fill gauges."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
APPS = ["Browser", "Game", "Photos", "Music", "Editor", "Chat"]


def cubby_row(x, y, n, a, filled, colors=None, w=150, gap=14):
    """A RAM 'shelf': n cubbies; filled[i] is a label (or None for empty)."""
    x0 = CX - (n * w + (n - 1) * gap) / 2
    for i in range(n):
        bx = x0 + i * (w + gap)
        x.rect([bx, y, bx + w, y + 150], WHITE, a, 4, r=16, fill=PANEL + (255,), glow=False)
        if filled[i]:
            c = (colors or {}).get(i, AMBER)
            x.rect([bx + 12, y + 12, bx + w - 12, y + 138], c, a, 0, r=12, fill=c + (255,), glow=False)
            x.text((bx + w / 2, y + 75), filled[i], "semi", 26, PANEL, a, anchor="mm")
    return x0


# ---------- scene 1: "almost no free memory" ----------
def s_hook(x):
    a = x.b(0)
    # a big RAM stick
    x.rect([110, 520, 970, 760], WHITE, a, 6, r=14, fill=PANEL + (255,), glow=False)
    for k in range(8):
        x.rect([150 + k * 100, 560, 220 + k * 100, 680], CYAN, a, 0, r=6, fill=CYAN + (255,), glow=False)
    for k in range(40):
        x.d.rectangle([130 + k * 21, 740, 142 + k * 21, 790], fill=col(AMBER, a))
    x.d.rectangle([520, 740, 545, 800], fill=col(NAVY, a))
    # free-memory gauge draining to a sliver
    p = ease(x.since(0) / 2.0)
    free = 1 - 0.97 * p
    x.text((110, 900), "Free", "title", 56, WHITE, a, anchor="ls")
    x.text((970, 900), f"{free * 16:.1f} GB", "title", 56, RED if p > 0.8 else WHITE, a, anchor="rs")
    x.rect([110, 925, 970, 995], WHITE, a, 4, r=35, fill=PANEL + (255,), glow=False)
    x.rect([118, 933, 118 + max(30, 844 * free), 987], RED, a, 0, r=27, fill=(RED if p > 0.8 else AMBER) + (255,), glow=False)
    x.text((CX, 1060), "example: 16 GB PC", "reg", 34, MUTED, a, anchor="mm")
    a1 = x.b(2)
    if a1 > 0:
        x.text((CX, 1170), "usually on purpose", "title", 64, GREEN, a1, anchor="mm")


# ---------- scene 2: Windows stocks the shelf ----------
def s_stock(x):
    a = x.b(0)
    # the drive on the left, shelf on the right
    x.rect([70, 470, 330, 700], WHITE, a, 5, r=20, fill=PANEL + (255,), glow=False)
    x.text((200, 585), "drive", "title", 50, WHITE, a, anchor="mm")
    x.text((640, 450), "RAM", "title", 50, CYAN, a, anchor="mm")
    n = 3
    filled = [None] * 6
    k = int(clamp(x.since(0) / 1.0) * n)
    for i in range(k):
        filled[i] = APPS[i]
    # second row of the shelf
    x0, y0, w = 400, 500, 150
    for r_ in range(2):
        for c_ in range(3):
            i = r_ * 3 + c_
            bx, by = x0 + c_ * (w + 14), y0 + r_ * 170
            x.rect([bx, by, bx + w, by + 150], WHITE, a, 4, r=16, fill=PANEL + (255,), glow=False)
            lab = filled[i]
            if i >= 3:
                # SysMain preloads these later
                if x.b(1) > 0 and x.since(1) > (i - 3) * 0.7:
                    lab = APPS[i]
            if lab:
                c = AMBER if i < 3 else CYAN
                x.rect([bx + 12, by + 12, bx + w - 12, by + 138], c, a, 0, r=12, fill=c + (255,), glow=False)
                x.text((bx + w / 2, by + 75), lab, "semi", 28, PANEL, a, anchor="mm")
    # a box in flight from drive to shelf
    f = (x.t * 0.9) % 1.0
    bx = 330 + 70 * f
    x.rect([bx - 30, 560, bx + 30, 610], AMBER, a * (1 - f), 0, r=8, fill=AMBER + (255,), glow=False)
    a1 = x.b(1)
    if a1 > 0:
        # SysMain badge: an eye that watches your habits
        x.rect([150, 900, 930, 1040], CYAN, a1, 4, r=24, fill=PANEL + (255,), glow=False)
        x.d.ellipse([200, 935, 300, 1005], outline=col(CYAN, a1), width=5)
        x.circle(250 + 18 * math.sin(x.t * 2), 970, 16, CYAN, a1, 0, fill=CYAN)
        x.text((330, 970), "SysMain loads apps early", "semi", 44, WHITE, a1, anchor="lm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((CX, 1150), "= the standby cache", "title", 62, CYAN, a2, anchor="mm")


# ---------- scene 3: the composition donut ----------
def s_donut(x):
    a = x.b(0)
    cx, cy, r = CX, 760, 270
    parts = [("In use", 0.38, WHITE), ("Standby", 0.56, CYAN), ("Free", 0.06, GRID)]
    p = ease(x.since(0) / 1.2)
    start = -90
    for name, frac, c in parts:
        ext = 360 * frac * p
        x.d.pieslice([cx - r, cy - r, cx + r, cy + r], start, start + ext, fill=col(c, a))
        start += ext
    x.circle(cx, cy, 150, NAVY, a, 0, fill=NAVY)
    x.text((cx, cy - 20), "16 GB", "title", 64, WHITE, a, anchor="mm")
    x.text((cx, cy + 40), "example", "reg", 32, MUTED, a, anchor="mm")
    # legend
    ly = 1080
    for i, (name, frac, c) in enumerate(parts):
        lx = 130 + i * 290
        x.rect([lx, ly - 22, lx + 44, ly + 22], c, a, 2, r=8, fill=c + (255,), glow=False)
        x.text((lx + 60, ly), name, "semi", 40, WHITE, a, anchor="lm")
    a1 = x.b(2)
    if a1 > 0:
        # bracket: Cached + Free = available
        x.rect([160, 1150, 920, 1240], GREEN, a1, 4, r=20, fill=PANEL + (255,), glow=False)
        x.text((CX, 1195), "Standby + Free = Available", "title", 46, GREEN, a1, anchor="mm")


# ---------- scene 4: an app needs room; the cache steps aside ----------
def s_evict(x):
    a = x.b(0)
    x0, y0, w = 120, 470, 200
    take = ease(x.since(0) / 1.5)
    for i in range(4):
        bx = x0 + i * (w + 13)
        x.rect([bx, y0, bx + w, y0 + 180], WHITE, a, 4, r=16, fill=PANEL + (255,), glow=False)
        if i < 2:  # the new game claims two slots, pushing cache out
            if take < 1:
                yy = y0 + 12 - 260 * take
                x.rect([bx + 12, yy, bx + w - 12, yy + 156], CYAN, a * (1 - take), 0, r=12, fill=CYAN + (255,), glow=False)
                x.text((bx + w / 2, yy + 78), "cache", "semi", 30, PANEL, a * (1 - take), anchor="mm")
            gy = y0 + 12 + 300 * (1 - take)
            x.rect([bx + 12, gy, bx + w - 12, gy + 156], AMBER, a * take, 0, r=12, fill=AMBER + (255,), glow=False)
            x.text((bx + w / 2, gy + 78), "new app", "semi", 30, PANEL, a * take, anchor="mm")
        else:
            x.rect([bx + 12, y0 + 12, bx + w - 12, y0 + 168], CYAN, a, 0, r=12, fill=CYAN + (255,), glow=False)
            x.text((bx + w / 2, y0 + 90), "cache", "semi", 30, PANEL, a, anchor="mm")
    x.text((CX, 720), "no waiting, no copying", "semi", 40, MUTED, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.rect([90, 800, 520, 1100], RED, a1, 4, r=24, fill=PANEL + (255,), glow=False)
        x.text((305, 880), "empty RAM", "title", 46, RED, a1, anchor="mm")
        x.rect([150, 950, 460, 1040], MUTED, a1, 3, r=12, glow=False)
        x.text((305, 995), "does nothing", "semi", 36, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.rect([560, 800, 990, 1100], GREEN, a2, 4, r=24, fill=PANEL + (255,), glow=False)
        x.text((775, 880), "cached RAM", "title", 46, GREEN, a2, anchor="mm")
        sp = (x.since(2) * 1.4) % 1.0
        x.line([(620, 995), (620 + 300 * sp, 995)], GREEN, a2, 10, glow=False)
        x.text((775, 1060), "faster relaunch", "semi", 36, WHITE, a2, anchor="mm")


# ---------- scene 5: the two numbers that matter ----------
def gauge(x, cx, label, sub, level, c, a):
    top, bot = 480, 1060
    x.rect([cx - 90, top, cx + 90, bot], WHITE, a, 5, r=40, fill=PANEL + (255,), glow=False)
    h = (bot - top - 20) * level
    x.rect([cx - 78, bot - 10 - h, cx + 78, bot - 10], c, a, 0, r=30, fill=c + (255,), glow=False)
    # the "limit" line near the top
    x.line([(cx - 120, top + 40), (cx + 120, top + 40)], RED, a, 4, glow=False)
    x.text((cx, bot + 50), label, "title", 46, WHITE, a, anchor="mm")
    x.text((cx, bot + 105), sub, "reg", 34, MUTED, a, anchor="mm")


def s_check(x):
    a = x.b(0)
    lv = 0.5 + 0.43 * ease(x.since(1) / 2.5) if x.b(1) > 0 else 0.5
    gauge(x, 300, "In use", "vs total RAM", lv, CYAN, a)
    gauge(x, 780, "Committed", "vs its limit", lv * 0.98, AMBER, a)
    a1 = x.b(1)
    if a1 > 0 and lv > 0.9:
        x.text((CX, 440), "both near the top = really short", "title", 44, RED, a1, anchor="mm")


# ---------- scene 6: pointer to the long video ----------
def s_next(x):
    a = x.b(0)
    x.rect([140, 520, 940, 1040], WHITE, a, 5, r=20, fill=PANEL + (255,), glow=False)
    x.d.rectangle([145, 525, 935, 590], fill=col(GRID, a))
    x.text((180, 557), "Task Manager", "semi", 34, WHITE, a, anchor="lm")
    for i, (name, v, c) in enumerate([("CPU", 0.15, CYAN), ("Memory", 0.68, AMBER), ("Disk", 1.0, RED)]):
        y = 660 + i * 120
        x.text((190, y), name, "semi", 38, WHITE, a, anchor="lm")
        bar_w = 420 * v * ease(x.since(0) / 1.0)
        x.rect([440, y - 26, 440 + max(20, bar_w), y + 26], c, a, 0, r=12, fill=c + (255,), glow=False)
    x.text((CX, 1150), "Why Your PC Is Slow", "title", 60, CYAN, a, anchor="mm")
    x.text((CX, 1225), "full video on the channel", "semi", 38, MUTED, a, anchor="mm")


SCENES = [
    ("\"No free memory\"?", s_hook),
    ("Windows stocks spare RAM", s_stock),
    ("Cached still counts", s_donut),
    ("The cache steps aside", s_evict),
    ("What to check instead", s_check),
    ("Find the real slowdown", s_next),
]
