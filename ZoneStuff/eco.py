from dataclasses import dataclass, field

from .flora_part import FloraPart
from .texture_part import TexturePart


@dataclass()
class Eco:
    texture_part: TexturePart = field(default_factory=TexturePart)
    flora_part: FloraPart = field(default_factory=FloraPart)
