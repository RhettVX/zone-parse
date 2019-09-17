from dataclasses import dataclass, field

from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class TexturePart:
    name: str = field()
    color_nx_map: str = field()
    spec_blend_ny_map: str = field()
    detail_repeat: int = field()
    blend_strength: float = field()
    spec_min: float = field()
    spec_max: float = field()
    spec_smoothness_min: float = field()
    spec_smoothness_max: float = field()
    physics_material: str = field()

    def __init__(self, reader: BinaryStructReader):
        self.name = reader.ztstring()
        self.color_nx_map = reader.ztstring()
        self.spec_blend_ny_map = reader.ztstring()
        self.detail_repeat = reader.uint32LE()
        self.blend_strength = reader.float32LE(_MAX_FLOAT)
        self.spec_min = reader.float32LE(_MAX_FLOAT)
        self.spec_max = reader.float32LE(_MAX_FLOAT)
        self.spec_smoothness_min = reader.float32LE(_MAX_FLOAT)
        self.spec_smoothness_max = reader.float32LE(_MAX_FLOAT)
        self.physics_material = reader.ztstring()
