# How to put AI energy efficiency in an RFP

> The clause to paste, the scoring box and a hosted-API variant: GPU watt-hours per million output tokens at a stated running batch and latency.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/rfp/ (this file: https://leadgreen.ai/rfp/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*[Why it matters](https://leadgreen.ai/why/) · Procurement*

Ask every bidder for the same figure at the same load: GPU energy per million output tokens (Wh/M) for each proposed model and serving configuration, measured at steady state on the proposed hardware at a stated average running batch, with median and p99 inter-token latency reported, GPU energy only, naming the method, the tool, the versions and the date. Score the answers with a gate on completeness, a floor from [the index](https://leadgreen.ai/index/)'s rows for the same model and GPU, a challenge at 10 percent below the floor, and the consistency check Wh/M = average GPU power ÷ output tokens per second × 1,000,000 ÷ 3,600. The clause, the scoring box and a second clause for hosted APIs are below, ready to paste.

**Unit** watt-hours per million output tokens (Wh/M), GPU only. **Floors** [index.json](https://leadgreen.ai/api/v1/index.json) and [models.json](https://leadgreen.ai/api/v1/models.json). Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. How to put AI energy efficiency in an RFP. https://leadgreen.ai/rfp/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [What to ask for](https://leadgreen.ai/rfp/#ask)
- [The clause](https://leadgreen.ai/rfp/#clause)
- [Scoring](https://leadgreen.ai/rfp/#scoring)
- [Hosted API](https://leadgreen.ai/rfp/#hosted)
- [Questions](https://leadgreen.ai/rfp/#faq)
- [Sources](https://leadgreen.ai/rfp/#sources)

*What to ask for*

## Six things every answer must carry

An energy figure without its load, its latency and its boundary cannot be compared with another bidder's. The clause asks for all six together; the scoring box treats an answer missing any of them as not stated.

*The figures the clause asks every bidder for, and why each is there*

| Ask for | Unit | Why it is in the clause |
|---|---|---|
| GPU energy per million output tokens | Wh/M | The comparable figure. One Wh/M is 0.0036 joules per output token; the index runs from 13.0 to 572.9 Wh/M across its rows. |
| Average running batch held, and the cap | requests | Load moves the figure more than hardware does: 7.1× for the reference model on the same cards between a running batch of 8 and 256. A cap of 256 with eight users is a running batch of eight. |
| Median and p99 inter-token latency | ms | The same latency limit for every bidder is what makes two figures comparable; a looser limit buys a lower number. |
| Output tokens per second and average GPU power | tokens/s, W | The consistency check: Wh/M must equal power ÷ throughput × 1,000,000 ÷ 3,600. On the reference row, 1,177.9 W ÷ 5,155.5 tokens per second = 63.47 Wh/M. |
| The boundary statement | GPU only | So that no bidder folds host, network or cooling into the figure, or leaves them out without saying so. Facility multipliers are the operator's own and belong in a separate line. |
| Method, tool, versions, date, prompt set | text | What makes the measurement repeatable and the floor comparison fair; the [measurement protocol](https://leadgreen.ai/contribute/#protocol) names the defaults. |

Power usage effectiveness and renewable share describe the building, not the work. Keep them in the facility section of the RFP; the clause below measures the model, the GPUs and the load.

*The clause*

## On-premise or dedicated GPUs, ready to paste

*RFP clause, ready to paste*

"The bidder shall state the GPU energy per million output tokens (Wh/M) for each proposed model and serving configuration, measured at steady state with the proposed serving engine on the proposed hardware, at an average running batch of [N] and with median inter-token latency not exceeding [T] ms and p99 inter-token latency not exceeding [T99] ms, both reported, on the prompt set supplied by the buyer in Annex [X], stating the average prompt and output token counts measured; where the buyer supplies none, on the LM Arena conversation sample used by the ML.ENERGY Leaderboard v3.0, named as such. Steady state, running batch and latency are as defined in the Lead Green measurement protocol v0.2 (leadgreen.ai/contribute/#protocol): a fixed cap of [N] sequences, held at least five minutes after warm-up and for at least 1,000 requests; the bidder shall report both the cap and the average running batch the server actually held, and the median and p99 inter-token latency over the same window. The bidder shall name the measurement method, the sampling tool, the software versions and the date. The figure shall be GPU energy only; host, network and cooling energy, where measured, shall be reported as separate figures and not folded in. The bidder shall attach the GPU power log and serving-engine log from which the figure was computed and shall state time to first token at the same load. The buyer may repeat the measurement on the delivered system at acceptance with the same prompt set; a result more than [X] percent above the stated figure is a non-conformance. Figures for sliced (MIG) configurations shall be measured with every slice on the card serving the proposed workload at the same time, reporting the card's energy per million output tokens, the slice profile, the slice count and the slices loaded. No figure may divide the card's energy by a slice count or come from a run in which any slice sat idle. A figure derived from a whole-card measurement at a different profile is not acceptable. Any carbon figure quoted shall name the grid, the emission factor source and year, whether the factor is combustion-only or lifecycle, and whether any market-based instruments have been applied, with the location-based figure stated in all cases. A bidder that cannot measure GPU energy for the proposed service, for example a hosted API on a closed-weight model, shall state that it cannot, shall attach the model provider's published energy documentation if any (Regulation (EU) 2024/1689, Annex XI, Section 1, point 2(e)), and shall not substitute a per-query or per-request figure that lacks the output token count, the concurrency and the hardware. A figure withheld as confidential is treated as not stated. The bidder may mark the raw logs confidential; the figure, the method, the running batch, the latency and the inclusion statement are not confidential and will be shared across the evaluation panel."

Fill [N] with the running batch you expect in production and [T] and [T99] with the latency your users will accept. The index uses 500 ms, the leaderboard's default, as a benchmark ceiling, not a recommendation, and no measured configuration reaches it. For an interactive assistant set [T] where your users would notice, and use the same [N] and [T] for every bidder. Everything else in the clause is there so that two bidders' numbers can be compared.

*Scoring*

## How to score the answers

Seven rules, in order. The floor comes from the index's rows for the same model and GPU, so a bidder's number is checked against a public measurement rather than against the other bidders.

*Scoring the answers*

1. **Gate.** An answer counts only if it carries the figure, the cap and the average running batch held, median and p99 inter-token latency, average output tokens per response, output tokens per second, average GPU power summed across cards, the method, the tool, the versions, the date and the GPU-only statement. An answer missing any of them scores zero on this criterion and is not disqualified.
2. **Floor.** For the same model and GPU, the floor is the configuration in `models/<slug>.json` with the smallest average running batch at or above [N] whose median inter-token latency is at or under [T] ms; if there is none, the configuration with the highest measured running batch.
3. **Tolerance.** An answer more than 10 percent below the floor is challenged, and the bidder supplies the raw power and engine logs. The protocol's own repeat threshold is 5 percent.
4. **Consistency.** Wh/M must equal average GPU power ÷ output tokens per second × 1,000,000 ÷ 3,600. On the reference row: 1,177.9 W ÷ 5,155.5 tokens per second × 1,000,000 ÷ 3,600 = 63.47 Wh/M. An answer that fails the check beyond rounding is treated as not stated.
5. **Cannot measure.** An answer that declares it cannot measure, as the clause provides, is scored as not stated, not compared.
6. **Confidential.** A figure withheld as confidential is scored as not stated. Logs may be confidential; the figure, method, running batch, latency and inclusion statement may not.
7. **Where Katonic bids.** Lead Green is a Katonic project. In a tender where Katonic may bid, take floor values from the ML.ENERGY rows directly and disclose the compilation, using the wording in [Using the index in a tender](https://leadgreen.ai/about/#tender).

*Hosted API*

## If the lot is a hosted or shared inference service

The index cannot measure a hosted API: its fleet is closed, its batches mix every customer's traffic and it states no concurrency. The clause below asks the provider for the fleet-average figure and the facts behind it, and the index tells the buyer whether the first answer is plausible. The [why page](https://leadgreen.ai/why/#hosted) has the seven questions to ask in writing and the reporting line the tokens land on.

*RFP clause, hosted or shared inference service*

"For a hosted or shared inference service, the bidder shall state, for each proposed model and service tier, the fleet-average GPU energy per million output tokens (Wh/M) over the preceding quarter at the fleet's actual utilisation, and shall state whether host, network and cooling energy are included; where they are measured they shall be reported as separate figures and not folded in. The bidder shall name the facilities and grid regions that will serve the buyer's traffic and the grid or contracted supply behind each, shall state their power usage effectiveness and the host-to-GPU power ratio of the serving systems, and shall state the rule by which the energy of a shared fleet is allocated to the buyer. Any carbon figure quoted shall name the grid, the emission factor source and year, whether the factor is combustion-only or lifecycle, and whether any market-based instruments have been applied, with the location-based figure stated in all cases. Any per-prompt or per-request figure offered shall state the output length, the concurrency and the boundary behind it. The bidder shall restate these figures to the buyer every quarter for the term of the contract. A bidder that cannot state the fleet figure shall say so; that answer is scored as not stated, not compared."

Use it as the second lot beside the on-premise clause above, so a tender with both lots scores both. The cannot-measure and confidential rules in "Scoring the answers" apply to it too.

*Sources*

## Where the floors come from

[ML.ENERGY Leaderboard](https://ml.energy/leaderboard/) version 3.0 (released 1 December 2025; data compiled 16 February 2026; retrieved 26 September 2026), The ML.ENERGY Initiative, started at SymbioticLab, University of Michigan. Text Conversation task, 328 stable configurations. Energy per token is steady-state GPU energy divided by the output tokens generated in the window, measured with Zeus under vLLM 0.11.1 on H100 80GB HBM3 and B200 servers; energy per request is that figure times the average output length. Each index row is the lowest-energy configuration for its model and GPU at or under a 500 ms median inter-token latency, the leaderboard's own default ceiling, which no configuration reaches. Apache 2.0 per the [ml-energy/benchmark-v3](https://huggingface.co/datasets/ml-energy/benchmark-v3) dataset card. Cite [Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks](https://arxiv.org/abs/2505.06371). The floor for a model and GPU is the configuration in `models/<slug>.json` that the scoring box names; the tolerance and repeat thresholds are the index's own (10 and 5 percent).

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.

*Questions*

## Asked about AI energy in an RFP

### How do I put AI energy efficiency in an RFP?

Ask every bidder for the same figure at the same load: GPU energy per million output tokens (Wh/M) for each proposed model and serving configuration, measured at steady state on the proposed hardware at a stated average running batch, with median and p99 inter-token latency reported, on the buyer's prompt set or the ML.ENERGY Leaderboard's conversation sample, GPU energy only, naming the method, the tool, the versions and the date. Score it with a gate on completeness, a floor from the index's rows for the same model and GPU, a challenge at 10 percent below the floor, and the consistency check Wh/M = average GPU power ÷ output tokens per second × 1,000,000 ÷ 3,600. The clause and the scoring box on this page are ready to paste.

### What unit should an RFP use for AI energy?

GPU watt-hours per million output tokens (Wh/M), GPU energy only, at a stated running batch and latency. It is the one figure that ties a named model on named GPUs to a measured load, and it is what the index's rows are in, so every answer has a public floor to be checked against. Watt-hours per query need an output length and a load to mean anything, and power usage effectiveness describes the building, not the work.

### What running batch and latency should the RFP specify?

The running batch you expect in production, as a number [N], and the median [T] and p99 [T99] inter-token latency your users will accept, the same for every bidder. Load moves the figure more than hardware does: Qwen 3 32B on 2 × H100 runs from 452 Wh/M at a running batch of 8 to 63.5 Wh/M at 256, 7.1× on the same cards. The index uses 500 ms as a benchmark ceiling, not a recommendation.

### How do I score a bidder's energy figure?

Gate first: an answer counts only if it carries the figure, the cap and running batch held, median and p99 latency, output tokens per response, tokens per second, average GPU power, the method, the tool, the versions, the date and the GPU-only statement. Then compare it with the floor, the index row for the same model and GPU at or above the stated running batch; challenge any answer more than 10 percent below it and ask for the power and engine logs. Last, check Wh/M = average GPU power ÷ output tokens per second × 1,000,000 ÷ 3,600; an answer that fails beyond rounding is treated as not stated.

### Can I ask a hosted API provider for energy per token?

Yes, as a fleet-average figure over the preceding quarter at the fleet's actual utilisation, with the boundary stated, the serving regions and their grids named, the sites' PUE and host-to-GPU power ratio given, the rule that allocates a shared fleet's energy to your account, and a quarterly restatement for the term. The index cannot measure a hosted fleet, but it tells you whether the first answer is plausible. The electricity is the provider's Scope 2 and your Scope 3, category 1.

### Is PUE enough to compare AI vendors on energy?

No. Power usage effectiveness is the building's overhead on top of the IT load; it says nothing about how much work the IT load does. Two vendors at the same PUE can differ many times in GPU energy per token through model, precision, GPU generation and load. Ask for PUE in the facility section and for Wh/M at a stated load in the clause, and keep the two apart.

Every question on the site, with a link to the page that answers it, is on [the questions page](https://leadgreen.ai/faq/); the terms are defined in [the glossary](https://leadgreen.ai/glossary/).
