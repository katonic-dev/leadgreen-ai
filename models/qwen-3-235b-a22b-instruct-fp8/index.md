# Qwen 3 235B A22B Instruct FP8: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 235B A22B Instruct FP8: 23 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/ (this file: https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 235B A22B Instruct FP8 serves a million output tokens for **139.1 Wh/M** on 2 × B200 (running batch 256, median inter-token latency 64 ms) and **206.0 Wh/M** on 8 × H100 (running batch 511, median inter-token latency 76 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-235B-A22B-Instruct-2507-FP8](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8), a mixture-of-experts model (22 B of 235 B parameters active per token), weights in FP8. **Measured** 23 configurations on B200 and H100. **Data** [models/qwen-3-235b-a22b-instruct-fp8.json](https://leadgreen.ai/api/v1/models/qwen-3-235b-a22b-instruct-fp8.json). Updated 17 October 2026.

- [Every configuration](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#carbon)
- [Questions](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#sources)

- **Index row, B200:** 139.1 Wh/M 2 × B200, FP8. Running batch 256, median ITL 64 ms, 1,891 W across the cards, 3,776 tokens a second.
- **Index row, H100:** 206.0 Wh/M 8 × H100, FP8. Running batch 511, median ITL 76 ms, 3,961 W across the cards, 5,342 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 235B A22B Instruct FP8 at every measured load

On 8 × H100, Qwen 3 235B A22B Instruct FP8 runs from **3,163.8 Wh/M** at a running batch of 8 to **206.0 Wh/M** at 511, a fall of 15.4×, while the cards' draw rises 10 percent (from 3,596 to 3,961 W) and throughput rises 16.9× (from 316 to 5,342 tokens a second). Median inter-token latency stays at 76 ms or under up to the best row.

*Qwen 3 235B A22B Instruct FP8, FP8, 2 × B200: six measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 2,339.2 | 37 | 214 | 1,806 |
| 16 | 16 | 1,297.2 | 40 | 389 | 1,818 |
| 32 | 32 | 729.8 | 43 | 721 | 1,895 |
| 64 | 64 | 408.9 | 48 | 1,285 | 1,892 |
| 128 | 128 | 228.3 | 54 | 2,255 | 1,853 |
| 256 | 256 | 139.1 | 64 | 3,776 | 1,891 |

*Qwen 3 235B A22B Instruct FP8, FP8, 4 × H100: seven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 2,630.9 | 35 | 224 | 2,120 |
| 16 | 16 | 1,459.2 | 37 | 421 | 2,210 |
| 32 | 32 | 835.9 | 43 | 732 | 2,202 |
| 64 | 64 | 483.7 | 49 | 1,262 | 2,198 |
| 96 | 96 | 352.2 | 53 | 1,752 | 2,222 |
| 128 | 128 | 305.8 | 53 | 2,295 | 2,526 |
| 192 | 192 | 233.4 | 60 | 3,016 | 2,534 |

*Qwen 3 235B A22B Instruct FP8, FP8, 8 × H100: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 3,163.8 | 25 | 316 | 3,596 |
| 16 | 16 | 1,749.2 | 27 | 578 | 3,638 |
| 32 | 32 | 1,012.3 | 30 | 1,017 | 3,706 |
| 64 | 64 | 587.8 | 35 | 1,761 | 3,725 |
| 96 | 96 | 451.9 | 39 | 2,347 | 3,817 |
| 128 | 128 | 378.9 | 42 | 2,840 | 3,874 |
| 192 | 192 | 306.7 | 50 | 3,609 | 3,985 |
| 256 | 256 | 264.0 | 55 | 4,322 | 4,107 |
| 384 | 383 | 229.4 | 67 | 5,023 | 4,149 |
| 512 | 511 | 206.0 | 76 | 5,342 | 3,961 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.48× the energy per token of the B200 configuration: 206.0 Wh/M on 8 × H100 against 139.1 Wh/M on 2 × B200. The two rows were not swept alike: the H100 row holds a running batch of 511 on 8 cards and the B200 row 256 on 2, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 235B A22B Instruct FP8 on 2 × B200 at its index row carries about 95.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.1 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 235B A22B Instruct FP8, 2 × B200 index row (139.1 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 98.3 |
| Saudi Arabia | 689 | 95.8 |
| Hong Kong | 676 | 94.0 |
| Serbia | 668 | 93.0 |
| World | 473 | 65.8 |
| Germany | 340 | 47.3 |
| Norway | 30 | 4.1 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Qwen 3 235B A22B Instruct FP8

### How much energy does Qwen 3 235B A22B Instruct FP8 use per million output tokens?

Qwen 3 235B A22B Instruct FP8 uses 139.1 Wh of GPU energy per million output tokens on 2 × B200 and 206.0 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 235B A22B Instruct FP8 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.48× the energy per token of the B200 configuration: 206.0 Wh/M on 8 × H100 against 139.1 Wh/M on 2 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 235B A22B Instruct FP8?

On 8 × H100, energy per token falls 15.4× between a running batch of 8 (3,163.8 Wh/M) and 511 (206.0 Wh/M), because the cards' power rises only 10 percent while throughput rises 16.9×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 235B A22B Instruct FP8?

A billion output tokens of Qwen 3 235B A22B Instruct FP8 on 2 × B200 at its index row carries about 95.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.1 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Qwen 3 235B A22B Instruct FP8 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 23 stable configurations of Qwen 3 235B A22B Instruct FP8 measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507-FP8).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-17, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-235b-a22b-instruct-fp8.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 235B A22B Instruct FP8 on your own grid and load.
