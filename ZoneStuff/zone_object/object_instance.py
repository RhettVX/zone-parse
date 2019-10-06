from dataclasses import dataclass, field

from ..util.special_types import Vector4
from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class ObjectInstance:
    position: Vector4 = field()
    rotation: Vector4 = field()
    scale: Vector4 = field()

    id: int = field()
    unk_byte0: int = field()
    unk_float3: float = field()

    def __init__(self, reader: BinaryStructReader):
        self.position = reader.vec4_float32LE(_MAX_FLOAT)
        self.rotation = reader.vec4_float32LE(_MAX_FLOAT)
        self.scale = reader.vec4_float32LE(_MAX_FLOAT)

        self.id = reader.uint32LE()
        self.unk_byte0 = reader.uint8()
        self.unk_float3 = reader.float32LE()

    def asdict(self):
        output = {
            'position': dict(self.position._asdict()),
            'rotation': dict(self.rotation._asdict()),
            'scale': dict(self.scale._asdict()),
            'id': self.id,
            'unk_byte0': self.unk_byte0,
            'unk_float3': self.unk_float3
        }
        return output
