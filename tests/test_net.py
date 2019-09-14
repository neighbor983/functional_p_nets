from arc import Arc
from net import Net
from place import Place
from transition import Transition

t1 = Transition(name="aT1", rate=1, input=["p1->aT1"], output=("aT1->p2"), inhibit=(""), control_rate=0,
                player_control="attacker", fire_cost=0)
transitions = [t1]

arcs = {}
a1 = Arc(place="p1", type="input", weight=1)
arcs.update({"p1->aT1": a1})
a2 = Arc(place="p2", type="output", weight=1)
arcs.update({"aT1->p2": a2})

places = {}
p1 = Place(name="p1", marking=1, success_place=False, player_observable="attacker", control="attacker",
           visited=True)
places.update({"p1": p1})

p2 = Place(name="p2", marking=0, success_place=True, player_observable="attacker", control="attacker", visited=False)
places.update({"p2": p2})

n1 = Net(transitions=transitions, arcs=arcs, places=places, determine_transition_to_fire=0, des_tracking=0)
enable_ts = n1.enabled_transitions()
print(enable_ts[0].name)
print(len(n1.generate_list_of_places()))
# print(len(enable_ts))