# Floor

> Every index row is a floor: Qwen 3 32B on 2 × H100 is 63.5 Wh per million tokens at a running batch of 256, and a real deployment sits above it.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/floor/ (this file: https://leadgreen.ai/glossary/floor/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

Every index row is a floor: Qwen 3 32B on 2 × H100 is 63.5 Wh per million tokens at a running batch of 256, and a real deployment sits above it. **A floor** is what every row on the index is: the lowest GPU energy per output token the ML.ENERGY Leaderboard v3.0 measured for a model on a GPU, among configurations whose median inter-token latency is at or under 500 ms, at high concurrency on a busy server (data compiled 16 February 2026). A real deployment sits above its floor, often far above it: the reference row, Qwen 3 32B on 2 × H100, is **63.5 Wh/M** at a running batch of 256, and the same model on the same cards measured **452 Wh/M** at a running batch of 8.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Floor: definition and the figure. https://leadgreen.ai/glossary/floor/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/floor/#working)
- [Where it is used](https://leadgreen.ai/glossary/floor/#used)
- [Questions](https://leadgreen.ai/glossary/floor/#faq)
- [Sources](https://leadgreen.ai/glossary/floor/#sources)

- **Reference floor:** 63.5 Wh/M Qwen 3 32B, 2 × H100, running batch 256
- **Same row, light load:** 452 Wh/M Running batch 8: 7.1× the floor
- **Challenge line:** 10 % below A bidder's figure this far under the floor is asked for its logs

*The working*

## How the term is used on the index

The word is chosen so that the rows are read the right way round. A floor is not a typical figure and not a target; it is the best the benchmark found, and it tells a buyer the lowest number a vendor could honestly report for that model on that GPU. An answer below the floor is the one to question: the [RFP scoring box](https://leadgreen.ai/why/#monday) challenges any figure more than 10 percent under it and asks for the raw power and engine logs.

Floors move with the ceiling that defines them. At 500 ms no measured configuration is excluded; at 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B Instruct FP8 on 8 × H100 at 674.9 Wh/M. None of those tighter ceilings is applied to the index. Above the floors sit every other measured configuration, 328 in all, on the [model pages](https://leadgreen.ai/models/); the highest the leaderboard measured is Llama 3.1 405B Instruct on 8 × B200 at 6,073 Wh/M, holding 8 requests.

*Where it is used*

## Pages that rely on this term

- [The index](https://leadgreen.ai/index/)
- [The index method](https://leadgreen.ai/index/#method)
- [Scoring RFP answers](https://leadgreen.ai/why/#monday)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What does the index mean by a floor?

The lowest GPU energy per output token measured for a model and GPU among configurations at or under a 500 ms median inter-token latency, at high concurrency. Every index row is one. A deployment sits above its floor; Qwen 3 32B on 2 × H100 is 63.5 Wh/M at its floor and 452 Wh/M at a running batch of 8.

### Is the floor what my deployment will use?

No. It is the best measured configuration on a busy server, GPU only. Your figure depends on your running batch, your prompt and answer lengths, your precision and your card count, and sits above the floor; the model pages show how far above at each measured load.

### What should I do with a vendor figure below the floor?

Ask for the measurement: the running batch held, the latency over the window, the method, the tool and the logs. The index's scoring method challenges any answer more than 10 percent below the floor for the same model and GPU; the measurement protocol's own repeat threshold is 5 percent.

### Does the floor change if the latency ceiling changes?

It can. At 500 ms, the leaderboard's default, no measured configuration is excluded. At 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B Instruct FP8 on 8 × H100 at 674.9 Wh/M. The index applies none of them.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
