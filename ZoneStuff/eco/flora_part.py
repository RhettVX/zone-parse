from dataclasses import dataclass, field
from typing import List

from .layer import Layer


@dataclass()
class FloraPart:
    layer_count: int = field(default=0)
    layers: List[Layer] = field(default_factory=list)
