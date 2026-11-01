# Why an idle GPU wastes energy: the concurrency ladder

> Same model, same two H100 cards: 7.1× in GPU energy per token between a running batch of 8 and 256. Why the under-used card is the expensive one.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/why-an-idle-gpu-wastes-energy/ (this file: https://leadgreen.ai/blog/why-an-idle-gpu-wastes-energy/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

By Prem Naraindas · 19 October 2026 · Lead Green, a Katonic project

Cite this page: Lead Green, a Katonic project. Why an idle GPU wastes energy: the concurrency ladder. https://leadgreen.ai/blog/why-an-idle-gpu-wastes-energy/, release 2026-10-19, retrieved [date]. CC BY 4.0.

Look, when people want to cut the energy their AI uses, they reach for a smaller model or a newer card. Both work. But on the same model and the same cards there is a lever that moves the number further than a change of GPU generation does, and in the deployments I see it is the one nobody has looked at: how many requests the server is handling at once. So here is the exhibit: Qwen 3 32B on 2 × H100, same weights, same prompts, measured by the ML.ENERGY Leaderboard at nine different loads. At a running batch of 8 it costs 452 Wh of GPU energy per million output tokens. At 256 it costs 63.5 Wh. That is 7.1× on hardware nobody touched.

## The ladder

*Qwen 3 32B, BF16, 2 × H100. ML.ENERGY Leaderboard v3.0, Text Conversation, all nine measured configurations. The highlighted row is the index row.*

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

The cap is how many requests the server was allowed to hold; the running batch is how many it actually held, on average, while it was decoding. Energy per token falls the whole way to the highlighted row. Power rises, but only 39 percent, from 850 W to 1,178 W across both cards. Tokens per second rise 9.9×, from 522 to 5,155. Median inter-token latency goes from 15 ms to 44 ms, and nobody reading an answer will notice either. Energy per token is power divided by throughput, so when throughput moves 9.9× and power moves 39 percent, energy per token moves 7.1×.

## Why the under-used card costs more

A model writes one token at a time, and to write each one it has to read its whole set of weights out of the cards' memory. In plain terms, for a dense model like this one, that read is the expensive part of every step, and it costs about the same whether the step produces one token for one user or 256 tokens for 256 users. The card is a lecturer. The lecture costs the same to give to 8 people as to 256; what changes is the cost per head. See, that is why the power column barely moves while the tokens column runs away: at a batch of 8 the cards were already doing the heavy work, for very few people.

One caveat on the word idle. The benchmark never measured an empty card: every row holds at least 8 conversations, with a queue behind them. A departmental assistant with two or three requests in flight, the common case in the deployments I see, sits above the top row. Idle here means under-used, and if anything the ladder understates what under-used costs.

## Most of the gain comes early

You do not need 256 requests in flight to get most of it. By a running batch of 64 the same cards read 102.0 Wh/M, 4.4× down from the top row, at 22 ms median latency and 974 W. That is 90 percent of the whole drop, at a load one busy business unit can generate. The rest of the ladder buys the remainder, and buys it more slowly.

## Where it turns

More is not always better. At a cap of 384 the two cards read 64.6 Wh/M, a little above the best row, at 55 ms median latency, and the slowest token in a hundred now waits 240 ms against 148 ms one row up. The server was allowed 384 and held 340, which I read as the cards running out of memory for the conversations in flight: the engine starts juggling them, the users at the back feel it, and energy per token stops improving. The index takes the lowest-energy row at or under the leaderboard's 500 ms ceiling, the 256 row here, and the curve past it is why an index row is a floor and not a target.

## A small model on one card does the same

*Llama 3.1 8B Instruct, BF16, 1 × H100. ML.ENERGY Leaderboard v3.0, Text Conversation, all eleven measured configurations. The highlighted row is the index row.*

| Cap | Running batch (avg) | Wh / M | Median ITL (ms) | Tokens / s | GPU power (W) |
|---|---|---|---|---|---|
| 8 | 8 | 126.3 | 7 | 1,070 | 486 |
| 16 | 16 | 73.0 | 8 | 1,954 | 513 |
| 32 | 32 | 45.8 | 9 | 3,391 | 560 |
| 64 | 64 | 32.9 | 12 | 5,147 | 610 |
| 96 | 96 | 28.6 | 14 | 6,260 | 644 |
| 128 | 128 | 26.4 | 16 | 7,037 | 669 |
| 192 | 192 | 23.2 | 21 | 8,223 | 688 |
| 256 | 255 | 21.3 | 26 | 9,010 | 691 |
| 384 | 383 | 20.6 | 38 | 9,248 | 687 |
| 512 | 511 | 19.5 | 47 | 9,806 | 688 |
| 768 | 691 | 19.8 | 63 | 9,603 | 685 |

Llama 3.1 8B Instruct on 1 × H100: 126 to 19.5 Wh/M, 6.5× on one card, power up 41 percent, throughput up 9.2×. 87 percent of the drop is in by a batch of 64, and past the best row, at a cap of 768, it turns the same way, holding 691 of the 768 it was allowed. A much smaller model, one card instead of two, the same shape. In my view the shape is the finding: it is a property of how these servers decode, not of one model, and every model's own ladder is on [its page](https://leadgreen.ai/models/).

## What it does to the bill

Electricity is the small part of this and I will not pretend otherwise. The number that moves a budget is GPU-hours, and the ladder is a GPU-hours table in disguise. At the top row a million output tokens takes 1.06 GPU-hours on these two cards; at the best row, 0.11. Same cards, same model, 9.9× the tokens out of every hour of silicon you rent or own. Turn it round for the facility: one megawatt-hour of GPU energy serves 2.2 billion output tokens at the top of the ladder and 15.8 billion at the index row, and a site with a fixed power envelope, which is every site, only gets to choose which of those two it is.

## What to do with it

- **Measure your running batch before you buy anything.** vLLM reports it as `num_requests_running`; average it over a busy hour. If it is in single figures you are at the top of the ladder, and no change of card on the [comparison page](https://leadgreen.ai/h100-vs-b200/) moves the number as far as filling the cards you have.
- **Consolidate.** Fewer, busier cards. Three teams each running their own copy of the same model on their own pair of cards is the usual arrangement I see; one shared deployment carrying all three sits rows further down this table, and it costs nothing in hardware.
- **Ask the vendor for Wh per million output tokens at your running batch,** not theirs, and put your own [N] into the RFP clause on the [why page](https://leadgreen.ai/rfp/). A figure measured at 256 in flight tells you nothing about a service that will run at 8.
- **Do not chase the bottom of the table.** Past the best row the users wait and the energy does not fall. Pick the row on the [model page](https://leadgreen.ai/models/qwen-3-32b/) that matches the latency you promised, and hold the vendor to it.

I think this is the table to take into the capacity meeting, because it is the lever you already hold. The full ladders, with the definitions, are on [the index](https://leadgreen.ai/index/#concurrency).

*References*

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).
2. The rows: all nine measured configurations of Qwen 3 32B on 2 × H100 and all eleven of Llama 3.1 8B Instruct on 1 × H100, Text Conversation, BF16. Cap is vLLM's `max_num_seqs`; running batch (avg) is the average `num_requests_running` over the steady-state window; queued requests are not counted. Full ladders on [the index](https://leadgreen.ai/index/#concurrency); every model's curve is in [the API](https://leadgreen.ai/api/).
3. GPU-hours per million output tokens = cards × 1,000,000 ÷ output tokens per second ÷ 3,600. Tokens per megawatt-hour = 1,000,000 ÷ Wh/M, in millions.
4. The mechanism: Pope et al., Efficiently Scaling Transformer Inference, November 2022, [arXiv 2211.05102](https://arxiv.org/abs/2211.05102), on generation at a small batch being bound by reading the weights; Kwon et al., Efficient Memory Management for Large Language Model Serving with PagedAttention, SOSP 2023, [arXiv 2309.06180](https://arxiv.org/abs/2309.06180), on the memory held for requests in flight limiting the batch a server can hold. The reading of the 384 row as memory running out is mine.
