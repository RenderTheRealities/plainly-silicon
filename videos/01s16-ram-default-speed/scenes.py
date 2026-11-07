"""Short 01s16: RAM runs at its default speed until XMP/EXPO is turned on (vertical)."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def stick(x, a, cx, cy, w=760, h=200, label="DDR5-6000", glow_chip=0.0):
    """A RAM module seen from the front: PCB, memory chips, gold contacts, notch."""
    if a <= 0:
        return
    x0, y0 = cx - w / 2, cy - h / 2
    x.rect([x0, y0, x0 + w, y0 + h], WHITE, a, 5, r=8, fill=PANEL + (255,), glow=False)
    n = 8
    cw = (w - 170) / n
    for i in range(n):
        bx = x0 + 40 + i * (cw + 40 / n * 1.0)
        x.d.rectangle([bx, y0 + 30, bx + cw - 14, y0 + h - 70], fill=col(WHITE, a * 0.85))
    # gold contacts
    for k in range(0, int(w - 20), 16):
        if abs(x0 + 10 + k - (cx - 60)) < 14:
            continue  # key notch
        x.d.rectangle([x0 + 10 + k, y0 + h - 34, x0 + 20 + k, y0 + h - 6], fill=col(AMBER, a))
    # SPD chip (where the profiles live)
    sx, sy = x0 + w - 70, y0 + h - 58
    if glow_chip > 0:
        x.circle(sx, sy, 34 + 8 * math.sin(x.t * 5), CYAN, a * glow_chip, 5)
    x.d.rectangle([sx - 16, sy - 12, sx + 16, sy + 12], fill=col(CYAN, a))
    if label:
        x.text((cx, y0 - 46), label, "title", 64, WHITE, a, anchor="mm")


def r_hook(x):
    a0 = x.b(0)
    # the box
    x.rect([200, 440, 880, 860], CYAN, a0, 6, r=26, fill=PANEL + (255,), glow=False)
    x.text((CX, 540), "DDR5 MEMORY", "semi", 44, MUTED, a0, anchor="mm")
    x.text((CX, 680), "6000", "title", 190, CYAN, a0, anchor="mm")
    x.text((CX, 800), "MT/s", "semi", 46, MUTED, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        p = ease(x.since(1) / 0.6)
        x.line([(220, 770 - 0 * p), (220 + 640 * p, 590)], RED, a1, 12, glow=False)
        label_box(x, CX, 1040, "your PC:  ???", AMBER, a1, 60)


def r_default(x):
    a = x.b(0)
    x.text((CX, 450), "speed out of the box", "semi", 42, MUTED, a, anchor="mm")
    rows = [(1, "DDR5", 4800, 6000), (2, "DDR4", 2133, 3200)]
    for k, (beat, name, d, box) in enumerate(rows):
        ab = x.b(beat)
        if ab <= 0:
            continue
        y = 600 + k * 330
        x.text((140, y - 30), name, "title", 56, WHITE, ab, anchor="ls")
        # rated (ghost) vs default (filled)
        full = 800
        x.d.rounded_rectangle([140, y, 140 + full, y + 70], radius=35, fill=col(GRID, ab))
        x.d.rounded_rectangle([140, y, 140 + full, y + 70], radius=35, outline=col(MUTED, ab), width=3)
        f = d / box * ease(x.since(beat) / 1.2)
        if f > 0.05:
            x.d.rounded_rectangle([140, y, 140 + full * f, y + 70], radius=35, fill=col(AMBER, ab))
        x.text((140 + full, y + 120), f"box says {box}", "semi", 36, MUTED, ab, anchor="rm")
        x.text((150, y + 120), f"runs at {d}", "title", 44, AMBER, ab * ease(x.since(beat) / 1.2), anchor="lm")
    label_box(x, CX, 1200, "industry-standard default", CYAN, x.b(0) * x.b(1), 38)


def r_profile(x):
    a = x.b(0)
    stick(x, a, CX, 560, label="", glow_chip=a)
    # callout from SPD chip to a profile card
    sx, sy = CX + 380 - 70, 560 + 100 - 58
    x.line([(sx, sy + 30), (sx, 760), (CX + 160, 760)], CYAN, a, 4, glow=False)
    x.rect([180, 760, 900, 1120], CYAN, a, 4, r=20, fill=PANEL + (255,), glow=False)
    x.text((220, 810), "profiles on the stick", "semi", 34, MUTED, a, anchor="lm")
    x.text((220, 890), "Default", "monob", 44, WHITE, a, anchor="lm")
    x.text((860, 890), "4800", "monob", 44, WHITE, a, anchor="rm")
    ab = max(x.b(1), x.b(2))
    tag = "XMP" if x.b(2) < 0.5 else "XMP / EXPO"
    x.text((220, 980), tag, "monob", 44, CYAN, ab, anchor="lm")
    x.text((860, 980), "6000", "monob", 44, CYAN, ab, anchor="rm")
    # off switch
    a3 = x.b(3)
    tx, ty = 660, 1060
    if a3 > 0:
        x.d.rounded_rectangle([tx, ty - 30, tx + 120, ty + 30], radius=30, fill=col(MUTED, a3))
        x.circle(tx + 30, ty, 24, WHITE, a3, 2, fill=WHITE)
    x.text((tx - 20, ty), "OFF", "title", 40, RED, a3, anchor="rm")
    label_box(x, CX, 1210, "a tested overclock", AMBER, a3, 40)


def r_bios(x):
    a = x.b(0)
    # BIOS window
    x.rect([110, 420, 970, 900], CYAN, a, 4, r=8, fill=PANEL + (255,), glow=False)
    x.d.rectangle([110, 420, 970, 480], fill=col(CYAN, a))
    x.text((140, 450), "BIOS  >  Memory", "monob", 34, NAVY, a, anchor="lm")
    x.text((150, 560), "XMP / EXPO", "semi", 42, WHITE, a, anchor="lm")
    on = x.since(0) > 2.6
    x.rect([560, 520, 930, 600], AMBER if on else MUTED, a, 4, r=8, glow=False)
    x.text((745, 560), "Profile 1" if on else "Disabled", "monob", 38, GREEN if on else MUTED, a, anchor="mm")
    x.text((150, 680), "Memory speed", "semi", 38, MUTED, a, anchor="lm")
    x.text((930, 680), "6000" if on else "4800", "monob", 42, GREEN if on else WHITE, a, anchor="rm")
    if x.since(0) > 4.2:
        label_box(x, CX, 820, "Save & Exit", GREEN, ease((x.since(0) - 4.2) / 0.4), 36)
    # Task Manager card
    a1 = x.b(1)
    x.rect([180, 960, 900, 1230], WHITE, a1, 4, r=16, fill=PANEL + (255,), glow=False)
    x.text((220, 1010), "Task Manager  >  Memory", "semi", 34, MUTED, a1, anchor="lm")
    x.text((220, 1110), "Speed:", "semi", 50, WHITE, a1, anchor="lm")
    x.text((860, 1110), "6000 MT/s", "title", 64, GREEN, a1, anchor="rm")
    x.text((220, 1185), "check it here", "reg", 30, MUTED, a1, anchor="lm")


def r_end(x):
    a = x.b(0)
    stick(x, a, CX, 620, w=640, h=170, label="DDR5-6000")
    x.text((CX, 830), "crashes?", "title", 64, RED, a, anchor="mm")
    p = ease(x.since(0) / 0.8)
    tx, ty = 470, 940
    x.d.rounded_rectangle([tx, ty - 34, tx + 140, ty + 34], radius=34, fill=col(MUTED, a))
    x.circle(tx + 106 - 72 * p, ty, 28, WHITE, a, 2, fill=WHITE)
    x.text((CX, 1020), "turn it back off", "semi", 40, WHITE, a, anchor="mm")
    label_box(x, CX, 1180, "Full video: Every PC Component Explained", GREEN, x.b(1), 32)


SCENES = [("Is your RAM at full speed?", r_hook), ("The default speed", r_default),
          ("XMP and EXPO", r_profile), ("Turn it on", r_bios), ("If it crashes", r_end)]
