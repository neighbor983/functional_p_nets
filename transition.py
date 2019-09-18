from typing import Dict, List


class Transition:
    def __init__(
            self,
            name: str,
            rate,
            input: List[str],
            output: List[str],
            inhibit: List[str],
            control_rate: Dict[str, int],
            player_control,
            fire_cost: int = 0,
    ):
        self.name = name
        self.rate = rate
        self.input = input
        self.output = set(output)
        self.inhibit = set(inhibit)
        self.control_rate = control_rate
        self.player_control = player_control
        self.fire_cost = fire_cost
