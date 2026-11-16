"""Scenes for video 10: Power Supplies Explained.

Design language (ember theme): an electronics bench. Waveforms are shown on small oscilloscope
screens with graticules; the PSU is a left-to-right signal chain of square stage blocks, each with
the waveform at that point drawn under it. Energy moves as small square "packets". Efficiency is a
Sankey-style split (useful power vs heat that rises as wavy lines), load is shown on analog dials,
protections are breaker switches that flip. Sharp corners and thin traces throughout.
"""
import math
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def scope(x, box, fn, a, c, t=0.0, label="", speed=0.25, w=4, n=160, fn2=None, c2=None):
    """Oscilloscope screen. fn(u) returns -1..1 for u in 0..1 (u scrolls with t*speed)."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    x.d.rectangle(box, fill=col(PANEL, a))
    for i in range(1, 8):
        gx = x0 + (x1 - x0) * i / 8
        x.d.line([(gx, y0), (gx, y1)], fill=col(GRID, a), width=1)
    for i in range(1, 4):
        gy = y0 + (y1 - y0) * i / 4
        x.d.line([(x0, gy), (x1, gy)], fill=col(GRID, a), width=2 if i == 2 else 1)
    x.rect(box, MUTED, a, 2, r=0, glow=False)
    h = (y1 - y0) * 0.4
    cy = (y0 + y1) / 2
    pts = [(x0 + (x1 - x0) * k / n, cy - h * fn(k / n + t * speed)) for k in range(n + 1)]
    if fn2:
        pts2 = [(x0 + (x1 - x0) * k / n, cy - h * fn2(k / n + t * speed)) for k in range(n + 1)]
        x.line(pts2, c2 or GREEN, a, max(2, w - 1), glow=False)
    x.line(pts, c, a, w)
    if label:
        x.text((x0 + 4, y0 - 8), label, "mono", 24, MUTED, a, anchor="ld")


def ac(u):
    return math.sin(2 * math.pi * 2 * u)


def rectified(u):
    return abs(math.sin(2 * math.pi * 2 * u)) * 1.8 - 0.9


def smooth_dc(u):
    return 0.75 + 0.06 * abs(math.sin(2 * math.pi * 4 * u))


def pulses(u):
    return 0.8 if (u * 10) % 1 < 0.5 else -0.8


def flat(v):
    return lambda u: v


def stage(x, cx, cy, s, name, c, a):
    """Square stage block with a name."""
    if a <= 0:
        return
    x.rect([cx - s / 2, cy - s / 2, cx + s / 2, cy + s / 2], c, a, 4, r=4, fill=PANEL + (255,))
    x.text((cx, cy), name, "semi", 28, WHITE, a, anchor="mm")


def packets(x, pts, a, t, c=None, gap=60, size=10, v=220):
    """Square energy packets moving along a polyline."""
    if a <= 0:
        return
    c = c or AMBER
    segs = []
    tot = 0
    for p, q in zip(pts, pts[1:]):
        L = math.dist(p, q)
        segs.append((p, q, L))
        tot += L
    d = (t * v) % gap
    while d < tot:
        acc = 0
        for p, q, L in segs:
            if acc + L >= d:
                f = (d - acc) / L
                px, py = p[0] + (q[0] - p[0]) * f, p[1] + (q[1] - p[1]) * f
                x.d.rectangle([px - size / 2, py - size / 2, px + size / 2, py + size / 2], fill=col(c, a))
                break
            acc += L
        d += gap


def arrow(x, x0, y0, x1, y1, c, a, w=4):
    if a <= 0:
        return
    x.line([(x0, y0), (x1, y1)], c, a, w, glow=False)
    ang = math.atan2(y1 - y0, x1 - x0)
    for s in (-1, 1):
        x.line([(x1, y1), (x1 - 18 * math.cos(ang + s * 0.5), y1 - 18 * math.sin(ang + s * 0.5))], c, a, w, glow=False)


def dial(x, cx, cy, r, frac, a, label, zone=(0.5, 0.67)):
    """Analog load dial from 0 to 100 percent, with the efficient zone in green."""
    if a <= 0:
        return
    def pt(f, rr):
        ang = math.pi * (1 - f)
        return cx + rr * math.cos(ang), cy - rr * math.sin(ang)
    x.d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col(GRID, a), width=22)
    z0, z1 = zone
    x.d.arc([cx - r, cy - r, cx + r, cy + r], 180 + 180 * z0, 180 + 180 * z1, fill=col(GREEN, a), width=22)
    for i in range(11):
        p, q = pt(i / 10, r - 30), pt(i / 10, r - 46 if i % 5 else r - 58)
        x.line([p, q], MUTED, a, 3, glow=False)
    tip = pt(clamp(frac), r - 40)
    x.line([(cx, cy), tip], AMBER, a, 6)
    x.circle(cx, cy, 12, AMBER, a, 0, fill=AMBER)
    x.text((cx, cy + 50), f"{frac * 100:.0f}% load", "monob", 40, WHITE, a, anchor="mm")
    x.text((cx, cy + 100), label, "semi", 30, MUTED, a, anchor="mm")


def heat(x, cx, y, a, t, n=3, h=90, c=None):
    """Wavy heat lines rising from (cx, y)."""
    if a <= 0:
        return
    c = c or RED
    for k in range(n):
        ox = cx + (k - (n - 1) / 2) * 34
        ph = t * 3 + k
        pts = [(ox + 9 * math.sin(ph + j / 3), y - j * h / 12) for j in range(13)]
        x.line(pts, c, a * 0.85, 4, glow=False)


def capacitor(x, cx, cy, w, h, c, a, fill_frac=1.0):
    if a <= 0:
        return
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=w * 0.18, fill=PANEL + (255,))
    fh = (h - 16) * clamp(fill_frac)
    if fh > 2:
        x.d.rounded_rectangle([cx - w / 2 + 8, cy + h / 2 - 8 - fh, cx + w / 2 - 8, cy + h / 2 - 8], radius=6,
                              fill=col(c, a * 0.45))
    x.line([(cx - w / 2 + 6, cy - h / 2 + 22), (cx + w / 2 - 6, cy - h / 2 + 22)], c, a, 3, glow=False)
    x.text((cx - w / 2 + 16, cy - h / 2 + 40), "-", "monob", 26, c, a)


def outlet(x, cx, cy, a, s=1.0):
    if a <= 0:
        return
    x.rect([cx - 80 * s, cy - 110 * s, cx + 80 * s, cy + 110 * s], WHITE, a, 4, r=8)
    for dx in (-28, 28):
        x.rect([cx + dx * s - 8 * s, cy - 50 * s, cx + dx * s + 8 * s, cy - 8 * s], WHITE, a, 3, r=2, glow=False)
    x.d.pieslice([cx - 16 * s, cy + 30 * s, cx + 16 * s, cy + 62 * s], 180, 360, fill=col(WHITE, a))


def psu_box(x, cx, cy, a, s=1.0, t=0.0, label=True):
    if a <= 0:
        return
    w, h = 300 * s, 190 * s
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], CYAN, a, 5, r=6, fill=PANEL + (255,))
    fr = 62 * s
    fx = cx - w / 2 + fr + 22 * s
    x.circle(fx, cy, fr, MUTED, a, 3)
    for k in range(5):
        ang = t * 6 + k * 2 * math.pi / 5
        x.line([(fx, cy), (fx + fr * 0.85 * math.cos(ang), cy + fr * 0.85 * math.sin(ang))], MUTED, a, 3, glow=False)
    if label:
        x.text((cx + 70 * s, cy - 20 * s), "PSU", "title", int(48 * s), CYAN, a, anchor="mm")
        x.text((cx + 70 * s, cy + 30 * s), "750 W", "mono", int(28 * s), MUTED, a, anchor="mm")


def gpu_card(x, cx, cy, a, s=1.0, c=None):
    if a <= 0:
        return
    c = c or WHITE
    w, h = 340 * s, 140 * s
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=6, fill=PANEL + (255,))
    for k in (-1, 1):
        x.circle(cx + k * w / 4, cy, h * 0.36, c, a, 3)
    x.d.rectangle([cx - w / 2 + 30 * s, cy + h / 2, cx + w / 2 - 80 * s, cy + h / 2 + 16 * s], fill=col(AMBER, a))
    x.text((cx, cy - h / 2 - 28 * s), "GPU", "semi", int(32 * s), c, a, anchor="mm")


# ---------- scenes ----------
def s_hook(x):
    a0 = x.b(0)
    outlet(x, 260, 470, a0)
    psu_box(x, 900, 470, a0, 1.1, x.t)
    gpu_card(x, 1560, 470, x.b(0, 0.8))
    packets(x, [(340, 470), (735, 470)], a0, x.t)
    packets(x, [(1065, 470), (1390, 470)], a0, x.t, c=CYAN)
    x.text((260, 640), "the wall", "semi", 30, MUTED, a0, anchor="mm")
    x.text((900, 640), "every watt passes here", "semi", 30, MUTED, a0, anchor="mm")
    w = int(lerp(0, 400, x.since(1) / 2.0))
    a1 = x.b(1)
    x.text((960, 230), f"{w} W", "monob", 110, AMBER, a1, anchor="mm")
    for i, s in enumerate(["What the watts mean", "What 80 Plus Gold promises", "Why cheap ones fail"]):
        label_box(x, 420 + i * 540, 760, s, CYAN, ease((x.since(1) - 1.2 - i * 0.6) / 0.4) * a1, 32)


def s_ac_dc(x):
    a0 = x.b(0)
    outlet(x, 200, 470, a0, 0.8)
    a1 = x.b(1)
    scope(x, [380, 300, 900, 640], ac, a1, AMBER, x.t, "CH1  wall")
    x.text((640, 700), "120 V AC", "monob", 44, AMBER, a1, anchor="mm")
    a2 = x.b(2)
    x.text((640, 760), "60 cycles every second", "semi", 30, WHITE, a2, anchor="mm")
    if a2 > 0:
        # bracket one cycle (half the screen shows one full cycle)
        x.line([(380, 240), (640, 240)], CYAN, a2, 3, glow=False)
        for xx in (380, 640):
            x.line([(xx, 228), (xx, 252)], CYAN, a2, 3, glow=False)
        x.text((510, 212), "1/60 s", "mono", 26, CYAN, a2, anchor="mm")
    a3 = x.b(3)
    arrow(x, 940, 470, 1060, 470, MUTED, a3)
    a4 = x.b(4)
    bx = [1100, 300, 1740, 640]
    if a4 > 0:
        x.d.rectangle(bx, fill=col(PANEL, a4))
        x.rect(bx, MUTED, a4, 2, r=0, glow=False)
        for i, (v, c) in enumerate([("12 V", AMBER), ("5 V", CYAN), ("3.3 V", GREEN)]):
            y = 360 + i * 110
            pa = ease((x.since(4) - i * 0.4) / 0.4)
            x.line([(1130, y), (1130 + 420 * pa, y)], c, a4 * pa, 6)
            x.text((1710, y), v, "monob", 34, c, a4 * pa, anchor="rm")
        x.text((1420, 700), "steady DC", "monob", 44, WHITE, a4, anchor="mm")
    a5 = x.b(5)
    label_box(x, 960, 860, "PSU job: wave in, flat lines out", AMBER, a5, 36)


def s_primary(x):
    names = ["FILTER", "RECTIFIER", "PFC", "STORE"]
    fns = [ac, rectified, rectified, smooth_dc]
    beats = [0, 1, 2, 4]
    xs = [300, 740, 1180, 1620]
    for i in range(4):
        a = x.b(beats[i])
        stage(x, xs[i], 330, 190, names[i], AMBER if i < 3 else CYAN, a)
        if i < 3:
            arrow(x, xs[i] + 105, 330, xs[i + 1] - 105, 330, MUTED, x.b(beats[i + 1]))
        f2 = (lambda u: 0.7 * rectified(u)) if i == 2 else None
        scope(x, [xs[i] - 170, 500, xs[i] + 170, 700], fns[i], a, AMBER, x.t, "", 0.25, 3, fn2=f2, c2=GREEN)
    a0 = x.b(0)
    if a0 > 0:
        # noise blocked both ways
        for k, (sx, d) in enumerate([(130, 1), (470, -1)]):
            yy = 220
            pts = [(sx + d * j * 6, yy + 10 * math.sin(j * 1.7 + x.t * 9)) for j in range(10)]
            x.line(pts, RED, a0 * 0.8, 3, glow=False)
        x.text((300, 450), "noise blocked", "mono", 24, MUTED, a0, anchor="mm")
    a1 = x.b(1)
    x.text((740, 450), "one direction only", "mono", 24, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    x.text((1180, 450), "current (green) follows voltage", "mono", 22, MUTED, a2, anchor="mm")
    a3 = x.b(3)
    label_box(x, 1180, 790, "power factor 0.9 or higher", GREEN, a3, 32)
    a4 = x.b(4)
    capacitor(x, 1620, 820, 90, 150, CYAN, a4, 0.3 + 0.7 * clamp(x.since(4) / 2))
    x.text((1620, 450), "reservoir", "mono", 24, MUTED, a4, anchor="mm")


def s_switch(x):
    a1 = x.b(1)
    # switch symbol that toggles fast
    sx, sy = 320, 360
    on = (x.t * 4) % 1 < 0.5
    x.circle(sx - 80, sy, 10, WHITE, a1, 0, fill=WHITE)
    x.circle(sx + 80, sy, 10, WHITE, a1, 0, fill=WHITE)
    end = (sx + 80, sy) if on else (sx + 60, sy - 70)
    x.line([(sx - 80, sy), end], AMBER, a1, 6)
    x.text((sx, sy + 70), "transistor switch", "semi", 28, MUTED, a1, anchor="mm")
    x.text((sx, 200), "on / off", "monob", 40, AMBER, x.b(0) * a1, anchor="mm")
    scope(x, [520, 240, 1080, 480], pulses, a1, AMBER, x.t, "CH2  pulses", 0.08)
    x.text((800, 525), "tens of thousands of times a second", "semi", 28, WHITE, a1, anchor="mm")
    a2 = x.b(2)
    x.text((1440, 200), "Why?", "title", 64, CYAN, a2 * (1 - x.b(3) * 0.6), anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        tx, ty = 1440, 380
        x.rect([tx - 30, ty - 110, tx + 30, ty + 110], MUTED, a3, 4, r=2, fill=GRID + (255,))
        for side, c in ((-1, AMBER), (1, CYAN)):
            for k in range(6):
                cyy = ty - 85 + k * 34
                x.d.arc([tx + side * 50 - 22, cyy - 17, tx + side * 50 + 22, cyy + 17],
                        90 if side < 0 else 270, 270 if side < 0 else 90, fill=col(c, a3), width=5)
        x.text((tx - 150, ty), "wall side", "mono", 24, AMBER, a3, anchor="mm")
        x.text((tx + 160, ty), "PC side", "mono", 24, CYAN, a3, anchor="mm")
        x.line([(tx, ty + 130), (tx, ty + 170)], GREEN, a3, 3, glow=False)
        x.text((tx, ty + 195), "isolated", "semi", 28, GREEN, a3, anchor="mm")
    a4 = x.b(4)
    if a4 > 0:
        x.rect([300, 640, 700, 900], MUTED, a4, 4, r=4, fill=GRID + (255,))
        x.text((500, 770), "60 Hz core", "semi", 34, WHITE, a4, anchor="mm")
        x.text((500, 930), "big, heavy iron", "mono", 24, MUTED, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        sc = lerp(1.0, 0.32, x.since(5) / 1.2)
        cx, cy, w, h = 1100, 770, 400 * sc, 260 * sc
        x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], CYAN, a5, 4, r=4, fill=GRID + (255,))
        x.text((1300, 770), "high frequency: fits in your hand", "semi", 30, CYAN, a5, anchor="lm")


def s_secondary(x):
    a0 = x.b(0)
    scope(x, [140, 200, 520, 380], pulses, a0, AMBER, x.t, "in", 0.08, 3)
    arrow(x, 540, 290, 620, 290, MUTED, a0)
    stage(x, 720, 290, 160, "RECTIFY", AMBER, a0)
    arrow(x, 810, 290, 890, 290, MUTED, a0)
    stage(x, 990, 290, 160, "SMOOTH", AMBER, a0)
    arrow(x, 1080, 290, 1160, 290, MUTED, a0)
    scope(x, [1180, 200, 1560, 380], flat(0.6), a0, AMBER, x.t, "12 V out", 0.1, 4)
    a1 = x.b(1)
    if a1 > 0:
        x.line([(1370, 400), (1370, 470), (720, 470), (720, 400)], GREEN, a1, 3, glow=False)
        packets(x, [(1370, 400), (1370, 470), (720, 470), (720, 400)], a1, x.t, GREEN, 70, 8, 160)
        x.text((1045, 500), "control chip watches and adjusts", "mono", 24, GREEN, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((260, 610), "one 1200 W unit", "semi", 30, MUTED, a2, anchor="lm")
        p = x.b(3)
        bar(x, 260, 690, 1100, 1.0 * p, AMBER, a2, 50, "12 V rail", "up to 1200 W")
        bar(x, 260, 820, 1100, 0.1 * p, CYAN, a2, 50, "5 V + 3.3 V together", "120 W")
    a4 = x.b(4)
    if a4 > 0:
        bx, by = 1620, 740
        x.rect([bx - 90, by - 60, bx + 90, by + 60], CYAN, a4, 3, r=4, fill=PANEL + (255,))
        x.text((bx, by), "DC-DC", "monob", 32, CYAN, a4, anchor="mm")
        x.text((bx, by - 110), "12 V in", "mono", 26, AMBER, a4, anchor="mm")
        arrow(x, bx, by - 90, bx, by - 64, AMBER, a4, 3)
        x.text((bx - 60, by + 110), "5 V", "monob", 28, CYAN, a4, anchor="mm")
        x.text((bx + 60, by + 110), "3.3 V", "monob", 28, GREEN, a4, anchor="mm")


TIERS = [("80 Plus", (80, 80, 80), MUTED), ("Bronze", (82, 85, 82), (205, 127, 50)),
         ("Gold", (87, 90, 87), AMBER), ("Platinum", (90, 92, 89), WHITE), ("Titanium", (92, 94, 90), CYAN)]


def s_80plus(x):
    a0 = x.b(0)
    # chain loses heat at each step
    for i in range(6):
        cx = 260 + i * 100
        x.rect([cx - 34, 180, cx + 34, 248], MUTED, a0, 3, r=2, glow=False)
        heat(x, cx, 172, a0 * 0.8, x.t + i, 1, 50)
    x.text((510, 290), "every step leaks a little heat", "mono", 24, MUTED, a0, anchor="mm")
    a1 = x.b(1)
    x.text((1400, 214), "80 PLUS measures this", "title", 48, AMBER, a1, anchor="mm")
    # chart
    a2 = x.b(2)
    gx0, gx1, gy0, gy1 = 380, 1540, 380, 880
    def X(i):
        return gx0 + (gx1 - gx0) * (0.12 + 0.38 * i)
    def Y(v):
        return gy1 - (v - 78) / (96 - 78) * (gy1 - gy0)
    if a2 > 0:
        for v in (80, 85, 90, 95):
            x.d.line([(gx0, Y(v)), (gx1, Y(v))], fill=col(GRID, a2), width=2)
            x.text((gx0 - 20, Y(v)), f"{v}%", "mono", 26, MUTED, a2, anchor="rm")
        for i, l in enumerate(["20% load", "50% load", "100% load"]):
            x.text((X(i), gy1 + 30), l, "semi", 28, WHITE, a2, anchor="mm")
    for k, (name, vals, c) in enumerate(TIERS):
        a = x.b(3) if k == 0 else ease((x.since(4) - (k - 1) * 0.5) / 0.4) * x.b(4)
        if a <= 0:
            continue
        pts = [(X(i), Y(v)) for i, v in enumerate(vals)]
        x.line(pts, c, a, 4)
        for (px, py) in pts:
            x.circle(px, py, 9, c, a, 0, fill=c)
        x.text((gx1 + 20, Y(vals[2]) + {"Titanium": -16, "Platinum": 14}.get(name, 0)), name, "semi", 28, c, a, anchor="lm")
        x.text((X(1), Y(vals[1]) - 26), f"{vals[1]}", "monob", 26, c, a, anchor="mm")


def flow(x, x0, y, total, used, a, t, title):
    """Sankey-style split: wall power -> parts + heat. 1 px per watt / 2."""
    if a <= 0:
        return
    k = 0.42
    hw = total * k
    hu = used * k
    hh = hw - hu
    x.text((x0 + 790, y + hh / 2), title, "semi", 30, WHITE, a, anchor="lm")
    x.d.rectangle([x0, y - hw / 2, x0 + 260, y + hw / 2], fill=col(AMBER, a * 0.85))
    x.text((x0 + 130, y), f"{total} W", "monob", 34, NAVY, a, anchor="mm")
    x.text((x0 + 130, y + hw / 2 + 28), "from the wall", "mono", 22, MUTED, a, anchor="mm")
    # used part continues
    x.d.polygon([(x0 + 260, y - hw / 2), (x0 + 560, y - hw / 2 + hh), (x0 + 560, y + hw / 2), (x0 + 260, y + hw / 2)],
                fill=col(CYAN, a * 0.7))
    x.d.rectangle([x0 + 560, y - hw / 2 + hh, x0 + 760, y + hw / 2], fill=col(CYAN, a * 0.85))
    x.text((x0 + 660, y + hh / 2), f"{used} W", "monob", 34, NAVY, a, anchor="mm")
    x.text((x0 + 660, y + hw / 2 + 28), "to your parts", "mono", 22, MUTED, a, anchor="mm")
    # heat peels off upward
    x.d.polygon([(x0 + 260, y - hw / 2), (x0 + 260 + hh * 1.2, y - hw / 2), (x0 + 380, y - hw / 2 - 40),
                 (x0 + 380 - hh, y - hw / 2 - 40)], fill=col(RED, a * 0.7))
    heat(x, x0 + 360, y - hw / 2 - 48, a, t, 2 if total < 480 else 4, 60)
    x.text((x0 + 470, y - hw / 2 - 70), f"{total - used} W heat", "monob", 30, RED, a, anchor="lm")


def s_400(x):
    a1 = x.b(1)
    flow(x, 160, 380, 444, 400, a1, x.t, "Gold, half load (90%)")
    a2 = x.b(2)
    flow(x, 160, 760, 500, 400, a2, x.t, "Basic 80 Plus (80%)")
    a4 = x.b(3)
    if a4 > 0:
        psu_box(x, 1450, 330, a4, 0.9, x.t * (1 + 2 * x.b(4)), label=False)
        heat(x, 1450, 220, a4 * x.b(4), x.t, 4, 80)
        x.text((1450, 450), "heat leaves through the fan", "semi", 28, MUTED, a4, anchor="mm")
    a6 = x.b(5)
    if a6 > 0:
        rows = [("efficiency", True, 6), ("voltage stability", False, 7), ("protects your parts", False, 7)]
        for i, (t, ok, bt) in enumerate(rows):
            ra = x.b(bt) * a6
            yy = 640 + i * 80
            x.rect([1340, yy - 24, 1388, yy + 24], GREEN if ok else MUTED, ra, 3, r=4, glow=False)
            x.text((1364, yy), "✓" if ok else "?", "monob", 30, GREEN if ok else MUTED, ra, anchor="mm")
            x.text((1410, yy), t, "semi", 32, WHITE, ra, anchor="lm")
        x.text((1340, 570), "what 80 Plus tests:", "semi", 30, AMBER, x.b(6) * a6, anchor="lm")


def s_label(x):
    a0 = x.b(0)
    if a0 > 0:
        x.rect([220, 200, 640, 460], AMBER, a0, 5, r=4, fill=PANEL + (255,))
        x.text((430, 290), "750 W", "monob", 84, AMBER, a0, anchor="mm")
        x.text((430, 390), "rated output", "semi", 30, WHITE, x.b(1), anchor="mm")
    a1 = x.b(1)
    x.text((430, 520), "most it can deliver, continuously", "mono", 24, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((430, 620), "feeding 400 W pulls about", "semi", 28, WHITE, a2, anchor="mm")
        x.text((430, 690), "444 W", "monob", 64, CYAN, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        parts = [("CPU", 120, AMBER), ("GPU", 220, CYAN), ("rest", 60, MUTED)]
        acc = 0
        x.text((820, 210), "example build", "semi", 30, MUTED, a3, anchor="lm")
        for i, (n, w, c) in enumerate(parts):
            pa = ease((x.since(3) - i * 0.5) / 0.4) * a3
            x0 = 820 + acc * 2.2
            x.d.rectangle([x0, 260, x0 + w * 2.2 - 4, 330], fill=col(c, pa * 0.85))
            x.text((x0 + w * 1.1, 295), f"{n} {w}", "monob", 26, NAVY, pa, anchor="mm")
            acc += w
        x.text((820 + 400 * 2.2 + 20, 295), "= 400 W", "monob", 34, WHITE, ease((x.since(3) - 1.6) / 0.4) * a3, anchor="lm")
    a4 = x.b(4)
    dial(x, 1050, 700, 190, 400 / 650, a4, "650 W unit")
    dial(x, 1560, 700, 190, 400 / 750, a4, "750 W unit")
    x.text((1300, 450), "efficient zone", "semi", 28, GREEN, a4, anchor="mm")


def s_spikes(x):
    a1 = x.b(1)
    def trace(u):
        u = u % 1
        base = -0.2
        for c in (0.18, 0.52, 0.81):
            if abs(u - c) < 0.012:
                return 0.95
        return base + 0.05 * math.sin(u * 90)
    scope(x, [140, 200, 900, 560], trace, a1, CYAN, x.t, "CH3  GPU power", 0.12, 3)
    if a1 > 0:
        x.d.line([(140, 380 - 0.25 * 144), (900, 380 - 0.25 * 144)], fill=col(AMBER, a1), width=3)
        x.text((150, 380 - 0.25 * 144 + 30), "average", "mono", 22, AMBER, a1, anchor="lm")
    a2 = x.b(2)
    if a2 > 0:
        x.rect([160, 640, 880, 760], RED, a2, 4, r=4, fill=PANEL + (255,))
        blink = 0.5 + 0.5 * math.sin(x.t * 8)
        x.text((520, 700), "older PSU: spike = fault -> OFF", "semi", 34, RED, a2 * (0.6 + 0.4 * blink), anchor="mm")
    a3 = x.b(3)
    x.text((1420, 200), "ATX 3.0 excursions", "title", 44, AMBER, a3, anchor="mm")
    steps = [("100 µs", 200), ("1 ms", 180), ("10 ms", 160), ("100 ms", 120)]
    a4 = x.b(4)
    bx0, by1 = 1040, 760
    if a4 > 0:
        x.d.line([(bx0, by1), (1820, by1)], fill=col(MUTED, a4), width=3)
        y100 = by1 - 100 * 2.2
        x.text((bx0 - 10, y100), "100%", "mono", 22, MUTED, a4, anchor="rm")
        for i, (lab, pct) in enumerate(steps):
            pa = ease((x.since(4) - i * 0.4) / 0.4) * a4
            cx = bx0 + 100 + i * 190
            h = pct * 2.2 * pa
            c = AMBER if pct in (200, 120) else MUTED
            x.d.rectangle([cx - 60, by1 - h, cx + 60, by1], fill=col(c, pa * 0.85))
            x.text((cx, by1 - h - 24), f"{pct}%", "monob", 30, c, pa, anchor="mm")
            x.text((cx, by1 + 30), lab, "mono", 26, WHITE, pa, anchor="mm")
        x.d.line([(bx0, y100), (1820, y100)], fill=col(WHITE, a4 * 0.5), width=2)
    a5 = x.b(5)
    if a5 > 0:
        cx, cy = 1420, 880
        x.rect([cx - 170, cy - 34, cx + 30, cy + 34], CYAN, a5, 3, r=4, fill=PANEL + (255,))
        for k in range(6):
            x.d.rectangle([cx - 150 + k * 28, cy - 20, cx - 130 + k * 28, cy + 2], fill=col(CYAN, a5))
        x.text((cx + 60, cy), "12V-2x6: up to 600 W", "semi", 32, CYAN, a5, anchor="lm")


def s_caps(x):
    a2 = x.b(2)
    rows = [(105, 5000), (95, 10000), (85, 20000)]
    x.text((200, 170), "same capacitor, cooler each row", "semi", 30, MUTED, a2, anchor="lm")
    for i, (temp, hours) in enumerate(rows):
        a = x.b(1) if i == 0 else ease((x.since(3) - (i - 1) * 0.8) / 0.4) * x.b(3)
        y = 280 + i * 150
        capacitor(x, 250, y, 70, 110, AMBER if i == 0 else CYAN, a, 0.8)
        x.text((330, y), f"{temp}°C", "monob", 40, RED if i == 0 else WHITE, a, anchor="lm")
        bar(x, 530, y - 20, 560, hours / 20000, GREEN, a, 40, "", f"{hours:,} h")
    a2b = x.b(2)
    x.text((810, 720), "10°C cooler = about 2x the life", "semi", 34, GREEN, a2b * x.b(3), anchor="mm")
    a4 = x.b(4)
    if a4 > 0:
        x.text((1500, 170), "where cheap units save", "semi", 30, AMBER, a4, anchor="mm")
        items = ["small heatsinks", "weak fan", "cheaper capacitors", "less headroom"]
        for i, t in enumerate(items):
            pa = ease((x.since(4) - i * 0.45) / 0.4) * a4
            y = 250 + i * 70
            x.d.line([(1290, y), (1320, y)], fill=col(RED, pa), width=6)
            x.text((1340, y), t, "semi", 32, WHITE, pa, anchor="lm")
    a5 = x.b(5)
    if a5 > 0:
        age = clamp(x.since(5) / 5.0)
        noise = 0.03 + 0.5 * age
        def v12(u):
            return 0.3 + noise * math.sin(u * 140) * math.sin(u * 23 + 1)
        dead = age >= 0.98
        scope(x, [1260, 560, 1760, 820], (lambda u: -0.9) if dead else v12, a5, RED if age > 0.6 else AMBER,
              x.t, "12 V rail", 0.3, 3)
        lab = "won't start" if dead else f"year {1 + int(age * 4)}"
        x.text((1510, 860), lab, "monob", 34, RED if dead else WHITE, a5, anchor="mm")


PROT = [("OVP", "over voltage", 2), ("UVP", "under voltage", 2), ("OCP", "over current", 3),
        ("OPP", "over power", 3), ("SCP", "short circuit", 5), ("OTP", "over temperature", 5)]


def breaker(x, cx, cy, code, desc, a, tripped):
    if a <= 0:
        return
    x.rect([cx - 135, cy - 80, cx + 135, cy + 80], GREEN, a, 3, r=4, fill=PANEL + (255,))
    x.rect([cx - 118, cy - 54, cx - 66, cy + 54], MUTED, a, 3, r=4, glow=False)
    ky = cy + 22 if tripped else cy - 22
    x.d.rectangle([cx - 112, ky - 26, cx - 72, ky + 26], fill=col(GREEN if not tripped else RED, a))
    x.text((cx + 36, cy - 20), code, "monob", 40, GREEN, a, anchor="mm")
    x.text((cx + 36, cy + 30), desc, "mono", 17, WHITE, a, anchor="mm")


def s_protect(x):
    a1 = x.b(1)
    x.text((620, 160), "protection circuits", "title", 44, GREEN, a1, anchor="mm")
    for i, (code, desc, bt) in enumerate(PROT):
        a = ease((x.since(bt) - (i % 2) * 0.4) / 0.4) * x.b(bt)
        cx = 230 + (i % 3) * 270 if False else 220 + (i // 2) * 290
        cy = 300 + (i % 2) * 200
        tripped = a > 0 and (x.since(bt) % 3.0) > 1.6
        breaker(x, cx, cy, code, desc, a, tripped)
    a4 = x.b(4)
    label_box(x, 510, 640, "OPP trips at about 115-135%", AMBER, a4, 30)
    a6 = x.b(6)
    if a6 > 0:
        psu_box(x, 300, 800, a6, 0.6, x.t, label=False)
        gpu_card(x, 900, 800, a6, 0.7, RED)
        k = (x.t * 5) % 1
        pts = [(400, 800), (500, 770), (560, 830), (640, 780), (720, 810), (780, 800)]
        x.line(pts, RED, a6 * (0.5 + 0.5 * k), 5)
        x.text((600, 885), "no protection: fault reaches your parts", "semi", 28, RED, a6, anchor="mm")
    a7 = x.b(7)
    if a7 > 0:
        x.rect([1260, 260, 1700, 460], MUTED, a7, 4, r=6, fill=PANEL + (255,))
        x.text((1480, 330), "1000 W", "monob", 60, MUTED, a7, anchor="mm")
        x.text((1480, 410), "just a sticker", "semi", 28, MUTED, a7, anchor="mm")
        p = x.b(7, 1.0)
        x.circle(1480 + 40 * math.sin(x.t), 640, 120, AMBER, a7, 6)
        x.line([(1565 + 40 * math.sin(x.t), 725), (1660 + 40 * math.sin(x.t), 820)], AMBER, a7, 10)
        x.text((1480 + 40 * math.sin(x.t), 640), "load test", "semi", 32, AMBER, p, anchor="mm")
        x.text((1480, 885), "read independent reviews", "semi", 30, WHITE, a7, anchor="mm")


def s_recap(x):
    a0 = x.b(0)
    names = ["filter", "flip", "smooth", "chop", "step down", "smooth", "12 V"]
    xs = [180 + i * 260 for i in range(7)]
    for i, n in enumerate(names):
        a = ease((x.since(1) - i * 0.45) / 0.4) * x.b(1) if i else a0
        if i == 0:
            a = max(a0 * 0.4, ease((x.since(1)) / 0.4) * x.b(1))
        c = CYAN if i == 6 else AMBER
        x.rect([xs[i] - 90, 220, xs[i] + 90, 330], c, a, 3, r=2, fill=PANEL + (255,))
        x.text((xs[i], 275), n, "semi", 28, WHITE, a, anchor="mm")
    packets(x, [(90, 380), (1830, 380)], a0, x.t, AMBER, 70, 12, 260)
    x.text((960, 170), "400 W, one last time", "semi", 34, MUTED, a0, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        items = ["reviewed, with full protections", "your load near the middle of its rating",
                 "80 Plus Gold if you game for hours a day"]
        for i, t in enumerate(items):
            pa = ease((x.since(2) - i * 0.7) / 0.4) * a2
            y = 500 + i * 80
            x.rect([200, y - 24, 248, y + 24], GREEN, pa, 3, r=4, glow=False)
            x.text((224, y), "✓", "monob", 30, GREEN, pa, anchor="mm")
            x.text((280, y), t, "semi", 34, WHITE, pa, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.rect([1260, 470, 1760, 860], CYAN, a3, 4, r=6, fill=PANEL + (255,))
        x.text((1510, 520), "NEXT", "monob", 30, AMBER, a3, anchor="mm")
        for k in range(4):
            x.rect([1320 + k * 110, 590, 1400 + k * 110, 670], CYAN, a3, 3, r=2, glow=False)
            x.text((1360 + k * 110, 630), "VRAM", "mono", 18, CYAN, a3, anchor="mm")
        x.text((1510, 740), "Why VRAM matters", "title", 42, WHITE, a3, anchor="mm")
        x.text((1510, 800), "running out wrecks frame rates", "mono", 22, MUTED, a3, anchor="mm")


SCENES = [
    ("Follow 400 watts", s_hook),
    ("Wall power vs what parts need", s_ac_dc),
    ("Filter, rectify, correct, store", s_primary),
    ("Why it switches so fast", s_switch),
    ("Making steady 12 volts", s_secondary),
    ("What 80 Plus measures", s_80plus),
    ("Gold vs basic: where 400 W goes", s_400),
    ("What the watts on the label mean", s_label),
    ("GPU power spikes and ATX 3.0", s_spikes),
    ("Why cheap ones fail", s_caps),
    ("Protections and honest labels", s_protect),
    ("Recap and up next", s_recap),
]
