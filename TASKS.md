# TASKS.md

## Build Goal

Build a fully playable Python/Pygame prototype of Underloam with host-specific traversal, death-morph terrain, room progression, HUD, win screen, and simple generated sounds.

## Phase 1: Setup

- [ ] Inspect folder.
- [ ] Read `AGENTS.md`.
- [ ] Read `spec.md`.
- [ ] Read `DESIGN.md`.
- [ ] Create Python project structure.
- [ ] Add `requirements.txt` with Pygame and pytest.
- [ ] Add `pyproject.toml` with basic pytest config if useful.
- [ ] Add `.env.example`.
- [ ] Add `README.md` setup section.

## M1: Movement and Tile Collision for All Three Hosts

- [ ] Create `main.py` entry point.
- [ ] Create `underloam/constants.py`.
- [ ] Create `underloam/levels.py` with the three provided rooms.
- [ ] Create `underloam/tiles.py` with tile definitions and passability rules.
- [ ] Create `underloam/hosts.py` with host data and fixed rotation.
- [ ] Create `underloam/room.py` for room loading, tile lookup, spawn lookup, and rendering helpers.
- [ ] Create `underloam/player.py` for player state, movement, gravity, jump, dash, and collision.
- [ ] Create `underloam/game.py` for the game loop.
- [ ] Render placeholder rectangles using the DESIGN.md palette.
- [ ] Implement Springtail movement, no jump, dash, and pass-through `G`.
- [ ] Implement Dung Beetle movement, high jump, and normal collision.
- [ ] Implement Earthworm movement, no jump, no dash, and collision.
- [ ] Add temporary debug key to cycle hosts only for M1 testing, then remove or disable before M2 if host switching must happen only by death.
- [ ] Add tests for tile passability.
- [ ] Run `pytest`.
- [ ] Run `python -m py_compile main.py underloam/*.py`.
- [ ] Record M1 status internally, then continue directly to M2.

## M2: Hazards, Death, and Host Rotation

- [ ] Add hazard contact detection.
- [ ] Implement Earthworm 2-second continuous-contact hazard immunity.
- [ ] Implement death state.
- [ ] Implement fixed host rotation only after death.
- [ ] Respawn at `P` after death.
- [ ] Remove any temporary host-cycle debug key from M1.
- [ ] Add simple generated death sound.
- [ ] Add tests for host rotation.
- [ ] Run `pytest`.
- [ ] Run `python -m py_compile main.py underloam/*.py`.
- [ ] Record M2 status internally, then continue directly to M3.

## M3: Death-Morph Corpse Terrain and 3-Death Room Reset

- [ ] Implement 3x3 tile mutation centered on death point.
- [ ] Springtail corpse converts area to `.`.
- [ ] Dung Beetle corpse converts area to `X`.
- [ ] Earthworm corpse converts area to `S`.
- [ ] Clamp terrain mutation to room bounds.
- [ ] Preserve corpse terrain within the room.
- [ ] Implement Beetle breaking `C` cracked tiles by landing on them.
- [ ] Implement Earthworm tunneling through `S` while holding down plus direction.
- [ ] Persist broken/digged tiles within room.
- [ ] Implement 3-death room reset that clears all mutations and keeps host rotation.
- [ ] Add break/dig sounds.
- [ ] Add tests for corpse mutation and room reset.
- [ ] Run `pytest`.
- [ ] Run `python -m py_compile main.py underloam/*.py`.
- [ ] Record M3 status internally, then continue directly to M4.

## M4: Room Progression, HUD, and Win Screen

- [ ] Implement exit tile detection.
- [ ] Load next room on reaching `E`.
- [ ] Reset deaths-in-room on entering a new room.
- [ ] Preserve host state according to spec when moving rooms unless a death occurs.
- [ ] Add HUD with host name, room number, deaths-in-room, and ability hint.
- [ ] Add win screen after Room 3 with text “You restored the soil”.
- [ ] Add restart option.
- [ ] Add exit and win sounds.
- [ ] Verify all three rooms are playable.
- [ ] Make minimal tile fixes only if a route is unsolvable.
- [ ] Update `README.md` with controls, mechanics, setup, run, and tests.
- [ ] Run `pytest`.
- [ ] Run `python -m py_compile main.py underloam/*.py`.
- [ ] Run manual smoke test as far as the local environment allows.
- [ ] Report final build summary.

## Finish

- [ ] Confirm done criteria in `spec.md`.
- [ ] Confirm no external assets are required.
- [ ] Confirm `.env.example` contains no secrets.
- [ ] List files changed.
- [ ] List commands run.
- [ ] List known limits.

## Handoff

- [ ] Explain how to run the game.
- [ ] Explain how to test the game.
- [ ] Recommend one next step only.
