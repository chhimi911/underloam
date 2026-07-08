# DESIGN.md

## Design Direction

A subterranean field-guide prototype: clean rectangular game pieces over layered soil colors, with every visual choice serving route readability.

## Banned Defaults

Do not use:

- Default Tailwind gray/blue app styling.
- Cream background + serif display + terracotta accent.
- Near-black background + single neon accent.
- Purple-to-blue gradient heroes.
- Stock gradient blobs, glassmorphism, or decorative UI cards.
- Pixel art or sprite packs.
- Any art asset not generated or drawn in code.
- Extra colors outside the palette below.

If the game could be mistaken for a generic Pygame tile demo, add clarity through the signature element, not through new art.

## Typography

Pygame does not load web fonts by default. Use these exact font decisions:

- Title/display face: `Bungee` if available on the system; otherwise `pygame.font.Font(None, size)` fallback.
- HUD/body face: `Atkinson Hyperlegible` if available on the system; otherwise `pygame.font.Font(None, size)` fallback.
- Utility/mono face: none.
- Type scale: 18 / 24 / 32 / 56px.
- Rules: display face only for win screen title. HUD uses body face. Do not add a third face or require bundled font files.

Do not include or distribute font files.

## Color Palette

Use only these colors.

| Name | Hex | Use |
|---|---|---|
| Loam Backdrop | #21170F | empty/background |
| Stone Solid | #6D6F70 | `X` solid |
| Cracked Clay | #B98B5F | `C` cracked |
| Soft Soil | #4B2D1E | `S` soft soil |
| Pore Dust | #C8C8C0 | `G` pore gap |
| Spore Hazard | #2FA84F | `H` hazard |
| Exit Mycelium | #F6D84A | `E` exit |
| Springtail Cyan | #33D7E8 | Springtail |
| Beetle Umber | #7A4B28 | Dung Beetle |
| Earthworm Pink | #F28BB3 | Earthworm |
| HUD Text | #F2E8D5 | HUD and win text |

## Signature Element

Each host has a small “soil imprint” marker drawn directly under the player rectangle:

- Springtail: three tiny cyan dash ticks.
- Dung Beetle: one flattened brown oval.
- Earthworm: short pink segmented trail.

This is decorative but also helps the user remember which body they are controlling. Keep it simple, drawn with Pygame primitives only.

## Layout and Spacing

- Screen: 1280x720.
- Tile size: 64px.
- Room grid: 20 columns x 10 rows = 1280x640.
- HUD band: remaining 80px.
- Spacing scale: 4 / 8 / 16 / 24 / 32px only.
- Border radius: none. Rectangles stay crisp.
- Shadows: none. Use outlines only if readability needs it.

## Motion

- Target 60 FPS.
- Allowed: simple position changes, dash burst, jump arc, brief 120ms corpse/death flash.
- Not allowed: screen shake, parallax, rapid flashing, particle storms, camera bob, long animations.
- If frame rate drops, remove decorative effects first.

## Components

- HUD: top or bottom band with host name, room number, deaths-in-room, and one-line ability hint.
- Win screen: centered title “You restored the soil” and restart prompt.
- Warnings/errors: draw plain HUD text. Never crash because audio or fonts are unavailable.
- Tile rendering: every tile is a filled rectangle with optional simple outline for readability.

## Copy Voice

- Sentence case.
- Plain verbs.
- HUD names the host and the current ability.
- Prompts say exactly what key does what, such as “Press R to restart”.

## Done Criteria for Design

- Every on-screen color appears in the palette table.
- Player and hazards are readable against all terrain tiles.
- HUD text is readable at 1280x720.
- Signature soil imprint exists for each host.
- No external art assets are required.
