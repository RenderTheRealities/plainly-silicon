"""Scenes for video 11: Why VRAM Suddenly Matters So Much.

Design language (graphite theme): an editorial print layout. Thin ruled lines, big serif
numerals, small-caps captions. VRAM is a suitcase drawn as a memory map: a grid of 64 tiles
(each 128 MB of an 8 GB card) that fills with hatched or solid blocks per data type. Bandwidth
is drawn as horizontal pipes whose thickness is to scale. Frame pacing is a frame-time strip
chart. Only the red accent (AMBER/RED) marks trouble; GREEN marks the good outcome.
"""
import math
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def rule(x, x0, x1, y, a, c=None, w=2):
    x.line([(x0, y), (x1, y)], c or MUTED, a, w, glow=False)


def caption(x, xy, s, a, c=None, size=26, anchor="la"):
    """Letter-spaced small caps caption."""
    x.text(xy, " ".join(s.upper()), "semi", size, c or MUTED, a, anchor=anchor)


def hatch(x, box, c, a, step=12, w=2):
    """Diagonal hatch inside a box (clipped by drawing short segments)."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    k = x0 - (y1 - y0)
    while k < x1:
        p0 = (max(x0, k), y1 - max(0, x0 - k))
        p1x = min(x1, k + (y1 - y0))
        p1 = (p1x, y1 - (p1x - k))
        if p1[1] < y0:
            p1 = (k + (y1 - y0), y0)
        x.d.line([p0, p1], fill=col(c, a), width=w)
        k += step


def card(x, cx, cy, w, h, label, a, c=None):
    """Side view of a graphics card: shroud with two fans and a PCIe edge."""
    if a <= 0:
        return
    c = c or WHITE
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 3, r=10, fill=PANEL + (255,), glow=False)
    for fx in (cx - w / 4, cx + w / 4):
        r = h * 0.34
        x.circle(fx, cy, r, MUTED, a, 3)
        for k in range(7):
            ang = k * 2 * math.pi / 7 + x.t * 3
            x.line([(fx, cy), (fx + r * 0.85 * math.cos(ang), cy + r * 0.85 * math.sin(ang))], MUTED, a * 0.8, 2, glow=False)
        x.circle(fx, cy, r * 0.18, c, a, 3, fill=PANEL)
    # gold fingers
    for k in range(14):
        gx = cx - w * 0.28 + k * (w * 0.3 / 14)
        x.d.rectangle([gx, cy + h / 2, gx + 10, cy + h / 2 + 18], fill=col(MUTED, a))
    x.text((cx, cy - h / 2 - 22), label, "title", 46, c, a, anchor="md")


GRID_N = 8  # 8x8 tiles of 128 MB = 8 GB


def suitcase(x, gx, gy, cell, a, fills=(), title="8 GB of VRAM", spill=0.0):
    """Memory map suitcase. fills = list of (n_tiles, color, style, progress)."""
    if a <= 0:
        return
    s = GRID_N * cell
    pad = 18
    # handle
    x.rect([gx + s / 2 - 70, gy - pad - 46, gx + s / 2 + 70, gy - pad + 4], WHITE, a, 4, r=16, glow=False)
    x.rect([gx - pad, gy - pad, gx + s + pad, gy + s + pad], WHITE, a, 4, r=18, fill=PANEL + (255,), glow=False)
    caption(x, (gx + s / 2, gy + s + pad + 18), title, a, anchor="ma", size=24)
    idx = 0
    for n, c, style, p in fills:
        shown = int(round(n * clamp(p)))
        for k in range(shown):
            i = idx + k
            if i >= GRID_N * GRID_N:
                break
            r_, c_ = divmod(i, GRID_N)
            bx, by = gx + c_ * cell + 3, gy + r_ * cell + 3
            box = [bx, by, bx + cell - 6, by + cell - 6]
            if style == "solid":
                x.d.rectangle(box, fill=col(c, a))
            elif style == "hatch":
                x.d.rectangle(box, outline=col(c, a), width=2)
                hatch(x, box, c, a * 0.9, step=10)
            else:
                x.d.rectangle(box, outline=col(c, a), width=3)
                x.d.ellipse([bx + cell / 2 - 8, by + cell / 2 - 8, bx + cell / 2 + 2, by + cell / 2 + 2], fill=col(c, a))
        idx += n
    for i in range(idx, GRID_N * GRID_N):
        r_, c_ = divmod(i, GRID_N)
        bx, by = gx + c_ * cell + 3, gy + r_ * cell + 3
        x.d.rectangle([bx, by, bx + cell - 6, by + cell - 6], outline=col(GRID, a), width=2)


def pipe(x, x0, x1, y, gbps, a, c, label, scale=0.32, flow=True):
    """Bandwidth pipe; thickness is proportional to GB/s."""
    if a <= 0:
        return
    th = max(4, gbps * scale)
    x.d.rectangle([x0, y - th / 2, x0 + (x1 - x0) * clamp(a * 1.2), y + th / 2], fill=col(c, a * 0.85))
    if flow and th > 10:
        off = (x.t * 160) % 60
        for k in range(int((x1 - x0) / 60) + 1):
            px = x0 + off + k * 60
            if px < x1 - 10:
                x.d.rectangle([px, y - 3, px + 18, y + 3], fill=col(NAVY, a * 0.7))
    x.text((x0, y - th / 2 - 12), label, "semi", 30, WHITE, a, anchor="ld")
    x.text((x1, y - th / 2 - 12), f"{gbps:g} GB/s", "title", 36, c, a, anchor="rd")


def frametime_strip(x, box, spikes, a, prog, c=None, base=16.7, ymax=60, seed=1):
    """Frame-time chart: each column is one frame; spikes is a list of (frame index, ms)."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    rule(x, x0, x1, y1, a, WHITE, 2)
    n = 90
    yb = y1 - (y1 - y0) * base / ymax
    x.d.line([(x0, yb), (x1, yb)], fill=col(GREEN, a * 0.8), width=2)
    x.text((x1 + 10, yb), "16.7 ms", "mono", 22, GREEN, a, anchor="lm")
    sp = dict(spikes)
    shown = int(n * clamp(prog))
    for i in range(shown):
        ms = sp.get(i, base + 1.6 * math.sin(i * 1.7 + seed) + 0.8 * math.sin(i * 0.37))
        h = (y1 - y0) * min(ms, ymax) / ymax
        bx = x0 + i * (x1 - x0) / n
        cc = (c or RED) if ms > 30 else MUTED
        x.d.rectangle([bx, y1 - h, bx + (x1 - x0) / n - 3, y1 - 2], fill=col(cc, a))


def big_num(x, xy, v, a, c, size=150, suffix="", anchor="ms"):
    x.text(xy, f"{v}{suffix}", "title", size, c, a, anchor=anchor)


# ---------- scenes ----------
def s_hook(x):
    a0, a1, a2 = x.b(0), x.b(1), x.b(2)
    card(x, 560, 330, 560, 190, "Card A", a0)
    card(x, 1360, 330, 560, 190, "Card B", a0)
    caption(x, (960, 160), "same chip   ·   same game", a0, anchor="ma")
    # counters
    p = ease(x.since(1) / 2.0)
    big_num(x, (560, 650), int(66 * p), a1, GREEN)
    big_num(x, (1360, 650), int(27 * p), a1, RED)
    caption(x, (560, 690), "fps average", a1, anchor="ma")
    caption(x, (1360, 690), "fps average   ·   dips to 9", a1, anchor="ma")
    frametime_strip(x, [1100, 740, 1620, 880], [(14, 52), (33, 60), (47, 44), (61, 58), (79, 49)], a1,
                    x.since(1) / 3.0)
    frametime_strip(x, [300, 740, 820, 880], [], a1, x.since(1) / 3.0, seed=4)
    # reveal the difference
    if a2 > 0:
        label_box(x, 560, 475, "16 GB VRAM", GREEN, a2, 38)
        label_box(x, 1360, 475, "8 GB VRAM", RED, a2, 38)


def s_what(x):
    a = [x.b(i) for i in range(6)]
    cx, cy = 1180, 520
    # GPU and four GDDR7 chips
    chip_icon(x, cx, cy, 200, WHITE, a[1], 4, pins=6)
    x.text((cx, cy), "GPU", "title", 54, WHITE, a[1], anchor="mm")
    chips = [(cx - 330, cy - 170), (cx + 330, cy - 170), (cx - 330, cy + 170), (cx + 330, cy + 170)]
    for k, (mx, my) in enumerate(chips):
        x.rect([mx - 85, my - 55, mx + 85, my + 55], CYAN, a[2], 3, r=4, fill=PANEL + (255,), glow=False)
        x.text((mx, my), "GDDR7", "semi", 28, CYAN, a[2], anchor="mm")
        # 32-bit trace bundle
        for j in range(4):
            off = (j - 1.5) * 10
            x.line([(mx + (60 if mx < cx else -60), my + off), (cx + (-100 if mx < cx else 100), cy + off * 0.6 + (my - cy) * 0.25)],
                   MUTED, a[2], 2, glow=False)
        # data dots
        if a[4] > 0:
            for j in range(3):
                q = ((x.since(4) * 1.6 + j / 3 + k * 0.17) % 1)
                px = lerp(mx + (60 if mx < cx else -60), cx + (-100 if mx < cx else 100), q)
                py = lerp(my, cy + (my - cy) * 0.25, q)
                x.d.rectangle([px - 7, py - 7, px + 7, py + 7], fill=col(AMBER, a[4]))
    caption(x, (cx, cy + 300), "128-bit bus   ·   4 chips × 32 bits", a[2], anchor="ma")
    # left column: text card
    x.text((140, 200), "RTX 5060 Ti", "title", 60, WHITE, a[0])
    x.text((140, 270), "8 GB  or  16 GB", "semi", 40, MUTED, a[0])
    rule(x, 140, 560, 340, a[0])
    # system RAM far away, greyed
    x.rect([140, 380, 520, 520], MUTED, a[1], 2, r=6, glow=False)
    x.text((330, 430), "System RAM", "semi", 32, MUTED, a[1], anchor="mm")
    caption(x, (330, 480), "for the CPU", a[1], anchor="mm", size=22)
    p = ease(x.since(4) / 1.6)
    big_num(x, (140, 760), int(448 * p), a[4], AMBER, size=130, anchor="ls")
    x.text((140, 820), "GB per second, card to its own memory", "semi", 30, WHITE, a[4])
    if a[5] > 0:
        caption(x, (140, 900), "everything for the next frame lives here", a[5], c=WHITE, size=24)


def s_texture(x):
    a = [x.b(i) for i in range(7)]
    # the texture swatch
    tx, ty, ts = 180, 170, 300
    if a[1] > 0:
        n = 8
        for i in range(n):
            for j in range(n):
                c = WHITE if (i + j) % 2 == 0 else MUTED
                x.d.rectangle([tx + i * ts / n, ty + j * ts / n, tx + (i + 1) * ts / n, ty + (j + 1) * ts / n],
                              fill=col(c, a[1] * (0.9 if c == WHITE else 0.5)))
        x.rect([tx, ty, tx + ts, ty + ts], WHITE, a[1], 3, r=0, glow=False)
        caption(x, (tx + ts / 2, ty + ts + 20), "4096 × 4096 pixels", a[2], anchor="ma", size=24)
    # size bars, to scale (64 MB = 600 px)
    bx = 700
    sc = 600 / 64
    raw_a = a[2]
    x.text((bx, 230), "Raw", "semi", 32, WHITE, raw_a, anchor="ls")
    x.d.rectangle([bx, 250, bx + 64 * sc * clamp(raw_a), 300], fill=col(MUTED, raw_a))
    x.text((bx + 620, 290), "64 MB", "title", 40, MUTED, raw_a, anchor="ls")
    x.text((bx, 380), "BC7 compressed · 1 byte per pixel", "semi", 32, WHITE, a[3], anchor="ls")
    x.d.rectangle([bx, 400, bx + 16 * sc * clamp(a[3]), 450], fill=col(WHITE, a[3]))
    mip = ease(x.since(4) / 1.0) * a[4]
    x.d.rectangle([bx + 16 * sc, 400, bx + 16 * sc + 5.33 * sc * mip, 450], fill=col(AMBER, mip))
    lbl = "16 MB" if mip < 0.5 else "about 21 MB"
    x.text((bx + 16 * sc + 5.33 * sc + 24, 440), lbl, "title", 40, WHITE, a[3], anchor="ls")
    if a[4] > 0:
        # mip pyramid under swatch
        s, px = 120, 180
        for k in range(5):
            x.rect([px, 690 - s, px + s, 690], AMBER if k else WHITE, a[4], 2, r=0, glow=False)
            px += s + 14
            s /= 2
        caption(x, (180, 715), "smaller copies", a[4], size=22)
        caption(x, (180, 750), "+ about a third", a[4], c=AMBER, size=22)
    # material stack
    if a[5] > 0:
        names = [("color", WHITE), ("bumps", CYAN), ("shine", MUTED)]
        for k, (nm, c) in enumerate(names):
            ox = 700 + k * 34
            oy = 560 + k * 26
            x.rect([ox, oy, ox + 220, oy + 150], c, a[5], 3, r=4, fill=PANEL + (255,), glow=False)
            x.text((ox + 236, oy + 14), nm, "semi", 24, c, a[5], anchor="lm")
        caption(x, (700, 800), "one material", a[5], size=22)
    if a[6] > 0:
        x.text((1700, 640), "× 10", "title", 80, WHITE, a[6], anchor="rm")
        x.text((1700, 780), "640 MB", "title", 90, AMBER, a[6], anchor="rs")
        caption(x, (1700, 820), "already", a[6], anchor="ra", size=22)


def s_pack(x):
    a = [x.b(i) for i in range(5)]
    cell = 82
    gx, gy = 220, 200
    fills = [
        (30, WHITE, "solid", a[0] * ease(x.since(0) / 3.0)),
        (8, CYAN, "hatch", ease(x.since(2) / 1.5) * a[2]),
        (6, MUTED, "solid", ease(x.since(3) / 1.0) * a[3]),
        (4, MUTED, "hatch", ease(x.since(3) / 1.5) * a[3]),
        (7, AMBER, "hatch", ease((x.since(3) - 1.5) / 1.2) * a[3]),
        (5, AMBER, "dot", ease(x.since(4) / 1.0) * a[4]),
    ]
    suitcase(x, gx, gy, cell, 1.0, fills, title="8 GB of VRAM · each tile 128 MB")
    # legend
    lx = 1060
    items = [("Textures", WHITE, "solid", a[0], "the nearby world, too"),
             ("Frame buffers", CYAN, "hatch", a[2], "1440p image ≈ 15 MB, and many of them"),
             ("Models", MUTED, "solid", a[3], "3D geometry"),
             ("Shaders", MUTED, "hatch", a[3], "small programs"),
             ("Ray tracing map", AMBER, "hatch", a[3], "BVH of the scene"),
             ("Frame generation", AMBER, "dot", a[4], "extra frames in flight")]
    for k, (nm, c, st, aa, sub) in enumerate(items):
        y = 220 + k * 112
        box = [lx, y, lx + 56, y + 56]
        if st == "solid":
            x.d.rectangle(box, fill=col(c, aa))
        elif st == "hatch":
            x.d.rectangle(box, outline=col(c, aa), width=2)
            hatch(x, box, c, aa, 10)
        else:
            x.d.rectangle(box, outline=col(c, aa), width=3)
            x.d.ellipse([lx + 22, y + 22, lx + 34, y + 34], fill=col(c, aa))
        x.text((lx + 86, y + 6), nm, "semi", 36, WHITE, aa)
        x.text((lx + 86, y + 50), sub, "reg", 26, MUTED, aa)



def s_console(x):
    a = [x.b(i) for i in range(5)]
    # console
    cx = 420
    if a[1] > 0:
        x.rect([cx - 70, 180, cx + 70, 590], WHITE, a[1], 3, r=28, fill=PANEL + (255,), glow=False)
        x.d.line([(cx, 200), (cx, 570)], fill=col(MUTED, a[1]), width=3)
        x.d.rectangle([cx - 100, 600, cx + 100, 616], fill=col(MUTED, a[1]))
        x.circle(cx + 35, 230, 8, MUTED, a[1], 2)
        caption(x, (cx, 660), "current consoles", a[1], anchor="ma")
    # shared memory bar
    if a[2] > 0:
        y = 760
        w = 16 * 40
        x.text((cx - 320, y - 20), "PlayStation 5: 16 GB shared", "semi", 34, WHITE, a[2], anchor="ls")
        x.d.rectangle([cx - 320, y, cx - 320 + w * clamp(a[2]), y + 50], outline=col(WHITE, a[2]), width=2)
        sp = ease(x.since(2) / 1.5)
        x.d.rectangle([cx - 320, y, cx - 320 + w * 0.35 * sp, y + 50], fill=col(MUTED, a[2]))
        hatch(x, [cx - 320 + w * 0.35 * sp, y, cx - 320 + w * sp, y + 50], WHITE, a[2] * 0.8, 12)
        x.text((cx - 320, y + 90), "CPU", "semi", 26, MUTED, a[2])
        x.text((cx - 320 + w * 0.35 + 10, y + 90), "graphics", "semi", 26, WHITE, a[2])
    # PC cards (to the same 40 px per GB scale)
    rx, sc = 1050, 34
    rule(x, 1000, 1800, 300, a[3])
    x.text((rx, 260), "On a PC, high settings", "semi", 38, WHITE, a[3], anchor="ls")
    x.text((rx, 400), "16 GB card", "semi", 34, WHITE, a[4], anchor="ls")
    x.d.rectangle([rx, 420, rx + 16 * sc, 480], outline=col(WHITE, a[4]), width=2)
    u = ease(x.since(4) / 1.6)
    x.d.rectangle([rx, 420, rx + 10 * sc * u, 480], fill=col(GREEN, a[4]))
    x.d.rectangle([rx + 9 * sc, 410, rx + 11 * sc, 490], outline=col(GREEN, a[4] * u), width=2)
    x.text((rx + 16 * sc + 20, 462), "9-11 GB used", "title", 34, GREEN, a[4] * u, anchor="ls")
    x.text((rx, 600), "8 GB card", "semi", 34, WHITE, a[4], anchor="ls")
    x.d.rectangle([rx, 620, rx + 8 * sc, 680], outline=col(WHITE, a[4]), width=2)
    x.d.rectangle([rx, 620, rx + 7.8 * sc * u, 680], fill=col(RED, a[4]))
    x.text((rx + 8 * sc + 20, 662), "nearly full", "title", 34, RED, a[4] * u, anchor="ls")
    if a[3] > 0:
        caption(x, (rx, 760), "PC Gamer, in-game tests, 2026", a[4], size=22)


def s_overflow(x):
    a = [x.b(i) for i in range(8)]
    cell = 52
    gx, gy = 1360, 170
    out = ease(x.since(2) / 1.5) * a[2]
    fills = [(64, WHITE, "solid", 1.0)]
    # the suitcase is full; spilled tiles fly out to the left into system RAM
    if a[7] <= 0:
        suitcase(x, gx, gy, cell, a[0] * (1 - a[7]), fills, title="VRAM · full")
        # RAM box
        x.rect([140, 170, 560, 590], MUTED, a[2], 3, r=8, glow=False)
        caption(x, (350, 610), "system RAM", a[2], anchor="ma")
        for k in range(10):
            sx, sy = gx - 30, gy + 60 + k * 36
            tx_, ty_ = 180 + (k % 5) * 76, 220 + (k // 5) * 76
            q = clamp(out * 1.6 - k * 0.06)
            px, py = lerp(sx, tx_, q), lerp(sy, ty_, q)
            x.d.rectangle([px, py, px + 60, py + 60], fill=col(WHITE, a[2] * clamp(q * 4)))
        if a[1] > 0 and a[2] <= 0:
            x.text((960, 650), "No crash.", "title", 70, WHITE, a[1], anchor="mm")
        # pipes, thickness to scale
        y0 = 770
        pipe(x, 140, 1240, y0 + 90, 32, a[4], RED, "PCIe 4.0 × 8 lanes", scale=0.9)
        if a[5] > 0:
            x.text((140, y0 - 40), "inside the card: 448 GB/s", "title", 40, GREEN, a[5], anchor="ls")
            x.d.rectangle([140, y0 - 25, 140 + 1100 * clamp(a[5]), y0 + 25], fill=col(GREEN, a[5] * 0.85))
            caption(x, (1260, y0), "14 × wider", a[5], c=WHITE, anchor="lm", size=22)
        if a[6] > 0:
            x.text((620, 300), "DDR5-6000 dual channel", "semi", 28, WHITE, a[6], anchor="ls")
            x.text((620, 360), "≈ 96 GB/s peak", "title", 44, AMBER, a[6], anchor="ls")
        if a[3] > 0:
            # courier dot crawling across the PCIe pipe
            q = (x.since(3) * 0.25) % 1
            px = lerp(1240, 140, q)
            x.d.rectangle([px - 12, y0 + 78, px + 12, y0 + 102], fill=col(WHITE, a[3]))
    else:
        # chef analogy
        b = a[7]
        x.rect([200, 260, 760, 760], WHITE, b, 3, r=8, glow=False)
        x.text((480, 230), "Kitchen", "title", 50, WHITE, b, anchor="ms")
        x.d.rectangle([260, 600, 700, 640], fill=col(MUTED, b))  # counter
        x.circle(480, 470, 50, WHITE, b, 4)  # chef head
        x.d.rectangle([440, 520, 520, 600], fill=col(WHITE, b))
        x.rect([1260, 360, 1720, 760], MUTED, b, 3, r=8, glow=False)
        x.text((1490, 330), "Shop", "title", 50, MUTED, b, anchor="ms")
        for k in range(6):
            x.d.rectangle([1300 + (k % 3) * 140, 420 + (k // 3) * 150, 1400 + (k % 3) * 140, 520 + (k // 3) * 150],
                          fill=col(WHITE, b * 0.7))
        rule(x, 760, 1260, 720, b, MUTED, 4)
        q = (x.since(7) * 0.4) % 1
        px = lerp(1250, 770, q)
        x.d.rectangle([px - 18, 690, px + 18, 714], fill=col(AMBER, b))
        caption(x, (1010, 780), "down the street", b, anchor="ma")


def s_stutter(x):
    a = [x.b(i) for i in range(8)]
    box = [160, 220, 1240, 600]
    spikes = [(18, 50), (41, 44), (63, 55), (80, 48)]
    frametime_strip(x, box, spikes if a[2] > 0 else [], max(a[0], 0.0), x.since(0) / 5.0)
    caption(x, (160, 180), "frame time, one bar per frame", a[0])
    if a[2] > 0:
        sx = 160 + 41 * (1080 / 90)
        x.text((sx, 270), "waiting on a texture", "semi", 28, RED, a[2], anchor="md")
    if a[4] > 0:
        x.text((1240, 650), "a frame 2-3× as long = a hitch", "semi", 32, WHITE, a[4], anchor="ra")
    # right: results
    rx = 1380
    if a[5] > 0:
        x.text((rx, 240), "1% low", "title", 56, WHITE, a[5])
        x.text((rx, 310), "the slowest 1 in 100 frames", "reg", 28, MUTED, a[5])
    caption(x, (160, 720), "Cyberpunk 2077 · 1080p · medium ray tracing · PC Gamer", a[6], size=22)
    for k, (lbl, v16, v8, aa) in enumerate([("average", 91, 91, a[6]), ("1% low", 63, 44, a[7])]):
        y = 790 + k * 80
        x.text((160, y + 30), lbl, "semi", 32, WHITE, aa, anchor="ls")
        x.d.rectangle([420, y, 420 + v16 * 8 * clamp(aa), y + 26], fill=col(GREEN, aa))
        x.text((420 + v16 * 8 + 16, y + 26), f"16 GB  {v16}", "monob", 26, GREEN, aa, anchor="ls")
        x.d.rectangle([420, y + 30, 420 + v8 * 8 * clamp(aa), y + 56], fill=col(RED if v8 < v16 else MUTED, aa))
        x.text((420 + v8 * 8 + 16, y + 56), f"8 GB  {v8}", "monob", 26, RED if v8 < v16 else MUTED, aa, anchor="ls")


def s_slot(x):
    a = [x.b(i) for i in range(7)]
    # staircase of slots: link bandwidth for an 8-lane card
    gens = [("PCIe 3", 16, a[1]), ("PCIe 4", 32, a[2]), ("PCIe 5", 64, a[3])]
    base_y = 640
    for k, (nm, bw, aa) in enumerate(gens):
        x0 = 200 + k * 300
        h = bw * 5
        x.d.rectangle([x0, base_y - h * clamp(aa), x0 + 220, base_y], fill=col(WHITE if k == 2 else MUTED, aa * 0.9))
        x.text((x0 + 110, base_y - h - 16), f"{bw} GB/s", "title", 38, WHITE, aa, anchor="ms")
        x.text((x0 + 110, base_y + 50), nm, "semi", 34, WHITE, aa, anchor="ms")
    rule(x, 160, 1100, base_y, a[0], WHITE, 3)
    caption(x, (160, 160), "8-lane card · link bandwidth, both directions", a[0], size=22)
    caption(x, (160, 750), "Dragon Age: The Veilguard · TechSpot", a[1], size=22)
    # results column
    rx = 1250
    x.text((rx, 250), "8 GB card", "title", 48, WHITE, a[1])
    rows = [("PCIe 3", "27 fps avg, 9 low", RED, a[1]),
            ("PCIe 4", "1% lows +111%", AMBER, a[2]),
            ("PCIe 5", "average +12% more", WHITE, a[3])]
    for k, (nm, s, c, aa) in enumerate(rows):
        y = 340 + k * 80
        x.text((rx, y), nm, "semi", 30, MUTED, aa)
        x.text((rx + 150, y), s, "semi", 32, c, aa)
    if a[4] > 0:
        rule(x, rx, 1800, 600, a[4], WHITE, 2)
        x.text((rx, 690), "16 GB card still", "semi", 34, WHITE, a[4], anchor="ls")
        x.text((rx, 820), "+68%", "title", 130, GREEN, a[4], anchor="ls")
    if a[5] > 0:
        x.text((960, 900), "A faster slot softens the hit.", "title", 40, WHITE, a[5], anchor="ms")
    if a[6] > 0:
        stamp(x, 400, 320, "NOT A FIX", RED, a[6], angle=-7)


def s_games(x):
    a = [x.b(i) for i in range(5)]
    # game rows (8 GB vs 16 GB average fps)
    rows = [("The Last of Us Part II", 92, 91, a[1], "PCIe 5"),
            ("Monster Hunter Wilds", 34, 84, a[2], "any slot")]
    for k, (nm, v8, v16, aa, note) in enumerate(rows):
        y = 220 + k * 170
        x.text((160, y), nm, "title", 40, WHITE, aa)
        caption(x, (1780, y + 10), note, aa, anchor="ra", size=20)
        x.d.rectangle([160, y + 60, 160 + v16 * 9 * clamp(aa), y + 86], fill=col(GREEN, aa))
        x.text((160 + v16 * 9 + 14, y + 86), f"16 GB  {v16}", "monob", 26, GREEN, aa, anchor="ls")
        bad = v8 < v16 * 0.8
        x.d.rectangle([160, y + 94, 160 + v8 * 9 * clamp(aa), y + 120], fill=col(RED if bad else MUTED, aa))
        x.text((160 + v8 * 9 + 14, y + 120), f"8 GB  {v8}", "monob", 26, RED if bad else MUTED, aa, anchor="ls")
    if a[2] > 0:
        x.text((160, 580), "Indiana Jones: a big gap too", "semi", 30, MUTED, a[2], anchor="ls")
    # settings sliders
    sl = [("Textures", 0.9), ("Resolution", 0.45), ("Ray tracing", 0.5), ("Frame generation", 0.35)]
    for k, (nm, w) in enumerate(sl):
        y = 660 + k * 66
        aa = a[3] * clamp((x.since(3) - k * 0.35) / 0.4)
        x.text((160, y + 10), nm, "semi", 30, WHITE, aa, anchor="lm")
        rule(x, 520, 1000, y + 10, aa, MUTED, 3)
        steps = 4
        for s in range(steps + 1):
            x.circle(520 + s * 120, y + 10, 6, MUTED, aa, 2, fill=PANEL)
        pos = 4 if k == 0 else 3 - (k > 1)
        if k == 0:
            pos = 4 - ease(x.since(4) / 0.8) * a[4]
        x.circle(520 + pos * 120, y + 10, 16, AMBER if k == 0 else WHITE, aa, 4, fill=NAVY)
        # memory used bar
        x.d.rectangle([1100, y - 6, 1100 + 600 * w * (1 - 0.35 * ease(x.since(4) / 0.8) * a[4] if k == 0 else 1), y + 26],
                      fill=col(AMBER if k == 0 else MUTED, aa * 0.8))
    if a[3] > 0:
        caption(x, (1100, 620), "VRAM it costs (illustrative)", a[3], size=22)


def s_need(x):
    a = [x.b(i) for i in range(5)]
    if a[0] > 0:
        x.text((960, 170), "How much do you need?", "title", 56, WHITE, a[0], anchor="mm")
    if a[1] > 0:
        caption(x, (960, 230), "PC Gamer 2026: 8 GB is enough, with caveats", a[1], anchor="mm", size=22)
    tiers = [("8 GB", "have one?", ["1080p", "textures: high, not ultra", "easy on RT and frame gen"], RED, a[2]),
             ("12 GB", "buying new", ["sensible floor", "for 1440p"], WHITE, a[3]),
             ("16 GB", "keeping for years", ["room to grow", "as games grow"], GREEN, a[3])]
    for k, (gb, sub, lines, c, aa) in enumerate(tiers):
        x0 = 170 + k * 540
        x.rect([x0, 290, x0 + 480, 760], c, aa, 3, r=6, fill=PANEL + (255,), glow=False)
        x.text((x0 + 40, 420), gb, "title", 100, c, aa, anchor="ls")
        caption(x, (x0 + 40, 450), sub, aa, size=22)
        for j, l in enumerate(lines):
            x.text((x0 + 40, 540 + j * 56), l, "reg", 32, WHITE, aa)
    if a[4] > 0:
        x.rect([170, 800, 1750, 900], AMBER, a[4], 3, r=50, glow=False)
        x.text((960, 850), "8-lane card + PCIe 3 board = hit twice as hard", "semi", 36, AMBER, a[4], anchor="mm")


def s_check(x):
    a = [x.b(i) for i in range(6)]
    if a[3] <= 0:
        # Task Manager-style window
        x.rect([300, 160, 1620, 880], WHITE, a[0], 3, r=10, fill=PANEL + (255,), glow=False)
        x.d.rectangle([303, 163, 1617, 220], fill=col(GRID, a[0]))
        x.text((330, 192), "Task Manager  ›  Performance  ›  GPU", "semi", 28, WHITE, a[1], anchor="lm")
        x.text((360, 290), "Dedicated GPU memory", "semi", 36, WHITE, a[1])
        # usage chart
        gx0, gy0, gx1, gy1 = 360, 360, 1560, 760
        x.rect([gx0, gy0, gx1, gy1], MUTED, a[1], 2, r=0, glow=False)
        lim = gy0 + 30
        x.d.line([(gx0, lim), (gx1, lim)], fill=col(RED, a[1]), width=2)
        x.text((gx1 - 10, lim - 8), "8.0 GB limit", "mono", 24, RED, a[1], anchor="rd")
        p = clamp(x.since(1) / 4.0)
        pts = []
        for i in range(int(120 * p) + 1):
            u = i / 120
            v = min(1.0, 0.35 + u * 1.3) + 0.01 * math.sin(i)
            pts.append((gx0 + u * (gx1 - gx0), gy1 - (gy1 - lim) * min(v, 0.995)))
        if len(pts) > 1:
            x.line(pts, WHITE, a[1], 4, glow=False)
        used = min(7.9, 2.8 + p * 10.4 * 0.5)
        x.text((1560, 290), f"{used:.1f} / 8.0 GB", "title", 40, RED if used > 7.5 else WHITE, a[1], anchor="ra")
        if a[2] > 0:
            label_box(x, 960, 820, "at the limit + stutter = your bottleneck", RED, a[2], 32)
    else:
        b = a[3]
        cell = 46
        suitcase(x, 260, 230, cell, b, [(64, WHITE, "solid", 1.0)], title="full suitcase")
        rule(x, 680, 1060, 410, b, MUTED, 4)
        x.rect([1060, 300, 1300, 520], MUTED, b, 3, r=6, glow=False)
        x.text((1180, 280), "shop = system RAM", "semi", 30, MUTED, b, anchor="ms")
        for k in range(4):
            x.d.rectangle([1090 + (k % 2) * 110, 330 + (k // 2) * 100, 1160 + (k % 2) * 110, 400 + (k // 2) * 100], fill=col(WHITE, b * 0.6))
        x.text((870, 470), "448 GB/s inside", "title", 34, GREEN, b, anchor="ma")
        x.text((870, 520), "32 GB/s across the slot", "title", 34, RED, b, anchor="ma")
        q = (x.since(3) * 0.4) % 1
        px = lerp(1050, 690, q)
        x.d.rectangle([px - 12, 398, px + 12, 422], fill=col(AMBER, b))
        if a[4] > 0:
            x.rect([1360, 220, 1760, 560], WHITE, a[4], 3, r=8, fill=PANEL + (255,), glow=False)
            caption(x, (1390, 260), "next video", a[4], size=22)
            x.text((1390, 360), "Clean your PC", "title", 46, WHITE, a[4])
            x.text((1390, 420), "without breaking it", "reg", 32, MUTED, a[4])
        if a[5] > 0:
            label_box(x, 960, 760, "Subscribe for the next one", AMBER, a[5], 40)


SCENES = [
    ("Same chip, different results", s_hook),
    ("What VRAM is", s_what),
    ("Packing one texture", s_texture),
    ("Everything else in the suitcase", s_pack),
    ("Why now: consoles set the budget", s_console),
    ("When VRAM runs out", s_overflow),
    ("Stutter and 1% lows", s_stutter),
    ("Your PCIe slot matters", s_slot),
    ("It depends on the game", s_games),
    ("How much you need", s_need),
    ("Check your own card", s_check),
]
