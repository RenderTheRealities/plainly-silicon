"""Scenes for video 02: How a GPU Actually Works.
Through-line: one frame travels the GPU pipeline inside a 16.7 ms budget.
Visual language: neon pipeline track, pixel grids, lane diagrams (no PC-case illustrations)."""
import math
from render import *  # noqa: F401,F403

STAGES = ["CPU", "Vertices", "Raster", "Shading", "Memory", "Output"]


def poly(x, pts, c, a, fill_a=None, w=4):
    if a <= 0:
        return
    if fill_a is not None:
        x.d.polygon(pts, fill=col(c, a * fill_a))
    x.line(list(pts) + [pts[0]], c, a, w)


def track(x, active, a=1.0, y=150):
    """Pipeline progress track shown at the top of the stage scenes."""
    if a <= 0:
        return
    x0, x1 = 360, 1560
    step = (x1 - x0) / (len(STAGES) - 1)
    x.line([(x0, y), (x1, y)], MUTED, a * 0.5, 3, glow=False)
    for i, s in enumerate(STAGES):
        cx = x0 + i * step
        on = i <= active
        c = CYAN if i == active else (AMBER if on else MUTED)
        x.circle(cx, y, 13 if i == active else 9, c, a, 3, fill=c if on else NAVY)
        x.text((cx, y + 30), s, "semi", 22, c, a * (1 if on else 0.6), anchor="mt")


def ms_clock(x, cx, cy, r, frac, a, label=True):
    """Ring that fills as the 16.7 ms budget is used."""
    if a <= 0:
        return
    x.circle(cx, cy, r, PANEL, a, 14)
    if frac > 0:
        box = [cx - r, cy - r, cx + r, cy + r]
        x.d.arc(box, -90, -90 + 360 * frac, fill=col(CYAN if frac < 0.95 else RED, a), width=14)
    if label:
        x.text((cx, cy - 10), f"{16.7 * frac:4.1f}", "monob", int(r * 0.5), WHITE, a, anchor="mm")
        x.text((cx, cy + r * 0.38), "ms", "semi", int(r * 0.2), MUTED, a, anchor="mm")


# 0 ---------------------------------------------------------------
def s_hook(x):
    a = x.b(0)
    frac = clamp(x.t / 6.0)
    ms_clock(x, 480, 500, 220, frac, a)
    x.text((480, 790), "1 frame at 60 fps", "semi", 34, MUTED, a, anchor="mm")
    # a frame on the right: wireframe triangles turning into filled pixels
    fx0, fy0, fw, fh = 900, 250, 840, 480
    x.rect([fx0, fy0, fx0 + fw, fy0 + fh], WHITE, a, 3, r=6, glow=False)
    a1 = x.b(1)
    n = 14
    cell = fw / n
    rows = int(fh / cell)
    fill = clamp(x.since(1) / 7.0)
    for r_ in range(rows):
        for c_ in range(n):
            k = (r_ * n + c_) / (rows * n)
            if k < fill:
                hue = (math.sin(c_ * 0.5 + r_ * 0.3) + 1) / 2
                cc = tuple(int(CYAN[i] * hue + AMBER[i] * (1 - hue)) for i in range(3))
                x0_, y0_ = fx0 + c_ * cell, fy0 + r_ * cell
                x.d.rectangle([x0_ + 3, y0_ + 3, x0_ + cell - 3, y0_ + cell - 3], fill=col(cc, a1 * 0.85))
    # triangle wireframe on top fading as pixels fill
    wa = a * (1 - 0.7 * fill)
    tris = [[(960, 700), (1200, 320), (1380, 690)], [(1200, 320), (1560, 280), (1380, 690)], [(1380, 690), (1560, 280), (1700, 680)]]
    for tri in tris:
        poly(x, tri, WHITE, wa, None, 3)
        for p in tri:
            x.circle(p[0], p[1], 9, AMBER, wa, 0, fill=AMBER)
    x.text((fx0 + fw / 2, fy0 + fh + 50), "triangles  ->  finished picture", "semi", 32, WHITE, a1, anchor="mm")


# 1 ---------------------------------------------------------------
def s_job(x):
    a = x.b(1)
    # full HD rectangle drawn to scale (1 px here = 4 real px)
    s = 0.22
    hx0, hy0 = 200, 300
    hw, hh = 1920 * s, 1080 * s
    x.rect([hx0, hy0, hx0 + hw, hy0 + hh], CYAN, a, 4, r=4, fill=PANEL + (255,))
    x.text((hx0 + hw / 2, hy0 + hh / 2 - 20), "Full HD", "title", 44, CYAN, a, anchor="mm")
    x.text((hx0 + hw / 2, hy0 + hh / 2 + 30), "1920 x 1080", "mono", 28, WHITE, a, anchor="mm")
    cnt = int(2073600 * clamp(x.since(1) / 1.5))
    x.text((hx0 + hw / 2, hy0 + hh + 50), f"{cnt:,} pixels", "monob", 40, WHITE, a, anchor="mm")
    # per second counter
    a3 = x.b(3)
    per = int(2073600 * 60 * clamp(x.since(3) / 2.0))
    x.text((hx0 + hw / 2, hy0 + hh + 130), "x 60 frames every second", "semi", 30, MUTED, a3, anchor="mm")
    x.text((hx0 + hw / 2, hy0 + hh + 200), f"{per:,} / s", "monob", 48, CYAN, a3, anchor="mm")
    # 4K rectangle: twice as wide, twice as tall
    a4 = x.b(4)
    kx0, ky0 = 860, 190
    kw, kh = 3840 * s * 0.98, 2160 * s * 0.98
    x.rect([kx0, ky0, kx0 + kw, ky0 + kh], AMBER, a4, 4, r=4)
    for i in (1,):
        x.line([(kx0 + kw / 2, ky0), (kx0 + kw / 2, ky0 + kh)], AMBER, a4 * 0.5, 2, glow=False)
        x.line([(kx0, ky0 + kh / 2), (kx0 + kw, ky0 + kh / 2)], AMBER, a4 * 0.5, 2, glow=False)
    x.text((kx0 + kw / 2, ky0 + kh / 2 - 26), "4K = 4 x Full HD", "title", 46, AMBER, a4, anchor="mm")
    x.text((kx0 + kw / 2, ky0 + kh / 2 + 34), "~497,000,000 pixel colors / s", "monob", 30, WHITE, a4, anchor="mm")
    sa = x.b(5) * (1 - x.b(6))
    stamp(x, 1270, 810, "TOO MUCH FOR ONE CORE", RED, sa)
    la = x.b(6)
    label_box(x, 1270, 810, "So the GPU is built differently", GREEN, la, 36)


# 2 ---------------------------------------------------------------
def s_cpu(x):
    track(x, 0, x.b(0))
    a = x.b(0)
    chip_icon(x, 380, 520, 230, AMBER, a, 5, pins=5)
    x.text((380, 520), "CPU", "title", 64, AMBER, a, anchor="mm")
    x.text((380, 700), "the director", "semi", 32, MUTED, x.b(4), anchor="mm")
    # scene thinking: camera, characters, visible
    a1 = x.b(1)
    for i, s in enumerate(["camera position", "where characters stand", "what's visible"]):
        aa = a1 * ease((x.since(1) - i * 0.5) / 0.4)
        x.rect([600, 250 + i * 70, 900, 300 + i * 70], MUTED, aa, 2, r=8, glow=False)
        x.text((750, 275 + i * 70), s, "semi", 24, WHITE, aa, anchor="mm")
    # GPU box
    ga = x.b(2)
    x.rect([1420, 300, 1800, 760], CYAN, ga, 5, r=22, fill=PANEL + (255,))
    x.text((1610, 520), "GPU", "title", 70, CYAN, ga, anchor="mm")
    x.text((1610, 800), "the crew", "semi", 32, MUTED, x.b(5), anchor="mm")
    # draw-call cards flying CPU -> GPU
    cards = [("hero", "hero_skin", "12, 0, 4"), ("tree", "bark", "30, 0, 9"), ("road", "asphalt", "0, 0, 0")]
    for i, (m, t, p) in enumerate(cards):
        st = x.since(2) - i * 1.2
        if x.b(2) <= 0 or st <= 0:
            continue
        f = ease(clamp(st / 1.6))
        cx = 560 + (1250 - 560) * f
        cy = 560 + i * 110 - 60 * math.sin(f * math.pi)
        aa = ga
        x.rect([cx - 170, cy - 46, cx + 170, cy + 46], AMBER, aa, 3, r=10, fill=NAVY + (240,), glow=False)
        x.text((cx - 150, cy - 24), f"DRAW {m}", "monob", 24, AMBER, aa)
        x.text((cx - 150, cy + 6), f"tex {t}  @ {p}", "mono", 20, WHITE, aa * x.b(3))


# 3 ---------------------------------------------------------------
def s_vertex(x):
    track(x, 1, x.b(0))
    a1 = x.b(1)
    # a single triangle with labeled vertices, left
    tri = [(260, 760), (480, 330), (700, 760)]
    poly(x, tri, CYAN, a1, 0.18, 5)
    for i, p in enumerate(tri):
        x.circle(p[0], p[1], 14, AMBER, a1, 0, fill=AMBER)
        x.text((p[0], p[1] + (40 if i != 1 else -44)), f"v{i}", "monob", 30, AMBER, a1, anchor="mm")
    x.text((480, 850), "3 vertices = 1 triangle", "semi", 30, WHITE, a1, anchor="mm")
    # vertex shader: points of a mesh move from model space box to perspective screen
    a2 = x.b(2)
    f = ease(clamp((x.since(2) - 0.5) / 2.5))
    # mesh: low-poly sphere-ish ring points
    pts = []
    for ring in range(4):
        rr = 0.3 + 0.7 * math.sin((ring + 1) / 5 * math.pi)
        for k in range(8):
            ang = k / 8 * 2 * math.pi + x.t * 0.4
            pts.append((rr * math.cos(ang), (ring - 1.5) * 0.45, rr * math.sin(ang)))
    # model space: small, left-middle. screen space: right, bigger with perspective
    mx, my, ms = 1000, 540, 110
    sx, sy, ss = 1500, 520, 260
    x.rect([880, 380, 1120, 700], MUTED, a2 * (1 - f * 0.6), 2, r=8, glow=False)
    x.text((1000, 730), "model space", "semi", 24, MUTED, a2, anchor="mm")
    x.rect([1270, 300, 1760, 760], CYAN, a2 * (0.3 + 0.7 * f), 3, r=8, glow=False)
    x.text((1515, 790), "your screen", "semi", 24, CYAN, a2, anchor="mm")
    proj = []
    for (px, py, pz) in pts:
        m2 = (mx + px * ms, my + py * ms)
        persp = 1 / (1.6 + pz * 0.6)
        s2 = (sx + px * ss * persp * 1.4, sy + py * ss * persp * 1.4)
        proj.append((m2[0] + (s2[0] - m2[0]) * f, m2[1] + (s2[1] - m2[1]) * f))
    for i in range(len(proj)):
        j = i + 1 if (i + 1) % 8 else i - 7
        x.line([proj[i], proj[j]], WHITE, a2 * 0.6, 2, glow=False)
        if i + 8 < len(proj):
            x.line([proj[i], proj[i + 8]], WHITE, a2 * 0.4, 2, glow=False)
    for p in proj:
        x.circle(p[0], p[1], 6, AMBER, a2, 0, fill=AMBER)
    # parallel badge
    a3 = x.b(3)
    label_box(x, 1300, 880, "every vertex at once: no vertex waits for another", GREEN, a3, 30)


# 4 ---------------------------------------------------------------
def s_raster(x):
    track(x, 2, x.b(0))
    a = x.b(1)
    gx0, gy0, n, m, c = 300, 230, 22, 13, 46
    tri = [(gx0 + 2 * c, gy0 + 12 * c), (gx0 + 9 * c, gy0 + 1 * c), (gx0 + 20 * c, gy0 + 11 * c)]

    def inside(px, py):
        def sgn(p1, p2, p3):
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])
        d1, d2, d3 = sgn((px, py), tri[0], tri[1]), sgn((px, py), tri[1], tri[2]), sgn((px, py), tri[2], tri[0])
        neg = d1 < 0 or d2 < 0 or d3 < 0
        pos = d1 > 0 or d2 > 0 or d3 > 0
        return not (neg and pos)

    scan = clamp(x.since(2) / 3.0) * m if x.b(2) > 0 else -1
    covered = 0
    for r_ in range(m):
        for c_ in range(n):
            cx, cy = gx0 + c_ * c + c / 2, gy0 + r_ * c + c / 2
            ins = inside(cx, cy)
            box = [gx0 + c_ * c + 2, gy0 + r_ * c + 2, gx0 + (c_ + 1) * c - 2, gy0 + (r_ + 1) * c - 2]
            if r_ < scan and ins:
                covered += 1
                x.d.rectangle(box, fill=col(CYAN, a * 0.75))
            else:
                x.d.rectangle(box, outline=col(MUTED, a * 0.35))
    poly(x, tri, WHITE, a, None, 3)
    if 0 <= scan < m:
        yy = gy0 + scan * c
        x.line([(gx0 - 10, yy), (gx0 + n * c + 10, yy)], AMBER, a, 3)
    x.text((gx0, gy0 + m * c + 30), "inside?  yes  =  fragment", "semi", 30, WHITE, x.b(2), anchor="lt")
    # fragment counter
    a3 = x.b(3)
    x.text((1460, 300), "fragments", "semi", 30, MUTED, a3, anchor="mm")
    x.text((1460, 360), f"{covered}", "monob", 72, CYAN, a3, anchor="mm")
    # back-facing triangle culled
    a4 = x.b(4)
    bt = [(1340, 640), (1460, 470), (1580, 640)]
    poly(x, bt, MUTED, a4, 0.15, 3)
    x.text((1460, 690), "facing away", "semi", 26, MUTED, a4, anchor="mm")
    ka = x.b(4) * ease((x.since(4) - 0.8) / 0.4)
    x.line([(1320, 460), (1600, 660)], RED, ka, 7)
    x.line([(1600, 460), (1320, 660)], RED, ka, 7)
    x.text((1460, 740), "skipped early", "semi", 28, RED, ka, anchor="mm")
    a6 = x.b(6)
    label_box(x, 1460, 860, "a scene: millions waiting for color", AMBER, a6, 30)


# 5 ---------------------------------------------------------------
def s_shade(x):
    track(x, 3, x.b(0))
    a = x.b(1)
    # central fragment
    fcx, fcy = 960, 520
    x.rect([fcx - 90, fcy - 90, fcx + 90, fcy + 90], WHITE, a, 4, r=10)
    x.text((fcx, fcy - 140), "pixel shader", "semi", 32, WHITE, a, anchor="mm")
    # output color builds from inputs
    k = sum(x.b(i) for i in (2, 3)) / 2
    outc = tuple(int(MUTED[i] * (1 - k) + CYAN[i] * k) for i in range(3))
    x.d.rounded_rectangle([fcx - 80, fcy - 80, fcx + 80, fcy + 80], radius=8, fill=col(outc, a))
    # texture input (checker)
    a2 = x.b(2)
    tx, ty = 360, 360
    for i in range(4):
        for j in range(4):
            cc = AMBER if (i + j) % 2 else PANEL
            x.d.rectangle([tx + i * 40, ty + j * 40, tx + i * 40 + 38, ty + j * 40 + 38], fill=col(cc, a2))
    x.text((tx + 80, ty + 190), "texture (from VRAM)", "semi", 26, AMBER, a2, anchor="mm")
    x.line([(tx + 170, ty + 80), (fcx - 100, fcy - 30)], AMBER, a2 * 0.8, 3)
    # light, shine, shadow inputs
    a3 = x.b(3)
    lx, ly = 1500, 330
    x.circle(lx, ly, 40, AMBER, a3, 4)
    for i in range(8):
        an = i / 8 * 2 * math.pi + x.t * 0.5
        x.line([(lx + 55 * math.cos(an), ly + 55 * math.sin(an)), (lx + 75 * math.cos(an), ly + 75 * math.sin(an))], AMBER, a3, 3, glow=False)
    x.text((lx, ly + 110), "light", "semi", 26, WHITE, a3, anchor="mm")
    x.line([(lx - 80, ly + 40), (fcx + 100, fcy - 40)], WHITE, a3 * 0.6, 3)
    x.text((1500, 700), "shiny?   in shadow?", "semi", 28, WHITE, a3, anchor="mm")
    x.line([(1380, 690), (fcx + 100, fcy + 40)], WHITE, a3 * 0.6, 3)
    # millions counter
    a4 = x.b(4) * (1 - x.b(5))
    x.text((fcx, 800), "x millions, every frame", "monob", 40, CYAN, a4, anchor="mm")
    # independence: nose vs tree
    a5 = x.b(5)
    for cx, lbl in ((620, "nose pixel"), (1300, "tree pixel")):
        x.rect([cx - 50, 760, cx + 50, 860], CYAN, a5, 3, r=8, fill=PANEL + (255,), glow=False)
        x.text((cx, 900), lbl, "semi", 26, WHITE, a5, anchor="mm")
    x.line([(690, 810), (1230, 810)], MUTED, a5 * 0.7, 3, glow=False)
    ka = x.b(6)
    x.text((960, 790), "no dependency", "semi", 28, GREEN, ka, anchor="mm")


# 6 ---------------------------------------------------------------
def s_sm(x):
    a = x.b(0)
    # 24 SM blocks (6 x 4) shrinking to the left as we zoom in
    z = ease(clamp(x.since(2) / 1.2)) if x.b(2) > 0 else 0
    bw, bh, gap = 150 - 70 * z, 110 - 50 * z, 16 - 8 * z
    ox, oy = 360 - 250 * z, 220
    for i in range(24):
        r_, c_ = divmod(i, 6)
        bx, by = ox + c_ * (bw + gap), oy + r_ * (bh + gap)
        aa = a * ease((x.t - i * 0.06) / 0.4)
        hi = (i == 0 and z > 0)
        x.rect([bx, by, bx + bw, by + bh], CYAN if hi else AMBER, aa, 3 if not hi else 5, r=8, fill=PANEL + (255,), glow=hi)
        if z < 0.5:
            x.text((bx + bw / 2, by + bh / 2), "SM", "semi", 28, AMBER, aa * (1 - 2 * z), anchor="mm")
    x.text((ox + 3 * (bw + gap), oy + 4 * (bh + gap) + 30), "24 streaming multiprocessors", "semi", 30 - int(8 * z), WHITE, a, anchor="mm")
    # 128 cores grid inside SM 0 -> counter 3,072
    a1 = x.b(1) * (1 - z)
    total = int(3072 * clamp(x.since(1) / 1.5))
    x.text((960, 820), f"24 x 128 = {total:,} cores", "monob", 48, CYAN, a1, anchor="mm")
    if z > 0:
        zx, zy = 700, 230
        x.rect([zx, zy, zx + 1100, zy + 600], CYAN, z, 4, r=14, fill=NAVY + (255,))
        x.text((zx + 20, zy + 18), "ONE SM: 128 cores", "monob", 26, CYAN, z)
        warp_a = x.b(4)
        instr_y = zy + 90
        if warp_a > 0:
            label_box(x, zx + 550, instr_y, "MUL  color, light", WHITE, warp_a, 32)
        for k in range(128):
            r_, c_ = divmod(k, 16)
            cx, cy = zx + 60 + c_ * 62, zy + 160 + r_ * 52
            in_warp = r_ < 2
            wa = warp_a if in_warp else 0
            cc = CYAN if in_warp and warp_a > 0 else MUTED
            x.d.rounded_rectangle([cx, cy, cx + 48, cy + 38], radius=6, outline=col(cc, z), width=2,
                                  fill=col(cc, z * 0.15) if not wa else None)
            if wa > 0:
                pulse = 0.5 + 0.5 * math.sin(x.t * 6 + c_ * 0.1)  # same phase across lanes
                hue = (k * 37 % 100) / 100
                pc = tuple(int(CYAN[i] * hue + AMBER[i] * (1 - hue)) for i in range(3))
                x.d.rounded_rectangle([cx + 4, cy + 4, cx + 44, cy + 34], radius=4, fill=col(pc, wa * (0.55 + 0.45 * pulse)))
        wa2 = x.b(4)
        x.d.rounded_rectangle([zx + 50, zy + 150, zx + 50 + 16 * 62, zy + 150 + 104], radius=10, outline=col(WHITE, wa2), width=3)
        x.text((zx + 1080, zy + 18), "1 warp = top 2 rows", "semi", 26, WHITE, wa2, anchor="ra")
        x.text((zx + 550, zy + 640), "32 threads  |  same instruction  |  different pixels", "semi", 30, WHITE, x.b(5), anchor="mm")


# 7 ---------------------------------------------------------------
def s_latency(x):
    a = x.b(1)
    split = x.b(5)
    # warp lanes timeline (top part); fades smaller when divergence part comes in
    lanes = 6
    tx0, ty0, tw, lh = 360, 200, 1300, 56
    T = x.since(2) if x.b(2) > 0 else 0
    slot = 0.6
    cur = int(T / slot)
    for w in range(lanes):
        y = ty0 + w * lh
        x.text((tx0 - 20, y + lh / 2 - 4), f"warp {w}", "semi", 24, MUTED, a * (1 - 0.6 * split), anchor="rm")
        x.line([(tx0, y + lh / 2), (tx0 + tw, y + lh / 2)], MUTED, a * 0.3 * (1 - 0.6 * split), 2, glow=False)
    # run schedule: one warp computes per slot; then waits several slots for memory
    for s in range(min(cur + 1, 26)):
        w = (s * 5) % lanes
        y = ty0 + w * lh
        x0_ = tx0 + s * 50
        x.d.rounded_rectangle([x0_, y + 10, x0_ + 46, y + lh - 14], radius=6, fill=col(CYAN, a * (1 - 0.6 * split)))
        # waiting bar after the compute slot
        x.d.rounded_rectangle([x0_ + 50, y + 22, x0_ + 50 + 200, y + lh - 26], radius=4, fill=col(MUTED, a * 0.35 * (1 - 0.6 * split)))
    x.text((tx0, ty0 - 40), "compute", "semi", 26, CYAN, a * (1 - 0.6 * split))
    x.text((tx0 + 170, ty0 - 40), "waiting for memory", "semi", 26, MUTED, a * (1 - 0.6 * split))
    a3 = x.b(3) * (1 - split)
    label_box(x, 960, 600, "warp state stays in registers: switching is nearly free", GREEN, a3, 30)
    a4 = x.b(4) * (1 - split)
    x.text((960, 690), "always more work lined up than it can run", "semi", 30, WHITE, a4, anchor="mm")
    # divergence: 32 lanes, half shadow / half lit, two passes
    if split > 0:
        y0 = 640
        x.text((960, y0 - 60), "if (in shadow) ... else ...", "monob", 32, WHITE, split, anchor="mm")
        phase = clamp(x.since(5) / 1.0)
        passA = x.since(5) % 3.0 < 1.5
        for k in range(32):
            cx = 360 + k * 38
            shadow = (k // 4) % 2 == 0
            active = (shadow and passA) or ((not shadow) and not passA)
            cc = AMBER if shadow else CYAN
            x.d.rounded_rectangle([cx, y0, cx + 30, y0 + 90], radius=5,
                                  fill=col(cc, split * (0.9 if active else 0.12)), outline=col(cc, split), width=2)
        x.text((960, y0 + 140), ("pass 1: shadow pixels" if passA else "pass 2: lit pixels") + "  (others wait)", "semi", 30,
               AMBER if passA else CYAN, split * phase, anchor="mm")
        a6 = x.b(7)
        label_box(x, 960, 880, "keep neighbors on the same path", GREEN, a6, 30)


# 8 ---------------------------------------------------------------
def s_memory(x):
    track(x, 4, x.b(0))
    a = x.b(0)
    # GPU die center with L2 block, VRAM chips around, bus lines with streaming dots
    dx0, dy0, dx1, dy1 = 760, 300, 1160, 660
    x.rect([dx0, dy0, dx1, dy1], CYAN, a, 5, r=14, fill=PANEL + (255,))
    x.text((960, 350), "GPU chip", "semi", 28, CYAN, a, anchor="mm")
    a2 = x.b(2)
    x.rect([820, 530, 1100, 620], GREEN, a2, 4, r=10, fill=NAVY + (255,))
    x.text((960, 575), "L2 cache 24 MB", "semi", 28, GREEN, a2, anchor="mm")
    a1 = x.b(1)
    chips = [(420, 300), (420, 560), (1400, 300), (1400, 560)]
    for i, (cx, cy) in enumerate(chips):
        x.rect([cx, cy, cx + 100, cy + 100], AMBER, a1, 4, r=8, fill=PANEL + (255,))
        x.text((cx + 50, cy + 50), "2 GB", "monob", 24, AMBER, a1, anchor="mm")
        # 4 lanes per chip (32 bits each)
        for l in range(4):
            yy = cy + 20 + l * 20
            xa, xb = (cx + 100, dx0) if cx < 960 else (dx1, cx)
            x.line([(xa, yy), (xb, yy)], AMBER, a1 * 0.6, 2, glow=False)
            k = ((x.t * 260) + l * 40 + i * 25) % (xb - xa)
            px = xa + k if cx < 960 else xb - k
            x.circle(px, yy, 5, AMBER, a1, 0, fill=AMBER)
    x.text((960, 740), "128-bit bus", "semi", 30, WHITE, a1, anchor="mm")
    gb = 272 * clamp(x.since(1) / 1.5)
    x.text((960, 245), f"{gb:5.0f} GB/s", "monob", 56, AMBER, a1, anchor="mm")
    x.text((470, 740), "8 GB VRAM", "semi", 30, AMBER, a1, anchor="mm")
    # overflow -> stutter
    a3 = x.b(3)
    need = clamp(x.since(3) / 2.0) * 1.3
    bx0, by = 1300, 715
    bar(x, bx0, by, 460, min(need, 1.0), RED if need > 1 else AMBER, a3, 30, "textures needed", f"{need * 8:4.1f} / 8 GB")
    if need > 1:
        stamp(x, 1530, 825, "STUTTER", RED, ease((need - 1) / 0.15) * a3, angle=6)


# 9 ---------------------------------------------------------------
def s_special(x):
    a = x.b(0)
    x.text((960, 170), "two specialists", "title", 48, WHITE, a, anchor="mm")
    # RT cores: ray from eye bouncing off boxes
    a1 = x.b(1)
    x.text((480, 260), "24 ray tracing cores", "semi", 34, CYAN, a1, anchor="mm")
    ex, ey = 180, 560
    x.circle(ex, ey, 26, WHITE, a1, 4)
    x.circle(ex + 6, ey, 9, WHITE, a1, 0, fill=WHITE)
    boxes = [(460, 380, 560, 470), (600, 520, 720, 640), (430, 700, 540, 790)]
    for i, b in enumerate(boxes):
        x.rect(list(b), MUTED, a1, 3, r=6, glow=False)
    f = clamp(x.since(1) / 1.2)
    hit = (600, 580)
    p1 = (ex + 30 + (hit[0] - ex - 30) * f, ey + (hit[1] - ey) * f)
    x.line([(ex + 30, ey), p1], CYAN, a1, 4)
    if f >= 1:
        x.rect(list(boxes[1]), CYAN, a1, 5, r=6)
        g = clamp((x.since(1) - 1.2) / 1.0)
        x.line([hit, (hit[0] + (760 - hit[0]) * g, hit[1] - 250 * g)], CYAN, a1 * 0.8, 3)
        x.text((660, 700), "hit!", "semi", 28, CYAN, a1, anchor="mm")
    x.text((480, 860), "reflections and shadows", "semi", 28, WHITE, a1, anchor="mm")
    # Tensor cores: matrix multiply grid + upscale
    a2 = x.b(2)
    x.text((1440, 260), "96 tensor cores", "semi", 34, AMBER, a2, anchor="mm")
    for m_, ox in enumerate((1080, 1290)):
        for i in range(4):
            for j in range(4):
                v = 0.4 + 0.6 * ((i * 3 + j * 5 + m_) % 7) / 6
                x.d.rectangle([ox + i * 36, 340 + j * 36, ox + i * 36 + 32, 340 + j * 36 + 32], fill=col(AMBER, a2 * v))
    x.text((1250, 410), "x", "title", 40, WHITE, a2, anchor="mm")
    # upscale small -> big image
    u = ease(clamp((x.since(2) - 1.0) / 1.5))
    sx0, sy0 = 1100, 560
    x.rect([sx0, sy0, sx0 + 160, sy0 + 90], AMBER, a2, 3, r=4, glow=False)
    x.text((sx0 + 80, sy0 + 120), "draw small", "semi", 24, MUTED, a2, anchor="mm")
    bw = 160 + 220 * u
    bx0 = 1340
    x.rect([bx0, sy0 - 40, bx0 + bw, sy0 - 40 + bw * 9 / 16], CYAN, a2 * u, 4, r=4)
    x.text((bx0 + bw / 2, sy0 - 40 + bw * 9 / 32), "rebuild big", "semi", 26, CYAN, a2 * u, anchor="mm")
    a4 = x.b(4)
    label_box(x, 960, 900, "they take the jobs the main cores are worst at", GREEN, a4, 30)


# 10 --------------------------------------------------------------
def s_output(x):
    track(x, 5, x.b(0))
    a = x.b(0)
    # front / back buffers, swapping
    swap = x.b(2)
    t = ease(clamp(x.since(2) / 0.8)) if swap > 0 else 0
    f_y = 320 + 320 * t  # front buffer moves down to back slot
    b_y = 640 - 320 * t
    fill_back = clamp(x.since(1) / 2.5) if x.b(1) > 0 else 0
    for y, lbl, filled, c in ((f_y, "frame on screen", 1.0, CYAN), (b_y, "next frame (drawing)", fill_back, AMBER)):
        x.rect([320, y, 800, y + 220], c, a, 4, r=10, fill=PANEL + (255,))
        rows = int(10 * filled)
        for r_ in range(rows):
            x.d.rectangle([330, y + 10 + r_ * 20, 790, y + 10 + r_ * 20 + 16], fill=col(c, a * 0.5))
        x.text((560, y + 110), lbl, "semi", 30, WHITE, a, anchor="mm")
    x.text((560, 270), "frame buffers", "semi", 30, MUTED, a, anchor="mm")
    # monitor on the right
    ma = x.b(2)
    x.rect([1080, 340, 1600, 660], WHITE, ma, 5, r=12)
    x.line([(1340, 660), (1340, 720)], WHITE, ma, 6, glow=False)
    x.line([(1260, 720), (1420, 720)], WHITE, ma, 6, glow=False)
    x.line([(810, 430), (1070, 430)], CYAN, ma * t, 4)
    for r_ in range(int(14 * t)):
        x.d.rectangle([1095, 355 + r_ * 21, 1585, 355 + r_ * 21 + 16], fill=col(CYAN, ma * 0.45))
    # loop counter
    a3 = x.b(3)
    fr = int(x.since(3) * 60) if a3 > 0 else 0
    x.text((1340, 780), f"frame #{fr}", "monob", 40, AMBER, a3, anchor="mm")
    # slowest stage sets pace
    a4 = x.b(4)
    if a4 > 0:
        for i, s in enumerate(STAGES):
            w = 150
            bx = 200 + i * (w + 20)
            slow = i == 3 and x.b(5) > 0
            x.rect([bx, 860, bx + w, 920], RED if slow else GREEN, a4, 3, r=10, glow=slow)
            x.text((bx + w / 2, 890), s, "semi", 26, RED if slow else GREEN, a4, anchor="mm")
        x.text((1240, 890), "slowest stage sets the fps", "semi", 26, RED, x.b(5), anchor="lm")


# 11 --------------------------------------------------------------
def s_recap(x):
    a = x.b(0)
    # all stages light in sequence along a big track, with the ms ring
    lit = clamp(x.since(1) / 6.0) * len(STAGES) if x.b(1) > 0 else 0
    for i, s in enumerate(STAGES):
        cx = 300 + i * 264
        on = i < lit
        c = CYAN if on else MUTED
        x.circle(cx, 330, 70, c, a, 5, fill=PANEL)
        x.text((cx, 330), f"{i + 1}", "title", 52, c, a, anchor="mm")
        x.text((cx, 430), s, "semi", 30, c, a, anchor="mm")
        if i:
            x.line([(cx - 194, 330), (cx - 70, 330)], c, a, 4)
    ms_clock(x, 960, 600, 90, clamp(lit / len(STAGES)), a * (1 - x.b(2)))
    # next video card
    na = x.b(2)
    x.rect([460, 520, 1460, 760], AMBER, na, 4, r=18, fill=PANEL + (255,))
    x.text((960, 575), "NEXT", "monob", 28, AMBER, na, anchor="mm")
    x.text((960, 640), "Every Type of RAM Explained", "title", 52, WHITE, na, anchor="mm")
    x.text((960, 705), "DDR3 to DDR5", "semi", 34, MUTED, na, anchor="mm")
    sa = x.b(4)
    if sa > 0:
        x.d.rounded_rectangle([780, 810, 1140, 880], radius=16, fill=col(RED, sa))
        x.text((960, 845), "SUBSCRIBE", "title", 36, (255, 255, 255), sa, anchor="mm")


SCENES = [
    ("Sixteen milliseconds", s_hook),
    ("The job: millions of pixels", s_job),
    ("The CPU sends draw calls", s_cpu),
    ("Vertices and the vertex shader", s_vertex),
    ("Rasterization", s_raster),
    ("Pixel shaders", s_shade),
    ("Cores and warps", s_sm),
    ("Hiding the wait", s_latency),
    ("Memory bandwidth and VRAM", s_memory),
    ("Ray tracing and tensor cores", s_special),
    ("Frame buffer and output", s_output),
    ("One frame, replayed", s_recap),
]
