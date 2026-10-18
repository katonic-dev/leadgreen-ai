# Llama 3.1 8B Instruct: GPU energy per million output tokens

> GPU watt-hours per million output tokens for Llama 3.1 8B Instruct: 20 measured configurations, load curve and carbon by grid. From ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-3-1-8b-instruct/ (this file: https://leadgreen.ai/models/llama-3-1-8b-instruct/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · B200 and H100*

Llama 3.1 8B Instruct serves a million output tokens for **13.0 Wh/M** on 1 × B200 (running batch 2,043, median inter-token latency 125 ms) and **19.5 Wh/M** on 1 × H100 (running batch 511, median inter-token latency 47 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [meta-llama/Llama-3.1-8B-Instruct](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct), a dense transformer, weights in BF16. **Measured** 20 configurations on B200 and H100. **Data** [models/llama-3-1-8b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-1-8b-instruct.json). Updated 18 October 2026.

- [Every configuration](https://leadgreen.ai/models/llama-3-1-8b-instruct/#configurations)
- [Two generations](https://leadgreen.ai/models/llama-3-1-8b-instruct/#generations)
- [Carbon](https://leadgreen.ai/models/llama-3-1-8b-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)
- [Sources](https://leadgreen.ai/models/llama-3-1-8b-instruct/#sources)

- **Index row, B200:** 13.0 Wh/M 1 × B200, BF16. Running batch 2,043, median ITL 125 ms, 691 W across the cards, 14,799 tokens a second.
- **Index row, H100:** 19.5 Wh/M 1 × H100, BF16. Running batch 511, median ITL 47 ms, 688 W across the cards, 9,806 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 3.1 8B Instruct at every measured load

On 1 × H100, Llama 3.1 8B Instruct runs from **126.3 Wh/M** at a running batch of 8 to **19.5 Wh/M** at 511, a fall of 6.5×, while the cards' draw rises 41 percent (from 486 to 688 W) and throughput rises 9.2× (from 1,070 to 9,806 tokens a second). Median inter-token latency stays at 47 ms or under up to the best row. Past it, at a cap of 768, the same cards read 19.8 Wh/M at 63 ms.

*Llama 3.1 8B Instruct, BF16, 1 × B200: nine measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 108.5 | 5 | 1,637 | 639 |
| 16 | 16 | 67.3 | 5 | 2,751 | 667 |
| 32 | 32 | 42.0 | 6 | 3,810 | 576 |
| 64 | 64 | 30.6 | 9 | 5,589 | 617 |
| 128 | 128 | 27.3 | 27 | 4,570 | 449 |
| 256 | 255 | 19.6 | 32 | 7,664 | 540 |
| 512 | 511 | 16.7 | 50 | 9,571 | 577 |
| 1,024 | 1,021 | 15.3 | 87 | 10,922 | 600 |
| 2,048 | 2,043 | 13.0 | 125 | 14,799 | 691 |

*Llama 3.1 8B Instruct, BF16, 1 × H100: eleven measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 126.3 | 7 | 1,070 | 486 |
| 16 | 16 | 73.0 | 8 | 1,954 | 513 |
| 32 | 32 | 45.8 | 9 | 3,391 | 560 |
| 64 | 64 | 32.9 | 12 | 5,147 | 610 |
| 96 | 96 | 28.6 | 14 | 6,260 | 644 |
| 128 | 128 | 26.4 | 16 | 7,037 | 669 |
| 192 | 192 | 23.2 | 21 | 8,223 | 688 |
| 256 | 255 | 21.3 | 26 | 9,010 | 691 |
| 384 | 383 | 20.6 | 38 | 9,248 | 687 |
| 512 | 511 | 19.5 | 47 | 9,806 | 688 |
| 768 | 691 | 19.8 | 63 | 9,603 | 685 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Two generations*

## H100 against B200

On the index rows, the H100 configuration uses 1.50× the energy per token of the B200 configuration: 19.5 Wh/M on 1 × H100 against 13.0 Wh/M on 1 × B200. The two rows were not swept alike: the H100 row holds a running batch of 511 on 1 card and the B200 row 2,043 on 1, so part of the gap is the sweep, not the silicon. The full comparison across 14 models is on [the index](https://leadgreen.ai/index/#generations).

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 3.1 8B Instruct on 1 × B200 at its index row carries about 8.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 3.1 8B Instruct, 1 × B200 index row (13.0 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 9.2 |
| Saudi Arabia | 689 | 8.9 |
| Hong Kong | 676 | 8.8 |
| Serbia | 668 | 8.7 |
| World | 473 | 6.1 |
| Germany | 340 | 4.4 |
| Norway | 30 | 0.4 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 3.1 8B Instruct

### How much energy does Llama 3.1 8B Instruct use per million output tokens?

Llama 3.1 8B Instruct uses 13.0 Wh of GPU energy per million output tokens on 1 × B200 and 19.5 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### Is Llama 3.1 8B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.50× the energy per token of the B200 configuration: 19.5 Wh/M on 1 × H100 against 13.0 Wh/M on 1 × B200. Both are floors at high load.

### How much does load change the energy per token of Llama 3.1 8B Instruct?

On 1 × H100, energy per token falls 6.5× between a running batch of 8 (126.3 Wh/M) and 511 (19.5 Wh/M), because the cards' power rises only 41 percent while throughput rises 9.2×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 3.1 8B Instruct?

A billion output tokens of Llama 3.1 8B Instruct on 1 × B200 at its index row carries about 8.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 3.1 8B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 20 stable configurations of Llama 3.1 8B Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-3.1-8B-Instruct).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-3-1-8b-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 3.1 8B Instruct on your own grid and load.
