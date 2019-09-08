from pathlib import Path

from ZoneStuff import Zone1


def test_zone1():
    test_zone = Zone1(Path('../examples/Tutorial.zone'))

    assert test_zone.quads_per_tile == 64
    assert test_zone.tile_size == 64.0

    assert test_zone.verts_per_tile == 65
    assert test_zone.tiles_per_chunk == 8
    assert test_zone.start_x == -8
    assert test_zone.start_y == -8
    assert test_zone.chunks_x == 16
    assert test_zone.chunks_y == 16

    assert test_zone.eco_count == 12
