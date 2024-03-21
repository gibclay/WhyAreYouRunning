import os
import shutil

from direction import Direction

def direction_map(direction):
    if direction == Direction.up:
        return "up"
    elif direction == Direction.right:
        return "right"
    elif direction == Direction.down:
        return "down"
    elif direction == Direction.left:
        return "left"

class FileWriter:
    def __init__(self, game, args):
        self.game = game

        self.individual = 0
        self.POP_SIZE = args["pop_size"]

        self.generation = 0
        self.GEN_SIZE = args["generations"]

        if not (os.path.exists("output") and os.path.isdir("output")):
            os.makedirs("output")

        self.run = 0
        while os.path.exists(f"output/{self.run}"):
            self.run += 1
        os.makedirs(f"output/{self.run}")

        self.full_file_path = f"output/{self.run}/{self.generation}/{self.individual}"
        shutil.copyfile("args.txt", f"output/{self.run}/args.txt")

    def check_if_generation_changed(self):
        if self.generation >= self.GEN_SIZE:
            self.individual = 0
            self.generation += 1
            if not (os.path.exists(f"output/{self.generation}") and os.path.isdir(f"output/{self.generation}")):
                os.makedirs(f"output/{self.generation}")
            self.full_file_path = f"output/{self.run}/{self.generation}/{self.individual}"

    def write_individual(self):
        self.predator_history = self.game.predator["history"]
        self.prey_histories = [prey["history"] for prey in self.game.preys]

        if not (os.path.exists(self.full_file_path) and os.path.isdir(self.full_file_path)):
            os.makedirs(self.full_file_path)

        # Writing down their moves.
        # Do I want to write, for example, "down" instead of "Direction.down"?
        with open(f"{self.full_file_path}/predator.txt", "a") as file:
            for state in self.predator_history:
                file.write("%s %s %s\n" % (state["x"], state["y"], direction_map(state["direction"])))
        
        for index, prey_history in enumerate(self.prey_histories):
            with open(f"{self.full_file_path}/prey{index}.txt", "a") as file:
                for state in prey_history:
                    file.write("%s %s %s\n" % (state["x"], state["y"], direction_map(state["direction"])))

        self.individual += 1
        self.full_file_path = f"output/{self.run}/{self.generation}/{self.individual}"

        self.check_if_generation_changed()