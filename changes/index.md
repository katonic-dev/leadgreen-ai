# Every change, dated

> The dated record: 5 changes to the published figures since 26 September 2026, every frozen data release with its hash, and each leadgreen-mcp version.
>
> Lead Green, a Katonic project. Canonical page: https://leadgreen.ai/changes/ (this file: https://leadgreen.ai/changes/index.md). Updated 19 October 2026, data version 2026-10-19. Licence: CC BY 4.0 for the compilation and text; sources keep their own licences. GPU energy only, measured at steady state on a busy server (the most energy-efficient configuration under a latency limit). Host, network, cooling and idle time are not counted. Every figure is a floor; a lightly used server sits well above it. Machine-readable data: https://leadgreen.ai/api/v1/ (see llms.txt).

*Changes*

The latest change to the data is dated 19 October 2026: Launch. Three blog posts: how much energy an AI query uses, what watt-hours per million tokens means, and why an idle GPU wastes energy. Every entry below is also in [changes.json](https://leadgreen.ai/api/v1/changes.json), and every dated release is kept unchanged for citation.

**Record** 5 data changes since 26 September 2026 · 4 dated releases (3 published) · 4 MCP server versions. Updated 19 October 2026.

Cite this page: Lead Green, a Katonic project. Changes: every dated update to the Lead Green data, releases and MCP server. https://leadgreen.ai/changes/, release 2026-10-19, retrieved [date]. CC BY 4.0.

- [Data changes](https://leadgreen.ai/changes/#data)
- [Data releases](https://leadgreen.ai/changes/#releases)
- [MCP server](https://leadgreen.ai/changes/#mcp)
- [Citing a release](https://leadgreen.ai/changes/#cite)

*Data changes*

## What changed in the published figures, newest first

- 19 Oct 2026Launch. Three blog posts: how much energy an AI query uses, what watt-hours per million tokens means, and why an idle GPU wastes energy. The site now serves from GitHub Pages at leadgreen.ai. No change to the data or its description.
 Documents: none (description only). Reason: launch. Source version: 3.0 (released 2025-12-01); data compiled 2026-02-16.
- 18 Oct 2026The publisher's registered office is added to About and to the manifest. No change to the data or its description.
 Documents: manifest.json. Reason: publisher. Source version: 3.0 (released 2025-12-01); data compiled 2026-02-16.
- 17 Oct 2026Ember's October 2026 release of its yearly electricity data (file dated 6 October 2026) replaces the September 2026 release. The 2024 emissions intensity moves for 26 of the 193 grids and World, seven of them on the carbon table (United Arab Emirates 467.5 to 477.3 gCO2e per kWh, Sri Lanka 386.8 to 392.8, Australia 554.0 to 549.5, Saudi Arabia 691.9 to 689.1, Taiwan 636.2 to 635.2, Japan 483.6 to 484.3, Serbia 668.0 to 668.4), and every kilogram figure priced on them follows. 2025 rows are added for Saudi Arabia and the United Arab Emirates. The reference year stays 2024, the latest with every listed grid present. No energy figure changes.
 Documents: grid.json, manifest.json. Reason: source release. Source version: October 2026 release (file last modified 2026-10-06).
- 27 Sep 2026Corrections after a nine-reader review, before launch. The ML.ENERGY data is dated to its compile date, not a banner update; the latency ceiling is the leaderboard's own 500 ms (no row moved); "requests in flight" is renamed running batch; full concurrency ladders; all AI Energy Score December rows; a two-task table; the carbon basis, grid years and display names; seven-decimal joules; additive API fields (data_version, row_id, repeat, p95_itl_ms, avg_running_batch, boundary, years, latest_year, iso2, display_name, source_label); changes.json, measurements.json, the measurement schema, a dated release archive, CSV, zip and TypeScript types.
 Documents: every document. Reason: review corrections. Source version: 3.0 (released 2025-12-01); data compiled 2026-02-16.
- 26 Sep 2026First build. 32 index rows from ML.ENERGY v3.0 (data compiled 16 February 2026), grid intensities from Ember (2024), NVIDIA specifications, AI Energy Score December 2025 round. The API, the MCP server and the first blog post.
 Documents: every document. Reason: first build. Source version: 3.0 (released 2025-12-01); data compiled 2026-02-16.

A change is recorded when a figure, a field or a description in [the data API](https://leadgreen.ai/api/) moves. Page copy that does not touch a figure is not listed. The index page carries the same record under [Changes](https://leadgreen.ai/index/#changes).

*Data releases*

## Dated copies of api/v1, newest first

*Each release is the whole API as it stood on that date*

| Release | Status | Documents that changed | Files | Zip SHA-256 |
|---|---|---|---|---|
| 19 Oct 2026 | published, frozen | as the previous release | [zip](https://leadgreen.ai/api/v1/releases/leadgreen-api-v1-2026-10-19.zip) · [manifest](https://leadgreen.ai/api/v1/releases/2026-10-19/manifest.json) | `6bf5e1ad57817f4a…` |
| 18 Oct 2026 | published, frozen | manifest.json | [zip](https://leadgreen.ai/api/v1/releases/leadgreen-api-v1-2026-10-18.zip) · [manifest](https://leadgreen.ai/api/v1/releases/2026-10-18/manifest.json) | `4eed461e8f03addb…` |
| 17 Oct 2026 | published, frozen | grid.json, manifest.json | [zip](https://leadgreen.ai/api/v1/releases/leadgreen-api-v1-2026-10-17.zip) · [manifest](https://leadgreen.ai/api/v1/releases/2026-10-17/manifest.json) | `2ead05cc4113a4bd…` |
| 27 Sep 2026 | built, not frozen | every document | [zip](https://leadgreen.ai/api/v1/releases/leadgreen-api-v1-2026-09-27.zip) · [manifest](https://leadgreen.ai/api/v1/releases/2026-09-27/manifest.json) | `set when frozen` |

A published release never changes: the build refuses to rewrite it. The current live files are release 2026-10-19. The list with full hashes is [releases/index.json](https://leadgreen.ai/api/v1/releases/index.json).

*MCP server*

## leadgreen-mcp versions

*The package is versioned separately from the data; it reads the live API first*

| Version | Date | What changed | Files |
|---|---|---|---|
| 0.3.1 | 20 Oct 2026 | Ownership marker for the official MCP Registry in the package README; listed as ai.leadgreen/green-token-index. No code change. | [wheel](https://leadgreen.ai/dist/leadgreen_mcp-0.3.1-py3-none-any.whl) · [PyPI](https://pypi.org/project/leadgreen-mcp/0.3.1/) |
| 0.3.0 | 20 Oct 2026 | First release on PyPI, with provenance attestations and a reproducible wheel; the install line becomes pip install leadgreen-mcp. | [wheel](https://leadgreen.ai/dist/leadgreen_mcp-0.3.0-py3-none-any.whl) · [PyPI](https://pypi.org/project/leadgreen-mcp/0.3.0/) |
| 0.2.0 | 28 Sep 2026 | Running batch and num_gpus parameters on estimate, PUE and system power ratio for energy at the meter, the wheel's SHA-256 on the install line. | [wheel](https://leadgreen.ai/dist/leadgreen_mcp-0.2.0-py3-none-any.whl) |
| 0.1.0 | 26 Sep 2026 | First build: eight tools over the index, grid and hardware documents, live API first with a bundled snapshot as fallback. | not kept |

Install and client configuration are on the [MCP page](https://leadgreen.ai/mcp/). The server is listed on the official MCP Registry as `ai.leadgreen/green-token-index`.

*Citing a release*

## Cite a date, not the live files

Quote the release date with the figure, for example "Lead Green, release 2026-10-19", and link the release zip or any file under its dated folder; both stay byte for byte as published. The repository's `CITATION.cff` and the Zenodo record ([doi.org/10.5281/zenodo.23478909](https://doi.org/10.5281/zenodo.23478909)) carry the same version. The feed at [feed.xml](https://leadgreen.ai/feed.xml) announces blog posts, not data changes; watch [changes.json](https://leadgreen.ai/api/v1/changes.json) or this page for those.

**Cite as.** Lead Green, a Katonic project. Green Tokens: GPU energy per million output tokens. https://leadgreen.ai/index/, release 2026-10-19, retrieved [date]. © 2026 Katonic AI Technology Ltd. Licensed [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), offered as-is and without warranty; state whether you changed any rows or columns. Underlying data: ML.ENERGY Leaderboard v3.0 (The ML.ENERGY Initiative; Apache 2.0 per the ml-energy/benchmark-v3 dataset card; cite Chung et al., The ML.ENERGY Benchmark, NeurIPS 2025 Datasets and Benchmarks, arXiv 2505.06371); Ember, Yearly electricity data, October 2026 release (CC BY 4.0); AI Energy Score (Apache-2.0 as tagged on its Space; results reproduced as facts with attribution); NVIDIA figures reproduced as facts from the documents named in the sources ledger.
