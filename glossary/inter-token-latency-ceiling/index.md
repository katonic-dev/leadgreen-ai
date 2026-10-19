# Inter-token latency ceiling

> The latency limit that defines which configurations may be an index row: a median inter-token latency at or under 500 ms, the leaderboard's own default.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/inter-token-latency-ceiling/ (this file: https://leadgreen.ai/glossary/inter-token-latency-ceiling/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

**The inter-token latency ceiling** is the limit that decides which measured configurations may be an index row: the median time between one output token and the next must be at or under **500 ms**, the ML.ENERGY Leaderboard's own default for every LLM task. Each index row is the lowest-energy configuration for its model and GPU under that ceiling. No measured configuration reaches it (the slowest Text Conversation row is 326 ms), so at 500 ms the ceiling excludes nothing; it is stated because any energy figure needs the latency it was measured at.

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Inter-token latency ceiling: definition and the figure. https://leadgreen.ai/glossary/inter-token-latency-ceiling/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#working)
- [Where it is used](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#used)
- [Questions](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#faq)
- [Sources](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#sources)

- **Ceiling:** 500 ms median ITL The leaderboard's default for every LLM task
- **Slowest measured row:** 326 ms Text Conversation; the ceiling excludes nothing at 500 ms
- **Reference row:** 44 ms median p99 148 ms at a running batch of 256

*The working*

## How the term is used on the index

Energy and latency trade against each other through the running batch: more requests in flight means more tokens per joule and a longer wait between each user's tokens. On the reference model's ladder, median inter-token latency rises from 15 ms at a running batch of 8 to 44 ms at 256 while energy per token falls 7.1×. The reference row's p99 is 148 ms.

Tighter ceilings would change rows: at 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B Instruct FP8 on 8 × H100 at 674.9 Wh/M. None of these is applied to the index; they are reported under [Method](https://leadgreen.ai/index/#method) so a reader with a stricter requirement can see what moves. In an RFP, fill the ceiling with the latency your users will accept, state it once and use it for every bidder; the [clause](https://leadgreen.ai/why/#monday) asks for median and p99 over the same window as the energy figure.

*Where it is used*

## Pages that rely on this term

- [The index method](https://leadgreen.ai/index/#method)
- [The concurrency ladder](https://leadgreen.ai/index/#concurrency)
- [The RFP clause](https://leadgreen.ai/why/#monday)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Running batch](https://leadgreen.ai/glossary/running-batch/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What is the inter-token latency ceiling on the index?

A median inter-token latency of at most 500 ms, the ML.ENERGY Leaderboard's default for every LLM task. Each index row is the lowest-energy configuration for its model and GPU at or under it. No measured configuration reaches it, so at this value it excludes nothing.

### What is inter-token latency?

The time between one output token and the next for a single request while the model is generating, usually reported as a median and a p99 over a window. On the reference model's ladder it runs from 15 ms at a running batch of 8 to 44 ms at 256.

### Would a stricter latency limit change the index?

Yes. At 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B Instruct FP8 on 8 × H100 at 674.9 Wh/M. The index applies none of these; they are reported so that a reader with a stricter requirement can see which rows move.

### Why state a latency ceiling with an energy figure at all?

Because energy per token falls as the running batch rises and latency rises with it; a figure without its latency can be made arbitrarily good by loading the server until users wait. The ceiling fixes the trade so that two figures can be compared.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
