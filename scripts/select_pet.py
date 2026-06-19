#!/usr/bin/env python3
"""Select the active Codex custom pet."""

from __future__ import annotations

import argparse
from pathlib import Path

from petlib import config_path, pets_dir, validate_folder


def set_selected_avatar(pet_id: str) -> None:
    path = config_path()
    value = f'selected-avatar-id = "custom:{pet_id}"'
    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        lines = []

    replaced = False
    out: list[str] = []
    for line in lines:
        if line.strip().startswith("selected-avatar-id"):
            out.append(value)
            replaced = True
        else:
            out.append(line)
    if not replaced:
        if out and out[-1].strip():
            out.append("")
        out.append(value)
    path.write_text("\n".join(out) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Set selected-avatar-id to custom:<pet-id>.")
    parser.add_argument("pet_id", help="Folder name under ~/.codex/pets.")
    parser.add_argument("--force", action="store_true", help="Select even if validation fails.")
    args = parser.parse_args()

    folder = pets_dir() / args.pet_id
    if not folder.exists():
        print(f"error: pet folder not found: {folder}")
        return 1

    result = validate_folder(folder)
    if not result["ok"] and not args.force:
        print(f"error: pet is not valid: {args.pet_id}")
        for error in result["errors"]:
            print(f"  - {error}")
        print("Use --force to select anyway.")
        return 1

    set_selected_avatar(args.pet_id)
    print(f"selected-avatar-id = custom:{args.pet_id}")
    print(f"config: {config_path()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
