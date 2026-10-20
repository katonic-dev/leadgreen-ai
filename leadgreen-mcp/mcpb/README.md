# Lead Green MCPB bundle

Source of `leadgreen-<version>.mcpb`, the bundle Smithery (and any MCPB-aware client) distributes for a local stdio install. It is a `uv` type bundle (manifest 0.4): the host runs `uv run --directory <bundle> src/server.py`, and uv installs `leadgreen-mcp==<version>` from PyPI, so the bundle carries no code of its own and stays cross-platform.

Build, from this directory, after the matching package version is on PyPI:

    npx @anthropic-ai/mcpb validate manifest.json
    npx @anthropic-ai/mcpb pack . ../../dist/leadgreen-<version>.mcpb

Bump `version` in `manifest.json` and the pin in `pyproject.toml` together with the package. Publish to Smithery with `smithery mcp publish ../../dist/leadgreen-<version>.mcpb -n leadgreen/leadgreen` after `smithery auth login`.
