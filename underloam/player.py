"""Player movement and rectangle collision for each host."""

from __future__ import annotations

import pygame

from underloam.constants import (
    DASH_COOLDOWN_MS,
    DASH_DISTANCE,
    GRAVITY,
    MAX_FALL_SPEED,
    PLAYER_HEIGHT,
    PLAYER_WIDTH,
    TILE_SIZE,
)
from underloam.hosts import BEETLE, EARTHWORM, SPRINGTAIL, HOSTS
from underloam.tiles import CRACKED, SOFT_SOIL, is_passable


class Player:
    """A small rectangle controlled through host-specific abilities."""

    def __init__(self, spawn: tuple[int, int], host: str):
        self.rect = pygame.Rect(spawn[0], spawn[1], PLAYER_WIDTH, PLAYER_HEIGHT)
        self.host = host
        self.vel_y = 0.0
        self.on_ground = False
        self.facing = 1
        self.last_dash_ms = -DASH_COOLDOWN_MS
        self.earthworm_hazard_ms = 0
        self.was_touching_hazard = False

    def respawn(self, spawn: tuple[int, int], host: str) -> None:
        self.rect.topleft = spawn
        self.host = host
        self.vel_y = 0.0
        self.on_ground = False
        self.earthworm_hazard_ms = 0
        self.was_touching_hazard = False

    def handle_input(self, keys, room, now_ms: int, sounds) -> None:
        left = keys[pygame.K_LEFT] or keys[pygame.K_a]
        right = keys[pygame.K_RIGHT] or keys[pygame.K_d]
        down = keys[pygame.K_DOWN] or keys[pygame.K_s]
        jump = keys[pygame.K_SPACE]
        dash = keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] or keys[pygame.K_j]

        direction = int(right) - int(left)
        if direction:
            self.facing = direction

        digging = self.host == EARTHWORM and down and direction != 0
        if digging:
            self._dig_ahead(room, direction, sounds)

        self._move_x(room, direction * HOSTS[self.host].speed, digging)

        if self.host == SPRINGTAIL and dash and now_ms - self.last_dash_ms >= DASH_COOLDOWN_MS:
            self._move_x(room, self.facing * DASH_DISTANCE, False)
            self.last_dash_ms = now_ms
            sounds.play("dash")

        if self.host == BEETLE and jump and self.on_ground:
            self.vel_y = -23
            self.on_ground = False
            sounds.play("jump")

    def apply_gravity(self, room, sounds) -> None:
        self.vel_y = min(self.vel_y + GRAVITY, MAX_FALL_SPEED)
        self._move_y(room, int(self.vel_y), sounds)

    def _move_x(self, room, amount: int, digging: bool) -> None:
        if amount == 0:
            return
        step = 1 if amount > 0 else -1
        for _ in range(abs(amount)):
            self.rect.x += step
            if self._collides(room, digging):
                self.rect.x -= step
                break

    def _move_y(self, room, amount: int, sounds) -> None:
        self.on_ground = False
        if amount == 0:
            return
        step = 1 if amount > 0 else -1
        for _ in range(abs(amount)):
            self.rect.y += step
            cracked_landed_on = self._cracked_tiles_underfoot(room) if step > 0 else []
            if self._collides(room, False):
                if step > 0 and self.host == BEETLE and cracked_landed_on:
                    for col, row in cracked_landed_on:
                        room.break_tile(col, row)
                    sounds.play("break")
                    continue
                self.rect.y -= step
                if step > 0:
                    self.on_ground = True
                self.vel_y = 0
                break

    def _collides(self, room, digging: bool) -> bool:
        for col, row in self._covered_tiles():
            if not is_passable(room.tile_at(col, row), self.host, digging):
                return True
        return False

    def _covered_tiles(self) -> set[tuple[int, int]]:
        left = self.rect.left // TILE_SIZE
        right = (self.rect.right - 1) // TILE_SIZE
        top = self.rect.top // TILE_SIZE
        bottom = (self.rect.bottom - 1) // TILE_SIZE
        return {(col, row) for row in range(top, bottom + 1) for col in range(left, right + 1)}

    def _cracked_tiles_underfoot(self, room) -> list[tuple[int, int]]:
        row = (self.rect.bottom - 1) // TILE_SIZE
        cols = {self.rect.left // TILE_SIZE, (self.rect.right - 1) // TILE_SIZE}
        return [(col, row) for col in cols if room.tile_at(col, row) == CRACKED]

    def _dig_ahead(self, room, direction: int, sounds) -> None:
        edge_x = self.rect.right if direction > 0 else self.rect.left - 1
        col = edge_x // TILE_SIZE
        rows = range(self.rect.top // TILE_SIZE, (self.rect.bottom - 1) // TILE_SIZE + 1)
        dug = False
        for row in rows:
            if room.tile_at(col, row) == SOFT_SOIL:
                room.dig_tile(col, row)
                dug = True
        if dug:
            sounds.play("dig")

    def center_tile(self) -> tuple[int, int]:
        return self.rect.centerx // TILE_SIZE, self.rect.centery // TILE_SIZE
