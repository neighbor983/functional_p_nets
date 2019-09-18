from dataclasses import dataclass


@dataclass
class Arc:
    place: str
    arc_type: str
    weight: int = 1
