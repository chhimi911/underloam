"""Host definitions and the fixed death rotation."""

from dataclasses import dataclass


SPRINGTAIL = "Springtail"
BEETLE = "Dung Beetle"
EARTHWORM = "Earthworm"

HOST_ORDER = (SPRINGTAIL, BEETLE, EARTHWORM)


@dataclass(frozen=True)
class Host:
    name: str
    speed: int
    color_key: str
    corpse_tile: str
    ability_hint: str


HOSTS = {
    SPRINGTAIL: Host(
        name=SPRINGTAIL,
        speed=8,
        color_key="springtail",
        corpse_tile=".",
        ability_hint="Dash with Left Shift or J. Pass through pore gaps.",
    ),
    BEETLE: Host(
        name=BEETLE,
        speed=3,
        color_key="beetle",
        corpse_tile="X",
        ability_hint="Jump with Space. Land on cracked clay to break it.",
    ),
    EARTHWORM: Host(
        name=EARTHWORM,
        speed=4,
        color_key="earthworm",
        corpse_tile="S",
        ability_hint="Hold Down plus left or right to tunnel soft soil.",
    ),
}


def next_host(current_host: str) -> str:
    """Return the next host in the death-only rotation."""

    index = HOST_ORDER.index(current_host)
    return HOST_ORDER[(index + 1) % len(HOST_ORDER)]
