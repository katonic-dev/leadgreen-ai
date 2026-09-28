"""Checks on the built site: internal links and fragments, headings, metadata, structured data, sitemap and feed
coverage, accessibility basics, the release list, and the em/en dash sweep. Exits 1 on any failure.

usage: python build/site_checks.py [--pages] [--json PATH] [--figures]
  --pages     print one line per page
  --json      write the full report to PATH
  --figures   recompute the headline figures from the snapshots in build/data and print them (informational)

Runs against the site this file lives in, so a copy's own build/site_checks.py checks that copy.
"""
import argparse
import csv
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://leadgreen.ai"
DASH = re.compile("[–—]")
GENERIC = ("here", "click here", "read more", "more", "link")


class P(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []; self.srcs = []; self.ids = set(); self.heads = []; self.meta = {}; self.title = None
        self.jsonld = []; self._in = None; self.imgs = []; self.tables = 0; self.captions = 0; self.ths = 0; self.th_scope = 0
        self.lang = None; self.canonical = None; self.buf = ""; self._h = None; self.svgs = 0; self.svg_hidden = 0
        self.a_text = []; self._a = None; self.words = 0; self._skip = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "html": self.lang = a.get("lang")
        if "id" in a: self.ids.add(a["id"])
        if tag == "a" and a.get("href"): self.links.append(a["href"]); self._a = [a["href"], ""]
        if tag in ("img", "script", "link"):
            u = a.get("src") or (a.get("href") if tag == "link" else None)
            if u: self.srcs.append((tag, u, a))
            if tag == "img": self.imgs.append(a)
            if tag == "link" and a.get("rel") == "canonical": self.canonical = a.get("href")
        if tag == "meta":
            k = a.get("name") or a.get("property")
            if k: self.meta[k] = a.get("content")
        if tag == "title": self._in = "title"; self.buf = ""
        if tag == "script" and a.get("type") == "application/ld+json": self._in = "ld"; self.buf = ""
        if tag in ("script", "style"): self._skip += 1
        if re.fullmatch(r"h[1-6]", tag): self._h = [int(tag[1]), ""]
        if tag == "table": self.tables += 1
        if tag == "caption": self.captions += 1
        if tag == "th": self.ths += 1; self.th_scope += 1 if a.get("scope") else 0
        if tag == "svg": self.svgs += 1; self.svg_hidden += 1 if a.get("aria-hidden") == "true" or a.get("role") == "img" else 0

    def handle_endtag(self, tag):
        if tag == "title" and self._in == "title": self.title = self.buf.strip(); self._in = None
        if tag == "script" and self._in == "ld": self.jsonld.append(self.buf); self._in = None
        if tag in ("script", "style"): self._skip -= 1
        if re.fullmatch(r"h[1-6]", tag) and self._h: self.heads.append((self._h[0], self._h[1].strip())); self._h = None
        if tag == "a" and self._a: self.a_text.append(tuple(self._a)); self._a = None

    def handle_data(self, d):
        if self._in: self.buf += d
        if self._h: self._h[1] += d
        if self._a: self._a[1] += d
        if not self._skip: self.words += len(d.split())


def rel_url(p: Path) -> str:
    r = p.relative_to(ROOT).as_posix()
    return "/" if r == "index.html" else "/" + r[: -len("index.html")]


def resolve(base_url: str, href: str):
    if href.startswith(("http://", "https://")): return ("ext", href, "")
    if href.startswith("mailto:"): return ("mail", href, "")
    u = urlsplit(urljoin(base_url, href))
    return ("int", unquote(u.path), u.fragment)


def check() -> tuple[dict, list[str], list[str]]:
    pages = [ROOT / "index.html"] + sorted(ROOT.glob("*/index.html")) + sorted(ROOT.glob("blog/*/index.html")) \
        + sorted(ROOT.glob("models/*/index.html")) + sorted(ROOT.glob("grids/*/index.html"))
    pages = [p for p in pages if "leadgreen-mcp" not in p.parts and "build" not in p.parts]
    report = {"pages": {}, "broken": [], "frag_broken": [], "ext": set(), "dash": []}
    failures, warnings = [], []
    parsed = {}
    for p in pages:
        txt = p.read_text(encoding="utf-8")
        h = P(); h.feed(txt); parsed[p] = h
        url = rel_url(p)
        if DASH.search(txt): report["dash"].append(url)
        h1s = [t for l, t in h.heads if l == 1]
        skips, prev = [], 0
        for l, t in h.heads:
            if prev and l > prev + 1: skips.append(f"h{prev}->h{l} '{t[:40]}'")
            prev = l
        ld_ok, ld_types = [], []
        for s in h.jsonld:
            try:
                j = json.loads(s); ld_ok.append(True)
                items = j.get("@graph", [j]) if isinstance(j, dict) else j
                ld_types += [i.get("@type") for i in items]
            except Exception as e:
                ld_ok.append(str(e))
        desc = h.meta.get("description", "")
        v = {"title": h.title, "title_len": len(h.title or ""), "desc_len": len(desc),
             "canonical": h.canonical, "canonical_ok": h.canonical == SITE + url,
             "og:title": bool(h.meta.get("og:title")), "og:image": h.meta.get("og:image"), "og:type": h.meta.get("og:type"),
             "twitter:card": h.meta.get("twitter:card"), "lang": h.lang, "h1": h1s, "heading_skips": skips,
             "headings": h.heads, "jsonld": ld_ok, "jsonld_types": ld_types,
             "tables": h.tables, "captions": h.captions, "th": h.ths, "th_scope": h.th_scope,
             "imgs_no_alt": [i.get("src") for i in h.imgs if "alt" not in i], "svgs": h.svgs, "svg_hidden": h.svg_hidden,
             "words": h.words, "links": len(h.links),
             "generic_link_text": sorted({t.strip() for _, t in h.a_text if t.strip().lower() in GENERIC})}
        report["pages"][url] = v
        if not v["canonical_ok"]: failures.append(f"{url}: canonical is {h.canonical!r}")
        if len(h1s) != 1: failures.append(f"{url}: {len(h1s)} h1 elements")
        if skips: failures.append(f"{url}: heading skips {skips}")
        if any(x is not True for x in ld_ok): failures.append(f"{url}: JSON-LD does not parse")
        if not ld_types: failures.append(f"{url}: no JSON-LD")
        if v["imgs_no_alt"]: failures.append(f"{url}: images without alt {v['imgs_no_alt']}")
        if not h.lang: failures.append(f"{url}: no lang attribute")
        if not h.title: failures.append(f"{url}: no title")
        if not desc: failures.append(f"{url}: no meta description")
        if len(desc) > 155: failures.append(f"{url}: meta description is {len(desc)} characters")
        if v["generic_link_text"]: warnings.append(f"{url}: generic link text {v['generic_link_text']}")
        for href in h.links + [u for _, u, _ in h.srcs]:
            kind, tgt, frag = resolve(url, href)
            if kind == "ext": report["ext"].add(tgt); continue
            if kind == "mail": continue
            fp = ROOT / tgt.lstrip("/")
            if tgt.endswith("/"): fp = fp / "index.html"
            if not fp.exists():
                report["broken"].append((url, href)); continue
            if frag and fp.suffix == ".html":
                tp = parsed.get(fp)
                if tp is None:
                    tp = P(); tp.feed(fp.read_text(encoding="utf-8")); parsed[fp] = tp
                if frag not in tp.ids: report["frag_broken"].append((url, href))
    if report["broken"]: failures.append(f"broken internal links: {report['broken']}")
    if report["frag_broken"]: failures.append(f"broken fragments: {report['frag_broken']}")
    if report["dash"]: failures.append(f"em or en dash on: {report['dash']}")

    sm = (ROOT / "sitemap.xml").read_text(encoding="utf-8")
    sm_urls = re.findall(r"<loc>(.*?)</loc>", sm)
    page_urls = [SITE + rel_url(p) for p in pages]
    report["sitemap"] = {"count": len(sm_urls), "missing_from_sitemap": sorted(set(page_urls) - set(sm_urls)),
                         "extra_in_sitemap": sorted(set(sm_urls) - set(page_urls))}
    if report["sitemap"]["missing_from_sitemap"]: failures.append(f"missing from sitemap: {report['sitemap']['missing_from_sitemap']}")
    if report["sitemap"]["extra_in_sitemap"]: failures.append(f"in sitemap but not built: {report['sitemap']['extra_in_sitemap']}")
    feed = (ROOT / "feed.xml").read_text(encoding="utf-8")
    report["feed"] = {"items": feed.count("<item>"), "links": re.findall(r"<link>(.*?)</link>", feed),
                      "has_atom_self": 'rel="self"' in feed, "unfilled": feed.count("{{")}
    blog_pages = [p for p in pages if p.parent.parent.name == "blog"]
    if report["feed"]["items"] != len(blog_pages): failures.append(f"feed has {report['feed']['items']} items for {len(blog_pages)} posts")
    if report["feed"]["unfilled"]: failures.append("feed carries an unfilled placeholder")
    if not report["feed"]["has_atom_self"]: failures.append("feed has no atom:link rel=self")
    report["robots"] = (ROOT / "robots.txt").read_text(encoding="utf-8").strip().splitlines()
    llms = (ROOT / "llms.txt").read_text(encoding="utf-8")
    report["llms"] = {"chars": len(llms), "links": len(set(re.findall(r"https?://\S+", llms)))}
    report["cname"] = (ROOT / "CNAME").read_text(encoding="utf-8").strip()
    report["nojekyll"] = (ROOT / ".nojekyll").exists()
    if report["cname"] != "leadgreen.ai": failures.append(f"CNAME is {report['cname']!r}")
    if not report["nojekyll"]: failures.append(".nojekyll is missing")
    rel = json.loads((ROOT / "api" / "v1" / "releases" / "index.json").read_text(encoding="utf-8"))
    chg = json.loads((ROOT / "api" / "v1" / "changes.json").read_text(encoding="utf-8"))
    cur = next((r for r in rel["releases"] if r["date"] == rel["current"]), None)
    report["release"] = {"current": rel["current"], "published": cur["published"] if cur else None,
                         "releases": [(r["date"], r["published"]) for r in rel["releases"]], "changes_last": chg["changes"][-1]["date"]}
    if cur is None: failures.append(f"release {rel['current']} is not listed in releases/index.json")
    if chg["changes"][-1]["date"] != rel["current"]: failures.append("changes.json last entry does not match the current release")
    report["ext"] = sorted(report["ext"])
    return report, failures, warnings


def figures() -> dict:
    """Recompute the headline figures from the snapshots. The 400 and 300 ms cut-offs here are the checker's own;
    for these snapshots no row moves between them and the leaderboard's 500 ms ceiling the site uses."""
    chat = json.load(open(ROOT / "build/data/mlenergy-v3-lm-arena-chat-2026-09-26.json", encoding="utf-8"))["configurations"]
    gpqa = json.load(open(ROOT / "build/data/mlenergy-v3-gpqa-2026-09-26.json", encoding="utf-8"))["configurations"]
    whm = lambda j: j * 1e6 / 3600
    best = {}
    for c in chat:
        if c["median_itl_ms"] > 400: continue
        k = (c["nickname"], c["gpu_model"])
        if k not in best or c["energy_per_token_joules"] < best[k]["energy_per_token_joules"]: best[k] = c
    rows = sorted(best.values(), key=lambda c: c["energy_per_token_joules"])
    lo, hi, ref = rows[0], rows[-1], best[("Qwen 3 32B", "H100")]
    fig = {"rows": len(rows), "models": len({c["nickname"] for c in rows}), "configs": len(chat),
           "low": (lo["nickname"], lo["gpu_model"], lo["num_gpus"], round(whm(lo["energy_per_token_joules"]), 2)),
           "high": (hi["nickname"], hi["gpu_model"], hi["num_gpus"], round(whm(hi["energy_per_token_joules"]), 2)),
           "ref": (ref["nickname"], ref["gpu_model"], ref["num_gpus"], round(whm(ref["energy_per_token_joules"]), 3),
                   round(ref["median_itl_ms"], 1), round(ref["avg_batch_size"], 1), round(ref["avg_power_watts"])),
           "span": round(whm(hi["energy_per_token_joules"]) / whm(lo["energy_per_token_joules"]), 1)}
    lad = sorted((c for c in chat if c["nickname"] == "Qwen 3 32B" and c["gpu_model"] == "H100" and c["num_gpus"] == 2),
                 key=lambda c: c["avg_batch_size"])
    fig["ladder32"] = [(round(c["avg_batch_size"], 1), round(whm(c["energy_per_token_joules"]), 1), round(c["median_itl_ms"], 1),
                        round(c["output_throughput_tokens_per_sec"]), round(c["avg_power_watts"]), c["max_num_seqs"]) for c in lad]
    fig["ladder32_ratio"] = round(whm(lad[0]["energy_per_token_joules"]) / whm(lad[-1]["energy_per_token_joules"]), 2)
    fig["ladder32_power_range"] = (round(min(c["avg_power_watts"] for c in lad)), round(max(c["avg_power_watts"] for c in lad)))
    lad8 = sorted((c for c in chat if c["nickname"].startswith("Llama 3.1 8B") and c["gpu_model"] == "H100" and c["num_gpus"] == 1),
                  key=lambda c: c["avg_batch_size"])
    fig["ladder8"] = [(round(c["avg_batch_size"], 1), round(whm(c["energy_per_token_joules"]), 1), round(c["median_itl_ms"], 1),
                       round(c["avg_power_watts"])) for c in lad8]
    bg = {}
    for c in gpqa:
        if c["median_itl_ms"] > 300: continue
        k = (c["nickname"], c["gpu_model"])
        if k not in bg or c["energy_per_token_joules"] < bg[k]["energy_per_token_joules"]: bg[k] = c
    pairs = sorted(((k, bg[k]["energy_per_request_joules"] / c["energy_per_request_joules"]) for k, c in best.items() if k in bg),
                   key=lambda p: p[1])
    fig["gpqa_pairs"] = len(pairs); fig["gpqa_ratio"] = (round(pairs[0][1], 2), round(pairs[-1][1], 2))
    grid = {}
    with open(ROOT / "build/data/ember-yearly-total-generation-extract-2026-09-26.csv", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f):
            if r["Year"] == "2024": grid[r["ISO 3 code"] or "WLD"] = float(r["Emissions intensity (gCO2e/kWh)"])
    rw = whm(ref["energy_per_token_joules"])
    fig["grid"] = {k: (grid[k], round(rw * grid[k] / 1000, 1)) for k in ("SAU", "SRB", "HKG", "NOR", "NZL", "ARE", "WLD")}
    fig["grid_countries_2024"] = len([k for k in grid if k != "WLD"])
    return fig


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pages", action="store_true")
    ap.add_argument("--json")
    ap.add_argument("--figures", action="store_true")
    a = ap.parse_args()
    report, failures, warnings = check()
    if a.pages:
        for u, v in report["pages"].items():
            print(u, "| title", v["title_len"], "| desc", v["desc_len"], "| canon", v["canonical_ok"], "| h1", len(v["h1"]),
                  "| skips", v["heading_skips"], "| ld", v["jsonld_types"], "| tables", v["tables"], "caps", v["captions"],
                  "| th", v["th"], "scope", v["th_scope"], "| img-noalt", v["imgs_no_alt"], "| words", v["words"])
    if a.figures:
        report["figures"] = figures()
        print(json.dumps(report["figures"], indent=1, default=str))
    if a.json:
        Path(a.json).write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")
    print(f"pages {len(report['pages'])} | broken {len(report['broken'])} | fragments {len(report['frag_broken'])} | dash {len(report['dash'])}"
          f" | sitemap {report['sitemap']['count']} (missing {len(report['sitemap']['missing_from_sitemap'])}, extra {len(report['sitemap']['extra_in_sitemap'])})"
          f" | feed {report['feed']['items']} items | external links {len(report['ext'])}")
    print(f"release {report['release']['current']} published={report['release']['published']} | releases {report['release']['releases']}")
    for w in warnings: print("warning:", w)
    if failures:
        print("FAILED:"); [print("  " + f) for f in failures]
        sys.exit(1)
    print("site checks passed")


if __name__ == "__main__":
    main()
