from functools import partial

from gameitems.direction import Direction
from gameitems.predator import Predator
from gameitems.prey import Prey

class Game:
    def __init__(self, map_size: tuple[int, int]):
        self.map_size = {
            "x": map_size[0],
            "y": map_size[1],
        }
        self.predator = Predator({"x": 0, "y": 0}, self.map_size, 1, Direction.down)
        self.preys = [
            Prey({"x": self.map_size["x"]-1, "y": self.map_size["y"]-1}, self.map_size, 1, Direction.up, 0),
            Prey({"x": 0, "y": self.map_size["y"]-1}, self.map_size, 1, Direction.up, 1),
            Prey({"x": self.map_size["x"]-1, "y": 0}, self.map_size, 1, Direction.up, 2),
        ]
    def _reset(self):
        self.predator = Predator({"x": 0, "y": 0}, self.map_size, 1, Direction.down)
        self.preys = [
            Prey({"x": self.map_size["x"]-1, "y": self.map_size["y"]-1}, self.map_size, 1, Direction.up, 0),
            Prey({"x": 0, "y": self.map_size["y"]-1}, self.map_size, 1, Direction.up, 1),
            Prey({"x": self.map_size["x"]-1, "y": 0}, self.map_size, 1, Direction.up, 2),
        ]
    def get_number_of_prey_eaten(self):
        return self.predator.get_number_of_prey_eaten()
    def prey_update(self):
        for prey in self.preys:
            prey.update()
    def check_if_prey_eaten(self):
        #print("Predator: %s, %s" % (self.predator.position["x"], self.predator.position["y"]))
        for count, prey in enumerate(self.preys):
            #print("Prey%s: %s, %s" % (count+1, prey.position["x"], prey.position["y"]))
            if self.predator.position["x"] == prey.position["x"] and self.predator.position["y"] == prey.position["y"]:
                self.predator.increment_prey_eaten()
                self.preys.remove(prey)
    def predator_move(self):
        self.predator.move()
        self.check_if_prey_eaten()
        self.prey_update()
    def predator_turn_left(self):
        self.predator.turn_left()
        self.check_if_prey_eaten()
        self.prey_update()
    def predator_turn_right(self):
        self.predator.turn_right()
        self.check_if_prey_eaten()
        self.prey_update()
    def if_then_else(self, condition, func1, func2):
        func1() if condition(self.preys) else func2()
    def predator_if_adjacent_creature(self, func1, func2):
        return partial(self.if_then_else, self.predator.is_there_adjacent_creature, func1, func2)
    def predator_progn(*args):
        for arg in args:
            # This might need to be fixed.
            if callable(arg):
                arg()
    def predator_progn2(self, func1, func2):
        return partial(self.predator_progn, func1, func2)
    def predator_progn3(self, func1, func2, func3):
        return partial(self.predator_progn, func1, func2, func3)
    def run(self, routine):
        self._reset()
        routine()