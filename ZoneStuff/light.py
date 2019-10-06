from dataclasses import dataclass, field

from .util.special_types import Vector4
from .util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class Light:
    name: str = field()
    color_name: str = field()
    type: int = field()

    unk_float0: float = field()

    # Position
    position: Vector4 = field()

    def __init__(self, reader: BinaryStructReader):
        self.name = reader.ztstring()
        self.color_name = reader.ztstring()
        self.type = reader.uint8()

        self.unk_float0 = reader.float32LE(_MAX_FLOAT)

        self.position = reader.vec4_float32LE(_MAX_FLOAT)

    def asdict(self):
        output = {
            'name': self.name,
            'color_name': self.color_name,
            'type': self.type,
            'unk_float0': self.unk_float0,
            'postion': dict(self.position._asdict())
        }
        return output
