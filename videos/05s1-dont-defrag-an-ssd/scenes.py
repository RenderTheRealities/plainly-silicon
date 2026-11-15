"""Short 05s1: why you shouldn't defrag an SSD (vertical, mint theme).
Flat, sticker-like illustrations: a spinning platter with scattered file pieces, a flash grid read all at once,
a wear meter that drains, and a TRIM pass that clears blocks."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540
PIECE = [(45, 212, 191), (253, 230, 138), (190, 242, 100), (251, 113, 133)]  # file colors


def ssd_card(x, cx, cy, a, w=620, h=220):
    """An M.2-style drive seen from above."""
    if a <= 0:
        return
    x0, y0 = cx - w / 2, cy - h / 2
    x.rect([x0, y0, x0 + w, y0 + h], CYAN, a, 5, r=18, fill=PANEL + (255,), glow=False)
    for k in range(3):
        bx = x0 + 150 + k * 150
        x.d.rounded_rectangle([bx, y0 + 40, bx + 120, y0 + h - 40], radius=8, fill=col(NAVY, a))
    x.d.rounded_rectangle([x0 + 30, y0 + 60, x0 + 110, y0 + h - 60], radius=6, fill=col(MUTED, a * 0.8))
    for k in range(10):
        x.d.rectangle([x0 + w - 6, y0 + 20 + k * 18, x0 + w + 14, y0 + 30 + k * 18], fill=col(AMBER, a * 0.8))
    x.circle(x0 - 26, cy, 16, MUTED, a, 4)


# ---------- scene 1: the question ----------
def s_hook(x):
    a = x.b(0)
    ssd_card(x, CX, 620, a)
    # a big "Defragment" button the viewer is tempted to press
    bob = 6 * math.sin(x.t * 4)
    x.rect([250, 900 + bob, 830, 1040 + bob], AMBER, a, 6, r=70, fill=NAVY + (255,), glow=False)
    x.text((CX, 970 + bob), "Defragment", "title", 58, AMBER, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.line([(250, 1040), (830, 900)], RED, a1, 14, glow=False)
        x.text((CX, 1170), "No.", "title", 96, RED, a1, anchor="mm")


# ---------- scene 2: hard drive fragments ----------
def platter(x, cx, cy, r, a, rot):
    x.circle(cx, cy, r, MUTED, a, 5, fill=PANEL)
    for k in range(1, 4):
        x.circle(cx, cy, r * k / 4, GRID, a, 3)
    x.circle(cx, cy, 26, WHITE, a, 0, fill=MUTED)
    # file pieces placed on different rings and angles
    spots = [(0.85, 0.3), (0.45, 2.2), (0.7, 4.1), (0.6, 5.3)]
    pos = []
    for k, (rr, ang) in enumerate(spots):
        th = ang + rot
        px, py = cx + r * rr * math.cos(th), cy + r * rr * math.sin(th)
        pos.append((px, py))
    return pos


def s_hdd(x):
    a = x.b(0)
    cx, cy, r = 470, 760, 300
    rot = x.t * 1.2
    pos = platter(x, cx, cy, r, a, rot)
    gather = ease(x.since(2) / 1.4) if x.t >= x.beats[min(2, len(x.beats) - 1)] else 0
    for k, (px, py) in enumerate(pos):
        tx, ty = 290 + k * 120, 1180
        qx, qy = px + (tx - px) * gather, py + (ty - py) * gather
        x.rect([qx - 50, qy - 32, qx + 50, qy + 32], PIECE[k], a, 4, r=8, fill=PIECE[k] + (255,), glow=False)
        x.text((qx, qy), str(k + 1), "title", 36, NAVY, a, anchor="mm")
    # read head arm, pivoting at the right, chasing the pieces in order during sentence 1
    a1 = x.b(1)
    piv = (900, 1080)
    if a1 > 0 and gather < 1:
        k = int(x.since(1) / 0.9) % 4
        tgt = pos[k]
        x.line([piv, tgt], WHITE, a1 * (1 - gather), 12, glow=False)
        x.circle(tgt[0], tgt[1], 18, AMBER, a1 * (1 - gather), 0, fill=AMBER)
        x.circle(piv[0], piv[1], 30, WHITE, a1 * (1 - gather), 0, fill=MUTED)
        x.text((CX, 1180), "jump, jump, jump...", "semi", 44, AMBER, a1 * (1 - gather), anchor="mm")
    if gather > 0:
        label_box(x, CX, 1080, "in a row = one sweep", GREEN, gather, 40)


# ---------- scene 3: SSD reads everywhere at once ----------
def s_flash(x):
    a = x.b(0)
    # controller on the left, 3x3 grid of flash cells on the right
    x.rect([110, 640, 300, 830], CYAN, a, 5, r=16, fill=NAVY + (255,), glow=False)
    x.text((205, 735), "ctrl", "title", 44, CYAN, a, anchor="mm")
    cells = []
    for r_ in range(3):
        for c_ in range(3):
            cells.append((440 + c_ * 180, 540 + r_ * 190))
    lit = {1: 0, 5: 1, 6: 2, 8: 3}  # scattered pieces of one file
    for i, (gx, gy) in enumerate(cells):
        k = lit.get(i)
        fillc = PIECE[k] if k is not None else PANEL
        x.rect([gx, gy, gx + 150, gy + 150], MUTED, a, 4, r=12, fill=fillc + (255,), glow=False)
    a1 = x.b(1)
    if a1 > 0:
        p = ease(x.since(1) / 0.6)
        for i, k in lit.items():
            gx, gy = cells[i]
            ex, ey = 300 + (gx + 75 - 300) * p, 735 + (gy + 75 - 735) * p
            x.line([(300, 735), (ex, ey)], WHITE, a1, 6, glow=False)
        # two equal bars: 1 piece vs 50 pieces
        bar(x, 160, 1110, 760, 0.92 * p, CYAN, a1, 44)
        bar(x, 160, 1225, 760, 0.90 * p, CYAN, a1, 44)
        x.text((160, 1092), "1 piece", "semi", 40, WHITE, a1, anchor="ld")
        x.text((160, 1207), "50 pieces", "semi", 40, WHITE, a1, anchor="ld")


# ---------- scene 4: wasted writes ----------
def s_wear(x):
    a = x.b(0)
    # blocks being copied from one spot to another, over and over
    for k in range(6):
        ph = (x.since(0) * 0.9 + k / 6) % 1
        y = 520 + k * 0
        sx = 170 + ph * 700
        sy = 560 + 120 * math.sin(ph * math.pi) * -1 + (k % 3) * 70
        x.rect([sx - 40, sy - 28, sx + 40, sy + 28], PIECE[k % 4], a, 3, r=6, fill=PIECE[k % 4] + (255,), glow=False)
    x.text((CX, 820), "rewrite, rewrite, rewrite", "semi", 44, MUTED, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        life = 1 - 0.45 * ease(x.since(1) / 2.5)
        x.text((160, 960), "Flash life", "title", 50, WHITE, a1, anchor="lm")
        x.d.rounded_rectangle([160, 1010, 920, 1090], radius=20, fill=col(GRID, a1))
        c = GREEN if life > 0.7 else AMBER
        x.d.rounded_rectangle([160, 1010, 160 + 760 * life, 1090], radius=20, fill=col(c, a1))
        x.text((920, 960), f"{int(life * 100)}%", "title", 50, c, a1, anchor="rm")
        label_box(x, CX, 1200, "zero speed gained", RED, a1, 40)


# ---------- scene 5: TRIM ----------
def s_trim(x):
    a = x.b(0)
    # a simple window: drive row with Optimize button
    x.rect([120, 450, 960, 760], WHITE, a, 4, r=18, fill=PANEL + (255,), glow=False)
    x.d.rounded_rectangle([120, 450, 960, 520], radius=18, fill=col(GRID, a))
    x.text((150, 485), "Optimize Drives", "semi", 36, WHITE, a, anchor="lm")
    x.text((160, 600), "C:  Solid state drive", "semi", 38, WHITE, a, anchor="lm")
    press = 1 if 0.8 < x.since(0) < 1.1 else 0
    x.rect([640, 650, 920, 730], CYAN, a, 4, r=14, fill=(CYAN if press else NAVY) + (255,), glow=False)
    x.text((780, 690), "Optimize", "semi", 36, NAVY if press else CYAN, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((CX, 830), "TRIM", "title", 80, AMBER, a1, anchor="mm")
    # blocks: deleted ones get marked free during sentence 1
    used = [1, 0, 1, 1, 0, 0, 1, 0]
    for k in range(8):
        bx = 150 + k * 100
        if used[k]:
            x.rect([bx, 930, bx + 80, 1010], CYAN, a, 3, r=8, fill=CYAN + (255,), glow=False)
        else:
            fr = ease((x.since(1) - k * 0.15) / 0.4) if a1 > 0 else 0
            x.rect([bx, 930, bx + 80, 1010], MUTED, a, 3, r=8, fill=MUTED + (255,) if fr < 0.5 else None, glow=False)
            if fr > 0:
                x.text((bx + 40, 1050), "free", "semi", 34, GREEN, fr, anchor="mm")
    if a1 > 0:
        label_box(x, CX, 1180, "not a defrag", GREEN, a1, 42)


# ---------- scene 6: outro ----------
def s_end(x):
    a = x.b(0)
    x.rect([150, 520, 510, 900], MUTED, a, 4, r=20, fill=PANEL + (255,), glow=False)
    x.circle(330, 690, 120, MUTED, a, 4, fill=GRID)
    x.text((330, 960), "HDD: defrag", "semi", 40, WHITE, a, anchor="mm")
    x.rect([570, 520, 930, 900], CYAN, a, 4, r=20, fill=PANEL + (255,), glow=False)
    for r_ in range(3):
        for c_ in range(3):
            x.d.rounded_rectangle([610 + c_ * 105, 560 + r_ * 110, 700 + c_ * 105, 650 + r_ * 110], radius=8, fill=col(CYAN, a * 0.7))
    x.text((750, 960), "SSD: TRIM", "semi", 40, CYAN, a, anchor="mm")
    label_box(x, CX, 1130, "SSD vs HDD vs NVMe", AMBER, a * ease(x.since(0) / 0.6 - 0.3), 44)


SCENES = [("Should you defrag an SSD?", s_hook), ("Hard drives: scattered pieces", s_hdd),
          ("SSDs: no moving parts", s_flash), ("Defrag only adds wear", s_wear),
          ("Windows sends TRIM", s_trim), ("The quick rule", s_end)]
