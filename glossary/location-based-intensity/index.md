# Location-based grid intensity

> The average carbon intensity of the electricity generated where a GPU runs, in gCO2e per kWh; the factor that turns energy per token into carbon per token.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/location-based-intensity/ (this file: https://leadgreen.ai/glossary/location-based-intensity/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

689 gCO2e per kWh for Saudi Arabia, 707 for India, 30 for Norway and 473 for the world (2024, Ember): the grid factor that turns energy per token into carbon. **Location-based grid intensity** is the average carbon intensity of the electricity generated in the area where a GPU runs, in grams of CO2e per kilowatt-hour, before any contracts, certificates or self-generation are considered. The index uses Ember's yearly figures (October 2026 release, 2024, the latest year with a value for every listed grid): **689 gCO2e per kWh** for Saudi Arabia, 707 for India, 30 for Norway and 473 for the world. It is a lifecycle figure on net generation, production-based, so upstream methane and plant manufacture are in and imports are out.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Location-based grid intensity: definition and the figure. https://leadgreen.ai/glossary/location-based-intensity/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/location-based-intensity/#working)
- [Where it is used](https://leadgreen.ai/glossary/location-based-intensity/#used)
- [Questions](https://leadgreen.ai/glossary/location-based-intensity/#faq)
- [Sources](https://leadgreen.ai/glossary/location-based-intensity/#sources)

- **Saudi Arabia:** 689 gCO2e/kWh Ember, 2024, lifecycle, location-based
- **World:** 473 gCO2e/kWh Ember, 2024
- **Norway:** 30 gCO2e/kWh 23× cleaner than Saudi Arabia for the same tokens

*The working*

## How the term is used on the index

Energy per token does not change with geography; carbon per token does. The reference row's 63.5 Wh/M carries 43.7 kg CO2e per billion tokens on Saudi Arabia's grid and 1.9 kg on Norway's, 23× apart for the same tokens on the same GPUs. Across the 193 grids Ember covers the spread is 55.6×, from Ethiopia at 23.5 to Turkmenistan at 1,306.2 gCO2e per kWh.

Location-based is the method ESRS E1-6 and the GHG Protocol pair with market-based, which uses the supply you contracted (certificates, power purchase agreements) and needs your own figures. Ember's number is for comparing places, not for filing as a Scope 2 combustion factor: a GPU server draws much the same power around the clock while an annual average weights each hour by its generation, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average. One page per listed grid is under [Grids](https://leadgreen.ai/grids/), and every grid is in [grid.json](https://leadgreen.ai/api/v1/grid.json).

*Where it is used*

## Pages that rely on this term

- [Grids](https://leadgreen.ai/grids/)
- [The carbon table](https://leadgreen.ai/index/#carbon)
- [Why it matters: location](https://leadgreen.ai/why/#location)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What is location-based grid carbon intensity?

The average carbon intensity of the electricity generated where the load runs, in gCO2e per kWh, before contracts or certificates. The index uses Ember's yearly figures (October 2026 release, 2024): Saudi Arabia 689, India 707, Norway 30, world 473.

### What is the difference between location-based and market-based?

Location-based uses the average intensity of the grid where the electricity was consumed. Market-based uses the intensity of the supply you contracted, through certificates or power purchase agreements, and needs your own contract data. ESRS E1-6 asks for both; the index can supply only the first.

### How much does location change the carbon of AI inference?

On the reference row, 23× between Saudi Arabia (43.7 kg CO2e per billion tokens) and Norway (1.9 kg), 2024 averages. The energy figure is identical in both places.

### Can I file Ember's figure in my Scope 2 report?

Use it for comparison, not as the filed factor. It is a lifecycle, production-based figure on net generation, not a Scope 2 combustion factor, and it is an annual average that a round-the-clock GPU load does not follow hour by hour.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
