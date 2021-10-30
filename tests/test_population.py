from unittest import TestCase
from app.genetic_algorithm.population import Population
import json


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

    def test_create_population(self):
        Population
