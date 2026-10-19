# Qwen 3 30B A3B Instruct vs Qwen 3 32B: GPU energy per million output tokens

> Qwen 3 32B against Qwen 3 30B A3B Instruct on GPU energy per output token: 2.57× on the H100 and 2.49× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/ (this file: https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Dense against mixture of experts · H100 and B200*

On the index rows, Qwen 3 32B uses **2.57×** the GPU energy per output token of Qwen 3 30B A3B Instruct on the H100 (63.5 against 24.7 Wh/M, both on two cards at running batches of 256 and 1,019) and **2.49×** on the B200 (39.1 against 15.7 Wh/M, both on one card at running batches of 383 and 1,023), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Qwen 3 30B A3B Instruct has 30 B parameters, 3 B active per token; Qwen 3 32B has 32 B parameters. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [qwen-3-30b-a3b-instruct.json](https://leadgreen.ai/api/v1/models/qwen-3-30b-a3b-instruct.json), [qwen-3-32b.json](https://leadgreen.ai/api/v1/models/qwen-3-32b.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Qwen 3 30B A3B Instruct vs Qwen 3 32B: GPU energy per million output tokens. https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#rows)
- [What explains it](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#why)
- [Questions](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)
- [Sources](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#sources)

- **H100, index rows:** 2.57 × Qwen 3 32B 63.5 Wh/M on 2 × H100 against Qwen 3 30B A3B Instruct 24.7 Wh/M on 2 × H100.
- **B200, index rows:** 2.49 × Qwen 3 32B 39.1 Wh/M on 1 × B200 against Qwen 3 30B A3B Instruct 15.7 Wh/M on 1 × B200.
- **Parameters:** 1.1 × Qwen 3 32B 32 B parameters; Qwen 3 30B A3B Instruct 30 B parameters, 3 B active per token.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Qwen 3 30B A3B Instruct and Qwen 3 32B, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| H100 | [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 2 × H100 | BF16 | 1,019 | 1,123 | 12,640 | 24.7 | 920 | 0.023 | 11.7 |
| H100 | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 2 × H100 | BF16 | 256 | 1,178 | 5,155 | 63.5 | 634 | 0.040 | 30.0 |
| B200 | [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 1 × B200 | BF16 | 1,023 | 601 | 10,648 | 15.7 | 928 | 0.015 | 7.4 |
| B200 | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 1 × B200 | BF16 | 383 | 972 | 6,912 | 39.1 | 635 | 0.025 | 18.5 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Dense against mixture of experts

A dense model reads all of its weights for every output token; a mixture-of-experts model routes each token through a few experts and reads only those. Qwen 3 30B A3B Instruct activates 3 B of its 30 B parameters per token; Qwen 3 32B is dense at 32 B. So the mixture-of-experts model reads about 11× fewer weights per token at a similar total size, and on the H100 its index row uses 0.39× less GPU energy per output token (24.7 against 63.5 Wh/M). The whole model must still fit in memory: On the H100 both rows sit on two cards, at running batches of 1,019 (Qwen 3 30B A3B Instruct) and 256 (Qwen 3 32B). The saving is in weights read per token, not in cards.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Qwen 3 30B A3B Instruct against Qwen 3 32B

### Is Qwen 3 30B A3B Instruct more energy-efficient than Qwen 3 32B?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Qwen 3 32B uses 2.57× the GPU energy per output token of Qwen 3 30B A3B Instruct on the H100 (63.5 against 24.7 Wh per million output tokens) and 2.49× the GPU energy per output token of Qwen 3 30B A3B Instruct on the B200 (39.1 against 15.7 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Qwen 3 32B use per million tokens than Qwen 3 30B A3B Instruct?

The index rows differ by 38.8 Wh/M on the H100 (38.8 kWh per billion tokens) and 23.4 Wh/M on the B200 (23.4 kWh per billion tokens). Per answer, at each row's own average output length, Qwen 3 30B A3B Instruct costs 0.023 Wh on the H100 and 0.015 Wh on the B200 and Qwen 3 32B 0.040 Wh on the H100 and 0.025 Wh on the B200.

### Does a mixture-of-experts model use less energy per token than a dense one?

At a similar total size, on these rows, yes: Qwen 3 30B A3B Instruct activates 3 B of 30 B parameters per token and its H100 index row uses 24.7 Wh/M against 63.5 for the dense Qwen 3 32B (32 B), 0.39× less. The mixture-of-experts model reads about 11× fewer weights per token; it still needs memory for all of them, so the saving is in energy per token, not in cards.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the H100 the rows here ran on 2 and 2 cards at running batches of 1,019 and 256. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
