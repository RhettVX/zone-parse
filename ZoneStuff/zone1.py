from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from .eco import Eco
from .flora import Flora
from .struct_reader import BinaryStructReader

# from lxml import etree

_MAGIC = b'ZONE'
_VERSION = 0x1
_MAX_FLOAT = 6


@dataclass()
class Zone1:
    path: Path = field()
    name: str = field()

    # TODO
    offset_block: bytes = field(repr=False)

    quads_per_tile: int = field()
    tile_size: float = field()

    unk_int0: bytes = field(repr=False)

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

    # object_count: int = field()

    # TODO
    # def export_xml(self, name: str, outdir: Path):
    #     """Export .zone as xml.
    #
    #     :param name: Name of output file
    #     :param outdir: Path of output directory
    #     """
    #
    #     # export header
    #     root = etree.Element('Zone', version=str(_VERSION))
    #     etree.SubElement(root, 'bytes')
    #     print(etree.tostring(root, pretty_print=True).decode('utf8'))

    def __init__(self, path: Path):
        self.path = path
        self.name = self.path.stem

        with BinaryStructReader(self.path) as reader:
            assert reader.read(len(_MAGIC)) == _MAGIC, 'Invalid magic'
            assert reader.uint32LE() == _VERSION, 'Invalid version'
            self.offset_block_block = reader.read(24)

            self.quads_per_tile = reader.uint32LE()
            self.tile_size = reader.float32LE()

            self.unk_int0 = reader.read(4)

            self.verts_per_tile = reader.uint32LE()
            self.tiles_per_chunk = reader.uint32LE()

            self.start_x = reader.int32LE()
            self.start_y = reader.int32LE()
            self.chunks_x = reader.uint32LE()
            self.chunks_y = reader.uint32LE()

            self.eco_count = reader.uint32LE()
            self.ecos = []
            for _ in range(self.eco_count):
                # print(reader.tell())
                self.ecos.append(Eco(reader))

            return  # FIXME
            self.flora_count = reader.uint32LE()
            self.floras = []
            for _ in range(self.flora_count):
                self.floras.append(Flora(reader))

            # TODO: Handle invisible walls when we find some
            assert reader.uint32LE() == 0, 'There are invis walls here. Handle them'

            # TODO: Finish object notes
            print('END POS:', reader.tell())
