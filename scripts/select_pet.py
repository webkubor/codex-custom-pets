#!/usr/bin/env python3
"""Select the active Codex custom pet."""

from __future__ import annotations

import argparse
from pathlib import Path

from petlib import config_path, pets_dir, set_selected_avatar, validate_folder


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
