# The reasoning behind the rows

> Short, sourced pieces on what GPU energy per token means: the baseline, the idle server, sliced GPUs, where the electricity is, what the law asks.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/ (this file: https://leadgreen.ai/blog/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

Each post takes one question the index raises and answers it with public data, the working shown and the sources listed. Written to be read by people, and to be cited by the machines that now answer people's questions.

**Feed** [RSS](https://leadgreen.ai/feed.xml) · **Editor** Prem Naraindas · **Licence** CC BY 4.0

Cite this page: Lead Green, a Katonic project. Blog. https://leadgreen.ai/blog/, release 2026-10-18, retrieved [date]. CC BY 4.0.

*Posts*

## Published

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
