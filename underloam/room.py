"""Mutable room state for terrain changes that persist until reset."""

from copy import deepcopy

from underloam.constants import GRID_COLS, GRID_ROWS, TILE_SIZE
from underloam.hosts import HOSTS
from underloam.tiles import EMPTY, EXIT, SPAWN


class Room:
    """A room stores both original and current terrain grids."""

    def __init__(self, rows: list[str]):
        self.original = [list(row) for row in rows]
        self.grid = deepcopy(self.original)

    def reset(self) -> None:
        """Restore the room exactly to its source text layout."""

        self.grid = deepcopy(self.original)

    def tile_at(self, col: int, row: int) -> str:
        if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
            return self.grid[row][col]
        return "X"

    def set_tile(self, col: int, row: int, tile: str) -> None:
        if 0 <= col < GRID_COLS and 0 <= row < GRID_ROWS:
            self.grid[row][col] = tile

    def find_tile(self, target: str) -> tuple[int, int]:
        for row_index, row in enumerate(self.grid):
            for col_index, tile in enumerate(row):
                if tile == target:
                    return col_index, row_index
        raise ValueError(f"Room is missing tile {target!r}")

    def spawn_pixel(self) -> tuple[int, int]:
        col, row = self.find_tile(SPAWN)
        x = col * TILE_SIZE + (TILE_SIZE - 42) // 2
        y = row * TILE_SIZE + (TILE_SIZE - 56)
        return x, y

    def mutate_corpse_area(self, center_col: int, center_row: int, host_name: str) -> None:
        """Apply the host corpse terrain to a clamped 3x3 tile area."""

        corpse_tile = HOSTS[host_name].corpse_tile
        for row in range(center_row - 1, center_row + 2):
            for col in range(center_col - 1, center_col + 2):
                if self.tile_at(col, row) in {SPAWN, EXIT}:
                    continue
                self.set_tile(col, row, corpse_tile)

    def break_tile(self, col: int, row: int) -> None:
        self.set_tile(col, row, EMPTY)

    def dig_tile(self, col: int, row: int) -> None:
        self.set_tile(col, row, EMPTY)
