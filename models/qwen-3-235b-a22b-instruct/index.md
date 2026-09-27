# Qwen 3 235B A22B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 235B A22B Instruct: 31 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/ (this file: https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 235B A22B Instruct serves a million output tokens for **66.7 Wh/M** on 4 × B200 (running batch 3,765, median inter-token latency 68 ms) and **303.5 Wh/M** on 8 × H100 (running batch 228, median inter-token latency 55 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-235B-A22B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507), a mixture-of-experts model (22 B of 235 B parameters active per token), weights in BF16. **Measured** 31 configurations on B200 and H100. **Data** [models/qwen-3-235b-a22b-instruct.json](https://leadgreen.ai/api/v1/models/qwen-3-235b-a22b-instruct.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#sources)

- **Index row, B200:** 66.7 Wh/M 4 × B200, BF16. Running batch 3,765, median ITL 68 ms, 3,196 W across the cards, 13,303 tokens a second.
- **Index row, H100:** 303.5 Wh/M 8 × H100, BF16. Running batch 228, median ITL 55 ms, 4,038 W across the cards, 3,696 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 235B A22B Instruct at every measured load

On 4 × B200, Qwen 3 235B A22B Instruct runs from **1,793.5 Wh/M** at a running batch of 8 to **66.7 Wh/M** at 3,765, a fall of 26.9×, while the cards' draw rises 25 percent (from 2,562 to 3,196 W) and throughput rises 33.5× (from 397 to 13,303 tokens a second). Median inter-token latency stays at 144 ms or under up to the best row.

*Qwen 3 235B A22B Instruct, BF16, 4 × B200: twelve measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,793.5 | 20 | 397 | 2,562 |
| 16 | 16 | 1,264.0 | 25 | 637 | 2,897 |
| 32 | 32 | 848.0 | 30 | 1,044 | 3,186 |
| 64 | 64 | 567.5 | 41 | 1,528 | 3,123 |
| 128 | 128 | 335.4 | 47 | 2,603 | 3,143 |
| 256 | 256 | 197.5 | 53 | 4,506 | 3,204 |
| 512 | 511 | 128.6 | 67 | 6,506 | 3,012 |
| 1,024 | 1,023 | 95.5 | 104 | 8,735 | 3,002 |
| 1,536 | 1,411 | 87.8 | 136 | 9,509 | 3,007 |
| 2,048 | 2,045 | 74.3 | 144 | 12,212 | 3,268 |
| 3,072 | 3,047 | 68.2 | 118 | 13,159 | 3,231 |
| 4,096 | 3,765 | 66.7 | 68 | 13,303 | 3,196 |

*Qwen 3 235B A22B Instruct, BF16, 8 × B200: eleven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 2,332.2 | 17 | 469 | 3,942 |
| 16 | 16 | 1,550.3 | 19 | 825 | 4,604 |
| 32 | 32 | 1,166.8 | 29 | 1,078 | 4,530 |
| 64 | 64 | 706.0 | 33 | 1,877 | 4,770 |
| 128 | 128 | 420.1 | 37 | 3,306 | 5,000 |
| 256 | 256 | 261.0 | 43 | 5,403 | 5,078 |
| 512 | 511 | 187.2 | 59 | 7,220 | 4,867 |
| 1,024 | 1,023 | 150.6 | 113 | 8,316 | 4,509 |
| 1,536 | 1,534 | 130.1 | 144 | 10,208 | 4,780 |
| 2,048 | 2,045 | 116.6 | 156 | 11,727 | 4,924 |
| 4,096 | 4,090 | 103.7 | 241 | 14,457 | 5,396 |

*Qwen 3 235B A22B Instruct, BF16, 8 × H100: eight measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 2,025.7 | 20 | 388 | 2,829 |
| 16 | 16 | 1,438.4 | 25 | 616 | 3,189 |
| 32 | 32 | 1,062.6 | 35 | 908 | 3,472 |
| 64 | 64 | 665.0 | 40 | 1,548 | 3,705 |
| 96 | 96 | 505.3 | 44 | 2,114 | 3,846 |
| 128 | 128 | 412.8 | 47 | 2,626 | 3,903 |
| 192 | 192 | 319.0 | 52 | 3,472 | 3,987 |
| 256 | 228 | 303.5 | 55 | 3,696 | 4,038 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 4.55× the energy per token of the B200 configuration: 303.5 Wh/M on 8 × H100 against 66.7 Wh/M on 4 × B200. The two rows were not swept alike: the H100 row holds a running batch of 228 on 8 cards and the B200 row 3,765 on 4, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 235B A22B Instruct on 4 × B200 at its index row carries about 46.2 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 2.0 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 235B A22B Instruct, 4 × B200 index row (66.7 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 47.2 |
| Saudi Arabia | 692 | 46.2 |
| Hong Kong | 676 | 45.1 |
| Serbia | 668 | 44.6 |
| World | 474 | 31.6 |
| Germany | 340 | 22.7 |
| Norway | 30 | 2.0 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Qwen 3 235B A22B Instruct

### How much energy does Qwen 3 235B A22B Instruct use per million output tokens?

Qwen 3 235B A22B Instruct uses 66.7 Wh of GPU energy per million output tokens on 4 × B200 and 303.5 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 235B A22B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 4.55× the energy per token of the B200 configuration: 303.5 Wh/M on 8 × H100 against 66.7 Wh/M on 4 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 235B A22B Instruct?

On 4 × B200, energy per token falls 26.9× between a running batch of 8 (1,793.5 Wh/M) and 3,765 (66.7 Wh/M), because the cards' power rises only 25 percent while throughput rises 33.5×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 235B A22B Instruct?

A billion output tokens of Qwen 3 235B A22B Instruct on 4 × B200 at its index row carries about 46.2 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 2.0 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Qwen 3 235B A22B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 31 stable configurations of Qwen 3 235B A22B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-235B-A22B-Instruct-2507).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-235b-a22b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 235B A22B Instruct on your own grid and load.
