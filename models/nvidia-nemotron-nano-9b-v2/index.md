# NVIDIA Nemotron Nano 9B V2: GPU energy per million output tokens

> GPU watt-hours per million output tokens for NVIDIA Nemotron Nano 9B V2: 14 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/ (this file: https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

NVIDIA Nemotron Nano 9B V2 serves a million output tokens for **40.9 Wh/M** on 1 × B200 (running batch 255, median inter-token latency 41 ms) and **43.1 Wh/M** on 1 × H100 (running batch 255, median inter-token latency 43 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [nvidia/NVIDIA-Nemotron-Nano-9B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2), a Mamba-Transformer hybrid, weights in BF16. **Measured** 14 configurations on B200 and H100. **Data** [models/nvidia-nemotron-nano-9b-v2.json](https://leadgreen.ai/api/v1/models/nvidia-nemotron-nano-9b-v2.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#configurations)
- [Two generations](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#generations)
- [Carbon](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#carbon)
- [Two tasks](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#workloads)
- [Questions](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)
- [Sources](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#sources)

- **Index row, B200:** 40.9 Wh/M 1 × B200, BF16. Running batch 255, median ITL 41 ms, 800 W across the cards, 5,425 tokens a second.
- **Index row, H100:** 43.1 Wh/M 1 × H100, BF16. Running batch 255, median ITL 43 ms, 693 W across the cards, 4,465 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## NVIDIA Nemotron Nano 9B V2 at every measured load

On 1 × H100, NVIDIA Nemotron Nano 9B V2 runs from **162.7 Wh/M** at a running batch of 8 to **43.1 Wh/M** at 255, a fall of 3.8×, while the cards' draw rises 48 percent (from 467 to 693 W) and throughput rises 5.6× (from 797 to 4,465 tokens a second). Median inter-token latency stays at 43 ms or under up to the best row.

*NVIDIA Nemotron Nano 9B V2, BF16, 1 × B200: six measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 143.4 | 6 | 1,234 | 637 |
| 16 | 16 | 91.2 | 7 | 1,804 | 592 |
| 32 | 32 | 67.2 | 11 | 2,259 | 547 |
| 64 | 64 | 53.2 | 16 | 3,010 | 576 |
| 128 | 128 | 44.1 | 25 | 4,038 | 642 |
| 256 | 255 | 40.9 | 41 | 5,425 | 800 |

*NVIDIA Nemotron Nano 9B V2, BF16, 1 × H100: eight measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 162.7 | 9 | 797 | 467 |
| 16 | 16 | 98.4 | 10 | 1,398 | 495 |
| 32 | 32 | 70.4 | 12 | 2,150 | 545 |
| 64 | 64 | 57.6 | 17 | 2,979 | 618 |
| 96 | 96 | 51.8 | 21 | 3,439 | 642 |
| 128 | 127 | 49.2 | 26 | 3,743 | 663 |
| 192 | 191 | 45.7 | 35 | 4,199 | 691 |
| 256 | 255 | 43.1 | 43 | 4,465 | 693 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.05× the energy per token of the B200 configuration: 43.1 Wh/M on 1 × H100 against 40.9 Wh/M on 1 × B200. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of NVIDIA Nemotron Nano 9B V2 on 1 × B200 at its index row carries about 28.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*NVIDIA Nemotron Nano 9B V2, 1 × B200 index row (40.9 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 28.9 |
| Saudi Arabia | 692 | 28.3 |
| Hong Kong | 676 | 27.7 |
| Serbia | 668 | 27.3 |
| World | 474 | 19.4 |
| Germany | 340 | 13.9 |
| Norway | 30 | 1.2 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 9B V2 costs 3.4× the energy per response and 0.79× the energy per token on 1 × B200 (answers of 5,361 tokens against 1,242; running batch 512 against 255) and 7.6× the energy per response and 0.70× the energy per token on 1 × H100 (answers of 5,531 tokens against 510; running batch 256 against 255), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about NVIDIA Nemotron Nano 9B V2

### How much energy does NVIDIA Nemotron Nano 9B V2 use per million output tokens?

NVIDIA Nemotron Nano 9B V2 uses 40.9 Wh of GPU energy per million output tokens on 1 × B200 and 43.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is NVIDIA Nemotron Nano 9B V2 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.05× the energy per token of the B200 configuration: 43.1 Wh/M on 1 × H100 against 40.9 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of NVIDIA Nemotron Nano 9B V2?

On 1 × H100, energy per token falls 3.8× between a running batch of 8 (162.7 Wh/M) and 255 (43.1 Wh/M), because the cards' power rises only 48 percent while throughput rises 5.6×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of NVIDIA Nemotron Nano 9B V2?

A billion output tokens of NVIDIA Nemotron Nano 9B V2 on 1 × B200 at its index row carries about 28.3 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does NVIDIA Nemotron Nano 9B V2 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 9B V2 costs 3.4× the energy per response and 0.79× the energy per token on 1 × B200 (answers of 5,361 tokens against 1,242; running batch 512 against 255) and 7.6× the energy per response and 0.70× the energy per token on 1 × H100 (answers of 5,531 tokens against 510; running batch 256 against 255), compared with Text Conversation.

### Is this the energy my NVIDIA Nemotron Nano 9B V2 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 14 stable configurations of NVIDIA Nemotron Nano 9B V2 measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-9B-v2).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/nvidia-nemotron-nano-9b-v2.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for NVIDIA Nemotron Nano 9B V2 on your own grid and load.
