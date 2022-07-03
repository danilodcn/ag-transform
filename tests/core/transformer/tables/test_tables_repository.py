import os
import unittest

from tcc.core.domain.transformer.entities import Table, TableNameEnum
from tcc.core.infra.db.memory.transformer.table_repository import (
    TableRepositoryInMemory,
)

FILE_NAME = os.getcwd() + "/tests/core/json/tables.json"


class TestTablesRepositoryCreation(unittest.TestCase):
    def test_should_be_error_in_read_tables_without_load_tables(self):
        repository = TableRepositoryInMemory()
        with self.assertRaises(ValueError) as context:
            _ = repository.tables

        self.assertIn("repository.load_tables(name)", str(context.exception))

    def test_should_read_all_tables(self):
        repository = TableRepositoryInMemory()
        repository.load_tables(FILE_NAME)


class TestTablesRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TableRepositoryInMemory()
        self.repository.load_tables(FILE_NAME)

    def test_should_read_number_of_steps_table(self):
        table = self.repository.get(TableNameEnum.number_of_steps)
        self.assertIsInstance(table, Table)

    def test_should_read_core_dimensions_table(self):
        table = self.repository.get(TableNameEnum.core_dimensions)
        self.assertIsInstance(table, Table)

    def test_should_read_curve_BH_table(self):
        table = self.repository.get(TableNameEnum.curve_BH)
        self.assertIsInstance(table, Table)

    def test_should_read_insulation_type_constant_table(self):
        table = self.repository.get(TableNameEnum.insulation_type_constant)
        self.assertIsInstance(table, Table)

    def test_should_read_core_magnetic_loss_table(self):
        table = self.repository.get(TableNameEnum.core_magnetic_loss)
        self.assertIsInstance(table, Table)
