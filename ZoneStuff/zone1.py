from dataclasses import dataclass, field
from json import dumps
from pathlib import Path
from typing import List

from .eco import Eco
from .flora import Flora
from .util.struct_reader import BinaryStructReader
from .zone_object.zone_object import ZoneObject

_MAGIC = b'ZONE'
_VERSION = 0x1
_MAX_FLOAT = 6


@dataclass()
class Zone1:
    path: Path = field()
    name: str = field()

    # TODO
    offsets: dict

    quads_per_tile: int = field()
    tile_size: float = field()
    tile_height: float = field()
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

    object_count: int = field()
    objects: List[ZoneObject] = field()

    def export_json(self, name: str, outdir: Path):
        """Exports a zone as json

        :param name: Name of output file
        :param outdir: Path of output directory
        """
        zone_dict = {
            'name': self.name,
            'version': _VERSION,
            'quads_per_tile': self.quads_per_tile,
            'tile_size': self.tile_size,
            'tile_height': self.tile_height,
            'verts_per_tile': self.verts_per_tile,
            'tiles_per_chunks': self.tiles_per_chunk,
            'start_x': self.start_x,
            'start_y': self.start_y,
            'chunks_x': self.chunks_x,
            'chunks_y': self.chunks_y,
            'ecos': [x.asdict() for x in self.ecos],
            'floras': [x.asdict() for x in self.floras],
            # TODO: InvisWalls
            'objects': [x.asdict() for x in self.objects]
        }

        with (outdir / name).open('w') as outfile:
            outfile.write(dumps(zone_dict, indent=2))

    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

        with BinaryStructReader(self.path) as reader:
            assert reader.read(len(_MAGIC)) == _MAGIC, 'Invalid magic'
            assert reader.uint32LE() == _VERSION, 'Invalid version'

            # Offset TODO
            # self.offsets = {
            #     'ecos': reader.uint32LE(),
            #     'floras': reader.uint32LE(),
            #     'invis_walls': reader.uint32LE()
            # }
            reader.seek(4 * 6, 1)

            self.quads_per_tile = reader.uint32LE()
            self.tile_size = reader.float32LE()
            self.tile_height = reader.float32LE()
            self.verts_per_tile = reader.uint32LE()
            self.tiles_per_chunk = reader.uint32LE()

            self.start_x = reader.int32LE()
            self.start_y = reader.int32LE()
            self.chunks_x = reader.uint32LE()
            self.chunks_y = reader.uint32LE()

            # Ecos
            print('ECOS', reader.tell())
            self.eco_count = reader.uint32LE()
            self.ecos = []
            for _ in range(self.eco_count):
                self.ecos.append(Eco(reader))

            # Floras
            print('FLORAS', reader.tell())
            self.flora_count = reader.uint32LE()
            self.floras = []
            for _ in range(self.flora_count):
                self.floras.append(Flora(reader))

            # TODO: Handle invisible walls when we find some
            print('INVIS_WALLS', reader.tell())
            assert reader.uint32LE() == 0, 'There are invis walls here. Handle them'

            # Objects
            self.object_count = reader.uint32LE()
            self.objects = []
            for _ in range(self.object_count):
                self.objects.append(ZoneObject(reader))

            # TODO: Finish object notes
            print('END POS:', reader.tell())
