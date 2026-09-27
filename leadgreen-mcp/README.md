# leadgreen-mcp

MCP server for the Lead Green Green Tokens index: GPU watt-hours per million output tokens by model, GPU and configuration, with grid carbon intensity by country and GPU hardware reference data. Every answer names its source and carries the caveat that the figures are GPU-only floors measured on a busy server.

Data comes from the site's read-only JSON API at `https://leadgreen.ai/api/v1`. If the site cannot be reached, the snapshot bundled in `leadgreen_mcp/data/` is used. Set `LEADGREEN_API_BASE` to another base URL, or to a local folder holding the API files, to override.

## Install

```
pip install https://leadgreen.ai/dist/leadgreen_mcp-0.1.0-py3-none-any.whl
```

or, without installing, `uvx --from https://leadgreen.ai/dist/leadgreen_mcp-0.1.0-py3-none-any.whl leadgreen-mcp`.

Works with the `mcp` Python SDK 1.x and 2.x.

## Tools

| Tool | What it answers |
|---|---|
| `list_models` | Which models are on the index and on which GPUs |
| `energy_per_million_tokens(model, gpu?)` | The index rows for a model |
| `estimate(model, output_tokens, gpu?, country?, requests_in_flight?)` | Energy in Wh and kWh for a token count, and kg CO2e for a grid |
| `compare_gpus(model)` | H100 versus B200 for a model |
| `concurrency_curve(model, gpu)` | Energy per token at every measured concurrency |
| `grid_intensity(country)` | Annual average gCO2e per kWh for a country or World |
| `gpu_hardware(gpu?)` | Max TDP, memory and MIG profiles |
| `sources` | Every source, version, retrieval date and licence |

Resource: `leadgreen://manifest`.

## Client configuration

Claude Desktop or Cursor (`claude_desktop_config.json` / `.cursor/mcp.json`):

```json
{ "mcpServers": { "leadgreen": { "command": "leadgreen-mcp" } } }
```

Claude Code: `claude mcp add leadgreen -- leadgreen-mcp`

## Licence

Apache 2.0 for the code. The data keeps the licences of its sources, listed in the manifest.
