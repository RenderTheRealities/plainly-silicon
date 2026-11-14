"""Short 03s1: why many laptops can't take a RAM upgrade (vertical, graphite theme).
Top-down motherboard drawings: a slot, soldered chips, a screwed-in LPCAMM2 module, then a spec sheet."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def board(x, a, box=(120, 470, 960, 1200)):
    """A laptop motherboard seen from above, with a few traces."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    x.rect([x0, y0, x1, y1], MUTED, a, 4, r=34, fill=PANEL + (255,), glow=False)
    for k in range(6):
        yy = y0 + 70 + k * (y1 - y0 - 140) / 5
        x.line([(x0 + 30, yy), (x0 + 90, yy), (x0 + 120, yy + 30)], GRID, a, 4, glow=False)
        x.line([(x1 - 30, yy), (x1 - 90, yy), (x1 - 120, yy - 30)], GRID, a, 4, glow=False)


def cpu(x, cx, cy, a, s=170):
    if a <= 0:
        return
    x.rect([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], CYAN, a, 5, r=14, fill=NAVY + (255,), glow=False)
    x.text((cx, cy), "CPU", "title", 46, CYAN, a, anchor="mm")


def stick(x, x0, y0, w, h, c, a, chips=4):
    """A memory module seen from above: green-less flat board with dark chips and gold edge."""
    if a <= 0:
        return
    x.rect([x0, y0, x0 + w, y0 + h], c, a, 4, r=8, fill=GRID + (255,), glow=False)
    cw = (w - 40) / chips
    for k in range(chips):
        x.d.rectangle([x0 + 20 + k * cw + 6, y0 + 18, x0 + 20 + (k + 1) * cw - 6, y0 + h - 34], fill=col(NAVY, a))
    for k in range(int(w / 14)):
        x.d.rectangle([x0 + 8 + k * 14, y0 + h - 22, x0 + 16 + k * 14, y0 + h - 6], fill=col(AMBER, a * 0.8))


def cross(x, cx, cy, s, a):
    x.line([(cx - s, cy - s), (cx + s, cy + s)], RED, a, 12, glow=False)
    x.line([(cx - s, cy + s), (cx + s, cy - s)], RED, a, 12, glow=False)


def check(x, cx, cy, s, a):
    x.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)], GREEN, a, 12, glow=False)


# ---------- scene 1: the question ----------
def s_hook(x):
    a = x.b(0)
    # an open laptop drawn in perspective-free side view
    x.rect([210, 470, 870, 890], WHITE, a, 6, r=22, fill=PANEL + (255,), glow=False)
    x.rect([250, 510, 830, 850], MUTED, a, 3, r=10, fill=NAVY + (255,), glow=False)
    x.d.polygon([(150, 930), (930, 930), (870, 890), (210, 890)], fill=col(GRID, a), outline=col(WHITE, a))
    x.d.rounded_rectangle([140, 930, 940, 960], radius=10, fill=col(WHITE, a))
    # a new stick hovering, wanting in
    bob = 12 * math.sin(x.t * 3)
    stick(x, 330, 1050 + bob, 420, 120, CYAN, a)
    x.text((540, 680), "+ RAM ?", "title", 88, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1235, "check before you buy", AMBER, a1, 44)


# ---------- scene 2: SO-DIMM slot ----------
def s_sodimm(x):
    a = x.b(0)
    board(x, a)
    cpu(x, 330, 640, a)
    # slot: a long connector with latches at both ends
    sx0, sx1, sy = 200, 880, 900
    x.rect([sx0, sy, sx1, sy + 50], WHITE, a, 4, r=8, fill=NAVY + (255,), glow=False)
    for ex in (sx0 - 10, sx1 - 14):
        x.d.rectangle([ex, sy - 20, ex + 24, sy + 70], fill=col(MUTED, a))
    x.text((CX, 1150), "SO-DIMM slot", "title", 56, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        p = ease(x.since(1) / 1.2)
        yy = 1250 - (1250 - 760) * p
        stick(x, 230, yy - 120 * (1 - p) if p < 1 else 760, 620, 140, CYAN, a1, chips=4)
        if p >= 1:
            check(x, 790, 610, 50, ease((x.since(1) - 1.2) / 0.4))


# ---------- scene 3: soldered LPDDR ----------
def s_soldered(x):
    a = x.b(0)
    board(x, a)
    cpu(x, CX, 760, a, 200)
    a1 = x.b(1)
    if a1 > 0:
        # empty space where a slot would be
        x.rect([220, 1000, 860, 1060], MUTED, a1 * 0.7, 3, r=8, glow=False)
        x.text((CX, 1030), "no slot", "semi", 40, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        # four LPDDR packages hug the CPU, solder balls flash
        for k, (dx, dy) in enumerate([(-230, -110), (-230, 110), (230, -110), (230, 110)]):
            ab = a2 * ease((x.since(2) - k * 0.2) / 0.4)
            cx, cy = CX + dx, 760 + dy
            x.rect([cx - 70, cy - 80, cx + 70, cy + 80], WHITE, ab, 4, r=8, fill=NAVY + (255,), glow=False)
            x.text((cx, cy), "LPDDR", "semi", 28, WHITE, ab, anchor="mm")
            flash = 0.5 + 0.5 * math.sin(x.t * 6 + k)
            for j in range(5):
                x.circle(cx - 56 + j * 28, cy + 92, 7, AMBER, ab * flash, 0, fill=AMBER)
        x.text((CX, 540), "soldered", "title", 64, AMBER, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        stamp(x, CX, 1140, "NO UPGRADES", RED, a3, angle=-6)


# ---------- scene 4: LPCAMM2 ----------
def s_lpcamm(x):
    a = x.b(0)
    board(x, a)
    cpu(x, CX, 600, a, 160)
    # the flat module, wide and short, beside the CPU
    mx0, my0, mx1, my1 = 230, 760, 850, 960
    x.rect([mx0, my0, mx1, my1], CYAN, a, 5, r=14, fill=GRID + (255,), glow=False)
    for k in range(4):
        cx0 = mx0 + 60 + k * 135
        x.d.rectangle([cx0, my0 + 50, cx0 + 100, my1 - 50], fill=col(NAVY, a))
    x.text((CX, 1010), "LPCAMM2", "title", 54, CYAN, a, anchor="mm")
    # screws at the corners turning
    spin = x.since(0) * 4 if x.since(0) < 2 else 8
    for sx, sy in ((mx0 + 25, my0 + 25), (mx1 - 25, my0 + 25), (mx0 + 25, my1 - 25), (mx1 - 25, my1 - 25)):
        x.circle(sx, sy, 16, WHITE, a, 3, fill=MUTED)
        x.line([(sx - 12 * math.cos(spin), sy - 12 * math.sin(spin)), (sx + 12 * math.cos(spin), sy + 12 * math.sin(spin))],
               NAVY, a, 4, glow=False)
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1095), "first in: ThinkPad P1 Gen 7", "semi", 40, WHITE, a1, anchor="mm")
        lift = 30 * ease((x.since(1) - 1.5) / 0.6) * (0.5 + 0.5 * math.sin(x.t * 2))
        check(x, 790, 620 - lift, 45, a1)


# ---------- scene 5: the spec sheet ----------
def s_spec(x):
    a = x.b(0)
    x.rect([150, 450, 930, 1210], WHITE, a, 4, r=20, fill=PANEL + (255,), glow=False)
    x.text((200, 520), "Spec sheet", "title", 54, WHITE, a, anchor="lm")
    rows = [("Display", "14 in", MUTED), ("Processor", "...", MUTED), ("Memory", "", WHITE), ("Storage", "1 TB SSD", MUTED)]
    for k, (lab, val, c) in enumerate(rows):
        y = 640 + k * 130
        x.text((200, y), lab, "semi", 40, c, a, anchor="lm")
        if val:
            x.text((880, y), val, "semi", 38, MUTED, a, anchor="rm")
        x.line([(200, y + 50), (880, y + 50)], GRID, a, 3, glow=False)
    # magnifier sweeps onto the memory row
    p = ease(x.since(0) / 1.2)
    my = 640 + 2 * 130
    gx = 720 - 460 * p
    x.circle(gx, my - 120 * (1 - p), 70, AMBER, a, 7)
    x.line([(gx + 50, my + 50 - 120 * (1 - p)), (gx + 110, my + 110 - 120 * (1 - p))], AMBER, a, 12, glow=False)
    a1 = x.b(1)
    if a1 > 0:
        flip = int(x.since(1) / 1.2) % 2
        x.text((880, my), "16 GB, soldered" if flip == 0 else "2x SO-DIMM slots", "title", 40,
               RED if flip == 0 else GREEN, a1, anchor="rm")
        label_box(x, CX, 1150, "soldered? buy enough on day one", AMBER, a1, 38)
    else:
        x.text((880, my), "?", "title", 48, AMBER, a, anchor="rm")


# ---------- scene 6: outro ----------
def s_end(x):
    a = x.b(0)
    labels = [("SO-DIMM", "swap it", GREEN), ("LPDDR", "soldered", RED), ("LPCAMM2", "swap it", GREEN)]
    for k, (n, v, c) in enumerate(labels):
        y = 540 + k * 170
        ab = a * ease((x.since(0) - k * 0.3) / 0.4)
        x.rect([170, y - 60, 910, y + 60], c, ab, 5, r=24, fill=PANEL + (255,), glow=False)
        x.text((220, y), n, "title", 50, WHITE, ab, anchor="lm")
        x.text((860, y), v, "semi", 42, c, ab, anchor="rm")
    label_box(x, CX, 1120, "Every Type of RAM Explained", CYAN, a * ease(x.since(0) / 0.6 - 0.5), 42)


SCENES = [("Can your laptop take more RAM?", s_hook), ("SO-DIMM: a slot", s_sodimm), ("LPDDR: soldered", s_soldered),
          ("LPCAMM2: screwed in", s_lpcamm), ("Read the spec sheet", s_spec), ("The quick guide", s_end)]
