# Qwen 3 30B A3B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 30B A3B Instruct: 31 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/ (this file: https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 30B A3B Instruct serves a million output tokens for **15.7 Wh/M** on 1 × B200 (running batch 1,023, median inter-token latency 89 ms) and **24.7 Wh/M** on 2 × H100 (running batch 1,019, median inter-token latency 75 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-30B-A3B-Instruct-2507](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507), a mixture-of-experts model (3 B of 30 B parameters active per token), weights in BF16. **Measured** 31 configurations on B200 and H100. **Data** [models/qwen-3-30b-a3b-instruct.json](https://leadgreen.ai/api/v1/models/qwen-3-30b-a3b-instruct.json). Updated 17 October 2026.

- [Every configuration](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#sources)

- **Index row, B200:** 15.7 Wh/M 1 × B200, BF16. Running batch 1,023, median ITL 89 ms, 601 W across the cards, 10,648 tokens a second.
- **Index row, H100:** 24.7 Wh/M 2 × H100, BF16. Running batch 1,019, median ITL 75 ms, 1,123 W across the cards, 12,640 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 30B A3B Instruct at every measured load

On 2 × H100, Qwen 3 30B A3B Instruct runs from **228.6 Wh/M** at a running batch of 8 to **24.7 Wh/M** at 1,019, a fall of 9.3×, while the cards' draw rises 64 percent (from 684 to 1,123 W) and throughput rises 15.2× (from 831 to 12,640 tokens a second). Median inter-token latency stays at 75 ms or under up to the best row.

*Qwen 3 30B A3B Instruct, BF16, 1 × B200: twelve measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 200.5 | 8 | 910 | 657 |
| 16 | 16 | 148.7 | 11 | 1,232 | 659 |
| 32 | 32 | 106.3 | 14 | 1,941 | 743 |
| 64 | 64 | 69.2 | 19 | 2,907 | 725 |
| 96 | 96 | 52.1 | 19 | 4,400 | 825 |
| 128 | 128 | 43.6 | 21 | 5,277 | 829 |
| 192 | 192 | 32.3 | 24 | 7,212 | 838 |
| 256 | 256 | 28.5 | 26 | 8,872 | 910 |
| 512 | 511 | 22.1 | 38 | 8,840 | 703 |
| 768 | 767 | 18.9 | 87 | 8,028 | 547 |
| 1,024 | 1,023 | 15.7 | 89 | 10,648 | 601 |
| 1,536 | 1,478 | 15.8 | 123 | 10,649 | 606 |

*Qwen 3 30B A3B Instruct, BF16, 1 × H100: five measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 181.4 | 13 | 611 | 399 |
| 16 | 16 | 135.2 | 18 | 902 | 439 |
| 32 | 32 | 93.2 | 23 | 1,394 | 468 |
| 64 | 64 | 61.6 | 29 | 2,164 | 480 |
| 96 | 89 | 51.6 | 32 | 2,659 | 494 |

*Qwen 3 30B A3B Instruct, BF16, 2 × H100: 14 measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 228.6 | 9 | 831 | 684 |
| 16 | 16 | 168.4 | 13 | 1,253 | 759 |
| 32 | 32 | 114.2 | 15 | 2,026 | 833 |
| 64 | 64 | 75.5 | 19 | 3,290 | 895 |
| 96 | 96 | 65.0 | 25 | 3,814 | 892 |
| 128 | 128 | 55.0 | 27 | 4,546 | 900 |
| 192 | 192 | 43.2 | 31 | 5,975 | 930 |
| 256 | 256 | 37.1 | 35 | 7,154 | 955 |
| 256 | 256 | 40.8 | 34 | 7,437 | 1,093 |
| 384 | 384 | 31.1 | 43 | 8,388 | 939 |
| 512 | 511 | 27.4 | 47 | 9,650 | 953 |
| 512 | 511 | 32.6 | 50 | 9,366 | 1,101 |
| 768 | 767 | 28.2 | 65 | 10,670 | 1,082 |
| 1,024 | 1,019 | 24.7 | 75 | 12,640 | 1,123 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.58× the energy per token of the B200 configuration: 24.7 Wh/M on 2 × H100 against 15.7 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 1,019 on 2 cards and the B200 row 1,023 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 30B A3B Instruct on 1 × B200 at its index row carries about 10.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 30B A3B Instruct, 1 × B200 index row (15.7 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 11.1 |
| Saudi Arabia | 689 | 10.8 |
| Hong Kong | 676 | 10.6 |
| Serbia | 668 | 10.5 |
| World | 473 | 7.4 |
| Germany | 340 | 5.3 |
| Norway | 30 | 0.5 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Qwen 3 30B A3B Instruct

### How much energy does Qwen 3 30B A3B Instruct use per million output tokens?

Qwen 3 30B A3B Instruct uses 15.7 Wh of GPU energy per million output tokens on 1 × B200 and 24.7 Wh of GPU energy per million output tokens on 2 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 30B A3B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.58× the energy per token of the B200 configuration: 24.7 Wh/M on 2 × H100 against 15.7 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 30B A3B Instruct?

On 2 × H100, energy per token falls 9.3× between a running batch of 8 (228.6 Wh/M) and 1,019 (24.7 Wh/M), because the cards' power rises only 64 percent while throughput rises 15.2×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 30B A3B Instruct?

A billion output tokens of Qwen 3 30B A3B Instruct on 1 × B200 at its index row carries about 10.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Qwen 3 30B A3B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 31 stable configurations of Qwen 3 30B A3B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-30B-A3B-Instruct-2507).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-17, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-30b-a3b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 30B A3B Instruct on your own grid and load.
