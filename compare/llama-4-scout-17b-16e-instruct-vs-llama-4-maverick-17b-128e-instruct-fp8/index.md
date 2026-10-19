# Llama 4 Scout 17B 16E Instruct vs Llama 4 Maverick 17B 128E Instruct FP8: GPU energy per million output tokens

> Llama 4 Maverick 17B 128E Instruct FP8 against Llama 4 Scout 17B 16E Instruct on GPU energy per output token: 1.44× on the H100, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/ (this file: https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two expert counts · H100*

On the index rows, Llama 4 Maverick 17B 128E Instruct FP8 uses **1.44×** the GPU energy per output token of Llama 4 Scout 17B 16E Instruct on the H100 (134.5 against 93.4 Wh/M, on eight cards and four cards at running batches of 383 and 473), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Llama 4 Scout 17B 16E Instruct has 109 B parameters, 17 B active per token; Llama 4 Maverick 17B 128E Instruct FP8 has 400 B parameters, 17 B active per token. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [llama-4-scout-17b-16e-instruct.json](https://leadgreen.ai/api/v1/models/llama-4-scout-17b-16e-instruct.json), [llama-4-maverick-17b-128e-instruct-fp8.json](https://leadgreen.ai/api/v1/models/llama-4-maverick-17b-128e-instruct-fp8.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Llama 4 Scout 17B 16E Instruct vs Llama 4 Maverick 17B 128E Instruct FP8: GPU energy per million output tokens. https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#rows)
- [What explains it](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#why)
- [Questions](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)
- [Sources](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#sources)

- **H100, index rows:** 1.44 × Llama 4 Maverick 17B 128E Instruct FP8 134.5 Wh/M on 8 × H100 against Llama 4 Scout 17B 16E Instruct 93.4 Wh/M on 4 × H100.
- **Parameters:** 3.7 × Llama 4 Maverick 17B 128E Instruct FP8 400 B parameters, 17 B active per token; Llama 4 Scout 17B 16E Instruct 109 B parameters, 17 B active per token.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Llama 4 Scout 17B 16E Instruct and Llama 4 Maverick 17B 128E Instruct FP8, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| H100 | [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/) | 4 × H100 | BF16 | 473 | 1,881 | 5,596 | 93.4 | 402 | 0.038 | 44.2 |
| H100 | [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/) | 8 × H100 | FP8 | 383 | 3,462 | 7,149 | 134.5 | 408 | 0.055 | 63.6 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two expert counts

Two mixture-of-experts models with the same active parameters per token (17 B) and very different totals: Llama 4 Scout 17B 16E Instruct routes across 16 experts (109 B in all), Llama 4 Maverick 17B 128E Instruct FP8 across 128 (400 B). The work per token is similar; the memory is not, so the larger model needs more cards to hold its experts and spreads each token's work across them. On the H100 the rows sit on four cards (Llama 4 Scout 17B 16E Instruct) and eight cards (Llama 4 Maverick 17B 128E Instruct FP8), at running batches of 473 (Llama 4 Scout 17B 16E Instruct) and 383 (Llama 4 Maverick 17B 128E Instruct FP8). The index row ratio on the H100 is 1.44×: the price of holding the extra experts, at the running batches stated in the table.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Llama 4 Scout 17B 16E Instruct against Llama 4 Maverick 17B 128E Instruct FP8

### Is Llama 4 Scout 17B 16E Instruct more energy-efficient than Llama 4 Maverick 17B 128E Instruct FP8?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 4 Maverick 17B 128E Instruct FP8 uses 1.44× the GPU energy per output token of Llama 4 Scout 17B 16E Instruct on the H100 (134.5 against 93.4 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Llama 4 Maverick 17B 128E Instruct FP8 use per million tokens than Llama 4 Scout 17B 16E Instruct?

The index rows differ by 41.1 Wh/M on the H100 (41.1 kWh per billion tokens). Per answer, at each row's own average output length, Llama 4 Scout 17B 16E Instruct costs 0.038 Wh on the H100 and Llama 4 Maverick 17B 128E Instruct FP8 0.055 Wh on the H100.

### Do more experts cost more energy per token at the same active parameters?

On these rows, yes: with 17 B active parameters each, Llama 4 Maverick 17B 128E Instruct FP8 (400 B in all) uses 1.44× the GPU energy per output token of Llama 4 Scout 17B 16E Instruct (109 B) on the H100, 134.5 against 93.4 Wh/M. The extra experts must be held in memory and the token's work spread across more cards (8 against 4), which is the energy the table shows.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the H100 the rows here ran on 4 and 8 cards at running batches of 473 and 383. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
