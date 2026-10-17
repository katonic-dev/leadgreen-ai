# 18 open-weight models, one page each

> One page per model on the Green Tokens index: GPU watt-hours per million output tokens on H100 and B200, every measured load, and carbon by grid.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/models/ (this file: https://leadgreen.ai/models/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Models*

Every model on the Green Tokens index has its own page: the index row per GPU, every measured configuration from a running batch of eight upward, H100 against B200 where both were measured, carbon on a spread of grids, and the questions people ask about it. Every figure comes from the same dated snapshot as [the index](https://leadgreen.ai/index/).

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated 17 October 2026.

*Lowest index row first*

## Pick a model  B200 and H100

### [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/)13.0 Wh/M, 1 × B200

8 B parameters; 20 measured configurations. B200 and H100

### [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/)14.7 Wh/M, 1 × B200

8 B parameters; 19 measured configurations. B200 and H100

### [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/)15.2 Wh/M, 1 × B200

14 B parameters; 17 measured configurations. B200 and H100

### [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/)15.7 Wh/M, 1 × B200

30 B parameters, 3 B active; 31 measured configurations. B200 and H100

### [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/)26.5 Wh/M, 1 × B200

12 B parameters; 13 measured configurations. B200 and H100

### [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/)39.1 Wh/M, 1 × B200

32 B parameters; 22 measured configurations. B200 and H100

### [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/)39.4 Wh/M, 1 × B200

12 B parameters; 14 measured configurations. B200 and H100

### [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/)40.9 Wh/M, 1 × B200

9 B parameters; 14 measured configurations. B200 and H100

### [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/)49.1 Wh/M, 1 × B200

27 B parameters; 16 measured configurations. B200 and H100

### [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/)52.4 Wh/M, 2 × B200

70 B parameters; 22 measured configurations. B200 and H100

### [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/)60.7 Wh/M, 2 × B200

70 B parameters; 19 measured configurations. B200 and H100

### [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/)66.7 Wh/M, 4 × B200

235 B parameters, 22 B active; 31 measured configurations. H100

### [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/)93.4 Wh/M, 4 × H100

109 B parameters, 17 B active; 20 measured configurations. H100

### [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/)134.5 Wh/M, 8 × H100

400 B parameters, 17 B active; 9 measured configurations. B200 and H100

### [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/)139.1 Wh/M, 2 × B200

235 B parameters, 22 B active; 23 measured configurations. B200

### [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/)168.4 Wh/M, 8 × B200

671 B parameters, 37 B active; 11 measured configurations. B200

### [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/)282.0 Wh/M, 8 × B200

405 B parameters; 12 measured configurations. B200 and H100

### [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/)318.5 Wh/M, 4 × B200

405 B parameters; 15 measured configurations.

The figure on each card is the model's lowest index row across the GPUs it was measured on. Closed-weight models served over an API cannot be measured from outside and are not here. Source: ML.ENERGY Leaderboard v3.0 (data compiled 16 February 2026), Text Conversation, 328 stable configurations, retrieved 26 September 2026.
