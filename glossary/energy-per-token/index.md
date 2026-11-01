# Energy per token

> 0.047 to 2.06 joules per output token is the index's range of GPU energy per token; 1 Wh per million tokens equals 0.0036 J per token.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/energy-per-token/ (this file: https://leadgreen.ai/glossary/energy-per-token/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

0.047 to 2.06 joules per output token is the index's range of GPU energy per token; 1 Wh per million tokens equals 0.0036 J per token. **Energy per token** is the GPU energy a serving system uses divided by the output tokens it generated in the same window, in joules per output token. The ML.ENERGY Leaderboard v3.0 measures it as steady-state GPU energy divided by the output tokens generated in the steady-state window, read from the device with Zeus under vLLM on H100 and B200 servers (data compiled 16 February 2026). On the index it runs from **0.047 J per token** (Llama 3.1 8B Instruct, 1 × B200) to **2.06 J** (Llama 3.1 405B Instruct FP8, 8 × H100); the index shows it as watt-hours per million output tokens.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Energy per token: definition and the figure. https://leadgreen.ai/glossary/energy-per-token/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/energy-per-token/#working)
- [Where it is used](https://leadgreen.ai/glossary/energy-per-token/#used)
- [Questions](https://leadgreen.ai/glossary/energy-per-token/#faq)
- [Sources](https://leadgreen.ai/glossary/energy-per-token/#sources)

*The working*

## How the term is used on the index

Energy per token is average power divided by token throughput: on the reference row, 1,177.9 W summed across 2 cards ÷ 5,155.5 output tokens per second = 0.2285 J per token, which is 63.47 Wh/M. The identity is also the consistency check the [RFP scoring box](https://leadgreen.ai/rfp/) applies to a bidder's figure.

Three ways of getting the number are not equal. A measured figure reads the GPU's energy counter (NVIDIA NVML or DCGM, which Zeus uses) over a window of steady load and divides by the tokens served. A whole-system figure reads the server's power supplies and includes host, memory, network and fans, which on a DGX B200 adds about 1.79× to the GPU figure. An estimate multiplies a rated power (TDP) by an assumed utilisation and divides by an assumed throughput; it is the kind most often quoted and the kind the index does not publish. Energy per token falls as the running batch rises because the cards' fixed draw is spread over more tokens: see [running batch](https://leadgreen.ai/glossary/running-batch/).

*Where it is used*

## Pages that rely on this term

- [The index method](https://leadgreen.ai/index/#method)
- [Why it matters: utilisation](https://leadgreen.ai/why/#utilisation)
- [The measurement protocol](https://leadgreen.ai/contribute/#protocol)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What is energy per token?

GPU energy divided by the output tokens generated in the same steady-state window, in joules per output token. The index measures it from the ML.ENERGY Leaderboard v3.0 and shows it as watt-hours per million output tokens; it runs from 0.047 to 2.06 J per token across the index rows.

### How is energy per token measured?

By reading the GPU's energy counter (through NVML or DCGM; the leaderboard uses Zeus) at the start and end of a steady-state window under a fixed load, and dividing the difference by the output tokens generated in that window. The index's protocol asks for a window of at least 5 minutes after warm-up and at least 1,000 requests. Average power divided by tokens per second gives the same number.

### Why do estimates of energy per token differ so much from measurements?

Estimates multiply a rated power by an assumed utilisation and divide by an assumed throughput, usually a single request at a time. A busy server serves hundreds of requests at once on nearly the same power: Qwen 3 32B on 2 × H100 moves 7.1× in energy per token between a running batch of 8 and 256. An estimate at one request per card lands far above every measured busy-server row.

### Does energy per token include the host, the network and cooling?

Not on this index. The figures are GPU energy only. A whole-system reading adds the host, memory, network and fans (about 1.79× for a DGX B200, from NVIDIA's rated system and GPU power), and the facility's PUE adds cooling and distribution on top.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
