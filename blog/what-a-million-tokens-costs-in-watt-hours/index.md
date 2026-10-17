# What a million tokens costs in watt-hours

> What the public measurements say a million output tokens takes in GPU watt-hours, and why a busy server uses a fraction of the energy of a quiet one.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/what-a-million-tokens-costs-in-watt-hours/ (this file: https://leadgreen.ai/blog/what-a-million-tokens-costs-in-watt-hours/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

By Prem Naraindas · 26 September 2026 · Lead Green, a Katonic project

Look, everybody in this industry now buys tokens. Per million, on an invoice, from a cloud or from their own GPUs. And nobody gets told what a million of them costs in electricity. I have sat in enough capacity meetings to know the question is coming, so this is the baseline: what the public measurements say a million output tokens takes in watt-hours, and what moves the number.

## The unit

Watt-hours per million output tokens, Wh/M. It is GPU energy only, divided by the tokens the model produced. Prompt processing is inside the figure, because the measurement divides total GPU energy by output tokens. Host, network, cooling and idle time are not inside it. So every number here is a floor.

For scale: a million output tokens is roughly three quarters of a million words of English. And the reference row below, 63.5 Wh, is a 2 kW kettle running for 1.9 minutes. The kettle is my assumption, not a source; the tokens are.

## Where the numbers come from

The ML.ENERGY Leaderboard, run by the ML.ENERGY Initiative (it started at SymbioticLab, University of Michigan), serves open-weight models with vLLM on real H100 and B200 servers and measures GPU energy at steady state with its Zeus library. It publishes every stable configuration it ran (328 for this task) as JSON in its repository, and every run including the unstable ones in a gated Hugging Face dataset whose card declares Apache 2.0. Version 3.0 was released on 1 December 2025; the data I use was compiled on 16 February 2026. I took its Text Conversation task, kept the 328 configurations it published, and for each model and GPU picked the one with the least energy per token at or under a median inter-token latency of 500 ms, the leaderboard's own default. None of them comes near it. That gives 32 rows for 18 models. My 32 rows match the leaderboard's table when one GPU is selected at a time; at its default view it shows one row per model, 18 rows.

## Three numbers

- **Lowest: 13.0 Wh/M.** Llama 3.1 8B Instruct on 1 × B200. A small model on the newest card, kept busy.
- **Reference: 63.5 Wh/M.** Qwen 3 32B on 2 × H100, at a running batch of 256 and 44 ms median inter-token latency, the two cards drawing 1,178 W between them. I use this row for every carbon calculation on the site, because, in the deployments I see, a 32B dense model on two H100s is what a serious enterprise deployment looks like today.
- **Highest: 572.9 Wh/M.** Llama 3.1 405B Instruct FP8 on 8 × H100. Eight cards to hold the weights, and every token pays for all eight.

The span from lowest to highest is 44×. That is model size and hardware generation, and it is what people expect the story to be. It is not the interesting part.

## The interesting part

Take the reference model and change nothing except how many requests the server holds at once.

*Qwen 3 32B, BF16, 2 × H100. ML.ENERGY Leaderboard v3.0, Text Conversation.*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 452.0 | 15 | 522 | 850 |
| 16 | 16 | 252.8 | 16 | 970 | 883 |
| 32 | 32 | 153.8 | 18 | 1,706 | 944 |
| 64 | 64 | 102.0 | 22 | 2,654 | 974 |
| 96 | 96 | 84.6 | 26 | 3,356 | 1,022 |
| 128 | 128 | 76.4 | 30 | 3,905 | 1,074 |
| 192 | 192 | 69.0 | 37 | 4,601 | 1,143 |
| 256 | 256 | 63.5 | 44 | 5,155 | 1,178 |
| 384 | 340 | 64.6 | 55 | 5,071 | 1,180 |

From 452 to 63.5 Wh/M. 7.1× on the same model, the same two cards, the same prompts. The power draw rises by about a third, 39 percent: 850 W at the top of the table, 1,178 W at the best row. What moves far more is how many tokens that power produces, from 522 a second to 5,155, 9.9×. Median latency goes from 15 ms to 44 ms, which no user will notice. Past that row the curve turns: at a cap of 384 the same cards read 64.6 Wh/M at 55 ms.

See, this is the part the invoice hides. A GPU is a bus. The diesel per trip goes up a little when the bus is full; the diesel per passenger comes down a long way. An enterprise assistant that serves a handful of people at a time is the bus running nearly empty, and in the deployments I see it is the usual case.

The same ladder for a small model on one card: Llama 3.1 8B Instruct on 1 × H100 goes from 126 Wh/M at a running batch of 8 to 19.5 at 511, a 6.5× drop, while its power rises 41 percent. All eleven of its configurations are on [the index](https://leadgreen.ai/index/#concurrency).

## What that does to the bill, and to the carbon

Electricity first, because people always ask and the answer is small. 63.5 Wh per million tokens is 63.5 kWh per billion. At USD 0.10 per kWh, my assumption and not a source figure, a billion tokens is USD 6.35 of electricity, or 0.6 cents per million. Nobody will change a decision over that. The number matters because it tracks GPU-hours, and GPU-hours are where the money actually goes. Halve the watt-hours per token and you have halved the GPU time per token, on the same kit.

Carbon depends on where the socket is. Multiply Wh/M by the grid's grams of CO2e per kWh and divide by a thousand, and you get kilograms per billion tokens. On Ember's 2024 annual averages the reference row is 43.7 kg per billion tokens in Saudi Arabia (689 g/kWh), 42.4 kg in Serbia (668), and 1.9 kg in Norway (30). Same tokens, same cards, 23× apart. Location moves the carbon and does nothing to the energy, which is why the two should never be reported as one number.

## What I am not telling you

Closed-weight models served over an API. The leaderboard cannot measure them, and neither can anyone outside those companies, so I say nothing about them. Sliced GPUs: NVIDIA does not publish power per MIG slice and no public benchmark has measured one, which is the first gap we will fill with a measurement of our own, on our own rig, with the protocol and the logs published. And the lightly loaded reality: every row on the index is the best case under a latency limit. Your deployment sits above it. The concurrency table tells you how far.

I wish I could tell you the platform we build already measures this for every tenant. It does not, yet. When it does, it will be published here under the same review as any other row, labelled as ours, beside the public ones.

## What to do with it

Ask your vendor for Wh per million output tokens at your concurrency, not theirs. Measure your own with DCGM; one row is an afternoon's work on a card you control, and a MIG pair is an evening. And put the number in the RFP. The clause is on the [why page](https://leadgreen.ai/why/#monday). If two bidders give you the same figure at the same load, you have learned something. If neither can, you have learned more.

*References*

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).
2. Ember, Yearly electricity data, October 2026 release, emissions intensity of total generation, 2024, CC BY 4.0, retrieved 17 October 2026. [ember-energy.org](https://ember-energy.org/data/yearly-electricity-data/).
3. OpenAI, What are tokens and how to count them, retrieved 27 September 2026, for the words-per-token rule of thumb.
4. Full tables, method and sources: [the index](https://leadgreen.ai/index/). Data: [the API](https://leadgreen.ai/api/).
