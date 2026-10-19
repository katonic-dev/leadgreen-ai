# How much energy does an AI query use?

> One answer from a busy 32B model costs about 0.040 Wh of GPU energy; Google says 0.24 Wh per median prompt. Both are right. Here is why.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/how-much-energy-does-an-ai-query-use/ (this file: https://leadgreen.ai/blog/how-much-energy-does-an-ai-query-use/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

By Prem Naraindas · 19 October 2026 · Lead Green, a Katonic project

Cite this page: Lead Green, a Katonic project. How much energy does an AI query use?. https://leadgreen.ai/blog/how-much-energy-does-an-ai-query-use/, release 2026-10-19, retrieved [date]. CC BY 4.0.

Look, this is the question I get asked most, usually by someone who has just signed off a token budget. "How much energy does one of these queries actually use?" And the honest first answer is that nobody who quotes a single figure is telling you the whole story, because the number depends on four things: which model, on which GPUs, how busy the server was, and how long the answer ran. So here is the number the public measurements give, with those four things stated, and then the two figures the vendors have published, and why they are different without either being wrong.

## The number

On the index's reference row, Qwen 3 32B on 2 × H100, a busy server produces a million output tokens for 63.5 Wh of GPU energy. The benchmark's answers on that row averaged 634 tokens, so one answer costs about **0.040 Wh**. That is a kilowatt-hour for roughly 24,800 answers. A 10 W LED bulb uses the same energy in about 14 seconds. The bulb is my assumption, not a source; the tokens are.

Three qualifications, and they are not fine print. It is GPU energy only: the host, the network, the cooling and the building are outside it. It was measured with the server running 256 requests at once, which is a busy server. And it is one model on one card count. Change any of those and the number moves, sometimes by a lot.

## What Google and Mistral published

In August 2025 Google put the median Gemini Apps text prompt at **0.24 Wh**, 0.03 g of CO2e and 0.26 mL of water. In July 2025 Mistral put a 400-token reply from its large model at 1.14 g of CO2e and 45 mL of water, without a watt-hour figure. Those are the only two per-prompt disclosures from model vendors I know of, and I am glad they exist.

Google's 0.24 Wh is about 6× my 0.040 Wh. See, that gap is the interesting part, and it is mostly boundary. Google counts the whole stack: the accelerators are 58 percent of its figure, so about 0.14 Wh, with the host machines, idle capacity held for peaks, and the data centre's overhead making up the rest. Google also reports a narrow, accelerator-only figure of 0.10 Wh, which is the boundary this index uses. So on a like-for-like boundary its number is 3.5× mine, and the rest of the difference is a different model, a different prompt length, and a fleet running at whatever utilisation Google's traffic gives it rather than a benchmark holding a server full.

None of that makes either figure wrong. They answer different questions. Google's tells you what a prompt costs a hyperscaler across its whole estate. The index tells you what a named model on named GPUs costs at a stated load, which is the figure you can hold a vendor to, because you can measure it yourself.

## What moves it most: how busy the server is

Take the same Qwen 3 32B on the same 2 × H100 and run it with 8 requests at once instead of 256. Energy per million tokens goes from 63.5 to 452 Wh, and one answer goes from 0.040 Wh to about **0.29 Wh**. Same model, same cards, same prompts, 7.1× the energy, because the cards draw only about 39 percent more power serving two hundred and fifty people than eight, and at eight they are mostly waiting.

Think of a bakery oven. It costs about the same gas to run whether there are two loaves in it or forty. The gas per loaf is a different matter. In the deployments I see, most enterprise assistants are the oven with two loaves in it: a department, a few dozen users, a handful of requests at any moment. Their energy per answer is at the top of that range, not the bottom, and nothing on their invoice says so.

## The range

Across the whole index, the lowest row is Llama 3.1 8B Instruct on 1 × B200 at 13.0 Wh per million tokens, which is about 0.005 Wh for one of its 396-token answers. The highest configuration the benchmark measured at all, not an index row but a real run, is Llama 3.1 405B Instruct on 8 × B200 holding 8 requests: 6,073 Wh per million tokens, about 2.2 Wh an answer, 10.6× the highest index row. So "how much energy does an AI query use" has a defensible answer somewhere between a few thousandths of a watt-hour and a couple of watt-hours, and the four things above decide where.

## What I am not telling you

Closed models served over an API. Nobody outside the operator can measure them, so I say nothing about them beyond what the operator publishes, which for most of them is nothing. Water: the index measures electricity and not water; Google and Mistral both publish a water figure and I think that is the right thing to do, but neither is per million tokens at a stated load, so it stays out of the tables. And the meter: to get from a GPU figure to what the building draws, multiply by the system's host-to-GPU ratio and the site's PUE, which only the operator knows. The [method](https://leadgreen.ai/index/#method) works one example.

## What to do with it

If you buy tokens from a hosted API, the concurrency is theirs and you cannot measure it; ask the provider the [seven questions](https://leadgreen.ai/why/#hosted) instead. If you run the GPUs, ask your vendor for watt-hours per million output tokens at your running batch, not theirs, and hold the answer against the [model's page](https://leadgreen.ai/models/qwen-3-32b/). Or ask the [MCP server](https://leadgreen.ai/mcp/) in plain words; it will give you the row, the source and the caveat, which is more than most invoices do.

*References*

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).
2. Elsworth et al., Measuring the environmental impact of delivering AI at Google Scale, Google, August 2025: 0.24 Wh, 0.03 gCO2e and 0.26 mL per median Gemini Apps text prompt; accelerators 58 percent; narrow boundary 0.10 Wh. [arXiv 2508.15734](https://arxiv.org/abs/2508.15734).
3. Mistral AI, Our contribution to a global environmental standard for AI, July 2025 (with Carbone 4 and ADEME): 1.14 gCO2e and 45 mL per 400-token reply. [mistral.ai](https://mistral.ai/news/our-contribution-to-a-global-environmental-standard-for-ai).
4. Per-answer figures are Wh per million output tokens multiplied by the row's own average output length; the LED bulb (10 W) is a stated assumption. Every row: [the index](https://leadgreen.ai/index/) and [the API](https://leadgreen.ai/api/).
