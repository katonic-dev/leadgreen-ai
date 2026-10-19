# Publish drafts (lane T of the GEO strategy): nothing here is published

These files are the registry entries, dataset card and record metadata the project will publish once the rulings that fix the names are made. They are drafts in the repository so that the wording is reviewed with the code and the data they describe, and so that the day a ruling lands the file is a copy, not a composition. **Nothing in this folder is public, uploaded or registered.** The Docker image does not serve `build/`, so none of it reaches leadgreen.ai either.

| File | Goes to | Gated by | Status |
|---|---|---|---|
| `huggingface-dataset-card.md` | The `README.md` of the Hugging Face dataset (T2) | G1 canonical description, G6 owner (`leadgreen` org or under `katonic`) | Draft; placeholders in square brackets |
| `zenodo.json` | `.zenodo.json` at the repository root, read by Zenodo on each GitHub release (T3) | G4 named outside reviewer (a DOI should name the reviewer), G7 yes/no | Draft |
| `mcp-registry-server.json` | `server.json` for the official MCP registry (T5), plus PulseMCP and Smithery listings | G2 public repository name, G8 stdio-only (as drafted) | Draft; the `ai.leadgreen/` namespace needs DNS or HTTP domain verification at publish time |
| `pypi-pyproject-additions.toml` | Merged into `leadgreen-mcp/pyproject.toml` with the next package release (T4) | G5 code licence (Apache 2.0, as the package already declares); the Source URL waits for G2 | Draft; apply with the 0.3.0 release, because rebuilding the wheel changes the SHA-256 printed on `/mcp/` |

## Placeholders

- `[G1]` the canonical two-sentence description from strategy section 10, once approved. Until then the files carry the home page's own sentences, so no new claim enters.
- `[G2-REPO-URL]` the public repository URL.
- `[G4-REVIEWER]` the named outside reviewer, with no Katonic affiliation.
- `[G6-OWNER]` `leadgreen` or `katonic` on Hugging Face.
- `[RELEASE-DATE]` the dated release being published (`api/v1/releases/<date>/`), never "latest".

## Publishing order, once ruled

1. T1 public repository (G2), with squashed history and `LICENSE` files for code (Apache 2.0) and data and text (CC BY 4.0).
2. T4 PyPI `leadgreen-mcp` 0.3.0 with the additions here; then the `/mcp/` page's install line can point at PyPI.
3. T2 Hugging Face dataset from the dated release zip, card from this folder; T3 Zenodo record from the same zip, DOI printed on `/index/#cite`.
4. T5 MCP registry entry pointing at the PyPI package; PulseMCP and Smithery after it.
5. `sameAs` links on the site's Organization JSON-LD to all of the above (T6 Wikidata after that).

Every step needs Prem's word before anything is uploaded, named or made public.
