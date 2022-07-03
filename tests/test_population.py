import json
from collections import OrderedDict
from unittest import TestCase

# import pandas as pd
from tcc.genetic_algorithm.gene import Gene
from tcc.genetic_algorithm.population import Population
from tcc.utils.plot import Plot, plt
from tcc.utils.sort import is_dominated

# import numpy as np


class TestPopulation(TestCase):
    def setUp(self) -> None:
        json_test_trafo_file_name = "tests/json/data_trafo.json"
        with open(json_test_trafo_file_name) as file:
            json_test_trafo = json.load(file)

        to_test = list(json_test_trafo[0].values())
        self.to_test_variables = to_test[0]
        self.to_test_constraints = to_test[1:-2]
        self.to_test_result = to_test[-2:]

        tables_file_name = "tests/json/tabelas.json"
        with open(tables_file_name) as file:
            self.tables = json.load(file)
        # import ipdb; ipdb.set_trace()

        variations = OrderedDict(
            {
                "Jbt": (1.2, 1.4),
                "Jat": (1.4, 1.6),
                "Bm": (1.5, 1.6),
                "Ksw": (6, 7),
                "kt": (0.45, 0.55),
                "Rjan": (3.4, 3.6),
                "rel": (1.1, 1.2),
            }
        )

        gene = Gene()
        gene.variations = variations

        self.n_population = 30

        self.population = Population(
            self.n_population, self.to_test_constraints, self.tables, data=[]
        )
        self.x = 0

    def plot(self):
        plot = Plot(self.population)
        plot.plot(self.population)
        plot.plot_with_rank()

    def test_calcule_all(self):
        self.population.calcule_all()
        # plot(self.population)
        sorted = self.population.sort_values(
            by=["PerdasT", "Mativa"], ascending=[False, False]
        ).index
        # plot(self.population)
        sorted
        # import ipdb; ipdb.set_trace()

    def test_sort_population_with_pareto_ranks(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        self.plot()
        # plt.show()
        # from IPython import embed
        # embed()
        # %timeit self.population.sort_pareto_ranks()
        # import ipdb; ipdb.set_trace()

    def test_is_dominated(self):
        gene1 = (40, 50)
        gene2 = (46, 56)
        gene3 = (36, 60)

        self.assertTrue(not is_dominated(gene1, gene2))
        self.assertTrue(not is_dominated(gene1, gene3))
        self.assertTrue(not is_dominated(gene2, gene3))
        self.assertTrue(is_dominated(gene2, gene1))
        self.assertTrue(not is_dominated(gene3, gene1))
        self.assertTrue(not is_dominated(gene3, gene2))

    def test_crowding_distance(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        self.population.calculate_crowding_distance()

    def test_calcule_fitness(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        self.population.calcule_fitness()
        # print(self.population)
        self.plot()
        plt.show()

    def test_penalize(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        Plot(self.population).plot_with_rank("Antes da penalização")

        # import ipdb; ipdb.set_trace()
        self.population.penalize()

        self.population.sort_pareto_ranks()
        Plot(self.population).plot_with_rank(
            "Depois da penalização", penalize=True
        )

        plt.show()
        # import ipdb; ipdb.set_trace()

    def test_add_gene(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        self.population.penalize()
        self.population.sort_pareto_ranks()
        gene = Gene()

        self.population.add_gene(gene)
        n = self.population.index.__len__() - 1
        assertion = gene == self.population.loc[n]
        assert assertion.all()
        # import ipdb; ipdb.set_trace()

    def test_crossover(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()
        # Plot(self.population).plot_with_rank("Antes da penalização")
        Plot(self.population).plot_with_rank(
            "Antes do Crossover com penalização", penalize=True
        )
        # import ipdb; ipdb.set_trace()
        self.population.calcule_fitness()
        self.population.crossover()
        self.population.calcule_all()

        self.population.penalize()

        self.population.sort_pareto_ranks()
        # self.population.calcule_fitness()
        Plot(self.population).plot_with_rank(
            "Após Crossover com penalização", penalize=True
        )
        Plot(self.population).plot(self.population)
        # import ipdb; ipdb.set_trace()
        plt.show()

    def test_mutation(self):
        self.population.calcule_all()
        self.population.sort_pareto_ranks()

        Plot(self.population).plot_with_rank(
            "Antes do Crossover com penalização", penalize=True
        )

        self.population.calcule_fitness()
        self.population.crossover()
        self.population.calcule_all()

        self.population.penalize()

        self.population.sort_pareto_ranks()
        # self.population.calcule_fitness()
        Plot(self.population).plot_with_rank(
            "Após Crossover com penalização", penalize=True
        )
        self.population.calcule_fitness()
        self.population.mutation(20)
        self.population.calcule_all()

        self.population.penalize()

        self.population.sort_pareto_ranks()
        Plot(self.population).plot_with_rank(
            "Após mutação com penalização", penalize=True
        )
