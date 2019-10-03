from dataclasses import dataclass

from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class ObjectInstance:
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

        self.unk_int0 = reader.uint32LE()
        self.unk_byte0 = reader.uint8()
        self.unk_float3 = reader.float32LE()
