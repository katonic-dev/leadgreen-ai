# NVIDIA Nemotron Nano 12B V2: GPU energy per million output tokens

> GPU watt-hours per million output tokens for NVIDIA Nemotron Nano 12B V2: 14 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/ (this file: https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

NVIDIA Nemotron Nano 12B V2 serves a million output tokens for **39.4 Wh/M** on 1 × B200 (running batch 256, median inter-token latency 34 ms) and **50.1 Wh/M** on 1 × H100 (running batch 241, median inter-token latency 46 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [nvidia/NVIDIA-Nemotron-Nano-12B-v2](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-12B-v2), a Mamba-Transformer hybrid, weights in BF16. **Measured** 14 configurations on B200 and H100. **Data** [models/nvidia-nemotron-nano-12b-v2.json](https://leadgreen.ai/api/v1/models/nvidia-nemotron-nano-12b-v2.json). Updated 17 October 2026.

- [Every configuration](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#configurations)
- [Two generations](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#generations)
- [Carbon](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#carbon)
- [Two tasks](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#workloads)
- [Questions](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)
- [Sources](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#sources)

- **Index row, B200:** 39.4 Wh/M 1 × B200, BF16. Running batch 256, median ITL 34 ms, 885 W across the cards, 6,233 tokens a second.
- **Index row, H100:** 50.1 Wh/M 1 × H100, BF16. Running batch 241, median ITL 46 ms, 694 W across the cards, 3,847 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## NVIDIA Nemotron Nano 12B V2 at every measured load

On 1 × H100, NVIDIA Nemotron Nano 12B V2 runs from **207.6 Wh/M** at a running batch of 8 to **50.1 Wh/M** at 241, a fall of 4.1×, while the cards' draw rises 39 percent (from 498 to 694 W) and throughput rises 5.8× (from 666 to 3,847 tokens a second). Median inter-token latency stays at 46 ms or under up to the best row.

*NVIDIA Nemotron Nano 12B V2, BF16, 1 × B200: six measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 182.4 | 7 | 1,032 | 678 |
| 16 | 16 | 116.9 | 11 | 1,213 | 510 |
| 32 | 32 | 83.9 | 16 | 1,717 | 519 |
| 64 | 64 | 56.9 | 20 | 2,764 | 566 |
| 128 | 128 | 43.8 | 23 | 4,560 | 719 |
| 256 | 256 | 39.4 | 34 | 6,233 | 885 |

*NVIDIA Nemotron Nano 12B V2, BF16, 1 × H100: eight measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 207.6 | 11 | 666 | 498 |
| 16 | 16 | 125.8 | 12 | 1,141 | 517 |
| 32 | 32 | 86.0 | 14 | 1,807 | 560 |
| 64 | 64 | 68.4 | 19 | 2,553 | 629 |
| 96 | 95 | 61.0 | 24 | 2,951 | 648 |
| 128 | 128 | 58.0 | 29 | 3,229 | 675 |
| 192 | 191 | 52.2 | 39 | 3,683 | 692 |
| 256 | 241 | 50.1 | 46 | 3,847 | 694 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.27× the energy per token of the B200 configuration: 50.1 Wh/M on 1 × H100 against 39.4 Wh/M on 1 × B200. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of NVIDIA Nemotron Nano 12B V2 on 1 × B200 at its index row carries about 27.2 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*NVIDIA Nemotron Nano 12B V2, 1 × B200 index row (39.4 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 27.9 |
| Saudi Arabia | 689 | 27.2 |
| Hong Kong | 676 | 26.6 |
| Serbia | 668 | 26.4 |
| World | 473 | 18.7 |
| Germany | 340 | 13.4 |
| Norway | 30 | 1.2 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Two tasks*

## Long answers cost more per token too

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 12B V2 costs 3.9× the energy per response and 1.02× the energy per token on 1 × B200 (answers of 5,646 tokens against 1,464; running batch 256 against 256) and 8.7× the energy per response and 0.70× the energy per token on 1 × H100 (answers of 5,768 tokens against 462; running batch 192 against 241), compared with Text Conversation. The long answers cut the batch the server can hold, which is why energy per token itself moves. All 11 pairs are on [the index](https://leadgreen.ai/index/#workloads).

*Questions*

## Asked about NVIDIA Nemotron Nano 12B V2

### How much energy does NVIDIA Nemotron Nano 12B V2 use per million output tokens?

NVIDIA Nemotron Nano 12B V2 uses 39.4 Wh of GPU energy per million output tokens on 1 × B200 and 50.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is NVIDIA Nemotron Nano 12B V2 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.27× the energy per token of the B200 configuration: 50.1 Wh/M on 1 × H100 against 39.4 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of NVIDIA Nemotron Nano 12B V2?

On 1 × H100, energy per token falls 4.1× between a running batch of 8 (207.6 Wh/M) and 241 (50.1 Wh/M), because the cards' power rises only 39 percent while throughput rises 5.8×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of NVIDIA Nemotron Nano 12B V2?

A billion output tokens of NVIDIA Nemotron Nano 12B V2 on 1 × B200 at its index row carries about 27.2 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Does NVIDIA Nemotron Nano 12B V2 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 12B V2 costs 3.9× the energy per response and 1.02× the energy per token on 1 × B200 (answers of 5,646 tokens against 1,464; running batch 256 against 256) and 8.7× the energy per response and 0.70× the energy per token on 1 × H100 (answers of 5,768 tokens against 462; running batch 192 against 241), compared with Text Conversation.

### Is this the energy my NVIDIA Nemotron Nano 12B V2 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 14 stable configurations of NVIDIA Nemotron Nano 12B V2 measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/nvidia/NVIDIA-Nemotron-Nano-12B-v2).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-17, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/nvidia-nemotron-nano-12b-v2.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for NVIDIA Nemotron Nano 12B V2 on your own grid and load.
