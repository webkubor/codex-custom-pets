# Codex Custom Pets

给 Codex 装一只桌面小伙伴。

<p align="center">
  <img src="./assets/golden-kitten/preview.png" width="192" alt="Golden Kitten Codex pet preview" />
</p>

这是一个 Codex Skill，用来安装、校验、切换 Codex 桌面宠物。仓库里已经内置了一只可以直接用的小猫：**Golden Kitten**。

## 给人看的

如果你想让 Codex 有一只可爱的桌面宠物，但不想自己生成 spritesheet、不想手动改配置，就用这个。

你不需要自己敲命令。把下面这句话丢给 Codex，让 Agent 去安装和配置：

```text
使用 https://github.com/webkubor/codex-custom-pets 这个 Codex Skill，安装内置的 golden-kitten 示例宠物，并把它设为我的 Codex 桌面宠物。
```

## 给 Agent 看的

你的任务不是解释工具，而是替用户装好并验证。

推荐执行：

```bash
mkdir -p ~/.codex/skills
git clone https://github.com/webkubor/codex-custom-pets.git ~/.codex/skills/codex-custom-pets
cd ~/.codex/skills/codex-custom-pets
python3 scripts/install_example_pet.py golden-kitten --select
```

如果 skill 已经安装，更新而不是覆盖：

```bash
cd ~/.codex/skills/codex-custom-pets
git pull --ff-only
python3 scripts/install_example_pet.py golden-kitten --select
```

如果本机已经有 `~/.codex/pets/golden-kitten`，不要擅自覆盖。只有用户明确要替换时才执行：

```bash
python3 scripts/install_example_pet.py golden-kitten --overwrite --select
```

安装后必须验证：

```bash
python3 scripts/list_pets.py
python3 scripts/validate_pet.py ~/.codex/pets/golden-kitten
rg -n 'selected-avatar-id' ~/.codex/config.toml
```

预期配置：

```toml
selected-avatar-id = "custom:golden-kitten"
```

## 内置了什么

```text
assets/golden-kitten/
├── preview.png
├── pet.json
└── spritesheet.png
```

`spritesheet.png` 尺寸是 `1536x1872`，符合 Codex 桌面宠物的 8 x 9 动画网格。

## 常用命令

```bash
# 查看本机宠物
python3 scripts/list_pets.py

# 安装内置小猫并设为当前宠物
python3 scripts/install_example_pet.py golden-kitten --select

# 校验某只宠物
python3 scripts/validate_pet.py ~/.codex/pets/golden-kitten

# 切换当前宠物
python3 scripts/select_pet.py golden-kitten
```

这个 skill 负责安装、校验、切换宠物。如果用户要生成一只全新的动画宠物，先用 `hatch-pet` 生成，再用这个 skill 做安装和选择。
