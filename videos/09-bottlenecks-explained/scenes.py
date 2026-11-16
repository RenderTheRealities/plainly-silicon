"""Scenes for video 09: Bottlenecks Explained.

Design language (ocean theme): plumbing. A frame's journey is water through a two-section pipe
(CPU section, then GPU section); the narrow section sets the flow and gets a pulsing ring.
Particles stream through the pipe at a rate set by the narrowest section. Test results are
shown as "flow meters" (horizontal tanks that fill), a lab test matrix of chips and cards,
a two-point line chart for 1080p vs 4K, per-core usage columns, and settings sliders.
Rounded, soft, liquid shapes; nothing reused from earlier videos.
"""
import math
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def pipe(x, x0, x1, cy, h_cpu, h_gpu, a, t, split=None, labels=True, ring=True, rate=None):
    """Two-section horizontal pipe. Left = CPU section (AMBER), right = GPU section (CYAN).
    h_* are inner heights. Water particles flow left to right; their rate follows the narrower section."""
    if a <= 0:
        return
    split = split if split is not None else (x0 + x1) / 2
    for (sx0, sx1, h, c) in [(x0, split, h_cpu, AMBER), (split, x1, h_gpu, CYAN)]:
        x.d.rounded_rectangle([sx0, cy - h / 2, sx1, cy + h / 2], radius=min(18, h / 2), fill=col(PANEL, a))
        x.rect([sx0, cy - h / 2, sx1, cy + h / 2], c, a, 5, r=min(18, h / 2), glow=True)
    narrow = min(h_cpu, h_gpu)
    v = rate if rate is not None else 60 + 3.2 * narrow
    gap = 46
    off = (t * v) % gap
    k = 0
    px = x0 + 14 - gap + off
    while px < x1 - 10:
        if px > x0 + 10:
            h = h_cpu if px < split else h_gpu
            lanes = max(1, int(h // 34))
            for ln in range(lanes):
                py = cy - h / 2 + (ln + 0.5) * h / lanes + 4 * math.sin(px / 40 + ln)
                x.circle(px + (ln % 2) * 12, py, 7, WHITE, a * 0.75, 0, fill=WHITE)
        px += gap
        k += 1
    if labels:
        x.text(((x0 + split) / 2, cy - max(h_cpu, h_gpu) / 2 - 34), "CPU", "title", 40, AMBER, a, anchor="mm")
        x.text(((split + x1) / 2, cy - max(h_cpu, h_gpu) / 2 - 34), "GPU", "title", 40, CYAN, a, anchor="mm")
    if ring:
        nx = (x0 + split) / 2 if h_cpu < h_gpu else (split + x1) / 2
        pr = 0.5 + 0.5 * math.sin(t * 4)
        rr = narrow / 2 + 34 + 10 * pr
        x.circle(nx, cy, rr, RED, a * (0.55 + 0.35 * pr), 4)


def meter(x, x0, y, w, frac, c, a, label, value, h=58):
    """Flow meter: a rounded tank that fills from the left."""
    if a <= 0:
        return
    x.d.rounded_rectangle([x0, y, x0 + w, y + h], radius=h / 2, fill=col(GRID, a))
    if frac > 0.01:
        x.d.rounded_rectangle([x0, y, x0 + max(h, w * frac), y + h], radius=h / 2, fill=col(c, a))
        # wave on the fill edge
        ex = x0 + max(h, w * frac)
        for k in range(3):
            x.circle(ex - 8, y + h * (k + 0.5) / 3, 5, WHITE, a * 0.5, 0, fill=WHITE)
    x.text((x0 - 24, y + h / 2), label, "semi", 34, WHITE, a, anchor="rm")
    x.text((x0 + w + 24, y + h / 2), value, "title", 40, c, a, anchor="lm")


def cpu_chip(x, cx, cy, s, a, cores=4, c=None, name=""):
    """Square chip with a visible core grid."""
    if a <= 0:
        return
    c = c or AMBER
    h = s / 2
    x.rect([cx - h, cy - h, cx + h, cy + h], c, a, 4, r=14, fill=PANEL)
    n = int(math.ceil(math.sqrt(cores)))
    rows = int(math.ceil(cores / n))
    cw = (s - 40) / n
    ch = (s - 40) / rows
    for i in range(cores):
        gx = cx - h + 20 + (i % n) * cw
        gy = cy - h + 20 + (i // n) * ch
        x.d.rounded_rectangle([gx + 3, gy + 3, gx + cw - 3, gy + ch - 3], radius=5, fill=col(c, a * 0.55))
    if name:
        x.text((cx, cy + h + 30), name, "semi", 30, WHITE, a, anchor="mm")


def gpu_card(x, cx, cy, w, a, name="", c=None, fans=2):
    """Side view of a graphics card: shroud with fans and a PCIe edge."""
    if a <= 0:
        return
    c = c or CYAN
    h = w * 0.42
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=16, fill=PANEL)
    for k in range(fans):
        fx = cx - w / 2 + w * (k + 0.5) / fans
        r = min(h * 0.36, w / fans * 0.36)
        x.circle(fx, cy - 6, r, c, a, 3)
        x.circle(fx, cy - 6, r * 0.25, c, a, 0, fill=c)
    x.d.rectangle([cx - w * 0.3, cy + h / 2, cx + w * 0.15, cy + h / 2 + 12], fill=col(AMBER, a))
    if name:
        x.text((cx, cy + h / 2 + 46), name, "semi", 30, WHITE, a, anchor="mm")


def gauge(x, cx, cy, r, frac, a, c, label):
    if a <= 0:
        return
    x.d.arc([cx - r, cy - r, cx + r, cy + r], 180, 360, fill=col(GRID, a), width=26)
    x.d.arc([cx - r, cy - r, cx + r, cy + r], 180, 180 + 180 * clamp(frac), fill=col(c, a), width=26)
    x.text((cx, cy - 20), f"{int(round(frac * 100))}%", "title", 64, WHITE, a, anchor="mm")
    x.text((cx, cy + 34), label, "semi", 30, MUTED, a, anchor="mm")


def timeline(x, x0, y, cpu_ms, gpu_ms, a, scale=40, frames=3):
    """Per-frame work bars: CPU lane and GPU lane; the faster lane shows waiting (hatched)."""
    if a <= 0:
        return
    frame_ms = max(cpu_ms, gpu_ms)
    for lane, (ms, c, nm) in enumerate([(cpu_ms, AMBER, "CPU"), (gpu_ms, CYAN, "GPU")]):
        ly = y + lane * 70
        x.text((x0 - 20, ly + 22), nm, "title", 32, c, a, anchor="rm")
        for f in range(frames):
            fx = x0 + f * frame_ms * scale
            x.d.rounded_rectangle([fx + 3, ly, fx + ms * scale - 3, ly + 44], radius=10, fill=col(c, a))
            if ms < frame_ms - 0.1:
                wx0, wx1 = fx + ms * scale + 3, fx + frame_ms * scale - 3
                x.d.rounded_rectangle([wx0, ly, wx1, ly + 44], radius=10, outline=col(MUTED, a), width=2)
                for k in range(int(wx0) + 10, int(wx1) - 4, 18):
                    x.line([(k, ly + 40), (k + 12, ly + 4)], MUTED, a * 0.6, 2, glow=False)
                if f == 0:
                    x.text(((wx0 + wx1) / 2, ly + 22), "wait", "semi", 24, MUTED, a, anchor="mm")


def pct_badge(x, cx, cy, txt, c, a, size=56):
    if a <= 0:
        return
    f = font("title", size)
    tw = x.d.textlength(txt, font=f)
    x.d.rounded_rectangle([cx - tw / 2 - 30, cy - size * 0.8, cx + tw / 2 + 30, cy + size * 0.8], radius=size * 0.8,
                          fill=col(c, a))
    x.text((cx, cy), txt, "title", size, NAVY, a, anchor="mm")


# ---------- scenes ----------
def s_hook(x):
    t = x.t
    a0 = x.b(0)
    # a tiny CPU feeding a huge GPU through a thin pipe
    cpu_chip(x, 330, 470, 150, a0, cores=4, name="processor")
    gpu_card(x, 1380, 470, 640, a0, name="top-end graphics card", fans=3)
    pipe(x, 420, 1050, 470, 34, 150, a0, t, split=700, labels=False, ring=False)
    gauge(x, 1380, 790, 110, lerp(0.0, 0.55, x.since(0) / 2.5), a0, CYAN, "of its frame rate")
    a1 = x.b(1)
    if a1 > 0:
        x.d.rounded_rectangle([560, 150, 1360, 250], radius=50, fill=col(PANEL, a1))
        x.text((960, 200), "CPU or GPU: which one sets your FPS?", "title", 44, WHITE, a1, anchor="mm")


def s_pipe(x):
    t = x.t
    a0 = x.b(0)
    if a0 > 0 and x.t < x.beats[min(3, len(x.beats) - 1)] + 0.4:
        a0b = a0 * (1 - x.b(3))
        # a literal bottle: wide body, narrow neck
        cy = 420
        x.d.rounded_rectangle([360, cy - 150, 1160, cy + 150], radius=60, fill=col(PANEL, a0b))
        x.rect([360, cy - 150, 1160, cy + 150], CYAN, a0b, 5, r=60)
        x.d.rounded_rectangle([1160, cy - 40, 1560, cy + 40], radius=20, fill=col(PANEL, a0b))
        x.rect([1160, cy - 40, 1560, cy + 40], RED, a0b, 5, r=20)
        a1 = x.b(1) * (1 - x.b(3))
        if a1 > 0:
            off = (t * 120) % 60
            for k in range(-1, 14):
                px = 390 + k * 60 + off
                if 380 < px < 1150:
                    for ln in range(5):
                        x.circle(px, cy - 110 + ln * 55, 7, WHITE, a1 * 0.6, 0, fill=WHITE)
            # only one particle per slot leaves through the neck
            for k in range(-1, 8):
                px = 1180 + k * 60 + off
                if 1170 < px < 1550:
                    x.circle(px, cy, 7, WHITE, a1, 0, fill=WHITE)
            x.text((960, cy + 230), "the narrowest part sets the flow", "title", 40, RED, a1, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        pipe(x, 260, 1660, 330, 120, 120, a3, x.since(3), labels=True, ring=False)
        a4 = x.b(4)
        if a4 > 0:
            for k, lab in enumerate(["game logic", "characters", "physics", "draw list"]):
                x.text((460 + (k % 2) * 270, 470 + (k // 2) * 44), lab, "semi", 28, AMBER, a4, anchor="mm")
        a5 = x.b(5)
        if a5 > 0:
            for i in range(6):
                for j in range(2):
                    p = clamp((x.since(5) - (i + j * 6) * 0.08) / 0.3)
                    x.d.rounded_rectangle([1180 + i * 46, 456 + j * 46, 1218 + i * 46, 494 + j * 46], radius=6,
                                          fill=col(CYAN, a5 * p))
            x.text((1310, 580), "pixels", "semi", 28, CYAN, a5, anchor="mm")
        a6 = x.b(6)
        timeline(x, 520, 690, 9, 14, a6, scale=30, frames=3)
        a7 = x.b(7)
        if a7 > 0:
            x.text((960, 900), "Slower stage = your frame rate. The other one waits.", "title", 40, WHITE, a7, anchor="mm")


def s_always(x):
    t = x.t
    a0 = x.b(0)
    combos = [(140, 70, "PC 1"), (70, 150, "PC 2"), (110, 90, "PC 3")]
    for k, (hc, hg, nm) in enumerate(combos):
        a = a0 * clamp((x.since(0) - k * 0.4) / 0.5)
        cy = 260 + k * 190
        pipe(x, 420, 1260, cy, hc, hg, a, t, labels=(k == 0), ring=True)
        x.text((380, cy), nm, "semi", 32, MUTED, a, anchor="rm")
        if k == 0:
            # GPU-limited: the good case
            a2 = x.b(2)
            if a2 > 0:
                x.text((1310, cy - 20), "GPU-limited", "title", 34, GREEN, a2, anchor="lm")
                x.text((1310, cy + 22), "ideal: full use of the", "semi", 26, WHITE, a2, anchor="lm")
                x.text((1310, cy + 54), "priciest part", "semi", 26, WHITE, a2, anchor="lm")
    a1 = x.b(1)
    if a1 > 0:
        pct_badge(x, 1720, 450, "not a fault", MUTED, a1, size=36)
    a3 = x.b(3)
    if a3 > 0:
        x.d.rounded_rectangle([420, 820, 1500, 910], radius=45, fill=col(PANEL, a3))
        q = "Which part?" if x.b(4) <= 0 else "Which part?   How much?"
        x.text((960, 865), q, "title", 46, WHITE, a3, anchor="mm")


def s_test(x):
    a0 = x.b(0)
    if a0 > 0:
        x.d.rounded_rectangle([200, 140, 1720, 900], radius=30, fill=col(PANEL, a0 * 0.6))
        x.text((260, 185), "TEST BENCH", "title", 34, MUTED, a0, anchor="lm")
    a1 = x.b(1)
    cpu_chip(x, 380, 420, 150, a1, cores=4, name="Core i3 13100 (4 cores)")
    gpus = ["RTX 3060", "RTX 3080", "RTX 4090"]
    for k, g in enumerate(gpus):
        ak = a1 * clamp((x.since(1) - 1.2 - k * 0.5) / 0.5)
        gpu_card(x, 780 + k * 380, 300, 260, ak, name=g, fans=2 + (k == 2))
    a2 = x.b(2)
    cpu_chip(x, 380, 720, 150, a2, cores=24, c=WHITE, name="Core i9 13900K")
    # result cells
    for row in range(2):
        for k in range(3):
            ar = (a1 if row == 0 else a2) * clamp((x.since(1 + row) - 1.0) / 0.5)
            cx, cy = 780 + k * 380, 470 + row * 250
            if row == 1:
                cy = 720
            x.d.rounded_rectangle([cx - 140, cy - 50, cx + 140, cy + 50], radius=20, outline=col(GRID, ar), width=3)
            x.text((cx, cy), "?", "title", 50, MUTED, ar, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        pct_badge(x, 1280, 185, "Watch Dogs Legion  ·  Very High", CYAN, a3, size=30)
    a5 = x.b(5)
    if a5 > 0:
        x.text((960, 870), "Only the parts change", "title", 36, WHITE, a5, anchor="mm")


def s_3060(x):
    t = x.t
    a0 = x.b(0)
    if a0 > 0:
        gpu_card(x, 1580, 250, 220, a0, name="RTX 3060")
        pct_badge(x, 260, 170, "1080p", MUTED, a0, size=30)
    pipe(x, 260, 1360, 300, 150, 56, a0, t, split=860)
    a1 = x.b(1)
    meter(x, 520, 520, 1000, lerp(0, 0.97, x.since(1) / 1.2), AMBER, a1, "Core i3", "100")
    meter(x, 520, 620, 1000, lerp(0, 1.0, x.since(1) / 1.2), WHITE, a1, "Core i9", "103")
    if a1 > 0:
        x.text((1020, 720), "relative frame rate (Core i3 = 100)", "semi", 24, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    pct_badge(x, 1800, 570, "+3%", AMBER, a2, size=56)
    a4 = x.b(4)
    timeline(x, 560, 790, 6, 13, a4, scale=26, frames=3)


def s_3080(x):
    t = x.t
    a0 = x.b(0)
    grow = ease(x.since(0) / 2.0) if a0 > 0 else 0
    if a0 > 0:
        gpu_card(x, 1580, 250, lerp(220, 300, grow), a0, name="RTX 3080", fans=2)
    hg = lerp(56, 190, grow)
    pipe(x, 260, 1360, 320, 120, hg, max(a0, 0.001) if a0 > 0 else 0, t, split=860)
    a1 = x.b(1)
    meter(x, 520, 580, 1000, lerp(0, 0.667, x.since(1) / 1.2), AMBER, a1, "Core i3", "100")
    meter(x, 520, 680, 1000, lerp(0, 1.0, x.since(1) / 1.2), WHITE, a1, "Core i9", "150")
    pct_badge(x, 1790, 630, "+50%", WHITE, a1, size=56)
    if a1 > 0:
        x.text((1020, 760), "relative frame rate (Core i3 = 100)", "semi", 24, MUTED, a1, anchor="mm")
    a4 = x.b(4)
    if a4 > 0:
        x.text((960, 810), "Same CPU. Different bottleneck.", "title", 48, RED, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.text((960, 890), "\"Is my CPU good enough?\"  depends on the GPU and the game", "semi", 32, MUTED, a5,
               anchor="mm")


def s_4090(x):
    a0 = x.b(0)
    if a0 > 0:
        gpu_card(x, 300, 230, 300, a0, name="RTX 4090", fans=3)
        x.text((560, 160), "1080p", "title", 36, MUTED, a0, anchor="lm")
    a1 = x.b(1)
    meter(x, 720, 210, 700, lerp(0, 102 / 186, x.since(1) / 1.2), AMBER, a1, "Core i3", "102 fps")
    a2 = x.b(2)
    meter(x, 720, 300, 700, lerp(0, 1.0, x.since(2) / 1.2), WHITE, a2, "Core i9", "186 fps")
    pct_badge(x, 1700, 400, "+82%", WHITE, a2, size=44)
    # line chart 1080p -> 4K
    a4 = x.b(4)
    if a4 > 0:
        gx0, gx1, gy0, gy1 = 560, 1300, 520, 880
        x.line([(gx0, gy0), (gx0, gy1), (gx1, gy1)], MUTED, a4, 3, glow=False)
        def Y(v):
            return gy1 - (v - 60) / (200 - 60) * (gy1 - gy0)
        for v in (100, 150):
            x.text((gx0 - 16, Y(v)), str(v), "mono", 24, MUTED, a4, anchor="rm")
        x.text((gx0 + 80, gy1 + 30), "1080p", "semi", 28, WHITE, a4, anchor="mm")
        x.text((gx1 - 80, gy1 + 30), "4K", "semi", 28, WHITE, a4, anchor="mm")
        p = ease(x.since(4) / 1.5)
        for (v0, v1, c, nm) in [(186, 149, WHITE, "Core i9"), (102, 99, AMBER, "Core i3")]:
            p0 = (gx0 + 80, Y(v0))
            p1 = (lerp(gx0 + 80, gx1 - 80, p), lerp(Y(v0), Y(v1), p))
            x.line([p0, p1], c, a4, 6)
            x.circle(*p0, 10, c, a4, 0, fill=c)
            x.circle(*p1, 10, c, a4, 0, fill=c)
            x.text((p0[0] - 22, p0[1]), f"{v0}", "title", 30, c, a4, anchor="rm")
            if p > 0.95:
                x.text((p1[0] + 24, p1[1]), f"{v1}  {nm}", "title", 30, c, a4, anchor="lm")
    a5 = x.b(5)
    if a5 > 0:
        # pixel area: 1 block vs 4 blocks
        bx, by = 1480, 560
        x.d.rectangle([bx, by, bx + 90, by + 50], fill=col(CYAN, a5))
        x.text((bx + 45, by + 75), "1080p", "semi", 24, WHITE, a5, anchor="mm")
        for i in range(2):
            for j in range(2):
                x.d.rectangle([bx + i * 94, by + 120 + j * 54, bx + i * 94 + 90, by + 170 + j * 54], fill=col(CYAN, a5))
        x.text((bx + 92, by + 260), "4K = 4x the pixels", "semi", 24, WHITE, a5, anchor="mm")
    a6 = x.b(6)
    if a6 > 0:
        x.text((960, 470), "Flat line = CPU limit", "title", 40, RED, a6, anchor="mm")


def s_why_res(x):
    a0 = x.b(0)
    if a0 > 0:
        x.text((560, 160), "1080p", "title", 40, WHITE, a0, anchor="mm")
        x.text((1360, 160), "4K", "title", 40, WHITE, a0, anchor="mm")
        x.line([(960, 140), (960, 680)], GRID, a0, 3, glow=False)
    a1 = x.b(1)
    stack = ["game logic", "characters", "physics", "draw list"]
    for side, cx in enumerate((420, 1220)):
        for k, s in enumerate(stack):
            ak = a1 * clamp((x.since(1) - k * 0.25) / 0.4)
            y = 520 - k * 80
            x.d.rounded_rectangle([cx - 110, y, cx + 110, y + 64], radius=14, fill=col(AMBER, ak * 0.85))
            x.text((cx, y + 32), s, "semi", 26, NAVY, ak, anchor="mm")
        x.text((cx, 620), "CPU work", "semi", 28, AMBER, a1, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        g = ease(x.since(3) / 1.5)
        for side, (cx, s) in enumerate(((680, 1.0), (1500, lerp(1.0, 2.0, g)))):
            w, h = 150 * s, 84 * s
            x.d.rounded_rectangle([cx - w / 2, 590 - h, cx + w / 2, 590], radius=10, fill=col(CYAN, a3 * 0.85))
            x.text((cx, 620), "GPU work", "semi", 28, CYAN, a3, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        items = ["crowds", "vehicles", "physics", "draw distance", "ray tracing"]
        for k, s in enumerate(items):
            ak = a5 * clamp((x.since(5) - k * 0.45) / 0.4)
            cx = 260 + k * 350
            x.circle(cx, 790, 54, AMBER, ak, 4, fill=PANEL)
            # tiny icon per item
            if k == 0:
                for j in range(3):
                    x.circle(cx - 22 + j * 22, 780, 8, AMBER, ak, 0, fill=AMBER)
                    x.line([(cx - 22 + j * 22, 790), (cx - 22 + j * 22, 812)], AMBER, ak, 5, glow=False)
            elif k == 1:
                x.d.rounded_rectangle([cx - 30, 776, cx + 30, 800], radius=6, fill=col(AMBER, ak))
                x.circle(cx - 16, 806, 8, AMBER, ak, 0, fill=AMBER)
                x.circle(cx + 16, 806, 8, AMBER, ak, 0, fill=AMBER)
            elif k == 2:
                x.circle(cx, 790, 14, AMBER, ak, 0, fill=AMBER)
                x.d.arc([cx - 34, 756, cx + 34, 824], 200, 330, fill=col(AMBER, ak), width=4)
            elif k == 3:
                x.line([(cx - 34, 812), (cx, 768), (cx + 34, 812)], AMBER, ak, 4, glow=False)
            else:
                x.line([(cx - 30, 770), (cx + 4, 796), (cx + 28, 772)], AMBER, ak, 4, glow=False)
                x.circle(cx - 30, 770, 6, AMBER, ak, 0, fill=AMBER)
            x.text((cx, 880), s, "semi", 28, WHITE, ak, anchor="mm")


def s_check(x):
    a1 = x.b(1)
    if a1 > 0:
        x.d.rounded_rectangle([160, 150, 760, 520], radius=24, fill=col(PANEL, a1))
        x.text((190, 185), "PERFORMANCE OVERLAY", "semi", 26, MUTED, a1, anchor="lm")
        frac = 0.98 if x.b(3) <= 0 else lerp(0.98, 0.62, x.since(3) / 1.2)
        gauge(x, 460, 420, 150, frac, a1, CYAN if frac > 0.9 else RED, "GPU usage")
    a2 = x.b(2)
    if a2 > 0 and x.b(3) < 1:
        x.text((1000, 260), "near 100%  =  GPU-limited (fine)", "title", 36, GREEN, a2 * (1 - x.b(3)), anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((860, 240), "well below  =  CPU-limited", "title", 36, RED, a3, anchor="lm")
        x.text((860, 290), "(if no frame cap or V-Sync)", "semi", 28, MUTED, a3, anchor="lm")
    a4 = x.b(4)
    if a4 > 0:
        loads = [1.0, 0.97, 0.9, 0.35, 0.3, 0.22, 0.2, 0.15, 0.12, 0.1, 0.1, 0.08]
        bx = 860
        for k, l in enumerate(loads):
            h = 220 * l * ease(x.since(4) / 1.0)
            c = RED if l > 0.85 else AMBER
            x.d.rounded_rectangle([bx + k * 64, 600 - h, bx + k * 64 + 46, 600], radius=8, fill=col(c, a4))
            x.d.rounded_rectangle([bx + k * 64, 380, bx + k * 64 + 46, 600], radius=8, outline=col(GRID, a4), width=2)
        x.text((bx, 640), "per-core usage", "semi", 28, WHITE, a4, anchor="la")
        x.text((bx + 760, 640), "total looks low", "semi", 28, MUTED, a4, anchor="ra")
    a6 = x.b(6)
    if a6 > 0:
        cpu_chip(x, 520, 790, 130, a6, cores=6, name="Ryzen 5600X: 6 cores")
        x.text((960, 790), "≈", "monob", 90, WHITE, a6, anchor="mm")
        cpu_chip(x, 1400, 790, 130, a6, cores=16, c=WHITE, name="Ryzen 5950X: 16 cores")
        x.text((960, 880), "in most games", "semi", 28, MUTED, a6, anchor="mm")


def s_calc(x):
    a0 = x.b(0)
    if a0 > 0 and x.b(5) < 1:
        ah = a0 * (1 - x.b(5))
        x.d.rounded_rectangle([200, 180, 760, 620], radius=28, fill=col(PANEL, ah))
        x.text((480, 230), "BOTTLENECK CALCULATOR", "semi", 26, MUTED, ah, anchor="mm")
        x.d.rounded_rectangle([250, 280, 710, 340], radius=12, outline=col(GRID, ah), width=3)
        x.text((270, 310), "CPU: Core i3 13100", "semi", 26, WHITE, ah, anchor="lm")
        x.d.rounded_rectangle([250, 360, 710, 420], radius=12, outline=col(GRID, ah), width=3)
        x.text((270, 390), "GPU: RTX 4090", "semi", 26, WHITE, ah, anchor="lm")
        x.text((480, 520), "??%", "title", 90, WHITE, ah, anchor="mm")
        stamp(x, 480, 500, "ONE NUMBER?", RED, x.b(1) * (1 - x.b(5)), angle=-9)
    a3 = x.b(3)
    if a3 > 0 and x.b(5) < 1:
        ah = a3 * (1 - x.b(5))
        steps = [("RTX 3060", 3), ("RTX 3080", 50), ("RTX 4090", 82)]
        for k, (g, v) in enumerate(steps):
            ak = ah * clamp((x.since(3) - k * 0.5) / 0.4)
            cy = 260 + k * 140
            meter(x, 1100, cy, 500, v / 100, AMBER if v > 10 else MUTED, ak, g, f"+{v}%", h=50)
        x.text((1350, 700), "Core i9 lead over the same Core i3", "semi", 26, MUTED, ah, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.text((960, 170), "Why reviewers test CPUs at 1080p", "title", 46, WHITE, a5, anchor="mm")
        pipe(x, 300, 1620, 470, 70, 230, a5, x.since(5), split=900)
        a6 = x.b(6)
        if a6 > 0:
            x.line([(300, 660), (1620, 660)], RED, a6, 4, glow=False)
            x.text((960, 710), "the CPU's real ceiling", "title", 40, RED, a6, anchor="mm")
            x.text((960, 780), "the number you'll hit after your next GPU upgrade", "semi", 32, MUTED, a6, anchor="mm")


def slider(x, x0, y, w, val, a, label, c):
    if a <= 0:
        return
    x.text((x0, y - 30), label, "semi", 28, WHITE, a, anchor="ld")
    x.d.rounded_rectangle([x0, y - 6, x0 + w, y + 6], radius=6, fill=col(GRID, a))
    x.d.rounded_rectangle([x0, y - 6, x0 + w * val, y + 6], radius=6, fill=col(c, a))
    x.circle(x0 + w * val, y, 18, c, a, 0, fill=c)


def s_fix(x):
    a0 = x.b(0)
    if a0 > 0:
        for cx, nm, c in ((520, "GPU-limited", CYAN), (1400, "CPU-limited", AMBER)):
            x.d.rounded_rectangle([cx - 380, 140, cx + 380, 640], radius=28, fill=col(PANEL, a0 * 0.8))
            x.text((cx, 190), nm, "title", 42, c, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        p = ease(x.since(1) / 1.5)
        slider(x, 220, 320, 600, lerp(0.9, 0.55, p), a1, "Heaviest settings", CYAN)
        slider(x, 220, 440, 600, 0.0 if p < 0.6 else 1.0, a1, "Upscaling: " + ("ON" if p >= 0.6 else "OFF"), CYAN)
        x.text((520, 560), "fewer pixels, more FPS", "semi", 28, MUTED, a1, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        p = ease(x.since(3) / 1.5)
        slider(x, 1100, 320, 600, lerp(0.5, 0.95, p), a3, "Resolution / textures / lighting", GREEN)
    a4 = x.b(4)
    if a4 > 0:
        p = ease(x.since(4) / 1.5)
        slider(x, 1100, 440, 600, lerp(0.9, 0.4, p), a4, "Crowd density, view distance", AMBER)
        x.text((1400, 560), "free quality, same FPS", "semi", 28, MUTED, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        x.d.rounded_rectangle([140, 690, 1780, 770], radius=40, fill=col(PANEL, a5))
        x.text((960, 730), "Above your refresh rate? Cap the frame rate: smoother, less power", "semi", 32, WHITE, a5,
               anchor="mm")
    a6 = x.b(6)
    if a6 > 0:
        pct_badge(x, 960, 860, "Upgrade the CPU only if it holds you well below your target", AMBER, a6, size=34)


def s_outro(x):
    t = x.t
    a0 = x.b(0)
    pipe(x, 260, 1300, 400, 150, 70, a0 * (1 - x.b(2)), t, split=780)
    a1 = x.b(1)
    if a1 > 0 and x.b(2) < 1:
        ah = a1 * (1 - x.b(2))
        x.circle(1040, 410, 100, WHITE, ah, 6)
        x.line([(1111, 481), (1210, 580)], WHITE, ah, 14, glow=False)
        x.text((780, 620), "Find the narrow part before you buy anything", "title", 40, WHITE, ah, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((960, 180), "NEXT VIDEO", "semi", 30, MUTED, a2, anchor="mm")
        # PSU box with fan grill
        x.rect([660, 260, 1260, 640], CYAN, a2, 5, r=20, fill=PANEL)
        x.circle(860, 450, 130, CYAN, a2, 4)
        for k in range(5):
            r = 26 + k * 24
            x.circle(860, 450, r, CYAN, a2 * 0.5, 2)
        x.d.rounded_rectangle([1080, 300, 1220, 360], radius=10, outline=col(AMBER, a2), width=3)
        x.text((1150, 330), "80 PLUS", "semi", 22, AMBER, a2, anchor="mm")
        x.text((1150, 470), "W", "title", 90, WHITE, a2, anchor="mm")
        x.text((960, 710), "Power Supplies Explained", "title", 56, WHITE, a2, anchor="mm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((960, 790), "watts  ·  80 Plus ratings  ·  why cheap ones fail", "semi", 34, MUTED, a3, anchor="mm")
    a4 = x.b(4)
    if a4 > 0:
        pct_badge(x, 960, 880, "Subscribe", RED, a4, size=40)


SCENES = [("Half the frame rate", s_hook),
          ("What a bottleneck is", s_pipe),
          ("Every PC has one", s_always),
          ("One CPU, three GPUs", s_test),
          ("RTX 3060: GPU-limited", s_3060),
          ("RTX 3080: the limit moves", s_3080),
          ("RTX 4090: 1080p vs 4K", s_4090),
          ("Why resolution doesn't load the CPU", s_why_res),
          ("Check your own PC", s_check),
          ("Bottleneck calculators and CPU reviews", s_calc),
          ("Free fixes for each case", s_fix),
          ("Up next", s_outro)]
