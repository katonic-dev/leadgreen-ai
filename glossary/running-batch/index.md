# Running batch

> Raising the running batch of Qwen 3 32B on 2 × H100 from 8 to 256 cuts GPU energy from 452.0 to 63.5 Wh per million tokens, 7.1× on the same cards.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/running-batch/ (this file: https://leadgreen.ai/glossary/running-batch/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Glossary](https://leadgreen.ai/glossary/)*

Raising the running batch of Qwen 3 32B on 2 × H100 from 8 to 256 cuts GPU energy from 452.0 to 63.5 Wh per million tokens, 7.1× on the same cards. **Running batch** is the average number of requests a serving engine was actually decoding at the same time over the steady-state window, which vLLM reports as `num_requests_running`. It is not the cap the operator set (vLLM's `max_num_seqs`) and it does not count requests waiting in the queue. On the index, raising the running batch of Qwen 3 32B on 2 × H100 from **8 to 256** cuts energy per token from **452 to 63.5 Wh/M**, 7.1× on the same hardware (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026).

**Data** [index.json](https://leadgreen.ai/api/v1/index.json), [grid.json](https://leadgreen.ai/api/v1/grid.json), [hardware.json](https://leadgreen.ai/api/v1/hardware.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Running batch: definition and the figure. https://leadgreen.ai/glossary/running-batch/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The working](https://leadgreen.ai/glossary/running-batch/#working)
- [Where it is used](https://leadgreen.ai/glossary/running-batch/#used)
- [Questions](https://leadgreen.ai/glossary/running-batch/#faq)
- [Sources](https://leadgreen.ai/glossary/running-batch/#sources)

- **Lightly loaded:** 452 Wh/M Qwen 3 32B, 2 × H100, running batch 8
- **Busy:** 63.5 Wh/M Same model, same cards, running batch 256
- **Same hardware:** 7.1 × Power up 39 percent, throughput up 9.9×

*The working*

## How the term is used on the index

The mechanism is fixed draw spread over more work. Between those two rows the cards' power rises 39 percent, from 850 W to 1,178 W, while output throughput rises 9.9×, from 522 to 5,155 tokens per second. Energy per token is power over throughput, so it falls by nearly the whole throughput gain. Median inter-token latency rises from 15 ms to 44 ms over the same range, far under the 500 ms ceiling.

Running batch, not cap, is the figure to ask a vendor for, because a cap of 256 with eight users is a running batch of eight. The [RFP clause](https://leadgreen.ai/why/#monday) asks for both, and the index's [protocol](https://leadgreen.ai/contribute/#protocol) reports both. The full ladder, 9 configurations, is on [the index](https://leadgreen.ai/index/#concurrency) and the [model's page](https://leadgreen.ai/models/qwen-3-32b/).

*Where it is used*

## Pages that rely on this term

- [The concurrency ladder](https://leadgreen.ai/index/#concurrency)
- [Why it matters: utilisation](https://leadgreen.ai/why/#utilisation)
- [The RFP clause](https://leadgreen.ai/why/#monday)

Other terms:

- [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)
- [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)
- [Floor](https://leadgreen.ai/glossary/floor/)
- [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)
- [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)
- [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)
- [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)
- [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

*Questions*

## Asked about this term

### What is running batch?

The average number of requests a serving engine was decoding at once over the measurement window (vLLM's num_requests_running). It is not the configured cap and it excludes queued requests. The index reports it on every row because it is the variable that moves energy per token most: 7.1× for Qwen 3 32B on 2 × H100 between 8 and 256.

### Why does an idle GPU use more energy per token than a busy one?

Because a GPU's power does not fall in step with its work. On the index, Qwen 3 32B on 2 × H100 draws 850 W serving 8 requests at once and 1,178 W serving 256, 39 percent more power for 9.9× the tokens per second. Energy per token is power over throughput, so the lightly loaded server uses 7.1× the energy per token: 452 against 63.5 Wh/M. A fully idle GPU produces no tokens, so its energy per token is undefined, and its draw is pure overhead.

### What is the difference between running batch and batch size?

Batch size is usually a configured limit (the cap, vLLM's max_num_seqs) or a fixed count in an offline benchmark. Running batch is what the server actually held on average under a live load, which is lower whenever demand is below the cap. The AI Energy Score's batch size of one is a fixed count; the index's running batch is a measurement.

### What running batch should I ask a vendor to measure at?

The one you expect in production, stated as a number, with the median and p99 inter-token latency your users will accept. The same running batch and latency limit for every bidder makes the figures comparable; the index's rows give the floor to hold each answer against.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Grid intensity: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, 2024, CC BY 4.0, retrieved 17 October 2026. Hardware: NVIDIA product specifications and the HGX B200 product carbon footprint summary (July 2025), retrieved 26 September 2026. Per-prompt figures: Google, [arXiv 2508.15734](https://arxiv.org/abs/2508.15734) (August 2025); Mistral AI, July 2025.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
