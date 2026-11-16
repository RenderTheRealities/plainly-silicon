"""Short 07s2: two different graphics cards sold under one name, RTX 3050 6 GB vs 8 GB (vertical, lab theme).
Spec-sheet / lab-bench look: card silhouettes with spinning fans, core dot grids, bus lanes, readout counters."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def card(x, cx, cy, w, h, c, a, label="", spin=0.0, fans=2):
    """Side view of a graphics card: shroud, fans, gold-finger PCIe tab."""
    if a <= 0:
        return
    x0, y0, x1, y1 = cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2
    x.rect([x0, y0, x1, y1], c, a, 5, r=18, fill=PANEL + (255,))
    fr = min(h * 0.36, w / (fans * 2.6))
    for k in range(fans):
        fx = x0 + w * (k + 0.5) / fans
        x.circle(fx, cy - 6, fr, c, a, 4)
        for s in range(5):
            ang = spin + s * 2 * math.pi / 5
            x.line([(fx, cy - 6), (fx + fr * 0.85 * math.cos(ang), cy - 6 + fr * 0.85 * math.sin(ang))], c, a, 4)
        x.circle(fx, cy - 6, fr * 0.18, c, a, 0, fill=c)
    # PCIe fingers
    for k in range(9):
        gx = x0 + w * 0.22 + k * w * 0.05
        x.rect([gx, y1, gx + w * 0.03, y1 + 22], AMBER if False else MUTED, a, 2, r=2, fill=MUTED, glow=False)
    if label:
        x.text((cx, y0 - 26), label, "title", 48, WHITE, a, anchor="md")


def core_grid(x, top, n_on, c, a, total=80, fade_from=None, prog=1.0):
    """80 dots, one per 32 CUDA cores. Dots past n_on are switched off (hollow, gray)."""
    cols = 10
    for i in range(total):
        r_, k = divmod(i, cols)
        px, py = 270 + k * 60, top + r_ * 46
        shown = i < total * prog
        if not shown:
            continue
        if i < n_on:
            x.circle(px, py, 16, c, a, 0, fill=c)
        else:
            x.circle(px, py, 16, MUTED, a, 3)
            x.line([(px - 12, py + 12), (px + 12, py - 12)], RED, a, 3, glow=False)


def lanes(x, top, n_on, c, a, t, total=16):
    """Memory bus: one lane per 8 bits, data packets flowing from GPU (left) to memory (right)."""
    chip_icon(x, 190, top + 95, 120, c, a, 4, 3)
    x.text((190, top + 95), "GPU", "title", 34, c, a, anchor="mm")
    x.rect([840, top + 10, 950, top + 180], c, a, 4, r=8, fill=PANEL + (255,), glow=False)
    x.text((895, top + 95), "VRAM", "semi", 26, c, a, anchor="mm")
    for i in range(total):
        y = top + 18 + i * 10.5
        on = i < n_on
        x.line([(270, y), (830, y)], c if on else GRID, a, 3 if on else 2, glow=False)
        if on:
            for k in range(3):
                p = (t * 0.6 + k / 3 + i * 0.07) % 1
                px = 270 + 560 * p
                x.rect([px - 9, y - 4, px + 9, y + 4], c, a, 1, r=3, fill=c, glow=False)


def readout(x, cx, cy, value, unit, c, a, size=96):
    x.text((cx, cy), f"{value}", "title", size, c, a, anchor="rm")
    x.text((cx + 16, cy + size * 0.18), unit, "semi", 44, MUTED, a, anchor="lm")


# ---------- 1: same name ----------
def s_hook(x):
    a = x.b(0)
    sp = x.t * 4
    for i, cx in enumerate((290, 790)):
        ai = ease((x.t - 0.3 * i) / 0.5)
        card(x, cx, 640, 400, 190, CYAN if i == 0 else AMBER, ai, "RTX 3050", spin=sp * (1 if i == 0 else 0.8))
    # an equals sign that gets struck through
    q = ease((x.t - 1.2) / 0.4)
    x.line([(512, 628), (568, 628)], WHITE, q, 6, glow=False)
    x.line([(512, 652), (568, 652)], WHITE, q, 6, glow=False)
    s = ease((x.t - 3.2) / 0.4)
    x.line([(522, 680), (558, 600)], RED, s, 7, glow=False)
    # labels under cards
    k = ease((x.t - 3.6) / 0.5)
    x.text((290, 840), "8 GB", "title", 64, CYAN, k, anchor="mm")
    x.text((790, 840), "6 GB", "title", 64, AMBER, k, anchor="mm")
    if x.t > 4.4:
        stamp(x, 790, 1060, "SLOWER", RED, ease((x.t - 4.4) / 0.35), angle=-7)


# ---------- 2: the 8 GB card ----------
def s_eight(x):
    a = x.b(0)
    x.text((CX, 430), "RTX 3050  8 GB", "title", 52, CYAN, a, anchor="mm")
    p = clamp(x.since(0) / 2.2)
    core_grid(x, 500, 80, CYAN, a, prog=p)
    x.text((CX, 900), f"{int(2560 * ease(p)):,} CUDA cores", "semi", 46, WHITE, a, anchor="mm")
    b = x.b(1)
    lanes(x, 960, 16, CYAN, b, x.t)
    x.text((CX, 1185), "128-bit bus", "semi", 36, MUTED, b, anchor="mm")
    readout(x, 640, 1240, int(224 * ease(x.since(1) / 1.2)) if b > 0 else 0, "GB/s", CYAN, b, 64)


# ---------- 3: the 6 GB card ----------
def s_six(x):
    a = x.b(0)
    x.text((CX, 430), "RTX 3050  6 GB", "title", 52, AMBER, a, anchor="mm")
    cut = ease((x.since(0) - 1.0) / 1.5)
    n_on = 80 - int(round(8 * cut))
    core_grid(x, 500, n_on, AMBER, a)
    x.text((CX, 900), f"{2560 - int(256 * cut):,} CUDA cores", "semi", 46, WHITE, a, anchor="mm")
    lc = ease((x.since(0) - 3.5) / 1.2)
    nl = 16 - int(round(4 * lc))
    lanes(x, 960, nl, AMBER, a, x.t)
    x.text((CX, 1185), f"{128 - int(32 * lc)}-bit bus", "semi", 36, MUTED, a, anchor="mm")
    bw = 224 - int(56 * ease((x.since(0) - 5.5) / 1.5))
    readout(x, 640, 1240, bw, "GB/s", AMBER if bw < 224 else CYAN, a, 64)
    b = x.b(1)
    if b > 0:
        # overlay: two dies to scale-ish
        x.rect([110, 470, 970, 862], WHITE, b, 3, r=20, fill=PANEL + (255,), glow=False)
        x.text((CX, 560), "a different, smaller chip", "semi", 40, WHITE, b, anchor="mm")
        chip_icon(x, 340, 740, 190, CYAN, b, 5, 5)
        x.text((340, 740), "GA106", "title", 38, CYAN, b, anchor="mm")
        s = 0.72
        chip_icon(x, 740, 740, 190 * s, AMBER, b, 5, 4)
        x.text((740, 740), "GA107", "title", 30, AMBER, b, anchor="mm")


# ---------- 4: power and the result ----------
def s_power(x):
    a = x.b(0)
    for i, (w, c, nm) in enumerate(((130, CYAN, "8 GB"), (70, AMBER, "6 GB"))):
        cx = 360 + i * 360
        bot, hmax = 860, 400
        x.rect([cx - 80, bot - hmax, cx + 80, bot], MUTED, a, 3, r=14, glow=False)
        f = ease((x.since(0) - 0.3) / 1.4) * w / 130
        if f > 0.01:
            x.rect([cx - 72, bot - 8 - (hmax - 16) * f, cx + 72, bot - 8], c, a, 0, r=10, fill=c, glow=False)
        x.text((cx, bot - 8 - (hmax - 16) * f - 40), f"{int(w * ease((x.since(0) - 0.3) / 1.4))} W", "title", 56, c, a, anchor="mm")
        x.text((cx, bot + 40), nm, "semi", 38, WHITE, a, anchor="mm")
    b = x.b(1)
    p = ease(x.since(1) / 1.2)
    x.text((150, 1000), "performance", "semi", 36, MUTED, b, anchor="lm")
    bar(x, 150, 1040, 780, p, CYAN, b, h=50)
    bar(x, 150, 1130, 780, p * 0.8, AMBER, b, h=50)
    x.text((160, 1065), "8 GB", "semi", 30, PANEL, b if p > 0.2 else 0, anchor="lm")
    x.text((160, 1155), "6 GB", "semi", 30, PANEL, b if p > 0.2 else 0, anchor="lm")
    x.text((930, 1230), "~20% behind", "title", 44, RED, ease((x.since(1) - 1.3) / 0.4), anchor="rm")


# ---------- 5: how to spot it ----------
def s_spot(x):
    a = x.b(0)
    x.rect([90, 430, 990, 760], WHITE, a, 3, r=16, fill=PANEL + (255,), glow=False)
    x.rect([90, 430, 990, 480], WHITE, a, 0, r=16, fill=GRID, glow=False)
    for k in range(3):
        x.circle(125 + k * 32, 455, 9, MUTED, a, 0, fill=MUTED)
    words = ["GeForce", "RTX", "3050", "6G", "OC", "Low", "Profile", "Gaming", "Graphics", "Card"]
    f = font("semi", 46)
    px, py = 130, 540
    hit = None
    for w_ in words:
        tw = x.d.textlength(w_, font=f)
        if px + tw > 960:
            px, py = 130, py + 70
        if w_ == "6G":
            hit = (px, py, tw)
        x.text((px, py), w_, "semi", 46, WHITE, a, anchor="lm")
        px += tw + 18
    # magnifier sweeps then lands on "6G"
    hx, hy, tw = hit
    land = ease((x.since(0) - 1.5) / 1.2)
    mx = 200 + (hx + tw / 2 - 200) * land + (1 - land) * 120 * math.sin(x.t * 2.5)
    my = 640 + (hy - 640) * land
    if land > 0.95:
        x.rect([hx - 10, hy - 34, hx + tw + 10, hy + 34], RED, a, 5, r=8, glow=False)
    x.circle(mx, my, 70, CYAN, a, 6)
    x.line([(mx + 50, my + 50), (mx + 110, my + 110)], CYAN, a, 12, glow=False)
    b = x.b(1)
    for i, s in enumerate(("Read the full model name", "Check that exact name on the maker's spec page")):
        bi = ease((x.since(1) - 0.2 - i * 1.6) / 0.5) if b > 0 else 0
        y = 900 + i * 150
        x.circle(150, y, 34, GREEN, bi, 0, fill=GREEN)
        x.line([(134, y), (146, y + 14), (168, y - 14)], PANEL, bi, 7, glow=False)
        lines = wrap(s, font("semi", 42), 760, x.d)
        for k, l in enumerate(lines):
            x.text((210, y - 22 * (len(lines) - 1) + k * 48), l, "semi", 42, WHITE, bi, anchor="lm")


# ---------- 6: the full video ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 480, 940, 930], WHITE, a, 4, r=20, fill=PANEL + (255,), glow=False)
    x.text((CX, 560), "FULL VIDEO", "semi", 34, MUTED, a, anchor="mm")
    x.text((CX, 650), "7 Black Friday", "title", 68, WHITE, a, anchor="mm")
    x.text((CX, 730), "PC Part Traps", "title", 68, WHITE, a, anchor="mm")
    for k in range(7):
        ak = ease((x.t - 0.4 - k * 0.18) / 0.3)
        cx = 240 + k * 100
        x.circle(cx, 840, 30, AMBER if k == 1 else CYAN, ak, 4, fill=(AMBER if k == 1 else None))
        x.text((cx, 840), str(k + 1), "title", 32, PANEL if k == 1 else CYAN, ak, anchor="mm")
    x.text((CX, 1040), "trap 2 of 7: same name, different chip", "semi", 38, AMBER, ease((x.t - 1.8) / 0.5), anchor="mm")


SCENES = [
    ("Same name, two cards", s_hook),
    ("The 8 GB RTX 3050", s_eight),
    ("The 6 GB RTX 3050", s_six),
    ("Power and speed", s_power),
    ("How to spot it", s_spot),
    ("The other six traps", s_end),
]
