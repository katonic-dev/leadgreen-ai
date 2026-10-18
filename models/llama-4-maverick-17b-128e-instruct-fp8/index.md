# Llama 4 Maverick 17B 128E Instruct FP8: GPU energy per million output tokens

> Llama 4 Maverick 17B 128E Instruct FP8: GPU watt-hours per million output tokens at every measured load, with carbon by grid. ML.ENERGY v3.0 data.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/ (this file: https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Models](https://leadgreen.ai/models/) · H100*

Llama 4 Maverick 17B 128E Instruct FP8 serves a million output tokens for **134.5 Wh/M** on 8 × H100 (running batch 383, median inter-token latency 48 ms), GPU energy only, at the most energy-efficient configuration the ML.ENERGY Leaderboard measured. That is the floor: a lightly loaded server sits above it.

**Model** [meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8), a mixture-of-experts model (17 B of 400 B parameters active per token), weights in FP8. **Measured** 9 configurations on H100. **Data** [models/llama-4-maverick-17b-128e-instruct-fp8.json](https://leadgreen.ai/api/v1/models/llama-4-maverick-17b-128e-instruct-fp8.json). Updated 18 October 2026.

- [Every configuration](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#configurations)
- [Carbon](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#carbon)
- [Questions](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)
- [Sources](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#sources)

- **Index row, H100:** 134.5 Wh/M 8 × H100, FP8. Running batch 383, median ITL 48 ms, 3,462 W across the cards, 7,149 tokens a second.

GPU only, busy server. Every row is a floor. The number a buyer should ask for is the one measured on their own server at their own load. Unit: watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token.

*Every configuration*

## Llama 4 Maverick 17B 128E Instruct FP8 at every measured load

On 8 × H100, Llama 4 Maverick 17B 128E Instruct FP8 runs from **779.0 Wh/M** at a running batch of 8 to **134.5 Wh/M** at 383, a fall of 5.8×, while the cards' draw rises 88 percent (from 1,845 to 3,462 W) and throughput rises 10.9× (from 658 to 7,149 tokens a second). Median inter-token latency stays at 48 ms or under up to the best row.

*Llama 4 Maverick 17B 128E Instruct FP8, FP8, 8 × H100: nine measured configurations*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 779.0 | 11 | 658 | 1,845 |
| 16 | 16 | 504.4 | 13 | 1,110 | 2,015 |
| 32 | 32 | 351.5 | 16 | 1,805 | 2,284 |
| 64 | 64 | 262.2 | 21 | 2,813 | 2,656 |
| 96 | 96 | 235.8 | 25 | 3,546 | 3,010 |
| 128 | 128 | 210.4 | 28 | 4,147 | 3,141 |
| 192 | 192 | 178.2 | 33 | 5,210 | 3,343 |
| 256 | 255 | 155.7 | 37 | 6,258 | 3,507 |
| 384 | 383 | 134.5 | 48 | 7,149 | 3,462 |

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted. The highlighted row is the index row for that GPU. Wh/M is derived from the source's joules per output token; prompt processing is included.

*Carbon*

## Same tokens, different grid

A billion output tokens of Llama 4 Maverick 17B 128E Instruct FP8 on 8 × H100 at its index row carries about 92.7 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.0 kg on the Norwegian grid (30). Energy per token does not change with geography; carbon per token does.

*Llama 4 Maverick 17B 128E Instruct FP8, 8 × H100 index row (134.5 Wh/M), priced on 2024 annual grid averages, location-based*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 95.1 |
| Saudi Arabia | 689 | 92.7 |
| Hong Kong | 676 | 90.9 |
| Serbia | 668 | 89.9 |
| World | 473 | 63.6 |
| Germany | 340 | 45.7 |
| Norway | 30 | 4.0 |

Wh/M × gCO2e per kWh ÷ 1,000. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. All 193 grids are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the [MCP server](https://leadgreen.ai/mcp/) prices any model on any grid.

*Questions*

## Asked about Llama 4 Maverick 17B 128E Instruct FP8

### How much energy does Llama 4 Maverick 17B 128E Instruct FP8 use per million output tokens?

Llama 4 Maverick 17B 128E Instruct FP8 uses 134.5 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). Host, network, cooling and idle time are not counted, so it is a floor.

### How much does load change the energy per token of Llama 4 Maverick 17B 128E Instruct FP8?

On 8 × H100, energy per token falls 5.8× between a running batch of 8 (779.0 Wh/M) and 383 (134.5 Wh/M), because the cards' power rises only 88 percent while throughput rises 10.9×. A server holding a handful of requests at a time sits at the top of that range.

### What is the carbon footprint of a billion tokens of Llama 4 Maverick 17B 128E Instruct FP8?

A billion output tokens of Llama 4 Maverick 17B 128E Instruct FP8 on 8 × H100 at its index row carries about 92.7 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.0 kg on the Norwegian grid (30). Multiply the Wh/M figure by your own grid's intensity and divide by 1,000 for kilograms per billion tokens.

### Is this the energy my Llama 4 Maverick 17B 128E Instruct FP8 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. Your deployment sits above it, often several times above it; the configuration table shows how far. To get your own figure, follow the measurement protocol on the contribute page.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 9 stable configurations of Llama 4 Maverick 17B 128E Instruct FP8 measured with Zeus under vLLM on H100 80GB and B200 servers. Grid intensities are Ember's 2024 yearly figures. Lead Green recomputes every number from dated snapshots.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024 (CC BY 4.0). Model card: [Hugging Face](https://huggingface.co/meta-llama/Llama-4-Maverick-17B-128E-Instruct-FP8).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshot as [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/v1/models/llama-4-maverick-17b-128e-instruct-fp8.json); no figure on it is typed by hand. Ask the [MCP server](https://leadgreen.ai/mcp/) for Llama 4 Maverick 17B 128E Instruct FP8 on your own grid and load.
