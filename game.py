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
        for _ in range(8):
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
            })

    def get_number_of_prey_eaten(self):
        return self.predator["prey eaten"]
    
    def if_same_spot(self, creature1, creature2):
        if creature1["x"] == creature2["x"] and creature1["y"] == creature2["y"]:
            return True
        return False

    def check_if_prey_eaten(self):
        if len(self.preys) < 1:
            raise GameOver
        for prey in self.preys:
            if self.if_same_spot(self.predator, prey):
                self.predator["prey eaten"] += 1
                self.preys.remove(prey)

    def move_prey(self):
        for prey in self.preys:
            match self.random_prey_move.randint(1, 2):
                case 1:
                    match prey["direction"]:
                        case Direction.up:
                            if prey["y"] > 0:
                                prey["y"] -= 1
                            return
                        case Direction.right:
                            if prey["x"] < self.map_size["x"]-1:
                                prey["x"] += 1
                            return
                        case Direction.down:
                            if prey["y"] < self.map_size["y"]-1:
                                prey["y"] += 1
                            return
                        case Direction.left:
                            if prey["x"] > 0:
                                prey["x"] -= 1
                            return
                case 2:
                    prey["direction"] = (Direction)(self.random_prey_direction.randint(0, 3))
                    return

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
        # This check is a huge bottleneck in speed.
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

    # This is for methods like if_in_front or if_nearby
    def if_then_else(self, condition, func1, func2):
        func1() if condition() else func2()

    def run(self, routine):
        self._reset()
        try:
            routine()
        except GameOver:
            return
        # print("%s %s" % (self.predator["x"], self.predator["y"]))