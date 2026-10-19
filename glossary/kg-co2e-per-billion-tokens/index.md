# kg CO2e per billion output tokens

> The carbon unit of the index: energy per million tokens multiplied by the grid's carbon intensity, which gives kilograms of CO2e per billion output tokens.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/ (this file: https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

**Kilograms of CO2e per billion output tokens** is the carbon unit of the index. It is watt-hours per million output tokens multiplied by the grid's grams of CO2e per kilowatt-hour, divided by 1,000: Wh/M × gCO2e/kWh ÷ 1,000 = kg CO2e per billion tokens, which is also grams of CO2e per million tokens. On the reference row, Qwen 3 32B on 2 × H100 at 63.5 Wh/M, a billion output tokens carries about **43.7 kg CO2e** on Saudi Arabia's 2024 grid (689 gCO2e/kWh, Ember), **44.9 kg** on India's (707), 30.0 kg on the world average (473) and 1.9 kg on Norway's (30). GPU energy only.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. kg CO2e per billion output tokens: definition and the figure. https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#working)
- [Where it is used](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#used)
- [Questions](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#faq)
- [Sources](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#sources)

- **Saudi Arabia:** 43.7 kg / bn tokens Reference row × 689 gCO2e/kWh, 2024
- **India:** 44.9 kg / bn tokens Reference row × 707 gCO2e/kWh
- **Norway:** 1.9 kg / bn tokens Reference row × 30 gCO2e/kWh

*The working*

## How the term is used on the index

The arithmetic as printed: 63.5 × 689 ÷ 1,000 = 43.7. Across the index the range on Saudi Arabia's grid is 8.9 kg (Llama 3.1 8B Instruct, 1 × B200) to 394.8 kg (Llama 3.1 405B Instruct FP8, 8 × H100) per billion tokens. Per million tokens, read the same numbers in grams: about 43.7 g for the reference row in Saudi Arabia.

The unit is a floor on two counts: the energy is a busy-server GPU-only figure and the grid factor is a location-based annual average. A lightly loaded server multiplies the first factor by several times (7.1× on the reference model's own ladder), and host, network and cooling add to it. Figures per billion are chosen because enterprise token volumes are counted in billions a month; the [grid pages](https://leadgreen.ai/grids/) price every index row on each listed grid, and the [MCP server](https://leadgreen.ai/mcp/) prices any configuration on any grid for a token count.

*Where it is used*

## Pages that rely on this term

- [The carbon table](https://leadgreen.ai/index/#carbon)
- [Grids](https://leadgreen.ai/grids/)
- [Why it matters: the SCI](https://leadgreen.ai/why/#sci)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### How much CO2 does a million AI tokens produce?

On the index's reference row (Qwen 3 32B, 2 × H100, 63.5 Wh per million output tokens, GPU only), about 43.7 g CO2e per million tokens on Saudi Arabia's 2024 grid, 44.9 g on India's, 30.0 g on the world average and 1.9 g on Norway's. Per billion tokens, the same numbers in kilograms.

### How do I calculate kg CO2e per billion tokens?

Multiply watt-hours per million output tokens by the grid's gCO2e per kWh and divide by 1,000. Example: 63.5 Wh/M × 689 gCO2e/kWh ÷ 1,000 = 43.7 kg CO2e per billion tokens.

### Why are some published figures thousands of times higher?

Usually because they start from an estimate of energy per token for a single request at a time, or from a whole-stack figure, and then multiply by a grid factor. The index's energy figures are measured on a busy server, GPU only; at the same grid factor they land far lower. State the boundary and the load before comparing two carbon figures.

### Is this a Scope 2 figure?

It is a location-based GPU-side figure for comparison. GPUs you run put their electricity in your own Scope 2 (ESRS E1-6, location-based matches this method; market-based needs your contracts). Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3, category 1.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
