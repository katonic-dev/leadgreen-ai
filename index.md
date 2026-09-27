# The energy behind the token

> A public index of the GPU energy it takes to serve a million output tokens, by model and GPU, with grid carbon, open data, an API and an MCP server.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/ (this file: https://leadgreen.ai/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

Lead Green is a public index of the **GPU watt-hours it takes to serve a million output tokens**, by model, GPU and configuration, with the grid carbon to price it anywhere. Every figure is from a named public measurement or a manufacturer's specification, dated and linked. The data is open, there is a JSON API and an MCP server, and anyone with a GPU will be able to add a measurement.

**Unit** watt-hours per million output tokens (Wh/M). One Wh/M is 0.0036 joules per token. GPU only, busy server. Every row is a floor. Updated 27 September 2026.  [Read the index](https://leadgreen.ai/index/) [Why it matters](https://leadgreen.ai/why/) [Use the data](https://leadgreen.ai/api/)
-  **Lowest floor on the index:**  13.0 Wh/M  Llama 3.1 8B Instruct, 1 × B200. Running batch 2,043, median ITL 125 ms.
-  **Reference floor:**  63.5 Wh/M  Qwen 3 32B, 2 × H100. Running batch 256, median ITL 44 ms. The carbon table is priced on this row.
-  **Highest floor on the index:**  572.9 Wh/M  Llama 3.1 405B Instruct FP8, 8 × H100. Running batch 255, median ITL 67 ms.

A million output tokens is roughly three quarters of a million words of English. The index spans **44×** from its lowest row to its highest, and the same model on the same two GPUs moves **7.1×** depending on how busy the server is. Every row is a floor. The number a buyer should ask for is the one measured on their own server.

*What it is*

## One unit, one place, for people and for machines  Index

### Green Tokens

32 rows, 18 open-weight models, two GPU generations, with the concurrency curves, the carbon table and the hardware ceilings behind them. Method and sources on the page, and [one page per model](https://leadgreen.ai/models/).[The index](https://leadgreen.ai/index/) API

### Read-only JSON

Every table as static JSON, CORS open, versioned, additive only. Pull it into a spreadsheet, a dashboard or a procurement model.[Data API](https://leadgreen.ai/api/) MCP

### Tools for assistants

An MCP server so Claude, Cursor or any MCP client can answer "how much energy would fifty million tokens of this model use, and what is the carbon in Serbia" with sourced numbers.[MCP server](https://leadgreen.ai/mcp/) Blog

### The reasoning behind the rows

Short, sourced pieces on what the numbers mean: the baseline, the idle token, sliced GPUs, per correct answer, where the electricity is, what the regulator asks.[Blog](https://leadgreen.ai/blog/) Newsletter

### One number a month

The Green Tokens edition: one reading from the index, one note on what moved, one pointer to read further.[Newsletter](https://leadgreen.ai/newsletter/) Contribute

### Measure, review, write

A measurement protocol anyone with a GPU can follow, and a review process so that what lands on the index can be defended.[Contribute](https://leadgreen.ai/contribute/)

*Why it exists*

## Everyone buys tokens. Nobody is told the energy.

Enterprises are buying GPUs by the rack and tokens by the billion, and neither invoice carries an energy figure. Model vendors have published, at most, a per-prompt average of energy, carbon and water with no load, output length or method a buyer could compare ([Google, August 2025](https://arxiv.org/abs/2508.15734); [Mistral, July 2025](https://mistral.ai/news/our-contribution-to-a-global-environmental-standard-for-ai)). None publishes watt-hours per million output tokens at a stated concurrency. The cloud providers do not itemise one. The measurements that do exist are academic and scattered across leaderboards and papers, in different units, on different hardware, under different load. A CIO who wants to know what a million tokens costs in watt-hours has nowhere to look it up.

Meanwhile the questions are arriving. Boards want the AI line in the energy report. Auditors want to know how Scope 2, or Scope 3 for a hosted API, grows when the assistants roll out. The EU AI Act already requires providers of general-purpose AI models to document the model's energy consumption for the AI Office, with exemptions for open-weight models. No law asks anyone for serving energy per token; buyers should. Sovereign and on-premise deployments run inside a fixed power envelope, so energy per token sets how much AI a site can serve at all.

Lead Green puts the public measurements in one unit on one page, explains what they mean, exposes them to software, and adds measurements of its own as they are made. It is run and paid for by [Katonic](https://www.katonic.ai), which sells a sovereign AI platform and benefits when buyers ask the questions on this site. It takes no money from hardware, cloud or model vendors.

*Why you should care*

## Six of the nine reasons  Utilisation7.1× same model, same GPUs

Energy per token is a utilisation meter. A high reading means you are paying for silicon that is waiting. Power is the ceiling15.8 bn tokens per GPU MWh

At the reference row, per megawatt-hour of GPU energy. At the top of the concurrency ladder the same megawatt-hour serves 2.2 billion. On a fixed feed, the number decides how much AI you can run. Location23× carbon, same tokens

Saudi grid against Norwegian grid, 2024 averages. Geography changes the carbon number and not the energy number. [One page per grid.](https://leadgreen.ai/grids/) ReportingE1-5 ESRS

European sustainability reporting asks for energy consumption in MWh. AI served on your own GPUs is a growing line inside it, and it needs a per-token figure to forecast. RegulationAnnex XI 1.2(e) EU AI Act

Providers of general-purpose AI models must record the model's known or estimated energy consumption in documentation held for the AI Office. The law's figure is training energy in MWh, and it does not reach buyers. No law yet asks anyone for serving energy per token. This index is the figure buyers need while that stays true. Cheap, and that is the point0.6¢ per million tokens

Electricity at the reference row, priced at USD 0.10 per kWh, at the floor; a lightly loaded server pays several times this. Trivial as a bill, decisive as a signal: it tracks GPU-hours, which is where the real money goes.

[All nine, with the working and the sources, and an RFP clause you can paste.](https://leadgreen.ai/why/)

*Who it is for*

## Five desks, one number

### CIO and CTO

To size a GPU estate against a power budget, to know what on-premise inference would cost in energy before a hosted invoice becomes a power bill, and to answer the board. Hosted APIs cannot be measured from outside; [the why page](https://leadgreen.ai/why/#hosted) says what to ask the vendor instead.

### Sustainability officer

To put AI serving into the energy and Scope 2 lines with a defensible method, and to know which questions to send back to the vendor.

### Platform engineer

To see what concurrency, quantisation and GPU generation do to energy per token, and to measure their own cluster against a public baseline.

### Procurement

To ask every bidder for the same figure at the same load, in [a clause](https://leadgreen.ai/why/#monday) that names the unit and the latency limit and tells you what to fill in, with a scoring method beside it.

### Facility and capacity planner

You own the feed, the power envelope and the capacity meeting. The index gives you GPU energy per unit of work and the two multipliers that take it to the meter, so a contracted feed becomes tokens per hour at a stated PUE and server overhead. It does not give you PUE, water, waste heat or anything else in facility units.

*How to use it*

## Three ways in

1. **Read.** Start with the three tiles and the concurrency section of [the index](https://leadgreen.ai/index/). If you take one thing away, take the 7.1× ladder.
2. **Compute.** Pull `index.json` and `grid.json` from the [API](https://leadgreen.ai/api/). Multiply Wh per million by your monthly tokens for energy; multiply by your grid's gCO2e per kWh and divide by 1,000 for kg CO2e per billion tokens.
3. **Ask.** Add the [MCP server](https://leadgreen.ai/mcp/) to your assistant and ask in plain words. It answers with the row, the source and the caveat.

Latest from the blog: [What a million tokens costs in watt-hours](https://leadgreen.ai/blog/what-a-million-tokens-costs-in-watt-hours/).
