# Lead Green MCPB bundle

Source of `leadgreen-<version>.mcpb`, the bundle Smithery (and any MCPB-aware client) distributes for a local stdio install. It is a `python` type bundle (manifest 0.3) whose launch command is `uvx leadgreen-mcp==<version>`: uv fetches the published package from PyPI, so the bundle carries no vendored code and stays cross-platform. (The MCPB `uv` server type would say the same thing more directly, but Smithery's CLI 1.2.0 accepts only the python, node, bun and binary runtimes.) `src/server.py` is the nominal entry point the manifest schema requires; `pyproject.toml` records the pin.

Build, from this directory, after the matching package version is on PyPI (the strict bundle the site serves, then the Smithery variant, which adds each tool's inputSchema because Smithery's API requires it and the MCPB schema forbids it):

    npx @anthropic-ai/mcpb validate manifest.json
    npx @anthropic-ai/mcpb pack . ../../dist/leadgreen-<version>.mcpb
    python build_smithery.py ../../dist/leadgreen-<version>-smithery.mcpb

Bump `version` and the `uvx` pin in `manifest.json`, and the pin in `pyproject.toml`, together with the package. Publish to Smithery with `smithery mcp publish ../../dist/leadgreen-<version>-smithery.mcpb -n prem-naraindas/leadgreen` after `smithery auth login`.
