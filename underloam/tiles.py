"""Tile rules centralize collision and gameplay meaning."""

from underloam.hosts import SPRINGTAIL

SOLID = "X"
CRACKED = "C"
PORE = "G"
SOFT_SOIL = "S"
HAZARD = "H"
SPAWN = "P"
EXIT = "E"
EMPTY = "."

PASSABLE_TILES = {EMPTY, SPAWN, EXIT, HAZARD}


def is_passable(tile: str, host: str, digging: bool = False) -> bool:
    """Return whether a host can move through this tile right now."""

    if tile in PASSABLE_TILES:
        return True
    if tile == PORE:
        return host == SPRINGTAIL
    if tile == SOFT_SOIL:
        return digging
    return False


def is_hazard(tile: str) -> bool:
    return tile == HAZARD


def is_breakable(tile: str) -> bool:
    return tile == CRACKED
