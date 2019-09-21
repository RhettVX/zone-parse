from dataclasses import dataclass, field

from ..util.struct_reader import BinaryStructReader

_MAX_FLOAT = 6


@dataclass()
class RuntimeObject:
    file_name: str = field()
    render_distance: float = field()

    instance_count: int = field()

    def __init__(self, reader: BinaryStructReader):
        self.file_name = reader.ztstring()
        self.render_distance = reader.float32LE(_MAX_FLOAT)

        self.instance_count = reader.uint32LE()
