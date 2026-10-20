# GPU-only boundary

> The measurement boundary of every index row: energy read from the GPUs alone, with host, network, cooling, idle time and embodied carbon outside it.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/gpu-only-boundary/ (this file: https://leadgreen.ai/glossary/gpu-only-boundary/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

Every index row counts the GPUs alone; in Google's August 2025 disclosure accelerators were 58 percent of a prompt's energy, and the rest sits outside this boundary. **The GPU-only boundary** is the measurement boundary of every index row: energy read from the GPU devices themselves over the steady-state window, with the host CPU and memory, the network and storage, cooling and the rest of the facility, time the GPU spends idle between requests, and the carbon embodied in the hardware all outside it. Google's August 2025 disclosure shows the size of what sits outside: accelerators were **58 percent** of its 0.24 Wh median prompt, and NVIDIA rates a DGX B200 at 14.3 kW against 8.0 kW for its 8 GPUs, a system-to-GPU ratio of **1.79**.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. GPU-only boundary: definition and the figure. https://leadgreen.ai/glossary/gpu-only-boundary/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/gpu-only-boundary/#working)
- [Where it is used](https://leadgreen.ai/glossary/gpu-only-boundary/#used)
- [Questions](https://leadgreen.ai/glossary/gpu-only-boundary/#faq)
- [Sources](https://leadgreen.ai/glossary/gpu-only-boundary/#sources)

- **Accelerator share:** 58 % of Google's 0.24 Wh median prompt, August 2025
- **System to GPU:** 1.79 × DGX B200: 14.3 kW rated against 8.0 kW of GPUs
- **At the meter:** 148 Wh/M Reference row × 1.79 × PUE 1.3; illustration, not a measurement

*The working*

## How the term is used on the index

Two multipliers take a GPU figure to the facility meter, and both belong to the operator. The system-to-GPU power ratio covers the host, memory, network and fans; the site's power usage effectiveness ([PUE](https://leadgreen.ai/glossary/pue/)) covers cooling and distribution. As an illustration, with the DGX B200 ratio of 1.79 and a PUE of 1.3, the reference row's 63.5 Wh/M becomes about 148 Wh/M at the meter, and a gigawatt-hour at the meter serves about 6.8 billion tokens instead of 15.8 billion per megawatt-hour of GPU energy. The PUE is the operator's own figure and the index publishes none.

The boundary is drawn at the GPU because it is the only part a buyer can measure, compare across vendors and hold a vendor to; the rest depends on the site. For scale on embodied carbon, NVIDIA's cradle-to-gate footprint for one HGX B200 baseboard, eight GPUs, is 2,274 kg CO2e. Water is outside the boundary too: the index measures electricity, and the only public per-prompt water figures are Google's 0.26 mL and Mistral's 45 mL per reply.

*Where it is used*

## Pages that rely on this term

- [The index method](https://leadgreen.ai/index/#method)
- [How much energy does an AI query use?](https://leadgreen.ai/per-query/)
- [Why it matters: power](https://leadgreen.ai/why/#power)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What does GPU-only mean on the index?

That the energy was read from the GPU devices alone over a steady-state window. Host, network, storage, cooling, idle time between requests and embodied carbon are not counted. Google's August 2025 figures show accelerators at 58 percent of a prompt's whole-stack energy.

### How do I take a GPU-only figure to the facility meter?

Multiply by the system-to-GPU power ratio (1.79 for a DGX B200: 14.3 kW rated against 8.0 kW of GPUs) and by the site's PUE. With a PUE of 1.3, 63.5 Wh/M at the GPU is about 148 Wh/M at the meter. Both multipliers are the operator's own.

### Why not publish whole-system figures?

Because they cannot be compared across vendors or sites: the host, the fans and the cooling design differ with every server and building, while the GPU figure for a named model on a named card at a stated load can be measured anywhere. The index publishes the comparable part and names the multipliers for the rest.

### Does the boundary include the energy of processing the prompt?

Yes. The benchmark divides steady-state GPU energy, which includes prefill, by the output tokens generated; the prompt's tokens are not in the denominator.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
