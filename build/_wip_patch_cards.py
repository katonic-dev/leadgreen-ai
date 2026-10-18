import io, ast
from pathlib import Path
REPO = Path(r"C:\Users\premk\leadgreen-ai")
SCR = Path(__file__).resolve().parent
bp = REPO / "build" / "build.py"
s = io.open(bp, encoding="utf-8").read()


def rep(old, new):
    global s
    assert s.count(old) == 1, ("missing or not unique: " + old[:100])
    s = s.replace(old, new)


# imports: io is needed by the card renderer
if "\nimport io\n" not in s:
    rep("\nimport json\n", "\nimport io\nimport json\n")

# the card module goes right before the render pipeline (after jsonld_for's helpers are defined, before render is called)
sec = io.open(SCR / "cards_section.py", encoding="utf-8").read()
rep("faq_all: list[tuple[str, str, list[tuple[str, str]]]] = []   # (page name, url, questions) for the FAQ hub\n",
    sec + "\nfaq_all: list[tuple[str, str, list[tuple[str, str]]]] = []   # (page name, url, questions) for the FAQ hub\n")

# render: a per-page og:image when the page carries a card
rep('''    content = with_cite(content, url, title)
    if post and post.get("faq"):
        faq_all.append((post.get("name") or re.sub(r"\\s*\\|\\s*Lead Green.*$", "", title), url, post["faq"]))
    page = fill(layout, {
        "TITLE": esc(title), "DESCRIPTION": esc(desc), "CANONICAL": url, "OG_TITLE": esc(title), "OG_TYPE": og_type,
        "SITE": SITE, "ROOT": root, "JSONLD": jsonld_for(kind, title, desc, url, post), "CONTENT": content,
        "UPDATED_LONG": long_date(UPDATED),
    })''',
    '''    content = with_cite(content, url, title)
    if post and post.get("faq"):
        faq_all.append((post.get("name") or re.sub(r"\\s*\\|\\s*Lead Green.*$", "", title), url, post["faq"]))
    og_image, og_alt = (card_for(path, post["card"]) if post and post.get("card") else (f"{SITE}/assets/social-card.png", "Lead Green: the energy behind the token"))
    page = fill(layout, {
        "TITLE": esc(title), "DESCRIPTION": esc(desc), "CANONICAL": url, "OG_TITLE": esc(title), "OG_TYPE": og_type,
        "SITE": SITE, "ROOT": root, "JSONLD": jsonld_for(kind, title, desc, url, post), "CONTENT": content,
        "UPDATED_LONG": long_date(UPDATED), "OG_IMAGE": og_image, "OG_IMAGE_ALT": esc(og_alt),
    })''')
# the 404 page fills the layout directly
rep('''    "OG_TYPE": "website", "SITE": SITE, "ROOT": "/", "JSONLD": "", "CONTENT": fill(fill(_b404, subs), {"ROOT": "/"}), "UPDATED_LONG": long_date(UPDATED),
})''',
    '''    "OG_TYPE": "website", "SITE": SITE, "ROOT": "/", "JSONLD": "", "CONTENT": fill(fill(_b404, subs), {"ROOT": "/"}), "UPDATED_LONG": long_date(UPDATED),
    "OG_IMAGE": f"{SITE}/assets/social-card.png", "OG_IMAGE_ALT": "Lead Green: the energy behind the token",
})''')

# model pages
rep('''    render(f"models/{s_}/index.html", "models", t_, d_, "article", "model", b_,
           {"date": UPDATED, "faq": faq_, "model": m_, "name": m_["name"]})
    lo_ = min(m_["gpus"], key=lambda g: cfg_wh(best[(m_["name"], g)]))
    lb_ = best[(m_["name"], lo_)]''',
    '''    lo_ = min(m_["gpus"], key=lambda g: cfg_wh(best[(m_["name"], g)]))
    lb_ = best[(m_["name"], lo_)]
    render(f"models/{s_}/index.html", "models", t_, d_, "article", "model", b_,
           {"date": UPDATED, "faq": faq_, "model": m_, "name": m_["name"],
            "card": {"eyebrow": "GPU energy per million output tokens", "value": fmt(cfg_wh(lb_)), "unit": "Wh/M",
                     "label": f"{m_['name']} on {lb_['num_gpus']} × {lo_}, running batch {fmt(lb_['avg_batch_size'], 0)}. GPU only, busy server, a floor."}})''')
# grid pages
rep('''    render(f"grids/{grid_slug(iso_)}/index.html", "", t_, d_, "article", "answer", b_,
           {"date": UPDATED, "faq": faq_, "name": a_["display_name"], "crumbs": [("Grids", f"{SITE}/grids/")],''',
    '''    render(f"grids/{grid_slug(iso_)}/index.html", "", t_, d_, "article", "answer", b_,
           {"date": UPDATED, "faq": faq_, "name": a_["display_name"], "crumbs": [("Grids", f"{SITE}/grids/")],
            "card": {"eyebrow": f"Grid carbon intensity · {EMBER_YEAR} · Ember", "value": fmt(intensity[iso_], 0), "unit": "gCO2e/kWh",
                     "label": f"{a_['display_name']}. {fmt(kg_per_billion(ref_wh_raw, intensity[iso_]))} kg CO2e per billion output tokens at the reference row; rank {_country_rank[iso_]} of {grid_count}."},''')
# H100 vs B200
rep('''render("h100-vs-b200/index.html", "", ct_, cd_, "article", "answer", cb_,
       {"date": UPDATED, "faq": cfaq_, "name": "H100 vs B200", "crumbs": [("The index", f"{SITE}/index/")],''',
    '''render("h100-vs-b200/index.html", "", ct_, cd_, "article", "answer", cb_,
       {"date": UPDATED, "faq": cfaq_, "name": "H100 vs B200", "crumbs": [("The index", f"{SITE}/index/")],
        "card": {"eyebrow": f"H100 against B200 · {len(pairs)} models", "value": f"{_pair_med:.2f}", "unit": "×",
                 "label": f"Median gap at the index rows: the H100 row over the B200 row, from {pairs[0][3]:.2f}× down to {pairs[-1][3]:.2f}×."},''')
# per-query
rep('''render("per-query/index.html", "index", pq_t, pq_d, "article", "answer", pq_b,
       {"date": UPDATED, "faq": pq_faq, "name": "Per query", "crumbs": [("The index", f"{SITE}/index/")],''',
    '''render("per-query/index.html", "index", pq_t, pq_d, "article", "answer", pq_b,
       {"date": UPDATED, "faq": pq_faq, "name": "Per query", "crumbs": [("The index", f"{SITE}/index/")],
        "card": {"eyebrow": "One answer, reference row", "value": f"{_ref_wh_per_answer:.3f}", "unit": "Wh",
                 "label": f"{ref['model']} on {ref['num_gpus']} × {ref['gpu']}: {fmt(raw_wh(ref))} Wh/M × {fmt(ref['_cfg']['avg_output_len'], 0)} output tokens. Google's median prompt: {GOOGLE_2025['wh']:g} Wh, whole stack."},''')
# glossary pages: the tile that names the term's headline figure
rep('''    render(f"glossary/{_t['slug']}/index.html", "", gt_, gd_, "article", "answer", gb_,
           {"date": UPDATED, "faq": gfaq_, "name": _t["name"], "crumbs": [("Glossary", f"{SITE}/glossary/")],
            "term": {"name": _t["name"], "description": _t["short"]}})''',
    '''    _ti = {"inter-token-latency-ceiling": 0, "location-based-intensity": 0, "kg-co2e-per-billion-tokens": 0, "pue": 0}.get(_t["slug"], 1)
    if _t["tiles"]:
        _tl, _tv, _tu, _ts = _t["tiles"][_ti]
        _card = {"eyebrow": f"Glossary · {_tl}", "value": _tv, "unit": _tu, "label": f"{_t['name']}. {re.sub('<[^>]+>', '', _ts)}"}
    else:
        _card = {"eyebrow": "Glossary · reference row", "value": f"{ref['_cfg']['energy_per_token_joules']:.4f}", "unit": "J per token",
                 "label": f"{_t['name']}. {ref['model']} on {ref['num_gpus']} × {ref['gpu']}: {fmt(ref['_cfg']['avg_power_watts'], 0)} W ÷ {fmt(ref['_cfg']['output_throughput_tokens_per_sec'], 0)} tokens per second."}
    render(f"glossary/{_t['slug']}/index.html", "", gt_, gd_, "article", "answer", gb_,
           {"date": UPDATED, "faq": gfaq_, "name": _t["name"], "crumbs": [("Glossary", f"{SITE}/glossary/")],
            "term": {"name": _t["name"], "description": _t["short"]}, "card": _card})''')
# compare pages
rep('''    render(f"compare/{card_['slug']}/index.html", "models", ct2, cd2, "article", "answer", cb2,
           {"date": UPDATED, "faq": cfaq2, "name": f"{_a} vs {_b}", "crumbs": [("Compare", f"{SITE}/compare/")],''',
    '''    _lg = card_["gpus"][0]
    render(f"compare/{card_['slug']}/index.html", "models", ct2, cd2, "article", "answer", cb2,
           {"date": UPDATED, "faq": cfaq2, "name": f"{_a} vs {_b}", "crumbs": [("Compare", f"{SITE}/compare/")],
            "card": {"eyebrow": f"Compare · {_lg} index rows", "value": f"{card_['ratios'][_lg]:.2f}", "unit": "×",
                     "label": f"{_b} uses {card_['ratios'][_lg]:.2f}× the GPU energy per output token of {_a} on the {_lg}, at each model's index row."},''')
# write the binary outputs with the text ones
rep('''for rel, text in outputs.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\\n")
for rel, doc in api_docs.items():''',
    '''for rel, text in outputs.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\\n")
for rel, data in outputs_bin.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_bytes() != data:
        p.write_bytes(data)
for rel, doc in api_docs.items():''')
# the closing report
rep('''print(f"wrote {len(outputs)} pages/files and {len(api_docs)} API documents; {len(index_rows)} index rows from {len(cfgs)} configurations; "''',
    '''print(f"wrote {len(outputs)} pages/files, {len(outputs_bin)} social cards and {len(api_docs)} API documents; {len(index_rows)} index rows from {len(cfgs)} configurations; "''')
rep('''if not wheel.exists():
    print(f"NOTE: {wheel.relative_to(ROOT)} is missing; the MCP page's install line points at it. "''',
    '''if not CARDS_OK:
    print("NOTE: Pillow or build/fonts is missing, so no social card was redrawn; pages keep the cards already in assets/cards (or the default card). "
          "Install Pillow (python -m pip install pillow) to regenerate them.")
if not wheel.exists():
    print(f"NOTE: {wheel.relative_to(ROOT)} is missing; the MCP page's install line points at it. "''')
ast.parse(s)
io.open(bp, "w", encoding="utf-8", newline="\n").write(s)

# layout: og:image per page
lp = REPO / "build" / "layout.html"
l = io.open(lp, encoding="utf-8").read()
old = '<meta property="og:image" content="{{SITE}}/assets/social-card.png">\n'
assert l.count(old) == 1
l = l.replace(old, '<meta property="og:image" content="{{OG_IMAGE}}">\n')
old = '<meta property="og:image:alt" content="Lead Green: the energy behind the token">\n'
assert l.count(old) == 1
l = l.replace(old, '<meta property="og:image:alt" content="{{OG_IMAGE_ALT}}">\n')
io.open(lp, "w", encoding="utf-8", newline="\n").write(l)

# site_checks: the og:image must exist
sp = REPO / "build" / "site_checks.py"
k = io.open(sp, encoding="utf-8").read()
old = '        if len(desc) > 155: failures.append(f"{url}: meta description is {len(desc)} characters")\n'
assert k.count(old) == 1
k = k.replace(old, old + '''        ogi = h.meta.get("og:image") or ""
        if not ogi.startswith(SITE + "/"): failures.append(f"{url}: og:image is {ogi!r}")
        elif not (ROOT / ogi[len(SITE) + 1:]).exists(): failures.append(f"{url}: og:image file missing {ogi}")
''')
io.open(sp, "w", encoding="utf-8", newline="\n").write(k)

# README: the build dependency and the fonts folder
rp = REPO / "README.md"
r = io.open(rp, encoding="utf-8").read()
old = "feed.xml sitemap.xml robots.txt llms.txt llms-full.txt .nojekyll   (generated)"
assert r.count(old) == 1
r = r.replace(old, old + "\nassets/cards/*.png                                   (generated social cards, one number per page; needs Pillow and build/fonts)")
io.open(rp, "w", encoding="utf-8", newline="\n").write(r)
print("patched")
