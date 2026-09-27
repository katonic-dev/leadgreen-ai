# Llama 4 Scout 17B 16E Instruct: GPU energy per million output tokens

> Llama 4 Scout 17B 16E Instruct: GPU watt-hours per million output tokens at every measured load, with carbon by grid. ML.ENERGY v3.0 data.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/ (this file: https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · H100*

Llama 4 Scout 17B 16E Instruct serves a million output tokens for **93.4 Wh/M** on 4 × H100 (running batch 473, median inter-token latency 69 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [meta-llama/Llama-4-Scout-17B-16E-Instruct](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct), a mixture-of-experts model (17 B of 109 B parameters active per token), weights in BF16. **Measured** 20 configurations on H100. **Data** [models/llama-4-scout-17b-16e-instruct.json](https://leadgreen.ai/api/v1/models/llama-4-scout-17b-16e-instruct.json). Updated 27 September 2026.

- [Every configuration](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#configurations)
- [Carbon](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#carbon)
- [Questions](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)
- [Sources](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#sources)

- **Index row, H100:** 93.4 Wh/M 4 × H100, BF16. Running batch 473, median ITL 69 ms, 1,881 W across the cards, 5,596 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 4 Scout 17B 16E Instruct at every measured load

On 4 × H100, Llama 4 Scout 17B 16E Instruct runs from **1,104.8 Wh/M** at a running batch of 8 to **93.4 Wh/M** at 473, a fall of 11.8×, while the cards' draw rises 47 percent (from 1,281 to 1,881 W) and throughput rises 17.4× (from 322 to 5,596 tokens a second). Median inter-token latency stays at 69 ms or under up to the best row.

*Llama 4 Scout 17B 16E Instruct, BF16, 4 × H100: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,104.8 | 24 | 322 | 1,281 |
| 16 | 16 | 742.6 | 29 | 532 | 1,423 |
| 32 | 32 | 480.3 | 33 | 929 | 1,606 |
| 64 | 64 | 294.3 | 36 | 1,652 | 1,750 |
| 96 | 96 | 220.5 | 39 | 2,292 | 1,819 |
| 128 | 128 | 181.7 | 42 | 2,806 | 1,835 |
| 192 | 192 | 143.4 | 48 | 3,615 | 1,867 |
| 256 | 255 | 120.7 | 52 | 4,325 | 1,879 |
| 384 | 383 | 99.7 | 65 | 5,191 | 1,863 |
| 512 | 473 | 93.4 | 69 | 5,596 | 1,881 |

*Llama 4 Scout 17B 16E Instruct, BF16, 8 × H100: ten measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 1,464.8 | 20 | 379 | 2,000 |
| 16 | 16 | 925.3 | 22 | 688 | 2,292 |
| 32 | 32 | 571.9 | 24 | 1,243 | 2,559 |
| 64 | 64 | 350.4 | 26 | 2,218 | 2,797 |
| 96 | 96 | 267.7 | 28 | 3,043 | 2,933 |
| 128 | 128 | 224.4 | 30 | 3,703 | 2,991 |
| 192 | 191 | 179.1 | 34 | 4,846 | 3,125 |
| 256 | 255 | 155.9 | 37 | 5,696 | 3,197 |
| 384 | 383 | 130.6 | 48 | 6,783 | 3,189 |
| 512 | 511 | 125.6 | 56 | 6,853 | 3,098 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 4 Scout 17B 16E Instruct on 4 × H100 at its index row carries about 64.6 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 2.8 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 4 Scout 17B 16E Instruct, 4 × H100 index row (93.4 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 66.0 |
| Saudi Arabia | 692 | 64.6 |
| Hong Kong | 676 | 63.1 |
| Serbia | 668 | 62.4 |
| World | 474 | 44.2 |
| Germany | 340 | 31.7 |
| Norway | 30 | 2.8 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 4 Scout 17B 16E Instruct

### How much energy does Llama 4 Scout 17B 16E Instruct use per million output tokens?

Llama 4 Scout 17B 16E Instruct uses 93.4 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### How much does load change the energy per token of Llama 4 Scout 17B 16E Instruct?

On 4 × H100, energy per token falls 11.8× between a running batch of 8 (1,104.8 Wh/M) and 473 (93.4 Wh/M), because the cards' power rises only 47 percent while throughput rises 17.4×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 4 Scout 17B 16E Instruct?

A billion output tokens of Llama 4 Scout 17B 16E Instruct on 4 × H100 at its index row carries about 64.6 kg CO2e of GPU-side emissions on the Saudi grid (692 gCO2e per kWh, Ember 2024) and 2.8 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 4 Scout 17B 16E Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 20 stable configurations of Llama 4 Scout 17B 16E Instruct measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-4-Scout-17B-16E-Instruct).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-4-scout-17b-16e-instruct.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 4 Scout 17B 16E Instruct on your own grid and load.
