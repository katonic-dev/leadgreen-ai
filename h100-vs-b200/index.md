# H100 vs B200: GPU energy per million output tokens

> H100 against B200 on GPU energy per output token, 14 open-weight models: the gap runs from 4.55× to 1.05×, and how much is the sweep. ML.ENERGY v3.0.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/h100-vs-b200/ (this file: https://leadgreen.ai/h100-vs-b200/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Two generations · 14 models*

On the index rows, the B200 uses less GPU energy per output token than the H100 for **all 14 models** measured on both cards. The H100 row uses from **4.55×** the energy of the B200 row (Qwen 3 235B A22B Instruct) down to **1.05×** (NVIDIA Nemotron Nano 9B V2), with a median of 1.63×. Part of many gaps is the sweep rather than the silicon: the two rows of a pair often differ in card count and running batch, and on eight of the 14 pairs the B200 row holds the model on fewer cards.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. **Data** [index.json](https://leadgreen.ai/api/v1/index.json). Updated 27 September 2026.

- [The 14 pairs](https://leadgreen.ai/h100-vs-b200/#pairs)
- [The sweep](https://leadgreen.ai/h100-vs-b200/#sweep)
- [Power against energy](https://leadgreen.ai/h100-vs-b200/#power)
- [Questions](https://leadgreen.ai/h100-vs-b200/#faq)
- [Sources](https://leadgreen.ai/h100-vs-b200/#sources)

- **Widest gap:** 4.55 × Qwen 3 235B A22B Instruct: 303.5 Wh/M on 8 × H100 against 66.7 on 4 × B200.
- **Median gap, 14 pairs:** 1.63 × H100 row energy per token over B200 row energy per token, at each model's index rows.
- **Narrowest gap:** 1.05 × NVIDIA Nemotron Nano 9B V2: 43.1 Wh/M on 1 × H100 against 40.9 on 1 × B200.

Each pair compares a model's index row on the H100 with its index row on the B200: the lowest-energy configuration the leaderboard measured on each card, at or under 500 ms median inter-token latency. The ratio is the H100 row's energy per token over the B200 row's.

*The pairs*

## Every model measured on both cards

*Index rows paired by model, with card count and running batch, sorted by the gap*

| Model | H100 | Running batch | Wh / M | B200 | Running batch | Wh / M | H100 ÷ B200 |
|---|---|---|---|---|---|---|---|
| [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 8 × H100 | 228 | 303.5 | 4 × B200 | 3,765 | 66.7 | 4.55× |
| [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/) | 1 × H100 | 253 | 31.1 | 1 × B200 | 2,045 | 15.2 | 2.04× |
| [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/) | 4 × H100 | 898 | 103.7 | 2 × B200 | 2,042 | 52.4 | 1.98× |
| [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 4 × H100 | 724 | 117.5 | 2 × B200 | 1,022 | 60.7 | 1.94× |
| [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 8 × H100 | 255 | 572.9 | 4 × B200 | 510 | 318.5 | 1.80× |
| [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/) | 1 × H100 | 128 | 46.1 | 1 × B200 | 487 | 26.5 | 1.74× |
| [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/) | 2 × H100 | 187 | 80.4 | 1 × B200 | 247 | 49.1 | 1.64× |
| [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 2 × H100 | 256 | 63.5 | 1 × B200 | 383 | 39.1 | 1.63× |
| [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 2 × H100 | 1,019 | 24.7 | 1 × B200 | 1,023 | 15.7 | 1.58× |
| [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × H100 | 511 | 19.5 | 1 × B200 | 2,043 | 13.0 | 1.50× |
| [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/) | 8 × H100 | 511 | 206.0 | 2 × B200 | 256 | 139.1 | 1.48× |
| [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 1 × H100 | 474 | 20.0 | 1 × B200 | 1,427 | 14.7 | 1.36× |
| [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/) | 1 × H100 | 241 | 50.1 | 1 × B200 | 256 | 39.4 | 1.27× |
| [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/) | 1 × H100 | 255 | 43.1 | 1 × B200 | 255 | 40.9 | 1.05× |

Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). Model names link to every measured configuration of that model.

*The sweep*

## How much of the gap is the silicon

The gap also depends on which configurations were swept. The 4.55× pair compares an H100 row that was run only at eight cards and a cap of at most 256 requests with a B200 row at a running batch of 3,765 on four cards; at the same cap of 256 the B200 row reads 197.5 Wh/M against the H100's 303.5, a gap of 1.54×. The two Nemotron pairs compare runs whose average answers are 3.2 and 2.4 times longer on the B200 (462 and 510 tokens on the H100 against 1,464 and 1,242).

At a 50 ms ceiling the comparison shifts: 14 models still have a row on both cards, and the H100 uses less energy per token than the B200 on two of them (Llama 3.1 8B Instruct, 19.5 Wh/M on 1 × H100 against 19.6 on 1 × B200; Qwen 3 235B A22B Instruct FP8, 306.7 Wh/M on 8 × H100 against 408.9 on 2 × B200).

Every configuration behind these rows is on [the model pages](https://leadgreen.ai/models/) and in the [API](https://leadgreen.ai/api/), so any pair can be re-cut at a matched cap or a matched running batch.

*Power against energy*

## The card that draws more can use less

A B200 card draws more power than an H100: NVIDIA rates the H100 SXM at up to 700 W and the B200 configurable up to 1,000 W, and on these index rows the cards averaged 612 W per H100 and 868 W per B200. It uses less energy per token because it finishes more tokens in each second of that draw. Power tells you the size of the feed; energy per token tells you what the feed produced. An eight-GPU DGX B200 is rated at about 14.3 kW against 8.0 kW for its GPUs, so the system draws 1.79× what the cards do; the [method](https://leadgreen.ai/index/#method) takes a GPU figure to the facility meter.

*Maximum thermal design power, as published by NVIDIA*

| GPU | Form | Max TDP | Memory |
|---|---|---|---|
| A100 80GB | SXM | 400 W | 80 GB HBM2e |
| A100 80GB | PCIe | 300 W | 80 GB HBM2e |
| H100 | SXM | up to 700 W | 80 GB HBM3 |
| H100 | NVL | 350 to 400 W | 94 GB HBM3 |
| H200 | SXM | up to 700 W | 141 GB HBM3e |
| H200 | NVL | up to 600 W | 141 GB HBM3e |
| B200 | HGX, SXM6 | configurable up to 1,000 W | 180 GB HBM3e |

*Questions*

## Asked about H100 against B200

### Is the B200 more energy-efficient than the H100 for LLM inference?

On the ML.ENERGY Leaderboard's index rows, yes for all 14 models measured on both:

### How much energy does a B200 save over an H100 per million tokens?

It depends on the model: for the reference model, Qwen 3 32B, the index rows are 63.5 Wh/M on 2 × H100 against 39.1 Wh/M on 1 × B200. The table on this page gives all 14 pairs.

### Does the B200 draw more power than the H100?

A B200 card draws more power than an H100: NVIDIA rates the H100 SXM at up to 700 W and the B200 configurable up to 1,000 W, and on these index rows the cards averaged 612 W per H100 and 868 W per B200. It uses less energy per token because it finishes more tokens in each second of that draw. Power tells you the size of the feed; energy per token tells you what the feed produced.

### Should I buy B200s to cut the energy of AI inference?

Not first. The same model on the same H100 cards moves 7.1× in energy per token between a running batch of 8 and 256, which is more than the widest generation gap here (4.55×). Consolidating traffic onto fewer, busier cards costs nothing in hardware; the generation change comes after.

### Why do the two rows of a pair have different card counts?

The leaderboard picks each GPU's configurations separately; a B200 has more memory, so a model that needs eight H100s can fit fewer B200s. On 8 of the 14 pairs the B200 row holds the model on fewer cards, and the running batches differ too, so the ratio compares the best measured row on each card, not like for like.

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration at or under 500 ms median inter-token latency. TDP figures are NVIDIA's published specifications.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).

TDP and memory: NVIDIA product specifications for [H100](https://www.nvidia.com/en-us/data-center/h100/) and [DGX B200](https://www.nvidia.com/en-us/data-center/dgx-b200/), and the [HGX B200 product carbon footprint summary](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf) (July 2025), retrieved 26 September 2026.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
