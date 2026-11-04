"""Short 01s11: the tiny battery inside your PC (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def coin(x, cx, cy, r, a, c=None):
    c = c or CYAN
    if r < 6:
        return
    x.circle(cx, cy, r, c, a, 8)
    x.circle(cx, cy, r * 0.72, c, a, 3)
    x.text((cx, cy), "+", "title", int(r * 0.9), c, a, anchor="mm")


def f_hook(x):
    a = x.b(0)
    x.rect([180, 480, 560, 1060], WHITE, a, 5, r=16)
    x.line([(560, 940), (700, 940), (700, 1140), (900, 1140)], WHITE, a, 5, glow=False)
    coin(x, 370, 760, 90 * ease(x.since(0) / 0.8 - 0.8), a)
    x.text((CX, 1230), "a battery? in a desktop?", "semi", 40, WHITE, x.b(0), anchor="mm")


def f_coin(x):
    a = x.b(0)
    x.rect([160, 460, 920, 1100], MUTED, a, 3, r=14, glow=False)
    chip_icon(x, 380, 640, 150, MUTED, a, 3)
    coin(x, 700, 860, 140, a, AMBER)
    label_box(x, 700, 1170, "coin cell", AMBER, a, 40)


def clock(x, cx, cy, a, frozen=False):
    x.circle(cx, cy, 170, WHITE, a, 8)
    t = 0 if frozen else x.t
    for L, sp, w in ((120, 0.6, 6), (80, 0.05, 9)):
        ang = -math.pi / 2 + t * sp
        x.line([(cx, cy), (cx + L * math.cos(ang), cy + L * math.sin(ang))], WHITE, a, w, glow=False)


def f_job(x):
    clock(x, CX, 680, x.b(0))
    label_box(x, CX, 1000, "keeps the clock running", CYAN, x.b(0), 42)
    label_box(x, CX, 1120, "+ BIOS settings (many boards)", AMBER, x.b(0) * ease(x.since(0) / 0.6 - 2), 36)


def f_dead(x):
    a = x.b(1)
    coin(x, 270, 560, 80, x.b(0), RED)
    x.text((440, 560), "years later…", "semi", 40, MUTED, x.b(0), anchor="lm")
    blink = 1 if int(x.t * 2) % 2 == 0 else 0.15
    x.rect([200, 760, 880, 1000], RED, a, 5, r=14)
    x.text((CX, 880), "12:00  01/01", "monob", 80, RED, a * blink, anchor="mm")
    label_box(x, CX, 1130, "settings reset", RED, a, 40)


def f_fix(x):
    a = x.b(0)
    coin(x, 330, 720, 110, a, MUTED)
    x.line([(470, 720), (610, 720)], WHITE, a, 6)
    x.d.polygon([(610, 700), (640, 720), (610, 740)], fill=col(WHITE, a))
    coin(x, 760, 720, 110, a, GREEN)
    label_box(x, CX, 960, "unplug first · same type", GREEN, x.b(0), 40)
    label_box(x, CX, 1150, "More on the channel", GREEN, x.b(1), 40)


SCENES = [("The battery in your PC", f_hook), ("A coin cell", f_coin), ("What it does", f_job),
          ("When it dies", f_dead), ("The easy fix", f_fix)]
