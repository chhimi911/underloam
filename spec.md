# spec.md

## Goal

Build **Underloam**, a fully playable local Python/Pygame 2D side-scrolling platformer prototype where three soil creatures solve rooms through movement differences and a death-morph terrain mechanic.

## Problem

The prototype needs to prove one core game idea: death is not failure; death reshapes the room and rotates the player into the next host. The code must be readable for a non-developer, so modules must be small, clearly named, and heavily commented around gameplay rules.

## Users

- Primary user: non-developer game designer testing the Underloam mechanic locally.
- Secondary user: Codex or another coding agent extending the prototype later.

## MVP Scope

Version 1 includes:

- Python 3.11 and Pygame.
- 1280x720 window.
- 60 FPS game loop.
- Tile-based rooms defined as text grids in `levels.py`.
- Three playable hosts in fixed death rotation:
  - Springtail → Dung Beetle → Earthworm → Springtail.
- Host switching only through the death mechanic.
- Tile collision and host-specific passability.
- Hazards and host-specific immunity.
- Death-morph corpse terrain conversion.
- Persistent room terrain changes across deaths inside the same room.
- Three deaths in one room triggers full room reset while host rotation continues.
- Three rooms using the provided layouts, with minimal tile placement fixes only if needed to keep all three routes solvable.
- Room progression through `E`.
- Win screen after Room 3: “You restored the soil”.
- Restart option from win screen.
- Simple HUD showing current host and deaths-in-room count.
- Placeholder rectangle graphics only.
- Simple generated sounds for dash, jump, dig, hazard/death, cracked-tile break, exit, and win.
- Clearly commented modules.

## Non-Goals

Version 1 does not include:

- Pixel art.
- Animations beyond simple rectangle movement and optional flash effects.
- Enemies.
- Menus beyond win/restart.
- Save files.
- Level editor.
- Controller support.
- Online features.
- GitHub setup.
- Complex audio assets.
- Camera scrolling beyond what is needed for these fixed-size rooms.
- Polished juice or particle effects.

## Assumptions

- Tile size is 64px, making 20-column rooms exactly 1280px wide. The 10-row rooms occupy 640px, leaving 80px for HUD or top/bottom margin.
- The game uses a fixed camera because provided rooms fit the 1280x720 window.
- Player hitboxes are rectangles smaller than a tile, such as 42x56px, so movement feels playable.
- Gravity applies to Springtail and Beetle. Earthworm can crawl/tunnel and should still collide cleanly with solid terrain.
- Springtail cannot jump but can move horizontally and dash.
- Dung Beetle can jump high enough to clear 3 tile heights. Tune jump velocity/gravity until this is true in-game.
- Earthworm tunnels through `S` only when holding down plus left or right.
- Earthworm hazard immunity applies only while touching hazard tiles and lasts for the first 2 seconds of continuous hazard contact. If contact ends, the timer resets.
- Death point for corpse terrain uses the player's center converted to tile coordinates.
- Corpse terrain affects a clamped 3x3 tile area centered on the death tile.
- Spawn and exit markers act like empty tiles for collision.
- Milestones M1–M4 are build-order checkpoints only. Codex must build all milestones in one continuous run without waiting for approval.

## Recommended Stack

- Runtime: Python 3.11.
- Game library: Pygame.
- Storage: in-memory state only.
- Audio: generated Pygame sounds using `array`/`math` or `pygame.sndarray` if available; do not require external sound files.
- Testing: pytest for pure logic modules where practical, plus manual smoke tests for Pygame behavior.
- Deployment: none. Local run only.

This stack matches the requested tech and keeps the prototype easy to run locally.

## Main Workflow

1. User runs the game.
2. Game opens Room 1 at 1280x720.
3. Player starts at `P` as Springtail.
4. Player controls the current host.
5. Host-specific abilities allow different routes:
   - Springtail dashes and passes through `G`.
   - Dung Beetle jumps high and breaks `C` by landing.
   - Earthworm digs through `S` by holding down plus a direction.
6. If the player touches hazard past any immunity window:
   - Current host dies.
   - 3x3 corpse terrain is written around the death point.
   - Host rotates to the next host.
   - Player respawns at `P`.
   - Death count increments.
7. At three deaths in a room:
   - The room resets to its original layout.
   - Corpse terrain and broken/digged tiles clear.
   - Host rotation continues from the death that triggered reset.
   - Player respawns at `P`.
8. Reaching `E` loads the next room.
9. After Room 3, game shows the win screen.
10. User can restart from the win screen.

## Controls

Use simple keyboard controls:

- Left/right arrows or A/D: move.
- Space: Beetle jump.
- Left Shift or J: Springtail dash.
- Down + left/right: Earthworm tunnel through soft soil.
- R: restart current game from Room 1 on win screen or during play.
- Esc: quit.

Host ability restrictions:

- Springtail cannot jump.
- Dung Beetle cannot dash or dig.
- Earthworm cannot jump or dash.

## Tile Characters

```text
X solid
C cracked, breakable by Beetle landing
G pore gap, passable only by Springtail
S soft soil, diggable only by Earthworm
H hazard
P player spawn
E exit
. empty
```

Collision rules:

- `X` is solid for all hosts.
- `C` is solid for all hosts until broken.
- `G` is solid for Beetle and Earthworm, passable for Springtail.
- `S` is solid for Springtail and Beetle. Earthworm can remove it only while holding down plus a horizontal direction.
- `H` damages on contact but should not be solid unless needed for route stability.
- `P`, `E`, and `.` are passable.

## Hosts

### Springtail

- Visual: cyan rectangle.
- Speed: 8 px/frame.
- Jump: none.
- Dash: horizontal 300 px burst.
- Dash cooldown: 1 second.
- Special passability: can pass through `G`.
- Corpse terrain: converts 3x3 area to empty tunnel tiles (`.`).

### Dung Beetle

- Visual: brown rectangle.
- Speed: 3 px/frame.
- Jump: high jump clearing 3 tiles of height.
- Special interaction: breaks `C` cracked tiles by landing on them.
- Corpse terrain: converts 3x3 area to solid platform tiles (`X`).

### Earthworm

- Visual: pink rectangle.
- Speed: 4 px/frame.
- Jump: none.
- Dash: none.
- Dig: while holding down plus left/right, removes `S` soft soil tiles and moves through them.
- Hazard immunity: first 2 seconds of continuous hazard contact.
- Corpse terrain: converts 3x3 area to soft soil tiles (`S`).

## Death-Morph Mechanic

This is the core feature. Do not simplify it.

When the current host takes hazard damage past any immunity window:

1. Convert the 3x3 tile area centered on the death point:
   - Springtail corpse: `.`
   - Dung Beetle corpse: `X`
   - Earthworm corpse: `S`
2. Respawn the player at `P`.
3. Rotate host:
   - Springtail → Dung Beetle
   - Dung Beetle → Earthworm
   - Earthworm → Springtail
4. Keep corpse terrain and broken/digged tiles persistent inside the current room.
5. Increment deaths-in-room.
6. If deaths-in-room reaches 3:
   - Reset the whole current room to its original layout.
   - Clear corpse terrain, broken cracked tiles, and tunneled soft soil.
   - Keep host rotation as already advanced by the death.
   - Reset deaths-in-room to 0.
   - Respawn at `P`.

## Rooms

Use these three rooms in `levels.py`. You may adjust individual tiles only if a route is unsolvable, and all three route types must remain intact.

Room 1:
```
XXXXXXXXXXXXXXXXXXXX
X..................X
X.....G.......XXX..X
X.P...G.......X.E..X
XXXX..G..XXX..X.XXXX
X.....G....C..X....X
X..XXXXXXX.C..XXXX.X
X..S.......C.......X
X..S..HHH..X..HHH..X
XXXXXXXXXXXXXXXXXXXX
```

Room 2:
```
XXXXXXXXXXXXXXXXXXXX
X.P........G.......X
XXXXXXCXXXXGXXXX...X
X.....C....G...X.E.X
X..H..C........X.XXX
X..XXXXXXXXSSSSX...X
X..........S...XXX.X
X...HHHH...S.......X
X..XXXXXX..S..HH...X
XXXXXXXXXXXXXXXXXXXX
```

Room 3:
```
XXXXXXXXXXXXXXXXXXXX
X.P..............E.X
XXXX..G..XXXXXXXXX.X
X.....G........X...X
X..C..G..HHHH..X.C.X
X..C..XXXXXXXX.X.C.X
X..C...........X...X
X..XXXX..SSSS..XXX.X
X.....H..S..H......X
XXXXXXXXXXXXXXXXXXXX
```

## Level Design Requirements

Each room must remain one layout containing all three route types:

- Springtail route using `G` pore gaps and dash mobility.
- Dung Beetle route using high jump and `C` cracked tile interactions.
- Earthworm route using `S` soft soil tunneling.

All three routes per room must be testable and playable.

## Screens or Interfaces

- Game screen:
  - 1280x720.
  - Level rendered as tiles.
  - Player rectangle.
  - HUD with current host, deaths-in-room, room number, and ability hint.
- Win screen:
  - Text: “You restored the soil”.
  - Restart prompt.

## Suggested File Structure

Codex should create a simple project like this:

```text
underloam/
├── README.md
├── AGENTS.md
├── spec.md
├── DESIGN.md
├── TASKS.md
├── CODEX_PROMPT.md
├── .env.example
├── requirements.txt
├── pyproject.toml
├── main.py
├── underloam/
│   ├── __init__.py
│   ├── constants.py
│   ├── levels.py
│   ├── tiles.py
│   ├── hosts.py
│   ├── player.py
│   ├── room.py
│   ├── game.py
│   ├── audio.py
│   └── utils.py
└── tests/
    ├── test_host_rotation.py
    ├── test_room_mutation.py
    └── test_tile_rules.py
```

If Codex is working in an existing repo, adapt to the repo structure instead of forcing this exact tree.

## Module Responsibilities

- `main.py`: entry point only.
- `constants.py`: screen size, FPS, tile size, colors, physics constants.
- `levels.py`: raw text-grid room definitions.
- `tiles.py`: tile character meanings, passability rules, draw colors.
- `hosts.py`: host definitions and rotation order.
- `player.py`: player state, movement, ability handling, collision resolution.
- `room.py`: room grid loading, mutation, reset, tile queries.
- `game.py`: main loop, state transitions, room progression, HUD, win screen.
- `audio.py`: simple generated sound effects.
- `utils.py`: small helpers like grid-to-pixel conversion.
- `tests/`: pure logic tests, not full Pygame rendering tests.

## Graphics

Use placeholder rectangles only:

- Springtail: cyan rectangle.
- Dung Beetle: brown rectangle.
- Earthworm: pink rectangle.
- Hazards: green.
- Solid: gray.
- Cracked: tan.
- Soft soil: dark brown.
- Pore gaps: light gray.
- Exit: yellow.
- Empty: background color.

No external art assets.

## Sound

Include simple sounds as needed, generated in code:

- Dash.
- Jump.
- Dig.
- Hazard/death.
- Cracked tile break.
- Exit.
- Win.

Do not require external audio files. If Pygame mixer is unavailable, the game should still run silently with no crash.

## Accessibility and Usability

This is a Pygame game, not a web app. Still include:

- Large readable HUD text.
- High contrast between player, hazards, exit, and terrain.
- Keyboard-only play.
- Simple controls.
- No color-only critical information: HUD text names host and ability.
- Avoid rapid flashing.
- Allow restart with a clear key prompt.

## Privacy and Security

- No accounts.
- No network calls.
- No analytics.
- No stored personal data.
- No secrets required.
- `.env.example` should say no environment variables are needed.

## Testing Plan

Automated tests:

- Host rotation order.
- Tile passability rules by host.
- Corpse terrain 3x3 mutation.
- Three-death room reset behavior.
- Beetle cracked tile break logic where practical.
- Earthworm soft soil dig mutation where practical.

Manual smoke test:

1. Start the game.
2. Confirm 1280x720 window opens.
3. Confirm Room 1 loads with player at `P`.
4. Confirm Springtail moves, cannot jump, can dash, and can pass through `G`.
5. Trigger hazard death and confirm host changes to Beetle.
6. Confirm Beetle can jump high and break `C` by landing.
7. Trigger hazard death and confirm host changes to Earthworm.
8. Confirm Earthworm digs through `S` with down plus direction.
9. Confirm Earthworm survives first 2 seconds of continuous hazard contact, then dies.
10. Confirm corpse terrain persists across deaths.
11. Confirm third death resets the current room and rotation continues.
12. Confirm reaching `E` advances rooms.
13. Confirm win screen after Room 3.
14. Confirm restart works.

## Build Order

Codex must build in approval milestones:

### M1: Movement and Tile Collision

- Create project structure.
- Add Pygame setup.
- Add rooms from `levels.py`.
- Render tiles and current host rectangle.
- Implement all three host movement rules.
- Implement tile collision and host-specific passability.
- Add basic keyboard controls.
- Stop and report M1 status. Wait for approval.

### M2: Hazards, Death, and Host Rotation

- Add hazard detection.
- Add Earthworm 2-second hazard immunity.
- Add death handling.
- Add fixed host rotation.
- Add respawn at `P`.
- Add simple death sound.
- Stop and report M2 status. Wait for approval.

### M3: Death-Morph Terrain and 3-Death Room Reset

- Add 3x3 corpse terrain conversion.
- Persist terrain changes within room.
- Add Beetle cracked tile breaking.
- Add Earthworm soft soil tunneling.
- Add 3-death room reset.
- Add sounds for break/dig.
- Stop and report M3 status. Wait for approval.

### M4: Room Progression, HUD, and Win Screen

- Add `E` exit detection.
- Add next-room loading.
- Add win screen after Room 3.
- Add restart option.
- Add full HUD.
- Add final sounds.
- Run checks and update README.
- Report final build summary.

## Risks

- Pygame physics may need tuning so Beetle reliably clears 3 tile heights.
- The provided rooms may need tiny tile adjustments to make all three routes genuinely solvable.
- Collision with pass-through `G` and diggable `S` can produce edge cases if implemented as one-off exceptions instead of centralized tile rules.
- Generated audio may be unavailable on systems without mixer support; handle gracefully.
- Milestone approval mode means the game will not be fully playable until M4 is complete.

## Done Criteria

The MVP is done when:

- The game runs locally with `python main.py`.
- Window is 1280x720 at 60 FPS.
- All three rooms load and are playable.
- All three hosts match the required movement/ability rules.
- Death-morph terrain works exactly as specified.
- Three-death room reset works exactly as specified.
- Reaching `E` progresses rooms.
- Win screen appears after Room 3.
- Restart works.
- HUD shows current host and deaths-in-room count.
- Sounds play when mixer is available and fail silently when unavailable.
- Code is clearly commented and separated into readable modules.
- Tests/checks pass or any limitations are clearly explained.
- `README.md` has setup, run, controls, and testing instructions.
