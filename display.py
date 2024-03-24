import os
import time

from readers.argreader import ArgReader

class Display:
    def __init__(self, arg_file, run, gen, ind):
        self.run_var = run
        self.gen = gen
        self.ind = ind

        self.index = 0

        self.argreader = ArgReader(arg_file)
        self.args = self.argreader.get_all()

        self.height = self.args["map_height"]
        self.width = self.args["map_width"]

        self.individual_path = f"output/run{run}/gen{gen}/ind{ind}"
        self.predator_history = []
        self.prey_histories = []

        # Add predator history.
        with open(f"{self.individual_path}/predator.txt") as file:
            for line in file.read().split("\n"):
                parts = [part for part in line.split(" ")]
                if len(parts) == 3:
                    self.predator_history.append({
                        "x": int(parts[0]),
                        "y": int(parts[1]),
                        "direction": parts[2],
                    })

        # Add prey histories.
        prey_list = os.listdir(self.individual_path)
        prey_list.remove("predator.txt")
        
        for prey in prey_list:
            prey_history = []
            with open(f"{self.individual_path}/{prey}") as file:
                for line in file.read().split("\n"):
                    parts = [part for part in line.split(" ")]
                    if len(parts) == 4:
                        prey_history.append({
                            "x": int(parts[0]),
                            "y": int(parts[1]),
                            "direction": parts[2],
                            "is alive": bool(parts[3]),
                        })
            self.prey_histories.append(prey_history)
    
    def draw_frame(self, index):
        os.system("cls")
        print("Run %s Gen %s Ind %s" % (self.run_var, self.gen, self.ind))
        for h in range(self.height):
            for w in range(self.width):
                nobody_is_here = True

                if self.predator_history[index]["x"] == w and self.predator_history[index]["y"] == h:
                    match self.predator_history[index]["direction"]:
                        case "up":
                            print("^", end="")
                        case "right":
                            print(">", end="")
                        case "down":
                            print("v", end="")
                        case "left":
                            print("<", end="")
                    # print("P", end="")
                    nobody_is_here = False

                for prey_history in self.prey_histories:
                    if prey_history[index]["x"] == w and prey_history[index]["y"] == h:
                        if prey_history[index]["is alive"]:
                            print("o", end="")
                            nobody_is_here = False

                if nobody_is_here:
                    print("_", end="")
            print()
        time.sleep(1/30)

    def run(self):
        while True:
            try:
                self.draw_frame(self.index)
                self.index += 1
            except IndexError:
                return

if __name__ == "__main__":
    display = Display("args.txt", 5, 0, 0)
    display.run()