"""Host a finished video for free on the repo's `media` branch so Metricool can pull it.

Usage: python3 publish.py videos/NN-slug
Needs VIDEO_DIR/final.mp4 (and thumbnail.jpg for long videos).
Prints JSON with public raw URLs. The repo must be public for the URLs to work.
Files for videos whose publish date has passed are removed from the branch to keep it small.
"""
import datetime as dt, json, os, shutil, subprocess, sys

OWNER_REPO = "RenderTheRealities/plainly-silicon"
ROOT = os.path.dirname(os.path.abspath(__file__))
WT = os.path.join(ROOT, ".media-worktree")


def git(*a, cwd=ROOT, check=True):
    return subprocess.run(["git", *a], cwd=cwd, check=check, capture_output=True, text=True)


def main(vdir):
    slug = os.path.basename(vdir.rstrip("/"))
    if not os.path.isdir(WT):
        has_remote = git("ls-remote", "--heads", "origin", "media").stdout.strip()
        if has_remote:
            git("fetch", "--depth", "1", "origin", "media:media")
            git("worktree", "add", WT, "media")
        else:
            git("worktree", "add", "--orphan", "-b", "media", WT)
    # drop files for videos already published
    cal = json.load(open(os.path.join(ROOT, "calendar.json")))
    today = dt.date.today().isoformat()
    for v in cal["videos"]:
        if v["publish"][:10] < today and v.get("status") != "ready":  # keep unposted ready videos hosted
            for ext in ("mp4", "jpg"):
                f = os.path.join(WT, f"{v['slug']}.{ext}")
                if os.path.exists(f):
                    git("rm", "-q", os.path.basename(f), cwd=WT)
    shutil.copy(os.path.join(vdir, "final.mp4"), os.path.join(WT, f"{slug}.mp4"))
    files = [f"{slug}.mp4"]
    if os.path.exists(os.path.join(vdir, "thumbnail.jpg")):  # Shorts have no thumbnail
        shutil.copy(os.path.join(vdir, "thumbnail.jpg"), os.path.join(WT, f"{slug}.jpg"))
        files.append(f"{slug}.jpg")
    git("add", *files, cwd=WT)
    git("commit", "-q", "-m", f"media: {slug}", cwd=WT, check=False)
    git("push", "-q", "origin", "media", cwd=WT)
    base = f"https://raw.githubusercontent.com/{OWNER_REPO}/media"
    print(json.dumps({"video": f"{base}/{slug}.mp4", "thumbnail": f"{base}/{slug}.jpg" if len(files) > 1 else None}, indent=1))


if __name__ == "__main__":
    main(sys.argv[1])
