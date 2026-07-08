"""Pygame loop, drawing, room progression, death, and restart flow."""

from __future__ import annotations

import pygame

from underloam.audio import SoundBank
from underloam.constants import (
    DEATH_FLASH_MS,
    EARTHWORM_HAZARD_IMMUNITY_MS,
    FPS,
    GRID_ROWS,
    HUD_HEIGHT,
    PALETTE,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TILE_SIZE,
)
from underloam.hosts import EARTHWORM, HOSTS, SPRINGTAIL, next_host
from underloam.levels import ROOMS
from underloam.player import Player
from underloam.room import Room
from underloam.tiles import CRACKED, EMPTY, EXIT, HAZARD, PORE, SOFT_SOIL, SOLID, is_hazard


TILE_COLORS = {
    SOLID: "stone",
    CRACKED: "cracked",
    SOFT_SOIL: "soft",
    PORE: "pore",
    HAZARD: "hazard",
    EXIT: "exit",
    EMPTY: "loam",
    "P": "loam",
}


class Game:
    """Owns high-level state and keeps the rules readable."""

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Underloam")
        self.clock = pygame.time.Clock()
        self.sounds = SoundBank(pygame)
        self.display_font = self._font("Bungee", 56)
        self.body_font = self._font("Atkinson Hyperlegible", 24)
        self.small_font = self._font("Atkinson Hyperlegible", 18)
        self.restart_game()

    def _font(self, name: str, size: int):
        available = pygame.font.get_fonts()
        normalized = name.lower().replace(" ", "")
        if normalized in available:
            return pygame.font.SysFont(name, size)
        return pygame.font.Font(None, size)

    def restart_game(self) -> None:
        self.rooms = [Room(rows) for rows in ROOMS]
        self.room_index = 0
        self.current_host = SPRINGTAIL
        self.deaths_in_room = 0
        self.win = False
        self.death_flash_until = 0
        self.player = Player(self.current_room.spawn_pixel(), self.current_host)

    @property
    def current_room(self) -> Room:
        return self.rooms[self.room_index]

    def run(self) -> None:
        running = True
        while running:
            now_ms = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                        self.restart_game()

            if not self.win:
                self.update(now_ms)
            self.draw(now_ms)
            self.clock.tick(FPS)
        pygame.quit()

    def update(self, now_ms: int) -> None:
        keys = pygame.key.get_pressed()
        self.player.handle_input(keys, self.current_room, now_ms, self.sounds)
        self.player.apply_gravity(self.current_room, self.sounds)
        self._handle_hazards()
        self._handle_exit()

    def _handle_hazards(self) -> None:
        touching = any(is_hazard(self.current_room.tile_at(col, row)) for col, row in self.player._covered_tiles())
        if self.player.host == EARTHWORM:
            if touching:
                self.player.earthworm_hazard_ms += self.clock.get_time()
                if self.player.earthworm_hazard_ms <= EARTHWORM_HAZARD_IMMUNITY_MS:
                    return
            else:
                self.player.earthworm_hazard_ms = 0
                return
        elif not touching:
            return
        self._kill_player()

    def _kill_player(self) -> None:
        dead_host = self.current_host
        center_col, center_row = self.player.center_tile()
        self.current_room.mutate_corpse_area(center_col, center_row, dead_host)
        self.current_host = next_host(self.current_host)
        self.deaths_in_room += 1
        if self.deaths_in_room >= 3:
            self.current_room.reset()
            self.deaths_in_room = 0
        self.player.respawn(self.current_room.spawn_pixel(), self.current_host)
        self.death_flash_until = pygame.time.get_ticks() + DEATH_FLASH_MS
        self.sounds.play("death")

    def _handle_exit(self) -> None:
        if not any(self.current_room.tile_at(col, row) == EXIT for col, row in self.player._covered_tiles()):
            return
        self.sounds.play("exit")
        self.room_index += 1
        if self.room_index >= len(self.rooms):
            self.win = True
            self.sounds.play("win")
            return
        self.deaths_in_room = 0
        self.player.respawn(self.current_room.spawn_pixel(), self.current_host)

    def draw(self, now_ms: int) -> None:
        self.screen.fill(PALETTE["loam"])
        if self.win:
            self._draw_win()
        else:
            self._draw_room()
            self._draw_player()
            if now_ms < self.death_flash_until:
                pygame.draw.rect(self.screen, PALETTE["hud"], (0, 0, SCREEN_WIDTH, GRID_ROWS * TILE_SIZE), 4)
            self._draw_hud()
        pygame.display.flip()

    def _draw_room(self) -> None:
        for row in range(GRID_ROWS):
            for col in range(SCREEN_WIDTH // TILE_SIZE):
                tile = self.current_room.tile_at(col, row)
                rect = pygame.Rect(col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, PALETTE[TILE_COLORS.get(tile, "loam")], rect)
                if tile != EMPTY:
                    pygame.draw.rect(self.screen, PALETTE["loam"], rect, 1)

    def _draw_player(self) -> None:
        host = HOSTS[self.current_host]
        pygame.draw.rect(self.screen, PALETTE[host.color_key], self.player.rect)
        self._draw_imprint(host.color_key)

    def _draw_imprint(self, color_key: str) -> None:
        color = PALETTE[color_key]
        y = self.player.rect.bottom + 4
        x = self.player.rect.centerx
        if self.current_host == SPRINGTAIL:
            for offset in (-12, 0, 12):
                pygame.draw.line(self.screen, color, (x + offset - 4, y), (x + offset + 4, y), 2)
        elif self.current_host == EARTHWORM:
            for offset in (-10, 0, 10):
                pygame.draw.rect(self.screen, color, (x + offset, y, 6, 3))
        else:
            pygame.draw.ellipse(self.screen, color, (x - 14, y - 2, 28, 6))

    def _draw_hud(self) -> None:
        hud_top = GRID_ROWS * TILE_SIZE
        pygame.draw.rect(self.screen, PALETTE["loam"], (0, hud_top, SCREEN_WIDTH, HUD_HEIGHT))
        host = HOSTS[self.current_host]
        status = f"Host: {host.name}   Room: {self.room_index + 1}/3   Deaths in room: {self.deaths_in_room}/3"
        self._text(status, self.body_font, 24, hud_top + 12)
        self._text(host.ability_hint, self.small_font, 24, hud_top + 44)

    def _draw_win(self) -> None:
        title = self.display_font.render("You restored the soil", True, PALETTE["hud"])
        prompt = self.body_font.render("Press R to restart", True, PALETTE["hud"])
        self.screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)))
        self.screen.blit(prompt, prompt.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 32)))

    def _text(self, text: str, font, x: int, y: int) -> None:
        surface = font.render(text, True, PALETTE["hud"])
        self.screen.blit(surface, (x, y))
