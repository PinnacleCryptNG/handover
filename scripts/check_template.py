#!/usr/bin/env python3
"""Sanity-check the Handover template: valid YAML, every room agent is defined,
links point at real rooms, and each instruction's {param} is declared."""
import re
import sys
from pathlib import Path

import yaml

path = Path(sys.argv[1] if len(sys.argv) > 1 else "templates/handover.template.yaml")
t = yaml.safe_load(path.read_text())
errors = []
params = set(t.get("params", {})) | {"$creator"}

agents = {a["name"] for a in t["agents"]}
rooms = {r["name"] for r in t["rooms"]}
for r in t["rooms"]:
    for a in r.get("agents", []):
        if a not in agents:
            errors.append(f"room {r['name']} uses undefined agent {a}")
for link in t.get("links", []):
    for end in (link.get("from"), link.get("to")):
        if end not in rooms:
            errors.append(f"link points at unknown room {end}")
for name in set(re.findall(r"\{(\$?\w+)\}", path.read_text())):
    if name not in params:
        errors.append(f"undeclared param {{{name}}}")

print("\n".join(errors) or f"{path}: {len(agents)} agents, {len(rooms)} rooms, ok")
sys.exit(1 if errors else 0)
