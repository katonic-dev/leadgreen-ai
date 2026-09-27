# Contributing to Lead Green

Thank you. The site's value is the number of independent, reproducible measurements on the index and the care with which each is checked. The public page at `/contribute/` describes the roles, the measurement protocol and the review rules; this file is the mechanics.

## What you can contribute

- **A measurement** (a new row): a JSON file in the row schema plus the raw logs it was computed from.
- **A correction**: a link to the primary source and what the site should say instead.
- **A blog post**: one question, answered with public data, working shown, every figure sourced.
- **A translation** of the index or the "why" page, checked by a second speaker.
- **Code**: the build script, the API, the MCP server.

Open an issue first if you want to discuss scope. Otherwise send a pull request.

## Submitting a measurement

1. Follow the protocol on `/contribute/#protocol` (vLLM, named hardware and versions, a published prompt set, fixed concurrency held to steady state, GPU power sampled at 1 Hz through DCGM or `nvidia-smi`, output tokens from the engine's metrics, two runs).
2. Put the result in `build/data/measurements/<YYYY-MM-DD>-<contributor>-<model>-<hardware>.json` using the configuration fields of `api/v1/models/<slug>.json` (`gpu`, `num_gpus`, `tensor_parallel`, `max_num_seqs`, `avg_running_batch` (vLLM's `num_requests_running` averaged over the steady-state window, not the queue), `joules_per_output_token`, `median_itl_ms`, `p90_itl_ms`, `p99_itl_ms`, `tokens_per_second`, `gpu_power_watts_total`, `avg_output_tokens`) plus `mig_profile` (or null), `engine`, `engine_version`, `driver_version`, `cuda_version`, `prompt_set` (URL or file), `measured_on` (date), `contributor`, `vendor_affiliation` (or null), `notes`.
3. Attach the power log and the engine log in the same folder, or link to them if they are large.
4. Say in the pull request how the number was computed. A reviewer will recompute it from your logs.

Rows measured by or paid for by a hardware, cloud or model vendor are welcome and are labelled and shown separately.

## Submitting a post

Add `build/posts/YYYY-MM-DD-slug.html` with a meta block:

```
<!--meta
title: ...
description: one sentence for the list, the feed and search
date: YYYY-MM-DD
author: Your Name
-->
```

then the body as HTML (`<p>`, `<h2>`, `<ul>`, `<table>` inside `<div class="table-scroll">`, and a closing `<div class="refs">` with the references). Placeholders such as `{{REF_WH_1}}` from `build/build.py` may be used for any figure the site already carries; a new figure needs a new placeholder computed from a snapshot, never a typed number. Run `python build/build.py` and check the post renders at phone width. Bylines are the author's own. No em or en dashes; the build refuses them.

## Corrections

Open an issue or a pull request with the primary source. Corrections are made in the open: the change record on `/index/#changes` names what changed, when and why, and a corrected post keeps a note at the top.

## Review

Two reviewers for a new row or a changed figure, one of whom recomputes the number from the logs or the source file. Every public figure comes from a dated snapshot kept in `build/data`. If it cannot be sourced, it does not ship. No customer names.

## Licences

Code is Apache 2.0. Data and text are CC BY 4.0. By contributing you agree your contribution is offered under the same terms. Public sources keep their own licences, listed per source in `api/v1/manifest.json`.
