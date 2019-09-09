from dataclasses import dataclass, field

from .struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class Flora:
    name: str = field()
    texture: str = field()
    model: str = field()

    unk0: bool = field()
    unk1: float = field()
    unk2: float = field()

    def __init__(self, reader: BinaryStructReader):
        self.name = reader.ztstring()
        self.texture = reader.ztstring()
        self.model = reader.ztstring()
        self.unk0 = reader.bool8()
        self.unk1 = reader.float32LE(_MAX_FLOAT)
        self.unk2 = reader.float32LE(_MAX_FLOAT)
