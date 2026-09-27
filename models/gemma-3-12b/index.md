# Gemma 3 12B: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Gemma 3 12B on B200 and H100: 13 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/gemma-3-12b/ (this file: https://leadgreen.ai/models/gemma-3-12b/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Gemma 3 12B serves a million output tokens for 26.5 Wh/M on 1 × B200 (running batch 487, median inter-token latency 44 ms) and 46.1 Wh/M on 1 × H100 (running batch 128, median inter-token latency 35 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

Model [google/gemma-3-12b-it](https://huggingface.co/google/gemma-3-12b-it), a dense transformer, weights in BF16. Measured 13 configurations on B200 and H100. Data [models/gemma-3-12b.json](https://leadgreen.ai/api/v1/models/gemma-3-12b.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/gemma-3-12b/#configurations)
- [Two generations](https://leadgreen.ai/models/gemma-3-12b/#generations)
- [Carbon](https://leadgreen.ai/models/gemma-3-12b/#carbon)
- [Questions](https://leadgreen.ai/models/gemma-3-12b/#faq)
- [Sources](https://leadgreen.ai/models/gemma-3-12b/#sources)

- Index row, B200: 26.5 Wh/M 1 × B200, BF16. Running batch 487, median ITL 44 ms, 928 W across the cards, 9,733 tokens a second.
- Index row, H100: 46.1 Wh/M 1 × H100, BF16. Running batch 128, median ITL 35 ms, 589 W across the cards, 3,546 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Gemma 3 12B at every measured load

On 1 × B200, Gemma 3 12B runs from 185.9 Wh/M at a running batch of 8 to 26.5 Wh/M at 487, a fall of 7.0×, while the cards' draw rises 39 percent (from 668 to 928 W) and throughput rises 9.8× (from 998 to 9,733 tokens a second). Median inter-token latency stays at 44 ms or under up to the best row.

*Gemma 3 12B, BF16, 1 × B200: seven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 185.9 | 8 | 998 | 668 |
| 16 | 16 | 109.5 | 8 | 1,726 | 681 |
| 32 | 32 | 68.5 | 11 | 2,535 | 625 |
| 64 | 64 | 47.7 | 13 | 4,375 | 751 |
| 128 | 128 | 37.4 | 19 | 6,203 | 834 |
| 256 | 256 | 31.4 | 28 | 8,333 | 943 |
| 512 | 487 | 26.5 | 44 | 9,733 | 928 |

*Gemma 3 12B, BF16, 1 × H100: six measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 195.0 | 13 | 604 | 424 |
| 16 | 16 | 116.1 | 15 | 1,082 | 452 |
| 32 | 32 | 75.2 | 17 | 1,787 | 484 |
| 64 | 64 | 55.8 | 23 | 2,691 | 541 |
| 96 | 96 | 49.6 | 28 | 3,224 | 575 |
| 128 | 128 | 46.1 | 35 | 3,546 | 589 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.74× the energy per token of the B200 configuration: 46.1 Wh/M on 1 × H100 against 26.5 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 128 on 1 card and the B200 row 487 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Gemma 3 12B on 1 × B200 at its index row carries about 18.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.8 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Gemma 3 12B, 1 × B200 index row (26.5 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 18.7 |
| Saudi Arabia | 692 | 18.3 |
| Hong Kong | 676 | 17.9 |
| Serbia | 668 | 17.7 |
| World | 474 | 12.5 |
| Germany | 340 | 9.0 |
| Norway | 30 | 0.8 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Gemma 3 12B

### How much energy does Gemma 3 12B use per million output tokens?

Gemma 3 12B uses 26.5 Wh of GPU energy per million output tokens on 1 × B200 and 46.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Gemma 3 12B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.74× the energy per token of the B200 configuration: 46.1 Wh/M on 1 × H100 against 26.5 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Gemma 3 12B?

On 1 × B200, energy per token falls 7.0× between a running batch of 8 (185.9 Wh/M) and 487 (26.5 Wh/M), because the cards' power rises only 39 percent while throughput rises 9.8×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Gemma 3 12B?

A billion output tokens of Gemma 3 12B on 1 × B200 at its index row carries about 18.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.8 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Gemma 3 12B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 13 stable configurations of Gemma 3 12B measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/google/gemma-3-12b-it).

Cite as. Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/gemma-3-12b.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Gemma 3 12B on your own grid and load.
