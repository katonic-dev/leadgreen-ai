# Ask your assistant, get a sourced number

> An MCP server that gives Claude, Cursor and other assistants the Green Tokens index as tools: energy by model and GPU, estimates, carbon and sources.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/mcp/ (this file: https://leadgreen.ai/mcp/index.md). Updated 27 September 2026, data version 2026-09-27. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*MCP server*

The Model Context Protocol (MCP) is an open standard that lets an AI assistant call tools a server exposes. Lead Green ships a small MCP server so that Claude, Cursor or any MCP-capable client can answer questions about the index with the row, the source and the caveat attached, instead of guessing.

**Package** leadgreen-mcp 0.2.0 · **Transport** stdio · **Data** the live API, with a bundled snapshot as fallback · **Licence** Apache 2.0 · **Wheel SHA-256** `b47948b9b23259a94759821a7584dd1174c64593276ce826b3b1ed01fb10957b`

*Install*

## One line

```
pip install https://leadgreen.ai/dist/leadgreen_mcp-0.2.0-py3-none-any.whl#sha256=b47948b9b23259a94759821a7584dd1174c64593276ce826b3b1ed01fb10957b
```

Or run it without installing, with [uv](https://docs.astral.sh/uv/):

```
uvx --from https://leadgreen.ai/dist/leadgreen_mcp-0.2.0-py3-none-any.whl leadgreen-mcp
```

pip checks the wheel against the SHA-256 in the line above and refuses a file that does not match. To rebuild it byte for byte from the site source: `SOURCE_DATE_EPOCH=1790467200 python -m pip wheel ./leadgreen-mcp --no-deps`. Python 3.10 or later. The server works with the `mcp` Python SDK 1.x and 2.x. It reads the API over HTTPS on first use and falls back to the snapshot bundled in the package when the site cannot be reached, so it also works offline. Every response says which it used.

*What it sends, and where*

## GET requests to one host, and nothing else

- **Where.** Only to `https://leadgreen.ai/api/v1/`, or to the base you set in `LEADGREEN_API_BASE`. Plain HTTPS GET requests for the published JSON files, once per file per session.
- **What never leaves your machine.** Your questions, your token counts, your country and anything else you pass to a tool. The arithmetic happens locally.
- **No network at all.** Point `LEADGREEN_API_BASE` at a local folder holding the API files and the server makes no requests.
- **When the site cannot be reached.** After the first failed fetch the server stops trying for the rest of the session, prints one line to stderr, and answers from the snapshot bundled in the package. Every response carries `data_source` (`live`, `local folder` or `bundled snapshot`) and `data_updated`, so a session left open for a month says how old its figures are.

*Configure*

## Three clients

### Claude Desktop

Add to `claude_desktop_config.json` (Settings, Developer, Edit Config):

```
{
  "mcpServers": {
    "leadgreen": { "command": "leadgreen-mcp" }
  }
}
```

### Claude Code

```
claude mcp add leadgreen -- leadgreen-mcp
```

Claude Desktop started from the Finder or the Start menu may not see the folder pip installed into. If the server does not appear, use the full path that `which leadgreen-mcp` (macOS, Linux) or `where leadgreen-mcp` (Windows) prints as the command, or run `python -m leadgreen_mcp.server`.

### Cursor

Add the same block to `.cursor/mcp.json` in the project, or to the global file from Cursor Settings, MCP.

If you run it with uv rather than installing it, use `"command": "uvx", "args": ["--from", "https://leadgreen.ai/dist/leadgreen_mcp-0.2.0-py3-none-any.whl", "leadgreen-mcp"]` instead.

*Tools*

## Eight tools, one resource

*What the server exposes, and a prompt that would call it*

| Tool | Answers | Try asking |
|---|---|---|
| list_models | Every model on the index, with slugs, ids, parameter counts and measured GPUs | "Which models does Lead Green have energy figures for?" |
| energy_per_million_tokens | The index rows for one model, optionally one GPU | "What is the energy per million tokens for Llama 3.1 70B on H100?" |
| estimate | Wh and kWh for a token count, with kg CO2e for a country; optionally at a given running batch and card count, under a latency ceiling, and at the meter with your PUE and system-to-GPU power ratio | "How much energy would 50 million tokens of Qwen 3 32B use on H100s, and what is the carbon in Serbia?" |
| compare_gpus | H100 against B200 for a model, with the ratio | "How much does B200 save over H100 for DeepSeek V3.1?" |
| concurrency_curve | Energy per token at every measured concurrency | "Show me how energy per token changes with load for Qwen 3 8B on B200" |
| grid_intensity | Annual average gCO2e per kWh for a country or World, with 2023 to 2025 where Ember has them. Accepts names, ISO codes and common short forms (UK, US, Korea) | "What is the grid carbon intensity of the UK?" |
| gpu_hardware | Max TDP, memory and MIG profiles | "What MIG slices can an H200 be split into?" |
| sources | Every source, version, retrieval date, licence and endpoint | "Where do these numbers come from?" |

The resource `leadgreen://manifest` returns the same manifest as a document. Every tool response carries `caveat`, `boundary` (`gpu_only`), `data_source` and `data_updated`. The caveat is the same string the API documents carry; a well-behaved assistant repeats it.

*Worked example*

## Fifty million tokens in Serbia

The estimate tool for Qwen 3 32B on H100, 50,000,000 output tokens, country Serbia, uses the index's best H100 row (63.47 Wh/M, the API's two-decimal value) and Ember's 2024 figure for Serbia (668 gCO2e per kWh):

- Energy: 63.47 Wh/M × 50 M = **3,173.5 Wh**, or 3.1735 kWh.
- Carbon: 3.1735 kWh × 668 g ÷ 1,000 = **2.12 kg CO2e**.

Add `pue` and `system_power_ratio` and the answer also carries energy at the meter: GPU energy times the system-to-GPU power ratio times the PUE, labelled as such. Both are your figures, not the index's; the [method](https://leadgreen.ai/index/#method) gives the DGX B200 ratio of 1.79 as an example.

Pass `running_batch` (`requests_in_flight` is still accepted as an alias) and the tool switches from the best row to the measured configuration on the same card count nearest that running batch (pass `num_gpus` for another count; the `basis` field names the row it used), which for a lightly loaded server can multiply the answer several times. In the deployments the editor sees, that is the number that applies.

*Settings*

## Environment

| Variable | Effect |
|---|---|
| LEADGREEN_API_BASE | Another base URL, or a local folder holding the API files. Default https://leadgreen.ai/api/v1. |
| LEADGREEN_TIMEOUT | Seconds to wait for the site before falling back to the bundled snapshot. Default 10. |

A hosted (HTTP) endpoint, so that clients need no local install, is a later step. The source is in the repository (link to follow once it is public).
