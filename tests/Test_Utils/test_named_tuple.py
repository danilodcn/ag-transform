import json
import os
from unittest import TestCase
from tcc.utils.named_tuple import NamedTuple


class TestNamedTuple(TestCase):
    def setUp(self) -> None:
        loc_file = os.path.join(os.getcwd(), "tests/json/tabelas.json")
        with open(loc_file) as file:
            self.json_tables = json.load(file)

    def test_create_named_tuple(self):
        tables = NamedTuple().convert_for_tuple(self.json_tables)

        bol = isinstance(tables, tuple)
        is_named_tuple = bol and getattr(tables, "_fields", None) is not None
        has_name_table = "Tabela" in str(type(tables))

        self.assertTrue(is_named_tuple and has_name_table)
