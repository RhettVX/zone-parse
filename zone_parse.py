from dataclasses import dataclass, field
from typing import List

from struct_reader import *

_MAGIC = b'ZONE'
_VERSION = 0x1
_MAX_FLOAT = 6


@dataclass
class Eco:
    name: str = field(default='')
    color_nx_map: str = field(default='')
    spec_blend_ny_map: str = field(default='')
    detail_repeat: int = field(default=0)
    blend_strength: float = field(default=0.0)
    spec_min: float = field(default=0.0)
    spec_max: float = field(default=0.0)
    spec_smoothness_min: float = field(default=0.0)
    spec_smoothness_max: float = field(default=0.0)
    physics_material: str = field(default='')

    unk0: int = field(default=0)


@dataclass
class Zone1:
    name: str = field()
    path: Path = field()
    ecos: List[Eco] = field()

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

    def __init__(self, path: Path):
        self.path = path
        self.name = path.stem

        with BinaryStructReader(self.path) as reader:
            assert reader.read(4) == _MAGIC, 'Invalid magic'
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
            for c in range(self.eco_count):
                eco = Eco()

                eco.unk0 = reader.uint32LE()
                eco.name = reader.ztstring()
                eco.color_nx_map = reader.ztstring()
                eco.spec_blend_ny_map = reader.ztstring()
                eco.detail_repeat = reader.uint32LE()
                eco.blend_strength = round(reader.float32LE(), _MAX_FLOAT)
                eco.spec_min = round(reader.float32LE(), _MAX_FLOAT)
                eco.spec_max = round(reader.float32LE(), _MAX_FLOAT)
                eco.spec_smoothness_min = round(reader.float32LE(), _MAX_FLOAT)
                eco.spec_smoothness_max = round(reader.float32LE(), _MAX_FLOAT)
                eco.physics_material = reader.ztstring()

                self.ecos.append(eco)
                break


if __name__ == '__main__':
    vr_path = Path('/home/rhett/Desktop/Tutorial.zone')

    vr_zone = Zone1(vr_path)
    pass
