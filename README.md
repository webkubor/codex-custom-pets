# Codex Custom Pets

Codex skill for managing desktop custom pets under `~/.codex/pets`.

Use it to:

- list installed custom pets
- validate `pet.json` + `spritesheet`
- switch the active Codex desktop pet
- install the bundled `golden-kitten` example
- hand off full pet generation to `hatch-pet` when available

## Install

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/webkubor/codex-custom-pets.git ~/.codex/skills/codex-custom-pets
```

If you already cloned it somewhere else, symlink it:

```bash
ln -s /path/to/codex-custom-pets ~/.codex/skills/codex-custom-pets
```

## Quick Use

```bash
cd ~/.codex/skills/codex-custom-pets

# List local pets and show the active one
python3 scripts/list_pets.py

# Install the bundled kitten example
python3 scripts/install_example_pet.py golden-kitten --select

# Validate one pet package
python3 scripts/validate_pet.py ~/.codex/pets/golden-kitten

# Select a pet as the active Codex companion
python3 scripts/select_pet.py golden-kitten
```

The active pet is stored in:

```toml
selected-avatar-id = "custom:<pet-id>"
```

inside `~/.codex/config.toml`.

## Pet Package Shape

```text
~/.codex/pets/<pet-id>/
├── pet.json
└── spritesheet.webp   # preferred
```

Older local exports with `spritesheet.png` are supported.

Required atlas size:

```text
1536x1872
```

## Bundled Example

This repo includes:

```text
assets/golden-kitten/
├── pet.json
└── spritesheet.png
```

Install it:

```bash
python3 scripts/install_example_pet.py golden-kitten --select
```

If `~/.codex/pets/golden-kitten` already exists, the script refuses to overwrite it. Use this only when you really want to replace it:

```bash
python3 scripts/install_example_pet.py golden-kitten --overwrite --select
```

## Use From Codex

Ask:

```text
Use $codex-custom-pets to list my installed Codex pets.
Use $codex-custom-pets to validate ~/.codex/pets/golden-kitten.
Use $codex-custom-pets to switch my active pet to golden-kitten.
```

For generating a brand-new animated pet, use `hatch-pet` if it is installed, then validate and select the output with this skill.
