from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from lxml.etree import tostring

from .eco import Eco
from .flora import Flora
from .runtime_object.runtime_object import RuntimeObject
from .util.struct_reader import BinaryStructReader
from .util.xml_binary import *

_MAGIC = b'ZONE'
_VERSION = 0x1
_MAX_FLOAT = 6


@dataclass()
class Zone1:
    path: Path = field()
    name: str = field()

    # TODO
    # offset_block: bytes = field(repr=False)
    offsets: dict

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

    object_count: int = field()
    runtime_objects: List[RuntimeObject] = field()

    # TODO
    def export_xml(self, name: str, outdir: Path):
        """Export .zone as xml.

        :param name: Name of output file
        :param outdir: Path of output directory
        """

        # export header
        root = Element('zone', version=str(_VERSION))

        section_header = element_section(root, 'header')
        element_int(section_header, self.quads_per_tile, 'quads_per_tile')
        element_float(section_header, self.tile_size, 'tile_size')
        element_bytes(section_header, self.unk_int0, 'unk_int0')
        element_int(section_header, self.verts_per_tile, 'verts_per_tile')
        element_int(section_header, self.tiles_per_chunk, 'tiles_per_chunk')
        element_int(section_header, self.start_x, 'start_x')
        element_int(section_header, self.start_y, 'start_y')
        element_int(section_header, self.chunks_x, 'chunks_x')
        element_int(section_header, self.chunks_y, 'chunks_y')

        section_ecos = element_section(root, 'ecos')
        for e in self.ecos:
            eco = SubElement(section_ecos, 'eco')

            # TexturePart
            section_texture_part = element_section(eco, 'texture_part')
            tp = e.texture_part
            element_string(section_texture_part, tp.name, 'name')
            element_string(section_texture_part, tp.color_nx_map, 'color_nx_map')
            element_string(section_texture_part, tp.spec_blend_ny_map, 'spec_blend_ny_map')
            element_int(section_texture_part, tp.detail_repeat, 'detail_repeat')
            element_float(section_texture_part, tp.blend_strength, 'blend_strength')
            element_float(section_texture_part, tp.spec_min, 'spec_min')
            element_float(section_texture_part, tp.spec_max, 'spec_max')
            element_float(section_texture_part, tp.spec_smoothness_min, 'spec_smoothness_min')
            element_float(section_texture_part, tp.spec_smoothness_max, 'spec_smoothness_max')
            element_string(section_texture_part, tp.physics_material, 'physics_material')

            # FloraPart
            section_flora_part = element_section(eco, 'flora_part')
            for l in e.flora_part.layers:
                layer = SubElement(section_flora_part, 'layer')

                element_float(layer, l.density, 'density')
                element_float(layer, l.min_scale, 'min_scale')
                element_float(layer, l.max_scale, 'max_scale')
                element_float(layer, l.slope_peak, 'slope_peak')
                element_float(layer, l.slope_extent, 'slope_extent')
                element_float(layer, l.min_elevation, 'min_elevation')
                element_float(layer, l.max_elevation, 'max_elevation')
                element_int(layer, l.min_alpha, 'min_alpha')
                element_string(layer, l.flora_name, 'flora_name')

                section_tints = element_section(layer, 'tints')
                for t in l.tints:
                    tint = SubElement(section_tints, 'tint')

                    element_rgba(tint, *t.color_rgba, 'color_rgba')
                    element_int(tint, t.strength, 'strength')

        # Floras
        section_floras = element_section(root, 'floras')
        for f in self.floras:
            flora = SubElement(section_floras, 'flora')

            element_string(flora, f.name, 'name')
            element_string(flora, f.texture, 'texture')
            element_string(flora, f.model, 'model')
            element_bool(flora, f.unk_bool0, 'unk_bool0')
            element_float(flora, f.unk_float0, 'unk_float0')
            element_float(flora, f.unk_float1, 'unk_float1')

        # InvisWalls  TODO: Skipped for now since this zone doesn't have any

        # RuntimeObjects

        # print(tostring(root, pretty_print=True).decode('utf8'))
        Path('zone_xml.xml').write_text(tostring(root, pretty_print=True).decode('utf8'))

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
            # self.offset_block_block = reader.read(24)

            self.quads_per_tile = reader.uint32LE()
            self.tile_size = reader.float32LE()

            self.unk_int0 = reader.read(4)

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
                # print(reader.tell())
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

            print('RUN_OBJECTS', reader.tell())
            self.object_count = reader.uint32LE()
            self.runtime_objects = []
            for _ in range(self.object_count):
                self.runtime_objects.append(RuntimeObject(reader))
                break

            # TODO: Finish object notes
            print('END POS:', reader.tell())
