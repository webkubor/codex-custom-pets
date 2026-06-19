#!/usr/bin/env python3
"""Install a bundled example Codex custom pet."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

from petlib import pets_dir, set_selected_avatar, validate_folder


def skill_root() -> Path:
    return Path(__file__).resolve().parents[1]


def install_example(pet_id: str, overwrite: bool) -> Path:
    source = skill_root() / "assets" / pet_id
    target = pets_dir() / pet_id
    if not source.exists():
        raise FileNotFoundError(f"example pet not found: {source}")
    if target.exists():
        if not overwrite:
            raise FileExistsError(f"target already exists: {target} (use --overwrite)")
        if not target.is_dir():
            raise FileExistsError(f"target exists and is not a directory: {target}")
        shutil.rmtree(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(source, target)
    return target


def main() -> int:
    parser = argparse.ArgumentParser(description="Install a bundled example pet into ~/.codex/pets.")
    parser.add_argument("pet_id", nargs="?", default="golden-kitten", help="Bundled pet id to install.")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing local pet folder.")
    parser.add_argument("--select", action="store_true", help="Set the installed pet as active.")
    args = parser.parse_args()

    try:
        target = install_example(args.pet_id, args.overwrite)
    except (FileNotFoundError, FileExistsError) as exc:
        print(f"error: {exc}")
        return 1

    result = validate_folder(target)
    if not result["ok"]:
        print(f"error: installed pet failed validation: {target}")
        for error in result["errors"]:
            print(f"  - {error}")
        return 1

    print(f"installed: {target}")
    if args.select:
        set_selected_avatar(args.pet_id)
        print(f"selected-avatar-id = custom:{args.pet_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
