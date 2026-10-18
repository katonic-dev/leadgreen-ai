# Llama 3.3 70B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Llama 3.3 70B Instruct: 19 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-3-3-70b-instruct/ (this file: https://leadgreen.ai/models/llama-3-3-70b-instruct/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Llama 3.3 70B Instruct serves a million output tokens for **60.7 Wh/M** on 2 × B200 (running batch 1,022, median inter-token latency 106 ms) and **117.5 Wh/M** on 4 × H100 (running batch 724, median inter-token latency 98 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [meta-llama/Llama-3.3-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct), a dense transformer, weights in BF16. **Measured** 19 configurations on B200 and H100. **Data** [models/llama-3-3-70b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-3-70b-instruct.json). Updated 18 October 2026.

- [Every configuration](https://leadgreen.ai/models/llama-3-3-70b-instruct/#configurations)
- [Two generations](https://leadgreen.ai/models/llama-3-3-70b-instruct/#generations)
- [Carbon](https://leadgreen.ai/models/llama-3-3-70b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/llama-3-3-70b-instruct/#sources)

- **Index row, B200:** 60.7 Wh/M 2 × B200, BF16. Running batch 1,022, median ITL 106 ms, 1,935 W across the cards, 8,854 tokens a second.
- **Index row, H100:** 117.5 Wh/M 4 × H100, BF16. Running batch 724, median ITL 98 ms, 2,546 W across the cards, 6,018 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 3.3 70B Instruct at every measured load

On 4 × H100, Llama 3.3 70B Instruct runs from **1,068.6 Wh/M** at a running batch of 8 to **117.5 Wh/M** at 724, a fall of 9.1×, while the cards' draw rises 42 percent (from 1,787 to 2,546 W) and throughput rises 13.0× (from 465 to 6,018 tokens a second). Median inter-token latency stays at 98 ms or under up to the best row.

*Llama 3.3 70B Instruct, BF16, 2 × B200: eight measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,004.7 | 17 | 470 | 1,701 |
| 16 | 16 | 533.7 | 17 | 908 | 1,746 |
| 32 | 32 | 305.1 | 19 | 1,600 | 1,758 |
| 64 | 64 | 189.9 | 22 | 2,655 | 1,815 |
| 128 | 128 | 133.6 | 28 | 3,973 | 1,912 |
| 256 | 256 | 97.8 | 37 | 5,515 | 1,942 |
| 512 | 511 | 75.7 | 64 | 7,079 | 1,930 |
| 1,024 | 1,022 | 60.7 | 106 | 8,854 | 1,935 |

*Llama 3.3 70B Instruct, BF16, 4 × H100: eleven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,068.6 | 17 | 465 | 1,787 |
| 16 | 16 | 583.8 | 18 | 875 | 1,839 |
| 32 | 32 | 347.0 | 20 | 1,518 | 1,896 |
| 64 | 64 | 228.4 | 22 | 2,564 | 2,108 |
| 96 | 96 | 186.3 | 25 | 3,315 | 2,224 |
| 128 | 128 | 167.7 | 28 | 3,895 | 2,351 |
| 192 | 192 | 150.0 | 34 | 4,558 | 2,461 |
| 256 | 255 | 136.4 | 39 | 5,130 | 2,519 |
| 384 | 383 | 123.3 | 54 | 5,658 | 2,511 |
| 512 | 511 | 118.1 | 74 | 5,858 | 2,491 |
| 768 | 724 | 117.5 | 98 | 6,018 | 2,546 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.94× the energy per token of the B200 configuration: 117.5 Wh/M on 4 × H100 against 60.7 Wh/M on 2 × B200. The two rows were not swept alike: the H100 row holds a running batch of 724 on 4 cards and the B200 row 1,022 on 2, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 3.3 70B Instruct on 2 × B200 at its index row carries about 41.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.8 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 3.3 70B Instruct, 2 × B200 index row (60.7 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 42.9 |
| Saudi Arabia | 689 | 41.8 |
| Hong Kong | 676 | 41.0 |
| Serbia | 668 | 40.6 |
| World | 473 | 28.7 |
| Germany | 340 | 20.6 |
| Norway | 30 | 1.8 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 3.3 70B Instruct

### How much energy does Llama 3.3 70B Instruct use per million output tokens?

Llama 3.3 70B Instruct uses 60.7 Wh of GPU energy per million output tokens on 2 × B200 and 117.5 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Llama 3.3 70B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.94× the energy per token of the B200 configuration: 117.5 Wh/M on 4 × H100 against 60.7 Wh/M on 2 × B200. Both are floors at high load.

### How much does load change the energy per token of Llama 3.3 70B Instruct?

On 4 × H100, energy per token falls 9.1× between a running batch of 8 (1,068.6 Wh/M) and 724 (117.5 Wh/M), because the cards' power rises only 42 percent while throughput rises 13.0×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 3.3 70B Instruct?

A billion output tokens of Llama 3.3 70B Instruct on 2 × B200 at its index row carries about 41.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.8 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 3.3 70B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 19 stable configurations of Llama 3.3 70B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-3.3-70B-Instruct).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-3-3-70b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 3.3 70B Instruct on your own grid and load.
