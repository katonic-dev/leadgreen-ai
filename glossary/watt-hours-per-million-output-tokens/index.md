# Watt-hours per million output tokens (Wh/M)

> The unit of the index: the GPU energy, in watt-hours, that a serving configuration uses to generate one million output tokens.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/ (this file: https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

**Watt-hours per million output tokens (Wh/M)** is the GPU energy, in watt-hours, that a model on a stated set of GPUs at a stated load uses to generate one million output tokens. One Wh/M equals 0.0036 joules per output token (joules per token × 1,000,000 ÷ 3,600 = Wh/M). On the index the unit runs from **13.0 Wh/M** (Llama 3.1 8B Instruct, 1 × B200) to **572.9 Wh/M** (Llama 3.1 405B Instruct FP8, 8 × H100), GPU only, at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for each model and GPU (data compiled 16 February 2026).

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 18 October 2026.

Cite this page: Lead Green, a Katonic project. Watt-hours per million output tokens (Wh/M): definition and the figure. https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/, release 2026-10-18, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#working)
- [Where it is used](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#used)
- [Questions](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#faq)
- [Sources](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#sources)

- **Lowest on the index:** 13.0 Wh/M Llama 3.1 8B Instruct, 1 × B200
- **Reference row:** 63.5 Wh/M Qwen 3 32B, 2 × H100
- **Highest on the index:** 572.9 Wh/M Llama 3.1 405B Instruct FP8, 8 × H100

*The working*

## How the term is used on the index

The same number reads three ways without conversion: Wh per million tokens equals kWh per billion tokens equals MWh per trillion tokens. The reference row, Qwen 3 32B on 2 × H100, is 63.5 Wh/M, so a billion of its tokens take 63.5 kWh of GPU energy and a trillion take 63.5 MWh. Multiply by the grid's gCO2e per kWh and divide by 1,000 for kg CO2e per billion tokens: 63.5 × 689 ÷ 1,000 = 43.7 kg on Saudi Arabia's 2024 grid.

The unit is chosen over joules per token because procurement, capacity planning and sustainability reporting all work in watt-hours and tokens, and over watt-hours per query because a query has no fixed length. It is an output-token unit: prompt processing is included in the energy but the prompt's tokens are not in the denominator, which is how the leaderboard measures it. It says nothing about the host, the network, cooling or idle time; see the [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/).

*Where it is used*

## Pages that rely on this term

- [The index](https://leadgreen.ai/index/)
- [Every model page](https://leadgreen.ai/models/)
- [How much energy does an AI query use?](https://leadgreen.ai/per-query/)

Other terms:

- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What does Wh/M mean?

Watt-hours per million output tokens: the GPU energy a serving configuration uses to generate a million output tokens. One Wh/M is 0.0036 joules per token. The index runs from 13.0 to 572.9 Wh/M across 32 rows and 18 models, GPU only, each row the lowest-energy configuration measured at or under a 500 ms median inter-token latency.

### How do I convert joules per token to watt-hours per million tokens?

Multiply joules per token by 1,000,000 and divide by 3,600. The reference row's 0.2285 J per token becomes 63.5 Wh/M. The reverse is Wh/M × 0.0036 = J per token.

### Is Wh per million tokens the same as kWh per billion tokens?

Yes, and the same as MWh per trillion tokens; the three scale together. 63.5 Wh/M is 63.5 kWh per billion and 63.5 MWh per trillion output tokens.

### Does the unit include the prompt?

The energy includes prompt processing, because the benchmark divides steady-state GPU energy by the output tokens generated in the window; the denominator counts output tokens only. A long-prompt workload therefore shows a higher Wh/M than a short-prompt one for the same answers.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
