#!/usr/bin/env python3
"""Validate one Codex custom pet package."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from petlib import validate_folder


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Codex custom pet folder.")
    parser.add_argument("pet_folder", help="Path to ~/.codex/pets/<pet-id>.")
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON.")
    args = parser.parse_args()

    result = validate_folder(Path(args.pet_folder).expanduser())
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"pet: {result['id']}")
        print(f"path: {result['path']}")
        print(f"spritesheet: {result['spritesheet'] or '-'}")
        print(f"size: {result['size'] or '-'}")
        print(f"status: {'ok' if result['ok'] else 'broken'}")
        for error in result["errors"]:
            print(f"error: {error}")
        for warning in result["warnings"]:
            print(f"warn: {warning}")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
