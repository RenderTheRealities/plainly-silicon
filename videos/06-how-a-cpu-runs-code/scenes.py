"""Scenes for video 06: How a CPU Runs Your Code, One Clock Cycle at a Time.

Design language (sunset theme): instructions are rounded "capsules" that travel between
stations; a thin square-wave clock strip ticks along the top of the core scenes; timing
diagrams, a register file, a cache ladder with live latency counters and a forked road
for the branch predictor. No arrow glyphs: arrows are drawn as shapes.
"""
import math
from render import *  # noqa: F401,F403


# ---------- shared helpers for this video ----------
def tw(s, kind, size, x):
    return x.d.textlength(safe(s, kind), font=font(kind, size))


def arrow(x, p0, p1, c, a, w=5, head=20):
    if a <= 0:
        return
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    bx, by = p1[0] - head * math.cos(ang), p1[1] - head * math.sin(ang)
    x.line([p0, (bx, by)], c, a, w)
    pts = [p1, (bx + head * 0.6 * math.sin(ang), by - head * 0.6 * math.cos(ang)),
           (bx - head * 0.6 * math.sin(ang), by + head * 0.6 * math.cos(ang))]
    x.d.polygon(pts, fill=col(c, a))


def capsule(x, cx, cy, s, c, a, size=32, kind="monob", fill=None, pad=26):
    """An instruction / micro-op capsule centered at (cx, cy)."""
    if a <= 0:
        return 0
    w = tw(s, kind, size, x) + pad * 2
    h = size * 1.7
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=h / 2,
           fill=(fill or PANEL) + (255,), glow=False)
    x.text((cx, cy), s, kind, size, c, a, anchor="mm")
    return w


def check(x, cx, cy, s, c, a, w=6):
    if a <= 0:
        return
    x.line([(cx - s * 0.5, cy), (cx - s * 0.15, cy + s * 0.35), (cx + s * 0.55, cy - s * 0.45)], c, a, w)


def clock_strip(x, a, y=128, x0=150, x1=1770, period=0.6, label=True):
    """Thin scrolling square wave; returns the current tick number."""
    if a <= 0:
        return 0
    per_px = 120
    off = (x.t / period) * per_px
    pts = []
    k0 = int(-off // per_px) - 1
    hi, lo = y - 14, y + 14
    for k in range(k0, k0 + int((x1 - x0) / per_px) + 3):
        xs = x0 + k * per_px + off
        pts += [(xs, lo), (xs, hi), (xs + per_px / 2, hi), (xs + per_px / 2, lo)]
    pts = [(clamp(px, x0, x1), py) for px, py in pts]
    x.line(pts, AMBER, a * 0.75, 3, glow=False)
    tick = int(x.t / period)
    if label:
        x.text((x1 + 12, y), f"tick {tick}", "mono", 24, AMBER, a, anchor="lm")
    return tick


def hud(x, cx, cy, value, a, pop=0.0):
    """Game-style score readout."""
    if a <= 0:
        return
    x.rect([cx - 230, cy - 80, cx + 230, cy + 80], CYAN, a, 5, r=28, fill=PANEL + (255,))
    x.text((cx, cy - 46), "SCORE", "semi", 28, MUTED, a, anchor="mm")
    x.text((cx, cy + 18), f"{value:,}", "title", int(78 + 18 * pop), WHITE, a, anchor="mm")


# ---------- scenes ----------
def s_hook(x):
    a0 = x.b(0)
    got = x.since(0) > 2.2
    pop = clamp(1 - (x.since(0) - 2.2) / 0.4) if got else 0
    hud(x, 960, 230, 1250 if got else 1240, a0, pop)
    if 0.8 < x.since(0) < 2.4:
        p = ease((x.since(0) - 0.8) / 1.4)
        capsule(x, 1300 - 120 * p, 260 - 40 * p, "+10", AMBER, a0 * (1 - p * 0.8), 40)
    # tick track
    n, tx0, step, ty = 56, 230, 26, 520
    for i in range(n):
        xx = tx0 + i * step
        c, aa = GRID, a0
        if i == 0 and x.b(0) > 0:
            c = GREEN
        elif x.b(1) > 0 and i < int(clamp(x.since(1) / 2.6) * n):
            c = AMBER
        x.d.rounded_rectangle([xx, ty - 40, xx + 14, ty + 40], radius=5, fill=col(c, aa))
    if x.b(0) > 0:
        pr = (x.t % 1.2) / 1.2
        x.rect([tx0 - 12 - 30 * pr, ty - 52 - 30 * pr, tx0 + 26 + 30 * pr, ty + 52 + 30 * pr], GREEN,
               x.b(0) * (1 - pr) * 0.8, 3, r=10, glow=False)
    x.text((tx0, ty + 80), "best case: 1 tick", "semi", 34, GREEN, x.b(0), anchor="la")
    x.text((tx0, ty + 124), "0.2 nanoseconds", "mono", 28, GREEN, x.b(0), anchor="la")
    wa = x.b(1)
    cnt = int(clamp(x.since(1) / 2.6) * 350)
    x.text((tx0 + n * step - 12, ty - 70), f"waiting... {cnt} ticks", "mono", 34, AMBER, wa, anchor="rd")
    x.text((tx0 + n * step - 12, ty + 80), "worst case: hundreds of ticks", "semi", 34, RED, wa, anchor="ra")
    # the trip ahead: five stations, a capsule hopping along
    ra = x.b(2)
    names = ["fetch", "decode", "execute", "memory", "branch"]
    xs = [360 + i * 300 for i in range(5)]
    x.line([(xs[0], 780), (xs[-1], 780)], MUTED, ra * 0.6, 4, glow=False)
    p = (x.since(2) / 4.0) % 1.0
    for i, (nm, xx) in enumerate(zip(names, xs)):
        lit = ra > 0 and abs(p * 4 - i) < 0.5
        x.circle(xx, 780, 22, CYAN, ra, 4, fill=CYAN if lit else PANEL)
        x.text((xx, 830), nm, "semi", 30, WHITE if lit else MUTED, ra, anchor="mt")
    capsule(x, xs[0] + p * (xs[-1] - xs[0]), 720, "+10", AMBER, ra, 30)


def s_code(x):
    a0 = x.b(0)
    x.rect([140, 180, 820, 420], CYAN, a0, 4, r=22, fill=PANEL + (255,))
    x.text((180, 215), "game code", "semi", 28, MUTED, a0, anchor="lm")
    x.text((180, 310), "score", "monob", 52, WHITE, a0, anchor="lm")
    w1 = tw("score ", "monob", 52, x)
    x.text((180 + w1, 310), "=", "monob", 52, AMBER, a0, anchor="lm")
    w2 = tw("score = ", "monob", 52, x)
    x.text((180 + w2, 310), "score + 10;", "monob", 52, WHITE, a0, anchor="lm")
    x.text((180, 375), "one line, written by a person", "semi", 26, MUTED, a0, anchor="lm")
    na = x.b(1) * (1 - x.b(2))
    label_box(x, 480, 480, "the CPU can't read this", RED, na, 34)
    # compiler arrow
    ca = x.b(2)
    arrow(x, (840, 300), (1000, 300), AMBER, ca, 6)
    x.text((920, 262), "compiler", "semi", 28, AMBER, ca, anchor="md")
    x.rect([1020, 170, 1780, 520], AMBER, ca, 4, r=22, fill=PANEL + (255,))
    x.text((1060, 210), "machine code", "semi", 28, MUTED, ca, anchor="lm")
    rows = [("401A20", "add  [score], 10", 3), ("401A27", "cmp  [score], [high]", 4), ("401A2E", "jg   new_record", 4)]
    pc_a = x.b(5)
    cur = int(x.since(5) / 1.3) % 3 if pc_a > 0 else -1
    for i, (ad, ins, bi) in enumerate(rows):
        ra = x.b(bi) * ease((x.since(bi) - (i - 1) * 0.4 if i else x.since(bi)) / 0.4)
        y = 290 + i * 70
        if i == cur:
            x.rect([1040, y - 30, 1760, y + 30], CYAN, ra, 3, r=12, fill=GRID + (255,), glow=False)
        x.text((1060, y), ad, "mono", 32, MUTED, ra, anchor="lm")
        x.text((1230, y), ins, "monob", 34, CYAN if i == cur else WHITE, ra, anchor="lm")
    # program counter register
    x.rect([1020, 600, 1440, 760], CYAN, pc_a, 5, r=20, fill=PANEL + (255,))
    x.text((1230, 640), "program counter", "semi", 30, MUTED, pc_a, anchor="mm")
    x.text((1230, 705), rows[max(cur, 0)][0], "monob", 56, CYAN, pc_a, anchor="mm")
    if pc_a > 0:
        ty = 290 + max(cur, 0) * 70
        x.line([(1440, 680), (1810, 680), (1810, ty), (1780, ty)], CYAN, pc_a, 4)
        x.d.polygon([(1765, ty), (1785, ty - 12), (1785, ty + 12)], fill=col(CYAN, pc_a))
    # memory strip: instructions live at addresses
    ma = x.b(5)
    x.text((140, 580), "memory", "semi", 28, MUTED, ma, anchor="lm")
    addrs = ["401A18", "401A20", "401A27", "401A2E", "401A34"]
    for i, ad in enumerate(addrs):
        y = 620 + i * 48
        on = (i - 1) == cur
        x.rect([140, y, 820, y + 40], CYAN if on else MUTED, ma, 3, r=8,
               fill=(GRID if on else NAVY) + (255,), glow=False)
        x.text((160, y + 20), ad, "mono", 26, CYAN if on else MUTED, ma, anchor="lm")
        x.text((800, y + 20), "instruction" if 0 < i < 4 else "...", "semi", 24, WHITE if on else MUTED, ma, anchor="rm")


def s_clock(x):
    a0 = x.b(0)
    x0, x1, yc, amp, per = 150, 1770, 370, 80, 220
    off = (x.t * 160) % per
    pts = []
    for k in range(-1, int((x1 - x0) / per) + 2):
        xs = x0 + k * per - off
        pts += [(xs, yc + amp), (xs, yc - amp), (xs + per / 2, yc - amp), (xs + per / 2, yc + amp)]
    pts = [(clamp(px, x0, x1), py) for px, py in pts]
    x.line(pts, AMBER, a0, 6)
    ticks = int(x.t * 160 / per)
    x.line([(960, yc - 130), (960, yc + 120)], WHITE, a0 * 0.5, 2, glow=False)
    x.text((1770, 190), f"tick {ticks:,}", "monob", 34, AMBER, a0, anchor="rm")
    x.text((150, 190), "the clock (slowed down a few billion times)", "semi", 28, MUTED, a0, anchor="lm")
    # one tick bracket
    ba = x.b(2)
    bx0, bx1 = 960 - per / 2, 960 + per / 2
    x.line([(bx0, 500), (bx0, 520), (bx1, 520), (bx1, 500)], CYAN, ba, 4, glow=False)
    x.text((960, 560), "one tick = 0.2 ns", "title", 38, CYAN, ba, anchor="mm")
    # 5 GHz panel
    ga = x.b(1)
    x.text((420, 660), "5 GHz", "title", 110, AMBER, ga, anchor="mm")
    x.text((420, 750), "5,000,000,000 ticks / second", "mono", 30, WHITE, ga, anchor="mm")
    x.text((420, 800), "fastest boost today: ~5.7 GHz", "semi", 28, MUTED, ga, anchor="mm")
    # light ruler
    la = x.b(3)
    rx0, rx1, ry = 1060, 1720, 720
    x.rect([rx0 - 20, ry - 50, rx1 + 20, ry + 50], WHITE, la, 3, r=10, glow=False)
    for i in range(7):
        xx = rx0 + (rx1 - rx0) * i / 6
        x.line([(xx, ry + 50), (xx, ry + 20)], WHITE, la, 3, glow=False)
        x.text((xx, ry + 2), f"{i}", "mono", 24, WHITE, la, anchor="mm")
    p = clamp((x.since(3) % 1.8) / 1.4)
    x.line([(rx0, ry - 28), (rx0 + (rx1 - rx0) * p, ry - 28)], AMBER, la, 6)
    x.circle(rx0 + (rx1 - rx0) * p, ry - 28, 10, AMBER, la, 0, fill=AMBER)
    x.text(((rx0 + rx1) / 2, ry - 80), "how far light gets in one tick: ~6 cm", "semi", 30, WHITE, la, anchor="md")
    sa = x.b(4)
    if sa > 0:
        label_box(x, 1390, 860, "every step has to fit inside these ticks", CYAN, sa, 30)


def s_fetch(x):
    tick = clock_strip(x, x.b(0), period=0.8)
    a0 = x.b(0)
    # program counter
    x.rect([130, 330, 450, 470], CYAN, a0, 5, r=18, fill=PANEL + (255,))
    x.text((290, 365), "program counter", "semi", 26, MUTED, a0, anchor="mm")
    x.text((290, 425), f"401A{0x20 + (tick % 6) * 16:02X}"[:6], "monob", 44, CYAN, a0, anchor="mm")
    # L1 instruction cache grid
    ca = x.b(1)
    gx0, gy0, cw, chh, cols, rows = 580, 250, 40, 52, 16, 9
    x.text((gx0, 205), "L1 instruction cache · 32 KB", "semi", 32, WHITE, ca, anchor="lm")
    cur_row = tick % rows
    palette = [CYAN, AMBER, GREEN, WHITE]
    for r_ in range(rows):
        for c_ in range(cols):
            k = (r_ * 7 + c_ * 3) % 11
            cc = palette[(r_ * 16 + c_) // 5 % 4]
            on = r_ == cur_row and x.b(2) > 0
            x.d.rectangle([gx0 + c_ * cw, gy0 + r_ * chh, gx0 + c_ * cw + cw - 6, gy0 + r_ * chh + chh - 8],
                          fill=col(cc, ca * (0.85 if on else 0.16 + 0.04 * (k % 3))))
    arrow(x, (450, 400), (gx0 - 20, gy0 + cur_row * chh + 22), CYAN, ca, 4)
    # fetch window around current row
    wa = x.b(2)
    if wa > 0:
        yy = gy0 + cur_row * chh
        x.rect([gx0 - 10, yy - 8, gx0 + cols * cw + 4, yy + chh], AMBER, wa, 4, r=8)
        x.text((gx0 + cols * cw + 20, yy + 22), "one chunk", "semi", 26, AMBER, wa, anchor="lm")
    x.text((290, 560), "not one instruction:", "semi", 28, MUTED, wa, anchor="mm")
    x.text((290, 600), "a whole chunk per tick", "semi", 30, AMBER, wa, anchor="mm")
    # fetch queue on the right, chunks stacking
    qa = x.b(3)
    qx0, qx1 = 1420, 1780
    x.rect([qx0, 250, qx1, 718], WHITE, qa, 3, r=16, glow=False)
    x.text(((qx0 + qx1) / 2, 760), "ready to decode", "semi", 30, WHITE, qa, anchor="mm")
    if qa > 0:
        n = 1 + int(x.since(3) / 0.8)
        for i in range(min(n, 7)):
            y = 690 - i * 64
            fr = clamp((x.since(3) - i * 0.8) / 0.4)
            xo = (1 - ease(fr)) * -300
            for j in range(4):
                x.rect([qx0 + 20 + j * 82 + xo, y - 44, qx0 + 92 + j * 82 + xo, y], palette[(i + j) % 4], qa * fr, 3,
                       r=10, fill=GRID + (255,), glow=False)
    # look-ahead dots
    la = x.b(3)
    for k in range(1, 4):
        yy = gy0 + ((cur_row + k) % rows) * chh + 22
        x.circle(gx0 + cols * cw + 40 + k * 14, yy, 5, MUTED, la * (1 - k * 0.25), 0, fill=MUTED)
    x.text((960, 800), "already planning several steps ahead", "semi", 30, MUTED, la, anchor="mm")


def s_decode(x):
    clock_strip(x, x.b(0), period=0.8)
    a1 = x.b(1)
    x.text((140, 200), "instructions come in different lengths", "semi", 28, MUTED, a1, anchor="lm")
    lens = [3, 7, 2, 5]
    for i, L in enumerate(lens):
        y = 250 + i * 64
        aa = a1 * ease((x.since(1) - i * 0.25) / 0.4)
        for j in range(L):
            x.d.rounded_rectangle([140 + j * 46, y, 180 + j * 46, y + 44], radius=6,
                                  fill=col([CYAN, AMBER, GREEN, WHITE][i], aa * 0.8))
        x.text((150 + L * 46, y + 22), f"{L} bytes", "mono", 24, MUTED, aa, anchor="lm")
    # decoder
    da = x.b(0)
    dx0, dx1, dy0, dy1 = 860, 1120, 290, 610
    x.rect([dx0, dy0, dx1, dy1], AMBER, da, 5, r=22, fill=PANEL + (255,))
    x.text(((dx0 + dx1) / 2, dy0 + 50), "DECODER", "title", 40, AMBER, da, anchor="mm")
    for k in range(5):
        yy = dy0 + 110 + k * 40
        x.line([(dx0 + 40, yy), (dx1 - 40, yy)], AMBER, da * 0.35, 3, glow=False)
    # our instruction goes in
    ia = x.b(2)
    p = ease(x.since(2) / 1.6)
    if p < 1:
        capsule(x, 480 + (dx0 + 130 - 480) * p, 600, "add [score], 10", WHITE, ia * (1 - p * 0.9), 32)
    elif x.b(3) == 0:
        x.text(((dx0 + dx1) / 2, 450), "...", "title", 60, AMBER, ia, anchor="mm")
    # three micro-ops come out
    ua = x.b(3)
    ops = [("LOAD  score", CYAN), ("ADD   +10", AMBER), ("STORE score", GREEN)]
    for i, (nm, c) in enumerate(ops):
        f = ease((x.since(3) - i * 0.35) / 0.6)
        y = 340 + i * 110
        xx = dx1 + 40 + 230 * f
        x.line([(dx1, 450), (xx - 150, y)], c, ua * f * 0.6, 3, glow=False)
        capsule(x, xx + 60, y, nm, c, ua * f, 32)
    x.text((1460, 300 - 50), "micro-ops", "semi", 30, WHITE, ua, anchor="mm")
    # micro-op cache
    ma = x.b(4)
    x.rect([860, 690, 1780, 850], GREEN, ma, 4, r=20, fill=PANEL + (255,))
    x.text((890, 720), "micro-op cache", "semi", 28, GREEN, ma, anchor="lm")
    for i in range(10):
        filled = i < 3 or (i < 6 and x.since(4) > 1.5)
        x.rect([890 + i * 86, 750, 960 + i * 86, 830], [CYAN, AMBER, GREEN][i % 3] if filled else MUTED,
               ma * (1 if filled else 0.4), 3, r=10, glow=False)
    if ma > 0:
        lp = ease((x.since(4) % 2.5) / 1.2)
        x.text((620, 770), "next frame:", "semi", 28, MUTED, ma, anchor="mm")
        x.text((620, 810), "skip the decoder", "semi", 30, GREEN, ma, anchor="mm")
        arrow(x, (790, 790), (850, 790), GREEN, ma * lp, 4, 16)


REGS = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp", "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]


def s_execute(x):
    tick = clock_strip(x, x.b(0), period=0.7)
    ra = x.b(1)
    x.rect([130, 180, 830, 860], CYAN, ra, 4, r=22, fill=PANEL + (255,))
    x.text((160, 215), "REGISTERS", "title", 32, CYAN, ra, anchor="lm")
    x.text((800, 215), "16 × 64-bit", "mono", 26, MUTED, x.b(2), anchor="rm")
    loaded = x.since(3) > 1.0 and x.b(3) > 0
    added = x.since(4) > 2.0 and x.b(4) > 0
    for i, nm in enumerate(REGS):
        c_, r_ = divmod(i, 8)
        bx, by = 160 + c_ * 340, 255 + r_ * 74
        if i == 0 and loaded:
            val = "1,250" if added else "1,240"
            hc = AMBER if added else CYAN
            x.rect([bx, by, bx + 320, by + 62], hc, ra, 4, r=12, fill=GRID + (255,))
            x.text((bx + 20, by + 31), nm, "monob", 28, hc, ra, anchor="lm")
            x.text((bx + 300, by + 31), val, "monob", 30, WHITE, ra, anchor="rm")
        else:
            v = (i * 2654435761 + (tick // (1 + i % 3)) * 40503) & 0xFFFFFF
            x.rect([bx, by, bx + 320, by + 62], MUTED, ra * 0.7, 2, r=12, glow=False)
            x.text((bx + 20, by + 31), nm, "monob", 28, MUTED, ra, anchor="lm")
            x.text((bx + 300, by + 31), f"{v:06x}", "mono", 28, MUTED, ra, anchor="rm")
    # load: score flies from memory into rax
    la = x.b(3)
    if la > 0 and not loaded:
        p = ease(x.since(3) / 1.0)
        capsule(x, 1650 + (330 - 1650) * p, 290, "score 1,240", CYAN, la, 28)
    x.text((1650, 240), "from memory", "semi", 26, MUTED, la * (1 - x.b(4)), anchor="mm")
    # ALU
    aa = x.b(4)
    cx, top, bot = 1350, 360, 600
    poly = [(cx - 240, top), (cx - 40, top), (cx, top + 50), (cx + 40, top), (cx + 240, top),
            (cx + 120, bot), (cx - 120, bot)]
    if aa > 0:
        x.d.polygon(poly, fill=col(PANEL, aa), outline=col(AMBER, aa))
        x.line(poly + [poly[0]], AMBER, aa, 5)
        x.text((cx, 500), "ALU", "title", 56, AMBER, aa, anchor="mm")
        p = ease((x.since(4) - 0.3) / 1.0)
        capsule(x, cx - 140, top - 60 - 20 * (1 - p), "1,240", CYAN, aa, 30)
        capsule(x, cx + 140, top - 60 - 20 * (1 - p), "10", WHITE, aa, 30)
        oa = aa * ease((x.since(4) - 1.2) / 0.5)
        capsule(x, cx, bot + 55, "1,250", AMBER, oa, 34)
        if added:
            x.line([(cx - 120, bot + 55), (880, bot + 55), (880, 286), (836, 286)], AMBER, aa * 0.6, 3, glow=False)
    # one cycle, four ALUs
    fa = x.b(5)
    label_box(x, 1700, 480, "1 cycle", GREEN, fa, 32)
    x.text((1350, 750), "Zen 4: four ALUs, four adds per tick", "semi", 30, WHITE, fa, anchor="mm")
    for k in range(4):
        lit = (tick + k) % 2 == 0
        kx = 1050 + k * 160
        x.rect([kx, 790, kx + 120, 850], AMBER, fa, 3, r=12, fill=(AMBER if lit else PANEL) + (255,) if lit else PANEL + (255,), glow=False)
        x.text((kx + 60, 820), "+", "title", 40, NAVY if lit else AMBER, fa, anchor="mm")


STAGES = ["Fetch", "Decode", "Execute", "Retire"]
ICOL = [CYAN, AMBER, GREEN, WHITE, CYAN, AMBER, GREEN]


def s_pipeline(x):
    # top: one-at-a-time strip
    sa = x.b(1)
    x.text((160, 170), "one at a time", "semi", 28, MUTED, sa, anchor="lm")
    for i in range(12):
        k, s = divmod(i, 3)
        xx = 400 + i * 100
        fill_on = sa > 0 and x.since(1) * 3 > i
        x.rect([xx, 145, xx + 88, 195], ICOL[k], sa, 3, r=10,
               fill=(GRID if fill_on else NAVY) + (255,), glow=False)
        if fill_on:
            x.text((xx + 44, 170), "FDE"[s], "monob", 26, ICOL[k], sa, anchor="mm")
    x.text((1610, 170), "1 done / 3 ticks", "mono", 26, RED, sa, anchor="lm")
    # main pipeline diagram
    pa = x.b(2)
    gx0, gy0, cw, rh, ncol = 420, 300, 132, 120, 10
    cyc = x.since(2) / 0.7 if pa > 0 else 0
    for s, nm in enumerate(STAGES):
        y = gy0 + s * rh
        x.text((380, y + rh / 2), nm, "semi", 34, WHITE, pa, anchor="rm")
        x.line([(gx0, y), (gx0 + cw * ncol, y)], GRID, pa, 2, glow=False)
    x.line([(gx0, gy0 + 4 * rh), (gx0 + cw * ncol, gy0 + 4 * rh)], GRID, pa, 2, glow=False)
    for c_ in range(ncol):
        x.text((gx0 + c_ * cw + cw / 2, gy0 - 24), f"{c_ + 1}", "mono", 26, MUTED, pa, anchor="mm")
    cur = int(cyc)
    if pa > 0 and cur < ncol:
        x.rect([gx0 + cur * cw, gy0 - 8, gx0 + (cur + 1) * cw, gy0 + 4 * rh + 8], AMBER, pa * 0.8, 3, r=10, glow=False)
    done = 0
    for k in range(7):
        for s in range(4):
            c_ = k + s
            if c_ >= ncol or c_ > cur:
                continue
            fr = clamp(cyc - c_) if c_ == cur else 1
            xx, yy = gx0 + c_ * cw, gy0 + s * rh
            name = "add" if k == 2 else f"i{k + 1}"
            x.rect([xx + 8, yy + 14, xx + cw - 8, yy + rh - 14], ICOL[k], pa * (0.4 + 0.6 * fr), 4, r=40,
                   fill=PANEL + (255,), glow=(c_ == cur))
            x.text((xx + cw / 2, yy + rh / 2), name, "monob", 30, ICOL[k], pa * (0.4 + 0.6 * fr), anchor="mm")
            if s == 3:
                done += 1
    x.text((gx0, gy0 + 4 * rh + 30), "clock cycle", "semi", 26, MUTED, pa, anchor="lt")
    # annotation on current column
    na = x.b(3) * (1 - x.b(4))
    label_box(x, 1090, 860, "every stage busy with a different instruction", AMBER, na, 32)
    fa = x.b(4)
    label_box(x, 1440, 860, f"finished: {done}  ·  one every tick", GREEN, fa, 34)


def s_ooo(x):
    a0 = x.b(0)
    x.text((140, 160), "program order", "semi", 30, MUTED, a0, anchor="lm")
    items = [("1", "LOAD score", CYAN), ("2", "ADD +10", AMBER), ("3", "move character", WHITE),
             ("4", "play sound", WHITE), ("5", "update timer", WHITE)]
    waiting = x.b(1)
    moved = x.b(2)
    for i, (n, nm, c) in enumerate(items):
        y = 210 + i * 104
        dim = 1.0
        if i == 1 and waiting > 0 and x.b(4) == 0:
            dim = 0.45
        x.rect([140, y, 690, y + 86], c, a0 * dim, 4, r=43, fill=PANEL + (255,), glow=False)
        x.text((190, y + 43), n, "monob", 32, MUTED, a0 * dim, anchor="mm")
        x.text((240, y + 43), nm, "semi", 32, c, a0 * dim, anchor="lm")
        if i == 0 and waiting > 0 and x.b(4) == 0:
            ang = x.t * 5
            for k in range(8):
                aa = 0.2 + 0.8 * ((k - ang) % 8) / 8
                x.circle(640 + 18 * math.cos(k * math.pi / 4), y + 43 + 18 * math.sin(k * math.pi / 4), 4, RED, waiting * aa, 0, fill=RED)
    x.text((415, 740), "load waits for memory", "semi", 28, RED, waiting * (1 - x.b(4)), anchor="mm")
    if waiting > 0:
        x.line([(170, 296), (170, 314)], AMBER, waiting * 0.6 * (1 - x.b(4)), 3, glow=False)
    # execution lane
    ex0, ex1 = 800, 1260
    x.rect([ex0, 210, ex1, 610], GREEN, moved, 4, r=22, fill=PANEL + (255,))
    x.text(((ex0 + ex1) / 2, 160), "running now", "semi", 30, GREEN, moved, anchor="mm")
    for j, i in enumerate([2, 3, 4]):
        f = ease((x.since(2) - j * 0.4) / 0.7)
        sy = 210 + i * 104 + 43
        ty = 290 + j * 110
        cx = 415 + ((ex0 + ex1) / 2 - 415) * f
        cy = sy + (ty - sy) * f
        if moved > 0 and f > 0:
            capsule(x, cx, cy, items[i][1], GREEN, moved * f, 28, kind="semi")
    # reorder buffer bars
    rb = x.b(3)
    x.text((800, 680), "reorder buffer: micro-ops in flight", "semi", 30, WHITE, rb, anchor="lm")
    full = 800
    for k, (nm, n) in enumerate([("Zen 4", 320), ("Zen 5", 448)]):
        y = 720 + k * 70
        wd = full * n / 448
        segs = 40 if k == 0 else 56
        fillp = ease((x.since(3) - k * 0.4) / 1.2)
        for s in range(segs):
            sx = 800 + s * (wd / segs)
            on = s < segs * fillp
            x.d.rectangle([sx, y, sx + wd / segs - 3, y + 44], fill=col(CYAN if on else GRID, rb))
        x.text((800 + wd + 16, y + 22), f"{nm}: {n}", "monob", 28, CYAN, rb * fillp, anchor="lm")
    # retire in order
    ta = x.b(4)
    rx0, rx1 = 1330, 1780
    x.rect([rx0, 210, rx1, 610], AMBER, ta, 4, r=22, fill=PANEL + (255,))
    x.text(((rx0 + rx1) / 2, 160), "retired in order", "semi", 30, AMBER, ta, anchor="mm")
    for i in range(5):
        f = ease((x.since(4) - i * 0.35) / 0.4)
        cx, cy = rx0 + 70 + (i % 3) * 150, 300 + (i // 3) * 170
        x.circle(cx, cy, 48, AMBER, ta * f, 4, fill=PANEL)
        x.text((cx, cy), str(i + 1), "title", 44, AMBER, ta * f, anchor="mm")
        check(x, cx + 50, cy + 45, 30, GREEN, ta * f, 5)


def s_cache(x):
    rungs = [("Registers", "", 0, 0), ("L1 data", "32 KB", 4, 1), ("L2", "1 MB", 14, 2),
             ("L3 (shared)", "32 MB", 50, 3), ("RAM", "16-32 GB", 350, 4)]
    cx = 640
    a0 = x.b(0)
    for i, (nm, sz, cyc, bi) in enumerate(rungs):
        y = 200 + i * 140
        wd = 200 + i * 100
        if i:
            x.line([(cx, y - 44), (cx, y)], MUTED, (a0 if i == 0 else x.b(bi)) * 0.7, 4, glow=False)
        ra = a0 if i == 0 else x.b(bi)
        c = [CYAN, CYAN, AMBER, AMBER, RED][i]
        x.rect([cx - wd, y, cx + wd, y + 96], c, ra, 4, r=20, fill=PANEL + (255,))
        x.text((cx - wd + 30, y + 48), nm, "title", 36, c, ra, anchor="lm")
        x.text((cx + wd - 30, y + 48), sz, "mono", 28, WHITE, ra, anchor="rm")
    # the request token drops down rung by rung
    lvl = 0
    for i in range(1, 5):
        if x.b(i) > 0:
            lvl = i
    prog = x.b(lvl, 0.8) if lvl else 1
    y_from = 200 + max(lvl - 1, 0) * 140 + 48
    y_to = 200 + lvl * 140 + 48
    ty = y_from + (y_to - y_from) * prog
    if lvl and x.b(5) == 0:
        wx0, wx1 = 200 + max(lvl - 1, 0) * 100, 200 + lvl * 100
        capsule(x, cx + 0.4 * (wx0 + (wx1 - wx0) * prog), ty, "score?", WHITE, 1.0, 26, kind="semi", pad=18)
    # live counter + bars
    pa = x.b(1)
    x.text((1250, 190), "wait, in clock cycles", "semi", 30, MUTED, pa, anchor="lm")
    for i in range(1, 5):
        nm, sz, cyc, bi = rungs[i]
        ba = x.b(bi)
        y = 260 + (i - 1) * 130
        f = ease(x.since(bi) / 1.2)
        val = int(round(cyc * f))
        c = [CYAN, CYAN, AMBER, AMBER, RED][i]
        bar(x, 1250, y + 30, 530, f * cyc / 350, c, ba, 34, nm, f"~{val}" if i == 4 else f"{val}")
    na = x.b(4)
    x.text((1780, 735), "≈ 70 ns at 5 GHz", "semi", 28, RED, na, anchor="ra")
    ga = x.b(5)
    label_box(x, 1515, 835, "bigger cache, fewer long trips", GREEN, ga, 32)


def s_branch(x):
    a0 = x.b(0)
    fx, fy = 760, 470
    up, dn = (1560, 260), (1560, 680)
    road = [(140, fy), (fx, fy)]
    for path in (road, [(fx, fy), up], [(fx, fy), dn]):
        x.line(path, GRID, a0, 70, glow=False)
        x.line(path, MUTED, a0 * 0.5, 3, glow=False)
    x.text((up[0], up[1] - 60), "new high score!", "semi", 32, AMBER, a0, anchor="md")
    x.text((dn[0], dn[1] + 60), "keep playing", "semi", 32, WHITE, a0, anchor="mt")
    x.text((300, fy - 60), "cmp score, high", "monob", 30, WHITE, a0, anchor="md")
    # predictor
    pa = x.b(1)
    x.rect([140, 600, 660, 840], CYAN, pa, 4, r=22, fill=PANEL + (255,))
    x.text((170, 635), "branch predictor", "semi", 30, CYAN, pa, anchor="lm")
    x.text((170, 690), "last 8 times:", "semi", 26, MUTED, pa, anchor="lm")
    for k in range(8):
        x.circle(372 + k * 34, 690, 12, MUTED, pa, 0, fill=MUTED)
    x.text((170, 760), "guess: keep playing", "semi", 32, WHITE, pa, anchor="lm")
    wrong = x.b(4)
    flush_t = x.since(4)

    def flow(dest, c, a, phase=0.0):
        for k in range(5):
            p = ((x.t * 0.45 + k / 5 + phase) % 1.0)
            px, py = fx + (dest[0] - fx) * p, fy + (dest[1] - fy) * p
            x.rect([px - 40, py - 20, px + 40, py + 20], c, a, 3, r=20, fill=PANEL + (255,), glow=False)

    sa = x.b(2)
    if wrong == 0:
        flow(dn, CYAN, sa)
    else:
        if flush_t < 1.0:
            flow(dn, RED, sa * (1 - flush_t))
            stamp(x, 1180, 600, "FLUSH", RED, ease(flush_t / 0.3))
        else:
            fa = ease((flush_t - 1.0) / 0.4)
            flow(up, GREEN, fa)
    ca = x.b(3) * (1 - x.b(4, 0.2))
    check(x, 1200, 610, 60, GREEN, ca, 8)
    x.text((1260, 600), "right: no time lost", "semi", 30, GREEN, ca, anchor="lm")
    # penalty meter
    ma = x.b(5)
    x.text((800, 790), "penalty: ~15-20 cycles", "semi", 30, RED, ma, anchor="lm")
    for k in range(20):
        on = k < int(clamp(x.since(5) / 1.6) * 18)
        x.rect([800 + k * 48, 820, 838 + k * 48, 860], RED, ma, 3, r=8,
               fill=(RED if on else PANEL) + (255,), glow=False)


def s_ipc(x):
    a0 = x.b(0)
    # formula row
    parts = [("ticks per second", AMBER), ("×", WHITE), ("work per tick (IPC)", CYAN), ("=", WHITE), ("speed", GREEN)]
    tot = sum(tw(p, "title", 44, x) for p, _ in parts) + 40 * (len(parts) - 1)
    xx = 960 - tot / 2
    for i, (p, c) in enumerate(parts):
        aa = a0 if i not in (0,) else max(a0, x.b(1))
        if i == 0:
            aa = x.b(1) if x.b(1) > 0 else a0 * 0.5
        if i == 2:
            aa = x.b(2) if x.b(2) > 0 else a0 * 0.5
        x.text((xx, 210), p, "title", 44, c, aa, anchor="lm")
        xx += tw(p, "title", 44, x) + 40
    # issue-slot grid: 14 ticks x 8 slots
    ga = x.b(2)
    gx0, gy0, cw, sh, nt = 260, 320, 66, 50, 14
    real = x.b(4) > 0
    pattern = [6, 3, 0, 0, 0, 4, 2, 5, 0, 0, 3, 7, 2, 4]
    x.text((gx0, gy0 - 30), "8 slots per tick (Zen 5)", "semi", 28, MUTED, ga, anchor="lm")
    for t in range(nt):
        n_fill = 8 if not real else pattern[t]
        appear = ease((x.since(3 if not real else 4) - t * 0.08) / 0.3) if x.b(3) > 0 else 0
        for s in range(8):
            y = gy0 + (7 - s) * sh
            on = s < n_fill and appear > 0
            c = GREEN if not real else CYAN
            x.d.rounded_rectangle([gx0 + t * cw, y, gx0 + t * cw + cw - 10, y + sh - 10], radius=8,
                                  fill=col(c if on else GRID, ga * (appear if on else 1)))
    x.text((gx0 + nt * cw / 2, gy0 + 8 * sh + 30), "clock ticks", "semi", 26, MUTED, ga, anchor="mt")
    ma = x.b(3) * (1 - x.b(4))
    label_box(x, gx0 + nt * cw / 2, gy0 + 8 * sh + 100, "maximum: every slot full", GREEN, ma, 32)
    ra = x.b(4)
    if ra > 0:
        x.text((gx0 + 3.5 * cw, gy0 + 4 * sh), "cache", "semi", 26, RED, ra, anchor="mm")
        x.text((gx0 + 3.5 * cw, gy0 + 4 * sh + 34), "miss", "semi", 26, RED, ra, anchor="mm")
        x.text((gx0 + 9 * cw - 5, gy0 + 4 * sh), "wrong", "semi", 26, RED, ra, anchor="mm")
        x.text((gx0 + 9 * cw - 5, gy0 + 4 * sh + 34), "guess", "semi", 26, RED, ra, anchor="mm")
        label_box(x, gx0 + nt * cw / 2, gy0 + 8 * sh + 100, "in games: far below the maximum", CYAN, ra, 32)
    # two chips, same GHz
    ca = x.b(4)
    for k, (nm, perf, c) in enumerate([("Chip A", 0.55, MUTED), ("Chip B", 0.9, GREEN)]):
        y = 360 + k * 220
        chip_icon(x, 1340, y + 40, 100, c, ca, 3, pins=3)
        x.text((1340, y + 40), "5 GHz", "semi", 22, c, ca, anchor="mm")
        bar(x, 1430, y + 40, 340, perf * ease(x.since(4) / 1.2), c, ca, 34, nm, "")
    x.text((1600, 820), "same GHz, different speed", "semi", 28, WHITE, ca, anchor="mm")


def s_replay(x):
    a0 = x.b(0)
    stations = ["fetch", "decode", "register", "ALU +10", "store", "predict"]
    xs = [230 + i * 292 for i in range(6)]
    y = 520
    t0, t1 = x.beats[1], x.beats[min(2, len(x.beats) - 1)]
    p = clamp((x.t - t0) / max(0.1, (t1 - t0) - 0.3))
    pos = p * 5
    x.line([(xs[0], y), (xs[-1], y)], MUTED, a0 * 0.5, 6, glow=False)
    for i, (nm, xx) in enumerate(zip(stations, xs)):
        lit = x.b(1) > 0 and pos >= i - 0.05
        c = CYAN if lit else MUTED
        x.circle(xx, y, 62, c, a0, 5, fill=GRID if lit else PANEL)
        x.text((xx, y), f"{i + 1}", "title", 44, c, a0, anchor="mm")
        x.text((xx, y + 100), nm, "semi", 32, WHITE if lit else MUTED, a0, anchor="mm")
    if x.b(1) > 0:
        capsule(x, xs[0] + (xs[-1] - xs[0]) * p, y - 110, "+10", AMBER, x.b(1), 34)
    hud(x, 960, 230, 1250 if pos >= 4 else 1240, a0, clamp(1 - abs(pos - 4.2) * 3) if pos >= 4 else 0)
    if x.b(1) > 0:
        for k in range(6):
            yy = y + 170 + (k % 2) * 30
            px = ((x.t * 0.4 + k / 6) % 1.0)
            x.rect([xs[0] + (xs[-1] - xs[0]) * px - 26, yy - 10, xs[0] + (xs[-1] - xs[0]) * px + 26, yy + 10],
                   MUTED, x.b(1) * 0.6, 2, r=10, glow=False)
        x.text((960, y + 230), "overlapped with dozens of other instructions", "semi", 28, MUTED, x.b(1) * 0.9, anchor="mm")
    fa = x.b(2)
    x.text((960, 820), "a few nanoseconds", "title", 64, AMBER, fa, anchor="mm")
    ba = x.b(3)
    if ba > 0:
        label_box(x, 1580, 230, "billions per second", CYAN, ba, 32)


def s_outro(x):
    a = x.b(0)
    x.text((960, 190), "Up next", "semi", 40, MUTED, a, anchor="mm")
    ca = x.b(1)
    x.rect([360, 260, 1560, 700], CYAN, ca, 5, r=30, fill=PANEL + (255,))
    # price tag illustration
    tx, ty = 560, 480
    tag = [(tx - 120, ty - 90), (tx + 70, ty - 90), (tx + 140, ty), (tx + 70, ty + 90), (tx - 120, ty + 90)]
    if ca > 0:
        x.d.polygon(tag, fill=col(GRID, ca))
        x.line(tag + [tag[0]], AMBER, ca, 5)
        x.circle(tx + 70, ty, 14, AMBER, ca, 4)
        x.text((tx - 30, ty - 30), "$199", "title", 40, MUTED, ca, anchor="mm")
        x.line([(tx - 90, ty - 30), (tx + 30, ty - 30)], RED, ca, 5, glow=False)
        x.text((tx - 30, ty + 35), "$149?", "title", 46, AMBER, ca, anchor="mm")
    x.text((1130, 420), "7 Black Friday", "title", 66, WHITE, ca, anchor="mm")
    x.text((1130, 500), "PC Part Traps", "title", 66, WHITE, ca, anchor="mm")
    x.text((1130, 590), "and how to spot a real deal", "semi", 36, AMBER, ca, anchor="mm")
    sa = x.b(2)
    x.rect([760, 770, 1160, 860], RED, sa, 0, r=45, fill=RED + (255,), glow=False)
    x.text((960, 815), "SUBSCRIBE", "title", 44, WHITE, sa, anchor="mm")


SCENES = [("Ten points, one core", s_hook),
          ("From code to instructions", s_code),
          ("The clock", s_clock),
          ("Fetch", s_fetch),
          ("Decode into micro-ops", s_decode),
          ("Registers and the ALU", s_execute),
          ("Pipelining", s_pipeline),
          ("Out-of-order execution", s_ooo),
          ("The cache ladder", s_cache),
          ("Branch prediction", s_branch),
          ("IPC: work per tick", s_ipc),
          ("The ten points, replayed", s_replay),
          ("Up next", s_outro)]
