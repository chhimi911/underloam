# README_START_HERE.md

# Underloam Codex Handoff

This package gives Codex everything needed to build **Underloam**, a local Python/Pygame 2D side-scrolling platformer prototype.

The game should be built as clearly commented Python modules, because the owner is not a developer and needs readable code.

## Files Included

```text
underloam-codex-handoff/
├── README_START_HERE.md
├── spec.md
├── DESIGN.md
├── AGENTS.md
├── TASKS.md
├── CODEX_PROMPT.md
└── .env.example
```

## What Codex Should Build

A playable Pygame prototype with:

- Python 3.11
- Pygame
- 1280x720 window
- 60 FPS
- Tile-grid rooms in `levels.py`
- Three hosts: Springtail, Dung Beetle, Earthworm
- Death-morph host rotation
- Persistent corpse terrain inside each room
- Full reset every 3 deaths in a room
- Room progression and win screen
- Simple generated sounds
- Placeholder rectangle graphics only

## Beginner Workflow

1. Download and unzip this package.
2. Open the unzipped folder in Codex Desktop.
3. Open `CODEX_PROMPT.md`.
4. Paste the whole prompt into Codex.
5. Let Codex create the game files.

## Important

Do **not** start with GitHub.
Do **not** ask Codex to redesign the game.
Do **not** add extra hosts, enemies, particle systems, save files, menus, or complex art.

Build the boring playable version first.

## Milestone Build Order

Codex should build the whole game in one continuous run.

Milestones are only the internal build order:

1. M1: movement and tile collision for all three hosts
2. M2: hazards, death, and host rotation
3. M3: death-morph corpse terrain and 3-death room reset
4. M4: room progression, HUD, and win screen

Codex should not wait for approval between milestones.

## One Next Action

Open `CODEX_PROMPT.md` and paste it into Codex Desktop.
