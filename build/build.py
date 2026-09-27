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
name), point the constants below at it, bump UPDATED, RETRIEVED and the source
versions, add an entry to CHANGES (the index page's change record and
api/v1/changes.json are both generated from it), and re-run. Never type a
figure into a page by hand.
"""
from __future__ import annotations

import csv
import hashlib
import html
import json
import os
import re
import shutil
import sys
import zipfile
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
UPDATED = "2026-09-27"                 # bump on every data or content change
DATA_VERSION = UPDATED                 # D20: carried by every API document; a published release never changes
RETRIEVED = "2026-09-26"               # when the snapshots in build/data were retrieved; not the same as UPDATED
INDEX_NAME = "Green Tokens"            # D1: "Green Tokens" or "The Green Token Index"
EDITOR = "Prem Naraindas"
LINKEDIN_URL = "https://www.linkedin.com/in/premnaraindas/"
OWN_YOUR_AI_URL = "https://www.linkedin.com/newsletters/own-your-ai-7508174547041292288/"
REPO_URL = ""                          # D6: set when the repository is public; links are omitted while empty
NEWSLETTER_SIGNUP_URL = ""             # D2: set when the email provider is chosen; never a fake form
MCP_VERSION = "0.2.0"
WHEEL_NAME = f"leadgreen_mcp-{MCP_VERSION}-py3-none-any.whl"
WHEEL_URL = f"{SITE}/dist/{WHEEL_NAME}"
# D16 publisher block. The address is typed only from the DIFC registry extract, after Prem confirms it.
PUBLISHER_ENTITY = "Katonic AI Technology Ltd"
PUBLISHER_REGISTRATION = "CL9944"
PUBLISHER_JURISDICTION = "Dubai International Financial Centre (DIFC), United Arab Emirates"
PUBLISHER_ADDRESS = ""                 # OWED: registered office, word for word from the registry extract
CONTACT_EMAIL = "hello@leadgreen.ai"   # D16: forwarded to the editor; mail on the domain must work before launch
RESPONSE_DAYS = 10                     # working days, for corrections and contributions
REVIEWERS: list[str] = []              # D1 OWED: the two named reviewers
OUTSIDE_REVIEWER = ""                  # D1 OWED: the reviewer with no Katonic affiliation who checks any Katonic row
SUBMISSIONS_OPEN = ""                  # D19: date contributed rows open while the repository is not public; "" = to be announced
MLE_LICENCE_CONFIRMED = False          # D17: True once the ML.ENERGY team confirms the leaderboard JSON is Apache 2.0
LEGAL_AS_AT = "2026-09-27"             # D15: the date the regulatory summaries were checked

MLE_CHAT = DATA / "mlenergy-v3-lm-arena-chat-2026-09-26.json"
MLE_GPQA = DATA / "mlenergy-v3-gpqa-2026-09-26.json"
EMBER = DATA / "ember-yearly-total-generation-extract-2026-09-26.csv"
AIES = DATA / "aienergyscore-text_generation-2026-09-26.csv"
HW = DATA / "nvidia-hardware-2026-09-26.json"
ISO3166 = DATA / "iso3166-1-alpha3-to-alpha2-2026-09-27.json"   # pycountry 26.2.16 (Debian iso-codes)
MEASUREMENTS = DATA / "measurements"
MEASUREMENT_SCHEMA = HERE / "schema" / "measurement.schema.json"

ITL_DEADLINE_MS = 500          # D5: the leaderboard's default for every LLM task (tasks.ts defaultItlDeadlineMs, the slider's start)
GPQA_DEADLINE_MS = 500         # D5: the same default; rows at or under the ceiling are kept, as the leaderboard keeps them
BOUNDARY = "gpu_only"             # D4: carried beside caveat; host, network, cooling and idle are outside it
SENSITIVITY_MS = (250, 100, 50)  # D5: tighter ceilings reported under Method; none of them is applied to the index
EMBER_YEAR = "2024"            # latest year with every listed grid present
REFERENCE = ("Qwen 3 32B", "H100")   # the row the carbon table is priced on
ELECTRICITY_USD_PER_KWH = 0.10       # stated assumption in one worked example
KETTLE_KW = 2.0                      # stated assumption in one worked example
PUE_EXAMPLE = 1.3                    # D4: stated assumption in the to-the-meter illustration (PUE is the operator's own figure)
SCI_LIFE_YEARS = 5                   # stated assumption in the SCI illustration (hardware life over which M is amortised)
AIES_FIXED_TOKENS = 10               # AI Energy Score protocol: ten generated tokens for non-reasoning runs (reasoning_helpers.py)
# Published per-prompt figures, cited on the site (F2, D4, D9). Neither is Wh per million output tokens at a stated load.
GOOGLE_2025 = {"date": "August 2025", "wh": 0.24, "accelerator_share": 0.58, "narrow_wh": 0.10, "g_co2e": 0.03,
               "water_ml": 0.26, "url": "https://arxiv.org/abs/2508.15734"}
MISTRAL_2025 = {"date": "July 2025", "g_co2e": 1.14, "water_ml": 45, "tokens": 400,
                "url": "https://mistral.ai/news/our-contribution-to-a-global-environmental-standard-for-ai"}

MLE_LICENCE_EVIDENCE = [
    "Hugging Face dataset ml-energy/benchmark-v3: tagged license:apache-2.0, ships a LICENSE file, and its dataset card's License section reads Apache-2.0",
    "The ML.ENERGY Leaderboard web app's footer says Apache 2.0",
    ("The ML.ENERGY team has confirmed that the licence covers the leaderboard JSON files" if MLE_LICENCE_CONFIRMED else
     "The leaderboard repository (github.com/ml-energy/leaderboard) carries no licence file; its JSON files are reproduced here "
     "as published measurements until the ML.ENERGY team confirms that the dataset licence covers them"),
]
SRC_MLE = {
    "name": "ML.ENERGY Leaderboard",
    "publisher": "The ML.ENERGY Initiative (started at SymbioticLab, University of Michigan)",
    "url": "https://ml.energy/leaderboard/",
    "data_url": "https://raw.githubusercontent.com/ml-energy/leaderboard/master/public/data/tasks/lm-arena-chat.json",
    "version": "3.0 (released 2025-12-01); data compiled 2026-02-16",
    "released": "2025-12-01",
    "compiled": "2026-02-16",
    "compiled_evidence": "the leaderboard's public/data/index.json last_updated, and the last commit to the task files, both 2026-02-16",
    "retrieved": RETRIEVED,
    "licence": "Apache-2.0 per the ml-energy/benchmark-v3 dataset card",
    "licence_evidence": MLE_LICENCE_EVIDENCE,
    "workload": "Text Conversation (lm-arena-chat)",
    "method": ("Energy per output token is steady-state GPU energy divided by the output tokens generated in the steady-state window "
               "(the benchmark's steady_state_energy_per_token), measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers. "
               "Energy per request is that figure multiplied by the average output length, not a separate measurement. "
               "Prompt processing is included."),
    "selection": (f"Each index row is the lowest-energy configuration for its model and GPU whose median inter-token latency does not "
                  f"exceed {ITL_DEADLINE_MS} ms, the leaderboard's own default ceiling; no measured configuration reaches it."),
    "cite": "Chung et al., The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371",
    "cite_url": "https://arxiv.org/abs/2505.06371",
    "used_for": "index, per-model configurations, concurrency curves, measured GPU power",
}
SRC_MLE_GPQA = {**SRC_MLE, "data_url": SRC_MLE["data_url"].replace("lm-arena-chat", "gpqa"),
                "workload": "Problem Solving (gpqa)", "used_for": "problem-solving versus chat comparison"}
EMBER_BASIS = ("Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors "
               "(IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are "
               "included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, "
               "not a Scope 2 combustion factor to file as reported.")
SRC_EMBER = {
    "name": "Ember, Yearly electricity data",
    "publisher": "Ember",
    "url": "https://ember-energy.org/data/yearly-electricity-data/",
    "data_url": "https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_yearly_global.csv",
    "version": "September 2026 release (file last modified 2026-09-22)",
    "retrieved": RETRIEVED,
    "licence": "CC-BY-4.0",
    "factor_basis": EMBER_BASIS,
    "used_for": f"grid emissions intensity of total generation, gCO2e per kWh, {EMBER_YEAR} (location-based)",
}
SRC_AIES = {
    "name": "AI Energy Score leaderboard",
    "publisher": "AI Energy Score (Hugging Face and Salesforce, with Neuralwatt, Cohere, Meta and Carnegie Mellon University)",
    "url": "https://huggingface.co/spaces/AIEnergyScore/Leaderboard",
    "data_url": "https://huggingface.co/spaces/AIEnergyScore/Leaderboard/raw/main/data/energy/text_generation.csv",
    "documentation": "https://huggingface.github.io/AIEnergyScore/",
    "version": "December 2025 round",
    "harness": "Neuralwatt's AI Energy Benchmarks for the December 2025 round; the February 2025 round ran on Optimum Benchmark",
    "retrieved": RETRIEVED,
    "licence": ("Apache-2.0 as tagged on the Space; the project states no separate licence for the results file, "
                "which is reproduced as facts with attribution"),
    "used_for": ("GPU energy per 1,000 text-generation queries at batch size 1 on NVIDIA H100 80GB GPUs "
                 "(one card for class A and B models, several for class C)"),
}
SRC_OPENAI_TOKENS = {
    "name": "OpenAI, What are tokens and how to count them",
    "publisher": "OpenAI",
    "url": "https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them",
    "version": "as published on the retrieval date",
    "retrieved": RETRIEVED,
    "licence": "cited, not redistributed",
    "used_for": "the rough words-per-token conversion",
}
SRC_GOOGLE_2025 = {
    "name": "Elsworth et al., Measuring the environmental impact of delivering AI at Google Scale",
    "publisher": "Google",
    "url": GOOGLE_2025["url"],
    "version": "arXiv 2508.15734, August 2025",
    "retrieved": RETRIEVED,
    "licence": "cited, not redistributed",
    "used_for": "the published per-prompt energy, carbon and water figures, and the accelerator share of serving energy",
}
SRC_MISTRAL_2025 = {
    "name": "Mistral AI, life-cycle analysis of its models (with Carbone 4 and ADEME)",
    "publisher": "Mistral AI",
    "url": MISTRAL_2025["url"],
    "version": "22 July 2025",
    "retrieved": RETRIEVED,
    "licence": "cited, not redistributed",
    "used_for": "the published per-reply carbon and water figures",
}
NVIDIA_LICENCE = "manufacturer specifications transcribed as facts; NVIDIA retains its rights in the source documents"
CAVEAT = ("GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration "
          "under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; "
          "a lightly used server sits well above it.")
BOUNDARY = "gpu_only"
FUNDING = ("Lead Green is run and paid for by Katonic, which sells a sovereign AI platform and benefits when buyers ask the "
           "questions on this site. It takes no money from hardware, cloud or model vendors.")
LICENCE_TEXT = ("Compilation and site text: CC BY 4.0. Code: Apache 2.0. Third-party figures remain subject to their sources' "
                "terms, listed per source.")


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


WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve"]


def word(n: int) -> str:
    return WORDS[n] if 0 <= n < len(WORDS) else f"{n:,}"


def times(x: float, d: int = 1) -> str:
    return f"{x:,.{d}f}×"


LEGAL_NOTE = f"Regulatory summaries on this site are as at {long_date(LEGAL_AS_AT)}, for orientation, and are not legal advice."
ATTRIBUTION = (f"{INDEX_NAME} index, Lead Green, a Katonic project, {SITE}/api/v1/, CC BY 4.0. Contains data from the "
               f"ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; data compiled {SRC_MLE['compiled']}, retrieved {RETRIEVED}) "
               "and Ember Yearly Electricity Data (CC BY 4.0). Changes: [none | describe].")


# ----------------------------------------------------------------- ML.ENERGY
chat = json.loads(MLE_CHAT.read_text(encoding="utf-8"))
cfgs = chat["configurations"]
gpqa = json.loads(MLE_GPQA.read_text(encoding="utf-8"))["configurations"]
for _src, _n in ((SRC_MLE, len(cfgs)), (SRC_MLE_GPQA, len(gpqa))):
    _src["configurations"] = (f"{_n} stable configurations: the leaderboard publishes the runs that passed its stability filter; "
                              "every run, including the unstable ones, is in the gated Hugging Face dataset ml-energy/benchmark-v3")


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


# F31: the source publishes a few configurations twice, with different results. Number the runs of an
# identical configuration in source order; row_id carries the run number from the second run on.
_seen: dict[tuple, int] = {}
RUN_NO: dict[int, int] = {}
for _c in cfgs:
    _k = (slug(_c["nickname"]), _c["gpu_model"], _c["num_gpus"], _c["max_num_seqs"], _c["tensor_parallel"],
          _c["data_parallel"], _c["expert_parallel"], _c["weight_precision"])
    _seen[_k] = _seen.get(_k, 0) + 1
    RUN_NO[id(_c)] = _seen[_k]


def api_wh(c) -> float:
    return round(round(c["energy_per_token_joules"], 7) * 1_000_000 / 3600, 2)


def row_id(c) -> str:
    base = f"{slug(c['nickname'])}/{c['gpu_model']}/{c['num_gpus']}/{c['max_num_seqs']}"
    n = RUN_NO[id(c)]
    return base if n == 1 else f"{base}/r{n}"


_ids = [row_id(c) for c in cfgs]
assert len(set(_ids)) == len(_ids), "row_id is not unique; extend it with the parallelism"
REPEATED = {k for k, n in _seen.items() if n > 1}


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
        "wh_per_million_output_tokens": api_wh(c),
        "joules_per_output_token": round(c["energy_per_token_joules"], 7),
        "median_itl_ms": round(c["median_itl_ms"], 1),
        "avg_requests_in_flight": round(c["avg_batch_size"], 1),
        "gpu_power_watts_total": round(c["avg_power_watts"]),
        "avg_output_tokens": round(c["avg_output_len"]),
        "avg_running_batch": round(c["avg_batch_size"], 1),
        "max_num_seqs": c["max_num_seqs"],
        "row_id": row_id(c),
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
        "wh_per_million_output_tokens": api_wh(c),
        "joules_per_output_token": round(c["energy_per_token_joules"], 7),
        "median_itl_ms": round(c["median_itl_ms"], 1),
        "p90_itl_ms": round(c["p90_itl_ms"], 1),
        "p99_itl_ms": round(c["p99_itl_ms"], 1),
        "tokens_per_second": round(c["output_throughput_tokens_per_sec"], 1),
        "gpu_power_watts_total": round(c["avg_power_watts"]),
        "avg_output_tokens": round(c["avg_output_len"]),
        "under_itl_deadline": c["median_itl_ms"] <= ITL_DEADLINE_MS,
        "avg_running_batch": round(c["avg_batch_size"], 1),
        "p95_itl_ms": round(c["p95_itl_ms"], 1),
        "row_id": row_id(c),
        "repeat": RUN_NO[id(c)],
    }


# D20: the API's Wh/M is computed from the seven-decimal joules it publishes, so a consumer who recomputes
# Wh/M = J x 1,000,000 / 3,600 from the published joules gets the published value on every configuration.
# (Seven decimals alone leave one configuration on a rounding edge; deriving from the published joules closes it.)
API_WH_EDGE = [row_id(_c) for _c in cfgs if api_wh(_c) != round(wh_per_million(_c["energy_per_token_joules"]), 2)]


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
    m["configurations"].sort(key=lambda x: (x["gpu"], x["num_gpus"], x["avg_requests_in_flight"], x["repeat"]))


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
            f"<td class=\"num key\">{ratio:.2f}×</td>"
            "</tr>"
        )
    return "\n".join(out), rows


def ladder(name, gpu, num_gpus):
    rows = sorted((c for c in cfgs if c["nickname"] == name and c["gpu_model"] == gpu and c["num_gpus"] == num_gpus),
                  key=lambda c: (c["max_num_seqs"], RUN_NO[id(c)]))
    best_c = min(rows, key=lambda c: c["energy_per_token_joules"])
    out = []
    for c in rows:
        mark = " class=\"best\"" if c is best_c else ""
        out.append(
            f"<tr{mark}>"
            f"<th scope=\"row\" class=\"num\">{fmt(c['max_num_seqs'], 0)}</th>"
            f"<td class=\"num\">{fmt(c['avg_batch_size'], 0)}</td>"
            f"<td class=\"num key\">{fmt(wh_per_million(c['energy_per_token_joules']))}</td>"
            f"<td class=\"num\">{fmt(c['median_itl_ms'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['output_throughput_tokens_per_sec'], 0)}</td>"
            f"<td class=\"num\">{fmt(c['avg_power_watts'], 0)}</td>"
            "</tr>"
        )
    first = rows[0]
    i = rows.index(best_c)
    turn = rows[i + 1] if i + 1 < len(rows) else None
    return {
        "rows": "\n".join(out), "count": len(rows),
        "ratio": first["energy_per_token_joules"] / best_c["energy_per_token_joules"],
        "first": wh_per_million(first["energy_per_token_joules"]), "best": wh_per_million(best_c["energy_per_token_joules"]),
        "first_w": first["avg_power_watts"], "best_w": best_c["avg_power_watts"],
        "power_pct": (best_c["avg_power_watts"] / first["avg_power_watts"] - 1) * 100,
        "first_itl": first["median_itl_ms"], "best_itl": best_c["median_itl_ms"],
        "max_itl_to_best": max(c["median_itl_ms"] for c in rows[: i + 1]),
        "first_tps": first["output_throughput_tokens_per_sec"], "best_tps": best_c["output_throughput_tokens_per_sec"],
        "tps_ratio": best_c["output_throughput_tokens_per_sec"] / first["output_throughput_tokens_per_sec"],
        "first_batch": first["avg_batch_size"], "best_batch": best_c["avg_batch_size"],
        "first_cap": first["max_num_seqs"], "best_cap": best_c["max_num_seqs"],
        # aliases kept while pages still say "last": the last row the old pages showed was the best row
        "last": wh_per_million(best_c["energy_per_token_joules"]), "last_w": best_c["avg_power_watts"],
        "last_itl": best_c["median_itl_ms"], "last_tps": best_c["output_throughput_tokens_per_sec"],
        "last_batch": best_c["avg_batch_size"],
        "turn": None if turn is None else {
            "cap": turn["max_num_seqs"], "wh": wh_per_million(turn["energy_per_token_joules"]),
            "itl": turn["median_itl_ms"], "batch": turn["avg_batch_size"]},
    }


# problem solving versus chat, same model and GPU, best row of each task (F30, D23)
gpqa_pairs = []
for k, c in best.items():
    if k in best_gpqa:
        g = best_gpqa[k]
        gpqa_pairs.append({
            "model": k[0], "gpu": k[1], "num_gpus": c["num_gpus"], "num_gpus_gpqa": g["num_gpus"],
            "ratio": g["energy_per_request_joules"] / c["energy_per_request_joules"],
            "ratio_tok": g["energy_per_token_joules"] / c["energy_per_token_joules"],
            "ratio_out": g["avg_output_len"] / c["avg_output_len"],
            "out_gpqa": g["avg_output_len"], "out_chat": c["avg_output_len"],
            "batch_chat": c["avg_batch_size"], "batch_gpqa": g["avg_batch_size"],
            "wh_chat": wh_per_million(c["energy_per_token_joules"]),
            "wh_gpqa": wh_per_million(g["energy_per_token_joules"]),
        })
gpqa_pairs.sort(key=lambda p: p["ratio"])
gp_nemo = [p for p in gpqa_pairs if "Nemotron" in p["model"]]
gp_rest = [p for p in gpqa_pairs if "Nemotron" not in p["model"]]
gp_rest_families = sorted({p["model"].split()[0] for p in gp_rest})


def gpqa_table() -> str:
    out = []
    for p in gpqa_pairs:
        gpus = (f"{p['num_gpus']} × {p['gpu']}" if p["num_gpus"] == p["num_gpus_gpqa"]
                else f"{p['num_gpus']} and {p['num_gpus_gpqa']} × {p['gpu']}")
        out.append(
            "<tr>"
            f"<th scope=\"row\"><span class=\"model\">{esc(p['model'])}</span></th>"
            f"<td class=\"num\">{gpus}</td>"
            f"<td class=\"num key\">{times(p['ratio'])}</td>"
            f"<td class=\"num\">{times(p['ratio_tok'], 2)}</td>"
            f"<td class=\"num\">{fmt(p['out_chat'], 0)} / {fmt(p['out_gpqa'], 0)}</td>"
            f"<td class=\"num\">{fmt(p['batch_chat'], 0)} / {fmt(p['batch_gpqa'], 0)}</td>"
            "</tr>"
        )
    return "\n".join(out)


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
REFERENCE_GRIDS = ("DEU", "FRA", "GBR", "IRL", "NOR", "USA", "JPN")  # D6: shown for reference; the rest are markets Katonic sells in or expects to
assert set(REFERENCE_GRIDS) <= {c for c, _ in COUNTRIES}
SHORT_NAMES = {  # F23: the short names the site shows; grid.json carries them as display_name
    "Hong Kong (SAR of China)": "Hong Kong", "Macao (SAR of China)": "Macao", "Taiwan (China)": "Taiwan",
    "Cook Islands (the)": "Cook Islands", "Palestine (State of)": "Palestine", "Tanzania (the United Republic of)": "Tanzania",
}
ISO2 = json.loads(ISO3166.read_text(encoding="utf-8"))["alpha_3_to_alpha_2"]
years_by_area: dict[str, dict[str, float]] = {}
for r in ember:
    key = "WLD" if r["Area"] == "World" else r["ISO 3 code"]
    val = r["Emissions intensity (gCO2e/kWh)"]
    if key and val != "":
        years_by_area.setdefault(key, {})[r["Year"]] = round(float(val), 1)
areas = []
intensity: dict[str, float] = {}
for r in ember:
    if r["Year"] != EMBER_YEAR:
        continue
    g = float(r["Emissions intensity (gCO2e/kWh)"])
    if r["Area"] == "World":
        intensity["World"] = g
        yrs = dict(sorted(years_by_area["WLD"].items()))
        areas.append({"iso3": "WLD", "name": "World", "area_type": "world", "g_co2e_per_kwh": round(g, 1),
                      "display_name": "World", "iso2": None, "years": yrs, "latest_year": max(yrs)})
        continue
    intensity[r["ISO 3 code"]] = g
    yrs = dict(sorted(years_by_area[r["ISO 3 code"]].items()))
    areas.append({"iso3": r["ISO 3 code"], "name": r["Area"], "area_type": "country", "continent": r["Continent"],
                  "g_co2e_per_kwh": round(g, 1), "display_name": SHORT_NAMES.get(r["Area"], r["Area"]),
                  "iso2": ISO2.get(r["ISO 3 code"]), "years": yrs, "latest_year": max(yrs)})
areas.sort(key=lambda a: (a["area_type"] != "world", a["name"]))
world = intensity["World"]
grid_count = sum(1 for a in areas if a["area_type"] == "country")
countries_only = [a for a in areas if a["area_type"] == "country"]
grid_min = min(countries_only, key=lambda a: intensity[a["iso3"]])
grid_max = max(countries_only, key=lambda a: intensity[a["iso3"]])
grid_2025_count = sum(1 for a in countries_only if "2025" in a["years"])
no_2025_listed = [name for iso, name in COUNTRIES if "2025" not in years_by_area[iso]]
no_iso2 = [a["name"] for a in countries_only if not a["iso2"]]


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


def aies_row(r) -> dict:
    row = {"model": r["model"].replace("*", ""), "class": r["class"],
           "wh_per_1000_queries": round(float(r["total_gpu_energy"]) * 1000, 1), "score": int(r["energy_score"]),
           "source_label": r["model"]}
    if "*" in r["model"]:
        row["note"] = "The source marks this row with an asterisk; model holds the clean Hugging Face id."
    return row


per_query_rows = sorted((aies_row(r) for r in aies_dec), key=lambda x: x["wh_per_1000_queries"])


def aies_table() -> str:
    out = []
    for r in per_query_rows:
        out.append(
            "<tr>"
            f"<th scope=\"row\"><span class=\"model\">{esc(r['model'])}</span></th>"
            f"<td>{r['class']}</td>"
            f"<td class=\"num key\">{fmt(r['wh_per_1000_queries'])}</td>"
            f"<td class=\"num\">{'★' * r['score']}{'☆' * (5 - r['score'])}</td>"
            "</tr>"
        )
    return "\n".join(out)


def aies_val(model_id: str, round_prefix: str = "Dec") -> float:
    return next(round(float(r["total_gpu_energy"]) * 1000, 1) for r in aies
                if r["model"] == model_id and r["test date"].strip().startswith(round_prefix))


aies_class = {}
for cl in ("A", "B", "C"):
    vals = [r["wh_per_1000_queries"] for r in per_query_rows if r["class"] == cl]
    lo, hi = min(vals), max(vals)
    aies_class[cl] = {"count": len(vals), "lo": lo, "hi": hi, "five_star_up_to": lo + (hi - lo) / 5}
_c5 = [r for r in per_query_rows if r["class"] == "C" and r["score"] == 5]
_b_low = min((r for r in per_query_rows if r["class"] == "B"), key=lambda r: r["score"])
aies_heavy5 = max(_c5, key=lambda r: r["wh_per_1000_queries"])
aies_light_b = min((r for r in per_query_rows if r["class"] == "B" and r["score"] == _b_low["score"]),
                   key=lambda r: r["wh_per_1000_queries"])


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
l32 = ladder("Qwen 3 32B", "H100", 2)
l8 = ladder("Llama 3.1 8B Instruct", "H100", 1)
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
aies_70b_feb = aies_val("meta-llama/Meta-Llama-3-70B", "Feb")
aies_apertus = aies_val("swiss-ai/Apertus-70B-Instruct-2509")
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
        "the fortnightly LinkedIn newsletter, which will carry one number from this index in every issue from its next edition.</p>"
        f"<div class=\"actions\"><a class=\"cta solid\" href=\"{OWN_YOUR_AI_URL}\">Read Own Your AI on LinkedIn</a>"
        "<a class=\"cta\" href=\"{{ROOT}}feed.xml\">Blog RSS feed</a></div>"
    ),
    # tables
    "INDEX_ROWS": index_table(), "PAIR_ROWS": pairs_html,
    "LADDER_32_ROWS": l32["rows"], "LADDER_8_ROWS": l8["rows"],
    "CARBON_ROWS": carbon_table(), "AIES_ROWS": aies_table(),
    "TDP_ROWS": tdp_table(), "MIG_ROWS": mig_table(),
    # tiles and counts
    "TILE_LOW_WH": fmt(raw_wh(low), 1),
    "TILE_LOW_LABEL": f"{low['model']}, {low['num_gpus']} × {low['gpu']}",
    "TILE_REF_WH": fmt(ref_wh, 1),
    "TILE_REF_LABEL": f"{ref['model']}, {ref['num_gpus']} × {ref['gpu']}",
    "TILE_HIGH_WH": fmt(raw_wh(high), 1),
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
    "PAIR_MAX_MODEL": pairs[0][0], "PAIR_MAX_RATIO": f"{pairs[0][3]:.2f}",
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

# ----------------------------------------------------------------- derived figures added in the review fixes
def cfg_wh(c) -> float:
    return wh_per_million(c["energy_per_token_joules"])


def and_list(items: list[str]) -> str:
    items = list(items)
    if len(items) <= 1:
        return "".join(items)
    return ", ".join(items[:-1]) + " and " + items[-1]


def short_date(iso: str) -> str:
    d = date.fromisoformat(iso)
    return f"{d.day} {d:%b %Y}"


def tile_sub(r, extra: str = "") -> str:
    c = r["_cfg"]
    return (f"{r['model']}, {r['num_gpus']} × {r['gpu']}. Running batch {fmt(c['avg_batch_size'], 0)}, "
            f"median ITL {fmt(c['median_itl_ms'], 0)} ms.{extra}")


ref_rank = index_rows.index(ref) + 1
max_chat_itl = max(c["median_itl_ms"] for c in cfgs)
max_gpqa_itl = max(c["median_itl_ms"] for c in gpqa)

# D5: what tighter ceilings would do (reported, not applied)
def sens_part(d: int) -> str:
    b = best_by_model_gpu(cfgs, d)
    changed = sum(1 for k, c in best.items() if b.get(k) is not c)
    gone = sum(1 for k in best if k not in b)
    ordered = sorted(b.values(), key=lambda c: c["energy_per_token_joules"])
    lo, hi = ordered[0], ordered[-1]
    part = f"at {d} ms, {changed} {'row changes' if changed == 1 else 'rows change'}"
    if gone:
        part += f" ({gone} of them with no configuration that fast)"
    extra = []
    if lo is not low["_cfg"]:
        extra.append(f"the lowest becomes {lo['nickname']} on {lo['num_gpus']} × {lo['gpu_model']} at {fmt(cfg_wh(lo))} Wh/M")
    if hi is not high["_cfg"]:
        extra.append(f"the highest becomes {hi['nickname']} on {hi['num_gpus']} × {hi['gpu_model']} at {fmt(cfg_wh(hi))} Wh/M")
    return part + (" and " + " and ".join(extra) if extra else "")


_sens = [sens_part(d) for d in SENSITIVITY_MS]
sens_sentence = (_sens[0][0].upper() + _sens[0][1:] + "; " + "; ".join(_sens[1:]) + ".")

# D5: the two generations at a 50 ms ceiling
_b50 = best_by_model_gpu(cfgs, 50)
_both50 = sorted({k[0] for k in _b50 if (k[0], "H100") in _b50 and (k[0], "B200") in _b50})
_hwins = [(m, _b50[(m, "H100")], _b50[(m, "B200")]) for m in _both50
          if _b50[(m, "H100")]["energy_per_token_joules"] < _b50[(m, "B200")]["energy_per_token_joules"]]
pair50_sentence = (
    f"At a 50 ms ceiling the comparison shifts: {len(_both50)} models still have a row on both cards, and the H100 uses less "
    f"energy per token than the B200 on {word(len(_hwins))} of them ("
    + "; ".join(f"{m}, {fmt(cfg_wh(h))} Wh/M on {h['num_gpus']} × H100 against {fmt(cfg_wh(b))} on {b['num_gpus']} × B200"
                for m, h, b in _hwins) + ")."
) if _hwins else f"At a 50 ms ceiling, {len(_both50)} models still have a row on both cards, and the B200 stays ahead on every one."

# D23: the widest generations gap, read against the sweep that produced it (F34)
_pm, _ph, _pb, _pratio = pairs[0]
_h_sweep = [c for c in cfgs if c["nickname"] == _pm and c["gpu_model"] == "H100"]
_h_counts = sorted({c["num_gpus"] for c in _h_sweep})
_h_cap_max = max(c["max_num_seqs"] for c in _h_sweep)
_hc, _bc = _ph["_cfg"], _pb["_cfg"]
_match = [c for c in cfgs if c["nickname"] == _pm and c["gpu_model"] == "B200" and c["num_gpus"] == _bc["num_gpus"]
          and c["max_num_seqs"] == _hc["max_num_seqs"]]
assert len(_match) == 1, "no B200 row at the H100 row's cap"
_mc = _match[0]
_match_ratio = cfg_wh(_hc) / cfg_wh(_mc)
_sweep_phrase = (f"was run only at {word(_h_counts[0])} cards and a cap of at most {_h_cap_max:,} requests" if len(_h_counts) == 1
                 else f"was run at {and_list([str(n) for n in _h_counts])} cards and a cap of at most {_h_cap_max:,} requests")
_nemo_pairs = [(m, h["_cfg"], b["_cfg"]) for m, h, b, _ in pairs if "Nemotron" in m]
_nemo_pairs.sort(key=lambda t: t[0])
pair_sweep_sentence = (
    f"The gap also depends on which configurations were swept. The {_pratio:.2f}× pair compares an H100 row that {_sweep_phrase} "
    f"with a B200 row at a running batch of {fmt(_bc['avg_batch_size'], 0)} on {word(_bc['num_gpus'])} cards; at the same cap of "
    f"{_hc['max_num_seqs']:,} the B200 row reads {fmt(cfg_wh(_mc))} Wh/M against the H100's {fmt(cfg_wh(_hc))}, a gap of "
    f"{_match_ratio:.2f}×."
    + (f" The {word(len(_nemo_pairs))} Nemotron pairs compare runs whose average answers are "
       + and_list([f"{b['avg_output_len'] / h['avg_output_len']:.1f}" for _, h, b in _nemo_pairs])
       + " times longer on the B200 ("
       + and_list([fmt(h['avg_output_len'], 0) for _, h, _b in _nemo_pairs]) + " tokens on the H100 against "
       + and_list([fmt(b['avg_output_len'], 0) for _, _h, b in _nemo_pairs]) + ")." if _nemo_pairs else "")
)

# D23 / F30: the two workloads
_rest_fam = sorted({p["model"].split()[0] for p in gp_rest}, key=lambda f: (-sum(1 for p in gp_rest if p["model"].startswith(f)), f))
gpqa_tok_sentence = (
    f"and because the long outputs cut the batch the server can hold, so energy per token itself is "
    f"{min(p['ratio_tok'] for p in gp_rest):.1f} to {max(p['ratio_tok'] for p in gp_rest):.1f} times the Text Conversation figure "
    f"for the {and_list(_rest_fam)} pairs, and {min(p['ratio_tok'] for p in gp_nemo):.1f} to "
    f"{max(p['ratio_tok'] for p in gp_nemo):.1f} times it for the {word(len(gp_nemo))} Nemotron pairs"
)

# D4: to the meter. The printed sum uses the displayed factors so that it multiplies out as printed.
_sys = hw["systems"][0]
_sys_n = int(re.match(r"\s*(\d+)", _sys["gpus"]).group(1))
_b200_w = next(t["max_tdp_w"] for t in hw["tdp"] if t["gpu"].startswith("B200"))
gpu_kw_sys = _sys_n * _b200_w / 1000
sys_ratio = _sys["max_power_kw"] / gpu_kw_sys
meter_wh = round(ref_wh, 1) * round(sys_ratio, 2) * PUE_EXAMPLE
meter_tokens_b = 1_000_000 / meter_wh / 1000

# F4: SCI illustration, M against E x I, for the one index row that uses a whole eight-GPU baseboard
_sci = next(r for r in index_rows if (r["model"], r["gpu"]) == ("DeepSeek V3.1", "B200"))
assert _sci["num_gpus"] == _sys_n, "the SCI illustration needs a row that uses one whole eight-GPU baseboard"
_sci_g_per_h = hw["embodied"]["kg_co2e_cradle_to_gate"] * 1000 / (SCI_LIFE_YEARS * 8760)
_sci_mtok_per_h = _sci["_cfg"]["output_throughput_tokens_per_sec"] * 3600 / 1_000_000
sci_m_per_m = _sci_g_per_h / _sci_mtok_per_h
sci_ei_nor = kg_per_billion(raw_wh(_sci), intensity["NOR"])   # g per million tokens = kg per billion

# AI Energy Score facts (F33)
aies_cross_ratio = aies_heavy5["wh_per_1000_queries"] / aies_light_b["wh_per_1000_queries"]

subs.update({
    # publisher, funding, contact (D1, D10, D13, D16)
    "CONTACT_EMAIL": CONTACT_EMAIL, "CONTACT_LINK": f"<a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>",
    "RESPONSE_DAYS": word(RESPONSE_DAYS), "PUBLISHER_ENTITY": PUBLISHER_ENTITY, "PUBLISHER_REGISTRATION": PUBLISHER_REGISTRATION,
    "PUBLISHER_JURISDICTION": PUBLISHER_JURISDICTION,
    "PUBLISHER_ADDRESS": (esc(PUBLISHER_ADDRESS) if PUBLISHER_ADDRESS else "to be added, word for word from the DIFC registry extract, before launch"),
    "REVIEWERS_PHRASE": (and_list([esc(n) for n in REVIEWERS]) if REVIEWERS else "two named reviewers, listed here before the first contributed row is accepted"),
    "OUTSIDE_REVIEWER_PHRASE": (esc(OUTSIDE_REVIEWER) if OUTSIDE_REVIEWER else "a named reviewer with no Katonic affiliation, to be named here before the first Katonic row is published"),
    "SUBMISSIONS_OPEN_PHRASE": (f"on {long_date(SUBMISSIONS_OPEN)}" if SUBMISSIONS_OPEN else "on a date to be announced on this page"),
    "LEGAL_AS_AT_LONG": long_date(LEGAL_AS_AT), "RETRIEVED_LONG": long_date(RETRIEVED), "DATA_VERSION": DATA_VERSION,
    # sources (D21)
    "MLE_SHORT": f"ML.ENERGY Leaderboard v3.0 (data compiled {long_date(SRC_MLE['compiled'])})",
    "MLE_COMPILED_LONG": long_date(SRC_MLE["compiled"]), "MLE_RELEASED_LONG": long_date(SRC_MLE["released"]),
    "MLE_CITE": SRC_MLE["cite"], "MLE_CITE_URL": SRC_MLE["cite_url"],
    "MLE_BLOCK": (
        f"<a href=\"{SRC_MLE['url']}\">ML.ENERGY Leaderboard</a> version 3.0 (released {long_date(SRC_MLE['released'])}; data compiled "
        f"{long_date(SRC_MLE['compiled'])}; retrieved {long_date(RETRIEVED)}), The ML.ENERGY Initiative, started at SymbioticLab, "
        f"University of Michigan. Text Conversation task, {len(cfgs)} stable configurations. Energy per token is steady-state GPU energy "
        "divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; "
        "energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its "
        f"model and GPU at or under a {ITL_DEADLINE_MS} ms median inter-token latency, the leaderboard's own default ceiling, which no "
        "configuration reaches. Apache 2.0 per the <a href=\"https://huggingface.co/datasets/ml-energy/benchmark-v3\">ml-energy/benchmark-v3</a> "
        f"dataset card. Cite <a href=\"{SRC_MLE['cite_url']}\">Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks</a>."
    ),
    "ATTRIBUTION": esc(ATTRIBUTION), "FUNDING": esc(FUNDING), "LEGAL_NOTE": esc(LEGAL_NOTE),
    # tiles (F10)
    "TILE_LOW_SUB": tile_sub(low), "TILE_HIGH_SUB": tile_sub(high),
    "TILE_REF_SUB": tile_sub(ref, " The carbon table is priced on this row."),
    "REF_RANK": str(ref_rank), "REF_P99": fmt(ref["_cfg"]["p99_itl_ms"], 0), "REF_TPS": fmt(ref["_cfg"]["output_throughput_tokens_per_sec"], 0),
    "MAX_CHAT_ITL": fmt(max_chat_itl, 0), "MAX_GPQA_ITL": fmt(max_gpqa_itl, 0),
    "SENS_SENTENCE": sens_sentence, "PAIR50_SENTENCE": pair50_sentence, "PAIR_SWEEP_SENTENCE": pair_sweep_sentence,
    # ladders (F7)
    **{f"{p}_{k}": v for p, lad in (("L32", l32), ("L8", l8)) for k, v in {
        "COUNT": str(lad["count"]), "COUNT_WORD": word(lad["count"]),
        "FIRST": fmt(lad["first"], 0), "FIRST_CAP": fmt(lad["first_cap"], 0), "FIRST_BATCH": fmt(lad["first_batch"], 0),
        "FIRST_W": fmt(lad["first_w"], 0), "FIRST_TPS": fmt(lad["first_tps"], 0), "FIRST_ITL": fmt(lad["first_itl"], 0),
        "BEST": fmt(lad["best"], 1), "BEST_CAP": fmt(lad["best_cap"], 0), "BEST_BATCH": fmt(lad["best_batch"], 0),
        "BEST_W": fmt(lad["best_w"], 0), "BEST_TPS": fmt(lad["best_tps"], 0), "BEST_ITL": fmt(lad["best_itl"], 0),
        "MAX_ITL": fmt(lad["max_itl_to_best"], 0), "POWER_PCT": fmt(lad["power_pct"], 0), "TPS_RATIO": f"{lad['tps_ratio']:.1f}",
        "RATIO": f"{lad['ratio']:.1f}",
        "TURN_CAP": fmt(lad["turn"]["cap"], 0) if lad["turn"] else "", "TURN_WH": fmt(lad["turn"]["wh"], 1) if lad["turn"] else "",
        "TURN_ITL": fmt(lad["turn"]["itl"], 0) if lad["turn"] else "",
    }.items()},
    # two workloads (F30, D23)
    "GPQA_ROWS": gpqa_table(), "GPQA_TOK_SENTENCE": gpqa_tok_sentence,
    "GPQA_OUTR_MIN": f"{min(p['ratio_out'] for p in gpqa_pairs):.1f}", "GPQA_OUTR_MAX": f"{max(p['ratio_out'] for p in gpqa_pairs):.1f}",
    "GPQA_TOK_MIN": f"{min(p['ratio_tok'] for p in gpqa_pairs):.2f}", "GPQA_TOK_MAX": f"{max(p['ratio_tok'] for p in gpqa_pairs):.2f}",
    # to the meter (D4)
    "SYS_NAME": _sys["system"], "SYS_KW": fmt(_sys["max_power_kw"], 1), "SYS_GPU_COUNT": str(_sys_n), "SYS_GPU_W": f"{_b200_w:,}",
    "SYS_GPU_KW": fmt(gpu_kw_sys, 1), "SYS_RATIO": f"{sys_ratio:.2f}", "PUE_EXAMPLE": f"{PUE_EXAMPLE:g}",
    "METER_WH": fmt(meter_wh, 0), "METER_TOKENS_B": fmt(meter_tokens_b, 1),
    "GOOGLE_WH": f"{GOOGLE_2025['wh']:g}", "GOOGLE_ACCEL_PCT": f"{GOOGLE_2025['accelerator_share'] * 100:.0f}",
    "GOOGLE_NARROW_WH": f"{GOOGLE_2025['narrow_wh']:.2f}", "GOOGLE_G": f"{GOOGLE_2025['g_co2e']:g}", "GOOGLE_ML": f"{GOOGLE_2025['water_ml']:g}",
    "GOOGLE_STACK_LO": f"{1 / GOOGLE_2025['accelerator_share']:.1f}", "GOOGLE_STACK_HI": f"{GOOGLE_2025['wh'] / GOOGLE_2025['narrow_wh']:.1f}",
    "GOOGLE_URL": GOOGLE_2025["url"], "MISTRAL_URL": MISTRAL_2025["url"],
    "MISTRAL_G": f"{MISTRAL_2025['g_co2e']:g}", "MISTRAL_ML": f"{MISTRAL_2025['water_ml']:g}", "MISTRAL_TOKENS": f"{MISTRAL_2025['tokens']:,}",
    # grids (D6, F14)
    "LISTED_GRID_COUNT": str(len(COUNTRIES)), "LISTED_GRID_WORD": word(len(COUNTRIES)),
    "MARKET_GRID_WORD": word(len(COUNTRIES) - len(REFERENCE_GRIDS)), "REFERENCE_GRID_WORD": word(len(REFERENCE_GRIDS)),
    "GRID_MIN_NAME": grid_min["display_name"], "GRID_MIN_G": fmt(intensity[grid_min["iso3"]], 1),
    "GRID_MAX_NAME": grid_max["display_name"], "GRID_MAX_G": fmt(intensity[grid_max["iso3"]], 1),
    "GRID_SPREAD": f"{intensity[grid_max['iso3']] / intensity[grid_min['iso3']]:.1f}",
    "GRID_2025_COUNT": str(grid_2025_count), "GRID_NO_2025": and_list(no_2025_listed),
    "EMBER_BASIS": esc(EMBER_BASIS),
    # SCI (F4)
    "SCI_LIFE_YEARS": str(SCI_LIFE_YEARS), "SCI_G_PER_H": fmt(_sci_g_per_h, 1), "SCI_MODEL": _sci["model"],
    "SCI_GPUS": f"{_sci['num_gpus']} × {_sci['gpu']}", "SCI_MTOK_PER_H": fmt(_sci_mtok_per_h, 1),
    "SCI_M_PER_M": fmt(sci_m_per_m, 1), "SCI_EI_NOR": fmt(sci_ei_nor, 1),
    # AI Energy Score (F9, F27, F28, F33)
    "AIES_ALL_COUNT": str(len(per_query_rows)), "AIES_FIXED_TOKENS": word(AIES_FIXED_TOKENS),
    "AIES_70B_FEB_WH": fmt(aies_70b_feb), "AIES_APERTUS_WH": fmt(aies_apertus),
    **{f"AIES_{cl}_{k}": v for cl, d in aies_class.items() for k, v in {
        "COUNT": str(d["count"]), "LO": fmt(d["lo"]), "HI": fmt(d["hi"]), "FIVE_UP_TO": fmt(d["five_star_up_to"])}.items()},
    "AIES_HEAVY5_MODEL": aies_heavy5["model"], "AIES_HEAVY5_WH": fmt(aies_heavy5["wh_per_1000_queries"]),
    "AIES_LIGHTB_MODEL": aies_light_b["model"], "AIES_LIGHTB_WH": fmt(aies_light_b["wh_per_1000_queries"]),
    "AIES_LIGHTB_STARS": word(aies_light_b["score"]), "AIES_CROSS_RATIO": f"{aies_cross_ratio:.1f}",
})

if os.environ.get("LEADGREEN_REPORT"):
    for k in sorted(subs):
        v = subs[k]
        if len(v) < 400 and "<tr" not in v:
            print(f"{k} = {v}")
    print("API_WH_EDGE", API_WH_EDGE, "REPEATED", sorted(REPEATED), "no_iso2", no_iso2)

# ----------------------------------------------------------------- API documents
ENDPOINTS = [
    ("manifest.json", "Sources, versions, retrieval dates, licences and this endpoint list."),
    ("index.json", f"The index: {len(index_rows)} rows, one per model and GPU, energy-optimal under the latency limit, sorted ascending."),
    ("models.json", "Every model on the index with its slug, Hugging Face id, parameter counts and measured GPUs."),
    ("models/{slug}.json", "One model: every measured configuration (concurrency, parallelism, latency, power) and the best row per GPU."),
    ("grid.json", f"Grid emissions intensity, gCO2e per kWh, {EMBER_YEAR} annual average, {grid_count} countries plus World."),
    ("hardware.json", "Manufacturer power ceilings, memory, MIG slice profiles and one embodied-carbon figure."),
    ("per-query.json", "AI Energy Score text-generation rows, December 2025 round: Wh per 1,000 queries at batch size 1 on H100 80GB GPUs (one card for classes A and B, several for C)."),
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
    "licence": LICENCE_TEXT, "caveat": CAVEAT, "boundary": BOUNDARY,
    "publisher": {"name": "Lead Green", "parent": "Katonic", "url": SITE},
}
api_docs["index.json"] = {
    "version": "1", "updated": UPDATED, "unit": "Wh per million output tokens", "workload": "text-conversation",
    "itl_deadline_ms": ITL_DEADLINE_MS, "selection": "per model and GPU, the configuration with the lowest energy per token whose median inter-token latency does not exceed itl_deadline_ms (the leaderboard's default ceiling; no measured configuration reaches it)",
    "reference_row": {"model": ref["model"], "gpu": ref["gpu"], "num_gpus": ref["num_gpus"]},
    "source": SRC_MLE, "caveat": CAVEAT, "boundary": BOUNDARY, "rows": [{k: v for k, v in r.items() if not k.startswith("_")} for r in index_rows],
}
api_docs["models.json"] = {
    "version": "1", "updated": UPDATED, "source": SRC_MLE,
    "models": [{"slug": m["slug"], "name": m["name"], "model_id": m["model_id"], "params_b": m["params_b"],
                "active_params_b": m["active_params_b"], "gpus": m["gpus"], "url": f"{SITE}/api/v1/models/{m['slug']}.json"}
               for m in sorted(models.values(), key=lambda m: m["name"])],
}
for m in models.values():
    api_docs[f"models/{m['slug']}.json"] = {"version": "1", "updated": UPDATED, "unit": "Wh per million output tokens",
                                            "itl_deadline_ms": ITL_DEADLINE_MS, "source": SRC_MLE, "caveat": CAVEAT, "boundary": BOUNDARY, **m}
api_docs["grid.json"] = {
    "version": "1", "updated": UPDATED, "year": EMBER_YEAR, "unit": "gCO2e per kWh",
    "basis": EMBER_BASIS + " Annual averages: hourly intensity, contracted supply and self-generation are not reflected.",
    "source": SRC_EMBER, "licence": "CC BY 4.0", "world": round(world, 1),
    "note": "Area names are Ember's labels. 'WLD' is used as the code for the World row; Ember gives it none.",
    "areas": areas,
}
api_docs["hardware.json"] = {"version": "1", "updated": UPDATED, **hw}
api_docs["per-query.json"] = {
    "version": "1", "updated": UPDATED, "unit": "Wh per 1,000 queries", "round": "December 2025",
    "setup": ("text generation, 1,000 queries one at a time (batch size 1) on NVIDIA H100 80GB GPUs: one card for class A and B models, "
              "several cards for class C; output length fixed at " + str(AIES_FIXED_TOKENS) + " tokens for non-reasoning runs; the score averages ten passes; GPU energy only"),
    "classes": {"A": "fits one consumer GPU", "B": "fits one H100 (single cloud GPU)", "C": "needs more than one H100 (multiple cloud GPUs)"},
    "score": "1 to 5 stars within a class for this round: the class's energy range is cut into five equal bands and the lowest band is five stars; stars do not compare across classes",
    "note": ("Only the December 2025 round is included: the benchmark harness changed between rounds (Optimum Benchmark in February 2025, "
             "Neuralwatt's AI Energy Benchmarks in December 2025); the project treats watt-hour values as stable across rounds and recalibrates only the stars. "
             "A query is a controlled probe with a fixed ten-token response, not a serving workload, so these values are not converted to Wh per million tokens. "
             "source_label keeps the model string exactly as the source CSV gives it; model carries the clean Hugging Face id."),
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
            "caveat": {"type": "string"}, "boundary": {"type": "string", "enum": ["gpu_only"]}, "rows": {"type": "array", "items": {"$ref": "#/components/schemas/IndexRow"}}}},
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

Key readings (ML.ENERGY Leaderboard v3.0, Text Conversation workload, energy-optimal configuration at or under a {ITL_DEADLINE_MS} ms median inter-token latency, the leaderboard's default ceiling, which no configuration reaches):
- Lowest on the index: {subs['TILE_LOW_WH']} Wh/M ({subs['TILE_LOW_LABEL']})
- Reference row: {subs['REF_WH_1']} Wh/M ({subs['TILE_REF_LABEL']})
- Highest on the index: {subs['TILE_HIGH_WH']} Wh/M ({subs['TILE_HIGH_LABEL']})
- The index spans {subs['SPAN']}x. The same model on the same GPUs moves {subs['LADDER_32_RATIO']}x with concurrency ({subs['LADDER_32_FIRST']} to {subs['LADDER_32_LAST']} Wh/M for Qwen 3 32B on 2 x H100, running batch {subs['LADDER_32_FIRST_BATCH']} to {subs['LADDER_32_LAST_BATCH']}). Running batch = the average number of requests the server was decoding at once (vLLM num_requests_running); queued requests are not counted.
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
def sync_tree(src: Path, dst: Path, skip: tuple[str, ...] = ()) -> None:
    """Make dst an exact copy of src, updating in place. rmtree then copytree
    fails inside OneDrive, which keeps handles on emptied folders."""
    keep = set()
    for p in sorted(src.rglob("*")):
        rel = p.relative_to(src)
        if rel.parts and rel.parts[0] in skip:
            continue
        keep.add(rel)
        q = dst / rel
        if p.is_dir():
            q.mkdir(parents=True, exist_ok=True)
        else:
            q.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(p, q)
    for q in sorted(dst.rglob("*"), key=lambda x: len(x.parts), reverse=True):
        if q.relative_to(dst) in keep:
            continue
        if q.is_dir():
            try:
                q.rmdir()
            except OSError:
                pass
        else:
            q.unlink()


sync_tree(API_DIR, MCP_DATA)

wheel = ROOT / "dist" / WHEEL_NAME
print(f"wrote {len(outputs)} pages/files and {len(api_docs)} API documents; {len(index_rows)} index rows from {len(cfgs)} configurations; "
      f"{grid_count} grids; {len(posts)} posts; reference {ref['model']} {ref['num_gpus']}x{ref['gpu']} = {ref_wh:.1f} Wh/M")
if not wheel.exists():
    print(f"NOTE: {wheel.relative_to(ROOT)} is missing; the MCP page's install line points at it. "
          f"Build it with: python -m pip wheel ./leadgreen-mcp -w dist --no-deps")
