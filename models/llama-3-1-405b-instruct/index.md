# Llama 3.1 405B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Llama 3.1 405B Instruct: 12 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-3-1-405b-instruct/ (this file: https://leadgreen.ai/models/llama-3-1-405b-instruct/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200*

Llama 3.1 405B Instruct serves a million output tokens for **282.0 Wh/M** on 8 × B200 (running batch 3,589, median inter-token latency 272 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [meta-llama/Llama-3.1-405B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct), a dense transformer, weights in BF16. **Measured** 12 configurations on B200. **Data** [models/llama-3-1-405b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-1-405b-instruct.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/llama-3-1-405b-instruct/#configurations)
- [Carbon](https://leadgreen.ai/models/llama-3-1-405b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/llama-3-1-405b-instruct/#sources)

- **Index row, B200:** 282.0 Wh/M 8 × B200, BF16. Running batch 3,589, median ITL 272 ms, 7,530 W across the cards, 7,419 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 3.1 405B Instruct at every measured load

On 8 × B200, Llama 3.1 405B Instruct runs from **6,073.4 Wh/M** at a running batch of 8 to **282.0 Wh/M** at 3,589, a fall of 21.5×, while the cards' draw rises 28 percent (from 5,878 to 7,530 W) and throughput rises 27.6× (from 269 to 7,419 tokens a second). Median inter-token latency stays at 326 ms or under up to the best row.

*Llama 3.1 405B Instruct, BF16, 8 × B200: twelve measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 6,073.4 | 29 | 269 | 5,878 |
| 16 | 16 | 3,228.0 | 29 | 523 | 6,077 |
| 32 | 32 | 1,777.6 | 28 | 1,052 | 6,735 |
| 64 | 64 | 1,133.9 | 31 | 1,800 | 7,350 |
| 128 | 128 | 750.2 | 37 | 2,805 | 7,575 |
| 256 | 255 | 591.9 | 49 | 3,587 | 7,643 |
| 512 | 510 | 467.2 | 77 | 4,551 | 7,655 |
| 768 | 766 | 379.7 | 122 | 5,496 | 7,512 |
| 1,024 | 1,021 | 331.5 | 146 | 6,461 | 7,710 |
| 2,048 | 2,043 | 297.4 | 240 | 7,173 | 7,680 |
| 3,072 | 3,063 | 289.8 | 326 | 7,174 | 7,484 |
| 4,096 | 3,589 | 282.0 | 272 | 7,419 | 7,530 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 3.1 405B Instruct on 8 × B200 at its index row carries about 195.1 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 8.4 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 3.1 405B Instruct, 8 × B200 index row (282.0 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 199.4 |
| Saudi Arabia | 692 | 195.1 |
| Hong Kong | 676 | 190.5 |
| Serbia | 668 | 188.4 |
| World | 474 | 133.6 |
| Germany | 340 | 95.8 |
| Norway | 30 | 8.4 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 3.1 405B Instruct

### How much energy does Llama 3.1 405B Instruct use per million output tokens?

Llama 3.1 405B Instruct uses 282.0 Wh of GPU energy per million output tokens on 8 × B200 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### How much does load change the energy per token of Llama 3.1 405B Instruct?

On 8 × B200, energy per token falls 21.5× between a running batch of 8 (6,073.4 Wh/M) and 3,589 (282.0 Wh/M), because the cards' power rises only 28 percent while throughput rises 27.6×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 3.1 405B Instruct?

A billion output tokens of Llama 3.1 405B Instruct on 8 × B200 at its index row carries about 195.1 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 8.4 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 3.1 405B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 12 stable configurations of Llama 3.1 405B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-3.1-405B-Instruct).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-3-1-405b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 3.1 405B Instruct on your own grid and load.
