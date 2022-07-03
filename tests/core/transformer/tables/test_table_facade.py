import os
import unittest

from tcc.core.application.transformer.table_use_cases.table_facade import (
    TableFacade,
)
from tcc.core.domain.transformer.entities import Table, TableNameEnum
from tcc.core.infra.db.memory.transformer.table_repository import (
    TableRepositoryInMemory,
)

FILE_NAME = os.getcwd() + "/tests/core/json/tables.json"


class TestTableFacade(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = TableRepositoryInMemory()
        self.repository.load_tables(FILE_NAME)
        self.facade = TableFacade(table_repository=self.repository)

    def test_get_number_of_steps_from_facade(self):

        expected = 1
        calculated = self.facade.get_number_of_steps(area=2)
        error_message = "Para área de até 2 mm² o número de degraus deve ser 1"
        self.assertEqual(expected, calculated, error_message)

    def test_get_insulation_type_constant_from_facade(self):
        expected = 0.49
        calculated = self.facade.get_insulation_type_constant(
            type="seco", number_of_steps=3
        )
        error_message = "Erro inesperado!"
        self.assertEqual(expected, calculated, error_message)

    def test_get_core_dimensions_constant_from_facade(self):
        expected = (0.636, [0.707])
        calculated = self.facade.get_core_dimensions(number_of_steps=1)
        error_message = "Erro inesperado!"
        self.assertEqual(expected, calculated, error_message)

    def test_get_curve_BH_from_facade(self):
        expected = 240.3265 + 1e-5  # valor obtido através de outra simulação
        calculated = self.facade.get_curve_BH(B=1.75)
        error_message = "Erro inesperado!"
        self.assertAlmostEqual(expected, calculated, 4, error_message)

    def test_get_core_magnetic_loss_from_facade(self):
        expected = 1.665 + 1e-5  # valor obtido através de outra simulação
        calculated = self.facade.get_core_magnetic_loss(B=1.75)
        error_message = "Erro inesperado!"
        self.assertAlmostEqual(expected, calculated, 4, error_message)
