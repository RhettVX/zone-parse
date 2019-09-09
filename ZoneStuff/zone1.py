from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from ZoneStuff.eco import Eco, Layer, Tint
from .struct_reader import BinaryStructReader

_MAGIC = b'ZONE'
_VERSION = 0x1
_MAX_FLOAT = 6


# TODO: Move behavior for reading ecos to their respective classes
@dataclass()
class Zone1:
    path: Path = field()
    name: str = field()

    unk_block: bytes = field(repr=False)

    quads_per_tile: int = field()
    tile_size: float = field()

    unk0: bytes = field(repr=False)

    verts_per_tile: int = field()
    tiles_per_chunk: int = field()

    start_x: int = field()
    start_y: int = field()
    chunks_x: int = field()
    chunks_y: int = field()

    eco_count: int = field()
    ecos: List[Eco] = field()

    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

        with BinaryStructReader(self.path) as reader:
            assert reader.read(len(_MAGIC)) == _MAGIC, 'Invalid magic'
            assert reader.uint32LE() == _VERSION, 'Invalid version'
            self.unk_block = reader.read(24)

            self.quads_per_tile = reader.uint32LE()
            self.tile_size = reader.float32LE()

            self.unk0 = reader.read(4)

            self.verts_per_tile = reader.uint32LE()
            self.tiles_per_chunk = reader.uint32LE()

            self.start_x = reader.int32LE()
            self.start_y = reader.int32LE()
            self.chunks_x = reader.uint32LE()
            self.chunks_y = reader.uint32LE()

            self.eco_count = reader.uint32LE()
            self.ecos = []
            for i in range(self.eco_count):
                e = Eco()

                e.texture_part.unk0 = reader.uint32LE()
                e.texture_part.name = reader.ztstring()
                e.texture_part.color_nx_map = reader.ztstring()
                e.texture_part.spec_blend_ny_map = reader.ztstring()
                e.texture_part.detail_repeat = reader.uint32LE()
                e.texture_part.blend_strength = reader.float32LE(_MAX_FLOAT)
                e.texture_part.spec_min = reader.float32LE(_MAX_FLOAT)
                e.texture_part.spec_max = reader.float32LE(_MAX_FLOAT)
                e.texture_part.spec_smoothness_min = reader.float32LE(_MAX_FLOAT)
                e.texture_part.spec_smoothness_max = reader.float32LE(_MAX_FLOAT)
                e.texture_part.physics_material = reader.ztstring()

                e.flora_part.layer_count = reader.uint32LE()
                for j in range(e.flora_part.layer_count):
                    l = Layer()

                    l.density = reader.float32LE(_MAX_FLOAT)
                    l.min_scale = reader.float32LE(_MAX_FLOAT)
                    l.max_scale = reader.float32LE(_MAX_FLOAT)
                    l.slope_peak = reader.float32LE(_MAX_FLOAT)
                    l.slope_extent = reader.float32LE(_MAX_FLOAT)
                    l.min_elevation = reader.float32LE(_MAX_FLOAT)
                    l.max_elevation = reader.float32LE(_MAX_FLOAT)
                    l.min_alpha = reader.uint8()
                    l.flora = reader.ztstring()

                    l.tint_count = reader.uint32LE()
                    for k in range(l.tint_count):
                        t = Tint

                        t.value1 = reader.int32LE()
                        t.value2 = reader.uint32LE()

                        l.tints.append(t)
                    e.flora_part.layers.append(l)
                self.ecos.append(e)
