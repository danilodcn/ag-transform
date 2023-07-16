import os
import unittest

from tcc.core.domain.entities.transformer.table import Table, TableNameEnum
from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
    TableRepositoryInMemory,
)

FILE_NAME = os.getcwd() + "/tests/core/json/tables.json"


class TestTablesRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TableRepositoryInMemory(FILE_NAME)

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
