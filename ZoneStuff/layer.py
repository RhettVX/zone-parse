from collections import namedtuple
from dataclasses import dataclass, field
from typing import List

Tint = namedtuple('Tint', 'value1 value2')


@dataclass()
class Layer:
    density: float = field(default=0.0)
    min_scale: float = field(default=0.0)
    max_scale: float = field(default=0.0)
    slope_peak: float = field(default=0.0)
    slope_extent: float = field(default=0.0)
    min_elevation: float = field(default=0.0)
    max_elevation: float = field(default=0.0)
    min_alpha: int = field(default=0)
    flora: str = field(default='')

    tint_count: int = field(default=0)
    tints: List[Tint] = field(default_factory=list)
