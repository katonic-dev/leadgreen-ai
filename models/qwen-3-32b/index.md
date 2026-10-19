# Qwen 3 32B: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 32B on B200 and H100: 22 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-32b/ (this file: https://leadgreen.ai/models/qwen-3-32b/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 32B serves a million output tokens for **39.1 Wh/M** on 1 × B200 (running batch 383, median inter-token latency 50 ms) and **63.5 Wh/M** on 2 × H100 (running batch 256, median inter-token latency 44 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-32B](https://huggingface.co/Qwen/Qwen3-32B), a dense transformer, weights in BF16. **Measured** 22 configurations on B200 and H100. **Data** [models/qwen-3-32b.json](https://leadgreen.ai/api/v1/models/qwen-3-32b.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Qwen 3 32B: energy per million output tokens. https://leadgreen.ai/models/qwen-3-32b/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [Every configuration](https://leadgreen.ai/models/qwen-3-32b/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-32b/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-32b/#carbon)
- [Two tasks](https://leadgreen.ai/models/qwen-3-32b/#workloads)
- [Questions](https://leadgreen.ai/models/qwen-3-32b/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-32b/#sources)

- **Index row, B200:** 39.1 Wh/M 1 × B200, BF16. Running batch 383, median ITL 50 ms, 972 W across the cards, 6,912 tokens a second.
- **Index row, H100:** 63.5 Wh/M 2 × H100, BF16. Running batch 256, median ITL 44 ms, 1,178 W across the cards, 5,155 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 32B at every measured load

On 1 × B200, Qwen 3 32B runs from **429.2 Wh/M** at a running batch of 8 to **39.1 Wh/M** at 383, a fall of 11.0×, while the cards' draw rises 13 percent (from 860 to 972 W) and throughput rises 12.4× (from 556 to 6,912 tokens a second). Median inter-token latency stays at 50 ms or under up to the best row. Past it, at a cap of 512, the same cards read 41.9 Wh/M at 58 ms.

*Qwen 3 32B, BF16, 1 × B200: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 429.2 | 14 | 556 | 860 |
| 16 | 16 | 226.6 | 15 | 1,025 | 836 |
| 32 | 32 | 131.5 | 17 | 1,793 | 849 |
| 64 | 64 | 86.8 | 20 | 3,024 | 945 |
| 96 | 96 | 65.7 | 21 | 4,102 | 970 |
| 128 | 128 | 58.0 | 25 | 4,676 | 976 |
| 192 | 192 | 49.1 | 32 | 5,483 | 969 |
| 256 | 256 | 41.9 | 36 | 6,444 | 971 |
| 384 | 383 | 39.1 | 50 | 6,912 | 972 |
| 512 | 456 | 41.9 | 58 | 6,426 | 969 |

*Qwen 3 32B, BF16, 1 × H100: three measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 479.4 | 25 | 312 | 538 |
| 16 | 16 | 267.0 | 26 | 589 | 566 |
| 32 | 29 | 173.3 | 29 | 961 | 599 |

*Qwen 3 32B, BF16, 2 × H100: nine measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 452.0 | 15 | 522 | 850 |
| 16 | 16 | 252.8 | 16 | 970 | 883 |
| 32 | 32 | 153.8 | 18 | 1,706 | 944 |
| 64 | 64 | 102.0 | 22 | 2,654 | 974 |
| 96 | 96 | 84.6 | 26 | 3,356 | 1,022 |
| 128 | 128 | 76.4 | 30 | 3,905 | 1,074 |
| 192 | 192 | 69.0 | 37 | 4,601 | 1,143 |
| 256 | 256 | 63.5 | 44 | 5,155 | 1,178 |
| 384 | 340 | 64.6 | 55 | 5,071 | 1,180 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.63× the energy per token of the B200 configuration: 63.5 Wh/M on 2 × H100 against 39.1 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 256 on 2 cards and the B200 row 383 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 32B on 1 × B200 at its index row carries about 26.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 32B, 1 × B200 index row (39.1 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 27.6 |
| Saudi Arabia | 689 | 26.9 |
| Hong Kong | 676 | 26.4 |
| Serbia | 668 | 26.1 |
| World | 473 | 18.5 |
| Germany | 340 | 13.3 |
| Norway | 30 | 1.2 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, Qwen 3 32B costs 24.6× the energy per response and 2.22× the energy per token on 1 × B200 (answers of 7,035 tokens against 635; running batch 111 against 383) and 26.1× the energy per response and 2.35× the energy per token on 2 × H100 (answers of 7,058 tokens against 634; running batch 64 against 256), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about Qwen 3 32B

### How much energy does Qwen 3 32B use per million output tokens?

Qwen 3 32B uses 39.1 Wh of GPU energy per million output tokens on 1 × B200 and 63.5 Wh of GPU energy per million output tokens on 2 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 32B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.63× the energy per token of the B200 configuration: 63.5 Wh/M on 2 × H100 against 39.1 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 32B?

On 1 × B200, energy per token falls 11.0× between a running batch of 8 (429.2 Wh/M) and 383 (39.1 Wh/M), because the cards' power rises only 13 percent while throughput rises 12.4×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 32B?

A billion output tokens of Qwen 3 32B on 1 × B200 at its index row carries about 26.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does Qwen 3 32B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 32B costs 24.6× the energy per response and 2.22× the energy per token on 1 × B200 (answers of 7,035 tokens against 635; running batch 111 against 383) and 26.1× the energy per response and 2.35× the energy per token on 2 × H100 (answers of 7,058 tokens against 634; running batch 64 against 256), compared with Text Conversation.

### Is this the energy my Qwen 3 32B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 22 stable configurations of Qwen 3 32B measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-32B).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-32b.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 32B on your own grid and load.
