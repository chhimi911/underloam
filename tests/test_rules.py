from underloam.hosts import BEETLE, EARTHWORM, SPRINGTAIL, next_host
from underloam.levels import ROOMS
from underloam.room import Room
from underloam.tiles import is_passable


def test_host_rotation_is_fixed():
    assert next_host(SPRINGTAIL) == BEETLE
    assert next_host(BEETLE) == EARTHWORM
    assert next_host(EARTHWORM) == SPRINGTAIL


def test_tile_passability_by_host():
    assert is_passable("G", SPRINGTAIL)
    assert not is_passable("G", BEETLE)
    assert not is_passable("S", SPRINGTAIL)
    assert not is_passable("S", EARTHWORM)
    assert is_passable("S", EARTHWORM, digging=True)
    assert not is_passable("X", SPRINGTAIL)
    assert is_passable("H", BEETLE)


def test_corpse_mutation_clamps_and_preserves_spawn_exit():
    room = Room(ROOMS[0])
    room.mutate_corpse_area(2, 3, BEETLE)

    assert room.tile_at(2, 3) == "P"
    assert room.tile_at(1, 2) == "X"
    assert room.tile_at(2, 2) == "X"


def test_three_death_reset_can_restore_room_after_mutations():
    room = Room(ROOMS[0])
    room.mutate_corpse_area(7, 7, SPRINGTAIL)
    room.dig_tile(2, 7)
    room.break_tile(11, 5)

    assert room.grid != room.original
    room.reset()
    assert room.grid == room.original


def test_earthworm_dig_mutation_removes_soft_soil():
    room = Room(ROOMS[0])
    assert room.tile_at(3, 7) == "S"
    room.dig_tile(3, 7)
    assert room.tile_at(3, 7) == "."


def test_beetle_break_mutation_removes_cracked_tile():
    room = Room(ROOMS[0])
    assert room.tile_at(11, 5) == "C"
    room.break_tile(11, 5)
    assert room.tile_at(11, 5) == "."
