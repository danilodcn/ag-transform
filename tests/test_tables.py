import json, os
from unittest import TestCase
from app.utils.tables import Tables

class TestTablesBasic(TestCase):

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

    def test_create_tables(self):
        tables = Tables(self.tables)

    def test_curva_BH(self):
        Bm, By = 1.5794831416883455, 1.3695543468743003
        atc, atj = 58.143199384244134, 32.490841038777084

        tables = Tables(self.tables)
        self.assertAlmostEqual(tables.curva_BH(Bm), atc)
        self.assertAlmostEqual(tables.curva_BH(By), atj)

    def test_errors(self):
        tables = Tables(self.tables)

        with self.assertRaises(ValueError) as context:
            tables.numero_degraus(203)
            tables.numero_degraus(-1)

        self.assertTrue("A a area nao pode" in str(context.exception))

        degraus = tables.numero_degraus(2.99)
        self.assertEqual(1, degraus)

        with self.assertRaises(KeyError) as context:
            tables.constante_tipo_isolacao("coisa", 6)

        