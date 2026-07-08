"""Shared game constants kept in one place for easy tuning."""

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60
TILE_SIZE = 64
HUD_HEIGHT = 80
GRID_COLS = 20
GRID_ROWS = 10

PLAYER_WIDTH = 42
PLAYER_HEIGHT = 56
GRAVITY = 1.0
MAX_FALL_SPEED = 18

DASH_DISTANCE = 300
DASH_COOLDOWN_MS = 1000
DEATH_FLASH_MS = 120
EARTHWORM_HAZARD_IMMUNITY_MS = 2000

PALETTE = {
    "loam": "#21170F",
    "stone": "#6D6F70",
    "cracked": "#B98B5F",
    "soft": "#4B2D1E",
    "pore": "#C8C8C0",
    "hazard": "#2FA84F",
    "exit": "#F6D84A",
    "springtail": "#33D7E8",
    "beetle": "#7A4B28",
    "earthworm": "#F28BB3",
    "hud": "#F2E8D5",
}
