import json
import os
import unittest

from tcc.core.application.transformer.run_transformer_use_case import (
    RunTransformerUseCase,
)
from tcc.core.domain.entities.transformer.constraints import Constraint
from tcc.core.domain.entities.transformer.transformer import Transformer
from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
    TableRepositoryInMemory,
)
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
    VariationRepositoryInMemory,
)
from tests.constants import *


class TestCreatePopulation(unittest.TestCase):
    def setUp(self) -> None:
        self.variation_repository = VariationRepositoryInMemory()
        self.table_repository = TableRepositoryInMemory()
        self.table_repository.load_tables(TABLE_FILE_NAME)

        with open(TRANSFORMER_FILE_NAME) as file:
            transformer_data = json.load(file)
            self.test_responses: dict[str, float] = transformer_data.get(
                "for_tests"
            )
            self.variables = Variable(**transformer_data.get("variables", {}))
            self.constraints = Constraint(
                **transformer_data.get("constraints", {})
            )

        self.variations = self.variation_repository.get()
        self.transformer = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=self.variations,
        )

    def test_create_transformer(self):
        self.assertIsInstance(self.transformer, Transformer)

    def test_transformers_not_equal(self):
        transformer01 = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=self.variations,
        )

        transformer02 = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=self.variations,
        )

        variables = self.variables.copy()
        variables.kt = 0

        transformer03 = Transformer(
            variables=variables,
            constraints=self.constraints,
            variations=self.variations,
        )
        self.assertEqual(transformer01, transformer02)
        self.assertNotEqual(transformer01, transformer03)

    def test_get_voltages(self):
        Vf1, Vf2 = self.transformer.get_voltages()

        expected_Vf1 = self.test_responses.get("Vf1")
        expected_Vf2 = self.test_responses.get("Vf2")

        assert expected_Vf1 is not None
        assert expected_Vf2 is not None

        self.assertAlmostEqual(
            first=Vf1,
            second=expected_Vf1,
            places=3,
            msg="Erro na Vf1",
        )
        self.assertAlmostEqual(
            first=Vf2,
            second=expected_Vf2,
            places=2,
            msg="Erro na Vf2",
        )

    def test_run_transformer(self):
        use_case = RunTransformerUseCase(
            table_repository=self.table_repository
        )

        PerdasT, Mativa = use_case.execute(self.transformer)

        expected_PerdasT = self.test_responses.get("PerdasT")
        expected_Mativa = self.test_responses.get("Mativa")

        self.assertAlmostEqual(
            first=Mativa,
            second=expected_Mativa,
            places=3,
            msg="Erro na Mativa",
        )
        self.assertAlmostEqual(
            first=PerdasT,
            second=expected_PerdasT,
            places=2,
            msg="Erro na PerdasT",
        )
