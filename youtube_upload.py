"""Upload a finished video straight to YouTube with the free YouTube Data API (no Metricool).

Usage:
  python3 youtube_upload.py videos/NN-slug --title "..." --publish 2026-11-08T10:00:00-07:00 [--short]

Reads the description and tags from VIDEO_DIR/package.md (sections "## Description" and "## Tags"),
uploads VIDEO_DIR/final.mp4 and sets VIDEO_DIR/thumbnail.jpg if present.
If --publish is in the future, the video is uploaded private and YouTube makes it public at that time.
Prints JSON with the video id and URL.

Secrets come ONLY from environment variables (never from the repo):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN
"""
import argparse, datetime as dt, json, os, re, sys, urllib.parse, urllib.request

API = "https://www.googleapis.com"


def token():
    try:
        body = urllib.parse.urlencode({
            "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
            "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    except KeyError as e:
        sys.exit(f"missing environment variable {e}")
    r = urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body))
    return json.load(r)["access_token"]


def package(vdir):
    s = open(os.path.join(vdir, "package.md")).read()
    desc = re.search(r"## Description\n\n(.*?)\n\n## ", s, re.S).group(1).strip()
    m = re.search(r"## Tags\n\n(.*?)(\n\n|$)", s, re.S)
    tags = [t.strip() for t in m.group(1).split(",")] if m else []
    return desc, tags


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vdir"); ap.add_argument("--title", required=True)
    ap.add_argument("--publish", help="ISO time with offset; omit to publish now")
    ap.add_argument("--short", action="store_true")
    a = ap.parse_args()
    desc, tags = package(a.vdir)
    status = {"privacyStatus": "public", "selfDeclaredMadeForKids": False, "containsSyntheticMedia": False}
    if a.publish and dt.datetime.fromisoformat(a.publish) > dt.datetime.now(dt.timezone.utc):
        status = dict(status, privacyStatus="private",
                      publishAt=dt.datetime.fromisoformat(a.publish).astimezone(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
    meta = {"snippet": {"title": a.title, "description": desc, "tags": tags[:30], "categoryId": "28"}, "status": status}
    tok = token()
    video = os.path.join(a.vdir, "final.mp4")
    size = os.path.getsize(video)
    # 1) start a resumable upload session
    req = urllib.request.Request(f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                                 data=json.dumps(meta).encode(), method="POST",
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                                          "X-Upload-Content-Type": "video/mp4", "X-Upload-Content-Length": str(size)})
    loc = urllib.request.urlopen(req).headers["Location"]
    # 2) send the file in one request
    with open(video, "rb") as f:
        req = urllib.request.Request(loc, data=f.read(), method="PUT",
                                     headers={"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"})
    vid = json.load(urllib.request.urlopen(req, timeout=1800))["id"]
    # 3) custom thumbnail (long videos only)
    thumb = os.path.join(a.vdir, "thumbnail.jpg")
    thumb_ok = None
    if os.path.exists(thumb) and not a.short:
        with open(thumb, "rb") as f:
            req = urllib.request.Request(f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}", data=f.read(),
                                         method="POST", headers={"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
        try:
            urllib.request.urlopen(req); thumb_ok = True
        except urllib.error.HTTPError as e:
            thumb_ok = f"thumbnail failed: {e.code} {e.read()[:200]!r}"
    url = f"https://www.youtube.com/{'shorts/' if a.short else 'watch?v='}{vid}"
    print(json.dumps({"id": vid, "url": url, "status": status, "thumbnail": thumb_ok}, indent=1))


if __name__ == "__main__":
    main()
