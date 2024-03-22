import matplotlib.pyplot as plt

from readers.argreader import ArgReader

class GetPlot:
    def __init__(self, arg_file, run_list):
        self.argreader = ArgReader(arg_file)
        self.args = self.argreader.get_all()

        # We average our averages+bests over runs with different seeds.
        # You might get an error if you've recently changed your generations argument.
        self.average_of_averages = [0.0 for _ in range(self.args["generations"]+1)]
        self.average_of_bests = [0.0 for _ in range(self.args["generations"]+1)]

        for run in run_list:
            with open(f"output/run{run}/average_values.txt") as file:
                values = file.read().split("\n")
                values.remove("")
                for index, value in enumerate(values):
                    self.average_of_averages[index] += float(value)

            with open(f"output/run{run}/best_values.txt") as file:
                values = file.read().split("\n")
                values.remove("")
                for index, value in enumerate(values):
                    self.average_of_bests[index] += float(value)
        
        for i in range(self.args["generations"]+1):
            self.average_of_averages[i] /= len(run_list)
            self.average_of_bests[i] /= len(run_list)
    
    def generate_plot(self):
        plt.plot(self.average_of_bests, color="red", label="bests")
        plt.plot(self.average_of_averages, color="green", label="averages")
        plt.legend(loc="upper left")
        plt.xlabel("Generations")
        plt.ylabel("Fitness")
        plt.title("Bests and Averages on a Generations vs Fitness Plot")
        plt.savefig(f"plot.png")


if __name__ == "__main__":
    # This is the list of runs you want for the plot. ex. [0, 4, 23, 1, 9]
    # All the values from these runs will be averaged and plotted.
    getplot = GetPlot("args.txt", [0])
    getplot.generate_plot()