"""Scenes for video 08: What Actually Raises FPS (and 5 Myths That Don't).

Design language (arctic theme): a lab bench. One example PC is measured like an experiment:
a big seven-segment style counter, a frame-time "lap" bar against a 16.7 ms target line, a
two-lane relay track (CPU lane and GPU lane), a BIOS toggle panel, a pixel-area diagram, a
frame timeline with real and generated frames, and myth "test cards" that print a result and
get a BARELY MOVES verdict. Rounded instrument panels, thin rulers with tick marks, no glow.
"""
import math
from render import *  # noqa: F401,F403


# ---------- helpers for this video ----------
def arrow(x, p0, p1, c, a, w=5, head=20):
    if a <= 0:
        return
    ang = math.atan2(p1[1] - p0[1], p1[0] - p0[0])
    bx, by = p1[0] - head * math.cos(ang), p1[1] - head * math.sin(ang)
    x.line([p0, (bx, by)], c, a, w, glow=False)
    pts = [p1, (bx + head * 0.6 * math.sin(ang), by - head * 0.6 * math.cos(ang)),
           (bx - head * 0.6 * math.sin(ang), by + head * 0.6 * math.cos(ang))]
    x.d.polygon(pts, fill=col(c, a))


def panel(x, box, a, c=None, r=22, w=3):
    x.rect(box, c or GRID, a, w, r=r, fill=PANEL, glow=False)


def counter(x, cx, cy, val, a, size=150, c=None, unit="FPS"):
    """Big instrument readout with a unit label underneath."""
    if a <= 0:
        return
    x.text((cx, cy), f"{int(round(val))}", "monob", size, c or WHITE, a, anchor="mm")
    x.text((cx, cy + size * 0.62), unit, "semi", int(size * 0.22), MUTED, a, anchor="mm")


def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def lap_bar(x, x0, y, ms, a, scale=34, target=True, c=None, label=True):
    """Frame-time bar: length = milliseconds per frame, with the 16.7 ms (60 FPS) target line."""
    if a <= 0:
        return
    full = 25 * scale
    x.d.rounded_rectangle([x0, y, x0 + full, y + 46], radius=12, fill=col(GRID, a * 0.7))
    x.d.rounded_rectangle([x0, y, x0 + ms * scale, y + 46], radius=12, fill=col(c or CYAN, a))
    for k in range(0, 26, 5):
        tx = x0 + k * scale
        x.line([(tx, y + 54), (tx, y + 66)], MUTED, a, 2, glow=False)
        x.text((tx, y + 72), f"{k}", "mono", 22, MUTED, a, anchor="ma")
    if target:
        tx = x0 + 16.7 * scale
        x.line([(tx, y - 26), (tx, y + 50)], GREEN, a, 4, glow=False)
        x.text((tx, y - 30), "60 FPS = 16.7 ms", "semi", 24, GREEN, a, anchor="md")
    if label:
        x.text((x0 + full + 24, y + 23), f"{ms:.1f} ms", "monob", 38, c or CYAN, a, anchor="lm")


def runner(x, cx, cy, s, c, a, phase=0.0):
    """Stick-figure runner made of circles and lines; phase animates the legs."""
    if a <= 0:
        return
    x.circle(cx, cy - s * 1.1, s * 0.28, c, a, 4, fill=c)
    hip = (cx, cy - s * 0.2)
    sh = (cx + s * 0.08, cy - s * 0.75)
    x.line([sh, hip], c, a, 6, glow=False)
    sw = math.sin(phase) * 0.6
    for sgn in (1, -1):
        k = sgn * sw
        x.line([hip, (cx + s * 0.45 * k, cy + s * 0.35), (cx + s * 0.6 * k - s * 0.1, cy + s * 0.75)], c, a, 6, glow=False)
        x.line([sh, (cx - s * 0.4 * k, cy - s * 0.45), (cx - s * 0.5 * k + s * 0.15, cy - s * 0.2)], c, a, 5, glow=False)


def verdict(x, cx, cy, a, text="BARELY MOVES"):
    stamp(x, cx, cy, text, RED, a, angle=-7)


def gauge(x, cx, cy, r, frac, a, c=None, label="GPU"):
    """Half-circle usage gauge, 0..100%."""
    if a <= 0:
        return
    box = [cx - r, cy - r, cx + r, cy + r]
    x.d.arc(box, 180, 360, fill=col(GRID, a), width=26)
    x.d.arc(box, 180, 180 + 180 * clamp(frac), fill=col(c or CYAN, a), width=26)
    x.text((cx, cy - 20), f"{int(frac * 100)}%", "monob", int(r * 0.42), WHITE, a, anchor="mm")
    x.text((cx, cy + 34), label, "semi", 30, MUTED, a, anchor="mm")


def example_tag(x, a, xy=(150, 132)):
    x.text(xy, "EXAMPLE PC  ·  illustration", "semi", 24, MUTED, a, anchor="lm")


# ---------- scenes ----------
def s_hook(x):
    a0 = x.b(0)
    example_tag(x, a0)
    if a0 > 0:
        # monitor
        panel(x, [180, 200, 940, 650], a0, WHITE, r=18, w=6)
        x.rect([520, 650, 600, 720], WHITE, a0, 6, r=4, glow=False)
        x.rect([440, 720, 680, 740], WHITE, a0, 6, r=6, glow=False)
        p = ease((x.since(0) - 3.5) / 6)
        v = lerp(48, 86, p)
        counter(x, 560, 400, v, a0, size=170, c=AMBER if p < 1 else GREEN)
        # progress ruler 48 -> 86
        x.line([(1060, 420), (1740, 420)], MUTED, a0, 4, glow=False)
        for k, (lab, f) in enumerate([("48", 0), ("60", 0.32), ("86", 1.0)]):
            tx = 1060 + 680 * f
            x.line([(tx, 404), (tx, 436)], MUTED, a0, 3, glow=False)
            x.text((tx, 460), lab, "mono", 28, MUTED, a0, anchor="ma")
        x.circle(1060 + 680 * p, 420, 16, GREEN, a0, 3, fill=GREEN)
        x.text((1400, 350), "no new parts", "title", 46, WHITE, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((1400, 600), "5 popular tricks", "semi", 34, MUTED, a1, anchor="mm")
        for k in range(5):
            cx = 1110 + k * 145
            ak = a1 * ease((x.since(1) - k * 0.35) / 0.5)
            panel(x, [cx - 55, 650, cx + 55, 790], ak, RED, r=12, w=3)
            x.text((cx, 700), "?", "title", 54, RED, ak, anchor="mm")
            x.text((cx, 760), f"myth {k + 1}", "semi", 22, MUTED, ak, anchor="mm")


def s_relay(x):
    a0 = x.b(0)
    if a0 > 0:
        x.text((960, 170), "One frame = one relay lap", "title", 54, WHITE, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        for k, (name, c, y) in enumerate([("CPU", AMBER, 330), ("GPU", CYAN, 500)]):
            x.d.rounded_rectangle([260, y - 60, 1660, y + 60], radius=60, fill=col(GRID, a1 * 0.6))
            x.text((220, y), name, "title", 40, c, a1, anchor="rm")
        t = x.since(1)
        lap = 3.0
        ph = (t % lap) / lap
        cpu_x = 320 + 1280 * clamp(ph / 0.45)
        gpu_x = 320 + 1280 * clamp((ph - 0.45) / 0.55)
        runner(x, cpu_x, 330, 62, AMBER, a1, t * 9)
        runner(x, gpu_x, 500, 62, CYAN, a1 * (1 if ph > 0.45 else 0.35), t * 9 if ph > 0.45 else 0)
        x.text((300, 395), "game logic, draw list", "semi", 24, MUTED, a1, anchor="la")
        x.text((300, 565), "paints the pixels", "semi", 24, MUTED, a1, anchor="la")
    a2 = x.b(3)
    lap_bar(x, 300, 700, 1000 / 48, a2, scale=46, c=AMBER)
    a4 = x.b(5)
    if a4 > 0:
        x.text((960, 880), "The slower runner sets the pace", "title", 40, RED, a4, anchor="mm")


def s_preset(x):
    a0 = x.b(0)
    if a0 > 0:
        panel(x, [150, 150, 760, 600], a0)
        gauge(x, 455, 420, 190, 0.99, a0, CYAN, "GPU usage")
        x.text((455, 520), "CPU usage 55%  ·  waiting", "semi", 26, MUTED, a0, anchor="mm")
    a1 = x.b(2)
    if a1 > 0:
        # preset slider
        panel(x, [150, 640, 760, 900], a1)
        presets = ["Low", "Medium", "High", "Ultra"]
        x.line([(220, 780), (690, 780)], MUTED, a1, 5, glow=False)
        for k, p in enumerate(presets):
            tx = 220 + k * 156.7
            x.line([(tx, 765), (tx, 795)], MUTED, a1, 3, glow=False)
            x.text((tx, 830), p, "semi", 26, WHITE, a1, anchor="ma")
        pos = lerp(3, 2, (x.since(2) - 0.8) / 1.2)
        kx = 220 + pos * 156.7
        x.circle(kx, 780, 24, AMBER, a1, 4, fill=AMBER)
        x.text((455, 700), "Graphics preset", "semi", 30, MUTED, a1, anchor="mm")
    a2 = x.b(3)
    if a2 > 0:
        x.text((880, 175), "TechSpot: Ultra -> High", "title", 42, WHITE, a2, anchor="lm")
        x.d.rounded_rectangle([880, 230, 880 + 900 * 0.25, 290], radius=14, fill=col(GRID, a2))
        x.d.rounded_rectangle([880 + 900 * 0.15 / 1, 230, 880 + 900 * 0.25, 290], radius=14, fill=col(CYAN, a2))
        x.text((880 + 900 * 0.25 + 24, 260), "typically 15–25% faster", "semi", 32, CYAN, a2, anchor="lm")
    a3 = x.b(4)
    if a3 > 0:
        g = ease(x.since(4) / 1.0)
        x.text((880, 370), "Cyberpunk 2077", "semi", 30, WHITE, a3, anchor="lm")
        x.d.rounded_rectangle([880, 400, 880 + 700 * g, 450], radius=12, fill=col(CYAN, a3))
        x.text((880 + 700 * g + 20, 425), "+24%", "monob", 34, CYAN, a3, anchor="lm")
    a4 = x.b(5)
    if a4 > 0:
        x.text((880, 530), "Flight Simulator, 4K", "semi", 30, WHITE, a4, anchor="lm")
        for k, (lab, v, c) in enumerate([("Ultra", 45, MUTED), ("High", 57, GREEN)]):
            g = ease((x.since(5) - k * 0.5) / 0.8)
            y = 570 + k * 80
            x.text((880, y + 25), lab, "semi", 26, MUTED, a4, anchor="lm")
            x.d.rounded_rectangle([990, y, 990 + 11 * v * g, y + 50], radius=12, fill=col(c, a4))
            x.text((1000 + 11 * v * g + 14, y + 25), f"{v} FPS", "monob", 32, c, a4, anchor="lm")
    a5 = x.b(6)
    if a5 > 0:
        x.text((880, 820), "Ultra = effects you rarely notice mid-game", "semi", 32, AMBER, a5, anchor="lm")


def scene_pic(x, box, a, extra=False):
    """Tiny stylised landscape: sky, sun, two hills; 'extra' adds faint ultra-only haze lines."""
    if a <= 0:
        return
    x0, y0, x1, y1 = box
    x.d.rounded_rectangle(box, radius=16, fill=col(CYAN, a * 0.18), outline=col(WHITE, a), width=4)
    x.circle(x0 + (x1 - x0) * 0.75, y0 + (y1 - y0) * 0.3, (y1 - y0) * 0.11, AMBER, a, 3, fill=AMBER)
    w, h = x1 - x0, y1 - y0
    x.d.polygon([(x0 + 4, y1 - 4), (x0 + w * 0.35, y0 + h * 0.45), (x0 + w * 0.7, y1 - 4)], fill=col(CYAN, a * 0.8))
    x.d.polygon([(x0 + w * 0.4, y1 - 4), (x0 + w * 0.72, y0 + h * 0.55), (x1 - 4, y1 - 4)], fill=col(GREEN, a * 0.75))
    if extra:
        for k in range(3):
            yy = y0 + h * (0.25 + 0.08 * k)
            x.line([(x0 + w * 0.08, yy), (x0 + w * 0.55, yy)], WHITE, a * 0.25, 3, glow=False)


def s_preset_result(x):
    a0 = x.b(0)
    if a0 > 0:
        p = ease((x.since(0) - 0.5) / 1.5)
        counter(x, 330, 300, lerp(48, 58, p), a0, size=130, c=CYAN)
        example_tag(x, a0, (150, 132))
        lap_bar(x, 620, 260, lerp(1000 / 48, 1000 / 58, p), a0, scale=36)
    a1 = x.b(1)
    if a1 > 0:
        scene_pic(x, [220, 470, 760, 770], a1, extra=True)
        x.text((490, 800), "Ultra", "semi", 30, MUTED, a1, anchor="ma")
        scene_pic(x, [860, 470, 1400, 770], a1, extra=False)
        x.text((1130, 800), "High", "semi", 30, MUTED, a1, anchor="ma")
        x.text((1600, 620), "≈", "title", 110, WHITE, a1, anchor="mm")
    a3 = x.b(4)
    if a3 > 0:
        panel(x, [1480, 690, 1800, 900], a3, AMBER)
        x.text((1640, 730), "Textures", "semi", 28, WHITE, a3, anchor="mm")
        x.text((1640, 775), "cost VRAM,", "semi", 26, AMBER, a3, anchor="mm")
        x.text((1640, 815), "not much speed", "semi", 26, AMBER, a3, anchor="mm")
        g = ease(x.since(4) / 1.2)
        x.d.rounded_rectangle([1520, 845, 1520 + 240 * g * 0.7, 875], radius=10, fill=col(AMBER, a3))
        x.d.rounded_rectangle([1520, 845, 1760, 875], radius=10, outline=col(MUTED, a3), width=2)


def s_upscale(x):
    a0 = x.b(0)
    if a0 > 0:
        x.text((150, 160), "Upscaling: draw small, rebuild big", "title", 50, WHITE, a0, anchor="lm")
    # full 1440p frame
    X0, Y0, S = 150, 260, 0.27  # 2560*0.27 = 691, 1440*0.27 = 389
    a1 = x.b(1)
    if a1 > 0:
        x.d.rectangle([X0, Y0, X0 + 2560 * S, Y0 + 1440 * S], outline=col(WHITE, a1), width=4)
        for gx in range(0, 2560, 160):
            x.line([(X0 + gx * S, Y0), (X0 + gx * S, Y0 + 1440 * S)], GRID, a1, 1, glow=False)
        for gy in range(0, 1440, 160):
            x.line([(X0, Y0 + gy * S), (X0 + 2560 * S, Y0 + gy * S)], GRID, a1, 1, glow=False)
        x.text((X0 + 2560 * S / 2, Y0 + 1440 * S + 30), "Output: 2560 × 1440", "semi", 28, MUTED, a1, anchor="ma")
    a2 = x.b(2)
    if a2 > 0:
        g = ease(x.since(2) / 1.2)
        f = lerp(1.0, 0.667, g)
        x.d.rectangle([X0, Y0, X0 + 2560 * S * f, Y0 + 1440 * S * f], fill=col(CYAN, a2 * 0.55), outline=col(CYAN, a2), width=4)
        x.text((1000, 300), "DLSS Quality", "title", 44, CYAN, a2, anchor="lm")
        x.text((1000, 360), "67% of each side", "semi", 32, WHITE, a2, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((1000, 420), "1707 × 960 rendered", "monob", 34, WHITE, a3, anchor="lm")
    a4 = x.b(4)
    if a4 > 0:
        x.text((1000, 500), "0.67 × 0.67 =", "mono", 34, MUTED, a4, anchor="lm")
        x.text((1290, 500), "44% of the pixels", "title", 40, AMBER, a4, anchor="lm")
    a5 = x.b(5)
    if a5 > 0:
        x.d.rectangle([X0, Y0, X0 + 2560 * S * 0.5, Y0 + 1440 * S * 0.5], outline=col(AMBER, a5), width=5)
        x.text((X0 + 10, Y0 + 1440 * S * 0.5 - 10), "Performance: 25%", "semi", 22, AMBER, a5, anchor="ld")
        x.text((1000, 580), "Performance mode: 50% per side = ¼", "semi", 30, WHITE, a5, anchor="lm")
    a6 = x.b(6)
    if a6 > 0:
        p = ease((x.since(6) - 0.3) / 1.5)
        panel(x, [1000, 660, 1760, 900], a6, CYAN)
        example_tag(x, a6, (1030, 700))
        counter(x, 1180, 780, lerp(58, 78, p), a6, size=100, c=CYAN)
        lap_bar(x, 1300, 760, lerp(1000 / 58, 1000 / 78, p), a6, scale=12, target=False, label=False)
        x.text((1300, 740), f"{lerp(1000 / 58, 1000 / 78, p):.1f} ms per frame", "mono", 24, MUTED, a6, anchor="ld")


def toggle(x, cx, cy, on, a):
    w, h = 120, 56
    c = GREEN if on > 0.5 else MUTED
    x.d.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=h / 2, fill=col(c, a))
    kx = lerp(cx - w / 2 + h / 2, cx + w / 2 - h / 2, on)
    x.circle(kx, cy, h / 2 - 6, PANEL, a, 1, fill=PANEL)


def s_memory(x):
    a0 = x.b(0)
    if a0 > 0:
        # BIOS-style panel
        x.rect([150, 150, 860, 560], WHITE, a0, 4, r=8, fill=PANEL, glow=False)
        x.d.rectangle([150, 150, 860, 205], fill=col(WHITE, a0))
        x.text((175, 178), "BIOS  ›  Memory", "monob", 28, PANEL, a0, anchor="lm")
    a1 = x.b(1)
    if a1 > 0:
        on = ease((x.since(1) - 1.2) / 0.6)
        x.text((190, 270), "Profile", "mono", 30, MUTED, a1, anchor="lm")
        x.text((420, 270), "XMP / EXPO", "monob", 30, WHITE, a1, anchor="lm")
        toggle(x, 760, 270, on, a1)
        x.text((190, 360), "Speed", "mono", 30, MUTED, a1, anchor="lm")
        x.text((420, 360), "DDR5-" + ("6000" if on > 0.5 else "4800"), "monob", 30, GREEN if on > 0.5 else AMBER, a1, anchor="lm")
        x.text((190, 450), "Default", "mono", 30, MUTED, a1, anchor="lm")
        x.text((420, 450), "slow, safe JEDEC", "mono", 30, MUTED, a1, anchor="lm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((960, 175), "PC Gamer · Ryzen 9 9900X · same kit", "semi", 28, MUTED, a2, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((960, 240), "Hogwarts Legacy, 1080p", "title", 38, WHITE, a3, anchor="lm")
        rows = [("avg  4800", 154, AMBER, 0), ("avg  6000", 183, GREEN, 0.4),
                ("1% low  4800", 65, AMBER, 1.0), ("1% low  6000", 78, GREEN, 1.4)]
        for k, (lab, v, c, d) in enumerate(rows):
            g = ease((x.since(3) - d) / 0.8)
            y = 300 + k * 78
            x.text((960, y + 24), lab, "mono", 26, MUTED, a3 * g, anchor="lm")
            x.d.rounded_rectangle([1200, y, 1200 + 2.9 * v * g, y + 48], radius=12, fill=col(c, a3 * g))
            x.text((1210 + 2.9 * v * g + 10, y + 24), f"{v}", "monob", 32, c, a3 * g, anchor="lm")
    a4 = x.b(4)
    if a4 > 0:
        x.text((960, 650), "At 4K: 131 vs 130 FPS. The GPU is the limit there.", "semi", 30, WHITE, a4, anchor="lm")
    a5 = x.b(5)
    if a5 > 0:
        x.d.rounded_rectangle([260, 620, 760, 680], radius=30, fill=col(GRID, a5 * 0.6))
        runner(x, 330 + 330 * ease(x.since(5) / 2), 650, 26, AMBER, a5, x.since(5) * 10)
        x.text((510, 710), "speeds up the CPU's lap", "semi", 28, AMBER, a5, anchor="ma")
    a6 = x.b(6)
    if a6 > 0:
        p = ease((x.since(6) - 0.3) / 1.5)
        example_tag(x, a6, (960, 760))
        counter(x, 1120, 840, lerp(78, 85, p), a6, size=90, c=GREEN)
        x.text((1260, 850), "smoother dips, a few more frames", "semi", 28, MUTED, a6, anchor="lm")


def ram_stick(x, cx, cy, w, h, c, a, label, fill_frac=0.0, fill_c=None):
    if a <= 0:
        return
    x.rect([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], c, a, 4, r=6, fill=PANEL, glow=False)
    if fill_frac > 0:
        x.d.rectangle([cx - w / 2 + 6, cy - h / 2 + 6, cx - w / 2 + 6 + (w - 12) * fill_frac, cy + h / 2 - 6], fill=col(fill_c or CYAN, a * 0.6))
    for k in range(8):
        tx = cx - w / 2 + 20 + k * (w - 40) / 7
        x.d.rectangle([tx - 12, cy - h / 4, tx + 12, cy + h / 4], fill=col(c, a * 0.35))
    for k in range(int(w / 16)):
        tx = cx - w / 2 + 10 + k * 16
        x.line([(tx, cy + h / 2), (tx, cy + h / 2 + 12)], AMBER, a, 4, glow=False)
    x.text((cx, cy - h / 2 - 20), label, "title", 34, WHITE, a, anchor="md")


def myth_card(x, n, title, a):
    if a <= 0:
        return
    x.d.rounded_rectangle([150, 130, 330, 180], radius=25, fill=col(RED, a))
    x.text((240, 155), f"MYTH {n}", "title", 28, PANEL, a, anchor="mm")
    x.text((360, 155), title, "title", 46, WHITE, a, anchor="lm")


def s_myth_ram(x):
    a0 = x.b(0)
    myth_card(x, 1, "Buy more RAM", a0)
    a1 = x.b(1)
    if a1 > 0:
        ram_stick(x, 420, 320, 460, 90, WHITE, a1, "16 GB")
        ram_stick(x, 420, 500, 460, 90, WHITE, a1, "32 GB")
        x.text((150, 620), "PC Gamer · RTX 5090 · same PC", "semi", 26, MUTED, a1, anchor="lm")
    a2 = x.b(2)
    games = [("Cyberpunk 2077", 83, 84, 2), ("Black Myth: Wukong", 76, 76, 3), ("Escape from Tarkov", 97, 109, 4)]
    for k, (g_, v16, v32, beat) in enumerate(games):
        ab = x.b(beat)
        if ab <= 0:
            continue
        y = 250 + k * 170
        g = ease(x.since(beat) / 0.9)
        x.text((900, y), g_, "semi", 30, WHITE, ab, anchor="lm")
        for j, (lab, v, c) in enumerate([("16", v16, MUTED), ("32", v32, CYAN)]):
            yy = y + 30 + j * 56
            x.text((900, yy + 22), lab, "mono", 24, MUTED, ab, anchor="lm")
            x.d.rounded_rectangle([950, yy, 950 + 6.5 * v * g, yy + 44], radius=10, fill=col(c, ab))
            x.text((960 + 6.5 * v * g + 10, yy + 22), f"{v}", "monob", 30, c, ab, anchor="lm")
    a5 = x.b(5)
    if a5 > 0:
        ram_stick(x, 420, 760, 460, 90, CYAN, a5, "Game fits in 16 GB?", fill_frac=0.7 * ease(x.since(5) / 1.2), fill_c=CYAN)
    a6 = x.b(6)
    if a6 > 0:
        verdict(x, 1350, 840, a6, "FIXES RUNNING OUT")


def s_myth_ssd(x):
    a0 = x.b(0)
    myth_card(x, 2, "A faster drive = more FPS", a0)
    a1 = x.b(1)
    if a1 > 0:
        # drive -> pipe -> RAM, separate from the frame loop
        x.rect([170, 300, 470, 460], WHITE, a1, 4, r=14, fill=PANEL, glow=False)
        x.text((320, 380), "SSD", "title", 46, WHITE, a1, anchor="mm")
        x.line([(470, 380), (760, 380)], CYAN, a1, 10, glow=False)
        t = x.since(1)
        for k in range(4):
            px = 470 + ((t * 160 + k * 72) % 290)
            x.d.rectangle([px - 14, 368, px + 14, 392], fill=col(AMBER, a1))
        x.text((615, 345), "files", "semi", 26, AMBER, a1, anchor="md")
        x.rect([760, 300, 1000, 460], WHITE, a1, 4, r=14, fill=PANEL, glow=False)
        x.text((880, 380), "RAM", "title", 46, WHITE, a1, anchor="mm")
        # frame loop on the right
        x.circle(1420, 380, 130, CYAN, a1, 6)
        ang = t * 3
        x.circle(1420 + 130 * math.cos(ang), 380 + 130 * math.sin(ang), 16, CYAN, a1, 2, fill=CYAN)
        x.text((1420, 380), "CPU + GPU", "title", 34, WHITE, a1, anchor="mm")
        x.text((1420, 545), "frames happen here", "semi", 26, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    if a2 > 0:
        x.text((170, 620), "Digital Citizen · Far Cry 5", "semi", 28, MUTED, a2, anchor="lm")
        for k, (lab, c) in enumerate([("HDD", MUTED), ("SSD", CYAN)]):
            y = 660 + k * 70
            g = ease((x.since(2) - 0.4 * k) / 0.8)
            x.text((170, y + 25), lab, "mono", 28, MUTED, a2, anchor="lm")
            x.d.rounded_rectangle([260, y, 260 + 600 * g + (8 if k else 0), y + 50], radius=12, fill=col(c, a2))
        x.text((900, 760), "+1 FPS", "monob", 44, CYAN, a2, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        panel(x, [1150, 640, 1760, 900], a3, GREEN)
        x.text((1455, 690), "What it does change", "semi", 30, GREEN, a3, anchor="mm")
        g = ease(x.since(3) / 1.5)
        x.d.rounded_rectangle([1200, 750, 1710, 800], radius=12, outline=col(MUTED, a3), width=3)
        x.d.rounded_rectangle([1200, 750, 1200 + 510 * g, 800], radius=12, fill=col(GREEN, a3))
        x.text((1455, 845), "Loading screens", "title", 34, WHITE, a3, anchor="mm")


def s_myth_fg(x):
    a0 = x.b(0)
    myth_card(x, 3, "Frame generation = real speed", a0)
    a1 = x.b(1)
    X0, Y = 170, 360
    if a1 > 0:
        x.line([(X0, Y + 120), (1750, Y + 120)], MUTED, a1, 3, glow=False)
        x.text((X0, Y + 160), "time", "mono", 24, MUTED, a1, anchor="la")
        t = x.since(1)
        for k in range(8):
            fx = X0 + 60 + k * 200
            ak = a1 * ease((t - k * 0.15) / 0.4)
            x.rect([fx - 50, Y - 40, fx + 50, Y + 80], CYAN, ak, 4, r=8, fill=CYAN + (110,), glow=False)
            x.text((fx, Y + 20), "real", "semi", 24, WHITE, ak, anchor="mm")
            gen = x.b(1) * ease((t - 1.5 - k * 0.15) / 0.4)
            if k < 7:
                gx = fx + 100
                for j in range(5):
                    yy = Y - 30 + j * 24
                    x.line([(gx - 30, yy), (gx + 30, yy)], AMBER, gen, 3, glow=False)
                x.rect([gx - 40, Y - 30, gx + 40, Y + 70], AMBER, gen, 3, r=8, glow=False)
    a2 = x.b(2)
    if a2 > 0:
        x.text((170, 230), "AMD: roughly doubles the frame rate", "semi", 32, AMBER, a2, anchor="lm")
    a3 = x.b(2)
    if a3 > 0:
        # thresholds ruler: 0..90 real FPS, 8 px per FPS
        R0 = 150
        x.line([(R0, 700), (R0 + 720, 700)], MUTED, a3, 4, glow=False)
        x.d.rectangle([R0, 694, R0 + 240, 706], fill=col(RED, a3 * 0.6))
        x.d.rectangle([R0 + 480, 694, R0 + 720, 706], fill=col(GREEN, a3 * 0.6))
        for v, c in [(30, RED), (60, GREEN)]:
            tx = R0 + v * 8
            x.line([(tx, 680), (tx, 720)], c, a3, 5, glow=False)
            x.text((tx, 650), str(v), "monob", 30, c, a3, anchor="mm")
        x.text((R0 + 120, 745), "below 30: avoid", "semi", 26, RED, a3, anchor="ma")
        x.text((R0 + 600, 745), "60+: recommended", "semi", 26, GREEN, a3, anchor="ma")
        x.text((R0, 615), "real frames per second before frame gen", "mono", 24, MUTED, a3, anchor="ld")
    a4 = x.b(3)
    if a4 > 0:
        for k in range(8):
            fx = X0 + 60 + k * 200
            x.line([(fx, Y + 95), (fx, Y + 145)], GREEN, a4, 5, glow=False)
        x.text((1750, Y + 175), "your mouse is read only on real frames", "semi", 26, GREEN, a4, anchor="ra")
    a5 = x.b(4)
    if a5 > 0:
        panel(x, [1250, 580, 1760, 730], a5, CYAN)
        x.text((1505, 620), "NVIDIA's version", "semi", 28, MUTED, a5, anchor="mm")
        x.text((1505, 680), "requires Reflex", "title", 40, CYAN, a5, anchor="mm")
    a6 = x.b(5)
    if a6 > 0:
        verdict(x, 1400, 845, a6, "SMOOTHER, NOT FASTER")


def s_myth_45(x):
    a0 = x.b(0)
    myth_card(x, 4, "Booster apps", a0)
    if a0 > 0:
        # fake app window
        x.rect([170, 230, 760, 560], WHITE, a0, 4, r=12, fill=PANEL, glow=False)
        x.d.rectangle([170, 230, 760, 275], fill=col(GRID, a0))
        for k, c in enumerate([RED, AMBER, GREEN]):
            x.circle(200 + k * 30, 252, 9, c, a0, 1, fill=c)
        x.text((465, 360), "FREE RAM!", "title", 60, AMBER, a0, anchor="mm")
        p = ease((x.since(0) - 1) / 1.5)
        x.d.rounded_rectangle([230, 440, 700, 480], radius=10, outline=col(MUTED, a0), width=2)
        x.d.rounded_rectangle([230, 440, 230 + 470 * (0.8 - 0.4 * p), 480], radius=10, fill=col(CYAN, a0))
        x.text((465, 520), f"{lerp(12.8, 6.4, p):.1f} GB in use", "mono", 26, MUTED, a0, anchor="mm")
    a1 = x.b(1)
    if a1 > 0:
        x.text((465, 620), "16 -> 32 GB barely moved FPS", "semi", 30, WHITE, a1, anchor="mm")
        verdict(x, 465, 760, a1, "NO FREE FRAMES")
    a2 = x.b(2)
    if a2 > 0:
        x.d.rounded_rectangle([900, 130, 1080, 180], radius=25, fill=col(RED, a2))
        x.text((990, 155), "MYTH 5", "title", 28, PANEL, a2, anchor="mm")
        x.text((1100, 155), "Lower res always helps", "title", 40, WHITE, a2, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((900, 260), "Only when the GPU is the slower runner", "semi", 30, MUTED, a3, anchor="lm")
    a4 = x.b(4)
    if a4 > 0:
        # CPU lap vs GPU lap shrinking with resolution
        p = (math.sin(x.since(4) * 1.4) + 1) / 2
        gpu_ms = lerp(10.5, 4.0, p)
        S = 50
        x.text((900, 360), "CPU", "title", 32, AMBER, a4, anchor="lm")
        x.d.rounded_rectangle([1000, 340, 1000 + 12 * S, 385], radius=12, fill=col(AMBER, a4))
        x.text((1000 + 12 * S + 16, 362), "12 ms", "monob", 30, AMBER, a4, anchor="lm")
        x.text((900, 450), "GPU", "title", 32, CYAN, a4, anchor="lm")
        x.d.rounded_rectangle([1000, 430, 1000 + gpu_ms * S, 475], radius=12, fill=col(CYAN, a4))
        x.text((1000 + gpu_ms * S + 16, 452), f"{gpu_ms:.1f} ms", "monob", 30, CYAN, a4, anchor="lm")
        res = ["1440p", "1080p", "720p"][min(2, int(p * 2.99))]
        x.text((900, 540), f"resolution: {res}", "mono", 28, MUTED, a4, anchor="lm")
        panel(x, [900, 600, 1760, 820], a4, RED)
        x.text((1330, 660), "1000 ÷ 12 ms", "mono", 34, MUTED, a4, anchor="mm")
        x.text((1330, 740), "capped at about 83 FPS", "title", 46, RED, a4, anchor="mm")


def s_recap(x):
    a0 = x.b(0)
    example_tag(x, a0)
    steps = [("Start", 48, MUTED, 0), ("Ultra -> High", 58, CYAN, 1), ("Upscaling", 78, CYAN, 2), ("XMP / EXPO", 85, GREEN, 3)]
    base_y, S = 820, 3.4
    for k, (lab, v, c, beat) in enumerate(steps):
        ab = x.b(beat)
        if ab <= 0:
            continue
        cx = 260 + k * 300
        h = v * S * ease(x.since(beat) / 0.8)
        x.d.rounded_rectangle([cx - 100, base_y - h, cx + 100, base_y], radius=14, fill=col(c, ab))
        x.text((cx, base_y - h - 14), f"{v}", "monob", 40, WHITE, ab, anchor="md")
        x.text((cx, base_y + 18), lab, "semi", 26, WHITE, ab, anchor="ma")
        if k:
            arrow(x, (cx - 290 + 100, base_y - steps[k - 1][1] * S - 40), (cx - 110, base_y - v * S - 40), MUTED, ab, 3, 14)
    a4 = x.b(4)
    if a4 > 0:
        x.text((260, 200), "$0 spent", "title", 52, GREEN, a4, anchor="mm")
    a5 = x.b(5)
    if a5 > 0:
        cx = 1460
        h = 160 * S * ease(x.since(5) / 0.8)
        x.d.rounded_rectangle([cx - 110, base_y - h, cx + 110, base_y], radius=14, outline=col(AMBER, a5), width=5)
        for j in range(0, int(h), 22):
            x.line([(cx - 100, base_y - j - 4), (cx + 100, base_y - j - 4)], AMBER, a5 * 0.35, 3, glow=False)
        x.text((cx, base_y - h - 14), "~160", "monob", 40, AMBER, a5, anchor="md")
        x.text((cx, base_y + 18), "+ frame generation", "semi", 26, AMBER, a5, anchor="ma")
        hh = 85 * S
        x.line([(cx - 150, base_y - hh), (cx + 150, base_y - hh)], GREEN, a5, 4, glow=False)
        x.text((cx + 160, base_y - hh), "feels like 85", "semi", 26, GREEN, a5, anchor="lm")


def s_check(x):
    a0 = x.b(0)
    if a0 > 0:
        x.rect([150, 150, 620, 520], WHITE, a0, 4, r=12, fill=PANEL, glow=False)
        x.text((180, 190), "OVERLAY", "monob", 26, MUTED, a0, anchor="lm")
        frac = 0.99 if (x.since(0) % 8) < 4 else 0.62
        gauge(x, 385, 420, 150, frac, a0, CYAN if frac > 0.9 else AMBER, "GPU usage")
    a1 = x.b(1)
    if a1 > 0:
        arrow(x, (640, 300), (800, 240), CYAN, a1, 5)
        panel(x, [820, 150, 1760, 360], a1, CYAN)
        x.text((850, 200), "≈ 99%  ·  GPU-limited", "title", 38, CYAN, a1, anchor="lm")
        x.text((850, 265), "lower settings", "semi", 32, WHITE, a1, anchor="lm")
        x.text((850, 315), "turn on upscaling", "semi", 32, WHITE, a1, anchor="lm")
    a2 = x.b(2)
    if a2 > 0:
        arrow(x, (640, 420), (800, 500), AMBER, a2, 5)
        panel(x, [820, 400, 1760, 640], a2, AMBER)
        x.text((850, 450), "well below  ·  CPU or memory", "title", 38, AMBER, a2, anchor="lm")
        x.text((850, 515), "turn on XMP / EXPO", "semi", 32, WHITE, a2, anchor="lm")
        x.text((850, 570), "lower resolution won't help", "semi", 32, RED, a2, anchor="lm")
    a3 = x.b(3)
    if a3 > 0:
        x.text((150, 600), "One change at a time.", "title", 40, WHITE, a3, anchor="lm")
        p = (x.since(3) % 6) / 6
        lap_bar(x, 150, 740, lerp(20.8, 12.0, ease(p * 1.5)), a3, scale=40)


def s_outro(x):
    a0 = x.b(0)
    if a0 > 0:
        panel(x, [360, 220, 1560, 620], a0, CYAN)
        x.text((960, 280), "NEXT VIDEO", "semi", 30, AMBER, a0, anchor="mm")
        x.text((960, 360), "Bottlenecks explained", "title", 60, WHITE, a0, anchor="mm")
        x.text((960, 430), "Is your CPU holding back your GPU?", "semi", 36, MUTED, a0, anchor="mm")
        t = x.since(0)
        x.d.rounded_rectangle([520, 480, 1400, 525], radius=22, fill=col(GRID, a0 * 0.6))
        x.d.rounded_rectangle([520, 545, 1400, 590], radius=22, fill=col(GRID, a0 * 0.6))
        runner(x, 560 + 760 * ((t * 0.25) % 1), 503, 18, AMBER, a0, t * 10)
        runner(x, 560 + 760 * ((t * 0.25 - 0.08) % 1) * 0.6, 568, 18, CYAN, a0, t * 6)
    a1 = x.b(1)
    if a1 > 0:
        x.d.rounded_rectangle([760, 690, 1160, 780], radius=45, fill=col(RED, a1))
        x.text((960, 735), "SUBSCRIBE", "title", 44, PANEL, a1, anchor="mm")
        x.text((960, 850), "What frame rate are you getting right now? Tell us below.", "semi", 30, WHITE, a1, anchor="mm")


SCENES = [("One PC, 48 FPS", s_hook),
          ("A frame is a relay race", s_relay),
          ("Fix 1: Ultra to High", s_preset),
          ("Fix 1: the result", s_preset_result),
          ("Fix 2: upscaling", s_upscale),
          ("Fix 3: the memory profile", s_memory),
          ("Myth 1: more RAM", s_myth_ram),
          ("Myth 2: a faster drive", s_myth_ssd),
          ("Myth 3: frame generation", s_myth_fg),
          ("Myths 4 and 5", s_myth_45),
          ("Back to the example PC", s_recap),
          ("The check you can run tonight", s_check),
          ("Up next", s_outro)]
