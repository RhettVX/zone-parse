from dataclasses import dataclass, field

from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class ObjectInstance:
    translation_x: float = field()
    translation_y: float = field()
    translation_z: float = field()
    unk_float0: float = field()

    rotation_x: float = field()
    rotation_y: float = field()
    rotation_z: float = field()
    unk_float1: float = field()

    scale_x: float = field()
    scale_y: float = field()
    scale_z: float = field()
    unk_float2: float = field()

    id: int = field()
    unk_byte0: int = field()
    unk_float3: float = field()

    def __init__(self, reader: BinaryStructReader):
        # Translation
        self.translation_x = reader.float32LE(_MAX_FLOAT)
        self.translation_y = reader.float32LE(_MAX_FLOAT)
        self.translation_z = reader.float32LE(_MAX_FLOAT)
        self.unk_float0 = reader.float32LE(_MAX_FLOAT)

        # Rotation
        self.rotation_x = reader.float32LE(_MAX_FLOAT)
        self.rotation_y = reader.float32LE(_MAX_FLOAT)
        self.rotation_z = reader.float32LE(_MAX_FLOAT)
        self.unk_float1 = reader.float32LE(_MAX_FLOAT)

        # Scale
        self.scale_x = reader.float32LE(_MAX_FLOAT)
        self.scale_y = reader.float32LE(_MAX_FLOAT)
        self.scale_z = reader.float32LE(_MAX_FLOAT)
        self.unk_float2 = reader.float32LE(_MAX_FLOAT)

        self.id = reader.uint32LE()
        self.unk_byte0 = reader.uint8()
        self.unk_float3 = reader.float32LE()

    def asdict(self):
        output = {
            'translation': [
                self.translation_x,
                self.translation_y,
                self.translation_z,
                self.unk_float0
            ],
            'rotation': [
                self.rotation_x,
                self.rotation_y,
                self.rotation_z,
                self.unk_float1
            ],
            'scale': [
                self.scale_x,
                self.scale_y,
                self.scale_z,
                self.unk_float2
            ],
            'id': self.id,
            'unk_byte0': self.unk_byte0,
            'unk_float3': self.unk_float3
        }
        return output
