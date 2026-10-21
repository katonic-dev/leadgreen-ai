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
import io
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
UPDATED = "2026-10-19"                 # bump on every data or content change
DATA_VERSION = UPDATED                 # D20: carried by every API document; a published release never changes
RETRIEVED = "2026-09-26"               # when the ML.ENERGY, AI Energy Score and NVIDIA snapshots in build/data were retrieved; not the same as UPDATED
EMBER_RETRIEVED = "2026-10-17"         # the Ember snapshot is refreshed on its own: Ember re-issues the yearly file monthly
EMBER_RELEASE = "October 2026 release" # Ember's own label for the file, as shown on every page that cites it
INDEX_NAME = "Green Tokens"            # D1: "Green Tokens" or "The Green Token Index"
EDITOR = "Prem Naraindas"
LINKEDIN_URL = "https://www.linkedin.com/in/premnaraindas/"
OWN_YOUR_AI_URL = "https://www.linkedin.com/newsletters/own-your-ai-7508174547041292288/"
# D6 / G2 / T6: REPO_URL (the public mirror), the Hugging Face and Zenodo identifiers, the canonical description and the funder line
# live in build/project_text.py, shared with hf_dataset.py. "" for REPO_URL omits the repository links.
from project_text import FUNDING, HF_DATASET_URL, PROJECT_DESCRIPTION, REPO_URL, SAME_AS, WIKIDATA_URL, ZENODO_CONCEPT_DOI, ZENODO_DOI_URL  # noqa: E402
NEWSLETTER_SIGNUP_URL = ""             # D2: set when the email provider is chosen; never a fake form
MCP_VERSION = "0.3.1"
WHEEL_NAME = f"leadgreen_mcp-{MCP_VERSION}-py3-none-any.whl"
WHEEL_URL = f"{SITE}/dist/{WHEEL_NAME}"
_wheel_file = Path(__file__).resolve().parent.parent / "dist" / WHEEL_NAME   # theme 10: the install line carries the wheel hash
WHEEL_SHA256 = hashlib.sha256(_wheel_file.read_bytes()).hexdigest() if _wheel_file.exists() else ""
WHEEL_BUILD_DATE = "2026-10-20"        # the wheel is built with SOURCE_DATE_EPOCH = this date 00:00 UTC so it reproduces byte for byte; launch.py sets it to the release date when it rebuilds the wheel
WHEEL_EPOCH = int(datetime.strptime(WHEEL_BUILD_DATE, "%Y-%m-%d").replace(tzinfo=timezone.utc).timestamp())
PYPI_URL = "https://pypi.org/project/leadgreen-mcp/"   # T4: set 20 October 2026, once 0.3.0 landed on PyPI (run 39450980200 on the mirror)
# D16 publisher block. The address is typed only from the DIFC registry extract, after Prem confirms it.
PUBLISHER_ENTITY = "Katonic AI Technology Ltd"
PUBLISHER_REGISTRATION = "CL9944"
PUBLISHER_JURISDICTION = "Dubai International Financial Centre (DIFC), United Arab Emirates"
PUBLISHER_ADDRESS = "Unit IH-00-VZ-01-FL-194, Level 1, Innovation Hub, Dubai International Financial Centre, Dubai, United Arab Emirates"   # D16: registered office, confirmed by Prem 18 October 2026
CONTACT_EMAIL = "hello@leadgreen.ai"   # D16: forwarded to the editor; mail on the domain must work before launch
RESPONSE_DAYS = 10                     # working days, for corrections and contributions
REVIEWERS: list[str] = []              # D1 OWED: the two named reviewers
OUTSIDE_REVIEWER = ""                  # D1 OWED: the reviewer with no Katonic affiliation who checks any Katonic row
SUBMISSIONS_OPEN = ""                  # D19: date contributed rows open while the repository is not public; "" = to be announced
MLE_LICENCE_CONFIRMED = False          # D17: True once the ML.ENERGY team confirms the leaderboard JSON is Apache 2.0
LEGAL_AS_AT = "2026-09-27"             # D15: the date the regulatory summaries were checked

MLE_CHAT = DATA / "mlenergy-v3-lm-arena-chat-2026-09-26.json"
MLE_GPQA = DATA / "mlenergy-v3-gpqa-2026-09-26.json"
EMBER = DATA / "ember-yearly-total-generation-extract-2026-10-17.csv"
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
LED_W = 10                           # stated assumption in the per-answer illustration (a 10 W LED bulb)
PROTO_MIN_MINUTES = 5                # protocol: steady-state window at least this long after warm-up
PROTO_MIN_REQUESTS = 1000            # protocol: at least this many requests in the window
REPEAT_THRESHOLD_PCT = 5             # protocol: two runs further apart than this need a reason or a third run
PAGES_MAX_AGE_S = 600               # D20: GitHub Pages Cache-Control max-age, checked 26 Sep 2026
PAGES_BANDWIDTH_GB = 100            # D20: GitHub Pages soft bandwidth limit per month
REVIEW_DECISION_DAYS = 30           # D19: a decision on a contributed row within this many days
MLE_PROMPT_REQUESTS = 1024          # D19: the benchmark's request count (run doc: --workload.num-requests 1024)
MLE_MAX_BATCHED_TOKENS = 8192       # D19: the benchmark's vLLM flags
MLE_MAX_MODEL_LEN = 20480
PROTOCOL_VERSION = "0.2"
CHALLENGE_TOLERANCE_PCT = 10         # D12: an answer this far below the floor is challenged
EED_MIN_KW = 500                     # D7: Delegated Regulation (EU) 2024/1364, Article 1: installed IT power demand of at least 500 kW
GPAI_MODIFY_SHARE = "a third"        # D7: Commission GPAI guidelines, July 2025: a modifier becomes a provider above about a third of the original training compute
PUE_EXAMPLE = 1.3                    # D4: stated assumption in the to-the-meter illustration (PUE is the operator's own figure)
SCI_LIFE_YEARS = 5                   # stated assumption in the SCI illustration (hardware life over which M is amortised)
AIES_FIXED_TOKENS = 10               # AI Energy Score protocol: ten generated tokens for non-reasoning runs (reasoning_helpers.py)
# Published per-prompt figures, cited on the site (F2, D4, D9). Neither is Wh per million output tokens at a stated load.
GOOGLE_2025 = {"date": "August 2025", "wh": 0.24, "accelerator_share": 0.58, "narrow_wh": 0.10, "g_co2e": 0.03,
               "water_ml": 0.26, "url": "https://arxiv.org/abs/2508.15734"}
# Two more published whole-stack per-query figures, cited on the per-query page beside Google's (GEO baseline, 21 October 2026).
EPOCH_2025 = {"date": "February 2025", "wh": 0.3, "tokens": 500, "url": "https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use"}
ALTMAN_2025 = {"date": "June 2025", "wh": 0.34, "url": "https://blog.samaltman.com/the-gentle-singularity"}
WHOLE_STACK_LO = min(0.24, EPOCH_2025["wh"], ALTMAN_2025["wh"])   # 0.24 is GOOGLE_2025["wh"], defined above
WHOLE_STACK_HI = max(0.24, EPOCH_2025["wh"], ALTMAN_2025["wh"])
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
    "version": f"{EMBER_RELEASE} (file last modified 2026-10-06)",
    "retrieved": EMBER_RETRIEVED,
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
NVIDIA_LABEL = "manufacturer specifications transcribed as facts; NVIDIA retains its rights in the source documents"
PUBLISHED_RELEASES = DATA / "published-releases.txt"   # D16: dates listed here are frozen; the build refuses to change them
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
            f"<th scope=\"row\"><a class=\"model\" href=\"{{{{ROOT}}}}models/{r['slug']}/\" title=\"{esc(r['model_id'])}\">{esc(r['model'])}</a></th>"
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


LADDER_MID_CAP = 64   # the row the concurrency post reads as 'a modest load': most of the drop is in by here


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
    mid = next((c for c in rows if c["max_num_seqs"] == LADDER_MID_CAP and c is not best_c), None)
    first_wh, best_wh = wh_per_million(first["energy_per_token_joules"]), wh_per_million(best_c["energy_per_token_joules"])
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
        "first_batch": first["avg_batch_size"], "best_batch": best_c["avg_batch_size"], "first_out": first["avg_output_len"],
        "first_cap": first["max_num_seqs"], "best_cap": best_c["max_num_seqs"],
        # aliases kept while pages still say "last": the last row the old pages showed was the best row
        "last": wh_per_million(best_c["energy_per_token_joules"]), "last_w": best_c["avg_power_watts"],
        "last_itl": best_c["median_itl_ms"], "last_tps": best_c["output_throughput_tokens_per_sec"],
        "last_batch": best_c["avg_batch_size"],
        "turn": None if turn is None else {
            "cap": turn["max_num_seqs"], "wh": wh_per_million(turn["energy_per_token_joules"]),
            "itl": turn["median_itl_ms"], "batch": turn["avg_batch_size"], "p99": turn["p99_itl_ms"]},
        "first_p99": first["p99_itl_ms"], "best_p99": best_c["p99_itl_ms"],
        "model": name, "gpus": f"{num_gpus} × {gpu}", "precision": precision_label(first["weight_precision"]),
        # GPU-hours per million output tokens: cards x seconds per million tokens / 3,600
        "first_gpuh": num_gpus * 1e6 / first["output_throughput_tokens_per_sec"] / 3600,
        "best_gpuh": num_gpus * 1e6 / best_c["output_throughput_tokens_per_sec"] / 3600,
        "mid": None if mid is None else {
            "cap": mid["max_num_seqs"], "batch": mid["avg_batch_size"], "wh": wh_per_million(mid["energy_per_token_joules"]),
            "itl": mid["median_itl_ms"], "w": mid["avg_power_watts"],
            "ratio": first["energy_per_token_joules"] / mid["energy_per_token_joules"],
            # share of the whole first-to-best drop already achieved at the mid row
            "drop_pct": (first_wh - wh_per_million(mid["energy_per_token_joules"])) / (first_wh - best_wh) * 100},
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
assert l32["mid"] and l32["turn"] and l8["mid"] and l8["turn"], "an exhibit ladder lost its cap-64 or past-best row; the concurrency post reads both"
# D18: the public comparators for the two MIG measurements (1 x H100, BF16)
_q14 = sorted((c for c in cfgs if c["nickname"] == "Qwen 3 14B" and c["gpu_model"] == "H100" and c["num_gpus"] == 1), key=lambda c: c["max_num_seqs"])
_q32 = sorted((c for c in cfgs if c["nickname"] == "Qwen 3 32B" and c["gpu_model"] == "H100" and c["num_gpus"] == 1), key=lambda c: c["max_num_seqs"])
assert _q14 and _q32
_hicfg = max(cfgs, key=lambda c: c["energy_per_token_joules"])   # the highest measured configuration, above every index row

# ----------------------------------------------------------------- D19: contributed measurements
MEAS_SCHEMA = json.loads(MEASUREMENT_SCHEMA.read_text(encoding="utf-8"))
_JTYPES = {"string": str, "integer": int, "number": (int, float), "boolean": bool, "object": dict, "array": list, "null": type(None)}


def _check(v, sch: dict, path: str, errs: list) -> None:
    """The subset of JSON Schema the measurement schema uses: type, enum, minimum, exclusiveMinimum,
    required, properties, additionalProperties false, items, minItems."""
    t = sch.get("type")
    if t:
        ts = t if isinstance(t, list) else [t]
        if not any(isinstance(v, _JTYPES[x]) and not (x in ("integer", "number") and isinstance(v, bool)) for x in ts):
            errs.append(f"{path}: expected {t}, got {type(v).__name__}")
            return
    if "enum" in sch and v not in sch["enum"]:
        errs.append(f"{path}: {v!r} is not one of {sch['enum']}")
    if isinstance(v, (int, float)) and not isinstance(v, bool):
        if "minimum" in sch and v < sch["minimum"]:
            errs.append(f"{path}: below {sch['minimum']}")
        if "exclusiveMinimum" in sch and v <= sch["exclusiveMinimum"]:
            errs.append(f"{path}: must be above {sch['exclusiveMinimum']}")
    if isinstance(v, dict):
        for k in sch.get("required", []):
            if k not in v:
                errs.append(f"{path}.{k}: required")
        props = sch.get("properties", {})
        for k, x in v.items():
            if k in props:
                _check(x, props[k], f"{path}.{k}", errs)
            elif sch.get("additionalProperties") is False:
                errs.append(f"{path}.{k}: not in the schema")
    if isinstance(v, list):
        if len(v) < sch.get("minItems", 0):
            errs.append(f"{path}: needs at least {sch['minItems']} items")
        if "items" in sch:
            for i, x in enumerate(v):
                _check(x, sch["items"], f"{path}[{i}]", errs)


measurement_rows: list[dict] = []
_meas_errs: list[str] = []
for mp in sorted(MEASUREMENTS.glob("*.json")) if MEASUREMENTS.exists() else []:
    m = json.loads(mp.read_text(encoding="utf-8"))
    errs: list[str] = []
    _check(m, MEAS_SCHEMA, mp.name, errs)
    if not errs:   # the rules a schema cannot state
        if abs(m["joules_per_output_token"] * 1_000_000 / 3600 - m["wh_per_million_output_tokens"]) > 0.01:
            errs.append(f"{mp.name}: wh_per_million_output_tokens is not joules_per_output_token x 1,000,000 / 3,600")
        if (m["mig_profile"] is None) != (m["slice_count"] is None) or m["slices_loaded"] != m["slice_count"]:
            errs.append(f"{mp.name}: a sliced row needs mig_profile, slice_count and slices_loaded, with every slice loaded")
        _runs = [r["joules_per_output_token"] for r in m["runs"]]
        if abs(sum(_runs) / len(_runs) - m["joules_per_output_token"]) > 1e-6:
            errs.append(f"{mp.name}: joules_per_output_token is not the mean of the runs")
        if (max(_runs) / min(_runs) - 1) * 100 > REPEAT_THRESHOLD_PCT and not m["notes"].strip():
            errs.append(f"{mp.name}: runs differ by more than {REPEAT_THRESHOLD_PCT} percent and the notes give no reason")
        if not mp.name.startswith(m["measured_on"]):
            errs.append(f"{mp.name}: file name must start with measured_on")
    _meas_errs += errs
    if not errs and not m["example"]:
        measurement_rows.append({**m, "source_file": mp.name, "comparable": m["median_itl_ms"] <= ITL_DEADLINE_MS})
if _meas_errs:
    sys.exit("REFUSING TO BUILD, contributed measurements fail the schema:\n  " + "\n  ".join(_meas_errs))


def _contributed_table() -> str:
    if not measurement_rows:
        return "<p class=\"lead\">None yet.</p>"
    out = ["<div class=\"table-scroll\"><table><caption>Contributed measurements, protocol v" + PROTOCOL_VERSION + "</caption>",
           "<thead><tr><th scope=\"col\">Model</th><th scope=\"col\" class=\"num\">GPUs</th><th scope=\"col\" class=\"num\">Wh / M</th>"
           "<th scope=\"col\" class=\"num\">Median ITL (ms)</th><th scope=\"col\" class=\"num\">Running batch (avg)</th><th scope=\"col\">Contributor</th></tr></thead><tbody>"]
    for r in sorted(measurement_rows, key=lambda r: r["wh_per_million_output_tokens"]):
        gpus = f"{r['num_gpus']} × {esc(r['gpu'])}" + (f", {r['slices_loaded']} × {esc(r['mig_profile'])}" if r["mig_profile"] else "")
        flag = "" if r["comparable"] else f" <span class=\"muted\">(above {ITL_DEADLINE_MS} ms)</span>"
        out.append(f"<tr><th scope=\"row\">{esc(r['model'])}, {r['precision']}</th><td class=\"num\">{gpus}</td>"
                   f"<td class=\"num key\">{fmt(r['wh_per_million_output_tokens'])}</td><td class=\"num\">{fmt(r['median_itl_ms'], 0)}{flag}</td>"
                   f"<td class=\"num\">{fmt(r['avg_running_batch'], 0)}</td><td>{esc(r['contributor'])}, {r['measured_on']}</td></tr>")
    out.append("</tbody></table></div>")
    return "\n".join(out)


contributed_html = _contributed_table()
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
    "WHEEL_URL": WHEEL_URL, "WHEEL_NAME": WHEEL_NAME, "MCP_VERSION": MCP_VERSION, "WHEEL_EPOCH": str(WHEEL_EPOCH),
    "REPO_LINK": (f"<a href=\"{REPO_URL}\">the repository</a>" if REPO_URL else "the repository (link to follow once it is public)"),
    "REPO_LINK_CAP": (f"<a href=\"{REPO_URL}\">The repository</a>" if REPO_URL else "The repository (link to follow once it is public)"),
    # the MCP worked example reproduces what the tool returns, so it uses the API's two-decimal values
    "EST_50M_WH": fmt(ref_wh_api * 50, 1), "EST_50M_KWH": fmt(ref_wh_api * 50 / 1000, 4),
    "EST_50M_KG_SRB": fmt(ref_wh_api * 50 / 1000 * round(intensity["SRB"], 1) / 1000, 2),
    # T4: once PYPI_URL is set the one-line install is the package; until then the public source, then the wheel
    "REPO_INSTALL": ("pip install leadgreen-mcp" if PYPI_URL else
                     f"pip install \"git+{REPO_URL}#subdirectory=leadgreen-mcp\"" if REPO_URL else
                     f"pip install {WHEEL_URL}#sha256={WHEEL_SHA256}" if WHEEL_SHA256 else f"pip install {WHEEL_URL}"),
    "WHEEL_SHA256": WHEEL_SHA256 or "not built yet",
    "REPO_UVX": ("uvx leadgreen-mcp" if PYPI_URL else
                 f"uvx --from \"git+{REPO_URL}#subdirectory=leadgreen-mcp\" leadgreen-mcp" if REPO_URL else f"uvx --from {WHEEL_URL} leadgreen-mcp"),
    "PYPI_LINE": (f"<div class=\"prose\"><p>The package is <a href=\"{PYPI_URL}\">leadgreen-mcp on PyPI</a>"
                  + (f"; the source installs with <code>pip install \"git+{REPO_URL}#subdirectory=leadgreen-mcp\"</code>" if REPO_URL else "")
                  + ".</p></div>" if PYPI_URL else ""),
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
PAIR50_MS = 50   # the tighter ceiling the two-generations comparison is re-cut at
_b50 = best_by_model_gpu(cfgs, PAIR50_MS)
_both50 = sorted({k[0] for k in _b50 if (k[0], "H100") in _b50 and (k[0], "B200") in _b50})
_hwins = [(m, _b50[(m, "H100")], _b50[(m, "B200")]) for m in _both50
          if _b50[(m, "H100")]["energy_per_token_joules"] < _b50[(m, "B200")]["energy_per_token_joules"]]
pair50_sentence = (
    f"At a {PAIR50_MS} ms ceiling the comparison shifts: {len(_both50)} models still have a row on both cards, and the H100 uses less "
    f"energy per token than the B200 on {word(len(_hwins))} of them ("
    + "; ".join(f"{m}, {fmt(cfg_wh(h))} Wh/M on {h['num_gpus']} × H100 against {fmt(cfg_wh(b))} on {b['num_gpus']} × B200"
                for m, h, b in _hwins) + ")."
) if _hwins else f"At a {PAIR50_MS} ms ceiling, {len(_both50)} models still have a row on both cards, and the B200 stays ahead on every one."

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

# blog post 4 (H100 against B200): the figures compare_page() derives, exposed for prose
_pair_ratios = sorted(r for *_, r in pairs)
_pair_med = (_pair_ratios[len(_pair_ratios) // 2] if len(_pair_ratios) % 2
             else (_pair_ratios[len(_pair_ratios) // 2 - 1] + _pair_ratios[len(_pair_ratios) // 2]) / 2)
_pair_wins = sum(1 for r in _pair_ratios if r > 1)
_lm, _lh, _lb, _lratio = pairs[-1]
_pair_fewer = sum(1 for _, h, b, _ in pairs if b["num_gpus"] < h["num_gpus"])
_pair_h100_w = sum(h["_cfg"]["avg_power_watts"] / h["num_gpus"] for _, h, _, _ in pairs) / len(pairs)
_pair_b200_w = sum(b["_cfg"]["avg_power_watts"] / b["num_gpus"] for _, _, b, _ in pairs) / len(pairs)   # measured, per card; not the TDP
_tdp_by = {(t["gpu"], t["form"]): t for t in hw["tdp"]}
_ref_pair = next((h, b, r) for m, h, b, r in pairs if m == ref["model"])   # the reference model must have both rows
_by_gpu: dict[str, set] = {}
for _r in index_rows:
    _by_gpu.setdefault(_r["model"], set()).add(_r["gpu"])
_h100_only = sorted(m for m, g in _by_gpu.items() if g == {"H100"})
_b200_only = sorted(m for m, g in _by_gpu.items() if g == {"B200"})
_pair50_clause = ((f"the H100 comes out ahead on {word(len(_hwins))} of them: "
                   + "; ".join(f"{m}, {fmt(cfg_wh(h))} Wh/M on {h['num_gpus']} \u00d7 H100 against {fmt(cfg_wh(b))} on {b['num_gpus']} \u00d7 B200"
                               for m, h, b in _hwins))
                  if _hwins else "the B200 stays ahead on every one")
_nemo_note = ((f"At the other end, the {word(len(_nemo_pairs))} Nemotron pairs compare runs whose answers were "
               + and_list([f"{b['avg_output_len'] / h['avg_output_len']:.1f}" for _, h, b in _nemo_pairs])
               + " times longer on the B200, which is a different workload wearing the same name.")
              if _nemo_pairs else "")

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
    "PUBLISHER_JURISDICTION": PUBLISHER_JURISDICTION, "RELEASES_URL": f"{SITE}/api/v1/releases/",
    # D13: the recusal reads as the dated-release rule alone until the outside reviewer is named
    "MLE_LICENCE_SENTENCE": ("Apache 2.0 per its dataset card, confirmed by the ML.ENERGY team for the leaderboard files." if MLE_LICENCE_CONFIRMED else
        "The leaderboard repository the JSON comes from carries no licence file; the benchmark data is published under Apache 2.0 on the "
        "dataset card and in the NeurIPS 2025 paper, and the JSON is reproduced here as published measurements on that basis while the "
        "ML.ENERGY team is asked to confirm that the licence covers it."),
    "Q14_FIRST_WH": fmt(cfg_wh(_q14[0])), "Q14_FIRST_CAP": fmt(_q14[0]["max_num_seqs"], 0),
    "Q14_LAST_WH": fmt(cfg_wh(_q14[-1])), "Q14_LAST_CAP": fmt(_q14[-1]["max_num_seqs"], 0),
    "Q32_1GPU_WH_LIST": and_list([fmt(cfg_wh(c)) for c in _q32]),
    "REVIEW_DECISION_DAYS": str(REVIEW_DECISION_DAYS), "MLE_PROMPT_REQUESTS": fmt(MLE_PROMPT_REQUESTS, 0),
    "MLE_MAX_BATCHED_TOKENS": str(MLE_MAX_BATCHED_TOKENS), "MLE_MAX_MODEL_LEN": str(MLE_MAX_MODEL_LEN), "PROTOCOL_VERSION": PROTOCOL_VERSION,
    "MEASUREMENT_COUNT": str(len(measurement_rows)), "CONTRIBUTED_ROWS": contributed_html,
    # per-answer figures for the blog (energy for one answer of the row's own average output length)
    "REF_OUT_TOKENS": fmt(ref["_cfg"]["avg_output_len"], 0),
    "REF_WH_PER_ANSWER": f"{cfg_wh(ref['_cfg']) * ref['_cfg']['avg_output_len'] / 1e6:.3f}",
    "REF_ANSWERS_PER_KWH": fmt(round(1000 / (cfg_wh(ref["_cfg"]) * ref["_cfg"]["avg_output_len"] / 1e6), -2), 0),
    "REF_ANSWER_LED_SECONDS": fmt(cfg_wh(ref["_cfg"]) * ref["_cfg"]["avg_output_len"] / 1e6 / LED_W * 3600, 0), "LED_W": str(LED_W),
    "L32_FIRST_WH_PER_ANSWER": f"{l32['first'] * l32['first_out'] / 1e6:.2f}",
    "GOOGLE_ACCEL_WH": f"{GOOGLE_2025['wh'] * GOOGLE_2025['accelerator_share']:.2f}",
    "GOOGLE_VS_REF": f"{GOOGLE_2025['wh'] / (cfg_wh(ref['_cfg']) * ref['_cfg']['avg_output_len'] / 1e6):.0f}",
    "GOOGLE_ACCEL_VS_REF": f"{GOOGLE_2025['wh'] * GOOGLE_2025['accelerator_share'] / (cfg_wh(ref['_cfg']) * ref['_cfg']['avg_output_len'] / 1e6):.1f}",
    "HIGHEST_CFG_MODEL": _hicfg["nickname"], "HIGHEST_CFG_GPUS": f"{_hicfg['num_gpus']} × {_hicfg['gpu_model']}", "HIGHEST_CFG_BATCH": fmt(_hicfg["avg_batch_size"], 0),
    "HIGHEST_CFG_WH": fmt(cfg_wh(_hicfg), 0), "HIGHEST_CFG_WH_PER_ANSWER": f"{cfg_wh(_hicfg) * _hicfg['avg_output_len'] / 1e6:.1f}",
    "HIGHEST_CFG_VS_TILE": f"{cfg_wh(_hicfg) / raw_wh(high):.1f}", "LOW_OUT_TOKENS": fmt(low["_cfg"]["avg_output_len"], 0),
    "LOW_WH_PER_ANSWER": f"{raw_wh(low) * low['_cfg']['avg_output_len'] / 1e6:.3f}",
    # joules per token at the ends of the index, for the unit explainer
    "LOW_J": f"{low['_cfg']['energy_per_token_joules']:.3f}", "HIGH_J": f"{high['_cfg']['energy_per_token_joules']:.2f}",
    "REF_J_PER_ANSWER": fmt(ref["_cfg"]["energy_per_request_joules"], 0),
    "RECUSAL": (f"While Katonic is a bidder in a tender that cites the index, the editor changes no row for a model Katonic proposes. "
                f"Rows change only when a source publishes a dated release, and those changes are applied by {esc(OUTSIDE_REVIEWER)}, "
                "who has no Katonic affiliation. " if OUTSIDE_REVIEWER else
                "While Katonic is a bidder in a tender that cites the index, rows change only when a source publishes a dated release. ")
               + f"Tenders cite a dated release, kept at <code>{SITE}/api/v1/releases/&lt;date&gt;/</code>, so no later change can move a cited figure.",
    "CITE_AS": (f"Lead Green, a Katonic project. {INDEX_NAME}: GPU energy per million output tokens. {SITE}/index/, release {DATA_VERSION}, "
                f"retrieved [date]. © 2026 {esc(PUBLISHER_ENTITY)}. Licensed <a href=\"https://creativecommons.org/licenses/by/4.0/\">CC BY 4.0</a>, "
                "offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 "
                "(The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, "
                f"NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, {EMBER_RELEASE} (CC BY 4.0); "
                "AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced "
                "as facts from the documents named in the sources ledger."),
    "PUBLISHER_ADDRESS": (esc(PUBLISHER_ADDRESS) if PUBLISHER_ADDRESS else "to be added, word for word from the DIFC registry extract, before launch"),
    "REVIEWED_LINE": (f" Reviewed by {and_list([esc(n) for n in REVIEWERS])}; recomputed from the snapshots." if REVIEWERS else ""),
    "REVIEWERS_PHRASE": (and_list([esc(n) for n in REVIEWERS]) if REVIEWERS else "two named reviewers, listed here before the first contributed row is accepted"),
    "OUTSIDE_REVIEWER_PHRASE": (esc(OUTSIDE_REVIEWER) if OUTSIDE_REVIEWER else "a named reviewer with no Katonic affiliation, to be named here before the first Katonic row is published"),
    "SUBMISSIONS_OPEN_PHRASE": (f"on {long_date(SUBMISSIONS_OPEN)}" if SUBMISSIONS_OPEN else "on a date to be announced on this page"),
    "SUBMISSIONS_SENTENCE": (
        f"If you would rather not open a pull request, send a measurement or a correction to <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>; it will be added under your name."
        if REPO_URL else
        f"The repository opens {f'on {long_date(SUBMISSIONS_OPEN)}' if SUBMISSIONS_OPEN else 'on a date to be announced on this page'}. "
        f"Until then, send a measurement or a correction to <a href=\"mailto:{CONTACT_EMAIL}\">{CONTACT_EMAIL}</a>; it will be moved into the repository under your name when the repository opens."),
    "LEGAL_AS_AT_LONG": long_date(LEGAL_AS_AT), "RETRIEVED_LONG": long_date(RETRIEVED), "DATA_VERSION": DATA_VERSION,
    "EMBER_RELEASE": EMBER_RELEASE, "EMBER_RETRIEVED_LONG": long_date(EMBER_RETRIEVED),
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
    # blog post 4 (H100 against B200)
    "PAIR_MEDIAN": f"{_pair_med:.2f}",
    "PAIR_WINS_PHRASE": ("all " + str(len(pairs))) if _pair_wins == len(pairs) else f"{_pair_wins} of the {len(pairs)}",
    "PAIR_MAX_H_CARDS": word(_ph["num_gpus"]), "PAIR_MAX_H_WH": fmt(raw_wh(_ph)), "PAIR_MAX_H_BATCH": fmt(_hc["avg_batch_size"], 0),
    "PAIR_MAX_B_CARDS": word(_pb["num_gpus"]), "PAIR_MAX_B_WH": fmt(raw_wh(_pb)), "PAIR_MAX_B_BATCH": fmt(_bc["avg_batch_size"], 0),
    "PAIR_MAX_H_SWEEP": _sweep_phrase, "PAIR_MATCH_CAP": f"{_hc['max_num_seqs']:,}",
    "PAIR_MATCH_B_WH": fmt(cfg_wh(_mc)), "PAIR_MATCH_H_WH": fmt(cfg_wh(_hc)), "PAIR_MATCH_RATIO": f"{_match_ratio:.2f}",
    "PAIR_MIN_H_CARDS": word(_lh["num_gpus"]), "PAIR_MIN_H_WH": fmt(raw_wh(_lh)), "PAIR_MIN_B_CARDS": word(_lb["num_gpus"]), "PAIR_MIN_B_WH": fmt(raw_wh(_lb)),
    "PAIR_FEWER_WORD": word(_pair_fewer), "PAIR_SAME_WORD": word(len(pairs) - _pair_fewer),
    "H100_AVG_W": fmt(_pair_h100_w, 0), "B200_AVG_W": fmt(_pair_b200_w, 0),
    "H100_TDP_LABEL": _tdp_by[("H100", "SXM")]["tdp_label"], "B200_TDP_LABEL": next(t for t in hw["tdp"] if t["gpu"] == "B200")["tdp_label"],
    "PAIR50_MS": str(PAIR50_MS), "PAIR50_COUNT": str(len(_both50)), "PAIR50_CLAUSE": _pair50_clause, "NEMO_NOTE": _nemo_note,
    "REF_B200_CARDS_WORD": word(_ref_pair[1]["num_gpus"]), "REF_B200_WH": fmt(raw_wh(_ref_pair[1])), "REF_PAIR_RATIO": f"{_ref_pair[2]:.2f}",
    "REF_PAIR_H_GPUH": f"{_ref_pair[0]['num_gpus'] * 1e6 / _ref_pair[0]['_cfg']['output_throughput_tokens_per_sec'] / 3600:.2f}",
    "REF_PAIR_B_GPUH": f"{_ref_pair[1]['num_gpus'] * 1e6 / _ref_pair[1]['_cfg']['output_throughput_tokens_per_sec'] / 3600:.2f}",
    "GPU_LIST": and_list(sorted({c["gpu_model"] for c in cfgs})),
    "H100_ONLY_WORD": word(len(_h100_only)), "H100_ONLY_LIST": and_list(_h100_only),
    "B200_ONLY_WORD": word(len(_b200_only)), "B200_ONLY_LIST": and_list(_b200_only),
    # ladders (F7)
    **{f"{p}_{k}": v for p, lad in (("L32", l32), ("L8", l8)) for k, v in {
        "COUNT": str(lad["count"]), "COUNT_WORD": word(lad["count"]),
        "FIRST": fmt(lad["first"], 0), "FIRST_CAP": fmt(lad["first_cap"], 0), "FIRST_BATCH": fmt(lad["first_batch"], 0),
        "FIRST_W": fmt(lad["first_w"], 0), "FIRST_TPS": fmt(lad["first_tps"], 0), "FIRST_ITL": fmt(lad["first_itl"], 0),
        "BEST": fmt(lad["best"], 1), "BEST_CAP": fmt(lad["best_cap"], 0), "BEST_BATCH": fmt(lad["best_batch"], 0),
        "BEST_W": fmt(lad["best_w"], 0), "BEST_TPS": fmt(lad["best_tps"], 0), "BEST_ITL": fmt(lad["best_itl"], 0),
        "MAX_ITL": fmt(lad["max_itl_to_best"], 0), "POWER_PCT": fmt(lad["power_pct"], 0), "TPS_RATIO": f"{lad['tps_ratio']:.1f}",
        "RATIO": f"{lad['ratio']:.1f}",
        # blog post 3 (the concurrency ladder)
        "MODEL": lad["model"], "GPUS": lad["gpus"], "PRECISION": lad["precision"],
        "FIRST_P99": fmt(lad["first_p99"], 0), "BEST_P99": fmt(lad["best_p99"], 0),
        "FIRST_GPUH": f"{lad['first_gpuh']:.2f}", "BEST_GPUH": f"{lad['best_gpuh']:.2f}",
        "TURN_BATCH": fmt(lad["turn"]["batch"], 0) if lad["turn"] else "", "TURN_P99": fmt(lad["turn"]["p99"], 0) if lad["turn"] else "",
        "MID_CAP": fmt(lad["mid"]["cap"], 0) if lad["mid"] else "", "MID_BATCH": fmt(lad["mid"]["batch"], 0) if lad["mid"] else "",
        "MID_WH": fmt(lad["mid"]["wh"], 1) if lad["mid"] else "", "MID_ITL": fmt(lad["mid"]["itl"], 0) if lad["mid"] else "",
        "MID_W": fmt(lad["mid"]["w"], 0) if lad["mid"] else "", "MID_RATIO": f"{lad['mid']['ratio']:.1f}" if lad["mid"] else "",
        "MID_DROP_PCT": fmt(lad["mid"]["drop_pct"], 0) if lad["mid"] else "",
        "TURN_CAP": fmt(lad["turn"]["cap"], 0) if lad["turn"] else "", "TURN_WH": fmt(lad["turn"]["wh"], 1) if lad["turn"] else "",
        "TURN_ITL": fmt(lad["turn"]["itl"], 0) if lad["turn"] else "",
    }.items()},
    # two workloads (F30, D23)
    "GPQA_ROWS": gpqa_table(), "GPQA_TOK_SENTENCE": gpqa_tok_sentence,
    "GPQA_OUTR_MIN": f"{min(p['ratio_out'] for p in gpqa_pairs):.1f}", "GPQA_OUTR_MAX": f"{max(p['ratio_out'] for p in gpqa_pairs):.1f}",
    "GPQA_TOK_MIN": f"{min(p['ratio_tok'] for p in gpqa_pairs):.2f}", "GPQA_TOK_MAX": f"{max(p['ratio_tok'] for p in gpqa_pairs):.2f}",
    # to the meter (D4)
    "SYS_NAME": _sys["system"], "SYS_KW": fmt(_sys["max_power_kw"], 1), "SYS_GPU_COUNT": str(_sys_n), "SYS_GPU_W": f"{_b200_w:,}",
    "SYS_GPU_KW": fmt(gpu_kw_sys, 1), "SYS_RATIO": f"{sys_ratio:.2f}", "EED_MIN_KW": fmt(EED_MIN_KW, 0), "PROTO_MIN_MINUTES": word(PROTO_MIN_MINUTES), "PROTO_MIN_REQUESTS": fmt(PROTO_MIN_REQUESTS, 0),
    "REPEAT_THRESHOLD_PCT": str(REPEAT_THRESHOLD_PCT), "CHALLENGE_TOLERANCE_PCT": str(CHALLENGE_TOLERANCE_PCT),
    "CONS_W": fmt(ref["_cfg"]["avg_power_watts"], 1), "CONS_TPS": fmt(ref["_cfg"]["output_throughput_tokens_per_sec"], 1),
    "CONS_WH": f"{ref['_cfg']['avg_power_watts'] / ref['_cfg']['output_throughput_tokens_per_sec'] * 1e6 / 3600:.2f}", "GPAI_MODIFY_SHARE": GPAI_MODIFY_SHARE, "PUE_EXAMPLE": f"{PUE_EXAMPLE:g}",
    "METER_WH": fmt(meter_wh, 0), "METER_TOKENS_B": fmt(meter_tokens_b, 1),
    "GOOGLE_WH": f"{GOOGLE_2025['wh']:g}", "GOOGLE_ACCEL_PCT": f"{GOOGLE_2025['accelerator_share'] * 100:.0f}",
    "GOOGLE_NARROW_WH": f"{GOOGLE_2025['narrow_wh']:.2f}", "GOOGLE_G": f"{GOOGLE_2025['g_co2e']:g}", "GOOGLE_ML": f"{GOOGLE_2025['water_ml']:g}",
    "GOOGLE_STACK_LO": f"{1 / GOOGLE_2025['accelerator_share']:.1f}", "GOOGLE_STACK_HI": f"{GOOGLE_2025['wh'] / GOOGLE_2025['narrow_wh']:.1f}",
    "GOOGLE_URL": GOOGLE_2025["url"], "MISTRAL_URL": MISTRAL_2025["url"],
    "MISTRAL_G": f"{MISTRAL_2025['g_co2e']:g}", "MISTRAL_ML": f"{MISTRAL_2025['water_ml']:g}", "MISTRAL_TOKENS": f"{MISTRAL_2025['tokens']:,}",
    # grids (D6, F14)
    "LISTED_GRID_COUNT": str(len(COUNTRIES)), "LISTED_GRID_WORD": word(len(COUNTRIES)),
    "MARKET_GRID_COUNT": str(len(COUNTRIES) - len(REFERENCE_GRIDS)), "REFERENCE_GRID_WORD": word(len(REFERENCE_GRIDS)),
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
    ("measurements.json", "Contributed measurements accepted under the protocol, with contributor, affiliation, date, versions and MIG profile; never merged into index.json."),
    ("schema/measurement.schema.json", "JSON Schema for a contributed measurement file (protocol v0.2); the build validates every submission against it."),
    ("changes.json", "Every change to the published data or its description: date, summary, documents, reason and source version."),
    ("index.csv", "The index rows as CSV, for a spreadsheet."),
    ("types.d.ts", "TypeScript types for every document, generated from the documents."),
    ("all.zip", "Every JSON document of the current release in one zip (the same bytes as the dated release zip)."),
    ("releases/index.json", "Every dated release of api/v1, each kept unchanged at releases/<date>/ with a zip of the whole release, for citation."),
]
api_docs: dict[str, dict] = {}
api_docs["manifest.json"] = {
    "version": "1", "updated": UPDATED, "site": SITE, "name": f"Lead Green {INDEX_NAME} API",
    "description": "GPU watt-hours per million output tokens by model, GPU and configuration, with grid carbon intensity and GPU hardware reference data. Static JSON, GET only, CORS open.",
    "endpoints": [{"path": p, "url": f"{SITE}/api/v1/{p}", "description": d} for p, d in ENDPOINTS],
    "sources": [SRC_MLE, SRC_MLE_GPQA, SRC_EMBER, {**hw["sources"][0], "licence": NVIDIA_LABEL},
                {**hw["sources"][1], "licence": NVIDIA_LABEL}, {**hw["sources"][2], "licence": NVIDIA_LABEL},
                SRC_AIES, SRC_OPENAI_TOKENS],
    "licence": LICENCE_TEXT, "caveat": CAVEAT, "boundary": BOUNDARY,
    "publisher": {"name": "Lead Green", "parent": "Katonic", "url": SITE, "entity": PUBLISHER_ENTITY,
                  "registration": PUBLISHER_REGISTRATION, "jurisdiction": PUBLISHER_JURISDICTION,
                  "address": PUBLISHER_ADDRESS or None, "contact": CONTACT_EMAIL, "response_working_days": RESPONSE_DAYS},
    "attribution": ATTRIBUTION, "data_version": DATA_VERSION,
    "releases": {"index": f"{SITE}/api/v1/releases/index.json", "pattern": f"{SITE}/api/v1/releases/<date>/"},
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
                "active_params_b": m["active_params_b"], "gpus": m["gpus"], "url": f"{SITE}/api/v1/models/{m['slug']}.json",
                "page": f"{SITE}/models/{m['slug']}/"}
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
api_docs["measurements.json"] = {
    "version": "1", "updated": UPDATED, "unit": "Wh per million output tokens", "protocol_version": PROTOCOL_VERSION,
    "schema": f"{SITE}/api/v1/schema/measurement.schema.json", "itl_deadline_ms": ITL_DEADLINE_MS,
    "note": ("Rows contributed under the measurement protocol and accepted by two reviewers. They are never merged into index.json. "
             "comparable is false for a row whose median inter-token latency exceeds itl_deadline_ms; such rows are shown and flagged."),
    "caveat": CAVEAT, "boundary": BOUNDARY, "rows": measurement_rows,
}
api_docs["schema/measurement.schema.json"] = MEAS_SCHEMA

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

# ----------------------------------------------------------------- D20: change list, data_version, field docs, typed schemas, downloads
CHANGES = [
    {"date": "2026-09-26", "summary": (f"First build. {len(index_rows)} index rows from ML.ENERGY v3.0 (data compiled {long_date(SRC_MLE['compiled'])}), "
                                        f"grid intensities from Ember ({EMBER_YEAR}), NVIDIA specifications, AI Energy Score December 2025 round. "
                                        "The API, the MCP server and the first blog post."),
     "documents": ["*"], "reason": "first build", "source_version": SRC_MLE["version"]},
    {"date": "2026-09-27", "summary": ("Corrections after a nine-reader review, before launch. The ML.ENERGY data is dated to its compile date, not a banner "
                                        f"update; the latency ceiling is the leaderboard's own {ITL_DEADLINE_MS} ms (no row moved); \"requests in flight\" is "
                                        "renamed running batch; full concurrency ladders; all AI Energy Score December rows; a two-task table; the carbon "
                                        "basis, grid years and display names; seven-decimal joules; additive API fields (data_version, row_id, repeat, "
                                        "p95_itl_ms, avg_running_batch, boundary, years, latest_year, iso2, display_name, source_label); changes.json, "
                                        "measurements.json, the measurement schema, a dated release archive, CSV, zip and TypeScript types."),
     "documents": ["*"], "reason": "review corrections", "source_version": SRC_MLE["version"]},
    {"date": "2026-10-17", "summary": (f"Ember's {EMBER_RELEASE} of its yearly electricity data (file dated 6 October 2026) replaces the September 2026 release. "
                                        f"The {EMBER_YEAR} emissions intensity moves for 26 of the {grid_count} grids and World, seven of them on the carbon table "
                                        "(United Arab Emirates 467.5 to 477.3 gCO2e per kWh, Sri Lanka 386.8 to 392.8, Australia 554.0 to 549.5, Saudi Arabia 691.9 to 689.1, "
                                        "Taiwan 636.2 to 635.2, Japan 483.6 to 484.3, Serbia 668.0 to 668.4), and every kilogram figure priced on them follows. "
                                        "2025 rows are added for Saudi Arabia and the United Arab Emirates. The reference year stays 2024, the latest with every "
                                        "listed grid present. No energy figure changes."),
     "documents": ["grid.json", "manifest.json"], "reason": "source release", "source_version": SRC_EMBER["version"]},
    {"date": "2026-10-18", "summary": "The publisher's registered office is added to About and to the manifest. No change to the data or its description.",
     "documents": ["manifest.json"], "reason": "publisher", "source_version": SRC_MLE["version"]},
    {"date": "2026-10-19", "summary": "Launch. Three blog posts: how much energy an AI query uses, what watt-hours per million tokens means, and why an idle GPU wastes energy. The site now serves from GitHub Pages at leadgreen.ai. No change to the data or its description.",
     "documents": [], "reason": "launch", "source_version": SRC_MLE["version"]},
]
assert CHANGES[-1]["date"] == DATA_VERSION, "add a CHANGES entry for this DATA_VERSION"
api_docs["changes.json"] = {"version": "1", "updated": UPDATED, "note": "One entry per change to the published data or its description, newest last.",
                            "changes": CHANGES}
subs["CHANGES_LIST"] = "\n".join(
    f"    <li><time datetime=\"{c['date']}\">{short_date(c['date'])}</time><span>{esc(c['summary'])}"
    + (subs["REVIEWED_LINE"] if c is CHANGES[0] else "") + "</span></li>" for c in reversed(CHANGES))

for _rel in list(api_docs):   # D20: data_version beside updated in every data document
    if _rel not in ("openapi.json", "schema/measurement.schema.json"):
        _d = api_docs[_rel]
        api_docs[_rel] = {**{k: _d[k] for k in ("version", "updated") if k in _d}, "data_version": DATA_VERSION,
                          **{k: v for k, v in _d.items() if k not in ("version", "updated", "data_version")}}

_CFG = {
    "gpu": "GPU model: H100 (H100 80GB HBM3) or B200.", "num_gpus": "Cards in the configuration.",
    "tensor_parallel": "Tensor-parallel degree.", "data_parallel": "Data-parallel degree.", "expert_parallel": "Expert-parallel degree (mixture-of-experts models).",
    "precision": "Weight precision (BF16, FP8, MXFP4).", "max_num_seqs": "The configured cap on sequences decoded at once (vLLM max_num_seqs).",
    "avg_running_batch": "The average number of requests the server was decoding at once over the steady-state window (vLLM num_requests_running). Queued requests are not counted.",
    "avg_requests_in_flight": "The same value as avg_running_batch under its first name, kept in v1 and removed at v2. It is the running batch, not client-side requests outstanding.",
    "wh_per_million_output_tokens": "GPU energy per million output tokens, watt-hours: joules_per_output_token x 1,000,000 / 3,600, which holds exactly on every row.",
    "joules_per_output_token": "The source's figure, seven decimals: steady-state GPU energy divided by the output tokens generated in that window (steady_state_energy_per_token). Prompt processing is included.",
    "median_itl_ms": "Median inter-token latency, milliseconds.", "p90_itl_ms": "90th percentile inter-token latency, milliseconds.",
    "p95_itl_ms": "95th percentile inter-token latency, milliseconds.", "p99_itl_ms": "99th percentile inter-token latency, milliseconds.",
    "tokens_per_second": "Output throughput of the whole configuration.", "gpu_power_watts_total": "Average power drawn, summed across every card.",
    "avg_output_tokens": "Average output length per response, tokens.",
    "under_itl_deadline": "Whether median_itl_ms is at or under itl_deadline_ms; every published configuration currently is.",
    "row_id": "Stable identifier, <slug>/<gpu>/<num_gpus>/<max_num_seqs>, with /r2 on a repeated run. It survives re-sorting and new rows.",
    "repeat": "1 for the first run of a configuration, 2 for the source's repeat of it (two Qwen 3 30B A3B configurations were run twice).",
}
FIELD_DOCS = {
    "*": {"version": "API major version; it changes only for a breaking change, which would ship at /api/v2/ with v1 left in place.",
          "updated": "Date the document was built.", "data_version": "Changes whenever a value in the document changes. Cite it with the release archive.",
          "unit": "Unit of the main figure in the document.", "caveat": "Carried on every document with energy figures. Please carry it into whatever you build.",
          "boundary": "gpu_only: GPU energy and nothing else; host, network, storage, cooling and idle time are outside it.",
          "itl_deadline_ms": f"The median inter-token latency ceiling used to pick best rows: {ITL_DEADLINE_MS} ms, the leaderboard's default.",
          "source": "The source object: name, publisher, url, data_url, version, retrieval date, licence with its evidence, method, selection and citation.",
          "note": "How to read the document.", "licence": "Licence of the document or of its source, as stated."},
    "index.json": {"workload": "The benchmark task behind the rows.", "selection": "The rule that picks each row, in words.",
                   "reference_row": "The row the carbon table and worked examples are priced on.", "reference_row.model": "Its model.",
                   "reference_row.gpu": "Its GPU.", "reference_row.num_gpus": "Its card count.",
                   "rows": "One row per model and GPU, sorted ascending by Wh/M.", "rows[].model": "Display name.", "rows[].slug": "Key for models/<slug>.json.",
                   "rows[].model_id": "Hugging Face id.", "rows[].params_b": "Total parameters, billions.", "rows[].active_params_b": "Parameters active per token, billions (they differ for mixture-of-experts models).",
                   **{f"rows[].{k}": v for k, v in _CFG.items()}},
    "models/{slug}.json": {"slug": "Model key.", "name": "Display name.", "model_id": "Hugging Face id.", "params_b": "Total parameters, billions.",
                           "active_params_b": "Parameters active per token, billions.", "architecture": "The source's label: Dense Transformer, MoE or Mamba-Transformer Hybrid.", "gpus": "GPUs the model was measured on.",
                           "configurations": "Every stable configuration the source measured for this model.",
                           **{f"configurations[].{k}": v for k, v in _CFG.items()},
                           "best": "The index row per GPU, keyed by GPU; each value has the configuration fields.",
                           **{f"best.<key>.{k}": v for k, v in _CFG.items()}, "best.<key>": "The configuration the index row uses for that GPU."},
    "models.json": {"models": "Every model on the index.", "models[].slug": "Model key.", "models[].name": "Display name.", "models[].model_id": "Hugging Face id.",
                    "models[].params_b": "Total parameters, billions.", "models[].active_params_b": "Parameters active per token, billions.",
                    "models[].gpus": "GPUs measured.", "models[].url": "URL of models/<slug>.json.", "models[].page": "URL of the model's page on the site."},
    "grid.json": {"year": f"The year g_co2e_per_kwh is taken from ({EMBER_YEAR}, the latest with every listed grid).", "basis": "What the figure is: lifecycle, location-based, production-based.",
                  "world": "The World figure for year.", "areas": "Every area Ember covers, plus the World row (iso3 WLD, area_type world); filter on area_type == country.",
                  "areas[].iso3": "ISO 3166-1 alpha-3 code (WLD for World).", "areas[].iso2": "ISO 3166-1 alpha-2 code; null for World and for Kosovo, which has none.",
                  "areas[].name": "Ember's label.", "areas[].display_name": "The shorter name the site shows.", "areas[].area_type": "country or world.",
                  "areas[].continent": "Ember's continent label.", "areas[].g_co2e_per_kwh": f"Emissions intensity, gCO2e per kWh, for year ({EMBER_YEAR}); kept for compatibility.",
                  "areas[].years": "Every year Ember holds for the area from 2023, keyed by year.", "areas[].years.<key>": "gCO2e per kWh in that year.",
                  "areas[].latest_year": "The newest year in years."},
    "hardware.json": {"retrieved": "When the specifications were read.", "tdp": "Maximum thermal design power per GPU.", "tdp[].gpu": "GPU.", "tdp[].form": "Form factor.",
                      "tdp[].max_tdp_w": "Maximum TDP, watts.", "tdp[].tdp_label": "TDP as NVIDIA words it.", "tdp[].memory": "Memory.", "tdp[].source": "Where the figure is from.",
                      "systems": "System power ratings.", "systems[].system": "System.", "systems[].gpus": "GPUs in the system.", "systems[].max_power_kw": "Maximum system power, kW.",
                      "systems[].label": "The rating as published.", "systems[].source": "Where it is from.",
                      "mig_profiles": "Multi-Instance GPU profiles per card (the media-extension variants are omitted).", "mig_profiles[].gpu": "Card.", "mig_profiles[].profile": "Profile name.",
                      "mig_profiles[].memory_fraction": "Share of the card's memory.", "mig_profiles[].sm_fraction": "Share of the card's streaming multiprocessors.",
                      "mig_profiles[].instances": "How many fit on one card.", "embodied": "One embodied-carbon figure.", "embodied.item": "What it covers.",
                      "embodied.kg_co2e_cradle_to_gate": "kg CO2e, cradle to gate, baseboard only.", "embodied.source": "Source.", "embodied.published": "Publication date.",
                      "sources": "The NVIDIA documents, with their terms."},
    "per-query.json": {"round": "The AI Energy Score round.", "setup": "How a query is run.", "classes": "Hardware classes.", "classes.<key>": "What the class means.",
                       "score": "What the stars mean.", "rows": "Every row of the round.", "rows[].model": "Clean Hugging Face id.", "rows[].source_label": "The model string exactly as the source gives it.",
                       "rows[].class": "Hardware class.", "rows[].wh_per_1000_queries": "GPU watt-hours for 1,000 queries.", "rows[].score": "Stars, 1 to 5, within the class.",
                       "rows[].note": "A note on the row, where there is one."},
    "manifest.json": {"site": "Site URL.", "name": "API name.", "description": "What the API is.", "endpoints": "Every endpoint.", "endpoints[].path": "Path under /api/v1/.",
                      "endpoints[].url": "Full URL.", "endpoints[].description": "What it returns.", "sources": "Every source with version, retrieval date, licence and evidence.",
                      "publisher": "Who publishes the API.", "publisher.name": "Project.", "publisher.parent": "Parent.", "publisher.url": "Site.", "publisher.entity": "Legal entity.",
                      "publisher.registration": "Registration number.", "publisher.jurisdiction": "Jurisdiction.", "publisher.address": "Registered office; null until confirmed.",
                      "publisher.contact": "Corrections and contributions mailbox.", "publisher.response_working_days": "Response time, working days.",
                      "attribution": "A ready CC BY 4.0 credit line.", "releases": "Where dated releases are kept.", "releases.index": "The list of releases.", "releases.pattern": "URL pattern of a release."},
    "measurements.json": {"protocol_version": "Protocol version the rows follow.", "schema": "URL of the measurement schema.",
                          "rows": "Contributed rows: the measurement schema's fields plus source_file and comparable (median ITL at or under itl_deadline_ms)."},
    "changes.json": {"changes": "One entry per change, oldest first.", "changes[].date": "Date of the change.", "changes[].summary": "What changed.",
                     "changes[].documents": "Documents affected (* for all).", "changes[].reason": "Why.", "changes[].source_version": "Source version at the time."},
    "releases/index.json": {"current": "The DATA_VERSION of the live files.", "releases": "Every release, newest first.", "releases[].date": "Release date.",
                            "releases[].url": "Folder holding that release's documents.", "releases[].zip": "Zip of the whole release.",
                            "releases[].sha256": "SHA-256 of the zip.", "releases[].published": "Whether the release is published and frozen."},
}


def _field_paths(o, prefix: str, acc: dict, doc: str) -> None:
    if isinstance(o, dict):
        for k, v in o.items():
            if prefix.endswith(("best.", "years.", "classes.")):
                k = "<key>"
            path = prefix + k
            if path in ("source", "sources") or path.startswith(("source.", "sources")):
                acc.setdefault(path.split(".")[0], None)
                continue
            acc.setdefault(path, None)
            _field_paths(v, path + ".", acc, doc)
    elif isinstance(o, list):
        for x in o:
            if isinstance(x, dict):
                _field_paths(x, prefix[:-1] + "[].", acc, doc)


_doc_samples = {"index.json": [api_docs["index.json"]], "models.json": [api_docs["models.json"]],
                "models/{slug}.json": [d for r, d in api_docs.items() if r.startswith("models/")],
                "grid.json": [api_docs["grid.json"]], "hardware.json": [api_docs["hardware.json"]], "per-query.json": [api_docs["per-query.json"]],
                "manifest.json": [api_docs["manifest.json"]], "measurements.json": [api_docs["measurements.json"]], "changes.json": [api_docs["changes.json"]]}
_undocumented = []
FIELD_ROWS: dict[str, list[tuple[str, str]]] = {}
for _doc, _samples in _doc_samples.items():
    _acc: dict = {}
    for _s in _samples:
        _field_paths(_s, "", _acc, _doc)
    FIELD_ROWS[_doc] = []
    for _f in _acc:
        _m = FIELD_DOCS.get(_doc, {}).get(_f) or (FIELD_DOCS["*"].get(_f) if "." not in _f and "[]" not in _f else None)
        if _m is None:
            _undocumented.append(f"{_doc}: {_f}")
        elif _f not in FIELD_DOCS["*"]:
            FIELD_ROWS[_doc].append((_f, _m))
if _undocumented:
    sys.exit("REFUSING TO BUILD, API fields without a description in FIELD_DOCS:\n  " + "\n  ".join(_undocumented))
subs["FIELD_TABLES"] = (
    "<div class=\"table-scroll\"><table class=\"spec\"><caption>Fields on every document</caption><thead><tr><th scope=\"col\">Field</th><th scope=\"col\">Meaning</th></tr></thead><tbody>\n"
    + "\n".join(f"<tr><th scope=\"row\">{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in FIELD_DOCS["*"].items()) + "\n</tbody></table></div>\n"
    + "\n".join(f"<details class=\"fields\"><summary><code>{esc(d)}</code>, {len(rows)} fields</summary><div class=\"table-scroll\"><table class=\"spec\"><thead><tr><th scope=\"col\">Field</th><th scope=\"col\">Meaning</th></tr></thead><tbody>\n"
                + "\n".join(f"<tr><th scope=\"row\">{esc(k)}</th><td>{esc(v)}</td></tr>" for k, v in rows) + "\n</tbody></table></div></details>"
                for d, rows in FIELD_ROWS.items() if rows))


def infer_schema(values: list, path: str = "", doc: str = "") -> dict:
    """A JSON Schema inferred from every real value at this position, so the published types are the published data."""
    vals = [v for v in values]
    types = []
    for v in vals:
        t = ("null" if v is None else "boolean" if isinstance(v, bool) else "integer" if isinstance(v, int) else "number" if isinstance(v, float)
             else "string" if isinstance(v, str) else "array" if isinstance(v, list) else "object")
        if t not in types:
            types.append(t)
    if "integer" in types and "number" in types:
        types.remove("integer")
    if path in ("publisher.address",) and types == ["null"]:
        types = ["string", "null"]   # null only until the registered office is confirmed
    sch: dict = {"type": types[0] if len(types) == 1 else types}
    desc = FIELD_DOCS.get(doc, {}).get(path) or FIELD_DOCS["*"].get(path)
    if desc:
        sch["description"] = desc
    objs = [v for v in vals if isinstance(v, dict)]
    if objs:
        if path.endswith(("best", "years", "classes")):
            sch["additionalProperties"] = infer_schema([x for o in objs for x in o.values()], path + ".<key>", doc)
        else:
            keys = list(dict.fromkeys(k for o in objs for k in o))
            sch["properties"] = {k: infer_schema([o[k] for o in objs if k in o], (path + "." if path else "") + k, doc)
                                 if not (path == "" and k in ("source", "sources")) else {"type": "object" if k == "source" else "array"}
                                 for k in keys}
            sch["required"] = [k for k in keys if all(k in o for o in objs)]
    lists = [v for v in vals if isinstance(v, list)]
    if lists:
        items = [x for l in lists for x in l]
        sch["items"] = infer_schema(items, path + "[]", doc) if items else {}
    return sch


_SCHEMA_NAMES = {"manifest.json": "Manifest", "index.json": "Index", "models.json": "Models", "models/{slug}.json": "Model", "grid.json": "Grid",
                 "hardware.json": "Hardware", "per-query.json": "PerQuery", "measurements.json": "Measurements", "changes.json": "Changes"}
_components = {name: infer_schema(_doc_samples[d], "", d) for d, name in _SCHEMA_NAMES.items()}
_components["Measurement"] = MEAS_SCHEMA
_paths = {}
for _p, _d in ENDPOINTS:
    _name = _SCHEMA_NAMES.get(_p)
    _ctype = {"csv": "text/csv", "ts": "text/plain", "zip": "application/zip"}.get(_p.rsplit(".", 1)[-1], "application/json")
    _schema = ({"$ref": f"#/components/schemas/{_name}"} if _name else {"$ref": "#/components/schemas/Measurement"} if _p.startswith("schema/")
               else {"type": "object"} if _ctype == "application/json" else {"type": "string"})
    _op = {"operationId": "get_" + re.sub(r"[^a-z0-9]+", "_", _p.replace(".json", "").replace("{slug}", "by_slug")).strip("_"), "summary": _d,
           "responses": {"200": {"description": _d, "content": {_ctype: {"schema": _schema}}}}}
    if "{slug}" in _p:
        _op["parameters"] = [{"name": "slug", "in": "path", "required": True, "schema": {"type": "string", "enum": sorted(models)}, "example": ref["slug"]}]
        _op["responses"]["404"] = {"description": "Unknown slug. The static host answers with its own HTML 404 page, not JSON."}
    _paths["/" + _p] = {"get": _op}
api_docs["openapi.json"]["paths"] = _paths
api_docs["openapi.json"]["components"] = {"schemas": _components}
api_docs["openapi.json"]["info"]["description"] = (
    "Static JSON files. GET only. No authentication. CORS open. Additive changes only within v1. Every schema here is inferred at build time "
    "from the published documents themselves, with the field descriptions the API page shows.")


def _ts(s: dict, ind: str = "") -> str:
    t = s.get("type")
    ts = t if isinstance(t, list) else [t]
    parts = []
    for x in ts:
        if x == "object":
            if "additionalProperties" in s and isinstance(s["additionalProperties"], dict):
                parts.append("Record<string, " + _ts(s["additionalProperties"], ind) + ">")
            elif "properties" in s:
                req = set(s.get("required", []))
                body = "".join(f"\n{ind}  {json.dumps(k) if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', k) else k}{'' if k in req else '?'}: {_ts(v, ind + '  ')};"
                               for k, v in s["properties"].items())
                parts.append("{" + body + f"\n{ind}}}")
            else:
                parts.append("Record<string, unknown>")
        elif x == "array":
            parts.append("Array<" + _ts(s.get("items") or {}, ind) + ">")
        elif x in ("integer", "number"):
            parts.append("number")
        elif x in ("string", "boolean", "null"):
            parts.append(x)
        else:
            parts.append("unknown")
    return " | ".join(parts) if parts else "unknown"


_extra_outputs: dict[str, str] = {}
# GEO item 6 (20 October 2026): the OpenAPI document also at the site root, where API clients and GPT builders look first,
# and an RFC 9727 API catalogue at /.well-known/api-catalog (a linkset) pointing at it. Both are copies; /api/v1/openapi.json stays canonical.
_extra_outputs["openapi.json"] = jdump(api_docs["openapi.json"])
_extra_outputs[".well-known/api-catalog"] = jdump({"linkset": [{
    "anchor": f"{SITE}/api/v1/",
    "service-desc": [{"href": f"{SITE}/api/v1/openapi.json", "type": "application/vnd.oai.openapi+json;version=3.1"}],
    "service-doc": [{"href": f"{SITE}/api/", "type": "text/html"}],
    "service-meta": [{"href": f"{SITE}/api/v1/manifest.json", "type": "application/json"}],
    "status": [{"href": f"{SITE}/api/v1/releases/index.json", "type": "application/json"}],
}]})
_extra_outputs["api/v1/types.d.ts"] = (f"// Lead Green API v1 types, generated from the published documents on {UPDATED} (data_version {DATA_VERSION}).\n"
                                "// Additive only within v1: new optional fields may appear.\n\n"
                                + "\n\n".join(f"export type {n} = {_ts(s)};" for n, s in _components.items() if n != "Measurement") + "\n")
_csv_cols = ["model", "slug", "model_id", "params_b", "active_params_b", "precision", "gpu", "num_gpus", "max_num_seqs", "avg_running_batch",
             "wh_per_million_output_tokens", "joules_per_output_token", "median_itl_ms", "gpu_power_watts_total", "avg_output_tokens", "row_id"]
import io as _io
_buf = _io.StringIO()
_w = csv.writer(_buf, lineterminator="\n")
_w.writerow(_csv_cols)
for _r in api_docs["index.json"]["rows"]:
    _w.writerow([_r.get(c, "") for c in _csv_cols])
_extra_outputs["api/v1/index.csv"] = _buf.getvalue()
subs["ENDPOINT_COUNT"] = str(len(ENDPOINTS))
subs["PAGES_MAX_AGE_S"] = str(PAGES_MAX_AGE_S)
subs["PAGES_BANDWIDTH_GB"] = str(PAGES_BANDWIDTH_GB)

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
       "parentOrganization": {"@type": "Organization", "name": "Katonic", "url": "https://www.katonic.ai"},
       **({"sameAs": SAME_AS} if SAME_AS else {})}   # T6: the same project elsewhere (public repository, dataset, DOI, Wikidata)
PERSON = {"@type": "Person", "name": EDITOR, "url": LINKEDIN_URL}


def jsonld_for(kind: str, title: str, desc: str, url: str, post: dict | None = None) -> str:
    if kind == "home":
        graph = [
            {**ORG, "@id": SITE + "/#org", "description": desc},
            {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/", "description": desc, "publisher": {"@id": SITE + "/#org"},
             "inLanguage": "en", "license": "https://creativecommons.org/licenses/by/4.0/", "dateModified": UPDATED},
        ]
        if post and post.get("faq"):
            graph.append({"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in post["faq"]]})
        return ld({"@context": "https://schema.org", "@graph": graph})
    if kind == "dataset":
        return ld({"@context": "https://schema.org", "@type": "Dataset", "name": f"{INDEX_NAME}: GPU energy per million output tokens",
                   "description": desc, "url": url, "license": "https://creativecommons.org/licenses/by/4.0/",
                   "creator": ORG, "publisher": ORG, "dateModified": UPDATED, "version": UPDATED, "inLanguage": "en",
                   "keywords": ["LLM inference energy", "watt-hours per token", "GPU energy", "grid carbon intensity", "H100", "B200"],
                   "variableMeasured": "GPU watt-hours per million output tokens",
                   **({"sameAs": HF_DATASET_URL} if HF_DATASET_URL else {}), **({"identifier": ZENODO_DOI_URL} if ZENODO_DOI_URL else {}),
                   "isBasedOn": [SRC_MLE["url"], SRC_EMBER["url"], SRC_AIES["url"], hw["sources"][0]["url"]],
                   "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}/api/v1/{p}"}
                                    for p, _ in ENDPOINTS if "{" not in p]})
    if kind == "webapi":
        return ld({"@context": "https://schema.org", "@type": "WebAPI", "name": f"Lead Green {INDEX_NAME} API", "description": desc,
                   "url": f"{SITE}/api/v1/manifest.json", "documentation": url, "provider": ORG,
                   "license": "https://creativecommons.org/licenses/by/4.0/", "termsOfService": url})
    if kind == "blog":
        return ld({"@context": "https://schema.org", "@type": "Blog", "name": "Lead Green blog", "url": url, "description": desc,
                   "publisher": ORG, "inLanguage": "en", "dateModified": UPDATED})
    if kind == "post" and post:
        return ld({"@context": "https://schema.org", "@type": "BlogPosting", "headline": title, "description": desc,
                   "datePublished": post["date"], "dateModified": post.get("updated", post["date"]),
                   "author": PERSON, "publisher": ORG, "mainEntityOfPage": url, "url": url, "inLanguage": "en",
                   "license": "https://creativecommons.org/licenses/by/4.0/", "isAccessibleForFree": True})
    if kind == "answer" and post:   # a generated answer page: the page, its FAQ, a breadcrumb and, where given, the dataset it draws on
        page = {"@type": "WebPage", "@id": url, "name": title, "description": desc, "url": url, "publisher": ORG, "inLanguage": "en",
                "dateModified": UPDATED, "license": "https://creativecommons.org/licenses/by/4.0/", "isPartOf": {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/"}}
        if post.get("dataset"):
            ds = post["dataset"]
            page["mainEntity"] = {"@type": "Dataset", "name": ds["name"], "description": desc, "license": "https://creativecommons.org/licenses/by/4.0/",
                                  "creator": ORG, "dateModified": UPDATED, "isBasedOn": ds["isBasedOn"],
                                  "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": ds["distribution"]}]}
        if post.get("term"):   # a glossary entry: the page defines one term of the site's glossary
            page["mainEntity"] = {"@type": "DefinedTerm", "@id": url + "#term", "name": post["term"]["name"], "description": post["term"]["description"], "url": url,
                                  "inDefinedTermSet": {"@type": "DefinedTermSet", "name": "Lead Green glossary", "url": SITE + "/glossary/"}}
        crumbs = [("Lead Green", SITE + "/")] + post.get("crumbs", []) + [(post["name"], url)]
        return ld({"@context": "https://schema.org", "@graph": [page,
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in post["faq"]]},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(crumbs)]}]})
    if kind == "model" and post:
        m = post["model"]
        return ld({"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url, "name": title, "description": desc, "url": url, "publisher": ORG, "inLanguage": "en",
             "dateModified": UPDATED, "license": "https://creativecommons.org/licenses/by/4.0/", "isPartOf": {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/"},
             "about": {"@type": "SoftwareApplication", "name": m["name"], "identifier": m["model_id"], "url": f"https://huggingface.co/{m['model_id']}", "applicationCategory": "Large language model"},
             "mainEntity": {"@type": "Dataset", "name": f"{m['name']}: GPU energy per million output tokens", "description": desc,
                            "license": "https://creativecommons.org/licenses/by/4.0/", "creator": ORG, "dateModified": UPDATED, "isBasedOn": SRC_MLE["url"],
                            "variableMeasured": "GPU watt-hours per million output tokens",
                            "distribution": [{"@type": "DataDownload", "encodingFormat": "application/json", "contentUrl": f"{SITE}/api/v1/models/{m['slug']}.json"}]}},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in post["faq"]]},
            {"@type": "BreadcrumbList", "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "Lead Green", "item": SITE + "/"},
                {"@type": "ListItem", "position": 2, "name": "Models", "item": SITE + "/models/"},
                {"@type": "ListItem", "position": 3, "name": m["name"], "item": url}]},
        ]})
    if kind == "glossary" and post:   # the glossary hub: the term set, each term pointing at its page
        return ld({"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url, "name": title, "description": desc, "url": url, "publisher": ORG, "inLanguage": "en",
             "dateModified": UPDATED, "license": "https://creativecommons.org/licenses/by/4.0/", "isPartOf": {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/"}},
            {"@type": "DefinedTermSet", "@id": url + "#set", "name": "Lead Green glossary", "url": url,
             "hasDefinedTerm": [{"@type": "DefinedTerm", "@id": f"{SITE}/glossary/{t['slug']}/#term", "name": t["name"], "description": t["short"], "url": f"{SITE}/glossary/{t['slug']}/"} for t in post["terms"]]},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Lead Green", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Glossary", "item": url}]}]})
    if kind == "faqhub" and post:   # the FAQ hub lists the questions; each page keeps its own FAQPage with the full answers
        return ld({"@context": "https://schema.org", "@graph": [
            {"@type": "WebPage", "@id": url, "name": title, "description": desc, "url": url, "publisher": ORG, "inLanguage": "en",
             "dateModified": UPDATED, "license": "https://creativecommons.org/licenses/by/4.0/", "isPartOf": {"@type": "WebSite", "name": "Lead Green", "url": SITE + "/"}},
            {"@type": "ItemList", "name": title, "numberOfItems": len(post["questions"]),
             "itemListElement": [{"@type": "ListItem", "position": i + 1, "item": {"@type": "Question", "name": q, "url": u + "#faq"}} for i, (q, u) in enumerate(post["questions"])]},
            {"@type": "BreadcrumbList", "itemListElement": [{"@type": "ListItem", "position": 1, "name": "Lead Green", "item": SITE + "/"}, {"@type": "ListItem", "position": 2, "name": "Questions", "item": url}]}]})
    page = {"@type": "WebPage", "name": title, "description": desc, "url": url, "publisher": ORG, "inLanguage": "en", "dateModified": UPDATED}
    if post and post.get("faq"):   # a hand-written page that also answers questions (the why page)
        return ld({"@context": "https://schema.org", "@graph": [{**page, "@id": url},
            {"@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in post["faq"]]}]})
    return ld({"@context": "https://schema.org", **page})


layout = LAYOUT.read_text(encoding="utf-8")
outputs: dict[str, str] = {}
outputs.update(_extra_outputs)
sitemap: list[tuple[str, str]] = []


# ----------------------------------------------------------------- social cards: one number per generated page (GEO strategy 6.3)
# A 1200 x 630 PNG per model, grid, glossary, compare and answer page, drawn from the same values as the page, in the
# design of assets/social-card.png (dark paper, the mark, Archivo for the figure, IBM Plex Mono for the labels).
# Pillow is a build dependency for the cards only: without it the build keeps the PNGs already on disk and says so.
FONTS = HERE / "fonts"
CARDS_REL = "assets/cards"
CARD_W, CARD_H = 1200, 630
CARD_BG, CARD_INK, CARD_INK2, CARD_MUTED, CARD_MINT, CARD_RULE = "#0E1411", "#E7EEE9", "#C9D2CD", "#8E9A93", "#5FCF97", "#1F6B47"
outputs_bin: dict[str, bytes] = {}
try:
    from PIL import Image as _PILImage, ImageDraw as _PILDraw, ImageFont as _PILFont
    CARDS_OK = all((FONTS / f).exists() for f in ("Archivo[wdth,wght].ttf", "IBMPlexMono-Regular.ttf", "IBMPlexMono-Medium.ttf"))
except ImportError:   # pragma: no cover
    CARDS_OK = False
_font_cache: dict[tuple, object] = {}


def _font(kind: str, size: int):
    key = (kind, size)
    if key not in _font_cache:
        if kind in ("bold", "medium"):
            f = _PILFont.truetype(str(FONTS / "Archivo[wdth,wght].ttf"), size)
            f.set_variation_by_axes([700 if kind == "bold" else 500, 100])   # axes: weight, width
        else:
            f = _PILFont.truetype(str(FONTS / ("IBMPlexMono-Medium.ttf" if kind == "mono-medium" else "IBMPlexMono-Regular.ttf")), size)
        _font_cache[key] = f
    return _font_cache[key]


def _wrap(draw, text: str, font, max_w: int, max_lines: int) -> list[str]:
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= max_w or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur:
        lines.append(cur)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        last = lines[-1]
        while draw.textlength(last + "...", font=font) > max_w and " " in last:
            last = last.rsplit(" ", 1)[0]
        lines[-1] = last.rstrip(",;:.") + "..."
    return lines


def card_png(eyebrow: str, value: str, unit: str, label: str, footer: str) -> bytes:
    im = _PILImage.new("RGB", (CARD_W, CARD_H), CARD_BG)
    d = _PILDraw.Draw(im)
    # the mark (assets/logo: a 64-unit grid), small, top left, with the wordmark beside it
    s, ox, oy = 1.5, 96, 64
    d.rectangle([ox + 22 * s, oy + 18 * s, ox + 42 * s, oy + 46 * s], fill=CARD_MINT)
    pts = [(ox + 4 * s, oy + 46 * s), (ox + 22 * s, oy + 46 * s), (ox + 22 * s, oy + 18 * s), (ox + 42 * s, oy + 18 * s), (ox + 42 * s, oy + 46 * s), (ox + 60 * s, oy + 46 * s)]
    d.line(pts, fill=CARD_INK, width=int(4 * s), joint="curve")
    for (x, y) in (pts[0], pts[-1]):
        d.ellipse([x - 2 * s, y - 2 * s, x + 2 * s, y + 2 * s], fill=CARD_INK)
    wm = _font("bold", 40)
    d.text((ox + 64 * s + 22, oy + 46 * s - 40), "Lead", font=wm, fill=CARD_INK)
    d.text((ox + 64 * s + 22 + d.textlength("Lead ", font=wm), oy + 46 * s - 40), "Green", font=wm, fill=CARD_MINT)
    # eyebrow
    eb = _font("mono-medium", 24)
    d.text((96, 186), eyebrow.upper(), font=eb, fill=CARD_MINT)
    # the number and its unit, sized to fit beside each other
    size = 190
    while size > 90:
        vf = _font("bold", size)
        uf = _font("mono", max(26, size // 5) if unit != "×" else size // 2)
        if d.textlength(value, font=vf) + 24 + d.textlength(unit, font=uf) <= CARD_W - 192:
            break
        size -= 10
    vb = vf.getbbox(value)
    base_y = 236 + (190 - size) // 2
    d.text((96 - vb[0], base_y), value, font=vf, fill=CARD_INK)
    d.text((96 + d.textlength(value, font=vf) + 24, base_y + (vb[3] - vb[1]) * 0.55), unit, font=uf, fill=CARD_MUTED)
    # the label, up to two lines
    if label and label[-1] not in ".!?":
        label += "."
    for lsize in (38, 34, 30):
        lf = _font("medium", lsize)
        if len(_wrap(d, label, lf, CARD_W - 192, 3)) <= 2:
            break
    y = base_y + (vb[3] - vb[1]) + 56 + (38 - lsize) // 2
    for line in _wrap(d, label, lf, CARD_W - 192, 2):
        d.text((96, y), line, font=lf, fill=CARD_INK2)
        y += lsize + 10
    # footer and rule
    ff = _font("mono", 22)
    if d.textlength(footer, font=ff) > CARD_W - 192 and " · a Katonic project" in footer:
        footer = footer.replace(" · a Katonic project", "")
    while d.textlength(footer, font=ff) > CARD_W - 192 and ff.size > 16:
        ff = _font("mono", ff.size - 1)
    d.text((96, 556), footer, font=ff, fill=CARD_MUTED)
    d.rectangle([96, 598, CARD_W - 96, 600], fill=CARD_RULE)
    im = im.quantize(colors=128, method=_PILImage.Quantize.MEDIANCUT, dither=_PILImage.Dither.NONE)
    buf = io.BytesIO()
    im.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def card_for(path: str, card: dict) -> tuple[str, str]:
    """Render (or keep) the card for a page path like 'models/qwen-3-32b/' and return (og:image URL, alt text)."""
    name = slug(path.strip("/")) or "home"
    rel = f"{CARDS_REL}/{name}.png"
    footer = f"leadgreen.ai/{path} · release {DATA_VERSION} · a Katonic project"
    alt = f"{card['value']} {card['unit']}: {card['label']}".strip()
    if CARDS_OK:
        outputs_bin[rel] = card_png(card["eyebrow"], card["value"], card["unit"], card["label"], footer)
    elif not (ROOT / rel).exists():
        return f"{SITE}/assets/social-card.png", "Lead Green: the energy behind the token"
    return f"{SITE}/{rel}", alt


faq_all: list[tuple[str, str, list[tuple[str, str]]]] = []   # (page name, url, questions) for the FAQ hub


def cite_line(url: str, title: str) -> str:
    """D13 per page: one line a reader can paste, naming the page, the URL and the dated release."""
    short = re.sub(r"\s*\|\s*Lead Green.*$", "", title).strip()
    return (f'<p class="cite">Cite this page: Lead Green, a Katonic project. {esc(short)}. {url}, release {DATA_VERSION}, '
            f'retrieved [date]. CC BY 4.0.</p>')


def with_cite(content: str, url: str, title: str) -> str:
    cite = cite_line(url, title)
    for pat in (r'<p class="unit">.*?</p>', r'<p class="byline">.*?</p>', r'<p class="stand">.*?</p>', r'</h1>'):
        m = re.search(pat, content, re.S)
        if m:
            return content[:m.end()] + "\n  " + cite + content[m.end():]
    return content


def render(out_rel: str, nav: str, title: str, desc: str, og_type: str, kind: str, body: str, post: dict | None = None):
    depth = out_rel.count("/")
    root = "../" * depth
    path = out_rel[: -len("index.html")]
    url = f"{SITE}/{path}"
    content = fill(body, subs)
    content = fill(content, {"ROOT": root})
    content = with_cite(content, url, title)
    if post and post.get("faq"):
        faq_all.append((post.get("name") or re.sub(r"\s*\|\s*Lead Green.*$", "", title), url, post["faq"]))
    og_image, og_alt = (card_for(path, post["card"]) if post and post.get("card") else (f"{SITE}/assets/social-card.png", "Lead Green: the energy behind the token"))
    page = fill(layout, {
        "TITLE": esc(title), "DESCRIPTION": esc(desc), "CANONICAL": url, "OG_TITLE": esc(title), "OG_TYPE": og_type,
        "SITE": SITE, "ROOT": root, "JSONLD": jsonld_for(kind, title, desc, url, post), "CONTENT": content,
        "UPDATED_LONG": long_date(UPDATED), "OG_IMAGE": og_image, "OG_IMAGE_ALT": esc(og_alt),
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
    # a post's title and description may carry placeholders (the drafts do); fill them once here so the blog list,
    # the RSS feed and the Markdown copies see the same text as the post page
    posts.append({**meta, "title": fill(meta["title"], subs), "description": fill(meta["description"], subs),
                  "slug": s, "author": meta.get("author", EDITOR), "body": body, "file": p.name})
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

PAGE_FAQ = {   # FAQPage structured data for the two hand-written pages the queries land on; the answers restate the page text
    "home": [
        ("What is Lead Green?",
         f"A public index of the GPU watt-hours it takes to serve a million output tokens, by model, GPU and configuration, with the grid carbon to price it anywhere. Every figure is from a named public measurement or a manufacturer's specification, dated and linked. The data is open under CC BY 4.0, there is a JSON API and an MCP server, and it is a Katonic project."),
        ("What unit does the index use?",
         f"Watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token. The index runs from {subs['TILE_LOW_WH']} Wh/M ({subs['TILE_LOW_LABEL']}) to {subs['TILE_HIGH_WH']} Wh/M ({subs['TILE_HIGH_LABEL']}), GPU only, measured on a busy server; every row is a floor that a real deployment sits above."),
        ("Where do the figures come from?",
         f"Energy per token from the ML.ENERGY Leaderboard v3.0 (data compiled {long_date(SRC_MLE['compiled'])}, retrieved {long_date(RETRIEVED)}); grid carbon intensity from Ember's yearly electricity data ({EMBER_RELEASE}, {EMBER_YEAR}); GPU power ceilings from NVIDIA's published specifications; per-query energy from the AI Energy Score's December 2025 round. Every source is listed with its version, licence and retrieval date in the index's ledger."),
        ("Is the data open, and how do I get it?",
         f"Yes. The compilation and site text are CC BY 4.0 and the sources keep their own licences. Every table is static JSON under {SITE}/api/v1/ with CORS open and no key, there is an MCP server for AI assistants, every page has a Markdown copy at its URL followed by index.md, and llms.txt at the site root lists all of it."),
        ("Who runs and pays for Lead Green?",
         f"{FUNDING} The publisher is {PUBLISHER_ENTITY}, registered in the {PUBLISHER_JURISDICTION}; the editor is {EDITOR}."),
    ],
    "why": [
        ("Does the EU AI Act require reporting the energy used by AI inference?",
         f"Not per inference. Regulation (EU) 2024/1689 requires providers of general-purpose AI models to keep technical documentation for the AI Office, and Annex XI, section 1, point 2(e) names the model's known or estimated energy consumption: a training figure in MWh, held by the provider, which does not reach buyers. Article 53(2) lifts the duty from models released under a free and open-source licence with public weights unless they carry systemic risk, and Article 111(3) gives models placed on the market before 2 August 2025 until 2 August 2027. No law asks anyone for serving energy per token. {LEGAL_NOTE}"),
        ("Which line of ESRS E1 does AI inference energy go on?",
         "For GPUs you run, the electricity is energy consumption from own operations under ESRS E1-5 (paragraph 37) and its emissions are Scope 2 under E1-6, location-based and market-based. Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3, category 1, purchased goods and services. In both cases the forecasting unit is energy per million tokens: tokens served next year multiplied by Wh/M gives the MWh."),
        ("How do I put AI energy efficiency in an RFP?",
         f"Ask every bidder for the same figure at the same load: GPU energy per million output tokens (Wh/M) for each proposed model and serving configuration, measured at steady state on the proposed hardware at a stated average running batch, with median and p99 inter-token latency reported, on the buyer's prompt set or the ML.ENERGY Leaderboard's conversation sample, GPU energy only, naming the method, the tool, the versions and the date. Score it with a gate on completeness, a floor from the index's rows for the same model and GPU, a challenge at {CHALLENGE_TOLERANCE_PCT} percent below the floor, and the consistency check Wh/M = average GPU power ÷ output tokens per second × 1,000,000 ÷ 3,600. The clause and the scoring box on this page are ready to paste."),
        ("Why does an idle GPU use more energy per token than a busy one?",
         f"Because the cards' power does not fall in step with their work. On the index, {l32['model']} on {l32['gpus']} goes from {fmt(l32['first'], 0)} Wh/M at a running batch of {fmt(l32['first_batch'], 0)} to {fmt(l32['best'])} Wh/M at {fmt(l32['best_batch'], 0)}, {l32['ratio']:.1f}× on the same hardware, while the cards' draw rises only {fmt(l32['power_pct'], 0)} percent. A high energy per token is what an under-used server looks like from the wall socket: you are paying for silicon that is waiting."),
        ("Does where I run AI change its energy per token?",
         f"No; it changes the carbon. The same tokens on the same GPUs use the same energy anywhere. On Ember's {EMBER_YEAR} figures the reference row carries {subs['REF_KG_SAU']} kg CO2e per billion tokens on Saudi Arabia's grid ({subs['SAU_G']} gCO2e per kWh) and {subs['REF_KG_NOR']} kg on Norway's ({subs['NOR_G']}), {subs['SAU_NOR_RATIO']}× apart."),
        ("Is the electricity for AI inference expensive?",
         f"No, and that is the point. At the reference row and USD {subs['ELECTRICITY_PRICE']} per kWh the electricity costs about {subs['CENTS_PER_M_REF']} cents per million tokens at the floor; a lightly loaded server pays several times that. Trivial as a bill, decisive as a signal: energy per token tracks GPU-hours, which is where the real money goes."),
    ],
}

for name, out_rel, nav, kind in PAGE_SPECS:
    meta, body = read_body(PAGES / f"{name}.html")
    for k in ("title", "description"):
        if k not in meta:
            raise SystemExit(f"pages/{name}.html: meta is missing '{k}'")
    _post = {"date": UPDATED, "faq": PAGE_FAQ[name], "name": "Lead Green" if name == "home" else "Why it matters"} if name in PAGE_FAQ else None
    if _post:   # the questions are visible on the page as well as in its structured data
        _h2 = "Asked about Lead Green" if name == "home" else "Asked about why the number matters"
        _qa = "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in _post["faq"])
        body = (body.rstrip("\n") + "\n\n<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>" + _h2 + "</h2>"
                + "<div class=\"prose faq\">" + _qa + "</div>"
                + "<p class=\"note\">Every question on the site, with a link to the page that answers it, is on "
                + "<a href=\"{{ROOT}}faq/\">the questions page</a>; the terms are defined in <a href=\"{{ROOT}}glossary/\">the glossary</a>.</p></section>\n")
    render(out_rel, nav, fill(meta["title"], subs), fill(meta["description"], subs), meta.get("og_type", "website"), kind, body, _post)

# The 404 page: nginx serves it (error_page) at whatever path was asked for, so every link and asset is absolute (ROOT = "/");
# it is not a page of the site (no sitemap entry, no Markdown copy, noindex). Written to /404.html, which the twin loop skips.
_m404, _b404 = read_body(PAGES / "404.html")
_p404 = fill(layout, {
    "TITLE": esc(_m404["title"]), "DESCRIPTION": esc(_m404["description"]), "CANONICAL": f"{SITE}/404.html", "OG_TITLE": esc(_m404["title"]),
    "OG_TYPE": "website", "SITE": SITE, "ROOT": "/", "JSONLD": "", "CONTENT": fill(fill(_b404, subs), {"ROOT": "/"}), "UPDATED_LONG": long_date(UPDATED),
    "OG_IMAGE": f"{SITE}/assets/social-card.png", "OG_IMAGE_ALT": "Lead Green: the energy behind the token",
})
_p404 = _p404.replace('<link rel="canonical" href="' + SITE + '/404.html">', '<meta name="robots" content="noindex">')
_p404 = _p404.replace('<link rel="alternate" type="text/markdown" href="' + SITE + '/404.htmlindex.md">\n', "")
assert "index.md" not in _p404.split("</head>")[0], "404 page must not advertise a Markdown copy"
outputs["404.html"] = _p404

# ----------------------------------------------------------------- model pages: one page per model, generated from the data (SEO / AEO)
MODEL_CARBON_GRIDS = ["SAU", "IND", "HKG", "SRB", "DEU", "NOR"]   # a spread of the listed grids; World is added
_country_name = dict(COUNTRIES)


def _gpu_groups(name: str) -> list[tuple[str, int, list]]:
    """(gpu, num_gpus, configurations) for one model, H100 first, fewest cards first."""
    groups: dict[tuple[str, int], list] = {}
    for c in cfgs:
        if c["nickname"] == name:
            groups.setdefault((c["gpu_model"], c["num_gpus"]), []).append(c)
    return [(g, n, sorted(v, key=lambda c: c["max_num_seqs"])) for (g, n), v in sorted(groups.items())]


def _pct(a: float, b: float) -> str:
    return f"{(a / b - 1) * 100:.0f}"


def model_page(m: dict) -> tuple[str, str, str, list[tuple[str, str]]]:
    """Returns (title, description, body html, faq) for one model."""
    name, s = m["name"], m["slug"]
    bests = {g: best[(name, g)] for g in m["gpus"]}            # raw source rows
    groups = _gpu_groups(name)
    n_cfg = sum(len(v) for _, _, v in groups)
    gpus_word = and_list(m["gpus"])
    arch = {"Dense Transformer": "a dense transformer", "Mamba-Transformer Hybrid": "a Mamba-Transformer hybrid"}.get(
        m["architecture"], f"a mixture-of-experts model ({m['active_params_b']:g} B of {m['params_b']:g} B parameters active per token)")
    prec = sorted({precision_label(c["weight_precision"]) for _, _, v in groups for c in v})

    # the direct answer
    parts = []
    for g in m["gpus"]:
        b = bests[g]
        parts.append(f"<b>{fmt(cfg_wh(b))} Wh/M</b> on {b['num_gpus']} × {g} (running batch {fmt(b['avg_batch_size'], 0)}, median inter-token latency {fmt(b['median_itl_ms'], 0)} ms)")
    answer = (f"{esc(name)} serves a million output tokens for " + and_list(parts) + f", GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. "
              f"That is the floor: a lightly loaded server sits above it.")

    # tiles, one per GPU
    tiles = []
    for g in m["gpus"]:
        b = bests[g]
        tiles.append(f"<div class=\"tile\"><span class=\"lbl\">Index row, {g}</span><span class=\"val\">{fmt(cfg_wh(b))}<small>Wh/M</small></span>"
                     f"<span class=\"sub\">{b['num_gpus']} × {g}, {precision_label(b['weight_precision'])}. Running batch {fmt(b['avg_batch_size'], 0)}, median ITL {fmt(b['median_itl_ms'], 0)} ms, "
                     f"{fmt(b['avg_power_watts'], 0)} W across the cards, {fmt(b['output_throughput_tokens_per_sec'], 0)} tokens a second.</span></div>")
    tiles_html = f"<div class=\"tiles auto n{len(tiles)}\" role=\"group\" aria-label=\"Index rows\">" + "".join(tiles) + "</div>"

    # every configuration, one table per GPU and card count
    tables, ladder_facts = [], []
    for g, n, v in groups:
        lad = ladder(name, g, n)
        cap = f"{esc(name)}, {precision_label(v[0]['weight_precision'])}, {n} × {g}: {word(len(v))} measured configuration{'s' if len(v) != 1 else ''}"
        tables.append(
            "<div class=\"table-scroll\"><table><caption>" + cap + "</caption><thead><tr>"
            "<th scope=\"col\" class=\"num\">Cap</th><th scope=\"col\" class=\"num\">Running batch (avg)</th><th scope=\"col\" class=\"num\">Wh / M</th>"
            "<th scope=\"col\" class=\"num\">Median ITL (ms)</th><th scope=\"col\" class=\"num\">Tokens / s</th><th scope=\"col\" class=\"num\">GPU power (W)</th>"
            "</tr></thead><tbody>\n" + lad["rows"] + "\n</tbody></table></div>")
        if len(v) >= 3:
            ladder_facts.append({"gpu": g, "n": n, **lad})
    ladder_facts.sort(key=lambda d: -d["count"])
    load_para = ""
    if ladder_facts:
        L = ladder_facts[0]
        load_para = (f"<p class=\"lead\">On {L['n']} × {L['gpu']}, {esc(name)} runs from <b>{fmt(L['first'])} Wh/M</b> at a running batch of {fmt(L['first_batch'], 0)} to "
                     f"<b>{fmt(L['best'])} Wh/M</b> at {fmt(L['best_batch'], 0)}, a fall of {L['ratio']:.1f}×, while the cards' draw rises {L['power_pct']:.0f} percent "
                     f"(from {fmt(L['first_w'], 0)} to {fmt(L['best_w'], 0)} W) and throughput rises {L['tps_ratio']:.1f}× (from {fmt(L['first_tps'], 0)} to {fmt(L['best_tps'], 0)} tokens a second). "
                     f"Median inter-token latency stays at {fmt(L['max_itl_to_best'], 0)} ms or under up to the best row."
                     + (f" Past it, at a cap of {fmt(L['turn']['cap'], 0)}, the same cards read {fmt(L['turn']['wh'])} Wh/M at {fmt(L['turn']['itl'], 0)} ms." if L["turn"] else "") + "</p>")

    # two generations
    compare_html, compare_fact = "", ""
    if "H100" in bests and "B200" in bests:
        h, b = bests["H100"], bests["B200"]
        ratio = cfg_wh(h) / cfg_wh(b)
        compare_fact = (f"On the index rows, the H100 configuration uses {ratio:.2f}× the energy per token of the B200 configuration: "
                        f"{fmt(cfg_wh(h))} Wh/M on {h['num_gpus']} × H100 against {fmt(cfg_wh(b))} Wh/M on {b['num_gpus']} × B200.")
        note = ""
        if h["num_gpus"] != b["num_gpus"] or abs(h["avg_batch_size"] - b["avg_batch_size"]) / max(h["avg_batch_size"], b["avg_batch_size"]) > 0.25:
            note = (f" The two rows were not swept alike: the H100 row holds a running batch of {fmt(h['avg_batch_size'], 0)} on {h['num_gpus']} card{'s' if h['num_gpus'] != 1 else ''} "
                    f"and the B200 row {fmt(b['avg_batch_size'], 0)} on {b['num_gpus']}, so part of the gap is the sweep, not the silicon.")
        compare_html = (f"<section id=\"generations\"><p class=\"eyebrow\">Two generations</p><h2>H100 against B200</h2>"
                        f"<p class=\"lead\">{compare_fact}{note} The full comparison across {{{{PAIR_COUNT}}}} models is on <a href=\"{{{{ROOT}}}}index/#generations\">the index</a>.</p></section>")

    # carbon on a spread of grids, for the lowest index row
    ref_gpu = min(bests, key=lambda g: cfg_wh(bests[g]))
    rb = bests[ref_gpu]
    rows = [(_country_name[iso], intensity[iso]) for iso in MODEL_CARBON_GRIDS] + [("World", world)]
    rows.sort(key=lambda t: -t[1])
    carbon_rows = "\n".join(f"<tr><th scope=\"row\">{esc(n_)}</th><td class=\"num\">{fmt(g_, 0)}</td><td class=\"num key\">{fmt(kg_per_billion(cfg_wh(rb), g_))}</td></tr>" for n_, g_ in rows)
    sau, nor = intensity["SAU"], intensity["NOR"]
    carbon_fact = (f"A billion output tokens of {esc(name)} on {rb['num_gpus']} × {ref_gpu} at its index row carries about {fmt(kg_per_billion(cfg_wh(rb), sau))} kg CO2e of GPU-side emissions "
                   f"on the Saudi grid ({fmt(sau, 0)} gCO2e per kWh, Ember {EMBER_YEAR}) and {fmt(kg_per_billion(cfg_wh(rb), nor))} kg on the Norwegian grid ({fmt(nor, 0)}).")
    carbon_html = (f"<section id=\"carbon\"><p class=\"eyebrow\">Carbon</p><h2>Same tokens, different grid</h2><p class=\"lead\">{carbon_fact} Energy per token does not change with geography; carbon per token does.</p>"
                   f"<div class=\"table-scroll\"><table><caption>{esc(name)}, {rb['num_gpus']} × {ref_gpu} index row ({fmt(cfg_wh(rb))} Wh/M), priced on {EMBER_YEAR} annual grid averages, location-based</caption>"
                   "<thead><tr><th scope=\"col\">Grid</th><th scope=\"col\" class=\"num\">g CO2e per kWh</th><th scope=\"col\" class=\"num\">kg CO2e per billion output tokens</th></tr></thead><tbody>\n"
                   + carbon_rows + "\n</tbody></table></div>"
                   f"<p class=\"note\">Wh/M × gCO2e per kWh ÷ 1,000. {{{{EMBER_BASIS}}}} All {{{{GRID_COUNT}}}} grids are in <a href=\"{{{{ROOT}}}}api/v1/grid.json\">grid.json</a>; the <a href=\"{{{{ROOT}}}}mcp/\">MCP server</a> prices any model on any grid.</p></section>")

    # two tasks
    task_html, task_fact = "", ""
    tp = [p for p in gpqa_pairs if p["model"] == name]
    if tp:
        bits = [f"{times(p['ratio'])} the energy per response and {times(p['ratio_tok'], 2)} the energy per token on {p['num_gpus']} × {p['gpu']} "
                f"(answers of {fmt(p['out_gpqa'], 0)} tokens against {fmt(p['out_chat'], 0)}; running batch {fmt(p['batch_gpqa'], 0)} against {fmt(p['batch_chat'], 0)})" for p in tp]
        task_fact = f"On the leaderboard's Problem Solving task, {esc(name)} costs " + and_list(bits) + ", compared with Text Conversation."
        task_html = (f"<section id=\"workloads\"><p class=\"eyebrow\">Two tasks</p><h2>Long answers cost more per token too</h2><p class=\"lead\">{task_fact} "
                     f"The long answers cut the batch the server can hold, which is why energy per token itself moves. All {{{{GPQA_PAIRS}}}} pairs are on <a href=\"{{{{ROOT}}}}index/#workloads\">the index</a>.</p></section>")

    # FAQ, visible text and structured data from the same list
    faq: list[tuple[str, str]] = []
    faq.append((f"How much energy does {name} use per million output tokens?",
                re.sub(r"<[^>]+>", "", f"{name} uses " + and_list([f"{fmt(cfg_wh(bests[g]))} Wh of GPU energy per million output tokens on {bests[g]['num_gpus']} × {g}" for g in m["gpus"]])
                       + f" at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled {long_date(SRC_MLE['compiled'])}). "
                       "Host, network, cooling and idle time are not counted, so it is a floor.")))
    if compare_fact:
        faq.append((f"Is {name} more energy-efficient on B200 or H100?", re.sub(r"<[^>]+>", "", compare_fact + " Both are floors at high load.")))
    if ladder_facts:
        L = ladder_facts[0]
        faq.append((f"How much does load change the energy per token of {name}?",
                    f"On {L['n']} × {L['gpu']}, energy per token falls {L['ratio']:.1f}× between a running batch of {fmt(L['first_batch'], 0)} ({fmt(L['first'])} Wh/M) and {fmt(L['best_batch'], 0)} ({fmt(L['best'])} Wh/M), "
                    f"because the cards' power rises only {L['power_pct']:.0f} percent while throughput rises {L['tps_ratio']:.1f}×. A server holding a handful of requests at a time sits at the top of that range."))
    faq.append((f"What is the carbon footprint of a billion tokens of {name}?", re.sub(r"<[^>]+>", "", carbon_fact) + " Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens."))
    if task_fact:
        faq.append((f"Does {name} use more energy for reasoning or problem-solving tasks?", re.sub(r"<[^>]+>", "", task_fact)))
    faq.append((f"Is this the energy my {name} deployment will use?",
                f"No. Every figure here is the lowest-energy configuration under the leaderboard's {ITL_DEADLINE_MS} ms median inter-token latency ceiling, on a busy server, GPU only. "
                "Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page."))
    faq.append(("Where do these figures come from?",
                f"The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released {long_date(SRC_MLE['released'])}, data compiled {long_date(SRC_MLE['compiled'])}, retrieved {long_date(RETRIEVED)}: "
                f"{n_cfg} stable configurations of {name} measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's {EMBER_YEAR} yearly figures. Lead Green recomputes every number from dated snapshots."))
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about " + esc(name) + "</h2><div class=\"prose faq\">" + "".join(
        f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq) + "</div></section>"

    toc = ["<li><a href=\"#configurations\">Every configuration</a></li>"]
    if compare_html:
        toc.append("<li><a href=\"#generations\">Two generations</a></li>")
    toc.append("<li><a href=\"#carbon\">Carbon</a></li>")
    if task_html:
        toc.append("<li><a href=\"#workloads\">Two tasks</a></li>")
    toc += ["<li><a href=\"#faq\">Questions</a></li>", "<li><a href=\"#sources\">Sources</a></li>"]

    body = f"""<div class="title">
  <p class="eyebrow"><a href="{{{{ROOT}}}}models/">Models</a> · {esc(gpus_word)}</p>
  <h1>{esc(name)}: GPU energy per million output tokens</h1>
  <p class="stand">{answer}</p>
  <p class="unit"><b>Model</b> <a href="https://huggingface.co/{esc(m['model_id'])}">{esc(m['model_id'])}</a>, {arch}, weights in {esc(and_list(prec))}. <b>Measured</b> {n_cfg} configurations on {esc(gpus_word)}. <b>Data</b> <a href="{{{{ROOT}}}}api/v1/models/{s}.json">models/{s}.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page">{"".join(toc)}</ul>
</div>
{tiles_html}
<p class="after-tiles">GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.</p>

<section id="configurations" class="first">
  <p class="eyebrow">Every configuration</p>
  <h2>{esc(name)} at every measured load</h2>
  {load_para}
  <div class="stack">
{chr(10).join(tables)}
  </div>
  <p class="note">Cap is the configured maximum batch (vLLM's <code>max_num_seqs</code>). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's <code>num_requests_running</code>); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.</p>
</section>
{compare_html}
{carbon_html}
{task_html}
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">{{{{MLE_BLOCK}}}}</p>
  <p class="note">Grid intensity: <a href="https://ember-energy.org/data/yearly-electricity-data/">Ember, Yearly electricity data</a>, {EMBER_RELEASE}, {EMBER_YEAR} (CC BY 4.0). Model card: <a href="https://huggingface.co/{esc(m['model_id'])}">Hugging Face</a>.</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
  <p class="note">This page is generated from the same dated snapshot as <a href="{{{{ROOT}}}}index/">the index</a> and <a href="{{{{ROOT}}}}api/v1/models/{s}.json">the API</a>; no figure on it is typed by hand. Ask the <a href="{{{{ROOT}}}}mcp/">MCP server</a> for {esc(name)} on your own grid and load.</p>
</section>"""
    title = f"{name}: energy per million output tokens | Lead Green"
    for desc in (f"GPU watt-hours per million output tokens for {name} on {gpus_word}: {n_cfg} measured configurations, the load curve, H100 vs B200 and carbon by grid. From ML.ENERGY v3.0.",
                 f"GPU watt-hours per million output tokens for {name} on {gpus_word}: {n_cfg} measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.",
                 f"GPU watt-hours per million output tokens for {name}: {n_cfg} measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.",
                 f"{name}: GPU watt-hours per million output tokens at every measured load, with carbon by grid. ML.ENERGY v3.0 data.",
                 f"{name}: GPU energy per million output tokens, every measured load. ML.ENERGY v3.0 data."):
        if len(desc) <= 155:
            break
    return title, desc, body, faq


model_cards = []
for s_, m_ in sorted(models.items(), key=lambda kv: min(cfg_wh(best[(kv[1]["name"], g)]) for g in kv[1]["gpus"])):
    t_, d_, b_, faq_ = model_page(m_)
    lo_ = min(m_["gpus"], key=lambda g: cfg_wh(best[(m_["name"], g)]))
    lb_ = best[(m_["name"], lo_)]
    render(f"models/{s_}/index.html", "models", t_, d_, "article", "model", b_,
           {"date": UPDATED, "faq": faq_, "model": m_, "name": m_["name"],
            "card": {"eyebrow": "GPU energy per million output tokens", "value": fmt(cfg_wh(lb_)), "unit": "Wh/M",
                     "label": f"{m_['name']} on {lb_['num_gpus']} × {lo_}, running batch {fmt(lb_['avg_batch_size'], 0)}. GPU only, busy server, a floor."}})
    params_ = f"{m_['params_b']:g} B parameters" + (f", {m_['active_params_b']:g} B active" if m_["architecture"] == "MoE" else "")
    model_cards.append(
        f"<div class=\"card\"><span class=\"k\">{esc(and_list(m_['gpus']))}</span><h3><a href=\"{{{{ROOT}}}}models/{s_}/\">{esc(m_['name'])}</a></h3>"
        f"<span class=\"n\">{fmt(cfg_wh(lb_))}<small>Wh/M, {lb_['num_gpus']} × {lo_}</small></span>"
        f"<p>{params_}; "
        f"{sum(1 for c in cfgs if c['nickname'] == m_['name'])} measured configurations.</p></div>")
subs["MODEL_CARDS"] = "\n".join(model_cards)
meta_, body_ = read_body(PAGES / "models.html")
render("models/index.html", "models", fill(meta_["title"], subs), fill(meta_["description"], subs), "website", "page", body_)

# ----------------------------------------------------------------- grid pages: one per listed grid, and the H100 vs B200 page (SEO / AEO)
_area_by_iso = {a["iso3"]: a for a in areas}
_country_rank = {a["iso3"]: i + 1 for i, a in enumerate(sorted(countries_only, key=lambda a: intensity[a["iso3"]]))}   # 1 = cleanest
_model_lowest = sorted(((m_["name"], min(m_["gpus"], key=lambda g: cfg_wh(best[(m_["name"], g)])), s_) for s_, m_ in models.items()),
                       key=lambda t: cfg_wh(best[(t[0], t[1])]))
ref_wh_raw, low_wh_raw, high_wh_raw = raw_wh(ref), raw_wh(low), raw_wh(high)


def ordinal(n: int) -> str:
    suf = "th" if 10 <= n % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n:,}{suf}"


def grid_slug(iso: str) -> str:
    return slug(_area_by_iso[iso]["display_name"])


def grid_page(iso: str) -> tuple[str, str, str, list[tuple[str, str]]]:
    a = _area_by_iso[iso]
    name = a["display_name"]
    g = intensity[iso]
    yrs = a["years"]
    latest = a["latest_year"]
    rank = _country_rank[iso]
    role = "a reference grid" if iso in REFERENCE_GRIDS else "a market Katonic sells in or expects to"
    vs_world = g / world
    where = f"{vs_world:.1f}× the world average of {fmt(world, 0)}" if vs_world >= 1.05 else (f"{1 / vs_world:.1f}× cleaner than the world average of {fmt(world, 0)}" if vs_world <= 0.95 else f"close to the world average of {fmt(world, 0)}")
    kg_ref, kg_low, kg_high = (kg_per_billion(w, g) for w in (ref_wh_raw, low_wh_raw, high_wh_raw))
    answer = (f"{esc(name)}'s grid ran at <b>{fmt(g, 0)} gCO2e per kWh</b> in {EMBER_YEAR} on Ember's yearly figures, {where}, and {ordinal(rank)} of the {grid_count} countries Ember covers, counting from the cleanest. "
              f"A billion output tokens of the index's reference row ({esc(REF_MODEL_NAME)}, {ref['num_gpus']} × {ref['gpu']}, {fmt(ref_wh_raw)} Wh/M) served on it carries about <b>{fmt(kg_ref)} kg CO2e</b> of GPU-side emissions; "
              f"the index's lowest row carries {fmt(kg_low)} kg and its highest {fmt(kg_high)} kg. Energy per token does not change with geography; carbon per token does.")
    # trend
    trend = ""
    if len(yrs) >= 2:
        y0, v0 = min(yrs), yrs[min(yrs)]
        v1 = yrs[latest]
        chg = (v1 / v0 - 1) * 100
        verb = "fell" if chg < -0.5 else ("rose" if chg > 0.5 else "was flat")
        trend = (f"From {y0} to {latest} the intensity {verb}" + (f" {abs(chg):.0f} percent, from {fmt(v0)} to {fmt(v1)} gCO2e per kWh" if verb != "was flat" else f" at about {fmt(v1)} gCO2e per kWh") + ". "
                 + (f"The table uses {EMBER_YEAR}, the latest year with a value for every listed grid; on the {latest} figure the reference row would carry {fmt(kg_per_billion(ref_wh_raw, v1))} kg per billion tokens." if latest != EMBER_YEAR else f"{EMBER_YEAR} is the latest year Ember publishes for {esc(name)}."))
    years_rows = "\n".join(f"<tr><th scope=\"row\">{y}</th><td class=\"num key\">{fmt(v)}</td><td class=\"num\">{fmt(kg_per_billion(ref_wh_raw, v))}</td></tr>" for y, v in sorted(yrs.items()))
    tiles = (f"<div class=\"tiles auto n3\" role=\"group\" aria-label=\"Headline readings\">"
             f"<div class=\"tile\"><span class=\"lbl\">Grid intensity, {EMBER_YEAR}</span><span class=\"val\">{fmt(g, 0)}<small>gCO2e/kWh</small></span><span class=\"sub\">Ember yearly data, lifecycle, location-based. World: {fmt(world, 0)}.</span></div>"
             f"<div class=\"tile ref\"><span class=\"lbl\">Reference row, per billion tokens</span><span class=\"val\">{fmt(kg_ref)}<small>kg CO2e</small></span><span class=\"sub\">{esc(REF_MODEL_NAME)}, {ref['num_gpus']} × {ref['gpu']}, {fmt(ref_wh_raw)} Wh/M, GPU only, a floor.</span></div>"
             f"<div class=\"tile\"><span class=\"lbl\">Rank</span><span class=\"val\">{rank}<small>of {grid_count}</small></span><span class=\"sub\">1 is the cleanest grid Ember covers ({esc(grid_min['display_name'])}, {fmt(intensity[grid_min['iso3']], 0)}); {grid_count} the highest ({esc(grid_max['display_name'])}, {fmt(intensity[grid_max['iso3']], 0)}).</span></div></div>")
    # every model on this grid
    model_rows = "\n".join(
        f"<tr><th scope=\"row\"><a class=\"model\" href=\"{{{{ROOT}}}}models/{s_}/\">{esc(mn)}</a></th><td class=\"num\">{best[(mn, gp)]['num_gpus']} × {gp}</td>"
        f"<td class=\"num\">{fmt(cfg_wh(best[(mn, gp)]))}</td><td class=\"num key\">{fmt(kg_per_billion(cfg_wh(best[(mn, gp)]), g))}</td></tr>"
        for mn, gp, s_ in _model_lowest)
    faq = [
        (f"What is the grid carbon intensity of {name}?",
         f"{fmt(g, 0)} gCO2e per kWh in {EMBER_YEAR}, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, {where}. "
         + (f"Ember's {latest} figure is {fmt(yrs[latest])}." if latest != EMBER_YEAR else "")),
        (f"How much CO2 does a million AI tokens produce in {name}?",
         f"At the index's reference row ({REF_MODEL_NAME} on {ref['num_gpus']} × {ref['gpu']}, {fmt(ref_wh_raw)} Wh per million output tokens, GPU only), about {fmt(kg_ref)} grams of CO2e per million tokens, or {fmt(kg_ref)} kg per billion, "
         f"on {name}'s {EMBER_YEAR} grid. Across the index the range is {fmt(kg_low)} to {fmt(kg_high)} kg per billion tokens. A lightly loaded server sits above these floors, and host, network and cooling are not counted."),
        (f"Is running AI in {name} cleaner than the world average?",
         f"{name}'s {EMBER_YEAR} intensity of {fmt(g, 0)} gCO2e per kWh is {where} ({fmt(world, 0)} gCO2e per kWh). The same tokens on the same GPUs produce the same energy figure anywhere; only the carbon figure moves with the grid."),
        (f"Can I use this figure for my Scope 2 report in {name}?",
         "As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. "
         "Tokens bought from a hosted API land in your Scope 3 category 1, not your Scope 2. The why page explains both."),
        ("Where do these figures come from?",
         f"Grid intensity: Ember, Yearly electricity data, {EMBER_RELEASE} ({EMBER_YEAR}; {', '.join(sorted(yrs))} shown), CC BY 4.0, retrieved {long_date(EMBER_RETRIEVED)}. Energy per token: the ML.ENERGY Leaderboard v3.0 (data compiled {long_date(SRC_MLE['compiled'])}). Carbon is Wh/M × gCO2e per kWh ÷ 1,000."),
    ]
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about AI carbon in " + esc(name) + "</h2><div class=\"prose faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq) + "</div></section>"
    body = f"""<div class="title">
  <p class="eyebrow"><a href="{{{{ROOT}}}}grids/">Grids</a> · {esc(a['continent'])} · {role}</p>
  <h1>{esc(name)}: the carbon of AI inference per billion tokens</h1>
  <p class="stand">{answer}</p>
  <p class="unit"><b>Area</b> {esc(a['name'])} ({iso}{', ' + a['iso2'] if a['iso2'] else ''}). <b>Basis</b> lifecycle, location-based, annual average. <b>Data</b> <a href="{{{{ROOT}}}}api/v1/grid.json">grid.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#trend">Trend</a></li><li><a href="#models">Every model</a></li><li><a href="#reporting">Reporting</a></li><li><a href="#faq">Questions</a></li><li><a href="#sources">Sources</a></li></ul>
</div>
{tiles}
<p class="after-tiles">Carbon per token is energy per token times the grid. The energy figures here are GPU-only floors from a busy server; a lightly loaded deployment sits above them, and so does anything that includes the host, the network and the cooling. Wh/M × gCO2e per kWh ÷ 1,000 gives kg CO2e per billion output tokens.</p>

<section id="trend" class="first">
  <p class="eyebrow">Trend</p>
  <h2>{esc(name)}'s grid, year by year</h2>
  <p class="lead">{trend}</p>
  <div class="table-scroll"><table><caption>Ember yearly emissions intensity for {esc(name)}, and the reference row priced on each year</caption>
  <thead><tr><th scope="col">Year</th><th scope="col" class="num">g CO2e per kWh</th><th scope="col" class="num">kg CO2e per billion tokens, reference row</th></tr></thead><tbody>
{years_rows}
  </tbody></table></div>
  <p class="note">{{{{EMBER_BASIS}}}} A GPU server draws much the same power around the clock, while an annual average weights each hour by its generation, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average.</p>
</section>

<section id="models">
  <p class="eyebrow">Every model</p>
  <h2>The index priced on {esc(name)}'s grid</h2>
  <p class="lead">Each model's lowest index row, GPU only, at the most energy-efficient configuration measured, multiplied by {fmt(g, 0)} gCO2e per kWh. The spread from the lowest row to the highest is {fmt(high_wh_raw / low_wh_raw, 0)}×, and it is entirely the model, the GPU and the load; the grid multiplies all of them alike.</p>
  <div class="table-scroll"><table><caption>Lowest index row per model, priced on {esc(name)}, {EMBER_YEAR}</caption>
  <thead><tr><th scope="col">Model</th><th scope="col" class="num">GPUs</th><th scope="col" class="num">Wh / M</th><th scope="col" class="num">kg CO2e per billion output tokens</th></tr></thead><tbody>
{model_rows}
  </tbody></table></div>
  <p class="note">Every configuration of every model, not only the lowest row, is on <a href="{{{{ROOT}}}}models/">the model pages</a>; the <a href="{{{{ROOT}}}}mcp/">MCP server</a> prices any of them on {esc(name)}'s grid for a token count you give it.</p>
</section>

<section id="reporting">
  <p class="eyebrow">Reporting</p>
  <h2>Which line it goes on</h2>
  <div class="prose">
    <p>For GPUs you run in {esc(name)}, the electricity is your own consumption: it goes into your ESRS E1-5 energy total and its emissions into E1-6 as Scope 2, location-based, which is the method this page's figure matches. The market-based figure nets your contracted supply and needs your own contracts. Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3 category 1, and sit outside your E1-5 line; <a href="{{{{ROOT}}}}why/#hosted">the why page</a> lists what to ask the provider. Ember's figure is a lifecycle intensity for comparing places, not a Scope 2 combustion factor to file as reported.</p>
  </div>
</section>
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">Grid intensity: <a href="https://ember-energy.org/data/yearly-electricity-data/">Ember, Yearly electricity data</a>, {EMBER_RELEASE}, emissions intensity of total generation, {', '.join(sorted(yrs))} (CC BY 4.0), retrieved {{{{EMBER_RETRIEVED_LONG}}}}. Energy per token: {{{{MLE_BLOCK}}}}</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
  <p class="note">This page is generated from the same dated snapshots as <a href="{{{{ROOT}}}}index/#carbon">the index</a>; no figure on it is typed by hand. All {{{{GRID_COUNT}}}} areas are in <a href="{{{{ROOT}}}}api/v1/grid.json">grid.json</a>; the {{{{LISTED_GRID_COUNT}}}} with a page are the markets Katonic sells in or expects to, plus seven reference grids.</p>
</section>"""
    title = f"{name}: carbon of AI inference per billion tokens | Lead Green"
    for desc in (f"{name}'s grid at {fmt(g, 0)} gCO2e/kWh ({EMBER_YEAR}, Ember): what a billion AI output tokens cost in CO2e there, every model on the index priced on it, and the trend since {min(yrs)}.",
                 f"{name}'s grid at {fmt(g, 0)} gCO2e/kWh: what a billion AI output tokens cost in CO2e there, every model on the index priced on it, and the trend.",
                 f"{name}: grid carbon intensity and the CO2e of AI inference per billion output tokens, every index model priced on it."):
        if len(desc) <= 155:
            break
    return title, desc, body, faq


REF_MODEL_NAME = ref["model"]
grid_cards = []
for iso_, _n in sorted(COUNTRIES, key=lambda t: -intensity[t[0]]):
    t_, d_, b_, faq_ = grid_page(iso_)
    a_ = _area_by_iso[iso_]
    render(f"grids/{grid_slug(iso_)}/index.html", "", t_, d_, "article", "answer", b_,
           {"date": UPDATED, "faq": faq_, "name": a_["display_name"], "crumbs": [("Grids", f"{SITE}/grids/")],
            "card": {"eyebrow": f"Grid carbon intensity · {EMBER_YEAR} · Ember", "value": fmt(intensity[iso_], 0), "unit": "gCO2e/kWh",
                     "label": f"{a_['display_name']}. {fmt(kg_per_billion(ref_wh_raw, intensity[iso_]))} kg CO2e per billion output tokens at the reference row; rank {_country_rank[iso_]} of {grid_count}."},
            "dataset": {"name": f"{a_['display_name']}: grid carbon intensity and AI inference carbon", "distribution": f"{SITE}/api/v1/grid.json", "isBasedOn": SRC_EMBER["url"]}})
    grid_cards.append(f"<div class=\"card\"><span class=\"k\">{esc(a_['continent'])}{' · reference' if iso_ in REFERENCE_GRIDS else ''}</span><h3><a href=\"{{{{ROOT}}}}grids/{grid_slug(iso_)}/\">{esc(a_['display_name'])}</a></h3>"
                      f"<span class=\"n\">{fmt(intensity[iso_], 0)}<small>gCO2e/kWh, {EMBER_YEAR}</small></span><p>{fmt(kg_per_billion(ref_wh_raw, intensity[iso_]))} kg CO2e per billion tokens at the reference row; rank {_country_rank[iso_]} of {grid_count}.</p></div>")
subs["GRID_CARDS"] = "\n".join(grid_cards)
meta_, body_ = read_body(PAGES / "grids.html")
render("grids/index.html", "", fill(meta_["title"], subs), fill(meta_["description"], subs), "website", "page", body_)


# ---- H100 vs B200
def compare_page() -> tuple[str, str, str, list[tuple[str, str]]]:
    ratios = sorted(r for _, _, _, r in pairs)
    med = ratios[len(ratios) // 2] if len(ratios) % 2 else (ratios[len(ratios) // 2 - 1] + ratios[len(ratios) // 2]) / 2
    wins = sum(1 for r in ratios if r > 1)
    pm, ph, pb, pr = pairs[0]
    lm, lh, lb, lr = pairs[-1]
    h100_w = [h["_cfg"]["avg_power_watts"] / h["_cfg"]["num_gpus"] for _, h, _, _ in pairs]
    b200_w = [b["_cfg"]["avg_power_watts"] / b["_cfg"]["num_gpus"] for _, _, b, _ in pairs]
    fewer = sum(1 for _, h, b, _ in pairs if b["_cfg"]["num_gpus"] < h["_cfg"]["num_gpus"])
    pct_less = (1 - 1 / med) * 100
    answer = (f"On the index the B200 uses a median <b>{pct_less:.0f} percent less</b> GPU energy per output token than the H100, "
              f"{'across all ' if wins == len(pairs) else f'winning {wins} of '}{len(pairs)} open-weight models measured on both cards: "
              f"the H100 row uses {med:.2f}× the B200 row's energy at the median, from <b>{pr:.2f}×</b> ({esc(pm)}) down to <b>{lr:.2f}×</b> ({esc(lm)}). "
              f"Part of many gaps is the sweep rather than the silicon: the two rows of a pair often differ in card count and running batch, and on {word(fewer)} of the {len(pairs)} pairs the B200 row holds the model on fewer cards.")
    tiles = (f"<div class=\"tiles auto n3\" role=\"group\" aria-label=\"Headline readings\">"
             f"<div class=\"tile\"><span class=\"lbl\">Widest gap</span><span class=\"val\">{pr:.2f}<small>×</small></span><span class=\"sub\">{esc(pm)}: {fmt(raw_wh(ph))} Wh/M on {ph['num_gpus']} × H100 against {fmt(raw_wh(pb))} on {pb['num_gpus']} × B200.</span></div>"
             f"<div class=\"tile ref\"><span class=\"lbl\">Median gap, {len(pairs)} pairs</span><span class=\"val\">{med:.2f}<small>×</small></span><span class=\"sub\">H100 row energy per token over B200 row energy per token, at each model's index rows.</span></div>"
             f"<div class=\"tile\"><span class=\"lbl\">Narrowest gap</span><span class=\"val\">{lr:.2f}<small>×</small></span><span class=\"sub\">{esc(lm)}: {fmt(raw_wh(lh))} Wh/M on {lh['num_gpus']} × H100 against {fmt(raw_wh(lb))} on {lb['num_gpus']} × B200.</span></div></div>")
    rows = "\n".join(
        f"<tr><th scope=\"row\"><a class=\"model\" href=\"{{{{ROOT}}}}models/{h['slug']}/\">{esc(m)}</a></th>"
        f"<td class=\"num\">{h['num_gpus']} × H100</td><td class=\"num\">{fmt(h['_cfg']['avg_batch_size'], 0)}</td><td class=\"num\">{fmt(raw_wh(h))}</td>"
        f"<td class=\"num\">{b['num_gpus']} × B200</td><td class=\"num\">{fmt(b['_cfg']['avg_batch_size'], 0)}</td><td class=\"num\">{fmt(raw_wh(b))}</td>"
        f"<td class=\"num key\">{r:.2f}×</td></tr>" for m, h, b, r in pairs)
    tdp = {(t["gpu"], t["form"]): t for t in hw["tdp"]}
    h_sxm = tdp.get(("H100", "SXM")); b_row = next(t for t in hw["tdp"] if t["gpu"] == "B200")
    power_para = (f"A B200 card draws more power than an H100: NVIDIA rates the H100 SXM at {h_sxm['tdp_label']} and the B200 {b_row['tdp_label']}, and on these index rows the cards averaged "
                  f"{fmt(sum(h100_w) / len(h100_w), 0)} W per H100 and {fmt(sum(b200_w) / len(b200_w), 0)} W per B200. It uses less energy per token because it finishes more tokens in each second of that draw. "
                  f"Power tells you the size of the feed; energy per token tells you what the feed produced.")
    faq = [
        ("Is the B200 more energy-efficient than the H100 for LLM inference?",
         f"On the ML.ENERGY Leaderboard's index rows, yes for {'all' if wins == len(pairs) else wins} {len(pairs)} models measured on both: " if wins == len(pairs) else f"On the ML.ENERGY Leaderboard's index rows, yes for {wins} of the {len(pairs)} models measured on both: "
         f"the H100 row uses {pr:.2f}× the GPU energy per output token of the B200 row for {pm} and {lr:.2f}× for {lm}, median {med:.2f}×, so the B200 uses about {pct_less:.0f} percent less at the median. "
         "These are floors at high load, GPU only, and part of each gap comes from the two rows being swept differently."),
        ("How much energy does a B200 save over an H100 per million tokens?",
         f"It depends on the model: for the reference model, {ref['model']}, the index rows are {fmt(raw_wh(ref))} Wh/M on {ref['num_gpus']} × H100 against {fmt(raw_wh(next(b for m, h, b, r in pairs if m == ref['model'])))} Wh/M on {next(b for m, h, b, r in pairs if m == ref['model'])['num_gpus']} × B200. The table on this page gives all {len(pairs)} pairs."),
        ("Does the B200 draw more power than the H100?", power_para),
        ("Should I buy B200s to cut the energy of AI inference?",
         f"Not first. The same model on the same H100 cards moves {subs['L32_RATIO']}× in energy per token between a running batch of {subs['L32_FIRST_BATCH']} and {subs['L32_BEST_BATCH']}, which is more than the widest generation gap here ({pr:.2f}×). Consolidating traffic onto fewer, busier cards costs nothing in hardware; the generation change comes after."),
        ("Why do the two rows of a pair have different card counts?",
         f"The leaderboard picks each GPU's configurations separately; a B200 has more memory, so a model that needs eight H100s can fit fewer B200s. On {fewer} of the {len(pairs)} pairs the B200 row holds the model on fewer cards, and the running batches differ too, so the ratio compares the best measured row on each card, not like for like."),
        ("Where do these figures come from?",
         f"The ML.ENERGY Leaderboard v3.0 (data compiled {long_date(SRC_MLE['compiled'])}, retrieved {long_date(RETRIEVED)}), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration at or under {ITL_DEADLINE_MS} ms median inter-token latency. TDP figures are NVIDIA's published specifications."),
    ]
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about H100 against B200</h2><div class=\"prose faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq) + "</div></section>"
    body = f"""<div class="title">
  <p class="eyebrow">Two generations · {len(pairs)} models</p>
  <h1>H100 vs B200: GPU energy per million output tokens</h1>
  <p class="stand">{answer}</p>
  <p class="unit"><b>Unit</b> watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. <b>Data</b> <a href="{{{{ROOT}}}}api/v1/index.json">index.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#pairs">The {len(pairs)} pairs</a></li><li><a href="#sweep">The sweep</a></li><li><a href="#power">Power against energy</a></li><li><a href="#faq">Questions</a></li><li><a href="#sources">Sources</a></li></ul>
</div>
{tiles}
<p class="after-tiles">Each pair compares a model's index row on the H100 with its index row on the B200: the lowest-energy configuration the leaderboard measured on each card, at or under {{{{ITL}}}} ms median inter-token latency. The ratio is the H100 row's energy per token over the B200 row's.</p>

<section id="pairs" class="first">
  <p class="eyebrow">The pairs</p>
  <h2>Every model measured on both cards</h2>
  <div class="table-scroll"><table><caption>Index rows paired by model, with card count and running batch, sorted by the gap</caption>
  <thead><tr><th scope="col">Model</th><th scope="col" class="num">H100</th><th scope="col" class="num">Running batch</th><th scope="col" class="num">Wh / M</th><th scope="col" class="num">B200</th><th scope="col" class="num">Running batch</th><th scope="col" class="num">Wh / M</th><th scope="col" class="num">H100 ÷ B200</th></tr></thead><tbody>
{rows}
  </tbody></table></div>
  <p class="note">Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's <code>num_requests_running</code>). Model names link to every measured configuration of that model.</p>
</section>

<section id="sweep">
  <p class="eyebrow">The sweep</p>
  <h2>How much of the gap is the silicon</h2>
  <p class="lead">{{{{PAIR_SWEEP_SENTENCE}}}}</p>
  <p class="lead">{{{{PAIR50_SENTENCE}}}}</p>
  <p class="note">Every configuration behind these rows is on <a href="{{{{ROOT}}}}models/">the model pages</a> and in the <a href="{{{{ROOT}}}}api/">API</a>, so any pair can be re-cut at a matched cap or a matched running batch.</p>
</section>

<section id="power">
  <p class="eyebrow">Power against energy</p>
  <h2>The card that draws more can use less</h2>
  <div class="prose"><p>{power_para} An eight-GPU {{{{SYS_NAME}}}} is rated at about {{{{SYS_KW}}}} kW against {{{{SYS_GPU_KW}}}} kW for its GPUs, so the system draws {{{{SYS_RATIO}}}}× what the cards do; the <a href="{{{{ROOT}}}}index/#method">method</a> takes a GPU figure to the facility meter.</p></div>
  <div class="table-scroll"><table class="spec"><caption>Maximum thermal design power, as published by NVIDIA</caption>
  <thead><tr><th scope="col">GPU</th><th scope="col">Form</th><th scope="col" class="num">Max TDP</th><th scope="col" class="num">Memory</th></tr></thead><tbody>
{{{{TDP_ROWS}}}}
  </tbody></table></div>
</section>
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">{{{{MLE_BLOCK}}}}</p>
  <p class="note">TDP and memory: NVIDIA product specifications for <a href="https://www.nvidia.com/en-us/data-center/h100/">H100</a> and <a href="https://www.nvidia.com/en-us/data-center/dgx-b200/">DGX B200</a>, and the <a href="https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf">HGX B200 product carbon footprint summary</a> (July 2025), retrieved {{{{RETRIEVED_LONG}}}}.</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
</section>"""
    title = f"H100 vs B200: which uses less GPU energy per token? {len(pairs)} models | Lead Green"
    desc = (f"B200 vs H100: the B200 uses a median {pct_less:.0f} percent less GPU energy per output token across {len(pairs)} open-weight models "
            f"({lr:.2f}× to {pr:.2f}×). ML.ENERGY v3.0.")
    return title, desc, body, faq


ct_, cd_, cb_, cfaq_ = compare_page()
render("h100-vs-b200/index.html", "", ct_, cd_, "article", "answer", cb_,
       {"date": UPDATED, "faq": cfaq_, "name": "H100 vs B200", "crumbs": [("The index", f"{SITE}/index/")],
        "card": {"eyebrow": f"H100 against B200 · {len(pairs)} models", "value": f"{_pair_med:.2f}", "unit": "×",
                 "label": f"Median gap at the index rows: the H100 row over the B200 row, from {pairs[0][3]:.2f}× down to {pairs[-1][3]:.2f}×."},
        "dataset": {"name": "H100 vs B200: GPU energy per million output tokens", "distribution": f"{SITE}/api/v1/index.json", "isBasedOn": SRC_MLE["url"]}})

# ----------------------------------------------------------------- GEO strategy 6.2: per-query bridge, glossary, FAQ hub (generated from the data)
# The page is the citation: each of these URLs answers one question in the words people type, first paragraph first,
# with the unit, the date and the source. Nothing here is typed by hand that the data can supply.

_ref_wh_per_answer = cfg_wh(ref["_cfg"]) * ref["_cfg"]["avg_output_len"] / 1e6
_wh_per_m_from_google = GOOGLE_2025["wh"] / ref["_cfg"]["avg_output_len"] * 1e6          # if Google's median prompt were 634 tokens long
_wh_per_m_from_google_narrow = GOOGLE_2025["narrow_wh"] / ref["_cfg"]["avg_output_len"] * 1e6
_aies_small, _aies_large = per_query_rows[0], per_query_rows[-1]
_aies_small_per_q = _aies_small["wh_per_1000_queries"] / 1000
_aies_large_per_q = _aies_large["wh_per_1000_queries"] / 1000
_aies_small_per_tok_wh_m = _aies_small_per_q / AIES_FIXED_TOKENS * 1e6     # the arithmetic a reader will do, shown so it can be refused
_bridge_rows = [
    ("Index, lowest row", low["model"], f"{low['num_gpus']} × {low['gpu']}", fmt(low["_cfg"]["avg_batch_size"], 0), raw_wh(low), low["_cfg"]["avg_output_len"], f"{{{{ROOT}}}}models/{low['slug']}/"),
    ("Index, reference row", ref["model"], f"{ref['num_gpus']} × {ref['gpu']}", fmt(ref["_cfg"]["avg_batch_size"], 0), raw_wh(ref), ref["_cfg"]["avg_output_len"], f"{{{{ROOT}}}}models/{ref['slug']}/"),
    ("Same row, lightly loaded", l32["model"], l32["gpus"], fmt(l32["first_batch"], 0), l32["first"], l32["first_out"], f"{{{{ROOT}}}}models/{ref['slug']}/"),
    ("Index, highest row", high["model"], f"{high['num_gpus']} × {high['gpu']}", fmt(high["_cfg"]["avg_batch_size"], 0), raw_wh(high), high["_cfg"]["avg_output_len"], f"{{{{ROOT}}}}models/{high['slug']}/"),
    ("Highest configuration measured", _hicfg["nickname"], f"{_hicfg['num_gpus']} × {_hicfg['gpu_model']}", fmt(_hicfg["avg_batch_size"], 0), cfg_wh(_hicfg), _hicfg["avg_output_len"], f"{{{{ROOT}}}}models/{next(s_ for s_, m_ in models.items() if m_['name'] == _hicfg['nickname'])}/"),
]


def per_query_page() -> tuple[str, str, str, list[tuple[str, str]]]:
    g = GOOGLE_2025
    assert abs(WHOLE_STACK_LO - min(g["wh"], EPOCH_2025["wh"], ALTMAN_2025["wh"])) < 1e-9
    lo_ans = raw_wh(low) * low["_cfg"]["avg_output_len"] / 1e6      # GPU share of one answer, lowest and highest index rows
    hi_ans = raw_wh(high) * high["_cfg"]["avg_output_len"] / 1e6
    answer = (f"An AI chatbot query uses about <b>{WHOLE_STACK_LO:g} to {WHOLE_STACK_HI:g} Wh</b> of electricity across the whole serving stack, by the three published "
              f"whole-stack figures: Google {g['wh']:g} Wh per median Gemini Apps text prompt ({g['date']}), Epoch AI {EPOCH_2025['wh']:g} Wh per typical "
              f"{EPOCH_2025['tokens']}-token ChatGPT reply ({EPOCH_2025['date']}) and OpenAI {ALTMAN_2025['wh']:g} Wh per average query ({ALTMAN_2025['date']}). "
              f"The GPU share of one answer on this index runs from <b>{lo_ans:.3f} to {hi_ans:.2f} Wh</b> by model and GPU, measured on busy servers. "
              f"One answer from a busy open-weight model costs about <b>{_ref_wh_per_answer:.3f} Wh</b> of GPU energy on the index's reference row "
              f"({esc(ref['model'])} on {ref['num_gpus']} × {ref['gpu']}: {fmt(raw_wh(ref))} Wh per million output tokens, answers averaging {fmt(ref['_cfg']['avg_output_len'], 0)} tokens, "
              f"{fmt(ref['_cfg']['avg_batch_size'], 0)} requests in flight). Of Google's {g['wh']:g} Wh the accelerators are {g['accelerator_share'] * 100:.0f} percent, "
              f"and its narrow accelerator-only figure is {g['narrow_wh']:.2f} Wh. "
              f"The gap between a per-prompt figure and a per-million-tokens figure is boundary, load and answer length, and this page converts one into the other with each of them stated.")
    tiles = (f"<div class=\"tiles auto n3\" role=\"group\" aria-label=\"Headline readings\">"
             f"<div class=\"tile ref\"><span class=\"lbl\">One answer, reference row</span><span class=\"val\">{_ref_wh_per_answer:.3f}<small>Wh</small></span><span class=\"sub\">{esc(ref['model'])}, {ref['num_gpus']} × {ref['gpu']}, {fmt(raw_wh(ref))} Wh/M × {fmt(ref['_cfg']['avg_output_len'], 0)} output tokens. GPU only, busy server, a floor.</span></div>"
             f"<div class=\"tile\"><span class=\"lbl\">Google, median prompt</span><span class=\"val\">{g['wh']:g}<small>Wh</small></span><span class=\"sub\">Gemini Apps text prompt, {g['date']}, whole stack: accelerators {g['accelerator_share'] * 100:.0f} percent ({g['wh'] * g['accelerator_share']:.2f} Wh), narrow accelerator-only figure {g['narrow_wh']:.2f} Wh.</span></div>"
             f"<div class=\"tile\"><span class=\"lbl\">AI Energy Score, one query</span><span class=\"val\">{_aies_small_per_q:.4f}<small>to {_aies_large_per_q:.2f} Wh</small></span><span class=\"sub\">{len(per_query_rows)} models, batch size 1, answers fixed at {word(AIES_FIXED_TOKENS)} tokens, H100 80GB, December 2025 round. A probe, not a serving load.</span></div></div>")
    bridge_rows = "\n".join(
        f"<tr><th scope=\"row\">{esc(lbl)}</th><td><a class=\"model\" href=\"{href}\">{esc(mn)}</a></td><td class=\"num\">{esc(gp)}</td><td class=\"num\">{bt}</td>"
        f"<td class=\"num\">{fmt(whm)}</td><td class=\"num\">{fmt(out, 0)}</td><td class=\"num key\">{whm * out / 1e6:.3f}</td></tr>"
        for lbl, mn, gp, bt, whm, out, href in _bridge_rows)
    aies_rows = "\n".join(
        f"<tr><th scope=\"row\">{cl}</th><td>{esc(per_query_json_classes[cl])}</td><td class=\"num\">{d['count']}</td><td class=\"num\">{fmt(d['lo'])} to {fmt(d['hi'])}</td><td class=\"num key\">{d['lo'] / 1000:.4f} to {d['hi'] / 1000:.3f}</td></tr>"
        for cl, d in sorted(aies_class.items()))
    faq = [
        ("How much energy does an AI query use?",
         f"About {WHOLE_STACK_LO:g} to {WHOLE_STACK_HI:g} Wh across the whole serving stack, by the published figures from Google ({g['wh']:g} Wh, {g['date']}), "
         f"Epoch AI ({EPOCH_2025['wh']:g} Wh, {EPOCH_2025['date']}) and OpenAI ({ALTMAN_2025['wh']:g} Wh, {ALTMAN_2025['date']}). "
         f"Below that headline it depends on the model, the GPUs, how busy the server is and how long the answer runs, so a single figure needs those four stated. On the index's reference row ({ref['model']} on {ref['num_gpus']} × {ref['gpu']}, {fmt(raw_wh(ref))} Wh per million output tokens, {fmt(ref['_cfg']['avg_batch_size'], 0)} requests in flight), one answer of {fmt(ref['_cfg']['avg_output_len'], 0)} tokens costs about {_ref_wh_per_answer:.3f} Wh of GPU energy. "
         f"The same model on the same cards holding {fmt(l32['first_batch'], 0)} requests costs about {l32['first'] * l32['first_out'] / 1e6:.2f} Wh an answer. Google's published median for a Gemini Apps text prompt is {g['wh']:g} Wh across the whole serving stack ({g['date']}). These figures are GPU energy from a busy server unless stated otherwise; host, network and cooling sit outside them."),
        ("Why is Google's 0.24 Wh per prompt higher than the index's figure?",
         f"Mostly boundary. Google counts the whole stack: the accelerators are {g['accelerator_share'] * 100:.0f} percent of its {g['wh']:g} Wh, about {g['wh'] * g['accelerator_share']:.2f} Wh, with host machines, idle capacity held for peaks and data-centre overhead making up the rest, and it also publishes a narrow accelerator-only figure of {g['narrow_wh']:.2f} Wh. The index counts GPU energy only, at steady state on a busy server. "
         f"On the narrow boundary Google's prompt is {g['narrow_wh'] / _ref_wh_per_answer:.1f}× the reference row's answer, and the two measure different models, loads and answer lengths. Neither figure is wrong; they answer different questions."),
        ("How do I convert watt-hours per prompt into watt-hours per million tokens?",
         f"Divide the energy per answer by the answer's output tokens and multiply by a million: Wh/M = Wh per answer ÷ output tokens × 1,000,000. The reverse is Wh per answer = Wh/M × output tokens ÷ 1,000,000; the reference row's {fmt(raw_wh(ref))} Wh/M × {fmt(ref['_cfg']['avg_output_len'], 0)} tokens gives {_ref_wh_per_answer:.3f} Wh. "
         f"The conversion only holds when both figures share a boundary and a load. A per-prompt figure with no output length cannot be converted; Google's {g['wh']:g} Wh would read {fmt(_wh_per_m_from_google, 0)} Wh/M at the reference row's answer length and {fmt(_wh_per_m_from_google_narrow, 0)} Wh/M on its narrow boundary, but Google does not publish the prompt's token count, so those are illustrations, not figures."),
        ("Can the AI Energy Score's Wh per 1,000 queries be converted to Wh per million tokens?",
         f"No. The AI Energy Score runs one query at a time (batch size 1) with the answer fixed at {word(AIES_FIXED_TOKENS)} tokens for non-reasoning models, so the arithmetic ({_aies_small['model']}: {fmt(_aies_small['wh_per_1000_queries'])} Wh per 1,000 queries ÷ 1,000 ÷ {AIES_FIXED_TOKENS} tokens × 1,000,000 = {fmt(_aies_small_per_tok_wh_m, 0)} Wh/M) describes an idle card answering a ten-token probe, not a serving workload. "
         f"The index keeps the AI Energy Score as a per-query measurement in its own table and does not mix the two units. The ML.ENERGY rows, measured on a busy server, are the ones in Wh/M."),
        ("Does how busy the server is change the energy of one query?",
         f"More than anything else. {l32['model']} on {l32['gpus']} goes from {fmt(l32['best'])} Wh/M at a running batch of {fmt(l32['best_batch'], 0)} to {fmt(l32['first'], 0)} Wh/M at {fmt(l32['first_batch'], 0)}, {l32['ratio']:.1f}× on the same hardware, because the cards draw only {fmt(l32['power_pct'], 0)} percent more power serving {fmt(l32['best_batch'], 0)} requests than {fmt(l32['first_batch'], 0)}. "
         f"One answer goes from {_ref_wh_per_answer:.3f} Wh to about {l32['first'] * l32['first_out'] / 1e6:.2f} Wh. A department assistant with a few users at a time sits at the top of that range."),
        ("What about the carbon and water of one query?",
         f"Google puts the median Gemini Apps text prompt at {g['g_co2e']:g} g CO2e and {g['water_ml']:g} mL of water ({g['date']}); Mistral puts a {MISTRAL_2025['tokens']:,}-token reply from its large model at {MISTRAL_2025['g_co2e']:g} g CO2e and {MISTRAL_2025['water_ml']:g} mL (July 2025), without a watt-hour figure. "
         f"For GPU-side carbon on the index, multiply Wh per answer by the grid's gCO2e per kWh: the reference row's answer carries about {_ref_wh_per_answer * intensity['SAU'] / 1000:.3f} g on Saudi Arabia's {EMBER_YEAR} grid ({fmt(intensity['SAU'], 0)} gCO2e per kWh) and {_ref_wh_per_answer * intensity['NOR'] / 1000:.4f} g on Norway's ({fmt(intensity['NOR'], 0)}). The index measures electricity, not water."),
    ]
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about the energy of one query</h2><div class=\"prose faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq) + "</div></section>"
    body = f"""<div class="title">
  <p class="eyebrow"><a href="{{{{ROOT}}}}index/">The index</a> · Per query</p>
  <h1>How much energy does an AI query use?</h1>
  <p class="stand">{answer}</p>
  <p class="unit"><b>Units</b> watt-hours per answer (Wh) and watt-hours per million output tokens (Wh/M). Wh per answer = Wh/M × output tokens ÷ 1,000,000. <b>Data</b> <a href="{{{{ROOT}}}}api/v1/index.json">index.json</a>, <a href="{{{{ROOT}}}}api/v1/per-query.json">per-query.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#bridge">The bridge</a></li><li><a href="#published">What vendors published</a></li><li><a href="#batch-one">Batch size one</a></li><li><a href="#budget">To a budget</a></li><li><a href="#faq">Questions</a></li><li><a href="#sources">Sources</a></li></ul>
</div>
{tiles}
<p class="after-tiles">Three kinds of figure are quoted as "the energy of an AI query", and they do not share a boundary or a load. The index's rows are GPU energy per million output tokens from a busy server. Vendors' per-prompt figures count a whole serving estate. The AI Energy Score runs one query at a time with a fixed ten-token answer. Each is a real measurement; the table below puts the first kind in per-answer units so it can sit beside the others.</p>

<section id="bridge" class="first">
  <p class="eyebrow">The bridge</p>
  <h2>From watt-hours per million tokens to watt-hours per answer</h2>
  <p class="lead">Energy per answer is energy per token times the answer's length. Each row below takes a measured Wh/M figure and the average output length the benchmark recorded on that row, and multiplies them. The result is what one average answer on that row cost in GPU energy.</p>
  <div class="table-scroll"><table><caption>Measured rows converted to GPU watt-hours per answer, using each row's own average output length</caption>
  <thead><tr><th scope="col">Row</th><th scope="col">Model</th><th scope="col" class="num">GPUs</th><th scope="col" class="num">Running batch</th><th scope="col" class="num">Wh / M</th><th scope="col" class="num">Output tokens</th><th scope="col" class="num">Wh per answer</th></tr></thead><tbody>
{bridge_rows}
  </tbody></table></div>
  <p class="note">Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's <code>num_requests_running</code>). The first four rows are index rows or ladder rows at or under the {{{{ITL}}}} ms median inter-token latency ceiling; the last is the highest-energy configuration the leaderboard measured at all, kept to show the range a lightly loaded large model can reach. A kilowatt-hour serves about {{{{REF_ANSWERS_PER_KWH}}}} answers at the reference row.</p>
</section>

<section id="published">
  <p class="eyebrow">What vendors published</p>
  <h2>Two per-prompt disclosures, and what they count</h2>
  <div class="prose">
    <p>In {g['date']} Google put the median Gemini Apps text prompt at <b>{g['wh']:g} Wh</b>, {g['g_co2e']:g} g CO2e and {g['water_ml']:g} mL of water. The figure counts the whole serving stack: the accelerators are {g['accelerator_share'] * 100:.0f} percent of it, about {g['wh'] * g['accelerator_share']:.2f} Wh, and the host machines, idle capacity held for peaks and the data centre's overhead make up the rest. Google also reports a narrow, accelerator-only figure of {g['narrow_wh']:.2f} Wh, which is the boundary this index uses. So Google's own numbers say the stack multiplies the accelerator figure by {1 / g['accelerator_share']:.1f}× to {g['wh'] / g['narrow_wh']:.1f}×, depending on which accelerator figure is the base.</p>
    <p>In July 2025 Mistral put a {MISTRAL_2025['tokens']:,}-token reply from its large model at {MISTRAL_2025['g_co2e']:g} g CO2e and {MISTRAL_2025['water_ml']:g} mL of water, without a watt-hour figure, so it cannot be placed on an energy axis at all.</p>
    <p>Neither disclosure states the model's serving load or the prompt's output length, so neither converts to watt-hours per million tokens. Set beside the index on the narrow boundary, Google's {g['narrow_wh']:.2f} Wh is {g['narrow_wh'] / _ref_wh_per_answer:.1f}× the reference row's {_ref_wh_per_answer:.3f} Wh answer; the rest of the difference is a different model, a different load and an unstated answer length. Google's figure tells a hyperscaler's customers what a prompt costs across its estate. The index tells a buyer what a named model on named GPUs costs at a stated load, which is the figure a vendor can be held to because the buyer can measure it.</p>
  </div>
</section>

<section id="batch-one">
  <p class="eyebrow">Batch size one</p>
  <h2>The AI Energy Score measures a probe, not a serving load</h2>
  <p class="lead">The AI Energy Score reports GPU watt-hours for 1,000 text-generation queries run one at a time on NVIDIA H100 80GB GPUs, with the answer fixed at {word(AIES_FIXED_TOKENS)} tokens for non-reasoning models. Per query, its {len(per_query_rows)} December 2025 rows run from {_aies_small_per_q:.4f} Wh ({esc(_aies_small['model'])}) to {_aies_large_per_q:.2f} Wh ({esc(_aies_large['model'])}). The index carries all of them in their own unit and does not convert them.</p>
  <div class="table-scroll"><table><caption>AI Energy Score, text generation, December 2025 round, by class</caption>
  <thead><tr><th scope="col">Class</th><th scope="col">Fits</th><th scope="col" class="num">Models</th><th scope="col" class="num">Wh per 1,000 queries</th><th scope="col" class="num">Wh per query</th></tr></thead><tbody>
{aies_rows}
  </tbody></table></div>
  <p class="note">Dividing a batch-size-one figure by its ten tokens gives an energy per token for a card that is mostly waiting ({esc(_aies_small['model'])} would read {fmt(_aies_small_per_tok_wh_m, 0)} Wh/M), which is why the index refuses the conversion. Every row, with its star rating, is on <a href="{{{{ROOT}}}}index/#per-query">the index</a> and in <a href="{{{{ROOT}}}}api/v1/per-query.json">per-query.json</a>.</p>
</section>

<section id="budget">
  <p class="eyebrow">To a budget</p>
  <h2>Per answer is for intuition; per million tokens is for the plan</h2>
  <div class="prose">
    <p>A per-answer figure makes the number legible: {_ref_wh_per_answer:.3f} Wh is a {{{{LED_W}}}} W LED bulb for about {{{{REF_ANSWER_LED_SECONDS}}}} seconds (the bulb is a stated assumption, the tokens are measured). A budget needs the per-token form, because tokens are what the invoice counts. Monthly output tokens × Wh/M gives watt-hours; at the reference row a megawatt-hour of GPU energy serves {{{{TOKENS_PER_MWH_REF_B}}}} billion output tokens, and at the top of the concurrency ladder the same megawatt-hour serves {{{{TOKENS_PER_MWH_TOP_B}}}} billion.</p>
    <p>To take either figure to the facility meter, multiply by the system-to-GPU power ratio ({{{{SYS_RATIO}}}} for a {{{{SYS_NAME}}}}) and the site's PUE; with a PUE of {{{{PUE_EXAMPLE}}}} the reference row's {{{{REF_WH_1}}}} Wh/M becomes about {{{{METER_WH}}}} Wh/M at the meter. Both multipliers are the operator's own. The <a href="{{{{ROOT}}}}glossary/gpu-only-boundary/">GPU-only boundary</a> entry explains what sits inside and outside each figure.</p>
  </div>
</section>
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">{{{{MLE_BLOCK}}}} Per-answer figures are Wh per million output tokens multiplied by the row's own average output length.</p>
  <p class="note">Elsworth et al., Measuring the environmental impact of delivering AI at Google Scale, Google, {g['date']}: {g['wh']:g} Wh, {g['g_co2e']:g} g CO2e and {g['water_ml']:g} mL per median Gemini Apps text prompt; accelerators {g['accelerator_share'] * 100:.0f} percent; narrow boundary {g['narrow_wh']:.2f} Wh. <a href="{g['url']}">arXiv 2508.15734</a>, retrieved {{{{RETRIEVED_LONG}}}}. Mistral AI, Our contribution to a global environmental standard for AI, July 2025 (with Carbone 4 and ADEME): {MISTRAL_2025['g_co2e']:g} g CO2e and {MISTRAL_2025['water_ml']:g} mL per {MISTRAL_2025['tokens']:,}-token reply. <a href="{MISTRAL_2025['url']}">mistral.ai</a>, retrieved {{{{RETRIEVED_LONG}}}}. Epoch AI, How much energy does ChatGPT use?, {EPOCH_2025['date']}: about {EPOCH_2025['wh']:g} Wh per typical {EPOCH_2025['tokens']}-token GPT-4o reply, whole stack. <a href="{EPOCH_2025['url']}">epoch.ai</a>, retrieved 21 October 2026. Sam Altman, The Gentle Singularity, OpenAI, {ALTMAN_2025['date']}: about {ALTMAN_2025['wh']:g} Wh per average ChatGPT query, whole stack, no method given. <a href="{ALTMAN_2025['url']}">blog.samaltman.com</a>, retrieved 21 October 2026.</p>
  <p class="note"><a href="{SRC_AIES['url']}">{SRC_AIES['name']}</a> ({SRC_AIES['publisher']}), {SRC_AIES['version']}, retrieved {{{{RETRIEVED_LONG}}}}: {SRC_AIES['used_for']}. Grid intensity in the carbon question: Ember, Yearly electricity data, {EMBER_RELEASE}, {EMBER_YEAR}.</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
</section>"""
    title = "How much energy does an AI query use? Per prompt against per million tokens | Lead Green"
    desc = (f"An AI query uses about {WHOLE_STACK_LO:g} to {WHOLE_STACK_HI:g} Wh by Google's, Epoch AI's and OpenAI's whole-stack figures; "
            f"the GPU share on this index is {lo_ans:.3f} to {hi_ans:.2f} Wh an answer.")
    return title, desc, body, faq


per_query_json_classes = api_docs["per-query.json"]["classes"]
pq_t, pq_d, pq_b, pq_faq = per_query_page()
render("per-query/index.html", "index", pq_t, pq_d, "article", "answer", pq_b,
       {"date": UPDATED, "faq": pq_faq, "name": "Per query", "crumbs": [("The index", f"{SITE}/index/")],
        "card": {"eyebrow": "One answer, reference row", "value": f"{_ref_wh_per_answer:.3f}", "unit": "Wh",
                 "label": f"{ref['model']} on {ref['num_gpus']} × {ref['gpu']}: {fmt(raw_wh(ref))} Wh/M × {fmt(ref['_cfg']['avg_output_len'], 0)} output tokens. Google's median prompt: {GOOGLE_2025['wh']:g} Wh, whole stack."},
        "dataset": {"name": "AI inference energy per query and per million output tokens", "distribution": f"{SITE}/api/v1/per-query.json",
                    "isBasedOn": [SRC_MLE["url"], SRC_AIES["url"], GOOGLE_2025["url"]]}})


# ---- glossary: one URL per term, the figure and the source in the first paragraph
def _term(slug_, name, short, definition, working, used, faq, tiles=None):
    return {"slug": slug_, "name": name, "short": short, "definition": definition, "working": working, "used": used, "faq": faq, "tiles": tiles or [], "answer": ""}


_sys_row = hw["systems"][0]
GLOSSARY = [
    _term("watt-hours-per-million-output-tokens", "Watt-hours per million output tokens (Wh/M)",
          "The unit of the index: the GPU energy, in watt-hours, that a serving configuration uses to generate one million output tokens.",
          f"<b>Watt-hours per million output tokens (Wh/M)</b> is the GPU energy, in watt-hours, that a model on a stated set of GPUs at a stated load uses to generate one million output tokens. One Wh/M equals 0.0036 joules per output token (joules per token × 1,000,000 ÷ 3,600 = Wh/M). On the index the unit runs from <b>{fmt(raw_wh(low))} Wh/M</b> ({esc(low['model'])}, {low['num_gpus']} × {low['gpu']}) to <b>{fmt(raw_wh(high))} Wh/M</b> ({esc(high['model'])}, {high['num_gpus']} × {high['gpu']}), GPU only, at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for each model and GPU (data compiled {long_date(SRC_MLE['compiled'])}).",
          f"<p>The same number reads three ways without conversion: Wh per million tokens equals kWh per billion tokens equals MWh per trillion tokens. The reference row, {esc(ref['model'])} on {ref['num_gpus']} × {ref['gpu']}, is {fmt(raw_wh(ref))} Wh/M, so a billion of its tokens take {fmt(raw_wh(ref))} kWh of GPU energy and a trillion take {fmt(raw_wh(ref))} MWh. Multiply by the grid's gCO2e per kWh and divide by 1,000 for kg CO2e per billion tokens: {fmt(raw_wh(ref))} × {fmt(intensity['SAU'], 0)} ÷ 1,000 = {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg on Saudi Arabia's {EMBER_YEAR} grid.</p>"
          f"<p>The unit is chosen over joules per token because procurement, capacity planning and sustainability reporting all work in watt-hours and tokens, and over watt-hours per query because a query has no fixed length. It is an output-token unit: prompt processing is included in the energy but the prompt's tokens are not in the denominator, which is how the leaderboard measures it. It says nothing about the host, the network, cooling or idle time; see the <a href=\"{{{{ROOT}}}}glossary/gpu-only-boundary/\">GPU-only boundary</a>.</p>",
          [("The index", "index/"), ("Every model page", "models/"), ("How much energy does an AI query use?", "per-query/")],
          [("What does Wh/M mean?", f"Watt-hours per million output tokens: the GPU energy a serving configuration uses to generate a million output tokens. One Wh/M is 0.0036 joules per token. The index runs from {fmt(raw_wh(low))} to {fmt(raw_wh(high))} Wh/M across {len(index_rows)} rows and {len({r['model'] for r in index_rows})} models, GPU only, each row the lowest-energy configuration measured at or under a {ITL_DEADLINE_MS} ms median inter-token latency."),
           ("How do I convert joules per token to watt-hours per million tokens?", f"Multiply joules per token by 1,000,000 and divide by 3,600. The reference row's {ref['_cfg']['energy_per_token_joules']:.4f} J per token becomes {fmt(raw_wh(ref))} Wh/M. The reverse is Wh/M × 0.0036 = J per token."),
           ("Is Wh per million tokens the same as kWh per billion tokens?", f"Yes, and the same as MWh per trillion tokens; the three scale together. {fmt(raw_wh(ref))} Wh/M is {fmt(raw_wh(ref))} kWh per billion and {fmt(raw_wh(ref))} MWh per trillion output tokens."),
           ("Does the unit include the prompt?", "The energy includes prompt processing, because the benchmark divides steady-state GPU energy by the output tokens generated in the window; the denominator counts output tokens only. A long-prompt workload therefore shows a higher Wh/M than a short-prompt one for the same answers.")],
          [("Lowest on the index", fmt(raw_wh(low)), "Wh/M", f"{esc(low['model'])}, {low['num_gpus']} × {low['gpu']}"),
           ("Reference row", fmt(raw_wh(ref)), "Wh/M", f"{esc(ref['model'])}, {ref['num_gpus']} × {ref['gpu']}"),
           ("Highest on the index", fmt(raw_wh(high)), "Wh/M", f"{esc(high['model'])}, {high['num_gpus']} × {high['gpu']}")]),
    _term("energy-per-token", "Energy per token",
          "GPU energy divided by the output tokens generated in the same steady-state window, in joules per token; the quantity the index converts to Wh/M.",
          f"<b>Energy per token</b> is the GPU energy a serving system uses divided by the output tokens it generated in the same window, in joules per output token. The ML.ENERGY Leaderboard v3.0 measures it as steady-state GPU energy divided by the output tokens generated in the steady-state window, read from the device with Zeus under vLLM on H100 and B200 servers (data compiled {long_date(SRC_MLE['compiled'])}). On the index it runs from <b>{low['_cfg']['energy_per_token_joules']:.3f} J per token</b> ({esc(low['model'])}, {low['num_gpus']} × {low['gpu']}) to <b>{high['_cfg']['energy_per_token_joules']:.2f} J</b> ({esc(high['model'])}, {high['num_gpus']} × {high['gpu']}); the index shows it as watt-hours per million output tokens.",
          f"<p>Energy per token is average power divided by token throughput: on the reference row, {{{{CONS_W}}}} W summed across {ref['num_gpus']} cards ÷ {{{{CONS_TPS}}}} output tokens per second = {ref['_cfg']['energy_per_token_joules']:.4f} J per token, which is {{{{CONS_WH}}}} Wh/M. The identity is also the consistency check the <a href=\"{{{{ROOT}}}}why/#monday\">RFP scoring box</a> applies to a bidder's figure.</p>"
          f"<p>Three ways of getting the number are not equal. A measured figure reads the GPU's energy counter (NVIDIA NVML or DCGM, which Zeus uses) over a window of steady load and divides by the tokens served. A whole-system figure reads the server's power supplies and includes host, memory, network and fans, which on a {esc(_sys_row['system'])} adds about {{{{SYS_RATIO}}}}× to the GPU figure. An estimate multiplies a rated power (TDP) by an assumed utilisation and divides by an assumed throughput; it is the kind most often quoted and the kind the index does not publish. Energy per token falls as the running batch rises because the cards' fixed draw is spread over more tokens: see <a href=\"{{{{ROOT}}}}glossary/running-batch/\">running batch</a>.</p>",
          [("The index method", "index/#method"), ("Why it matters: utilisation", "why/#utilisation"), ("The measurement protocol", "contribute/#protocol")],
          [("What is energy per token?", f"GPU energy divided by the output tokens generated in the same steady-state window, in joules per output token. The index measures it from the ML.ENERGY Leaderboard v3.0 and shows it as watt-hours per million output tokens; it runs from {low['_cfg']['energy_per_token_joules']:.3f} to {high['_cfg']['energy_per_token_joules']:.2f} J per token across the index rows."),
           ("How is energy per token measured?", f"By reading the GPU's energy counter (through NVML or DCGM; the leaderboard uses Zeus) at the start and end of a steady-state window under a fixed load, and dividing the difference by the output tokens generated in that window. The index's protocol asks for a window of at least {PROTO_MIN_MINUTES} minutes after warm-up and at least {PROTO_MIN_REQUESTS:,} requests. Average power divided by tokens per second gives the same number."),
           ("Why do estimates of energy per token differ so much from measurements?", f"Estimates multiply a rated power by an assumed utilisation and divide by an assumed throughput, usually a single request at a time. A busy server serves hundreds of requests at once on nearly the same power: {ref['model']} on {ref['num_gpus']} × {ref['gpu']} moves {l32['ratio']:.1f}× in energy per token between a running batch of {fmt(l32['first_batch'], 0)} and {fmt(l32['best_batch'], 0)}. An estimate at one request per card lands far above every measured busy-server row."),
           ("Does energy per token include the host, the network and cooling?", f"Not on this index. The figures are GPU energy only. A whole-system reading adds the host, memory, network and fans (about {sys_ratio:.2f}× for a {_sys_row['system']}, from NVIDIA's rated system and GPU power), and the facility's PUE adds cooling and distribution on top.")]),
    _term("running-batch", "Running batch",
          "The average number of requests a serving engine was decoding at once over the measurement window; the variable that moves energy per token most.",
          f"<b>Running batch</b> is the average number of requests a serving engine was actually decoding at the same time over the steady-state window, which vLLM reports as <code>num_requests_running</code>. It is not the cap the operator set (vLLM's <code>max_num_seqs</code>) and it does not count requests waiting in the queue. On the index, raising the running batch of {esc(l32['model'])} on {l32['gpus']} from <b>{fmt(l32['first_batch'], 0)} to {fmt(l32['best_batch'], 0)}</b> cuts energy per token from <b>{fmt(l32['first'], 0)} to {fmt(l32['best'])} Wh/M</b>, {l32['ratio']:.1f}× on the same hardware (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled {long_date(SRC_MLE['compiled'])}).",
          f"<p>The mechanism is fixed draw spread over more work. Between those two rows the cards' power rises {fmt(l32['power_pct'], 0)} percent, from {fmt(l32['first_w'], 0)} W to {fmt(l32['best_w'], 0)} W, while output throughput rises {l32['tps_ratio']:.1f}×, from {fmt(l32['first_tps'], 0)} to {fmt(l32['best_tps'], 0)} tokens per second. Energy per token is power over throughput, so it falls by nearly the whole throughput gain. Median inter-token latency rises from {fmt(l32['first_itl'], 0)} ms to {fmt(l32['best_itl'], 0)} ms over the same range, far under the {ITL_DEADLINE_MS} ms ceiling.</p>"
          f"<p>Running batch, not cap, is the figure to ask a vendor for, because a cap of 256 with eight users is a running batch of eight. The <a href=\"{{{{ROOT}}}}why/#monday\">RFP clause</a> asks for both, and the index's <a href=\"{{{{ROOT}}}}contribute/#protocol\">protocol</a> reports both. The full ladder, {l32['count']} configurations, is on <a href=\"{{{{ROOT}}}}index/#concurrency\">the index</a> and the <a href=\"{{{{ROOT}}}}models/{ref['slug']}/\">model's page</a>.</p>",
          [("The concurrency ladder", "index/#concurrency"), ("Why it matters: utilisation", "why/#utilisation"), ("The RFP clause", "why/#monday")],
          [("What is running batch?", f"The average number of requests a serving engine was decoding at once over the measurement window (vLLM's num_requests_running). It is not the configured cap and it excludes queued requests. The index reports it on every row because it is the variable that moves energy per token most: {l32['ratio']:.1f}× for {l32['model']} on {l32['gpus']} between {fmt(l32['first_batch'], 0)} and {fmt(l32['best_batch'], 0)}."),
           ("Why does an idle GPU use more energy per token than a busy one?", f"Because a GPU's power does not fall in step with its work. On the index, {l32['model']} on {l32['gpus']} draws {fmt(l32['first_w'], 0)} W serving {fmt(l32['first_batch'], 0)} requests at once and {fmt(l32['best_w'], 0)} W serving {fmt(l32['best_batch'], 0)}, {fmt(l32['power_pct'], 0)} percent more power for {l32['tps_ratio']:.1f}× the tokens per second. Energy per token is power over throughput, so the lightly loaded server uses {l32['ratio']:.1f}× the energy per token: {fmt(l32['first'], 0)} against {fmt(l32['best'])} Wh/M. A fully idle GPU produces no tokens, so its energy per token is undefined, and its draw is pure overhead."),
           ("What is the difference between running batch and batch size?", "Batch size is usually a configured limit (the cap, vLLM's max_num_seqs) or a fixed count in an offline benchmark. Running batch is what the server actually held on average under a live load, which is lower whenever demand is below the cap. The AI Energy Score's batch size of one is a fixed count; the index's running batch is a measurement."),
           ("What running batch should I ask a vendor to measure at?", "The one you expect in production, stated as a number, with the median and p99 inter-token latency your users will accept. The same running batch and latency limit for every bidder makes the figures comparable; the index's rows give the floor to hold each answer against.")],
          [("Lightly loaded", fmt(l32["first"], 0), "Wh/M", f"{esc(l32['model'])}, {l32['gpus']}, running batch {fmt(l32['first_batch'], 0)}"),
           ("Busy", fmt(l32["best"]), "Wh/M", f"Same model, same cards, running batch {fmt(l32['best_batch'], 0)}"),
           ("Same hardware", f"{l32['ratio']:.1f}", "×", f"Power up {fmt(l32['power_pct'], 0)} percent, throughput up {l32['tps_ratio']:.1f}×")]),
    _term("floor", "Floor",
          "What every index row is: the lowest GPU energy per token measured for a model and GPU under the latency ceiling, which a real deployment sits above.",
          f"<b>A floor</b> is what every row on the index is: the lowest GPU energy per output token the ML.ENERGY Leaderboard v3.0 measured for a model on a GPU, among configurations whose median inter-token latency is at or under {ITL_DEADLINE_MS} ms, at high concurrency on a busy server (data compiled {long_date(SRC_MLE['compiled'])}). A real deployment sits above its floor, often far above it: the reference row, {esc(ref['model'])} on {ref['num_gpus']} × {ref['gpu']}, is <b>{fmt(raw_wh(ref))} Wh/M</b> at a running batch of {fmt(ref['_cfg']['avg_batch_size'], 0)}, and the same model on the same cards measured <b>{fmt(l32['first'], 0)} Wh/M</b> at a running batch of {fmt(l32['first_batch'], 0)}.",
          f"<p>The word is chosen so that the rows are read the right way round. A floor is not a typical figure and not a target; it is the best the benchmark found, and it tells a buyer the lowest number a vendor could honestly report for that model on that GPU. An answer below the floor is the one to question: the <a href=\"{{{{ROOT}}}}why/#monday\">RFP scoring box</a> challenges any figure more than {CHALLENGE_TOLERANCE_PCT} percent under it and asks for the raw power and engine logs.</p>"
          f"<p>Floors move with the ceiling that defines them. At {ITL_DEADLINE_MS} ms no measured configuration is excluded; {subs['SENS_SENTENCE'][0].lower() + subs['SENS_SENTENCE'][1:]} None of those tighter ceilings is applied to the index. Above the floors sit every other measured configuration, {len(cfgs)} in all, on the <a href=\"{{{{ROOT}}}}models/\">model pages</a>; the highest the leaderboard measured is {esc(_hicfg['nickname'])} on {_hicfg['num_gpus']} × {_hicfg['gpu_model']} at {fmt(cfg_wh(_hicfg), 0)} Wh/M, holding {fmt(_hicfg['avg_batch_size'], 0)} requests.</p>",
          [("The index", "index/"), ("The index method", "index/#method"), ("Scoring RFP answers", "why/#monday")],
          [("What does the index mean by a floor?", f"The lowest GPU energy per output token measured for a model and GPU among configurations at or under a {ITL_DEADLINE_MS} ms median inter-token latency, at high concurrency. Every index row is one. A deployment sits above its floor; {ref['model']} on {ref['num_gpus']} × {ref['gpu']} is {fmt(raw_wh(ref))} Wh/M at its floor and {fmt(l32['first'], 0)} Wh/M at a running batch of {fmt(l32['first_batch'], 0)}."),
           ("Is the floor what my deployment will use?", f"No. It is the best measured configuration on a busy server, GPU only. Your figure depends on your running batch, your prompt and answer lengths, your precision and your card count, and sits above the floor; the model pages show how far above at each measured load."),
           ("What should I do with a vendor figure below the floor?", f"Ask for the measurement: the running batch held, the latency over the window, the method, the tool and the logs. The index's scoring method challenges any answer more than {CHALLENGE_TOLERANCE_PCT} percent below the floor for the same model and GPU; the measurement protocol's own repeat threshold is {REPEAT_THRESHOLD_PCT} percent."),
           ("Does the floor change if the latency ceiling changes?", f"It can. At {ITL_DEADLINE_MS} ms, the leaderboard's default, no measured configuration is excluded. {subs['SENS_SENTENCE']} The index applies none of them.")],
          [("Reference floor", fmt(raw_wh(ref)), "Wh/M", f"{esc(ref['model'])}, {ref['num_gpus']} × {ref['gpu']}, running batch {fmt(ref['_cfg']['avg_batch_size'], 0)}"),
           ("Same row, light load", fmt(l32["first"], 0), "Wh/M", f"Running batch {fmt(l32['first_batch'], 0)}: {l32['ratio']:.1f}× the floor"),
           ("Challenge line", str(CHALLENGE_TOLERANCE_PCT), "% below", "A bidder's figure this far under the floor is asked for its logs")]),
    _term("gpu-only-boundary", "GPU-only boundary",
          "The measurement boundary of every index row: energy read from the GPUs alone, with host, network, cooling, idle time and embodied carbon outside it.",
          f"<b>The GPU-only boundary</b> is the measurement boundary of every index row: energy read from the GPU devices themselves over the steady-state window, with the host CPU and memory, the network and storage, cooling and the rest of the facility, time the GPU spends idle between requests, and the carbon embodied in the hardware all outside it. Google's {GOOGLE_2025['date']} disclosure shows the size of what sits outside: accelerators were <b>{GOOGLE_2025['accelerator_share'] * 100:.0f} percent</b> of its {GOOGLE_2025['wh']:g} Wh median prompt, and NVIDIA rates a {esc(_sys_row['system'])} at {fmt(_sys_row['max_power_kw'], 1)} kW against {fmt(gpu_kw_sys, 1)} kW for its {_sys_n} GPUs, a system-to-GPU ratio of <b>{sys_ratio:.2f}</b>.",
          f"<p>Two multipliers take a GPU figure to the facility meter, and both belong to the operator. The system-to-GPU power ratio covers the host, memory, network and fans; the site's power usage effectiveness (<a href=\"{{{{ROOT}}}}glossary/pue/\">PUE</a>) covers cooling and distribution. As an illustration, with the {esc(_sys_row['system'])} ratio of {sys_ratio:.2f} and a PUE of {PUE_EXAMPLE:g}, the reference row's {fmt(raw_wh(ref))} Wh/M becomes about {fmt(meter_wh, 0)} Wh/M at the meter, and a gigawatt-hour at the meter serves about {fmt(meter_tokens_b, 1)} billion tokens instead of {{{{TOKENS_PER_MWH_REF_B}}}} billion per megawatt-hour of GPU energy. The PUE is the operator's own figure and the index publishes none.</p>"
          f"<p>The boundary is drawn at the GPU because it is the only part a buyer can measure, compare across vendors and hold a vendor to; the rest depends on the site. For scale on embodied carbon, NVIDIA's cradle-to-gate footprint for one HGX B200 baseboard, eight GPUs, is {fmt(hw['embodied']['kg_co2e_cradle_to_gate'], 0)} kg CO2e. Water is outside the boundary too: the index measures electricity, and the only public per-prompt water figures are Google's {GOOGLE_2025['water_ml']:g} mL and Mistral's {MISTRAL_2025['water_ml']:g} mL per reply.</p>",
          [("The index method", "index/#method"), ("How much energy does an AI query use?", "per-query/"), ("Why it matters: power", "why/#power")],
          [("What does GPU-only mean on the index?", f"That the energy was read from the GPU devices alone over a steady-state window. Host, network, storage, cooling, idle time between requests and embodied carbon are not counted. Google's {GOOGLE_2025['date']} figures show accelerators at {GOOGLE_2025['accelerator_share'] * 100:.0f} percent of a prompt's whole-stack energy."),
           ("How do I take a GPU-only figure to the facility meter?", f"Multiply by the system-to-GPU power ratio ({sys_ratio:.2f} for a {_sys_row['system']}: {fmt(_sys_row['max_power_kw'], 1)} kW rated against {fmt(gpu_kw_sys, 1)} kW of GPUs) and by the site's PUE. With a PUE of {PUE_EXAMPLE:g}, {fmt(raw_wh(ref))} Wh/M at the GPU is about {fmt(meter_wh, 0)} Wh/M at the meter. Both multipliers are the operator's own."),
           ("Why not publish whole-system figures?", "Because they cannot be compared across vendors or sites: the host, the fans and the cooling design differ with every server and building, while the GPU figure for a named model on a named card at a stated load can be measured anywhere. The index publishes the comparable part and names the multipliers for the rest."),
           ("Does the boundary include the energy of processing the prompt?", "Yes. The benchmark divides steady-state GPU energy, which includes prefill, by the output tokens generated; the prompt's tokens are not in the denominator.")],
          [("Accelerator share", f"{GOOGLE_2025['accelerator_share'] * 100:.0f}", "%", f"of Google's {GOOGLE_2025['wh']:g} Wh median prompt, {GOOGLE_2025['date']}"),
           ("System to GPU", f"{sys_ratio:.2f}", "×", f"{esc(_sys_row['system'])}: {fmt(_sys_row['max_power_kw'], 1)} kW rated against {fmt(gpu_kw_sys, 1)} kW of GPUs"),
           ("At the meter", fmt(meter_wh, 0), "Wh/M", f"Reference row × {sys_ratio:.2f} × PUE {PUE_EXAMPLE:g}; illustration, not a measurement")]),
    _term("location-based-intensity", "Location-based grid intensity",
          "The average carbon intensity of the electricity generated where a GPU runs, in gCO2e per kWh; the factor that turns energy per token into carbon per token.",
          f"<b>Location-based grid intensity</b> is the average carbon intensity of the electricity generated in the area where a GPU runs, in grams of CO2e per kilowatt-hour, before any contracts, certificates or self-generation are considered. The index uses Ember's yearly figures ({EMBER_RELEASE}, {EMBER_YEAR}, the latest year with a value for every listed grid): <b>{fmt(intensity['SAU'], 0)} gCO2e per kWh</b> for Saudi Arabia, {fmt(intensity['IND'], 0)} for India, {fmt(intensity['NOR'], 0)} for Norway and {fmt(world, 0)} for the world. It is a lifecycle figure on net generation, production-based, so upstream methane and plant manufacture are in and imports are out.",
          f"<p>Energy per token does not change with geography; carbon per token does. The reference row's {fmt(raw_wh(ref))} Wh/M carries {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg CO2e per billion tokens on Saudi Arabia's grid and {fmt(kg_per_billion(raw_wh(ref), intensity['NOR']))} kg on Norway's, {sau_nor_ratio:.0f}× apart for the same tokens on the same GPUs. Across the {grid_count} grids Ember covers the spread is {fmt(intensity[grid_max['iso3']] / intensity[grid_min['iso3']], 1)}×, from {esc(grid_min['display_name'])} at {fmt(intensity[grid_min['iso3']], 1)} to {esc(grid_max['display_name'])} at {fmt(intensity[grid_max['iso3']], 1)} gCO2e per kWh.</p>"
          f"<p>Location-based is the method ESRS E1-6 and the GHG Protocol pair with market-based, which uses the supply you contracted (certificates, power purchase agreements) and needs your own figures. Ember's number is for comparing places, not for filing as a Scope 2 combustion factor: a GPU server draws much the same power around the clock while an annual average weights each hour by its generation, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average. One page per listed grid is under <a href=\"{{{{ROOT}}}}grids/\">Grids</a>, and every grid is in <a href=\"{{{{ROOT}}}}api/v1/grid.json\">grid.json</a>.</p>",
          [("Grids", "grids/"), ("The carbon table", "index/#carbon"), ("Why it matters: location", "why/#location")],
          [("What is location-based grid carbon intensity?", f"The average carbon intensity of the electricity generated where the load runs, in gCO2e per kWh, before contracts or certificates. The index uses Ember's yearly figures ({EMBER_RELEASE}, {EMBER_YEAR}): Saudi Arabia {fmt(intensity['SAU'], 0)}, India {fmt(intensity['IND'], 0)}, Norway {fmt(intensity['NOR'], 0)}, world {fmt(world, 0)}."),
           ("What is the difference between location-based and market-based?", "Location-based uses the average intensity of the grid where the electricity was consumed. Market-based uses the intensity of the supply you contracted, through certificates or power purchase agreements, and needs your own contract data. ESRS E1-6 asks for both; the index can supply only the first."),
           ("How much does location change the carbon of AI inference?", f"On the reference row, {sau_nor_ratio:.0f}× between Saudi Arabia ({fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg CO2e per billion tokens) and Norway ({fmt(kg_per_billion(raw_wh(ref), intensity['NOR']))} kg), {EMBER_YEAR} averages. The energy figure is identical in both places."),
           ("Can I file Ember's figure in my Scope 2 report?", "Use it for comparison, not as the filed factor. It is a lifecycle, production-based figure on net generation, not a Scope 2 combustion factor, and it is an annual average that a round-the-clock GPU load does not follow hour by hour.")],
          [("Saudi Arabia", fmt(intensity["SAU"], 0), "gCO2e/kWh", f"Ember, {EMBER_YEAR}, lifecycle, location-based"),
           ("World", fmt(world, 0), "gCO2e/kWh", f"Ember, {EMBER_YEAR}"),
           ("Norway", fmt(intensity["NOR"], 0), "gCO2e/kWh", f"{sau_nor_ratio:.0f}× cleaner than Saudi Arabia for the same tokens")]),
    _term("kg-co2e-per-billion-tokens", "kg CO2e per billion output tokens",
          "The carbon unit of the index: energy per million tokens multiplied by the grid's carbon intensity, which gives kilograms of CO2e per billion output tokens.",
          f"<b>Kilograms of CO2e per billion output tokens</b> is the carbon unit of the index. It is watt-hours per million output tokens multiplied by the grid's grams of CO2e per kilowatt-hour, divided by 1,000: Wh/M × gCO2e/kWh ÷ 1,000 = kg CO2e per billion tokens, which is also grams of CO2e per million tokens. On the reference row, {esc(ref['model'])} on {ref['num_gpus']} × {ref['gpu']} at {fmt(raw_wh(ref))} Wh/M, a billion output tokens carries about <b>{fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg CO2e</b> on Saudi Arabia's {EMBER_YEAR} grid ({fmt(intensity['SAU'], 0)} gCO2e/kWh, Ember), <b>{fmt(kg_per_billion(raw_wh(ref), intensity['IND']))} kg</b> on India's ({fmt(intensity['IND'], 0)}), {fmt(kg_per_billion(raw_wh(ref), world))} kg on the world average ({fmt(world, 0)}) and {fmt(kg_per_billion(raw_wh(ref), intensity['NOR']))} kg on Norway's ({fmt(intensity['NOR'], 0)}). GPU energy only.",
          f"<p>The arithmetic as printed: {fmt(raw_wh(ref))} × {fmt(intensity['SAU'], 0)} ÷ 1,000 = {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))}. Across the index the range on Saudi Arabia's grid is {fmt(kg_per_billion(raw_wh(low), intensity['SAU']))} kg ({esc(low['model'])}, {low['num_gpus']} × {low['gpu']}) to {fmt(kg_per_billion(raw_wh(high), intensity['SAU']))} kg ({esc(high['model'])}, {high['num_gpus']} × {high['gpu']}) per billion tokens. Per million tokens, read the same numbers in grams: about {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} g for the reference row in Saudi Arabia.</p>"
          f"<p>The unit is a floor on two counts: the energy is a busy-server GPU-only figure and the grid factor is a location-based annual average. A lightly loaded server multiplies the first factor by several times ({l32['ratio']:.1f}× on the reference model's own ladder), and host, network and cooling add to it. Figures per billion are chosen because enterprise token volumes are counted in billions a month; the <a href=\"{{{{ROOT}}}}grids/\">grid pages</a> price every index row on each listed grid, and the <a href=\"{{{{ROOT}}}}mcp/\">MCP server</a> prices any configuration on any grid for a token count.</p>",
          [("The carbon table", "index/#carbon"), ("Grids", "grids/"), ("Why it matters: the SCI", "why/#sci")],
          [("How much CO2 does a million AI tokens produce?", f"On the index's reference row ({ref['model']}, {ref['num_gpus']} × {ref['gpu']}, {fmt(raw_wh(ref))} Wh per million output tokens, GPU only), about {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} g CO2e per million tokens on Saudi Arabia's {EMBER_YEAR} grid, {fmt(kg_per_billion(raw_wh(ref), intensity['IND']))} g on India's, {fmt(kg_per_billion(raw_wh(ref), world))} g on the world average and {fmt(kg_per_billion(raw_wh(ref), intensity['NOR']))} g on Norway's. Per billion tokens, the same numbers in kilograms."),
           ("How do I calculate kg CO2e per billion tokens?", f"Multiply watt-hours per million output tokens by the grid's gCO2e per kWh and divide by 1,000. Example: {fmt(raw_wh(ref))} Wh/M × {fmt(intensity['SAU'], 0)} gCO2e/kWh ÷ 1,000 = {fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg CO2e per billion tokens."),
           ("Why are some published figures thousands of times higher?", "Usually because they start from an estimate of energy per token for a single request at a time, or from a whole-stack figure, and then multiply by a grid factor. The index's energy figures are measured on a busy server, GPU only; at the same grid factor they land far lower. State the boundary and the load before comparing two carbon figures."),
           ("Is this a Scope 2 figure?", "It is a location-based GPU-side figure for comparison. GPUs you run put their electricity in your own Scope 2 (ESRS E1-6, location-based matches this method; market-based needs your contracts). Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3, category 1.")],
          [("Saudi Arabia", fmt(kg_per_billion(raw_wh(ref), intensity["SAU"])), "kg / bn tokens", f"Reference row × {fmt(intensity['SAU'], 0)} gCO2e/kWh, {EMBER_YEAR}"),
           ("India", fmt(kg_per_billion(raw_wh(ref), intensity["IND"])), "kg / bn tokens", f"Reference row × {fmt(intensity['IND'], 0)} gCO2e/kWh"),
           ("Norway", fmt(kg_per_billion(raw_wh(ref), intensity["NOR"])), "kg / bn tokens", f"Reference row × {fmt(intensity['NOR'], 0)} gCO2e/kWh")]),
    _term("inter-token-latency-ceiling", "Inter-token latency ceiling",
          "The latency limit that defines which configurations may be an index row: a median inter-token latency at or under 500 ms, the leaderboard's own default.",
          f"<b>The inter-token latency ceiling</b> is the limit that decides which measured configurations may be an index row: the median time between one output token and the next must be at or under <b>{ITL_DEADLINE_MS} ms</b>, the ML.ENERGY Leaderboard's own default for every LLM task. Each index row is the lowest-energy configuration for its model and GPU under that ceiling. No measured configuration reaches it (the slowest Text Conversation row is {fmt(max_chat_itl, 0)} ms), so at {ITL_DEADLINE_MS} ms the ceiling excludes nothing; it is stated because any energy figure needs the latency it was measured at.",
          f"<p>Energy and latency trade against each other through the running batch: more requests in flight means more tokens per joule and a longer wait between each user's tokens. On the reference model's ladder, median inter-token latency rises from {fmt(l32['first_itl'], 0)} ms at a running batch of {fmt(l32['first_batch'], 0)} to {fmt(l32['best_itl'], 0)} ms at {fmt(l32['best_batch'], 0)} while energy per token falls {l32['ratio']:.1f}×. The reference row's p99 is {{{{REF_P99}}}} ms.</p>"
          f"<p>Tighter ceilings would change rows: {subs['SENS_SENTENCE'][0].lower() + subs['SENS_SENTENCE'][1:]} None of these is applied to the index; they are reported under <a href=\"{{{{ROOT}}}}index/#method\">Method</a> so a reader with a stricter requirement can see what moves. In an RFP, fill the ceiling with the latency your users will accept, state it once and use it for every bidder; the <a href=\"{{{{ROOT}}}}why/#monday\">clause</a> asks for median and p99 over the same window as the energy figure.</p>",
          [("The index method", "index/#method"), ("The concurrency ladder", "index/#concurrency"), ("The RFP clause", "why/#monday")],
          [("What is the inter-token latency ceiling on the index?", f"A median inter-token latency of at most {ITL_DEADLINE_MS} ms, the ML.ENERGY Leaderboard's default for every LLM task. Each index row is the lowest-energy configuration for its model and GPU at or under it. No measured configuration reaches it, so at this value it excludes nothing."),
           ("What is inter-token latency?", f"The time between one output token and the next for a single request while the model is generating, usually reported as a median and a p99 over a window. On the reference model's ladder it runs from {fmt(l32['first_itl'], 0)} ms at a running batch of {fmt(l32['first_batch'], 0)} to {fmt(l32['best_itl'], 0)} ms at {fmt(l32['best_batch'], 0)}."),
           ("Would a stricter latency limit change the index?", f"Yes. {subs['SENS_SENTENCE']} The index applies none of these; they are reported so that a reader with a stricter requirement can see which rows move."),
           ("Why state a latency ceiling with an energy figure at all?", "Because energy per token falls as the running batch rises and latency rises with it; a figure without its latency can be made arbitrarily good by loading the server until users wait. The ceiling fixes the trade so that two figures can be compared.")],
          [("Ceiling", str(ITL_DEADLINE_MS), "ms median ITL", "The leaderboard's default for every LLM task"),
           ("Slowest measured row", fmt(max_chat_itl, 0), "ms", "Text Conversation; the ceiling excludes nothing at 500 ms"),
           ("Reference row", fmt(ref["_cfg"]["median_itl_ms"], 0), "ms median", f"p99 {fmt(ref['_cfg']['p99_itl_ms'], 0)} ms at a running batch of {fmt(ref['_cfg']['avg_batch_size'], 0)}")]),
    _term("pue", "Power usage effectiveness (PUE)",
          "Total facility energy divided by IT equipment energy, per ISO/IEC 30134-2; the operator's own multiplier that takes a GPU figure to the building's meter.",
          f"<b>Power usage effectiveness (PUE)</b> is a data centre's total facility energy divided by the energy delivered to its IT equipment, as defined in ISO/IEC 30134-2. A PUE of 1.0 would mean no energy for cooling, power distribution or lighting; real sites sit above it, and the figure is the operator's own, measured at the building. The index publishes no PUE. It names it because PUE is the second of two multipliers that take a GPU-only figure to the meter: with a system-to-GPU power ratio of {sys_ratio:.2f} ({esc(_sys_row['system'])}) and an illustrative PUE of <b>{PUE_EXAMPLE:g}</b>, the reference row's {fmt(raw_wh(ref))} Wh/M at the GPU becomes about <b>{fmt(meter_wh, 0)} Wh/M</b> at the facility meter.",
          f"<p>The arithmetic as printed: {fmt(raw_wh(ref))} × {sys_ratio:.2f} × {PUE_EXAMPLE:g} = {fmt(meter_wh, 0)}. The order of the two multipliers does not matter; what matters is that both are stated. A contracted feed then becomes a token capacity: at that figure a gigawatt-hour at the meter serves about {fmt(meter_tokens_b, 1)} billion output tokens of the reference row, against {{{{TOKENS_PER_MWH_REF_B}}}} billion per megawatt-hour of GPU energy.</p>"
          f"<p>PUE is a facility metric and says nothing about how much useful work the IT equipment did; a site with a PUE of 1.1 serving eight requests per GPU wastes more energy per token than a site at 1.4 serving two hundred and fifty. Under the Energy Efficiency Directive (EU) 2023/1791 and Delegated Regulation (EU) 2024/1364, data centres with an installed IT power demand of at least {fmt(EED_MIN_KW, 0)} kW report PUE and other facility indicators to the European database; none of those indicators is energy per unit of work, which is what the <a href=\"{{{{ROOT}}}}index/\">index</a> adds. The <a href=\"{{{{ROOT}}}}glossary/gpu-only-boundary/\">GPU-only boundary</a> entry draws the line the multipliers cross.</p>",
          [("The index method: to the meter", "index/#method"), ("Why it matters: power", "why/#power"), ("Why it matters: the regulator", "why/#regulator")],
          [("What is PUE?", "Power usage effectiveness: a data centre's total facility energy divided by the energy delivered to its IT equipment, per ISO/IEC 30134-2. It is measured by the operator at the building and the index publishes none; it is one of the two multipliers that take a GPU-only energy figure to the meter."),
           ("How do I use PUE with watt-hours per million tokens?", f"Multiply the GPU figure by the system-to-GPU power ratio and by the PUE. Illustration: {fmt(raw_wh(ref))} Wh/M × {sys_ratio:.2f} ({_sys_row['system']}) × {PUE_EXAMPLE:g} = about {fmt(meter_wh, 0)} Wh/M at the facility meter. Use your own site's PUE and your own server's ratio."),
           ("Does a low PUE mean efficient AI inference?", "No. PUE measures the building's overhead, not the work the GPUs did. A site with a low PUE serving few requests per GPU uses more energy per token than a site with a higher PUE whose GPUs are busy. Energy per token measures the work; PUE measures the building."),
           ("Which regulation asks for PUE?", f"In the EU, the Energy Efficiency Directive (EU) 2023/1791, Article 12, with Commission Delegated Regulation (EU) 2024/1364: data centres with an installed IT power demand of at least {fmt(EED_MIN_KW, 0)} kW report facility indicators including PUE. No regulation asks for energy per token.")],
          [("Illustrative PUE", f"{PUE_EXAMPLE:g}", "", "A stated assumption; the operator's figure is the only real one"),
           ("System to GPU", f"{sys_ratio:.2f}", "×", f"{esc(_sys_row['system'])}, NVIDIA rated power"),
           ("Reference row at the meter", fmt(meter_wh, 0), "Wh/M", f"{fmt(raw_wh(ref))} × {sys_ratio:.2f} × {PUE_EXAMPLE:g}")]),
]
assert len(GLOSSARY) == 9, "the strategy names nine glossary terms"
assert len({t["slug"] for t in GLOSSARY}) == 9

# GEO item 4 (20 October 2026): one figure-first sentence per term, rendered before the definition and used as the meta description
# where it fits 155 characters, so the first sentence an extractor sees carries the number.
GLOSSARY_ANSWERS = {
    "watt-hours-per-million-output-tokens": (f"{fmt(raw_wh(low))} to {fmt(raw_wh(high))} Wh per million output tokens is the index's range, from {esc(low['model'])} on "
                                             f"{low['num_gpus']} × {low['gpu']} to {esc(high['model'])} on {high['num_gpus']} × {high['gpu']}, GPU only."),
    "energy-per-token": (f"{low['_cfg']['energy_per_token_joules']:.3f} to {high['_cfg']['energy_per_token_joules']:.2f} joules per output token is the index's range "
                         "of GPU energy per token; 1 Wh per million tokens equals 0.0036 J per token."),
    "running-batch": (f"Raising the running batch of {esc(l32['model'])} on {l32['gpus']} from {fmt(l32['first_batch'], 0)} to {fmt(l32['best_batch'], 0)} cuts GPU energy "
                      f"from {fmt(l32['first'])} to {fmt(l32['best'])} Wh per million tokens, {l32['ratio']:.1f}× on the same cards."),
    "floor": (f"Every index row is a floor: {esc(ref['model'])} on {ref['num_gpus']} × {ref['gpu']} is {fmt(raw_wh(ref))} Wh per million tokens at a running batch of "
              f"{fmt(ref['_cfg']['avg_batch_size'], 0)}, and a real deployment sits above it."),
    "gpu-only-boundary": (f"Every index row counts the GPUs alone; in Google's {GOOGLE_2025['date']} disclosure accelerators were "
                          f"{GOOGLE_2025['accelerator_share'] * 100:.0f} percent of a prompt's energy, and the rest sits outside this boundary."),
    "location-based-intensity": (f"{fmt(intensity['SAU'], 0)} gCO2e per kWh for Saudi Arabia, {fmt(intensity['IND'], 0)} for India, {fmt(intensity['NOR'], 0)} for Norway and "
                                 f"{fmt(world, 0)} for the world ({EMBER_YEAR}, Ember): the grid factor that turns energy per token into carbon."),
    "kg-co2e-per-billion-tokens": (f"{fmt(kg_per_billion(raw_wh(ref), intensity['SAU']))} kg CO2e per billion output tokens for {esc(ref['model'])} on {ref['num_gpus']} × "
                                   f"{ref['gpu']} on Saudi Arabia's grid: Wh per million tokens × gCO2e per kWh ÷ 1,000."),
    "inter-token-latency-ceiling": (f"{ITL_DEADLINE_MS} ms median inter-token latency is the ceiling an index row must meet; the slowest measured row is "
                                    f"{fmt(max_chat_itl, 0)} ms, so today it excludes nothing."),
    "pue": ("The index publishes no PUE: its figures stop at the GPU; PUE, facility energy ÷ IT energy per ISO/IEC 30134-2, is the operator's own multiplier "
            "to the meter."),
}
for _t in GLOSSARY:
    _t["answer"] = GLOSSARY_ANSWERS[_t["slug"]]
    assert "\u2013" not in _t["answer"] and "\u2014" not in _t["answer"]


def glossary_page(t: dict) -> tuple[str, str, str, list[tuple[str, str]]]:
    tiles = ""
    if t["tiles"]:
        tiles = ("<div class=\"tiles auto n3\" role=\"group\" aria-label=\"Headline readings\">"
                 + "".join(f"<div class=\"tile{' ref' if i == 1 else ''}\"><span class=\"lbl\">{esc(l)}</span><span class=\"val\">{v}<small>{esc(u)}</small></span><span class=\"sub\">{s}</span></div>"
                           for i, (l, v, u, s) in enumerate(t["tiles"])) + "</div>")
    used = "".join(f"<li><a href=\"{{{{ROOT}}}}{href}\">{esc(label)}</a></li>" for label, href in t["used"])
    others = "".join(f"<li><a href=\"{{{{ROOT}}}}glossary/{o['slug']}/\">{esc(o['name'])}</a></li>" for o in GLOSSARY if o is not t)
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about this term</h2><div class=\"prose faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in t["faq"]) + "</div></section>"
    body = f"""<div class="title">
  <p class="eyebrow"><a href="{{{{ROOT}}}}glossary/">Glossary</a></p>
  <h1>{esc(t['name'])}</h1>
  <p class="stand">{esc(t['answer'])} {t['definition']}</p>
  <p class="unit"><b>Data</b> <a href="{{{{ROOT}}}}api/v1/index.json">index.json</a>, <a href="{{{{ROOT}}}}api/v1/grid.json">grid.json</a>, <a href="{{{{ROOT}}}}api/v1/hardware.json">hardware.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#working">The working</a></li><li><a href="#used">Where it is used</a></li><li><a href="#faq">Questions</a></li><li><a href="#sources">Sources</a></li></ul>
</div>
{tiles}
<section id="working" class="first">
  <p class="eyebrow">The working</p>
  <h2>How the term is used on the index</h2>
  <div class="prose">{t['working']}</div>
</section>

<section id="used">
  <p class="eyebrow">Where it is used</p>
  <h2>Pages that rely on this term</h2>
  <div class="prose"><ul>{used}</ul>
  <p>Other terms: </p><ul>{others}</ul></div>
</section>
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">{{{{MLE_BLOCK}}}}</p>
  <p class="note">Grid intensity: <a href="{SRC_EMBER['url']}">Ember, Yearly electricity data</a>, {EMBER_RELEASE}, {EMBER_YEAR}, CC BY 4.0, retrieved {{{{EMBER_RETRIEVED_LONG}}}}. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved {{{{RETRIEVED_LONG}}}}. Per-prompt figures: Google, <a href="{GOOGLE_2025['url']}">arXiv 2508.15734</a> ({GOOGLE_2025['date']}); Mistral AI, July 2025.</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
</section>"""
    title = f"{t['name']}: definition and the figure | Lead Green glossary"
    desc = t["answer"] if 0 < len(t["answer"]) <= 155 else t["short"]
    if len(desc) > 155:
        desc = desc[:152].rsplit(" ", 1)[0] + "..."
    return title, desc, body, t["faq"]


glossary_cards = []
for _t in GLOSSARY:
    gt_, gd_, gb_, gfaq_ = glossary_page(_t)
    _ti = {"inter-token-latency-ceiling": 0, "location-based-intensity": 0, "kg-co2e-per-billion-tokens": 0, "pue": 0}.get(_t["slug"], 1)
    if _t["tiles"]:
        _tl, _tv, _tu, _ts = _t["tiles"][_ti]
        _card = {"eyebrow": f"Glossary · {_tl}", "value": _tv, "unit": _tu, "label": f"{_t['name']}. {re.sub('<[^>]+>', '', _ts)}"}
    else:
        _card = {"eyebrow": "Glossary · reference row", "value": f"{ref['_cfg']['energy_per_token_joules']:.4f}", "unit": "J per token",
                 "label": f"{_t['name']}. {ref['model']} on {ref['num_gpus']} × {ref['gpu']}: {fmt(ref['_cfg']['avg_power_watts'], 0)} W ÷ {fmt(ref['_cfg']['output_throughput_tokens_per_sec'], 0)} tokens per second."}
    render(f"glossary/{_t['slug']}/index.html", "", gt_, gd_, "article", "answer", gb_,
           {"date": UPDATED, "faq": gfaq_, "name": _t["name"], "crumbs": [("Glossary", f"{SITE}/glossary/")],
            "term": {"name": _t["name"], "description": _t["short"]}, "card": _card})
    glossary_cards.append(f"<div class=\"card\"><span class=\"k\">Term</span><h3><a href=\"{{{{ROOT}}}}glossary/{_t['slug']}/\">{esc(_t['name'])}</a></h3><p>{esc(_t['short'])}</p></div>")

_gl_body = f"""<div class="title">
  <p class="eyebrow">Glossary</p>
  <h1>The nine terms behind the index</h1>
  <p class="stand">Every figure on this site depends on a handful of defined terms: the unit, the boundary, the load, the latency limit and the carbon factor. Each has one page that states the definition, the figure and the source in its first paragraph, with the working underneath. Read them once and every row on the index reads the same way.</p>
  <p class="unit"><b>Unit</b> watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated {{{{UPDATED_LONG}}}}.</p>
</div>

<section id="terms" class="first">
  <p class="eyebrow">Terms</p>
  <h2>One page each</h2>
  <div class="cards">
{chr(10).join(glossary_cards)}
  </div>
  <p class="note">Each term's page carries its own FAQ and sources, and a Markdown copy at its URL followed by <code>index.md</code>. The terms are also the vocabulary of the <a href="{{{{ROOT}}}}contribute/#protocol">measurement protocol</a> and the <a href="{{{{ROOT}}}}why/#monday">RFP clause</a>.</p>
</section>"""
render("glossary/index.html", "", "Glossary: the terms behind GPU energy per token | Lead Green",
       "Nine defined terms behind the index, one page each with the figure and the source: Wh per million tokens, energy per token, running batch, floor, PUE.",
       "website", "glossary", _gl_body, {"date": UPDATED, "terms": GLOSSARY})


# ---- compare pages: the model pairs people ask about, generated from the index rows (GEO strategy 6.2)
# Each page compares two models' index rows on every GPU both were measured on. The ratio is the second
# model's energy per token over the first's; the sweep caveat (card count, running batch) is stated on every page.
# The first model is the smaller, the FP8 variant or the mixture-of-experts one, so a ratio above 1 reads as "the second costs more".
COMPARE_PAIRS = [  # (first model, second model, angle)
    ("Llama 3.1 8B Instruct", "Llama 3.3 70B Instruct", "size"),
    ("Llama 3.3 70B Instruct", "Llama 3.1 405B Instruct FP8", "size"),
    ("Qwen 3 32B", "Llama 3.3 70B Instruct", "cross"),
    ("Qwen 3 235B A22B Instruct", "DeepSeek V3.1", "moe-size"),
    ("Qwen 3 30B A3B Instruct", "Qwen 3 32B", "dense-vs-moe"),
    ("Qwen 3 235B A22B Instruct FP8", "Qwen 3 235B A22B Instruct", "precision"),
    ("Llama 3.1 405B Instruct FP8", "Llama 3.1 405B Instruct", "precision"),
    ("Qwen 3 8B", "Llama 3.1 8B Instruct", "family"),
    ("Llama 4 Scout 17B 16E Instruct", "Llama 4 Maverick 17B 128E Instruct FP8", "moe-experts"),
]
for _a, _b, _ in COMPARE_PAIRS:
    assert slug(_a) in models and slug(_b) in models, f"compare pair names a model that is not on the index: {_a} / {_b}"


def _cmp_slug(a: str, b: str) -> str:
    return f"{slug(a)}-vs-{slug(b)}"


def _params(m: dict) -> str:
    t, act = m["params_b"], m["active_params_b"]
    return f"{t:g} B parameters" + (f", {act:g} B active per token" if act and abs(act - t) > 0.01 else "")


def _per_answer(c) -> float:
    return cfg_wh(c) * c["avg_output_len"] / 1e6


def _cards(n: int) -> str:
    return f"{word(n)} card{'s' if n > 1 else ''}"


def _more_less(r: float) -> str:
    """'1.85× the' or '0.68× the (less)': a ratio read aloud without pretending 0.9× is 'more'."""
    return f"{r:.2f}× the" if r >= 1 else f"{r:.2f}× the (that is, less)"


def compare_pair_page(a_name: str, b_name: str, angle: str) -> tuple[str, str, str, list[tuple[str, str]], dict]:
    ma, mb = models[slug(a_name)], models[slug(b_name)]
    gpus = [g for g in ("H100", "B200") if (a_name, g) in best and (b_name, g) in best]
    assert gpus, f"{a_name} and {b_name} share no GPU on the index"
    rows = [(g, best[(a_name, g)], best[(b_name, g)], cfg_wh(best[(b_name, g)]) / cfg_wh(best[(a_name, g)])) for g in gpus]
    ratios = {g: r for g, _, _, r in rows}
    lead_g, lead_a, lead_b, lead_r = rows[0]
    b_more_everywhere = all(r > 1 for r in ratios.values())
    b_less_everywhere = all(r < 1 for r in ratios.values())

    def row_phrase(g) -> str:
        ca, cb = best[(a_name, g)], best[(b_name, g)]
        cards = (f"both on {_cards(cb['num_gpus'])}" if cb['num_gpus'] == ca['num_gpus'] else f"on {_cards(cb['num_gpus'])} and {_cards(ca['num_gpus'])}")
        return (f"on the {g} ({fmt(cfg_wh(cb))} against {fmt(cfg_wh(ca))} Wh/M, {cards} "
                f"at running batches of {fmt(cb['avg_batch_size'], 0)} and {fmt(ca['avg_batch_size'], 0)})")

    per_gpu = (f"<b>{ratios[gpus[0]]:.2f}×</b> the GPU energy per output token of {esc(a_name)} {row_phrase(gpus[0])}"
               + (f" and <b>{ratios[gpus[1]]:.2f}×</b> {row_phrase(gpus[1])}" if len(gpus) > 1 else ""))
    answer = (f"On the index rows, {esc(b_name)} uses {per_gpu}, GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it "
              f"(data compiled {long_date(SRC_MLE['compiled'])}). {esc(a_name)} has {_params(ma)}; {esc(b_name)} has {_params(mb)}. "
              f"Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.")
    pa, pb = ma["params_b"], mb["params_b"]
    aa, ab = ma["active_params_b"] or pa, mb["active_params_b"] or pb
    pr = pb / pa
    gap_vs_params = ("smaller than" if lead_r < pr * 0.9 else "larger than" if lead_r > pr * 1.1 else "close to")
    sweep_note = ((f"On the {lead_g} both rows sit on {_cards(lead_a['num_gpus'])}" if lead_a['num_gpus'] == lead_b['num_gpus'] else
                   f"On the {lead_g} the rows sit on {_cards(lead_a['num_gpus'])} ({esc(a_name)}) and {_cards(lead_b['num_gpus'])} ({esc(b_name)})")
                  + f", at running batches of {fmt(lead_a['avg_batch_size'], 0)} ({esc(a_name)}) and {fmt(lead_b['avg_batch_size'], 0)} ({esc(b_name)}).")
    if angle == "size":
        why = (f"The second model has {pr:.1f}× the parameters of the first, and a dense model reads every parameter for every output token, so the weights moved per token scale with size and so does the memory needed to hold them. {sweep_note} "
               f"The energy gap on the {lead_g} ({lead_r:.2f}×) is {gap_vs_params} the parameter gap ({pr:.1f}×), because each row runs at its own card count and running batch, where its fixed draw is spread over its own number of tokens. "
               f"Size is the largest lever after load; the question for a buyer is whether the task needs the larger model's answers.")
    elif angle == "cross":
        why = (f"Two families and two sizes: {esc(a_name)} ({_params(ma)}, {esc(ma['architecture'])}) against {esc(b_name)} ({_params(mb)}, {esc(mb['architecture'])}), {pr:.1f}× the parameters. "
               f"{sweep_note} The energy gap on the {lead_g} ({lead_r:.2f}×) is {gap_vs_params} the parameter gap ({pr:.1f}×); architecture, vocabulary and the configuration each model was swept at account for the rest. "
               f"{esc(a_name)} is the index's reference model, so its full ladder of measured loads is on <a href=\"{{{{ROOT}}}}index/#concurrency\">the index</a>, and both models' every configuration is on their pages.")
    elif angle == "family":
        why = (f"Two models of the same size class from different families: {esc(a_name)} ({_params(ma)}, {esc(ma['architecture'])}) against {esc(b_name)} ({_params(mb)}, {esc(mb['architecture'])}). "
               f"At the same size the energy per token depends on the architecture's depth and width, the vocabulary, the attention design and, on the leaderboard, the configuration swept for each: card count, cap and the running batch reached. {sweep_note} "
               f"The gap here is {'under' if max(abs(1 - r) for r in ratios.values()) < 0.2 else 'about'} {max(abs(1 - r) for r in ratios.values()) * 100:.0f} percent, which is inside what load alone moves; read the ratio with the running batches beside it.")
    elif angle == "dense-vs-moe":
        why = (f"A dense model reads all of its weights for every output token; a mixture-of-experts model routes each token through a few experts and reads only those. {esc(a_name)} activates {aa:g} B of its {pa:g} B parameters per token; {esc(b_name)} is dense at {pb:g} B. "
               f"So the mixture-of-experts model reads about {ab / aa:.0f}× fewer weights per token at a similar total size, and on the {lead_g} its index row uses {1 / lead_r:.2f}× less GPU energy per output token "
               f"({fmt(cfg_wh(lead_a))} against {fmt(cfg_wh(lead_b))} Wh/M). The whole model must still fit in memory: {sweep_note} The saving is in weights read per token, not in cards.")
    elif angle == "moe-size":
        why = (f"Two mixture-of-experts models of different total size: {esc(a_name)} activates {aa:g} B of {pa:g} B parameters per token, {esc(b_name)} {ab:g} B of {pb:g} B. "
               f"Weights read per token scale with the active parameters ({ab / aa:.1f}× here), memory with the total ({pr:.1f}×), so the larger model needs more cards to hold its experts and spreads each token's work across them. {sweep_note} "
               f"The index row ratio on the {lead_g} is {lead_r:.2f}×, between the active-parameter gap and the total-parameter gap.")
    elif angle == "precision":
        fp8_saves = [g for g in gpus if ratios[g] > 1]
        fp8_costs = [g for g in gpus if ratios[g] <= 1]
        verdict = ("On both GPUs the FP8 row uses less energy per token" if len(fp8_saves) == len(gpus) and len(gpus) > 1 else
                   "On this GPU the FP8 row uses less energy per token" if len(fp8_saves) == len(gpus) else
                   "On these index rows FP8 does not come out ahead" if not fp8_saves else
                   f"The FP8 row uses less energy per token on the {and_list(fp8_saves)} and more on the {and_list(fp8_costs)}")
        detail = "; ".join(f"{g}: FP8 {fmt(cfg_wh(best[(a_name, g)]))} Wh/M on {_cards(best[(a_name, g)]['num_gpus'])} at a running batch of {fmt(best[(a_name, g)]['avg_batch_size'], 0)}, "
                           f"BF16 {fmt(cfg_wh(best[(b_name, g)]))} Wh/M on {_cards(best[(b_name, g)]['num_gpus'])} at {fmt(best[(b_name, g)]['avg_batch_size'], 0)}" for g in gpus)
        why = (f"The same model weights at two precisions. FP8 stores each weight in one byte and BF16 in two, so an FP8 row moves half the bytes per token from memory and the model fits on fewer cards or leaves more memory for batching. "
               f"{verdict} ({detail}). Where the FP8 row costs more, the reason is in the table: the two rows were swept to different card counts and reached different running batches, and a quieter row carries a higher energy per token whatever its precision. "
               f"Quantisation is the cheapest energy lever after load, but these rows show it only pays when the serving configuration is matched; the model pages hold every configuration so the pair can be re-cut at the same cards and cap.")
    else:  # moe-experts
        why = (f"Two mixture-of-experts models with the same active parameters per token ({aa:g} B) and very different totals: {esc(a_name)} routes across 16 experts ({pa:g} B in all), {esc(b_name)} across 128 ({pb:g} B). "
               f"The work per token is similar; the memory is not, so the larger model needs more cards to hold its experts and spreads each token's work across them. {sweep_note} "
               f"The index row ratio on the {lead_g} is {lead_r:.2f}×: the price of holding the extra experts, at the running batches stated in the table.")
    tiles_html = "".join(
        f"<div class=\"tile{' ref' if i == 0 else ''}\"><span class=\"lbl\">{g}, index rows</span><span class=\"val\">{ratios[g]:.2f}<small>×</small></span>"
        f"<span class=\"sub\">{esc(b_name)} {fmt(cfg_wh(best[(b_name, g)]))} Wh/M on {best[(b_name, g)]['num_gpus']} × {g} against {esc(a_name)} {fmt(cfg_wh(best[(a_name, g)]))} Wh/M on {best[(a_name, g)]['num_gpus']} × {g}.</span></div>"
        for i, g in enumerate(gpus))
    tiles_html += (f"<div class=\"tile\"><span class=\"lbl\">Parameters</span><span class=\"val\">{pr:.1f}<small>×</small></span>"
                   f"<span class=\"sub\">{esc(b_name)} {_params(mb)}; {esc(a_name)} {_params(ma)}.</span></div>")
    tiles = f"<div class=\"tiles auto n{len(gpus) + 1}\" role=\"group\" aria-label=\"Headline readings\">{tiles_html}</div>"
    table_rows = "\n".join(
        f"<tr><th scope=\"row\">{g}</th><td><a class=\"model\" href=\"{{{{ROOT}}}}models/{slug(n)}/\">{esc(n)}</a></td><td class=\"num\">{c['num_gpus']} × {g}</td><td class=\"num\">{precision_label(c['weight_precision'])}</td>"
        f"<td class=\"num\">{fmt(c['avg_batch_size'], 0)}</td><td class=\"num\">{fmt(c['avg_power_watts'], 0)}</td><td class=\"num\">{fmt(c['output_throughput_tokens_per_sec'], 0)}</td>"
        f"<td class=\"num key\">{fmt(cfg_wh(c))}</td><td class=\"num\">{fmt(c['avg_output_len'], 0)}</td><td class=\"num\">{_per_answer(c):.3f}</td><td class=\"num\">{fmt(kg_per_billion(cfg_wh(c), world))}</td></tr>"
        for g, ca, cb, _ in rows for n, c in ((a_name, ca), (b_name, cb)))
    diff_rows = and_list([f"{fmt(abs(cfg_wh(cb) - cfg_wh(ca)))} Wh/M on the {g} ({fmt(abs(cfg_wh(cb) - cfg_wh(ca)))} kWh per billion tokens)" for g, ca, cb, _ in rows])
    yes_no = ("Yes, on these rows: " if b_more_everywhere else "No, on these rows: " if b_less_everywhere else "It depends on the GPU: ")
    faq = [
        (f"Is {a_name} more energy-efficient than {b_name}?",
         yes_no + f"on the ML.ENERGY Leaderboard's index rows, {b_name} uses " + and_list([f"{ratios[g]:.2f}× the GPU energy per output token of {a_name} on the {g} ({fmt(cfg_wh(best[(b_name, g)]))} against {fmt(cfg_wh(best[(a_name, g)]))} Wh per million output tokens)" for g in gpus])
         + ". These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch."),
        (f"How much more energy does {b_name} use per million tokens than {a_name}?",
         (f"The index rows differ by {diff_rows}" + ("" if b_more_everywhere else f"; where the ratio is under 1, {b_name} is the lower row") + f". Per answer, at each row's own average output length, {a_name} costs "
          + and_list([f"{_per_answer(best[(a_name, g)]):.3f} Wh on the {g}" for g in gpus]) + f" and {b_name} " + and_list([f"{_per_answer(best[(b_name, g)]):.3f} Wh on the {g}" for g in gpus]) + ".")),
        {"size": (f"Does the bigger model cost more per answer?",
                  f"Yes, at these rows: on the {lead_g}, {_per_answer(lead_a):.3f} Wh for {a_name} against {_per_answer(lead_b):.3f} Wh for {b_name}, using each row's own average output length ({fmt(lead_a['avg_output_len'], 0)} and {fmt(lead_b['avg_output_len'], 0)} tokens). The larger model also needs more cards to hold its weights ({lead_a['num_gpus']} against {lead_b['num_gpus']} on the {lead_g}). Whether its answers are worth the difference is a question about the task, not the index."),
         "cross": (f"Does {b_name} cost more per answer than {a_name}?",
                   f"At these rows, on the {lead_g}: {_per_answer(lead_a):.3f} Wh for {a_name} against {_per_answer(lead_b):.3f} Wh for {b_name}, using each row's own average output length ({fmt(lead_a['avg_output_len'], 0)} and {fmt(lead_b['avg_output_len'], 0)} tokens). The two differ in family and in size ({pr:.1f}× the parameters), and the rows differ in cards ({lead_a['num_gpus']} against {lead_b['num_gpus']}) and running batch, so the per-answer figure is a reading, not a verdict on either architecture."),
         "family": (f"Why do two models of the same size differ in energy per token?",
                    f"Architecture (depth, width, attention design), vocabulary and, on the leaderboard, the configuration swept for each model: card count, cap and the running batch actually reached. On the {lead_g} the rows here ran at running batches of {fmt(lead_a['avg_batch_size'], 0)} ({a_name}) and {fmt(lead_b['avg_batch_size'], 0)} ({b_name}); a quieter row carries a higher energy per token whatever its architecture. The gap is {max(abs(1 - r) for r in ratios.values()) * 100:.0f} percent at most, inside what load alone moves."),
         "dense-vs-moe": (f"Does a mixture-of-experts model use less energy per token than a dense one?",
                          f"At a similar total size, on these rows, yes: {a_name} activates {aa:g} B of {pa:g} B parameters per token and its {lead_g} index row uses {fmt(cfg_wh(lead_a))} Wh/M against {fmt(cfg_wh(lead_b))} for the dense {b_name} ({pb:g} B), {1 / lead_r:.2f}× less. The mixture-of-experts model reads about {ab / aa:.0f}× fewer weights per token; it still needs memory for all of them, so the saving is in energy per token, not in cards."),
         "moe-size": (f"Does the larger mixture-of-experts model cost more energy per token?",
                      f"On the {lead_g} index rows, yes: {b_name} ({ab:g} B active of {pb:g} B) uses {lead_r:.2f}× the GPU energy per output token of {a_name} ({aa:g} B active of {pa:g} B), {fmt(cfg_wh(lead_b))} against {fmt(cfg_wh(lead_a))} Wh/M, on {lead_b['num_gpus']} and {lead_a['num_gpus']} cards at running batches of {fmt(lead_b['avg_batch_size'], 0)} and {fmt(lead_a['avg_batch_size'], 0)}. Active parameters set the work per token; total parameters set the cards."),
         "precision": (f"Does FP8 save energy compared with BF16 for the same model?",
                       (("Not consistently on these index rows. " if any(r <= 1 for r in ratios.values()) and any(r > 1 for r in ratios.values()) else
                         "Not on these index rows. " if all(r <= 1 for r in ratios.values()) else "Yes, on these index rows. ")
                        + (lambda t: t[0].upper() + t[1:])("; ".join(f"on the {g} the FP8 row ({a_name}) uses {fmt(cfg_wh(best[(a_name, g)]))} Wh/M on {best[(a_name, g)]['num_gpus']} card{'s' if best[(a_name, g)]['num_gpus'] > 1 else ''} at a running batch of {fmt(best[(a_name, g)]['avg_batch_size'], 0)} and the BF16 row {fmt(cfg_wh(best[(b_name, g)]))} Wh/M on {best[(b_name, g)]['num_gpus']} at {fmt(best[(b_name, g)]['avg_batch_size'], 0)}" for g in gpus))
                        + ". FP8 halves the bytes moved per token and the memory the weights take, but the leaderboard swept the two variants to different card counts and loads, and load moves energy per token more than precision does. A matched run, same cards and same cap, is the comparison to ask a vendor for.")),
         "moe-experts": (f"Do more experts cost more energy per token at the same active parameters?",
                         f"On these rows, yes: with {aa:g} B active parameters each, {b_name} ({pb:g} B in all) uses {lead_r:.2f}× the GPU energy per output token of {a_name} ({pa:g} B) on the {lead_g}, {fmt(cfg_wh(lead_b))} against {fmt(cfg_wh(lead_a))} Wh/M. The extra experts must be held in memory and the token's work spread across more cards ({lead_b['num_gpus']} against {lead_a['num_gpus']}), which is the energy the table shows.")}[angle],
        ("Why are the two rows not like for like?",
         f"The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the {lead_g} the rows here ran on {lead_a['num_gpus']} and {lead_b['num_gpus']} cards at running batches of {fmt(lead_a['avg_batch_size'], 0)} and {fmt(lead_b['avg_batch_size'], 0)}. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch."),
        ("Where do these figures come from?",
         f"The ML.ENERGY Leaderboard v3.0 (data compiled {long_date(SRC_MLE['compiled'])}, retrieved {long_date(RETRIEVED)}), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under {ITL_DEADLINE_MS} ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, {fmt(world, 0)} gCO2e per kWh (Ember, {EMBER_YEAR})."),
    ]
    faq_html = "<section id=\"faq\"><p class=\"eyebrow\">Questions</p><h2>Asked about " + esc(a_name) + " against " + esc(b_name) + "</h2><div class=\"prose faq\">" + "".join(f"<h3>{esc(q)}</h3><p>{esc(a)}</p>" for q, a in faq) + "</div></section>"
    angle_label = {"size": "Two sizes", "cross": "Two families, two sizes", "family": "Two families, one size", "dense-vs-moe": "Dense against mixture of experts",
                   "moe-size": "Two mixture-of-experts sizes", "precision": "Two precisions", "moe-experts": "Two expert counts"}[angle]
    body = f"""<div class="title">
  <p class="eyebrow"><a href="{{{{ROOT}}}}compare/">Compare</a> · {angle_label} · {and_list(gpus)}</p>
  <h1>{esc(a_name)} vs {esc(b_name)}: GPU energy per million output tokens</h1>
  <p class="stand">{answer}</p>
  <p class="unit"><b>Unit</b> watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. <b>Data</b> <a href="{{{{ROOT}}}}api/v1/models/{slug(a_name)}.json">{slug(a_name)}.json</a>, <a href="{{{{ROOT}}}}api/v1/models/{slug(b_name)}.json">{slug(b_name)}.json</a>. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#rows">The rows</a></li><li><a href="#why">What explains it</a></li><li><a href="#faq">Questions</a></li><li><a href="#sources">Sources</a></li></ul>
</div>
{tiles}
<p class="after-tiles">Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under {{{{ITL}}}} ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.</p>

<section id="rows" class="first">
  <p class="eyebrow">The rows</p>
  <h2>Index rows on every GPU both models share</h2>
  <div class="table-scroll"><table><caption>Index rows for {esc(a_name)} and {esc(b_name)}, with the configuration behind each and the per-answer and carbon readings</caption>
  <thead><tr><th scope="col">GPU</th><th scope="col">Model</th><th scope="col" class="num">Cards</th><th scope="col" class="num">Precision</th><th scope="col" class="num">Running batch</th><th scope="col" class="num">GPU W</th><th scope="col" class="num">Tokens / s</th><th scope="col" class="num">Wh / M</th><th scope="col" class="num">Output tokens</th><th scope="col" class="num">Wh per answer</th><th scope="col" class="num">kg CO2e / bn tokens, world grid</th></tr></thead><tbody>
{table_rows}
  </tbody></table></div>
  <p class="note">Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's <code>num_requests_running</code>). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, {fmt(world, 0)} gCO2e per kWh (Ember, {EMBER_YEAR}); the <a href="{{{{ROOT}}}}grids/">grid pages</a> price every model on each listed grid. Model names link to every measured configuration.</p>
</section>

<section id="why">
  <p class="eyebrow">What explains it</p>
  <h2>{angle_label}</h2>
  <div class="prose"><p>{why}</p>
  <p>Load still moves the number more than either model does: {esc(l32['model'])} on {l32['gpus']} spans {l32['ratio']:.1f}× between a running batch of {fmt(l32['first_batch'], 0)} and {fmt(l32['best_batch'], 0)} on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The <a href="{{{{ROOT}}}}glossary/running-batch/">running batch</a> and <a href="{{{{ROOT}}}}glossary/floor/">floor</a> entries define the terms.</p></div>
</section>
{faq_html}
<section id="sources">
  <p class="eyebrow">Sources</p>
  <h2>Where every figure came from</h2>
  <p class="note">{{{{MLE_BLOCK}}}}</p>
  <p class="note">Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, {EMBER_RELEASE}, world average {EMBER_YEAR}, CC BY 4.0, retrieved {{{{EMBER_RETRIEVED_LONG}}}}.</p>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
</section>"""
    assert l32["ratio"] > max(ratios.values()), f"the load sentence claims the ladder is wider than the gap; not true for {a_name} vs {b_name}"
    title = f"{a_name} vs {b_name}: GPU energy per million output tokens | Lead Green"
    desc_parts = and_list([f"{ratios[g]:.2f}× on the {g}" for g in gpus])
    for desc in (f"{b_name} uses {desc_parts} the GPU energy per output token of {a_name}, from the ML.ENERGY index rows: the figures, the sweep caveat and what explains the gap.",
                 f"{b_name} uses {desc_parts} the GPU energy per output token of {a_name}: the index rows, the sweep caveat and what explains the gap.",
                 f"{b_name} against {a_name} on GPU energy per output token: {desc_parts}, from the index rows.",
                 f"{b_name} vs {a_name}: {desc_parts} on GPU energy per output token, from the index rows.",
                 f"Two models on GPU energy per million output tokens: {desc_parts}, from the ML.ENERGY index rows."):
        if len(desc) <= 155:
            break
    card = {"a": a_name, "b": b_name, "angle": angle_label, "gpus": gpus, "ratios": ratios, "slug": _cmp_slug(a_name, b_name)}
    return title, desc, body, faq, card


compare_cards = []
for _a, _b, _angle in COMPARE_PAIRS:
    ct2, cd2, cb2, cfaq2, card_ = compare_pair_page(_a, _b, _angle)
    _lg = card_["gpus"][0]
    render(f"compare/{card_['slug']}/index.html", "models", ct2, cd2, "article", "answer", cb2,
           {"date": UPDATED, "faq": cfaq2, "name": f"{_a} vs {_b}", "crumbs": [("Compare", f"{SITE}/compare/")],
            "card": {"eyebrow": f"Compare · {_lg} index rows", "value": f"{card_['ratios'][_lg]:.2f}", "unit": "×",
                     "label": f"{_b} uses {card_['ratios'][_lg]:.2f}× the GPU energy per output token of {_a}."},
            "dataset": {"name": f"{_a} vs {_b}: GPU energy per million output tokens", "distribution": f"{SITE}/api/v1/index.json", "isBasedOn": SRC_MLE["url"]}})
    _lead_g = card_["gpus"][0]
    compare_cards.append(
        f"<div class=\"card\"><span class=\"k\">{esc(card_['angle'])} · {esc(and_list(card_['gpus']))}</span><h3><a href=\"{{{{ROOT}}}}compare/{card_['slug']}/\">{esc(_a)} vs {esc(_b)}</a></h3>"
        f"<span class=\"n\">{card_['ratios'][_lead_g]:.2f}×<small>{_lead_g} index rows</small></span>"
        f"<p>{esc(_b)} over {esc(_a)}, GPU energy per output token" + (f"; {card_['ratios'][card_['gpus'][1]]:.2f}× on the {card_['gpus'][1]}" if len(card_['gpus']) > 1 else "") + ".</p></div>")

_cmp_body = f"""<div class="title">
  <p class="eyebrow">Compare</p>
  <h1>{len(COMPARE_PAIRS)} model pairs, side by side</h1>
  <p class="stand">The comparisons people ask for, each on one page: a small model against a large one, two families at the same size, dense against mixture of experts, FP8 against BF16, and two expert counts at the same active size. Every page sets the two models' index rows beside each other on each GPU both were measured on, states the card count and running batch behind each row, and says what explains the gap. The GPU generations themselves are compared on <a href="{{{{ROOT}}}}h100-vs-b200/">H100 vs B200</a>.</p>
  <p class="unit"><b>Unit</b> watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated {{{{UPDATED_LONG}}}}.</p>
</div>

<section id="pairs" class="first">
  <p class="eyebrow">Pairs</p>
  <h2>Pick a comparison</h2>
  <div class="cards">
{chr(10).join(compare_cards)}
  </div>
  <p class="note">The ratio on each card is the second model's energy per token over the first's, on the GPU named, at the index rows; under 1 means the second model's row is the lower one. Any other pair can be read off <a href="{{{{ROOT}}}}models/">the model pages</a> or asked of the <a href="{{{{ROOT}}}}mcp/">MCP server</a>. Source: {{{{MLE_SHORT}}}}, Text Conversation, retrieved {{{{RETRIEVED_LONG}}}}.</p>
</section>"""
render("compare/index.html", "models", f"Compare: {len(COMPARE_PAIRS)} model pairs on GPU energy per million output tokens | Lead Green",
       "Model pairs people ask about, side by side on GPU energy per output token: small against large, dense against MoE, FP8 against BF16, two families.",
       "website", "page", _cmp_body)


# ---- FAQ hub: every FAQPage question on the site, each linking its canonical page (the per-page FAQPage stays the structured data)
def _first_sentence(a: str, limit: int = 240) -> str:
    a = a.strip()
    cut = len(a)
    for m_ in re.finditer(r"\.\s", a):
        if m_.start() >= 60:
            cut = m_.start() + 1
            break
    s_ = a[:cut].strip()
    if len(s_) > limit:
        s_ = s_[:limit].rsplit(" ", 1)[0].rstrip(",;:") + "..."
    return s_


_faq_groups = []   # (page name, url, [(q, a)]) in site order: home, why, per query, compare, glossary, models, grids
_order = [SITE + "/", f"{SITE}/why/", f"{SITE}/per-query/", f"{SITE}/h100-vs-b200/"]
_order += [f"{SITE}/compare/{_cmp_slug(a, b)}/" for a, b, _ in COMPARE_PAIRS]
_order += [f"{SITE}/glossary/{t['slug']}/" for t in GLOSSARY]
_seen_faq = set()
for _u in _order + [u for _, u, _ in faq_all]:
    for _n, _url, _faq in faq_all:
        if _url == _u and _url not in _seen_faq:
            _faq_groups.append((_n, _url, _faq)); _seen_faq.add(_url)
_faq_count = sum(len(f) for _, _, f in _faq_groups)
_faq_sections = []
for _n, _url, _faq in _faq_groups:
    _rel = _url[len(SITE) + 1:]
    _items = "".join(f"<h3>{esc(q)}</h3><p>{esc(_first_sentence(a))} <a href=\"{{{{ROOT}}}}{_rel}#faq\">Full answer</a></p>" for q, a in _faq)
    _faq_sections.append(f"<section id=\"{slug(_n) or 'home'}\"><p class=\"eyebrow\">{len(_faq)} questions</p><h2><a href=\"{{{{ROOT}}}}{_rel}\">{esc(_n)}</a></h2><div class=\"prose faq\">{_items}</div></section>")
_faq_toc = "".join(f"<li><a href=\"#{slug(n) or 'home'}\">{esc(n)}</a></li>" for n, _, _ in _faq_groups[:13])
_faq_body = f"""<div class="title">
  <p class="eyebrow">Questions</p>
  <h1>Every question the site answers</h1>
  <p class="stand">{_faq_count} questions from {len(_faq_groups)} pages, each with the first sentence of its answer and a link to the page that holds the full answer, the figure and the source. The questions are the ones people type: how much energy an AI query uses, what a million tokens costs in watt-hours, which grid is cleaner, what the regulator asks.</p>
  <p class="unit"><b>Unit</b> watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page">{_faq_toc}<li><a href="#models">Models</a></li><li><a href="#grids">Grids</a></li></ul>
</div>
<p class="after-tiles">Each page's questions are also published as FAQPage structured data on that page, so an assistant that reads one page gets the full answers; this hub is the human index of them. The glossary defines the terms the answers use.</p>
{chr(10).join(_faq_sections)}"""
# anchors for the two long runs of pages
_first_model = next((i for i, (n, u, _) in enumerate(_faq_groups) if "/models/" in u), None)
_first_grid = next((i for i, (n, u, _) in enumerate(_faq_groups) if "/grids/" in u), None)
if _first_model is not None:
    _faq_body = _faq_body.replace(f"<section id=\"{slug(_faq_groups[_first_model][0])}\">", f"<section id=\"models\">", 1)
if _first_grid is not None:
    _faq_body = _faq_body.replace(f"<section id=\"{slug(_faq_groups[_first_grid][0])}\">", f"<section id=\"grids\">", 1)
render("faq/index.html", "", f"FAQ: {_faq_count} questions about GPU energy per token, answered with sources | Lead Green",
       f"Every question the site answers, from {len(_faq_groups)} pages: energy per AI query, Wh per million tokens, carbon by grid, H100 against B200, the regulator.",
       "website", "faqhub", _faq_body, {"date": UPDATED, "questions": [(q, u) for _, u, f in _faq_groups for q, _a in f]})

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

# ----------------------------------------------------------------- GEO item 5 (20 October 2026): /changes/, the dated record on one URL
# Data changes come from CHANGES (the same list as changes.json and the index page), releases from the release folders, and the MCP
# server versions from MCP_RELEASES below. Nothing here touches an API document, so a frozen release stays frozen.
MCP_RELEASES = [
    ("0.3.1", "2026-10-20", "Ownership marker for the official MCP Registry in the package README; listed as ai.leadgreen/green-token-index. No code change.", True),
    ("0.3.0", "2026-10-20", "First release on PyPI, with provenance attestations and a reproducible wheel; the install line becomes pip install leadgreen-mcp.", True),
    ("0.2.0", "2026-09-28", "Running batch and num_gpus parameters on estimate, PUE and system power ratio for energy at the meter, the wheel's SHA-256 on the install line.", False),
    ("0.1.0", "2026-09-26", "First build: eight tools over the index, grid and hardware documents, live API first with a bundled snapshot as fallback.", False),
]
_frozen_for_page = ({l.strip() for l in (HERE / "data" / "published-releases.txt").read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
                    if (HERE / "data" / "published-releases.txt").exists() else set())
_rel_dir_for_page = API_DIR / "releases"
_release_rows = []
for _d in sorted((p.name for p in _rel_dir_for_page.iterdir() if p.is_dir()), reverse=True) if _rel_dir_for_page.exists() else []:
    _z = _rel_dir_for_page / f"leadgreen-api-v1-{_d}.zip"
    _sha = hashlib.sha256(_z.read_bytes()).hexdigest() if (_z.exists() and _d in _frozen_for_page) else ""
    _ch = [c for c in CHANGES if c["date"] == _d]
    _release_rows.append((_d, _d in _frozen_for_page, _sha, _ch[0]["documents"] if _ch else []))
_chg_items = "\n".join(
    f"    <li><time datetime=\"{c['date']}\">{short_date(c['date'])}</time><span>{esc(c['summary'])}"
    f"<br><small>Documents: {esc(', '.join('every document' if d == '*' else d for d in c['documents'])) or 'none (description only)'}. "
    f"Reason: {esc(c['reason'])}. Source version: {esc(str(c['source_version']))}.</small></span></li>" for c in reversed(CHANGES))
_rel_items = "\n".join(
    f"<tr><th scope=\"row\"><time datetime=\"{d}\">{short_date(d)}</time></th><td>{'published, frozen' if fr else 'built, not frozen'}</td>"
    f"<td>{esc(', '.join('every document' if x == '*' else x for x in docs)) or 'as the previous release'}</td>"
    f"<td><a href=\"{{{{ROOT}}}}api/v1/releases/leadgreen-api-v1-{d}.zip\">zip</a> · <a href=\"{{{{ROOT}}}}api/v1/releases/{d}/manifest.json\">manifest</a></td>"
    f"<td><code>{sha[:16] + '…' if sha else 'set when frozen'}</code></td></tr>" for d, fr, sha, docs in _release_rows)
_mcp_items = "\n".join(
    f"<tr><th scope=\"row\">{v}</th><td><time datetime=\"{d}\">{short_date(d)}</time></td><td>{esc(what)}</td>"
    f"<td>" + (f"<a href=\"{{{{ROOT}}}}dist/leadgreen_mcp-{v}-py3-none-any.whl\">wheel</a>" if (ROOT / "dist" / f"leadgreen_mcp-{v}-py3-none-any.whl").exists() else "not kept")
    + (f" · <a href=\"https://pypi.org/project/leadgreen-mcp/{v}/\">PyPI</a>" if on_pypi else "") + "</td></tr>" for v, d, what, on_pypi in MCP_RELEASES)
_latest_change = CHANGES[-1]
_changes_stand = (f"The latest change to the data is dated {long_date(_latest_change['date'])}: "
                  f"{_first_sentence(_latest_change['summary'], 200)} Every entry below is also in "
                  f"<a href=\"{{{{ROOT}}}}api/v1/changes.json\">changes.json</a>, and every dated release is kept unchanged for citation.")
_changes_body = f"""<div class="title">
  <p class="eyebrow">Changes</p>
  <h1>Every change, dated</h1>
  <p class="stand">{_changes_stand}</p>
  <p class="unit"><b>Record</b> {len(CHANGES)} data changes since {long_date(CHANGES[0]['date'])} · {len(_release_rows)} dated releases ({sum(1 for r in _release_rows if r[1])} published) · {len(MCP_RELEASES)} MCP server versions. Updated {{{{UPDATED_LONG}}}}.</p>
  <ul class="toc" aria-label="On this page"><li><a href="#data">Data changes</a></li><li><a href="#releases">Data releases</a></li><li><a href="#mcp">MCP server</a></li><li><a href="#cite">Citing a release</a></li></ul>
</div>

<section id="data" class="first">
  <p class="eyebrow">Data changes</p>
  <h2>What changed in the published figures, newest first</h2>
  <ul class="changes">
{_chg_items}
  </ul>
  <p class="note">A change is recorded when a figure, a field or a description in <a href="{{{{ROOT}}}}api/">the data API</a> moves. Page copy that does not touch a figure is not listed. The index page carries the same record under <a href="{{{{ROOT}}}}index/#changes">Changes</a>.</p>
</section>

<section id="releases">
  <p class="eyebrow">Data releases</p>
  <h2>Dated copies of api/v1, newest first</h2>
  <div class="table-scroll"><table class="spec"><caption>Each release is the whole API as it stood on that date</caption>
  <thead><tr><th scope="col">Release</th><th scope="col">Status</th><th scope="col">Documents that changed</th><th scope="col">Files</th><th scope="col">Zip SHA-256</th></tr></thead>
  <tbody>
{_rel_items}
  </tbody></table></div>
  <p class="note">A published release never changes: the build refuses to rewrite it. The current live files are release {DATA_VERSION}. The list with full hashes is <a href="{{{{ROOT}}}}api/v1/releases/index.json">releases/index.json</a>.</p>
</section>

<section id="mcp">
  <p class="eyebrow">MCP server</p>
  <h2>leadgreen-mcp versions</h2>
  <div class="table-scroll"><table class="spec"><caption>The package is versioned separately from the data; it reads the live API first</caption>
  <thead><tr><th scope="col">Version</th><th scope="col">Date</th><th scope="col">What changed</th><th scope="col">Files</th></tr></thead>
  <tbody>
{_mcp_items}
  </tbody></table></div>
  <p class="note">Install and client configuration are on the <a href="{{{{ROOT}}}}mcp/">MCP page</a>. The server is listed on the official MCP Registry as <code>ai.leadgreen/green-token-index</code>.</p>
</section>

<section id="cite">
  <p class="eyebrow">Citing a release</p>
  <h2>Cite a date, not the live files</h2>
  <div class="prose"><p>Quote the release date with the figure, for example "Lead Green, release {DATA_VERSION}", and link the release zip or any file under its dated folder; both stay byte for byte as published. The repository's <code>CITATION.cff</code> and the Zenodo record (<a href="{ZENODO_DOI_URL}">{ZENODO_DOI_URL.replace('https://', '')}</a>) carry the same version. The feed at <a href="{{{{ROOT}}}}feed.xml">feed.xml</a> announces blog posts, not data changes; watch <a href="{{{{ROOT}}}}api/v1/changes.json">changes.json</a> or this page for those.</p></div>
  <p class="note"><b>Cite as.</b> {{{{CITE_AS}}}}</p>
</section>"""
render("changes/index.html", "", "Changes: every dated update to the Lead Green data, releases and MCP server",
       f"The dated record: {len(CHANGES)} changes to the published figures since {long_date(CHANGES[0]['date'])}, every frozen data release with its hash, and each leadgreen-mcp version.",
       "website", "changes", _changes_body, {"date": UPDATED})


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
- Publisher and funder: {FUNDING}
- Contact: {CONTACT_EMAIL}, for corrections, measurements and data requests, answered within {word(RESPONSE_DAYS)} working days.
- {LEGAL_NOTE} The EU AI Act asks providers of general-purpose AI models for training energy in MWh, held for the AI Office; no law asks anyone for serving energy per token.

## Pages
- [Home]({SITE}/): what Lead Green is, why it exists, who it is for
- [Why it matters]({SITE}/why/): nine reasons the number belongs in procurement, operations and reporting, with an RFP clause
- [The index]({SITE}/index/): the full tables, method, sources ledger and change record
- [Models]({SITE}/models/): one page per model, with every measured configuration, H100 against B200 and carbon by grid
- [H100 vs B200]({SITE}/h100-vs-b200/): the {len(pairs)} models measured on both cards, the gap per model and how much of it is the sweep
- [Grids]({SITE}/grids/): one page per listed grid, the whole index priced on it, the trend since 2023 and the reporting line
- [How much energy does an AI query use?]({SITE}/per-query/): per prompt against per million tokens, with Google's and Mistral's published figures and the AI Energy Score on one page
- [Compare]({SITE}/compare/): {len(COMPARE_PAIRS)} model pairs side by side on GPU energy per output token (small against large, dense against MoE, BF16 against FP8, two families, two expert counts), one page each
- [Glossary]({SITE}/glossary/): {len(GLOSSARY)} defined terms, one page each with the figure and the source (Wh/M, energy per token, running batch, floor, GPU-only boundary, location-based intensity, kg CO2e per billion tokens, inter-token latency ceiling, PUE)
- [Questions]({SITE}/faq/): every question the site answers, each linking the page with the full answer
- [Data API]({SITE}/api/): read-only JSON, CORS open, CC BY 4.0
- [MCP server]({SITE}/mcp/): tools for AI assistants (list_models, energy_per_million_tokens, estimate, compare_gpus, concurrency_curve, grid_intensity, gpu_hardware, sources)
- [Blog]({SITE}/blog/): RSS at {SITE}/feed.xml
- [Newsletter]({SITE}/newsletter/)
- [Contribute]({SITE}/contribute/): volunteer roles and the measurement protocol
- [About]({SITE}/about/)

## Models (one page each; the figure is the lowest index row, GPU only, a floor)
""" + "\n".join(
    f"- [{m['name']}]({SITE}/models/{s}/): {fmt(min(cfg_wh(best[(m['name'], g)]) for g in m['gpus']))} Wh/M on {min(m['gpus'], key=lambda g: cfg_wh(best[(m['name'], g)]))}"
    for s, m in sorted(models.items(), key=lambda kv: min(cfg_wh(best[(kv[1]['name'], g)]) for g in kv[1]['gpus']))) + f"""

## Data API (JSON)
""" + "\n".join(f"- {SITE}/api/v1/{p}: {d}" for p, d in ENDPOINTS) + f"""

## Sources
- {SRC_MLE['name']} ({SRC_MLE['publisher']}), {SRC_MLE['version']}, {SRC_MLE['licence']}: {SRC_MLE['url']}
- {SRC_EMBER['name']}, {SRC_EMBER['version']}, {SRC_EMBER['licence']}: {SRC_EMBER['url']}
- NVIDIA Multi-Instance GPU User Guide, supported MIG profiles: https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-mig-profiles.html
- NVIDIA product specifications: https://www.nvidia.com/en-us/data-center/a100/, https://www.nvidia.com/en-us/data-center/h100/, https://www.nvidia.com/en-us/data-center/h200/, https://www.nvidia.com/en-us/data-center/dgx-b200/
- NVIDIA, Product Carbon Footprint Summary for HGX B200: https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf
- {SRC_AIES['name']} ({SRC_AIES['publisher']}), {SRC_AIES['version']}: {SRC_AIES['url']}

## Licence
{LICENCE_TEXT} Code: Apache 2.0.
"""

# ----------------------------------------------------------------- Markdown copies of every page (for crawlers and assistants), and IndexNow bookkeeping
from html.parser import HTMLParser
from urllib.parse import urljoin


class _MD(HTMLParser):
    """Turn the site's own <main> HTML into Markdown. Covers the tags the pages use: headings, paragraphs,
    lists, tables with captions, details/summary, pre, inline code, bold, italics, links, line breaks."""
    BLOCK = {"p", "h1", "h2", "h3", "li", "caption", "summary", "pre", "div", "section", "ul", "ol", "table", "thead", "tbody", "tr", "article", "details", "main"}
    SKIP = {"svg", "script", "style", "button", "nav", "header", "footer"}

    def __init__(self, base_url: str):
        super().__init__(convert_charrefs=True)
        self.base, self.out, self.skip, self.stack = base_url, [], 0, []
        self.in_main = False
        self.table = None      # {"caption": str, "rows": [[cells]], "head": bool}
        self.cell = None
        self.li_stack: list[tuple[str, int]] = []
        self.pre = False
        self.href = None
        self.cls: list[tuple[str, str]] = []   # (tag, class) for p, span and div, so end tags close what start tags opened
        self.i_skip: list[bool] = []            # the bar chart <i style=...> elements carry no text and are skipped

    def _emit(self, s: str) -> None:
        if self.cell is not None:
            self.cell.append(s)
        else:
            self.out.append(s)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "main":
            self.in_main = True
            return
        if not self.in_main:
            return
        if tag in self.SKIP:
            self.skip += 1
            return
        if self.skip:
            return
        if tag == "table":
            self.table = {"caption": "", "rows": [], "head": False}
        elif tag == "caption" and self.table is not None:
            self.cell = []
        elif tag == "thead":
            self.table["head"] = True
        elif tag == "tr" and self.table is not None:
            self.table["rows"].append([])
        elif tag in ("th", "td") and self.table is not None and self.table["rows"]:
            self.cell = []
        elif tag in ("h1", "h2", "h3"):
            self._emit("\n\n" + "#" * int(tag[1]) + " ")
        elif tag == "p":
            self.cls.append((tag, a.get("class", "")))
            self._emit("\n\n*" if "eyebrow" in a.get("class", "") else "\n\n")
        elif tag == "div":
            self.cls.append((tag, a.get("class", "")))
            if "tile" in a.get("class", "").split():
                self._emit("\n- ")
        elif tag == "span":
            c = a.get("class", "")
            self.cls.append((tag, c))
            if c == "lbl":
                self._emit("**")
        elif tag in ("ul", "ol"):
            self.li_stack.append((tag, 0))
            self._emit("\n")
        elif tag == "li" and self.li_stack:
            t, n = self.li_stack[-1]
            self.li_stack[-1] = (t, n + 1)
            self._emit("\n" + ("  " * (len(self.li_stack) - 1)) + ("- " if t == "ul" else f"{n + 1}. "))
        elif tag == "summary":
            self._emit("\n\n**")
        elif tag == "pre":
            self.pre = True
            self._emit("\n\n```\n")
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("b", "strong"):
            self._emit("**")
        elif tag == "i":
            self.i_skip.append("style" in a)
            if "style" in a:
                self.skip += 1
            else:
                self._emit("*")
        elif tag == "em":
            self._emit("*")
        elif tag == "a" and a.get("href"):
            self.href = urljoin(self.base, a["href"])
            self._emit("[")
        elif tag == "br":
            self._emit("  \n" if self.cell is None else " ")
        elif tag == "small":
            self._emit(" ")

    def handle_endtag(self, tag):
        if tag == "main":
            self.in_main = False
            return
        if not self.in_main:
            return
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == "caption" and self.table is not None:
            self.table["caption"] = "".join(self.cell).strip()
            self.cell = None
        elif tag in ("th", "td") and self.cell is not None and self.table is not None:
            self.table["rows"][-1].append(re.sub(r"\s+", " ", "".join(self.cell)).strip().replace("|", "\\|"))
            self.cell = None
        elif tag == "table" and self.table is not None:
            rows = [r for r in self.table["rows"] if r]
            if rows:
                width = max(len(r) for r in rows)
                rows = [r + [""] * (width - len(r)) for r in rows]
                head, body = (rows[0], rows[1:]) if self.table["head"] else ([""] * width, rows)
                lines = ["| " + " | ".join(head) + " |", "|" + "---|" * width] + ["| " + " | ".join(r) + " |" for r in body]
                self.out.append("\n\n" + (f"*{self.table['caption']}*\n\n" if self.table["caption"] else "") + "\n".join(lines))
            self.table = None
        elif tag in ("ul", "ol") and self.li_stack:
            self.li_stack.pop()
            self._emit("\n")
        elif tag == "summary":
            self._emit("**")
        elif tag in ("p", "div", "span"):
            c = ""
            for i in range(len(self.cls) - 1, -1, -1):
                if self.cls[i][0] == tag:
                    c = self.cls.pop(i)[1]
                    break
            if tag == "p" and "eyebrow" in c:
                self._emit("*")
            elif tag == "span" and c == "lbl":
                self._emit(":** ")
            elif tag == "span" and c == "val":
                self._emit(" ")
        elif tag == "pre":
            self.pre = False
            self._emit("\n```\n")
        elif tag == "code" and not self.pre:
            self._emit("`")
        elif tag in ("b", "strong"):
            self._emit("**")
        elif tag == "i":
            if self.i_skip and self.i_skip.pop():
                self.skip = max(0, self.skip - 1)
            else:
                self._emit("*")
        elif tag == "em":
            self._emit("*")
        elif tag == "a" and self.href:
            self._emit(f"]({self.href})")
            self.href = None

    def handle_data(self, data):
        if not self.in_main or self.skip:
            return
        if self.pre:
            self._emit(data)
        else:
            self._emit(re.sub(r"[ \t\r\n]+", " ", data))

    def text(self) -> str:
        s = "".join(self.out)
        s = re.sub(r"\*\*\s*\*\*", "", s)          # empty bold from icon-only spans
        s = re.sub(r"[ \t]+\n", "\n", s)
        s = re.sub(r"\n{3,}", "\n\n", s)
        s = re.sub(r"^\s*(#+ )", r"\1", s, count=1)
        return s.strip() + "\n"



def to_markdown(page_html: str, url: str, title: str, desc: str) -> str:
    p = _MD(url)
    p.feed(page_html)
    body = p.text()
    head = (f"> {desc}\n>\n> Lead Green, a Katonic project. Canonical page: {url} (this file: {url}index.md). Updated {long_date(UPDATED)}, data version {DATA_VERSION}. "
            f"Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. {CAVEAT} Machine-readable data: {SITE}/api/v1/ (see llms.txt).\n\n")
    m = re.search(r"^# .+$", body, re.M)
    if m:
        first = m.group(0)
        body = re.sub(r"\n{3,}", "\n\n", body[:m.start()] + body[m.end():]).strip("\n") + "\n"
        return first + "\n\n" + head + body
    return f"# {title}\n\n" + head + body


_md_urls = []
for _rel in sorted(k for k in list(outputs) if k.endswith("index.html")):
    _url = f"{SITE}/{_rel[:-len('index.html')]}"
    _html = outputs[_rel]
    _t = html.unescape(re.search(r"<title>(.*?)</title>", _html, re.S).group(1))
    _d = html.unescape(re.search(r'<meta name="description" content="([^"]*)"', _html).group(1))
    outputs[_rel[:-len("index.html")] + "index.md"] = to_markdown(_html, _url, _t, _d)
    _md_urls.append(_url + "index.md")
outputs["llms.txt"] += "\n## Markdown copies\nEvery page has a Markdown copy at its URL followed by index.md, generated from the same build and linked from the page head (rel=alternate, text/markdown).\n" + "\n".join(f"- {u}" for u in _md_urls) + "\n"
# llms-full.txt: the Markdown copies concatenated in sitemap order, for an assistant that fetches one file
_full_parts = []
for _u, _ in sitemap:
    _rel = _u[len(SITE) + 1:] + "index.md"
    if _rel in outputs:
        _full_parts.append(outputs[_rel].rstrip("\n") + "\n")
outputs["llms-full.txt"] = (f"# Lead Green: every page in full\n\n> The Markdown copy of every page on {SITE}, in sitemap order, built {long_date(UPDATED)}, data version {DATA_VERSION}. "
                            f"Each page begins with its title and canonical URL. The short index is {SITE}/llms.txt; the data is {SITE}/api/v1/. CC BY 4.0 for the compilation and text; sources keep their own licences.\n\n---\n\n"
                            + "\n---\n\n".join(_full_parts))
outputs["llms.txt"] += f"\n## Full text\n- {SITE}/llms-full.txt: every Markdown copy above in one file, sitemap order, {len(_full_parts)} pages.\n"
outputs["llms.txt"] += (f"\n## Changes and API description\n- {SITE}/changes/: the dated record of every change to the figures, every frozen data release with its hash, and each MCP server version.\n"
                        f"- {SITE}/openapi.json: the OpenAPI 3.1 description, also at {SITE}/api/v1/openapi.json; the API catalogue (RFC 9727) is {SITE}/.well-known/api-catalog.\n")

# IndexNow: the build cannot ping (the URLs and the key file must be live), so it records what changed and build/indexnow.py pings after a deploy.
INDEXNOW_KEY_FILE = HERE / "indexnow-key.txt"
if not INDEXNOW_KEY_FILE.exists():
    import secrets as _secrets
    INDEXNOW_KEY_FILE.write_text(_secrets.token_hex(16) + "\n", encoding="utf-8")
INDEXNOW_KEY = INDEXNOW_KEY_FILE.read_text(encoding="utf-8").strip()
outputs[f"{INDEXNOW_KEY}.txt"] = INDEXNOW_KEY + "\n"      # IndexNow verifies ownership by fetching <site>/<key>.txt
_url_hashes = {}
for _rel, _text in outputs.items():
    if _rel.endswith("index.html"):
        _url_hashes[f"{SITE}/{_rel[:-len('index.html')]}"] = hashlib.sha256(_text.encode("utf-8")).hexdigest()
for _rel in api_docs:
    if "{" not in _rel:
        _url_hashes[f"{SITE}/api/v1/{_rel}"] = hashlib.sha256(jdump(api_docs[_rel]).encode("utf-8")).hexdigest()
_state_file = HERE / "indexnow-state.json"
_state = json.loads(_state_file.read_text(encoding="utf-8")) if _state_file.exists() else {}
_changed = sorted(u for u, h in _url_hashes.items() if _state.get(u) != h)
(HERE / "indexnow-current.json").write_text(jdump(_url_hashes), encoding="utf-8", newline="\n")
(HERE / "indexnow-changed.txt").write_text("\n".join(_changed) + ("\n" if _changed else ""), encoding="utf-8", newline="\n")

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
# D16: a dated release that has been published never changes
RELEASES = API_DIR / "releases"
frozen = ({l.strip() for l in PUBLISHED_RELEASES.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")}
          if PUBLISHED_RELEASES.exists() else set())
if DATA_VERSION in frozen:
    for rel, doc in api_docs.items():
        old = RELEASES / DATA_VERSION / rel
        if not old.exists() or old.read_text(encoding="utf-8") != jdump(doc):
            problems.append(f"release {DATA_VERSION} is published and frozen, but {rel} would change: bump UPDATED")
for rel, text in outputs.items():   # D10: search engines cut meta descriptions at about 155 characters
    for d in re.findall(r'<meta name="description" content="([^"]*)"', text):
        if len(html.unescape(d)) > 155:
            problems.append(f"{rel}: meta description is {len(html.unescape(d))} characters, over 155")
if problems:
    sys.exit("REFUSING TO WRITE:\n  " + "\n  ".join(problems))

for rel, text in outputs.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8", newline="\n")
for rel, data in outputs_bin.items():
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    if not p.exists() or p.read_bytes() != data:
        p.write_bytes(data)
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


# D16 / D20: the dated release, its zip, and the list of releases
rel_dir = RELEASES / DATA_VERSION
for rel, doc in api_docs.items():
    p = rel_dir / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(jdump(doc), encoding="utf-8", newline="\n")
_stamp = tuple(int(x) for x in DATA_VERSION.split("-")) + (0, 0, 0)
zip_path = RELEASES / f"leadgreen-api-v1-{DATA_VERSION}.zip"
with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(api_docs):
        info = zipfile.ZipInfo(f"leadgreen-api-v1-{DATA_VERSION}/{rel}", date_time=_stamp)
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, jdump(api_docs[rel]).encode("utf-8"))
_releases = []
for d in sorted((p.name for p in RELEASES.iterdir() if p.is_dir()), reverse=True):
    _releases.append({"date": d, "url": f"{SITE}/api/v1/releases/{d}/", "zip": f"{SITE}/api/v1/releases/leadgreen-api-v1-{d}.zip",
                      "sha256": hashlib.sha256((RELEASES / f"leadgreen-api-v1-{d}.zip").read_bytes()).hexdigest()
                      if (RELEASES / f"leadgreen-api-v1-{d}.zip").exists() else None,
                      "published": d in frozen})
(RELEASES / "index.json").write_text(jdump({"version": "1", "updated": UPDATED, "current": DATA_VERSION,
    "note": "A release listed as published never changes. Cite a release, not the live files.", "releases": _releases}),
    encoding="utf-8", newline="\n")

shutil.copyfile(zip_path, API_DIR / "all.zip")

sync_tree(API_DIR, MCP_DATA, skip=("releases", "all.zip", "index.csv", "types.d.ts"))

# T3: citation metadata at the repository root, regenerated every build so version and date never drift from DATA_VERSION.
# CITATION.cff is what GitHub renders as "Cite this repository"; .zenodo.json is the metadata Zenodo reads when it archives a release.
_given, _family = EDITOR.split(" ", 1)
_cite_title = f"{INDEX_NAME}: GPU energy per million output tokens, by model, GPU and configuration, with grid carbon intensity"
_keywords = ["LLM inference energy", "watt-hours per token", "GPU energy", "grid carbon intensity", "green AI", "open data", "MCP server"]
def _yq(v: str) -> str:
    return json.dumps(v, ensure_ascii=False)   # a JSON string is a valid double-quoted YAML scalar
_cff = ["cff-version: 1.2.0",
        f"message: {_yq('If you use this index, cite the dated release you used; the list is at ' + SITE + '/api/v1/releases/index.json.')}",
        "type: dataset", f"title: {_yq(_cite_title)}", f"version: {_yq(DATA_VERSION)}", f"date-released: {_yq(DATA_VERSION)}",
        f"url: {_yq(SITE + '/')}", *([f"repository-code: {_yq(REPO_URL)}"] if REPO_URL else []), "license: CC-BY-4.0",
        *([f"doi: {_yq(ZENODO_CONCEPT_DOI)}"] if ZENODO_CONCEPT_DOI else []),
        "authors:", f"  - family-names: {_yq(_family)}", f"    given-names: {_yq(_given)}", "    affiliation: Katonic",
        f"  - name: {_yq(PUBLISHER_ENTITY + ' (Lead Green, a Katonic project)')}",
        f"abstract: {_yq(PROJECT_DESCRIPTION + ' ' + CAVEAT)}",
        "keywords:", *[f"  - {_yq(k)}" for k in _keywords],
        "references:",
        "  - type: conference-paper", f"    title: {_yq('The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization')}",
        "    authors:", "      - name: Chung et al.", f"    url: {_yq(SRC_MLE['cite_url'])}", "    notes: NeurIPS 2025 Datasets and Benchmarks",
        "  - type: data", f"    title: {_yq(SRC_EMBER['name'])}", "    authors:", "      - name: Ember", f"    url: {_yq(SRC_EMBER['url'])}",
        f"    notes: {_yq(SRC_EMBER['version'])}"]
(ROOT / "CITATION.cff").write_text("\n".join(_cff) + "\n", encoding="utf-8", newline="\n")
_zenodo = {
    "upload_type": "dataset", "title": _cite_title, "version": DATA_VERSION, "publication_date": DATA_VERSION, "language": "eng",
    "access_right": "open", "license": "cc-by-4.0",
    "creators": [{"name": f"{_family}, {_given}", "affiliation": "Katonic"}],
    "contributors": [{"name": PUBLISHER_ENTITY, "type": "HostingInstitution"}],
    "description": "<p>" + "</p><p>".join(esc(t) for t in (PROJECT_DESCRIPTION, CAVEAT, FUNDING, LICENCE_TEXT +
                   " The archive deposited from GitHub holds the site source and code (Apache 2.0) together with the data (CC BY 4.0).")) + "</p>",
    "keywords": _keywords,
    "related_identifiers": [
        {"identifier": SITE + "/", "relation": "isDocumentedBy", "resource_type": "other"},
        {"identifier": f"{SITE}/api/v1/releases/{DATA_VERSION}/", "relation": "isVariantFormOf", "resource_type": "dataset"},
        {"identifier": SRC_MLE["data_url"], "relation": "isDerivedFrom", "resource_type": "dataset"},
        {"identifier": SRC_EMBER["url"], "relation": "isDerivedFrom", "resource_type": "dataset"},
        {"identifier": SRC_MLE["cite_url"], "relation": "cites", "resource_type": "publication-preprint"},
        # T6: the Wikidata item for the project, so the archive and the knowledge graph point at each other.
        *([{"identifier": WIKIDATA_URL, "relation": "isIdenticalTo", "resource_type": "other"}] if WIKIDATA_URL else []),
    ],
    "notes": ATTRIBUTION,
}
(ROOT / ".zenodo.json").write_text(jdump(_zenodo), encoding="utf-8", newline="\n")

wheel = ROOT / "dist" / WHEEL_NAME
print(f"wrote {len(outputs)} pages/files, {len(outputs_bin)} social cards and {len(api_docs)} API documents; {len(index_rows)} index rows from {len(cfgs)} configurations; "
      f"{grid_count} grids; {len(posts)} posts; reference {ref['model']} {ref['num_gpus']}x{ref['gpu']} = {ref_wh:.1f} Wh/M")
if not CARDS_OK:
    print("NOTE: Pillow or build/fonts is missing, so no social card was redrawn; pages keep the cards already in assets/cards (or the default card). "
          "Install Pillow (python -m pip install pillow) to regenerate them.")
if not wheel.exists():
    print(f"NOTE: {wheel.relative_to(ROOT)} is missing; the MCP page's install line points at it. "
          f"Build it with: python -m pip wheel ./leadgreen-mcp -w dist --no-deps")
