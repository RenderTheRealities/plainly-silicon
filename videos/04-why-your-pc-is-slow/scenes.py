"""Scenes for video 04: Why Your PC Is Slow, and Why More RAM Usually Isn't the Fix.
Through-line: one slow five-year-old desktop (8 GB RAM, hard drive) diagnosed reading by reading
with Task Manager. Design language: square-cornered instrument windows, vertical meters,
sparkline graphs, request tokens queuing in front of a slow drive."""
import math
from render import *  # noqa: F401,F403


# ---------- helpers (instrument-panel style) ----------
def lerp(a, b, p):
    return a + (b - a) * p


def heat(frac):
    return CYAN if frac < 0.6 else (AMBER if frac < 0.9 else RED)


def window(x, box, title, a, accent=None):
    """Square instrument window with a title strip."""
    if a <= 0:
        return
    accent = accent or CYAN
    x0, y0, x1, y1 = box
    x.d.rectangle(box, fill=col(PANEL, a))
    x.d.rectangle([x0, y0, x1, y0 + 46], fill=col(GRID, a))
    x.d.rectangle(box, outline=col(accent, a * 0.7), width=2)
    x.d.rectangle([x0, y0, x0 + 8, y0 + 46], fill=col(accent, a))
    x.text((x0 + 26, y0 + 23), title, "monob", 24, WHITE, a, anchor="lm")
    for k in range(3):
        x.d.rectangle([x1 - 30 - k * 30, y0 + 17, x1 - 16 - k * 30, y0 + 29], outline=col(MUTED, a), width=2)


def vmeter(x, cx, ytop, ybot, w, frac, label, val, a, c=None, pulse=0.0):
    if a <= 0:
        return
    c = c or heat(frac)
    x.d.rectangle([cx - w / 2, ytop, cx + w / 2, ybot], fill=col(GRID, a))
    for k in range(1, 10):
        yy = ybot - (ybot - ytop) * k / 10
        x.d.line([(cx - w / 2, yy), (cx - w / 2 + 14, yy)], fill=col(MUTED, a * 0.7), width=2)
    fy = ybot - (ybot - ytop) * clamp(frac)
    if frac > 0.003:
        x.d.rectangle([cx - w / 2, fy, cx + w / 2, ybot], fill=col(c, a))
    if pulse > 0:
        x.rect([cx - w / 2 - 10, ytop - 10, cx + w / 2 + 10, ybot + 10], c, a * pulse, 4, r=2)
    x.text((cx, ybot + 22), label, "semi", 30, WHITE, a, anchor="mt")
    x.text((cx, ytop - 18), val, "monob", 38, c, a, anchor="md")


def hbar(x, x0, y, wmax, h, frac, c, a, bgc=None):
    if a <= 0:
        return
    x.d.rectangle([x0, y, x0 + wmax, y + h], fill=col(bgc or GRID, a))
    if frac > 0.002:
        x.d.rectangle([x0, y, x0 + wmax * clamp(frac), y + h], fill=col(c, a))


def spark(x, box, ys, c, a, fill=True):
    if a <= 0 or len(ys) < 2:
        return
    x0, y0, x1, y1 = box
    pts = [(x0 + (x1 - x0) * i / (len(ys) - 1), y1 - (y1 - y0) * clamp(v)) for i, v in enumerate(ys)]
    if fill:
        x.d.polygon(pts + [(x1, y1), (x0, y1)], fill=col(c, a * 0.22))
    x.line(pts, c, a, 3)


def token(x, cx, cy, s, c, a):
    if a <= 0:
        return
    h = s / 2
    x.d.rectangle([cx - h, cy - h, cx + h, cy + h], fill=col(c, a * 0.85), outline=col(WHITE, a * 0.5), width=1)
    x.d.line([(cx - h * 0.5, cy - h * 0.2), (cx + h * 0.5, cy - h * 0.2)], fill=col(NAVY, a), width=2)
    x.d.line([(cx - h * 0.5, cy + h * 0.25), (cx + h * 0.3, cy + h * 0.25)], fill=col(NAVY, a), width=2)


def arrow(x, p0, p1, c, a, w=4, head=18):
    if a <= 0:
        return
    x.line([p0, p1], c, a, w)
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    l, r = ang + 2.6, ang - 2.6
    x.d.polygon([p1, (p1[0] + head * math.cos(l), p1[1] + head * math.sin(l)),
                 (p1[0] + head * math.cos(r), p1[1] + head * math.sin(r))], fill=col(c, a))


def ring(x, cx, cy, r, frac, c, a, w=22):
    if a <= 0:
        return
    x.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col(GRID, a), width=w)
    if frac > 0.002:
        x.d.arc([cx - r, cy - r, cx + r, cy + r], -90, -90 + 360 * clamp(frac), fill=col(c, a), width=w)


def spinner(x, cx, cy, r, c, a):
    if a <= 0:
        return
    s = (x.t * 300) % 360
    x.d.arc([cx - r, cy - r, cx + r, cy + r], s, s + 260, fill=col(c, a), width=max(3, int(r / 4)))


def hdd(x, cx, cy, s, a, c=None):
    """Small hard-drive icon: case, platter, arm."""
    if a <= 0:
        return
    c = c or WHITE
    x.d.rectangle([cx - s * 0.6, cy - s * 0.8, cx + s * 0.6, cy + s * 0.8], fill=col(PANEL, a), outline=col(c, a), width=3)
    x.circle(cx, cy - s * 0.12, s * 0.45, c, a, 3)
    x.circle(cx, cy - s * 0.12, s * 0.08, c, a, 0, fill=c)
    ang = 0.3 * math.sin(x.t * 6)
    px, py = cx + s * 0.42, cy + s * 0.6
    x.line([(px, py), (px - s * 0.55 * math.cos(1.2 + ang), py - s * 0.55 * math.sin(1.2 + ang) - s * 0.2)], AMBER, a, 4, glow=False)


def chip_label(x, cx, cy, s, c, a, size=30):
    """Square-cornered tag (this video's label style)."""
    if a <= 0:
        return
    f = font("semi", size)
    tw = x.d.textlength(s, font=f)
    x.d.rectangle([cx - tw / 2 - 18, cy - size * 0.8, cx + tw / 2 + 18, cy + size * 0.8], fill=col(NAVY, a), outline=col(c, a), width=2)
    x.d.rectangle([cx - tw / 2 - 18, cy - size * 0.8, cx - tw / 2 - 12, cy + size * 0.8], fill=col(c, a))
    x.text((cx, cy), s, "semi", size, c, a, anchor="mm")


def window_icon(x, cx, cy, w, h, a, c=None):
    c = c or CYAN
    x.d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], fill=col(PANEL, a), outline=col(c, a), width=3)
    x.d.rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy - h / 2 + 18], fill=col(c, a * 0.6))


CHAIN = ["Disk", "RAM", "CPU", "GPU", "Screen"]


def chain(x, y, a, slow=0, ssd=0.0, boost=-1):
    """Five parts in a chain; the disk link is narrow (slow=1) or wide (ssd=1)."""
    if a <= 0:
        return
    xs = [300 + i * 330 for i in range(5)]
    for i, nm in enumerate(CHAIN):
        bad = (i == 0 and ssd < 0.5)
        c = RED if bad else (GREEN if (i == 0 and ssd >= 0.5) else (AMBER if i == boost else CYAN))
        x.d.rectangle([xs[i] - 95, y - 62, xs[i] + 95, y + 62], fill=col(PANEL, a), outline=col(c, a), width=3)
        label = "SSD" if (i == 0 and ssd >= 0.5) else nm
        x.text((xs[i], y), label, "title", 40, c, a, anchor="mm")
        if i:
            x.line([(xs[i - 1] + 95, y), (xs[i] - 95, y)], MUTED, a, 3, glow=False)
    # flow of work tokens: rate set by the disk (narrow) unless ssd
    rate = lerp(0.55, 2.6, ssd)
    span = xs[-1] - xs[0]
    n = 14
    for k in range(n):
        p = ((x.t * rate * 0.08) + k / n) % 1.0
        tx = xs[0] + p * span
        if ssd < 0.5 and k % 3:      # throttled: only every 3rd slot carries work
            continue
        token(x, tx, y - 92, 22, CYAN, a * 0.9)
    if ssd < 0.5:
        for k in range(6):            # pile waiting at the disk
            token(x, xs[0] - 140 - (k % 3) * 26, y - 30 + (k // 3) * 30 - 10, 22, AMBER, a)


# ---------- scenes ----------
def s_hook(x):
    a0 = x.b(0, 0.4)
    # monitor
    mx0, my0, mx1, my1 = 180, 190, 900, 610
    x.d.rectangle([mx0, my0, mx1, my1], fill=col(PANEL, a0), outline=col(WHITE, a0), width=4)
    x.d.rectangle([500, my1, 580, my1 + 60], fill=col(WHITE, a0 * 0.8))
    x.d.rectangle([420, my1 + 60, 660, my1 + 72], fill=col(WHITE, a0 * 0.8))
    x.d.rectangle([mx0 + 4, my1 - 44, mx1 - 4, my1 - 4], fill=col(GRID, a0))
    for k in range(4):
        x.d.rectangle([mx0 + 40, my0 + 40 + k * 80, mx0 + 90, my0 + 90 + k * 80], outline=col(MUTED, a0), width=2)
    # busy cursor + spinner
    cxp, cyp = 600, 380
    pts = [(cxp, cyp), (cxp, cyp + 46), (cxp + 12, cyp + 35), (cxp + 22, cyp + 56), (cxp + 31, cyp + 52),
           (cxp + 21, cyp + 32), (cxp + 37, cyp + 32)]
    x.d.polygon(pts, fill=col(WHITE, a0), outline=col(NAVY, a0))
    spinner(x, cxp + 58, cyp + 66, 18, CYAN, a0)
    # click ripples during sentence 3 (lagging response)
    if x.since(3) > 0:
        ph = x.since(3) % 2.0
        x.circle(cxp, cyp, 20 + ph * 40, AMBER, x.b(3) * (1 - ph / 2.0), 3)
        lag = clamp(ph - 1.3) / 0.7
        window_icon(x, 380, 330, 180 * (0.4 + 0.6 * lag), 120 * (0.4 + 0.6 * lag), x.b(3) * lag)
    # timer counting up to 2:00
    secs = min(120, x.t * 120 / 6.0)
    x.text((1340, 205), f"{int(secs // 60)}:{int(secs % 60):02d}", "monob", 120, AMBER, a0, anchor="mt")
    x.text((1340, 345), "after login, until usable", "semi", 30, MUTED, a0, anchor="mt")
    # advice bubbles (sentence 0 only)
    ba = x.b(0) * (1 - x.b(1))
    for k, (bx, by) in enumerate([(1160, 470), (1520, 520), (1300, 600)]):
        aa = ba * ease((x.t - 1.0 - k * 0.6) / 0.4)
        if aa <= 0:
            continue
        x.d.rectangle([bx - 160, by - 36, bx + 160, by + 36], fill=col(NAVY, aa), outline=col(WHITE, aa), width=3)
        x.d.polygon([(bx - 100, by + 36), (bx - 70, by + 36), (bx - 110, by + 66)], fill=col(WHITE, aa))
        x.text((bx, by), "Buy more RAM!", "semi", 32, WHITE, aa, anchor="mm")
    # free built-in tool
    ta = x.b(1)
    window_icon(x, 1200, 520, 200, 140, ta)
    for k, f_ in enumerate([0.3, 0.6, 1.0, 0.2]):
        hh = 80 * f_ * (0.8 + 0.2 * math.sin(x.t * 3 + k))
        x.d.rectangle([1130 + k * 40, 580 - hh, 1155 + k * 40, 580], fill=col(heat(f_), ta))
    x.text((1330, 500), "Task Manager", "title", 40, CYAN, ta, anchor="lm")
    x.text((1330, 548), "free, already installed", "semi", 28, MUTED, ta, anchor="lm")
    # spec tags
    sa = x.b(2)
    for k, s in enumerate(["5 years old", "8 GB RAM", "Hard drive"]):
        chip_label(x, 300 + k * 240, 760, s, WHITE if k < 2 else AMBER, sa * ease((x.since(2) - k * 0.3) / 0.4), 28)
    # empty meters waiting for readings
    ma = x.b(4)
    for k, nm in enumerate(["CPU", "Mem", "Disk", "Net", "GPU"]):
        vmeter(x, 1110 + k * 140, 700, 860, 70, 0, nm, "?", ma * ease((x.since(4) - k * 0.15) / 0.4), MUTED)


PROCS = [("Browser", 4, "900 MB", 0.4), ("Game launcher", 2, "210 MB", 3.1), ("Cloud sync", 3, "160 MB", 6.8),
         ("Chat app", 1, "300 MB", 2.2), ("Updater", 5, "120 MB", 4.5)]
COLS = [("CPU", 820), ("Memory", 1030), ("Disk", 1240), ("Network", 1450), ("GPU", 1640)]


def s_columns(x):
    a = x.b(0, 0.4)
    window(x, [160, 130, 1760, 560], "Task Manager  |  Processes", a)
    x.text((220, 210), "Name", "semi", 28, MUTED, a, anchor="lm")
    for k, (nm, cx) in enumerate(COLS):
        ca = x.b(1) * ease((x.since(1) - k * 0.3) / 0.4)
        sel = nm == "Disk" and x.since(3) > 0
        x.text((cx, 210), nm, "semi", 30, AMBER if sel else WHITE, ca, anchor="mm")
        if sel:
            x.d.polygon([(cx - 10, 176), (cx + 10, 176), (cx, 188)], fill=col(AMBER, ca))
    # "each can run out": a sweep highlight across columns during sentence 2
    if 0 < x.since(2) and x.since(3) <= 0:
        k = int(x.since(2) / 0.5) % 5
        cx = COLS[k][1]
        x.rect([cx - 95, 182, cx + 95, 545], CYAN, x.b(2) * 0.8, 3, r=2)
    # rows; sorted by disk after sentence 3
    order = sorted(range(5), key=lambda i: -PROCS[i][3])
    sp = ease(x.since(3) / 1.0)
    for i, (nm, cpu, mem, disk) in enumerate(PROCS):
        y = lerp(270 + i * 56, 270 + order.index(i) * 56, sp)
        x.d.rectangle([180, y - 24, 1740, y + 24], fill=col(GRID, a * 0.5))
        x.text((220, y), nm, "semi", 28, WHITE, a, anchor="lm")
        x.text((COLS[0][1], y), f"{cpu}%", "mono", 28, WHITE, a, anchor="mm")
        x.text((COLS[1][1], y), mem, "mono", 28, WHITE, a, anchor="mm")
        dc = heat(disk / 7.0) if sp > 0.5 else WHITE
        x.text((COLS[2][1], y), f"{disk} MB/s", "mono", 28, dc, a, anchor="mm")
        x.text((COLS[3][1], y), "0 Mbps", "mono", 28, MUTED, a, anchor="mm")
        x.text((COLS[4][1], y), "0%", "mono", 28, MUTED, a, anchor="mm")
    # chain = bottleneck
    ca = x.b(4)
    x.text((960, 620), "bottleneck: the slowest link sets the pace", "semi", 32, WHITE, ca, anchor="mm")
    chain(x, 800, x.b(5), boost=2 if x.since(6) > 0 else -1)
    if x.since(6) > 0:
        aa = x.b(6)
        x.text((960, 900), "CPU made faster  ->  same flow through the chain", "semi", 30, AMBER, aa, anchor="mm")


def s_readings(x):
    vals = [("CPU", 0.15, 1), ("Memory", 0.68, 2), ("Disk", 1.0, 3), ("Network", 0.0, 0), ("GPU", 0.02, 0)]
    for k, (nm, v, bt) in enumerate(vals):
        aa = x.b(0, 0.4)
        f = v * ease(x.since(bt) / 0.9) if bt else v
        if bt and x.since(bt) <= 0:
            f = 0
        pulse = (0.5 + 0.5 * math.sin(x.t * 6)) * x.b(3) if nm == "Disk" else 0
        vmeter(x, 230 + k * 175, 220, 760, 110, f, nm, f"{round(f * 100)}%", aa, pulse=pulse)
    # memory isn't a problem by itself
    ma = x.b(4) * (1 - 0.6 * x.b(8))
    x.rect([405 - 80, 160, 405 + 80, 830], AMBER, ma, 3, r=2)
    x.text((405, 135), "not a problem by itself", "semi", 26, AMBER, ma, anchor="mm")
    # desk analogy
    da = x.b(5) * (1 - 0.6 * x.b(8))
    x.text((1460, 190), "RAM is desk space", "title", 44, WHITE, da, anchor="mm")
    for row, (y0, ok, bt) in enumerate([(250, True, 6), (560, False, 7)]):
        a2 = x.b(bt) * (1 - 0.6 * x.b(8))
        if a2 <= 0 or x.since(bt) <= 0:
            continue
        c = GREEN if ok else RED
        x.d.rectangle([1150, y0 + 150, 1770, y0 + 166], fill=col(c, a2))
        x.d.rectangle([1170, y0 + 166, 1186, y0 + 230], fill=col(c, a2))
        x.d.rectangle([1734, y0 + 166, 1750, y0 + 230], fill=col(c, a2))
        spots = [(1190 + k * 58, y0 + 122) for k in range(6 if ok else 10)]
        if not ok:
            spots += [(1210 + k * 58, y0 + 76) for k in range(9)] + [(1240 + k * 58, y0 + 30) for k in range(6)]
            spots += [(1800, y0 + 212), (1850, y0 + 212), (1825, y0 + 170)]
        for k, (bx, by) in enumerate(spots):
            token(x, bx, by, 46, WHITE, a2 * ease((x.since(bt) - k * 0.05) / 0.3))
        x.text((1460, y0 + 262), "busy, still room: fine" if ok else "no room left: slow", "semi", 30, c, a2, anchor="mm")
    # spotlight on disk
    sa = x.b(8)
    arrow(x, (580, 905), (580, 860), RED, sa, 5)
    x.text((615, 900), "the reading that matters", "semi", 32, RED, sa, anchor="lm")


def s_active(x):
    # capacity is not the issue
    a1 = x.b(0, 0.4)
    x.text((160, 190), "Space used", "semi", 30, WHITE, a1, anchor="lm")
    hbar(x, 160, 220, 740, 44, 0.45 * x.b(1, 1.0), CYAN, a1)
    x.text((900, 190), "45%", "monob", 30, CYAN, a1, anchor="rm")
    na = x.b(1)
    x.text((530, 330), "100% disk  ≠  full drive", "title", 46, AMBER, na, anchor="mm")
    # active time sample
    a2 = x.b(2)
    x.text((160, 440), "Busy time in each sample", "semi", 30, WHITE, a2, anchor="lm")
    x.d.rectangle([160, 470, 900, 540], fill=col(GRID, a2))
    fill = clamp(x.since(2) / 1.6)
    for k in range(20):
        if k / 20 < fill:
            x.d.rectangle([162 + k * 37, 472, 162 + k * 37 + 33, 538], fill=col(RED, a2))
    x.text((160, 590), "Active time", "semi", 32, MUTED, x.b(3), anchor="lm")
    x.text((900, 590), f"{round(fill * 100)}%", "monob", 54, RED, x.b(3), anchor="rm")
    # queue at the drive
    qa = x.b(4)
    hdd(x, 1640, 360, 120, qa, RED)
    n = int(min(11, 3 + x.since(4) * 1.2))
    served = (x.since(4) * 0.9) % 1.0
    for k in range(n):
        tx = 1500 - k * 46 - (0 if k else served * 0)
        token(x, tx, 360, 36, AMBER if k else WHITE, qa)
    # arriving
    for k in range(3):
        p = ((x.since(4) * 0.7) + k / 3) % 1.0
        token(x, lerp(960, 1500 - n * 46, p), 270 + 30 * math.sin(p * 3), 30, AMBER, qa * (1 - p) * 0.9)
    x.text((1260, 450), "requests wait in line", "semi", 30, WHITE, qa, anchor="mm")
    # response time graph
    ra = x.b(5)
    window(x, [960, 520, 1760, 880], "Disk 0 (C:)  |  Average response time", ra)
    s6 = x.since(6)
    ys = []
    for i in range(60):
        tt = x.t - (59 - i) * 0.12
        grow = clamp((tt - x.beats[min(6, len(x.beats) - 1)]) / 6.0)
        ys.append(0.08 + 0.75 * grow + 0.04 * math.sin(i * 1.7))
    spark(x, [990, 600, 1730, 850], ys, AMBER if s6 > 0 else CYAN, ra)
    ms = int(18 + 600 * clamp(s6 / 6.0))
    x.text((1000, 590), f"{ms:,} ms", "monob", 44, RED if ms > 200 else CYAN, ra, anchor="la")


def s_hdd(x):
    a0 = x.b(0, 0.4)
    cx, cy, R = 470, 450, 230
    x.circle(cx, cy, R, WHITE, a0, 4, fill=PANEL)
    for r in (70, 110, 150, 190):
        x.circle(cx, cy, r, MUTED, a0 * 0.6, 2)
    x.circle(cx, cy, 30, WHITE, a0, 3, fill=GRID)
    # spinning data sector on the target track
    spin = x.t * 2.2
    sx, sy = cx + 150 * math.cos(spin), cy + 150 * math.sin(spin)
    x.circle(sx, sy, 16, AMBER, a0, 0, fill=AMBER)
    x.text((cx, 180), "spinning platter", "semi", 28, MUTED, a0, anchor="mm")
    # arm swings in 2.4 s cycles: seek, then wait for the sector
    aa = x.b(1)
    px, py = 860, 700
    cyc = x.t % 2.4
    sw = ease(cyc / 0.8)
    ang = lerp(3.55, 3.88, sw) if (int(x.t / 2.4) % 2 == 0) else lerp(3.88, 3.55, sw)
    hx, hy = px + 470 * math.cos(ang), py + 470 * math.sin(ang)
    x.line([(px, py), (hx, hy)], CYAN, aa, 10)
    x.circle(px, py, 26, CYAN, aa, 4, fill=PANEL)
    x.d.rectangle([hx - 12, hy - 12, hx + 12, hy + 12], fill=col(WHITE, aa))
    x.text((px + 50, py), "arm + head", "semi", 28, CYAN, aa, anchor="lm")
    # timeline: seek + rotation
    t0, ty = 140, 790
    scale = 50  # px per ms
    sa = x.b(2)
    w_seek = 10 * scale * ease(x.since(2) / 0.8)
    x.d.rectangle([t0, ty, t0 + w_seek, ty + 44], fill=col(AMBER, sa))
    x.text((t0 + 250, ty - 14), "seek  8 to 12 ms", "semi", 28, AMBER, sa, anchor="md")
    ra = x.b(3)
    w_rot = 4 * scale * ease(x.since(3) / 0.6)
    x.d.rectangle([t0 + 500, ty, t0 + 500 + w_rot, ty + 44], fill=col(CYAN, ra))
    x.text((t0 + 600, ty - 14), "spin  ~4 ms", "semi", 28, CYAN, ra, anchor="md")
    ta = x.b(4)
    x.line([(t0, ty + 60), (t0, ty + 70), (t0 + 700, ty + 70), (t0 + 700, ty + 60)], WHITE, ta, 3, glow=False)
    x.text((t0 + 720, ty + 22), "≈ 14 ms", "monob", 40, WHITE, ta, anchor="lm")
    x.text((t0 + 350, ty + 110), "≈ 75 to 100 random reads per second", "semi", 30, RED, ta, anchor="mm")
    # SSD side
    s5 = x.b(5)
    window(x, [1140, 160, 1770, 880], "Solid state drive", s5, GREEN)
    x.d.rectangle([1200, 260, 1710, 470], fill=col(GRID, s5), outline=col(GREEN, s5), width=3)
    x.d.rectangle([1225, 300, 1345, 430], fill=col(NAVY, s5), outline=col(WHITE, s5), width=2)
    x.text((1285, 365), "ctrl", "mono", 24, WHITE, s5, anchor="mm")
    for k in range(3):
        x.d.rectangle([1380 + k * 108, 300, 1470 + k * 108, 430], fill=col(NAVY, s5), outline=col(GREEN, s5), width=2)
    x.text((1455, 510), "no moving parts", "semi", 32, GREEN, s5, anchor="mm")
    s6 = x.b(6)
    for k in range(18):
        p = ((x.t * 1.6) + k / 18) % 1.0
        token(x, lerp(1200, 1710, p), 600 + (k % 3) * 34, 22, GREEN, s6)
    x.text((1455, 740), "< 1 ms per read", "monob", 44, GREEN, s6, anchor="mm")
    x.text((1455, 810), "tens of thousands per second", "semi", 30, WHITE, s6, anchor="mm")


START = [("Cloud sync", 6.8, "High"), ("Updater", 4.5, "High"), ("Game launcher", 3.1, "High"),
         ("Chat app", 2.2, "Medium"), ("Touchpad driver", 0.1, "Low")]


def s_startup(x):
    pa = x.b(0, 0.4) * (1 - x.b(4))
    if pa > 0:
        window(x, [140, 150, 900, 600], "Processes  |  sorted by Disk", pa, AMBER)
        for i, (nm, d, _) in enumerate(START[:4] + [("Browser", 0.4, "")]):
            y = 240 + i * 70
            x.text((170, y), nm, "semi", 30, WHITE, pa, anchor="lm")
            hbar(x, 520, y - 12, 240, 24, d / 7.0, heat(d / 7.0), pa)
            x.text((880, y), f"{d}", "mono", 28, WHITE, pa, anchor="rm")
            if i < 4:
                x.text((170, y + 28), "starts at login", "reg", 20, AMBER, pa * x.b(2), anchor="lm")
        # all feeding one slow drive
        qa = x.b(3) * pa
        hdd(x, 1620, 400, 130, qa, RED)
        for i in range(4):
            for k in range(3):
                p = ((x.since(3) * 0.35) + k / 3 + i * 0.08) % 1.0
                sx, sy = 920, 240 + i * 70
                ex, ey = 1480, 400
                token(x, lerp(sx, ex, ease(p)), lerp(sy, ey, ease(p)), 26, AMBER, qa * (0.4 + 0.6 * (1 - p)))
        x.text((1250, 640), "all waiting on one hard drive", "semi", 32, WHITE, qa, anchor="mm")
    sa = x.b(4)
    if sa <= 0:
        return
    window(x, [240, 140, 1680, 900], "Task Manager  |  Startup apps", sa)
    x.text((290, 225), "Name", "semi", 28, MUTED, sa, anchor="lm")
    x.text((1000, 225), "Status", "semi", 28, MUTED, sa, anchor="mm")
    x.text((1400, 225), "Startup impact", "semi", 28, MUTED, sa, anchor="mm")
    for i, (nm, _, imp) in enumerate(START):
        y = 290 + i * 66
        ra = sa * ease((x.since(4) - i * 0.15) / 0.4)
        off = i < 4 and x.since(7) > 0.6 + i * 0.6
        x.text((290, y), nm, "semi", 32, MUTED if off else WHITE, ra, anchor="lm")
        x.text((1000, y), "Disabled" if off else "Enabled", "mono", 28, MUTED if off else GREEN, ra, anchor="mm")
        ic = {"High": RED, "Medium": AMBER, "Low": GREEN}[imp]
        ia = ra * (x.b(5) if i else x.b(5))
        x.d.rectangle([1320, y - 20, 1480, y + 20], outline=col(ic, ia), width=2)
        x.text((1400, y), imp, "semi", 26, ic, ia, anchor="mm")
    la = x.b(6)
    x.d.rectangle([290, 640, 1630, 710], fill=col(NAVY, la), outline=col(RED, la), width=2)
    x.text((960, 675), "High = over 1 second of CPU time, or over 3 MB of disk, at startup", "semi", 30, WHITE, la, anchor="mm")
    # cursor clicking Disable
    if x.since(7) > 0:
        k = min(3, int(x.since(7) / 0.6))
        cy0 = 290 + k * 66
        mx, my = 1060, cy0 + 4
        pts = [(mx, my), (mx, my + 40), (mx + 10, my + 30), (mx + 19, my + 48), (mx + 27, my + 44), (mx + 18, my + 27), (mx + 32, my + 27)]
        x.d.polygon(pts, fill=col(WHITE, x.b(7)), outline=col(NAVY, x.b(7)))
    wa = x.b(8)
    x.text((290, 780), "Login wait", "semi", 30, WHITE, wa, anchor="lm")
    frac = lerp(1.0, 0.6, ease(x.since(8) / 1.5))
    hbar(x, 520, 762, 1100, 36, frac, AMBER, wa)


def s_pagefile(x):
    a0 = x.b(0, 0.4)
    window(x, [200, 140, 1720, 470], "RAM  |  8 GB", a0)
    pa = x.b(4)
    x.d.rectangle([660, 640, 1260, 900], fill=col(PANEL, pa), outline=col(WHITE, pa), width=3)
    x.text((960, 670), "Hard drive  |  page file (hidden)", "semi", 28, WHITE, pa, anchor="mm")
    cols_, rows_ = 16, 3
    bw, bh = 84, 76
    stale = {1, 4, 6, 9, 12, 15, 17, 20, 23, 26, 30, 33, 36, 39, 41, 44}
    comp = sorted(stale)[:8]
    moved = sorted(stale)[8:]
    fill_p = clamp(x.t / max(0.1, x.beats[min(3, len(x.beats) - 1)] - 0.5))
    nfill = int(fill_p * 48)
    sc = x.b(3)
    mv = x.since(4)
    for k in range(48):
        r_, c_ = divmod(k, cols_)
        bx = 250 + c_ * (bw + 6) + bw / 2
        by = 220 + r_ * (bh + 8) + bh / 2
        if k >= nfill:
            x.d.rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], outline=col(GRID, a0), width=2)
            continue
        c = MUTED if k in stale and x.since(2) > 0 else CYAN
        s = bw - 14
        if k in comp:
            s = lerp(s, s * 0.4, sc)
        if k in moved and mv > 0:
            j = moved.index(k)
            p = ease((mv - j * 0.15) / 1.1)
            tx, ty = 780 + (j % 4) * 70, 740 + (j // 4) * 64
            if p > 0:
                x.d.rectangle([bx - bw / 2, by - bh / 2, bx + bw / 2, by + bh / 2], outline=col(GRID, a0), width=2)
            bx, by = lerp(bx, tx, p), lerp(by, ty, p)
            s = lerp(s, 50, p)
        token(x, bx, by, s, c, a0)
    x.text((1720, 495), "grey = not touched in a while", "reg", 24, MUTED, x.b(2), anchor="ra")
    x.text((200, 500), "compressed to ~40% of their size", "semi", 30, AMBER, sc, anchor="lt")
    arrow(x, (960, 520), (960, 625), AMBER, pa, 4)
    # mud waves on a hard drive
    ma = x.b(7)
    for k in range(4):
        pts = [(680 + i * 20, 850 + k * 10 + 5 * math.sin(i * 0.8 + x.t * 2 + k)) for i in range(30)]
        x.line(pts, AMBER, ma * 0.5, 2, glow=False)
    # data needed back: crawls up to an app that waits
    ba = x.b(5)
    window_icon(x, 1550, 720, 200, 150, ba, AMBER)
    spinner(x, 1550, 735, 30, AMBER, ba * (1 - x.b(7) * 0))
    p = clamp(x.since(5) / 7.0)
    token(x, lerp(1180, 1440, p), lerp(800, 720, p), 40, CYAN, ba)
    x.text((1550, 830), "app waits", "semi", 28, AMBER, ba, anchor="mm")
    # disk meter jumps
    da = x.b(6)
    f = ease(x.since(6) / 0.8)
    vmeter(x, 360, 620, 840, 90, f, "Disk", f"{round(f * 100)}%", da, pulse=(0.5 + 0.5 * math.sin(x.t * 6)) * da)


def s_commit(x):
    a = x.b(0, 0.4)
    window(x, [140, 140, 1080, 900], "Performance  |  Memory", a)
    gx0, gy0, gx1, gy1 = 180, 230, 1040, 520
    x.d.rectangle([gx0, gy0, gx1, gy1], outline=col(MUTED, a * 0.6), width=2)
    x.text((gx1, gy0 - 8), "8.0 GB", "mono", 24, MUTED, a, anchor="rd")
    ys = [0.675 + 0.012 * math.sin(i * 0.9 + x.t) for i in range(50)]
    spark(x, [gx0, gy0, gx1, gy1], ys, CYAN, a)
    hi_use = x.b(2) * (1 - x.b(5))
    rows = [("In use", "5.4 GB", 590), ("Available", "2.6 GB", 680), ("Committed", "7.1 / 12.8 GB", 770)]
    for nm, v, y in rows:
        hl = hi_use if nm in ("In use", "Committed") else 0
        x.text((190, y), nm, "semi", 32, AMBER if hl > 0.5 else MUTED, a, anchor="lm")
        x.text((1030, y), v, "monob", 40, WHITE, a, anchor="rm")
        if hl > 0:
            x.rect([170, y - 34, 1050, y + 34], AMBER, hl, 3, r=2)
    # commit limit decomposition
    ca = x.b(3)
    x.text((1180, 190), "Commit limit = RAM + page file", "semi", 30, WHITE, ca, anchor="lm")
    tot = 12.8
    W_ = 560
    x.d.rectangle([1180, 230, 1180 + W_ * 8 / tot, 290], fill=col(CYAN, ca))
    x.d.rectangle([1180 + W_ * 8 / tot + 4, 230, 1180 + W_, 290], fill=col(AMBER, ca))
    x.text((1180 + W_ * 4 / tot, 260), "RAM 8", "semi", 26, NAVY, ca, anchor="mm")
    x.text((1180 + W_ * 10.4 / tot, 260), "page file", "semi", 24, NAVY, ca, anchor="mm")
    x.text((1740, 315), "12.8 GB", "mono", 24, MUTED, ca, anchor="ra")

    def gauge(y, title, inuse, com, c, aa):
        if aa <= 0:
            return
        x.text((1180, y), title, "title", 34, c, aa, anchor="lm")
        x.text((1180, y + 50), "In use", "reg", 24, MUTED, aa, anchor="lm")
        hbar(x, 1330, y + 38, 410, 26, inuse / 8.0, c, aa)
        x.text((1180, y + 96), "Committed", "reg", 24, MUTED, aa, anchor="lm")
        hbar(x, 1330, y + 84, 410, 26, com / tot, c, aa)
        x.text((1740, y), f"{inuse} / 8 GB", "mono", 24, c, aa, anchor="rm")

    gauge(420, "Short on RAM", 7.8, 12.4, RED, x.b(4))
    gauge(610, "Our desktop", 5.4, 7.1, GREEN, x.b(5))
    va = x.b(7)
    chip_label(x, 1460, 830, "Real cause: startup apps + slow drive", AMBER, va, 26)
    if x.since(6) > 0:
        x.text((1400, 612), "room to spare", "semi", 26, GREEN, x.b(6), anchor="lm")


def s_ram_matters(x):
    a = x.b(0, 0.4)
    gb = 34  # px per GB
    base = 810

    def cont(cx, size, load, title, aa, note, ncol):
        if aa <= 0:
            return
        top = base - size * gb
        x.d.rectangle([cx - 120, top, cx + 120, base], outline=col(WHITE, aa), width=3)
        x.text((cx, top - 22), title, "monob", 34, WHITE, aa, anchor="md")
        fit = min(load, size)
        p = ease(x.since(1) / 2.0)
        shown = load * p
        for k in range(int(math.ceil(shown * 2))):
            g = k / 2
            yb = base - g * gb - gb / 2
            over = g >= size
            if over:
                kk = int((g - size) * 2)
                bx, by = cx + 170 + (kk % 2) * 50, base - 30 - (kk // 2) * 40
                token(x, bx, by, 34, RED, aa)
            else:
                x.d.rectangle([cx - 110, yb - gb / 4 + 3, cx + 110, yb + gb / 4 - 3], fill=col(CYAN, aa * 0.8))
        if note:
            x.text((cx, base + 30), note, "semi", 26, ncol, aa * p, anchor="mt")

    x.text((180, 150), "Windows + 30 tabs + background apps", "semi", 30, WHITE, a, anchor="lm")
    cont(330, 8, 10, "8 GB", x.b(1), "spills to page file", RED)
    cont(740, 16, 10, "16 GB", x.b(1), "fits", GREEN)
    ha = x.b(1)
    chip_label(x, 1270, 260, "HP: 16 GB ideal for Windows 11", CYAN, ha, 28)
    x.text((1270, 330), "8 GB can struggle with many tabs", "reg", 26, MUTED, ha, anchor="mm")
    ga = x.b(2)
    x.text((540, 960 - 30), "", "semi", 10, WHITE, 0)
    chip_label(x, 1270, 450, "RAM full?  More RAM helps a lot", GREEN, ga, 28)
    # light workload in a big container
    la = x.b(3)
    if la > 0:
        cx = 1540
        top = base - 16 * gb * 0.6
        x.d.rectangle([cx - 110, base - 300, cx + 110, base], outline=col(MUTED, la), width=3)
        for k in range(8):
            yb = base - k * (300 / 16) - 10
            x.d.rectangle([cx - 100, yb - 6, cx + 100, yb + 6], fill=col(CYAN, la * 0.8))
        for yy in range(int(base - 290), int(base - 160), 24):
            x.d.line([(cx - 100, yy), (cx + 100, yy)], fill=col(GRID, la), width=2)
        x.text((cx - 140, 600), "empty RAM", "semi", 28, MUTED, la, anchor="rm")
        x.text((cx - 140, 650), "speed-up: none", "monob", 30, AMBER, la, anchor="rm")
        x.text((cx, base + 30), "light use", "semi", 26, MUTED, la, anchor="mt")


def s_cpu_heat(x):
    a = x.b(0, 0.4)
    ra = x.b(1)
    f = ease(x.since(1) / 1.0) * (0.97 + 0.03 * math.sin(x.t * 7))
    ring(x, 440, 380, 170, f, heat(f), ra)
    x.text((440, 370), f"{round(f * 100)}%", "monob", 64, heat(f), ra, anchor="mm")
    x.text((440, 430), "CPU", "semi", 30, WHITE, ra, anchor="mm")
    pa = x.b(2)
    for i, (nm, v) in enumerate([("Runaway process", 0.86), ("Browser", 0.07), ("System", 0.04)]):
        y = 650 + i * 64
        x.text((160, y), nm, "semi", 28, WHITE, pa, anchor="lm")
        hbar(x, 470, y - 12, 300, 24, v, heat(v * 1.1), pa)
        x.text((830, y), f"{round(v * 100)}%", "mono", 26, WHITE, pa, anchor="rm")
    # thermometer
    ta = x.b(3)
    tx, ytop, ybot = 960, 200, 760
    temp_of = lambda c: ybot - (ybot - ytop) * (c - 30) / 90.0
    x.d.rounded_rectangle([tx - 26, ytop, tx + 26, ybot], radius=26, outline=col(WHITE, ta), width=3)
    x.circle(tx, ybot + 30, 44, WHITE, ta, 3)
    temp = lerp(55, 100, ease(x.since(3) / 4.0))
    x.circle(tx, ybot + 30, 34, RED, ta, 0, fill=RED)
    x.d.rectangle([tx - 14, temp_of(temp), tx + 14, ybot + 10], fill=col(heat((temp - 30) / 80), ta))
    x.text((tx, ytop - 24), f"{round(temp)} °C", "monob", 34, WHITE, ta, anchor="md")
    ba = x.b(4)
    x.d.rectangle([tx - 70, temp_of(110), tx - 40, temp_of(95)], fill=col(RED, ba * 0.7))
    x.text((tx - 85, temp_of(102)), "limit 95 to 110 °C", "semi", 26, RED, ba, anchor="rm")
    # clock speed graph
    ga = x.b(3)
    window(x, [1180, 170, 1770, 470], "CPU  |  Speed", ga)
    hit = x.beats[min(5, len(x.beats) - 1)]
    ys = []
    for i in range(50):
        tt = x.t - (49 - i) * 0.4
        drop = ease((tt - hit) / 1.0)
        ys.append(lerp(0.82, 0.45, drop) + 0.02 * math.sin(i * 2.1))
    spark(x, [1200, 300, 1750, 455], ys, CYAN, ga)
    sp = lerp(3.9, 2.3, ease((x.t - hit) / 1.0))
    x.text((1740, 230), f"{sp:.1f} GHz", "monob", 34, AMBER if sp < 3 else CYAN, x.b(7), anchor="ra")
    x.text((1475, 510), "power + clock cut", "semi", 28, AMBER, x.b(5), anchor="mm")
    stamp(x, 1470, 650, "THERMAL THROTTLING", RED, x.b(6))
    # fan + dust
    fa = x.b(8)
    fcx, fcy = 1640, 845
    x.circle(fcx, fcy, 62, WHITE, fa, 3)
    for k in range(5):
        an = x.t * 8 + k * 2 * math.pi / 5
        x.line([(fcx, fcy), (fcx + 52 * math.cos(an), fcy + 52 * math.sin(an))], CYAN, fa, 8, glow=False)
    for k in range(10):
        p = ((x.t * 0.6) + k / 10) % 1.0
        x.circle(fcx + 70 + p * 160, fcy - 50 + (k * 37) % 100, 6, MUTED, fa * (1 - p), 0, fill=MUTED)
    x.text((fcx - 90, fcy), "clean the dust", "semi", 28, WHITE, fa, anchor="rm")


def s_gpu(x):
    a = x.b(0, 0.4)

    def lane(x0, title, cpu, gpu, ok, aa, gaps):
        if aa <= 0:
            return
        c = GREEN if ok else RED
        window(x, [x0, 150, x0 + 760, 880], title, aa, c)
        x.d.rectangle([x0 + 60, 260, x0 + 260, 420], fill=col(GRID, aa), outline=col(WHITE, aa), width=3)
        x.text((x0 + 160, 340), "CPU", "title", 44, RED if cpu > 0.95 else WHITE, aa, anchor="mm")
        x.d.rectangle([x0 + 500, 260, x0 + 700, 420], fill=col(GRID, aa), outline=col(WHITE, aa), width=3)
        x.text((x0 + 600, 340), "GPU", "title", 44, GREEN if ok else MUTED, aa, anchor="mm")
        for k in range(8):
            if gaps and k % 2:
                continue
            p = ((x.t * 0.5) + k / 8) % 1.0
            token(x, lerp(x0 + 280, x0 + 480, p), 340, 26, CYAN, aa)
        if not ok:
            x.text((x0 + 600, 455), "waiting...", "semi", 26, MUTED, aa * (0.5 + 0.5 * math.sin(x.t * 4)), anchor="mm")
        for j, (nm, v) in enumerate([("CPU", cpu), ("GPU", gpu)]):
            y = 560 + j * 120
            x.text((x0 + 60, y), nm, "semi", 30, WHITE, aa, anchor="lm")
            hbar(x, x0 + 170, y - 18, 440, 36, v * ease(x.since(1) / 0.8), (GREEN if (ok and nm == "GPU") else heat(v)), aa)
            x.text((x0 + 700, y), f"{round(v * 100)}%", "monob", 32, WHITE, aa, anchor="rm")

    lane(140, "Graphics card is the limit: normal", 0.6, 0.99, True, x.b(1), False)
    lane(1020, "CPU is the limit", 1.0, 0.55, False, x.b(3), True)
    chip_label(x, 520, 820, "what you paid for", GREEN, x.b(2), 28)
    chip_label(x, 1400, 820, "faster graphics card won't fix it", RED, x.b(4), 28)


def s_verdict(x):
    a = x.b(0, 0.4)
    fixed = x.b(2)
    chain(x, 330, a, ssd=fixed)
    x.text((960, 190), "the bottleneck was the hard drive", "semi", 32, WHITE, x.b(1) * (1 - fixed), anchor="mm")
    x.text((960, 190), "Windows on an SSD: the chain flows", "semi", 32, GREEN, fixed, anchor="mm")
    sa = x.b(3)
    steps = [("1", "Open Task Manager"), ("2", "Sort each column"), ("3", "Fix the part at the top")]
    for k, (n, s) in enumerate(steps):
        cx = 400 + k * 560
        aa = x.b(4) * ease((x.since(4) - k * 0.5) / 0.4) if k else sa
        x.d.rectangle([cx - 230, 560, cx + 230, 720], fill=col(PANEL, aa), outline=col(CYAN, aa), width=3)
        x.d.rectangle([cx - 230, 560, cx - 170, 720], fill=col(CYAN, aa))
        x.text((cx - 200, 640), n, "monob", 40, NAVY, aa, anchor="mm")
        x.text((cx + 30, 640), s, "semi", 32, WHITE, aa, anchor="mm")
        if k:
            arrow(x, (cx - 330, 640), (cx - 240, 640), CYAN, aa, 4)
    ba = x.b(5)
    x.d.rectangle([760, 790, 1160, 870], outline=col(MUTED, ba), width=3)
    x.text((960, 830), "Buy more RAM!", "semi", 34, MUTED, ba, anchor="mm")
    p = ease(x.since(5) / 0.5)
    x.line([(740, 830), (740 + 440 * p, 830)], RED, ba, 6)


def s_next(x):
    a = x.b(0, 0.4)
    x.text((960, 170), "NEXT", "monob", 34, AMBER, a, anchor="mm")
    t1 = x.b(1)
    names = ["HDD", "SATA SSD", "NVMe SSD"]
    for k, nm in enumerate(names):
        cx = 400 + k * 560
        aa = t1 * ease((x.since(1) - k * 0.4) / 0.4)
        if k == 0:
            hdd(x, cx, 400, 120, aa, WHITE)
        elif k == 1:
            x.d.rectangle([cx - 100, 300, cx + 100, 500], fill=col(PANEL, aa), outline=col(WHITE, aa), width=3)
            x.d.rectangle([cx - 70, 340, cx + 70, 420], outline=col(CYAN, aa), width=2)
        else:
            x.d.rectangle([cx - 190, 370, cx + 190, 430], fill=col(PANEL, aa), outline=col(WHITE, aa), width=3)
            for j in range(4):
                x.d.rectangle([cx - 160 + j * 80, 380, cx - 100 + j * 80, 420], fill=col(GRID, aa), outline=col(CYAN, aa), width=2)
        x.text((cx, 560), nm, "title", 40, WHITE, aa, anchor="mm")
        hbar(x, cx - 200, 620, 400, 28, (0.5 + 0.5 * math.sin(x.t * 1.3 + k)) * 0.9, CYAN, aa)
        x.text((cx, 690), "load time ?", "mono", 28, MUTED, aa, anchor="mm")
    x.text((960, 780), "What really makes games load faster", "title", 46, WHITE, t1, anchor="mm")
    sa = x.b(2)
    pul = 1 + 0.05 * math.sin(x.since(2) * 6)
    w2, h2 = 220 * pul, 44 * pul
    x.d.rectangle([960 - w2, 880 - h2, 960 + w2, 880 + h2], fill=col(RED, sa))
    x.text((960, 880), "SUBSCRIBE", "title", 40, (255, 255, 255), sa, anchor="mm")


SCENES = [
    ("A slow PC", s_hook),
    ("Open Task Manager", s_columns),
    ("Read the columns", s_readings),
    ("What 100% disk means", s_active),
    ("Why hard drives choke", s_hdd),
    ("Startup apps", s_startup),
    ("When RAM fills up", s_pagefile),
    ("Is RAM really full?", s_commit),
    ("When more RAM helps", s_ram_matters),
    ("CPU and heat", s_cpu_heat),
    ("Gamers: the GPU column", s_gpu),
    ("The verdict", s_verdict),
    ("Up next", s_next),
]
