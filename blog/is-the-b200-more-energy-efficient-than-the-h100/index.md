# Is the B200 more energy-efficient than the H100?

> Yes on all 14 models measured on both cards: the H100 row uses 1.05× to 4.55× the B200 row's energy per token, median 1.63×. How much is the silicon.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/is-the-b200-more-energy-efficient-than-the-h100/ (this file: https://leadgreen.ai/blog/is-the-b200-more-energy-efficient-than-the-h100/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

By Prem Naraindas · 1 November 2026 · Lead Green, a Katonic project

Cite this page: Lead Green, a Katonic project. Is the B200 more energy-efficient than the H100?. https://leadgreen.ai/blog/is-the-b200-more-energy-efficient-than-the-h100/, release 2026-10-19, retrieved [date]. CC BY 4.0.

Look, this question usually arrives with a quote attached. Somebody has a B200 price on the desk, the H100s are two years old, and the board wants to know whether the new card is worth it on energy. The public data says yes, on all 14 models the ML.ENERGY Leaderboard measured on both cards: the H100's index row uses from 4.55× the B200 row's energy per output token (Qwen 3 235B A22B Instruct) down to 1.05× (NVIDIA Nemotron Nano 9B V2), with a median of 1.63×. So the short answer is yes. The longer answer is that the number is smaller than the headline, part of it is not the silicon, and it is the second lever, not the first.

## The 14 pairs

*Index rows paired by model, sorted by the gap. ML.ENERGY Leaderboard v3.0, Text Conversation.*

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

Each pair is a model's index row on each card: the lowest-energy configuration the leaderboard measured, at or under 500 ms median inter-token latency. The ratio is the H100 row over the B200 row. The reference model, Qwen 3 32B, goes from 63.5 Wh/M on 2 × H100 to 39.1 on one B200, 1.63×, with one card doing the work of two: a million output tokens takes 0.11 card-hours on the H100 pair and 0.04 on the single B200.

## How much of it is the silicon

See, the leaderboard sweeps each card on its own terms. It picks the configurations it runs per GPU, and the B200's memory holds a model on fewer cards, so on eight of the 14 pairs the B200 row has fewer cards than the H100 row, and the running batches differ too. The widest gap shows what that does to the number. The 4.55× pair compares an H100 row that was run only at eight cards and a cap of at most 256 requests with a B200 row holding 3,765 requests on four cards. Re-cut the pair at the same cap of 256 and the B200 row reads 197.5 Wh/M against the H100's 303.5: a gap of 1.54×, not 4.55×. The rest was the batch. At the other end, the two Nemotron pairs compare runs whose answers were 3.2 and 2.4 times longer on the B200, which is a different workload wearing the same name.

Tighten the latency and the picture moves again. At a 50 ms ceiling, 14 models still have a row on both cards, and the H100 comes out ahead on two of them: Llama 3.1 8B Instruct, 19.5 Wh/M on 1 × H100 against 19.6 on 1 × B200; Qwen 3 235B A22B Instruct FP8, 306.7 Wh/M on 8 × H100 against 408.9 on 2 × B200. I think the honest reading is this: on a busy server the generation is worth about the median, 1.63×, and on a server that is not busy it is worth less than that, because the concurrency ladder does not care which card is sitting idle.

## Power against energy

The B200 draws more. NVIDIA rates the H100 SXM at up to 700 W and the B200 as configurable up to 1,000 W, and on these index rows the cards averaged 612 W per H100 and 868 W per B200. It uses less energy per token because it produces more tokens in every second of that draw. The distinction matters to the facility. An eight-GPU DGX B200 is rated at about 14.3 kW, 1.79× what its cards draw, so a B200 fleet is a bigger feed that produces more tokens per kilowatt-hour, and the envelope decides how many boxes you can stand up before the tokens do. Power sizes the feed. Energy per token tells you what the feed produced.

## The second lever

Here is the part I would put in the memo. The widest generation gap on the table is 4.55×. The same model on the same H100 cards moves 7.1× in energy per token between a running batch of 8 and 256, and that lever costs nothing in hardware. A department that serves a handful of people at a time and buys B200s has bought a faster car for a road where it never gets out of second gear. In the deployments I see, that is the usual order of events: the card gets upgraded, the utilisation does not, and the energy per token barely moves. Consolidate first. Then the generation change is worth its median, and the new card carries the load on fewer cards, which is also fewer boxes to power and cool.

## What I am not telling you

Two cards, one benchmark. The leaderboard ran B200 and H100 and nothing else, so there is nothing here about the H200, the GB200 or anyone else's silicon. On the index, two models have an H100 row and no B200 row (Llama 4 Maverick 17B 128E Instruct FP8 and Llama 4 Scout 17B 16E Instruct), and two have the reverse (DeepSeek V3.1 and Llama 3.1 405B Instruct), so the 14 pairs are the models that happen to have both. A TDP is a rating, not a reading; the measured draws above are the ones to plan on. And every row is a floor at high load: your fleet sits above it on both cards, and the question is by how much on each.

## What to do with it

- **Ask for both cards at your running batch and your latency.** The pairs above can be re-cut at a matched cap or a matched running batch from the [API](https://leadgreen.ai/api/); ask the vendor to do the same with the configuration they are quoting, and refuse a ratio that comes without its two running batches.
- **Count cards, not only watts.** On eight of the 14 pairs the B200 holds the model on fewer cards. Fewer cards is fewer boxes, and that saving sits outside the GPU-only figure on this site; the [method](https://leadgreen.ai/index/#method) takes a figure to the meter.
- **Size the feed on the rating, judge the kit on the energy.** A rating of configurable up to 1,000 W per card is what the electrical engineer plans for; 868 W per card is what the benchmark saw on these rows; watt-hours per million tokens is what you are buying.
- **Fix the utilisation before the purchase order.** The [concurrency ladder](https://leadgreen.ai/blog/why-an-idle-gpu-wastes-energy/) is the bigger lever and the cheaper one.

The full comparison, with every pair and the questions people ask about it, is on the [H100 vs B200 page](https://leadgreen.ai/h100-vs-b200/); every configuration behind it is on the [model pages](https://leadgreen.ai/models/).

*References*

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).
2. The pairs: for each model with an index row on both cards, the H100 row's Wh/M over the B200 row's. The matched-cap figure re-cuts the widest pair at the H100 row's cap (vLLM's `max_num_seqs`) using the B200 configuration at that cap. The 50 ms figures take each card's lowest-energy configuration at or under that median inter-token latency. Card-hours per million output tokens = cards × 1,000,000 ÷ output tokens per second ÷ 3,600. Every pair and configuration: [the comparison page](https://leadgreen.ai/h100-vs-b200/) and [the API](https://leadgreen.ai/api/).
3. NVIDIA product specifications for the [H100](https://www.nvidia.com/en-us/data-center/h100/) and the [DGX B200](https://www.nvidia.com/en-us/data-center/dgx-b200/), and the [HGX B200 product carbon footprint summary](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf) (July 2025), retrieved 26 September 2026, for the TDP ratings and the system power rating. Average power per card is the benchmark's measured draw on the index rows, divided by the card count.
