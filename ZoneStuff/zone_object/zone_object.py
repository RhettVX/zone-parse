from dataclasses import dataclass, field
from typing import List

from .object_instance import ObjectInstance
from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class ZoneObject:
    actor_definition: str = field()
    render_distance: float = field()

    instance_count: int = field()
    instances: List[ObjectInstance] = field()

    def __init__(self, reader: BinaryStructReader):
        self.actor_definition = reader.ztstring()
        self.render_distance = reader.float32LE(_MAX_FLOAT)

        self.instance_count = reader.uint32LE()
        self.instances = []

        for _ in range(self.instance_count):
            self.instances.append(ObjectInstance(reader))

    def asdict(self):
        output = {
            'actor_definition': self.actor_definition,
            'render_distance': self.render_distance,

            'instances': [x.asdict() for x in self.instances]
        }
        return output
