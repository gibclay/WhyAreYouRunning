from types import MappingProxyType as ImmutableDict

from gameitems.direction import Direction

class Creature:
    def __init__(self, position: dict, map_size: dict, speed: int, direction: Direction):
        self.history = []
        self.list_of_functions = [self.move, self.turn_left, self.turn_right, self.is_there_adjacent_creature]
        self.size = {
            "x": map_size["x"],
            "y": map_size["y"],
        }
        self.position = {
            "x": position["x"],
            "y": position["y"],
        }
        self.speed = speed
        self.direction = direction
    def update_history(self):
        # All these are deep copies, so there should be no copying problems.
        self.history.append(ImmutableDict(
            {
                "x": self.position["x"],
                "y": self.position["y"],
                "direction": self.direction,
            }
        ))
    def move(self):
        self.update_history()
        if self.direction == Direction.up:
            if self.position["y"] > 0:
                self.position["y"] -= self.speed
        elif self.direction == Direction.down:
            if self.position["y"] < self.size["y"]:
                self.position["y"] += self.speed
        elif self.direction == Direction.left:
            if self.position["x"] > 0:
                self.position["x"] -= self.speed
        elif self.direction == Direction.right:
            if self.position["x"] < self.size["x"]:
                self.position["x"] += self.speed
    def turn_left(self):
        self.update_history()
        if self.direction == Direction.up:
            self.direction = Direction.left
        elif self.direction == Direction.left:
            self.direction = Direction.down
        elif self.direction == Direction.down:
            self.direction = Direction.right
        elif self.direction == Direction.right:
            self.direction = Direction.up
    def turn_right(self):
        self.update_history()
        if self.direction == Direction.up:
            self.direction = Direction.right
        elif self.direction == Direction.right:
            self.direction = Direction.down
        elif self.direction == Direction.down:
            self.direction = Direction.left
        elif self.direction == Direction.left:
            self.direction = Direction.up
    def is_there_adjacent_creature(self, creatures):
        self.update_history()
        # Adjacent means one square to the up, down, left, right, or any of the four diagonals (8 possible squares).
        x_diff = 0
        y_diff = 0
        for creature in creatures:
            x_diff = self.position["x"] - creature.position["x"]
            y_diff = self.position["y"] - creature.position["y"]

            if abs(x_diff) == 1 or abs(y_diff) == 1:
                return True
        return False

