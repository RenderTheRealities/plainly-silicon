"""Short 10s2: 80 Plus only measures efficiency, not quality (vertical, lab theme).
Visual language: a lab report card look: a rosette badge, a flow band that splits into
useful power and heat, a test-bench load dial with a results table, a checklist with
hand-drawn ticks and crosses, and an oscilloscope trace."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
GOLD = (202, 138, 4)


def rosette(x, cx, cy, r, a, txt1="80 PLUS", txt2="GOLD"):
    if a <= 0:
        return
    pts = []
    for k in range(48):
        ang = k * math.pi / 24 + x.t * 0.3
        rr = r * (1.0 if k % 2 == 0 else 0.9)
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    x.d.polygon(pts, fill=col(GOLD, a))
    x.circle(cx, cy, r * 0.78, PANEL, a, 6, fill=PANEL)
    x.circle(cx, cy, r * 0.7, GOLD, a, 4)
    x.text((cx, cy - r * 0.18), txt1, "title", int(r * 0.26), WHITE, a, anchor="mm")
    x.text((cx, cy + r * 0.2), txt2, "title", int(r * 0.34), GOLD, a, anchor="mm")


def tick(x, cx, cy, s, c, a):
    x.line([(cx - s, cy), (cx - s * 0.3, cy + s * 0.7), (cx + s, cy - s * 0.8)], c, a, 10, glow=False)


def cross(x, cx, cy, s, c, a):
    x.line([(cx - s, cy - s), (cx + s, cy + s)], c, a, 10, glow=False)
    x.line([(cx - s, cy + s), (cx + s, cy - s)], c, a, 10, glow=False)


# ---------- scene 1: the sticker ----------
def s_hook(x):
    a = x.b(0)
    s = 0.7 + 0.3 * ease(x.since(0) / 0.7)
    rosette(x, CX, 740, 290 * s, a)
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 1170), "quality", "title", 96, MUTED, a1, anchor="mm")
        w = 230 * ease(x.since(1) / 0.5)
        x.line([(CX - w, 1175), (CX + w, 1165)], RED, a1, 12, glow=False)


# ---------- scene 2: efficiency as a flow band ----------
def s_flow(x):
    a = x.b(0)
    # wall plug at top
    x.rect([440, 420, 640, 520], WHITE, a, 5, r=14, fill=PANEL + (255,), glow=False)
    for dx in (-40, 40):
        x.line([(CX + dx, 450), (CX + dx, 490)], WHITE, a, 10, glow=False)
    x.text((700, 470), "wall: 100 W", "title", 48, WHITE, a, anchor="lm")
    # band
    g = ease(x.since(0) / 1.2)
    top, mid = 540, 800
    x.d.rectangle([CX - 200, top, CX + 200, top + (mid - top) * g], fill=col(CYAN, a * 0.85))
    a1 = x.b(1)
    if a1 > 0:
        q = ease(x.since(1) / 1.0)
        # useful: 90%
        x.d.rectangle([CX - 200, mid, CX + 160, mid + 330 * q], fill=col(CYAN, a1 * 0.85))
        x.text((CX - 20, mid + 380), "90 W to your parts", "title", 50, CYAN, a1 * q, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        # heat: 10% peeling off the right edge
        for k in range(4):
            yy = mid + 40 + k * 60
            pts = [(CX + 170 + j * 16, yy - 20 * math.sin(x.t * 4 + j * 0.9 + k)) for j in range(14)]
            x.line(pts, RED, a2, 6, glow=False)
        x.text((900, mid - 40), "10 W heat", "title", 46, RED, a2, anchor="mm")


# ---------- scene 3: the load test ----------
def s_test(x):
    a = x.b(0)
    # load dial sweeping 20 -> 50 -> 100
    cx, cy, r = CX, 700, 230
    for k in range(0, 11):
        ang = math.pi + k * math.pi / 10
        x.line([(cx + (r - 30) * math.cos(ang), cy + (r - 30) * math.sin(ang)),
                (cx + r * math.cos(ang), cy + r * math.sin(ang))], MUTED, a, 5, glow=False)
    stops = [0.2, 0.5, 1.0]
    tt = x.since(0)
    idx = min(2, int(tt / 1.1))
    v = stops[idx]
    ang = math.pi + v * math.pi
    x.line([(cx, cy), (cx + (r - 50) * math.cos(ang), cy + (r - 50) * math.sin(ang))], CYAN, a, 12, glow=False)
    x.circle(cx, cy, 20, CYAN, a, 4, fill=CYAN)
    x.text((cx, cy + 70), f"{int(v * 100)}% load", "title", 60, WHITE, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        # results table: rows Gold and Bronze, highlight the 50% column
        y0 = 900
        x.rect([110, y0, 970, y0 + 320], WHITE, a1, 4, r=16, fill=PANEL + (255,), glow=False)
        x.rect([480, y0 + 10, 720, y0 + 310], CYAN, a1, 4, r=12, glow=False)
        for j, h in enumerate(("20%", "50%", "100%")):
            x.text((360 + j * 240, y0 + 55), h, "semi", 40, MUTED, a1, anchor="mm")
        rows = [("Gold", (87, 90, 87), GOLD, 1), ("Bronze", (82, 85, 82), (161, 98, 7), 2)]
        for i, (nm, vals, c, beat) in enumerate(rows):
            aa = x.b(beat)
            y = y0 + 150 + i * 110
            x.text((140, y), nm, "title", 50, c, aa, anchor="lm")
            for j, val in enumerate(vals):
                x.text((360 + j * 240, y), f"{val}%", "title", 52, WHITE, aa, anchor="mm")


# ---------- scene 4: what the badge leaves out ----------
def s_missing(x):
    a = x.b(0)
    items = [("Efficiency", True, 0), ("Steady voltages", False, 1), ("Ripple noise", False, 1), ("Protections", False, 1)]
    for k, (nm, ok, beat) in enumerate(items):
        aa = x.b(beat)
        y = 460 + k * 130
        x.rect([120, y - 50, 960, y + 50], GREEN if ok else RED, aa, 4, r=14, fill=PANEL + (255,), glow=False)
        x.text((200, y), nm, "title", 54, WHITE, aa, anchor="lm")
        if ok:
            tick(x, 880, y, 30, GREEN, aa)
        else:
            cross(x, 880, y, 26, RED, aa)
    x.text((CX, 405), "what 80 Plus tests", "semi", 34, MUTED, a, anchor="mb")
    a2 = x.b(2)
    if a2 > 0:
        # a hand-picked sample: one box lifted out of a row of boxes
        for j in range(5):
            bx = 170 + j * 160
            lift = 70 * ease(x.since(2) / 0.8) if j == 2 else 0
            c = GOLD if j == 2 else MUTED
            x.rect([bx, 1110 - lift, bx + 120, 1210 - lift], c, a2, 4, r=10, fill=PANEL + (255,), glow=False)
        x.text((CX, 1250), "hand-picked test samples", "semi", 38, GOLD, a2, anchor="mm")


# ---------- scene 5: bad build, gold badge, check the review ----------
def s_review(x):
    a = x.b(0)
    x.rect([180, 430, 900, 760], MUTED, a, 5, r=16, fill=PANEL + (255,), glow=False)
    for k in range(5):
        x.line([(230 + k * 40, 470), (230 + k * 40, 720)], GRID, a, 6, glow=False)
    rosette(x, 720, 595, 120, a)
    # noisy scope trace under it
    x.rect([180, 800, 900, 1010], WHITE, a, 4, r=12, fill=PANEL + (255,), glow=False)
    pts = []
    for j in range(90):
        xx = 200 + j * 7.8
        n = 28 * math.sin(j * 1.7 + x.t * 9) * math.sin(j * 0.31 + x.t * 2)
        pts.append((xx, 905 + n))
    x.line(pts, RED, a, 4, glow=False)
    x.text((200, 830), "12 V output", "semi", 30, MUTED, a, anchor="lt")
    a1 = x.b(1)
    if a1 > 0:
        label_box(x, CX, 1120, "look for a load-tested review", CYAN, a1, 44)
        tick(x, CX, 1220, 30, GREEN, a1 * ease(x.since(1) / 0.6))


# ---------- scene 6: the long video ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 560, 940, 1060], WHITE, a, 6, r=8, fill=PANEL + (255,), glow=False)
    x.d.rectangle([140, 560, 940, 600], fill=col(CYAN, a))
    x.text((CX, 680), "FULL VIDEO", "semi", 38, MUTED, a, anchor="mm")
    x.text((CX, 810), "Power Supplies", "title", 92, WHITE, a, anchor="mm")
    x.text((CX, 930), "Explained", "title", 92, CYAN, a, anchor="mm")


SCENES = [
    ("One sticker, one test", s_hook),
    ("Efficiency: wall in, parts out", s_flow),
    ("The 80 Plus load test", s_test),
    ("What the badge leaves out", s_missing),
    ("Read the review, not the sticker", s_review),
    ("Watch the full video", s_end),
]
