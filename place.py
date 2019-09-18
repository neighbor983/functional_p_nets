from dataclasses import dataclass
from typing import Any


@dataclass
class Place:
    name: str
    marking: int
    success_place: Any
    player_observable: bool
    control: Any
    visited: bool = False


# def set_weight(self, new_weight):
#     return Place(name=self.name, marking=new_weight, success_place=self.success_place,
#                  player_observable=self.player_observable, control=self.control, visited=True)
