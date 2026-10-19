# Llama 3.1 405B Instruct FP8 vs Llama 3.1 405B Instruct: GPU energy per million output tokens

> Llama 3.1 405B Instruct against Llama 3.1 405B Instruct FP8 on GPU energy per output token: 0.89× on the B200, from the index rows.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/ (this file: https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Compare](https://leadgreen.ai/compare/) · Two precisions · B200*

On the index rows, Llama 3.1 405B Instruct uses **0.89×** the GPU energy per output token of Llama 3.1 405B Instruct FP8 on the B200 (282.0 against 318.5 Wh/M, on eight cards and four cards at running batches of 3,589 and 510), GPU only, each at the most energy-efficient configuration the ML.ENERGY Leaderboard v3.0 measured for it (data compiled 16 February 2026). Llama 3.1 405B Instruct FP8 has 405 B parameters; Llama 3.1 405B Instruct has 405 B parameters. Part of each gap is the sweep rather than the model: the two rows of a pair differ in card count and running batch, and the table states both.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [llama-3-1-405b-instruct-fp8.json](https://leadgreen.ai/api/v1/models/llama-3-1-405b-instruct-fp8.json), [llama-3-1-405b-instruct.json](https://leadgreen.ai/api/v1/models/llama-3-1-405b-instruct.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Llama 3.1 405B Instruct FP8 vs Llama 3.1 405B Instruct: GPU energy per million output tokens. https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The rows](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#rows)
- [What explains it](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#why)
- [Questions](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)
- [Sources](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#sources)

- **B200, index rows:** 0.89 × Llama 3.1 405B Instruct 282.0 Wh/M on 8 × B200 against Llama 3.1 405B Instruct FP8 318.5 Wh/M on 4 × B200.
- **Parameters:** 1.0 × Llama 3.1 405B Instruct 405 B parameters; Llama 3.1 405B Instruct FP8 405 B parameters.

Each ratio compares the two models' index rows on the same GPU: the lowest-energy configuration the leaderboard measured for each, at or under 500 ms median inter-token latency. The ratio is the second model's energy per token over the first's, so a figure under 1 means the second model's row is the lower one. Card count and running batch differ between the rows and are shown in the table.

*The rows*

## Index rows on every GPU both models share

*Index rows for Llama 3.1 405B Instruct FP8 and Llama 3.1 405B Instruct, with the configuration behind each and the per-answer and carbon readings*

| GPU | Model | Cards | Precision | Running batch | GPU W | Tokens / s | Wh / M | Output tokens | Wh per answer | kg CO2e / bn tokens, world grid |
|---|---|---|---|---|---|---|---|---|---|---|
| B200 | [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 4 × B200 | FP8 | 510 | 3,883 | 3,386 | 318.5 | 380 | 0.121 | 150.7 |
| B200 | [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/) | 8 × B200 | BF16 | 3,589 | 7,530 | 7,419 | 282.0 | 370 | 0.104 | 133.4 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). GPU W is the measured average power summed across the cards. Wh per answer is Wh/M times the row's own average output length. Carbon uses the world average grid, 473 gCO2e per kWh (Ember, 2024); the [grid pages](https://leadgreen.ai/grids/) price every model on each listed grid. Model names link to every measured configuration.

*What explains it*

## Two precisions

The same model weights at two precisions. FP8 stores each weight in one byte and BF16 in two, so an FP8 row moves half the bytes per token from memory and the model fits on fewer cards or leaves more memory for batching. On these index rows FP8 does not come out ahead (B200: FP8 318.5 Wh/M on four cards at a running batch of 510, BF16 282.0 Wh/M on eight cards at 3,589). Where the FP8 row costs more, the reason is in the table: the two rows were swept to different card counts and reached different running batches, and a quieter row carries a higher energy per token whatever its precision. Quantisation is the cheapest energy lever after load, but these rows show it only pays when the serving configuration is matched; the model pages hold every configuration so the pair can be re-cut at the same cards and cap.

Load still moves the number more than either model does: Qwen 3 32B on 2 × H100 spans 7.1× between a running batch of 8 and 256 on the same cards, which is wider than the gap on this page. Pick the model for the task, then run it busy. The [running batch](https://leadgreen.ai/glossary/running-batch/) and [floor](https://leadgreen.ai/glossary/floor/) entries define the terms.

*Questions*

## Asked about Llama 3.1 405B Instruct FP8 against Llama 3.1 405B Instruct

### Is Llama 3.1 405B Instruct FP8 more energy-efficient than Llama 3.1 405B Instruct?

No, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 405B Instruct uses 0.89× the GPU energy per output token of Llama 3.1 405B Instruct FP8 on the B200 (282.0 against 318.5 Wh per million output tokens). These are floors at high load, GPU only, and the two rows of a pair differ in card count and running batch.

### How much more energy does Llama 3.1 405B Instruct use per million tokens than Llama 3.1 405B Instruct FP8?

The index rows differ by 36.6 Wh/M on the B200 (36.6 kWh per billion tokens); where the ratio is under 1, Llama 3.1 405B Instruct is the lower row. Per answer, at each row's own average output length, Llama 3.1 405B Instruct FP8 costs 0.121 Wh on the B200 and Llama 3.1 405B Instruct 0.104 Wh on the B200.

### Does FP8 save energy compared with BF16 for the same model?

Not on these index rows. On the B200 the FP8 row (Llama 3.1 405B Instruct FP8) uses 318.5 Wh/M on 4 cards at a running batch of 510 and the BF16 row 282.0 Wh/M on 8 at 3,589. FP8 halves the bytes moved per token and the memory the weights take, but the leaderboard swept the two variants to different card counts and loads, and load moves energy per token more than precision does. A matched run, same cards and same cap, is the comparison to ask a vendor for.

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. On the B200 the rows here ran on 4 and 8 cards at running batches of 510 and 3,589. The ratio compares the best measured row on each side, not a matched run; every configuration is on the model pages and in the API, so any pair can be re-cut at a matched cap or running batch.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration for its model and GPU at or under 500 ms median inter-token latency. Carbon per billion tokens multiplies the row by the world average grid intensity, 473 gCO2e per kWh (Ember, 2024).

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

Parameters and architecture as the leaderboard records them (total and activated parameters in billions). Carbon: Ember, Yearly electricity data, October 2026 release, world average 2024, CC BY 4.0, retrieved 17 October 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
