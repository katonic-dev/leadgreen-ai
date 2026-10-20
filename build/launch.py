"""One dated content release, end to end, with its proofs: the sequence rehearsed on 28 September 2026.

usage: python build/launch.py --date 2026-09-29 --summary "Launch. Three blog posts: ..." [--reason launch]
                              [--documents ...] [--no-freeze] [--skip-wheel]

In order, in the site this file lives in (so a copy's own build/launch.py rehearses on that copy):
  1. promote every build/drafts/<date>-*.html to build/posts/ (a post is published by being moved; nothing is backdated)
  2. set UPDATED = "<date>" in build/build.py and append a CHANGES entry for it (documents [] by default: no data change)
  3. python build/build.py
  4. rebuild the MCP wheel twice with SOURCE_DATE_EPOCH = <date> 00:00Z and require identical bytes
  5. python build/build.py again, so the install line on /mcp/ carries the new wheel's SHA-256
  6. add <date> to build/data/published-releases.txt: the release is then frozen and the build refuses later changes to it
  7. python build/build.py twice and require every file in the site to be unchanged between the two
  8. python build/site_checks.py
It stops at the first failure. It never commits, pushes or deploys; commit afterwards, one commit per step if wanted.
"""
import argparse
import calendar
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import date
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
BUILD = SITE / "build"
PY = sys.executable


def run(*args: str, env: dict | None = None) -> list[str]:
    r = subprocess.run([PY, *args], cwd=SITE, env=env, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        sys.exit(f"FAILED: {' '.join(args)}\n{r.stdout.strip()}\n{r.stderr.strip()}")
    return r.stdout.strip().splitlines()


def build() -> str:
    lines = run("build/build.py")
    summary = next((l for l in lines if l.startswith("wrote ")), lines[-1] if lines else "")
    print("    " + summary)
    return summary


def hashes() -> dict[str, str]:
    return {p.relative_to(SITE).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in SITE.rglob("*") if p.is_file() and "__pycache__" not in p.parts}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--date", required=True, help="the release date, YYYY-MM-DD; drafts named <date>-*.html are promoted")
    ap.add_argument("--summary", required=True, help="the CHANGES entry summary; no em or en dash")
    ap.add_argument("--reason", default="launch")
    ap.add_argument("--documents", nargs="*", default=[], help='API documents that change; default none, "*" for all')
    ap.add_argument("--no-freeze", action="store_true", help="do not add the date to build/data/published-releases.txt")
    ap.add_argument("--skip-wheel", action="store_true", help="do not rebuild the wheel (only when no API document changed)")
    a = ap.parse_args()
    d = date.fromisoformat(a.date)
    if re.search("[–—]", a.summary + a.reason):
        sys.exit("the summary or reason carries an em or en dash")

    print(f"1. drafts dated {a.date}")
    drafts = sorted((BUILD / "drafts").glob(f"{a.date}-*.html"))
    for p in drafts:
        q = BUILD / "posts" / p.name
        if q.exists():
            sys.exit(f"{q.relative_to(SITE)} exists already")
        shutil.move(str(p), str(q))
        print("    promoted", p.name)
    if not drafts:
        already = sorted(p.name for p in (BUILD / "posts").glob(f"{a.date}-*.html"))
        print(f"    no drafts to promote; posts already dated {a.date}: {len(already)}")
    left = sorted(p.name for p in (BUILD / "drafts").glob("*.html"))
    if left:
        print("    still drafts, not published:", ", ".join(left))

    print("2. UPDATED and CHANGES in build/build.py")
    bp = BUILD / "build.py"
    src = bp.read_text(encoding="utf-8")
    m = re.search(r'^UPDATED = "(\d{4}-\d{2}-\d{2})"', src, re.M)
    if not m:
        sys.exit("UPDATED line not found in build/build.py")
    if m.group(1) != a.date:
        src = src[: m.start(1)] + a.date + src[m.end(1):]
        print(f"    UPDATED {m.group(1)} -> {a.date}")
    else:
        print(f"    UPDATED is already {a.date}")
    if not a.skip_wheel:
        w = re.search(r'^WHEEL_BUILD_DATE = "(\d{4}-\d{2}-\d{2})"', src, re.M)
        if not w:
            sys.exit("WHEEL_BUILD_DATE line not found in build/build.py")
        if w.group(1) != a.date:
            src = src[: w.start(1)] + a.date + src[w.end(1):]
            print(f"    WHEEL_BUILD_DATE {w.group(1)} -> {a.date} (the wheel's SOURCE_DATE_EPOCH, printed on /mcp/)")
    if f'{{"date": "{a.date}"' in src:
        print("    a CHANGES entry for this date exists already")
    else:
        anchor = '\n]\nassert CHANGES[-1]["date"] == DATA_VERSION'
        if src.count(anchor) != 1:
            sys.exit("the end of the CHANGES list was not found in build/build.py")
        entry = (f'    {{"date": "{a.date}", "summary": {json.dumps(a.summary, ensure_ascii=False)},\n'
                 f'     "documents": {json.dumps(a.documents)}, "reason": {json.dumps(a.reason, ensure_ascii=False)}, '
                 f'"source_version": SRC_MLE["version"]}},')
        src = src.replace(anchor, "\n" + entry + anchor)
        print("    CHANGES entry appended")
    bp.write_text(src, encoding="utf-8", newline="\n")

    print("3. build")
    build()

    if a.skip_wheel:
        print("4. wheel rebuild skipped (--skip-wheel)\n5. skipped")
    else:
        mcp_version = re.search(r'^MCP_VERSION = "([^"]+)"', src, re.M).group(1)
        whl = SITE / "dist" / f"leadgreen_mcp-{mcp_version}-py3-none-any.whl"
        epoch = calendar.timegm(d.timetuple())
        print(f"4. wheel, twice, SOURCE_DATE_EPOCH={epoch}")
        env = {**os.environ, "SOURCE_DATE_EPOCH": str(epoch), "PIP_DISABLE_PIP_VERSION_CHECK": "1"}
        run("-m", "pip", "wheel", "./leadgreen-mcp", "-w", "dist", "--no-deps", env=env)
        with tempfile.TemporaryDirectory() as tmp:
            run("-m", "pip", "wheel", "./leadgreen-mcp", "-w", tmp, "--no-deps", env=env)
            second = Path(tmp) / whl.name
            if not second.exists():
                sys.exit(f"the second wheel build did not produce {whl.name}")
            h1 = hashlib.sha256(whl.read_bytes()).hexdigest()
            h2 = hashlib.sha256(second.read_bytes()).hexdigest()
        if h1 != h2:
            sys.exit(f"the wheel is not reproducible: {h1} then {h2}")
        print(f"    {whl.name} sha256 {h1}")
        print("5. build again: the install line follows the wheel")
        build()
        # with REPO_URL set the install line is the git+ form and the hash sits beside it as the wheel's SHA-256
        if h1 not in (SITE / "mcp" / "index.html").read_text(encoding="utf-8"):
            sys.exit("/mcp/ does not carry the new wheel's hash")
        print("    /mcp/ carries it")

    if a.no_freeze:
        print("6. freeze skipped (--no-freeze)")
    else:
        print("6. freeze the release")
        pr = BUILD / "data" / "published-releases.txt"
        frozen = [l.strip() for l in pr.read_text(encoding="utf-8").splitlines()] if pr.exists() else []
        if a.date in frozen:
            print(f"    {a.date} is already listed")
        else:
            with pr.open("a", encoding="utf-8", newline="\n") as f:
                f.write(a.date + "\n")
            print(f"    {a.date} added to build/data/published-releases.txt")

    print("7. build twice: every file must be unchanged")
    build()
    before = hashes()
    build()
    after = hashes()
    changed = sorted(k for k in set(before) | set(after) if before.get(k) != after.get(k))
    if changed:
        sys.exit("the build is not idempotent; changed: " + ", ".join(changed))
    print(f"    {len(after)} files, none changed")
    rel = json.loads((SITE / "api" / "v1" / "releases" / "index.json").read_text(encoding="utf-8"))
    cur = next(r for r in rel["releases"] if r["date"] == rel["current"])
    print(f"    release {rel['current']} published={cur['published']} zip sha256 {cur['sha256']}")
    if not a.no_freeze and not cur["published"]:
        sys.exit("the current release is not marked published")

    print("8. site checks")
    for line in run("build/site_checks.py"):
        print("    " + line)
    print("done: nothing committed, pushed or deployed")


if __name__ == "__main__":
    main()
