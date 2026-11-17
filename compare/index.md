# Compare models on GPU energy per token: 9 pairs, side by side

> Llama 3.1 8B vs Llama 3.3 70B, Qwen 3 32B vs Llama 3.3 70B, FP8 vs BF16, dense vs MoE: nine model pairs on GPU energy per token.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/ (this file: https://leadgreen.ai/compare/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Compare*

The widest gap among these nine model pairs is **6.03×**: Llama 3.3 70B Instruct uses 117.5 Wh per million output tokens against 19.5 for Llama 3.1 8B Instruct on the H100 index rows, GPU only. The comparisons people ask for, each on one page: a small model against a large one, two families at the same size, dense against mixture of experts, FP8 against BF16, and two expert counts at the same active size. Every page sets the two models' index rows beside each other on each GPU both were measured on, states the card count and running batch behind each row, and says what explains the gap. The GPU generations themselves are compared on [H100 vs B200](https://leadgreen.ai/h100-vs-b200/).

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated 19 October 2026.

*Pairs*

## Pick a comparison  Two sizes · H100 and B200

### [Llama 3.1 8B Instruct vs Llama 3.3 70B Instruct](https://leadgreen.ai/compare/llama-3-1-8b-instruct-vs-llama-3-3-70b-instruct/)6.03× H100 index rows

Llama 3.3 70B Instruct over Llama 3.1 8B Instruct, GPU energy per output token; 4.68× on the B200. Two sizes · H100 and B200

### [Llama 3.3 70B Instruct vs Llama 3.1 405B Instruct FP8](https://leadgreen.ai/compare/llama-3-3-70b-instruct-vs-llama-3-1-405b-instruct-fp8/)4.88× H100 index rows

Llama 3.1 405B Instruct FP8 over Llama 3.3 70B Instruct, GPU energy per output token; 5.25× on the B200. Two families, two sizes · H100 and B200

### [Qwen 3 32B vs Llama 3.3 70B Instruct](https://leadgreen.ai/compare/qwen-3-32b-vs-llama-3-3-70b-instruct/)1.85× H100 index rows

Llama 3.3 70B Instruct over Qwen 3 32B, GPU energy per output token; 1.55× on the B200. Two mixture-of-experts sizes · B200

### [Qwen 3 235B A22B Instruct vs DeepSeek V3.1](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-vs-deepseek-v3-1/)2.52× B200 index rows

DeepSeek V3.1 over Qwen 3 235B A22B Instruct, GPU energy per output token. Dense against mixture of experts · H100 and B200

### [Qwen 3 30B A3B Instruct vs Qwen 3 32B](https://leadgreen.ai/compare/qwen-3-30b-a3b-instruct-vs-qwen-3-32b/)2.57× H100 index rows

Qwen 3 32B over Qwen 3 30B A3B Instruct, GPU energy per output token; 2.49× on the B200. Two precisions · H100 and B200

### [Qwen 3 235B A22B Instruct FP8 vs Qwen 3 235B A22B Instruct](https://leadgreen.ai/compare/qwen-3-235b-a22b-instruct-fp8-vs-qwen-3-235b-a22b-instruct/)1.47× H100 index rows

Qwen 3 235B A22B Instruct over Qwen 3 235B A22B Instruct FP8, GPU energy per output token; 0.48× on the B200. Two precisions · B200

### [Llama 3.1 405B Instruct FP8 vs Llama 3.1 405B Instruct](https://leadgreen.ai/compare/llama-3-1-405b-instruct-fp8-vs-llama-3-1-405b-instruct/)0.89× B200 index rows

Llama 3.1 405B Instruct over Llama 3.1 405B Instruct FP8, GPU energy per output token. Two families, one size · H100 and B200

### [Qwen 3 8B vs Llama 3.1 8B Instruct](https://leadgreen.ai/compare/qwen-3-8b-vs-llama-3-1-8b-instruct/)0.97× H100 index rows

Llama 3.1 8B Instruct over Qwen 3 8B, GPU energy per output token; 0.88× on the B200. Two expert counts · H100

### [Llama 4 Scout 17B 16E Instruct vs Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/compare/llama-4-scout-17b-16e-instruct-vs-llama-4-maverick-17b-128e-instruct-fp8/)1.44× H100 index rows

Llama 4 Maverick 17B 128E Instruct FP8 over Llama 4 Scout 17B 16E Instruct, GPU energy per output token.

The ratio on each card is the second model's energy per token over the first's, on the GPU named, at the index rows; under 1 means the second model's row is the lower one. Any other pair can be read off [the model pages](https://leadgreen.ai/models/) or asked of the [MCP server](https://leadgreen.ai/mcp/). Source: ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026), Text Conversation, retrieved 26 September 2026. The terms behind every figure are [energy per token](https://leadgreen.ai/glossary/energy-per-token/) and [running batch](https://leadgreen.ai/glossary/running-batch/).

*Questions*

## Asked about comparing models

### Which LLM uses the least energy per token?

On the index, Llama 3.1 8B Instruct on 1 × B200: 13.0 Wh per million output tokens, GPU only, at the most energy-efficient configuration measured for it. The highest row is Llama 3.1 405B Instruct FP8 on 8 × H100 at 572.9 Wh/M. Both are floors on a busy server, and the ranking covers the 18 models the index holds, not every model that exists.

### Does a larger model always use more energy per token?

Usually, but size is not the whole story. Llama 3.3 70B Instruct uses 6.03× the GPU energy per output token of Llama 3.1 8B Instruct on the H100 index rows, while the mixture-of-experts Qwen 3 30B A3B Instruct sits below the dense Qwen 3 32B at a similar total size: 24.7 against 63.5 Wh/M on the H100. Card count and running batch differ between the rows of every pair, and each page states both.

### How do I compare two models that are not paired here?

Every model has a page with all of its measured configurations, and the JSON API carries the same rows, so any two can be set side by side on the same GPU; the MCP server answers the same question in plain words. Read the card count and the running batch beside each figure, because load moves energy per token more than most differences between models do.

Cite this page: Lead Green, a Katonic project. Compare LLMs on energy per token: 9 model pairs, side by side. https://leadgreen.ai/compare/, release 2026-10-19, retrieved [date]. CC BY 4.0.
