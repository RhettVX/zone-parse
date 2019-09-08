from dataclasses import dataclass, field


@dataclass()
class TexturePart:
    unk0: int = field(default=0, repr=False)

    name: str = field(default='')
    color_nx_map: str = field(default='')
    spec_blend_ny_map: str = field(default='')
    detail_repeat: int = field(default=0)
    blend_strength: float = field(default=0.0)
    spec_min: float = field(default=0.0)
    spec_max: float = field(default=0.0)
    spec_smoothness_min: float = field(default=0.0)
    spec_smoothness_max: float = field(default=0.0)
    physics_material: str = field(default='')
