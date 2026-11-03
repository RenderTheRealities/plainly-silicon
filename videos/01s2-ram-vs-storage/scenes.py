"""Short 01s2: RAM vs storage, desk vs filing cabinet (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def cabinet(x, cx, top, a):
    x.rect([cx - 180, top, cx + 180, top + 440], CYAN, a, 5, r=12)
    for i in range(4):
        y0 = top + 20 + i * 105
        x.rect([cx - 155, y0, cx + 155, y0 + 85], CYAN, a, 3, r=6, glow=False)
        x.line([(cx - 40, y0 + 42), (cx + 40, y0 + 42)], CYAN, a, 4, glow=False)


def desk(x, cx, top, a):
    x.rect([cx - 260, top, cx + 260, top + 50], AMBER, a, 5, r=8)
    x.line([(cx - 230, top + 50), (cx - 230, top + 240)], AMBER, a, 5)
    x.line([(cx + 230, top + 50), (cx + 230, top + 240)], AMBER, a, 5)


def q_hook(x):
    a = x.b(0)
    label_box(x, 300, 700, "RAM", AMBER, a, 64)
    label_box(x, 780, 700, "Storage", CYAN, ease((x.t - 0.4) / 0.4), 64)
    x.text((CX, 900), "?", "title", 260, WHITE, x.b(1), anchor="mm")


def q_cabinet(x):
    cabinet(x, CX, 470, x.b(0))
    x.text((CX, 990), "Storage = filing cabinet", "title", 52, CYAN, x.b(0), anchor="mm")
    x.text((CX, 1060), "huge · keeps data with power off", "semi", 36, WHITE, x.b(1), anchor="mm")
    label_box(x, CX, 1180, "but it's a walk away", AMBER, x.b(2), 40)


def q_desk(x):
    desk(x, CX, 650, x.b(0))
    x.text((CX, 990), "RAM = your desk", "title", 52, AMBER, x.b(0), anchor="mm")
    x.text((CX, 1060), "small · right in front of you", "semi", 36, WHITE, x.b(1), anchor="mm")
    label_box(x, CX, 1180, "nanoseconds away", GREEN, x.b(2), 40)


def q_move(x):
    a = x.b(0)
    cabinet(x, 290, 480, a)
    desk(x, 790, 640, a)
    wipe = x.b(1)
    for i in range(4):
        p = ease((x.since(0) - i * 0.35) / 0.8)
        sx, sy = 240, 510 + i * 105
        ex, ey = 600 + i * 95, 580
        fx = sx + (ex - sx) * p
        fy = sy + (ey - sy) * p - 140 * math.sin(math.pi * p)
        x.rect([fx, fy, fx + 80, fy + 50], WHITE, a * (1 - 0.85 * wipe), 3, r=6, fill=PANEL + (255,), glow=False)
    label_box(x, 790, 1000, "power off → desk wiped", RED, wipe, 36)
    label_box(x, 290, 1000, "cabinet keeps it", CYAN, x.b(2), 36)


def q_size(x):
    a = x.b(0)
    x0, y0, wbar = 140, 760, 800
    x.d.rounded_rectangle([x0, y0, x0 + wbar, y0 + 40], radius=20, fill=col(GRID, a))
    sa = x.b(1)
    x.d.rounded_rectangle([x0 + wbar * 0.33, y0, x0 + wbar * 0.66, y0 + 40], radius=20, fill=col(GREEN, sa))
    for gb, f in [(8, 0.0), (16, 0.33), (32, 0.66), (64, 1.0)]:
        x.text((x0 + wbar * f, y0 - 20), f"{gb} GB", "mono", 36, WHITE, a, anchor="md")
    x.text((CX, 880), "plenty for most gaming", "semi", 40, GREEN, sa, anchor="mm")
    label_box(x, CX, 1180, "Full video on the channel", GREEN, x.b(2), 42)


SCENES = [("RAM vs storage", q_hook), ("The filing cabinet", q_cabinet), ("The desk", q_desk),
          ("Opening a game", q_move), ("How much RAM?", q_size)]
