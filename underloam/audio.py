"""Tiny generated sounds that fail silently when audio is unavailable."""

from __future__ import annotations

import math
from array import array


class SoundBank:
    """Stores optional Pygame sounds. Missing audio never stops the game."""

    def __init__(self, pygame_module):
        self.pygame = pygame_module
        self.enabled = False
        self.sounds = {}
        try:
            self.pygame.mixer.init(frequency=22050, size=-16, channels=1)
            self.enabled = True
            self.sounds = {
                "dash": self._tone(660, 80),
                "jump": self._tone(440, 90),
                "dig": self._tone(180, 70),
                "death": self._tone(90, 160),
                "break": self._tone(260, 90),
                "exit": self._tone(740, 100),
                "win": self._tone(520, 220),
            }
        except Exception:
            self.enabled = False

    def _tone(self, frequency: int, duration_ms: int):
        sample_rate = 22050
        sample_count = int(sample_rate * duration_ms / 1000)
        samples = array("h")
        for i in range(sample_count):
            fade = 1 - (i / max(sample_count, 1))
            wave = math.sin(2 * math.pi * frequency * i / sample_rate)
            samples.append(int(12000 * fade * wave))
        return self.pygame.mixer.Sound(buffer=samples.tobytes())

    def play(self, name: str) -> None:
        if not self.enabled:
            return
        sound = self.sounds.get(name)
        if sound:
            try:
                sound.play()
            except Exception:
                pass
