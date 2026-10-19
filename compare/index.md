# 9 model pairs, side by side

> Model pairs people ask about, side by side on GPU energy per output token: small against large, dense against MoE, FP8 against BF16, two families.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/compare/ (this file: https://leadgreen.ai/compare/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Compare*

The comparisons people ask for, each on one page: a small model against a large one, two families at the same size, dense against mixture of experts, FP8 against BF16, and two expert counts at the same active size. Every page sets the two models' index rows beside each other on each GPU both were measured on, states the card count and running batch behind each row, and says what explains the gap. The GPU generations themselves are compared on [H100 vs B200](https://leadgreen.ai/h100-vs-b200/).

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated 18 October 2026.

Cite this page: Lead Green, a Katonic project. Compare: 9 model pairs on GPU energy per million output tokens. https://leadgreen.ai/compare/, release 2026-10-18, retrieved [date]. CC BY 4.0.

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

The ratio on each card is the second model's energy per token over the first's, on the GPU named, at the index rows; under 1 means the second model's row is the lower one. Any other pair can be read off [the model pages](https://leadgreen.ai/models/) or asked of the [MCP server](https://leadgreen.ai/mcp/). Source: ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026), Text Conversation, retrieved 26 September 2026.
