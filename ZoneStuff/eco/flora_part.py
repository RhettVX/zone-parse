from dataclasses import dataclass, field
from typing import List

from .layer import Layer
from ..struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class FloraPart:
    layer_count: int = field()
    layers: List[Layer] = field()

    def __init__(self, reader: BinaryStructReader):
        self.layer_count = reader.uint32LE()
        self.layers = []

        for _ in range(self.layer_count):
            self.layers.append(Layer(reader))
