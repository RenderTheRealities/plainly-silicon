"""Short 01s4: the one upgrade that revives an old PC (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def u_hook(x):
    a = x.b(0)
    x.rect([CX - 300, 480, CX + 300, 900], WHITE, a, 5, r=20)
    x.rect([CX - 260, 520, CX + 260, 820], MUTED, a, 3, r=8, glow=False)
    # loading spinner
    for k in range(10):
        ang = k * 2 * math.pi / 10 + x.t * 4
        x.circle(CX + 70 * math.cos(ang), 670 + 70 * math.sin(ang), 8, CYAN, a * (k / 10), 0, fill=CYAN)
    x.text((CX, 1050), "one upgrade beats the rest", "title", 50, AMBER, ease((x.t - 1.5) / 0.5), anchor="mm")


def u_hdd(x):
    a = x.b(0)
    cx, cy = CX, 760
    x.rect([cx - 300, cy - 260, cx + 300, cy + 260], WHITE, a, 5, r=24)
    x.circle(cx - 40, cy, 190, WHITE, a, 4)
    x.circle(cx - 40, cy, 24, WHITE, a, 4)
    ang = x.t * 8
    for k in range(3):
        aa = ang + k * 2.09
        x.line([(cx - 40 + 36 * math.cos(aa), cy + 36 * math.sin(aa)), (cx - 40 + 180 * math.cos(aa), cy + 180 * math.sin(aa))], WHITE, a * 0.35, 3, glow=False)
    arm = 0.4 * math.sin(x.t * 1.7) * x.b(1)
    ax, ay = cx + 230, cy + 190
    x.line([(ax, ay), (ax - 270 * math.cos(2.4 + arm), ay - 270 * math.sin(2.4 + arm))], AMBER, a, 8)
    x.text((CX, 1090), "Hard drive: moving parts", "title", 48, WHITE, a, anchor="mm")


def u_slow(x):
    a = x.b(0)
    x.text((CX, 680), "150–200", "title", 150, WHITE, a, anchor="mm")
    x.text((CX, 800), "MB/s", "monob", 60, MUTED, a, anchor="mm")
    p = ease(x.since(0) / 3)
    bar(x, 140, 1000, 800, p * 0.04, WHITE, a, 40, "HDD", "~180 MB/s")


def u_ssd(x):
    a = x.b(0)
    x.rect([CX - 320, 520, CX + 320, 680], CYAN, a, 5, r=12, fill=(17, 27, 46, 255))
    for i in range(4):
        x.rect([CX - 290 + i * 150, 550, CX - 170 + i * 150, 650], CYAN, a, 3, r=6, glow=False)
    x.text((CX, 740), "SSD: no moving parts", "title", 48, CYAN, a, anchor="mm")
    bar(x, 140, 900, 800, 0.04, WHITE, a, 36, "HDD", "~180 MB/s")
    bar(x, 140, 1010, 800, ease(x.since(1) / 1.2) * 0.11, CYAN, x.b(1), 36, "SATA SSD", "~550 MB/s")
    bar(x, 140, 1120, 800, ease(x.since(1) / 1.2) * (x.b(1)), CYAN, x.b(1), 36, "NVMe SSD", "thousands MB/s")


def u_end(x):
    for i, s in enumerate(["faster boot", "faster apps", "shorter loading"]):
        label_box(x, CX, 560 + i * 150, s, GREEN, ease((x.since(0) - i * 0.4) / 0.4), 50)
    label_box(x, CX, 1060, "still on a hard drive? start there", AMBER, x.b(1), 40)
    label_box(x, CX, 1190, "Full video on the channel", GREEN, x.b(2), 42)


SCENES = [("Slow old PC?", u_hook), ("The hard drive", u_hdd), ("How slow?", u_slow),
          ("The SSD", u_ssd), ("The result", u_end)]
