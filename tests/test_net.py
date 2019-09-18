from arc import Arc
from net import Net
from place import Place
from transition import Transition
from des_tracking import DesTracking

from typing import Dict, List

t1 = Transition(
    name="aT1",
    rate=1,
    input=["p1->aT1"],
    output=["aT1->p2"],
    inhibit=["p2--aT1"],
    control_rate={"p1": 2},
    player_control="attacker",
    fire_cost=10,
)
transitions = [t1]

arcs = {}
a1 = Arc(place="p1", arc_type="input", weight=1)
arcs.update({"p1->aT1": a1})
a2 = Arc(place="p2", arc_type="output", weight=1)
arcs.update({"aT1->p2": a2})
a3 = Arc(place="p2", arc_type="inhibit", weight=1)
arcs.update({"p2--aT1": a3})

places = {}
p1 = Place(
    name="p1",
    marking=1,
    success_place=False,
    player_observable="attacker",
    control="attacker",
    visited=True,
)
places.update({"p1": p1})

p2 = Place(
    name="p2",
    marking=0,
    success_place=True,
    player_observable="attacker",
    control="attacker",
    visited=False,
)
places.update({"p2": p2})


def pick_first(list_of_enabled: List[Transition]):
    return list_of_enabled[0]


n1 = Net(
    transitions=transitions,
    arcs=arcs,
    places=places,
    determine_transition_to_fire=pick_first,
    des_tracking=DesTracking(),
)
enable_ts = n1.enabled_transitions()
new_net = n1.run_with_net_list()
print(len(new_net))
print(new_net[0].generate_list_of_places())
# new_net = new_net.step()
# new_net_enabled_ts = new_net.enabled_transitions()
# print(len(new_net_enabled_ts))
# print(len(new_net.marked_places()))
# print(enable_ts[0].name)
# print(len(n1.generate_list_of_places()))
# print(len(enable_ts))
