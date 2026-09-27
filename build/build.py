"""Build leadgreen.ai from the snapshots in build/data, the page bodies in
build/pages and the posts in build/posts.

Run from the leadgreen-site folder:

    python build/build.py

Outputs, all at the site root in GitHub Pages folder style (no .html in links):

    index.html                                  home
    why/ index/ api/ mcp/ blog/ newsletter/ contribute/ about/   one index.html each
    blog/<slug>/index.html                      one per post in build/posts
    api/v1/*.json                               the read-only data API
    feed.xml  sitemap.xml  robots.txt  llms.txt  .nojekyll
    leadgreen-mcp/leadgreen_mcp/data/           a copy of api/v1 bundled with the MCP server

Every number on every page comes from a file in build/data. Page bodies and
posts carry {{PLACEHOLDERS}}; the script renders everything first and refuses
to write anything if a single placeholder is left unfilled. To update the
index: replace a snapshot with a newer retrieval (keep the date in the file
name), point the constants below at it, bump UPDATED and the source versions,
add a line to the Changes list in build/pages/index.html, and re-run. Never
type a figure into a page by hand.
"""
from __future__ import annotations

import csv
import html
import json
import re
import shutil
import sys
from datetime import date, datetime, timezone
from email.utils import format_datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATA = HERE / "data"
PAGES = HERE / "pages"
POSTS = HERE / "posts"
LAYOUT = HERE / "layout.html"
API_DIR = ROOT / "api" / "v1"
MCP_DATA = ROOT / "leadgreen-mcp" / "leadgreen_mcp" / "data"

# ----------------------------------------------------------------- settings
SITE = "https://leadgreen.ai"
UPDATED = "2026-09-26"                 # bump on every data or content change
INDEX_NAME = "Green Tokens"            # D1: "Green Tokens" or "The Green Token Index"
EDITOR = "Prem Naraindas"
LINKEDIN_URL = "https://www.linkedin.com/in/premnaraindas/"
OWN_YOUR_AI_URL = "https://www.linkedin.com/newsletters/own-your-ai-7508174547041292288/"
REPO_URL = ""                          # D6: set when the repository is public; links are omitted while empty
NEWSLETTER_SIGNUP_URL = ""             # D2: set when the email provider is chosen; never a fake form
MCP_VERSION = "0.1.0"
WHEEL_NAME = f"leadgreen_mcp-{MCP_VERSION}-py3-none-any.whl"
WHEEL_URL = f"{SITE}/dist/{WHEEL_NAME}"

MLE_CHAT = DATA / "mlenergy-v3-lm-arena-chat-2026-09-26.json"
MLE_GPQA = DATA / "mlenergy-v3-gpqa-2026-09-26.json"
EMBER = DATA / "ember-yearly-total-generation-extract-2026-09-26.csv"
AIES = DATA / "aienergyscore-text_generation-2026-09-26.csv"
HW = DATA / "nvidia-hardware-2026-09-26.json"

ITL_DEADLINE_MS = 400          # the leaderboard's Text Conversation default
GPQA_DEADLINE_MS = 300         # the leaderboard's Problem Solving default
EMBER_YEAR = "2024"            # latest year with every listed grid present
REFERENCE = ("Qwen 3 32B", "H100")   # the row the carbon table is priced on
ELECTRICITY_USD_PER_KWH = 0.10       # stated assumption in one worked example
KETTLE_KW = 2.0                      # stated assumption in one worked example

SRC_MLE = {
    "name": "ML.ENERGY Leaderboard",
    "publisher": "The ML.ENERGY Initiative, University of Michigan",
    "url": "https://ml.energy/leaderboard/",
    "data_url": "https://raw.githubusercontent.com/ml-energy/leaderboard/master/public/data/tasks/lm-arena-chat.json",
    "version": "3.0, last updated 2026-09-23",
    "retrieved": UPDATED,
    "licence": "Apache-2.0",
    "workload": "Text Conversation (lm-arena-chat)",
    "method": "vLLM serving on H100 80GB HBM3 or B200 servers; steady-state GPU energy measured with Zeus; "
              "energy per output token = GPU energy per request / output tokens, so prompt processing is included.",
    "used_for": "index, per-model configurations, concurrency curves, measured GPU power",
}
SRC_MLE_GPQA = {**SRC_MLE, "data_url": SRC_MLE["data_url"].replace("lm-arena-chat", "gpqa"),
                "workload": "Problem Solving (gpqa)", "used_for": "problem-solving versus chat comparison"}
SRC_EMBER = {
    "name": "Ember, Yearly electricity data",
    "publisher": "Ember",
    "url": "https://ember-energy.org/data/yearly-electricity-data/",
    "data_url": "https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_yearly_global.csv",
    "version": "September 2026 release (file last modified 2026-09-22)",
    "retrieved": UPDATED,
    "licence": "CC-BY-4.0",
    "used_for": f"grid emissions intensity of total generation, gCO2e per kWh, {EMBER_YEAR}",
}
SRC_AIES = {
    "name": "AI Energy Score leaderboard",
    "publisher": "Hugging Face",
    "url": "https://huggingface.co/spaces/AIEnergyScore/Leaderboard",
    "data_url": "https://huggingface.co/spaces/AIEnergyScore/Leaderboard/raw/main/data/energy/text_generation.csv",
    "version": "December 2025 round",
    "retrieved": UPDATED,
    "licence": "Apache-2.0 (the space)",
    "used_for": "GPU energy per 1,000 text-generation queries at batch size 1 on one H100",
}
SRC_OPENAI_TOKENS = {
    "name": "OpenAI, What are tokens and how to count them",
    "publisher": "OpenAI",
    "url": "https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them",
    "version": "as published on the retrieval date",
    "retrieved": UPDATED,
    "licence": "cited, not redistributed",
    "used_for": "the rough words-per-token conversion",
}
CAVEAT = ("GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration "
          "under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; "
          "a lightly used server sits well above it.")
LICENCE_TEXT = "Compilation, site text and derived figures: CC BY 4.0. Each source keeps its own licence, listed per source."


# ----------------------------------------------------------------- helpers
def wh_per_million(j_per_token: float) -> float:
    return j_per_token * 1_000_000 / 3600


def fmt(n, d=1) -> str:
    return f"{n:,.{d}f}"


def slug(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")


def precision_label(p: str) -> str:
    return {"bfloat16": "BF16", "fp8": "FP8", "mxfp4": "MXFP4", "float16": "FP16"}.get(p, p.upper())


def long_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%B %Y}"


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def jdump(obj) -> str:
    return json.dumps(obj, ensure_ascii=False, indent=2) + "\n"


# ----------------------------------------------------------------- ML.ENERGY
chat = json.loads(MLE_CHAT.read_text(encoding="utf-8"))
cfgs = chat["configurations"]
gpqa = json.loads(MLE_GPQA.read_text(encoding="utf-8"))["configurations"]


def best_by_model_gpu(configs, deadline_ms):
    best = {}
    for c in configs:
        if c["median_itl_ms"] > deadline_ms:
            continue
        k = (c["nickname"], c["gpu_model"])
        if k not in best or c["energy_per_token_joules"] < best[k]["energy_per_token_joules"]:
            best[k] = c
    return best


best = best_by_model_gpu(cfgs, ITL_DEADLINE_MS)
best_gpqa = best_by_model_gpu(gpqa, GPQA_DEADLINE_MS)


def api_row(c) -> dict:
    return {
        "model": c["nickname"],
        "slug": slug(c["nickname"]),
        "model_id": c["model_id"],
        "params_b": c["total_params_billions"],
        "active_params_b": c["activated_params_billions"],
        "precision": precision_label(c["weight_precision"]),
        "gpu": c["gpu_model"],
        "num_gpus": c["num_gpus"],
        "wh_per_million_output_tokens": round(wh_per_million(c["energy_per_token_joules"]), 2),
        "joules_per_output_token": round(c["energy_per_token_joules"], 5),
        "median_itl_ms": round(c["median_itl_ms"], 1),
        "avg_requests_in_flight": round(c["avg_batch_size"], 1),
        "gpu_power_watts_total": round(c["avg_power_watts"]),
        "avg_output_tokens": round(c["avg_output_len"]),
    }


def api_cfg(c) -> dict:
    return {
        "gpu": c["gpu_model"],
        "num_gpus": c["num_gpus"],
        "tensor_parallel": c["tensor_parallel"],
        "data_parallel": c["data_parallel"],
        "expert_parallel": c["expert_parallel"],
        "precision": precision_label(c["weight_precision"]),
        "max_num_seqs": c["max_num_seqs"],
        "avg_requests_in_flight": round(c["avg_batch_size"], 1),
        "wh_per_million_output_tokens": round(wh_per_million(c["energy_per_token_joules"]), 2),
        "joules_per_output_token": round(c["energy_per_token_joules"], 5),
        "median_itl_ms": round(c["median_itl_ms"], 1),
        "p90_itl_ms": round(c["p90_itl_ms"], 1),
        "p99_itl_ms": round(c["p99_itl_ms"], 1),
        "tokens_per_second": round(c["output_throughput_tokens_per_sec"], 1),
        "gpu_power_watts_total": round(c["avg_power_watts"]),
        "avg_output_tokens": round(c["avg_output_len"]),
        "under_itl_deadline": c["median_itl_ms"] <= ITL_DEADLINE_MS,
    }


index_rows = []
for c in best.values():
    r = api_row(c)
    r["_cfg"] = c            # raw source values for the page tables; stripped from the API documents
    index_rows.append(r)


def raw_wh(r) -> float:
    return wh_per_million(r["_cfg"]["energy_per_token_joules"])


index_rows.sort(key=raw_wh)
wh_max = max(raw_wh(r) for r in index_rows)
ref = next(r for r in index_rows if (r["model"], r["gpu"]) == REFERENCE)
ref_j = best[REFERENCE]["energy_per_token_joules"]
low = index_rows[0]
high = index_rows[-1]

# per-model documents
models: dict[str, dict] = {}
for c in cfgs:
    s = slug(c["nickname"])
    m = models.setdefault(s, {
        "slug": s, "name": c["nickname"], "model_id": c["model_id"],
        "params_b": c["total_params_billions"], "active_params_b": c["activated_params_billions"],
        "architecture": c["architecture"], "gpus": [], "configurations": [], "best": {},
    })
    m["configurations"].append(api_cfg(c))
    if c["gpu_model"] not in m["gpus"]:
        m["gpus"].append(c["gpu_model"])
for (name, gpu), c in best.items():
    models[slug(name)]["best"][gpu] = api_cfg(c)
for m in models.values():
    m["gpus"].sort()
    m["configurations"].sort(key=lambda x: (x["gpu"], x["num_gpus"], x["avg_requests_in_flight"]))


def params_cell(r) -> str:
    t, a = r["params_b"], r["active_params_b"]
    ts = f"{t:g}"
    if a and abs(a - t) > 0.01:
        return f"{ts} <span class=\"muted\">({a:g} active)</span>"
    return ts


def index_table() -> str:
    out = []
    for r in index_rows:
        c = r["_cfg"]
        wh = raw_wh(r)
        pct = wh / wh_max * 100
        out.append(
            "<tr>"
            f"<th scope=\"row\"><span class=\"model\" title=\"{esc(r['model_id'])}\">{esc(r['model'])}</span></th>"
            f"<td class=\"num soft\">{params_cell(r)} <span class=\"muted\">· {r['precision']}</span></td>"
            f"<td class=\"num\">{r['num_gpus']} × <span class=\"chip chip-{r['gpu'].lower()}\">{r['gpu']}</span></td>"
            f"<td class=\"num key\" title=\"{c['energy_per_token_joules']:.4f} J per token\"><span class=\"bar\" aria-hidden=\"true\"><i style=\"width:{pct:.1f}%\"></i></span>{fmt(wh)}</td>"
            f"<td class=\"num\">{fmt(c['median_itl_ms'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['avg_batch_size'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['avg_power_watts'], 0)}</td>"
            "</tr>"
        )
    return "\n".join(out)


def pairs_table():
    by_model: dict[str, dict] = {}
    for r in index_rows:
        by_model.setdefault(r["model"], {})[r["gpu"]] = r
    rows = []
    for m, g in by_model.items():
        if "H100" in g and "B200" in g:
            h, b = g["H100"], g["B200"]
            rows.append((m, h, b, raw_wh(h) / raw_wh(b)))
    rows.sort(key=lambda t: -t[3])
    out = []
    for m, h, b, ratio in rows:
        out.append(
            "<tr>"
            f"<th scope=\"row\"><span class=\"model\">{esc(m)}</span></th>"
            f"<td class=\"num\">{h['num_gpus']} × H100</td><td class=\"num\">{fmt(raw_wh(h))}</td>"
            f"<td class=\"num\">{b['num_gpus']} × B200</td><td class=\"num\">{fmt(raw_wh(b))}</td>"
            f"<td class=\"num key\">{ratio:.1f}×</td>"
            "</tr>"
        )
    return "\n".join(out), rows


def ladder(name, gpu, num_gpus, seqs):
    rows = {c["max_num_seqs"]: c for c in cfgs if c["nickname"] == name and c["gpu_model"] == gpu and c["num_gpus"] == num_gpus}
    out = []
    for s in seqs:
        c = rows[s]
        out.append(
            "<tr>"
            f"<th scope=\"row\" class=\"num\">{fmt(c['avg_batch_size'], 0)}</th>"
            f"<td class=\"num key\">{fmt(wh_per_million(c['energy_per_token_joules']))}</td>"
            f"<td class=\"num\">{fmt(c['median_itl_ms'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['output_throughput_tokens_per_sec'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['avg_power_watts'], 0)}</td>"
            "</tr>"
        )
    first, last = rows[seqs[0]], rows[seqs[-1]]
    return {
        "rows": "\n".join(out),
        "ratio": first["energy_per_token_joules"] / last["energy_per_token_joules"],
        "first": wh_per_million(first["energy_per_token_joules"]),
        "last": wh_per_million(last["energy_per_token_joules"]),
        "first_w": first["avg_power_watts"], "last_w": last["avg_power_watts"],
        "first_itl": first["median_itl_ms"], "last_itl": last["median_itl_ms"],
        "first_tps": first["output_throughput_tokens_per_sec"], "last_tps": last["output_throughput_tokens_per_sec"],
        "first_batch": first["avg_batch_size"], "last_batch": last["avg_batch_size"],
    }


# problem solving versus chat, energy per response, same model and GPU, best row each
gpqa_pairs = []
for k, c in best.items():
    if k in best_gpqa:
        g = best_gpqa[k]
        gpqa_pairs.append({
            "model": k[0], "gpu": k[1],
            "ratio": g["energy_per_request_joules"] / c["energy_per_request_joules"],
            "out_gpqa": g["avg_output_len"], "out_chat": c["avg_output_len"],
            "wh_chat": wh_per_million(c["energy_per_token_joules"]),
            "wh_gpqa": wh_per_million(g["energy_per_token_joules"]),
        })
gpqa_pairs.sort(key=lambda p: p["ratio"])

# ----------------------------------------------------------------- Ember
ember = list(csv.DictReader(EMBER.open(encoding="utf-8")))
COUNTRIES = [  # the grids shown on the page; the API carries every country
    ("SAU", "Saudi Arabia"), ("ARE", "United Arab Emirates"), ("QAT", "Qatar"),
    ("SRB", "Serbia"), ("HUN", "Hungary"), ("BGR", "Bulgaria"), ("SVK", "Slovakia"),
    ("HKG", "Hong Kong"), ("TWN", "Taiwan"), ("SGP", "Singapore"), ("PHL", "Philippines"),
    ("LKA", "Sri Lanka"), ("IND", "India"), ("AUS", "Australia"), ("NZL", "New Zealand"),
    ("DEU", "Germany"), ("FRA", "France"), ("GBR", "United Kingdom"), ("IRL", "Ireland"),
    ("NOR", "Norway"), ("USA", "United States"), ("JPN", "Japan"),
]
areas = []
intensity: dict[str, float] = {}
for r in ember:
    if r["Year"] != EMBER_YEAR:
        continue
    g = float(r["Emissions intensity (gCO2e/kWh)"])
    if r["Area"] == "World":
        intensity["World"] = g
        areas.append({"iso3": "WLD", "name": "World", "area_type": "world", "g_co2e_per_kwh": round(g, 1)})
        continue
    intensity[r["ISO 3 code"]] = g
    areas.append({"iso3": r["ISO 3 code"], "name": r["Area"], "area_type": "country", "continent": r["Continent"],
                  "g_co2e_per_kwh": round(g, 1)})
areas.sort(key=lambda a: (a["area_type"] != "world", a["name"]))
world = intensity["World"]
grid_count = sum(1 for a in areas if a["area_type"] == "country")


def kg_per_billion(wh_per_m: float, g_per_kwh: float) -> float:
    return wh_per_m * g_per_kwh / 1000   # Wh/M × gCO2e/kWh ÷ 1000 = g per M = kg per B


def carbon_table() -> str:
    rows = [(name, intensity[iso]) for iso, name in COUNTRIES]
    rows.sort(key=lambda t: -t[1])
    out = []
    for name, g in rows:
        out.append(
            "<tr>"
            f"<th scope=\"row\">{name}</th>"
            f"<td class=\"num\">{fmt(g, 0)}</td>"
            f"<td class=\"num key\">{fmt(kg_per_billion(ref_wh, g))}</td>"
            "</tr>"
        )
    out.append(
        "<tr class=\"total\">"
        "<th scope=\"row\">World average</th>"
        f"<td class=\"num\">{fmt(world, 0)}</td>"
        f"<td class=\"num key\">{fmt(kg_per_billion(ref_wh, world))}</td>"
        "</tr>"
    )
    return "\n".join(out)


# ----------------------------------------------------------------- AI Energy Score
aies = list(csv.DictReader(AIES.open(encoding="utf-8-sig")))
aies_dec = [r for r in aies if r["test date"].strip().startswith("Dec")]
AIES_PICK = [
    "google/gemma-3-270m", "Qwen/Qwen3-0.6B", "HuggingFaceTB/SmolLM3-3B", "google/gemma-3-4b-pt",
    "mistralai/Mistral-Nemo-Instruct-2407", "Qwen/Qwen2.5-Coder-14B", "Qwen/Qwen3-30B-A3B",
    "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B", "google/gemma-3-27b-pt",
    "deepseek-ai/DeepSeek-R1-Distill-Llama-70B", "Qwen/Qwen3-235B-A22B", "zai-org/GLM-4.6",
]
per_query_rows = sorted(
    ({"model": r["model"], "class": r["class"], "wh_per_1000_queries": round(float(r["total_gpu_energy"]) * 1000, 1),
      "score": int(r["energy_score"])} for r in aies_dec),
    key=lambda x: x["wh_per_1000_queries"],
)


def aies_table() -> str:
    out = []
    for r in per_query_rows:
        if r["model"] not in AIES_PICK:
            continue
        out.append(
            "<tr>"
            f"<th scope=\"row\"><span class=\"model\">{esc(r['model'])}</span></th>"
            f"<td>{r['class']}</td>"
            f"<td class=\"num key\">{fmt(r['wh_per_1000_queries'])}</td>"
            f"<td class=\"num\">{'★' * r['score']}{'☆' * (5 - r['score'])}</td>"
            "</tr>"
        )
    return "\n".join(out)


def aies_val(model_id: str) -> float:
    return next(r["wh_per_1000_queries"] for r in per_query_rows if r["model"] == model_id)


# ----------------------------------------------------------------- hardware
hw = json.loads(HW.read_text(encoding="utf-8"))


def tdp_table() -> str:
    return "\n".join(
        f"<tr><th scope=\"row\">{t['gpu']}</th><td>{t['form']}</td><td class=\"num\">{t['tdp_label']}</td><td class=\"num\">{t['memory']}</td></tr>"
        for t in hw["tdp"]
    )


def mig_table() -> str:
    h100 = [p for p in hw["mig_profiles"] if p["gpu"] == "H100 80GB"]
    h200 = {p["sm_fraction"] + p["memory_fraction"]: p for p in hw["mig_profiles"] if p["gpu"] == "H200 141GB"}
    out = []
    for p in h100:
        q = h200[p["sm_fraction"] + p["memory_fraction"]]
        out.append(
            f"<tr><th scope=\"row\">{p['profile']}</th><td>{q['profile']}</td><td class=\"num\">{p['memory_fraction']}</td>"
            f"<td class=\"num\">{p['sm_fraction']}</td><td class=\"num\">{p['instances']}</td></tr>"
        )
    return "\n".join(out)


# ----------------------------------------------------------------- derived figures for prose
pairs_html, pairs = pairs_table()
l32 = ladder("Qwen 3 32B", "H100", 2, [8, 16, 32, 64, 128, 256])
l8 = ladder("Llama 3.1 8B Instruct", "H100", 1, [8, 16, 32, 64, 128, 256, 512])
ref_wh = wh_per_million(ref_j)                     # raw, for the page tables and prose
ref_wh_api = ref["wh_per_million_output_tokens"]   # the two-decimal value the API and MCP server return
tokens_per_mwh_ref_b = 1_000_000 / ref_wh / 1000          # million Wh ÷ Wh per million tokens = million tokens; ÷1000 = billions
tokens_per_mwh_top_b = 1_000_000 / l32["first"] / 1000
cents_per_m_ref = ref_wh / 1000 * ELECTRICITY_USD_PER_KWH * 100
usd_per_b_ref = ref_wh / 1000 * ELECTRICITY_USD_PER_KWH * 1000
kettle_minutes_ref = ref_wh / (KETTLE_KW * 1000) * 60
sau_nor_ratio = intensity["SAU"] / intensity["NOR"]
gp_min, gp_max = gpqa_pairs[0], gpqa_pairs[-1]
aies_70b = aies_val("deepseek-ai/DeepSeek-R1-Distill-Llama-70B")
aies_small = per_query_rows[0]
aies_large = per_query_rows[-1]

subs = {
    # site-wide
    "SITE": SITE, "INDEX_NAME": INDEX_NAME, "UPDATED": UPDATED, "UPDATED_LONG": long_date(UPDATED),
    "EDITOR": EDITOR, "LINKEDIN_URL": LINKEDIN_URL, "OWN_YOUR_AI_URL": OWN_YOUR_AI_URL,
    "WHEEL_URL": WHEEL_URL, "WHEEL_NAME": WHEEL_NAME, "MCP_VERSION": MCP_VERSION,
    "REPO_LINK": (f"<a href=\"{REPO_URL}\">the repository</a>" if REPO_URL else "the repository (link to follow once it is public)"),
    "REPO_LINK_CAP": (f"<a href=\"{REPO_URL}\">The repository</a>" if REPO_URL else "The repository (link to follow once it is public)"),
    # the MCP worked example reproduces what the tool returns, so it uses the API's two-decimal values
    "EST_50M_WH": fmt(ref_wh_api * 50, 1), "EST_50M_KWH": fmt(ref_wh_api * 50 / 1000, 4),
    "EST_50M_KG_SRB": fmt(ref_wh_api * 50 / 1000 * round(intensity["SRB"], 1) / 1000, 2),
    "REPO_INSTALL": (f"pip install \"git+{REPO_URL}#subdirectory=leadgreen-mcp\"" if REPO_URL else f"pip install {WHEEL_URL}"),
    "REPO_UVX": (f"uvx --from \"git+{REPO_URL}#subdirectory=leadgreen-mcp\" leadgreen-mcp" if REPO_URL else f"uvx --from {WHEEL_URL} leadgreen-mcp"),
    "NEWSLETTER_CTA": (
        f"<div class=\"actions\"><a class=\"cta solid\" href=\"{NEWSLETTER_SIGNUP_URL}\">Subscribe by email</a>"
        f"<a class=\"cta\" href=\"{OWN_YOUR_AI_URL}\">Own Your AI on LinkedIn</a></div>"
        if NEWSLETTER_SIGNUP_URL else
        f"<p class=\"lead\">The email edition is being set up. Until it opens, the meter runs inside <a href=\"{OWN_YOUR_AI_URL}\">Own Your AI</a>, "
        "the fortnightly LinkedIn newsletter, which carries one number from this index in every issue.</p>"
        f"<div class=\"actions\"><a class=\"cta solid\" href=\"{OWN_YOUR_AI_URL}\">Read Own Your AI on LinkedIn</a>"
        "<a class=\"cta\" href=\"{{ROOT}}feed.xml\">Blog RSS feed</a></div>"
    ),
    # tables
    "INDEX_ROWS": index_table(), "PAIR_ROWS": pairs_html,
    "LADDER_32_ROWS": l32["rows"], "LADDER_8_ROWS": l8["rows"],
    "CARBON_ROWS": carbon_table(), "AIES_ROWS": aies_table(),
    "TDP_ROWS": tdp_table(), "MIG_ROWS": mig_table(),
    # tiles and counts
    "TILE_LOW_WH": fmt(raw_wh(low), 0),
    "TILE_LOW_LABEL": f"{low['model']}, {low['num_gpus']} × {low['gpu']}",
    "TILE_REF_WH": fmt(ref_wh, 0),
    "TILE_REF_LABEL": f"{ref['model']}, {ref['num_gpus']} × {ref['gpu']}",
    "TILE_HIGH_WH": fmt(raw_wh(high), 0),
    "TILE_HIGH_LABEL": f"{high['model']}, {high['num_gpus']} × {high['gpu']}",
    "LOW_MODEL": low["model"], "LOW_GPUS": f"{low['num_gpus']} × {low['gpu']}", "LOW_WH_1": fmt(raw_wh(low)),
    "HIGH_MODEL": high["model"], "HIGH_GPUS": f"{high['num_gpus']} × {high['gpu']}", "HIGH_WH_1": fmt(raw_wh(high)),
    "SPAN": f"{raw_wh(high) / raw_wh(low):.0f}",
    "ROW_COUNT": str(len(index_rows)),
    "MODEL_COUNT": str(len({r['model'] for r in index_rows})),
    "CONFIG_COUNT": str(len(cfgs)),
    "GPQA_CONFIG_COUNT": str(len(gpqa)),
    "GRID_COUNT": str(grid_count),
    "PER_QUERY_COUNT": str(len(per_query_rows)),
    # pairs
    "PAIR_COUNT": str(len(pairs)),
    "PAIR_MAX_MODEL": pairs[0][0], "PAIR_MAX_RATIO": f"{pairs[0][3]:.1f}",
    "PAIR_MIN_MODEL": pairs[-1][0], "PAIR_MIN_RATIO": f"{pairs[-1][3]:.2f}",
    # ladders
    "LADDER_32_RATIO": f"{l32['ratio']:.1f}", "LADDER_32_FIRST": fmt(l32["first"], 0), "LADDER_32_LAST": fmt(l32["last"], 0),
    "LADDER_32_FIRST_W": fmt(l32["first_w"], 0), "LADDER_32_LAST_W": fmt(l32["last_w"], 0),
    "LADDER_32_FIRST_ITL": fmt(l32["first_itl"], 0), "LADDER_32_LAST_ITL": fmt(l32["last_itl"], 0),
    "LADDER_32_FIRST_TPS": fmt(l32["first_tps"], 0), "LADDER_32_LAST_TPS": fmt(l32["last_tps"], 0),
    "LADDER_32_FIRST_BATCH": fmt(l32["first_batch"], 0), "LADDER_32_LAST_BATCH": fmt(l32["last_batch"], 0),
    "LADDER_8_RATIO": f"{l8['ratio']:.1f}", "LADDER_8_FIRST": fmt(l8["first"], 0), "LADDER_8_LAST": fmt(l8["last"]),
    "LADDER_8_FIRST_BATCH": fmt(l8["first_batch"], 0), "LADDER_8_LAST_BATCH": fmt(l8["last_batch"], 0),
    "LADDER_8_FIRST_W": fmt(l8["first_w"], 0), "LADDER_8_LAST_W": fmt(l8["last_w"], 0),
    # reference row and worked figures
    "REF_WH": fmt(ref_wh, 0), "REF_WH_1": fmt(ref_wh, 1), "REF_J": f"{ref_j:.4f}",
    "REF_MODEL": ref["model"], "REF_GPUS": f"{ref['num_gpus']} × {ref['gpu']}", "REF_SLUG": ref["slug"],
    "REF_MODEL_ID": ref["model_id"], "REF_ITL": fmt(ref["_cfg"]["median_itl_ms"], 0), "REF_BATCH": fmt(ref["_cfg"]["avg_batch_size"], 0),
    "REF_W": fmt(ref["_cfg"]["avg_power_watts"], 0), "REF_WH_2": fmt(ref_wh_api, 2),
    "REF_KG_SAU": fmt(kg_per_billion(ref_wh, intensity["SAU"])), "REF_KG_NOR": fmt(kg_per_billion(ref_wh, intensity["NOR"])),
    "REF_KG_SRB": fmt(kg_per_billion(ref_wh, intensity["SRB"])), "REF_KG_WORLD": fmt(kg_per_billion(ref_wh, world)),
    "REF_KWH_PER_B": fmt(ref_wh, 1),           # Wh per million = kWh per billion
    "REF_MWH_PER_T": fmt(ref_wh, 1),           # Wh per million = MWh per trillion
    "TOKENS_PER_MWH_REF_B": fmt(tokens_per_mwh_ref_b, 1),
    "TOKENS_PER_MWH_TOP_B": fmt(tokens_per_mwh_top_b, 1),
    "CENTS_PER_M_REF": fmt(cents_per_m_ref, 1), "USD_PER_B_REF": fmt(usd_per_b_ref, 2),
    "ELECTRICITY_PRICE": f"{ELECTRICITY_USD_PER_KWH:.2f}",
    "KETTLE_KW": f"{KETTLE_KW:g}", "KETTLE_MINUTES_REF": fmt(kettle_minutes_ref, 1),
    "SAU_G": fmt(intensity["SAU"], 0), "NOR_G": fmt(intensity["NOR"], 0), "SRB_G": fmt(intensity["SRB"], 0),
    "HKG_G": fmt(intensity["HKG"], 0), "NZL_G": fmt(intensity["NZL"], 0), "IND_G": fmt(intensity["IND"], 0),
    "FRA_G": fmt(intensity["FRA"], 0), "WORLD_G": fmt(world, 0), "SAU_NOR_RATIO": f"{sau_nor_ratio:.0f}",
    "EMBER_YEAR": EMBER_YEAR, "ITL": str(ITL_DEADLINE_MS), "GPQA_ITL": str(GPQA_DEADLINE_MS),
    # problem solving versus chat
    "GPQA_PAIRS": str(len(gpqa_pairs)),
    "GPQA_RATIO_MIN": f"{gp_min['ratio']:.0f}", "GPQA_RATIO_MAX": f"{gp_max['ratio']:.0f}",
    "GPQA_MIN_MODEL": gp_min["model"], "GPQA_MAX_MODEL": gp_max["model"],
    "GPQA_OUT_MIN": fmt(min(p["out_gpqa"] for p in gpqa_pairs), 0), "GPQA_OUT_MAX": fmt(max(p["out_gpqa"] for p in gpqa_pairs), 0),
    "CHAT_OUT_MIN": fmt(min(p["out_chat"] for p in gpqa_pairs), 0), "CHAT_OUT_MAX": fmt(max(p["out_chat"] for p in gpqa_pairs), 0),
    # per query
    "AIES_70B_WH": fmt(aies_70b), "AIES_70B_WH_EACH": fmt(aies_70b / 1000, 3),
    "AIES_SMALL_MODEL": aies_small["model"], "AIES_SMALL_WH": fmt(aies_small["wh_per_1000_queries"]),
    "AIES_LARGE_MODEL": aies_large["model"], "AIES_LARGE_WH": fmt(aies_large["wh_per_1000_queries"]),
    # hardware
    "B200_TDP": "1,000", "H100_TDP": "700", "DGX_B200_KW": fmt(hw["systems"][0]["max_power_kw"], 1),
    "B200_EMBODIED_KG": fmt(hw["embodied"]["kg_co2e_cradle_to_gate"], 0),
}

# ----------------------------------------------------------------- API documents
ENDPOINTS = [
    ("manifest.json", "Sources, versions, retrieval dates, licences and this endpoint list."),
    ("index.json", f"The index: {len(index_rows)} rows, one per model and GPU, energy-optimal under the latency limit, sorted ascending."),
    ("models.json", "Every model on the index with its slug, Hugging Face id, parameter counts and measured GPUs."),
    ("models/{slug}.json", "One model: every measured configuration (concurrency, parallelism, latency, power) and the best row per GPU."),
    ("grid.json", f"Grid emissions intensity, gCO2e per kWh, {EMBER_YEAR} annual average, {grid_count} countries plus World."),
    ("hardware.json", "Manufacturer power ceilings, memory, MIG slice profiles and one embodied-carbon figure."),
    ("per-query.json", "AI Energy Score text-generation rows: Wh per 1,000 queries at batch size 1 on one H100."),
    ("openapi.json", "OpenAPI 3.1 description of these endpoints."),
]
api_docs: dict[str, dict] = {}
api_docs["manifest.json"] = {
    "version": "1", "updated": UPDATED, "site": SITE, "name": f"Lead Green {INDEX_NAME} API",
    "description": "GPU watt-hours per million output tokens by model, GPU and configuration, with grid carbon intensity and GPU hardware reference data. Static JSON, GET only, CORS open.",
    "endpoints": [{"path": p, "url": f"{SITE}/api/v1/{p}", "description": d} for p, d in ENDPOINTS],
    "sources": [SRC_MLE, SRC_MLE_GPQA, SRC_EMBER, {**hw["sources"][0], "licence": "cited, not redistributed"},
                {**hw["sources"][1], "licence": "cited, not redistributed"}, {**hw["sources"][2], "licence": "cited, not redistributed"},
                SRC_AIES, SRC_OPENAI_TOKENS],
    "licence": LICENCE_TEXT, "caveat": CAVEAT,
    "publisher": {"name": "Lead Green", "parent": "Katonic", "url": SITE},
}
api_docs["index.json"] = {
    "version": "1", "updated": UPDATED, "unit": "Wh per million output tokens", "workload": "text-conversation",
    "itl_deadline_ms": ITL_DEADLINE_MS, "selection": "per model and GPU, the configuration with the lowest energy per token whose median inter-token latency is under itl_deadline_ms",
    "reference_row": {"model": ref["model"], "gpu": ref["gpu"], "num_gpus": ref["num_gpus"]},
    "source": SRC_MLE, "caveat": CAVEAT, "rows": [{k: v for k, v in r.items() if not k.startswith("_")} for r in index_rows],
}
api_docs["models.json"] = {
    "version": "1", "updated": UPDATED, "source": SRC_MLE,
    "models": [{"slug": m["slug"], "name": m["name"], "model_id": m["model_id"], "params_b": m["params_b"],
                "active_params_b": m["active_params_b"], "gpus": m["gpus"], "url": f"{SITE}/api/v1/models/{m['slug']}.json"}
               for m in sorted(models.values(), key=lambda m: m["name"])],
}
for m in models.values():
    api_docs[f"models/{m['slug']}.json"] = {"version": "1", "updated": UPDATED, "unit": "Wh per million output tokens",
                                            "itl_deadline_ms": ITL_DEADLINE_MS, "source": SRC_MLE, "caveat": CAVEAT, **m}
api_docs["grid.json"] = {
    "version": "1", "updated": UPDATED, "year": EMBER_YEAR, "unit": "gCO2e per kWh",
    "basis": "annual average emissions intensity of total generation; hourly intensity, contracted supply and self-generation are not reflected",
    "source": SRC_EMBER, "licence": "CC BY 4.0", "world": round(world, 1),
    "note": "Area names are Ember's labels. 'WLD' is used as the code for the World row; Ember gives it none.",
    "areas": areas,
}
api_docs["hardware.json"] = {"version": "1", "updated": UPDATED, **hw}
api_docs["per-query.json"] = {
    "version": "1", "updated": UPDATED, "unit": "Wh per 1,000 queries", "round": "December 2025",
    "setup": "text generation, 1,000 queries one at a time (batch size 1), one NVIDIA H100, GPU energy only",
    "classes": {"A": "fits one consumer GPU", "B": "fits one H100", "C": "needs more than one H100"},
    "score": "1 to 5 stars, relative within the hardware class",
    "note": "The February 2025 round is not comparable with this one and is not included. Output lengths are not published, so these values cannot be converted to Wh per million tokens.",
    "source": SRC_AIES, "rows": per_query_rows,
}
api_docs["openapi.json"] = {
    "openapi": "3.1.0",
    "info": {"title": f"Lead Green {INDEX_NAME} API", "version": "1", "summary": "GPU energy per million output tokens, grid carbon, GPU hardware.",
             "description": "Static JSON files. GET only. No authentication. CORS open. Additive changes only within v1.",
             "license": {"name": "CC BY 4.0", "url": "https://creativecommons.org/licenses/by/4.0/"}},
    "servers": [{"url": f"{SITE}/api/v1"}],
    "paths": {
        "/manifest.json": {"get": {"summary": ENDPOINTS[0][1], "responses": {"200": {"description": "Manifest", "content": {"application/json": {"schema": {"type": "object"}}}}}}},
        "/index.json": {"get": {"summary": ENDPOINTS[1][1], "responses": {"200": {"description": "Index", "content": {"application/json": {"schema": {"$ref": "#/components/schemas/Index"}}}}}}},
        "/models.json": {"get": {"summary": ENDPOINTS[2][1], "responses": {"200": {"description": "Models", "content": {"application/json": {"schema": {"type": "object"}}}}}}},
        "/models/{slug}.json": {"get": {"summary": ENDPOINTS[3][1], "parameters": [{"name": "slug", "in": "path", "required": True, "schema": {"type": "string"}, "example": ref["slug"]}],
                                        "responses": {"200": {"description": "Model", "content": {"application/json": {"schema": {"type": "object"}}}}, "404": {"description": "Unknown slug"}}}},
        "/grid.json": {"get": {"summary": ENDPOINTS[4][1], "responses": {"200": {"description": "Grid", "content": {"application/json": {"schema": {"type": "object"}}}}}}},
        "/hardware.json": {"get": {"summary": ENDPOINTS[5][1], "responses": {"200": {"description": "Hardware", "content": {"application/json": {"schema": {"type": "object"}}}}}}},
        "/per-query.json": {"get": {"summary": ENDPOINTS[6][1], "responses": {"200": {"description": "Per query", "content": {"application/json": {"schema": {"type": "object"}}}}}}},
    },
    "components": {"schemas": {
        "IndexRow": {"type": "object", "properties": {
            "model": {"type": "string"}, "slug": {"type": "string"}, "model_id": {"type": "string"},
            "params_b": {"type": "number"}, "active_params_b": {"type": "number"}, "precision": {"type": "string"},
            "gpu": {"type": "string", "enum": ["H100", "B200"]}, "num_gpus": {"type": "integer"},
            "wh_per_million_output_tokens": {"type": "number"}, "joules_per_output_token": {"type": "number"},
            "median_itl_ms": {"type": "number"}, "avg_requests_in_flight": {"type": "number"},
            "gpu_power_watts_total": {"type": "number"}, "avg_output_tokens": {"type": "number"}}},
        "Index": {"type": "object", "properties": {
            "version": {"type": "string"}, "updated": {"type": "string", "format": "date"}, "unit": {"type": "string"},
            "workload": {"type": "string"}, "itl_deadline_ms": {"type": "integer"}, "source": {"type": "object"},
            "caveat": {"type": "string"}, "rows": {"type": "array", "items": {"$ref": "#/components/schemas/IndexRow"}}}},
    }},
}

# examples for the API page, taken from the real documents
_ex_index = {k: v for k, v in api_docs["index.json"].items() if k not in ("rows", "source", "caveat")}
_ex_index["source"] = {"name": SRC_MLE["name"], "version": SRC_MLE["version"], "url": SRC_MLE["url"], "...": "..."}
_ex_index["rows"] = api_docs["index.json"]["rows"][:2] + ["... " + str(len(index_rows) - 2) + " more rows"]
_ex_model = {k: v for k, v in api_docs[f"models/{ref['slug']}.json"].items() if k in ("slug", "name", "model_id", "params_b", "gpus")}
_ex_model["configurations"] = [api_docs[f"models/{ref['slug']}.json"]["configurations"][0], "... " + str(len(models[ref["slug"]]["configurations"]) - 1) + " more configurations"]
_ex_model["best"] = {g: {"num_gpus": b["num_gpus"], "wh_per_million_output_tokens": b["wh_per_million_output_tokens"], "...": "..."} for g, b in models[ref["slug"]]["best"].items()}
_ex_grid = {"year": EMBER_YEAR, "unit": "gCO2e per kWh", "world": round(world, 1),
            "areas": [a for a in areas if a["iso3"] in ("SRB", "NOR")] + ["... " + str(len(areas) - 2) + " more areas"]}
subs["API_EXAMPLE_INDEX"] = esc(json.dumps(_ex_index, ensure_ascii=False, indent=2))
subs["API_EXAMPLE_MODEL"] = esc(json.dumps(_ex_model, ensure_ascii=False, indent=2))
subs["API_EXAMPLE_GRID"] = esc(json.dumps(_ex_grid, ensure_ascii=False, indent=2))
subs["ENDPOINT_LIST"] = "\n".join(
    f"<div class=\"endpoint\"><span class=\"m\">GET</span><div><code>/api/v1/{p}</code><br>{esc(d)}</div></div>" for p, d in ENDPOINTS
)
subs["MODEL_SLUGS"] = ", ".join(f"<code>{m['slug']}</code>" for m in sorted(models.values(), key=lambda m: m["name"]))

# ----------------------------------------------------------------- pages and posts
META_RE = re.compile(r"^<!--meta\n(.*?)\n-->\n?", re.S)


def read_body(path: Path):
    text = path.read_text(encoding="utf-8")
    meta = {}
    m = META_RE.match(text)
    if m:
        for line in m.group(1).splitlines():
            if ":" in line:
                k, v = line.split(":", 1)
                meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text


def fill(text: str, mapping: dict) -> str:
    for k, v in mapping.items():
        text = text.replace("{{" + k + "}}", v)
    return text


def ld(obj) -> str:
    return "<script type=\"application/ld+json\">\n" + json.dumps(obj, ensure_ascii=False, indent=1) + "\n</script>"


ORG = {"@type": "Organization", "name": "Lead Green", "url": SITE + "/", "logo": SITE + "/assets/logo/leadgreen-icon-512.png",
       "parentOrganization": {"@type": "Organization", "name": "Katonic", "url": "https://www.katonic.ai"}}
PERSON = {"@type": "Person", "name": EDITOR, "url": LINKEDIN_URL}


def jsonld_for(kind: str, title: str, desc: str, url: str, post: dict | None = None) -> str:
    if kind == "home":
        return ld({"@context": "https://schema.org", "@graph": [
            {**ORG, "@id": SITE + "/#org", "description": desc},
            {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/", "description": desc, "publisher": {"@id": SITE + "/#org"},
             "inLanguage": "en", "license": "https://creativecommons.org/licenses/by/4.0/"},
        ]})
    if kind == "dataset":
        return ld({"@context": "https://schema.org", "@type": "Dataset", "name": f"{INDEX_NAME}: GPU energy per million output tokens",
                   "description": desc, "url": url, "license": "https://creativecommons.org/licenses/by/4.0/",
                   "creator": ORG, "publisher": ORG, "dateModified": UPDATED, "version": UPDATED, "inLanguage": "en",
                   "keywords": ["LLM inference energy", "watt-hours per token", "GPU energy", "grid carbon intensity", "H100", "B200"],
                   "variableMeasured": "GPU watt-hours per million output tokens",
                   "isBasedOn": [SRC_MLE["url"], SRC_EMBER["url"], SRC_AIES["url"], hw["sources"][0]["url"]],
                   "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}/api/v1/{p}"}
                                    for p, _ in ENDPOINTS if "{" not in p]})
    if kind == "webapi":
        return ld({"@context": "https://schema.org", "@type": "WebAPI", "name": f"Lead Green {INDEX_NAME} API", "description": desc,
                   "url": f"{SITE}/api/v1/manifest.json", "documentation": url, "provider": ORG,
                   "license": "https://creativecommons.org/licenses/by/4.0/", "termsOfService": url})
    if kind == "blog":
        return ld({"@context": "https://schema.org", "@type": "Blog", "name": "Lead Green blog", "url": url, "description": desc,
                   "publisher": ORG, "inLanguage": "en"})
    if kind == "post" and post:
        return ld({"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "description": desc,
                   "datePublished": post["date"], "dateModified": post.get("updated", post["date"]),
                   "author": PERSON, "publisher": ORG, "mainEntityOfPage": url, "url": url, "inLanguage": "en",
                   "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True})
    return ld({"@context": "https://schema.org", "@type": "WebPage", "name": title, "description": desc, "url": url,
               "publisher": ORG, "inLanguage": "en"})


layout = LAYOUT.read_text(encoding="utf-8")
outputs: dict[str, str] = {}
sitemap: list[tuple[str, str]] = []


def render(out_rel: str, nav: str, title: str, desc: str, og_type: str, kind: str, body: str, post: dict | None = None):
    depth = out_rel.count("/")
    root = "../" * depth
    path = out_rel[: -len("index.html")]
    url = f"{SITE}/{path}"
    content = fill(body, subs)
    content = fill(content, {"ROOT": root})
    page = fill(layout, {
        "TITLE": esc(title), "DESCRIPTION": esc(desc), "CANONICAL": url, "OG_TITLE": esc(title), "OG_TYPE": og_type,
        "SITE": SITE, "ROOT": root, "JSONLD": jsonld_for(kind, title, desc, url, post), "CONTENT": content,
        "UPDATED_LONG": long_date(UPDATED),
    })
    if nav:
        page = page.replace(f'data-nav="{nav}"', f'data-nav="{nav}" aria-current="page"')
    outputs[out_rel] = page
    sitemap.append((url, post["date"] if post else UPDATED))


PAGE_SPECS = [  # (file in build/pages, output path, nav key, json-ld kind)
    ("home", "index.html", "", "home"),
    ("why", "why/index.html", "why", "page"),
    ("index", "index/index.html", "index", "dataset"),
    ("api", "api/index.html", "api", "webapi"),
    ("mcp", "mcp/index.html", "mcp", "page"),
    ("blog", "blog/index.html", "blog", "blog"),
    ("newsletter", "newsletter/index.html", "newsletter", "page"),
    ("contribute", "contribute/index.html", "contribute", "page"),
    ("about", "about/index.html", "about", "page"),
]

# posts first, so the blog index can list them
posts = []
for p in sorted(POSTS.glob("*.html")):
    meta, body = read_body(p)
    for k in ("title", "description", "date"):
        if k not in meta:
            raise SystemExit(f"{p.name}: post meta is missing '{k}'")
    s = meta.get("slug") or slug(re.sub(r"^\d{4}-\d{2}-\d{2}-", "", p.stem))
    posts.append({**meta, "slug": s, "author": meta.get("author", EDITOR), "body": body, "file": p.name})
posts.sort(key=lambda x: x["date"], reverse=True)
for post in posts:
    out_rel = f"blog/{post['slug']}/index.html"
    wrapped = (
        "<article class=\"post\">\n<div class=\"title\">\n<p class=\"eyebrow\">Blog</p>\n"
        f"<h1>{esc(post['title'])}</h1>\n"
        f"<p class=\"byline\">By {esc(post['author'])} · <time datetime=\"{post['date']}\">{long_date(post['date'])}</time> · Lead Green, a Katonic project</p>\n"
        "</div>\n<div class=\"body\">\n" + post["body"] + "\n</div>\n</article>"
    )
    render(out_rel, "blog", fill(post["title"], subs), fill(post["description"], subs), "article", "post", wrapped, post)
subs["POST_LIST"] = "\n".join(
    f"<li><div class=\"byline\"><time datetime=\"{p['date']}\">{long_date(p['date'])}</time> · {esc(p['author'])}</div>"
    f"<h3><a href=\"{{{{ROOT}}}}blog/{p['slug']}/\">{esc(p['title'])}</a></h3><p>{esc(p['description'])}</p></li>"
    for p in posts
) or "<li><p class=\"muted\">No posts yet.</p></li>"
subs["POST_COUNT"] = str(len(posts))
subs["LATEST_POST_LINK"] = (f"<a href=\"{{{{ROOT}}}}blog/{posts[0]['slug']}/\">{esc(posts[0]['title'])}</a>" if posts else "")

for name, out_rel, nav, kind in PAGE_SPECS:
    meta, body = read_body(PAGES / f"{name}.html")
    for k in ("title", "description"):
        if k not in meta:
            raise SystemExit(f"pages/{name}.html: meta is missing '{k}'")
    render(out_rel, nav, fill(meta["title"], subs), fill(meta["description"], subs), meta.get("og_type", "website"), kind, body)

# ----------------------------------------------------------------- feed, sitemap, robots, llms.txt
def rfc822(iso: str) -> str:
    d = date.fromisoformat(iso)
    return format_datetime(datetime(d.year, d.month, d.day, 6, 0, tzinfo=timezone.utc))


feed_items = "\n".join(
    f"  <item>\n    <title>{esc(p['title'])}</title>\n    <link>{SITE}/blog/{p['slug']}/</link>\n"
    f"    <guid isPermaLink=\"true\">{SITE}/blog/{p['slug']}/</guid>\n    <pubDate>{rfc822(p['date'])}</pubDate>\n"
    f"    <dc:creator>{esc(p['author'])}</dc:creator>\n    <description>{esc(p['description'])}</description>\n  </item>"
    for p in posts
)
outputs["feed.xml"] = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n"
    "<rss version=\"2.0\" xmlns:atom=\"http://www.w3.org/2005/Atom\" xmlns:dc=\"http://purl.org/dc/elements/1.1/\">\n<channel>\n"
    f"  <title>Lead Green blog</title>\n  <link>{SITE}/blog/</link>\n"
    "  <description>The energy behind the token. Public measurements of GPU energy per million output tokens, and what they mean for the people who buy, run and audit AI.</description>\n"
    f"  <language>en</language>\n  <lastBuildDate>{rfc822(UPDATED)}</lastBuildDate>\n"
    f"  <atom:link href=\"{SITE}/feed.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
    f"{feed_items}\n</channel>\n</rss>\n"
)
outputs["sitemap.xml"] = (
    "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<urlset xmlns=\"http://www.sitemaps.org/schemas/sitemap/0.9\">\n"
    + "\n".join(f"  <url><loc>{u}</loc><lastmod>{d}</lastmod></url>" for u, d in sitemap)
    + "\n</urlset>\n"
)
outputs["robots.txt"] = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
outputs[".nojekyll"] = ""
outputs["llms.txt"] = f"""# Lead Green

> Lead Green is a public index of the GPU energy it takes to serve a million output tokens (watt-hours per million output tokens, Wh/M), by model, GPU and configuration, with grid carbon intensity to price it anywhere. Every figure comes from a named public source with a retrieval date. It is a Katonic project. Updated {long_date(UPDATED)}.

Key readings (ML.ENERGY Leaderboard v3.0, Text Conversation workload, energy-optimal configuration under a {ITL_DEADLINE_MS} ms median inter-token-latency limit):
- Lowest on the index: {subs['TILE_LOW_WH']} Wh/M ({subs['TILE_LOW_LABEL']})
- Reference row: {subs['REF_WH_1']} Wh/M ({subs['TILE_REF_LABEL']})
- Highest on the index: {subs['TILE_HIGH_WH']} Wh/M ({subs['TILE_HIGH_LABEL']})
- The index spans {subs['SPAN']}x. The same model on the same GPUs moves {subs['LADDER_32_RATIO']}x with concurrency ({subs['LADDER_32_FIRST']} to {subs['LADDER_32_LAST']} Wh/M for Qwen 3 32B on 2 x H100, {subs['LADDER_32_FIRST_BATCH']} to {subs['LADDER_32_LAST_BATCH']} requests in flight).
- Carbon: multiply Wh/M by the grid's gCO2e/kWh and divide by 1,000 for kg CO2e per billion tokens. Saudi Arabia {subs['SAU_G']}, Serbia {subs['SRB_G']}, Norway {subs['NOR_G']}, World {subs['WORLD_G']} gCO2e/kWh (Ember, {EMBER_YEAR}).
- Caveat: {CAVEAT}

## Pages
- [Home]({SITE}/): what Lead Green is, why it exists, who it is for
- [Why it matters]({SITE}/why/): nine reasons the number belongs in procurement, operations and reporting, with an RFP clause
- [The index]({SITE}/index/): the full tables, method, sources ledger and change record
- [Data API]({SITE}/api/): read-only JSON, CORS open, CC BY 4.0
- [MCP server]({SITE}/mcp/): tools for AI assistants (list_models, energy_per_million_tokens, estimate, compare_gpus, concurrency_curve, grid_intensity, gpu_hardware, sources)
- [Blog]({SITE}/blog/): RSS at {SITE}/feed.xml
- [Newsletter]({SITE}/newsletter/)
- [Contribute]({SITE}/contribute/): volunteer roles and the measurement protocol
- [About]({SITE}/about/)

## Data API (JSON)
""" + "\n".join(f"- {SITE}/api/v1/{p}: {d}" for p, d in ENDPOINTS) + f"""

## Sources
- {SRC_MLE['name']} ({SRC_MLE['publisher']}), {SRC_MLE['version']}, {SRC_MLE['licence']}: {SRC_MLE['url']}
- {SRC_EMBER['name']}, {SRC_EMBER['version']}, {SRC_EMBER['licence']}: {SRC_EMBER['url']}
- NVIDIA MIG profiles, product specifications and the HGX B200 product carbon footprint summary: {hw['sources'][0]['url']}
- {SRC_AIES['name']} ({SRC_AIES['publisher']}), {SRC_AIES['version']}: {SRC_AIES['url']}

## Licence
{LICENCE_TEXT} Code: Apache 2.0.
"""

# ----------------------------------------------------------------- validate, then write
PLACEHOLDER = re.compile(r"\{\{[A-Za-z0-9_]+\}\}")
problems = []
for rel, text in outputs.items():
    left = sorted(set(PLACEHOLDER.findall(text)))
    if left:
        problems.append(f"{rel}: unfilled {', '.join(left)}")
    if chr(8212) in text or chr(8211) in text:   # em dash, en dash
        problems.append(f"{rel}: contains an em or en dash")
for rel, doc in api_docs.items():
    json.loads(jdump(doc))
if problems:
    sys.exit("REFUSING TO WRITE:\n  " + "\n  ".join(problems))

for rel, text in outputs.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
for rel, doc in api_docs.items():
    p = API_DIR / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(jdump(doc), encoding="utf-8", newline="\n")
shutil.rmtree(MCP_DATA, ignore_errors=True)
shutil.copytree(API_DIR, MCP_DATA)

wheel = ROOT / "dist" / WHEEL_NAME
print(f"wrote {len(outputs)} pages/files and {len(api_docs)} API documents; {len(index_rows)} index rows from {len(cfgs)} configurations; "
      f"{grid_count} grids; {len(posts)} posts; reference {ref['model']} {ref['num_gpus']}x{ref['gpu']} = {ref_wh:.1f} Wh/M")
if not wheel.exists():
    print(f"NOTE: {wheel.relative_to(ROOT)} is missing; the MCP page's install line points at it. "
          f"Build it with: python -m pip wheel ./leadgreen-mcp -w dist --no-deps")
