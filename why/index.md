# Nine reasons to know your watt-hours per million tokens

> Why GPU energy per million output tokens belongs in procurement, operations and reporting, with the working, the sources and what to do on Monday.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/why/ (this file: https://leadgreen.ai/why/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Why it matters*

The number is small, cheap to buy and easy to ignore. It is also the only figure that ties a model, a GPU and a workload to a power feed, a carbon line and a utilisation rate at the same time. Here is why each of those matters, with the working shown.

Cite this page: Lead Green, a Katonic project. Why it matters. https://leadgreen.ai/why/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [1 Utilisation](https://leadgreen.ai/why/#utilisation)
- [2 Power](https://leadgreen.ai/why/#power)
- [3 The board](https://leadgreen.ai/why/#board)
- [4 The regulator](https://leadgreen.ai/why/#regulator)
- [5 Location](https://leadgreen.ai/why/#location)
- [6 The SCI](https://leadgreen.ai/why/#sci)
- [7 Cheap](https://leadgreen.ai/why/#cheap)
- [8 Sliced GPUs](https://leadgreen.ai/why/#mig)
- [9 Monday](https://leadgreen.ai/why/#monday)
- [Hosted API](https://leadgreen.ai/why/#hosted)
- [Questions](https://leadgreen.ai/why/#faq)

*1*

## It is a utilisation meter

Take one model on one pair of GPUs and change nothing but how many requests the server holds at once. On the index, Qwen 3 32B on two H100 cards goes from **452 Wh/M** at a running batch of 8 to **63.5 Wh/M** at 256. That is 7.1× on the same hardware. The cards' draw rises 39 percent, from 850 W to 1,178 W, while the tokens they produce each second rise 9.9×, and median inter-token latency stays at 44 ms or under.

Read it the other way round. A high energy per token does not mean the GPU is working hard. It means the GPU is drawing close to full power and producing few tokens, which is what an under-used server looks like from the wall socket. Energy per token is the utilisation rate expressed in a unit finance can see. If yours is high, you are paying for silicon that is waiting.

Source: [ML.ENERGY Leaderboard v3.0](https://ml.energy/leaderboard/), Text Conversation, all nine measured configurations of Qwen 3 32B on 2 × H100. Full ladder on [the index](https://leadgreen.ai/index/#concurrency).

*2*

## Power is the ceiling

A data hall, a sovereign site or a telco exchange has a fixed power envelope long before it has a fixed GPU count. Energy per token converts that envelope into capacity. One megawatt-hour of GPU energy serves **15.8 billion output tokens** at the reference row (63.5 Wh/M). At the top of the concurrency ladder, 452 Wh/M, the same megawatt-hour serves **2.2 billion**.

An eight-GPU DGX B200 is rated at about 14.3 kW, and each B200 can be configured up to 1,000 W. Those are the numbers a facility engineer works with. What they buy depends entirely on the Wh/M the platform achieves, which is why the figure belongs in the capacity plan and not only in the sustainability report. To take a GPU figure to the facility meter, multiply by the system-to-GPU power ratio and the site's PUE; the [method](https://leadgreen.ai/index/#method) works one example.

Sources: [ML.ENERGY Leaderboard v3.0](https://ml.energy/leaderboard/) for the rows; [NVIDIA DGX B200 product page](https://www.nvidia.com/en-us/data-center/dgx-b200/) and the [HGX B200 product carbon footprint summary](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf) (July 2025) for the ceilings.

*3*

## The board will ask

Under the European Sustainability Reporting Standards, disclosure E1-5 asks for total energy consumption in MWh from own operations, split by fossil, nuclear and renewable sources. AI served on GPUs the company runs is a new and growing line inside that total, and its electricity lands in Scope 2. Tokens bought from a hosted API are different: that electricity is the provider's Scope 2 and the buyer's Scope 3 category 1 (purchased goods and services), and it sits outside the buyer's E1-5 MWh. A company that cannot say how many MWh its assistants used last quarter, or how many they will use next year as adoption grows, cannot fill in the line with a method it can defend.

Energy per million tokens is the forecasting unit in both cases. Tokens served next year multiplied by Wh/M gives the MWh. Without the first factor the second is a guess.

Sources: [Commission Delegated Regulation (EU) 2023/2772](https://eur-lex.europa.eu/eli/reg_del/2023/2772/oj), ESRS E1-5 "Energy consumption and mix", paragraph 37 (energy consumption related to own operations), carried into ESRS (2026) for financial years from 2027, and E1-6 (Scope 2, location-based and market-based); GHG Protocol Scope 3, category 1, purchased goods and services.

Regulatory summaries on this site are as at 27 September 2026, for orientation, and are not legal advice.

*4*

## What the regulator asks, and what it does not

The EU AI Act ([Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj)) requires providers of general-purpose AI models to keep technical documentation, and Annex XI lists what it must contain. Section 1, point 2(e) names the "known or estimated energy consumption of the model", and adds that where it is unknown it may be based on the computational resources used. The duty sits with the model provider, not with the company deploying the model.

Two limits apply. Article 53(2) lifts this duty from models released under a free and open-source licence with public weights, unless the model carries systemic risk. Every model on this index is open-weight, though whether each licence and model qualifies is for its provider to show. Article 111(3) gives models placed on the market before 2 August 2025 until 2 August 2027 to comply. So for many rows on this index no energy documentation is yet required by law.

That documentation stays between the provider and the AI Office. Annex XII, the information a provider must give downstream, has no energy item, and the Code of Practice's Model Documentation Form marks its energy fields for the AI Office and national authorities only, asks for training energy in megawatt-hours, and records inference as compute in floating-point operations. So the Act does not put a serving energy figure in a buyer's hands. Lead Green expects buyers to ask for one anyway, at their own load, and the index is the public baseline for that question.

The reporting duty that reaches a data centre operator is not the AI Act. Under the Energy Efficiency Directive (EU) 2023/1791, Article 12, and Commission Delegated Regulation (EU) 2024/1364, a data centre with an installed IT power demand of at least 500 kW reports to the European database, first by 15 September 2024 and then by 15 May every year. Annex II sets the indicators: total energy consumption, IT equipment energy, PUE, water use, renewable share and waste heat reuse. None of them can be filled from this index, because they are facility figures. Wh/M sits one level beneath the IT energy line: it is how that total divides across tenants and workloads, and why two tenants on identical racks can draw the same kilowatts and serve very different token volumes. The AI Act, by contrast, asks nothing of an operator serving models to tenants unless the operator becomes a provider by modifying a model with more than about a third of its original training compute (Commission guidelines, July 2025).

Source: [Regulation (EU) 2024/1689](https://eur-lex.europa.eu/eli/reg/2024/1689/oj), Article 53(1)(a) and (2), Article 111(3), Annex XI, Section 1, point 2(e), and Annex XII; General-Purpose AI Code of Practice, Model Documentation Form. [Directive (EU) 2023/1791](https://eur-lex.europa.eu/eli/dir/2023/1791/oj), Article 12 and Annex VII; [Commission Delegated Regulation (EU) 2024/1364](https://eur-lex.europa.eu/eli/reg_del/2024/1364/oj), Articles 1 and 3 and Annex II; Commission guidelines on general-purpose AI models, July 2025.

Legal texts are summarised as at 27 September 2026 for orientation and are not legal advice. ESRS (2026), adopted 3 July 2026, keeps E1-5 and applies to financial years from 1 January 2027. Regulation (EU) 2026/1744, in force 27 July 2026, moved the high-risk dates to 2 December 2027 and 2 August 2028 and left the general-purpose model duties unchanged.

*5*

## Location changes carbon 23×, and not energy

Energy per token is a property of the model, the hardware and the load. Carbon per token adds the grid. On Ember's 2024 annual averages, Saudi Arabia's grid runs at 689 gCO2e per kWh and Norway's at 30. The reference row priced against them gives **43.7 kg CO2e per billion tokens** in one place and **1.9 kg** in the other, for identical tokens on identical GPUs.

So a sovereign or in-country deployment changes the carbon figure with no change to the energy figure, in either direction. Which is why the two numbers should be reported separately, and why a claim about one should never be dressed as a claim about the other.

Source: [Ember, Yearly electricity data](https://ember-energy.org/data/yearly-electricity-data/), October 2026 release, emissions intensity of total generation, 2024: a lifecycle, generation-based figure for comparing places, not a Scope 2 combustion factor to file. 193 countries in [the API](https://leadgreen.ai/api/); 22 on [the index](https://leadgreen.ai/index/#carbon).

*6*

## It is the E in the SCI

ISO/IEC 21031:2024 standardises the Software Carbon Intensity specification: SCI = ((E × I) + M) per R, where E is the energy consumed by the software, I the carbon intensity of that energy, M the embodied emissions of the hardware, and R the functional unit. For a language model, R is naturally a million output tokens. E is the energy of all the hardware reserved for the service; this index supplies the GPU part of it, which is a floor. I is the location-based grid intensity, which Ember supplies. M is an amortised share of the embodied emissions, not a total: TE × (TiR / EL) × (RR / ToR).

NVIDIA's 2,274 kg CO2e cradle-to-gate figure for an eight-GPU HGX B200 baseboard covers the baseboard only; it excludes the host, the use phase and end of life. As an illustration, spread over 5 years of continuous use it comes to 51.9 g an hour. DeepSeek V3.1 on 8 × B200 serves 32.5 million output tokens an hour at its index row, so M is about 1.6 g per million tokens, against E × I of 5.0 g on the Norwegian grid. The 5-year life is an assumption for the illustration, not a source figure.

Anyone building an SCI score for an AI service needs the E. The index is a public place to get a baseline for its GPU part.

Sources: [ISO/IEC 21031:2024](https://www.iso.org/standard/86612.html), Information technology, Software Carbon Intensity (SCI) specification; [NVIDIA, Product Carbon Footprint Summary for HGX B200](https://images.nvidia.com/aem-dam/Solutions/documents/HGX-B200-PCF-Summary.pdf), July 2025.

*7*

## Electricity per token is cheap. That is exactly why the number matters.

At the reference row, a million output tokens takes 63.5 Wh, which at USD 0.10 per kWh is **0.6 US cents**. A billion tokens is about USD 6.35. Nobody will make a decision on that bill.

But the bill is not the point. Energy per token is the power a GPU draws multiplied by the time it spends on the tokens. Watt-hours per token track GPU-hours per token, and GPU-hours are the real cost of serving, whether they are rented at cloud rates or depreciated on a balance sheet. A configuration that halves Wh/M has halved the GPU-hours per token. The electricity figure is a cheap instrument to put on an expensive thing.

Working: 63.5 Wh per million tokens is 63.5 kWh per billion; at USD 0.10 per kWh that is USD 6.35 per billion tokens, or 0.6 cents per million. The electricity price is an assumption for the worked example, not a source figure.

*8*

## Sliced GPUs are unmeasured

Multi-Instance GPU lets one A100, H100, H200 or B200 be split into up to seven isolated slices, and it is how many enterprise and telco platforms serve several small models from one card. NVIDIA publishes the slice shapes. It does not publish power draw per slice, and neither of the two public benchmarks on the index has measured a sliced card. So the configuration a great many production deployments actually run in has no public energy figure at all.

That is the first gap Lead Green intends to close with measurements of its own. First, Qwen 3 14B in BF16 on one H100, the whole card against two 3g.40gb slices each serving its own BF16 copy under the same load, beside the public 1 × H100 rows for the same model. Second, Qwen 3 32B, the whole card in BF16 against two 3g.40gb slices each serving an FP8 or INT4 copy, labelled as not like-for-like on precision. GPU power is sampled through NVIDIA DCGM, with hardware, driver, engine and prompt set named. A 32B model in BF16 does not fit a 3g.40gb slice, which is why the like-for-like run is the 14B. Until it is published, Lead Green's working answer for a sliced deployment is "unknown, and in our view above the index".

Source: [NVIDIA Multi-Instance GPU User Guide, supported MIG profiles](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/supported-mig-profiles.html), last updated 11 September 2026. Profiles on [the index](https://leadgreen.ai/index/#hardware).

*9*

## What to do on Monday

1. **Ask the vendor for Wh per million output tokens at your concurrency.** Not at theirs. Name the model, the precision, the GPU count, the workload and the latency limit, and ask for the average running batch the figure was measured at (the number of requests the server was decoding at once, not the queue). Workload matters as much as load: on the same leaderboard, the Problem Solving task costs 3 to 41 times the energy per response of Text Conversation for the same model on the same GPU, because its answers run 5,361 to 8,969 tokens against 462 to 1,464, and because the long outputs cut the batch the server can hold, so energy per token itself is 2.2 to 3.3 times the Text Conversation figure for the Qwen and DeepSeek pairs, and 0.7 to 1.0 times it for the four Nemotron pairs. If the vendor cannot answer, the index gives you the floor to hold them to. If you buy tokens from a hosted API rather than run GPUs, the concurrency is the provider's, not yours: send the questions in the [hosted API section](https://leadgreen.ai/why/#hosted) instead.
2. **Measure your own.** NVIDIA DCGM reports the GPU's energy counter; read it at the start and end of a steady load, divide the energy by the output tokens served, and you have your own row. The [measurement protocol](https://leadgreen.ai/contribute/#protocol) is short and the result can be listed beside the public ones.
3. **Put the number in the RFP.** One clause, below, turns a marketing conversation into a comparable figure across every bidder.

Source for the workload comparison: ML.ENERGY Leaderboard v3.0, Problem Solving (gpqa) against Text Conversation, energy-optimal rows at or under a 500 ms median inter-token latency, the leaderboard's own default for both tasks; no measured configuration exceeds 326 ms, so the limit changes no row; 11 model and GPU pairs measured on both.

*The clause and the scoring method*

Both have their own page, with a variant for hosted APIs: [How to put AI energy efficiency in an RFP](https://leadgreen.ai/rfp/). Fill [N] with the running batch you expect in production and [T] and [T99] with the latency your users will accept, and use the same values for every bidder.

*Hosted API*

## If you buy tokens from a hosted API

The index cannot measure a hosted API. The benchmark behind it serves open-weight models on GPUs it controls, at a load it sets. A hosted provider's fleet is closed to outsiders, its batches mix every customer's traffic, and it states no concurrency, so there is no configuration to measure and no row to compare, and "at your concurrency" has no meaning. What a buyer can do is ask the provider in writing for the figures below, then use the index to judge whether the first answer is plausible.

The reporting line differs too. On GPUs you run, the electricity is your own consumption: it goes into your ESRS E1-5 energy total, and its emissions into your Scope 2. When you buy tokens from a hosted API, the same electricity is part of the provider's operations: it is the provider's Scope 2 and your Scope 3 category 1 (purchased goods and services), and it sits outside your E1-5 total. Wh/M is the forecasting unit in both cases. Only the line it lands on differs.

**Ask the provider, in writing:**

1. The fleet-average GPU energy per million output tokens for the model and tier you buy, at the fleet's real utilisation over the period and not a best case, with the boundary stated: GPU only, or with host, network and cooling included.
2. The regions that serve your traffic, and the grid or contracted supply behind each.
3. The power usage effectiveness (PUE) of those sites, and the host-to-GPU power ratio of the serving systems.
4. The carbon factor: its source, its year, whether it is combustion-only or lifecycle, and any market-based instruments netted off, stated separately from the location-based figure.
5. The rule that allocates a shared fleet's energy to your account.
6. A restatement of these figures every quarter for the term of the contract.
7. For any per-prompt figure the provider publishes, the output length, the concurrency and the boundary behind it.

Together they give the supplier-specific figure your Scope 3 category 1 line needs, and the index tells you whether the first number is plausible.

The clause for a hosted or shared inference service is on [the RFP page](https://leadgreen.ai/rfp/#hosted), as the second lot beside the on-premise clause; the cannot-measure and confidential rules apply to it too.

*Questions*

## Asked about why the number matters

### Does the EU AI Act require reporting the energy used by AI inference?

Not per inference. Regulation (EU) 2024/1689 requires providers of general-purpose AI models to keep technical documentation for the AI Office, and Annex XI, section 1, point 2(e) names the model's known or estimated energy consumption: a training figure in MWh, held by the provider, which does not reach buyers. Article 53(2) lifts the duty from models released under a free and open-source licence with public weights unless they carry systemic risk, and Article 111(3) gives models placed on the market before 2 August 2025 until 2 August 2027. No law asks anyone for serving energy per token. Regulatory summaries on this site are as at 27 September 2026, for orientation, and are not legal advice.

### Which line of ESRS E1 does AI inference energy go on?

For GPUs you run, the electricity is energy consumption from own operations under ESRS E1-5 (paragraph 37) and its emissions are Scope 2 under E1-6, location-based and market-based. Tokens bought from a hosted API are the provider's Scope 2 and your Scope 3, category 1, purchased goods and services. In both cases the forecasting unit is energy per million tokens: tokens served next year multiplied by Wh/M gives the MWh.

### Why does an idle GPU use more energy per token than a busy one?

Because the cards' power does not fall in step with their work. On the index, Qwen 3 32B on 2 × H100 goes from 452 Wh/M at a running batch of 8 to 63.5 Wh/M at 256, 7.1× on the same hardware, while the cards' draw rises only 39 percent. A high energy per token is what an under-used server looks like from the wall socket: you are paying for silicon that is waiting.

### Does where I run AI change its energy per token?

No; it changes the carbon. The same tokens on the same GPUs use the same energy anywhere. On Ember's 2024 figures the reference row carries 43.7 kg CO2e per billion tokens on Saudi Arabia's grid (689 gCO2e per kWh) and 1.9 kg on Norway's (30), 23× apart.

### Is the electricity for AI inference expensive?

No, and that is the point. At the reference row and USD 0.10 per kWh the electricity costs about 0.6 cents per million tokens at the floor; a lightly loaded server pays several times that. Trivial as a bill, decisive as a signal: energy per token tracks GPU-hours, which is where the real money goes.

Every question on the site, with a link to the page that answers it, is on [the questions page](https://leadgreen.ai/faq/); the terms are defined in [the glossary](https://leadgreen.ai/glossary/).
