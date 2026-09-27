# Qwen 3 14B: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Qwen 3 14B on B200 and H100: 17 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/qwen-3-14b/ (this file: https://leadgreen.ai/models/qwen-3-14b/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Qwen 3 14B serves a million output tokens for **15.2 Wh/M** on 1 × B200 (running batch 2,045, median inter-token latency 113 ms) and **31.1 Wh/M** on 1 × H100 (running batch 253, median inter-token latency 38 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [Qwen/Qwen3-14B](https://huggingface.co/Qwen/Qwen3-14B), a dense transformer, weights in BF16. **Measured** 17 configurations on B200 and H100. **Data** [models/qwen-3-14b.json](https://leadgreen.ai/api/v1/models/qwen-3-14b.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/qwen-3-14b/#configurations)
- [Two generations](https://leadgreen.ai/models/qwen-3-14b/#generations)
- [Carbon](https://leadgreen.ai/models/qwen-3-14b/#carbon)
- [Two tasks](https://leadgreen.ai/models/qwen-3-14b/#workloads)
- [Questions](https://leadgreen.ai/models/qwen-3-14b/#faq)
- [Sources](https://leadgreen.ai/models/qwen-3-14b/#sources)

- **Index row, B200:** 15.2 Wh/M 1 × B200, BF16. Running batch 2,045, median ITL 113 ms, 869 W across the cards, 15,875 tokens a second.
- **Index row, H100:** 31.1 Wh/M 1 × H100, BF16. Running batch 253, median ITL 38 ms, 645 W across the cards, 5,760 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Qwen 3 14B at every measured load

On 1 × B200, Qwen 3 14B runs from **194.3 Wh/M** at a running batch of 8 to **15.2 Wh/M** at 2,045, a fall of 12.8×, while the cards' draw rises 14 percent (from 760 to 869 W) and throughput rises 14.6× (from 1,087 to 15,875 tokens a second). Median inter-token latency stays at 113 ms or under up to the best row.

*Qwen 3 14B, BF16, 1 × B200: nine measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 194.3 | 7 | 1,087 | 760 |
| 16 | 16 | 110.6 | 8 | 1,913 | 762 |
| 32 | 32 | 67.8 | 9 | 2,866 | 700 |
| 64 | 64 | 46.4 | 13 | 4,176 | 697 |
| 128 | 128 | 34.0 | 19 | 5,787 | 709 |
| 256 | 256 | 24.8 | 21 | 10,709 | 955 |
| 512 | 511 | 21.4 | 39 | 11,858 | 913 |
| 1,024 | 1,022 | 17.2 | 62 | 15,050 | 932 |
| 2,048 | 2,045 | 15.2 | 113 | 15,875 | 869 |

*Qwen 3 14B, BF16, 1 × H100: eight measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 196.1 | 13 | 627 | 443 |
| 16 | 16 | 110.6 | 13 | 1,168 | 465 |
| 32 | 32 | 67.8 | 15 | 2,023 | 494 |
| 64 | 64 | 46.4 | 19 | 3,140 | 525 |
| 96 | 96 | 39.9 | 23 | 3,775 | 542 |
| 128 | 128 | 35.5 | 26 | 4,474 | 572 |
| 192 | 192 | 32.1 | 33 | 5,309 | 613 |
| 256 | 253 | 31.1 | 38 | 5,760 | 645 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 2.04× the energy per token of the B200 configuration: 31.1 Wh/M on 1 × H100 against 15.2 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 253 on 1 card and the B200 row 2,045 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Qwen 3 14B on 1 × B200 at its index row carries about 10.5 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Qwen 3 14B, 1 × B200 index row (15.2 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 10.8 |
| Saudi Arabia | 692 | 10.5 |
| Hong Kong | 676 | 10.3 |
| Serbia | 668 | 10.2 |
| World | 474 | 7.2 |
| Germany | 340 | 5.2 |
| Norway | 30 | 0.5 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, Qwen 3 14B costs 26.8× the energy per response and 2.50× the energy per token on 1 × H100 (answers of 6,711 tokens against 625; running batch 59 against 253) and 39.8× the energy per response and 3.33× the energy per token on 1 × B200 (answers of 7,327 tokens against 613; running batch 128 against 2,045), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about Qwen 3 14B

### How much energy does Qwen 3 14B use per million output tokens?

Qwen 3 14B uses 15.2 Wh of GPU energy per million output tokens on 1 × B200 and 31.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Qwen 3 14B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 2.04× the energy per token of the B200 configuration: 31.1 Wh/M on 1 × H100 against 15.2 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Qwen 3 14B?

On 1 × B200, energy per token falls 12.8× between a running batch of 8 (194.3 Wh/M) and 2,045 (15.2 Wh/M), because the cards' power rises only 14 percent while throughput rises 14.6×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Qwen 3 14B?

A billion output tokens of Qwen 3 14B on 1 × B200 at its index row carries about 10.5 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does Qwen 3 14B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 14B costs 26.8× the energy per response and 2.50× the energy per token on 1 × H100 (answers of 6,711 tokens against 625; running batch 59 against 253) and 39.8× the energy per response and 3.33× the energy per token on 1 × B200 (answers of 7,327 tokens against 613; running batch 128 against 2,045), compared with Text Conversation.

### Is this the energy my Qwen 3 14B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 17 stable configurations of Qwen 3 14B measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/Qwen/Qwen3-14B).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/qwen-3-14b.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Qwen 3 14B on your own grid and load.
