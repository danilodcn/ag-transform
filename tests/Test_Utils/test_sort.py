import json
from collections import OrderedDict
from unittest import TestCase

from tcc.genetic_algorithm.gene import Gene
from tcc.genetic_algorithm.population import Population


class TestSort(TestCase):
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

    def test_basic_sort(self):
        self.population.calcule_all()
        sorted = self.population.sort_values(
            by=["PerdasT", "Mativa"], ascending=[False, False]
        )
        sorted
        # import ipdb; ipdb.set_trace()
