"""Scenes for video 03: Every Type of RAM Explained, DDR3 to DDR5.
Through-line: one old DDR3 stick and the question "will it fit my new board?"."""
import math
from render import *  # noqa: F401,F403

# schematic notch positions (fraction of module length from the left)
NOTCH = {"DDR3": 0.40, "DDR4": 0.49, "DDR5": 0.545, "SO4": 0.36, "SO5": 0.60}


def lerp(a, b, p):
    return a + (b - a) * p


def stick(x, x0, y0, L, Hh, a, notch=0.5, c=None, chips=8, contacts=56, curve=0.0, label=None,
          pmic=False, lit=None, chip_c=None):
    """Front view of a memory module. Returns the x position of the notch.
    lit(i) -> 0..1 highlight for contact i (optional)."""
    if a <= 0:
        return x0 + L * notch
    c = c or CYAN
    cx = x0 + L / 2

    def bot(xx):
        u = (xx - cx) / (L / 2)
        return y0 + Hh + curve * (1 - u * u)

    n = 40
    outline = [(x0, y0), (x0 + L, y0)] + [(x0 + L - L * k / n, bot(x0 + L - L * k / n)) for k in range(n + 1)]
    x.d.polygon(outline, fill=col(PANEL, a))
    x.line(outline + [outline[0]], c, a, 3, glow=False)
    # DRAM chips
    cw = (L - 60) / chips
    for i in range(chips):
        bx = x0 + 30 + i * cw
        x.d.rectangle([bx + cw * 0.12, y0 + Hh * 0.16, bx + cw * 0.88, y0 + Hh * 0.58], fill=col(chip_c or (20, 24, 26), a))
        x.d.rectangle([bx + cw * 0.12, y0 + Hh * 0.16, bx + cw * 0.88, y0 + Hh * 0.58], outline=col(MUTED, a * 0.6), width=1)
    if pmic:
        x.rect([x0 + 30, y0 + Hh * 0.64, x0 + 30 + cw * 0.9, y0 + Hh * 0.80], GREEN, a, 2, r=3, fill=GREEN + (90,), glow=False)
    # gold contacts with notch gap
    nx = x0 + L * notch
    gap = L * 0.022
    pitch = (L - 24) / contacts
    for i in range(contacts):
        px = x0 + 12 + i * pitch
        if abs(px + pitch / 2 - nx) < gap:
            continue
        b = bot(px + pitch / 2)
        hl = lit(i) if lit else 0
        cc = tuple(int(lerp(AMBER[k], WHITE[k], hl)) for k in range(3))
        x.d.rectangle([px + pitch * 0.18, b - Hh * 0.13, px + pitch * 0.82, b - 3], fill=col(cc, a))
    # notch cut-out
    x.d.rectangle([nx - gap * 0.55, bot(nx) - Hh * 0.17, nx + gap * 0.55, bot(nx) + 3], fill=col(NAVY, a))
    if label:
        f = font("title", int(Hh * 0.17))
        tw = x.d.textlength(label, font=f)
        lx, ly = x0 + L - 40 - tw, y0 + Hh * 0.62
        x.d.rectangle([lx - 12, ly, lx + tw + 12, ly + Hh * 0.2], fill=col(WHITE, a))
        x.text((lx, ly + Hh * 0.1), label, "title", int(Hh * 0.17), NAVY, a, anchor="lm")
    return nx


def arrow(x, p0, p1, c, a, w=4, head=16):
    if a <= 0:
        return
    x.line([p0, p1], c, a, w, glow=False)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    pts = [p1, (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45)),
           (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))]
    x.d.polygon(pts, fill=col(c, a))


def dashed(x, p0, p1, c, a, w=3, seg=14):
    if a <= 0:
        return
    L = math.dist(p0, p1)
    n = max(1, int(L / seg))
    for i in range(0, n, 2):
        t0, t1 = i / n, min(1, (i + 1) / n)
        x.line([(lerp(p0[0], p1[0], t0), lerp(p0[1], p1[1], t0)), (lerp(p0[0], p1[0], t1), lerp(p0[1], p1[1], t1))], c, a, w, glow=False)


def gpu_card_icon(x, cx, cy, s, c, a):
    x.rect([cx - s, cy - s * 0.45, cx + s, cy + s * 0.45], c, a, 3, r=8, glow=False)
    x.circle(cx - s * 0.45, cy, s * 0.32, c, a, 3)
    x.circle(cx + s * 0.45, cy, s * 0.32, c, a, 3)


# ---------- 1. hook ----------
def s_hook(x):
    a0 = x.b(0)
    # new motherboard on the right
    bx0, by0, bx1, by1 = 1080, 170, 1800, 700
    x.rect([bx0, by0, bx1, by1], MUTED, a0, 3, r=14, fill=PANEL + (255,), glow=False)
    x.text((bx0 + 24, by0 + 22), "NEW MOTHERBOARD", "semi", 24, MUTED, a0)
    chip_icon(x, 1260, 330, 130, WHITE, a0, 3)
    x.text((1260, 330), "CPU", "title", 32, WHITE, a0, anchor="mm")
    for k in range(2):
        yy = 560 + k * 56
        x.rect([1140, yy, 1740, yy + 22], WHITE, a0, 2, r=4, glow=False, fill=NAVY + (255,))
    # old stick floats from the left toward the slot
    p = ease(x.since(1) / 1.6) * x.b(1, 0.05)
    sx = lerp(150, 1160, p)
    sy = lerp(330, 380, p) + 8 * math.sin(x.t * 2.2)
    stick(x, sx, sy, 560, 150, a0, NOTCH["DDR3"], WHITE, label="DDR3")
    if p < 0.3:
        x.text((sx + 280, sy - 34), "your old stick", "semi", 30, WHITE, a0 * (1 - p / 0.3), anchor="mm")
    qa = x.b(1) * ease((x.since(1) - 1.6) / 0.4)
    x.text((1600, 250), "fit?", "title", 64, AMBER, qa * (0.75 + 0.25 * math.sin(x.t * 5)), anchor="mm")
    # the journey: 6 kinds of memory along a route
    ra = x.b(2)
    stops = [("DDR3", "desktop"), ("DDR4", "desktop"), ("DDR5", "desktop"), ("SO-DIMM", "laptop"), ("LPDDR", "soldered"), ("GDDR", "graphics card")]
    y = 815
    x.line([(200, y), (1720, y)], GRID, ra, 6, glow=False)
    prog = clamp(x.since(2) / 4.0)
    x.line([(200, y), (lerp(200, 1720, prog), y)], CYAN, ra, 6, glow=False)
    for i, (nm, sub) in enumerate(stops):
        px = 200 + i * 304
        on = ra * ease((prog * 5 - i) / 0.6 + 1)
        x.circle(px, y, 14, CYAN, max(ra * 0.4, on), 3, fill=NAVY)
        if on > 0:
            x.circle(px, y, 7, CYAN, on, 0, fill=CYAN)
        x.text((px, y - 48), nm, "title", 34, CYAN, max(ra * 0.35, on), anchor="mm")
        x.text((px, y + 46), sub, "reg", 26, WHITE, x.b(3) * on, anchor="mm")
    x.circle(lerp(200, 1720, prog), y, 20, AMBER, ra * (prog < 1), 4)


# ---------- 2. what's on the stick, double data rate ----------
def s_inside(x):
    # zoomed DRAM chip: cells leak, refresh sweep restores
    ca = x.b(1)
    x0, y0, cw, chh = 170, 190, 66, 54
    cols_, rows_ = 10, 6
    x.rect([x0 - 30, y0 - 30, x0 + cols_ * cw + 20, y0 + rows_ * chh + 20], WHITE, ca, 3, r=12, fill=(20, 24, 26, 255), glow=False)
    x.text((x0 - 30, y0 - 46), "inside one DRAM chip", "semi", 28, WHITE, ca, anchor="ld")
    la = x.b(2)
    period = 3.0
    sweep = (x.since(2) % period) / period
    for r_ in range(rows_):
        for c_ in range(cols_):
            bit = ((r_ * 7 + c_ * 3) % 5) < 3
            if not bit:
                lvl = 0.12
            elif la <= 0:
                lvl = 1
            else:
                last = (r_ + 0.5) / rows_
                age = (sweep - last) % 1.0
                lvl = 1 - 0.75 * age
            bx, by = x0 + c_ * cw, y0 + r_ * chh
            x.d.rounded_rectangle([bx, by, bx + cw - 10, by + chh - 10], radius=6, fill=col(CYAN, ca * lvl))
    if la > 0:
        sy = y0 + sweep * rows_ * chh
        x.line([(x0 - 20, sy), (x0 + cols_ * cw + 10, sy)], GREEN, la, 4, glow=False)
        x.text((x0 + cols_ * cw + 10, sy - 8), "refresh", "semi", 24, GREEN, la, anchor="rd")
        x.text((x0 + 300, y0 + rows_ * chh + 60), "charge leaks away, so every row is rewritten", "reg", 26, WHITE, la, anchor="mm")
    # DDR title
    da = x.b(3)
    x.text((475, 740), "D D R", "title", 92, AMBER, da, anchor="mm")
    x.text((475, 820), "Double Data Rate", "semi", 36, WHITE, da, anchor="mm")
    # clock and data on both edges
    wa = x.b(4)
    wx0, wx1, hy, ly = 1000, 1800, 210, 300
    P = 200.0
    ph = (x.t * 70) % P
    edges = []
    k = 0
    while True:
        ex = wx0 - ph + k * P / 2
        if ex > wx1:
            break
        edges.append((ex, k % 2 == 0))
        k += 1
    pts = []
    for i, (ex, rising) in enumerate(edges):
        exc = clamp(ex, wx0, wx1)
        lvl_before = ly if rising else hy
        lvl_after = hy if rising else ly
        pts += [(exc, lvl_before), (exc, lvl_after)]
    if pts:
        pts = [(wx0, pts[0][1])] + pts + [(wx1, pts[-1][1])]
        x.line(pts, WHITE, wa, 4, glow=False)
    x.text((wx0, hy - 30), "clock: one tick", "semi", 28, WHITE, wa, anchor="ld")
    # data transfers: a dot on every edge
    for ex, rising in edges:
        if wx0 <= ex <= wx1:
            x.circle(ex, 390, 17, AMBER, wa, 0, fill=AMBER)
            x.line([(ex, ly + 10), (ex, 365)], AMBER, wa * 0.5, 2, glow=False)
    x.text((wx0, 450), "a transfer on the rise AND the fall", "semi", 28, AMBER, wa, anchor="lm")
    # numbers
    na = x.b(5)
    x.text((1400, 560), "speed = transfers per second (MT/s)", "semi", 32, WHITE, na, anchor="mm")
    ea = x.b(6)
    x.rect([1010, 630, 1380, 860], WHITE, ea, 3, r=16, glow=False)
    x.text((1195, 700), "1600", "title", 84, WHITE, ea, anchor="mm")
    x.text((1195, 800), "MHz clock", "semi", 30, WHITE, ea, anchor="mm")
    arrow(x, (1395, 745), (1460, 745), AMBER, ea)
    x.text((1428, 712), "x2", "monob", 30, AMBER, ea, anchor="mm")
    x.rect([1470, 630, 1840, 860], AMBER, ea, 4, r=16, glow=False, fill=PANEL + (255,))
    x.text((1655, 700), "3200", "title", 84, AMBER, ea, anchor="mm")
    x.text((1655, 800), "MT/s on the box", "semi", 30, AMBER, ea, anchor="mm")


# ---------- 3. DDR3 ----------
def s_ddr3(x):
    a = x.b(0)
    fx = None
    fa = x.b(4)
    sweep = clamp(x.since(4) / 2.6)
    lit = (lambda i: 1.0 if fa > 0 and i / 60 < sweep else 0.0)
    L, x0, y0, Hh = 1340, 290, 170, 300
    nx = stick(x, x0, y0, L, Hh, a, NOTCH["DDR3"], WHITE, contacts=60, label="DDR3" if x.b(1) > 0.5 else None, lit=lit)
    if x.b(1) > 0:
        x.circle(x0 + L - 160, y0 + Hh * 0.72, 120 - 40 * x.b(1, 0.4), AMBER, x.b(1) * (1 - x.b(2)), 4)
    # widgets row
    va = x.b(2)
    gx, gy, R = 430, 830, 150
    if va > 0:
        x.d.arc([gx - R, gy - R, gx + R, gy + R], 180, 360, fill=col(MUTED, va), width=8)
        for k, v in enumerate([1.0, 1.2, 1.4, 1.6]):
            ang = math.pi * (1 - (v - 1.0) / 0.6)
            x.text((gx + (R + 28) * math.cos(ang), gy - (R + 28) * math.sin(ang)), f"{v:.1f}", "reg", 22, MUTED, va, anchor="mm")

        def needle(v, c, aa):
            ang = math.pi * (1 - (v - 1.0) / 0.6)
            x.line([(gx, gy), (gx + (R - 18) * math.cos(ang), gy - (R - 18) * math.sin(ang))], c, aa, 6, glow=False)
        v = lerp(1.0, 1.5, ease(x.since(2) / 1.0))
        needle(v, AMBER, va)
        l3 = ease((x.since(2) - 3.0) / 0.6) * va
        needle(1.35, GREEN, l3)
        x.circle(gx, gy, 12, AMBER, va, 0, fill=AMBER)
        x.text((gx, 625), f"{v:.2f} V", "title", 40, AMBER, va, anchor="mm")
        x.text((gx + 170, 880), "DDR3L 1.35 V", "semi", 24, GREEN, l3, anchor="lm")
        x.text((gx, 560), "launched 2007", "semi", 28, WHITE, va, anchor="mm")
    sa = x.b(3)
    if sa > 0:
        sp = int(lerp(800, 2133, ease(x.since(3) / 2.2)))
        x.text((960, 690), f"{sp}", "title", 80, CYAN, sa, anchor="mm")
        x.text((960, 760), "MT/s  (official: 800 to 2133)", "semi", 26, WHITE, sa, anchor="mm")
        bar(x, 790, 805, 340, (sp - 800) / (2133 - 800), CYAN, sa, 24)
    if fa > 0:
        sx = x0 + 12 + sweep * (L - 24)
        x.line([(sx, y0 + Hh - 70), (sx, y0 + Hh + 40)], WHITE, fa * (sweep < 1), 4, glow=False)
        x.text((1490, 690), f"{int(240 * sweep)}", "title", 80, AMBER, fa, anchor="mm")
        x.text((1490, 760), "contacts", "semi", 30, WHITE, fa, anchor="mm")
    ga = x.b(5)
    if ga > 0:
        pr = 50 + 10 * math.sin(x.t * 6)
        x.circle(nx, y0 + Hh - 10, pr, AMBER, ga, 5)
        x.text((nx, y0 + Hh + 80), "the gap", "title", 36, AMBER, ga, anchor="mm")


# ---------- 4. DDR4 ----------
def s_ddr4(x):
    a3 = x.b(0)
    L, x0, Hh = 1060, 420, 150
    n3 = stick(x, x0, 160, L, Hh, a3 * 0.75, NOTCH["DDR3"], MUTED, contacts=48)
    x.text((x0 - 30, 235), "DDR3", "title", 38, MUTED, a3, anchor="rm")
    x.text((x0 + L + 30, 215), "1.5 V", "semi", 28, MUTED, a3, anchor="lm")
    x.text((x0 + L + 30, 255), "240 pins", "semi", 28, MUTED, a3, anchor="lm")
    a4 = x.b(0)
    # DDR4 descends into a slot during beat 2
    slot_y = 760
    drop = ease(x.since(2) / 2.4) * x.b(2, 0.05)
    curve = 16
    y_top_free = 380
    y_top_seat = slot_y - Hh - curve + 26
    y4 = lerp(y_top_free, y_top_seat, drop)
    bottom_c = y4 + Hh + curve

    def lit(i):
        if drop <= 0:
            return 0
        u = abs((i + 0.5) / 56 - 0.5) * 2
        depth = bottom_c - slot_y - curve * (1 - u * u)
        return clamp((depth + curve) / curve)
    sa = x.b(2)
    # slot drawn behind the stick bottom
    if sa > 0:
        x.rect([x0 - 30, slot_y - 4, x0 + L + 30, slot_y + 60], WHITE, sa, 3, r=6, fill=NAVY + (255,), glow=False)
        x.text((x0 + L / 2, slot_y + 100), "curved edge: the middle pins touch first, then the rest", "semi", 28, WHITE, sa, anchor="mm")
    n4 = stick(x, x0, y4, L, Hh, a4, NOTCH["DDR4"], CYAN, contacts=56, curve=curve, lit=lit)
    x.text((x0 - 30, y4 + 75), "DDR4", "title", 38, CYAN, a4, anchor="rm")
    x.text((x0 - 30, y4 + 115), "2014", "semi", 26, WHITE, a4, anchor="rm")
    ia = x.b(1)
    x.text((x0 + L + 50, y4 + 15), "1.2 V", "semi", 28, CYAN, ia, anchor="lm")
    x.text((x0 + L + 50, y4 + 50), "2133 to", "semi", 28, CYAN, ia, anchor="lm")
    x.text((x0 + L + 50, y4 + 85), "3200 MT/s", "semi", 28, CYAN, ia, anchor="lm")
    pa = x.b(2) * (1 - drop)
    x.text((x0 + L + 50, y4 + 120), "288 pins", "semi", 28, AMBER, x.b(2), anchor="lm")
    # same length guides
    dashed(x, (x0, 140), (x0, y4 + Hh + 10), MUTED, x.b(2) * 0.8)
    dashed(x, (x0 + L, 140), (x0 + L, y4 + Hh + 10), MUTED, x.b(2) * 0.8)
    x.text((x0 + L / 2, 140), "same length", "semi", 26, MUTED, pa, anchor="mm")
    # notch offset
    na = x.b(3)
    if na > 0:
        dashed(x, (n3, 160 + Hh - 30), (n3, y4 + Hh + 40), AMBER, na)
        dashed(x, (n4, 160 + Hh - 30), (n4, y4 + Hh + 40), CYAN, na)
        arrow(x, (n3, 400), (n4, 400), AMBER, na, 4, 14)
        x.text(((n3 + n4) / 2, 388), "notch moved", "title", 30, AMBER, na, anchor="md")


# ---------- 5. the notch is a key ----------
def s_key(x):
    a = x.b(0)
    # a DDR4 slot with its ridge, front view
    sx0, sx1, sy = 140, 940, 560
    L = sx1 - sx0 - 40
    ridge_x = sx0 + 20 + L * NOTCH["DDR4"]
    ka = x.b(1)
    x.rect([sx0, sy, sx1, sy + 70], WHITE, a, 3, r=8, fill=NAVY + (255,), glow=False)
    x.text(((sx0 + sx1) / 2, sy + 110), "DDR4 slot", "semi", 30, WHITE, a, anchor="mm")
    rc = AMBER if ka > 0.5 else WHITE
    x.d.rectangle([ridge_x - 7, sy - 22, ridge_x + 7, sy + 4], fill=col(rc, a))
    if ka > 0:
        x.circle(ridge_x, sy - 10, 34 + 4 * math.sin(x.t * 6), AMBER, ka * (1 - x.b(4)), 4)
        x.text((ridge_x, sy + 150), "ridge = key", "title", 32, AMBER, ka, anchor="mm")
    # DDR3 stick tries to go in, lands on the ridge
    da = x.b(2)
    p = ease(x.since(2) / 1.1) * x.b(2, 0.05)
    Hh = 150
    stop_top = sy - 22 - Hh + 10
    yy = lerp(190, stop_top, p)
    if x.since(2) > 1.1:
        yy += -14 * abs(math.sin((x.since(2) - 1.1) * 9)) * math.exp(-(x.since(2) - 1.1) * 3)
    n3 = stick(x, sx0 + 20, yy, L, Hh, max(a * 0.0, da), NOTCH["DDR3"], WHITE, contacts=48, label="DDR3")
    if da > 0 and x.since(2) > 1.1:
        dashed(x, (n3, yy + Hh - 10), (n3, sy + 60), RED, da)
        x.text((n3 - 20, sy + 200), "stick's gap", "semi", 26, RED, da, anchor="rm")
        x.text((ridge_x + 20, sy + 200), "slot's ridge", "semi", 26, AMBER, da, anchor="lm")
    # why: the memory controller in the CPU
    ma = x.b(4)
    cx, cy = 1420, 385
    if ma > 0:
        chip_icon(x, cx, cy, 300, WHITE, ma, 4, pins=5)
        x.text((cx, cy - 95), "CPU", "title", 40, WHITE, ma, anchor="mm")
        x.rect([cx - 120, cy - 40, cx + 120, cy + 100], CYAN, ma, 3, r=10, fill=PANEL + (255,), glow=False)
        x.text((cx, cy + 10), "memory", "semi", 30, CYAN, ma, anchor="mm")
        x.text((cx, cy + 55), "controller", "semi", 30, CYAN, ma, anchor="mm")
        x.text((cx, 120 + 20), "voltage, signals, timing: all built for one generation", "reg", 26, WHITE, ma, anchor="mm")
    ba = x.b(5)
    for k, (nm, bxx) in enumerate([("DDR4 board", 1190), ("DDR5 board", 1650)]):
        aa = ba * ease((x.since(5) - k * 0.4) / 0.5)
        if aa <= 0:
            continue
        dashed(x, (cx, cy + 190), (bxx, 680), CYAN, aa)
        x.rect([bxx - 170, 680, bxx + 170, 820], CYAN, aa, 3, r=12, fill=PANEL + (255,), glow=False)
        for j in range(2):
            x.rect([bxx - 130, 720 + j * 36, bxx + 130, 736 + j * 36], WHITE, aa, 2, r=3, glow=False)
        x.text((bxx, 860), nm, "semi", 28, CYAN, aa, anchor="mm")
    label_box(x, 1420, 625, "one CPU, but each board picks one", WHITE, ba, 26)
    sa = x.b(6)
    stamp(x, 540, 250, "WON'T FIT", RED, sa)


# ---------- 6. DDR5 numbers and the trap ----------
def s_ddr5(x):
    a = x.b(0)
    # speed ranges on one axis
    ax0, ax1, ay = 170, 880, 420
    scale = lambda v: ax0 + (ax1 - ax0) * v / 9000
    x.text((ax0, 160), "official speeds, MT/s", "semi", 28, WHITE, a, anchor="ld")
    rows = [("DDR3", 800, 2133, MUTED, 0), ("DDR4", 2133, 3200, WHITE, 0), ("DDR5", 4800, 8800, CYAN, 1)]
    for i, (nm, lo, hi, c, bi) in enumerate(rows):
        ra = a if bi == 0 else x.b(1)
        grow = ease((x.since(bi) - (i * 0.4 if bi == 0 else 0)) / 1.2)
        yy = 205 + i * 70
        x.text((ax0 - 14, yy + 18), nm, "title", 28, c, ra, anchor="rm")
        if ra > 0:
            xr = scale(lo) + (scale(hi) - scale(lo)) * grow
            x.d.rounded_rectangle([scale(lo), yy, max(scale(lo) + 20, xr), yy + 36], radius=18, fill=col(c, ra))
            x.text((xr + 16, yy + 18), f"{lo} to {int(lerp(lo, hi, grow))}", "semi", 24, c, ra, anchor="lm")
    x.line([(ax0, ay), (ax1, ay)], MUTED, a, 2, glow=False)
    # voltage staircase
    va = x.b(2)
    vx0, vy = 1120, 440
    steps = [("DDR3", 1.5), ("DDR4", 1.2), ("DDR5", 1.1)]
    x.text((vx0, 160), "voltage", "semi", 28, WHITE, a, anchor="ld")
    for i, (nm, v) in enumerate(steps):
        sa_ = a if i < 2 else va
        h = (v - 0.8) * 300
        bx = vx0 + i * 230
        if i == 2:
            h = lerp((1.2 - 0.8) * 300, h, ease(x.since(2) / 0.8))
        x.rect([bx, vy - h, bx + 180, vy], [MUTED, WHITE, CYAN][i], sa_, 3, r=8, fill=PANEL + (255,), glow=False)
        x.text((bx + 90, vy - h - 30), f"{v} V", "title", 32, [MUTED, WHITE, CYAN][i], sa_, anchor="mm")
        x.text((bx + 90, vy + 30), nm, "semi", 26, [MUTED, WHITE, CYAN][i], sa_, anchor="mm")
    # the trap: overlay DDR4 and DDR5
    ta = x.b(3)
    L, x0, y0, Hh = 1100, 410, 590, 210
    sep = 1 - ease(x.since(5) / 1.0) if x.b(5) > 0 else 1
    off = 0 if x.b(4) <= 0 else 0
    if ta > 0:
        n4 = stick(x, x0 - 0, y0, L, Hh, ta * 0.55, NOTCH["DDR4"], WHITE, contacts=56)
        n5 = stick(x, x0, y0, L, Hh, ta * (0.85 if x.b(4) > 0 else 0), NOTCH["DDR5"], CYAN, contacts=56, pmic=True)
        x.text((x0 - 30, y0 + 80), "DDR4", "title", 32, WHITE, ta, anchor="rm")
        x.text((x0 - 30, y0 + 125), "DDR5", "title", 32, CYAN, x.b(4), anchor="rm")
        x.text((x0 + L + 30, y0 + 90), "288", "title", 44, AMBER, x.b(4), anchor="lm")
        x.text((x0 + L + 30, y0 + 140), "= 288", "title", 44, AMBER, x.b(4), anchor="lm")
        x.text((x0 + L + 30, y0 + 190), "pins", "semi", 26, WHITE, x.b(4), anchor="lm")
        dashed(x, (x0, y0 - 20), (x0, y0 + Hh + 10), MUTED, x.b(5))
        dashed(x, (x0 + L, y0 - 20), (x0 + L, y0 + Hh + 10), MUTED, x.b(5))
        x.text((x0 + L / 2, y0 - 22), "same length", "semi", 24, MUTED, x.b(5) * (1 - x.b(6)), anchor="md")
        ga = x.b(6)
        if ga > 0:
            for nx, c, lab in [(n4, WHITE, "DDR4"), (n5, CYAN, "DDR5")]:
                pr = 30 + 5 * math.sin(x.t * 6)
                x.circle(nx, y0 + Hh - 12, pr, c, ga, 4)
            x.text((n4 - 30, y0 - 22), "DDR4 notch", "semi", 24, WHITE, ga, anchor="rd")
            x.text((n5 + 30, y0 - 22), "DDR5 notch", "semi", 24, CYAN, ga, anchor="ld")


# ---------- 7. subchannels ----------
def s_roads(x):
    a = x.b(0)

    def road(y0, h, c, aa, label, packets):
        if aa <= 0:
            return
        x.d.rectangle([300, y0, 1560, y0 + h], fill=col(GRID, aa))
        for k in range(1, 8):
            ly = y0 + h * k / 8
            x.line([(300, ly), (1560, ly)], NAVY, aa * 0.6, 1, glow=False)
        x.text((300, y0 - 12), label, "semi", 26, c, aa, anchor="ld")
        for (ph, pc) in packets:
            px = 300 + ((x.t * 260 + ph) % 1400) - 140
            x0_, x1_ = max(300, px), min(1560, px + 130)
            if x1_ > x0_:
                x.d.rounded_rectangle([x0_, y0 + 4, x1_, y0 + h - 4], radius=6, fill=col(pc, aa))

    # endpoints
    for yy in (220, 590):
        pass
    sa = x.b(1)
    stick_icon_a = max(a, sa)
    x.rect([130, 180, 270, 400], WHITE, sa, 3, r=6, glow=False)
    x.text((200, 290), "DDR4", "title", 28, WHITE, sa, anchor="mm")
    road(225, 110, WHITE, sa, "one 64-bit channel: everything rides together", [(0, AMBER), (700, AMBER)])
    da = x.b(2)
    x.rect([130, 450, 270, 700], CYAN, da, 3, r=6, glow=False)
    x.text((200, 575), "DDR5", "title", 28, CYAN, da, anchor="mm")
    road(475, 55, CYAN, da, "two independent 32-bit subchannels", [(200, AMBER), (900, AMBER)])
    if da > 0:
        x.d.rectangle([300, 600, 1560, 655], fill=col(GRID, da))
        x.text((300, 668), "", "semi", 20, CYAN, da)
        for (ph, pc) in [(500, GREEN), (1150, GREEN)]:
            px = 300 + ((x.t * 330 + ph) % 1400) - 140
            x0_, x1_ = max(300, px), min(1560, px + 100)
            if x1_ > x0_:
                x.d.rounded_rectangle([x0_, 604, x1_, 651], radius=6, fill=col(pc, da))
        for k in range(1, 4):
            ly = 600 + 55 * k / 4
            x.line([(300, ly), (1560, ly)], NAVY, da * 0.6, 1, glow=False)
    # CPU at the end
    chip_icon(x, 1720, 450, 200, WHITE, a, 4)
    x.text((1720, 450), "CPU", "title", 40, WHITE, a, anchor="mm")
    # burst math
    ba = x.b(3)
    if ba > 0:
        fill4 = clamp(x.since(3) / 2.0)
        fill5 = clamp(x.since(3) / 2.0)
        gx, gy, cs = 330, 760, 13
        for c_ in range(8):
            for r_ in range(8):
                on = c_ < fill4 * 8
                x.d.rectangle([gx + c_ * cs * 2.2, gy + r_ * cs, gx + c_ * cs * 2.2 + cs * 2, gy + r_ * cs + cs - 3], fill=col(AMBER if on else GRID, ba))
        x.text((gx + 260, gy + 50), "8 transfers x 64 bits", "semi", 28, WHITE, ba, anchor="lm")
        x.text((gx + 260, gy + 90), "= 64 bytes", "title", 30, AMBER, ba, anchor="lm")
        hx = 1010
        for c_ in range(16):
            for r_ in range(4):
                on = c_ < fill5 * 16
                x.d.rectangle([hx + c_ * cs * 1.1, gy + 26 + r_ * cs, hx + c_ * cs * 1.1 + cs - 2, gy + 26 + r_ * cs + cs - 3], fill=col(GREEN if on else GRID, ba))
        x.text((hx + 240, gy + 50), "16 transfers x 32 bits", "semi", 28, WHITE, ba, anchor="lm")
        x.text((hx + 240, gy + 90), "= 64 bytes", "title", 30, GREEN, ba, anchor="lm")
    ra = x.b(4)
    if ra > 0:
        label_box(x, 930, 712, "2 requests at once per stick", GREEN, ra, 30)


# ---------- 8. PMIC, on-die ECC, capacity ----------
def s_power(x):
    a = x.b(0)
    old = x.b(1) * (1 - x.b(2))
    new = x.b(2)
    L, x0, y0, Hh = 620, 260, 200, 220
    stick(x, x0, y0, L, Hh, a, NOTCH["DDR5"], CYAN, contacts=44, pmic=new > 0.5)
    x.text((x0 + L / 2, y0 - 30), "DDR5 stick", "title", 32, CYAN, a, anchor="mm")
    # old way: motherboard regulator feeding up into the stick
    if old > 0:
        x.rect([x0 + 160, 560, x0 + 460, 640], WHITE, old, 3, r=10, glow=False)
        x.text((x0 + 310, 600), "board regulator", "semi", 26, WHITE, old, anchor="mm")
        arrow(x, (x0 + 310, 556), (x0 + 310, y0 + Hh + 8), WHITE, old)
        x.text((x0 + 330, 520), "older sticks", "reg", 24, MUTED, old, anchor="lm")
    if new > 0:
        px, py = x0 + 30 + 34, y0 + Hh * 0.72
        x.circle(px, py, 40 + 4 * math.sin(x.t * 5), GREEN, new, 3)
        arrow(x, (px - 140, py + 130), (px - 10, py + 30), AMBER, new)
        x.text((px - 150, py + 150), "5 V in", "title", 30, AMBER, new, anchor="mm")
        x.text((px + 50, y0 + Hh + 40), "power chip (PMIC) on the stick", "semi", 26, GREEN, new, anchor="lt")
        for k in range(4):
            ph = (x.t * 1.2 + k * 0.25) % 1
            tx = lerp(px + 40, x0 + L - 60, ph)
            x.circle(tx, y0 + Hh * 0.72, 6, GREEN, new * (1 - ph), 0, fill=GREEN)
        x.text((x0 + L + 16, y0 + Hh * 0.72), "1.1 V", "title", 28, GREEN, new, anchor="lm")
    # on-die ECC
    ea = x.b(3)
    gx, gy, cs = 1080, 190, 46
    if ea > 0:
        x.rect([gx - 30, gy - 30, gx + 8 * cs + 20, gy + 5 * cs + 20], WHITE, ea, 3, r=10, fill=(20, 24, 26, 255), glow=False)
        x.text((gx - 30, gy - 44), "inside one chip", "semi", 26, WHITE, ea, anchor="ld")
        cyc = x.since(3) % 3.0
        for r_ in range(5):
            for c_ in range(8):
                v = (r_ * 5 + c_ * 3) % 2
                c = CYAN
                if (r_, c_) == (2, 5):
                    if 0.8 < cyc < 1.8:
                        v, c = 1 - v, RED
                    elif cyc >= 1.8:
                        c = GREEN
                bx, by = gx + c_ * cs, gy + r_ * cs
                x.text((bx + cs / 2 - 5, by + cs / 2 - 5), str(v), "monob", 30, c, ea, anchor="mm")
        lab = "bit flips" if 0.8 < (x.since(3) % 3.0) < 1.8 else ("fixed inside the chip" if (x.since(3) % 3.0) >= 1.8 else "")
        x.text((gx + 8 * cs + 50, gy + 2.5 * cs), lab, "semi", 28, RED if lab == "bit flips" else GREEN, ea, anchor="lm")
        x.text((gx + 4 * cs, gy + 5 * cs + 60), "on-die ECC", "title", 34, GREEN, ea, anchor="mm")
    # protected vs unprotected path
    pa = x.b(4)
    if pa > 0:
        yy = 640
        x.rect([1060, yy - 40, 1200, yy + 40], CYAN, pa, 3, r=8, glow=False)
        x.text((1130, yy), "chip", "semi", 26, CYAN, pa, anchor="mm")
        chip_icon(x, 1720, yy, 90, WHITE, pa, 3)
        x.text((1720, yy), "CPU", "semi", 22, WHITE, pa, anchor="mm")
        x.d.rounded_rectangle([1062, yy - 38, 1198, yy + 38], radius=8, fill=col(GREEN, pa * 0.25))
        dashed(x, (1205, yy), (1655, yy), RED, pa, 4)
        x.text((1430, yy - 22), "trip to the CPU: not covered", "reg", 24, RED, pa, anchor="md")
        x.text((1430, yy + 30), "server ECC memory covers this too", "reg", 24, WHITE, pa, anchor="ma")
    # capacity
    ca = x.b(5)
    if ca > 0:
        s = 54
        bx, by = 260, 760
        x.d.rectangle([bx, by, bx + s, by + s], fill=col(WHITE, ca))
        x.text((bx + s / 2, by + s + 30), "64 GB", "title", 28, WHITE, ca, anchor="mm")
        x.text((bx + s / 2, by - 28), "DDR4 max", "reg", 22, MUTED, ca, anchor="mm")
        n = int(clamp(x.since(5) / 1.6) * 8 + 0.999)
        for k in range(n):
            r_, c_ = divmod(k, 4)
            xx, yy2 = 420 + c_ * (s + 8), by - 34 + r_ * (s + 8)
            x.d.rectangle([xx, yy2, xx + s, yy2 + s], fill=col(CYAN, ca))
        x.text((420 + 2 * (s + 8) - 4, by + s + 64), "512 GB  DDR5 max", "title", 28, CYAN, ca, anchor="mm")


# ---------- 9. laptops: SO-DIMM ----------
def s_laptop(x):
    a = x.b(0)
    sa = x.b(1)
    k = 6.0  # px per mm
    # desktop DIMM vs SO-DIMM, to scale
    dx0, dy = 160, 190
    dL, dH = 133.35 * k, 31 * k
    stick(x, dx0, dy, dL, dH, sa, NOTCH["DDR5"], WHITE, contacts=56)
    sx0 = 1130
    sL, sH = 67.6 * k, 30 * k
    grow = ease(x.since(1) / 0.8)
    stick(x, sx0, dy, sL, sH, sa * grow, NOTCH["SO5"], CYAN, chips=4, contacts=32)
    x.text((dx0, dy - 18), "desktop DIMM", "semi", 28, WHITE, sa, anchor="ld")
    x.text((sx0, dy - 18), "laptop SO-DIMM", "semi", 28, CYAN, sa, anchor="ld")
    for (x0_, L_, lab, c) in [(dx0, dL, "133 mm", WHITE), (sx0, sL, "about 68 mm", CYAN)]:
        ry = dy + dH + 34
        x.line([(x0_, ry), (x0_ + L_, ry)], c, sa, 2, glow=False)
        for e in (x0_, x0_ + L_):
            x.line([(e, ry - 12), (e, ry + 12)], c, sa, 2, glow=False)
        x.text((x0_ + L_ / 2, ry + 32), lab, "title", 30, c, sa, anchor="mm")
    if a > 0 and sa <= 0:
        x.text((960, 300), "same question, smaller stick", "title", 50, WHITE, a, anchor="mm")
    # two SO-DIMMs, different keys
    ka = x.b(3)
    y2 = 560
    so4 = stick(x, 160, y2, sL, sH, ka, NOTCH["SO4"], WHITE, chips=4, contacts=32)
    so5 = stick(x, 680, y2, sL, sH, ka * ease((x.since(3) - 0.5) / 0.5), NOTCH["SO5"], CYAN, chips=4, contacts=32)
    x.text((160 + sL / 2, y2 - 22), "DDR4 SO-DIMM: 260", "semi", 26, WHITE, ka, anchor="md")
    x.text((680 + sL / 2, y2 - 22), "DDR5 SO-DIMM: 262", "semi", 26, CYAN, ka, anchor="md")
    if ka > 0:
        pr = 26 + 4 * math.sin(x.t * 6)
        x.circle(so4, y2 + sH - 10, pr, AMBER, ka, 4)
        x.circle(so5, y2 + sH - 10, pr, AMBER, ka, 4)
        x.text((660, y2 + sH + 50), "different notches: neither fits the other", "semi", 26, AMBER, ka, anchor="mm")
    # laptop with an open slot
    la = x.b(4)
    if la > 0:
        x.rect([1260, 520, 1800, 860], WHITE, la, 4, r=18, glow=False)
        x.d.rounded_rectangle([1300, 800, 1760, 830], radius=8, fill=col(GRID, la))
        x.rect([1390, 600, 1670, 690], CYAN, la, 3, r=6, fill=PANEL + (255,), glow=False)
        x.text((1530, 645), "DDR5 SO-DIMM slot", "semi", 24, CYAN, la, anchor="mm")
        x.text((1530, 735), "upgrade: same generation only", "semi", 24, GREEN, la, anchor="mm")


# ---------- 10. LPDDR and GDDR ----------
def s_soldered(x):
    a = x.b(0)
    # thin-laptop board, top view
    x.rect([120, 160, 880, 620], MUTED, a, 3, r=16, fill=PANEL + (255,), glow=False)
    x.text((140, 180), "thin laptop board", "semi", 24, MUTED, a)
    cx, cy = 500, 400
    chip_icon(x, cx, cy, 150, WHITE, a, 3)
    x.text((cx, cy), "CPU", "title", 34, WHITE, a, anchor="mm")
    la = x.b(1)
    for k, (px, py) in enumerate([(300, 320), (300, 480), (700, 320), (700, 480)]):
        x.d.rectangle([px - 55, py - 35, px + 55, py + 35], fill=col((20, 24, 26), la))
        x.rect([px - 55, py - 35, px + 55, py + 35], CYAN, la, 2, r=3, glow=False)
        x.line([(px + (55 if px < cx else -55), py), (cx + (-95 if px < cx else 95), py)], AMBER, la, 3, glow=False)
        for j in range(5):
            x.circle(px - 40 + j * 20, py, 4, CYAN, la, 0, fill=CYAN)
    x.text((500, 570), "LPDDR: soldered right beside the CPU", "semi", 26, CYAN, la, anchor="mm")
    ua = x.b(2)
    if ua > 0:
        label_box(x, 500, 650, "no slot = no upgrade", RED, ua, 28)
    ca = x.b(3)
    if ca > 0:
        p = ease(x.since(3) / 1.0)
        mx = lerp(-200, 260, p)
        x.rect([mx, 690, mx + 480, 860], GREEN, ca, 3, r=10, fill=PANEL + (255,), glow=False)
        for j in range(4):
            x.d.rectangle([mx + 30 + j * 85, 725, mx + 95 + j * 85, 790], fill=col((20, 24, 26), ca))
        for (sx_, sy_) in [(mx + 440, 715), (mx + 440, 835)]:
            x.circle(sx_, sy_, 10, GREEN, ca, 3)
        x.text((mx + 240, 830), "LPCAMM2: removable", "semi", 24, GREEN, ca, anchor="mm")
    # graphics card
    ga = x.b(4)
    if ga > 0:
        x.rect([1000, 160, 1800, 620], WHITE, ga, 3, r=16, fill=PANEL + (255,), glow=False)
        x.text((1020, 180), "graphics card", "semi", 24, WHITE, ga)
        gx, gy = 1400, 390
        x.rect([gx - 90, gy - 90, gx + 90, gy + 90], WHITE, ga, 4, r=8, glow=False)
        x.text((gx, gy), "GPU", "title", 40, WHITE, ga, anchor="mm")
    ma = x.b(5)
    if ma > 0:
        gx, gy = 1400, 390
        spots = [(-250, -120), (-250, 0), (-250, 120), (250, -120), (250, 0), (250, 120), (-110, -178), (110, -178)]
        for k, (dx, dy) in enumerate(spots):
            px, py = gx + dx, gy + dy
            x.d.rectangle([px - 48, py - 30, px + 48, py + 30], fill=col((20, 24, 26), ma))
            x.rect([px - 48, py - 30, px + 48, py + 30], AMBER, ma, 2, r=3, glow=False)
            tx, ty = (gx + (90 if dx > 0 else -90), py) if abs(dx) > 200 else (px, gy - 90)
            x.line([(px, py), (tx, ty)], AMBER, ma * 0.6, 3, glow=False)
            ph = (x.t * 1.5 + k * 0.13) % 1
            x.circle(lerp(px, tx, ph), lerp(py, ty, ph), 6, AMBER, ma, 0, fill=AMBER)
        x.text((1400, 580), "GDDR: built for bandwidth", "semi", 26, AMBER, ma, anchor="mm")
    # per-pin speed bars
    b6 = x.b(6)
    b7 = x.b(7)
    bar(x, 1000, 730, 520, 24 / 48 * ease(x.since(6) / 1.0), CYAN, b6, 30, "GDDR6", "up to 24 Gbps/pin")
    if b7 > 0:
        g = ease(x.since(7) / 1.4)
        bar(x, 1000, 830, 520, lerp(32, 48, g) / 48, AMBER, b7, 30, "GDDR7", f"{int(lerp(32, 48, g))} Gbps/pin")
        # signal levels: 2 vs 3
        wx0, wy = 1580, 700
        x.text((wx0, wy), "2 levels", "reg", 20, CYAN, b7, anchor="ld")
        pts2 = []
        for i, v in enumerate([1, 0, 1, 1, 0, 1]):
            pts2 += [(wx0 + i * 38, wy + 50 - v * 36), (wx0 + i * 38 + 38, wy + 50 - v * 36)]
        x.line(pts2, CYAN, b7, 3, glow=False)
        wy2 = 800
        x.text((wx0, wy2), "3 levels", "reg", 20, AMBER, b7, anchor="ld")
        pts3 = []
        for i, v in enumerate([2, 0, 1, 2, 1, 0]):
            pts3 += [(wx0 + i * 38, wy2 + 70 - v * 28), (wx0 + i * 38 + 38, wy2 + 70 - v * 28)]
        x.line(pts3, AMBER, b7, 3, glow=False)


# ---------- 11. back to the stick ----------
def s_decide(x):
    a = x.b(0)
    p = ease(x.since(1) / 1.2) * x.b(1, 0.05)
    sy = lerp(170, 360, p)
    stick(x, 120, sy, 380, 110, a, NOTCH["DDR3"], MUTED, contacts=30, chips=6, label="DDR3")
    ba = x.b(1)
    x.rect([110, 400, 510, 520], MUTED, ba, 3, r=12, glow=False)
    x.text((310, 545), "spare parts box", "semi", 24, MUTED, ba, anchor="mt")
    # spec page
    sa = x.b(2)
    if sa > 0:
        x.rect([700, 150, 1100, 520], WHITE, sa, 3, r=10, fill=PANEL + (255,), glow=False)
        x.text((720, 168), "motherboard specs", "semi", 22, WHITE, sa)
        for j in range(6):
            yy = 230 + j * 46
            if j == 2:
                hl = ease((x.since(2) - 0.6) / 0.5)
                x.d.rounded_rectangle([716, yy - 18, 1084, yy + 22], radius=6, fill=col(GREEN, sa * 0.3 * hl))
                x.text((730, yy + 2), "Memory: DDR5 only", "semi", 26, GREEN, sa, anchor="lm")
            else:
                x.d.rounded_rectangle([730, yy - 6, 730 + [300, 240, 0, 320, 200, 280][j], yy + 8], radius=4, fill=col(MUTED, sa * 0.6))
    ka = x.b(3)
    if ka > 0:
        arrow(x, (1110, 330), (1230, 330), GREEN, ka)
        for j in range(2):
            pj = ease((x.since(3) - j * 0.4) / 1.0)
            stick(x, 1260 + j * 0.0, lerp(150, 170 + j * 140, pj), 520, 110, ka, NOTCH["DDR5"], CYAN, contacts=36, chips=6, pmic=True)
        x.text((1520, 470), "matched kit: 2 sticks", "semi", 26, CYAN, ka, anchor="mm")
        x.text((1520, 510), "then switch on its speed profile", "reg", 24, WHITE, ka, anchor="mm")
    # the family
    fa = x.b(4)
    fam = [("DDR", "desktops"), ("SO-DIMM", "laptops"), ("LPDDR", "soldered, battery life"), ("GDDR", "graphics cards")]
    for i, (nm, sub) in enumerate(fam):
        aa = fa * ease((x.since(5) - i * 0.6) / 0.5) if x.b(5) > 0 else fa * 0.35
        cx = 300 + i * 440
        x.rect([cx - 190, 630, cx + 190, 880], CYAN, max(aa, fa * 0.35), 3, r=16, fill=PANEL + (255,), glow=False)
        ia = max(aa, fa * 0.35)
        if i == 0:
            stick(x, cx - 150, 670, 300, 80, ia, 0.5, WHITE, contacts=24, chips=5)
        elif i == 1:
            stick(x, cx - 80, 670, 160, 80, ia, 0.6, CYAN, contacts=14, chips=3)
        elif i == 2:
            chip_icon(x, cx, 710, 60, WHITE, ia, 2)
            for dx in (-90, 90):
                x.d.rectangle([cx + dx - 30, 690, cx + dx + 30, 730], fill=col(CYAN, ia))
        else:
            gpu_card_icon(x, cx, 710, 90, AMBER, ia)
        x.text((cx, 790), nm, "title", 34, CYAN if i < 3 else AMBER, ia, anchor="mm")
        x.text((cx, 840), sub, "reg", 24, WHITE, ia, anchor="mm")


# ---------- 12. next video ----------
def s_next(x):
    a = x.b(0)
    # a pipeline: widen the RAM pipe, flow still limited by a narrow stage
    stages = [("CPU", 70), ("RAM", 70), ("storage", 22), ("GPU", 70)]
    wide = x.b(1)
    x0, y = 260, 300
    seg = 360
    for i, (nm, h) in enumerate(stages):
        hh = h + (40 * wide if nm == "RAM" else 0)
        c = RED if (nm == "storage" and wide > 0.5) else (GREEN if nm == "RAM" and wide > 0 else CYAN)
        sx = x0 + i * seg
        x.rect([sx, y - hh, sx + seg - 40, y + hh], c, a, 4, r=12, fill=PANEL + (255,), glow=False)
        x.text((sx + (seg - 40) / 2, y + 140), nm, "semi", 30, c, a, anchor="mm")
        if i < 3:
            x.line([(sx + seg - 40, y), (sx + seg, y)], CYAN, a, 6, glow=False)
    # flow dots move at the speed of the narrowest stage
    speed = 160
    for k in range(14):
        px = x0 + ((x.t * speed + k * 103) % (4 * seg - 40))
        x.circle(px, y, 9, AMBER, a, 0, fill=AMBER)
    if wide > 0:
        x.text((x0 + seg + 160, y - 140), "faster RAM", "semi", 26, GREEN, wide, anchor="mm")
        x.text((x0 + 2 * seg + 160, y - 140), "still the slow part", "semi", 26, RED, wide, anchor="mm")
    na = x.b(2)
    x.rect([460, 540, 1460, 790], CYAN, na, 4, r=24, fill=PANEL + (255,), glow=False)
    x.text((960, 590), "NEXT VIDEO", "semi", 26, MUTED, na, anchor="mm")
    x.text((960, 660), "Why your PC is slow", "title", 64, WHITE, na, anchor="mm")
    x.text((960, 735), "and why more RAM usually isn't the fix", "semi", 34, AMBER, na, anchor="mm")
    sa = x.b(3)
    if sa > 0:
        sc = 1 + 0.04 * math.sin(x.t * 5)
        w2 = 210 * sc
        x.d.rounded_rectangle([960 - w2, 835, 960 + w2, 910], radius=38, fill=col(RED, sa))
        x.text((960, 872), "SUBSCRIBE", "title", 40, WHITE, sa, anchor="mm")


SCENES = [("Will it fit?", s_hook), ("What DDR means", s_inside), ("DDR3", s_ddr3), ("DDR4", s_ddr4),
          ("The notch is a key", s_key), ("DDR5", s_ddr5), ("Two subchannels", s_roads),
          ("Power and error correction", s_power), ("Laptops: SO-DIMM", s_laptop),
          ("LPDDR and GDDR", s_soldered), ("Back to the stick", s_decide), ("Up next", s_next)]
