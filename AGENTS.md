# AGENTS.md

## Commands

Use these commands for this Python/Pygame project.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python main.py
pytest
python -m py_compile main.py underloam/*.py
```

On Windows, activate the virtual environment with:

```bash
.venv\Scripts\activate
```

Run tests and `py_compile` before the final report, and optionally after major milestones if useful. If a command does not exist yet, create the missing project file or report it as unavailable.

## Project Mission

Build the Underloam MVP in `spec.md`. Small, playable prototype first. Do not overengineer.

## Read First

1. `spec.md` - gameplay and mechanics.
2. `DESIGN.md` - visual rules.
3. `TASKS.md` - milestone build order.

Read silently. Do not print file contents.

## Milestone Build Order

Build all milestones in one continuous run. Do not stop for approval between milestones.

Use this order:

1. M1: movement and tile collision for all three hosts.
2. M2: hazards, death, and host rotation.
3. M3: death-morph corpse terrain and 3-death room reset.
4. M4: room progression, HUD, and win screen.

After finishing a milestone, continue directly to the next one unless there is a true blocker.

## Build Rules

- Follow `spec.md` exactly.
- Follow `DESIGN.md` exactly: only its colors, typography rules, spacing, and signature element.
- Use Python 3.11 and Pygame.
- Keep modules clearly commented for a non-developer.
- Prefer simple rectangles and pure Pygame primitives.
- No external image or sound assets.
- Generate simple sounds in code and fail silently if mixer is unavailable.
- Do not invent credentials or hard-code secrets.
- Keep `.env.example` current with placeholders only.
- Update `README.md` with setup, run, controls, and test steps.

## Coding Standards

- Clear module names.
- Small functions.
- Comments should explain gameplay rules, not every line of syntax.
- Keep tile passability rules centralized.
- Keep host constants centralized.
- Keep room mutation logic testable without launching Pygame.
- Avoid clever physics. Use simple, readable rectangle collision.

## Testing Standards

Add pytest tests for pure logic where practical:

- Host rotation.
- Tile passability by host.
- 3x3 corpse terrain mutation.
- Three-death reset.
- Earthworm dig mutation.
- Beetle cracked tile break behavior where practical.

Do not try to fully automate interactive Pygame rendering.

## Self-Correction

If a check fails:

1. Read the error.
2. Fix the root cause.
3. Re-run the check.
4. Repeat until passing or truly blocked.

Do not stop for style questions. Make a reasonable call and continue.

## True Blockers

Stop and ask only if:

- A required external credential is missing.
- A major product decision is not covered by `spec.md`.
- Pygame cannot run in the local environment and no headless-safe check is available.
- A requested feature conflicts with the core mechanics.

## Done Criteria

- Game runs locally with `python main.py`.
- M1–M4 are implemented in order.
- Main workflow works end to end.
- Tests and `py_compile` pass, or failures are clearly explained.
- `README.md` updated.
- `.env.example` exists.
- Final report lists changed files and commands run.
