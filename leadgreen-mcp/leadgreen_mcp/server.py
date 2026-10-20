"""Lead Green MCP server.

Exposes the Green Tokens index (GPU watt-hours per million output tokens, by
model, GPU and configuration) plus grid carbon intensity and GPU hardware
reference data as MCP tools, so an AI assistant can answer questions such as
"how much energy would 50 million tokens of Qwen 3 32B use on H100s, and what
is the carbon in Serbia?" with sourced numbers.

Data comes from the site's read-only JSON API (https://leadgreen.ai/api/v1).
If a fetch fails, the snapshot bundled with this package is used for the rest
of the session and one line on stderr says so. Set LEADGREEN_API_BASE to
another base URL or to a local folder to override. Every response says where
its data came from (data_source) and how current it is (data_updated).

Every answer is GPU energy only, measured at steady state on a busy server.
It is a floor. The caveat and boundary fields on each response say so, and
assistants should repeat the caveat.
"""
from __future__ import annotations

import inspect
import json
import math
import os
import re
import sys
import threading
import unicodedata
from pathlib import Path
from typing import Any, Optional

import httpx

try:  # mcp 2.x renamed FastMCP to MCPServer; the decorators and run() are the same
    from mcp.server.mcpserver import MCPServer as _Server
    from mcp.server.mcpserver.exceptions import ResourceError, ToolError
except ImportError:  # mcp 1.x
    from mcp.server.fastmcp import FastMCP as _Server
    from mcp.server.fastmcp.exceptions import ResourceError, ToolError
# ToolError is the "anticipated failure" class in both SDK versions: its message reaches the
# model as an is_error result. A plain ValueError is treated as a crash by mcp 2.x and the
# model only sees "Error executing tool <name>". ResourceError plays the same part for resources.

API_BASE = os.environ.get("LEADGREEN_API_BASE", "https://leadgreen.ai/api/v1").rstrip("/")
BUNDLED = Path(__file__).parent / "data"
TIMEOUT = float(os.environ.get("LEADGREEN_TIMEOUT", "10"))
_REMOTE = API_BASE.lower().startswith(("http://", "https://"))

# data_source values: where the document behind a response came from.
LIVE = "live"
BUNDLE = "bundled snapshot"
FOLDER = "local folder"

BOUNDARY = "gpu_only"  # used when the documents carry no boundary field of their own
DEFAULT_ITL_DEADLINE_MS = 500  # the leaderboard's default; used only if index.json omits its ceiling

# The caveat every tool returns is index.json's "caveat" (live, local folder or bundled), so the
# text lives in one place, the API. There is deliberately no second copy of it in this file.
GRID_BASIS_FALLBACK = (
    "annual average emissions intensity of total generation; hourly intensity, contracted "
    "supply and self-generation are not reflected"
)
GRID_SCOPE = (
    "Lifecycle and location-based: a figure for comparing places, not a Scope 2 figure to file."
)
AT_METER_NOTE = (
    "Energy at the meter = GPU energy x system_power_ratio ({spr:g}) x pue ({pue:g}). "
    "Both factors are the caller's assumptions, not measurements. For scale, the "
    "site's worked example takes a DGX B200 at its 14.3 kW maximum over 8 x 1.0 kW "
    "of GPU power, a ratio of 1.79, and assumes a PUE of 1.3."
)

_FALLBACK_VERSION = "0.3.1"  # keep in step with pyproject.toml; used when running from a source checkout


def _package_version() -> str:
    try:
        import importlib.metadata as _md

        return _md.version("leadgreen-mcp")
    except Exception:  # not installed, for example a source checkout on PYTHONPATH
        return _FALLBACK_VERSION


VERSION = _package_version()

_INSTRUCTIONS = (
    "Tools for the Lead Green Green Tokens index: GPU watt-hours per million "
    "output tokens for open-weight LLMs on H100 and B200, with grid carbon "
    "intensity by country and GPU hardware reference data. Every figure is "
    "from a public source named in the response. Always pass the caveat on: "
    "the numbers are GPU-only floors from a busy server. data_source says "
    "whether a response came from the live API or the bundled snapshot."
)


def _make_server() -> Any:
    """Create the server object carrying the package version, on either SDK line.

    mcp 2.x takes version= in the MCPServer constructor and reports an empty
    version without it. mcp 1.x FastMCP has no such argument; its low-level
    server reports whatever its version attribute holds, so set that instead.
    """
    try:
        takes_version = "version" in inspect.signature(_Server.__init__).parameters
    except (TypeError, ValueError):
        takes_version = False
    if takes_version:
        return _Server("leadgreen", instructions=_INSTRUCTIONS, version=VERSION)
    server = _Server("leadgreen", instructions=_INSTRUCTIONS)
    low = getattr(server, "_mcp_server", None)
    if low is not None:
        low.version = VERSION
    return server


mcp = _make_server()

_cache: dict[str, Any] = {}
_origin: dict[str, str] = {}  # document name -> LIVE, BUNDLE or FOLDER
_offline = False  # set by the first failed fetch; the network is not tried again this session
_lock = threading.Lock()


def _read(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise ToolError(f"{path} could not be read: {exc}") from None


def _bundled_updated() -> Optional[str]:
    try:
        return json.loads((BUNDLED / "manifest.json").read_text(encoding="utf-8")).get("updated")
    except Exception:
        return None


def _go_offline(name: str, exc: Exception) -> None:
    """Stop using the network for the rest of the session and say so, once, on stderr."""
    global _offline
    _offline = True
    reason = " ".join(f"{type(exc).__name__}: {exc}".split())[:200]
    updated = _bundled_updated()
    snapshot = f"the bundled snapshot (updated {updated})" if updated else "the bundled snapshot"
    line = (
        f"leadgreen-mcp: could not fetch {API_BASE}/{name} ({reason}); "
        f"using {snapshot} for the rest of this session."
    )
    try:  # stderr only: stdout carries the MCP protocol
        print(line.encode("ascii", "replace").decode("ascii"), file=sys.stderr, flush=True)
    except Exception:
        pass


def _load(name: str) -> Any:
    """Load an API document by relative path, e.g. 'index.json' or 'models/qwen-3-32b.json'."""
    with _lock:
        if name in _cache:
            return _cache[name]
        data, origin = None, None
        if _REMOTE:
            if not _offline:
                try:
                    r = httpx.get(f"{API_BASE}/{name}", timeout=TIMEOUT, follow_redirects=True)
                    r.raise_for_status()
                    data, origin = r.json(), LIVE
                except Exception as exc:  # network, HTTP status and JSON failures alike
                    _go_offline(name, exc)
        else:
            p = Path(API_BASE) / name
            if p.is_file():
                data, origin = _read(p), FOLDER
        if data is None:
            p = BUNDLED / name
            if not p.is_file():
                raise ToolError(f"{name} is not available from {API_BASE} or the bundled snapshot.")
            data, origin = _read(p), BUNDLE
        _cache[name] = data
        _origin[name] = origin
        return data


def _caveat() -> str:
    """The one caveat string every tool returns: index.json's, from wherever it was loaded.

    If that copy has none (an older or partial API), the bundled index.json's is used.
    """
    for get in (lambda: _load("index.json"), lambda: _read(BUNDLED / "index.json")):
        try:
            c = get().get("caveat")
        except Exception:
            c = None
        if isinstance(c, str) and c.strip():
            return c
    raise ToolError("No caveat could be read from index.json; the bundled snapshot is damaged.")


def _grid_caveat(grid: dict) -> str:
    """grid.json's basis sentence plus the lifecycle, location-based scope of the figures."""
    basis = grid.get("basis") if isinstance(grid.get("basis"), str) and grid["basis"].strip() else GRID_BASIS_FALLBACK
    basis = basis.strip().rstrip(".")
    year = grid.get("year")
    lead = f"Grid year {year}: " if year else "Grid: "
    return f"{lead}{basis}. {GRID_SCOPE}"


def _common(primary: str, *others: str) -> dict[str, Any]:
    """Fields every tool response carries. primary is the document the figures came from."""
    caveat = _caveat()  # loads index.json, so it joins the documents below
    names = list(dict.fromkeys([primary, *others, "index.json"]))
    docs = {n: _cache[n] for n in names if isinstance(_cache.get(n), dict)}
    ref = docs.get("index.json", {})
    boundary = BOUNDARY
    for d in docs.values():
        b = d.get("boundary")
        if isinstance(b, str) and b.strip():
            boundary = b
            break
    doc = docs.get(primary, {})
    out: dict[str, Any] = {
        "caveat": caveat,
        "boundary": boundary,
        "data_source": _origin.get(primary),
        "data_updated": doc.get("updated", ref.get("updated")),
    }
    # data_version arrives in a later build; until then it falls back to the document's updated date
    out["data_version"] = doc.get("data_version") or ref.get("data_version") or out["data_updated"]
    origins = {n: _origin[n] for n in names if n in _origin}
    if len(set(origins.values())) > 1:  # only after the network failed partway through a session
        out["data_sources"] = origins
    return out


def _norm(s: str) -> str:
    """Lower-case ASCII letters and digits only; accents are folded, so 'Turkiye' matches 'Türkiye'."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", s.lower())


def _find_model(query: str) -> dict:
    models = _load("models.json")["models"]
    q = _norm(query or "")
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


# Names people type that Ember labels differently, or that a substring search gets wrong.
_AREA_ALIASES = {
    _norm(k): v
    for k, v in {
        "UK": "GBR", "GB": "GBR", "Great Britain": "GBR", "Britain": "GBR",
        "US": "USA", "USA": "USA", "United States": "USA", "United States of America": "USA",
        "America": "USA",  # a substring search would answer American Samoa
        "Turkey": "TUR", "Turkiye": "TUR",
        "South Korea": "KOR", "Korea": "KOR", "Republic of Korea": "KOR", "Korea, Republic of": "KOR",
        "Russia": "RUS", "Russian Federation": "RUS",
        "UAE": "ARE",
        "Czech Republic": "CZE",
        "Ivory Coast": "CIV",
        "Laos": "LAO",
        "DRC": "COD", "DR Congo": "COD", "Democratic Republic of the Congo": "COD",
        "Cape Verde": "CPV",
        "Macau": "MAC",
        "Swaziland": "SWZ",
    }.items()
}
_AREA_EXACT_FIELDS = ("iso3", "iso2", "name", "display_name")  # iso2 and display_name when the data has them


def _display(a: dict) -> str:
    """The short name the site shows (display_name), else the data source's label."""
    return a.get("display_name") or a["name"]


def _find_area(query: str) -> dict:
    """Resolve a country query: alias, then exact code or name, then a substring of 4+ characters."""
    areas = _load("grid.json")["areas"]
    q = _norm(query or "")
    if not q:
        raise ToolError("country is required: a country name, an ISO 3166 code, or 'World'.")
    target = _AREA_ALIASES.get(q)
    if target:
        for a in areas:
            if a.get("iso3") == target:
                return a
    for a in areas:
        if any(isinstance(a.get(k), str) and _norm(a[k]) == q for k in _AREA_EXACT_FIELDS):
            return a
    has_iso2 = any(a.get("iso2") for a in areas)
    codes = "an ISO 3166 alpha-3 code such as GBR" + (" or alpha-2 code such as GB" if has_iso2 else "")
    if len(q) <= 3:  # short queries are codes: "US" must not land on Australia by substring
        raise ToolError(
            f"No grid area has the code or name '{query}'. Use a country name, {codes}, or 'World'. "
            "Queries of three characters or fewer must match a code or name exactly."
        )
    partial = [a for a in areas if any(isinstance(a.get(k), str) and q in _norm(a[k]) for k in ("name", "display_name"))]
    if len(partial) == 1:
        return partial[0]
    if partial:
        raise ToolError(f"'{query}' matches several areas: {', '.join(_display(a) for a in partial)}. Use one of them.")
    raise ToolError(f"No grid area matches '{query}'. Use a country name, {codes}, or 'World'.")


def _gpu_name(gpu: Optional[str]) -> Optional[str]:
    if gpu is None:
        return None
    g = _norm(gpu)
    for known in ("H100", "B200"):
        if g == _norm(known):
            return known
    raise ToolError(f"GPU '{gpu}' is not on the index. Measured GPUs: H100, B200.")


def _rb(c: dict) -> Optional[float]:
    """Average running batch of a row (vLLM num_requests_running): the API's new key, else its old one."""
    v = c.get("avg_running_batch")
    return c.get("avg_requests_in_flight") if v is None else v


def _row(c: dict) -> dict:
    """Copy a row or configuration so it names the running batch under both keys, side by side."""
    if "avg_running_batch" in c:
        out = dict(c)
        out.setdefault("avg_requests_in_flight", c["avg_running_batch"])
        return out
    out = {}
    for k, v in c.items():
        if k == "avg_requests_in_flight":
            out["avg_running_batch"] = v
        out[k] = v
    return out


def _detail_row(m: dict, c: dict) -> dict:
    """An index-shaped row built from one of a model's measured configurations."""
    base = {k: m[k] for k in ("params_b", "active_params_b") if k in m}
    cfg = {k: v for k, v in c.items() if k != "under_itl_deadline"}  # that flag refers to the index ceiling
    return _row({"model": m["name"], "slug": m["slug"], "model_id": m["model_id"], **base, **cfg})


def _number(name: str, value: Optional[float]) -> Optional[float]:
    if value is None:
        return None
    try:
        v = float(value)
    except (TypeError, ValueError):
        raise ToolError(f"{name} must be a number.") from None
    if not math.isfinite(v):
        raise ToolError(f"{name} must be a finite number.")
    return v


def _deadline(value: Optional[float]) -> Optional[float]:
    v = _number("itl_deadline_ms", value)
    if v is not None and v <= 0:
        raise ToolError("itl_deadline_ms must be a positive number of milliseconds.")
    return v


def _factor(name: str, value: Optional[float]) -> Optional[float]:
    v = _number(name, value)
    if v is not None and v < 1.0:
        raise ToolError(f"{name} must be at least 1.0 (1.0 means no overhead above the GPUs); got {v:g}.")
    return v


def _index_ceiling(index: dict) -> float:
    c = index.get("itl_deadline_ms")
    return c if isinstance(c, (int, float)) and not isinstance(c, bool) else DEFAULT_ITL_DEADLINE_MS


def _select(m: dict, g: Optional[str], itl_deadline_ms: Optional[float], num_gpus: Optional[int] = None) -> dict:
    """The rows a tool answers from, ascending by energy.

    Without a ceiling or GPU count these are the index rows. Otherwise each GPU's row is
    re-selected from models/<slug>.json: the lowest energy among the configurations with
    median inter-token latency at or under the ceiling (and on num_gpus GPUs, if given).
    """
    index = _load("index.json")
    index_ceiling = _index_ceiling(index)
    if g is not None and g not in m["gpus"]:
        raise ToolError(f"{m['name']} was not measured on {g}. Measured on: {', '.join(m['gpus'])}")
    if itl_deadline_ms is None and num_gpus is None:
        rows = [_row(r) for r in index["rows"] if r["slug"] == m["slug"] and (g is None or r["gpu"] == g)]
        if not rows:
            raise ToolError(f"{m['name']} has no index row{' on ' + g if g else ''}. Measured on: {', '.join(m['gpus'])}")
        rows.sort(key=lambda r: r["wh_per_million_output_tokens"])
        return {
            "rows": rows, "ceiling": index_ceiling, "set_by": "index", "primary": "index.json",
            "docs": ["index.json"], "notes": [],
            "selection": (
                "index rows: per GPU, the lowest-energy measured configuration with median "
                f"inter-token latency under the index ceiling of {index_ceiling:g} ms"
            ),
        }
    ceiling = index_ceiling if itl_deadline_ms is None else itl_deadline_ms
    set_by = "index" if itl_deadline_ms is None else "caller"
    doc = f"models/{m['slug']}.json"
    configs = _load(doc)["configurations"]
    rows, notes = [], []
    for gpu in [g] if g else list(m["gpus"]):
        on_gpu = [c for c in configs if c["gpu"] == gpu]
        cands = [c for c in on_gpu if num_gpus is None or c["num_gpus"] == num_gpus]
        if not cands:
            counts = ", ".join(str(n) for n in sorted({c["num_gpus"] for c in on_gpu})) or "none"
            notes.append(f"{m['name']} was not measured on {num_gpus} x {gpu} (GPU counts measured on {gpu}: {counts}).")
            continue
        within = [c for c in cands if isinstance(c.get("median_itl_ms"), (int, float)) and c["median_itl_ms"] <= ceiling]
        if not within:
            itls = [c["median_itl_ms"] for c in cands if isinstance(c.get("median_itl_ms"), (int, float))]
            where = f"{num_gpus} x {gpu}" if num_gpus is not None else gpu
            fastest = f"; the fastest measured has {min(itls):g} ms" if itls else ""
            notes.append(
                f"No measured configuration of {m['name']} on {where} has a median inter-token "
                f"latency at or under {ceiling:g} ms{fastest}."
            )
            continue
        rows.append(_detail_row(m, min(within, key=lambda c: c["wh_per_million_output_tokens"])))
    if not rows:
        raise ToolError(" ".join(notes))
    rows.sort(key=lambda r: r["wh_per_million_output_tokens"])
    on = f" on {num_gpus} GPU{'' if num_gpus == 1 else 's'}" if num_gpus is not None else ""
    limit = f"the index ceiling of {ceiling:g} ms" if set_by == "index" else f"{ceiling:g} ms (set by the caller)"
    return {
        "rows": rows, "ceiling": ceiling, "set_by": set_by, "primary": doc,
        "docs": [doc, "index.json"], "notes": notes,
        "selection": (
            f"re-selected from the measured configurations{on}: per GPU, the lowest energy with "
            f"median inter-token latency at or under {limit}"
        ),
    }


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
        **_common("models.json"),
    }


@mcp.tool()
def energy_per_million_tokens(model: str, gpu: Optional[str] = None, itl_deadline_ms: Optional[float] = None) -> dict:
    """GPU energy per million output tokens for a model, from the index.

    Args:
        model: model name, slug or Hugging Face id (for example "Qwen 3 32B",
            "qwen-3-32b" or "Qwen/Qwen3-32B").
        gpu: optional, "H100" or "B200". If omitted, every GPU the model was
            measured on is returned.
        itl_deadline_ms: optional latency ceiling in milliseconds. If given, each
            GPU's row is re-selected from every measured configuration: the
            lowest energy whose median inter-token latency is at or under it.
            If omitted, the index rows (the index's own ceiling) are returned.

    Each row is the most energy-efficient configuration found for that model on
    that GPU while keeping median inter-token latency under the ceiling, on a
    text-conversation workload. The response reports the ceiling used.
    """
    m = _find_model(model)
    g = _gpu_name(gpu)
    deadline = _deadline(itl_deadline_ms)
    index = _load("index.json")
    sel = _select(m, g, deadline)
    out: dict[str, Any] = {
        "model": m["name"],
        "model_id": m["model_id"],
        "unit": index.get("unit"),
        "workload": index.get("workload"),
        "itl_deadline_ms": sel["ceiling"],
        "itl_deadline_set_by": sel["set_by"],
        "selection": sel["selection"],
        "rows": sel["rows"],
    }
    if sel["notes"]:
        out["note"] = " ".join(sel["notes"])
    out["source"] = index.get("source")
    return {**out, **_common(sel["primary"], *sel["docs"])}


@mcp.tool()
def estimate(
    model: str,
    output_tokens: float,
    gpu: Optional[str] = None,
    country: Optional[str] = None,
    running_batch: Optional[float] = None,
    num_gpus: Optional[int] = None,
    itl_deadline_ms: Optional[float] = None,
    pue: Optional[float] = None,
    system_power_ratio: Optional[float] = None,
    requests_in_flight: Optional[float] = None,
) -> dict:
    """Estimate GPU energy, and optionally carbon and energy at the meter, for serving a number of output tokens.

    Args:
        model: model name, slug or Hugging Face id.
        output_tokens: how many output tokens will be generated (for example
            50_000_000 for fifty million).
        gpu: "H100" or "B200". If omitted, the most efficient measured GPU is used.
        country: optional country name or ISO 3166 code (or "World") to convert
            the energy to kg CO2e using that grid's annual average intensity.
        running_batch: optional. The average running batch the server will hold:
            how many requests it decodes at once (vLLM num_requests_running). If
            given, the estimate uses the measured configuration nearest to it, on
            the same GPU count as the best row unless num_gpus is set. A small
            running batch can raise energy per token several-fold.
        num_gpus: optional. Use configurations on this many GPUs (for example 2
            for 2 x H100).
        itl_deadline_ms: optional latency ceiling in milliseconds. The lowest-energy
            configuration with median inter-token latency at or under it is used.
            If omitted, the index's own ceiling applies.
        pue: optional power usage effectiveness of the facility, at least 1.0.
        system_power_ratio: optional ratio of whole-server power to GPU power, at
            least 1.0 (a DGX B200 at its 14.3 kW maximum over 8 x 1.0 kW of GPU
            power is about 1.79).
        requests_in_flight: the old name for running_batch, still accepted.

    Returns energy in Wh and kWh, the configuration used, and, with a country,
    kg CO2e. With pue or system_power_ratio it also returns energy at the meter,
    which rests on those assumptions. The measured figures are GPU-only floors;
    see the caveat.
    """
    tokens = _number("output_tokens", output_tokens)
    if tokens is None or tokens <= 0:
        raise ToolError("output_tokens must be positive")
    rb_in = _number("running_batch", running_batch)
    rif = _number("requests_in_flight", requests_in_flight)
    if rb_in is not None and rif is not None and not math.isclose(rb_in, rif, rel_tol=1e-9, abs_tol=1e-9):
        raise ToolError(
            f"running_batch ({rb_in:g}) and requests_in_flight ({rif:g}) differ. requests_in_flight is "
            "the old name for running_batch: give one of them, or the same value for both."
        )
    batch = rb_in if rb_in is not None else rif
    if batch is not None and batch <= 0:
        raise ToolError("running_batch must be positive.")
    if num_gpus is not None and (isinstance(num_gpus, bool) or int(num_gpus) != num_gpus or num_gpus < 1):
        raise ToolError("num_gpus must be a whole number, 1 or more.")
    count_asked = int(num_gpus) if num_gpus is not None else None
    deadline = _deadline(itl_deadline_ms)
    spr = _factor("system_power_ratio", system_power_ratio)
    facility = _factor("pue", pue)

    m = _find_model(model)
    g = _gpu_name(gpu)
    index = _load("index.json")
    sel = _select(m, g, deadline, count_asked)
    best = sel["rows"][0]
    used = best
    primary = sel["primary"]
    docs = list(sel["docs"])
    notes = list(sel["notes"])
    ceiling = sel["ceiling"]
    shape = f"{best['num_gpus']} x {best['gpu']}"
    if batch is None:
        if sel["set_by"] == "index" and count_asked is None:
            basis = f"index best row: the energy-optimal configuration under the {ceiling:g} ms latency ceiling ({shape})"
        elif sel["set_by"] == "index":
            basis = f"energy-optimal measured configuration on {shape} under the index's {ceiling:g} ms latency ceiling"
        else:
            basis = (
                "energy-optimal measured configuration with median inter-token latency at or under "
                f"{ceiling:g} ms, the caller's ceiling ({shape})"
            )
    else:
        doc = f"models/{m['slug']}.json"
        configs = _load(doc)["configurations"]
        primary = doc
        docs.insert(0, doc)
        count = count_asked if count_asked is not None else best["num_gpus"]
        on_gpu = [c for c in configs if c["gpu"] == best["gpu"] and _rb(c) is not None]
        cands = [c for c in on_gpu if c["num_gpus"] == count]
        widened = False
        if not cands and count_asked is None:  # the best row's GPU count has no ladder: use every count
            cands, widened = on_gpu, True
        if not cands:
            raise ToolError(f"{m['name']} has no measured configuration on {count} x {best['gpu']}.")
        near = min(cands, key=lambda c: (abs(_rb(c) - batch), _rb(c)))  # a tie goes to the smaller batch
        used = _detail_row(m, near)
        basis = f"nearest to {batch:g} running batch ({_rb(near):.1f} measured), {near['num_gpus']} x {near['gpu']}"
        if widened:
            basis += f"; no {count} x {best['gpu']} configuration was measured, so every GPU count was considered"
        itl = near.get("median_itl_ms")
        if isinstance(itl, (int, float)) and itl > ceiling:
            notes.append(
                f"The configuration nearest to that running batch has a median inter-token latency of "
                f"{itl:g} ms, above the {ceiling:g} ms ceiling."
            )

    wh = used["wh_per_million_output_tokens"] * tokens / 1_000_000
    out: dict[str, Any] = {
        "model": m["name"],
        "gpu": used["gpu"],
        "num_gpus": used["num_gpus"],
        "basis": basis,
        "wh_per_million_output_tokens": used["wh_per_million_output_tokens"],
        "output_tokens": output_tokens,
        "energy_wh": round(wh, 3),
        "energy_kwh": round(wh / 1000, 6),
        "median_itl_ms": used.get("median_itl_ms"),
        "itl_deadline_ms": ceiling,
        "itl_deadline_set_by": sel["set_by"],
        "avg_running_batch": _rb(used),
        "avg_requests_in_flight": used.get("avg_requests_in_flight", _rb(used)),
    }
    meter_wh = None
    if facility is not None or spr is not None:
        spr_used = 1.0 if spr is None else spr
        pue_used = 1.0 if facility is None else facility
        meter_wh = wh * spr_used * pue_used
        out.update({
            "system_power_ratio": spr_used,
            "pue": pue_used,
            "energy_at_meter_wh": round(meter_wh, 3),
            "energy_at_meter_kwh": round(meter_wh / 1000, 6),
            "at_meter_note": AT_METER_NOTE.format(spr=spr_used, pue=pue_used),
            "at_meter_boundary": "facility meter, estimated: GPU energy scaled by the caller's factors",
        })
    if country:
        a = _find_area(country)
        grid = _load("grid.json")
        docs.append("grid.json")
        intensity = a.get("g_co2e_per_kwh")
        if not isinstance(intensity, (int, float)):
            raise ToolError(f"The grid data has no intensity for {_display(a)}.")
        out.update({
            "grid": _display(a),
            "grid_name": a.get("name"),
            "grid_iso3": a.get("iso3"),
            "grid_year": grid.get("year"),
            "g_co2e_per_kwh": intensity,
            "co2e_kg": round(wh / 1000 * intensity / 1000, 4),
        })
        if meter_wh is not None:
            out["co2e_at_meter_kg"] = round(meter_wh / 1000 * intensity / 1000, 4)
        out["grid_source"] = grid.get("source")
        out["grid_caveat"] = _grid_caveat(grid)
    if notes:
        out["note"] = " ".join(notes)
    out["source"] = index.get("source")
    return {**out, **_common(primary, *docs)}


@mcp.tool()
def compare_gpus(model: str, itl_deadline_ms: Optional[float] = None) -> dict:
    """Compare a model's energy per million output tokens on H100 and B200.

    Args:
        model: model name, slug or Hugging Face id.
        itl_deadline_ms: optional latency ceiling in milliseconds. If given, each
            GPU's row is the lowest-energy configuration with median inter-token
            latency at or under it. If omitted, the index rows are compared.

    Returns the best row per GPU and the ratio between them. Models measured on
    only one GPU return that single row.
    """
    m = _find_model(model)
    deadline = _deadline(itl_deadline_ms)
    index = _load("index.json")
    sel = _select(m, None, deadline)
    rows = sel["rows"]
    by_gpu = {r["gpu"]: r for r in rows}
    out: dict[str, Any] = {
        "model": m["name"],
        "unit": index.get("unit"),
        "itl_deadline_ms": sel["ceiling"],
        "itl_deadline_set_by": sel["set_by"],
        "selection": sel["selection"],
        "rows": rows,
    }
    notes = list(sel["notes"])
    if "H100" in by_gpu and "B200" in by_gpu:
        h, b = by_gpu["H100"], by_gpu["B200"]
        out["b200_advantage"] = round(h["wh_per_million_output_tokens"] / b["wh_per_million_output_tokens"], 2)
        notes.insert(0, (
            f"B200 uses {out['b200_advantage']}x less energy per token than H100 for this model, "
            f"at each GPU's best configuration under the {sel['ceiling']:g} ms ceiling."
        ))
    if notes:
        out["note"] = " ".join(notes)
    out["source"] = index.get("source")
    return {**out, **_common(sel["primary"], *sel["docs"])}


@mcp.tool()
def concurrency_curve(model: str, gpu: str) -> dict:
    """Energy per million output tokens at every measured running batch for a model on a GPU.

    Args:
        model: model name, slug or Hugging Face id.
        gpu: "H100" or "B200".

    The running batch (avg_running_batch, vLLM num_requests_running) is how many
    requests the server decodes at once. Energy per token falls as it grows. Use
    this to see where a lightly loaded deployment sits relative to the index.
    """
    m = _find_model(model)
    g = _gpu_name(gpu)
    doc = f"models/{m['slug']}.json"
    detail = _load(doc)
    cfgs = [_row(c) for c in detail["configurations"] if c["gpu"] == g]
    if not cfgs:
        raise ToolError(f"{m['name']} was not measured on {g}. Measured on: {', '.join(m['gpus'])}")
    cfgs.sort(key=lambda c: (c["num_gpus"], _rb(c) if _rb(c) is not None else 0))
    return {
        "model": m["name"],
        "gpu": g,
        "unit": "Wh per million output tokens",
        "configurations": cfgs,
        "source": detail.get("source"),
        **_common(doc),
    }


@mcp.tool()
def grid_intensity(country: str) -> dict:
    """Annual average grid carbon intensity for a country, in g CO2e per kWh.

    Args:
        country: country name (common names such as "UK", "US" or "Turkey"
            work), ISO 3166 alpha-3 code, alpha-2 code where the data carries
            it, or "World".

    display_name is the short name the site shows; name is the data source's label.
    """
    a = _find_area(country)
    grid = _load("grid.json")
    return {
        "display_name": _display(a),
        **a,
        "unit": grid.get("unit"),
        "year": grid.get("year"),
        "grid_caveat": _grid_caveat(grid),
        "source": grid.get("source"),
        "licence": grid.get("licence"),
        **_common("grid.json"),
    }


@mcp.tool()
def gpu_hardware(gpu: Optional[str] = None) -> dict:
    """Manufacturer power ceilings (max TDP), memory, and MIG slice profiles for data-centre GPUs.

    Args:
        gpu: optional filter such as "H100", "H200", "A100" or "B200". Omit for all.

    Whole-system ceilings (for example DGX B200) come with the matching GPU; they
    help choose a system_power_ratio for estimate.
    """
    hw = _load("hardware.json")
    if gpu:
        g = _norm(gpu)
        tdp = [t for t in hw.get("tdp", []) if g and g in _norm(t["gpu"])]
        mig = [p for p in hw.get("mig_profiles", []) if g and g in _norm(p["gpu"])]
        systems = [
            s for s in hw.get("systems", [])
            if g and (g in _norm(str(s.get("gpus", ""))) or g in _norm(str(s.get("system", ""))))
        ]
        if not tdp and not mig and not systems:
            raise ToolError(f"No hardware entry matches '{gpu}'.")
        out: dict[str, Any] = {"tdp": tdp, "mig_profiles": mig}
        if systems:
            out["systems"] = systems
        out.update({"sources": hw.get("sources"), "note": hw.get("note")})
        return {**out, **_common("hardware.json")}
    return {**hw, **_common("hardware.json")}


@mcp.tool()
def sources() -> dict:
    """Every source behind the index, with version, retrieval date and licence, plus the API endpoints."""
    return {**_load("manifest.json"), **_common("manifest.json")}


@mcp.resource("leadgreen://manifest")
def manifest_resource() -> str:
    """The Lead Green API manifest: sources, dates, licences and endpoints."""
    try:
        return json.dumps(_load("manifest.json"), indent=2)
    except ToolError as exc:
        raise ResourceError(str(exc)) from None


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
