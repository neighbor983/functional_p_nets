class Place:
    def __init__(self, name, marking, success_place, player_observable, control, visited=False):
        self.name = name
        self.marking = marking
        self.success_place = success_place
        self.player_observable = player_observable
        self.control = control
        self.visited = visited

# def set_weight(self, new_weight):
#     return Place(name=self.name, marking=new_weight, success_place=self.success_place,
#                  player_observable=self.player_observable, control=self.control, visited=True)
