# Bring a GPU, a red pen or a keyboard

> How to add a measurement, review a claim or write for Lead Green: the measurement protocol, the review rules, what is needed first and the licences.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/contribute/ (this file: https://leadgreen.ai/contribute/index.md). Updated 17 October 2026, data version 2026-10-17. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Contribute*

Lead Green is small and it is public. Its value is the number of independent, reproducible measurements on the index and the care with which each one is checked. Both grow faster with volunteers. Here is what is needed, how to do it, and the rules that keep a row defensible.

*Roles*

## Five ways to help  Measurers

### Run the protocol

You have access to a GPU server, on-premise or rented, and can run a serving engine under a fixed load for an hour. You produce rows. Reviewers

### Check the working

You can read a benchmark's method, recompute a figure from its raw file, and say whether a claim on the site survives contact with its source. Writers

### Explain one question

You can take one of the upcoming blog topics, or propose one, and write it with the working shown and every figure sourced. Translators

### Carry it across

The carbon table was chosen for readers in the Gulf, South Asia, South-East Asia and Central Europe. Translations of the index and the "why" page, checked by a second speaker, are welcome. Developers

### API and MCP

The build script, the JSON API and the MCP server are small Python. A hosted MCP endpoint and a per-model comparison tool are open.

*How*

## Issues and pull requests

Everything lives in the repository (link to follow once it is public): the page sources, the build script, the dated data snapshots, the API and the MCP server. Propose a change as a pull request, or open an issue if you want to discuss it first. A measurement is submitted as a JSON file in the [measurement schema](https://leadgreen.ai/api/v1/schema/measurement.schema.json) plus the logs it was computed from; a correction is submitted with a link to the primary source. The repository opens on a date to be announced on this page. Until then, send a measurement or a correction to [hello@leadgreen.ai](mailto:hello@leadgreen.ai); it will be moved into the repository under your name when the repository opens.

Contributors are credited by name on the change record and, for measurements, on the row itself. Bylines on blog posts are the author's own.

*Measurement protocol v0.2*

## How to produce a row that can sit beside the public ones

1. **Serving engine.** vLLM, the engine the public benchmark uses, so rows are comparable. Record the exact version. Other engines are welcome as clearly labelled separate rows. The public rows were made with vLLM 0.11.1 and the server flags in the benchmark's configs (max-num-batched-tokens 8192, max-model-len 20480, dtype bfloat16); record yours.
2. **Hardware.** Name the GPU model, memory, form factor (SXM, PCIe, NVL), count, any MIG profile and the weight precision (BF16, FP8, INT4). Name the driver and CUDA versions and the host. If the card is shared with anything else, say so.
3. **Prompt set.** A fixed, published prompt set with a stated average prompt length, linked or attached so another measurer can repeat it. To match the public rows, use the benchmark's own sample: lmarena-ai/arena-human-preference-100k (train), field conversation_a, one request per turn with the full history as the prompt, 1,024 requests, seed 0, as in the benchmark's datasets.py; for Qwen 3 pass chat_template_kwargs enable_thinking false. Or run the [benchmark harness](https://github.com/ml-energy/benchmark) itself and submit its output.
4. **Load.** Send at least 1,000 requests with the server's max_num_seqs as the only cap. The window starts when max_num_seqs requests have returned a first token and ends when all but max_num_seqs + 1 requests have finished (the public benchmark's rule); it must last at least five minutes, so send more requests at high concurrency. Record the average running batch the server actually held (vLLM's `num_requests_running`, scraped every second inside the window and averaged), not only the cap.
5. **Energy.** Read the GPU energy counter at the start and end of the window for every card (DCGM field 156, `DCGM_FI_DEV_TOTAL_ENERGY_CONSUMPTION`, millijoules); it is the counter the public benchmark reads through Zeus. Also log board power (field 155, `DCGM_FI_DEV_BOARD_POWER_WATTS`) every second for the average power column. If you only have `nvidia-smi`, sample `power.draw` every second, integrate, and say so.
6. **Latency and tokens.** Use a client that records the time of every streamed token, such as `vllm bench serve` with `--save-result`, which reports median and p99 inter-token latency, and attach its JSON. Read `vllm:generation_tokens_total` at both ends of the window, and record the average output length and the average prompt length.
7. **Report.** Joules per output token (energy ÷ output tokens), Wh per million (× 1,000,000 ÷ 3,600), median and p99 inter-token latency, tokens per second, average power summed across cards, and the fields above, in the [measurement schema](https://leadgreen.ai/api/v1/schema/measurement.schema.json); the example file `build/data/measurements/2026-09-26-example-qwen-3-14b-h100-3g40gb-x2.json` has every field filled. The build validates every file against the schema and refuses to publish one that fails. Attach the power log and the engine's metrics log; strip request bodies from engine logs, or link the prompt set instead of reproducing it. A row is comparable with the index only if its median inter-token latency is at or under 500 ms.
8. **Repeat.** Two runs; report both and the mean. If joules per output token differ by more than 5 percent between runs, say why or run a third.

The protocol measures GPU energy only, like the index. If you also have facility or host power, report it as separate fields; do not fold it in. The same goes for water: if you know the site's water use, report it in the optional site water field as water usage effectiveness (litres per kWh of IT energy, ISO/IEC 30134-9), never folded into Wh/M. Power for a sliced card is the whole card's; no tool reports power per slice. Load every slice with the same workload at the same time, read the card's energy exactly as for an unsliced card, and report Wh/M for the card with `mig_profile`, `slice_count` and `slices_loaded`. Never divide the card's power by the slice count, and never report a slice measured while the other slices sit idle. Compare a sliced run with the same person's whole-card run on the same card in the same session; the public 1 × H100 rows are the reference.

*Review rules*

## What it takes to land on the index

- **Two reviewers** for a new row or a changed figure, one of whom recomputes the number from the attached logs or the source file. The reviewers are two named reviewers, listed here before the first contributed row is accepted. Any row Katonic measures is also checked by a named reviewer with no Katonic affiliation, to be named here before the first Katonic row is published. A decision within 30 days.
- **Where accepted rows go.** Accepted rows are served at [`/api/v1/measurements.json`](https://leadgreen.ai/api/v1/measurements.json) with contributor, affiliation, measured_on, engine_version, driver_version and mig_profile on each row, and listed on the index under [Contributed measurements](https://leadgreen.ai/index/#contributed) with the contributor's name. They are never merged into the index table. A contributed row states its median inter-token latency; rows above 500 ms are shown and flagged.
- **Source snapshot.** Every public figure is taken from a dated copy of the source file, kept with the site, so it can be recomputed later even if the source moves.
- **Claims ledger.** Every figure on every page has a source and a retrieval date in the sources list. If it cannot be sourced, it does not ship.
- **Corrections** are made in the open: the change record on the index names what changed, when and why, and a corrected blog post keeps a note at the top.
- **Vendor rows are labelled.** A measurement made by or paid for by a hardware, cloud or model vendor is marked as such and shown separately from independent rows.
- **No customer names.** A measurement from a production site is described by hardware and workload, not by whose site it is.

*Needed first*

## The gaps, in order

1. **MIG slices.** Any model on a 1g, 2g or 3g slice of an H100 or H200, against the same model on the same whole card, measured by the same person in the same session with the same engine, driver and prompt set. Nothing public exists. The API's 1 × H100 rows are the public reference: for Qwen 3 14B in BF16, 196.1 Wh/M at a cap of 8 down to 31.1 at 256.
2. **Other GPUs.** A100, H200, L40S, and AMD MI300X. The index has H100 and B200 only.
3. **Hourly grid data.** Annual averages hide a lot. Hourly intensity for the grids on the carbon table, from a source whose licence allows republishing.
4. **Translations.** Arabic, Serbian, Traditional Chinese, Tagalog and Sinhala first, for the readers the carbon table was built for.
5. **Water.** Site water use beside any contributed row, as its own field. The index has none, and the two public per-prompt figures are measured on different boundaries and units of work.
6. **Reviews.** A second pair of eyes on any figure on the site, starting with the ones that get cited most.

*Licences*

## What you give and what you get

Code (the build script, the API generator, the MCP server) is Apache 2.0. Data and text (the compiled index, derived figures, page text, blog posts) are CC BY 4.0. By contributing you agree your contribution is offered under the same terms: your row and your logs are CC BY 4.0, and prompt sets keep their own licence. Sign commits with a Developer Certificate of Origin line (`Signed-off-by`). Public sources keep their own licences, which are listed per source and never overridden.
