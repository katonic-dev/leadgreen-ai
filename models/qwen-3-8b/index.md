# Qwen 3 8B: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 8B on B200 and H100: 19 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-8b/ (this file: https://leadgreen.ai/models/qwen-3-8b/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 8B serves a million output tokens for **14.7 Wh/M** on 1 × B200 (running batch 1,427, median inter-token latency 91 ms) and **20.0 Wh/M** on 1 × H100 (running batch 474, median inter-token latency 47 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-8B](https://huggingface.co/Qwen/Qwen3-8B), a dense transformer, weights in BF16. **Measured** 19 configurations on B200 and H100. **Data** [models/qwen-3-8b.json](https://leadgreen.ai/api/v1/models/qwen-3-8b.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/qwen-3-8b/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-8b/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-8b/#carbon)
- [Two tasks](https://leadgreen.ai/models/qwen-3-8b/#workloads)
- [Questions](https://leadgreen.ai/models/qwen-3-8b/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-8b/#sources)

- **Index row, B200:** 14.7 Wh/M 1 × B200, BF16. Running batch 1,427, median ITL 91 ms, 801 W across the cards, 15,100 tokens a second.
- **Index row, H100:** 20.0 Wh/M 1 × H100, BF16. Running batch 474, median ITL 47 ms, 616 W across the cards, 8,535 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 8B at every measured load

On 1 × H100, Qwen 3 8B runs from **123.3 Wh/M** at a running batch of 8 to **20.0 Wh/M** at 474, a fall of 6.2×, while the cards' draw rises 44 percent (from 427 to 616 W) and throughput rises 8.9× (from 962 to 8,535 tokens a second). Median inter-token latency stays at 47 ms or under up to the best row.

*Qwen 3 8B, BF16, 1 × B200: nine measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 119.6 | 5 | 1,502 | 646 |
| 16 | 16 | 70.9 | 6 | 2,086 | 532 |
| 32 | 32 | 51.3 | 10 | 2,673 | 494 |
| 64 | 64 | 34.0 | 13 | 4,432 | 543 |
| 128 | 128 | 22.8 | 12 | 9,119 | 748 |
| 256 | 255 | 20.1 | 20 | 11,463 | 831 |
| 512 | 511 | 17.2 | 35 | 12,164 | 752 |
| 1,024 | 1,022 | 17.0 | 80 | 11,809 | 723 |
| 1,536 | 1,427 | 14.7 | 91 | 15,100 | 801 |

*Qwen 3 8B, BF16, 1 × H100: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 123.3 | 8 | 962 | 427 |
| 16 | 16 | 71.9 | 9 | 1,745 | 451 |
| 32 | 32 | 45.4 | 11 | 2,928 | 478 |
| 64 | 64 | 33.1 | 14 | 4,315 | 514 |
| 96 | 96 | 28.7 | 18 | 5,255 | 544 |
| 128 | 128 | 26.8 | 21 | 5,930 | 573 |
| 192 | 192 | 24.0 | 26 | 6,932 | 600 |
| 256 | 255 | 22.8 | 31 | 7,719 | 633 |
| 384 | 383 | 20.9 | 43 | 8,258 | 622 |
| 512 | 474 | 20.0 | 47 | 8,535 | 616 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.36× the energy per token of the B200 configuration: 20.0 Wh/M on 1 × H100 against 14.7 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 474 on 1 card and the B200 row 1,427 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 8B on 1 × B200 at its index row carries about 10.2 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 8B, 1 × B200 index row (14.7 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 10.4 |
| Saudi Arabia | 692 | 10.2 |
| Hong Kong | 676 | 10.0 |
| Serbia | 668 | 9.8 |
| World | 474 | 7.0 |
| Germany | 340 | 5.0 |
| Norway | 30 | 0.4 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, Qwen 3 8B costs 38.3× the energy per response and 3.06× the energy per token on 1 × H100 (answers of 8,052 tokens against 645; running batch 82 against 474) and 40.6× the energy per response and 3.26× the energy per token on 1 × B200 (answers of 8,074 tokens against 649; running batch 128 against 1,427), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about Qwen 3 8B

### How much energy does Qwen 3 8B use per million output tokens?

Qwen 3 8B uses 14.7 Wh of GPU energy per million output tokens on 1 × B200 and 20.0 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 8B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.36× the energy per token of the B200 configuration: 20.0 Wh/M on 1 × H100 against 14.7 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 8B?

On 1 × H100, energy per token falls 6.2× between a running batch of 8 (123.3 Wh/M) and 474 (20.0 Wh/M), because the cards' power rises only 44 percent while throughput rises 8.9×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 8B?

A billion output tokens of Qwen 3 8B on 1 × B200 at its index row carries about 10.2 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does Qwen 3 8B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 8B costs 38.3× the energy per response and 3.06× the energy per token on 1 × H100 (answers of 8,052 tokens against 645; running batch 82 against 474) and 40.6× the energy per response and 3.26× the energy per token on 1 × B200 (answers of 8,074 tokens against 649; running batch 128 against 1,427), compared with Text Conversation.

### Is this the energy my Qwen 3 8B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 19 stable configurations of Qwen 3 8B measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-8B).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-8b.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 8B on your own grid and load.
