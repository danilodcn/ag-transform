import json, os
from unittest import TestCase
from app.named_tuple import NamedTuple


class TestNamedTuple(TestCase):
    def setUp(self) -> None:
        loc_file = os.path.join(os.getcwd(), "tests/json/tabelas.json")
        with open(loc_file) as file:
            self.json_tables = json.load(file)

    def test_create_named_tuple(self):
        tables = NamedTuple().convert_for_tuple(self.json_tables)

        is_named_tuple = isinstance(tables, tuple) and getattr(tables, "_fields", None) is not None
        has_name_table = "Tabela" in str(type(tables))

        self.assertTrue(is_named_tuple and has_name_table)
