from dataclasses import dataclass, field

from ..util.special_types import Color4
from ..util.struct_reader import BinaryStructReader


@dataclass()
class Tint:
    color_rgba: Color4 = field()
    strength: int = field()

    def __init__(self, reader: BinaryStructReader):
        self.color_rgba = reader.col4_uint8()
        self.strength = reader.uint32LE()

    def asdict(self):
        output = {
            'color': dict(self.color_rgba._asdict()),
            'strength': self.strength
        }
        return output
