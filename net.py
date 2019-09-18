import copy
from typing import Dict, List
from arc import Arc
from place import Place
from transition import Transition


class Net:
    def __init__(
            self,
            transitions: List[Transition],
            arcs: Dict[str, Arc],
            places: Dict[str, Place],
            determine_transition_to_fire,
            des_tracking,
            cost=[],
    ):
        self.transitions = transitions  # list of transitions
        self.arcs = arcs  # dictionary of arcs
        self.places = places  # dictionary of places
        self.determine_transition_to_fire = determine_transition_to_fire
        self.des_tracking = des_tracking
        self.cost = cost

    def run(self):
        new_net = copy.deepcopy(self)
        if new_net.empty_inputs():
            new_net = new_net.handle_empty_inputs()
        else:
            while len(new_net.enabled_transitions()) > 0:
                new_net = new_net.step()
        return new_net

    def run_with_net_list(self):
        new_net = copy.deepcopy(self)
        running_list = [new_net]
        print(running_list)
        if new_net.empty_inputs():
            running_list = new_net.handle_empty_inputs_list(running_list=running_list)
        else:
            print("here")
            while len(new_net.enabled_transitions()) > 0:
                print("inside while loop")
                new_net = new_net.step()
                print(new_net)
                running_list.append(new_net)
        return running_list

    def handle_empty_inputs(self):
        int_round_limit = get_round_limit()
        new_net = copy.deepcopy(self)
        for _ in range(int_round_limit):
            new_net = new_net.step()
        return new_net

    def handle_empty_inputs_list(self, running_list):
        int_round_limit = get_round_limit()
        new_net = copy.deepcopy(self)

        for _ in range(int_round_limit):
            new_net = new_net.step()
            running_list.append(new_net)
        return running_list

    def step(self):
        new_net = copy.deepcopy(self)
        enabled_transitions = new_net.enabled_transitions()
        if not enabled_transitions:
            return new_net
        transition = self.determine_transition_to_fire(enabled_transitions)
        self.track_transitions_fired(
            transition_name=transition.name,
            transitions_fired_cost=self.current_transition_cost(transition=transition),
        )
        return self.fire(transition=transition)

    def enabled_transitions(self) -> List[Transition]:
        return [
            trans
            for trans in self.transitions
            if (
                    self.all_input_arcs_enabled(trans)
                    and not (self.is_transition_inihibited(trans))
            )
        ]

    def all_input_arcs_enabled(self, transition: Transition) -> bool:
        if transition.input:
            return True
        input_holder = [
            x
            for x in transition.input
            if (self.places[self.arcs[x].place].marking >= self.arcs[x].weight)
        ]
        return len(input_holder) == len(transition.input)

    def fire(self, transition):
        inputs = transition.input
        outputs = transition.output
        new_places_dict = self.new_place_after_firing(
            arc_list=outputs,
            places_dict=self.new_place_after_firing(
                arc_list=inputs, places_dict=copy.deepcopy(self.places)
            ),
        )

        return Net(
            transitions=self.transitions,
            arcs=self.arcs,
            places=new_places_dict,
            determine_transition_to_fire=self.determine_transition_to_fire,
            des_tracking=self.des_tracking,
        )

    def new_place_after_firing(
            self, arc_list: Dict[str, Arc], places_dict: Dict[str, Place]
    ) -> Dict[str, Place]:
        for arc_name in arc_list:
            arc = self.arcs[arc_name]
            p1 = places_dict[arc.place]
            p2 = Place(
                name=p1.name,
                marking=new_marking_value(
                    arc_type=arc.arc_type, marking=p1.marking, weight=arc.weight
                ),
                success_place=p1.success_place,
                player_observable=p1.player_observable,
                control=p1.control,
                visited=True,
            )
            places_dict[p1.name] = p2
        return places_dict

    def generate_list_of_places(self) -> List[Place]:
        return [self.places[x] for x in self.places]

    def marked_places(self) -> List[Place]:
        places = self.generate_list_of_places()
        return [x for x in places if x.marking > 0]

    def is_transition_inihibited(self, transition: Transition) -> bool:
        inhibitors = transition.inhibit
        inhibited_arcs = [
            arc
            for arc in inhibitors
            if self.arcs[arc].weight <= self.places[self.arcs[arc].place].marking
        ]
        return len(inhibited_arcs) >= 1

    def visited_places(self) -> List[Place]:
        places = self.generate_list_of_places()
        return [x for x in places if x.visited]

    def empty_inputs(self) -> bool:
        return len([x for x in self.transitions if len(x.input) == 0]) > 0

    def track_transitions_fired(self, transition_name: str, transitions_fired_cost):
        self.des_tracking.add_to_transitions_fired_list(
            transition_name=transition_name,
            transitions_fired_cost=transitions_fired_cost,
        )
        return self.des_tracking.transitions_fired_list

    def current_transition_cost(self, transition: Transition) -> int:
        base = transition.fire_cost
        current = base
        for key in transition.control_rate:
            marking = self.places[key].marking
            if marking > 0:
                current += transition.control_rate[key]
        return current


def get_round_limit() -> int:
    while True:
        round_limit = input(
            "Atleast one of your transitions is missing input arcs to prevent an infinity loop how my rounds would "
            "you like to use: "
        )
        try:
            int_round_limit = int(round_limit)
        except ValueError:
            print("Error!, you did not input an integer. Please try again")
        else:
            break
    return int_round_limit


def new_marking_value(arc_type: str, marking: int, weight: int) -> int:
    if arc_type == "input":
        return marking - weight
    return marking + weight
