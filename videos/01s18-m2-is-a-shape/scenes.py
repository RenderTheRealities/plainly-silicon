"""Short 01s18: M.2 is a form factor, not a speed — SATA vs NVMe (vertical, retro)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def m2stick(x, a, x0, cy, w=620, h=150, keys="M", tint=None):
    """An M.2 stick lying horizontally: edge connector on the left, screw half-moon on the right."""
    if a <= 0:
        return
    tint = tint or CYAN
    y0, y1 = cy - h / 2, cy + h / 2
    x.d.rounded_rectangle([x0, y0, x0 + w, y1], radius=10, fill=col(PANEL, a), outline=col(tint, a), width=5)
    # controller + flash packages
    x.d.rectangle([x0 + 90, y0 + 32, x0 + 190, y1 - 32], fill=col(WHITE, a * 0.85))
    for k in range(2):
        bx = x0 + 230 + k * 160
        x.d.rectangle([bx, y0 + 24, bx + 130, y1 - 24], fill=col(MUTED, a * 0.9))
    # screw notch (half circle cut on the right end)
    x.d.ellipse([x0 + w - 26, cy - 26, x0 + w + 26, cy + 26], fill=col(NAVY, a))
    # gold fingers on the left edge, with notches
    notch_b = cy - h / 2 + h * 0.30   # B key position (one side)
    notch_m = cy + h / 2 - h * 0.25   # M key position (other side)
    fx = x0 - 34
    for k in range(int(h / 12)):
        fy = y0 + 6 + k * 12
        if "M" in keys and abs(fy + 4 - notch_m) < 12:
            continue
        if "B" in keys and abs(fy + 4 - notch_b) < 12:
            continue
        x.d.rectangle([fx, fy, x0, fy + 7], fill=col(CYAN, a))


def gauge(x, a, cx, cy, r, val, vmax, c, label):
    """A half-dial speedometer."""
    if a <= 0:
        return
    x.d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col(GRID, a), width=34)
    f = clamp(val / vmax)
    if f > 0.005:
        x.d.arc([cx - r, cy - r, cx + r, cy + r], 180, 180 + 180 * f, fill=col(c, a), width=34)
    ang = math.pi * (1 - f)
    x.line([(cx, cy), (cx + (r - 50) * math.cos(ang), cy - (r - 50) * math.sin(ang))], WHITE, a, 9, glow=False)
    x.circle(cx, cy, 16, WHITE, a, 0, fill=WHITE)
    x.text((cx, cy + 70), f"{int(val):,}", "title", 84, c, a, anchor="mm")
    x.text((cx, cy + 140), label, "semi", 34, MUTED, a, anchor="mm")


def s_hook(x):
    a = x.b(0)
    m2stick(x, a, 280, 520, keys="BM", tint=MUTED)
    m2stick(x, a, 280, 760, keys="M", tint=MUTED)
    x.text((140, 520), "?", "title", 80, WHITE, a, anchor="mm")
    x.text((140, 760), "?", "title", 80, WHITE, a, anchor="mm")
    # speed race bars under them
    p = ease((x.since(0) - 1.2) / 2.6)
    a2 = a * ease((x.since(0) - 1.0) / 0.4)
    bar(x, 160, 950, 760, 0.075 * p, AMBER, a2, h=56, label="drive A", value=f"{int(550 * p)} MB/s")
    bar(x, 160, 1130, 760, 1.0 * p, CYAN, a2, h=56, label="drive B", value=f"{int(7000 * p):,} MB/s")


def s_shape(x):
    a = x.b(0)
    # motherboard patch with M.2 socket and standoff
    x.d.rounded_rectangle([90, 560, 990, 980], radius=24, fill=col(GRID, a))
    x.d.rectangle([150, 690, 200, 850], fill=col(WHITE, a * 0.8))           # socket
    x.text((175, 650), "slot", "semi", 32, MUTED, a, anchor="mm")
    x.circle(860, 770, 20, CYAN, a, 4)                                       # standoff
    x.text((860, 610), "screw", "semi", 32, MUTED, a, anchor="mm")
    # stick slides in and drops flat
    p = ease(x.since(0) / 1.6)
    m2stick(x, a, 234 + (1 - p) * 220, 770 - (1 - p) * 140, w=626, h=140, keys="M")
    stamp(x, CX, 470, "SHAPE", CYAN, a * ease((x.since(0) - 1.6) / 0.5), angle=-5)
    a1 = x.b(1)
    x.line([(234, 1040), (860, 1040)], WHITE, a1, 4, glow=False)
    for xx in (234, 860):
        x.line([(xx, 1020), (xx, 1060)], WHITE, a1, 4, glow=False)
    x.text((CX, 1100), "22 mm wide  x  80 mm long", "title", 46, WHITE, a1, anchor="mm")
    label_box(x, CX, 1200, "says nothing about speed", AMBER, a1 * ease((x.since(1) - 1.0) / 0.5), 38)


def s_sata(x):
    a = x.b(0)
    # 2.5-inch SSD box and an M.2 stick, both feeding the same narrow SATA pipe
    x.rect([120, 450, 440, 690], WHITE, a, 5, r=14, fill=PANEL + (255,), glow=False)
    x.text((280, 570), "2.5-inch", "title", 46, WHITE, a, anchor="mm")
    x.rect([640, 510, 960, 630], AMBER, a, 5, r=10, fill=PANEL + (255,), glow=False)
    x.text((800, 570), "M.2 SATA", "title", 42, AMBER, a, anchor="mm")
    for sx in (280, 800):
        x.line([(sx, 700 if sx == 280 else 640), (sx, 760), (CX, 760)], MUTED, a, 8, glow=False)
    # narrow pipe
    x.d.rounded_rectangle([CX - 26, 760, CX + 26, 900], radius=10, fill=col(AMBER, a * 0.4))
    for k in range(3):
        yy = 760 + ((x.since(0) * 140 + k * 47) % 140)
        x.circle(CX, yy, 12, AMBER, a, 0, fill=AMBER)
    x.text((CX + 60, 830), "SATA", "title", 44, AMBER, a, anchor="lm")
    a1 = x.b(1)
    gauge(x, a1, CX, 1100, 170, 550 * ease(x.since(1) / 1.2), 7000, AMBER, "MB/s max")


def s_nvme(x):
    a = x.b(0)
    x.rect([290, 440, 790, 570], CYAN, a, 5, r=10, fill=PANEL + (255,), glow=False)
    x.text((540, 505), "M.2 NVMe", "title", 52, CYAN, a, anchor="mm")
    # four PCIe lanes with racing packets
    for k in range(4):
        lx = 330 + k * 140
        x.d.rounded_rectangle([lx - 22, 590, lx + 22, 830], radius=10, fill=col(CYAN, a * 0.35))
        for j in range(4):
            yy = 590 + ((x.since(0) * 420 + j * 60 + k * 23) % 240)
            x.circle(lx, yy, 11, CYAN, a, 0, fill=CYAN)
    x.text((CX, 870), "PCIe lanes", "semi", 40, MUTED, a, anchor="mm")
    a1 = x.b(1)
    s = x.since(1)
    v = 3500 * ease(s / 1.5) + 3500 * ease((s - 3.6) / 1.5)
    gauge(x, a1, CX, 1110, 170, v, 7000, CYAN, "PCIe 3.0  ->  newer" if s > 3.6 else "PCIe 3.0")


def s_keys(x):
    a = x.b(0)
    # big close-ups of the connector edges
    def edge(cx, keys, c, ab, name):
        if ab <= 0:
            return
        x.d.rounded_rectangle([cx - 190, 520, cx + 190, 900], radius=12, fill=col(PANEL, ab), outline=col(c, ab), width=5)
        top = 900
        fingers = 15
        fw = 380 / fingers
        for k in range(fingers):
            fx = cx - 190 + k * fw
            if "B" in keys and k in (3,):
                continue
            if "M" in keys and k in (11,):
                continue
            x.d.rectangle([fx + 4, top, fx + fw - 4, top + 70], fill=col(CYAN, ab))
        x.text((cx, 600), name, "title", 54, c, ab, anchor="mm")
        if "B" in keys:
            x.text((cx - 190 + 3.5 * fw, top + 120), "B", "title", 50, WHITE, ab, anchor="mm")
        if "M" in keys:
            x.text((cx - 190 + 11.5 * fw, top + 120), "M", "title", 50, WHITE, ab, anchor="mm")
    edge(285, "BM", AMBER, x.b(1), "SATA")
    edge(795, "M", CYAN, x.b(2), "NVMe")
    x.text((CX, 470), "count the notches", "semi", 40, MUTED, a * (1 - x.b(1)), anchor="mm")
    a3 = x.b(3)
    x.rect([170, 1110, 910, 1230], WHITE, a3, 4, r=12, fill=PANEL + (255,), glow=False)
    x.text((210, 1170), "Interface:", "semi", 40, MUTED, a3, anchor="lm")
    x.text((870, 1170), "PCIe 4.0 NVMe", "monob", 42, GREEN, a3, anchor="rm")


def s_manual(x):
    a = x.b(0)
    # open manual with a slot table
    x.d.rounded_rectangle([110, 440, 970, 1080], radius=18, fill=col(WHITE, a * 0.95))
    x.line([(CX, 460), (CX, 1060)], MUTED, a, 3, glow=False)
    x.text((320, 500), "MANUAL", "title", 40, NAVY, a, anchor="mm")
    x.text((760, 500), "M.2 slots", "title", 40, NAVY, a, anchor="mm")
    rows = [("M2_1", "NVMe", True, False), ("M2_2", "NVMe", True, False), ("M2_3", "NVMe/SATA", True, True)]
    for k, (slot, kinds, ok, sat) in enumerate(rows):
        ab = a * ease((x.since(0) - 0.6 - k * 0.6) / 0.4)
        y = 620 + k * 140
        x.text((170, y), slot, "monob", 46, NAVY, ab, anchor="lm")
        x.text((600, y), kinds, "monob", 38, PANEL, ab, anchor="lm")
        x.line([(150, y + 60), (930, y + 60)], MUTED, ab * 0.6, 2, glow=False)
    # highlight the SATA-capable row
    hp = ease((x.since(0) - 3.0) / 0.5)
    x.rect([575, 862, 950, 938], AMBER, a * hp, 6, r=10, glow=False)
    label_box(x, CX, 1190, "More PC hardware on the channel", CYAN, x.b(1), 36)


SCENES = [("Same shape. Same speed?", s_hook), ("M.2 is a shape", s_shape), ("Some are SATA", s_sata),
          ("Some are NVMe", s_nvme), ("Read the notches", s_keys), ("Check your slots", s_manual)]
