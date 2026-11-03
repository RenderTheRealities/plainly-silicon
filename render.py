"""Plainly Silicon video renderer.

Usage:
  python3 render.py VIDEO_DIR frames  T1 T2 ...   # write preview PNGs at times (s)
  python3 render.py VIDEO_DIR render               # full render -> VIDEO_DIR/video_silent.mp4

VIDEO_DIR holds narration.txt and timing.json:
  {"paragraphs": [[start, end], ...]}   one entry per paragraph, seconds in the final audio
If timing.json is missing, durations are estimated from character counts.
"""
import json, math, os, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont

W, H, FPS = 1920, 1080, 30
NAVY = (11, 18, 32)
GRID = (20, 31, 52)
CYAN = (34, 211, 238)
AMBER = (245, 158, 11)
WHITE = (229, 231, 235)
MUTED = (120, 135, 160)
RED = (239, 68, 68)
GREEN = (52, 211, 153)
FD = "/usr/share/fonts/opentype/inter/"
_fc = {}


def font(kind, size):
    key = (kind, size)
    if key not in _fc:
        path = {"title": FD + "InterDisplay-Bold.otf", "semi": FD + "Inter-SemiBold.otf",
                "reg": FD + "Inter-Regular.otf",
                "mono": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
                "monob": "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf"}[kind]
        _fc[key] = ImageFont.truetype(path, size)
    return _fc[key]


# ---------- easing / helpers ----------
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease(x):
    x = clamp(x)
    return x * x * (3 - 2 * x)


def col(c, a):
    return (c[0], c[1], c[2], int(255 * clamp(a)))


class Ctx:
    """Per-frame drawing context with beat timing for one scene."""

    def __init__(self, img, t, dur, beats):
        self.img = img
        self.d = ImageDraw.Draw(img, "RGBA")
        self.t, self.dur, self.beats = t, dur, beats

    def b(self, i, fade=0.5):
        """0..1 appearance progress of beat i (sentence i of the paragraph)."""
        i = min(i, len(self.beats) - 1)
        return ease((self.t - self.beats[i]) / fade)

    def since(self, i):
        i = min(i, len(self.beats) - 1)
        return max(0.0, self.t - self.beats[i])

    # primitives
    def line(self, pts, c, a, w=4, glow=True):
        if a <= 0:
            return
        if glow:
            self.d.line(pts, fill=col(c, a * 0.18), width=w * 4, joint="curve")
        self.d.line(pts, fill=col(c, a), width=w, joint="curve")

    def rect(self, box, c, a, w=4, r=10, fill=None, glow=True):
        if a <= 0:
            return
        if glow:
            x0, y0, x1, y1 = box
            self.d.rounded_rectangle([x0 - 4, y0 - 4, x1 + 4, y1 + 4], radius=r + 4, outline=col(c, a * 0.18), width=w * 3)
        self.d.rounded_rectangle(box, radius=r, outline=col(c, a), width=w,
                                 fill=col(fill, a * (fill[3] / 255 if len(fill) > 3 else 1)) if fill else None)

    def text(self, xy, s, kind, size, c, a, anchor="la"):
        if a <= 0:
            return
        self.d.text(xy, s, font=font(kind, size), fill=col(c, a), anchor=anchor)

    def circle(self, cx, cy, r, c, a, w=4, fill=None):
        if a <= 0:
            return
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=col(c, a), width=w,
                       fill=col(fill, a) if fill else None)


def chip_icon(x, cx, cy, s, c, a, w=4, pins=4):
    h = s / 2
    x.rect([cx - h, cy - h, cx + h, cy + h], c, a, w, r=s * 0.08)
    pl = s * 0.16
    g = s / (pins + 1)
    for i in range(1, pins + 1):
        o = -h + g * i
        for seg in [(cx + o, cy - h, cx + o, cy - h - pl), (cx + o, cy + h, cx + o, cy + h + pl),
                    (cx - h, cy + o, cx - h - pl, cy + o), (cx + h, cy + o, cx + h + pl, cy + o)]:
            x.line([seg[:2], seg[2:]], c, a, w, glow=False)


def label_box(x, cx, cy, s, c, a, tsize=34):
    """A pill label centered at (cx, cy)."""
    if a <= 0:
        return
    f = font("semi", tsize)
    tw = x.d.textlength(s, font=f)
    x.rect([cx - tw / 2 - 22, cy - tsize * 0.85, cx + tw / 2 + 22, cy + tsize * 0.85], c, a, 3, r=tsize * 0.85,
           fill=NAVY + (230,), glow=False)
    x.text((cx, cy), s, "semi", tsize, c, a, anchor="mm")


def stamp(x, cx, cy, s, c, a, angle=-8):
    """Rotated rubber-stamp text (MYTH / WARNING)."""
    if a <= 0:
        return
    f = font("title", 64)
    tw = int(ImageDraw.Draw(Image.new("L", (1, 1))).textlength(s, font=f))
    layer = Image.new("RGBA", (tw + 80, 140), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.rounded_rectangle([6, 6, tw + 74, 134], radius=14, outline=col(c, a), width=7)
    ld.text(((tw + 80) / 2, 70), s, font=f, fill=col(c, a), anchor="mm")
    sc = 1 + 0.6 * (1 - a)
    layer = layer.rotate(angle, expand=True, resample=Image.BICUBIC)
    layer = layer.resize((int(layer.width * sc), int(layer.height * sc)), Image.BICUBIC)
    x.img.alpha_composite(layer, (int(cx - layer.width / 2), int(cy - layer.height / 2)))


def bar(x, x0, y, wmax, frac, c, a, h=34, label="", value=""):
    if a <= 0:
        return
    x.d.rounded_rectangle([x0, y, x0 + wmax, y + h], radius=h / 2, fill=col(GRID, a))
    if frac > 0.002:
        x.d.rounded_rectangle([x0, y, x0 + max(h, wmax * frac), y + h], radius=h / 2, fill=col(c, a))
    if label:
        x.text((x0, y - 14), label, "semi", 30, WHITE, a, anchor="ld")
    if value:
        x.text((x0 + wmax, y - 14), value, "mono", 30, c, a, anchor="rd")


# ---------- layout / timing ----------
def load_scenes(vdir):
    """Each video folder has scenes.py defining SCENES = [(chapter title, draw fn), ...],
    one entry per narration paragraph. Draw fns get a Ctx; x.b(i) fades in with sentence i."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("scenes", os.path.join(vdir, "scenes.py"))
    mod = importlib.util.module_from_spec(spec)
    sys.modules["scenes"] = mod
    spec.loader.exec_module(mod)
    return mod.SCENES


def sentences(p):
    return [s for s in re.split(r"(?<=[.!?])\s+", p.strip()) if s]


def load(vdir):
    SCENES = load_scenes(vdir)
    paras = [p for p in open(os.path.join(vdir, "narration.txt")).read().strip().split("\n\n") if p.strip()]
    tpath = os.path.join(vdir, "timing.json")
    exact = None
    if os.path.exists(tpath):
        tj = json.load(open(tpath))
        spans = tj["paragraphs"]
        exact = tj.get("sentences")
    else:
        cps, t, spans = 14.67, 0.4, []
        for p in paras:
            d = len(p) / cps
            spans.append([t, t + d])
            t += d + 0.6
    total = spans[-1][1] + 1.5
    scenes = []
    for i, p in enumerate(paras):
        start = spans[i][0] if i else 0.0
        end = spans[i + 1][0] if i + 1 < len(spans) else total
        sp0, sp1 = spans[i]
        beats, subs = [], []
        if exact is not None:
            for st, en, s in exact[i]:
                beats.append(st - start)
                subs.append((st, en, s))
        else:
            ss = sentences(p)
            L = sum(len(s) for s in ss)
            acc = 0
            for s in ss:
                st = sp0 + (sp1 - sp0) * acc / L
                acc += len(s)
                en = sp0 + (sp1 - sp0) * acc / L
                beats.append(st - start)
                subs.append((st, en, s))
        scenes.append(dict(start=start, end=end, beats=beats, subs=subs, title=SCENES[i][0], fn=SCENES[i][1]))
    return scenes, total


def background():
    bg = Image.new("RGBA", (W, H), NAVY + (255,))
    d = ImageDraw.Draw(bg)
    for gx in range(0, W, 60):
        d.line([(gx, 0), (gx, H)], fill=GRID + (110,), width=1)
    for gy in range(0, H, 60):
        d.line([(0, gy), (W, gy)], fill=GRID + (110,), width=1)
    return bg


BG = None
LOGO = None


def wrap(text, f, maxw, d):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        trial = (cur + " " + w_).strip()
        if d.textlength(trial, font=f) <= maxw:
            cur = trial
        else:
            lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def frame(scenes, total, T):
    global BG, LOGO
    if BG is None:
        BG = background()
        LOGO = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand/plainly-silicon-logo.png")).convert("RGBA").resize((64, 64))
    img = BG.copy()
    si = max(i for i, s in enumerate(scenes) if s["start"] <= T or i == 0)
    sc = scenes[si]
    t = T - sc["start"]
    dur = sc["end"] - sc["start"]
    x = Ctx(img, t, dur, sc["beats"])
    sc["fn"](x)
    # scene fade in/out (0.35 s)
    fade = min(ease(t / 0.35), ease((dur - t) / 0.35)) if si < len(scenes) - 1 else ease(t / 0.35)
    if fade < 1:
        veil = Image.new("RGBA", (W, H), NAVY + (int(255 * (1 - fade)),))
        img.alpha_composite(veil)
    d = ImageDraw.Draw(img, "RGBA")
    # chapter label
    d.text((60, 52), f"{si + 1:02d}", font=font("monob", 30), fill=CYAN + (255,))
    d.text((112, 52), sc["title"].upper(), font=font("semi", 30), fill=WHITE + (230,))
    # subtitle (current sentence)
    cur = [s for (a, b, s) in sc["subs"] if a - 0.05 <= T < b + 0.2]
    if cur:
        f = font("semi", 36)
        lines = wrap(cur[-1], f, 1500, d)[:3]
        lh = 48
        y = 1040 - lh * len(lines)
        tw = max(d.textlength(l, font=f) for l in lines)
        d.rounded_rectangle([960 - tw / 2 - 26, y - 14, 960 + tw / 2 + 26, y + lh * len(lines) + 6], radius=16, fill=(6, 10, 20, 205))
        for k, l in enumerate(lines):
            d.text((960, y + k * lh), l, font=f, fill=WHITE + (255,), anchor="ma")
    # progress bar + watermark
    d.rectangle([0, H - 6, W * T / total, H], fill=CYAN + (255,))
    img.alpha_composite(LOGO, (W - 96, 36))
    return img.convert("RGB")


def main():
    vdir, mode = sys.argv[1], sys.argv[2]
    scenes, total = load(vdir)
    if mode == "frames":
        for ts in sys.argv[3:]:
            T = float(ts)
            frame(scenes, total, T).save(os.path.join(vdir, f"preview_{T:07.2f}.png"))
        print("scene starts:", [round(s["start"], 1) for s in scenes], "total", round(total, 1))
        return
    if mode == "render":
        out = os.path.join(vdir, "video_silent.mp4")
        tmp = os.path.join(vdir, "video_silent.tmp.mp4")
        n = int(math.ceil(total * FPS))
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for i in range(n):
            p.stdin.write(frame(scenes, total, i / FPS).tobytes())
            if i % 900 == 0:
                print(f"{i}/{n}", flush=True)
        p.stdin.close()
        if p.wait() == 0:
            os.replace(tmp, out)
            print("done", out)
        # captions file for YouTube
        def ts_(s):
            h, r = divmod(s, 3600); m, s2 = divmod(r, 60)
            return f"{int(h):02d}:{int(m):02d}:{s2:06.3f}".replace(".", ",")
        with open(os.path.join(vdir, "captions.srt"), "w") as f:
            k = 1
            for sc in scenes:
                for a, b, s in sc["subs"]:
                    f.write(f"{k}\n{ts_(a)} --> {ts_(b)}\n{s}\n\n"); k += 1


if __name__ == "__main__":
    main()
