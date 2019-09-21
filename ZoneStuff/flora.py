from dataclasses import dataclass, field

from .util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class Flora:
    name: str = field()
    texture: str = field()
    model: str = field()

    unk_bool0: bool = field()
    unk_float0: float = field()
    unk_float1: float = field()

    def __init__(self, reader: BinaryStructReader):
        self.name = reader.ztstring()
        self.texture = reader.ztstring()
        self.model = reader.ztstring()
        self.unk_bool0 = reader.bool8()
        self.unk_float0 = reader.float32LE(_MAX_FLOAT)
        self.unk_float1 = reader.float32LE(_MAX_FLOAT)
