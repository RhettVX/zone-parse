from pathlib import Path

from ZoneStuff import Zone


def test_zone1():
    test_zone = Zone(Path('../examples/Tutorial.zone'))

    assert test_zone.quads_per_tile == 64
    assert test_zone.tile_size == 64.0

    assert test_zone.verts_per_tile == 65
    assert test_zone.tiles_per_chunk == 8
    assert test_zone.start_x == -8
    assert test_zone.start_y == -8
    assert test_zone.chunks_x == 16
    assert test_zone.chunks_y == 16

    assert test_zone.eco_count == 12 and len(test_zone.ecos) == 12
    assert test_zone.ecos[0].index == 0

    tp = test_zone.ecos[0].texture_part
    assert tp.name == 'Indar_dirt_packdark'
    assert tp.color_nx_map == 'Indar_dirt_packdark_cnx.dds'
    assert tp.spec_blend_ny_map == 'Indar_dirt_packdark_sbny.dds'
    assert tp.detail_repeat == 14
    assert tp.blend_strength == 1.283335
    assert tp.spec_min == 0.026
    assert tp.spec_max == 0.714
    assert tp.spec_smoothness_min == 0.0
    assert tp.spec_smoothness_max == 0.623
    assert tp.physics_material == 'dirtlightbrown'

    fp = test_zone.ecos[0].flora_part
    assert fp.layer_count == 4 and len(fp.layers) == 4

    l = fp.layers[0]
    assert l.density == 2200.0
    assert l.min_scale == 0.2
    assert l.max_scale == 0.9
    assert l.slope_peak == 0.0
    assert l.slope_extent == 1.047198
    assert l.min_elevation == -9999.0
    assert l.max_elevation == 9999.0
    assert l.min_alpha == 110
    assert l.flora_name == 'flora_rock02'

    assert l.tint_count == 2 and len(l.tints) == 2

    assert l.tints[0].color_rgba == (49, 105, 147, 255)
    assert l.tints[0].strength == 63  # Should be 100?

    # TODO: Check Floras
