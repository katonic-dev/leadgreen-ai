"""Lead Green MCP server.

Exposes the Green Tokens index (GPU watt-hours per million output tokens, by
model, GPU and configuration) plus grid carbon intensity and GPU hardware
reference data as MCP tools, so an AI assistant can answer questions such as
"how much energy would 50 million tokens of Qwen 3 32B use on H100s, and what
is the carbon in Serbia?" with sourced numbers.

Data comes from the site's read-only JSON API (https://leadgreen.ai/api/v1).
If the site cannot be reached, the snapshot bundled with this package is used.
Set LEADGREEN_API_BASE to another base URL or to a local folder to override.

Every answer is GPU energy only, measured at steady state on a busy server.
It is a floor. The caveat field on each response says so, and assistants
should repeat it.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any, Optional

import httpx

try:  # mcp 2.x renamed FastMCP to MCPServer; the decorators and run() are the same
    from mcp.server.mcpserver import MCPServer as _Server
    from mcp.server.mcpserver.exceptions import ToolError
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server
    from mcp.server.fastmcp.exceptions import ToolError
# ToolError is the "anticipated failure" class in both SDK versions: its message reaches the
# model as an is_error result. A plain ValueError is treated as a crash by mcp 2.x and the
# model only sees "Error executing tool <name>".

API_BASE = os.environ.get("LEADGREEN_API_BASE", "https://leadgreen.ai/api/v1").rstrip("/")
BUNDLED = Path(__file__).parent / "data"
TIMEOUT = float(os.environ.get("LEADGREEN_TIMEOUT", "10"))

CAVEAT = (
    "GPU energy only, measured at steady state with vLLM on a busy server "
    "(the most energy-efficient configuration under a latency limit). Host, "
    "network, cooling and idle time are not counted. Treat it as a floor: a "
    "lightly used server sits well above it."
)

mcp = _Server(
    "leadgreen",
    instructions=(
        "Tools for the Lead Green Green Tokens index: GPU watt-hours per million "
        "output tokens for open-weight LLMs on H100 and B200, with grid carbon "
        "intensity by country and GPU hardware reference data. Every figure is "
        "from a public source named in the response. Always pass the caveat on: "
        "the numbers are GPU-only floors from a busy server."
    ),
)

_cache: dict[str, Any] = {}


def _load(name: str) -> Any:
    """Load an API document by relative path, e.g. 'index.json' or 'models/qwen-3-32b.json'."""
    if name in _cache:
        return _cache[name]
    data = None
    if API_BASE.startswith("http"):
        try:
            r = httpx.get(f"{API_BASE}/{name}", timeout=TIMEOUT, follow_redirects=True)
            r.raise_for_status()
            data = r.json()
        except Exception:
            data = None
    else:
        p = Path(API_BASE) / name
        if p.exists():
            data = json.loads(p.read_text(encoding="utf-8"))
    if data is None:
        p = BUNDLED / name
        if not p.exists():
            raise FileNotFoundError(f"{name} is not available from {API_BASE} or the bundled snapshot")
        data = json.loads(p.read_text(encoding="utf-8"))
    _cache[name] = data
    return data


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _find_model(query: str) -> dict:
    models = _load("models.json")["models"]
    q = _norm(query)
    if not q:
        raise ToolError("model is required")
    exact = [m for m in models if q in (_norm(m["slug"]), _norm(m["name"]), _norm(m["model_id"]))]
    if exact:
        return exact[0]
    partial = [m for m in models if q in _norm(m["name"]) or q in _norm(m["model_id"]) or q in _norm(m["slug"])]
    if len(partial) == 1:
        return partial[0]
    if partial:
        names = ", ".join(m["name"] for m in partial)
        raise ToolError(f"'{query}' matches several models: {names}. Use one of them.")
    names = ", ".join(m["name"] for m in models)
    raise ToolError(f"No model matches '{query}'. Models on the index: {names}")


def _find_area(query: str) -> dict:
    grid = _load("grid.json")
    q = _norm(query)
    for a in grid["areas"]:
        if q in (_norm(a["iso3"]), _norm(a["name"])):
            return a
    partial = [a for a in grid["areas"] if q and q in _norm(a["name"])]
    if len(partial) == 1:
        return partial[0]
    if partial:
        raise ToolError("'" + query + "' matches several areas: " + ", ".join(a["name"] for a in partial))
    raise ToolError(f"No grid area matches '{query}'. Use a country name or ISO 3166 alpha-3 code; 'World' is also accepted.")


def _gpu_name(gpu: Optional[str]) -> Optional[str]:
    if gpu is None:
        return None
    g = _norm(gpu)
    for known in ("H100", "B200"):
        if g == _norm(known):
            return known
    raise ToolError(f"GPU '{gpu}' is not on the index. Measured GPUs: H100, B200.")


@mcp.tool()
def list_models() -> dict:
    """List every model on the Green Tokens index with the GPUs it was measured on.

    Returns names, Hugging Face ids, parameter counts and the GPUs available, so
    you can pick exact arguments for the other tools.
    """
    models = _load("models.json")
    return {
        "count": len(models["models"]),
        "models": models["models"],
        "gpus_measured": ["H100", "B200"],
        "unit": "Wh per million output tokens",
        "source": models.get("source"),
    }


@mcp.tool()
def energy_per_million_tokens(model: str, gpu: Optional[str] = None) -> dict:
    """GPU energy per million output tokens for a model, from the index.

    Args:
        model: model name, slug or Hugging Face id (for example "Qwen 3 32B",
            "qwen-3-32b" or "Qwen/Qwen3-32B").
        gpu: optional, "H100" or "B200". If omitted, every GPU the model was
            measured on is returned.

    Each row is the most energy-efficient configuration found for that model on
    that GPU while keeping median inter-token latency under the index's limit,
    on a text-conversation workload.
    """
    m = _find_model(model)
    g = _gpu_name(gpu)
    index = _load("index.json")
    rows = [r for r in index["rows"] if r["slug"] == m["slug"] and (g is None or r["gpu"] == g)]
    if not rows:
        raise ToolError(f"{m['name']} was not measured on {g}. Measured on: {', '.join(m['gpus'])}")
    return {
        "model": m["name"],
        "model_id": m["model_id"],
        "unit": index["unit"],
        "workload": index["workload"],
        "itl_deadline_ms": index["itl_deadline_ms"],
        "rows": rows,
        "caveat": CAVEAT,
        "source": index["source"],
    }


@mcp.tool()
def estimate(
    model: str,
    output_tokens: float,
    gpu: Optional[str] = None,
    country: Optional[str] = None,
    requests_in_flight: Optional[float] = None,
) -> dict:
    """Estimate GPU energy, and optionally carbon, for serving a number of output tokens.

    Args:
        model: model name, slug or Hugging Face id.
        output_tokens: how many output tokens will be generated (for example
            50_000_000 for fifty million).
        gpu: "H100" or "B200". If omitted, the most efficient measured GPU is used.
        country: optional country name or ISO3 code (or "World") to convert the
            energy to kg CO2e using that grid's annual average intensity.
        requests_in_flight: optional. The average number of concurrent requests
            the server will hold. If given, the estimate uses the measured
            configuration closest to that concurrency instead of the index's
            best row. Low concurrency can raise energy per token several-fold.

    Returns energy in Wh and kWh, the configuration used, and, with a country,
    kg CO2e. Everything is GPU-only and a floor; see the caveat.
    """
    if output_tokens <= 0:
        raise ToolError("output_tokens must be positive")
    m = _find_model(model)
    g = _gpu_name(gpu)
    index = _load("index.json")
    rows = [r for r in index["rows"] if r["slug"] == m["slug"] and (g is None or r["gpu"] == g)]
    if not rows:
        raise ToolError(f"{m['name']} was not measured on {g}. Measured on: {', '.join(m['gpus'])}")
    best = min(rows, key=lambda r: r["wh_per_million_output_tokens"])
    used = dict(best)
    basis = "index best row (energy-optimal configuration under the latency limit)"
    if requests_in_flight is not None:
        detail = _load(f"models/{m['slug']}.json")
        cands = [c for c in detail["configurations"] if c["gpu"] == best["gpu"]]
        if cands:
            near = min(cands, key=lambda c: abs(c["avg_requests_in_flight"] - requests_in_flight))
            used = dict(near)
            basis = (
                f"measured configuration nearest to {requests_in_flight:g} requests in flight "
                f"({near['avg_requests_in_flight']:.0f} measured)"
            )
    wh = used["wh_per_million_output_tokens"] * output_tokens / 1_000_000
    out = {
        "model": m["name"],
        "gpu": used["gpu"],
        "num_gpus": used["num_gpus"],
        "basis": basis,
        "wh_per_million_output_tokens": used["wh_per_million_output_tokens"],
        "output_tokens": output_tokens,
        "energy_wh": round(wh, 3),
        "energy_kwh": round(wh / 1000, 6),
        "median_itl_ms": used.get("median_itl_ms"),
        "avg_requests_in_flight": used.get("avg_requests_in_flight"),
        "caveat": CAVEAT,
        "source": index["source"],
    }
    if country:
        a = _find_area(country)
        grid = _load("grid.json")
        kg = wh / 1000 * a["g_co2e_per_kwh"] / 1000
        out.update({
            "grid": a["name"],
            "grid_year": grid["year"],
            "g_co2e_per_kwh": a["g_co2e_per_kwh"],
            "co2e_kg": round(kg, 4),
            "grid_source": grid["source"],
            "grid_caveat": "Annual average of the national grid. Hourly intensity, contracted renewable supply and on-site generation change the real figure.",
        })
    return out


@mcp.tool()
def compare_gpus(model: str) -> dict:
    """Compare a model's energy per million output tokens on H100 and B200.

    Args:
        model: model name, slug or Hugging Face id.

    Returns the best row per GPU and the ratio between them. Models measured on
    only one GPU return that single row.
    """
    m = _find_model(model)
    index = _load("index.json")
    rows = [r for r in index["rows"] if r["slug"] == m["slug"]]
    by_gpu = {r["gpu"]: r for r in rows}
    out: dict[str, Any] = {"model": m["name"], "unit": index["unit"], "rows": rows, "caveat": CAVEAT, "source": index["source"]}
    if "H100" in by_gpu and "B200" in by_gpu:
        h, b = by_gpu["H100"], by_gpu["B200"]
        out["b200_advantage"] = round(h["wh_per_million_output_tokens"] / b["wh_per_million_output_tokens"], 2)
        out["note"] = f"B200 uses {out['b200_advantage']}x less energy per token than H100 for this model, at each GPU's best configuration."
    return out


@mcp.tool()
def concurrency_curve(model: str, gpu: str) -> dict:
    """Energy per million output tokens at every measured concurrency for a model on a GPU.

    Args:
        model: model name, slug or Hugging Face id.
        gpu: "H100" or "B200".

    Shows how energy per token falls as the server holds more requests at once.
    Use it to see where a lightly loaded deployment sits relative to the index.
    """
    m = _find_model(model)
    g = _gpu_name(gpu)
    detail = _load(f"models/{m['slug']}.json")
    cfgs = [c for c in detail["configurations"] if c["gpu"] == g]
    if not cfgs:
        raise ToolError(f"{m['name']} was not measured on {g}. Measured on: {', '.join(m['gpus'])}")
    cfgs.sort(key=lambda c: (c["num_gpus"], c["avg_requests_in_flight"]))
    return {"model": m["name"], "gpu": g, "unit": "Wh per million output tokens", "configurations": cfgs, "caveat": CAVEAT, "source": detail.get("source")}


@mcp.tool()
def grid_intensity(country: str) -> dict:
    """Annual average grid carbon intensity for a country, in g CO2e per kWh.

    Args:
        country: country name or ISO 3166 alpha-3 code, or "World".
    """
    a = _find_area(country)
    grid = _load("grid.json")
    return {**a, "unit": grid["unit"], "year": grid["year"], "source": grid["source"], "licence": grid.get("licence")}


@mcp.tool()
def gpu_hardware(gpu: Optional[str] = None) -> dict:
    """Manufacturer power ceilings (max TDP), memory, and MIG slice profiles for data-centre GPUs.

    Args:
        gpu: optional filter such as "H100", "H200", "A100" or "B200". Omit for all.
    """
    hw = _load("hardware.json")
    if gpu:
        g = _norm(gpu)
        tdp = [t for t in hw["tdp"] if g in _norm(t["gpu"])]
        mig = [p for p in hw["mig_profiles"] if g in _norm(p["gpu"])]
        if not tdp and not mig:
            raise ToolError(f"No hardware entry matches '{gpu}'.")
        return {"tdp": tdp, "mig_profiles": mig, "sources": hw["sources"], "note": hw.get("note")}
    return hw


@mcp.tool()
def sources() -> dict:
    """Every source behind the index, with version, retrieval date and licence, plus the API endpoints."""
    return _load("manifest.json")


@mcp.resource("leadgreen://manifest")
def manifest_resource() -> str:
    """The Lead Green API manifest: sources, dates, licences and endpoints."""
    return json.dumps(_load("manifest.json"), indent=2)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
