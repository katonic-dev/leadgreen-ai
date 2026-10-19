# What is watt-hours per million tokens, and why not joules per token?

> The unit behind the index: what Wh/M counts, what it leaves out, how it converts to kWh, carbon and the meter, and why joules per token became watt-hours.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/blog/what-is-watt-hours-per-million-tokens/ (this file: https://leadgreen.ai/blog/what-is-watt-hours-per-million-tokens/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Blog*

By Prem Naraindas · 19 October 2026 · Lead Green, a Katonic project

Cite this page: Lead Green, a Katonic project. What is watt-hours per million tokens, and why not joules per token?. https://leadgreen.ai/blog/what-is-watt-hours-per-million-tokens/, release 2026-10-19, retrieved [date]. CC BY 4.0.

Look, every table on this site is in one unit, watt-hours per million output tokens, and I get asked why. The benchmark we build on publishes joules per token. Finance thinks in kilowatt-hours. Facilities thinks in kilowatts. Sustainability wants kilograms of CO2e. So this post is the unit, start to finish: what it counts, what it leaves out, how to move between it and every other number people ask for, and why I picked it over the alternatives.

## The definition

Take the GPU energy a server used while it was serving, in joules. Divide by the output tokens it produced in the same window. That is joules per output token, which is what the ML.ENERGY benchmark measures. Multiply by a million, divide by 3,600, and you have watt-hours per million output tokens, Wh/M. One Wh/M is 0.0036 joules per token; the arithmetic never changes, so you can go back and forth without losing anything. The reference row on the index is 0.2285 J per token, which is 63.5 Wh/M.

Two words in that definition carry the weight. **GPU energy:** the cards and nothing else. The host, the network, the cooling and the building are outside the figure. **Output tokens:** the tokens the model produced, not the ones it read. The prompt still costs energy to process, and that energy is inside the figure, because the benchmark divides everything the GPUs used by the outputs alone. So Wh/M is the whole GPU bill per unit of what you got.

## Why not joules per token?

Because the numbers are hard to hold in your head. Across the index, joules per token run from 0.047 to 2.06. Those are decimals with the interesting part in the second and third place, and nobody in a capacity meeting is going to compare 0.047 with 0.2285 and feel the difference. The same rows in Wh/M are 13.0 to 572.9: whole numbers, a 44× spread you can see. The scaling is the only change; the information is identical.

The second reason is the bill. Tokens are sold by the million, and electricity is sold by the kilowatt-hour. A unit that is watt-hours over millions of tokens sits between the two invoices, which is where the question lives. See, 63.5 Wh per million tokens is 63.5 kWh per billion tokens, no conversion table needed, and that is the number a finance person can multiply by a tariff.

## Why not energy per request?

Because requests are not the same size. On the index's chat workload, the average answer runs from 462 to 1,464 tokens depending on the model; on the same leaderboard's problem-solving task, answers run 5,361 to 8,969 tokens. Energy per request is what a bill sees, and it is the right number to ask for when you are forecasting a particular product, but it mixes the model's efficiency with how talkative it is. Energy per token separates the two. When you want per request, multiply by your own average output length: the reference row's 634-token answers cost about 145 joules each, which is 0.040 Wh.

## Why not power?

Power, in watts, is what the facility engineer sees and what the feed is sized for. It is not efficiency. A card at full draw producing few tokens and a card at full draw producing many read the same on a power meter, and the difference between them is the whole point. Energy per token is power divided by throughput: watts divided by tokens per second gives joules per token, and the same scaling gives Wh/M. On the reference row that is 1,177.9 W divided by 5,155.5 tokens per second, times a million, over 3,600, equals 63.47 Wh/M. I put that identity in the RFP scoring box on the [why page](https://leadgreen.ai/why/#monday), because any bidder's figure that fails it was not measured.

## The conditions that travel with the number

A Wh/M figure without its conditions is a number without a unit. Three conditions must come with it. The **running batch**: how many requests the server was decoding at once, averaged over the window; the same model on the same cards moves 7.1× between a batch of 8 and 256. The **latency**: the median inter-token latency users were getting, 44 ms on the reference row, under the leaderboard's 500 ms ceiling. And the **boundary**: GPU only, or with the host, network and cooling, and if so how much. Every row on the index states all three. Every vendor figure you are given should too, and if it does not, ask.

## From Wh/M to everything else

- **Kilowatt-hours.** Wh/M × millions of tokens ÷ 1,000. A billion tokens at 63.5 Wh/M is 63.5 kWh.
- **Tokens per megawatt-hour**, the capacity planner's number. One MWh of GPU energy at the reference row serves 15.8 billion output tokens; at the top of the concurrency ladder, 2.2 billion. Same cards, same MWh.
- **Carbon.** Wh/M × the grid's grams of CO2e per kWh ÷ 1,000 gives kilograms per billion tokens. The reference row on Serbia's grid (668 gCO2e per kWh, Ember 2024) is 42.4 kg per billion. The grid figure is location-based and lifecycle; the [grid pages](https://leadgreen.ai/grids/) say what that means for your report.
- **The meter.** Multiply by the system-to-GPU power ratio (a DGX B200 is 1.79) and the site's PUE, which only the operator knows. With an assumed PUE of 1.3, the reference row is about 148 Wh/M at the meter, 6.8 billion tokens per facility MWh. Both multipliers are assumptions in that example, and I say so every time I use it.
- **Money.** At USD 0.10 per kWh, my assumption, the reference row is 0.6 cents per million tokens. Small. The number matters because it tracks GPU-hours, which are not small.

## What the unit does not tell you

It does not tell you what your deployment uses. Every index row is a floor: the most efficient configuration measured, on a busy server, GPU only. It does not tell you about water, which the index does not measure. It does not tell you about closed models behind an API, which nobody outside the operator can measure. And it does not rank anyone as green. In my view it is the one number that ties a model, a card and a load to a feed, a bill and a carbon line at the same time, and that is the case for it. The rows are on [the index](https://leadgreen.ai/index/), the same numbers are in [the API](https://leadgreen.ai/api/), and the [MCP server](https://leadgreen.ai/mcp/) will do the conversions above for you and repeat the caveat every time.

*References*

1. [ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371).
2. Ember, Yearly electricity data, September 2026 release, emissions intensity of total generation, 2024, CC BY 4.0. [ember-energy.org](https://ember-energy.org/data/yearly-electricity-data/).
3. NVIDIA DGX B200 product page, for the system power rating behind the system-to-GPU ratio. The PUE of 1.3 and the electricity price of USD 0.10 per kWh are stated assumptions, not source figures.
4. Conversions: Wh/M = J per token × 1,000,000 ÷ 3,600; kWh per billion tokens = Wh/M; kg CO2e per billion tokens = Wh/M × gCO2e per kWh ÷ 1,000. Method and every row: [the index](https://leadgreen.ai/index/#method).
