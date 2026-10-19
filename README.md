# leadgreen.ai, the Lead Green site

Static, generated, no forms, no tracking. The only script is a short inline light/dark switch in the page shell. Serve the folder as-is (folder-style URLs; see Deploy).

```
index.html                      home
why/ index/ api/ mcp/ blog/ newsletter/ contribute/ about/   one index.html each (generated)
blog/<slug>/index.html          one folder per post (generated)
api/v1/                         the read-only JSON API (generated)
feed.xml sitemap.xml robots.txt llms.txt llms-full.txt .nojekyll   (generated)
assets/cards/*.png                                   (generated social cards, one number per page; needs Pillow and build/fonts)
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
Dockerfile .dockerignore docker/nginx.conf   the production container image (nginx); see Deploy (container)
k8s/leadgreen-website.yaml      its Kubernetes Deployment, Service, Istio Gateway and VirtualService
```

## Where this lives

- The working repository sits in Katonic's GitHub Enterprise organisation, which cannot host public repositories; the site image is built and deployed from its `master`.
- The public mirror is [katonic-dev/leadgreen-ai](https://github.com/katonic-dev/leadgreen-ai): `master` is pushed there after every merge, and it is where issues and pull requests from outside are opened. A change accepted there is merged into the working repository and reaches the mirror on the next push.
- The project's other homes (the Hugging Face dataset, the Zenodo DOI, Wikidata) are set in `build/project_text.py`; the build writes them into the pages' JSON-LD `sameAs`, `CITATION.cff` and `.zenodo.json`. `build/hf_dataset.py` assembles and pushes the dataset.

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

## Deploy (container)

The site is served from a container, not from GitHub Pages (Pages hosted it until 5 October 2026; keep Pages switched off in the repository settings so no second copy of the site exists). The image serves the committed folder with unprivileged nginx, minus `build/`, `leadgreen-mcp/` and the repository docs (see `.dockerignore`). It does not run the build: build and commit first. New page folders need no change to the image.

```
docker build -t leadgreen-site .
docker run --rm -p 8080:8080 leadgreen-site
```

On Kubernetes, `k8s/leadgreen-website.yaml` runs it as `docker.io/katonic/leadgreen-website` in the `application` namespace: two replicas behind the ClusterIP Service `leadgreen-website:80`, published through the cluster's Istio ingress gateway (`leadgreen-gateway` and a VirtualService; `www.leadgreen.ai` redirects to `leadgreen.ai`). DNS: an `A` record for the apex pointing at the ingress gateway's address (`kubectl -n istio-system get svc istio-ingressgateway`), and `www` as a `CNAME` to the apex. TLS comes from the secret `leadgreen-tls` in `istio-system`: a Let's Encrypt certificate issued by DNS-01 and renewed by hand, after which the secret is replaced with the new files. Apply it with `kubectl apply -f k8s/leadgreen-website.yaml`; for a new image, push a new tag and change `image:`. What the pod spec relies on: container port 8080; it runs as UID 101, so `runAsNonRoot: true` works; point the liveness and readiness probes at `GET /healthz`. With `readOnlyRootFilesystem: true`, mount an `emptyDir` at `/tmp`, the only path nginx writes to. TLS and the `leadgreen.ai` host belong on the ingress, and the VirtualService sets HSTS on the HTTPS route; nginx serves `/404.html` for unknown paths and answers `/api/v1/` with CORS headers; redirects are relative, so they keep the client's scheme and host.

After a deploy: fetch `https://leadgreen.ai/api/v1/manifest.json` and the wheel named on the `/mcp/` page once to confirm both are served; run `python build/indexnow.py` (`--all` the first time, then only the URLs whose content changed; the key file it checks is served at the site root). The sitemap is submitted once in Google Search Console and Bing Webmaster Tools; Bing's index also feeds ChatGPT search.

## Logo

The mark is one square pulse of GPU power with the area beneath it filled in: energy is the area under the power curve, a watt-hour drawn the way the meter sees it. Ink and accent only, no third colour, no gradient; on dark pages only the ink flips. Masters live in `assets/logo/`; the masthead carries an inline copy of the mark in `build/layout.html`, so a change to the geometry has to be made in both. The wordmark is Archivo Bold with tight tracking, "Lead" in ink and "Green" in the accent; the lockup SVGs have the type outlined, so they need no font. Rasters (`favicon.ico`, `apple-touch-icon.png`, `assets/logo/leadgreen-icon-512.png`, `assets/social-card.png`) are rendered from the SVG masters; re-render them after any change.

## Rules

No figure is typed into a page by hand. Every figure has a source in the ledger with a retrieval date. Nothing on the site claims a Katonic measurement until one exists. No customer names. No em or en dashes. Lead Green is a Katonic project, never a separate entity.
