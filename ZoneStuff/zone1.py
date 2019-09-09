from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .eco import Eco
from .flora import Flora
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

    flora_count: int = field()
    floras: List[Flora] = field()

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
            for _ in range(self.eco_count):
                self.ecos.append(Eco(reader))

            self.flora_count = reader.uint32LE()
            self.floras = []
            for _ in range(self.flora_count):
                self.floras.append(Flora(reader))
