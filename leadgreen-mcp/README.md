# leadgreen-mcp

Lead Green is a public index of the GPU energy it takes to serve a million output tokens (watt-hours per million output tokens), by model, GPU and configuration, with grid carbon intensity to price it anywhere, published as open data with a JSON API and an MCP server under CC BY 4.0. Every figure comes from a named public source with a retrieval date; it is a Katonic project, run and paid for by Katonic, and takes no money from hardware, cloud or model vendors.

Lead Green is run and paid for by Katonic, which sells a sovereign AI platform; it takes no money from hardware, cloud or model vendors.

This package is the MCP server for that index: GPU watt-hours per million output tokens by model, GPU and configuration, with grid carbon intensity by country and GPU hardware reference data. Every answer names its source and carries the caveat that the figures are GPU-only floors measured on a busy server.

## Install

```
pip install leadgreen-mcp
```

or, without installing, `uvx leadgreen-mcp`.

The same wheel is served from the site, with its SHA-256 printed on <https://leadgreen.ai/mcp/>:

```
pip install https://leadgreen.ai/dist/leadgreen_mcp-0.3.0-py3-none-any.whl
```

and the source installs with `pip install "git+https://github.com/katonic-dev/leadgreen-ai#subdirectory=leadgreen-mcp"`.

Python 3.10 or later. Works with the `mcp` Python SDK 1.x and 2.x.

## Versions

Two things are versioned separately. The **package** is 0.3.0 (this file, `pyproject.toml`, the wheel name). The **data** is a dated release of the Lead Green API; the copy bundled in the package is the release named in `leadgreen_mcp/data/manifest.json` (`data_version`), and the server reads the live API first, so a session normally answers from the current release whatever package version is installed. Every response says which it used in `data_source` and `data_updated`.

## Tools

| Tool | What it answers |
|---|---|
| `list_models` | Which models are on the index and on which GPUs |
| `energy_per_million_tokens(model, gpu?, itl_deadline_ms?)` | The best row per GPU for a model |
| `estimate(model, output_tokens, gpu?, country?, running_batch?, num_gpus?, itl_deadline_ms?, pue?, system_power_ratio?)` | GPU energy in Wh and kWh for a token count, kg CO2e for a grid, and optionally energy at the meter |
| `compare_gpus(model, itl_deadline_ms?)` | H100 versus B200 for a model |
| `concurrency_curve(model, gpu)` | Energy per token at every measured running batch |
| `grid_intensity(country)` | Annual average gCO2e per kWh for a country or World |
| `gpu_hardware(gpu?)` | Max TDP, memory, MIG profiles and whole-system ceilings |
| `sources` | Every source, version, retrieval date and licence |

Resource: `leadgreen://manifest`.

### Parameters

- `running_batch`: the average running batch the server holds, meaning how many requests it decodes at once (vLLM `num_requests_running`). The estimate then uses the measured configuration nearest to it, on the same GPU count as the best row (for example 2 x H100 for Qwen 3 32B), and widens to every GPU count only when that count has no measurements. `requests_in_flight` is the old name and is still accepted; giving both with different values is an error. Responses carry both `avg_running_batch` and `avg_requests_in_flight` (the same number).
- `num_gpus`: use configurations on exactly this many GPUs.
- `itl_deadline_ms`: the latency ceiling for choosing the best row. Rows whose median inter-token latency is at or under it are kept, and the lowest energy wins. Default 500 ms, the leaderboard's own default.
- `pue` and `system_power_ratio` (each at least 1.0): when either is given, `estimate` also returns energy at the meter, GPU energy x system_power_ratio x pue, labelled as such and shown beside the GPU figure. These are your assumptions, not measurements. For scale, a DGX B200 at its 14.3 kW maximum over 8 x 1.0 kW of GPU power is a ratio of about 1.79.
- `country`: a country name, the site's short name, an ISO 3166 alpha-3 or alpha-2 code, or `World`. Common names work: UK, GB, Britain, US, USA, America, Turkey, Korea, South Korea, Russia. Exact matches win over partial ones, and queries of three characters or fewer must match exactly, so `US` never lands on Australia. Grid figures are the 2024 annual average; `years` and `latest_year` show the other years available. They are lifecycle, location-based figures for comparing places, not a Scope 2 figure to file.

### Fields on every response

- `caveat`: the same sentence on every tool, taken from the API's `index.json`. Pass it on.
- `boundary`: `gpu_only` for the measured figures.
- `data_source`: `live` (fetched from the API), `bundled snapshot` (the copy shipped in the package) or `local folder` (when `LEADGREEN_API_BASE` is a folder).
- `data_updated` and `data_version`: how current the data is.

## What the server sends, and where

- Only HTTP GET requests to `https://leadgreen.ai/api/v1` (or the base you set), for the published JSON files: at most once per file per session, then cached in memory.
- Your questions, prompts and tool arguments never leave your machine. No request carries them; lookups and arithmetic happen locally.
- If a fetch fails, the server prints one line on stderr and uses the bundled snapshot for the rest of the session without trying the network again.
- For no network at all, set `LEADGREEN_API_BASE` to a local folder holding the API files (for example a copy of `leadgreen_mcp/data`). Any other URL works too.

## Client configuration

Claude Desktop or Cursor (`claude_desktop_config.json` / `.cursor/mcp.json`):

```json
{ "mcpServers": { "leadgreen": { "command": "leadgreen-mcp" } } }
```

With no network:

```json
{ "mcpServers": { "leadgreen": { "command": "leadgreen-mcp", "env": { "LEADGREEN_API_BASE": "/path/to/api/v1" } } } }
```

Claude Code: `claude mcp add leadgreen -- leadgreen-mcp`

### If Claude Desktop cannot find `leadgreen-mcp`

Claude Desktop started from Finder, the Dock or the Start menu does not see the PATH your terminal uses, so a bare `leadgreen-mcp` can fail to start. Use the full path instead: run `which leadgreen-mcp` (macOS, Linux) or `where leadgreen-mcp` (Windows) and put the result in `command`. Alternatively, point `command` at the full path of your Python and set `"args": ["-m", "leadgreen_mcp.server"]`.

## Licence

Apache 2.0 for the code (see `LICENSE`). The data keeps the licences of its sources, listed in the manifest.
