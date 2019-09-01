from struct_reader import *
from dataclasses import dataclass, field
from pathlib import Path


_MAGIC = b'ZONE'
_VERSION = 0x1


@dataclass
class Eco:
    name: str = field()
    color_nx_map: str = field()
    spec_ny_map: str = field()

    unk0: int = field()


@dataclass
class Zone1:
    name: str = field()
    path: Path = field()

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

            reader.seek(4, 1)
            test = reader.ztstring()
            pass


if __name__ == '__main__':
    vr_path = Path('/home/rhett/Desktop/Tutorial.zone')

    vr_zone = Zone1(vr_path)
    pass
