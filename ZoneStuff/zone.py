from dataclasses import dataclass, field
from json import dumps
from pathlib import Path
from typing import List, Dict

from .eco import Eco
from .flora import Flora
from .light import Light
from .util.struct_reader import BinaryStructReader
from .zone_object.zone_object import ZoneObject

_MAGIC = b'ZONE'
# _VERSION = 0x1
_MAX_FLOAT = 6


@dataclass()
class Zone:
    path: Path = field()
    name: str = field()

    magic: bytes = field()
    version: int = field()
    offsets: Dict[str, int] = field()

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

    light_count: int = field()
    lights: List[Light] = field()

    unknowns: bytes = field()

    def export_json(self, name: str, outdir: Path):
        """Exports a zone as json

        :param name: Name of output file
        :param outdir: Path of output directory
        """
        zone_dict = {
            'magic': ' '.join([f'{x:02x}' for x in self.magic]),
            'name': self.name,
            'version': self.version,
            'offsets': self.offsets,
            'quads_per_tile': self.quads_per_tile,
            'tile_size': self.tile_size,
            'tile_height': self.tile_height,
            'verts_per_tile': self.verts_per_tile,
            'tiles_per_chunks': self.tiles_per_chunk,
            'start_x': self.start_x,
            'start_y': self.start_y,
            'chunks_x': self.chunks_x,
            'chunks_y': self.chunks_y,
            'eco_count': self.eco_count,
            'ecos': [x.asdict() for x in self.ecos],
            'flora_count': self.flora_count,
            'floras': [x.asdict() for x in self.floras],
            # TODO: InvisWalls
            'object_count': self.object_count,
            'objects': [x.asdict() for x in self.objects],
            'light_count': self.light_count,
            'lights': [x.asdict() for x in self.lights],
            'unknowns': ' '.join([f'{x:02}' for x in self.unknowns])
        }

        with (outdir / name).open('w') as outfile:
            outfile.write(dumps(zone_dict, indent=2))

    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

        with BinaryStructReader(self.path) as reader:
            self.magic = reader.read(len(_MAGIC))
            assert self.magic == _MAGIC, 'Invalid magic'

            self.version = reader.uint32LE()
            print(f'VERSION:\t{self.version}')

            # Offsets
            self.offsets = {
                'ecos': reader.uint32LE(),
                'floras': reader.uint32LE(),
                'invis_walls': reader.uint32LE(),
                'objects': reader.uint32LE(),
                'lights': reader.uint32LE(),
                'unknowns': reader.uint32LE()
            }

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
            self.eco_count = reader.uint32LE()
            self.ecos = []
            for _ in range(self.eco_count):
                self.ecos.append(Eco(reader))

            # Floras
            self.flora_count = reader.uint32LE()
            self.floras = []
            for _ in range(self.flora_count):
                self.floras.append(Flora(reader))

            # TODO: Handle invisible walls when we find some
            assert reader.uint32LE() == 0, 'There are invis walls here. Handle them'

            # Objects
            self.object_count = reader.uint32LE()
            self.objects = []
            for _ in range(self.object_count):
                self.objects.append(ZoneObject(reader))

            # Lights
            self.light_count = reader.uint32LE()
            self.lights = []
            for _ in range(self.light_count):
                self.lights.append(Light(reader))

            # Unknown
            self.unknowns = reader.read()
