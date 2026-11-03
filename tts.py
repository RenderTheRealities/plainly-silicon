"""Free narration with Kokoro (voice: am_michael).

Usage: python3 tts.py VIDEO_DIR
Reads VIDEO_DIR/narration.txt, writes VIDEO_DIR/narration.m4a and VIDEO_DIR/timing.json
with exact paragraph and sentence start/end times.
Needs tts/model.onnx and tts/voices.npz (downloaded by setup.sh).
"""
import json, os, re, subprocess, sys
import numpy as np
import soundfile as sf
from kokoro_onnx import Kokoro

HERE = os.path.dirname(os.path.abspath(__file__))
VOICE, SPEED = "am_michael", 1.0
GAP_SENT, GAP_PARA, LEAD = 0.28, 0.75, 0.3


def sentences(p):
    return [s for s in re.split(r"(?<=[.!?])\s+", p.strip()) if s]


def main(vdir):
    k = Kokoro(os.path.join(HERE, "tts/model.onnx"), os.path.join(HERE, "tts/voices.npz"))
    paras = [p for p in open(os.path.join(vdir, "narration.txt")).read().strip().split("\n\n") if p.strip()]
    sr = 24000
    chunks = [np.zeros(int(sr * LEAD), np.float32)]
    t = LEAD
    out = {"paragraphs": [], "sentences": []}
    for pi, p in enumerate(paras):
        p_start, sents = t, []
        ss = sentences(p)
        for si, s in enumerate(ss):
            a, sr = k.create(s, voice=VOICE, speed=SPEED, lang="en-us")
            # trim leading/trailing near-silence so gaps stay even
            nz = np.where(np.abs(a) > 0.01)[0]
            if len(nz):
                a = a[max(0, nz[0] - int(0.03 * sr)): nz[-1] + int(0.08 * sr)]
            st = t
            t += len(a) / sr
            sents.append([round(st, 3), round(t, 3), s])
            chunks.append(a.astype(np.float32))
            gap = GAP_SENT if si < len(ss) - 1 else GAP_PARA
            chunks.append(np.zeros(int(sr * gap), np.float32))
            t += gap
        out["paragraphs"].append([round(p_start, 3), sents[-1][1]])
        out["sentences"].append(sents)
        print(f"paragraph {pi + 1}/{len(paras)} done at {t:.1f}s", flush=True)
    wav = os.path.join(vdir, "narration.wav")
    sf.write(wav, np.concatenate(chunks), sr)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", wav, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11",
                    "-ar", "48000", "-c:a", "aac", "-b:a", "192k", os.path.join(vdir, "narration.m4a")], check=True)
    os.remove(wav)
    json.dump(out, open(os.path.join(vdir, "timing.json"), "w"), indent=1)
    print("total", round(t, 1), "s")


if __name__ == "__main__":
    main(sys.argv[1])
