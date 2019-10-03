from dataclasses import dataclass, field
from typing import Dict

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

    def asdict(self) -> Dict:
        output = {
            'name': self.name,
            'color_nx_map': self.color_nx_map,
            'spec_blend_ny_map': self.spec_blend_ny_map,
            'detail_repeat': self.detail_repeat,
            'blend_strength': self.blend_strength,
            'spec_min': self.spec_min,
            'spec_max': self.spec_max,
            'spec_smoothness_min': self.spec_smoothness_min,
            'spec_smoothness_max': self.spec_smoothness_max,
            'physics_material': self.physics_material
        }
        return output
