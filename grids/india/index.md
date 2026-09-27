# India: the carbon of AI inference per billion tokens

> India's grid at 707 gCO2e/kWh: what a billion AI output tokens cost in CO2e there, every model on the index priced on it, and the trend.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/grids/india/ (this file: https://leadgreen.ai/grids/india/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Grids](https://leadgreen.ai/grids/) · Asia · a market Katonic sells in or expects to*

India's grid ran at 707 gCO2e per kWh in 2024 on Ember's yearly figures, 1.5× the world average of 474, and 181st of the 193 countries Ember covers, counting from the cleanest. A billion output tokens of the index's reference row (Qwen 3 32B, 2 × H100, 63.5 Wh/M) served on it carries about 44.9 kg CO2e of GPU-side emissions; the index's lowest row carries 9.2 kg and its highest 405.1 kg. Energy per token does not change with geography; carbon per token does.

Area India (IND, IN). Basis lifecycle, location-based, annual average. Data [grid.json](https://leadgreen.ai/api/v1/grid.json). Updated 27 September 2026.

- [Trend](https://leadgreen.ai/grids/india/#trend)
- [Every model](https://leadgreen.ai/grids/india/#models)
- [Reporting](https://leadgreen.ai/grids/india/#reporting)
- [Questions](https://leadgreen.ai/grids/india/#faq)
- [Sources](https://leadgreen.ai/grids/india/#sources)

- Grid intensity, 2024: 707 gCO2e/kWh Ember yearly data, lifecycle, location-based. World: 474.
- Reference row, per billion tokens: 44.9 kg CO2e Qwen 3 32B, 2 × H100, 63.5 Wh/M, GPU only, a floor.
- Rank: 181 of 193 1 is the cleanest grid Ember covers (Ethiopia, 23); 193 the highest (Turkmenistan, 1,306).

Carbon per token is energy per token times the grid. The energy figures here are GPU-only floors from a busy server; a lightly loaded deployment sits above them, and so does anything that includes the host, the network and the cooling. Wh/M × gCO2e per kWh ÷ 1,000 gives kg CO2e per billion output tokens.

*Trend*

## India's grid, year by year

From 2023 to 2025 the intensity fell 6 percent, from 714.2 to 670.9 gCO2e per kWh. The table uses 2024, the latest year with a value for every listed grid; on the 2025 figure the reference row would carry 42.6 kg per billion tokens.

*Ember yearly emissions intensity for India, and the reference row priced on each year*

| Year | g CO2e per kWh | kg CO2e per billion tokens, reference row |
|---|---|---|
| 2023 | 714.2 | 45.3 |
| 2024 | 707.1 | 44.9 |
| 2025 | 670.9 | 42.6 |

Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. A GPU server draws much the same power around the clock, while an annual average weights each hour by its generation, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average.

*Every model*

## The index priced on India's grid

Each model's lowest index row, GPU only, at the most energy-efficient configuration measured, multiplied by 707 gCO2e per kWh. The spread from the lowest row to the highest is 44×, and it is entirely the model, the GPU and the load; the grid multiplies all of them alike.

*Lowest index row per model, priced on India, 2024*

| Model | GPUs | Wh / M | kg CO2e per billion output tokens |
|---|---|---|---|
| [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × B200 | 13.0 | 9.2 |
| [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 1 × B200 | 14.7 | 10.4 |
| [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/) | 1 × B200 | 15.2 | 10.8 |
| [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 1 × B200 | 15.7 | 11.1 |
| [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/) | 1 × B200 | 26.5 | 18.7 |
| [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 1 × B200 | 39.1 | 27.6 |
| [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/) | 1 × B200 | 39.4 | 27.9 |
| [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/) | 1 × B200 | 40.9 | 28.9 |
| [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/) | 1 × B200 | 49.1 | 34.7 |
| [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/) | 2 × B200 | 52.4 | 37.1 |
| [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 2 × B200 | 60.7 | 42.9 |
| [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 4 × B200 | 66.7 | 47.2 |
| [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/) | 4 × H100 | 93.4 | 66.0 |
| [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/) | 8 × H100 | 134.5 | 95.1 |
| [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/) | 2 × B200 | 139.1 | 98.3 |
| [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/) | 8 × B200 | 168.4 | 119.1 |
| [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/) | 8 × B200 | 282.0 | 199.4 |
| [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 4 × B200 | 318.5 | 225.2 |

Every configuration of every model, not only the lowest row, is on [the model pages](https://leadgreen.ai/models/); the [MCP server](https://leadgreen.ai/mcp/) prices any of them on India's grid for a token count you give it.

*Reporting*

## Which line it goes on

For GPUs you run in India, the electricity is your own consumption: it goes into your ESRS E1-5 energy total and its emissions into E1-6 as Scope 2, location-based, which is the method this page's figure matches. The market-based figure nets your contracted supply and needs your own contracts. Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3 category 1, and sit outside your E1-5 line; [the why page](https://leadgreen.ai/why/#hosted) lists what to ask the provider. Ember's figure is a lifecycle intensity for comparing places, not a Scope 2 combustion factor to file as reported.

*Questions*

## Asked about AI carbon in India

### What is the grid carbon intensity of India?

707 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.5× the world average of 474. Ember's 2025 figure is 670.9.

### How much CO2 does a million AI tokens produce in India?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 44.9 grams of CO2e per million tokens, or 44.9 kg per billion, on India's 2024 grid. Across the index the range is 9.2 to 405.1 kg per billion tokens. A lightly loaded server sits above these floors, and host, network and cooling are not counted.

### Is running AI in India cleaner than the world average?

India's 2024 intensity of 707 gCO2e per kWh is 1.5× the world average of 474 (474 gCO2e per kWh). The same tokens on the same GPUs produce the same energy figure anywhere; only the carbon figure moves with the grid.

### Can I use this figure for my Scope 2 report in India?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. Tokens bought from a hosted API land in your Scope 3 category 1, not your Scope 2. The why page explains both.

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, September 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 26 September 2026. Energy per token: the ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026). Carbon is Wh/M × gCO2e per kWh ÷ 1,000.

*Sources*

## Where every figure came from

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), September 2026 release, emissions intensity of total generation, 2023, 2024, 2025 (CC BY 4.0), retrieved 26 September 2026. Energy per token: [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Cite as. Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshots as [the index](https://leadgreen.ai/index/#carbon); no figure on it is typed by hand. All 193 areas are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the 22 with a page are the markets Katonic sells in or expects to, plus seven reference grids.
