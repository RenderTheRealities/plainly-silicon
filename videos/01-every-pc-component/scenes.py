"""Scenes for video 01: Every PC Component Explained."""
import math
from render import *  # noqa: F401,F403  (drawing helpers and colors)

# ---------- scenes (one per narration paragraph) ----------
CX, CY = W / 2, 500


def s_hook(x):
    # game tile + cursor double click
    tile_a = x.b(0, 0.6)
    tx, ty = 960, 470
    x.rect([tx - 110, ty - 110, tx + 110, ty + 110], CYAN, tile_a, 5, r=36, fill=PANEL + (255,))
    x.d.polygon([(tx - 30, ty - 45), (tx - 30, ty + 45), (tx + 45, ty)], fill=col(CYAN, tile_a))
    x.text((tx, ty + 160), "Your game", "semi", 34, WHITE, tile_a, anchor="mm")
    # cursor glides in during first 1.2 s
    p = ease(x.t / 1.2)
    mx, my = 1500 + (tx + 30 - 1500) * p, 900 + (ty + 40 - 900) * p
    click = x.t > 1.2 and (x.t - 1.2) % 0.5 < 0.12 and x.t < 2.4
    cur_a = 1 - x.b(2)
    pts = [(mx, my), (mx, my + 52), (mx + 14, my + 40), (mx + 26, my + 64), (mx + 36, my + 59), (mx + 24, my + 36), (mx + 42, my + 36)]
    x.d.polygon(pts, fill=col(WHITE, cur_a), outline=col(NAVY, cur_a))
    if click:
        x.circle(mx, my, 40, CYAN, cur_a * 0.7, 3)
    # 3-second timer
    ta = x.b(1)
    secs = clamp(x.since(1) / 2.5) * 3.0
    x.text((960, 180), f"{secs:0.2f} s", "monob", 92, AMBER, ta, anchor="mm")
    # parts list lights up
    parts = ["Power supply", "Motherboard", "CPU", "Storage", "RAM", "Cache", "GPU", "Cooling"]
    la = x.b(2)
    if la > 0:
        for i, pname in enumerate(parts):
            pa = ease((x.since(2) - i * 0.35) / 0.4) * la
            col_x = 360 + (i % 4) * 400
            row_y = 760 + (i // 4) * 110
            label_box(x, col_x, row_y, pname, CYAN, pa, 34)


def s_psu(x):
    # wall outlet
    a0 = x.b(0)
    ox, oy = 260, 470
    x.rect([ox - 90, oy - 120, ox + 90, oy + 120], WHITE, a0, 4, r=24)
    for dx in (-30, 30):
        x.rect([ox + dx - 9, oy - 50, ox + dx + 9, oy - 10], WHITE, a0, 3, r=4, glow=False)
    x.circle(ox, oy + 50, 16, WHITE, a0, 3)
    x.text((ox, oy + 175), "Wall: ~120 V AC", "semi", 32, WHITE, a0, anchor="mm")
    # AC sine traveling into PSU
    a1 = x.b(0)
    pts = []
    for i in range(0, 361, 6):
        px = 380 + i
        pts.append((px, oy + 60 * math.sin((i / 60.0) - x.t * 6)))
    x.line(pts, AMBER, a1, 5)
    # PSU box
    a2 = x.b(2)
    px0, px1 = 800, 1180
    x.rect([px0, oy - 170, px1, oy + 170], CYAN, a2, 5, r=20, fill=PANEL + (255,))
    x.text(((px0 + px1) / 2, oy - 30), "POWER", "title", 54, CYAN, a2, anchor="mm")
    x.text(((px0 + px1) / 2, oy + 35), "SUPPLY", "title", 54, CYAN, a2, anchor="mm")
    # fan circle with rotating blades
    fcx, fcy = (px0 + px1) / 2, oy + 120
    # outputs: flat DC lines
    a3 = x.b(3)
    for j, (v, yy) in enumerate([("12 V", oy - 90), ("5 V", oy), ("3.3 V", oy + 90)]):
        aa = a3 * ease((x.since(3) - j * 0.3) / 0.4)
        x.line([(px1 + 20, yy), (1620, yy)], CYAN, aa, 5)
        x.text((1650, yy), v, "monob", 44, CYAN, aa, anchor="lm")
        # pulse dots
        k = ((x.t * 300) + j * 90) % 440
        x.circle(px1 + 20 + k, yy, 8, CYAN, aa, 0, fill=CYAN)
    x.text((1400, oy - 160), "Steady DC", "semi", 32, WHITE, a3, anchor="mm")
    # warning stamp on cheap PSUs
    sa = x.b(4) * (1 - x.b(6))
    stamp(x, 990, 820, "NEVER CHEAP OUT", AMBER, sa)
    # rating badge
    ba = x.b(6)
    label_box(x, 990, 820, "80 PLUS Bronze or better  +  headroom", GREEN, ba, 38)


def s_mobo(x):
    a = x.b(0)
    bx0, by0, bx1, by1 = 460, 150, 1460, 900
    x.rect([bx0, by0, bx1, by1], CYAN, a, 5, r=18, fill=PANEL + (255,))
    x.text((bx0 + 30, by0 + 30), "MOTHERBOARD", "monob", 30, CYAN, a)
    # components on the board
    ca = x.b(1)
    cpu = (760, 380)
    chip_icon(x, cpu[0], cpu[1], 160, WHITE, ca, 4)
    x.text((cpu[0], cpu[1]), "CPU", "title", 44, WHITE, ca, anchor="mm")
    ram = [(1010 + i * 50, 250, 1035 + i * 50, 560) for i in range(4)]
    for r_ in ram:
        x.rect(r_, AMBER, ca, 3, r=4, glow=False)
    x.text((1085, 590), "RAM slots", "semi", 28, AMBER, ca, anchor="mt")
    gpu_slot = (560, 690, 1240, 720)
    x.rect(gpu_slot, WHITE, ca, 3, r=6, glow=False)
    x.text((900, 740), "Graphics card slot (PCIe)", "semi", 28, WHITE, ca, anchor="mt")
    m2 = (560, 580, 720, 615)
    x.rect(m2, WHITE, ca, 3, r=6, glow=False)
    x.text((640, 625), "SSD slot (M.2)", "semi", 26, WHITE, ca, anchor="mt")
    # traces = roads, animated pulses
    ta = x.b(3)
    roads = [[(840, 380), (1010, 380)], [(710, 460), (710, 520), (640, 520), (640, 580)], [(800, 460), (800, 690)], [(840, 330), (930, 330), (930, 250)]]
    for k, rd in enumerate(roads):
        x.line(rd, CYAN, ta, 4)
        p = ((x.t * 0.8) + k * 0.25) % 1.0
        segs = list(zip(rd[:-1], rd[1:]))
        lens = [math.dist(a_, b_) for a_, b_ in segs]
        dist_ = p * sum(lens)
        for (a_, b_), L_ in zip(segs, lens):
            if dist_ <= L_ or (a_, b_) == segs[-1]:
                f_ = clamp(dist_ / L_ if L_ else 0)
                x.circle(a_[0] + (b_[0] - a_[0]) * f_, a_[1] + (b_[1] - a_[1]) * f_, 9, CYAN, ta, 0, fill=CYAN)
                break
            dist_ -= L_
    # UEFI chip + checklist
    ua = x.b(4)
    x.rect([1250, 760, 1400, 850], GREEN, ua, 4, r=8)
    x.text((1325, 805), "UEFI", "monob", 36, GREEN, ua, anchor="mm")
    checks = ["CPU", "RAM", "Storage", "Graphics", "Boot OS →"]
    for i, cname in enumerate(checks):
        aa = ease((x.since(6) - i * 0.4) / 0.4) if len(x.beats) > 6 else ease((x.since(5) - i * 0.4) / 0.4)
        y = 260 + i * 80
        x.text((1530, y), ("✓ " if i < 4 else "") + cname, "semi", 38, GREEN if i < 4 else WHITE, aa * ua)


def s_cpu(x):
    a = x.b(0)
    # signal path mouse -> board -> CPU
    nodes = [(220, 300, "Mouse"), (560, 300, "USB → board"), (960, 300, "CPU")]
    for i, (nx, ny, nm) in enumerate(nodes):
        na = ease((x.t - i * 0.5) / 0.5)
        label_box(x, nx, ny, nm, WHITE if i < 2 else CYAN, na, 34)
        if i:
            px = nodes[i - 1][0]
            x.line([(px + 110, ny), (nx - 110, ny)], CYAN, na, 3)
    # chip with cores
    ca = x.b(1)
    cx, cy, s = 760, 660, 330
    chip_icon(x, cx, cy, s, CYAN, ca, 5, pins=5)
    cores_a = x.b(4)
    for i in range(8):
        r_, c_ = divmod(i, 4)
        x0 = cx - 135 + c_ * 70
        y0 = cy - 100 + r_ * 110
        lit = 0.35 + 0.65 * (0.5 + 0.5 * math.sin(x.t * 5 + i * 1.3))
        x.rect([x0, y0, x0 + 55, y0 + 85], CYAN, cores_a * lit, 3, r=6, fill=CYAN + (int(70 * lit),), glow=False)
    x.text((cx, cy + 250), "8 cores = 8 workers", "semi", 32, WHITE, cores_a, anchor="mm")
    # clock counter
    ga = x.b(2)
    cyc = int(x.since(2) * 4_000_000_000)
    x.text((1440, 520), "4 GHz", "title", 96, AMBER, ga, anchor="mm")
    x.text((1440, 610), f"{cyc:,} cycles", "mono", 34, AMBER, ga, anchor="mm")
    x.text((1440, 660), "≈ 4 billion per second", "semi", 30, WHITE, ga, anchor="mm")
    # instruction list
    ia = x.b(5)
    for i, step in enumerate(["1  find the game", "2  load it", "3  start it"]):
        aa = ia * ease((x.since(5) - i * 0.35) / 0.4)
        x.text((1250, 770 + i * 60), step, "mono", 34, CYAN, aa)


def s_storage(x):
    a = x.b(1)
    # HDD
    ha = x.b(4)
    hx, hy = 520, 450
    x.rect([hx - 260, hy - 220, hx + 260, hy + 220], WHITE, ha, 4, r=20)
    x.circle(hx - 40, hy, 160, WHITE, ha, 3)
    x.circle(hx - 40, hy, 20, WHITE, ha, 3)
    ang = x.t * 8
    for k in range(3):
        aa = ang + k * 2.09
        x.line([(hx - 40 + 30 * math.cos(aa), hy + 30 * math.sin(aa)), (hx - 40 + 150 * math.cos(aa), hy + 150 * math.sin(aa))], WHITE, ha * 0.35, 2, glow=False)
    arm = 0.4 * math.sin(x.t * 1.7)
    ax, ay = hx + 200, hy + 160
    x.line([(ax, ay), (ax - 230 * math.cos(2.4 + arm), ay - 230 * math.sin(2.4 + arm))], AMBER, ha, 6)
    x.text((hx, hy - 260), "Hard drive (HDD)", "semi", 36, WHITE, ha, anchor="mm")
    # SSD
    sa = x.b(7)
    sx, sy = 1400, 450
    x.rect([sx - 300, sy - 70, sx + 300, sy + 70], CYAN, sa, 4, r=10, fill=PANEL + (255,))
    for i in range(4):
        x.rect([sx - 270 + i * 140, sy - 45, sx - 160 + i * 140, sy + 45], CYAN, sa, 3, r=6, glow=False)
    x.text((sx, sy - 120), "NVMe SSD (no moving parts)", "semi", 36, CYAN, sa, anchor="mm")
    # speed race
    ra = x.b(5)
    rp = ease(x.since(5) / 3)
    bar(x, 260, 730, 1400, rp * (180 / 5000), WHITE, ra, 34, "HDD", "~180 MB/s")
    sp = ease(x.since(8) / 1.5)
    bar(x, 260, 840, 1400, sp, CYAN, x.b(8), 34, "NVMe SSD", "~5,000 MB/s")
    # always-visible caption top
    x.text((960, 110), "Storage = long-term memory (keeps data with power off)", "semi", 36, WHITE, a, anchor="mm")
    ua = x.b(9)
    label_box(x, 1400, 610, "Biggest upgrade: HDD → SSD", GREEN, ua, 36)


def s_ram(x):
    # desk (RAM) left, cabinet (storage) right
    da = x.b(3)
    x.rect([200, 470, 860, 520], AMBER, da, 4, r=8)
    x.line([(250, 520), (250, 700)], AMBER, da, 4)
    x.line([(810, 520), (810, 700)], AMBER, da, 4)
    x.text((530, 740), "RAM = your desk", "title", 46, AMBER, da, anchor="mm")
    x.text((530, 790), "fast, forgets when power is off", "semi", 30, WHITE, da, anchor="mm")
    ca = x.b(0)
    x.rect([1260, 220, 1620, 700], CYAN, ca, 4, r=10)
    for i in range(4):
        y0 = 240 + i * 115
        x.rect([1285, y0, 1595, y0 + 95], CYAN, ca, 3, r=6, glow=False)
        x.line([(1400, y0 + 47), (1480, y0 + 47)], CYAN, ca, 4, glow=False)
    x.text((1440, 740), "Storage = filing cabinet", "title", 46, CYAN, ca, anchor="mm")
    x.text((1440, 790), "slower, remembers everything", "semi", 30, WHITE, ca, anchor="mm")
    # files sliding from cabinet to desk
    off = x.b(4) * (1 - x.b(5))  # power-off wipe between beats 4 and 5
    wiped = x.since(4) > 0.3 and x.t < x.beats[min(6, len(x.beats) - 1)]
    for i in range(5):
        p = ease((x.since(2) - i * 0.4) / 0.9)
        sx, sy = 1300 + (i % 2) * 120, 260 + i * 80
        ex, ey = 260 + i * 115, 410
        fx, fy = sx + (ex - sx) * p, sy + (ey - sy) * p - 120 * math.sin(math.pi * p)
        fa = x.b(2) * (0.15 if wiped else 1)
        x.rect([fx, fy, fx + 90, fy + 54], WHITE, fa, 3, r=6, fill=PANEL + (255,), glow=False)
    if wiped:
        label_box(x, 530, 360, "POWER OFF → desk cleared", RED, x.b(4), 32)
    # sizing bar
    sa = x.b(8)
    x0, y0, wbar = 360, 870, 1200
    x.d.rounded_rectangle([x0, y0, x0 + wbar, y0 + 30], radius=15, fill=col(GRID, sa))
    marks = [(8, 0.0), (16, 0.33), (32, 0.66), (64, 1.0)]
    x.d.rounded_rectangle([x0 + wbar * 0.33, y0, x0 + wbar * 0.66, y0 + 30], radius=15, fill=col(GREEN, sa))
    for gb, f in marks:
        x.text((x0 + wbar * f, y0 - 14), f"{gb} GB", "mono", 30, WHITE, sa, anchor="md")
    x.text((x0 + wbar * 0.495, y0 + 70), "comfortable for most gaming", "semi", 30, GREEN, sa, anchor="mm")


def s_cache(x):
    tiers = [("CACHE", "MB · on the chip · fastest", AMBER, 380),
             ("RAM", "GB · nanoseconds away", CYAN, 640),
             ("STORAGE", "TB · slowest · keeps data", WHITE, 900)]
    for i, (nm, sub, c, wd) in enumerate(tiers):
        a = x.b(1 if i == 0 else 4) * ease((x.since(1 if i == 0 else 4) - (i if i else 0) * 0.4) / 0.5) if i else x.b(1)
        if i:
            a = x.b(4) * ease((x.since(4) - (i - 1) * 0.4) / 0.5)
        y = 250 + i * 200
        x.rect([960 - wd, y, 960 + wd, y + 150], c, a, 5, r=14, fill=PANEL + (255,))
        x.text((960, y + 55), nm, "title", 58, c, a, anchor="mm")
        x.text((960, y + 112), sub, "semi", 30, WHITE, a, anchor="mm")
    aa = x.b(5)
    x.line([(250, 270), (250, 830)], WHITE, aa, 3, glow=False)
    x.text((230, 270), "faster", "semi", 28, WHITE, aa, anchor="rm")
    x.text((230, 830), "bigger, cheaper", "semi", 28, WHITE, aa, anchor="rm")


def s_gpu(x):
    # CPU: few big cores
    ca = x.b(2)
    x.text((480, 200), "CPU: a few smart cores", "semi", 36, WHITE, ca, anchor="mm")
    for i in range(8):
        r_, c_ = divmod(i, 4)
        x.rect([250 + c_ * 120, 270 + r_ * 150, 350 + c_ * 120, 390 + r_ * 150], WHITE, ca, 4, r=10, glow=False)
    # GPU: many tiny cores
    ga = x.b(3)
    x.text((1400, 200), "GPU: thousands of simple cores", "semi", 36, CYAN, ga, anchor="mm")
    cols_, rows_ = 32, 14
    gx, gy, cell = 1050, 260, 22
    pa = x.b(5)
    fill_p = clamp(x.since(5) / 1.2)
    for r_ in range(rows_):
        for c_ in range(cols_):
            x0, y0 = gx + c_ * cell, gy + r_ * cell
            lit = pa > 0 and fill_p >= 1 - 0.0001 or (pa > 0 and ((r_ * 7 + c_ * 13) % 100) / 100 < fill_p)
            if ga > 0:
                x.d.rectangle([x0, y0, x0 + cell - 5, y0 + cell - 5],
                              fill=col(CYAN, ga * (0.9 if lit else 0.18)))
    # pixels label
    x.text((1400, 600), "every pixel calculated at once", "semi", 30, WHITE, pa, anchor="mm")
    # VRAM block
    va = x.b(7)
    x.rect([1150, 680, 1650, 770], AMBER, va, 4, r=10)
    x.text((1400, 725), "VRAM: textures & models", "semi", 32, AMBER, va, anchor="mm")
    fa = x.b(8)
    label_box(x, 960, 860, "For gaming FPS, the GPU usually matters most", GREEN, fa, 36)


def s_cooling(x):
    a = x.b(0)
    cx, cy = 700, 640
    chip_icon(x, cx, cy, 240, CYAN, a, 5)
    # heat waves
    for k in range(3):
        ph = (x.t * 0.7 + k / 3) % 1.0
        y = cy - 150 - ph * 220
        pts = [(cx - 100 + i * 8, y + 12 * math.sin(i * 0.5 + x.t * 4)) for i in range(26)]
        x.line(pts, AMBER, a * (1 - ph), 4)
    x.text((cx, cy + 210), "100+ W of heat in a tiny chip", "semi", 32, WHITE, a, anchor="mm")
    # paste + fins
    pa = x.b(3)
    x.rect([cx - 140, cy - 165, cx + 140, cy - 150], WHITE, pa, 3, r=3, glow=False, fill=WHITE + (255,))
    x.text((cx + 170, cy - 158), "thermal paste", "semi", 26, WHITE, pa, anchor="lm")
    fa = x.b(4)
    for i in range(9):
        fx = cx - 140 + i * 35
        x.line([(fx, cy - 190), (fx, cy - 360)], CYAN, fa, 4, glow=False)
    # fan
    fcx, fcy = cx - 300, cy - 270
    x.circle(fcx, fcy, 90, CYAN, fa, 4)
    for k in range(4):
        ang = x.t * 10 + k * math.pi / 2
        x.line([(fcx, fcy), (fcx + 80 * math.cos(ang), fcy + 80 * math.sin(ang))], CYAN, fa, 5, glow=False)
    # throttling meters
    ta = x.b(7)
    th = ease(x.since(7) / 2.5)
    temp = 0.45 + 0.5 * th
    bar(x, 1150, 450, 560, temp, RED if temp > 0.85 else AMBER, ta, 34, "Temperature", f"{int(55 + 45 * th)}°C")
    bar(x, 1150, 600, 560, 1 - 0.35 * th, CYAN, ta, 34, "Clock speed", f"{4.8 - 1.6 * th:0.1f} GHz")
    label_box(x, 1430, 760, "thermal throttling", RED, ta * th, 34)


def s_case(x):
    a = x.b(0)
    x0, y0, x1, y1 = 560, 170, 1360, 900
    x.rect([x0, y0, x1, y1], WHITE, a, 5, r=24)
    # internal outlines
    ia = x.b(1)
    x.rect([640, 260, 1120, 640], CYAN, ia * 0.7, 3, r=8, glow=False)
    x.rect([650, 560, 1200, 610], AMBER, ia, 3, r=6, glow=False)
    x.rect([640, 760, 960, 870], WHITE, ia * 0.7, 3, r=8, glow=False)
    # airflow arrows front -> back
    for k in range(4):
        p = ((x.t * 0.5) + k * 0.25) % 1.0
        yy = 300 + k * 140
        ax = 420 + p * 1080
        x.line([(ax - 70, yy), (ax, yy)], CYAN, ia * (1 - abs(p - 0.5) * 1.4), 5)
        x.d.polygon([(ax, yy - 12), (ax + 22, yy), (ax, yy + 12)], fill=col(CYAN, ia * (1 - abs(p - 0.5) * 1.4)))
    x.text((960, 130), "Airflow: in the front, out the back", "semi", 34, CYAN, ia, anchor="mm")
    da = x.b(1)
    x.line([(650, 545), (1200, 545)], AMBER, da, 3, glow=False)
    x.text((925, 532), "max GPU length", "semi", 28, AMBER, da, anchor="md")
    x.line([(1440, 260), (1440, 640)], AMBER, da, 3, glow=False)
    x.text((1460, 450), "max cooler height", "semi", 28, AMBER, da, anchor="lm")


def s_replay(x):
    parts = [("PSU", "clean power"), ("Motherboard", "connects it all"), ("CPU", "runs your click"),
             ("SSD", "hands over files"), ("RAM", "holds them close"), ("Cache", "feeds the CPU"),
             ("GPU", "draws the frame"), ("Coolers", "keep it cool")]
    n = len(parts)
    for i, (nm, sub) in enumerate(parts):
        bi = min(i + 1, len(x.beats) - 1)
        a = 0.25 + 0.75 * x.b(bi)
        cx = 300 + (i % 4) * 440
        cy = 330 + (i // 4) * 330
        x.rect([cx - 190, cy - 110, cx + 190, cy + 110], CYAN, a, 4, r=18, fill=PANEL + (255,), glow=x.b(bi) > 0.5)
        x.text((cx, cy - 25), nm, "title", 48, CYAN if x.b(bi) > 0.5 else MUTED, a, anchor="mm")
        x.text((cx, cy + 40), sub, "semi", 28, WHITE, a, anchor="mm")
    fa = x.b(len(x.beats) - 1)
    x.text((960, 900), "3 seconds · 8 parts", "title", 64, AMBER, fa, anchor="mm")


def s_outro(x):
    a = x.b(0)
    x.text((960, 230), "Up next", "semi", 40, MUTED, a, anchor="mm")
    x.rect([460, 300, 1460, 720], CYAN, x.b(1), 5, r=26, fill=PANEL + (255,))
    x.text((960, 450), "Why your PC is slow", "title", 72, WHITE, x.b(1), anchor="mm")
    x.text((960, 550), "and why more RAM usually isn't the fix", "semi", 38, AMBER, x.b(1), anchor="mm")
    sa = x.b(2)
    x.rect([760, 820, 1160, 910], RED, sa, 0, r=45, fill=RED + (255,), glow=False)
    x.text((960, 865), "SUBSCRIBE", "title", 44, WHITE, sa, anchor="mm")


SCENES = [("One click, three seconds", s_hook), ("Power supply", s_psu), ("Motherboard", s_mobo),
          ("CPU", s_cpu), ("Storage", s_storage), ("RAM", s_ram), ("Cache", s_cache), ("GPU", s_gpu),
          ("Cooling", s_cooling), ("The case", s_case), ("Replay", s_replay), ("Up next", s_outro)]


