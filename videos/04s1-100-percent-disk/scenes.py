"""Short 04s1: what "Disk 100%" in Task Manager really measures (vertical, circuit theme).
Visual language: a big ring gauge, a one-second busy/idle tape, a top-down hard drive platter with a
swinging arm, and a request queue that never drains."""
import math
from render import *  # noqa: F401,F403

SIZE = (1080, 1920)
CX = 540


def ring(x, cx, cy, r, frac, c, a, w=34):
    """Thick circular gauge, filling clockwise from 12 o'clock."""
    if a <= 0:
        return
    x.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col(GRID, a), width=w)
    if frac > 0.003:
        x.d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * frac, fill=col(c, a), width=w)


def tape(x, y, busy, a, label, p=1.0, c=None):
    """A one-second strip split into 20 slots; busy(k) says if slot k was busy. p reveals left to right."""
    c = c or AMBER
    x0, x1, h = 110, 970, 110
    n = 20
    sw = (x1 - x0) / n
    shown = int(n * clamp(p) + 0.999)
    for k in range(n):
        bx = x0 + k * sw
        on = k < shown and busy(k)
        if k < shown:
            x.d.rectangle([bx + 3, y, bx + sw - 3, y + h], fill=col(c if on else PANEL, a))
        x.d.rectangle([bx + 3, y, bx + sw - 3, y + h], outline=col(GRID, a), width=2)
    x.text((x0, y - 18), label, "semi", 38, MUTED, a, anchor="ld")
    x.text((x0, y + h + 22), "0 s", "mono", 30, MUTED, a, anchor="la")
    x.text((x1, y + h + 22), "1 s", "mono", 30, MUTED, a, anchor="ra")
    busy_n = sum(1 for k in range(shown) if busy(k))
    return int(round(100 * busy_n / n))


# ---------- scene 1: 100% but not full ----------
def s_hook(x):
    a = x.b(0)
    p = ease(x.since(0) / 1.2)
    ring(x, CX, 690, 220, p, RED, a)
    x.text((CX, 665), f"{int(100 * p)}%", "title", 120, WHITE, a, anchor="mm")
    x.text((CX, 760), "DISK", "semi", 44, MUTED, a, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        # the drive's capacity bar: mostly empty
        x.rect([150, 1030, 930, 1110], CYAN, a1, 4, r=16, fill=PANEL + (255,), glow=False)
        x.d.rounded_rectangle([156, 1036, 156 + 778 * 0.31, 1104], radius=12, fill=col(CYAN, a1 * 0.8))
        x.text((CX, 1160), "drive space: 69% free", "semi", 44, CYAN, a1, anchor="mm")
        x.text((CX, 1230), "so what's at 100?", "title", 52, AMBER, a1, anchor="mm")


# ---------- scene 2: active time ----------
def s_active(x):
    a = x.b(0)
    pattern = [1, 1, 0, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0]
    p = clamp(x.since(0) / 3.0)
    pct = tape(x, 560, lambda k: pattern[k], a, "busy or idle, every 50 ms", p)
    x.text((CX, 830), f"active time {pct}%", "title", 78, AMBER, a, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        # free space is a different question entirely
        x.rect([230, 960, 850, 1150], MUTED, a2, 4, r=20, fill=PANEL + (255,), glow=False)
        x.text((CX, 1020), "free space?", "semi", 50, MUTED, a2, anchor="mm")
        x.text((CX, 1095), "not measured here", "semi", 44, MUTED, a2, anchor="mm")
        x.line([(250, 1150), (830, 960)], RED, a2, 6, glow=False)


# ---------- scene 3: inside a hard drive ----------
def s_hdd(x):
    a = x.b(0)
    pcx, pcy, R = 470, 790, 300
    x.rect([130, 460, 950, 1120], MUTED, a, 4, r=30, fill=PANEL + (255,), glow=False)
    x.circle(pcx, pcy, R, CYAN, a, 4, fill=NAVY)
    for rr in (240, 180, 120):
        x.circle(pcx, pcy, rr, GRID, a, 2)
    x.circle(pcx, pcy, 40, CYAN, a, 4, fill=PANEL)
    # a data block spinning around on a track
    ang = x.t * 2.2
    trk = [270, 210, 150][int(x.since(0) / 1.6) % 3]
    bx, by = pcx + trk * math.cos(ang), pcy + trk * math.sin(ang)
    x.d.rounded_rectangle([bx - 22, by - 22, bx + 22, by + 22], radius=6, fill=col(AMBER, a))
    # the arm: pivot bottom right, swings between tracks
    a1 = x.b(1)
    px, py = 860, 1080
    target = [270, 210, 150][int(x.since(1) / 1.6) % 3] if a1 > 0 else 270
    # point on the 9-o'clock-ish side of the platter at radius target, toward the pivot
    tx, ty = pcx + target * 0.75, pcy + target * 0.66
    x.line([(px, py), (tx, ty)], WHITE, a, 14, glow=False)
    x.circle(px, py, 34, WHITE, a, 4, fill=PANEL)
    x.circle(tx, ty, 14, AMBER if a1 > 0 else WHITE, a, 4, fill=NAVY)
    if a1 > 0:
        x.text((CX, 1165), "seek ~9 ms  +  spin ~4 ms", "mono", 40, WHITE, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        label_box(x, CX, 1235, "≈ 13 ms per read", AMBER, a2, 44)


# ---------- scene 4: the queue ----------
def s_queue(x):
    a = x.b(0)
    # the drive on the right, a counter on top
    x.rect([760, 600, 980, 900], CYAN, a, 5, r=24, fill=PANEL + (255,))
    x.circle(870, 720, 70, CYAN, a, 4)
    x.text((870, 850), "HDD", "title", 40, CYAN, a, anchor="mm")
    x.text((CX, 470), "75-100 random reads / s", "title", 54, WHITE, a, anchor="mm")
    # requests arrive faster than they leave
    a1 = x.b(1)
    if a1 > 0:
        names = ["chat", "sync", "updater", "launcher", "browser", "antivirus", "mail"]
        s1 = x.since(1)
        n = min(len(names), 1 + int(s1 * 2.2))
        for k in range(n):
            yy = 560 + k * 92
            if yy > 1110:
                break
            xx = 640 - 4 * k
            x.rect([100, yy, xx, yy + 72], AMBER, a1, 3, r=36, fill=NAVY + (255,), glow=False)
            x.text((130, yy + 36), names[k], "semi", 38, AMBER, a1, anchor="lm")
            x.text((xx - 28, yy + 36), "waiting", "reg", 30, MUTED, a1, anchor="rm")
        # one request being served: pulse into the drive
        ph = (x.t * 1.6) % 1
        x.circle(650 + 110 * ph, 600 + 36, 16, AMBER, a1 * (1 - ph), 0, fill=AMBER)
    a2 = x.b(2)
    if a2 > 0:
        ring(x, 870, 1060, 90, ease(x.since(2) / 0.8), RED, a2, w=22)
        x.text((870, 1060), "100%", "title", 46, RED, a2, anchor="mm")


# ---------- scene 5: an SSD ----------
def s_ssd(x):
    a = x.b(0)
    # a flat M.2 stick: no moving parts
    x.rect([170, 470, 910, 600], CYAN, a, 5, r=14, fill=PANEL + (255,))
    for k in range(4):
        x.d.rectangle([230 + k * 150, 495, 340 + k * 150, 575], fill=col(MUTED, a * 0.55))
    x.text((CX, 650), "no arm, no spinning", "semi", 42, CYAN, a, anchor="mm")
    a1 = x.b(1)
    pct = 0
    if a1 > 0:
        pct = tape(x, 820, lambda k: k % 7 == 0, a1, "same requests, one second", clamp(x.since(1) / 2.0), GREEN)
        x.text((CX, 1060), "< 1 ms per read", "mono", 46, GREEN, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((CX, 1170), f"active time {pct}%", "title", 70, GREEN, a2, anchor="mm")


# ---------- scene 6: full video ----------
def s_end(x):
    a = x.b(0)
    x.rect([140, 560, 940, 1010], CYAN, a, 5, r=30, fill=PANEL + (255,))
    x.d.polygon([(500, 680), (500, 820), (620, 750)], fill=col(AMBER, a))
    x.text((CX, 900), "Why Your PC Is Slow", "title", 60, WHITE, a, anchor="mm")
    x.text((CX, 1110), "full video on the channel", "semi", 42, MUTED, a, anchor="mm")


SCENES = [
    ("Disk 100%?", s_hook),
    ("It's active time", s_active),
    ("Why hard drives choke", s_hdd),
    ("The line never empties", s_queue),
    ("The SSD difference", s_ssd),
    ("Find the real culprit", s_end),
]
