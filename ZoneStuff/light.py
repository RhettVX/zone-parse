from dataclasses import dataclass, field

from .util.special_types import Vector4, Color4
from .util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class Light:
    name: str = field()
    color_name: str = field()
    type: int = field()

    unk_float0: float = field()

    position: Vector4 = field()
    rotation: Vector4 = field()

    range_: float = field()
    inner_range: float = field()
    color: Color4 = field()

    unk_bytes0: bytes = field()
    unk_vec0: Vector4 = field()
    unk_string0: str = field()

    id: int = field()

    def __init__(self, reader: BinaryStructReader):
        self.name = reader.ztstring()
        self.color_name = reader.ztstring()
        self.type = reader.uint8()

        self.unk_float0 = reader.float32LE(_MAX_FLOAT)

        self.position = reader.vec4_float32LE(_MAX_FLOAT)
        self.rotation = reader.vec4_float32LE(_MAX_FLOAT)

        self.range_ = reader.float32LE(_MAX_FLOAT)
        self.inner_range = reader.float32LE(_MAX_FLOAT)
        self.color = reader.col4_uint8()

        self.unk_bytes0 = reader.read(5)
        self.unk_vec0 = reader.vec4_float32LE(_MAX_FLOAT)
        self.unk_string0 = reader.ztstring()

        self.id = reader.uint32LE()

    def asdict(self):
        output = {
            'name': self.name,
            'color_name': self.color_name,
            'type': self.type,
            'unk_float0': self.unk_float0,

            'position': dict(self.position._asdict()),
            'rotation': dict(self.rotation._asdict()),

            'range': self.range_,
            'inner_range': self.inner_range,
            'color': dict(self.color._asdict()),

            'unk_bytes0': ' '.join([f'{x:02x}' for x in self.unk_bytes0]),
            'unk_vec0': dict(self.unk_vec0._asdict()),
            'unk_string0': self.unk_string0,

            'id': self.id
        }
        return output
