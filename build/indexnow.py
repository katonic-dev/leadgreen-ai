"""Tell IndexNow (Bing, and the engines that share its feed) which URLs changed, after a deploy.

Run from the leadgreen-site folder once the new build is live:

    python build/indexnow.py            # pings the URLs in build/indexnow-changed.txt
    python build/indexnow.py --all      # pings every URL (first deploy, or after a key change)
    python build/indexnow.py --dry-run  # shows what would be sent

build/build.py writes indexnow-changed.txt (URLs whose content differs from the last successful ping) and
indexnow-current.json (every URL's content hash). On a successful ping this script copies current to
indexnow-state.json, so the next build only lists what changed since. The key in build/indexnow-key.txt is
served at <site>/<key>.txt, which is how IndexNow checks the site is ours; it is not a secret.
"""
from __future__ import annotations

import json
import shutil
import sys
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SITE = "https://leadgreen.ai"
ENDPOINT = "https://api.indexnow.org/indexnow"
BATCH = 10_000   # the protocol's limit per request


def main(argv: list[str]) -> int:
    dry = "--dry-run" in argv
    key = (HERE / "indexnow-key.txt").read_text(encoding="utf-8").strip()
    current = json.loads((HERE / "indexnow-current.json").read_text(encoding="utf-8"))
    if "--all" in argv:
        urls = sorted(current)
    else:
        urls = [u for u in (HERE / "indexnow-changed.txt").read_text(encoding="utf-8").splitlines() if u.strip()]
    if not urls:
        print("nothing changed since the last ping")
        return 0
    # the key file must be live before anything is sent, or every ping is rejected
    key_url = f"{SITE}/{key}.txt"
    try:
        with urllib.request.urlopen(key_url, timeout=15) as r:
            live = r.read().decode("utf-8").strip()
    except (urllib.error.URLError, OSError) as e:
        sys.exit(f"cannot read {key_url} ({e}); deploy first")
    if live != key:
        sys.exit(f"{key_url} does not hold the key in build/indexnow-key.txt; deploy the current build first")
    print(f"{len(urls)} URL{'s' if len(urls) != 1 else ''} to submit")
    for i in range(0, len(urls), BATCH):
        body = json.dumps({"host": SITE.removeprefix("https://"), "key": key, "keyLocation": key_url, "urlList": urls[i:i + BATCH]}).encode("utf-8")
        if dry:
            print(body.decode("utf-8")[:2000])
            continue
        req = urllib.request.Request(ENDPOINT, data=body, headers={"Content-Type": "application/json; charset=utf-8"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                print("IndexNow answered", r.status)
        except urllib.error.HTTPError as e:
            sys.exit(f"IndexNow refused the batch: HTTP {e.code} {e.read().decode('utf-8', 'replace')[:300]}")
    if not dry:
        shutil.copyfile(HERE / "indexnow-current.json", HERE / "indexnow-state.json")
        print("recorded; the next build lists only what changes from here")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
