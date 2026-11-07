"""Short 01s21: why some USB ports are blue (vertical, technical-drawing style)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
PBLUE = (37, 112, 235)
PBLACK = (18, 20, 26)
PRED = (220, 52, 52)
PTEAL = (24, 196, 190)


def port(x, cx, cy, w, insert, a, label=None):
    """Front view of a USB-A receptacle: metal shell, colored tongue insert, contacts."""
    if a <= 0:
        return
    h = w * 0.4
    x0, y0 = cx - w / 2, cy - h / 2
    x.d.rectangle([x0, y0, x0 + w, y0 + h], fill=col((200, 210, 225), a))
    x.d.rectangle([x0 + 10, y0 + 10, x0 + w - 10, y0 + h - 10], fill=col((10, 14, 22), a))
    # tongue (the colored plastic) in the upper half
    x.d.rectangle([x0 + 24, y0 + 22, x0 + w - 24, y0 + h * 0.5], fill=col(insert, a),
                  outline=col((120, 130, 150), a) if sum(insert) < 120 else None, width=2)
    for k in range(4):
        px = x0 + 50 + k * (w - 100) / 3.6
        x.d.rectangle([px, y0 + h * 0.5, px + w * 0.11, y0 + h * 0.5 + 10], fill=col(AMBER, a))
    # blueprint dimension ticks
    x.line([(x0, y0 - 24), (x0 + w, y0 - 24)], MUTED, a * 0.7, 2, glow=False)
    x.line([(x0, y0 - 34), (x0, y0 - 14)], MUTED, a * 0.7, 2, glow=False)
    x.line([(x0 + w, y0 - 34), (x0 + w, y0 - 14)], MUTED, a * 0.7, 2, glow=False)
    if label:
        x.text((cx, y0 + h + 50), label, "title", 44, WHITE, a, anchor="mm")


def ss_logo(x, cx, cy, s, a, c=None):
    c = c or WHITE
    x.circle(cx, cy, s, c, a, 5)
    x.text((cx, cy + 2), "SS", "title", int(s * 0.95), c, a, anchor="mm")


def pipe(x, x0, y, w, thick, c, a, speed, n):
    """A data pipe with packets streaming through it at a given speed."""
    if a <= 0:
        return
    x.d.rounded_rectangle([x0, y - thick / 2, x0 + w, y + thick / 2], radius=thick / 2, outline=col(c, a), width=4)
    for k in range(n):
        u = (x.t * speed + k / n) % 1
        px = x0 + 20 + (w - 60) * u
        r = thick * 0.28
        x.d.rounded_rectangle([px, y - r, px + r * 2, y + r], radius=r * 0.4, fill=col(c, a))


def u_hook(x):
    a = x.b(0)
    port(x, CX, 560, 520, PBLACK, a, "black")
    port(x, CX, 940, 520, PBLUE, a, "blue")
    a1 = x.b(1)
    if a1 > 0:
        bob = 10 * math.sin(x.t * 4)
        x.text((900, 900 + bob), "?", "title", 160, AMBER, a1, anchor="mm")
        label_box(x, CX, 1200, "not decoration", AMBER, a1, 44)


def u_superspeed(x):
    a = x.b(0)
    port(x, 380, 560, 460, PBLUE, a)
    ss_logo(x, 830, 560, 80, x.b(0) * ease(x.since(0) / 0.6 - 2))
    x.text((380, 720), "USB 3", "title", 70, WHITE, a, anchor="mm")
    x.text((830, 690), "SuperSpeed", "semi", 36, CYAN, x.b(0) * ease(x.since(0) / 0.6 - 2), anchor="mm")
    a1 = x.b(1)
    pipe(x, 120, 930, 840, 150, CYAN, a1, 1.2, 6)
    x.text((CX, 1120), "up to 5 Gbps", "title", 76, AMBER, a1, anchor="mm")
    x.text((CX, 1200), "first-gen USB 3", "semi", 34, MUTED, a1, anchor="mm")


def u_compare(x):
    a = x.b(0)
    port(x, 270, 520, 300, PBLACK, a)
    x.text((520, 520), "USB 2", "title", 64, WHITE, a, anchor="lm")
    pipe(x, 120, 700, 840, 44, MUTED, a, 0.12, 3)
    a1 = x.b(1)
    x.text((960, 780), "480 Mbps", "title", 54, WHITE, a1, anchor="rm")
    port(x, 270, 920, 300, PBLUE, a1)
    x.text((520, 920), "USB 3", "title", 64, WHITE, a1, anchor="lm")
    pipe(x, 120, 1090, 840, 150, CYAN, a1, 1.2, 6)
    a2 = a1 * ease(x.since(1) / 0.6 - 2.5)
    stamp(x, 820, 1210, "~10x", AMBER, a2, angle=-6)


def u_convention(x):
    a = x.b(0)
    stamp(x, CX, 460, "CONVENTION", AMBER, a, angle=-4)
    a1 = x.b(1)
    cols = [(PRED, "red"), (PTEAL, "teal"), (PBLACK, "black")]
    for k, (c, name) in enumerate(cols):
        ab = a1 * ease((x.since(1) - k * 0.4) / 0.4)
        cy = 640 + k * 190
        port(x, 330, cy, 300, c, ab)
        x.text((560, cy), name, "title", 50, WHITE, ab, anchor="lm")
        x.text((900, cy), "fast?", "semi", 40, MUTED, ab, anchor="rm")
    a2 = x.b(2)
    if a2 > 0:
        x.rect([150, 1060, 930, 1240], GREEN, a2, 5, r=24, fill=NAVY + (240,), glow=False)
        ss_logo(x, 280, 1150, 62, a2, GREEN)
        x.text((390, 1120), "SS logo or manual", "title", 46, GREEN, a2, anchor="lm")
        x.text((390, 1185), "the better clue", "semi", 38, WHITE, a2, anchor="lm")


def u_plug(x):
    a = x.b(0)
    p = ease(x.since(0) / 1.4)
    # flash drive slides down into the blue port
    port(x, CX, 760, 460, PBLUE, a)
    dy = 420 + 200 * p
    x.d.rounded_rectangle([CX - 120, dy - 260, CX + 120, dy], radius=24, fill=col(PANEL, a), outline=col(WHITE, a), width=5)
    x.d.rectangle([CX - 90, dy, CX + 90, dy + 50], fill=col((200, 210, 225), a))
    x.text((CX, dy - 130), "SSD", "title", 54, CYAN, a, anchor="mm")
    a1 = x.b(1)
    q = x.since(1)
    bar(x, 160, 1000, 760, min(1.0, q / 1.5), CYAN, a1, h=44, label="blue port", value="done" if q > 1.5 else "")
    bar(x, 160, 1160, 760, min(1.0, q / 15), MUTED, a1, h=44, label="black port", value="copying...")


def u_end(x):
    a = x.b(0)
    port(x, CX, 680, 560, PBLUE, a)
    ss_logo(x, CX, 900, 60, a, CYAN)
    label_box(x, CX, 1120, "More PC hardware on the channel", CYAN, a, 38)


SCENES = [("Why are some USB ports blue?", u_hook), ("Blue = SuperSpeed", u_superspeed), ("About 10x faster", u_compare),
          ("Color isn't a guarantee", u_convention), ("Use the fast port", u_plug), ("Plainly Silicon", u_end)]
