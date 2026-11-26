"""Scenes for video 31: Can Your PC Run GTA 6? What the PS5 Tells Us (crimson theme, "what happens if").

Design language: a console teardown on a dark-red bench. The recurring device is the FRAME BUDGET
BAR: a horizontal track whose length is the time one frame may take (33.3 ms at 30 fps, 16.7 ms at
60 fps), with a CPU block and a GPU block laid on it. When the CPU block doesn't fit, the frame is
late. Parts are drawn as flat outlined plates with spec text; estimates always carry an ESTIMATE tag.
"""
import math
from render import *  # noqa: F401,F403


def lerp(a, b, p):
    return a + (b - a) * clamp(p)


def plate(x, box, title, sub, c, a, tsize=44, ssize=28):
    if a <= 0:
        return
    x.rect(box, c, a, 4, r=16, fill=PANEL + (255,), glow=False)
    x0, y0, x1, y1 = box
    x.text((x0 + 26, y0 + 22), title, "title", tsize, c, a)
    if sub:
        x.text((x0 + 26, y1 - 22), sub, "semi", ssize, WHITE, a, anchor="ld")


def est_tag(x, cx, cy, a):
    label_box(x, cx, cy, "ESTIMATE", AMBER, a, 26)


def frame_bar(x, x0, y, w, budget, cpu, gpu, a, scale_ms=34.0, label=""):
    """Budget track (budget ms long) with CPU and GPU blocks (ms). Over-budget CPU shows red."""
    if a <= 0:
        return
    px = w / scale_ms
    x.d.rounded_rectangle([x0, y, x0 + budget * px, y + 56], radius=10, outline=col(WHITE, a), width=4)
    x.text((x0 + budget * px, y - 12), f"{budget:g} ms", "mono", 26, WHITE, a, anchor="rd")
    if label:
        x.text((x0, y - 12), label, "semi", 30, WHITE, a, anchor="ld")
    cc = RED if cpu > budget else CYAN
    x.d.rounded_rectangle([x0 + 6, y + 8, x0 + 6 + cpu * px, y + 26], radius=6, fill=col(cc, a))
    x.text((x0 + 14 + cpu * px, y + 17), "CPU", "monob", 22, cc, a, anchor="lm")
    x.d.rounded_rectangle([x0 + 6, y + 32, x0 + 6 + gpu * px, y + 50], radius=6, fill=col(GREEN, a))
    x.text((x0 + 14 + gpu * px, y + 41), "GPU", "monob", 22, GREEN, a, anchor="lm")


def fps_counter(x, cx, cy, val, c, a, size=220):
    if a <= 0:
        return
    x.rect([cx - 260, cy - 170, cx + 260, cy + 170], WHITE, a, 6, r=30, fill=PANEL + (255,))
    x.text((cx, cy - 120), "FPS", "semi", 36, MUTED, a, anchor="mm")
    x.text((cx, cy + 20), val, "title", size, c, a, anchor="mm")


def crowd(x, box, n, a, t, target=None):
    """Dots for pedestrians and cars; with target, they stream into it."""
    x0, y0, x1, y1 = box
    for k in range(n):
        bx = x0 + (k * 97) % (x1 - x0)
        by = y0 + (k * 53) % (y1 - y0)
        if target:
            p = (t * 0.4 + k / n) % 1
            px, py = lerp(bx, target[0], p), lerp(by, target[1], p)
            al = a * (1 - p * 0.7)
        else:
            px = bx + 12 * math.sin(t * 1.5 + k)
            py = by + 12 * math.cos(t * 1.2 + k * 0.7)
            al = a
        c = AMBER if k % 3 else CYAN
        x.circle(px, py, 8, c, al, 0, fill=c)


# ---------------- scenes ----------------
def s_hook(x):
    a0 = x.b(0)
    fps_counter(x, 600, 470, "30", AMBER, a0)
    label_box(x, 600, 700, "PS5 Pro, Nov 2026", WHITE, a0, 34)
    a1 = x.b(1)
    plate(x, [1080, 300, 1640, 520], "PC VERSION", "not announced", RED, a1)
    a2 = x.b(2)
    plate(x, [1080, 560, 1640, 780], "THE CONSOLE", "already shows what a PC needs", CYAN, a2, ssize=26)
    label_box(x, 960, 880, "which upgrade actually matters", GREEN, x.b(3), 34)


def s_facts(x):
    x.text((160, 170), "GTA 6, as of late November 2026", "title", 46, WHITE, x.b(0))
    x.rect([160, 250, 1760, 330], MUTED, x.b(1), 3, r=14, glow=False)
    x.text((200, 290), "Launched Nov 19, 2026: PS5 + Xbox Series", "semi", 34, WHITE, x.b(1), anchor="lm")
    items = [("30 FPS", "cap on both PS5s", AMBER, 2), ("~1440p", "internal resolution", CYAN, 2),
             ("~4K", "PS5 Pro upscales (PSSR)", GREEN, 3), ("< 30", "base PS5 in big fights", RED, 4),
             ("NO", "performance mode", RED, 5)]
    for i, (big, small, c, b) in enumerate(items):
        x0 = 160 + i * 322
        plate(x, [x0, 400, x0 + 296, 640], big, small, c, x.b(b), tsize=70, ssize=24)
    x.text((960, 720), "source: Digital Foundry tech review, Nov 18, 2026", "semi", 28, MUTED, x.b(2), anchor="mm")


def s_when(x):
    rows = [("GTA 5", 2013.7, 2015.3, "~1.5 years", 4), ("Red Dead 2", 2018.8, 2019.85, "~1 year", 4),
            ("GTA 6", 2026.9, 2027.15, "Q1 2027?", 2)]
    X = lambda yr: 380 + (yr - 2013) * 80
    a = x.b(0)
    for yr in range(2013, 2029):
        x.line([(X(yr), 760), (X(yr), 780)], MUTED, a, 2, glow=False)
        x.text((X(yr), 800), str(yr)[2:], "mono", 22, MUTED, a, anchor="ma")
    x.line([(X(2013), 770), (X(2028.5), 770)], MUTED, a, 2, glow=False)
    for i, (name, c0, c1, lab, b) in enumerate(rows):
        y = 260 + i * 160
        aa = x.b(b)
        x.text((140, y + 30), name, "title", 40, WHITE, aa, anchor="lm")
        x.circle(X(c0), y + 30, 16, CYAN, aa, 0, fill=CYAN)
        x.text((X(c0), y - 6), "console", "semi", 22, CYAN, aa, anchor="md")
        dashed = name == "GTA 6"
        x1 = X(c0) + (X(c1) - X(c0)) * ease(x.since(b) / 1.2)
        x.line([(X(c0), y + 30), (x1, y + 30)], AMBER, aa, 6, glow=False)
        x.circle(X(c1), y + 30, 16, AMBER if not dashed else RED, aa * ease(x.since(b) / 1.2), 4)
        x.text((X(c1) + 30, y + 30), lab, "title", 36, AMBER if not dashed else RED, aa, anchor="lm")
    label_box(x, 1500, 900 - 30, "report: GamesBeat, 4 unnamed sources; Rockstar: no comment", RED, x.b(3), 24)


def s_teardown(x):
    a = x.b(0)
    x.rect([140, 180, 1000, 860], WHITE, a, 5, r=40, fill=PANEL + (255,))
    x.text((570, 230), "PS5", "title", 50, WHITE, a, anchor="mm")
    parts = [("CPU", "8 Zen 2 cores, 3.5 GHz", CYAN, (180, 300, 960, 420)),
             ("GPU", "~10 teraflops", GREEN, (180, 440, 960, 560)),
             ("16 GB", "GDDR6, shared by game + graphics", AMBER, (180, 580, 960, 700)),
             ("SSD", "fast NVMe", WHITE, (180, 720, 960, 820))]
    for i, (t, s, c, box) in enumerate(parts):
        aa = x.b(1) * ease((x.since(1) - i * 0.6) / 0.4)
        plate(x, list(box), t, None, c, aa, tsize=40)
        x.text((box[0] + 220, (box[1] + box[3]) / 2), s, "semi", 30, WHITE, aa, anchor="lm")
    a2 = x.b(2)
    x.text((1080, 470), "->", "title", 60, MUTED, a2, anchor="mm")
    plate(x, [1150, 420, 1780, 560], "~ RTX 2070 Super", "or Radeon RX 6700 (Digital Foundry tests)", GREEN, a2, tsize=40, ssize=24)
    a3 = x.b(3)
    x.text((1080, 330), "->", "title", 60, MUTED, a3, anchor="mm")
    plate(x, [1150, 280, 1780, 400], "~ Ryzen 7 3700X", "lower clocks, less cache", CYAN, a3, tsize=40, ssize=24)


def s_ask(x):
    a = x.b(0)
    x.text((960, 430), "99%", "title", 260, AMBER, a, anchor="mm")
    x.text((960, 640), "of watch time here: viewers who aren't subscribed", "semi", 40, WHITE, a, anchor="mm")
    label_box(x, 960, 780, "subscribing is free", GREEN, x.b(1), 40)


def s_why30(x):
    a0 = x.b(0)
    x.text((140, 160), "Who works first?", "title", 46, WHITE, a0)
    a2 = x.b(2)
    crowd(x, (140, 240, 860, 520), 30, a2, x.since(2), target=(1180, 380))
    chip_icon(x, 1180, 380, 170, RED, x.b(1), 5, pins=5)
    x.text((1180, 380), "CPU", "title", 48, RED, x.b(1), anchor="mm")
    x.text((1420, 380), "->", "title", 50, MUTED, x.b(1), anchor="mm")
    chip_icon(x, 1640, 380, 150, GREEN, x.b(1), 5, pins=5)
    x.text((1640, 380), "GPU", "title", 44, GREEN, x.b(1), anchor="mm")
    frame_bar(x, 160, 660, 1500, 33.3, 30, 18, x.b(3), label="30 fps")
    frame_bar(x, 160, 800, 1500, 16.7, 30, 18, x.b(4), label="60 fps")
    label_box(x, 1350, 180, "crowds keep it at 30 (Digital Foundry)", AMBER, x.b(5), 28)


def s_pro(x):
    a0 = x.b(0)
    x.text((960, 180), "PS5  ->  PS5 Pro", "title", 56, WHITE, a0, anchor="mm")
    a1 = x.b(1)
    base = 720
    for k, (lbl, gain, c, note) in enumerate([("GPU", 1.0, GREEN, "much bigger"), ("CPU", 0.10, RED, "3.5 -> 3.85 GHz (+10%)")]):
        cx0 = 560 + k * 800
        h0 = 200
        h1 = h0 * (1 + gain * ease(x.since(1) / 1.5))
        x.d.rounded_rectangle([cx0 - 120, base - h0, cx0 - 20, base], radius=12, fill=col(MUTED, a1))
        x.d.rounded_rectangle([cx0 + 20, base - h1, cx0 + 120, base], radius=12, fill=col(c, a1))
        x.text((cx0, base + 40), lbl, "title", 48, c, a1, anchor="mm")
        x.text((cx0, base - h1 - 30), note, "semi", 30, c, a1, anchor="md")
    label_box(x, 960, 870, "sharper + steadier 30, not 60", AMBER, x.b(2), 36)


def s_check(x):
    a0 = x.b(0)
    x.rect([140, 170, 1100, 820], WHITE, a0, 3, r=12, fill=(250, 250, 250), glow=False)
    x.d.rectangle([140, 170, 1100, 220], fill=col((60, 60, 70), a0))
    x.text((160, 195), "Task Manager  >  Performance  >  CPU", "semi", 26, (255, 255, 255), a0, anchor="lm")
    a1 = x.b(1)
    x.text((1080, 260), "Your processor name", "semi", 30, (30, 30, 30), a1, anchor="ra")
    for k in range(6):
        yy = 600 - 30 * math.sin(k * 1.3 + x.t)
        x.line([(180 + k * 150, yy), (330 + k * 150, 600 - 30 * math.sin((k + 1) * 1.3 + x.t))], (37, 99, 235), a1, 4, glow=False)
    a2 = x.b(2)
    x.text((180, 700), "Cores:  8", "semi", 34, (30, 30, 30), a2)
    x.text((180, 750), "Logical processors:  16", "semi", 34, (30, 30, 30), a2)
    x.rect([740, 245, 1092, 302], RED, a2, 4, r=8, glow=False)
    x.rect([170, 690, 420, 745], RED, a2, 4, r=8, glow=False)
    a4 = x.b(4)
    plate(x, [1200, 260, 1780, 440], "2017, 4 cores", "similar GHz", MUTED, a4)
    plate(x, [1200, 520, 1780, 700], "2022+, 8 cores", "different league", GREEN, a4)


def s_cpu(x):
    a0 = x.b(0)
    x.text((140, 170), "To hold 60 fps", "title", 50, WHITE, a0)
    frame_bar(x, 160, 330, 1500, 16.7, 30 * (1 - 0.5 * ease(x.since(1) / 2)), 16, x.b(1), label="console CPU work, sped up")
    label_box(x, 1450, 300, "needs ~2x the console CPU", CYAN, x.b(1), 30)
    a2 = x.b(2)
    x.rect([160, 470, 1760, 600], AMBER, a2, 4, r=16, fill=PANEL + (255,), glow=False)
    x.text((200, 535), "\"Even 200% of console performance may not hold 60 in the most CPU-heavy scenes\"", "semi", 30, WHITE, a2, anchor="lm")
    x.text((1720, 585), "Digital Foundry, Oliver Mackenzie", "semi", 22, MUTED, a2, anchor="rd")
    a3 = x.b(3)
    plate(x, [160, 660, 900, 850], "Modern 8-core, big cache", "far ahead of Zen 2", GREEN, a3)
    plate(x, [1020, 660, 1760, 850], "4-6 cores, 2019 or older", "near console frame rates", RED, a3)


def s_gpu(x):
    a0 = x.b(0)
    x.text((140, 170), "Graphics card", "title", 50, WHITE, a0)
    a1 = x.b(1)
    bar(x, 160, 340, 1100, 0.45 * ease(x.since(1)), GREEN, a1, h=60, label="Console look: ~1440p internal, 30 fps", value="RTX 2070 Super / RX 6700 class")
    a2 = x.b(2)
    bar(x, 160, 540, 1100, 0.9 * ease(x.since(2)), CYAN, a2, h=60, label="Same settings, 60 fps", value="~2x: today's mid-range + upscaling")
    est_tag(x, 1500, 700, x.b(3))
    x.text((960, 820), "until Rockstar publishes real requirements", "semi", 32, MUTED, x.b(3), anchor="mm")


def s_upscale(x):
    a0 = x.b(0)
    x.text((140, 170), "Upscaling: half the problem", "title", 50, WHITE, a0)
    a1 = x.b(1)
    for i in range(6):
        for j in range(4):
            x.d.rectangle([160 + i * 50, 280 + j * 50, 200 + i * 50, 320 + j * 50], fill=col(CYAN, a1 * 0.7))
    x.text((310, 500), "lower res", "semi", 28, MUTED, a1, anchor="mm")
    x.text((560, 380), "->", "title", 60, MUTED, a1, anchor="mm")
    x.rect([660, 260, 1020, 480], CYAN, a1, 4, r=8, fill=PANEL + (255,), glow=False)
    x.text((840, 370), "DLSS / FSR / XeSS", "semi", 28, WHITE, a1, anchor="mm")
    x.text((840, 500), "sharp image", "semi", 28, MUTED, a1, anchor="mm")
    frame_bar(x, 1100, 340, 640, 16.7, 30, 18 * (1 - 0.45 * ease(x.since(2) / 1.5)), x.b(2), label="60 fps")
    label_box(x, 1420, 470, "CPU block unchanged", RED, x.b(3), 28)
    a4 = x.b(4)
    fps_counter(x, 560, 720, "60", GREEN, a4, size=120)
    x.text((960, 720), "but input reacts at", "semi", 34, WHITE, a4, anchor="mm")
    x.text((1300, 720), "30", "title", 110, RED, a4, anchor="mm")


def s_memory(x):
    a0 = x.b(0)
    x.text((140, 170), "Memory: one pool vs two", "title", 50, WHITE, a0)
    a1 = x.b(1)
    x.rect([160, 330, 760, 480], AMBER, a1, 4, r=14, fill=PANEL + (255,), glow=False)
    split = 160 + 600 * 0.45
    x.d.rectangle([166, 336, split, 474], fill=col(CYAN, a1 * 0.5))
    x.d.rectangle([split, 336, 754, 474], fill=col(GREEN, a1 * 0.5))
    x.text((460, 312), "Console: 16 GB shared", "semi", 30, AMBER, a1, anchor="md")
    x.text(((166 + split) / 2, 405), "game", "semi", 30, WHITE, a1, anchor="mm")
    x.text(((split + 754) / 2, 405), "graphics", "semi", 30, WHITE, a1, anchor="mm")
    a2 = x.b(2)
    plate(x, [900, 300, 1300, 480], "RAM", "for the game", CYAN, a2)
    plate(x, [1360, 300, 1760, 480], "VRAM", "on the card", GREEN, a2)
    a3 = x.b(3)
    plate(x, [160, 540, 700, 700], "8 GB card", "textures down", RED, a3)
    plate(x, [760, 540, 1300, 700], "12-16 GB card", "safer bet", GREEN, a3)
    a4 = x.b(4)
    plate(x, [1360, 540, 1760, 700], "16 / 32 GB", "floor / comfortable", CYAN, a4, ssize=24)
    a5 = x.b(5)
    label_box(x, 960, 790, "NVMe SSD with free space, not a hard drive", WHITE, a5, 32)


def s_prices(x):
    a0 = x.b(0)
    x.text((140, 170), "Memory prices, Nov 2026", "title", 50, WHITE, a0)
    a1 = x.b(1)
    for k in range(8):
        h = 60 + k * k * 9 * ease(x.since(1) / 2)
        x.d.rounded_rectangle([200 + k * 90, 720 - h, 260 + k * 90, 720], radius=8, fill=col(RED, a1))
    x.text((520, 770), "AI demand -> memory prices up", "semi", 30, MUTED, a1, anchor="mm")
    a2 = x.b(2)
    x.rect([1000, 300, 1760, 560], AMBER, a2, 5, r=24, fill=PANEL + (255,), glow=False)
    x.text((1380, 360), "32 GB DDR5 kit, US", "semi", 32, WHITE, a2, anchor="mm")
    x.text((1380, 460), "$430-600", "title", 96, AMBER, a2, anchor="mm")
    x.text((1380, 600), "mid-November 2026", "semi", 26, MUTED, a2, anchor="mm")
    label_box(x, 1380, 720, "don't rush it for a game you can't buy", GREEN, x.b(3), 30)


def s_now(x):
    a0 = x.b(0)
    x.text((960, 250), "Upgrade now?", "title", 64, WHITE, a0, anchor="mm")
    stamp(x, 960, 420, "NO", RED, x.b(1), angle=-6)
    reasons = ["no official specs", "prices are high this year", "PC version months away"]
    for i, r in enumerate(reasons):
        aa = x.b(2) * ease((x.since(2) - i * 0.8) / 0.4)
        x.text((560, 580 + i * 70), f"{i + 1}.  {r}", "semi", 40, WHITE, aa)
    label_box(x, 960, 840, "specs usually arrive close to a PC launch", CYAN, x.b(3), 30)


def s_three(x):
    a0 = x.b(0)
    x.text((140, 170), "Three example PCs", "title", 50, WHITE, a0)
    est_tag(x, 1650, 190, a0)
    pcs = [("6-core 2019 CPU", "RTX 2070 Super", "~30", "dips in crowds", AMBER, 1),
           ("recent 8-core CPU", "16 GB mid-range card", "~60", "dips in the busiest scenes", CYAN, 2),
           ("large-cache gaming CPU", "high-end card", "60", "best chance, not locked", GREEN, 3)]
    for i, (cpu, gpu, fps, note, c, b) in enumerate(pcs):
        x0 = 160 + i * 540
        aa = x.b(b)
        x.rect([x0, 280, x0 + 500, 840], c, aa, 4, r=20, fill=PANEL + (255,), glow=False)
        x.text((x0 + 30, 320), cpu, "semi", 30, WHITE, aa)
        x.text((x0 + 30, 370), gpu, "semi", 30, MUTED, aa)
        x.text((x0 + 250, 560), fps, "title", 150, c, aa, anchor="mm")
        x.text((x0 + 250, 670), "fps", "semi", 34, MUTED, aa, anchor="mm")
        x.text((x0 + 250, 780), note, "semi", 26, WHITE, aa, anchor="mm")


def s_verdict(x):
    x.text((140, 170), "The verdict", "title", 56, WHITE, x.b(0))
    steps = [("1", "Check your CPU first", WHITE, 1), ("2", "8-core from the last few years: you're fine, tune settings", GREEN, 2),
             ("3", "4-6 cores, 2019 or older: upgrade the CPU before the GPU", RED, 3),
             ("4", "8 GB graphics card: turn textures down", AMBER, 4)]
    for i, (n, t, c, b) in enumerate(steps):
        y = 280 + i * 140
        aa = x.b(b)
        x.circle(200, y + 40, 40, c, aa, 4, fill=PANEL)
        x.text((200, y + 40), n, "title", 44, c, aa, anchor="mm")
        x.text((270, y + 40), t, "semi", 40, WHITE, aa, anchor="lm")


def s_outro(x):
    a0 = x.b(0)
    x.text((160, 360), "NEXT UP: WEDNESDAY", "semi", 34, MUTED, a0)
    x.text((160, 430), "DDR4 or DDR5", "title", 84, CYAN, a0)
    x.text((160, 530), "in 2026?", "title", 84, CYAN, a0)
    x.line([(160, 640), (160 + 500 * ease(x.since(0) / 1.5), 640)], AMBER, a0, 6)


SCENES = [
    ("30 fps on a PS5 Pro", s_hook),
    ("What we know", s_facts),
    ("When will it reach PC?", s_when),
    ("Inside the PS5", s_teardown),
    ("Quick favor", s_ask),
    ("Why only 30", s_why30),
    ("The PS5 Pro proves it", s_pro),
    ("Check your CPU in 30 seconds", s_check),
    ("The CPU is the key part", s_cpu),
    ("The graphics card", s_gpu),
    ("Upscaling and frame generation", s_upscale),
    ("Memory and storage", s_memory),
    ("Memory prices right now", s_prices),
    ("Should you upgrade now?", s_now),
    ("Three example PCs", s_three),
    ("The verdict", s_verdict),
    ("Next up: Wednesday", s_outro),
]
