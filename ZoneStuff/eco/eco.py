from dataclasses import dataclass, field
from typing import Dict

from .flora_part import FloraPart
from .texture_part import TexturePart
from ..util.struct_reader import BinaryStructReader


@dataclass()
class Eco:
    index: int = field()

    texture_part: TexturePart = field()
    flora_part: FloraPart = field()

    def __init__(self, reader: BinaryStructReader):
        self.index = reader.uint32LE()

        self.texture_part = TexturePart(reader)
        self.flora_part = FloraPart(reader)

    def asdict(self) -> Dict:
        output = {
            'index': self.index,
            'texture_part': self.texture_part.asdict(),
            'flora_part': self.flora_part.asdict()
        }
        return output
