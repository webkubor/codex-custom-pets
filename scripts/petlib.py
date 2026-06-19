#!/usr/bin/env python3
"""Shared helpers for Codex custom pet scripts."""

from __future__ import annotations

import json
import os
import struct
from pathlib import Path
from typing import Any


EXPECTED_SIZE = (1536, 1872)


def codex_home() -> Path:
    return Path(os.environ.get("CODEX_HOME", Path.home() / ".codex")).expanduser()


def pets_dir() -> Path:
    return codex_home() / "pets"


def config_path() -> Path:
    return codex_home() / "config.toml"


def read_active_pet() -> str | None:
    path = config_path()
    if not path.exists():
        return None
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not stripped.startswith("selected-avatar-id"):
            continue
        _, _, raw = stripped.partition("=")
        value = raw.strip().strip('"').strip("'")
        if value.startswith("custom:"):
            return value.split(":", 1)[1]
        return value or None
    return None


def load_manifest(folder: Path) -> dict[str, Any] | None:
    manifest = folder / "pet.json"
    if not manifest.exists():
        return None
    return json.loads(manifest.read_text(encoding="utf-8"))


def manifest_spritesheet(folder: Path, manifest: dict[str, Any] | None) -> Path | None:
    candidates: list[Path] = []
    if manifest:
        value = manifest.get("spritesheetPath") or manifest.get("spritesheet")
        if isinstance(value, str) and value:
            candidates.append(folder / value)
    candidates.extend([folder / "spritesheet.webp", folder / "spritesheet.png"])
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return None


def image_size(path: Path) -> tuple[int, int] | None:
    data = path.read_bytes()
    if data.startswith(b"\x89PNG\r\n\x1a\n") and len(data) >= 24:
        width, height = struct.unpack(">II", data[16:24])
        return width, height
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return webp_size(data)
    return None


def webp_size(data: bytes) -> tuple[int, int] | None:
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height
    if chunk == b"VP8 " and len(data) >= 30:
        start = data.find(b"\x9d\x01\x2a")
        if start == -1 or len(data) < start + 7:
            return None
        width, height = struct.unpack("<HH", data[start + 3 : start + 7])
        return width & 0x3FFF, height & 0x3FFF
    if chunk == b"VP8L" and len(data) >= 25:
        b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
        width = 1 + (((b1 & 0x3F) << 8) | b0)
        height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
        return width, height
    return None


def validate_folder(folder: Path) -> dict[str, Any]:
    manifest = load_manifest(folder)
    sprite = manifest_spritesheet(folder, manifest)
    errors: list[str] = []
    warnings: list[str] = []

    if manifest is None:
        errors.append("missing pet.json")
    else:
        if not (manifest.get("id") or folder.name):
            errors.append("manifest missing id")
        if not (manifest.get("displayName") or manifest.get("name")):
            warnings.append("manifest missing displayName")
        if not manifest.get("description"):
            warnings.append("manifest missing description")
        if not manifest.get("spritesheetPath"):
            warnings.append("manifest missing spritesheetPath")

    if sprite is None:
        errors.append("missing spritesheet.webp or spritesheet.png")
        size = None
    else:
        size = image_size(sprite)
        if size is None:
            errors.append(f"unsupported spritesheet format: {sprite.name}")
        elif size != EXPECTED_SIZE:
            errors.append(f"spritesheet size {size[0]}x{size[1]} != {EXPECTED_SIZE[0]}x{EXPECTED_SIZE[1]}")

    return {
        "id": folder.name,
        "path": str(folder),
        "manifest": str(folder / "pet.json"),
        "spritesheet": str(sprite) if sprite else None,
        "size": f"{size[0]}x{size[1]}" if size else None,
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
    }
