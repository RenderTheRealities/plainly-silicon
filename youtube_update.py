"""Edit existing uploads with the free YouTube Data API: retitles, description fixes, first comments.

Usage:
  python3 youtube_update.py scope                       # which scopes the token has; can it edit?
  python3 youtube_update.py apply  [--dry-run]          # apply every "pending" change in retitles.json
  python3 youtube_update.py revert [--dry-run]          # put the old titles/descriptions back
  python3 youtube_update.py comment VIDEO_ID "text"     # post a first comment (pinning is Studio-only)

Editing videos (videos.update) and posting comments (commentThreads.insert) need the
youtube.force-ssl scope. A token with only youtube.upload + youtube.readonly can't do either:
`scope` says so, and the other commands stop with a message instead of failing halfway.
Secrets come ONLY from YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN (never the repo).
"""
import datetime as dt, json, os, sys, urllib.error, urllib.parse, urllib.request

API = "https://www.googleapis.com/youtube/v3"
ROOT = os.path.dirname(os.path.abspath(__file__))
LOG = os.path.join(ROOT, "retitles.json")
WRITE_SCOPES = {"https://www.googleapis.com/auth/youtube.force-ssl", "https://www.googleapis.com/auth/youtube"}


def token():
    try:
        body = urllib.parse.urlencode({
            "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
            "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    except KeyError as e:
        sys.exit(f"missing environment variable {e}")
    r = json.load(urllib.request.urlopen(urllib.request.Request("https://oauth2.googleapis.com/token", data=body)))
    return r["access_token"], set(r.get("scope", "").split())


def call(tok, method, path, body=None):
    req = urllib.request.Request(f"{API}/{path}", method=method,
                                 data=json.dumps(body).encode() if body is not None else None,
                                 headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req))


def can_write(scopes):
    return bool(scopes & WRITE_SCOPES)


def need_write(scopes):
    if not can_write(scopes):
        sys.exit("The token has only: " + ", ".join(sorted(scopes)) + ".\nEditing videos and posting comments need "
                 "youtube.force-ssl. Make the change by hand (see manual-fixes.md) or re-authorize the token with that scope.")


def edit(tok, vid, title=None, desc=None, expect_title=None, expect_desc=None, dry=False):
    """Change title and/or description, keeping every other snippet field as it is."""
    items = call(tok, "GET", f"videos?part=snippet&id={vid}").get("items", [])
    if not items:
        return "video not found"
    sn = items[0]["snippet"]
    if expect_title is not None and sn["title"] != expect_title:
        return f"skipped: title is now {sn['title']!r}, not the logged one"
    if expect_desc is not None and sn["description"] != expect_desc:
        return "skipped: description changed since it was logged"
    keep = {k: sn[k] for k in ("title", "description", "categoryId", "tags", "defaultLanguage", "defaultAudioLanguage") if k in sn}
    if title is not None:
        keep["title"] = title
    if desc is not None:
        keep["description"] = desc
    if dry:
        return "dry run ok"
    call(tok, "PUT", "videos?part=snippet", {"id": vid, "snippet": keep})
    return "ok"


def run(direction, dry):
    tok, scopes = token()
    need_write(scopes)
    log = json.load(open(LOG))
    want, done = ("pending", "applied") if direction == "apply" else ("applied", "reverted")
    for e in log["long_videos"]:
        if e["status"] != want:
            continue
        a, b = (e["old_title"], e["new_title"]) if direction == "apply" else (e["new_title"], e["old_title"])
        da, db = (e["old_description"], e["new_description"]) if direction == "apply" else (e["new_description"], e["old_description"])
        r = edit(tok, e["id"], b, db, expect_title=a, dry=dry)
        print(e["slug"], "->", b, ":", r)
        if r == "ok":
            e["status"], e[done] = done, dt.date.today().isoformat()
    for e in log["shorts_descriptions"]:
        if e["status"] != want or not e.get("long_url"):
            continue
        da, db = (e["old_description"], e["new_description"]) if direction == "apply" else (e["new_description"], e["old_description"])
        r = edit(tok, e["id"], desc=db, expect_desc=da, dry=dry)
        print(e["slug"], "description:", r)
        if r == "ok":
            e["status"], e[done] = done, dt.date.today().isoformat()
    if not dry:
        json.dump(log, open(LOG, "w"), indent=1, ensure_ascii=False)


def main():
    a = sys.argv[1:]
    if not a or a[0] not in ("scope", "apply", "revert", "comment"):
        sys.exit(__doc__)
    if a[0] == "scope":
        tok, scopes = token()
        print(json.dumps({"scopes": sorted(scopes), "can_edit_videos_and_comment": can_write(scopes)}, indent=1))
    elif a[0] in ("apply", "revert"):
        run(a[0], "--dry-run" in a)
    else:
        tok, scopes = token()
        need_write(scopes)
        r = call(tok, "POST", "commentThreads?part=snippet",
                 {"snippet": {"videoId": a[1], "topLevelComment": {"snippet": {"textOriginal": a[2]}}}})
        print(json.dumps({"commentId": r["id"], "note": "Pin it in Studio: the API can't pin comments."}))


if __name__ == "__main__":
    try:
        main()
    except urllib.error.HTTPError as e:
        sys.exit(f"YouTube API error {e.code}: {e.read()[:300]!r}")
