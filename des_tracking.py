class DesTracking:
    def __init__(self, transitions_fired_list=[], transitions_fired_cost=[]):
        self.transitions_fired_list = list(transitions_fired_list)
        self.transitions_fired_cost = list(transitions_fired_cost)

    def add_to_transitions_fired_list(self, transition_name, transitions_fired_cost):
        self.transitions_fired_list.append(transition_name)
        self.transitions_fired_cost.append(transitions_fired_cost)
