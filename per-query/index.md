# How much energy does an AI query use?

> An AI query uses about 0.24 to 0.34 Wh by Google's, Epoch AI's and OpenAI's whole-stack figures; the GPU share on this index is 0.005 to 0.21 Wh an answer.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/per-query/ (this file: https://leadgreen.ai/per-query/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[The index](https://leadgreen.ai/index/) · Per query*

An AI chatbot query uses about **0.24 to 0.34 Wh** of electricity across the whole serving stack, by the three published whole-stack figures: Google 0.24 Wh per median Gemini Apps text prompt (August 2025), Epoch AI 0.3 Wh per typical 500-token ChatGPT reply (February 2025) and OpenAI 0.34 Wh per average query (June 2025). The GPU share of one answer on this index runs from **0.005 to 0.21 Wh** by model and GPU, measured on busy servers. One answer from a busy open-weight model costs about **0.040 Wh** of GPU energy on the index's reference row (Qwen 3 32B on 2 × H100: 63.5 Wh per million output tokens, answers averaging 634 tokens, 256 requests in flight). Of Google's 0.24 Wh the accelerators are 58 percent, and its narrow accelerator-only figure is 0.10 Wh. The gap between a per-prompt figure and a per-million-tokens figure is boundary, load and answer length, and this page converts one into the other with each of them stated.

**Units** watt-hours per answer (Wh) and watt-hours per million output tokens (Wh/M). Wh per answer = Wh/M × output tokens ÷ 1,000,000. **Data** [index.json](https://leadgreen.ai/api/v1/index.json), [per-query.json](https://leadgreen.ai/api/v1/per-query.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. How much energy does an AI query use? Per prompt against per million tokens. https://leadgreen.ai/per-query/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [The bridge](https://leadgreen.ai/per-query/#bridge)
- [What vendors published](https://leadgreen.ai/per-query/#published)
- [Batch size one](https://leadgreen.ai/per-query/#batch-one)
- [To a budget](https://leadgreen.ai/per-query/#budget)
- [Questions](https://leadgreen.ai/per-query/#faq)
- [Sources](https://leadgreen.ai/per-query/#sources)

- **One answer, reference row:** 0.040 Wh Qwen 3 32B, 2 × H100, 63.5 Wh/M × 634 output tokens. GPU only, busy server, a floor.
- **Google, median prompt:** 0.24 Wh Gemini Apps text prompt, August 2025, whole stack: accelerators 58 percent (0.14 Wh), narrow accelerator-only figure 0.10 Wh.
- **AI Energy Score, one query:** 0.0042 to 1.27 Wh 22 models, batch size 1, answers fixed at ten tokens, H100 80GB, December 2025 round. A probe, not a serving load.

Three kinds of figure are quoted as "the energy of an AI query", and they do not share a boundary or a load. The index's rows are GPU energy per million output tokens from a busy server. Vendors' per-prompt figures count a whole serving estate. The AI Energy Score runs one query at a time with a fixed ten-token answer. Each is a real measurement; the table below puts the first kind in per-answer units so it can sit beside the others.

*The bridge*

## From watt-hours per million tokens to watt-hours per answer

Energy per answer is energy per token times the answer's length. Each row below takes a measured Wh/M figure and the average output length the benchmark recorded on that row, and multiplies them. The result is what one average answer on that row cost in GPU energy.

*Measured rows converted to GPU watt-hours per answer, using each row's own average output length*

| Row | Model | GPUs | Running batch | Wh / M | Output tokens | Wh per answer |
|---|---|---|---|---|---|---|
| Index, lowest row | [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 1 × B200 | 2,043 | 13.0 | 396 | 0.005 |
| Index, reference row | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 2 × H100 | 256 | 63.5 | 634 | 0.040 |
| Same row, lightly loaded | [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 2 × H100 | 8 | 452.0 | 631 | 0.285 |
| Index, highest row | [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 8 × H100 | 255 | 572.9 | 367 | 0.210 |
| Highest configuration measured | [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/) | 8 × B200 | 8 | 6,073.4 | 363 | 2.207 |

Running batch is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`). The first four rows are index rows or ladder rows at or under the 500 ms median inter-token latency ceiling; the last is the highest-energy configuration the leaderboard measured at all, kept to show the range a lightly loaded large model can reach. A kilowatt-hour serves about 24,800 answers at the reference row.

*What vendors published*

## Two per-prompt disclosures, and what they count

In August 2025 Google put the median Gemini Apps text prompt at **0.24 Wh**, 0.03 g CO2e and 0.26 mL of water. The figure counts the whole serving stack: the accelerators are 58 percent of it, about 0.14 Wh, and the host machines, idle capacity held for peaks and the data centre's overhead make up the rest. Google also reports a narrow, accelerator-only figure of 0.10 Wh, which is the boundary this index uses. So Google's own numbers say the stack multiplies the accelerator figure by 1.7× to 2.4×, depending on which accelerator figure is the base.

In July 2025 Mistral put a 400-token reply from its large model at 1.14 g CO2e and 45 mL of water, without a watt-hour figure, so it cannot be placed on an energy axis at all.

Neither disclosure states the model's serving load or the prompt's output length, so neither converts to watt-hours per million tokens. Set beside the index on the narrow boundary, Google's 0.10 Wh is 2.5× the reference row's 0.040 Wh answer; the rest of the difference is a different model, a different load and an unstated answer length. Google's figure tells a hyperscaler's customers what a prompt costs across its estate. The index tells a buyer what a named model on named GPUs costs at a stated load, which is the figure a vendor can be held to because the buyer can measure it.

*Batch size one*

## The AI Energy Score measures a probe, not a serving load

The AI Energy Score reports GPU watt-hours for 1,000 text-generation queries run one at a time on NVIDIA H100 80GB GPUs, with the answer fixed at ten tokens for non-reasoning models. Per query, its 22 December 2025 rows run from 0.0042 Wh (tencent/Hunyuan-1.8B-Instruct) to 1.27 Wh (zai-org/GLM-4.6). The index carries all of them in their own unit and does not convert them.

*AI Energy Score, text generation, December 2025 round, by class*

| Class | Fits | Models | Wh per 1,000 queries | Wh per query |
|---|---|---|---|---|
| A | fits one consumer GPU | 12 | 4.2 to 81.8 | 0.0042 to 0.082 |
| B | fits one H100 (single cloud GPU) | 3 | 37.4 to 54.5 | 0.0374 to 0.054 |
| C | needs more than one H100 (multiple cloud GPUs) | 7 | 36.6 to 1,273.5 | 0.0366 to 1.274 |

Dividing a batch-size-one figure by its ten tokens gives an energy per token for a card that is mostly waiting (tencent/Hunyuan-1.8B-Instruct would read 420 Wh/M), which is why the index refuses the conversion. Every row, with its star rating, is on [the index](https://leadgreen.ai/index/#per-query) and in [per-query.json](https://leadgreen.ai/api/v1/per-query.json).

*To a budget*

## Per answer is for intuition; per million tokens is for the plan

A per-answer figure makes the number legible: 0.040 Wh is a 10 W LED bulb for about 14 seconds (the bulb is a stated assumption, the tokens are measured). A budget needs the per-token form, because tokens are what the invoice counts. Monthly output tokens × Wh/M gives watt-hours; at the reference row a megawatt-hour of GPU energy serves 15.8 billion output tokens, and at the top of the concurrency ladder the same megawatt-hour serves 2.2 billion.

To take either figure to the facility meter, multiply by the system-to-GPU power ratio (1.79 for a DGX B200) and the site's PUE; with a PUE of 1.3 the reference row's 63.5 Wh/M becomes about 148 Wh/M at the meter. Both multipliers are the operator's own. The [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/) entry explains what sits inside and outside each figure.

*Questions*

## Asked about the energy of one query

### How much energy does an AI query use?

About 0.24 to 0.34 Wh across the whole serving stack, by the published figures from Google (0.24 Wh, August 2025), Epoch AI (0.3 Wh, February 2025) and OpenAI (0.34 Wh, June 2025). Below that headline it depends on the model, the GPUs, how busy the server is and how long the answer runs, so a single figure needs those four stated. On the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, 256 requests in flight), one answer of 634 tokens costs about 0.040 Wh of GPU energy. The same model on the same cards holding 8 requests costs about 0.29 Wh an answer. Google's published median for a Gemini Apps text prompt is 0.24 Wh across the whole serving stack (August 2025). These figures are GPU energy from a busy server unless stated otherwise; host, network and cooling sit outside them.

### Why is Google's 0.24 Wh per prompt higher than the index's figure?

Mostly boundary. Google counts the whole stack: the accelerators are 58 percent of its 0.24 Wh, about 0.14 Wh, with host machines, idle capacity held for peaks and data-centre overhead making up the rest, and it also publishes a narrow accelerator-only figure of 0.10 Wh. The index counts GPU energy only, at steady state on a busy server. On the narrow boundary Google's prompt is 2.5× the reference row's answer, and the two measure different models, loads and answer lengths. Neither figure is wrong; they answer different questions.

### How do I convert watt-hours per prompt into watt-hours per million tokens?

Divide the energy per answer by the answer's output tokens and multiply by a million: Wh/M = Wh per answer ÷ output tokens × 1,000,000. The reverse is Wh per answer = Wh/M × output tokens ÷ 1,000,000; the reference row's 63.5 Wh/M × 634 tokens gives 0.040 Wh. The conversion only holds when both figures share a boundary and a load. A per-prompt figure with no output length cannot be converted; Google's 0.24 Wh would read 378 Wh/M at the reference row's answer length and 158 Wh/M on its narrow boundary, but Google does not publish the prompt's token count, so those are illustrations, not figures.

### Can the AI Energy Score's Wh per 1,000 queries be converted to Wh per million tokens?

No. The AI Energy Score runs one query at a time (batch size 1) with the answer fixed at ten tokens for non-reasoning models, so the arithmetic (tencent/Hunyuan-1.8B-Instruct: 4.2 Wh per 1,000 queries ÷ 1,000 ÷ 10 tokens × 1,000,000 = 420 Wh/M) describes an idle card answering a ten-token probe, not a serving workload. The index keeps the AI Energy Score as a per-query measurement in its own table and does not mix the two units. The ML.ENERGY rows, measured on a busy server, are the ones in Wh/M.

### Does how busy the server is change the energy of one query?

More than anything else. Qwen 3 32B on 2 × H100 goes from 63.5 Wh/M at a running batch of 256 to 452 Wh/M at 8, 7.1× on the same hardware, because the cards draw only 39 percent more power serving 256 requests than 8. One answer goes from 0.040 Wh to about 0.29 Wh. A department assistant with a few users at a time sits at the top of that range.

### What about the carbon and water of one query?

Google puts the median Gemini Apps text prompt at 0.03 g CO2e and 0.26 mL of water (August 2025); Mistral puts a 400-token reply from its large model at 1.14 g CO2e and 45 mL (July 2025), without a watt-hour figure. For GPU-side carbon on the index, multiply Wh per answer by the grid's gCO2e per kWh: the reference row's answer carries about 0.028 g on Saudi Arabia's 2024 grid (689 gCO2e per kWh) and 0.0012 g on Norway's (30). The index measures electricity, not water.

*Sources*

## Where every figure came from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371). Per-answer figures are Wh per million output tokens multiplied by the row's own average output length.

Elsworth et al., Measuring the environmental impact of delivering AI at Google Scale, Google, August 2025: 0.24 Wh, 0.03 g CO2e and 0.26 mL per median Gemini Apps text prompt; accelerators 58 percent; narrow boundary 0.10 Wh. [arXiv 2508.15734](https://arxiv.org/abs/2508.15734), retrieved 26 September 2026. Mistral AI, Our contribution to a global environmental standard for AI, July 2025 (with Carbone 4 and ADEME): 1.14 g CO2e and 45 mL per 400-token reply. [mistral.ai](https://mistral.ai/news/our-contribution-to-a-global-environmental-standard-for-ai), retrieved 26 September 2026. Epoch AI, How much energy does ChatGPT use?, February 2025: about 0.3 Wh per typical 500-token GPT-4o reply, whole stack. [epoch.ai](https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use), retrieved 21 October 2026. Sam Altman, The Gentle Singularity, OpenAI, June 2025: about 0.34 Wh per average ChatGPT query, whole stack, no method given. [blog.samaltman.com](https://blog.samaltman.com/the-gentle-singularity), retrieved 21 October 2026.

[AI Energy Score leaderboard](https://huggingface.co/spaces/AIEnergyScore/Leaderboard) (AI Energy Score (Hugging Face and Salesforce, with Neuralwatt, Cohere, Meta and Carnegie Mellon University)), December 2025 round, retrieved 26 September 2026: GPU energy per 1,000 text-generation queries at batch size 1 on NVIDIA H100 80GB GPUs (one card for class A and B models, several for class C). Grid intensity in the carbon question: Ember, Yearly electricity data, October 2026 release, 2024.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
