"""Short 05s2: why a fast NVMe barely beats a SATA SSD on load screens (vertical, sand theme).
Visual language: flat workshop diagrams - pipes with flowing particles, measuring columns,
race lanes, and a conveyor belt where a CPU unpacks crates into level blocks."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def drive(x, cx, cy, kind, c, a, s=1.0):
    """Small drive icons: 'sata' (2.5-inch box), 'nvme' (M.2 stick), 'hdd' (platter)."""
    if kind == "sata":
        x.rect([cx - 70 * s, cy - 50 * s, cx + 70 * s, cy + 50 * s], c, a, 4, r=8, fill=PANEL + (255,), glow=False)
        x.rect([cx - 40 * s, cy - 20 * s, cx + 40 * s, cy + 20 * s], c, a, 3, r=4, glow=False)
    elif kind == "nvme":
        x.rect([cx - 90 * s, cy - 22 * s, cx + 90 * s, cy + 22 * s], c, a, 4, r=4, fill=PANEL + (255,), glow=False)
        for k in range(3):
            x.rect([cx - 70 * s + k * 50 * s, cy - 12 * s, cx - 34 * s + k * 50 * s, cy + 12 * s], c, a, 3, r=2,
                   fill=c, glow=False)
    else:
        x.rect([cx - 70 * s, cy - 55 * s, cx + 70 * s, cy + 55 * s], c, a, 4, r=8, fill=PANEL + (255,), glow=False)
        x.circle(cx, cy, 40 * s, c, a, 3)
        x.circle(cx, cy, 8 * s, c, a, 3, fill=c)


# ---------- 1: the hook - a thin pipe and a fat pipe, same loading bar ----------
def s_hook(x):
    a = x.b(0)
    rows = [("SATA", 500, 14, 1.0), ("NVMe", 760, 70, 13.5)]
    for name, y, h, rate in rows:
        x.text((80, y - h / 2 - 34), name, "title", 44, WHITE, a, anchor="ls")
        x.rect([80, y - h / 2, 1000, y + h / 2], MUTED, a, 3, r=h / 2 if h < 40 else 12, glow=False)
        # particles flowing through the pipe; density follows the rate
        n = int(4 + rate * 3)
        for k in range(n):
            px = 90 + ((x.t * 260 + k * 900 / n) % 900)
            py = y + (((k * 37) % 100) / 100 - 0.5) * (h - 14)
            x.circle(px, py, 5 if h < 40 else 8, CYAN, a, 0, fill=CYAN)
    x.text((CX, 640), "about 13x the speed", "semi", 40, AMBER, x.b(0) * ease((x.t - 1.5) / 0.5), anchor="mm")
    b = x.b(1)
    if b > 0:
        for k, (name, y0) in enumerate([("SATA", 960), ("NVMe", 1090)]):
            p = clamp(x.since(1) / 2.2)
            x.text((80, y0 - 10), name, "semi", 34, WHITE, b, anchor="ls")
            x.rect([80, y0, 1000, y0 + 50], WHITE, b, 3, r=10, glow=False)
            if p > 0.01:
                x.rect([84, y0 + 4, 84 + 912 * p, y0 + 46], CYAN, b, 0, r=8, fill=CYAN, glow=False)
        x.text((CX, 1210), "same load bar?", "title", 52, AMBER, b, anchor="mm")


# ---------- 2: rated speeds as measuring columns ----------
def s_speeds(x):
    a = x.b(0)
    base = 1180
    scale = 680 / 7450
    cols = [("SATA SSD", 550, 330, "sata", 0), ("PCIe 4.0", 7450, 750, "nvme", 1)]
    for label, mbps, cx, kind, beat in cols:
        ab = x.b(beat)
        if ab <= 0:
            continue
        p = ease(x.since(beat) / 1.6)
        hgt = max(6, mbps * scale * p)
        x.rect([cx - 110, base - hgt, cx + 110, base], CYAN, ab, 4, r=6, fill=CYAN if kind == "nvme" else AMBER, glow=False)
        x.text((cx, base - hgt - 40), f"{int(mbps * p):,} MB/s", "title", 44, WHITE, ab, anchor="mm")
        x.text((cx, base + 40), label, "semi", 36, WHITE, ab, anchor="mm")
    # ruler
    x.line([(130, base), (950, base)], WHITE, a, 4, glow=False)
    for v in range(0, 8001, 1000):
        yy = base - v * scale
        if yy < 440:
            break
        x.line([(110, yy), (130, yy)], MUTED, a, 3, glow=False)
    m = x.b(1) * ease((x.since(1) - 1.8) / 0.5)
    x.text((750, base - 60), "990 Pro", "semi", 36, PANEL, m, anchor="mm")


# ---------- 3: the race lanes ----------
def s_race(x):
    a = x.b(0)

    def lane(y, label, cx_, frac, c, al):
        x.text((80, y - 50), label, "semi", 34, WHITE, al, anchor="ls")
        x.line([(80, y + 30), (980, y + 30)], MUTED, al, 3, glow=False)
        px = 140 + 760 * frac
        x.rect([px - 60, y - 30, px + 60, y + 20], c, al, 4, r=10, fill=c, glow=False)
        x.circle(px - 32, y + 22, 12, WHITE, al, 0, fill=WHITE)
        x.circle(px + 32, y + 22, 12, WHITE, al, 0, fill=WHITE)

    # finish line
    for k in range(10):
        x.rect([970, 470 + k * 36, 988, 470 + k * 36 + 18], WHITE, a, 0, r=0, fill=WHITE, glow=False)
    x.text((CX, 430), "Cyberpunk save reload", "title", 44, AMBER, a, anchor="mm")
    p = ease(x.since(0) / 3.0)
    lane(560, "SATA", 0, p * 0.97, AMBER, a)
    lane(700, "NVMe", 0, p, CYAN, a)
    b = x.b(1)
    if b > 0:
        x.text((CX, 890), "Starfield", "title", 44, AMBER, b, anchor="mm")
        q = ease(x.since(1) / 2.5)
        lane(1010, "PCIe 3.0", 0, q * 0.96, AMBER, b)
        lane(1150, "PCIe 5.0", 0, q, CYAN, b)
        if q >= 1:
            label_box(x, CX, 1235, "less than 1 s apart", WHITE, b, 36)


# ---------- 4: the conveyor - the CPU unpacks every crate ----------
def crate(x, cx, cy, s, c, a):
    x.rect([cx - s, cy - s, cx + s, cy + s], c, a, 3, r=4, fill=PANEL + (255,), glow=False)
    x.line([(cx - s, cy - s), (cx + s, cy + s)], c, a, 3, glow=False)
    x.line([(cx - s, cy + s), (cx + s, cy - s)], c, a, 3, glow=False)


def conveyor(x, a, helpers):
    """Crates arrive from the drive at left, queue up, get unpacked by the chips, become level blocks."""
    y = 640
    drive(x, 120, y, "nvme", CYAN, a, 0.8)
    x.line([(200, y + 40), (560, y + 40)], WHITE, a, 4, glow=False)
    # queue of crates in front of the CPU grows with time (arrive fast, leave slowly)
    rate_out = 1.2 * len(helpers)
    q = int(clamp(x.t * (4.0 - rate_out), 0, 7))
    for k in range(q):
        crate(x, 520 - k * 46, y + 15, 18, AMBER, a)
    # moving crate on the belt
    px = 200 + (x.t * 400) % 300
    crate(x, px, y + 15, 18, AMBER, a)
    # unpacker chips
    for j, (name, cy) in enumerate(helpers):
        chip_icon(x, 660, cy, 120, CYAN if name == "CPU" else AMBER, a, 4, 4)
        x.text((660, cy), name, "title", 40, CYAN if name == "CPU" else AMBER, a, anchor="mm")
    # level being built from unpacked blocks
    built = int(clamp(x.t * rate_out, 0, 12))
    for k in range(built):
        bx, by = 820 + (k % 3) * 64, 1180 - (k // 3) * 64
        x.rect([bx, by - 56, bx + 56, by], GREEN, a, 3, r=4, fill=GREEN, glow=False)
    x.text((880, 1230), "level", "semi", 32, WHITE, a, anchor="mm")


def s_cpu(x):
    a = x.b(0)
    conveyor(x, a, [("CPU", 640)])
    b = x.b(1)
    x.text((330, 520), "crates wait here", "semi", 34, AMBER, b, anchor="mm")
    x.text((CX, 900), "drive done  ·  CPU still unpacking", "semi", 36, WHITE, b, anchor="mm")


# ---------- 5: DirectStorage hands unpacking to the GPU ----------
def s_gpu(x):
    a = x.b(0)
    conveyor(x, a, [("CPU", 600), ("GPU", 820)])
    x.text((CX, 470), "DirectStorage", "title", 46, AMBER, a, anchor="mm")
    b = x.b(1)
    if b > 0:
        x.rect([60, 940, 760, 1240], WHITE, b, 4, r=20, fill=PANEL + (255,), glow=False)
        for k, kind in enumerate(["sata", "nvme", "nvme"]):
            drive(x, 170 + k * 220, 1040, kind, CYAN, b, 0.8)
            x.text((170 + k * 220, 1110), ["SATA", "PCIe 4", "PCIe 5"][k], "semi", 30, WHITE, b, anchor="mm")
        x.text((410, 1190), "most games: any SSD", "title", 38, GREEN, b, anchor="mm")


# ---------- 6: outro ----------
def s_out(x):
    a = x.b(0)
    for k, (kind, nm) in enumerate([("hdd", "HDD"), ("sata", "SATA"), ("nvme", "NVMe")]):
        cy = 520 + k * 170
        ak = a * ease((x.since(0) - k * 0.25) / 0.4)
        drive(x, 400, cy, kind, CYAN, ak, 0.9)
        x.text((530, cy), nm, "title", 48, WHITE, ak, anchor="lm")
    x.text((CX, 1060), "SSD vs HDD vs NVMe", "title", 62, AMBER, a, anchor="mm")
    x.text((CX, 1150), "full video on the channel", "semi", 38, MUTED, a, anchor="mm")


SCENES = [("13x faster, same load?", s_hook), ("Rated speeds", s_speeds), ("The load-time race", s_race),
          ("Where the time goes", s_cpu), ("The exception", s_gpu), ("Every drive, raced", s_out)]
