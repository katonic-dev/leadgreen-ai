# Green Tokens

> GPU watt-hours per million output tokens by model, GPU and configuration, from public measurements, with concurrency curves, grid carbon and sources.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/index/ (this file: https://leadgreen.ai/index/index.md). Updated 18 October 2026, data version 2026-10-18. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*The index*

The GPU energy it takes to serve a million tokens, by model, GPU and configuration. Every figure is from a public measurement or a manufacturer's specification, and every source is listed at the foot of the page. Updated 18 October 2026.

Green here is a direction, not a verdict. This table ranks serving configurations by GPU energy per token and by nothing else.

**Unit** watt-hours per million output tokens (Wh/M). One Wh/M is 0.0036 joules per token. GPU only, busy server. Every row is a floor. The same data as [JSON](https://leadgreen.ai/api/) and through the [MCP server](https://leadgreen.ai/mcp/).

- [Index](https://leadgreen.ai/index/#index)
- [Two generations](https://leadgreen.ai/index/#generations)
- [Concurrency](https://leadgreen.ai/index/#concurrency)
- [Two tasks](https://leadgreen.ai/index/#workloads)
- [Carbon](https://leadgreen.ai/index/#carbon)
- [Hardware](https://leadgreen.ai/index/#hardware)
- [Per query](https://leadgreen.ai/index/#per-query)
- [Method](https://leadgreen.ai/index/#method)
- [Own measurements](https://leadgreen.ai/index/#own)
- [Contributed](https://leadgreen.ai/index/#contributed)
- [Cite as](https://leadgreen.ai/index/#cite)
- [Sources](https://leadgreen.ai/index/#sources)
- [Changes](https://leadgreen.ai/index/#changes)

-  **Lowest floor on the index:**  13.0 Wh/M  Llama 3.1 8B Instruct, 1 × B200. Running batch 2,043, median ITL 125 ms.
-  **Reference floor:**  63.5 Wh/M  Qwen 3 32B, 2 × H100. Running batch 256, median ITL 44 ms. The carbon table is priced on this row.
-  **Highest floor on the index:**  572.9 Wh/M  Llama 3.1 405B Instruct FP8, 8 × H100. Running batch 255, median ITL 67 ms.

A million output tokens is roughly three quarters of a million words of English. The index spans **44×** from its lowest row to its highest, and the same model on the same two GPUs moves **7.1×** depending on how busy the server is. Every row here is a floor. The number a buyer should ask for is the one measured on their own server.

*The index*

## Energy per million output tokens

32 rows, 18 open-weight models, two GPUs. Each row is the most energy-efficient configuration the ML.ENERGY benchmark found for that model on that GPU at or under a median inter-token latency of 500 ms, the leaderboard's own default ceiling, on its Text Conversation workload. No measured configuration reaches the ceiling (the highest median is 326 ms), so it selects nothing: each row is also the lowest-energy configuration for its model and GPU at any latency. Sorted from least energy to most.
