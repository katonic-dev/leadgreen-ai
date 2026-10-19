---
license: cc-by-4.0
pretty_name: "Lead Green Green Tokens index: GPU energy per million output tokens"
language:
  - en
tags:
  - energy
  - llm-inference
  - gpu
  - sustainability
  - carbon
  - watt-hours-per-token
  - benchmark-derived
size_categories:
  - n<1K
task_categories:
  - tabular-regression
configs:
  - config_name: index
    data_files: "api/v1/index.csv"
---

# Lead Green Green Tokens index

**Draft dataset card. Not uploaded. Owner `[G6-OWNER]`, description `[G1]` once approved; the sentences below are the site's own.**

Lead Green is a public index of the GPU watt-hours it takes to serve a million output tokens, by model, GPU and configuration, with the grid carbon to price it anywhere. Every figure is from a named public measurement or a manufacturer's specification, dated and linked. The data is open under CC BY 4.0, there is a JSON API and an MCP server, and it is a Katonic project.

This dataset is the `api/v1` release `[RELEASE-DATE]` of https://leadgreen.ai, exactly as served, so that a row cited from here matches the row on the site and in `https://leadgreen.ai/api/v1/releases/[RELEASE-DATE]/`. A release listed as published never changes; cite the release, not the live files.

## What is in it

| File | Rows | What |
|---|---|---|
| `api/v1/index.csv`, `api/v1/index.json` | 32 | One row per model and GPU: the lowest-energy configuration measured at or under a 500 ms median inter-token latency. Watt-hours per million output tokens, cards, running batch, measured GPU power, output tokens per second, latency |
| `api/v1/models/<slug>.json` | 18 files, 328 configurations | Every measured configuration per model, with the index row per GPU |
| `api/v1/grid.json` | 193 countries plus World | Grid carbon intensity, gCO2e per kWh, lifecycle, location-based, by year (Ember) |
| `api/v1/hardware.json` | 4 GPUs, 1 system | Maximum TDP, memory, MIG profiles and whole-system power ceilings (NVIDIA specifications) |
| `api/v1/per-query.json` | 22 | AI Energy Score text-generation rows, Wh per 1,000 queries at batch size 1 (not converted to Wh per million tokens, and the card says why) |
| `api/v1/measurements.json` | 0 | Contributed measurements under the project's protocol; none yet |
| `api/v1/manifest.json`, `changes.json`, `openapi.json`, `schema/measurement.schema.json`, `types.d.ts` | | The manifest, the change record, the OpenAPI description, the measurement schema and the TypeScript types |

## Unit and boundary

Watt-hours per million output tokens (Wh/M). One Wh/M is 0.0036 joules per output token. **GPU energy only, measured at steady state on a busy server, at the most energy-efficient configuration measured: every row is a floor.** Host, network, cooling, idle time between requests and embodied carbon are outside the boundary. The same model on the same two H100 cards moves 7.1× in energy per token between a running batch of 8 and 256 (452 to 63.5 Wh/M for Qwen 3 32B); a real deployment sits above its floor. Running batch is the average number of requests the server was decoding at once (vLLM `num_requests_running`), not the configured cap.

Carbon: Wh/M × gCO2e per kWh ÷ 1,000 = kg CO2e per billion output tokens. Grid figures are lifecycle, location-based annual averages for comparing places, not Scope 2 factors to file as reported.

## Sources

- ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), Text Conversation task, data compiled 16 February 2026, retrieved 26 September 2026; Apache 2.0 per the `ml-energy/benchmark-v3` dataset card. Cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371. The leaderboard's measurements are reproduced as published; the index selects rows, converts units and states the rule.
- Ember, Yearly electricity data, October 2026 release (CC BY 4.0): emissions intensity of total generation.
- NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025): manufacturer figures transcribed as facts.
- AI Energy Score leaderboard, December 2025 round (Apache 2.0 as tagged on the Space; results reproduced as facts with attribution).

Full ledger with versions, licences and retrieval dates: https://leadgreen.ai/index/#sources and `api/v1/manifest.json`.

## Licence

Compilation and text: CC BY 4.0. Third-party figures keep their sources' licences, named above. Offered as-is and without warranty; state whether you changed any rows or columns.

## Cite

Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release `[RELEASE-DATE]`. Underlying data: ML.ENERGY Leaderboard v3.0 (Chung et al., NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data; AI Energy Score; NVIDIA. DOI: `[ZENODO-DOI once T3 is done]`.

## Who runs it and who pays

Lead Green is run and paid for by Katonic, which sells a sovereign AI platform and benefits when buyers ask the questions the index answers. It takes no money from hardware, cloud or model vendors. Publisher: Katonic AI Technology Ltd, Dubai International Financial Centre. Editor: Prem Naraindas. Reviewer with no Katonic affiliation: `[G4-REVIEWER]`. Corrections: hello@leadgreen.ai, answered within ten working days.

## Tools

- JSON API: https://leadgreen.ai/api/v1/ (CORS open, no key).
- MCP server: `pip install leadgreen-mcp` once on PyPI; today `pip install https://leadgreen.ai/dist/leadgreen_mcp-0.2.0-py3-none-any.whl`. Tools: `list_models`, `energy_per_million_tokens`, `estimate`, `compare_gpus`, `concurrency_curve`, `grid_intensity`, `gpu_hardware`, `sources`.
- Every page of the site has a Markdown copy at its URL followed by `index.md`; `https://leadgreen.ai/llms.txt` lists them.
