# CODEX_PROMPT.md

## Goal

Build the MVP described in `spec.md`: a fully playable local Python/Pygame prototype of **Underloam**, where three soil-creature hosts solve tile-grid rooms through different movement abilities and a death-morph terrain mechanic.

## Context

- Inspect this folder first.
- Read `AGENTS.md`, `spec.md`, `DESIGN.md`, and `TASKS.md` silently. Do not print their contents.
- `AGENTS.md` is the operating authority.
- `spec.md` defines the game rules.
- `DESIGN.md` defines the visual style.
- `TASKS.md` defines the milestone build order.

## Constraints

- Follow `AGENTS.md` rules and run the checks it lists.
- Build all milestones in one continuous run. Do not stop for approval between milestones.
- Use milestones only as build order:
  - M1: movement and tile collision for all three hosts.
  - M2: hazards, death, and host rotation.
  - M3: death-morph corpse terrain and 3-death room reset.
  - M4: room progression, HUD, and win screen.
- After finishing each milestone, continue directly to the next one unless there is a true blocker.
- Follow `DESIGN.md` exactly: only its palette, typography rules, spacing, and signature element. No design defaults.
- Keep the MVP small. Simplest working implementation.
- Use clearly commented Python modules because the user is not a developer.
- Use Python 3.11 and Pygame.
- Use text-grid rooms in `levels.py`.
- Do not use external art or sound assets.
- Generate simple sounds in code and fail silently if audio is unavailable.
- Do not invent credentials or hard-code secrets.
- Keep `.env.example` current.
- Do not modify `spec.md`, `DESIGN.md`, `AGENTS.md`, `TASKS.md`, or `CODEX_PROMPT.md`.
- Runnable locally with simple commands. No deployment and no GitHub steps.
- If a command fails: read the error, fix the root cause, re-run. Ask only on a true blocker.
- Keep progress updates brief. No printing of full logs or instruction files.

## Done when

- M1–M4 are complete in one continuous build run.
- The game runs locally with `python main.py`.
- Window is 1280x720 at 60 FPS.
- The main workflow works end to end:
  - all three hosts move correctly,
  - host-specific tile rules work,
  - hazards trigger death correctly,
  - Earthworm immunity works,
  - host rotation works only through death,
  - corpse terrain persists,
  - three deaths reset the room,
  - exits progress rooms,
  - win screen appears after Room 3,
  - restart works.
- Available tests and `py_compile` pass, or failures are clearly explained.
- `README.md` has setup, run, controls, mechanics, and test steps.
- `.env.example` exists.
- Final report delivered in this format:

### Build Summary
### Files Changed
### Commands Run
### Checks: Passed / Failed
### Known Limits
### Next Recommended Step
