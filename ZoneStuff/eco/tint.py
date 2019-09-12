from dataclasses import dataclass, field
from typing import Tuple

from ..struct_reader import BinaryStructReader


@dataclass()
class Tint:
    color_rgba: Tuple[int, int, int, int] = field()
    strength: int = field()

    def __init__(self, reader: BinaryStructReader):
        r = reader.uint8()
        g = reader.uint8()
        b = reader.uint8()
        a = reader.uint8()

        self.color_rgba = (r, g, b, a)
        self.strength = reader.uint32LE()
