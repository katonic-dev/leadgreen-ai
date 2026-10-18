# Llama 3.3 70B Instruct vs Llama 3.1 405B Instruct FP8: GPU energy per million output tokens

> Llama 3.1 405B Instruct FP8 against Llama 3.3 70B Instruct on GPU energy per output token: 4.88× on the H100 and 5.25× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/ (this file: https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two sizes · H100 and B200*

On the index rows, Llama 3.1 405B Instruct FP8 uses **4.88×** the GPU energy per output token of Llama 3.3 70B Instruct on the H100 (572.9 against 117.5 Wh/M, on eight cards and four cards at running batches of 255 and 724) and **5.25×** on the B200 (318.5 against 60.7 Wh/M, on four cards and two cards at running batches of 510 and 1,022), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Llama 3.3 70B Instruct has 70 B parameters; Llama 3.1 405B Instruct FP8 has 405 B parameters. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [llama-3-3-70b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-3-70b-instruct.json), [llama-3-1-405b-instruct-fp8.json](https://leadgreen.ai/api/v1/models/llama-3-1-405b-instruct-fp8.json). Updated 18 October 2026.

Cite this page: Lead Green, a Katonic project. Llama 3.3 70B Instruct vs Llama 3.1 405B Instruct FP8: GPU energy per million output tokens. https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/, release 2026-10-18, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#rows)
- [What explains it](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#why)
- [Questions](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)
- [Sources](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#sources)

- **H100, index rows:** 4.88 × Llama 3.1 405B Instruct FP8 572.9 Wh/M on 8 × H100 against Llama 3.3 70B Instruct 117.5 Wh/M on 4 × H100.
- **B200, index rows:** 5.25 × Llama 3.1 405B Instruct FP8 318.5 Wh/M on 4 × B200 against Llama 3.3 70B Instruct 60.7 Wh/M on 2 × B200.
- **Parameters:** 5.8 × Llama 3.1 405B Instruct FP8 405 B parameters; Llama 3.3 70B Instruct 70 B parameters.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Llama 3.3 70B Instruct and Llama 3.1 405B Instruct FP8, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| H100 | [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 4 × H100 | BF16 | 724 | 2,546 | 6,018 | 117.5 | 413 | 0.049 | 55.6 |
| H100 | [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 8 × H100 | FP8 | 255 | 4,875 | 2,363 | 572.9 | 367 | 0.210 | 271.0 |
| B200 | [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 2 × B200 | BF16 | 1,022 | 1,935 | 8,854 | 60.7 | 409 | 0.025 | 28.7 |
| B200 | [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 4 × B200 | FP8 | 510 | 3,883 | 3,386 | 318.5 | 380 | 0.121 | 150.7 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two sizes

The second model has 5.8× the parameters of the first, and a dense model reads every parameter for every output token, so the weights moved per token scale with size and so does the memory needed to hold them. On the H100 the rows sit on four cards (Llama 3.3 70B Instruct) and eight cards (Llama 3.1 405B Instruct FP8), at running batches of 724 (Llama 3.3 70B Instruct) and 255 (Llama 3.1 405B Instruct FP8). The energy gap on the H100 (4.88×) is smaller than the parameter gap (5.8×), because each row runs at its own card count and running batch, where its fixed draw is spread over its own number of tokens. Size is the largest lever after load; the question for a buyer is whether the task needs the larger model's answers.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Llama 3.3 70B Instruct against Llama 3.1 405B Instruct FP8

### Is Llama 3.3 70B Instruct more energy-efficient than Llama 3.1 405B Instruct FP8?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 405B Instruct FP8 uses 4.88× the GPU energy per output token of Llama 3.3 70B Instruct on the H100 (572.9 against 117.5 Wh per million output tokens) and 5.25× the GPU energy per output token of Llama 3.3 70B Instruct on the B200 (318.5 against 60.7 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Llama 3.1 405B Instruct FP8 use per million tokens than Llama 3.3 70B Instruct?

The index rows differ by 455.4 Wh/M on the H100 (455.4 kWh per billion tokens) and 257.8 Wh/M on the B200 (257.8 kWh per billion tokens). Per answer, at each row's own average output length, Llama 3.3 70B Instruct costs 0.049 Wh on the H100 and 0.025 Wh on the B200 and Llama 3.1 405B Instruct FP8 0.210 Wh on the H100 and 0.121 Wh on the B200.

### Does the bigger model cost more per answer?

Yes, at these rows: on the H100, 0.049 Wh for Llama 3.3 70B Instruct against 0.210 Wh for Llama 3.1 405B Instruct FP8, using each row's own average output length (413 and 367 tokens). The larger model also needs more cards to hold its weights (4 against 8 on the H100). Whether its answers are worth the difference is a question about the task, not the index.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the H100 the rows here ran on 4 and 8 cards at running batches of 724 and 255. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
