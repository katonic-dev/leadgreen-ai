# United Kingdom: the carbon of AI inference per billion tokens

> About 13.7 kg CO2e per billion LLM output tokens on United Kingdom's grid (216 gCO2e/kWh, 2024, Ember), every index model priced, trend since 2023.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/grids/united-kingdom/ (this file: https://leadgreen.ai/grids/united-kingdom/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Grids](https://leadgreen.ai/grids/) · Europe · a reference grid*

An LLM served on United Kingdom's grid emits about **13.7 kg CO2e per billion output tokens** at the index's reference row (Qwen 3 32B, 2 × H100, 63.5 Wh/M), GPU energy only; the index's lowest row emits 2.8 kg and its highest 124.0 kg. The grid ran at **216 gCO2e per kWh** in 2024 on Ember's yearly figures, 2.2× cleaner than the world average of 473, and 50th of the 193 countries Ember covers, counting from the cleanest. Energy per token does not change with geography; carbon per token does.

**Area** United Kingdom (GBR, GB). **Basis** lifecycle, location-based, annual average. **Data** [grid.json](https://leadgreen.ai/api/v1/grid.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. United Kingdom: carbon of AI inference per billion tokens. https://leadgreen.ai/grids/united-kingdom/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [Trend](https://leadgreen.ai/grids/united-kingdom/#trend)
- [Every model](https://leadgreen.ai/grids/united-kingdom/#models)
- [Reporting](https://leadgreen.ai/grids/united-kingdom/#reporting)
- [Questions](https://leadgreen.ai/grids/united-kingdom/#faq)
- [Sources](https://leadgreen.ai/grids/united-kingdom/#sources)

- **Grid intensity, 2024:** 216 gCO2e/kWh Ember yearly data, lifecycle, location-based. World: 473.
- **Reference row, per billion tokens:** 13.7 kg CO2e Qwen 3 32B, 2 × H100, 63.5 Wh/M, GPU only, a floor.
- **Rank:** 50 of 193 1 is the cleanest grid Ember covers (Ethiopia, 23); 193 the highest (Turkmenistan, 1,306).

Carbon per token is energy per token times the grid. The energy figures here are GPU-only floors from a busy server; a lightly loaded deployment sits above them, and so does anything that includes the host, the network and the cooling. Wh/M × gCO2e per kWh ÷ 1,000 gives kg CO2e per billion output tokens.

*Trend*

## United Kingdom's grid, year by year

From 2023 to 2025 the intensity fell 7 percent, from 235.6 to 218.2 gCO2e per kWh. The table uses 2024, the latest year with a value for every listed grid; on the 2025 figure the reference row would carry 13.8 kg per billion tokens.

*Ember yearly emissions intensity for United Kingdom, and the reference row priced on each year*

| Year | g CO2e per kWh | kg CO2e per billion tokens, reference row |
|---|---|---|
| 2023 | 235.6 | 15.0 |
| 2024 | 216.5 | 13.7 |
| 2025 | 218.2 | 13.8 |

Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. A GPU server draws much the same power around the clock, while an annual average weights each hour by its generation, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average.

*Every model*

## The index priced on United Kingdom's grid

Each model's lowest index row, GPU only, at the most energy-efficient configuration measured, multiplied by 216 gCO2e per kWh. The spread from the lowest row to the highest is 44×, and it is entirely the model, the GPU and the load; the grid multiplies all of them alike.

*Lowest index row per model, priced on United Kingdom, 2024*

| Model | GPUs | Wh / M | kg CO2e per billion output tokens |
|---|---|---|---|
| [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × B200 | 13.0 | 2.8 |
| [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 1 × B200 | 14.7 | 3.2 |
| [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/) | 1 × B200 | 15.2 | 3.3 |
| [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 1 × B200 | 15.7 | 3.4 |
| [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/) | 1 × B200 | 26.5 | 5.7 |
| [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 1 × B200 | 39.1 | 8.5 |
| [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/) | 1 × B200 | 39.4 | 8.5 |
| [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/) | 1 × B200 | 40.9 | 8.9 |
| [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/) | 1 × B200 | 49.1 | 10.6 |
| [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/) | 2 × B200 | 52.4 | 11.3 |
| [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 2 × B200 | 60.7 | 13.1 |
| [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 4 × B200 | 66.7 | 14.4 |
| [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/) | 4 × H100 | 93.4 | 20.2 |
| [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/) | 8 × H100 | 134.5 | 29.1 |
| [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/) | 2 × B200 | 139.1 | 30.1 |
| [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/) | 8 × B200 | 168.4 | 36.5 |
| [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/) | 8 × B200 | 282.0 | 61.0 |
| [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 4 × B200 | 318.5 | 69.0 |

Every configuration of every model, not only the lowest row, is on [the model pages](https://leadgreen.ai/models/); the [MCP server](https://leadgreen.ai/mcp/) prices any of them on United Kingdom's grid for a token count you give it.

*Reporting*

## Which line it goes on

For GPUs you run in United Kingdom, the electricity is your own consumption: it goes into your ESRS E1-5 energy total and its emissions into E1-6 as Scope 2, location-based, which is the method this page's figure matches. The market-based figure nets your contracted supply and needs your own contracts. Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3 category 1, and sit outside your E1-5 line; [the why page](https://leadgreen.ai/why/#hosted) lists what to ask the provider. Ember's figure is a lifecycle intensity for comparing places, not a Scope 2 combustion factor to file as reported.

*Questions*

## Asked about AI carbon in United Kingdom

### What is the grid carbon intensity of United Kingdom?

216 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 2.2× cleaner than the world average of 473. Ember's 2025 figure is 218.2.

### How much CO2 does a million AI tokens produce in United Kingdom?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 13.7 grams of CO2e per million tokens, or 13.7 kg per billion, on United Kingdom's 2024 grid. Across the index the range is 2.8 to 124.0 kg per billion tokens. A lightly loaded server sits above these floors, and host, network and cooling are not counted.

### Is running AI in United Kingdom cleaner than the world average?

United Kingdom's 2024 intensity of 216 gCO2e per kWh is 2.2× cleaner than the world average of 473 (473 gCO2e per kWh). The same tokens on the same GPUs produce the same energy figure anywhere; only the carbon figure moves with the grid.

### Can I use this figure for my Scope 2 report in United Kingdom?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. Tokens bought from a hosted API land in your Scope 3 category 1, not your Scope 2. The why page explains both.

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. Energy per token: the ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026). Carbon is Wh/M × gCO2e per kWh ÷ 1,000.

*Sources*

## Where every figure came from

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, emissions intensity of total generation, 2023, 2024, 2025 (CC BY 4.0), retrieved 17 October 2026. Energy per token: [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

This page is generated from the same dated snapshots as [the index](https://leadgreen.ai/index/#carbon); no figure on it is typed by hand. All 193 areas are in [grid.json](https://leadgreen.ai/api/v1/grid.json); the 22 with a page are the markets Katonic sells in or expects to, plus seven reference grids.
