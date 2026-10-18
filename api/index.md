# Every table, as JSON

> The Green Tokens index as read-only JSON: index rows, per-model configurations, grid carbon, GPU hardware and per-query scores. CORS open, CC BY 4.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/api/ (this file: https://leadgreen.ai/api/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Data API*

The index is published as static JSON files under `/api/v1/`. No key, no tracking, no rate limit beyond what a static host imposes. Fetch them from a browser, a spreadsheet, a notebook or a build pipeline. Version 1 only ever adds fields; it never renames or removes them.

**Base URL** https://leadgreen.ai/api/v1/ · **Updated** 18 October 2026 · **Licence** CC BY 4.0 for the compilation; sources keep theirs

Cite this page: Lead Green, a Katonic project. Data API. https://leadgreen.ai/api/, release 2026-10-18, retrieved [date]. CC BY 4.0.

*Endpoints*

## 15 files  GET`/api/v1/manifest.json`
Sources, versions, retrieval dates, licences and this endpoint list. GET`/api/v1/index.json`
The index: 32 rows, one per model and GPU, energy-optimal under the latency limit, sorted ascending. GET`/api/v1/models.json`
Every model on the index with its slug, Hugging Face id, parameter counts and measured GPUs. GET`/api/v1/models/{slug}.json`
One model: every measured configuration (concurrency, parallelism, latency, power) and the best row per GPU. GET`/api/v1/grid.json`
Grid emissions intensity, gCO2e per kWh, 2024 annual average, 193 countries plus World. GET`/api/v1/hardware.json`
Manufacturer power ceilings, memory, MIG slice profiles and one embodied-carbon figure. GET`/api/v1/per-query.json`
AI Energy Score text-generation rows, December 2025 round: Wh per 1,000 queries at batch size 1 on H100 80GB GPUs (one card for classes A and B, several for C). GET`/api/v1/openapi.json`
OpenAPI 3.1 description of these endpoints. GET`/api/v1/measurements.json`
Contributed measurements accepted under the protocol, with contributor, affiliation, date, versions and MIG profile; never merged into index.json. GET`/api/v1/schema/measurement.schema.json`
JSON Schema for a contributed measurement file (protocol v0.2); the build validates every submission against it. GET`/api/v1/changes.json`
Every change to the published data or its description: date, summary, documents, reason and source version. GET`/api/v1/index.csv`
The index rows as CSV, for a spreadsheet. GET`/api/v1/types.d.ts`
TypeScript types for every document, generated from the documents. GET`/api/v1/all.zip`
Every JSON document of the current release in one zip (the same bytes as the dated release zip). GET`/api/v1/releases/index.json`
Every dated release of api/v1, each kept unchanged at releases/<date>/ with a zip of the whole release, for citation.

Model slugs are lower-case with hyphens: `deepseek-v3-1`, `gemma-3-12b`, `gemma-3-27b`, `llama-3-1-405b-instruct`, `llama-3-1-405b-instruct-fp8`, `llama-3-1-70b-instruct`, `llama-3-1-8b-instruct`, `llama-3-3-70b-instruct`, `llama-4-maverick-17b-128e-instruct-fp8`, `llama-4-scout-17b-16e-instruct`, `nvidia-nemotron-nano-12b-v2`, `nvidia-nemotron-nano-9b-v2`, `qwen-3-14b`, `qwen-3-235b-a22b-instruct`, `qwen-3-235b-a22b-instruct-fp8`, `qwen-3-30b-a3b-instruct`, `qwen-3-32b`, `qwen-3-8b`. The list, with Hugging Face ids, is in `models.json`.

*Example*

## Fetch the index and price it on your grid

Two requests, one multiplication. Energy per million tokens times the grid's grams per kWh, divided by 1,000, is kilograms of CO2e per billion tokens.

```
curl -s https://leadgreen.ai/api/v1/index.json | jq '.rows[] | select(.slug == "qwen-3-32b")'
curl -s https://leadgreen.ai/api/v1/grid.json  | jq '.areas[] | select(.iso3 == "SRB")'
```

The first returns the reference model's rows (one per GPU); the second returns Serbia at 668 gCO2e per kWh. 63.5 × 668 ÷ 1,000 = 42.4 kg CO2e per billion output tokens on the H100 row.

### index.json, trimmed

```
{
  "version": "1",
  "updated": "2026-10-18",
  "data_version": "2026-10-18",
  "unit": "Wh per million output tokens",
  "workload": "text-conversation",
  "itl_deadline_ms": 500,
  "selection": "per model and GPU, the configuration with the lowest energy per token whose median inter-token latency does not exceed itl_deadline_ms (the leaderboard's default ceiling; no measured configuration reaches it)",
  "reference_row": {
    "model": "Qwen 3 32B",
    "gpu": "H100",
    "num_gpus": 2
  },
  "boundary": "gpu_only",
  "source": {
    "name": "ML.ENERGY Leaderboard",
    "version": "3.0 (released 2025-12-01); data compiled 2026-02-16",
    "url": "https://ml.energy/leaderboard/",
    "...": "..."
  },
  "rows": [
    {
      "model": "Llama 3.1 8B Instruct",
      "slug": "llama-3-1-8b-instruct",
      "model_id": "meta-llama/Llama-3.1-8B-Instruct",
      "params_b": 8.0,
      "active_params_b": 8.0,
      "precision": "BF16",
      "gpu": "B200",
      "num_gpus": 1,
      "wh_per_million_output_tokens": 12.97,
      "joules_per_output_token": 0.0466958,
      "median_itl_ms": 124.9,
      "avg_requests_in_flight": 2042.9,
      "gpu_power_watts_total": 691,
      "avg_output_tokens": 396,
      "avg_running_batch": 2042.9,
      "max_num_seqs": 2048,
      "row_id": "llama-3-1-8b-instruct/B200/1/2048"
    },
    {
      "model": "Qwen 3 8B",
      "slug": "qwen-3-8b",
      "model_id": "Qwen/Qwen3-8B",
      "params_b": 8.0,
      "active_params_b": 8.0,
      "precision": "BF16",
      "gpu": "B200",
      "num_gpus": 1,
      "wh_per_million_output_tokens": 14.74,
      "joules_per_output_token": 0.0530581,
      "median_itl_ms": 91.2,
      "avg_requests_in_flight": 1426.7,
      "gpu_power_watts_total": 801,
      "avg_output_tokens": 649,
      "avg_running_batch": 1426.7,
      "max_num_seqs": 1536,
      "row_id": "qwen-3-8b/B200/1/1536"
    },
    "... 30 more rows"
  ]
}
```

### models/qwen-3-32b.json, trimmed

```
{
  "slug": "qwen-3-32b",
  "name": "Qwen 3 32B",
  "model_id": "Qwen/Qwen3-32B",
  "params_b": 32.0,
  "gpus": [
    "B200",
    "H100"
  ],
  "configurations": [
    {
      "gpu": "B200",
      "num_gpus": 1,
      "tensor_parallel": 1,
      "data_parallel": 1,
      "expert_parallel": 1,
      "precision": "BF16",
      "max_num_seqs": 8,
      "avg_requests_in_flight": 8.0,
      "wh_per_million_output_tokens": 429.18,
      "joules_per_output_token": 1.5450541,
      "median_itl_ms": 14.1,
      "p90_itl_ms": 15.7,
      "p99_itl_ms": 27.1,
      "tokens_per_second": 556.4,
      "gpu_power_watts_total": 860,
      "avg_output_tokens": 646,
      "under_itl_deadline": true,
      "avg_running_batch": 8.0,
      "p95_itl_ms": 17.3,
      "row_id": "qwen-3-32b/B200/1/8",
      "repeat": 1
    },
    "... 21 more configurations"
  ],
  "best": {
    "B200": {
      "num_gpus": 1,
      "wh_per_million_output_tokens": 39.05,
      "...": "..."
    },
    "H100": {
      "num_gpus": 2,
      "wh_per_million_output_tokens": 63.47,
      "...": "..."
    }
  }
}
```

### grid.json, trimmed

```
{
  "year": "2024",
  "unit": "gCO2e per kWh",
  "world": 473.0,
  "areas": [
    {
      "iso3": "NOR",
      "name": "Norway",
      "area_type": "country",
      "continent": "Europe",
      "g_co2e_per_kwh": 29.6,
      "display_name": "Norway",
      "iso2": "NO",
      "years": {
        "2023": 30.4,
        "2024": 29.6,
        "2025": 28.1
      },
      "latest_year": "2025"
    },
    {
      "iso3": "SRB",
      "name": "Serbia",
      "area_type": "country",
      "continent": "Europe",
      "g_co2e_per_kwh": 668.4,
      "display_name": "Serbia",
      "iso2": "RS",
      "years": {
        "2023": 638.9,
        "2024": 668.4,
        "2025": 699.1
      },
      "latest_year": "2025"
    },
    "... 192 more areas"
  ]
}
```

The examples above are generated from the live files at build time, so they match what the endpoints return.

*From a browser*

## CORS is open

Every file under `/api/v1/` is sent with `access-control-allow-origin: *`, and a preflight `OPTIONS` request gets 204, so a page on any origin can fetch them directly.

```
const r = await fetch("https://leadgreen.ai/api/v1/index.json");
const { rows } = await r.json();
const best = rows[0];   // sorted ascending by Wh per million output tokens
console.log(best.model, best.gpu, best.wh_per_million_output_tokens);
```

### Python

```
import json, urllib.request

BASE = "https://leadgreen.ai/api/v1/"
index = json.load(urllib.request.urlopen(BASE + "index.json"))
grid = {a["iso3"]: a for a in json.load(urllib.request.urlopen(BASE + "grid.json"))["areas"]}

row = next(r for r in index["rows"] if r["slug"] == "qwen-3-32b" and r["gpu"] == "H100")
kg = row["wh_per_million_output_tokens"] * grid["SRB"]["g_co2e_per_kwh"] / 1000
print(row["model"], row["num_gpus"], "x", row["gpu"], round(kg, 1), "kg CO2e per billion output tokens in Serbia")
print(index["caveat"])
```

A spreadsheet can open [`index.csv`](https://leadgreen.ai/api/v1/index.csv) directly. [`all.zip`](https://leadgreen.ai/api/v1/all.zip) holds every document of the current release.

*Fields*

## What the columns mean

One table for the fields every document carries, then one per document. The build refuses to publish a field that has no description here, and [`openapi.json`](https://leadgreen.ai/api/v1/openapi.json) and [`types.d.ts`](https://leadgreen.ai/api/v1/types.d.ts) are generated from the same documents, so the three cannot drift apart. `joules_per_output_token` is published to seven decimals, so `wh_per_million_output_tokens` = joules × 1,000,000 ÷ 3,600 holds exactly on every row.

*Fields on every document*

| Field | Meaning |
|---|---|
| version | API major version; it changes only for a breaking change, which would ship at /api/v2/ with v1 left in place. |
| updated | Date the document was built. |
| data_version | Changes whenever a value in the document changes. Cite it with the release archive. |
| unit | Unit of the main figure in the document. |
| caveat | Carried on every document with energy figures. Please carry it into whatever you build. |
| boundary | gpu_only: GPU energy and nothing else; host, network, storage, cooling and idle time are outside it. |
| itl_deadline_ms | The median inter-token latency ceiling used to pick best rows: 500 ms, the leaderboard's default. |
| source | The source object: name, publisher, url, data_url, version, retrieval date, licence with its evidence, method, selection and citation. |
| note | How to read the document. |
| licence | Licence of the document or of its source, as stated. |

**`index.json`, 24 fields**

| Field | Meaning |
|---|---|
| workload | The benchmark task behind the rows. |
| selection | The rule that picks each row, in words. |
| reference_row | The row the carbon table and worked examples are priced on. |
| reference_row.model | Its model. |
| reference_row.gpu | Its GPU. |
| reference_row.num_gpus | Its card count. |
| rows | One row per model and GPU, sorted ascending by Wh/M. |
| rows[].model | Display name. |
| rows[].slug | Key for models/<slug>.json. |
| rows[].model_id | Hugging Face id. |
| rows[].params_b | Total parameters, billions. |
| rows[].active_params_b | Parameters active per token, billions (they differ for mixture-of-experts models). |
| rows[].precision | Weight precision (BF16, FP8, MXFP4). |
| rows[].gpu | GPU model: H100 (H100 80GB HBM3) or B200. |
| rows[].num_gpus | Cards in the configuration. |
| rows[].wh_per_million_output_tokens | GPU energy per million output tokens, watt-hours: joules_per_output_token x 1,000,000 / 3,600, which holds exactly on every row. |
| rows[].joules_per_output_token | The source's figure, seven decimals: steady-state GPU energy divided by the output tokens generated in that window (steady_state_energy_per_token). Prompt processing is included. |
| rows[].median_itl_ms | Median inter-token latency, milliseconds. |
| rows[].avg_requests_in_flight | The same value as avg_running_batch under its first name, kept in v1 and removed at v2. It is the running batch, not client-side requests outstanding. |
| rows[].gpu_power_watts_total | Average power drawn, summed across every card. |
| rows[].avg_output_tokens | Average output length per response, tokens. |
| rows[].avg_running_batch | The average number of requests the server was decoding at once over the steady-state window (vLLM num_requests_running). Queued requests are not counted. |
| rows[].max_num_seqs | The configured cap on sequences decoded at once (vLLM max_num_seqs). |
| rows[].row_id | Stable identifier, <slug>/<gpu>/<num_gpus>/<max_num_seqs>, with /r2 on a repeated run. It survives re-sorting and new rows. |

**`models.json`, 9 fields**

| Field | Meaning |
|---|---|
| models | Every model on the index. |
| models[].slug | Model key. |
| models[].name | Display name. |
| models[].model_id | Hugging Face id. |
| models[].params_b | Total parameters, billions. |
| models[].active_params_b | Parameters active per token, billions. |
| models[].gpus | GPUs measured. |
| models[].url | URL of models/<slug>.json. |
| models[].page | URL of the model's page on the site. |

**`models/{slug}.json`, 52 fields**

| Field | Meaning |
|---|---|
| slug | Model key. |
| name | Display name. |
| model_id | Hugging Face id. |
| params_b | Total parameters, billions. |
| active_params_b | Parameters active per token, billions. |
| architecture | The source's label: Dense Transformer, MoE or Mamba-Transformer Hybrid. |
| gpus | GPUs the model was measured on. |
| configurations | Every stable configuration the source measured for this model. |
| configurations[].gpu | GPU model: H100 (H100 80GB HBM3) or B200. |
| configurations[].num_gpus | Cards in the configuration. |
| configurations[].tensor_parallel | Tensor-parallel degree. |
| configurations[].data_parallel | Data-parallel degree. |
| configurations[].expert_parallel | Expert-parallel degree (mixture-of-experts models). |
| configurations[].precision | Weight precision (BF16, FP8, MXFP4). |
| configurations[].max_num_seqs | The configured cap on sequences decoded at once (vLLM max_num_seqs). |
| configurations[].avg_requests_in_flight | The same value as avg_running_batch under its first name, kept in v1 and removed at v2. It is the running batch, not client-side requests outstanding. |
| configurations[].wh_per_million_output_tokens | GPU energy per million output tokens, watt-hours: joules_per_output_token x 1,000,000 / 3,600, which holds exactly on every row. |
| configurations[].joules_per_output_token | The source's figure, seven decimals: steady-state GPU energy divided by the output tokens generated in that window (steady_state_energy_per_token). Prompt processing is included. |
| configurations[].median_itl_ms | Median inter-token latency, milliseconds. |
| configurations[].p90_itl_ms | 90th percentile inter-token latency, milliseconds. |
| configurations[].p99_itl_ms | 99th percentile inter-token latency, milliseconds. |
| configurations[].tokens_per_second | Output throughput of the whole configuration. |
| configurations[].gpu_power_watts_total | Average power drawn, summed across every card. |
| configurations[].avg_output_tokens | Average output length per response, tokens. |
| configurations[].under_itl_deadline | Whether median_itl_ms is at or under itl_deadline_ms; every published configuration currently is. |
| configurations[].avg_running_batch | The average number of requests the server was decoding at once over the steady-state window (vLLM num_requests_running). Queued requests are not counted. |
| configurations[].p95_itl_ms | 95th percentile inter-token latency, milliseconds. |
| configurations[].row_id | Stable identifier, <slug>/<gpu>/<num_gpus>/<max_num_seqs>, with /r2 on a repeated run. It survives re-sorting and new rows. |
| configurations[].repeat | 1 for the first run of a configuration, 2 for the source's repeat of it (two Qwen 3 30B A3B configurations were run twice). |
| best | The index row per GPU, keyed by GPU; each value has the configuration fields. |
| best.<key> | The configuration the index row uses for that GPU. |
| best.<key>.gpu | GPU model: H100 (H100 80GB HBM3) or B200. |
| best.<key>.num_gpus | Cards in the configuration. |
| best.<key>.tensor_parallel | Tensor-parallel degree. |
| best.<key>.data_parallel | Data-parallel degree. |
| best.<key>.expert_parallel | Expert-parallel degree (mixture-of-experts models). |
| best.<key>.precision | Weight precision (BF16, FP8, MXFP4). |
| best.<key>.max_num_seqs | The configured cap on sequences decoded at once (vLLM max_num_seqs). |
| best.<key>.avg_requests_in_flight | The same value as avg_running_batch under its first name, kept in v1 and removed at v2. It is the running batch, not client-side requests outstanding. |
| best.<key>.wh_per_million_output_tokens | GPU energy per million output tokens, watt-hours: joules_per_output_token x 1,000,000 / 3,600, which holds exactly on every row. |
| best.<key>.joules_per_output_token | The source's figure, seven decimals: steady-state GPU energy divided by the output tokens generated in that window (steady_state_energy_per_token). Prompt processing is included. |
| best.<key>.median_itl_ms | Median inter-token latency, milliseconds. |
| best.<key>.p90_itl_ms | 90th percentile inter-token latency, milliseconds. |
| best.<key>.p99_itl_ms | 99th percentile inter-token latency, milliseconds. |
| best.<key>.tokens_per_second | Output throughput of the whole configuration. |
| best.<key>.gpu_power_watts_total | Average power drawn, summed across every card. |
| best.<key>.avg_output_tokens | Average output length per response, tokens. |
| best.<key>.under_itl_deadline | Whether median_itl_ms is at or under itl_deadline_ms; every published configuration currently is. |
| best.<key>.avg_running_batch | The average number of requests the server was decoding at once over the steady-state window (vLLM num_requests_running). Queued requests are not counted. |
| best.<key>.p95_itl_ms | 95th percentile inter-token latency, milliseconds. |
| best.<key>.row_id | Stable identifier, <slug>/<gpu>/<num_gpus>/<max_num_seqs>, with /r2 on a repeated run. It survives re-sorting and new rows. |
| best.<key>.repeat | 1 for the first run of a configuration, 2 for the source's repeat of it (two Qwen 3 30B A3B configurations were run twice). |

**`grid.json`, 14 fields**

| Field | Meaning |
|---|---|
| year | The year g_co2e_per_kwh is taken from (2024, the latest with every listed grid). |
| basis | What the figure is: lifecycle, location-based, production-based. |
| world | The World figure for year. |
| areas | Every area Ember covers, plus the World row (iso3 WLD, area_type world); filter on area_type == country. |
| areas[].iso3 | ISO 3166-1 alpha-3 code (WLD for World). |
| areas[].name | Ember's label. |
| areas[].area_type | country or world. |
| areas[].g_co2e_per_kwh | Emissions intensity, gCO2e per kWh, for year (2024); kept for compatibility. |
| areas[].display_name | The shorter name the site shows. |
| areas[].iso2 | ISO 3166-1 alpha-2 code; null for World and for Kosovo, which has none. |
| areas[].years | Every year Ember holds for the area from 2023, keyed by year. |
| areas[].years.<key> | gCO2e per kWh in that year. |
| areas[].latest_year | The newest year in years. |
| areas[].continent | Ember's continent label. |

**`hardware.json`, 26 fields**

| Field | Meaning |
|---|---|
| retrieved | When the specifications were read. |
| tdp | Maximum thermal design power per GPU. |
| tdp[].gpu | GPU. |
| tdp[].form | Form factor. |
| tdp[].max_tdp_w | Maximum TDP, watts. |
| tdp[].tdp_label | TDP as NVIDIA words it. |
| tdp[].memory | Memory. |
| tdp[].source | Where the figure is from. |
| systems | System power ratings. |
| systems[].system | System. |
| systems[].gpus | GPUs in the system. |
| systems[].max_power_kw | Maximum system power, kW. |
| systems[].label | The rating as published. |
| systems[].source | Where it is from. |
| mig_profiles | Multi-Instance GPU profiles per card (the media-extension variants are omitted). |
| mig_profiles[].gpu | Card. |
| mig_profiles[].profile | Profile name. |
| mig_profiles[].memory_fraction | Share of the card's memory. |
| mig_profiles[].sm_fraction | Share of the card's streaming multiprocessors. |
| mig_profiles[].instances | How many fit on one card. |
| embodied | One embodied-carbon figure. |
| embodied.item | What it covers. |
| embodied.kg_co2e_cradle_to_gate | kg CO2e, cradle to gate, baseboard only. |
| embodied.source | Source. |
| embodied.published | Publication date. |
| sources | The NVIDIA documents, with their terms. |

**`per-query.json`, 12 fields**

| Field | Meaning |
|---|---|
| round | The AI Energy Score round. |
| setup | How a query is run. |
| classes | Hardware classes. |
| classes.<key> | What the class means. |
| score | What the stars mean. |
| rows | Every row of the round. |
| rows[].model | Clean Hugging Face id. |
| rows[].class | Hardware class. |
| rows[].wh_per_1000_queries | GPU watt-hours for 1,000 queries. |
| rows[].score | Stars, 1 to 5, within the class. |
| rows[].source_label | The model string exactly as the source gives it. |
| rows[].note | A note on the row, where there is one. |

**`manifest.json`, 22 fields**

| Field | Meaning |
|---|---|
| site | Site URL. |
| name | API name. |
| description | What the API is. |
| endpoints | Every endpoint. |
| endpoints[].path | Path under /api/v1/. |
| endpoints[].url | Full URL. |
| endpoints[].description | What it returns. |
| sources | Every source with version, retrieval date, licence and evidence. |
| publisher | Who publishes the API. |
| publisher.name | Project. |
| publisher.parent | Parent. |
| publisher.url | Site. |
| publisher.entity | Legal entity. |
| publisher.registration | Registration number. |
| publisher.jurisdiction | Jurisdiction. |
| publisher.address | Registered office; null until confirmed. |
| publisher.contact | Corrections and contributions mailbox. |
| publisher.response_working_days | Response time, working days. |
| attribution | A ready CC BY 4.0 credit line. |
| releases | Where dated releases are kept. |
| releases.index | The list of releases. |
| releases.pattern | URL pattern of a release. |

**`measurements.json`, 3 fields**

| Field | Meaning |
|---|---|
| protocol_version | Protocol version the rows follow. |
| schema | URL of the measurement schema. |
| rows | Contributed rows: the measurement schema's fields plus source_file and comparable (median ITL at or under itl_deadline_ms). |

**`changes.json`, 6 fields**

| Field | Meaning |
|---|---|
| changes | One entry per change, oldest first. |
| changes[].date | Date of the change. |
| changes[].summary | What changed. |
| changes[].documents | Documents affected (* for all). |
| changes[].reason | Why. |
| changes[].source_version | Source version at the time. |

*Versioning and licence*

## Additive only

**Caching and limits.** The files are served by GitHub Pages, which sends `Cache-Control: max-age=600`, an ETag and Last-Modified. Poll with `If-None-Match`, no more than hourly, and mirror the files rather than fetching them for each of your users: the host has a soft bandwidth limit of 100 GB a month and does not allow software-as-a-service use. There is no uptime promise. The data is refreshed when a source publishes a new release, checked monthly; the date is in every document and in [`changes.json`](https://leadgreen.ai/api/v1/changes.json).

**Version 1.** Fields are added, never renamed or removed. A new source or a re-measurement changes values, `data_version` and the `updated` date, and the change is recorded in [`changes.json`](https://leadgreen.ai/api/v1/changes.json) and on [the index's change list](https://leadgreen.ai/index/#changes). `row_id` identifies a row across releases. A breaking change would ship as `/api/v2/` with v1 left in place.

**Licence.** The compilation, the derived figures and the site text are offered under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/): use them, credit Lead Green and the underlying source. Each source keeps its own licence, stated per source in `manifest.json` with the evidence. ML.ENERGY: The leaderboard repository the JSON comes from carries no licence file; the benchmark data is published under Apache 2.0 on the dataset card and in the NeurIPS 2025 paper, and the JSON is reproduced here as published measurements on that basis while the ML.ENERGY team is asked to confirm that the licence covers it. Ember's data is CC BY 4.0. AI Energy Score: Apache-2.0 as tagged on the Hugging Face Space; the project states no separate licence for the results file, which is reproduced as facts with attribution. NVIDIA's figures are reproduced as facts with attribution; NVIDIA grants no licence and none is claimed. The Apache License 2.0 text is in [`LICENSE`](https://leadgreen.ai/LICENSE), and `build/data/NOTICE.md` records each snapshot's source, retrieval date and terms.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

**Attribution.** If you republish the data, this line covers the CC BY 4.0 credit (it is also the `attribution` field in `manifest.json`): Green Tokens index, Lead Green, a Katonic project, https://leadgreen.ai/api/v1/, CC BY 4.0. Contains data from the ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; data compiled 2026-02-16, retrieved 2026-09-26) and Ember Yearly Electricity Data (CC BY 4.0). Changes: [none | describe].

**Releases.** Every dated release is kept unchanged at `https://leadgreen.ai/api/v1/releases/<date>/` with a zip of the whole release; [`releases/index.json`](https://leadgreen.ai/api/v1/releases/index.json) lists them with each zip's SHA-256. Cite a release, not the live files.

**OpenAPI.** A machine-readable description is at [`openapi.json`](https://leadgreen.ai/api/v1/openapi.json). The [MCP server](https://leadgreen.ai/mcp/) is built on these same files.
