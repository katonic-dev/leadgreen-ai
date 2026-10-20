"""Entry point of the Lead Green MCPB bundle: runs the leadgreen-mcp package that uv installs from pyproject.toml."""
from leadgreen_mcp.server import main

if __name__ == "__main__":
    main()
