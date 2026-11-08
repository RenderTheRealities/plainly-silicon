"""Scenes for video 05: SSD vs HDD vs NVMe, what really makes games load faster.

Design language: a green-phosphor terminal. Every scene is a "trace" of one load screen:
terminal windows print log lines, ASCII block bars fill, and line-art hardware
(platter + seeking head, flash chips, PCIe lanes, pipelines) moves underneath.
"""
import math
from render import *  # noqa: F401,F403

BLK, SHD = "█", "░"   # full block / light shade for ASCII bars


# ---------- helpers unique to this video ----------
def term(x, box, title, a, c=None, fill=True):
    """Terminal window: border, title bar with three dots, title text."""
    if a <= 0:
        return
    c = c or CYAN
    x0, y0, x1, y1 = box
    x.rect(box, c, a, 3, r=8, fill=PANEL + (235,) if fill else None, glow=False)
    x.d.line([(x0, y0 + 46), (x1, y0 + 46)], fill=col(c, a * 0.6), width=2)
    for k in range(3):
        x.circle(x0 + 24 + k * 26, y0 + 23, 7, c, a * 0.8, 2)
    x.text((x0 + 110, y0 + 23), title, "mono", 24, MUTED, a, anchor="lm")


def typed(x, xy, s, size, c, a, t, cps=28, cursor=True, kind="mono"):
    """Type a string out over time t (seconds), with a blinking block cursor."""
    if a <= 0 or t <= 0:
        return
    n = int(t * cps)
    shown = s[:n]
    x.text(xy, shown, kind, size, c, a)
    if cursor and (n < len(s) or int(t * 2) % 2 == 0):
        w = font(kind, size).getlength(shown)
        x.d.rectangle([xy[0] + w + 4, xy[1] + 4, xy[0] + w + 4 + size * 0.55, xy[1] + size * 1.05], fill=col(c, a * 0.8))


def logl(x, x0, y0, lines, a, lh=40, size=26):
    """Print log lines; each item = (beat alpha, text, color)."""
    for i, (la, s, c) in enumerate(lines):
        x.text((x0, y0 + i * lh), s, "mono", size, c, a * la)


def abar(x, xy, cells, frac, c, a, size=30, label="", value="", lw=None):
    """ASCII block bar: label, [█████░░░░], value."""
    if a <= 0:
        return
    x0, y = xy
    f = font("mono", size)
    if label:
        x.text((x0, y), label, "mono", size, WHITE, a)
        x0 += lw if lw is not None else f.getlength(label + " ")
    n = int(round(clamp(frac) * cells))
    x.text((x0, y), BLK * n, "mono", size, c, a)
    cw = f.getlength(BLK)
    x.text((x0 + cw * n, y), SHD * (cells - n), "mono", size, MUTED, a * 0.35)
    if value:
        x.text((x0 + cw * cells + 20, y), value, "mono", size, c, a)


def rnd(i, k=1):
    """Deterministic pseudo-random 0..1."""
    v = math.sin(i * 12.9898 + k * 78.233) * 43758.5453
    return v - math.floor(v)


def platter(x, cx, cy, r, a, spin, tracks=7, hi_track=None, hi_ang=None):
    x.circle(cx, cy, r, WHITE, a, 3)
    for k in range(1, tracks):
        rr = r * (0.28 + 0.72 * k / tracks)
        x.circle(cx, cy, rr, MUTED, a * 0.35, 1)
    x.circle(cx, cy, r * 0.16, WHITE, a, 3)
    x.circle(cx, cy, 8, WHITE, a, 0, fill=WHITE)
    # spinning sector marks
    for k in range(6):
        ang = spin + k * math.pi / 3
        x.line([(cx + r * 0.2 * math.cos(ang), cy + r * 0.2 * math.sin(ang)),
                (cx + r * 0.97 * math.cos(ang), cy + r * 0.97 * math.sin(ang))], MUTED, a * 0.18, 2, glow=False)
    if hi_track is not None:
        rr = r * (0.28 + 0.72 * hi_track / tracks)
        a0 = spin + hi_ang
        pts = [(cx + rr * math.cos(a0 + q * 0.04), cy + rr * math.sin(a0 + q * 0.04)) for q in range(8)]
        x.line(pts, AMBER, a, 12)


def arm_to(px, py, cx, cy, L, r):
    """Head position at distance L from pivot and r from platter centre (circle intersection)."""
    dx, dy = cx - px, cy - py
    d = math.hypot(dx, dy)
    aa = (L * L - r * r + d * d) / (2 * d)
    h = math.sqrt(max(0.0, L * L - aa * aa))
    mx, my = px + aa * dx / d, py + aa * dy / d
    return mx - h * dy / d, my + h * dx / d


def chip(x, box, c, a, label=""):
    x0, y0, x1, y1 = box
    x.rect(box, c, a, 3, r=6, fill=PANEL + (255,), glow=False)
    for k in range(5):
        xx = x0 + (x1 - x0) * (k + 1) / 6
        x.line([(xx, y0 - 10), (xx, y0)], c, a * 0.7, 2, glow=False)
        x.line([(xx, y1), (xx, y1 + 10)], c, a * 0.7, 2, glow=False)
    if label:
        x.text(((x0 + x1) / 2, (y0 + y1) / 2), label, "mono", 22, c, a, anchor="mm")


def flow(x, pts, n, speed, c, a, size=8, phase=0.0):
    """Packets moving along a polyline."""
    if a <= 0:
        return
    segs = list(zip(pts[:-1], pts[1:]))
    lens = [math.dist(p, q) for p, q in segs]
    tot = sum(lens)
    for k in range(n):
        dist_ = ((x.t * speed + phase) / tot + k / n) % 1.0 * tot
        for (p, q), L_ in zip(segs, lens):
            if dist_ <= L_:
                f_ = dist_ / L_
                x.d.rectangle([p[0] + (q[0] - p[0]) * f_ - size, p[1] + (q[1] - p[1]) * f_ - size * 0.6,
                               p[0] + (q[0] - p[0]) * f_ + size, p[1] + (q[1] - p[1]) * f_ + size * 0.6], fill=col(c, a))
                break
            dist_ -= L_


# ---------- scenes ----------
def s_hook(x):
    # two terminals racing the same save file
    a0 = x.b(0)
    boxes = [([120, 150, 930, 560], "load_save --drive=ssd", CYAN, 6.0),
             ([990, 150, 1800, 560], "load_save --drive=hdd", AMBER, 63.0)]
    clock = x.since(1) * 6.0  # compressed clock: 6 game-seconds per real second
    for box, title, c, done in boxes:
        term(x, box, title, a0, c)
        x0, y0 = box[0] + 40, box[1] + 80
        x.text((x0, y0), "Cyberpunk 2077 · same PC · same save", "mono", 26, MUTED, a0)
        fa = x.b(1)
        frac = clamp(clock / done)
        abar(x, (x0, y0 + 90), 22, frac, c, fa, 32)
        secs = min(clock, done)
        x.text((x0, y0 + 150), f"{secs:5.1f} s", "monob", 92, c, fa)
        if frac >= 1:
            x.text((x0, y0 + 270), "> READY", "monob", 34, GREEN, fa)
        elif fa > 0:
            x.text((x0, y0 + 270), "> loading" + "." * (int(x.t * 3) % 4), "mono", 30, c, fa)
    x.text((960, 600), "source: PCWorld test (SSD vs hard drive)", "mono", 22, MUTED, x.b(1), anchor="mm")
    # second fact: PCIe 5 vs PCIe 3 in Starfield
    sa = x.b(2)
    term(x, [120, 640, 1800, 790], "starfield --compare gen5 gen3   (TechSpot)", sa, WHITE)
    p = ease(x.since(2) / 1.6)
    abar(x, (160, 705), 30, 0.80 * p, CYAN, sa, 28, "PCIe 5 ", "", lw=150)
    abar(x, (1000, 705), 30, 0.83 * p, CYAN, sa, 28, "PCIe 3 ", "", lw=150)
    x.text((960, 760), "several x the top speed  ->  under 1 s apart", "mono", 24, AMBER, sa * ease(x.since(2) - 1.6), anchor="mm")
    # prompt
    ta = x.b(3)
    typed(x, (140, 840), "$ trace ./load_screen --every-drive", 40, GREEN, ta, x.since(3), 22)


def s_request(x):
    # drive map: sectors with the level's pieces scattered
    a = x.b(0)
    term(x, [100, 140, 1000, 700], "level_01.manifest  ->  drive map", a)
    cols_, rows_, cell = 26, 14, 32
    gx, gy = 135, 210
    kinds = [("texture", CYAN), ("model", AMBER), ("sound", GREEN), ("map", WHITE)]
    pa = x.b(2)
    for r_ in range(rows_):
        for c_ in range(cols_):
            i = r_ * cols_ + c_
            x0, y0 = gx + c_ * cell, gy + r_ * cell
            x.d.rectangle([x0, y0, x0 + cell - 6, y0 + cell - 6], fill=col(GRID, a))
            if rnd(i) < 0.22 and pa > 0:
                k = int(rnd(i, 3) * 4)
                appear = ease((x.since(2) - rnd(i, 5) * 1.5) / 0.3)
                taken = x.since(3) > 0.4 + rnd(i, 7) * 3.0 and x.b(3) > 0
                x.d.rectangle([x0, y0, x0 + cell - 6, y0 + cell - 6],
                              fill=col(kinds[k][1], pa * appear * (0.25 if taken else 0.9)))
    for k, (nm, c) in enumerate(kinds):
        x.d.rectangle([140 + k * 210, 662, 160 + k * 210, 682], fill=col(c, pa))
        x.text((170 + k * 210, 672), nm, "mono", 24, c, pa, anchor="lm")
    # pipeline on the right: find -> read -> unpack (CPU) -> world
    ca = x.b(3)
    steps = [("FIND", 230), ("READ", 360), ("UNPACK  cpu", 490), ("WORLD", 620)]
    for i, (nm, y) in enumerate(steps):
        sa_ = ca * ease((x.since(3) - i * 0.35) / 0.4)
        x.rect([1200, y - 45, 1700, y + 45], CYAN if i < 3 else GREEN, sa_, 3, r=6, fill=PANEL + (255,), glow=False)
        x.text((1450, y), nm, "monob", 34, CYAN if i < 3 else GREEN, sa_, anchor="mm")
        if i:
            x.line([(1450, y - 85), (1450, y - 45)], CYAN, sa_, 3, glow=False)
    x.line([(1005, 420), (1120, 420), (1120, 230), (1200, 230)], CYAN, ca * 0.5, 2, glow=False)
    flow(x, [(1005, 420), (1120, 420), (1120, 230), (1200, 230)], 4, 260, AMBER, ca)
    x.line([(1700, 230), (1760, 230), (1760, 620), (1700, 620)], CYAN, ca * 0.5, 2, glow=False)
    flow(x, [(1700, 230), (1760, 230), (1760, 620), (1700, 620)], 5, 180, AMBER, ca, 7)
    # two jobs: sequential vs random
    ja = x.b(5)
    term(x, [100, 720, 930, 875], "job 1: sequential", ja)
    for k in range(20):
        x.d.rectangle([140 + k * 38, 790, 170 + k * 38, 825], fill=col(CYAN, ja * 0.85))
    sx = 140 + (x.since(5) * 260) % 760
    x.d.polygon([(sx, 785), (sx + 14, 770), (sx - 14, 770)], fill=col(AMBER, ja))
    x.text((140, 850), "one long stream  ->  MB/s", "mono", 22, MUTED, ja, anchor="lm")
    ra = x.b(6)
    term(x, [990, 720, 1820, 875], "job 2: random lookups", ra)
    spots = [(1030 + rnd(k, 2) * 740, 780 + rnd(k, 9) * 30) for k in range(12)]
    for (px_, py_) in spots:
        x.d.rectangle([px_, py_, px_ + 22, py_ + 22], fill=col(AMBER, ra * 0.8))
    hop = int(x.since(6) * 3) % 12
    p0, p1 = spots[hop], spots[(hop + 1) % 12]
    f_ = ease((x.since(6) * 3) % 1.0)
    hx, hy = p0[0] + (p1[0] - p0[0]) * f_ + 11, p0[1] + (p1[1] - p0[1]) * f_ + 11
    x.line([(p0[0] + 11, p0[1] + 11), (hx, hy)], WHITE, ra * 0.6, 2, glow=False)
    x.circle(hx, hy, 14, WHITE, ra, 3)
    x.text((1030, 850), "many small pieces  ->  time per lookup", "mono", 22, MUTED, ra, anchor="lm")


def s_hdd(x):
    a = x.b(0)
    cx, cy, R = 560, 520, 330
    spin = x.t * 2.2
    # target track/sector chosen by beat
    tr_target = 5 if x.b(2) > 0 else 2
    sb = x.b(1)
    platter(x, cx, cy, R, a, spin, 7, hi_track=tr_target if x.b(2) > 0 else None, hi_ang=1.2)
    # arm
    px, py, L = cx + 430, cy + 300, 470
    p_seek = ease(x.since(2) / 1.2) if x.b(2) > 0 else 0
    r_from = R * (0.28 + 0.72 * 2 / 7)
    r_to = R * (0.28 + 0.72 * 5 / 7)
    r_now = r_from + (r_to - r_from) * p_seek
    if x.b(6) > 0:  # outer edge for sequential read
        r_now = r_to + (R * 0.94 - r_to) * ease(x.since(6) / 1.0)
    hx, hy = arm_to(px, py, cx, cy, L, r_now)
    x.line([(px, py), (hx, hy)], AMBER, sb, 10)
    x.circle(px, py, 28, AMBER, sb, 4, fill=PANEL)
    x.d.rectangle([hx - 12, hy - 12, hx + 12, hy + 12], fill=col(AMBER, sb))
    x.text((cx, 150), "7,200 rpm", "monob", 36, WHITE, a, anchor="mm")
    # outer-edge glow during beat 6
    oa = x.b(6)
    if oa > 0:
        x.circle(cx, cy, R * 0.94, CYAN, oa * (0.6 + 0.4 * math.sin(x.t * 6)), 8)
    # readout terminal
    ta = x.b(1)
    term(x, [1120, 160, 1820, 870], "hdd.trace", ta)
    seek_ms = 9.0 * ease(x.since(2) / 1.2)
    rot_ms = 4.2 * ease(x.since(3) / 1.0)
    lines = [
        (x.b(1), "platter : spinning", WHITE),
        (x.b(1), "head    : parked track 2", WHITE),
        (x.b(2), "> seek to track 5", AMBER),
        (x.b(2), f"  arm move   {seek_ms:4.1f} ms  (8-10)", AMBER),
        (x.b(3), "> wait for sector", AMBER),
        (x.b(3), f"  rotation   {rot_ms:4.1f} ms  (~4)", AMBER),
        (x.b(4), "  ----------------------", MUTED),
        (x.b(4), "  per lookup ~12 ms", RED),
        (x.b(5), "> read", CYAN),
        (x.b(6), "  sequential up to", CYAN),
        (x.b(6), "  190 MB/s (outer edge)", CYAN),
        (x.b(6), "  BarraCuda datasheet", MUTED),
    ]
    logl(x, 1160, 240, lines, 1, 52, 30)


def s_hdd_load(x):
    a = x.b(0)
    term(x, [100, 140, 1820, 470], "queue: level_01  (hard drive)", a, AMBER)
    # small platter icon serving the queue
    platter(x, 250, 320, 110, a, x.t * 2.2, 4)
    # queue of requests sliding left slowly, one served every 1/3 s
    served = int(x.since(1) * 3) if x.b(1) > 0 else 0
    fr = (x.since(1) * 3) % 1.0 if x.b(1) > 0 else 0
    for k in range(34):
        bx = 420 + k * 40 - (ease(fr * 2) * 40 if x.b(1) > 0 else 0)
        if bx < 400:
            continue
        hue = [CYAN, AMBER, GREEN, WHITE][int(rnd(k + served, 4) * 4)]
        x.d.rectangle([bx, 280, bx + 30, 320], fill=col(hue, a * 0.85))
    x.text((420, 340), "more requests waiting ...", "mono", 24, MUTED, a)
    ia = x.b(1)
    x.text((420, 200), f"served {served:4d} / 4,000", "monob", 38, AMBER, ia)
    x.text((1100, 205), "~100-200 random reads/s", "mono", 30, WHITE, ia)
    # arm travelling vs reading meter
    ma = x.b(2)
    abar(x, (420, 395), 16, 0.85, RED, ma, 28, "arm travelling", "", lw=270)
    abar(x, (1100, 395), 16, 0.15, CYAN, ma, 28, "reading", "", lw=160)
    # load times
    ca = x.b(3)
    term(x, [100, 510, 940, 870], "results", ca)
    abar(x, (140, 590), 16, ease(x.since(3) / 2.0), AMBER, ca, 30, "Cyberpunk", "63 s", lw=200)
    x.text((140, 640), "SSD: 6 s   (PCWorld)", "mono", 24, MUTED, ca)
    ka = x.b(4)
    abar(x, (140, 720), 16, ease(x.since(4) / 2.0), RED, ka, 30, "KCD II", "> 4 min", lw=200)
    x.text((140, 770), "WARNING: game warns", "monob", 26, RED, ka * (0.6 + 0.4 * math.sin(x.t * 6)))
    x.text((140, 810), "against hard drives (TechSpot)", "mono", 24, MUTED, ka)
    # streaming while playing: world tiles, some missing
    wa = x.b(5)
    term(x, [980, 510, 1820, 870], "stream while playing", wa)
    for i in range(6):
        for j in range(3):
            k = i * 3 + j
            bx, by = 1020 + i * 128, 570 + j * 92
            missing = x.b(6) > 0 and rnd(k, 11) < 0.35
            if missing:
                for q in range(0, 110, 16):
                    x.d.line([(bx + q, by), (bx + min(q + 8, 110), by)], fill=col(RED, wa), width=3)
                    x.d.line([(bx + q, by + 70), (bx + min(q + 8, 110), by + 70)], fill=col(RED, wa), width=3)
                x.text((bx + 55, by + 35), "?", "monob", 40, RED, wa, anchor="mm")
            else:
                loaded = ease((x.since(5) - k * 0.15) / 0.3)
                x.rect([bx, by, bx + 110, by + 70], GREEN, wa * loaded, 3, r=4, fill=GREEN + (60,), glow=False)
    x.text((1400, 848), "slow HDD -> missing pieces (Stalker 2)", "mono", 22, RED, x.b(6), anchor="mm")


def s_sata(x):
    a = x.b(0)
    # SSD board: controller + 8 flash chips
    bx0, by0, bx1, by1 = 140, 150, 1000, 540
    term(x, [bx0, by0, bx1, by1], "sata_ssd  (no moving parts)", a)
    ctrl = (220, 300, 400, 480)
    pa = x.b(2)
    chip(x, ctrl, AMBER, a, "CTRL")
    chips = [(470 + (k % 4) * 128, 260 + (k // 4) * 150) for k in range(8)]
    for k, (qx, qy) in enumerate(chips):
        busy = pa > 0 and (int(x.t * 4 + k) % 3 != 0)
        chip(x, (qx, qy, qx + 100, qy + 100), CYAN, a * (1 if busy else 0.6), "NAND")
        if pa > 0:
            flow(x, [(400, 390), (qx + 50, qy + 50)], 2, 500, AMBER, pa * 0.9, 6, phase=k * 40)
    # crossed-out platter
    ca = x.b(1)
    platter(x, 1150, 360, 110, ca * 0.5, 0, 4)
    x.line([(1040, 250), (1260, 470)], RED, ca, 6)
    x.text((1150, 510), "no arm, no platter", "mono", 24, RED, ca, anchor="mm")
    # latency comparison
    la = x.b(3)
    term(x, [1320, 150, 1820, 540], "lookup latency", la)
    p = ease(x.since(3) / 1.4)
    x.text((1360, 250), "HDD", "monob", 30, AMBER, la)
    x.d.rectangle([1360, 300, 1360 + 400 * p, 340], fill=col(AMBER, la))
    x.text((1360, 350), "~12 ms", "mono", 26, AMBER, la)
    x.text((1360, 420), "SSD", "monob", 30, CYAN, la)
    x.d.rectangle([1360, 470, 1360 + max(4, 400 * p * 0.1 / 12), 510], fill=col(CYAN, la))
    x.text((1380, 470), "~0.1 ms", "mono", 26, CYAN, la)
    # the cable
    ka = x.b(4)
    term(x, [140, 580, 1820, 875], "the catch: the SATA link", ka, AMBER)
    x.rect([180, 650, 360, 770], CYAN, ka, 3, r=6, glow=False)
    x.text((270, 710), "SSD", "monob", 34, CYAN, ka, anchor="mm")
    x.rect([1560, 650, 1780, 770], WHITE, ka, 3, r=6, glow=False)
    x.text((1670, 710), "PC", "monob", 34, WHITE, ka, anchor="mm")
    x.d.rectangle([360, 690, 1560, 730], outline=col(AMBER, ka), width=3)
    x.text((960, 672), "built for hard drives", "mono", 24, AMBER, x.b(5), anchor="md")
    # 10-bit symbols: 8 data bits + 2 encoding bits
    ea = x.b(6)
    if ka > 0:
        off = (x.t * 160) % 230
        for s_ in range(6):
            sx = 380 + s_ * 230 + off - 230
            if sx < 370 or sx > 1340:
                continue
            for b_ in range(10):
                c_ = CYAN if b_ < 8 else MUTED
                x.d.rectangle([sx + b_ * 20, 698, sx + b_ * 20 + 14, 722], fill=col(c_ if ea > 0 else CYAN, ka))
    x.text((420, 815), "6 Gb/s link", "mono", 28, WHITE, ea)
    x.text((760, 815), "8 of 10 bits = data", "mono", 28, MUTED, ea)
    x.text((1200, 815), "~600 MB/s ceiling", "monob", 30, AMBER, ea)
    x.text((1560, 815), "drives ~550", "monob", 30, CYAN, ea)


def s_sata_load(x):
    a = x.b(0)
    # the wait collapsing
    term(x, [120, 150, 900, 520], "wait per lookup", a)
    c = ease(x.since(2) / 1.2) if x.b(2) > 0 else 0
    ms = 12.0 - 11.9 * c
    h = 260 * (1 - c * 0.99)
    x.d.rectangle([220, 480 - h, 420, 480], fill=col(AMBER if c < 0.5 else CYAN, a))
    x.text((470, 300), f"{ms:5.1f} ms", "monob", 80, AMBER if c < 0.5 else CYAN, a)
    x.text((470, 400), "HDD -> SSD", "mono", 30, WHITE, a)
    ja = x.b(1)
    x.text((470, 450), "the big jump", "monob", 32, GREEN, ja)
    # bench table: Cyberpunk reload, relative time
    ta = x.b(3)
    term(x, [960, 150, 1820, 640], "bench: cyberpunk reload (TechSpot)", ta)
    rows = [("PCIe 5", 1.0, CYAN), ("PCIe 4", 1.0, CYAN), ("PCIe 3", 1.0, CYAN), ("SATA", 1.0, CYAN), ("HDD", 3.8, AMBER)]
    for i, (nm, rel, cc) in enumerate(rows):
        ra = ta * ease((x.since(3) - i * 0.25) / 0.4)
        y = 240 + i * 75
        x.text((1000, y), nm, "mono", 28, WHITE, ra)
        w_ = 400 * rel / 3.8 * ease((x.since(3) - i * 0.25) / 1.2)
        x.d.rectangle([1150, y + 4, 1150 + w_, y + 34], fill=col(cc, ra))
        x.text((1150 + w_ + 14, y), "1x" if rel == 1 else "up to 3.8x", "mono", 26, cc, ra)
    x.text((1000, 620), "relative load time · lower is better", "mono", 22, MUTED, ta, anchor="ld")
    # status
    sa = x.b(4)
    term(x, [120, 680, 1820, 875], "status", sa, GREEN)
    typed(x, (160, 750), "bottleneck(storage) ........ [ OK ]", 42, GREEN, sa, x.since(4), 30)
    x.text((160, 820), "for a lot of games, any SSD clears the storage problem", "mono", 26, MUTED, sa * ease(x.since(4) - 1.5))


def s_nvme(x):
    a = x.b(0)
    # M.2 NVMe stick
    term(x, [100, 140, 1000, 470], "nvme0n1", a)
    x.rect([150, 230, 560, 330], CYAN, a, 3, r=6, fill=PANEL + (255,), glow=False)
    for k in range(3):
        x.rect([170 + k * 95, 250, 250 + k * 95, 310], CYAN, a * 0.8, 2, r=3, glow=False)
    for k in range(10):
        x.d.rectangle([540, 238 + k * 9, 556, 243 + k * 9], fill=col(AMBER, a))
    x.text((355, 365), "M.2 · NVMe", "mono", 26, WHITE, a, anchor="mm")
    # 4 PCIe lanes to the CPU
    la = x.b(1)
    gen = 3 if x.b(5) <= 0 else 5
    gen = 4 if (x.b(4) > 0 and x.b(5) <= 0) else gen
    spd = {3: 260, 4: 520, 5: 1040}[gen] if x.b(3) > 0 else 260
    for k in range(4):
        y = 248 + k * 20
        x.line([(560, y), (840, y)], CYAN, la * 0.5, 3, glow=False)
        flow(x, [(560, y), (840, y)], 3, spd, AMBER, la, 6, phase=k * 50)
    chip_icon(x, 910, 280, 110, WHITE, la, 3, 3)
    x.text((910, 280), "CPU", "monob", 28, WHITE, la, anchor="mm")
    x.text((700, 210), "PCIe x4", "monob", 26, CYAN, la, anchor="mm")
    x.text((700, 420), "same kind of link as a GPU", "mono", 22, MUTED, la, anchor="mm")
    # generation readout
    ga = x.b(2)
    term(x, [100, 500, 1820, 875], "rated sequential read", ga)
    x.text((1780, 550), "each gen ~2x per lane", "mono", 24, AMBER, ga, anchor="rm")
    rows = [("SATA SSD   ", 550, "~550 MB/s", 0, MUTED),
            ("PCIe 3  970 EVO Plus", 3500, "3,500 MB/s", 3, CYAN),
            ("PCIe 4  990 Pro     ", 7450, "7,450 MB/s", 4, CYAN),
            ("PCIe 5  9100 Pro    ", 14800, "14,800 MB/s", 5, GREEN)]
    for i, (nm, v, lab, bi, cc) in enumerate(rows):
        ra = ga if bi == 0 else x.b(bi)
        y = 595 + i * 68
        x.text((140, y), nm, "mono", 28, WHITE, ra)
        p = ease((x.since(bi if bi else 2)) / 1.2)
        w_ = 860 * v / 14800 * p
        x.d.rectangle([560, y + 4, 560 + max(4, w_), y + 34], fill=col(cc, ra))
        x.text((560 + max(4, w_) + 16, y), lab, "monob", 28, cc, ra)
    # many queues
    qa = x.b(6)
    term(x, [1060, 140, 1820, 470], "queues", qa)
    for qn in range(10):
        qx = 1100 + qn * 70
        for k in range(4):
            yy = 200 + ((x.t * 90 + k * 55 + qn * 17) % 190)
            x.d.rectangle([qx, yy, qx + 44, yy + 30], fill=col([CYAN, AMBER, GREEN][(qn + k) % 3], qa * 0.85))
    x.text((1440, 445), "many queues, all open at once", "mono", 22, MUTED, qa, anchor="mm")


def s_bottleneck(x):
    a = x.b(0)
    # pipeline: DRIVE -> UNPACK (CPU) -> BUILD WORLD
    term(x, [100, 140, 1820, 520], "pipeline: load_screen", a)
    stages = [("DRIVE", 260, CYAN), ("UNPACK cpu", 820, AMBER), ("BUILD WORLD", 1450, GREEN)]
    ba = x.b(1)
    for i, (nm, cx_, cc) in enumerate(stages):
        sa_ = a if i == 0 else ba
        x.rect([cx_ - 170, 240, cx_ + 170, 340], cc, sa_, 3, r=6, fill=PANEL + (255,), glow=False)
        x.text((cx_, 290), nm, "monob", 32, cc, sa_, anchor="mm")
    # wide fast pipe out of the drive, then a pile up before the CPU stage
    flow(x, [(430, 290), (650, 290)], 8, 600, CYAN, a, 8)
    pile = clamp(x.since(1) / 3.0) if ba > 0 else 0
    for k in range(int(pile * 9)):
        x.d.rectangle([600 + (k % 3) * 34, 360 + (k // 3) * 22, 628 + (k % 3) * 34, 378 + (k // 3) * 22], fill=col(CYAN, ba * 0.8))
    x.text((540, 385), "waiting", "mono", 22, MUTED, ba * pile, anchor="mm")
    flow(x, [(990, 290), (1280, 290)], 3, 120, AMBER, ba, 8)
    # busy meters
    ma = x.b(2)
    abar(x, (1000, 380), 14, 0.2, CYAN, ma, 26, "drive busy", " 20%", lw=210)
    abar(x, (1000, 430), 14, 0.98 + 0.02 * math.sin(x.t * 8), RED, ma, 26, "cpu busy  ", " 100%", lw=210)
    x.text((820, 470), "bottleneck: CPU", "monob", 34, RED, ma, anchor="mm")
    x.text((260, 400), "fast enough", "mono", 26, CYAN, ma, anchor="mm")
    # bench log
    la = x.b(3)
    term(x, [100, 550, 1820, 875], "bench.log  (TechSpot / Legit Reviews)", la)
    p = ease(x.since(3) / 1.2)
    abar(x, (140, 610), 24, 0.78 * p, CYAN, la, 28, "Starfield  PCIe 5", "", lw=320)
    abar(x, (140, 655), 24, 0.81 * p, CYAN, la, 28, "Starfield  PCIe 3", "", lw=320)
    x.text((1260, 635), "< 1 s apart", "monob", 32, AMBER, la * ease(x.since(3) - 1.2), anchor="lm")
    fa = x.b(4)
    x.text((140, 725), "F1 25          every NVMe drive    = identical", "mono", 28, WHITE, fa)
    x.text((140, 770), "Red Dead 2     every SSD           = no difference", "mono", 28, WHITE, fa * ease(x.since(4) - 1.0))
    ra = x.b(5)
    x.text((140, 815), "2018 FFXIV     budget NVMe < good SATA SSD", "mono", 28, AMBER, ra)


def s_console(x):
    a = x.b(0)
    # constant streaming: packets pour from an NVMe console-style box into the world
    term(x, [100, 140, 1820, 420], "designed for console NVMe: stream all the time", a)
    ba = x.b(1)
    x.rect([160, 220, 420, 380], WHITE, ba, 3, r=10, glow=False)
    x.text((290, 270), "CONSOLE", "monob", 28, WHITE, ba, anchor="mm")
    x.text((290, 330), "NVMe", "monob", 30, CYAN, ba, anchor="mm")
    for k in range(3):
        flow(x, [(420, 260 + k * 40), (1180, 260 + k * 40)], 7, 700, CYAN, ba, 7, phase=k * 80)
    # world being built as you move
    for i in range(8):
        tx = 1220 + i * 70
        h_ = 40 + 80 * (0.5 + 0.5 * math.sin(i * 1.7 + x.t * 1.5))
        x.d.rectangle([tx, 380 - h_, tx + 54, 380], fill=col(GREEN, ba * 0.7))
    # relative results: PCIe vs SATA
    ra = x.b(2)
    term(x, [100, 450, 1820, 875], "PCIe vs SATA   (TechSpot, lower is better)", ra)
    games = [("Ratchet & Clank: Rift Apart", 5.0, "1.3 s  vs  nearly 5x", 2),
             ("Spider-Man 2  (worst case)", 4.0, "up to nearly 4x", 3),
             ("The Last of Us Part II", 1.6, "at least +60%", 3)]
    for i, (nm, rel, lab, bi) in enumerate(games):
        ga = x.b(bi) * ease((x.since(bi) - (i - 1 if i else 0) * 0.6) / 0.5)
        y = 520 + i * 115
        x.text((140, y), nm, "mono", 28, WHITE, ga)
        p = ease((x.since(bi) - (i - 1 if i else 0) * 0.6) / 1.4)
        unit = 230
        x.d.rectangle([140, y + 45, 140 + unit * p, y + 70], fill=col(CYAN, ga))
        x.d.rectangle([140, y + 78, 140 + unit * rel * p, y + 103], fill=col(AMBER, ga))
        x.text((140 + unit * 5 + 30, y + 58), "PCIe", "mono", 22, CYAN, ga, anchor="lm")
        x.text((140 + unit * 5 + 30, y + 90), "SATA", "mono", 22, AMBER, ga, anchor="lm")
        x.text((1780, y + 75), lab, "monob", 28, AMBER, ga, anchor="rm")


def s_directstorage(x):
    a = x.b(0)
    term(x, [100, 140, 1820, 600], "DirectStorage", a)
    # old path: requests one at a time through the CPU
    oa = x.b(1)
    x.text((140, 220), "old:", "monob", 28, MUTED, oa)
    nodes_old = [("DRIVE", 380), ("CPU unpack", 900), ("GPU", 1450)]
    for nm, cx_ in nodes_old:
        x.rect([cx_ - 140, 195, cx_ + 140, 265], MUTED, oa, 2, r=6, glow=False)
        x.text((cx_, 230), nm, "mono", 28, MUTED, oa, anchor="mm")
    flow(x, [(520, 230), (760, 230)], 1, 120, MUTED, oa, 8)
    flow(x, [(1040, 230), (1310, 230)], 1, 120, MUTED, oa, 8)
    x.text((640, 290), "one request at a time", "mono", 22, MUTED, oa, anchor="mm")
    # new path: batched requests into NVMe queues, GPU decompresses
    na = x.b(1)
    x.text((140, 380), "new:", "monob", 28, CYAN, na)
    x.rect([240, 345, 520, 415], CYAN, na, 3, r=6, glow=False)
    x.text((380, 380), "NVMe", "monob", 28, CYAN, na, anchor="mm")
    for q in range(4):
        flow(x, [(520, 360 + q * 14), (1310, 360 + q * 14)], 6, 600, CYAN, na, 5, phase=q * 30)
    x.text((900, 450), "batches of thousands, many queues", "mono", 22, CYAN, na, anchor="mm")
    ga = x.b(2)
    x.rect([1310, 345, 1590, 415], GREEN, max(na, ga), 3, r=6, glow=False)
    x.text((1450, 380), "GPU" + (" unpack" if ga > 0 else ""), "monob", 28, GREEN, max(na, ga), anchor="mm")
    x.text((1450, 450), "v1.1: decompression on GPU", "mono", 22, GREEN, ga, anchor="mm")
    x.text((900, 540), "CPU freed up", "monob", 28, GREEN, ga * ease(x.since(2) - 1.0), anchor="mm")
    # Forspoken result
    fa = x.b(3)
    term(x, [100, 630, 1820, 875], "Forspoken, one scene  (PCWorld)", fa)
    p = ease(x.since(3) / 1.6)
    x.text((140, 700), "SATA SSD", "mono", 30, WHITE, fa)
    x.d.rectangle([420, 702, 420 + 1100 * p, 732], fill=col(AMBER, fa))
    x.text((420 + 1100 * p + 16, 698), f"{7.4 * p:.1f} s", "monob", 30, AMBER, fa)
    x.text((140, 770), "PCIe 4 NVMe", "mono", 30, WHITE, fa)
    w4 = 1100 * 1.9 / 7.4 * p
    x.d.rectangle([420, 772, 420 + w4, 802], fill=col(CYAN, fa))
    x.text((420 + w4 + 16, 768), f"{1.9 * p:.1f} s", "monob", 30, CYAN, fa)
    x.text((140, 845), "only in games built for it", "mono", 24, MUTED, x.b(4), anchor="lm")


def s_race(x):
    a = x.b(0)
    term(x, [100, 140, 1820, 640], "race: one load screen, four drives", a)
    lanes = [("HDD", 1, 0.0, AMBER, "minutes, worst case"), ("SATA SSD", 2, 0.0, CYAN, "close, slips on new games"),
             ("NVMe PCIe 3/4", 3, 0.0, GREEN, "nearly all the benefit"), ("NVMe PCIe 5", 4, 0.0, GREEN, "rarely faster in games")]
    rates = [0.07, 0.62, 0.80, 0.82]
    caps = [0.55, 1, 1, 1]
    t_ = x.since(0)
    for i, (nm, bi, _, cc, note) in enumerate(lanes):
        y = 230 + i * 100
        x.text((140, y), nm, "monob", 30, WHITE, a)
        fr = min(caps[i], clamp(t_ * rates[i] / 2.2))
        cells = 40
        abar(x, (470, y), cells, fr, cc, a, 30)
        if fr >= 1:
            x.text((1250, y), "READY", "monob", 30, GREEN, a)
        elif i == 0:
            x.text((1250, y), "seeking" + "." * (int(x.t * 3) % 4), "mono", 30, AMBER, a)
        x.text((470, y + 44), note, "mono", 22, cc, x.b(bi))
    # price check
    pa = x.b(4)
    term(x, [100, 670, 900, 875], "price check (TechSpot)", pa, AMBER)
    x.text((140, 730), "PCIe 5 vs PCIe 4", "mono", 30, WHITE, pa)
    x.text((140, 780), "cost  +40% or more", "monob", 34, RED, pa)
    x.text((140, 825), "games  ~ same", "monob", 34, GREEN, pa)
    # M.2 shape check
    ma = x.b(5)
    term(x, [960, 670, 1820, 875], "M.2 = a shape, not a speed", ma)
    for k, (lab, cc) in enumerate([("M.2 SATA", MUTED), ("M.2 NVMe", CYAN)]):
        y0 = 725 + k * 72
        x.rect([1000, y0, 1360, y0 + 55], cc, ma, 3, r=5, glow=False)
        x.text((1180, y0 + 28), lab, "monob", 26, cc, ma, anchor="mm")
    x.text((1400, 765), "same stick shape", "mono", 24, WHITE, ma)
    x.text((1400, 805), "check your slot", "monob", 26, AMBER, ma)


def s_outro(x):
    a = x.b(0)
    # the bottleneck pointer moves from storage to the CPU
    term(x, [100, 140, 900, 560], "bottleneck", a)
    p = ease(x.since(0) / 1.5)
    x.rect([160, 230, 460, 330], MUTED, a, 2, r=6, glow=False)
    x.text((310, 280), "STORAGE", "monob", 30, MUTED, a, anchor="mm")
    chip_icon(x, 680, 420, 150, AMBER, a, 4, 4)
    x.text((680, 420), "CPU", "monob", 34, AMBER, a, anchor="mm")
    ax_, ay_ = 310 + (440 - 310) * p, 360 + (420 - 360) * p
    tick = int(x.t * 2) % 2
    x.text((ax_, ay_), "waiting on ->" if p > 0.5 else "waiting on", "monob", 28, RED, a, anchor="mm")
    x.text((680, 542), "clk " + ("1" if tick else "0"), "mono", 26, AMBER, a, anchor="mm")
    # next video card
    na = x.b(1)
    term(x, [960, 140, 1820, 560], "next.sh", na, AMBER)
    typed(x, (1000, 220), "$ ./next", 34, GREEN, na, x.since(1), 20, cursor=False)
    x.text((1000, 300), "How a CPU", "monob", 56, WHITE, na * ease(x.since(1) - 0.6))
    x.text((1000, 370), "Runs Your Code,", "monob", 56, WHITE, na * ease(x.since(1) - 0.8))
    x.text((1000, 450), "One Clock Cycle", "monob", 46, AMBER, na * ease(x.since(1) - 1.0))
    x.text((1000, 505), "at a Time", "monob", 46, AMBER, na * ease(x.since(1) - 1.0))
    sa = x.b(2)
    x.rect([760, 700, 1160, 800], RED, sa, 0, r=10, fill=RED + (255,), glow=False)
    x.text((960, 750), "[ SUBSCRIBE ]", "monob", 40, NAVY, sa, anchor="mm")


SCENES = [("One load screen, two drives", s_hook), ("What a load screen asks for", s_request),
          ("Inside a hard drive", s_hdd), ("The hard drive queue", s_hdd_load),
          ("SATA SSD: flash and a cable", s_sata), ("The big jump", s_sata_load),
          ("NVMe and PCIe lanes", s_nvme), ("Why faster isn't faster", s_bottleneck),
          ("Where SATA shows its age", s_console), ("DirectStorage", s_directstorage),
          ("The final race", s_race), ("Up next", s_outro)]
