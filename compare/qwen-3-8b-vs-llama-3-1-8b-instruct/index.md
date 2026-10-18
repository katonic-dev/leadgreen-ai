# Qwen 3 8B vs Llama 3.1 8B Instruct: GPU energy per million output tokens

> Llama 3.1 8B Instruct against Qwen 3 8B on GPU energy per output token: 0.97× on the H100 and 0.88× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/ (this file: https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two families, one size · H100 and B200*

On the index rows, Llama 3.1 8B Instruct uses **0.97×** the GPU energy per output token of Qwen 3 8B on the H100 (19.5 against 20.0 Wh/M, both on one card at running batches of 511 and 474) and **0.88×** on the B200 (13.0 against 14.7 Wh/M, both on one card at running batches of 2,043 and 1,427), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Qwen 3 8B has 8 B parameters; Llama 3.1 8B Instruct has 8 B parameters. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [qwen-3-8b.json](https://leadgreen.ai/api/v1/models/qwen-3-8b.json), [llama-3-1-8b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-1-8b-instruct.json). Updated 18 October 2026.

Cite this page: Lead Green, a Katonic project. Qwen 3 8B vs Llama 3.1 8B Instruct: GPU energy per million output tokens. https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/, release 2026-10-18, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#rows)
- [What explains it](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#why)
- [Questions](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)
- [Sources](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#sources)

- **H100, index rows:** 0.97 × Llama 3.1 8B Instruct 19.5 Wh/M on 1 × H100 against Qwen 3 8B 20.0 Wh/M on 1 × H100.
- **B200, index rows:** 0.88 × Llama 3.1 8B Instruct 13.0 Wh/M on 1 × B200 against Qwen 3 8B 14.7 Wh/M on 1 × B200.
- **Parameters:** 1.0 × Llama 3.1 8B Instruct 8 B parameters; Qwen 3 8B 8 B parameters.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Qwen 3 8B and Llama 3.1 8B Instruct, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| H100 | [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 1 × H100 | BF16 | 474 | 616 | 8,535 | 20.0 | 645 | 0.013 | 9.5 |
| H100 | [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × H100 | BF16 | 511 | 688 | 9,806 | 19.5 | 397 | 0.008 | 9.2 |
| B200 | [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 1 × B200 | BF16 | 1,427 | 801 | 15,100 | 14.7 | 649 | 0.010 | 7.0 |
| B200 | [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × B200 | BF16 | 2,043 | 691 | 14,799 | 13.0 | 396 | 0.005 | 6.1 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two families, one size

Two models of the same size class from different families: Qwen 3 8B (8 B parameters, Dense Transformer) against Llama 3.1 8B Instruct (8 B parameters, Dense Transformer). At the same size the energy per token depends on the architecture's depth and width, the vocabulary, the attention design and, on the leaderboard, the configuration swept for each: card count, cap and the running batch reached. On the H100 both rows sit on one card, at running batches of 474 (Qwen 3 8B) and 511 (Llama 3.1 8B Instruct). The gap here is under 12 percent, which is inside what load alone moves; read the ratio with the running batches beside it.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Qwen 3 8B against Llama 3.1 8B Instruct

### Is Qwen 3 8B more energy-efficient than Llama 3.1 8B Instruct?

No, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 8B Instruct uses 0.97× the GPU energy per output token of Qwen 3 8B on the H100 (19.5 against 20.0 Wh per million output tokens) and 0.88× the GPU energy per output token of Qwen 3 8B on the B200 (13.0 against 14.7 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Llama 3.1 8B Instruct use per million tokens than Qwen 3 8B?

The index rows differ by 0.5 Wh/M on the H100 (0.5 kWh per billion tokens) and 1.8 Wh/M on the B200 (1.8 kWh per billion tokens); where the ratio is under 1, Llama 3.1 8B Instruct is the lower row. Per answer, at each row's own average output length, Qwen 3 8B costs 0.013 Wh on the H100 and 0.010 Wh on the B200 and Llama 3.1 8B Instruct 0.008 Wh on the H100 and 0.005 Wh on the B200.

### Why do two models of the same size differ in energy per token?

Architecture (depth, width, attention design), vocabulary and, on the leaderboard, the configuration swept for each model: card count, cap and the running batch actually reached. On the H100 the rows here ran at running batches of 474 (Qwen 3 8B) and 511 (Llama 3.1 8B Instruct); a quieter row carries a higher energy per token whatever its architecture. The gap is 12 percent at most, inside what load alone moves.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the H100 the rows here ran on 1 and 1 cards at running batches of 474 and 511. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-18, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
