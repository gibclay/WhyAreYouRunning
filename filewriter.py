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

        if not (os.path.exists("output") and os.path.isdir("output")):
            os.makedirs("output")

        self.run = 0
        while os.path.exists(f"output/run{self.run}"):
            self.run += 1
        os.makedirs(f"output/run{self.run}")

        shutil.copy("args.txt", f"output/run{self.run}")

        os.makedirs(f"output/run{self.run}/gen{self.generation}")
        self.individual_path = f"output/run{self.run}/gen{self.generation}/ind{self.individual}"
        os.makedirs(self.individual_path)
    
    def check_if_next_generation(self):
        if self.individual > self.POP_SIZE-1:
            self.individual = 0
            self.generation += 1
            os.makedirs(f"output/run{self.run}/gen{self.generation}")
            self.individual_path = f"output/run{self.run}/gen{self.generation}/ind{self.individual}"
            os.makedirs(self.individual_path)
            return True

    def write_individual(self):
        with open(f"{self.individual_path}/predator.txt", "a") as file:
            for state in self.game.predator["history"]:
                file.write("%s %s %s\n" % (state["x"], state["y"], direction_map(state["direction"])))
        
        for index, prey in enumerate(self.game.preys):
            with open(f"{self.individual_path}/prey{index}.txt", "a") as file:
                for state in prey["history"]:
                    file.write("%s %s %s %s\n" % (state["x"], state["y"], direction_map(state["direction"]), state["is alive"]))
        
        self.individual += 1
        if self.check_if_next_generation():
            return
        else:
            self.individual_path = f"output/run{self.run}/gen{self.generation}/ind{self.individual}"
            os.makedirs(self.individual_path)
    
    def write_averages_and_bests(self, best_values, average_values):
        with open(f"output/run{self.run}/best_values.txt", "a") as file:
            for value in best_values:
                file.write("%s\n" % value)

        with open(f"output/run{self.run}/average_values.txt", "a") as file:
            for value in average_values:
                file.write("%s\n" % value)

    def write_hall_of_famers(self, hall_of_famers):
        os.makedirs(f"output/run{self.run}/hall_of_famers")
        for index, hall_of_famer in enumerate(hall_of_famers):
            with open(f"output/run{self.run}/hall_of_famers/{index}.txt", "a") as file:
                file.write(str(hall_of_famer))