from functools import partial
from copy import deepcopy

from direction import Direction
import random

def progn(*args):
        for arg in args:
            arg()

def prog2(func1, func2):
    return partial(progn, func1, func2)

def prog3(func1, func2, func3):
    return partial(progn, func1, func2, func3)

# This is for methods like if_prey_in_front or if_prey_nearby
def if_then_else(condition, func1, func2):
    func1() if condition() else func2()

class GameOver(Exception):
    pass

class Game:
    def __init__(self, args):
        self.random_prey_gen = random.Random(args["random_prey_gen"])
        self.random_prey_move = random.Random(args["random_prey_move"])
        self.random_prey_direction = random.Random(args["random_prey_direction"])
        self.map_size = {
            "x": args["map_width"],
            "y": args["map_height"],
        }
        self.predator = {
            "x": 0,
            "y": 0,
            "direction": Direction.down,
            "history": [],
            "prey eaten": 0,
        }
        
        self.preys = []
        for _ in range(args["number_of_prey"]):
            self.add_prey(
                self.random_prey_gen.randint(0, self.map_size["x"]-1), 
                self.random_prey_gen.randint(0, self.map_size["y"]-1),
                self.random_prey_gen.choice([Direction.up, Direction.right, Direction.down, Direction.left]),
            )

    def add_prey(self, x, y, direction):
        self.preys.append({
            "x": x,
            "y": y,
            "direction": direction,
            "history": [],
            "is alive": True,
        })
    
    def _reset(self):
        self.predator = {
            "x": 0,
            "y": 0,
            "direction": Direction.down,
            "history": [],
            "prey eaten": 0,
        }
        self.random = random.Random(0)
        self.preys = []
        for _ in range(8):
            self.add_prey(
                self.random_prey_gen.randint(0, self.map_size["x"]-1), 
                self.random_prey_gen.randint(0, self.map_size["y"]-1),
                self.random_prey_gen.choice([Direction.up, Direction.right, Direction.down, Direction.left]),
            )
    
    def log_history(self):
        self.predator["history"].append({
            "x": deepcopy(self.predator["x"]),
            "y": deepcopy(self.predator["y"]),
            "direction": deepcopy(self.predator["direction"]),
        })

        for prey in self.preys:
            prey["history"].append({
                "x": deepcopy(prey["x"]),
                "y": deepcopy(prey["y"]),
                "direction": deepcopy(prey["direction"]),
                "is alive": deepcopy(prey["is alive"])
            })

    def get_number_of_prey_eaten(self):
        return self.predator["prey eaten"]
    
    def if_same_spot(self, creature1, creature2):
        if creature1["x"] == creature2["x"] and creature1["y"] == creature2["y"]:
            return True
        return False

    def check_if_prey_eaten(self):
        all_prey_are_dead = True

        for prey in self.preys:
            if prey["is alive"]:
                all_prey_are_dead = False

        if all_prey_are_dead:
            raise GameOver
        
        for prey in self.preys:
            if prey["is alive"]:
                if self.if_same_spot(self.predator, prey):
                    prey["is alive"] = False
                    self.predator["prey eaten"] += 1

    def move_prey(self):
        for prey in self.preys:
            if prey["is alive"]:
                match self.random_prey_move.choice([1, 1, 1, 2]):
                    case 1:
                        match prey["direction"]:
                            case Direction.up:
                                if prey["y"] > 0:
                                    prey["y"] -= 1
                                continue
                            case Direction.right:
                                if prey["x"] < self.map_size["x"]-1:
                                    prey["x"] += 1
                                continue
                            case Direction.down:
                                if prey["y"] < self.map_size["y"]-1:
                                    prey["y"] += 1
                                continue
                            case Direction.left:
                                if prey["x"] > 0:
                                    prey["x"] -= 1
                                continue
                    case 2:
                        prey["direction"] = (Direction)((self.random_prey_direction.choice([1, -1]) + prey["direction"].value) % 4)
                        continue

    def move(self):
        self.move_prey()
        # Move forwards.
        creature = self.predator

        match creature["direction"]:
            case Direction.up:
                if creature["y"] > 0:
                    creature["y"] -= 1
                return
            case Direction.right:
                if creature["x"] < self.map_size["x"]-1:
                    creature["x"] += 1
                return
            case Direction.down:
                if creature["y"] < self.map_size["y"]-1:
                    creature["y"] += 1
                return
            case Direction.left:
                if creature["x"] > 0:
                    creature["x"] -= 1
        self.check_if_prey_eaten()
        self.log_history()

    def turn_left(self):
        self.move_prey()
        self.predator["direction"] = (Direction)((self.predator["direction"].value-1) % 4)
        self.log_history()

    def turn_right(self):
        self.move_prey()
        self.predator["direction"] = (Direction)((self.predator["direction"].value+1) % 4)
        self.log_history()

    def check_for_prey_in_a_direction(self, checking_direction_relative_to_predator):
        absolute_direction_of_the_prey = (self.predator["direction"].value + checking_direction_relative_to_predator.value) % 4
        absolute_direction_of_the_prey = (Direction)(absolute_direction_of_the_prey)

        if absolute_direction_of_the_prey == Direction.up:
            for prey in self.preys:
                if prey["y"] < self.predator["y"]:
                    return True
            return False
        elif absolute_direction_of_the_prey == Direction.right:
            for prey in self.preys:
                if prey["x"] > self.predator["x"]:
                    return True
            return False
        elif absolute_direction_of_the_prey == Direction.down:
            for prey in self.preys:
                if prey["y"] > self.predator["y"]:
                    return True
            return False
        elif absolute_direction_of_the_prey == Direction.left:
            for prey in self.preys:
                if prey["x"] < self.predator["x"]:
                    return True
            return False

    def is_there_something_in_front(self):
        return self.check_for_prey_in_a_direction(Direction.up)

    def is_there_something_to_the_left(self):
        return self.check_for_prey_in_a_direction(Direction.left)
    
    def is_there_something_to_the_right(self):
        return self.check_for_prey_in_a_direction(Direction.right)

    def if_prey_in_front(self, func1, func2):
        return partial(if_then_else, self.is_there_something_in_front, func1, func2)
    
    def if_prey_to_left(self, func1, func2):
        return partial(if_then_else, self.is_there_something_to_the_left, func1, func2)
    
    def if_prey_to_right(self, func1, func2):
        return partial(if_then_else, self.is_there_something_to_the_right, func1, func2)

    def run(self, routine):
        self._reset()
        try:
            routine()
        except GameOver:
            return