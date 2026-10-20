"""Build the Smithery variant of the bundle: manifest.json plus each tool's inputSchema.

Smithery's publish API requires an inputSchema object per tool; the MCPB manifest schema forbids
that field (tools items allow only name and description). So the strict bundle in ../../dist stays
the one the site serves and MCPB hosts install, and this script writes a superset for Smithery only.

usage: python build_smithery.py ../../dist/leadgreen-<version>-smithery.mcpb
Refresh tools-input-schemas.json from a live tools/list when a tool's parameters change.
"""
import json, sys, zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
manifest = json.loads((HERE / "manifest.json").read_text(encoding="utf-8"))
schemas = json.loads((HERE / "tools-input-schemas.json").read_text(encoding="utf-8"))
missing = [t["name"] for t in manifest["tools"] if t["name"] not in schemas]
if missing:
    sys.exit(f"no inputSchema for: {', '.join(missing)}")
for t in manifest["tools"]:
    t["inputSchema"] = schemas[t["name"]]
out = Path(sys.argv[1]).resolve()
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.writestr("manifest.json", json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    for rel in ("icon.png", "pyproject.toml", "src/server.py"):
        z.write(HERE / rel, rel)
print(f"wrote {out} ({out.stat().st_size} B): {len(manifest['tools'])} tools with inputSchema")
