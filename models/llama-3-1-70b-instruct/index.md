# Llama 3.1 70B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Llama 3.1 70B Instruct: 22 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-3-1-70b-instruct/ (this file: https://leadgreen.ai/models/llama-3-1-70b-instruct/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Llama 3.1 70B Instruct serves a million output tokens for 52.4 Wh/M on 2 × B200 (running batch 2,042, median inter-token latency 140 ms) and 103.7 Wh/M on 4 × H100 (running batch 898, median inter-token latency 106 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

Model [meta-llama/Llama-3.1-70B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct), a dense transformer, weights in BF16. Measured 22 configurations on B200 and H100. Data [models/llama-3-1-70b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-1-70b-instruct.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/llama-3-1-70b-instruct/#configurations)
- [Two generations](https://leadgreen.ai/models/llama-3-1-70b-instruct/#generations)
- [Carbon](https://leadgreen.ai/models/llama-3-1-70b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/llama-3-1-70b-instruct/#sources)

- Index row, B200: 52.4 Wh/M 2 × B200, BF16. Running batch 2,042, median ITL 140 ms, 1,907 W across the cards, 10,108 tokens a second.
- Index row, H100: 103.7 Wh/M 4 × H100, BF16. Running batch 898, median ITL 106 ms, 2,548 W across the cards, 6,827 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 3.1 70B Instruct at every measured load

On 4 × H100, Llama 3.1 70B Instruct runs from 1,044.1 Wh/M at a running batch of 8 to 103.7 Wh/M at 898, a fall of 10.1×, while the cards' draw rises 44 percent (from 1,765 to 2,548 W) and throughput rises 14.5× (from 470 to 6,827 tokens a second). Median inter-token latency stays at 106 ms or under up to the best row.

*Llama 3.1 70B Instruct, BF16, 2 × B200: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 991.5 | 16 | 476 | 1,698 |
| 16 | 16 | 528.5 | 17 | 911 | 1,733 |
| 32 | 32 | 303.2 | 19 | 1,590 | 1,735 |
| 64 | 64 | 193.6 | 22 | 2,598 | 1,811 |
| 128 | 128 | 133.6 | 27 | 3,978 | 1,913 |
| 256 | 255 | 100.4 | 36 | 5,372 | 1,942 |
| 512 | 511 | 75.2 | 64 | 7,134 | 1,932 |
| 1,024 | 1,021 | 63.0 | 105 | 8,551 | 1,938 |
| 1,536 | 1,407 | 61.4 | 135 | 8,682 | 1,919 |
| 2,048 | 2,042 | 52.4 | 140 | 10,108 | 1,907 |

*Llama 3.1 70B Instruct, BF16, 4 × H100: twelve measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,044.1 | 17 | 470 | 1,765 |
| 16 | 16 | 580.8 | 18 | 863 | 1,804 |
| 32 | 32 | 335.2 | 20 | 1,487 | 1,794 |
| 64 | 64 | 221.5 | 22 | 2,511 | 2,002 |
| 96 | 96 | 179.9 | 25 | 3,244 | 2,102 |
| 128 | 128 | 156.5 | 28 | 3,876 | 2,184 |
| 192 | 192 | 142.8 | 34 | 4,461 | 2,293 |
| 256 | 255 | 133.1 | 40 | 4,915 | 2,354 |
| 384 | 383 | 122.4 | 55 | 5,319 | 2,344 |
| 512 | 511 | 116.9 | 74 | 5,921 | 2,493 |
| 768 | 766 | 108.2 | 104 | 6,507 | 2,535 |
| 1,024 | 898 | 103.7 | 106 | 6,827 | 2,548 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.98× the energy per token of the B200 configuration: 103.7 Wh/M on 4 × H100 against 52.4 Wh/M on 2 × B200. The two rows were not swept alike: the H100 row holds a running batch of 898 on 4 cards and the B200 row 2,042 on 2, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 3.1 70B Instruct on 2 × B200 at its index row carries about 36.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 1.6 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 3.1 70B Instruct, 2 × B200 index row (52.4 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 37.1 |
| Saudi Arabia | 692 | 36.3 |
| Hong Kong | 676 | 35.4 |
| Serbia | 668 | 35.0 |
| World | 474 | 24.8 |
| Germany | 340 | 17.8 |
| Norway | 30 | 1.6 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 3.1 70B Instruct

### How much energy does Llama 3.1 70B Instruct use per million output tokens?

Llama 3.1 70B Instruct uses 52.4 Wh of GPU energy per million output tokens on 2 × B200 and 103.7 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Llama 3.1 70B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.98× the energy per token of the B200 configuration: 103.7 Wh/M on 4 × H100 against 52.4 Wh/M on 2 × B200. Both are floors at high load.

### How much does load change the energy per token of Llama 3.1 70B Instruct?

On 4 × H100, energy per token falls 10.1× between a running batch of 8 (1,044.1 Wh/M) and 898 (103.7 Wh/M), because the cards' power rises only 44 percent while throughput rises 14.5×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 3.1 70B Instruct?

A billion output tokens of Llama 3.1 70B Instruct on 2 × B200 at its index row carries about 36.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 1.6 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 3.1 70B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 22 stable configurations of Llama 3.1 70B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-3.1-70B-Instruct).

Cite as. Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-3-1-70b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 3.1 70B Instruct on your own grid and load.
