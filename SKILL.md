---
name: codex-custom-pets
description: Create, inspect, validate, repair, package, and select Codex desktop custom pets stored under ~/.codex/pets. Use when the user asks about Codex pets, desktop pets, custom avatars, spritesheets, pet.json, selected-avatar-id, golden-kitten, hatch-pet outputs, or switching the active Codex companion.
---

# Codex Custom Pets

## Overview

Manage Codex desktop custom pets as local packages under `${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/`. Use this skill for quick inventory, validation, activation, and packaging work; delegate full image generation or animation repair to the installed `hatch-pet` skill when available.

## Quick Start

Use the bundled scripts first:

```bash
python scripts/list_pets.py
python scripts/validate_pet.py ~/.codex/pets/golden-kitten
python scripts/select_pet.py golden-kitten
python scripts/install_example_pet.py golden-kitten --select
```

Do not print secrets or unrelated Codex config. Only touch `selected-avatar-id` in `${CODEX_HOME:-$HOME/.codex}/config.toml` when switching pets.

## Pet Package Contract

A custom pet lives at:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
├── pet.json
└── spritesheet.webp   # preferred
```

`spritesheet.png` is tolerated for older local exports, but prefer WebP for new packages.

Canonical `pet.json` shape:

```json
{
  "id": "golden-kitten",
  "displayName": "Golden Kitten",
  "description": "A cute golden shaded kitten companion.",
  "spritesheetPath": "spritesheet.webp"
}
```

Atlas requirements:

- size: `1536x1872`
- grid: `8` columns x `9` rows
- cell: `192x208`
- background: transparent
- unused cells after each row's final frame should be transparent

Read `references/codex-pet-contract.md` for the row map and validation notes.

## Workflow

### Inspect Existing Pets

Run:

```bash
python scripts/list_pets.py --json
```

Report:

- active pet from `selected-avatar-id`
- each pet folder under `~/.codex/pets`
- whether `pet.json` and a spritesheet exist
- which packages fail validation

### Validate Or Repair Metadata

Run validation before selecting or publishing a pet:

```bash
python scripts/validate_pet.py ~/.codex/pets/<pet-id>
```

If only metadata is missing, create or patch `pet.json` to the canonical shape. Preserve the existing spritesheet filename if it is already used locally. Do not regenerate art just to fix metadata.

### Select Active Pet

Run:

```bash
python scripts/select_pet.py <pet-id>
```

This should set:

```toml
selected-avatar-id = "custom:<pet-id>"
```

in `${CODEX_HOME:-$HOME/.codex}/config.toml`. Verify with:

```bash
rg -n 'selected-avatar-id' ~/.codex/config.toml
```

### Create A New Pet

If the user wants a new animated pet from text, a reference image, a mascot, a brand, or a company concept, use the installed `hatch-pet` skill if present:

```text
${CODEX_HOME:-$HOME/.codex}/vendor_imports/skills/skills/.curated/hatch-pet/SKILL.md
```

After `hatch-pet` produces a package, copy the final package under `~/.codex/pets/<pet-id>/`, validate it with `validate_pet.py`, then select it only if the user asked to make it active.

If `hatch-pet` is not installed, keep this skill scoped to packaging and explain that full spritesheet generation requires the hatch-pet pipeline or equivalent image generation workflow.

### Install The Built-In Kitten

This skill ships with a working `golden-kitten` example under `assets/golden-kitten/`. Install it with:

```bash
python scripts/install_example_pet.py golden-kitten --select
```

If the user already has a local `golden-kitten`, do not overwrite it unless they ask. Use `--overwrite --select` only after confirming replacement is intended.

## Safety Rules

- Do not edit generated vendor skills in place.
- Do not overwrite an existing pet folder without making a timestamped backup or asking first.
- Do not delete pet folders unless the user explicitly asks.
- Do not switch the active pet as a side effect of validation.
- Do not store generated images or large binaries inside this skill repository; pet assets belong under `~/.codex/pets` or task-specific output folders.
