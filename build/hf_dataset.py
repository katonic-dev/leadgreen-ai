"""Assemble the Hugging Face dataset for Lead Green from api/v1, and push it when asked (lane T2).

    python build/hf_dataset.py                  writes build/out/hf-dataset/ (dataset card + data files) and stops
    python build/hf_dataset.py --push           also uploads that folder to HF_DATASET_REPO as one commit
    python build/hf_dataset.py --push --create  creates the dataset repository first (the organisation must already exist)

The card is generated: every figure in it is read from the API documents, never typed. Run build.py first so
api/v1 is current. Pushing needs a Hugging Face login (`hf auth login`, or HF_TOKEN in the environment); this
script never prints or stores the token. Nothing is pushed without --push.
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from project_text import FUNDING, HF_DATASET_REPO, PROJECT_DESCRIPTION, REPO_URL, ZENODO_DOI_URL

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
API = ROOT / "api" / "v1"
OUT = HERE / "out" / "hf-dataset"

# Files copied as they are served. models/*.json and schema/*.json are added below.
FILES = ["manifest.json", "index.json", "index.csv", "models.json", "grid.json", "hardware.json",
         "per-query.json", "measurements.json", "changes.json", "openapi.json"]


def load(name: str):
    return json.loads((API / name).read_text(encoding="utf-8"))


def wh(v: float) -> str:
    return f"{v:,.1f} Wh/M"


def card() -> str:
    man, index, models, grid, perq, meas, hw, changes = (
        load("manifest.json"), load("index.json"), load("models.json"), load("grid.json"),
        load("per-query.json"), load("measurements.json"), load("hardware.json"), load("changes.json"))
    rows = index["rows"]
    lo = min(rows, key=lambda r: r["wh_per_million_output_tokens"])
    hi = max(rows, key=lambda r: r["wh_per_million_output_tokens"])
    rr = index["reference_row"]
    ref = next(r for r in rows if r["model"] == rr["model"] and r["gpu"] == rr["gpu"] and r["num_gpus"] == rr["num_gpus"])
    span = hi["wh_per_million_output_tokens"] / lo["wh_per_million_output_tokens"]
    world = grid.get("world")
    if isinstance(world, dict):
        world = next((v for v in world.values() if isinstance(v, (int, float))), None)
    pub = man["publisher"]
    endpoints = {e["path"]: e["description"] for e in man["endpoints"]}
    data_version = man["data_version"]
    site = man["site"]
    model_files = sorted(p.name for p in (API / "models").glob("*.json"))
    latest_change = changes["changes"][-1] if changes.get("changes") else None

    def row(r):
        return f"{r['model']}, {r['num_gpus']} x {r['gpu']}"

    file_rows = []
    for f in FILES:
        file_rows.append(f"| `{f}` | {endpoints.get(f, 'The index as a flat table, one row per model and GPU, for the dataset viewer.' if f == 'index.csv' else '')} |")
    file_rows.append(f"| `models/<slug>.json` ({len(model_files)} files) | {endpoints.get('models/{slug}.json', '')} |")
    file_rows.append(f"| `schema/measurement.schema.json` | The JSON schema a contributed measurement must satisfy (protocol {meas.get('protocol_version', '')}). |")
    file_rows.append("| `NOTICE.md` | Per-source provenance and terms for every data snapshot the index is computed from. |")

    src_rows, seen = [], set()
    for s in man["sources"]:
        key = (s.get("name"), s.get("version"))
        if key in seen:
            continue   # the leaderboard and its GPQA task file share a name and version
        seen.add(key)
        src_rows.append(f"| {s.get('name', '')} | {s.get('version', '')} | {s.get('retrieved', '')} | {s.get('licence', '')} |")

    elsewhere = [f"- Website and documentation: {site}/",
                 f"- JSON API (GET only, CORS open): {site}/api/v1/ ({site}/api/v1/manifest.json lists every endpoint)",
                 f"- MCP server for assistants: {site}/mcp/",
                 f"- Dated releases, each frozen once published: {man['releases']['index']}"]
    if REPO_URL:
        elsewhere.append(f"- Source, build script and issue tracker: {REPO_URL}")
    if ZENODO_DOI_URL:
        elsewhere.append(f"- Concept DOI (always resolves to the latest release): {ZENODO_DOI_URL}")

    front = "\n".join([
        "---",
        "license: cc-by-4.0",
        'pretty_name: "Green Tokens: GPU energy per million output tokens"',
        "language:", "  - en",
        "tags:", *[f"  - {t}" for t in ("energy", "llm-inference", "gpu", "carbon", "grid-carbon-intensity",
                                         "sustainability", "green-ai", "benchmark", "mcp", "open-data")],
        "size_categories:", "  - n<1K",
        "configs:",
        "  - config_name: index", "    default: true", "    data_files: index.csv",
        "---",
    ])

    body = f"""
# Green Tokens: GPU energy per million output tokens

{PROJECT_DESCRIPTION}

This dataset is the `{data_version}` release of the Lead Green JSON API, file for file, with a flat CSV of the index for the viewer. Figures change only when a source publishes a dated release; a release listed as published never changes. Cite a release, not the live files.

## What is in it

- `index.csv` and `index.json`: {len(rows)} rows, one per model and GPU, each the configuration with the lowest energy per output token whose median inter-token latency stays under {index['itl_deadline_ms']} ms (workload: {index['workload']}).
- `models/`: every measured configuration for each of the {len(models['models'])} models (concurrency, parallelism, latency, power), with the best row per GPU.
- `grid.json`: grid emissions intensity in {grid['unit']} for {len(grid['areas'])} countries and regions plus the world figure ({grid['year']} annual).
- `hardware.json`: GPU reference data ({len(hw['tdp'])} parts, {len(hw['mig_profiles'])} MIG profiles) transcribed from manufacturer documents.
- `per-query.json`: {len(perq['rows'])} rows of energy per query from the AI Energy Score ({perq.get('round', '')}).
- `measurements.json`: rows contributed under the measurement protocol ({len(meas['rows'])} at this release); never merged into the index.

## Reading a row

The unit is {index['unit']}: the GPU energy a server drew while generating one million output tokens, at steady state, in the configuration named by the row. Selection rule, verbatim from the API: {index['selection'].rstrip('.')}.

At this release the index runs from {wh(lo['wh_per_million_output_tokens'])} ({row(lo)}) to {wh(hi['wh_per_million_output_tokens'])} ({row(hi)}), a span of {span:.0f}x. The reference row, used on the site for every comparison, is {row(ref)} at {wh(ref['wh_per_million_output_tokens'])}.

## Boundary

{man['caveat']} The `boundary` field on every document reads `{man['boundary']}`.

## Carbon

Multiply watt-hours per million output tokens by the grid's gCO2e per kWh and divide by one thousand to get kilograms of CO2e per billion output tokens. `grid.json` carries the intensity for each area{f'; the world average at this release is {world:g} {grid["unit"]}' if world is not None else ''}. The site's per-country pages apply exactly this arithmetic.

## Files

| File | What it holds |
|---|---|
{chr(10).join(file_rows)}

## Sources and licences

| Source | Version | Retrieved | Terms |
|---|---|---|---|
{chr(10).join(src_rows)}

{man['licence']}

## Citation

Attribution line to copy (fill the Changes field): {man['attribution']}

The site root carries a `CITATION.cff`; GitHub renders it as "Cite this repository". {f'The concept DOI {ZENODO_DOI_URL} always resolves to the latest release.' if ZENODO_DOI_URL else 'A DOI per release is issued through Zenodo once the first deposit exists.'}

## Latest change

{(latest_change['date'] + ': ' + latest_change['summary']) if latest_change else 'See changes.json.'} The full record is in `changes.json`.

## Elsewhere

{chr(10).join(elsewhere)}

## Publisher and funder

{FUNDING}

Publisher: {pub['entity']}, registration {pub['registration']}, {pub['jurisdiction']}, trading this project as Lead Green. Corrections and contributions: {pub['contact']}, answered within {pub['response_working_days']} working days. Contributed measurements are made under the protocol described at {site}/contribute/.
"""
    return front + "\n" + body.lstrip("\n")


def assemble() -> Path:
    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "models").mkdir(parents=True)
    (OUT / "schema").mkdir()
    for f in FILES:
        shutil.copyfile(API / f, OUT / f)
    for p in (API / "models").glob("*.json"):
        shutil.copyfile(p, OUT / "models" / p.name)
    for p in (API / "schema").glob("*.json"):
        shutil.copyfile(p, OUT / "schema" / p.name)
    shutil.copyfile(HERE / "data" / "NOTICE.md", OUT / "NOTICE.md")
    text = card()
    for bad in ("—", "–"):
        if bad in text:
            sys.exit("dataset card contains an em or en dash; fix the source text")
    (OUT / "README.md").write_text(text, encoding="utf-8", newline="\n")
    return OUT


def push(folder: Path, create: bool) -> None:
    from huggingface_hub import HfApi  # imported here so assembling never needs the library

    api = HfApi()
    who = api.whoami()
    orgs = [o.get("name") for o in who.get("orgs", [])]
    owner = HF_DATASET_REPO.split("/")[0]
    if owner != who.get("name") and owner not in orgs:
        sys.exit(f"the logged-in account is not a member of '{owner}'; create the organisation first, then run again")
    if create:
        api.create_repo(HF_DATASET_REPO, repo_type="dataset", exist_ok=True)
    data_version = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))["data_version"]
    api.upload_folder(folder_path=str(folder), repo_id=HF_DATASET_REPO, repo_type="dataset",
                      commit_message=f"Release {data_version}", delete_patterns=["**"])
    print(f"pushed release {data_version} to https://huggingface.co/datasets/{HF_DATASET_REPO}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--push", action="store_true", help="upload the assembled folder to the dataset repository")
    ap.add_argument("--create", action="store_true", help="with --push: create the dataset repository if it does not exist")
    a = ap.parse_args()
    folder = assemble()
    n = sum(1 for p in folder.rglob("*") if p.is_file())
    print(f"assembled {n} files in {folder.relative_to(ROOT)} (card {len((folder / 'README.md').read_text(encoding='utf-8')):,} chars)")
    if a.push:
        push(folder, a.create)


if __name__ == "__main__":
    main()
