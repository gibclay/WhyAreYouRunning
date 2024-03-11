from gameitems.creature import Creature
from gameitems.direction import Direction

class Predator(Creature):
    def __init__(self, position: dict, map_size: dict, speed: int, direction: Direction):
        super().__init__(position, map_size, speed, direction)
        self.prey_eaten = 0
    def increment_prey_eaten(self):
        self.prey_eaten += 1
    def get_number_of_prey_eaten(self):
        return self.prey_eaten