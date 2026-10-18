# Qwen 3 32B vs Llama 3.3 70B Instruct: GPU energy per million output tokens

> Llama 3.3 70B Instruct against Qwen 3 32B on GPU energy per output token: 1.85× on the H100 and 1.55× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/ (this file: https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two families, two sizes · H100 and B200*

On the index rows, Llama 3.3 70B Instruct uses **1.85×** the GPU energy per output token of Qwen 3 32B on the H100 (117.5 against 63.5 Wh/M, on four cards and two cards at running batches of 724 and 256) and **1.55×** on the B200 (60.7 against 39.1 Wh/M, on two cards and one card at running batches of 1,022 and 383), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Qwen 3 32B has 32 B parameters; Llama 3.3 70B Instruct has 70 B parameters. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [qwen-3-32b.json](https://leadgreen.ai/api/v1/models/qwen-3-32b.json), [llama-3-3-70b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-3-70b-instruct.json). Updated 18 October 2026.

Cite this page: Lead Green, a Katonic project. Qwen 3 32B vs Llama 3.3 70B Instruct: GPU energy per million output tokens. https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/, release 2026-10-18, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#rows)
- [What explains it](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#why)
- [Questions](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)
- [Sources](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#sources)

- **H100, index rows:** 1.85 × Llama 3.3 70B Instruct 117.5 Wh/M on 4 × H100 against Qwen 3 32B 63.5 Wh/M on 2 × H100.
- **B200, index rows:** 1.55 × Llama 3.3 70B Instruct 60.7 Wh/M on 2 × B200 against Qwen 3 32B 39.1 Wh/M on 1 × B200.
- **Parameters:** 2.2 × Llama 3.3 70B Instruct 70 B parameters; Qwen 3 32B 32 B parameters.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Qwen 3 32B and Llama 3.3 70B Instruct, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| H100 | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 2 × H100 | BF16 | 256 | 1,178 | 5,155 | 63.5 | 634 | 0.040 | 30.0 |
| H100 | [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 4 × H100 | BF16 | 724 | 2,546 | 6,018 | 117.5 | 413 | 0.049 | 55.6 |
| B200 | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 1 × B200 | BF16 | 383 | 972 | 6,912 | 39.1 | 635 | 0.025 | 18.5 |
| B200 | [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 2 × B200 | BF16 | 1,022 | 1,935 | 8,854 | 60.7 | 409 | 0.025 | 28.7 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two families, two sizes

Two families and two sizes: Qwen 3 32B (32 B parameters, Dense Transformer) against Llama 3.3 70B Instruct (70 B parameters, Dense Transformer), 2.2× the parameters. On the H100 the rows sit on two cards (Qwen 3 32B) and four cards (Llama 3.3 70B Instruct), at running batches of 256 (Qwen 3 32B) and 724 (Llama 3.3 70B Instruct). The energy gap on the H100 (1.85×) is smaller than the parameter gap (2.2×); architecture, vocabulary and the configuration each model was swept at account for the rest. Qwen 3 32B is the index's reference model, so its full ladder of measured loads is on [the index](https://leadgreen.ai/index/#concurrency), and both models' every configuration is on their pages.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Qwen 3 32B against Llama 3.3 70B Instruct

### Is Qwen 3 32B more energy-efficient than Llama 3.3 70B Instruct?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.3 70B Instruct uses 1.85× the GPU energy per output token of Qwen 3 32B on the H100 (117.5 against 63.5 Wh per million output tokens) and 1.55× the GPU energy per output token of Qwen 3 32B on the B200 (60.7 against 39.1 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Llama 3.3 70B Instruct use per million tokens than Qwen 3 32B?

The index rows differ by 54.1 Wh/M on the H100 (54.1 kWh per billion tokens) and 21.7 Wh/M on the B200 (21.7 kWh per billion tokens). Per answer, at each row's own average output length, Qwen 3 32B costs 0.040 Wh on the H100 and 0.025 Wh on the B200 and Llama 3.3 70B Instruct 0.049 Wh on the H100 and 0.025 Wh on the B200.

### Does Llama 3.3 70B Instruct cost more per answer than Qwen 3 32B?

At these rows, on the H100: 0.040 Wh for Qwen 3 32B against 0.049 Wh for Llama 3.3 70B Instruct, using each row's own average output length (634 and 413 tokens). The two differ in family and in size (2.2× the parameters), and the rows differ in cards (2 against 4) and running batch, so the per-answer figure is a reading, not a verdict on either architecture.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the H100 the rows here ran on 2 and 4 cards at running batches of 256 and 724. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
