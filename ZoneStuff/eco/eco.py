from dataclasses import dataclass, field

from .flora_part import FloraPart
from .texture_part import TexturePart
from ..struct_reader import BinaryStructReader


@dataclass()
class Eco:
    texture_part: TexturePart = field()
    flora_part: FloraPart = field()

    def __init__(self, reader: BinaryStructReader):
        self.texture_part = TexturePart(reader)
        self.flora_part = FloraPart(reader)
