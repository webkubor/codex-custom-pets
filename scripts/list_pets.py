#!/usr/bin/env python3
"""List local Codex custom pets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from petlib import pets_dir, read_active_pet, validate_folder


def main() -> int:
    parser = argparse.ArgumentParser(description="List Codex custom pets.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    root = pets_dir()
    active = read_active_pet()
    folders = sorted([p for p in root.iterdir() if p.is_dir()]) if root.exists() else []
    results = [validate_folder(folder) for folder in folders]

    if args.json:
        print(json.dumps({"active": active, "pets_dir": str(root), "pets": results}, indent=2))
        return 0

    print(f"pets_dir: {root}")
    print(f"active: {active or '-'}")
    for item in results:
        marker = "*" if item["id"] == active else " "
        status = "ok" if item["ok"] else "broken"
        sprite = Path(item["spritesheet"]).name if item["spritesheet"] else "-"
        print(f"{marker} {item['id']}: {status} ({sprite}, {item['size'] or 'unknown-size'})")
        for error in item["errors"]:
            print(f"    error: {error}")
        for warning in item["warnings"]:
            print(f"    warn: {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
