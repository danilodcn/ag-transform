from unittest import TestCase

# from timeit import timeit
from tcc.transformer import Transformer
import json


class TestTransformer(TestCase):
    def setUp(self):
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

    def test_create_transformer(self):
        transformer = Transformer(self.to_test_constraints, self.tables)
        transformer.tables

    def test_execute_run_in_transformer(self):
        transformer = Transformer(self.to_test_constraints, self.tables)
        PerdasT, Mativa = transformer.run(self.to_test_variables)

        PerdasT_, Mativa_ = self.to_test_result

        self.assertAlmostEqual(PerdasT, PerdasT_, delta=PerdasT_ * 1e-6)
        self.assertAlmostEqual(Mativa, Mativa_, delta=Mativa_ * 1e-6)

        def function_to_repeat():
            transformer.run(self.to_test_variables)

        """print("\nAqui")
        n = 1000
        duration = timeit(function_to_repeat, globals=globals(), number=n)
        print("Média = ", duration / n * 1e6, "ms")"""

        return

    def test_update_tables(self):
        transformer = Transformer(self.to_test_constraints, self.tables)
        key = list(self.tables.keys())[0]
        transformer.update_tables({key: 0})

        self.assertEqual(transformer.tables.tables.get(key), 0)

    def test_tipo_estrela(self):
        constraints = self.to_test_constraints
        constraints[0] = "estrela-delta"
        # import ipdb; ipdb.set_trace()

        transformer = Transformer(constraints, self.tables)
        transformer.run(self.to_test_variables)
