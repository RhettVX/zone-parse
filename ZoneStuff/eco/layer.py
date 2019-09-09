from collections import namedtuple
from dataclasses import dataclass, field
from typing import List

from ..struct_reader import BinaryStructReader

_MAX_FLOAT = 6
Tint = namedtuple('Tint', 'value1 value2')


@dataclass()
class Layer:
    density: float = field()
    min_scale: float = field()
    max_scale: float = field()
    slope_peak: float = field()
    slope_extent: float = field()
    min_elevation: float = field()
    max_elevation: float = field()
    min_alpha: int = field()
    flora: str = field()

    tint_count: int = field()
    tints: List[Tint] = field()

    def __init__(self, reader: BinaryStructReader):
        self.density = reader.float32LE(_MAX_FLOAT)
        self.min_scale = reader.float32LE(_MAX_FLOAT)
        self.max_scale = reader.float32LE(_MAX_FLOAT)
        self.slope_peak = reader.float32LE(_MAX_FLOAT)
        self.slope_extent = reader.float32LE(_MAX_FLOAT)
        self.min_elevation = reader.float32LE(_MAX_FLOAT)
        self.max_elevation = reader.float32LE(_MAX_FLOAT)
        self.min_alpha = reader.uint8()
        self.flora = reader.ztstring()

        self.tint_count = reader.uint32LE()
        self.tints = []
        for _ in range(self.tint_count):
            value1 = reader.int32LE()
            value2 = reader.uint32LE()

            self.tints.append(Tint(value1, value2))
