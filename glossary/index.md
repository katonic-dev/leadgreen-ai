# The nine terms behind the index

> Nine defined terms behind the index, one page each with the figure and the source: Wh per million tokens, energy per token, running batch, floor, PUE.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/glossary/ (this file: https://leadgreen.ai/glossary/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Glossary*

Every figure on this site depends on a handful of defined terms: the unit, the boundary, the load, the latency limit and the carbon factor. Each has one page that states the definition, the figure and the source in its first paragraph, with the working underneath. Read them once and every row on the index reads the same way.

**Unit** watt-hours per million output tokens (Wh/M). GPU only, busy server. Every row is a floor. Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Glossary: the terms behind GPU energy per token. https://leadgreen.ai/glossary/, release 2026-10-19, retrieved [date]. CC BY 4.0.

*Terms*

## One page each  Term

### [Watt-hours per million output tokens (Wh/M)](https://leadgreen.ai/glossary/watt-hours-per-million-output-tokens/)

The unit of the index: the GPU energy, in watt-hours, that a serving configuration uses to generate one million output tokens. Term

### [Energy per token](https://leadgreen.ai/glossary/energy-per-token/)

GPU energy divided by the output tokens generated in the same steady-state window, in joules per token; the quantity the index converts to Wh/M. Term

### [Running batch](https://leadgreen.ai/glossary/running-batch/)

The average number of requests a serving engine was decoding at once over the measurement window, under continuous batching; the variable that moves energy per token most. Term

### [Floor](https://leadgreen.ai/glossary/floor/)

What every index row is: the lowest GPU energy per token measured for a model and GPU under the latency ceiling, which a real deployment sits above. Term

### [GPU-only boundary](https://leadgreen.ai/glossary/gpu-only-boundary/)

The measurement boundary of every index row: energy read from the GPUs alone, with host, network, cooling, idle time and embodied carbon outside it. Term

### [Location-based grid intensity](https://leadgreen.ai/glossary/location-based-intensity/)

The average carbon intensity of the electricity generated where a GPU runs, in gCO2e per kWh; the factor that turns energy per token into carbon per token. Term

### [kg CO2e per billion output tokens](https://leadgreen.ai/glossary/kg-co2e-per-billion-tokens/)

The carbon unit of the index: energy per million tokens multiplied by the grid's carbon intensity, which gives kilograms of CO2e per billion output tokens. Term

### [Inter-token latency ceiling](https://leadgreen.ai/glossary/inter-token-latency-ceiling/)

The latency limit that defines which configurations may be an index row: a median inter-token latency at or under 500 ms, the leaderboard's own default. Term

### [Power usage effectiveness (PUE)](https://leadgreen.ai/glossary/pue/)

Total facility energy divided by IT equipment energy, per ISO/IEC 30134-2; the operator's own multiplier that takes a GPU figure to the building's meter.

Each term's page carries its own FAQ and sources, and a Markdown copy at its URL followed by `index.md`. The terms are also the vocabulary of the [measurement protocol](https://leadgreen.ai/contribute/#protocol) and the [RFP clause](https://leadgreen.ai/rfp/).
