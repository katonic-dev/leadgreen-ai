# Power usage effectiveness (PUE)

> Total facility energy divided by IT equipment energy, per ISO/IEC 30134-2; the operator's own multiplier that takes a GPU figure to the building's meter.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/pue/ (this file: https://leadgreen.ai/glossary/pue/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

**Power usage effectiveness (PUE)** is a data centre's total facility energy divided by the energy delivered to its IT equipment, as defined in ISO/IEC 30134-2. A PUE of 1.0 would mean no energy for cooling, power distribution or lighting; real sites sit above it, and the figure is the operator's own, measured at the building. The index publishes no PUE. It names it because PUE is the second of two multipliers that take a GPU-only figure to the meter: with a system-to-GPU power ratio of 1.79 (DGX B200) and an illustrative PUE of **1.3**, the reference row's 63.5 Wh/M at the GPU becomes about **148 Wh/M** at the facility meter.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Power usage effectiveness (PUE): definition and the figure. https://leadgreen.ai/glossary/pue/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/pue/#working)
- [Where it is used](https://leadgreen.ai/glossary/pue/#used)
- [Questions](https://leadgreen.ai/glossary/pue/#faq)
- [Sources](https://leadgreen.ai/glossary/pue/#sources)

- **Illustrative PUE:** 1.3  A stated assumption; the operator's figure is the only real one
- **System to GPU:** 1.79 × DGX B200, NVIDIA rated power
- **Reference row at the meter:** 148 Wh/M 63.5 × 1.79 × 1.3

*The working*

## How the term is used on the index

The arithmetic as printed: 63.5 × 1.79 × 1.3 = 148. The order of the two multipliers does not matter; what matters is that both are stated. A contracted feed then becomes a token capacity: at that figure a gigawatt-hour at the meter serves about 6.8 billion output tokens of the reference row, against 15.8 billion per megawatt-hour of GPU energy.

PUE is a facility metric and says nothing about how much useful work the IT equipment did; a site with a PUE of 1.1 serving eight requests per GPU wastes more energy per token than a site at 1.4 serving two hundred and fifty. Under the Energy Efficiency Directive (EU) 2023/1791 and Delegated Regulation (EU) 2024/1364, data centres with an installed IT power demand of at least 500 kW report PUE and other facility indicators to the European database; none of those indicators is energy per unit of work, which is what the [index](https://leadgreen.ai/index/) adds. The [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/) entry draws the line the multipliers cross.

*Where it is used*

## Pages that rely on this term

- [The index method: to the meter](https://leadgreen.ai/index/#method)
- [Why it matters: power](https://leadgreen.ai/why/#power)
- [Why it matters: the regulator](https://leadgreen.ai/why/#regulator)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)

*Questions*

## Asked about this term

### What is PUE?

Power usage effectiveness: a data centre's total facility energy divided by the energy delivered to its IT equipment, per ISO/IEC 30134-2. It is measured by the operator at the building and the index publishes none; it is one of the two multipliers that take a GPU-only energy figure to the meter.

### How do I use PUE with watt-hours per million tokens?

Multiply the GPU figure by the system-to-GPU power ratio and by the PUE. Illustration: 63.5 Wh/M × 1.79 (DGX B200) × 1.3 = about 148 Wh/M at the facility meter. Use your own site's PUE and your own server's ratio.

### Does a low PUE mean efficient AI inference?

No. PUE measures the building's overhead, not the work the GPUs did. A site with a low PUE serving few requests per GPU uses more energy per token than a site with a higher PUE whose GPUs are busy. Energy per token measures the work; PUE measures the building.

### Which regulation asks for PUE?

In the EU, the Energy Efficiency Directive (EU) 2023/1791, Article 12, with Commission Delegated Regulation (EU) 2024/1364: data centres with an installed IT power demand of at least 500 kW report facility indicators including PUE. No regulation asks for energy per token.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
