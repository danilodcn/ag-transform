# import json

from dataclasses import dataclass

from matplotlib import colors

from tcc.genetic_algorithm.population import Population

COLORS = list(colors.TABLEAU_COLORS.values())


@dataclass
class AGProps:
    n_generations: int
    n_population: int
    n_mutation: int
    current_generation: int = 0


class AG:
    def __init__(self, n_generations, n_population, n_mutation, constraints, tables):

        self.population = Population(n_population, constraints, tables)

        self.props = AGProps(
            n_generations=n_generations,
            n_population=n_population,
            n_mutation=n_mutation,
        )

        self.population.calcule_all()
        self.population.penalize()
        self.population.sort_pareto_ranks()
        self.population.calcule_fitness()

    def next(self):
        self.props.current_generation += 1

        # self.plot(True)
        print(f"Starting the generation {self.props.current_generation}")
        print("Starting crossover ...")
        self.population.crossover()
        self.population.calcule_all()
        self.population.penalize()
        self.population.sort_pareto_ranks()
        self.population.calcule_fitness()

        # self.plot(True)
        print("End crossover")
        print("Starting mutations ...")
        self.population.mutation(self.props.n_mutation)
        self.population.calcule_all()
        self.population.penalize()
        self.population.sort_pareto_ranks()
        self.population.calcule_fitness()

        # self.plot(True)
        print("End mutations")

        print("Populations clean")
        self.population = self.population.clean()

        self.population.calcule_all()
        self.population.penalize()
        self.population.sort_pareto_ranks()
        self.population.calcule_fitness()

        return True

    def get_data(self, key):
        return {
            "status": 1,
            "n_generations": self.props.n_generations,
            "current_generation": self.props.current_generation,
            "population": self.population.to_json(),
        }

    def run(self):
        for _ in range(self.props.n_generations):
            yield self.next()
