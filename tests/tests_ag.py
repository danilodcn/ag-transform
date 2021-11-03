import json
# import numpy as np

from collections import OrderedDict
from unittest import TestCase
from app.genetic_algorithm.ag import AG

# import pandas as pd
from app.genetic_algorithm.gene import Gene
# from app.genetic_algorithm.population import Population
# from app.utils.plot import Plot, plt

# from app.utils.sort import is_dominated


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

        variations = OrderedDict({
            "Jbt": (1.2, 1.4),
            "Jat": (1.4, 1.6),
            "Bm": (1.5, 1.6),
            "Ksw": (6, 7),
            "kt": (0.45, 0.55),
            "Rjan": (3.4, 3.6),
            "rel": (1.1, 1.2),
            })

        gene = Gene()
        gene.variations = variations

        self.n_population = 30
        self.n_generations = 10

        self.ag = AG(
            self.n_generations,
            self.n_population,
            int(self.n_population / 1.5),
            self.to_test_constraints,
            self.tables
        )

    def test_basic(self):
        # self.ag.run()
        # import ipdb; ipdb.set_trace()
        # self.ag.plot(True)
        ...

    def test_clean_population(self):
        self.ag.population.calcule_all()
        self.ag.population.penalize()
        self.ag.population.sort_pareto_ranks()
        self.ag.population.calcule_fitness()

        self.ag.population.crossover()
        self.ag.population.calcule_all()
        self.ag.population.penalize()
        self.ag.population.sort_pareto_ranks()
        self.ag.population.calcule_fitness()

        # self.ag.plot(False)
        # import ipdb; ipdb.set_trace()

        # self.ag.population = self.ag.population.clean()
        # self.ag.plot(False)

    def test_run_server(self):
        # self.ag.serve()
        ...
