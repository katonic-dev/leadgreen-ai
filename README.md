# leadgreen.ai, the Lead Green site

Static, generated, no forms, no tracking. The only script is a short inline light/dark switch in the page shell. Serve the folder as-is (GitHub Pages, folder-style URLs).

```
index.html                      home
why/ index/ api/ mcp/ blog/ newsletter/ contribute/ about/   one index.html each (generated)
blog/<slug>/index.html          one folder per post (generated)
api/v1/                         the read-only JSON API (generated)
feed.xml sitemap.xml robots.txt llms.txt .nojekyll   (generated)
CNAME                           custom domain for GitHub Pages
assets/site.css                 the one stylesheet (hand-written)
assets/logo/                    the mark and lockups (SVG masters, light and dark), the icon master and its 512 px PNG
assets/social-card.svg .png     the 1200 by 630 link preview image (og:image); the PNG is rendered from the SVG
favicon.svg favicon.ico apple-touch-icon.png   site icons, cut from assets/logo/leadgreen-icon.svg
build/build.py                  the generator: reads build/data, build/pages, build/posts; writes everything above
build/layout.html               page shell: head, nav, footer, {{PLACEHOLDERS}}
build/pages/*.html              page bodies, one per page, with a meta block at the top
build/posts/YYYY-MM-DD-slug.html  blog posts, same shape
build/data/                     dated snapshots of every source file used, plus the NVIDIA hardware transcription
leadgreen-mcp/                  the MCP server package (pyproject.toml, leadgreen_mcp/, README); leadgreen_mcp/data/ is a copy of api/v1
dist/                           the built wheel that the MCP page's install line points at
```

## Build

From this folder:

```
python build/build.py
```

It renders every page and API file in memory first and refuses to write anything if a single `{{PLACEHOLDER}}` is unfilled or an em or en dash appears. Numbers on pages come only from `build/data` through placeholders defined in `build/build.py`; never type a figure into a page.

After any change to `leadgreen-mcp/` or to the data, rebuild the wheel:

```
python -m pip wheel ./leadgreen-mcp -w dist --no-deps
```

The MCP server works with the `mcp` Python SDK 1.x and 2.x (guarded import in `server.py`). To exercise it, run any MCP client against `python -m leadgreen_mcp.server` with `PYTHONPATH=leadgreen-mcp` and `LEADGREEN_API_BASE` set to the `api/v1` folder; an example client script that checks the worked example (50 million tokens of Qwen 3 32B on H100 in Serbia = about 3,173 Wh and 2.12 kg CO2e) is described in the handover.

Preview: the Browser pane config `leadgreen-site-static` in `.claude/launch.json` (Python `http.server` on port 8171, bound to this folder). Folder-style links need a server; opening the files directly works for single pages only.

## Edit

- **A page:** edit `build/pages/<name>.html`. The meta block (`title`, `description`, optional `og_type`) feeds the head. `{{ROOT}}` prefixes every internal link so pages work from any depth.
- **A post:** add `build/posts/YYYY-MM-DD-slug.html` with a meta block (`title`, `description`, `date`, optional `slug`, `author`) and the body HTML; rebuild. It appears on `/blog/`, in `feed.xml`, `sitemap.xml` and the home page's "latest" line.
- **A figure:** add or change a placeholder in the `subs` dict of `build/build.py`, computed from a snapshot.
- **Constants to set before launch** (top of `build/build.py`): `REPO_URL` (links to the repository are omitted while empty; the MCP install line then points at the wheel on this site), `NEWSLETTER_SIGNUP_URL` (the newsletter page points at Own Your AI until it is set; never a fake form), `UPDATED`.

## Update the numbers

1. Replace the relevant snapshot in `build/data/` with a fresh retrieval, keeping the date in the file name:
   - ML.ENERGY: `https://raw.githubusercontent.com/ml-energy/leaderboard/master/public/data/tasks/lm-arena-chat.json` and `.../gpqa.json` (branch `master`, not `main`)
   - Ember: the yearly CSV at `https://files.ember-energy.org/public-downloads/generation/outputs/release_generation_yearly_global.csv` (16 MB), then extract the `Total generation` rows for every `Country or economy` plus `World` for the three latest years, keeping the columns in the existing extract
   - AI Energy Score: `https://huggingface.co/spaces/AIEnergyScore/Leaderboard/raw/main/data/energy/text_generation.csv`
   - NVIDIA: re-check the pages named in `build/data/nvidia-hardware-*.json` and save a new dated copy
2. Point the file constants at the top of `build/build.py` at the new snapshots; bump `UPDATED` and the source `version` strings.
3. Add a line to the Changes section of `build/pages/index.html`.
4. Run the build, then rebuild the wheel.
5. Open the home page and the index locally and read the three tiles and the first rows before pushing.

## Deploy (GitHub Pages)

1. Create a repository and push this folder's contents to its default branch (`.nojekyll` is included so folders are served verbatim).
2. Repository Settings, Pages, Build and deployment: Source "Deploy from a branch", branch = default, folder = `/ (root)`.
3. Settings, Pages, Custom domain: `leadgreen.ai` (the `CNAME` file carries it). Tick "Enforce HTTPS" once the certificate is issued.
4. At the registrar, replace the site-builder DNS with GitHub Pages: `A` records for the apex pointing at 185.199.108.153, 185.199.109.153, 185.199.110.153, 185.199.111.153; `AAAA` records 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153; `CNAME` for `www` pointing at `<github-user>.github.io`. Check the current list in GitHub's docs ("Managing a custom domain for your GitHub Pages site") before entering them.
5. Cancel or park the site-builder plan that serves the "Launching Soon" page, so its contact form stops accepting messages into an unmonitored mailbox.
6. After the first deploy, fetch `https://leadgreen.ai/api/v1/manifest.json` and `https://leadgreen.ai/dist/leadgreen_mcp-0.1.0-py3-none-any.whl` once to confirm both are served, then run the MCP install line from the `/mcp/` page.

## Logo

The mark is one square pulse of GPU power with the area beneath it filled in: energy is the area under the power curve, a watt-hour drawn the way the meter sees it. Ink and accent only, no third colour, no gradient; on dark pages only the ink flips. Masters live in `assets/logo/`; the masthead carries an inline copy of the mark in `build/layout.html`, so a change to the geometry has to be made in both. The wordmark is Archivo Bold with tight tracking, "Lead" in ink and "Green" in the accent; the lockup SVGs have the type outlined, so they need no font. Rasters (`favicon.ico`, `apple-touch-icon.png`, `assets/logo/leadgreen-icon-512.png`, `assets/social-card.png`) are rendered from the SVG masters; re-render them after any change.

## Rules

No figure is typed into a page by hand. Every figure has a source in the ledger with a retrieval date. Nothing on the site claims a Katonic measurement until one exists. No customer names. No em or en dashes. Lead Green is a Katonic project, never a separate entity.
