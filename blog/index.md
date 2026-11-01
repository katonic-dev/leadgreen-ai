# The reasoning behind the rows

> Short, sourced pieces on what GPU energy per token means: the baseline, the idle server, sliced GPUs, where the electricity is, what the law asks.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/ (this file: https://leadgreen.ai/blog/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

Each post takes one question the index raises and answers it with public data, the working shown and the sources listed. Written to be read by people, and to be cited by the machines that now answer people's questions.

**Feed** [RSS](https://leadgreen.ai/feed.xml) · **Editor** Prem Naraindas · **Licence** CC BY 4.0

Cite this page: Lead Green, a Katonic project. Blog. https://leadgreen.ai/blog/, release 2026-10-19, retrieved [date]. CC BY 4.0.

*Posts*

## Published

- 1 November 2026 · Prem Naraindas

### [Is the B200 more energy-efficient than the H100?](https://leadgreen.ai/blog/is-the-b200-more-energy-efficient-than-the-h100/)

Yes on all 14 models measured on both cards: the H100 row uses 1.05× to 4.55× the B200 row's energy per token, median 1.63×. How much is the silicon.
- 19 October 2026 · Prem Naraindas

### [How much energy does an AI query use?](https://leadgreen.ai/blog/how-much-energy-does-an-ai-query-use/)

One answer from a busy 32B model costs about 0.040 Wh of GPU energy; Google says 0.24 Wh per median prompt. Both are right. Here is why.
- 19 October 2026 · Prem Naraindas

### [What is watt-hours per million tokens, and why not joules per token?](https://leadgreen.ai/blog/what-is-watt-hours-per-million-tokens/)

The unit behind the index: what Wh/M counts, what it leaves out, how it converts to kWh, carbon and the meter, and why joules per token became watt-hours.
- 19 October 2026 · Prem Naraindas

### [Why an idle GPU wastes energy: the concurrency ladder](https://leadgreen.ai/blog/why-an-idle-gpu-wastes-energy/)

Same model, same two H100 cards: 7.1× in GPU energy per token between a running batch of 8 and 256. Why the under-used card is the expensive one.
- 26 September 2026 · Prem Naraindas

### [What a million tokens costs in watt-hours](https://leadgreen.ai/blog/what-a-million-tokens-costs-in-watt-hours/)

What the public measurements say a million output tokens takes in GPU watt-hours, and why a busy server uses a fraction of the energy of a quiet one.

*Upcoming*

## The next five

- next**The sliced GPU.** Energy per token when one card is split into MIG instances, measured: Qwen 3 14B on two 3g.40gb slices against the whole card, both in BF16; then Qwen 3 32B, whole card in BF16 against two FP8 or INT4 slices.
- then**The idle token.** Why an under-used GPU spends more energy on every token than a busy one, with the concurrency ladder as the evidence.
- then**Per correct answer, not per token.** Small model against large model once re-tries and wrong answers are counted.
- then**Where the electricity is.** The same workload in Riyadh, Belgrade, Hong Kong and Auckland, by grid intensity.
- then**What the EU AI Act asks, and what it does not.** The training-energy item on model providers, the open-source exemption and the 2027 date, and why none of it reaches a buyer.

Order and timing may change; a post ships when its data does. Volunteers who want to take one of these: see [Contribute](https://leadgreen.ai/contribute/).
