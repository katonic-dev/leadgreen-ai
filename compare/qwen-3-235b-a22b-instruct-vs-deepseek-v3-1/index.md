# Qwen 3 235B A22B Instruct vs DeepSeek V3.1: GPU energy per million output tokens

> DeepSeek V3.1 against Qwen 3 235B A22B Instruct on GPU energy per output token: 2.52× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/ (this file: https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two mixture-of-experts sizes · B200*

On the index rows, DeepSeek V3.1 uses **2.52×** the GPU energy per output token of Qwen 3 235B A22B Instruct on the B200 (168.4 against 66.7 Wh/M, on eight cards and four cards at running batches of 3,008 and 3,765), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Qwen 3 235B A22B Instruct has 235 B parameters, 22 B active per token; DeepSeek V3.1 has 671 B parameters, 37 B active per token. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [qwen-3-235b-a22b-instruct.json](https://leadgreen.ai/api/v1/models/qwen-3-235b-a22b-instruct.json), [deepseek-v3-1.json](https://leadgreen.ai/api/v1/models/deepseek-v3-1.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Qwen 3 235B A22B Instruct vs DeepSeek V3.1: GPU energy per million output tokens. https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#rows)
- [What explains it](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#why)
- [Questions](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)
- [Sources](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#sources)

- **B200, index rows:** 2.52 × DeepSeek V3.1 168.4 Wh/M on 8 × B200 against Qwen 3 235B A22B Instruct 66.7 Wh/M on 4 × B200.
- **Parameters:** 2.9 × DeepSeek V3.1 671 B parameters, 37 B active per token; Qwen 3 235B A22B Instruct 235 B parameters, 22 B active per token.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Qwen 3 235B A22B Instruct and DeepSeek V3.1, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| B200 | [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 4 × B200 | BF16 | 3,765 | 3,196 | 13,303 | 66.7 | 874 | 0.058 | 31.6 |
| B200 | [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/) | 8 × B200 | FP8 | 3,008 | 5,470 | 9,021 | 168.4 | 842 | 0.142 | 79.7 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two mixture-of-experts sizes

Two mixture-of-experts models of different total size: Qwen 3 235B A22B Instruct activates 22 B of 235 B parameters per token, DeepSeek V3.1 37 B of 671 B. Weights read per token scale with the active parameters (1.7× here), memory with the total (2.9×), so the larger model needs more cards to hold its experts and spreads each token's work across them. On the B200 the rows sit on four cards (Qwen 3 235B A22B Instruct) and eight cards (DeepSeek V3.1), at running batches of 3,765 (Qwen 3 235B A22B Instruct) and 3,008 (DeepSeek V3.1). The index row ratio on the B200 is 2.52×, between the active-parameter gap and the total-parameter gap.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Qwen 3 235B A22B Instruct against DeepSeek V3.1

### Is Qwen 3 235B A22B Instruct more energy-efficient than DeepSeek V3.1?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, DeepSeek V3.1 uses 2.52× the GPU energy per output token of Qwen 3 235B A22B Instruct on the B200 (168.4 against 66.7 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does DeepSeek V3.1 use per million tokens than Qwen 3 235B A22B Instruct?

The index rows differ by 101.7 Wh/M on the B200 (101.7 kWh per billion tokens). Per answer, at each row's own average output length, Qwen 3 235B A22B Instruct costs 0.058 Wh on the B200 and DeepSeek V3.1 0.142 Wh on the B200.

### Does the larger mixture-of-experts model cost more energy per token?

On the B200 index rows, yes: DeepSeek V3.1 (37 B active of 671 B) uses 2.52× the GPU energy per output token of Qwen 3 235B A22B Instruct (22 B active of 235 B), 168.4 against 66.7 Wh/M, on 8 and 4 cards at running batches of 3,008 and 3,765. Active parameters set the work per token; total parameters set the cards.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the B200 the rows here ran on 4 and 8 cards at running batches of 3,765 and 3,008. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
