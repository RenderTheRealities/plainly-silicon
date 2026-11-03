# Plainly Silicon

Pipeline for the Plainly Silicon YouTube channel (@plainlysilicon): animated PC hardware explainers, made and scheduled automatically at no cost.

- `AGENT.md` is the step-by-step playbook each scheduled run follows.
- `calendar.json` lists upcoming videos and their status.
- `render.py` is the video engine; each `videos/<slug>/scenes.py` holds that video's visuals.
- `tts.py` is free narration with Kokoro (voice: am_michael).
- `publish.py` hosts finished files on the `media` branch so Metricool can post them to YouTube.
- `brand/` holds the logo and banner; `brand_art.py` regenerates them.
