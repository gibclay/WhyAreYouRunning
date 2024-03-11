from deap import algorithms, base, creator, tools, gp
from numpy import mean, std, min, max

from operator import attrgetter
import random

from readers.argreader import ArgReader
from game import Game

class GPSystem:
    def __init__(self, arg_file):
        self.argreader = ArgReader(arg_file)
        self.args = self.argreader.get_all()
        self.ephemeral_random = random.Random(0)
        self.pset = gp.PrimitiveSet("MAIN", 0)
        self.toolbox = base.Toolbox()
        self.game = Game([100, 100])
        
        # Number represents arity of operator.
        self.pset.addPrimitive(self.game.predator_progn2, 2)
        self.pset.addPrimitive(self.game.predator_if_adjacent_creature, 2)
        self.pset.addPrimitive(self.game.predator_progn3, 3)
        self.pset.addTerminal(self.game.predator_move)
        self.pset.addTerminal(self.game.predator_turn_left)
        self.pset.addTerminal(self.game.predator_turn_right)

        # Positive weight represents a maximization problem.
        creator.create("FitnessMax", base.Fitness, weights=(1.0,))
        creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMax)

        self.toolbox.register(
            "expr",
            gp.genHalfAndHalf,
            pset=self.pset,
            min_=self.args["individual_min_depth"],
            max_=self.args["individual_max_depth"],
        )
        self.toolbox.register("individual", tools.initIterate, creator.Individual, self.toolbox.expr)
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)
        self.toolbox.register("compile", gp.compile, pset=self.pset)
        self.toolbox.register("evaluate", self.fitness_function)
        self.toolbox.register("select", tools.selTournament, tournsize=self.args["tournament_size"])
        self.toolbox.register("mate", gp.cxOnePoint)
        self.toolbox.register("expr_mut", gp.genFull, min_=self.args["mutation_min_depth"], max_=self.args["mutation_max_depth"])
        self.toolbox.register("mutate", gp.mutUniform, expr=self.toolbox.expr_mut, pset=self.pset)
        self.toolbox.decorate("mate", gp.staticLimit(key=attrgetter("height"), max_value=17))
        self.toolbox.decorate("mutate", gp.staticLimit(key=attrgetter("height"), max_value=17))

    def fitness_function(self, individual):
        routine = gp.compile(individual, self.pset)
        self.game.run(routine)
        return self.game.get_number_of_prey_eaten(),

    def run(self):
        random.seed(1)
        pop = self.toolbox.population(n=self.args["pop_size"])
        hof = tools.HallOfFame(self.args["hof_size"])

        # INITIALIZING STATISTICAL OUTPUT.
        stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
        stats_size = tools.Statistics(len)
        mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
        mstats.register("avg", mean)
        mstats.register("std", std)
        mstats.register("min", min)
        mstats.register("max", max)

        # THE GP SYSTEM FINALLY RUNS.
        pop, log = algorithms.eaSimple(
            pop, 
            self.toolbox, 
            cxpb=self.args["prob_crossover"], 
            mutpb=self.args["prob_mutation"],
            ngen=self.args["generations"],
            stats=mstats,
            halloffame=hof,
            verbose=True,
        )
        bestVals, avgVals = log.chapters["fitness"].select("min", "avg")            
        return pop, log, hof