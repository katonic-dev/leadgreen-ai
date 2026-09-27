# Green Tokens

> GPU watt-hours per million output tokens by model, GPU and configuration, from public measurements, with concurrency curves, grid carbon and sources.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/index/ (this file: https://leadgreen.ai/index/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*The index*

The GPU energy it takes to serve a million tokens, by model, GPU and configuration. Every figure is from a public measurement or a manufacturer's specification, and every source is listed at the foot of the page. Updated 27 September 2026.

Green here is a direction, not a verdict. This table ranks serving configurations by GPU energy per token and by nothing else.

Unit watt-hours per million output tokens (Wh/M). One Wh/M is 0.0036 joules per token. GPU only, busy server. Every row is a floor. The same data as [JSON](https://leadgreen.ai/api/) and through the [MCP server](https://leadgreen.ai/mcp/).

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

-  Lowest floor on the index:  13.0 Wh/M  Llama 3.1 8B Instruct, 1 × B200. Running batch 2,043, median ITL 125 ms.
-  Reference floor:  63.5 Wh/M  Qwen 3 32B, 2 × H100. Running batch 256, median ITL 44 ms. The carbon table is priced on this row.
-  Highest floor on the index:  572.9 Wh/M  Llama 3.1 405B Instruct FP8, 8 × H100. Running batch 255, median ITL 67 ms.

A million output tokens is roughly three quarters of a million words of English. The index spans 44× from its lowest row to its highest, and the same model on the same two GPUs moves 7.1× depending on how busy the server is. Every row here is a floor. The number a buyer should ask for is the one measured on their own server.

*The index*

## Energy per million output tokens

32 rows, 18 open-weight models, two GPUs. Each row is the most energy-efficient configuration the ML.ENERGY benchmark found for that model on that GPU at or under a median inter-token latency of 500 ms, the leaderboard's own default ceiling, on its Text Conversation workload. No measured configuration reaches the ceiling (the highest median is 326 ms), so it selects nothing: each row is also the lowest-energy configuration for its model and GPU at any latency. Sorted from least energy to most.

*ML.ENERGY Leaderboard v3.0, Text Conversation, energy-optimal configuration per model and GPU at or under the leaderboard's default 500 ms median ITL ceiling*

| Model | Params (B) · weights | GPUs | Wh / M tokens | Median ITL (ms) | Running batch (avg) | GPU power, all cards (W) |
|---|---|---|---|---|---|---|
| [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 8 · BF16 | 1 × B200 | 13.0 | 125 | 2,043 | 691 |
| [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 8 · BF16 | 1 × B200 | 14.7 | 91 | 1,427 | 801 |
| [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/) | 14 · BF16 | 1 × B200 | 15.2 | 113 | 2,045 | 869 |
| [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 30 (3 active) · BF16 | 1 × B200 | 15.7 | 89 | 1,023 | 601 |
| [Llama 3.1 8B Instruct](https://leadgreen.ai/models/llama-3-1-8b-instruct/) | 8 · BF16 | 1 × H100 | 19.5 | 47 | 511 | 688 |
| [Qwen 3 8B](https://leadgreen.ai/models/qwen-3-8b/) | 8 · BF16 | 1 × H100 | 20.0 | 47 | 474 | 616 |
| [Qwen 3 30B A3B Instruct](https://leadgreen.ai/models/qwen-3-30b-a3b-instruct/) | 30 (3 active) · BF16 | 2 × H100 | 24.7 | 75 | 1,019 | 1,123 |
| [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/) | 12 · BF16 | 1 × B200 | 26.5 | 44 | 487 | 928 |
| [Qwen 3 14B](https://leadgreen.ai/models/qwen-3-14b/) | 14 · BF16 | 1 × H100 | 31.1 | 38 | 253 | 645 |
| [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 32 · BF16 | 1 × B200 | 39.1 | 50 | 383 | 972 |
| [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/) | 12 · BF16 | 1 × B200 | 39.4 | 34 | 256 | 885 |
| [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/) | 9 · BF16 | 1 × B200 | 40.9 | 41 | 255 | 800 |
| [NVIDIA Nemotron Nano 9B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-9b-v2/) | 9 · BF16 | 1 × H100 | 43.1 | 43 | 255 | 693 |
| [Gemma 3 12B](https://leadgreen.ai/models/gemma-3-12b/) | 12 · BF16 | 1 × H100 | 46.1 | 35 | 128 | 589 |
| [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/) | 27 · BF16 | 1 × B200 | 49.1 | 40 | 247 | 974 |
| [NVIDIA Nemotron Nano 12B V2](https://leadgreen.ai/models/nvidia-nemotron-nano-12b-v2/) | 12 · BF16 | 1 × H100 | 50.1 | 46 | 241 | 694 |
| [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/) | 70 · BF16 | 2 × B200 | 52.4 | 140 | 2,042 | 1,907 |
| [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 70 · BF16 | 2 × B200 | 60.7 | 106 | 1,022 | 1,935 |
| [Qwen 3 32B](https://leadgreen.ai/models/qwen-3-32b/) | 32 · BF16 | 2 × H100 | 63.5 | 44 | 256 | 1,178 |
| [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 235 (22 active) · BF16 | 4 × B200 | 66.7 | 68 | 3,765 | 3,196 |
| [Gemma 3 27B](https://leadgreen.ai/models/gemma-3-27b/) | 27 · BF16 | 2 × H100 | 80.4 | 40 | 187 | 1,210 |
| [Llama 4 Scout 17B 16E Instruct](https://leadgreen.ai/models/llama-4-scout-17b-16e-instruct/) | 109 (17 active) · BF16 | 4 × H100 | 93.4 | 69 | 473 | 1,881 |
| [Llama 3.1 70B Instruct](https://leadgreen.ai/models/llama-3-1-70b-instruct/) | 70 · BF16 | 4 × H100 | 103.7 | 106 | 898 | 2,548 |
| [Llama 3.3 70B Instruct](https://leadgreen.ai/models/llama-3-3-70b-instruct/) | 70 · BF16 | 4 × H100 | 117.5 | 98 | 724 | 2,546 |
| [Llama 4 Maverick 17B 128E Instruct FP8](https://leadgreen.ai/models/llama-4-maverick-17b-128e-instruct-fp8/) | 400 (17 active) · FP8 | 8 × H100 | 134.5 | 48 | 383 | 3,462 |
| [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/) | 235 (22 active) · FP8 | 2 × B200 | 139.1 | 64 | 256 | 1,891 |
| [DeepSeek V3.1](https://leadgreen.ai/models/deepseek-v3-1/) | 671 (37 active) · FP8 | 8 × B200 | 168.4 | 186 | 3,008 | 5,470 |
| [Qwen 3 235B A22B Instruct FP8](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct-fp8/) | 235 (22 active) · FP8 | 8 × H100 | 206.0 | 76 | 511 | 3,961 |
| [Llama 3.1 405B Instruct](https://leadgreen.ai/models/llama-3-1-405b-instruct/) | 405 · BF16 | 8 × B200 | 282.0 | 272 | 3,589 | 7,530 |
| [Qwen 3 235B A22B Instruct](https://leadgreen.ai/models/qwen-3-235b-a22b-instruct/) | 235 (22 active) · BF16 | 8 × H100 | 303.5 | 55 | 228 | 4,038 |
| [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 405 · FP8 | 4 × B200 | 318.5 | 98 | 510 | 3,883 |
| [Llama 3.1 405B Instruct FP8](https://leadgreen.ai/models/llama-3-1-405b-instruct-fp8/) | 405 · FP8 | 8 × H100 | 572.9 | 67 | 255 | 4,875 |

Wh/M is derived from the source's joules per output token (hover a value to see it). Prompt processing is included: the benchmark divides steady-state GPU energy by the output tokens generated in the same window. Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted, and the benchmark keeps a queue at all times. GPU power is the average draw summed across every card in the configuration. The bar is linear, scaled to the highest row.

Source: [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371). The table shows the best of the 328 stable configurations per model and GPU; the 32 rows match the leaderboard's own table with one GPU selected at a time (its default view shows one row per model, 18 rows). Every configuration is in the [API](https://leadgreen.ai/api/).

*Two generations*

## The same model on H100 and B200

14 models were measured on both GPUs. The newer card's advantage runs from 4.55× on Qwen 3 235B A22B Instruct to 1.05× on NVIDIA Nemotron Nano 9B V2. The gap also depends on which configurations were swept. The 4.55× pair compares an H100 row that was run only at eight cards and a cap of at most 256 requests with a B200 row at a running batch of 3,765 on four cards; at the same cap of 256 the B200 row reads 197.5 Wh/M against the H100's 303.5, a gap of 1.54×. The two Nemotron pairs compare runs whose average answers are 3.2 and 2.4 times longer on the B200 (462 and 510 tokens on the H100 against 1,464 and 1,242).

*Energy-optimal rows from the index, paired by model*

| Model | H100 configuration | Wh / M | B200 configuration | Wh / M | B200 advantage |
|---|---|---|---|---|---|
| Qwen 3 235B A22B Instruct | 8 × H100 | 303.5 | 4 × B200 | 66.7 | 4.55× |
| Qwen 3 14B | 1 × H100 | 31.1 | 1 × B200 | 15.2 | 2.04× |
| Llama 3.1 70B Instruct | 4 × H100 | 103.7 | 2 × B200 | 52.4 | 1.98× |
| Llama 3.3 70B Instruct | 4 × H100 | 117.5 | 2 × B200 | 60.7 | 1.94× |
| Llama 3.1 405B Instruct FP8 | 8 × H100 | 572.9 | 4 × B200 | 318.5 | 1.80× |
| Gemma 3 12B | 1 × H100 | 46.1 | 1 × B200 | 26.5 | 1.74× |
| Gemma 3 27B | 2 × H100 | 80.4 | 1 × B200 | 49.1 | 1.64× |
| Qwen 3 32B | 2 × H100 | 63.5 | 1 × B200 | 39.1 | 1.63× |
| Qwen 3 30B A3B Instruct | 2 × H100 | 24.7 | 1 × B200 | 15.7 | 1.58× |
| Llama 3.1 8B Instruct | 1 × H100 | 19.5 | 1 × B200 | 13.0 | 1.50× |
| Qwen 3 235B A22B Instruct FP8 | 8 × H100 | 206.0 | 2 × B200 | 139.1 | 1.48× |
| Qwen 3 8B | 1 × H100 | 20.0 | 1 × B200 | 14.7 | 1.36× |
| NVIDIA Nemotron Nano 12B V2 | 1 × H100 | 50.1 | 1 × B200 | 39.4 | 1.27× |
| NVIDIA Nemotron Nano 9B V2 | 1 × H100 | 43.1 | 1 × B200 | 40.9 | 1.05× |

At a tighter ceiling. At a 50 ms ceiling the comparison shifts: 14 models still have a row on both cards, and the H100 uses less energy per token than the B200 on two of them (Llama 3.1 8B Instruct, 19.5 Wh/M on 1 × H100 against 19.6 on 1 × B200; Qwen 3 235B A22B Instruct FP8, 306.7 Wh/M on 8 × H100 against 408.9 on 2 × B200).

A card that draws more power can still use less energy per token, because it finishes more tokens per second. Power tells you the size of the feed. Energy per token tells you what the feed produced. The pairs, with card counts and running batches, are on [the H100 vs B200 page](https://leadgreen.ai/h100-vs-b200/).

*Concurrency*

## The idle server is the expensive one

Energy per token depends on how many requests the server is handling at once. Below is the same Qwen 3 32B on the same two H100 cards, all nine measured configurations, from a running batch of 8 to the index row at 256. Energy per token falls 7.1×, from 452 to 63.5 Wh/M, while median inter-token latency stays at 44 ms or under. Power rises 39 percent, from 850 W to 1,178 W, while throughput rises 9.9×, from 522 to 5,155 tokens per second. Energy per token falls because the second effect dwarfs the first. Past the best row the curve turns: at a cap of 384 the same pair of cards reads 64.6 Wh/M at 55 ms.

*Qwen 3 32B, BF16, 2 × H100*

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

*Llama 3.1 8B Instruct, BF16, 1 × H100*

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

A departmental deployment that serves a handful of people at a time lives at the top of these tables, not the bottom. In the editor's view, consolidating traffic onto fewer, busier cards is a lever every operator already holds, it costs nothing in hardware, and on these tables it moves energy per token further than a change of GPU generation does.

The Llama 3.1 8B ladder has eleven measured configurations. Its power rises 41 percent, from 486 W to 688 W, while energy per token falls 6.5×, from 126 to 19.5 Wh/M; past its best row, at a cap of 768, it reads 19.8 Wh/M at 63 ms.

Cap is the configured maximum batch (vLLM's `max_num_seqs`). Running batch (avg) is the average number of requests the server was decoding at once over the steady-state window (vLLM's `num_requests_running`); queued requests are not counted, and the benchmark keeps a queue at all times. The highlighted row is the index row.

Same source and workload as the index. Each row is one benchmarked configuration; the index takes the best of them. Every model's full curve is in its [API document](https://leadgreen.ai/api/).

*Two tasks*

## Long answers also shrink the batch

The same leaderboard also runs a Problem Solving task, whose answers are far longer. For the 11 model and GPU pairs measured on both tasks, Problem Solving costs 3 to 41 times the energy per response of Text Conversation, because its answers run 5,361 to 8,969 tokens against 462 to 1,464, and because the long outputs cut the batch the server can hold, so energy per token itself is 2.2 to 3.3 times the Text Conversation figure for the Qwen and DeepSeek pairs, and 0.7 to 1.0 times it for the four Nemotron pairs.

*Problem Solving (gpqa) against Text Conversation, energy-optimal row of each task per model and GPU, at or under 500 ms*

| Model | GPUs | Energy per response | Energy per token | Output tokens, chat / gpqa | Running batch (avg), chat / gpqa |
|---|---|---|---|---|---|
| NVIDIA Nemotron Nano 9B V2 | 1 × B200 | 3.4× | 0.79× | 1,242 / 5,361 | 255 / 512 |
| NVIDIA Nemotron Nano 12B V2 | 1 × B200 | 3.9× | 1.02× | 1,464 / 5,646 | 256 / 256 |
| NVIDIA Nemotron Nano 9B V2 | 1 × H100 | 7.6× | 0.70× | 510 / 5,531 | 255 / 256 |
| NVIDIA Nemotron Nano 12B V2 | 1 × H100 | 8.7× | 0.70× | 462 / 5,768 | 241 / 192 |
| DeepSeek V3.1 | 8 × B200 | 23.5× | 2.20× | 842 / 8,969 | 3,008 / 256 |
| Qwen 3 32B | 1 × B200 | 24.6× | 2.22× | 635 / 7,035 | 383 / 111 |
| Qwen 3 32B | 2 × H100 | 26.1× | 2.35× | 634 / 7,058 | 256 / 64 |
| Qwen 3 14B | 1 × H100 | 26.8× | 2.50× | 625 / 6,711 | 253 / 59 |
| Qwen 3 8B | 1 × H100 | 38.3× | 3.06× | 645 / 8,052 | 474 / 82 |
| Qwen 3 14B | 1 × B200 | 39.8× | 3.33× | 613 / 7,327 | 2,045 / 128 |
| Qwen 3 8B | 1 × B200 | 40.6× | 3.26× | 649 / 8,074 | 1,427 / 128 |

Both ratio columns are Problem Solving over Text Conversation for the same model and GPU. Energy per token is the fairer comparison across workloads; energy per response is what a bill sees. Same source as the index.

*Carbon*

## Same tokens, different grid

Energy per token does not change with geography. Carbon per token does. This table prices the reference row (Qwen 3 32B, 2 × H100, 63.5 Wh/M) against each grid's average emissions intensity for 2024. A billion output tokens on the Saudi grid carries about 43.9 kg CO2e of GPU-side emissions. The same billion tokens on the Norwegian grid carries 1.9 kg.

*Grid emissions intensity, 2024 annual average, location-based, and the reference row priced against it*

| Grid | g CO2e per kWh | kg CO2e per billion output tokens |
|---|---|---|
| India | 707 | 44.9 |
| Saudi Arabia | 692 | 43.9 |
| Hong Kong | 676 | 42.9 |
| Serbia | 668 | 42.4 |
| Taiwan | 636 | 40.4 |
| Philippines | 629 | 40.0 |
| Qatar | 582 | 36.9 |
| Australia | 554 | 35.2 |
| Singapore | 499 | 31.6 |
| Japan | 484 | 30.7 |
| United Arab Emirates | 468 | 29.7 |
| Sri Lanka | 387 | 24.5 |
| United States | 384 | 24.4 |
| Germany | 340 | 21.6 |
| Bulgaria | 279 | 17.7 |
| Ireland | 271 | 17.2 |
| United Kingdom | 216 | 13.7 |
| Hungary | 184 | 11.7 |
| New Zealand | 112 | 7.1 |
| Slovakia | 97 | 6.2 |
| France | 40 | 2.6 |
| Norway | 30 | 1.9 |
| World average | 474 | 30.1 |

Which grids. The 22 grids are 15 markets Katonic sells in or expects to, plus seven reference grids. Ember's 2024 figures run from Ethiopia at 23.5 to Turkmenistan at 1,306.2 gCO2e per kWh, a spread of 55.6×; all 193 areas plus World are in [`grid.json`](https://leadgreen.ai/api/v1/grid.json), and each listed grid has [its own page](https://leadgreen.ai/grids/) with the whole index priced on it. Area names are shortened from Ember's labels.

What the figure is. Grid figures are Ember's yearly emissions intensity (CC BY 4.0), September 2026 release. Lifecycle emissions intensity: CO2e per kWh of net generation, built from per-technology lifecycle factors (IPCC AR5 WG3 Annex III midpoints, all gases at GWP-100), so upstream methane, supply chains and plant manufacture are included. Production-based: imports and grid losses are excluded. A location-based figure for comparing places, not a Scope 2 combustion factor to file as reported. The table is location-based in the ESRS E1-6 sense, so what it prices belongs in the Scope 2 location-based line of E1-6, not in the E1-5 energy line. The other method, market-based, nets the buyer's contracted supply (certificates and power purchase agreements) and needs the buyer's own contracts.

Why 2024. It is the latest year with a value for every grid listed. 93 of Ember's 193 areas already have a 2025 value, but Saudi Arabia, United Arab Emirates and Hong Kong do not yet; `grid.json` carries 2023 to 2025 per area where present, with the latest year named. A flat load. A GPU server draws much the same power around the clock, while an annual average weights each hour by how much was generated in it, so on a grid whose clean supply peaks at midday a flat load sees a higher figure than the average, and on one with steady clean supply much the same. Hourly intensity, contracted supply, on-site generation and facility overhead are not counted here. Multiply any row of the index by the grid figure and divide by 1,000 to price a different model.

*Hardware*

## What a card can draw, and how it splits

Manufacturer ceilings, for scale. A card at the index's best rows runs close to these numbers. The concurrency tables above show what that draw earns.

*Maximum thermal design power, as published by NVIDIA*

| GPU | Form | Max TDP | Memory |
|---|---|---|---|
| A100 80GB | SXM | 400 W | 80 GB HBM2e |
| A100 80GB | PCIe | 300 W | 80 GB HBM2e |
| H100 | SXM | up to 700 W | 80 GB HBM3 |
| H100 | NVL | 350 to 400 W | 94 GB HBM3 |
| H200 | SXM | up to 700 W | 141 GB HBM3e |
| H200 | NVL | up to 600 W | 141 GB HBM3e |
| B200 | HGX, SXM6 | configurable up to 1,000 W | 180 GB HBM3e |

*Multi-Instance GPU profiles, H100 80GB and H200 141GB*

| H100 profile | H200 profile | Memory | Compute (SMs) | Per card |
|---|---|---|---|---|
| 1g.10gb | 1g.18gb | 1/8 | 1/7 | 7 |
| 1g.20gb | 1g.35gb | 1/4 | 1/7 | 4 |
| 2g.20gb | 2g.35gb | 2/8 | 2/7 | 3 |
| 3g.40gb | 3g.71gb | 4/8 | 3/7 | 2 |
| 4g.40gb | 4g.71gb | 4/8 | 4/7 | 1 |
| 7g.80gb | 7g.141gb | full | 7/7 | 1 |

The A100 80GB uses the same six shapes as the H100 column (the seventh, a 1g media-extension variant, is omitted for all four cards), and the B200 180GB has the same shapes at its own sizes (all four cards are in the [API](https://leadgreen.ai/api/)). NVIDIA does not publish power draw per MIG slice, and neither public benchmark on this page measures a sliced card. That gap is the first measurement Lead Green will add.

Sources: NVIDIA product specifications for A100, H100 and H200; NVIDIA Product Carbon Footprint Summary for HGX B200 (July 2025) for the B200 ceiling; NVIDIA Multi-Instance GPU User Guide, supported profiles, last updated 11 September 2026. The "+me" media-extension variants of the 1g profiles are omitted.

*Per query*

## Batch size one, a different question

The AI Energy Score measures something else: GPU watt-hours for 1,000 text-generation queries, one query at a time, on NVIDIA H100 80GB GPUs: one card for class A and B models, several cards for class C. A query is one prompt from the benchmark's 1,000-prompt text-generation set, run at batch size 1 with the response fixed at ten generated tokens for non-reasoning models, averaged over ten passes. It is a controlled probe, not a serving workload, so its watt-hours are not comparable with the index and are not converted. It is shown because the ranking within a class is useful.

*AI Energy Score, text generation, December 2025 round, all 22 rows, NVIDIA H100 80GB (one card for classes A and B, several for C), batch size 1*

| Model | Class | Wh per 1,000 queries | Score |
|---|---|---|---|
| tencent/Hunyuan-1.8B-Instruct | A | 4.2 | ★★★★★ |
| google/gemma-3-270m | A | 9.3 | ★★★★★ |
| Qwen/Qwen3-0.6B | A | 11.8 | ★★★★★ |
| google/gemma-3-1b-pt | A | 12.3 | ★★★★★ |
| ibm-granite/granite-4.0-micro | A | 16.6 | ★★★★★ |
| microsoft/Phi-4-reasoning-plus | A | 18.4 | ★★★★★ |
| HuggingFaceTB/SmolLM3-3B | A | 18.4 | ★★★★★ |
| swiss-ai/Apertus-8B-Instruct-2509 | A | 21.7 | ★★★★☆ |
| mistralai/Mistral-Nemo-Instruct-2407 | A | 23.2 | ★★★★☆ |
| Qwen/Qwen2.5-Coder-14B | A | 27.1 | ★★★★☆ |
| google/gemma-3-4b-pt | A | 34.4 | ★★★★☆ |
| deepseek-ai/DeepSeek-R1-Distill-Qwen-32B | C | 36.6 | ★★★★★ |
| Qwen/Qwen3-30B-A3B | B | 37.4 | ★★★★★ |
| deepseek-ai/DeepSeek-R1-Distill-Llama-70B | C | 49.5 | ★★★★★ |
| google/gemma-3-27b-pt | B | 50.4 | ★★☆☆☆ |
| LGAI-EXAONE/EXAONE-4.0-32B | B | 54.5 | ★☆☆☆☆ |
| ibm-granite/granite-4.0-h-tiny | A | 81.8 | ★☆☆☆☆ |
| zai-org/GLM-4.5-Air | C | 220.5 | ★★★★★ |
| Qwen/Qwen3-235B-A22B | C | 305.8 | ★★★★☆ |
| swiss-ai/Apertus-70B-Instruct-2509 | C | 697.5 | ★★★☆☆ |
| zai-org/GLM-4.5 | C | 1,225.4 | ★☆☆☆☆ |
| zai-org/GLM-4.6 | C | 1,273.5 | ★☆☆☆☆ |

Only the December 2025 round is shown, all 22 of its rows, and they are in the [API](https://leadgreen.ai/api/). Lead Green does not mix it with the February 2025 round because the benchmark harness changed between them (the February round ran on Optimum Benchmark, the December round on Neuralwatt's AI Energy Benchmarks); the project itself treats the watt-hour values as stable across rounds and recalibrates only the stars. The 70B figures people quote from the two rounds are two different models: Meta-Llama-3-70B at 1,719.7 Wh in February 2025 and DeepSeek-R1-Distill-Llama-70B at 49.5 Wh in December, while Apertus-70B reads 697.5 Wh inside the December round.

Stars are the AI Energy Score's rating within a class for this round: the class's energy range is cut into five equal bands and the lowest band is five stars. They do not compare across classes: zai-org/GLM-4.5-Air, five stars in class C at 220.5 Wh, uses 4.0 times the energy of LGAI-EXAONE/EXAONE-4.0-32B, a one-star class B model at 54.5 Wh. Class A fits one consumer GPU, B one H100, C more than one H100. Source: AI Energy Score (Hugging Face and Salesforce, with Neuralwatt, Cohere, Meta and Carnegie Mellon University), retrieved 26 September 2026.

*Method*

## What is counted, and what is not

- The unit. Watt-hours per million output tokens equals joules per output token multiplied by one million and divided by 3,600. The reference row, 0.2285 J per token, becomes 63.5 Wh/M.
- Counted. GPU energy only, read from the device by the benchmark's measurement library (Zeus) at steady state, with vLLM serving the model on a real H100 80GB HBM3 or B200 server. Prompt processing is included, because the benchmark divides steady-state GPU energy by the output tokens generated in the window (its steady_state_energy_per_token); energy per request is that figure times the average output length.
- Not counted. Host CPU and memory, network and storage, cooling and the rest of the facility, time the GPU spends idle between requests, and the carbon embodied in the hardware. For scale on that last item, NVIDIA's own cradle-to-gate footprint for one HGX B200 baseboard, eight GPUs, is 2,274 kg CO2e.
- Water. The index measures electricity, not water. For a public scale, [Google](https://arxiv.org/abs/2508.15734) puts the median Gemini Apps text prompt at 0.26 mL (August 2025) and [Mistral](https://mistral.ai/news/our-contribution-to-a-global-environmental-standard-for-ai) puts a 400-token reply at 45 mL (July 2025). Neither is per million tokens at a stated load, and site water depends on the cooling design and the climate.
- To the meter. Two multipliers take a GPU figure to the facility meter, and both are the operator's own. The system-to-GPU power ratio covers the host, memory, network and fans: a DGX B200 is rated at 14.3 kW against 8.0 kW for its 8 GPUs, a ratio of 1.79. Power usage effectiveness (PUE, per ISO/IEC 30134-2) covers cooling and the rest of the building, and only the operator knows theirs. As an illustration, with that ratio and an assumed PUE of 1.3, both assumptions and not measurements: 63.5 × 1.79 × 1.3 = 148 Wh/M at the meter, about 6.8 billion tokens per facility MWh. For a public scale, [Google's August 2025 figures](https://arxiv.org/abs/2508.15734) put the accelerators at 58 percent of 0.24 Wh per median text prompt and the accelerator-only boundary at 0.10 Wh, so its full stack is 1.7 to 2.4 times the accelerator figure.
- Not measurable. Closed-weight models served over an API cannot be measured from outside the operator, and this index says nothing about them.
- The reference row. Qwen 3 32B on 2 × H100 is the row the carbon table and the worked examples are priced on because it is a dense model, on two cards, with a full ladder of nine measured configurations; it ranks 19 of 32. It is a scaling point, not a claim about typical deployments.
- A floor. Every index row is the best configuration found under a latency limit, at high concurrency. A real deployment sits above it, often far above it. The concurrency section shows how far.
- The latency ceiling. 500 ms is the leaderboard's own default for every LLM task, chosen to match it. No measured configuration reaches it, so it changes no row. Tighter ceilings would: At 250 ms, 1 row changes; at 100 ms, 7 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 14.7 Wh/M; at 50 ms, 19 rows change and the lowest becomes Qwen 3 8B on 1 × B200 at 17.2 Wh/M and the highest becomes Llama 3.1 405B Instruct FP8 on 8 × H100 at 674.9 Wh/M. None of these is applied to the index.
- Workload. The index uses the Text Conversation task. The same leaderboard's Problem Solving task costs 3 to 41 times the energy per response for the same model and GPU, because its answers run 5,361 to 8,969 tokens against 462 to 1,464, and because the long outputs cut the batch the server can hold, so energy per token itself is 2.2 to 3.3 times the Text Conversation figure for the Qwen and DeepSeek pairs, and 0.7 to 1.0 times it for the four Nemotron pairs ([table](https://leadgreen.ai/index/#workloads)). Energy per token is the fairer comparison across workloads; energy per response is what a bill sees.
- Grid intensity. Annual generation average per country, in grams of CO2e per kWh, from Ember. Hourly values, contracted supply and self-generation are not reflected.
- Words. The words-per-token conversion uses the common English rule of thumb of about three quarters of a word per token. It is a rough guide, nothing more.

*Own measurements*

## None yet

Lead Green has not published a measurement of its own. The first will be Qwen 3 14B in BF16 on one H100: the whole card, then the same card split into two 3g.40gb slices, each serving its own BF16 copy under the same load at the same time, with GPU power sampled through NVIDIA DCGM on a server Katonic operates. It is like-for-like on precision and will sit beside the public 1 × H100 BF16 rows for the same model (196.1 Wh/M at a cap of 8 down to 31.1 at a cap of 256). The second will be Qwen 3 32B: the whole card in BF16, then two 3g.40gb slices each serving an FP8 or INT4 copy under the same load. It is not like-for-like on precision and will be labelled so, beside the public 1 × H100 rows (479.4, 267.0 and 173.3 Wh/M). MIG exposes no per-slice power and NCCL does not run across slices, so both read the card's energy as a whole with every slice loaded. It will be labelled as ours, with hardware, driver, serving engine and prompt set named, and it will sit beside the public figures rather than in place of them. The protocol it will follow is on the [contribute page](https://leadgreen.ai/contribute/#protocol), and anyone with a GPU can follow it too.

*Contributed measurements*

## Rows measured by volunteers

None yet.

Rows measured under the [protocol](https://leadgreen.ai/contribute/#protocol) and accepted by two reviewers appear here with the contributor's name, and in [`measurements.json`](https://leadgreen.ai/api/v1/measurements.json). They are never merged into the index table above.

*Cite as*

## How to credit this index

Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-09-27, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, September 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

In a tender where Katonic may bid, read [Using the index in a tender](https://leadgreen.ai/about/#tender) first.

*Sources*

## Every figure, and where it came from

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/), The ML.ENERGY Initiative (started at SymbioticLab, University of Michigan)Index, two-generation table, concurrency tables, the workload comparison and the measured GPU power figures. Text Conversation, all 328 stable configurations; Problem Solving, all 187. The leaderboard publishes the runs that passed its stability filter as JSON in its repository; every run, including the unstable ones, is in the gated Hugging Face dataset [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3). The leaderboard repository the JSON comes from carries no licence file; the benchmark data is published under Apache 2.0 on the dataset card and in the NeurIPS 2025 paper, and the JSON is reproduced here as published measurements on that basis while the ML.ENERGY team is asked to confirm that the licence covers it. Cite: [Chung et al., The ML.ENERGY Benchmark: Toward Automated Inference Energy Measurement and Optimization, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371](https://arxiv.org/abs/2505.06371).Version 3.0, released 1 December 2025; data compiled 16 February 2026 (the leaderboard's index.json). Retrieved 26 September 2026.
2. [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/)Carbon table and the grid API. Emissions intensity of total generation, gCO2e per kWh, 2024. CC BY 4.0.September 2026 release. Retrieved 27 September 2026.
3. [NVIDIA Multi-Instance GPU User Guide, Supported MIG Profiles](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-mig-profiles.html)MIG profile table.Last updated 11 September 2026. Retrieved 27 September 2026.
4. NVIDIA product specifications: [A100](https://www.nvidia.com/en-us/data-center/a100/), [H100](https://www.nvidia.com/en-us/data-center/h100/), [H200](https://www.nvidia.com/en-us/data-center/h200/), [DGX B200](https://www.nvidia.com/en-us/data-center/dgx-b200/)Maximum TDP and memory in the hardware table; the DGX B200 system power figure used on the "why" page.Retrieved 27 September 2026.
5. [NVIDIA, Product Carbon Footprint Summary for NVIDIA HGX B200](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf)B200 maximum TDP (configurable up to 1,000 W per GPU) and the 2,274 kg CO2e cradle-to-gate figure in the method.July 2025. Retrieved 27 September 2026.
6. [AI Energy Score leaderboard](https://huggingface.co/spaces/AIEnergyScore/Leaderboard) (Hugging Face and Salesforce, with Neuralwatt, Cohere, Meta and Carnegie Mellon University), with its [documentation](https://huggingface.github.io/AIEnergyScore/)Per-query table. Text generation task, December 2025 round, all 22 rows. Apache-2.0 as tagged on the Space; the project states no separate licence for the results file, which is reproduced as facts with attribution.Retrieved 27 September 2026.
7. [OpenAI, What are tokens and how to count them](https://help.openai.com/en/articles/4936856-what-are-tokens-and-how-to-count-them)The rough words-per-token conversion in the opening paragraph.Retrieved 27 September 2026.

Snapshots of every data file used, as retrieved, are kept alongside the page so each figure can be recomputed. Corrections are welcome and are recorded below.

*Changes*

## Record

- 27 Sep 2026Corrections after a nine-reader review, before launch. The ML.ENERGY data is dated to its compile date, not a banner update; the latency ceiling is the leaderboard's own 500 ms (no row moved); "requests in flight" is renamed running batch; full concurrency ladders; all AI Energy Score December rows; a two-task table; the carbon basis, grid years and display names; seven-decimal joules; additive API fields (data_version, row_id, repeat, p95_itl_ms, avg_running_batch, boundary, years, latest_year, iso2, display_name, source_label); changes.json, measurements.json, the measurement schema, a dated release archive, CSV, zip and TypeScript types.
- 26 Sep 2026First build. 32 index rows from ML.ENERGY v3.0 (data compiled 16 February 2026), grid intensities from Ember (2024), NVIDIA specifications, AI Energy Score December 2025 round. The API, the MCP server and the first blog post.
