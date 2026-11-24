# Plainly Silicon

Pipeline for the Plainly Silicon YouTube channel (@plainlysilicon): animated PC hardware explainers, made and scheduled automatically at no cost. Cadence: 1 long video every Saturday, 2 Shorts a day.

- `AGENT.md` is the step-by-step playbook each scheduled run follows.
- `calendar.json` lists upcoming videos and their status.
- `render.py` is the video engine; each `videos/<slug>/scenes.py` holds that video's visuals.
- `tts.py` is free narration with Kokoro (voice: am_michael).
- `youtube_upload.py` uploads and schedules videos with the free YouTube Data API; `youtube_update.py` edits existing uploads (needs the youtube.force-ssl scope).
- `retitles.json` logs every change to an existing upload so it can be reverted; `manual-fixes.md` lists what the owner still does by hand in YouTube Studio.
- `publish.py` hosts finished files on the `media` branch so Metricool can post them to YouTube.
- `brand/` holds the logo and banner; `brand_art.py` regenerates them.
