# DeepSeek V3.1: GPU energy per million output tokens

> GPU watt-hours per million output tokens for DeepSeek V3.1 on B200: 11 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/deepseek-v3-1/ (this file: https://leadgreen.ai/models/deepseek-v3-1/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200*

DeepSeek V3.1 serves a million output tokens for **168.4 Wh/M** on 8 × B200 (running batch 3,008, median inter-token latency 186 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [deepseek-ai/DeepSeek-V3.1](https://huggingface.co/deepseek-ai/DeepSeek-V3.1), a mixture-of-experts model (37 B of 671 B parameters active per token), weights in FP8. **Measured** 11 configurations on B200. **Data** [models/deepseek-v3-1.json](https://leadgreen.ai/api/v1/models/deepseek-v3-1.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/deepseek-v3-1/#configurations)
- [Carbon](https://leadgreen.ai/models/deepseek-v3-1/#carbon)
- [Two tasks](https://leadgreen.ai/models/deepseek-v3-1/#workloads)
- [Questions](https://leadgreen.ai/models/deepseek-v3-1/#faq)
- [Sources](https://leadgreen.ai/models/deepseek-v3-1/#sources)

- **Index row, B200:** 168.4 Wh/M 8 × B200, FP8. Running batch 3,008, median ITL 186 ms, 5,470 W across the cards, 9,021 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## DeepSeek V3.1 at every measured load

On 8 × B200, DeepSeek V3.1 runs from **2,379.3 Wh/M** at a running batch of 8 to **168.4 Wh/M** at 3,008, a fall of 14.1×, while the cards' draw rises 42 percent (from 3,854 to 5,470 W) and throughput rises 20.1× (from 450 to 9,021 tokens a second). Median inter-token latency stays at 187 ms or under up to the best row.

*DeepSeek V3.1, FP8, 8 × B200: eleven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 2,379.3 | 17 | 450 | 3,854 |
| 16 | 16 | 1,685.1 | 20 | 729 | 4,422 |
| 32 | 32 | 1,219.3 | 27 | 1,091 | 4,791 |
| 64 | 64 | 811.0 | 33 | 1,776 | 5,186 |
| 128 | 128 | 537.9 | 39 | 2,907 | 5,629 |
| 256 | 256 | 363.6 | 49 | 4,534 | 5,935 |
| 512 | 511 | 267.6 | 64 | 5,588 | 5,384 |
| 768 | 767 | 251.3 | 113 | 5,820 | 5,266 |
| 1,024 | 1,022 | 214.5 | 128 | 7,298 | 5,635 |
| 2,048 | 2,042 | 175.0 | 187 | 9,302 | 5,862 |
| 3,072 | 3,008 | 168.4 | 186 | 9,021 | 5,470 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Carbon*

## Same tokens, different grid

A billion output tokens of DeepSeek V3.1 on 8 × B200 at its index row carries about 116.5 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 5.0 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*DeepSeek V3.1, 8 × B200 index row (168.4 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 119.1 |
| Saudi Arabia | 692 | 116.5 |
| Hong Kong | 676 | 113.8 |
| Serbia | 668 | 112.5 |
| World | 474 | 79.8 |
| Germany | 340 | 57.2 |
| Norway | 30 | 5.0 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, DeepSeek V3.1 costs 23.5× the energy per response and 2.20× the energy per token on 8 × B200 (answers of 8,969 tokens against 842; running batch 256 against 3,008), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about DeepSeek V3.1

### How much energy does DeepSeek V3.1 use per million output tokens?

DeepSeek V3.1 uses 168.4 Wh of GPU energy per million output tokens on 8 × B200 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### How much does load change the energy per token of DeepSeek V3.1?

On 8 × B200, energy per token falls 14.1× between a running batch of 8 (2,379.3 Wh/M) and 3,008 (168.4 Wh/M), because the cards' power rises only 42 percent while throughput rises 20.1×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of DeepSeek V3.1?

A billion output tokens of DeepSeek V3.1 on 8 × B200 at its index row carries about 116.5 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 5.0 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does DeepSeek V3.1 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, DeepSeek V3.1 costs 23.5× the energy per response and 2.20× the energy per token on 8 × B200 (answers of 8,969 tokens against 842; running batch 256 against 3,008), compared with Text Conversation.

### Is this the energy my DeepSeek V3.1 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 11 stable configurations of DeepSeek V3.1 measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V3.1).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/deepseek-v3-1.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for DeepSeek V3.1 on your own grid and load.
