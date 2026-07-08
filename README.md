# Underloam

Underloam is a local Python/Pygame MVP about three soil-creature hosts solving fixed tile rooms through movement differences, death, and terrain mutation.

## Setup

Use Python 3.11 when available.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

On Windows:

```bash
.venv\Scripts\activate
```

## Run

```bash
python main.py
```

The game opens a 1280x720 window and runs at 60 FPS.

## Controls

- Left/right arrows or A/D: move.
- Space: Dung Beetle jump.
- Left Shift or J: Springtail dash.
- Down plus left/right: Earthworm tunnel through soft soil.
- R: restart the game.
- Esc: quit.

## Mechanics

- Hosts rotate only through death: Springtail, Dung Beetle, Earthworm, then Springtail again.
- Springtail passes through pore gaps and leaves empty tunnel terrain when it dies.
- Dung Beetle jumps high, breaks cracked clay by landing, and leaves solid terrain when it dies.
- Earthworm tunnels soft soil, survives the first 2 seconds of continuous hazard contact, and leaves soft soil when it dies.
- Three deaths in a room reset that room terrain, but the host rotation continues.
- Reaching the exit loads the next room. After Room 3, the win screen appears.

## Tests

```bash
pytest
python -m py_compile main.py underloam/*.py
```

Interactive rendering is intentionally not fully automated. Use `python main.py` for the manual smoke test.
