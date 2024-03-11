from random import Random

from gameitems.creature import Creature
from gameitems.direction import Direction

class Prey(Creature):
    def __init__(self, position: dict, map_size: dict, speed: int, direction: Direction, seed: int):
        super().__init__(position, map_size, speed, direction)
        self.random = Random(seed)
        self.movement_options = [self.move, self.turn_left, self.turn_right]
    def update(self):
        self.random.choice(self.movement_options)()