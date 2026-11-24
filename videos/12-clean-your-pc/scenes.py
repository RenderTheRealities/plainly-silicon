"""Scenes for video 12: How to Clean Your PC Without Breaking It.

Design language (mint theme): a soft, chunky "workshop manual" look. Thick rounded outlines,
flat filled shapes, no glow. Dust is always drawn as drifting speckles (seeded, so frames are
stable) that build up, fall and get blown out. Each danger gets a numbered red "WAY n" tab
along the top; safe actions get lime check badges, risky ones pink cross badges. The tower is
shown as a side cross-section with the front on the right.
"""
import math
import random
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def specks(x, box, n, a, seed=1, rmin=2, rmax=6, fall=0.0, c=None):
    """Deterministic dust speckles inside box. fall shifts them down (pixels)."""
    if a <= 0 or n <= 0:
        return
    rnd = random.Random(seed)
    x0, y0, x1, y1 = box
    for _ in range(int(n)):
        px, py = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.uniform(rmin, rmax)
        al = rnd.uniform(0.45, 0.95)
        sp = rnd.uniform(0.6, 1.4)
        py = py + fall * sp
        if py > y1 + 200:
            continue
        x.d.ellipse([px - r, py - r, px + r, py + r], fill=col(c or MUTED, a * al))


def fan(x, cx, cy, r, ang, c, a, w=4, frame=True):
    if a <= 0:
        return
    if frame:
        x.rect([cx - r * 1.12, cy - r * 1.12, cx + r * 1.12, cy + r * 1.12], c, a, w, r=r * 0.18,
               fill=PANEL + (255,), glow=False)
    x.circle(cx, cy, r, c, a, w)
    for k in range(7):
        th = ang + k * 2 * math.pi / 7
        pts = [(cx + r * 0.25 * math.cos(th), cy + r * 0.25 * math.sin(th)),
               (cx + r * 0.9 * math.cos(th + 0.2), cy + r * 0.9 * math.sin(th + 0.2)),
               (cx + r * 0.9 * math.cos(th + 0.62), cy + r * 0.9 * math.sin(th + 0.62)),
               (cx + r * 0.25 * math.cos(th + 0.5), cy + r * 0.25 * math.sin(th + 0.5))]
        x.d.polygon(pts, fill=col(c, a * 0.5))
    x.circle(cx, cy, r * 0.24, c, a, w, fill=PANEL)


def arrow(x, p0, p1, c, a, w=6, head=22):
    if a <= 0:
        return
    x.line([p0, p1], c, a, w, glow=False)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    pts = [p1, (p1[0] - head * math.cos(ang - 0.45), p1[1] - head * math.sin(ang - 0.45)),
           (p1[0] - head * math.cos(ang + 0.45), p1[1] - head * math.sin(ang + 0.45))]
    x.d.polygon(pts, fill=col(c, a))


def badge(x, cx, cy, ok, a, r=30):
    """Lime check badge (ok) or pink cross badge."""
    if a <= 0:
        return
    c = GREEN if ok else RED
    x.circle(cx, cy, r, c, a, 4, fill=c)
    if ok:
        x.line([(cx - r * 0.45, cy + r * 0.02), (cx - r * 0.1, cy + r * 0.38), (cx + r * 0.5, cy - r * 0.35)], NAVY, a, 7, glow=False)
    else:
        k = r * 0.4
        x.line([(cx - k, cy - k), (cx + k, cy + k)], NAVY, a, 7, glow=False)
        x.line([(cx - k, cy + k), (cx + k, cy - k)], NAVY, a, 7, glow=False)


def way_tab(x, n, label, a):
    """Red 'WAY n' danger tab at the top center."""
    if a <= 0:
        return
    f = font("title", 44)
    s = f"WAY {n}  ·  {label}"
    tw = x.d.textlength(s, font=f)
    x.d.rounded_rectangle([960 - tw / 2 - 34, 120, 960 + tw / 2 + 34, 196], radius=38, fill=col(RED, a))
    x.text((960, 158), s, "title", 44, NAVY, a, anchor="mm")


def note(x, xy, s, a, c=None, size=34, anchor="mm", kind="semi"):
    x.text(xy, s, kind, size, c or WHITE, a, anchor=anchor)


def card(x, box, a, c=None, fill=True):
    x.rect(box, c or MUTED, a, 4, r=26, fill=(PANEL + (255,)) if fill else None, glow=False)


def thermo(x, cx, top, h, frac, c, a, label):
    if a <= 0:
        return
    x.rect([cx - 26, top, cx + 26, top + h], WHITE, a, 5, r=26, fill=PANEL + (255,), glow=False)
    x.circle(cx, top + h + 30, 48, WHITE, a, 5, fill=c)
    lvl = top + h - (h - 20) * clamp(frac)
    x.d.rounded_rectangle([cx - 14, lvl, cx + 14, top + h + 10], radius=14, fill=col(c, a))
    note(x, (cx, top + h + 120), label, a, MUTED, 32)


def tower(x, x0, y0, w, h, a, dust=0.0, seed=3, fall=0.0, spin=1.0):
    """Side cross-section of a tower, front on the right. Returns key part boxes."""
    if a <= 0:
        return {}
    x.rect([x0, y0, x0 + w, y0 + h], WHITE, a, 6, r=28, fill=PANEL + (255,), glow=False)
    # motherboard plate
    mb = [x0 + 40, y0 + 40, x0 + w * 0.68, y0 + h * 0.62]
    x.rect(mb, MUTED, a * 0.7, 3, r=12, glow=False)
    # rear exhaust fan (top left)
    fr = h * 0.08
    fan(x, x0 + 40 + fr * 1.2, y0 + 70 + fr, fr, x.t * 4 * spin, CYAN, a, 3)
    # CPU cooler: fin stack
    cx0, cy0 = x0 + w * 0.32, y0 + h * 0.12
    cw, ch = w * 0.2, h * 0.3
    for k in range(9):
        fx = cx0 + k * cw / 8
        x.line([(fx, cy0), (fx, cy0 + ch)], WHITE, a, 4, glow=False)
    x.rect([cx0 - 10, cy0 + ch, cx0 + cw + 10, cy0 + ch + 24], AMBER, a, 3, r=6, fill=AMBER, glow=False)
    # RAM sticks
    for k in range(2):
        rx = x0 + w * 0.58 + k * 22
        x.rect([rx, y0 + h * 0.13, rx + 12, y0 + h * 0.4], CYAN, a, 3, r=3, fill=CYAN, glow=False)
    # GPU
    gpu = [x0 + 60, y0 + h * 0.5, x0 + w * 0.7, y0 + h * 0.6]
    x.rect(gpu, WHITE, a, 4, r=10, fill=NAVY + (255,), glow=False)
    gr = (gpu[3] - gpu[1]) * 0.36
    for k in (0.3, 0.7):
        fan(x, gpu[0] + (gpu[2] - gpu[0]) * k, (gpu[1] + gpu[3]) / 2, gr, -x.t * 5 * spin, MUTED, a, 2, frame=False)
    # PSU shroud + PSU
    sh = y0 + h * 0.74
    x.line([(x0 + 6, sh), (x0 + w - 6, sh)], MUTED, a, 4, glow=False)
    psu = [x0 + 40, sh + 24, x0 + w * 0.45, y0 + h - 30]
    x.rect(psu, WHITE, a, 4, r=10, fill=NAVY + (255,), glow=False)
    note(x, ((psu[0] + psu[2]) / 2, (psu[1] + psu[3]) / 2), "PSU", a, MUTED, 28, kind="title")
    # front intakes
    ir = h * 0.085
    fronts = []
    for k in range(3):
        fy = y0 + h * (0.18 + k * 0.22)
        fan(x, x0 + w - 30 - ir * 1.1, fy, ir, x.t * 4 * spin, CYAN, a, 3)
        fronts.append((x0 + w - 30 - ir * 1.1, fy))
    # dust
    if dust > 0:
        specks(x, [x0 + 20, y0 + 20, x0 + w - 20, y0 + h - 20], 260 * dust, a, seed, 2, 6, fall)
    return dict(cooler=[cx0, cy0, cx0 + cw, cy0 + ch], gpu=gpu, psu=psu, fronts=fronts, mb=mb,
                floor=[x0 + w * 0.5, sh + 20, x0 + w - 20, y0 + h - 20])


def can(x, cx, cy, ang, c, a, scale=1.0):
    """Compressed air can, rotated by ang (degrees, 0 = upright)."""
    if a <= 0:
        return
    s = scale
    layer = Image.new("RGBA", (int(220 * s), int(360 * s)), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    d.rounded_rectangle([50 * s, 90 * s, 170 * s, 340 * s], radius=26 * s, fill=col(c, a), outline=col(WHITE, a), width=int(5 * s))
    d.rectangle([80 * s, 50 * s, 140 * s, 92 * s], fill=col(WHITE, a))
    d.rectangle([140 * s, 58 * s, 200 * s, 70 * s], fill=col(WHITE, a))
    d.rectangle([62 * s, 170 * s, 158 * s, 240 * s], fill=col(NAVY, a))
    d.text((110 * s, 205 * s), "AIR", font=font("title", int(38 * s)), fill=col(WHITE, a), anchor="mm")
    layer = layer.rotate(-ang, expand=True, resample=Image.BICUBIC)
    x.img.paste(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)), layer)


# ---------- scenes ----------
def s_hook(x):
    # a tower gathering dust over six months
    a0 = x.b(0)
    p = clamp(x.t / 5)
    tower(x, 160, 190, 520, 620, a0, dust=0.15 + 0.85 * p, seed=11)
    months = 1 + int(5 * p)
    x.rect([250, 830, 590, 900], AMBER, a0, 4, r=34, fill=NAVY + (255,), glow=False)
    note(x, (420, 865), f"{months} month{'s' if months > 1 else ''} of dust", a0, AMBER, 34)
    # thermometers drop after cleaning
    a1 = x.b(1)
    d1 = ease(x.since(1) / 2.0)
    thermo(x, 920, 230, 420, lerp(0.85, 0.85 - 0.33, d1), RED if d1 < 0.5 else GREEN, a1, "Processor")
    thermo(x, 1150, 230, 420, lerp(0.7, 0.7 - 0.12, d1), RED if d1 < 0.5 else GREEN, a1, "Graphics card")
    note(x, (920, 190), f"-{int(round(11 * d1))} °C", a1, GREEN, 46, kind="title")
    note(x, (1150, 190), f"-{int(round(4 * d1))} °C", a1, GREEN, 46, kind="title")
    # three ways to break it
    a2 = x.b(2)
    labels = ["Static", "Spinning fans", "Going too deep"]
    for i, s in enumerate(labels):
        pa = ease((x.since(2) - i * 0.5) / 0.4) * a2
        y = 330 + i * 150
        x.rect([1350, y - 50, 1780, y + 50], RED, pa, 4, r=50, fill=NAVY + (255,), glow=False)
        x.circle(1405, y, 30, RED, pa, 4, fill=RED)
        note(x, (1405, y), str(i + 1), pa, NAVY, 36, kind="title")
        note(x, (1455, y), s, pa, WHITE, 38, anchor="lm")
    note(x, (1565, 210), "3 ways cleaning breaks PCs", a2, MUTED, 30)


def s_dust_matters(x):
    a0 = x.b(0)
    # heatsink fins
    fx0, fy0, fx1, fy1 = 720, 260, 1120, 700
    for k in range(11):
        xx = fx0 + k * (fx1 - fx0) / 10
        x.d.rounded_rectangle([xx - 7, fy0, xx + 7, fy1], radius=6, fill=col(WHITE, a0))
    x.rect([fx0 - 30, fy1, fx1 + 30, fy1 + 50], AMBER, a0, 4, r=10, fill=AMBER, glow=False)
    note(x, ((fx0 + fx1) / 2, fy1 + 25), "hot chip", a0, NAVY, 28, kind="title")
    # fan on the left
    a1 = x.b(1)
    blanket = ease(x.since(2) / 3.0) * x.b(2)
    fan(x, 420, 480, 150, x.t * (6 - 3 * blanket), CYAN, max(a0, a1))
    # airflow arrows: thin as dust builds
    flow = 1 - 0.7 * blanket
    for k in range(5):
        y = 300 + k * 90
        off = (x.t * 160 * flow + k * 40) % 120
        aa = a1 * (0.35 + 0.65 * flow)
        arrow(x, (600 + off, y), (680 + off, y), CYAN, aa, int(3 + 5 * flow), 18)
        # heat leaving on the right
        hx = 1150 + off
        x.line([(hx, y), (hx + 30, y - 12), (hx + 60, y)], AMBER, aa, 4, glow=False)
    # dust blanket on the fin intake side
    if blanket > 0:
        specks(x, [fx0 - 40, fy0, fx0 + 60, fy1], 220 * blanket, a0, 5, 3, 8)
        specks(x, [fx0, fy0, fx1, fy1], 90 * blanket, a0, 6, 2, 5)
        note(x, (fx0 + 10, fy0 - 40), "dust blanket", blanket, MUTED, 32)
    # temperature + clocks panel
    a3 = x.b(3)
    heat = ease(x.since(3) / 3)
    bar(x, 1380, 330, 400, lerp(0.5, 0.92, heat * a3), RED, a3, label="Chip temperature", value="hotter")
    a5 = x.b(5)
    drop = ease(x.since(5) / 2.5)
    bar(x, 1380, 480, 400, lerp(0.95, 0.7, drop), CYAN, a5, label="Boost clock", value="lower")
    bar(x, 1380, 630, 400, lerp(0.9, 0.66, drop), GREEN, a5, label="Frames per second", value="fewer")
    bar(x, 1380, 780, 400, lerp(0.35, 0.9, drop), AMBER, a5, label="Fan noise", value="louder")
    stamp(x, 960, 850, "DUSTY = SLOWER", RED, x.b(6), angle=-4)


def s_power_down(x):
    steps = [("Shut down in Windows", 1), ("Power supply switch to O", 2), ("Pull the power cord", 2),
             ("Hold power button 30 s", 3)]
    active = 0
    for i, (s, b) in enumerate(steps):
        extra = 1.6 if i == 2 else 0.0
        pa = ease((x.since(b) - extra) / 0.4) * x.b(b)
        done = ease((x.since(b) - extra - 1.4) / 0.3) * pa if i < 3 else ease((x.since(4) - 0.2) / 0.3)
        if pa > 0.5:
            active = i
        y = 260 + i * 140
        card(x, [140, y - 52, 760, y + 52], max(pa, 0.001) * x.b(0), CYAN if pa > 0.5 else MUTED)
        x.circle(200, y, 30, CYAN, pa, 4, fill=NAVY)
        note(x, (200, y), str(i + 1), pa, CYAN, 32, kind="title")
        note(x, (250, y), s, pa, WHITE, 32, anchor="lm")
        badge(x, 710, y, True, done)
    note(x, (450, 170), "Before you touch it", x.b(0), MUTED, 32)
    rx, ry = 1300, 470
    ill = x.b(1) * (1 - x.b(5))
    if active == 0:
        # shutdown icon
        x.circle(rx, ry, 160, CYAN, ill, 12)
        x.d.rectangle([rx - 40, ry - 200, rx + 40, ry - 90], fill=NAVY + (255,))
        x.line([(rx, ry - 190), (rx, ry - 40)], CYAN, ill, 14, glow=False)
    elif active == 1:
        # PSU back with rocker switch
        x.rect([rx - 280, ry - 180, rx + 280, ry + 180], WHITE, ill, 6, r=20, fill=PANEL + (255,), glow=False)
        for k in range(6):
            x.circle(rx - 120 + (k % 3) * 60, ry - 60 + (k // 3) * 60, 22, MUTED, ill, 3)
        flip = ease((x.since(2) - 0.6) / 0.4)
        x.rect([rx + 110, ry - 90, rx + 210, ry + 90], WHITE, ill, 5, r=10, fill=NAVY + (255,), glow=False)
        ty = lerp(ry - 85, ry + 5, flip)
        x.d.rounded_rectangle([rx + 118, ty, rx + 202, ty + 80], radius=8, fill=col(GREEN if flip > 0.5 else RED, ill))
        note(x, (rx + 160, ry - 125), "I", ill, MUTED, 36, kind="title")
        x.circle(rx + 160, ry + 125, 16, MUTED, ill, 4)
        note(x, (rx + 160, ry + 175), "O = off", ill * flip, GREEN, 30)
    elif active == 2:
        pull = ease((x.since(2) - 1.8) / 1.0)
        x.rect([rx - 300, ry - 100, rx - 120, ry + 100], WHITE, ill, 6, r=16, fill=PANEL + (255,), glow=False)
        for k in (-40, 0, 40):
            x.d.rectangle([rx - 230, ry + k - 8, rx - 190, ry + k + 8], fill=col(MUTED, ill))
        px = lerp(rx - 110, rx + 80, pull)
        x.rect([px, ry - 70, px + 150, ry + 70], CYAN, ill, 6, r=16, fill=CYAN, glow=False)
        x.line([(px + 150, ry), (px + 400, ry + 40)], CYAN, ill, 10, glow=False)
        note(x, (rx, ry + 190), "unplugged", ill * pull, GREEN, 34)
    else:
        # power button with 30 s ring
        p = clamp(x.since(3) / 4.0)
        x.circle(rx, ry, 150, MUTED, ill, 6, fill=PANEL)
        x.d.arc([rx - 190, ry - 190, rx + 190, ry + 190], -90, -90 + 360 * p, fill=col(AMBER, ill), width=16)
        x.circle(rx, ry, 70, CYAN, ill, 8)
        x.d.rectangle([rx - 18, ry - 90, rx + 18, ry - 40], fill=PANEL + (255,))
        x.line([(rx, ry - 85), (rx, ry - 20)], CYAN, ill, 10, glow=False)
        note(x, (rx, ry + 240), f"{int(round(30 * (1 - p)))} s left  ·  draining charge", ill, AMBER, 34)
    # where to clean
    a5 = x.b(5)
    for i, s in enumerate(["Garage", "Balcony", "Open window"]):
        pa = ease((x.since(6) - i * 0.4) / 0.4) * a5
        y = 300 + i * 170
        card(x, [1040, y - 60, 1560, y + 60], pa, GREEN)
        note(x, (1300, y), s, pa, WHITE, 40)
    note(x, (1300, 170), "Hard floor + fresh air", a5, GREEN, 36, kind="title")
    specks(x, [1600, 220, 1820, 800], 70 * a5, a5, 9, 3, 7, fall=-x.since(5) * 30 % 300)


def s_static(x):
    way_tab(x, 1, "STATIC", x.b(0))
    a1 = x.b(1)
    # finger approaching a chip with a spark
    chip_icon(x, 380, 520, 180, WHITE, a1 * (1 - x.b(2)), 5, pins=5)
    fx = lerp(760, 520, ease(x.since(1) / 1.2))
    x.rect([fx, 380, fx + 260, 450], AMBER, a1 * (1 - x.b(2)), 5, r=35, fill=PANEL + (255,), glow=False)
    if x.since(1) > 1.2 and x.b(2) < 1:
        for k in range(3):
            sx = 480 + k * 12
            pts = [(sx, 410), (sx - 30, 450), (sx - 5, 455), (sx - 40, 500)]
            x.line(pts, AMBER, a1 * (1 - x.b(2)), 5, glow=False)
        note(x, (380, 740), "a spark you can't see", a1 * (1 - x.b(2)), RED, 34)
    # floors
    a2 = x.b(2)
    card(x, [140, 300, 600, 560], a2 * (1 - x.b(5)), RED)
    for k in range(5):
        pts = [(170 + j * 20, 400 + k * 30 + 8 * math.sin(j)) for j in range(21)]
        x.line(pts, MUTED, a2 * (1 - x.b(5)), 3, glow=False)
    note(x, (370, 350), "Carpet", a2 * (1 - x.b(5)), WHITE, 36, kind="title")
    badge(x, 560, 340, False, a2 * (1 - x.b(5)))
    card(x, [140, 610, 600, 870], a2 * (1 - x.b(5)), GREEN)
    for k in range(4):
        for j in range(2):
            x.rect([170 + k * 105, 700 + j * 75, 260 + k * 105, 765 + j * 75], MUTED, a2 * (1 - x.b(5)), 3, r=4, glow=False)
    note(x, (370, 655), "Hard floor", a2 * (1 - x.b(5)), WHITE, 36, kind="title")
    badge(x, 560, 650, True, a2 * (1 - x.b(5)))
    # body charge draining into the case
    tx, ty = 1300, 520
    am = x.b(2) * (1 - x.b(5))
    x.rect([tx + 120, 300, tx + 480, 840], WHITE, am, 6, r=20, fill=PANEL + (255,), glow=False)
    note(x, (tx + 300, 570), "bare metal case", am, MUTED, 30)
    x.circle(tx - 160, ty - 120, 70, WHITE, am, 5)
    x.rect([tx - 240, ty - 40, tx - 80, ty + 260], WHITE, am, 5, r=60, glow=False)
    touch = ease((x.since(2) - 0.8) / 0.8)
    x.line([(tx - 90, ty + 20), (lerp(tx - 90, tx + 120, touch), ty + 20)], WHITE, am, 14, glow=False)
    charge = 1 - ease((x.since(2) - 1.6) / 1.5)
    rnd = random.Random(4)
    for k in range(10):
        cx_, cy_ = tx - 240 + rnd.uniform(20, 140), ty - 20 + rnd.uniform(10, 240)
        note(x, (cx_, cy_), "+", am * charge, AMBER, 40, kind="title")
    note(x, (tx - 160, ty + 320), "charge gone" if charge < 0.5 else "you, charged", am, GREEN if charge < 0.5 else AMBER, 32)
    # wrist strap
    a4 = x.b(4) * (1 - x.b(5))
    x.rect([tx - 270, ty + 150, tx - 50, ty + 200], GREEN, a4, 5, r=20, fill=GREEN, glow=False)
    x.line([(tx - 50, ty + 175), (tx + 40, ty + 240), (tx + 120, ty + 230)], GREEN, a4, 6, glow=False)
    note(x, (tx - 160, ty + 380), "wrist strap: even better", a4, GREEN, 32)
    # vacuum
    a5 = x.b(5)
    vx, vy = 760, 560
    x.d.polygon([(vx - 300, vy - 60), (vx + 120, vy - 30), (vx + 120, vy + 30), (vx - 300, vy + 60)],
                fill=col(PANEL, a5), outline=col(WHITE, a5))
    x.rect([vx - 520, vy - 110, vx - 290, vy + 110], WHITE, a5, 5, r=30, fill=PANEL + (255,), glow=False)
    rnd = random.Random(int(x.t * 6))
    for k in range(4):
        sx = vx + 140 + rnd.uniform(0, 80)
        sy = vy + rnd.uniform(-60, 60)
        x.line([(sx, sy - 30), (sx + 20, sy), (sx - 10, sy + 10), (sx + 15, sy + 40)], AMBER, a5, 4, glow=False)
    note(x, (vx - 100, vy + 140), "static builds in the nozzle", a5, AMBER, 32)
    tower(x, 1180, 300, 420, 520, a5, dust=0.4, seed=2)
    badge(x, 1390, 260, False, x.b(6))
    note(x, (1390, 870), "never inside the case", x.b(6), RED, 34, kind="title")


def s_filters(x):
    a0 = x.b(0)
    # front view of a case
    cx0, cy0, cw, ch = 220, 170, 460, 640
    x.rect([cx0, cy0, cx0 + cw, cy0 + ch], WHITE, a0, 6, r=24, fill=PANEL + (255,), glow=False)
    a1 = x.b(1)
    spots = [("Top", [cx0 + 30, cy0 - 30, cx0 + cw - 30, cy0 + 20]),
             ("Front", [cx0 + 40, cy0 + 60, cx0 + cw - 40, cy0 + ch - 150]),
             ("Under the PSU", [cx0 + 40, cy0 + ch - 20, cx0 + cw - 40, cy0 + ch + 30])]
    slide = ease((x.since(2) - 0.3) / 1.2) * x.b(2)
    for i, (s, b) in enumerate(spots):
        pa = ease((x.since(1) - i * 0.5) / 0.4) * a1
        if i == 1:
            b = [b[0] + slide * 620, b[1], b[2] + slide * 620, b[3]]
        x.rect(b, AMBER, pa, 4, r=10, fill=NAVY + (200,), glow=False)
        for gx in range(int(b[0]) + 10, int(b[2]) - 4, 18):
            x.line([(gx, b[1] + 8), (gx, b[3] - 8)], MUTED, pa * 0.5, 1, glow=False)
        if i == 1:
            specks(x, b, 120 * (1 - ease(x.since(3) / 2) * x.b(3)) * (1 - x.b(4)), pa, 21, 3, 7)
            note(x, ((b[0] + b[2]) / 2, b[3] + 30), "Front filter", pa * slide, AMBER, 30)
        else:
            note(x, (cx0 + cw + 30, (b[1] + b[3]) / 2), s, pa * (1 - slide), AMBER, 30, anchor="lm")
    # magnet / slide note
    note(x, (cx0 + cw / 2, cy0 + ch + 80), "slides out or pulls off (magnets)", x.b(2), MUTED, 30)
    # vacuum OK
    a3 = x.b(3) * (1 - x.b(4))
    x.rect([1380, 280, 1760, 360], GREEN, a3, 5, r=30, fill=NAVY + (255,), glow=False)
    note(x, (1570, 320), "vacuum OK out here", a3, GREEN, 32)
    badge(x, 1800, 320, True, a3)
    # water
    a4 = x.b(4)
    bx = 760
    x.rect([bx + 80, 180, bx + 340, 220], WHITE, a4, 5, r=12, fill=PANEL + (255,), glow=False)
    x.rect([bx + 300, 220, bx + 340, 280], WHITE, a4, 5, r=8, fill=PANEL + (255,), glow=False)
    for k in range(6):
        dy = (x.since(4) * 300 + k * 70) % 420
        x.d.ellipse([bx + 310, 290 + dy, bx + 330, 318 + dy], fill=col(CYAN, a4 * (1 - x.b(5))))
    # drying
    a5 = x.b(5)
    dry = ease(x.since(5) / 3.0)
    bar(x, 1100, 820, 600, dry, GREEN, a5, label="Drying", value=f"{int(dry * 100)}%")
    badge(x, 1760, 837, True, x.b(6) * (dry > 0.99))
    note(x, (1400, 750), "completely dry before it goes back in", x.b(6), GREEN, 30)


def s_air(x):
    way_tab(x, 2, "SPINNING FANS", x.b(0))
    # fan getting blasted
    a1 = x.b(1)
    hold = x.b(3)
    spin_rate = ease(x.since(1) / 2.0) * a1 * (1 - hold)
    ang = x.t * (2 + 40 * spin_rate)
    fan(x, 480, 520, 190, ang, CYAN, max(a1, 0.001) * x.b(0))
    for k in range(4):
        off = (x.t * 600 + k * 70) % 260
        x.line([(820 - off * 0.2 + 40, 380 + k * 80), (760 - off, 380 + k * 80)], WHITE, a1 * (1 - hold) * 0.7, 4, glow=False)
    rpm = int(1200 + spin_rate * 8800)
    rc = RED if rpm > 4000 else WHITE
    note(x, (480, 790), f"{rpm:,} rpm", a1 * (1 - hold), rc, 52, kind="title")
    note(x, (480, 845), "illustrative", a1 * (1 - hold), MUTED, 26)
    a2 = x.b(2) * (1 - hold)
    note(x, (480, 280), "worn bearings, cracked blades", a2, RED, 34)
    # finger holds it
    x.rect([440, 260, 520, 480], AMBER, hold, 5, r=38, fill=PANEL + (255,), glow=False)
    badge(x, 720, 340, True, hold)
    note(x, (480, 790), "hold it still", hold, GREEN, 52, kind="title")
    # bursts vs blast
    a4 = x.b(4)
    note(x, (1300, 270), "Short bursts", a4, GREEN, 34, anchor="lm")
    for k in range(4):
        x.d.rounded_rectangle([1300 + k * 90, 310, 1360 + k * 90, 340], radius=10, fill=col(GREEN, a4))
    note(x, (1300, 400), "One long blast", a4, RED, 34, anchor="lm")
    x.d.rounded_rectangle([1300, 440, 1690, 470], radius=10, fill=col(RED, a4 * 0.8))
    # distance ruler
    x.line([(1300, 560), (1690, 560)], WHITE, a4, 4, glow=False)
    for k in range(11):
        h = 24 if k % 5 == 0 else 12
        x.line([(1300 + k * 39, 560), (1300 + k * 39, 560 - h)], WHITE, a4, 3, glow=False)
    x.d.rectangle([1300 + 5 * 39, 545, 1300 + 10 * 39, 575], fill=col(GREEN, a4 * 0.35))
    note(x, (1495, 605), "5 to 10 cm away", a4, GREEN, 32)
    # can upright vs tilted
    a5 = x.b(5)
    can(x, 1210, 790, 0, CYAN, a5, 0.55)
    badge(x, 1290, 700, True, a5)
    a6 = x.b(6)
    tilt = ease(x.since(6) / 0.8)
    can(x, 1600, 790, 140 * tilt, CYAN, a6, 0.55)
    for k in range(5):
        dy = (x.since(6) * 200 + k * 30) % 120
        x.d.ellipse([1690 + k * 10, 740 + dy, 1702 + k * 10, 756 + dy], fill=col(AMBER, a6 * tilt))
    badge(x, 1740, 700, False, a6 * tilt)
    note(x, (1600, 900), "freezing liquid", a6 * tilt, RED, 30)


def s_order(x):
    a0 = x.b(0)
    a1 = x.b(1)
    clean = ease(x.since(5) / 1.5) * x.b(5)
    fall = x.since(1) * 120 * a1
    parts = tower(x, 160, 170, 620, 720, a0, dust=0.9 * (1 - clean), seed=13, fall=fall % 600 if a1 > 0 else 0)
    note(x, (470, 140), "Top down", a1, AMBER, 36, kind="title")
    for k in range(3):
        arrow(x, (830, 230 + k * 200), (830, 380 + k * 200), AMBER, a1, 8, 26)
    # inset: blow from the exit side
    a2 = x.b(2)
    ix0, iy0 = 1000, 210
    card(x, [ix0, iy0, ix0 + 780, iy0 + 420], a2, MUTED)
    for k in range(10):
        xx = ix0 + 230 + k * 34
        x.d.rounded_rectangle([xx, iy0 + 70, xx + 12, iy0 + 350], radius=5, fill=col(WHITE, a2))
    note(x, (ix0 + 150, iy0 + 40), "air in", a2, MUTED, 28)
    note(x, (ix0 + 640, iy0 + 40), "air out", a2, MUTED, 28)
    arrow(x, (ix0 + 60, iy0 + 210), (ix0 + 200, iy0 + 210), MUTED, a2, 5)
    arrow(x, (ix0 + 580, iy0 + 120), (ix0 + 720, iy0 + 120), MUTED, a2 * (1 - x.b(3)), 5)
    # nozzle from the out side, dust exits the in side
    a3 = x.b(3)
    push = x.since(3) * 220 * a3
    x.rect([ix0 + 660, iy0 + 260, ix0 + 770, iy0 + 300], CYAN, a3, 4, r=8, fill=CYAN, glow=False)
    arrow(x, (ix0 + 650, iy0 + 280), (ix0 + 590, iy0 + 280), CYAN, a3, 6)
    specks(x, [ix0 + 230, iy0 + 80, ix0 + 560, iy0 + 340], 90, a2, 31, 3, 6)
    if a3 > 0:
        rnd = random.Random(8)
        for _ in range(60):
            px = rnd.uniform(ix0 + 230, ix0 + 560) - (push % 520)
            py = rnd.uniform(iy0 + 80, iy0 + 340)
            if px > ix0 + 20:
                x.d.ellipse([px - 4, py - 4, px + 4, py + 4], fill=col(MUTED, a3))
    note(x, (ix0 + 390, iy0 + 390), "dust leaves the way it came in", a3, GREEN, 30)
    # numbered order
    a4 = x.b(4)
    if parts:
        spots = [(parts["fronts"][0][0], parts["fronts"][0][1] - 80, "Case fans"),
                 ((parts["cooler"][0] + parts["cooler"][2]) / 2, parts["cooler"][1] - 30, "Cooler"),
                 ((parts["gpu"][0] + parts["gpu"][2]) / 2, parts["gpu"][3] + 30, "Graphics card"),
                 ((parts["floor"][0] + parts["floor"][2]) / 2, (parts["floor"][1] + parts["floor"][3]) / 2, "Floor")]
        for i, (sx, sy, s) in enumerate(spots):
            pa = ease((x.since(4) - i * 0.6) / 0.4) * a4
            x.circle(sx, sy, 28, AMBER, pa, 4, fill=AMBER)
            note(x, (sx, sy), str(i + 1), pa, NAVY, 32, kind="title")
            note(x, (1040, 700 + i * 52), f"{i + 1}  {s}", pa, AMBER, 34, anchor="lm")
    note(x, (1560, 800), "about 10 minutes", x.b(5), GREEN, 40, kind="title")


def s_too_deep(x):
    way_tab(x, 3, "GOING TOO DEEP", x.b(0))
    cards = [(1, "Power supply", "never open it"), (4, "Graphics card", "don't take it apart"),
             (5, "CPU cooler", "lift it = new paste")]
    for i, (b, title, sub) in enumerate(cards):
        pa = x.b(b)
        cx = 360 + i * 600
        card(x, [cx - 250, 240, cx + 250, 700], pa, RED)
        note(x, (cx, 290), title, pa, WHITE, 40, kind="title")
        if i == 0:
            x.rect([cx - 140, 360, cx + 140, 560], WHITE, pa, 5, r=12, fill=NAVY + (255,), glow=False)
            for k in range(3):
                x.rect([cx - 110 + k * 80, 420, cx - 60 + k * 80, 520], MUTED, pa, 4, r=20, glow=False)
            bolt = x.b(2)
            pts = [(cx + 20, 330), (cx - 30, 450), (cx + 10, 450), (cx - 20, 580)]
            x.line(pts, AMBER, bolt * (0.6 + 0.4 * math.sin(x.t * 9)), 10, glow=False)
            note(x, (cx, 610), "holds a charge unplugged", bolt, AMBER, 28)
            vents = x.b(3)
            arrow(x, (cx + 230, 470), (cx + 150, 470), GREEN, vents, 6)
            note(x, (cx, 655), "blow through vents: OK", vents, GREEN, 28)
        elif i == 1:
            x.rect([cx - 200, 400, cx + 200, 500], WHITE, pa, 5, r=12, fill=NAVY + (255,), glow=False)
            for k in (-1, 1):
                fan(x, cx + k * 100, 450, 40, x.t * 3, MUTED, pa, 3, frame=False)
            for k in range(4):
                sx = cx - 160 + k * 105
                x.circle(sx, 380, 9, MUTED, pa, 3, fill=MUTED)
            note(x, (cx, 610), sub, pa, RED, 30)
        else:
            lift = ease((x.since(5) - 0.5) / 1.0)
            x.rect([cx - 120, 560, cx + 120, 600], AMBER, pa, 4, r=6, fill=AMBER, glow=False)
            x.d.ellipse([cx - 70, 535, cx + 70, 565], fill=col(MUTED, pa * lift))
            for k in range(8):
                fx = cx - 100 + k * 28
                x.line([(fx, 380 - 60 * lift), (fx, 520 - 60 * lift)], WHITE, pa, 5, glow=False)
            note(x, (cx, 650), sub, pa, RED, 30)
        badge(x, cx + 220, 260, False, pa)
    # motherboard & RAM: air only
    a6 = x.b(6)
    card(x, [360, 740, 1560, 880], a6, GREEN)
    note(x, (420, 810), "Motherboard + memory: air only", a6, GREEN, 36, anchor="lm", kind="title")
    badge(x, 1240, 810, True, a6)
    a7 = x.b(7)
    x.rect([1300, 790, 1420, 830], MUTED, a7, 4, r=8, fill=MUTED, glow=False)
    for k in range(6):
        x.line([(1420, 795 + k * 7), (1460, 785 + k * 11)], MUTED, a7, 3, glow=False)
    badge(x, 1500, 810, False, a7)


def s_grime(x):
    a0 = x.b(0)
    # sticky stain on a panel
    card(x, [140, 240, 900, 860], a0, MUTED)
    note(x, (520, 290), "sticky grime", a0, MUTED, 32)
    a1 = x.b(1)
    wipe = ease((x.since(1) - 1.0) / 2.5)
    stain = 1 - wipe * a1
    rnd = random.Random(17)
    for _ in range(40):
        sx, sy = rnd.uniform(300, 760), rnd.uniform(420, 680)
        r = rnd.uniform(12, 34)
        x.d.ellipse([sx - r, sy - r * 0.7, sx + r, sy + r * 0.7], fill=col(AMBER, a0 * 0.35 * stain))
    # bottle
    x.rect([200, 640, 300, 820], CYAN, a1, 5, r=16, fill=PANEL + (255,), glow=False)
    x.rect([225, 600, 275, 640], CYAN, a1, 4, r=6, fill=CYAN, glow=False)
    note(x, (250, 730), "IPA", a1, CYAN, 30, kind="title")
    # swab moving
    sw = lerp(320, 760, (math.sin(x.since(1) * 2.2) + 1) / 2)
    swy = lerp(450, 650, wipe)
    x.line([(sw, swy), (sw + 180, swy - 140)], WHITE, a1, 8, glow=False)
    x.d.ellipse([sw - 26, swy - 18, sw + 26, swy + 18], fill=col(WHITE, a1))
    for k in range(3):
        wy = 560 - ((x.since(1) * 60 + k * 50) % 150)
        wx = 520 + k * 90
        x.line([(wx, wy + 40), (wx + 12, wy + 20), (wx, wy), (wx + 12, wy - 20)], MUTED, a1 * wipe * 0.8, 3, glow=False)
    note(x, (520, 800), "wipe, then let it evaporate", a1, GREEN, 30)
    # don'ts
    donts = [(2, "Spraying into the case"), (3, "Bleach or ammonia cleaners"), (3, "Paper towels")]
    for i, (b, s) in enumerate(donts):
        pa = ease((x.since(b) - (0.9 if i == 2 else 0)) / 0.4) * x.b(b)
        y = 300 + i * 130
        card(x, [1000, y - 50, 1780, y + 50], pa, RED)
        badge(x, 1060, y, False, pa)
        note(x, (1110, y), s, pa, WHITE, 34, anchor="lm")
    # mask
    a4 = x.b(4)
    mx, my = 1390, 760
    x.d.rounded_rectangle([mx - 140, my - 70, mx + 140, my + 70], radius=50, fill=col(GREEN, a4))
    for k in (-1, 1):
        x.line([(mx + k * 140, my - 30), (mx + k * 230, my - 80)], GREEN, a4, 6, glow=False)
        x.line([(mx + k * 140, my + 30), (mx + k * 230, my + 60)], GREEN, a4, 6, glow=False)
    for k in range(3):
        x.line([(mx - 90, my - 30 + k * 30), (mx + 90, my - 30 + k * 30)], NAVY, a4, 4, glow=False)
    note(x, (mx, my + 120), "wear a dust mask", a4, GREEN, 34, kind="title")


def s_test(x):
    a0 = x.b(0)
    note(x, (960, 160), "Side panel still off: power on and look", a0, MUTED, 34)
    a1 = x.b(1)
    for i in range(4):
        cx = 360 + i * 400
        stuck = i == 2
        st = x.b(3)
        rate = 0 if stuck and st > 0 else 6
        fan(x, cx, 330, 100, x.t * rate + i, CYAN if not (stuck and st > 0) else RED, a1)
        ok = ease((x.since(2) - i * 0.3) / 0.3) * x.b(2)
        if stuck:
            badge(x, cx + 110, 220, True, ok * (1 - st))
            badge(x, cx + 110, 220, False, st)
            # loose cable
            sw = 20 * math.sin(x.t * 3)
            x.line([(cx + 60, 445), (cx + 80 + sw, 475), (cx + 50 + sw, 500)], RED, st, 6, glow=False)
            x.rect([cx + 30 + sw, 500, cx + 70 + sw, 525], RED, st, 4, r=4, fill=RED, glow=False)
            note(x, (cx + 190, 500), "loose cable?", st, RED, 30)
        else:
            badge(x, cx + 110, 220, True, ok)
    # temperature chart
    a4 = x.b(4)
    gx0, gy0, gx1, gy1 = 360, 640, 1560, 890
    am = a4 * (1 - x.b(3) * 0) * (x.since(4) > 0)
    if am > 0:
        x.d.rectangle([gx0 - 40, gy0 - 60, gx1 + 360, gy1 + 20], fill=col(NAVY, a4))
        x.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], MUTED, a4, 3, glow=False)
        note(x, (gx0, gy0 - 30), "CPU temperature, same game  (shape illustrative)", a4, MUTED, 28, anchor="lm")
        n = 60
        a5 = x.b(5)
        prog = ease(x.since(5) / 2.0)
        for which, base, c, aa, pr in [(0, 0.25, RED, a4, 1.0), (1, 0.62, GREEN, a5, prog)]:
            pts = []
            for k in range(int(n * pr) + 1):
                v = base + 0.05 * math.sin(k * 0.7 + which) + 0.03 * math.sin(k * 2.3)
                pts.append((gx0 + (gx1 - gx0) * k / n, gy0 + (gy1 - gy0) * v))
            if len(pts) > 1:
                x.line(pts, c, aa, 5, glow=False)
        note(x, (gx1 + 30, gy0 + (gy1 - gy0) * 0.25), "before", a4, RED, 32, anchor="lm")
        note(x, (gx1 + 30, gy0 + (gy1 - gy0) * 0.62), "after", a5 * prog, GREEN, 32, anchor="lm")
        a6 = x.b(6)
        mxp = gx0 + (gx1 - gx0) * 0.8
        arrow(x, (mxp, gy0 + (gy1 - gy0) * 0.3), (mxp, gy0 + (gy1 - gy0) * 0.57), AMBER, a6, 6)
        note(x, (mxp + 30, gy0 + (gy1 - gy0) * 0.44), "-11 °C for the tester", a6, AMBER, 34, anchor="lm", kind="title")


def s_keep_clean(x):
    a0 = x.b(0)
    # timeline of 12 months
    tx0, tx1, ty = 200, 1720, 250
    x.line([(tx0, ty), (tx1, ty)], WHITE, a0, 5, glow=False)
    for m in range(13):
        mx = tx0 + (tx1 - tx0) * m / 12
        x.line([(mx, ty - 12), (mx, ty + 12)], WHITE, a0, 3, glow=False)
        if m % 3 == 0:
            note(x, (mx, ty + 40), f"{m} mo", a0, MUTED, 24)
    p0 = ease(x.since(0) / 2)
    for m in range(0, 13, 2):
        mx = tx0 + (tx1 - tx0) * m / 12
        if m / 12 <= p0:
            x.rect([mx - 14, ty - 60, mx + 14, ty - 32], CYAN, a0, 3, r=4, fill=CYAN, glow=False)
    for m in (4, 8, 12):
        mx = tx0 + (tx1 - tx0) * m / 12
        if m / 12 <= p0:
            x.circle(mx, ty, 20, AMBER, a0, 4, fill=AMBER)
    note(x, (tx0, 150), "filters: every 1 to 2 months", a0, CYAN, 30, anchor="lm")
    note(x, (tx1, 150), "full clean: every 3 to 6 months", a0, AMBER, 30, anchor="rm")
    a1 = x.b(1)
    for m in (2, 5, 7, 10):
        mx = tx0 + (tx1 - tx0) * m / 12
        x.circle(mx, ty, 16, RED, a1, 4, fill=RED)
    note(x, (960, 330), "pets, smoke or dust: every 2 to 3 months", a1, RED, 30)
    # off the carpet
    a2 = x.b(0) * (1 - x.b(3))
    for k in range(4):
        pts = [(200 + j * 30, 830 + k * 18 + 6 * math.sin(j)) for j in range(20)]
        x.line(pts, MUTED, a2, 3, glow=False)
    lift = ease((x.since(2) - 0.3) / 0.8)
    tower(x, 330, lerp(470, 380, lift), 300, 360, a2, spin=0.5)
    x.rect([300, 760, 660, 790], WHITE, a2 * lift, 4, r=6, fill=PANEL + (255,), glow=False)
    note(x, (900, 600), "off the carpet", x.b(2) * (1 - x.b(3)), GREEN, 38, kind="title")
    # positive pressure diagram
    a3 = x.b(3)
    bx0, by0, bw, bh = 500, 410, 920, 460
    x.rect([bx0, by0, bx0 + bw, by0 + bh], WHITE, a3, 6, r=24, fill=PANEL + (255,), glow=False)
    a4 = x.b(3)
    for k in range(3):
        fy = by0 + 90 + k * 140
        x.rect([bx0 + bw - 20, fy - 60, bx0 + bw + 20, fy + 60], AMBER, a4, 3, r=6, fill=NAVY + (255,), glow=False)
        fan(x, bx0 + bw - 90, fy, 52, x.t * 5, CYAN, a4, 3)
        off = (x.t * 140 + k * 30) % 120
        arrow(x, (bx0 + bw + 160 - off, fy), (bx0 + bw + 80 - off, fy), GREEN, a4, 6, 20)
        specks(x, [bx0 + bw + 26, fy - 50, bx0 + bw + 50, fy + 50], 12, a4, 40 + k, 2, 4)
    fan(x, bx0 + 90, by0 + 110, 60, x.t * 4, CYAN, a4, 3)
    off = (x.t * 140) % 120
    arrow(x, (bx0 - 10 - off * 0.3, by0 + 110), (bx0 - 110 - off * 0.3, by0 + 110), AMBER, a4, 6, 20)
    note(x, (bx0 + bw + 200, by0 - 30), "3 in", a4, GREEN, 40, kind="title")
    note(x, (bx0 - 60, by0 + 30), "1 out", a4, AMBER, 40, kind="title")
    note(x, (bx0 + bw / 2, by0 + bh / 2), "slight positive pressure", a3, WHITE, 40, kind="title")
    a5 = x.b(5)
    # gaps: air pushes out through seams, not in
    for gx in (bx0 + 300, bx0 + 600):
        arrow(x, (gx, by0 + bh - 10), (gx, by0 + bh + 40), MUTED, a5, 4, 14)
    note(x, (bx0 + bw / 2, by0 + bh / 2 + 60), "air leaks out of the gaps, dust stays out", a5, GREEN, 30)


def s_outro(x):
    a0 = x.b(0)
    press = 1 - 0.08 * math.sin(clamp(x.since(0) / 0.4) * math.pi)
    r = 170 * press
    glow_r = 170 + 60 * ease(x.since(0) / 0.8)
    x.circle(560, 500, glow_r, CYAN, a0 * 0.4 * (1 - ease((x.since(0) - 0.8) / 1.0)), 10)
    x.circle(560, 500, r, WHITE, a0, 8, fill=PANEL)
    x.circle(560, 500, r * 0.45, CYAN, a0, 12)
    x.d.rectangle([560 - 22, 500 - r * 0.6, 560 + 22, 500 - r * 0.2], fill=PANEL + (255,))
    x.line([(560, 500 - r * 0.6), (560, 500 - r * 0.05)], CYAN, a0, 12, glow=False)
    note(x, (560, 730), "clean and cool", a0, CYAN, 36, kind="title")
    a1 = x.b(1)
    card(x, [880, 300, 1780, 620], a1, AMBER)
    note(x, (920, 350), "THIS SATURDAY", a1, AMBER, 28, anchor="lm", kind="title")
    note(x, (920, 430), "Every budget graphics", a1, WHITE, 48, anchor="lm", kind="title")
    note(x, (920, 495), "card, ranked", a1, WHITE, 48, anchor="lm", kind="title")
    for k, (t, c) in enumerate([("S", GREEN), ("A", CYAN), ("B", AMBER), ("SKIP", RED)]):
        pa = ease((x.since(1) - 0.6 - k * 0.2) / 0.3) * a1
        x.d.rounded_rectangle([920 + k * 200, 545, 920 + k * 200 + 170, 595], radius=12, fill=col(c, pa))
        note(x, (1005 + k * 200, 570), t, pa, NAVY, 30, kind="title")

SCENES = [
    ("Six months of dust", s_hook),
    ("Why dust slows you down", s_dust_matters),
    ("Power it down properly", s_power_down),
    ("Way 1: static", s_static),
    ("Dust filters first", s_filters),
    ("Way 2: spinning fans", s_air),
    ("The right order", s_order),
    ("Way 3: going too deep", s_too_deep),
    ("Sticky grime", s_grime),
    ("Test before closing", s_test),
    ("Keep it clean longer", s_keep_clean),
    ("This Saturday: budget GPUs", s_outro),
]
