# Every question the site answers

> Every question the site answers, from 63 pages: energy per AI query, Wh per million tokens, carbon by grid, H100 against B200, the regulator.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/faq/ (this file: https://leadgreen.ai/faq/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Questions*

330 questions from 63 pages, each with the first sentence of its answer and a link to the page that holds the full answer, the figure and the source. The questions are the ones people type: how much energy an AI query uses, what a million tokens costs in watt-hours, which grid is cleaner, what the regulator asks.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. FAQ: 330 questions about GPU energy per token, answered with sources. https://leadgreen.ai/faq/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [Lead Green](https://leadgreen.ai/faq/#lead-green)
- [Why it matters](https://leadgreen.ai/faq/#why-it-matters)
- [AI energy in an RFP](https://leadgreen.ai/faq/#ai-energy-in-an-rfp)
- [Per query](https://leadgreen.ai/faq/#per-query)
- [H100 vs B200](https://leadgreen.ai/faq/#h100-vs-b200)
- [Llama 3.1 8B Instruct vs Llama 3.3 70B Instruct](https://leadgreen.ai/faq/#llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct)
- [Llama 3.3 70B Instruct vs Llama 3.1 405B Instruct FP8](https://leadgreen.ai/faq/#llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8)
- [Qwen 3 32B vs Llama 3.3 70B Instruct](https://leadgreen.ai/faq/#qwen-3-32b-vs-llama-3-3-70b-instruct)
- [Qwen 3 235B A22B Instruct vs DeepSeek V3.1](https://leadgreen.ai/faq/#qwen-3-235b-a22b-instruct-vs-deepseek-v3-1)
- [Qwen 3 30B A3B Instruct vs Qwen 3 32B](https://leadgreen.ai/faq/#qwen-3-30b-a3b-instruct-vs-qwen-3-32b)
- [Qwen 3 235B A22B Instruct FP8 vs Qwen 3 235B A22B Instruct](https://leadgreen.ai/faq/#qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct)
- [Llama 3.1 405B Instruct FP8 vs Llama 3.1 405B Instruct](https://leadgreen.ai/faq/#llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct)
- [Qwen 3 8B vs Llama 3.1 8B Instruct](https://leadgreen.ai/faq/#qwen-3-8b-vs-llama-3-1-8b-instruct)
- [Models](https://leadgreen.ai/faq/#models)
- [Grids](https://leadgreen.ai/faq/#grids)

Each page's questions are also published as FAQPage structured data on that page, so an assistant that reads one page gets the full answers; this hub is the human index of them. The glossary defines the terms the answers use.

*5 questions*

## [Lead Green](https://leadgreen.ai/)

### What is Lead Green?

A public index of LLM inference energy per token: the GPU watt-hours it takes to serve a million output tokens, by model, GPU and configuration, with the grid carbon to price it anywhere. [Full answer](https://leadgreen.ai/#faq)

### What unit does the index use?

Watt-hours per million output tokens (Wh/M); one Wh/M is 0.0036 joules per token. [Full answer](https://leadgreen.ai/#faq)

### Where do the figures come from?

Energy per token from the ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026); grid carbon intensity from Ember's yearly electricity data (October 2026 release, 2024); GPU power ceilings from NVIDIA's... [Full answer](https://leadgreen.ai/#faq)

### Is the data open, and how do I get it?

Yes. The compilation and site text are CC BY 4.0 and the sources keep their own licences. [Full answer](https://leadgreen.ai/#faq)

### Who runs and pays for Lead Green?

Lead Green is run and paid for by Katonic, which sells a sovereign AI platform and benefits when buyers ask the questions on this site. [Full answer](https://leadgreen.ai/#faq)

*5 questions*

## [Why it matters](https://leadgreen.ai/why/)

### Does the EU AI Act require reporting the energy used by AI inference?

Not per inference. Regulation (EU) 2024/1689 requires providers of general-purpose AI models to keep technical documentation for the AI Office, and Annex XI, section 1, point 2(e) names the model's known or estimated energy consumption: a... [Full answer](https://leadgreen.ai/why/#faq)

### Which line of ESRS E1 does AI inference energy go on?

For GPUs you run, the electricity is energy consumption from own operations under ESRS E1-5 (paragraph 37) and its emissions are Scope 2 under E1-6, location-based and market-based. [Full answer](https://leadgreen.ai/why/#faq)

### Why does an idle GPU use more energy per token than a busy one?

Because the cards' power does not fall in step with their work. [Full answer](https://leadgreen.ai/why/#faq)

### Does where I run AI change its energy per token?

No; it changes the carbon. The same tokens on the same GPUs use the same energy anywhere. [Full answer](https://leadgreen.ai/why/#faq)

### Is the electricity for AI inference expensive?

No, and that is the point. At the reference row and USD 0.10 per kWh the electricity costs about 0.6 cents per million tokens at the floor; a lightly loaded server pays several times that. [Full answer](https://leadgreen.ai/why/#faq)

*6 questions*

## [AI energy in an RFP](https://leadgreen.ai/rfp/)

### How do I put AI energy efficiency in an RFP?

Ask every bidder for the same figure at the same load: GPU energy per million output tokens (Wh/M) for each proposed model and serving configuration, measured at steady state on the proposed hardware at a stated average running batch, with... [Full answer](https://leadgreen.ai/rfp/#faq)

### What unit should an RFP use for AI energy?

GPU watt-hours per million output tokens (Wh/M), GPU energy only, at a stated running batch and latency. [Full answer](https://leadgreen.ai/rfp/#faq)

### What running batch and latency should the RFP specify?

The running batch you expect in production, as a number [N], and the median [T] and p99 [T99] inter-token latency your users will accept, the same for every bidder. [Full answer](https://leadgreen.ai/rfp/#faq)

### How do I score a bidder's energy figure?

Gate first: an answer counts only if it carries the figure, the cap and running batch held, median and p99 latency, output tokens per response, tokens per second, average GPU power, the method, the tool, the versions, the date and the... [Full answer](https://leadgreen.ai/rfp/#faq)

### Can I ask a hosted API provider for energy per token?

Yes, as a fleet-average figure over the preceding quarter at the fleet's actual utilisation, with the boundary stated, the serving regions and their grids named, the sites' PUE and host-to-GPU power ratio given, the rule that allocates a... [Full answer](https://leadgreen.ai/rfp/#faq)

### Is PUE enough to compare AI vendors on energy?

No. Power usage effectiveness is the building's overhead on top of the IT load; it says nothing about how much work the IT load does. [Full answer](https://leadgreen.ai/rfp/#faq)

*6 questions*

## [Per query](https://leadgreen.ai/per-query/)

### How much energy does an AI query use?

About 0.24 to 0.34 Wh across the whole serving stack, by the published figures from Google (0.24 Wh, August 2025), Epoch AI (0.3 Wh, February 2025), OpenAI (0.34 Wh, June 2025) and Microsoft Research (0.31 Wh, a modelled median for a... [Full answer](https://leadgreen.ai/per-query/#faq)

### Why is Google's 0.24 Wh per prompt higher than the index's figure?

Mostly boundary. Google counts the whole stack: the accelerators are 58 percent of its 0.24 Wh, about 0.14 Wh, with host machines, idle capacity held for peaks and data-centre overhead making up the rest, and it also publishes a narrow... [Full answer](https://leadgreen.ai/per-query/#faq)

### How do I convert watt-hours per prompt into watt-hours per million tokens?

Divide the energy per answer by the answer's output tokens and multiply by a million: Wh/M = Wh per answer ÷ output tokens × 1,000,000. [Full answer](https://leadgreen.ai/per-query/#faq)

### Can the AI Energy Score's Wh per 1,000 queries be converted to Wh per million tokens?

No. The AI Energy Score runs one query at a time (batch size 1) with the answer fixed at ten tokens for non-reasoning models, so the arithmetic (tencent/Hunyuan-1.8B-Instruct: 4.2 Wh per 1,000 queries ÷ 1,000 ÷ 10 tokens × 1,000,000 = 420... [Full answer](https://leadgreen.ai/per-query/#faq)

### Does how busy the server is change the energy of one query?

More than anything else. Qwen 3 32B on 2 × H100 goes from 63.5 Wh/M at a running batch of 256 to 452 Wh/M at 8, 7.1× on the same hardware, because the cards draw only 39 percent more power serving 256 requests than 8. [Full answer](https://leadgreen.ai/per-query/#faq)

### What about the carbon and water of one query?

Google puts the median Gemini Apps text prompt at 0.03 g CO2e and 0.26 mL of water (August 2025); Mistral puts a 400-token reply from its large model at 1.14 g CO2e and 45 mL (July 2025), without a watt-hour figure. [Full answer](https://leadgreen.ai/per-query/#faq)

*6 questions*

## [H100 vs B200](https://leadgreen.ai/h100-vs-b200/)

### Is the B200 more energy-efficient than the H100 for LLM inference?

On the ML.ENERGY Leaderboard's index rows, yes for all 14 models measured on both: [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

### How much energy does a B200 save over an H100 per million tokens?

It depends on the model: for the reference model, Qwen 3 32B, the index rows are 63.5 Wh/M on 2 × H100 against 39.1 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

### Does the B200 draw more power than the H100?

A B200 card draws more power than an H100: NVIDIA rates the H100 SXM at up to 700 W and the B200 configurable up to 1,000 W, and on these index rows the cards averaged 612 W per H100 and 868 W per B200. [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

### Should I buy B200s to cut the energy of AI inference?

Not first. The same model on the same H100 cards moves 7.1× in energy per token between a running batch of 8 and 256, which is more than the widest generation gap here (4.55×). [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

### Why do the two rows of a pair have different card counts?

The leaderboard picks each GPU's configurations separately; a B200 has more memory, so a model that needs eight H100s can fit fewer B200s. [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/h100-vs-b200/#faq)

*5 questions*

## [Llama 3.1 8B Instruct vs Llama 3.3 70B Instruct](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/)

### Is Llama 3.1 8B Instruct more energy-efficient than Llama 3.3 70B Instruct?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.3 70B Instruct uses 6.03× the GPU energy per output token of Llama 3.1 8B Instruct on the H100 (117.5 against 19.5 Wh per million output tokens) and 4.68× the GPU... [Full answer](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/#faq)

### How much more energy does Llama 3.3 70B Instruct use per million tokens than Llama 3.1 8B Instruct?

The index rows differ by 98.0 Wh/M on the H100 (98.0 kWh per billion tokens) and 47.7 Wh/M on the B200 (47.7 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/#faq)

### Does the bigger model cost more per answer?

Yes, at these rows: on the H100, 0.008 Wh for Llama 3.1 8B Instruct against 0.049 Wh for Llama 3.3 70B Instruct, using each row's own average output length (397 and 413 tokens). [Full answer](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/#faq)

*5 questions*

## [Llama 3.3 70B Instruct vs Llama 3.1 405B Instruct FP8](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/)

### Is Llama 3.3 70B Instruct more energy-efficient than Llama 3.1 405B Instruct FP8?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 405B Instruct FP8 uses 4.88× the GPU energy per output token of Llama 3.3 70B Instruct on the H100 (572.9 against 117.5 Wh per million output tokens) and 5.25× the... [Full answer](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)

### How much more energy does Llama 3.1 405B Instruct FP8 use per million tokens than Llama 3.3 70B Instruct?

The index rows differ by 455.4 Wh/M on the H100 (455.4 kWh per billion tokens) and 257.8 Wh/M on the B200 (257.8 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)

### Does the bigger model cost more per answer?

Yes, at these rows: on the H100, 0.049 Wh for Llama 3.3 70B Instruct against 0.210 Wh for Llama 3.1 405B Instruct FP8, using each row's own average output length (413 and 367 tokens). [Full answer](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/#faq)

*5 questions*

## [Qwen 3 32B vs Llama 3.3 70B Instruct](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/)

### Is Qwen 3 32B more energy-efficient than Llama 3.3 70B Instruct?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.3 70B Instruct uses 1.85× the GPU energy per output token of Qwen 3 32B on the H100 (117.5 against 63.5 Wh per million output tokens) and 1.55× the GPU energy per... [Full answer](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)

### How much more energy does Llama 3.3 70B Instruct use per million tokens than Qwen 3 32B?

The index rows differ by 54.1 Wh/M on the H100 (54.1 kWh per billion tokens) and 21.7 Wh/M on the B200 (21.7 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)

### Does Llama 3.3 70B Instruct cost more per answer than Qwen 3 32B?

At these rows, on the H100: 0.040 Wh for Qwen 3 32B against 0.049 Wh for Llama 3.3 70B Instruct, using each row's own average output length (634 and 413 tokens). [Full answer](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/#faq)

*5 questions*

## [Qwen 3 235B A22B Instruct vs DeepSeek V3.1](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/)

### Is Qwen 3 235B A22B Instruct more energy-efficient than DeepSeek V3.1?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, DeepSeek V3.1 uses 2.52× the GPU energy per output token of Qwen 3 235B A22B Instruct on the B200 (168.4 against 66.7 Wh per million output tokens). [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)

### How much more energy does DeepSeek V3.1 use per million tokens than Qwen 3 235B A22B Instruct?

The index rows differ by 101.7 Wh/M on the B200 (101.7 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)

### Does the larger mixture-of-experts model cost more energy per token?

On the B200 index rows, yes: DeepSeek V3.1 (37 B active of 671 B) uses 2.52× the GPU energy per output token of Qwen 3 235B A22B Instruct (22 B active of 235 B), 168.4 against 66.7 Wh/M, on 8 and 4 cards at running batches of 3,008 and... [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/#faq)

*5 questions*

## [Qwen 3 30B A3B Instruct vs Qwen 3 32B](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/)

### Is Qwen 3 30B A3B Instruct more energy-efficient than Qwen 3 32B?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Qwen 3 32B uses 2.57× the GPU energy per output token of Qwen 3 30B A3B Instruct on the H100 (63.5 against 24.7 Wh per million output tokens) and 2.49× the GPU energy per... [Full answer](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)

### How much more energy does Qwen 3 32B use per million tokens than Qwen 3 30B A3B Instruct?

The index rows differ by 38.8 Wh/M on the H100 (38.8 kWh per billion tokens) and 23.4 Wh/M on the B200 (23.4 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)

### Does a mixture-of-experts model use less energy per token than a dense one?

At a similar total size, on these rows, yes: Qwen 3 30B A3B Instruct activates 3 B of 30 B parameters per token and its H100 index row uses 24.7 Wh/M against 63.5 for the dense Qwen 3 32B (32 B), 0.39× less. [Full answer](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/#faq)

*5 questions*

## [Qwen 3 235B A22B Instruct FP8 vs Qwen 3 235B A22B Instruct](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/)

### Is Qwen 3 235B A22B Instruct FP8 more energy-efficient than Qwen 3 235B A22B Instruct?

It depends on the GPU: on the ML.ENERGY Leaderboard's index rows, Qwen 3 235B A22B Instruct uses 1.47× the GPU energy per output token of Qwen 3 235B A22B Instruct FP8 on the H100 (303.5 against 206.0 Wh per million output tokens) and... [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/#faq)

### How much more energy does Qwen 3 235B A22B Instruct use per million tokens than Qwen 3 235B A22B Instruct FP8?

The index rows differ by 97.6 Wh/M on the H100 (97.6 kWh per billion tokens) and 72.3 Wh/M on the B200 (72.3 kWh per billion tokens); where the ratio is under 1, Qwen 3 235B A22B Instruct is the lower row. [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/#faq)

### Does FP8 save energy compared with BF16 for the same model?

Not consistently on these index rows. On the H100 the FP8 row (Qwen 3 235B A22B Instruct FP8) uses 206.0 Wh/M on 8 cards at a running batch of 511 and the BF16 row 303.5 Wh/M on 8 at 228; on the B200 the FP8 row (Qwen 3 235B A22B Instruct... [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/#faq)

*5 questions*

## [Llama 3.1 405B Instruct FP8 vs Llama 3.1 405B Instruct](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/)

### Is Llama 3.1 405B Instruct FP8 more energy-efficient than Llama 3.1 405B Instruct?

No, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 405B Instruct uses 0.89× the GPU energy per output token of Llama 3.1 405B Instruct FP8 on the B200 (282.0 against 318.5 Wh per million output tokens). [Full answer](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)

### How much more energy does Llama 3.1 405B Instruct use per million tokens than Llama 3.1 405B Instruct FP8?

The index rows differ by 36.6 Wh/M on the B200 (36.6 kWh per billion tokens); where the ratio is under 1, Llama 3.1 405B Instruct is the lower row. [Full answer](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)

### Does FP8 save energy compared with BF16 for the same model?

Not on these index rows. On the B200 the FP8 row (Llama 3.1 405B Instruct FP8) uses 318.5 Wh/M on 4 cards at a running batch of 510 and the BF16 row 282.0 Wh/M on 8 at 3,589. [Full answer](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/#faq)

*5 questions*

## [Qwen 3 8B vs Llama 3.1 8B Instruct](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/)

### Is Qwen 3 8B more energy-efficient than Llama 3.1 8B Instruct?

No, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 3.1 8B Instruct uses 0.97× the GPU energy per output token of Qwen 3 8B on the H100 (19.5 against 20.0 Wh per million output tokens) and 0.88× the GPU energy per output... [Full answer](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)

### How much more energy does Llama 3.1 8B Instruct use per million tokens than Qwen 3 8B?

The index rows differ by 0.5 Wh/M on the H100 (0.5 kWh per billion tokens) and 1.8 Wh/M on the B200 (1.8 kWh per billion tokens); where the ratio is under 1, Llama 3.1 8B Instruct is the lower row. [Full answer](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)

### Why do two models of the same size differ in energy per token?

Architecture (depth, width, attention design), vocabulary and, on the leaderboard, the configuration swept for each model: card count, cap and the running batch actually reached. [Full answer](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/#faq)

*5 questions*

## [Llama 4 Scout 17B 16E Instruct vs Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/)

### Is Llama 4 Scout 17B 16E Instruct more energy-efficient than Llama 4 Maverick 17B 128E Instruct FP8?

Yes, on these rows: on the ML.ENERGY Leaderboard's index rows, Llama 4 Maverick 17B 128E Instruct FP8 uses 1.44× the GPU energy per output token of Llama 4 Scout 17B 16E Instruct on the H100 (134.5 against 93.4 Wh per million output... [Full answer](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)

### How much more energy does Llama 4 Maverick 17B 128E Instruct FP8 use per million tokens than Llama 4 Scout 17B 16E Instruct?

The index rows differ by 41.1 Wh/M on the H100 (41.1 kWh per billion tokens). [Full answer](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)

### Do more experts cost more energy per token at the same active parameters?

On these rows, yes: with 17 B active parameters each, Llama 4 Maverick 17B 128E Instruct FP8 (400 B in all) uses 1.44× the GPU energy per output token of Llama 4 Scout 17B 16E Instruct (109 B) on the H100, 134.5 against 93.4 Wh/M. [Full answer](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)

### Why are the two rows not like for like?

The leaderboard sweeps each model separately: card count, the cap on requests in flight and the precision are chosen per model, and the running batch actually reached differs. [Full answer](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026, retrieved 26 September 2026), Text Conversation task, GPU energy measured with Zeus under vLLM on H100 80GB HBM3 and B200 servers; each row is the lowest-energy configuration... [Full answer](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/#faq)

*4 questions*

## [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)

### What does Wh/M mean?

Watt-hours per million output tokens: the GPU energy a serving configuration uses to generate a million output tokens. [Full answer](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#faq)

### How do I convert joules per token to watt-hours per million tokens?

Multiply joules per token by 1,000,000 and divide by 3,600. The reference row's 0.2285 J per token becomes 63.5 Wh/M. [Full answer](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#faq)

### Is Wh per million tokens the same as kWh per billion tokens?

Yes, and the same as MWh per trillion tokens; the three scale together. [Full answer](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#faq)

### Does the unit include the prompt?

The energy includes prompt processing, because the benchmark divides steady-state GPU energy by the output tokens generated in the window; the denominator counts output tokens only. [Full answer](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/#faq)

*4 questions*

## [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)

### What is energy per token?

GPU energy divided by the output tokens generated in the same steady-state window, in joules per output token. [Full answer](https://leadgreen.ai/glossary/energy-per-token/#faq)

### How is energy per token measured?

By reading the GPU's energy counter (through NVML or DCGM; the leaderboard uses Zeus) at the start and end of a steady-state window under a fixed load, and dividing the difference by the output tokens generated in that window. [Full answer](https://leadgreen.ai/glossary/energy-per-token/#faq)

### Why do estimates of energy per token differ so much from measurements?

Estimates multiply a rated power by an assumed utilisation and divide by an assumed throughput, usually a single request at a time. [Full answer](https://leadgreen.ai/glossary/energy-per-token/#faq)

### Does energy per token include the host, the network and cooling?

Not on this index. The figures are GPU energy only. A whole-system reading adds the host, memory, network and fans (about 1.79× for a DGX B200, from NVIDIA's rated system and GPU power), and the facility's PUE adds cooling and distribution... [Full answer](https://leadgreen.ai/glossary/energy-per-token/#faq)

*5 questions*

## [Running batch](https://leadgreen.ai/glossary/running-batch/)

### What is running batch?

The average number of requests a serving engine was decoding at once over the measurement window (vLLM's num_requests_running). [Full answer](https://leadgreen.ai/glossary/running-batch/#faq)

### Is running batch the same as continuous batching?

Continuous batching, also called in-flight batching, is the scheduling: requests join and leave the batch at every decode step instead of waiting for a fixed group to finish. [Full answer](https://leadgreen.ai/glossary/running-batch/#faq)

### Why does an idle GPU use more energy per token than a busy one?

Because a GPU's power does not fall in step with its work. On the index, Qwen 3 32B on 2 × H100 draws 850 W serving 8 requests at once and 1,178 W serving 256, 39 percent more power for 9.9× the tokens per second. [Full answer](https://leadgreen.ai/glossary/running-batch/#faq)

### What is the difference between running batch and batch size?

Batch size is usually a configured limit (the cap, vLLM's max_num_seqs) or a fixed count in an offline benchmark. [Full answer](https://leadgreen.ai/glossary/running-batch/#faq)

### What running batch should I ask a vendor to measure at?

The one you expect in production, stated as a number, with the median and p99 inter-token latency your users will accept. [Full answer](https://leadgreen.ai/glossary/running-batch/#faq)

*4 questions*

## [Floor](https://leadgreen.ai/glossary/floor/)

### What does the index mean by a floor?

The lowest GPU energy per output token measured for a model and GPU among configurations at or under a 500 ms median inter-token latency, at high concurrency. [Full answer](https://leadgreen.ai/glossary/floor/#faq)

### Is the floor what my deployment will use?

No. It is the best measured configuration on a busy server, GPU only. [Full answer](https://leadgreen.ai/glossary/floor/#faq)

### What should I do with a vendor figure below the floor?

Ask for the measurement: the running batch held, the latency over the window, the method, the tool and the logs. [Full answer](https://leadgreen.ai/glossary/floor/#faq)

### Does the floor change if the latency ceiling changes?

It can. At 500 ms, the leaderboard's default, no measured configuration is excluded. [Full answer](https://leadgreen.ai/glossary/floor/#faq)

*4 questions*

## [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)

### What does GPU-only mean on the index?

That the energy was read from the GPU devices alone over a steady-state window. [Full answer](https://leadgreen.ai/glossary/gpu-only-boundary/#faq)

### How do I take a GPU-only figure to the facility meter?

Multiply by the system-to-GPU power ratio (1.79 for a DGX B200: 14.3 kW rated against 8.0 kW of GPUs) and by the site's PUE. [Full answer](https://leadgreen.ai/glossary/gpu-only-boundary/#faq)

### Why not publish whole-system figures?

Because they cannot be compared across vendors or sites: the host, the fans and the cooling design differ with every server and building, while the GPU figure for a named model on a named card at a stated load can be measured anywhere. [Full answer](https://leadgreen.ai/glossary/gpu-only-boundary/#faq)

### Does the boundary include the energy of processing the prompt?

Yes. The benchmark divides steady-state GPU energy, which includes prefill, by the output tokens generated; the prompt's tokens are not in the denominator. [Full answer](https://leadgreen.ai/glossary/gpu-only-boundary/#faq)

*4 questions*

## [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)

### What is location-based grid carbon intensity?

The average carbon intensity of the electricity generated where the load runs, in gCO2e per kWh, before contracts or certificates. [Full answer](https://leadgreen.ai/glossary/location-based-intensity/#faq)

### What is the difference between location-based and market-based?

Location-based uses the average intensity of the grid where the electricity was consumed. [Full answer](https://leadgreen.ai/glossary/location-based-intensity/#faq)

### How much does location change the carbon of AI inference?

On the reference row, 23× between Saudi Arabia (43.7 kg CO2e per billion tokens) and Norway (1.9 kg), 2024 averages. [Full answer](https://leadgreen.ai/glossary/location-based-intensity/#faq)

### Can I file Ember's figure in my Scope 2 report?

Use it for comparison, not as the filed factor. It is a lifecycle, production-based figure on net generation, not a Scope 2 combustion factor, and it is an annual average that a round-the-clock GPU load does not follow hour by hour. [Full answer](https://leadgreen.ai/glossary/location-based-intensity/#faq)

*4 questions*

## [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)

### How much CO2 does a million AI tokens produce?

On the index's reference row (Qwen 3 32B, 2 × H100, 63.5 Wh per million output tokens, GPU only), about 43.7 g CO2e per million tokens on Saudi Arabia's 2024 grid, 44.9 g on India's, 30.0 g on the world average and 1.9 g on Norway's. [Full answer](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#faq)

### How do I calculate kg CO2e per billion tokens?

Multiply watt-hours per million output tokens by the grid's gCO2e per kWh and divide by 1,000. [Full answer](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#faq)

### Why are some published figures thousands of times higher?

Usually because they start from an estimate of energy per token for a single request at a time, or from a whole-stack figure, and then multiply by a grid factor. [Full answer](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#faq)

### Is this a Scope 2 figure?

It is a location-based GPU-side figure for comparison. GPUs you run put their electricity in your own Scope 2 (ESRS E1-6, location-based matches this method; market-based needs your contracts). [Full answer](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/#faq)

*4 questions*

## [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)

### What is the inter-token latency ceiling on the index?

A median inter-token latency of at most 500 ms, the ML.ENERGY Leaderboard's default for every LLM task. [Full answer](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#faq)

### What is inter-token latency?

The time between one output token and the next for a single request while the model is generating, usually reported as a median and a p99 over a window. [Full answer](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#faq)

### Would a stricter latency limit change the index?

Yes. At 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B... [Full answer](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#faq)

### Why state a latency ceiling with an energy figure at all?

Because energy per token falls as the running batch rises and latency rises with it; a figure without its latency can be made arbitrarily good by loading the server until users wait. [Full answer](https://leadgreen.ai/glossary/inter-token-latency-ceiling/#faq)

*4 questions*

## [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

### What is PUE?

Power usage effectiveness: a data centre's total facility energy divided by the energy delivered to its IT equipment, per ISO/IEC 30134-2. [Full answer](https://leadgreen.ai/glossary/pue/#faq)

### How do I use PUE with watt-hours per million tokens?

Multiply the GPU figure by the system-to-GPU power ratio and by the PUE. [Full answer](https://leadgreen.ai/glossary/pue/#faq)

### Does a low PUE mean efficient AI inference?

No. PUE measures the building's overhead, not the work the GPUs did. [Full answer](https://leadgreen.ai/glossary/pue/#faq)

### Which regulation asks for PUE?

In the EU, the Energy Efficiency Directive (EU) 2023/1791, Article 12, with Commission Delegated Regulation (EU) 2024/1364: data centres with an installed IT power demand of at least 500 kW report facility indicators including PUE. [Full answer](https://leadgreen.ai/glossary/pue/#faq)

*6 questions*

## [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/)

### How much energy does Llama 3.1 8B Instruct use per million output tokens?

Llama 3.1 8B Instruct uses 13.0 Wh of GPU energy per million output tokens on 1 × B200 and 19.5 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

### Is Llama 3.1 8B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.50× the energy per token of the B200 configuration: 19.5 Wh/M on 1 × H100 against 13.0 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

### How much does load change the energy per token of Llama 3.1 8B Instruct?

On 1 × H100, energy per token falls 6.5× between a running batch of 8 (126.3 Wh/M) and 511 (19.5 Wh/M), because the cards' power rises only 41 percent while throughput rises 9.2×. [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Llama 3.1 8B Instruct?

A billion output tokens of Llama 3.1 8B Instruct on 1 × B200 at its index row carries about 8.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

### Is this the energy my Llama 3.1 8B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 20 stable configurations of Llama 3.1 8B Instruct measured with Zeus under vLLM on H100 80GB... [Full answer](https://leadgreen.ai/models/llama-3-1-8b-instruct/#faq)

*7 questions*

## [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/)

### How much energy does Qwen 3 8B use per million output tokens?

Qwen 3 8B uses 14.7 Wh of GPU energy per million output tokens on 1 × B200 and 20.0 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation... [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### Is Qwen 3 8B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.36× the energy per token of the B200 configuration: 20.0 Wh/M on 1 × H100 against 14.7 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### How much does load change the energy per token of Qwen 3 8B?

On 1 × H100, energy per token falls 6.2× between a running batch of 8 (123.3 Wh/M) and 474 (20.0 Wh/M), because the cards' power rises only 44 percent while throughput rises 8.9×. [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 8B?

A billion output tokens of Qwen 3 8B on 1 × B200 at its index row carries about 10.2 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.4 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### Does Qwen 3 8B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 8B costs 38.3× the energy per response and 3.06× the energy per token on 1 × H100 (answers of 8,052 tokens against 645; running batch 82 against 474) and 40.6× the energy per response and... [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### Is this the energy my Qwen 3 8B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 19 stable configurations of Qwen 3 8B measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/qwen-3-8b/#faq)

*7 questions*

## [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/)

### How much energy does Qwen 3 14B use per million output tokens?

Qwen 3 14B uses 15.2 Wh of GPU energy per million output tokens on 1 × B200 and 31.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation... [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### Is Qwen 3 14B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 2.04× the energy per token of the B200 configuration: 31.1 Wh/M on 1 × H100 against 15.2 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### How much does load change the energy per token of Qwen 3 14B?

On 1 × B200, energy per token falls 12.8× between a running batch of 8 (194.3 Wh/M) and 2,045 (15.2 Wh/M), because the cards' power rises only 14 percent while throughput rises 14.6×. [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 14B?

A billion output tokens of Qwen 3 14B on 1 × B200 at its index row carries about 10.5 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### Does Qwen 3 14B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 14B costs 26.8× the energy per response and 2.50× the energy per token on 1 × H100 (answers of 6,711 tokens against 625; running batch 59 against 253) and 39.8× the energy per response and... [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### Is this the energy my Qwen 3 14B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 17 stable configurations of Qwen 3 14B measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/qwen-3-14b/#faq)

*6 questions*

## [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/)

### How much energy does Qwen 3 30B A3B Instruct use per million output tokens?

Qwen 3 30B A3B Instruct uses 15.7 Wh of GPU energy per million output tokens on 1 × B200 and 24.7 Wh of GPU energy per million output tokens on 2 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

### Is Qwen 3 30B A3B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.58× the energy per token of the B200 configuration: 24.7 Wh/M on 2 × H100 against 15.7 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

### How much does load change the energy per token of Qwen 3 30B A3B Instruct?

On 2 × H100, energy per token falls 9.3× between a running batch of 8 (228.6 Wh/M) and 1,019 (24.7 Wh/M), because the cards' power rises only 64 percent while throughput rises 15.2×. [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 30B A3B Instruct?

A billion output tokens of Qwen 3 30B A3B Instruct on 1 × B200 at its index row carries about 10.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.5 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

### Is this the energy my Qwen 3 30B A3B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 31 stable configurations of Qwen 3 30B A3B Instruct measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/#faq)

*6 questions*

## [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/)

### How much energy does Gemma 3 12B use per million output tokens?

Gemma 3 12B uses 26.5 Wh of GPU energy per million output tokens on 1 × B200 and 46.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

### Is Gemma 3 12B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.74× the energy per token of the B200 configuration: 46.1 Wh/M on 1 × H100 against 26.5 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

### How much does load change the energy per token of Gemma 3 12B?

On 1 × B200, energy per token falls 7.0× between a running batch of 8 (185.9 Wh/M) and 487 (26.5 Wh/M), because the cards' power rises only 39 percent while throughput rises 9.8×. [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

### What is the carbon footprint of a billion tokens of Gemma 3 12B?

A billion output tokens of Gemma 3 12B on 1 × B200 at its index row carries about 18.3 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 0.8 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

### Is this the energy my Gemma 3 12B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 13 stable configurations of Gemma 3 12B measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/gemma-3-12b/#faq)

*7 questions*

## [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/)

### How much energy does Qwen 3 32B use per million output tokens?

Qwen 3 32B uses 39.1 Wh of GPU energy per million output tokens on 1 × B200 and 63.5 Wh of GPU energy per million output tokens on 2 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation... [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### Is Qwen 3 32B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.63× the energy per token of the B200 configuration: 63.5 Wh/M on 2 × H100 against 39.1 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### How much does load change the energy per token of Qwen 3 32B?

On 1 × B200, energy per token falls 11.0× between a running batch of 8 (429.2 Wh/M) and 383 (39.1 Wh/M), because the cards' power rises only 13 percent while throughput rises 12.4×. [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 32B?

A billion output tokens of Qwen 3 32B on 1 × B200 at its index row carries about 26.9 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### Does Qwen 3 32B use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, Qwen 3 32B costs 24.6× the energy per response and 2.22× the energy per token on 1 × B200 (answers of 7,035 tokens against 635; running batch 111 against 383) and 26.1× the energy per response and... [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### Is this the energy my Qwen 3 32B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 22 stable configurations of Qwen 3 32B measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/qwen-3-32b/#faq)

*7 questions*

## [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/)

### How much energy does NVIDIA Nemotron Nano 12B V2 use per million output tokens?

NVIDIA Nemotron Nano 12B V2 uses 39.4 Wh of GPU energy per million output tokens on 1 × B200 and 50.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### Is NVIDIA Nemotron Nano 12B V2 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.27× the energy per token of the B200 configuration: 50.1 Wh/M on 1 × H100 against 39.4 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### How much does load change the energy per token of NVIDIA Nemotron Nano 12B V2?

On 1 × H100, energy per token falls 4.1× between a running batch of 8 (207.6 Wh/M) and 241 (50.1 Wh/M), because the cards' power rises only 39 percent while throughput rises 5.8×. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### What is the carbon footprint of a billion tokens of NVIDIA Nemotron Nano 12B V2?

A billion output tokens of NVIDIA Nemotron Nano 12B V2 on 1 × B200 at its index row carries about 27.2 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### Does NVIDIA Nemotron Nano 12B V2 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 12B V2 costs 3.9× the energy per response and 1.02× the energy per token on 1 × B200 (answers of 5,646 tokens against 1,464; running batch 256 against 256) and 8.7× the energy... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### Is this the energy my NVIDIA Nemotron Nano 12B V2 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 14 stable configurations of NVIDIA Nemotron Nano 12B V2 measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/#faq)

*7 questions*

## [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/)

### How much energy does NVIDIA Nemotron Nano 9B V2 use per million output tokens?

NVIDIA Nemotron Nano 9B V2 uses 40.9 Wh of GPU energy per million output tokens on 1 × B200 and 43.1 Wh of GPU energy per million output tokens on 1 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### Is NVIDIA Nemotron Nano 9B V2 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.05× the energy per token of the B200 configuration: 43.1 Wh/M on 1 × H100 against 40.9 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### How much does load change the energy per token of NVIDIA Nemotron Nano 9B V2?

On 1 × H100, energy per token falls 3.8× between a running batch of 8 (162.7 Wh/M) and 255 (43.1 Wh/M), because the cards' power rises only 48 percent while throughput rises 5.6×. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### What is the carbon footprint of a billion tokens of NVIDIA Nemotron Nano 9B V2?

A billion output tokens of NVIDIA Nemotron Nano 9B V2 on 1 × B200 at its index row carries about 28.2 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.2 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### Does NVIDIA Nemotron Nano 9B V2 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, NVIDIA Nemotron Nano 9B V2 costs 3.4× the energy per response and 0.79× the energy per token on 1 × B200 (answers of 5,361 tokens against 1,242; running batch 512 against 255) and 7.6× the energy... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### Is this the energy my NVIDIA Nemotron Nano 9B V2 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 14 stable configurations of NVIDIA Nemotron Nano 9B V2 measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/#faq)

*6 questions*

## [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/)

### How much energy does Gemma 3 27B use per million output tokens?

Gemma 3 27B uses 49.1 Wh of GPU energy per million output tokens on 1 × B200 and 80.4 Wh of GPU energy per million output tokens on 2 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

### Is Gemma 3 27B more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.64× the energy per token of the B200 configuration: 80.4 Wh/M on 2 × H100 against 49.1 Wh/M on 1 × B200. [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

### How much does load change the energy per token of Gemma 3 27B?

On 2 × H100, energy per token falls 5.3× between a running batch of 8 (430.2 Wh/M) and 187 (80.4 Wh/M), because the cards' power rises only 49 percent while throughput rises 8.0×. [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

### What is the carbon footprint of a billion tokens of Gemma 3 27B?

A billion output tokens of Gemma 3 27B on 1 × B200 at its index row carries about 33.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.5 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

### Is this the energy my Gemma 3 27B deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 16 stable configurations of Gemma 3 27B measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/gemma-3-27b/#faq)

*6 questions*

## [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/)

### How much energy does Llama 3.1 70B Instruct use per million output tokens?

Llama 3.1 70B Instruct uses 52.4 Wh of GPU energy per million output tokens on 2 × B200 and 103.7 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

### Is Llama 3.1 70B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.98× the energy per token of the B200 configuration: 103.7 Wh/M on 4 × H100 against 52.4 Wh/M on 2 × B200. [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

### How much does load change the energy per token of Llama 3.1 70B Instruct?

On 4 × H100, energy per token falls 10.1× between a running batch of 8 (1,044.1 Wh/M) and 898 (103.7 Wh/M), because the cards' power rises only 44 percent while throughput rises 14.5×. [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Llama 3.1 70B Instruct?

A billion output tokens of Llama 3.1 70B Instruct on 2 × B200 at its index row carries about 36.1 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.6 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

### Is this the energy my Llama 3.1 70B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 22 stable configurations of Llama 3.1 70B Instruct measured with Zeus under vLLM on H100 80GB... [Full answer](https://leadgreen.ai/models/llama-3-1-70b-instruct/#faq)

*6 questions*

## [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/)

### How much energy does Llama 3.3 70B Instruct use per million output tokens?

Llama 3.3 70B Instruct uses 60.7 Wh of GPU energy per million output tokens on 2 × B200 and 117.5 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text... [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

### Is Llama 3.3 70B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.94× the energy per token of the B200 configuration: 117.5 Wh/M on 4 × H100 against 60.7 Wh/M on 2 × B200. [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

### How much does load change the energy per token of Llama 3.3 70B Instruct?

On 4 × H100, energy per token falls 9.1× between a running batch of 8 (1,068.6 Wh/M) and 724 (117.5 Wh/M), because the cards' power rises only 42 percent while throughput rises 13.0×. [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Llama 3.3 70B Instruct?

A billion output tokens of Llama 3.3 70B Instruct on 2 × B200 at its index row carries about 41.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 1.8 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

### Is this the energy my Llama 3.3 70B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 19 stable configurations of Llama 3.3 70B Instruct measured with Zeus under vLLM on H100 80GB... [Full answer](https://leadgreen.ai/models/llama-3-3-70b-instruct/#faq)

*6 questions*

## [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/)

### How much energy does Qwen 3 235B A22B Instruct use per million output tokens?

Qwen 3 235B A22B Instruct uses 66.7 Wh of GPU energy per million output tokens on 4 × B200 and 303.5 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0... [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

### Is Qwen 3 235B A22B Instruct more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 4.55× the energy per token of the B200 configuration: 303.5 Wh/M on 8 × H100 against 66.7 Wh/M on 4 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

### How much does load change the energy per token of Qwen 3 235B A22B Instruct?

On 4 × B200, energy per token falls 26.9× between a running batch of 8 (1,793.5 Wh/M) and 3,765 (66.7 Wh/M), because the cards' power rises only 25 percent while throughput rises 33.5×. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 235B A22B Instruct?

A billion output tokens of Qwen 3 235B A22B Instruct on 4 × B200 at its index row carries about 46.0 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 2.0 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

### Is this the energy my Qwen 3 235B A22B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 31 stable configurations of Qwen 3 235B A22B Instruct measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/#faq)

*5 questions*

## [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/)

### How much energy does Llama 4 Scout 17B 16E Instruct use per million output tokens?

Llama 4 Scout 17B 16E Instruct uses 93.4 Wh of GPU energy per million output tokens on 4 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). [Full answer](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)

### How much does load change the energy per token of Llama 4 Scout 17B 16E Instruct?

On 4 × H100, energy per token falls 11.8× between a running batch of 8 (1,104.8 Wh/M) and 473 (93.4 Wh/M), because the cards' power rises only 47 percent while throughput rises 17.4×. [Full answer](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)

### What is the carbon footprint of a billion tokens of Llama 4 Scout 17B 16E Instruct?

A billion output tokens of Llama 4 Scout 17B 16E Instruct on 4 × H100 at its index row carries about 64.3 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 2.8 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)

### Is this the energy my Llama 4 Scout 17B 16E Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 20 stable configurations of Llama 4 Scout 17B 16E Instruct measured with Zeus under vLLM on... [Full answer](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/#faq)

*5 questions*

## [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/)

### How much energy does Llama 4 Maverick 17B 128E Instruct FP8 use per million output tokens?

Llama 4 Maverick 17B 128E Instruct FP8 uses 134.5 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). [Full answer](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)

### How much does load change the energy per token of Llama 4 Maverick 17B 128E Instruct FP8?

On 8 × H100, energy per token falls 5.8× between a running batch of 8 (779.0 Wh/M) and 383 (134.5 Wh/M), because the cards' power rises only 88 percent while throughput rises 10.9×. [Full answer](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)

### What is the carbon footprint of a billion tokens of Llama 4 Maverick 17B 128E Instruct FP8?

A billion output tokens of Llama 4 Maverick 17B 128E Instruct FP8 on 8 × H100 at its index row carries about 92.7 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.0 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)

### Is this the energy my Llama 4 Maverick 17B 128E Instruct FP8 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 9 stable configurations of Llama 4 Maverick 17B 128E Instruct FP8 measured with Zeus under... [Full answer](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/#faq)

*6 questions*

## [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/)

### How much energy does Qwen 3 235B A22B Instruct FP8 use per million output tokens?

Qwen 3 235B A22B Instruct FP8 uses 139.1 Wh of GPU energy per million output tokens on 2 × B200 and 206.0 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard... [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

### Is Qwen 3 235B A22B Instruct FP8 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.48× the energy per token of the B200 configuration: 206.0 Wh/M on 8 × H100 against 139.1 Wh/M on 2 × B200. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

### How much does load change the energy per token of Qwen 3 235B A22B Instruct FP8?

On 8 × H100, energy per token falls 15.4× between a running batch of 8 (3,163.8 Wh/M) and 511 (206.0 Wh/M), because the cards' power rises only 10 percent while throughput rises 16.9×. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

### What is the carbon footprint of a billion tokens of Qwen 3 235B A22B Instruct FP8?

A billion output tokens of Qwen 3 235B A22B Instruct FP8 on 2 × B200 at its index row carries about 95.8 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 4.1 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

### Is this the energy my Qwen 3 235B A22B Instruct FP8 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 23 stable configurations of Qwen 3 235B A22B Instruct FP8 measured with Zeus under vLLM on... [Full answer](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/#faq)

*6 questions*

## [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/)

### How much energy does DeepSeek V3.1 use per million output tokens?

DeepSeek V3.1 uses 168.4 Wh of GPU energy per million output tokens on 8 × B200 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

### How much does load change the energy per token of DeepSeek V3.1?

On 8 × B200, energy per token falls 14.1× between a running batch of 8 (2,379.3 Wh/M) and 3,008 (168.4 Wh/M), because the cards' power rises only 42 percent while throughput rises 20.1×. [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

### What is the carbon footprint of a billion tokens of DeepSeek V3.1?

A billion output tokens of DeepSeek V3.1 on 8 × B200 at its index row carries about 116.1 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 5.0 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

### Does DeepSeek V3.1 use more energy for reasoning or problem-solving tasks?

On the leaderboard's Problem Solving task, DeepSeek V3.1 costs 23.5× the energy per response and 2.20× the energy per token on 8 × B200 (answers of 8,969 tokens against 842; running batch 256 against 3,008), compared with Text Conversation. [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

### Is this the energy my DeepSeek V3.1 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 11 stable configurations of DeepSeek V3.1 measured with Zeus under vLLM on H100 80GB and B200... [Full answer](https://leadgreen.ai/models/deepseek-v3-1/#faq)

*5 questions*

## [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/)

### How much energy does Llama 3.1 405B Instruct use per million output tokens?

Llama 3.1 405B Instruct uses 282.0 Wh of GPU energy per million output tokens on 8 × B200 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0, Text Conversation, data compiled 16 February 2026). [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)

### How much does load change the energy per token of Llama 3.1 405B Instruct?

On 8 × B200, energy per token falls 21.5× between a running batch of 8 (6,073.4 Wh/M) and 3,589 (282.0 Wh/M), because the cards' power rises only 28 percent while throughput rises 27.6×. [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)

### What is the carbon footprint of a billion tokens of Llama 3.1 405B Instruct?

A billion output tokens of Llama 3.1 405B Instruct on 8 × B200 at its index row carries about 194.3 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 8.4 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)

### Is this the energy my Llama 3.1 405B Instruct deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 12 stable configurations of Llama 3.1 405B Instruct measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct/#faq)

*6 questions*

## [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/)

### How much energy does Llama 3.1 405B Instruct FP8 use per million output tokens?

Llama 3.1 405B Instruct FP8 uses 318.5 Wh of GPU energy per million output tokens on 4 × B200 and 572.9 Wh of GPU energy per million output tokens on 8 × H100 at the most energy-efficient configuration measured (ML.ENERGY Leaderboard v3.0... [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

### Is Llama 3.1 405B Instruct FP8 more energy-efficient on B200 or H100?

On the index rows, the H100 configuration uses 1.80× the energy per token of the B200 configuration: 572.9 Wh/M on 8 × H100 against 318.5 Wh/M on 4 × B200. [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

### How much does load change the energy per token of Llama 3.1 405B Instruct FP8?

On 8 × H100, energy per token falls 6.8× between a running batch of 8 (3,881.9 Wh/M) and 255 (572.9 Wh/M), because the cards' power rises only 50 percent while throughput rises 10.1×. [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

### What is the carbon footprint of a billion tokens of Llama 3.1 405B Instruct FP8?

A billion output tokens of Llama 3.1 405B Instruct FP8 on 4 × B200 at its index row carries about 219.5 kg CO2e of GPU-side emissions on the Saudi grid (689 gCO2e per kWh, Ember 2024) and 9.4 kg on the Norwegian grid (30). [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

### Is this the energy my Llama 3.1 405B Instruct FP8 deployment will use?

No. Every figure here is the lowest-energy configuration under the leaderboard's 500 ms median inter-token latency ceiling, on a busy server, GPU only. [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

### Where do these figures come from?

The ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative), released 1 December 2025, data compiled 16 February 2026, retrieved 26 September 2026: 15 stable configurations of Llama 3.1 405B Instruct FP8 measured with Zeus under vLLM on H100... [Full answer](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/#faq)

*5 questions*

## [India](https://leadgreen.ai/grids/india/)

### What is the grid carbon intensity of India?

707 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.5× the world average of 473. [Full answer](https://leadgreen.ai/grids/india/#faq)

### How much CO2 does a million AI tokens produce in India?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 44.9 grams of CO2e per million tokens, or 44.9 kg per billion, on India's 2024 grid. [Full answer](https://leadgreen.ai/grids/india/#faq)

### Is running AI in India cleaner than the world average?

India's 2024 intensity of 707 gCO2e per kWh is 1.5× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/india/#faq)

### Can I use this figure for my Scope 2 report in India?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/india/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/india/#faq)

*5 questions*

## [Saudi Arabia](https://leadgreen.ai/grids/saudi-arabia/)

### What is the grid carbon intensity of Saudi Arabia?

689 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.5× the world average of 473. [Full answer](https://leadgreen.ai/grids/saudi-arabia/#faq)

### How much CO2 does a million AI tokens produce in Saudi Arabia?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 43.7 grams of CO2e per million tokens, or 43.7 kg per billion, on Saudi Arabia's 2024 grid. [Full answer](https://leadgreen.ai/grids/saudi-arabia/#faq)

### Is running AI in Saudi Arabia cleaner than the world average?

Saudi Arabia's 2024 intensity of 689 gCO2e per kWh is 1.5× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/saudi-arabia/#faq)

### Can I use this figure for my Scope 2 report in Saudi Arabia?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/saudi-arabia/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/saudi-arabia/#faq)

*5 questions*

## [Hong Kong](https://leadgreen.ai/grids/hong-kong/)

### What is the grid carbon intensity of Hong Kong?

676 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.4× the world average of 473. [Full answer](https://leadgreen.ai/grids/hong-kong/#faq)

### How much CO2 does a million AI tokens produce in Hong Kong?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 42.9 grams of CO2e per million tokens, or 42.9 kg per billion, on Hong Kong's 2024 grid. [Full answer](https://leadgreen.ai/grids/hong-kong/#faq)

### Is running AI in Hong Kong cleaner than the world average?

Hong Kong's 2024 intensity of 676 gCO2e per kWh is 1.4× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/hong-kong/#faq)

### Can I use this figure for my Scope 2 report in Hong Kong?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/hong-kong/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/hong-kong/#faq)

*5 questions*

## [Serbia](https://leadgreen.ai/grids/serbia/)

### What is the grid carbon intensity of Serbia?

668 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.4× the world average of 473. [Full answer](https://leadgreen.ai/grids/serbia/#faq)

### How much CO2 does a million AI tokens produce in Serbia?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 42.4 grams of CO2e per million tokens, or 42.4 kg per billion, on Serbia's 2024 grid. [Full answer](https://leadgreen.ai/grids/serbia/#faq)

### Is running AI in Serbia cleaner than the world average?

Serbia's 2024 intensity of 668 gCO2e per kWh is 1.4× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/serbia/#faq)

### Can I use this figure for my Scope 2 report in Serbia?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/serbia/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/serbia/#faq)

*5 questions*

## [Taiwan](https://leadgreen.ai/grids/taiwan/)

### What is the grid carbon intensity of Taiwan?

635 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.3× the world average of 473. [Full answer](https://leadgreen.ai/grids/taiwan/#faq)

### How much CO2 does a million AI tokens produce in Taiwan?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 40.3 grams of CO2e per million tokens, or 40.3 kg per billion, on Taiwan's 2024 grid. [Full answer](https://leadgreen.ai/grids/taiwan/#faq)

### Is running AI in Taiwan cleaner than the world average?

Taiwan's 2024 intensity of 635 gCO2e per kWh is 1.3× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/taiwan/#faq)

### Can I use this figure for my Scope 2 report in Taiwan?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/taiwan/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/taiwan/#faq)

*5 questions*

## [The Philippines](https://leadgreen.ai/grids/the-philippines/)

### What is the grid carbon intensity of The Philippines?

629 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.3× the world average of 473. [Full answer](https://leadgreen.ai/grids/the-philippines/#faq)

### How much CO2 does a million AI tokens produce in The Philippines?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 40.0 grams of CO2e per million tokens, or 40.0 kg per billion, on The Philippines's 2024 grid. [Full answer](https://leadgreen.ai/grids/the-philippines/#faq)

### Is running AI in The Philippines cleaner than the world average?

The Philippines's 2024 intensity of 629 gCO2e per kWh is 1.3× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/the-philippines/#faq)

### Can I use this figure for my Scope 2 report in The Philippines?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/the-philippines/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/the-philippines/#faq)

*5 questions*

## [Qatar](https://leadgreen.ai/grids/qatar/)

### What is the grid carbon intensity of Qatar?

582 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.2× the world average of 473. [Full answer](https://leadgreen.ai/grids/qatar/#faq)

### How much CO2 does a million AI tokens produce in Qatar?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 36.9 grams of CO2e per million tokens, or 36.9 kg per billion, on Qatar's 2024 grid. [Full answer](https://leadgreen.ai/grids/qatar/#faq)

### Is running AI in Qatar cleaner than the world average?

Qatar's 2024 intensity of 582 gCO2e per kWh is 1.2× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/qatar/#faq)

### Can I use this figure for my Scope 2 report in Qatar?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/qatar/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/qatar/#faq)

*5 questions*

## [Australia](https://leadgreen.ai/grids/australia/)

### What is the grid carbon intensity of Australia?

549 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.2× the world average of 473. [Full answer](https://leadgreen.ai/grids/australia/#faq)

### How much CO2 does a million AI tokens produce in Australia?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 34.9 grams of CO2e per million tokens, or 34.9 kg per billion, on Australia's 2024 grid. [Full answer](https://leadgreen.ai/grids/australia/#faq)

### Is running AI in Australia cleaner than the world average?

Australia's 2024 intensity of 549 gCO2e per kWh is 1.2× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/australia/#faq)

### Can I use this figure for my Scope 2 report in Australia?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/australia/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/australia/#faq)

*5 questions*

## [Singapore](https://leadgreen.ai/grids/singapore/)

### What is the grid carbon intensity of Singapore?

499 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.1× the world average of 473. [Full answer](https://leadgreen.ai/grids/singapore/#faq)

### How much CO2 does a million AI tokens produce in Singapore?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 31.6 grams of CO2e per million tokens, or 31.6 kg per billion, on Singapore's 2024 grid. [Full answer](https://leadgreen.ai/grids/singapore/#faq)

### Is running AI in Singapore cleaner than the world average?

Singapore's 2024 intensity of 499 gCO2e per kWh is 1.1× the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/singapore/#faq)

### Can I use this figure for my Scope 2 report in Singapore?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/singapore/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/singapore/#faq)

*5 questions*

## [Japan](https://leadgreen.ai/grids/japan/)

### What is the grid carbon intensity of Japan?

484 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, close to the world average of 473. [Full answer](https://leadgreen.ai/grids/japan/#faq)

### How much CO2 does a million AI tokens produce in Japan?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 30.7 grams of CO2e per million tokens, or 30.7 kg per billion, on Japan's 2024 grid. [Full answer](https://leadgreen.ai/grids/japan/#faq)

### Is running AI in Japan cleaner than the world average?

Japan's 2024 intensity of 484 gCO2e per kWh is close to the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/japan/#faq)

### Can I use this figure for my Scope 2 report in Japan?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/japan/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/japan/#faq)

*5 questions*

## [United Arab Emirates](https://leadgreen.ai/grids/united-arab-emirates/)

### What is the grid carbon intensity of United Arab Emirates?

477 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, close to the world average of 473. [Full answer](https://leadgreen.ai/grids/united-arab-emirates/#faq)

### How much CO2 does a million AI tokens produce in United Arab Emirates?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 30.3 grams of CO2e per million tokens, or 30.3 kg per billion, on United Arab Emirates's 2024 grid. [Full answer](https://leadgreen.ai/grids/united-arab-emirates/#faq)

### Is running AI in United Arab Emirates cleaner than the world average?

United Arab Emirates's 2024 intensity of 477 gCO2e per kWh is close to the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/united-arab-emirates/#faq)

### Can I use this figure for my Scope 2 report in United Arab Emirates?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/united-arab-emirates/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/united-arab-emirates/#faq)

*5 questions*

## [Sri Lanka](https://leadgreen.ai/grids/sri-lanka/)

### What is the grid carbon intensity of Sri Lanka?

393 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.2× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/sri-lanka/#faq)

### How much CO2 does a million AI tokens produce in Sri Lanka?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 24.9 grams of CO2e per million tokens, or 24.9 kg per billion, on Sri Lanka's 2024 grid. [Full answer](https://leadgreen.ai/grids/sri-lanka/#faq)

### Is running AI in Sri Lanka cleaner than the world average?

Sri Lanka's 2024 intensity of 393 gCO2e per kWh is 1.2× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/sri-lanka/#faq)

### Can I use this figure for my Scope 2 report in Sri Lanka?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/sri-lanka/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/sri-lanka/#faq)

*5 questions*

## [United States](https://leadgreen.ai/grids/united-states/)

### What is the grid carbon intensity of United States?

384 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.2× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/united-states/#faq)

### How much CO2 does a million AI tokens produce in United States?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 24.4 grams of CO2e per million tokens, or 24.4 kg per billion, on United States's 2024 grid. [Full answer](https://leadgreen.ai/grids/united-states/#faq)

### Is running AI in United States cleaner than the world average?

United States's 2024 intensity of 384 gCO2e per kWh is 1.2× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/united-states/#faq)

### Can I use this figure for my Scope 2 report in United States?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/united-states/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/united-states/#faq)

*5 questions*

## [Germany](https://leadgreen.ai/grids/germany/)

### What is the grid carbon intensity of Germany?

340 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.4× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/germany/#faq)

### How much CO2 does a million AI tokens produce in Germany?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 21.6 grams of CO2e per million tokens, or 21.6 kg per billion, on Germany's 2024 grid. [Full answer](https://leadgreen.ai/grids/germany/#faq)

### Is running AI in Germany cleaner than the world average?

Germany's 2024 intensity of 340 gCO2e per kWh is 1.4× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/germany/#faq)

### Can I use this figure for my Scope 2 report in Germany?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/germany/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/germany/#faq)

*5 questions*

## [Bulgaria](https://leadgreen.ai/grids/bulgaria/)

### What is the grid carbon intensity of Bulgaria?

279 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.7× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/bulgaria/#faq)

### How much CO2 does a million AI tokens produce in Bulgaria?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 17.7 grams of CO2e per million tokens, or 17.7 kg per billion, on Bulgaria's 2024 grid. [Full answer](https://leadgreen.ai/grids/bulgaria/#faq)

### Is running AI in Bulgaria cleaner than the world average?

Bulgaria's 2024 intensity of 279 gCO2e per kWh is 1.7× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/bulgaria/#faq)

### Can I use this figure for my Scope 2 report in Bulgaria?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/bulgaria/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/bulgaria/#faq)

*5 questions*

## [Ireland](https://leadgreen.ai/grids/ireland/)

### What is the grid carbon intensity of Ireland?

271 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 1.7× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/ireland/#faq)

### How much CO2 does a million AI tokens produce in Ireland?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 17.2 grams of CO2e per million tokens, or 17.2 kg per billion, on Ireland's 2024 grid. [Full answer](https://leadgreen.ai/grids/ireland/#faq)

### Is running AI in Ireland cleaner than the world average?

Ireland's 2024 intensity of 271 gCO2e per kWh is 1.7× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/ireland/#faq)

### Can I use this figure for my Scope 2 report in Ireland?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/ireland/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/ireland/#faq)

*5 questions*

## [United Kingdom](https://leadgreen.ai/grids/united-kingdom/)

### What is the grid carbon intensity of United Kingdom?

216 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 2.2× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/united-kingdom/#faq)

### How much CO2 does a million AI tokens produce in United Kingdom?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 13.7 grams of CO2e per million tokens, or 13.7 kg per billion, on United Kingdom's 2024 grid. [Full answer](https://leadgreen.ai/grids/united-kingdom/#faq)

### Is running AI in United Kingdom cleaner than the world average?

United Kingdom's 2024 intensity of 216 gCO2e per kWh is 2.2× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/united-kingdom/#faq)

### Can I use this figure for my Scope 2 report in United Kingdom?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/united-kingdom/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/united-kingdom/#faq)

*5 questions*

## [Hungary](https://leadgreen.ai/grids/hungary/)

### What is the grid carbon intensity of Hungary?

184 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 2.6× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/hungary/#faq)

### How much CO2 does a million AI tokens produce in Hungary?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 11.7 grams of CO2e per million tokens, or 11.7 kg per billion, on Hungary's 2024 grid. [Full answer](https://leadgreen.ai/grids/hungary/#faq)

### Is running AI in Hungary cleaner than the world average?

Hungary's 2024 intensity of 184 gCO2e per kWh is 2.6× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/hungary/#faq)

### Can I use this figure for my Scope 2 report in Hungary?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/hungary/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/hungary/#faq)

*5 questions*

## [New Zealand](https://leadgreen.ai/grids/new-zealand/)

### What is the grid carbon intensity of New Zealand?

112 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 4.2× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/new-zealand/#faq)

### How much CO2 does a million AI tokens produce in New Zealand?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 7.1 grams of CO2e per million tokens, or 7.1 kg per billion, on New Zealand's 2024 grid. [Full answer](https://leadgreen.ai/grids/new-zealand/#faq)

### Is running AI in New Zealand cleaner than the world average?

New Zealand's 2024 intensity of 112 gCO2e per kWh is 4.2× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/new-zealand/#faq)

### Can I use this figure for my Scope 2 report in New Zealand?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/new-zealand/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/new-zealand/#faq)

*5 questions*

## [Slovakia](https://leadgreen.ai/grids/slovakia/)

### What is the grid carbon intensity of Slovakia?

97 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 4.9× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/slovakia/#faq)

### How much CO2 does a million AI tokens produce in Slovakia?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 6.2 grams of CO2e per million tokens, or 6.2 kg per billion, on Slovakia's 2024 grid. [Full answer](https://leadgreen.ai/grids/slovakia/#faq)

### Is running AI in Slovakia cleaner than the world average?

Slovakia's 2024 intensity of 97 gCO2e per kWh is 4.9× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/slovakia/#faq)

### Can I use this figure for my Scope 2 report in Slovakia?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/slovakia/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/slovakia/#faq)

*5 questions*

## [France](https://leadgreen.ai/grids/france/)

### What is the grid carbon intensity of France?

40 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 11.7× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/france/#faq)

### How much CO2 does a million AI tokens produce in France?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 2.6 grams of CO2e per million tokens, or 2.6 kg per billion, on France's 2024 grid. [Full answer](https://leadgreen.ai/grids/france/#faq)

### Is running AI in France cleaner than the world average?

France's 2024 intensity of 40 gCO2e per kWh is 11.7× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/france/#faq)

### Can I use this figure for my Scope 2 report in France?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/france/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/france/#faq)

*5 questions*

## [Norway](https://leadgreen.ai/grids/norway/)

### What is the grid carbon intensity of Norway?

30 gCO2e per kWh in 2024, on Ember's yearly electricity data: a lifecycle, location-based figure for the country's own generation, 16.0× cleaner than the world average of 473. [Full answer](https://leadgreen.ai/grids/norway/#faq)

### How much CO2 does a million AI tokens produce in Norway?

At the index's reference row (Qwen 3 32B on 2 × H100, 63.5 Wh per million output tokens, GPU only), about 1.9 grams of CO2e per million tokens, or 1.9 kg per billion, on Norway's 2024 grid. [Full answer](https://leadgreen.ai/grids/norway/#faq)

### Is running AI in Norway cleaner than the world average?

Norway's 2024 intensity of 30 gCO2e per kWh is 16.0× cleaner than the world average of 473 (473 gCO2e per kWh). [Full answer](https://leadgreen.ai/grids/norway/#faq)

### Can I use this figure for my Scope 2 report in Norway?

As a comparison, not as a filing. Ember's intensity is a lifecycle figure on net generation, not a Scope 2 combustion factor, and it is location-based; a market-based figure needs your own contracted supply. [Full answer](https://leadgreen.ai/grids/norway/#faq)

### Where do these figures come from?

Grid intensity: Ember, Yearly electricity data, October 2026 release (2024; 2023, 2024, 2025 shown), CC BY 4.0, retrieved 17 October 2026. [Full answer](https://leadgreen.ai/grids/norway/#faq)
