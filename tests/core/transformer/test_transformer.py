# import json
# import unittest

# from tcc.core.application.registry.registry_type import RegistryType
# from tcc.core.application.transformer.runners.transformer_three_phase_runner import (
#     TransformerThreePhaseRunner,
# )
# from tcc.core.domain.entities.transformer.constraints import Constraint
# from tcc.core.domain.entities.transformer.transformer import Transformer
# from tcc.core.domain.entities.transformer.variable import Variable
# from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
#     TableRepositoryInMemory,
# )
# from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
#     VariationRepositoryInMemory,
# )
# from tcc.core.infra.registry.application_registry import ApplicationRegistry
# from tests.constants import TABLE_FILE_NAME, TRANSFORMER_FILE_NAME


# class TestCreatePopulation(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         variation_repository = VariationRepositoryInMemory()
#         table_repository = TableRepositoryInMemory(TABLE_FILE_NAME)

#         cls.registry = ApplicationRegistry()
#         cls.registry.provide(RegistryType.TABLE_REPOSITORY, table_repository)
#         cls.registry.provide(
#             RegistryType.VARIATION_REPOSITORY, variation_repository
#         )

#     def setUp(self) -> None:
#         with open(TRANSFORMER_FILE_NAME) as file:
#             transformer_data = json.load(file)
#             self.test_responses: dict[str, float] = transformer_data.get(
#                 "for_tests"
#             )
#             self.variables = Variable(**transformer_data.get("variables", {}))
#             self.constraints = Constraint(
#                 **transformer_data.get("constraints", {})
#             )

#         variation_repository: VariationRepositoryInMemory = (
#             self.registry.inject(RegistryType.VARIATION_REPOSITORY)
#         )

#         self.variations = variation_repository.get()
#         self.transformer = Transformer(
#             variables=self.variables,
#             constraints=self.constraints,
#             variations=self.variations,
#         )

#     def test_create_transformer(self):
#         self.assertIsInstance(self.transformer, Transformer)

#     def test_transformers_not_equal(self):
#         transformer01 = Transformer(
#             variables=self.variables,
#             constraints=self.constraints,
#             variations=self.variations,
#         )

#         transformer02 = Transformer(
#             variables=self.variables,
#             constraints=self.constraints,
#             variations=self.variations,
#         )

#         variables = self.variables.copy()
#         variables.kt = 0

#         transformer03 = Transformer(
#             variables=variables,
#             constraints=self.constraints,
#             variations=self.variations,
#         )
#         self.assertEqual(transformer01, transformer02)
#         self.assertNotEqual(transformer01, transformer03)

#     def test_get_voltages(self):
#         Vf1, Vf2 = self.transformer.get_voltages()

#         expected_Vf1 = self.test_responses.get("Vf1")
#         expected_Vf2 = self.test_responses.get("Vf2")

#         assert expected_Vf1 is not None
#         assert expected_Vf2 is not None

#         self.assertAlmostEqual(
#             first=Vf1,
#             second=expected_Vf1,
#             places=3,
#             msg="Erro na Vf1",
#         )
#         self.assertAlmostEqual(
#             first=Vf2,
#             second=expected_Vf2,
#             places=2,
#             msg="Erro na Vf2",
#         )

#     def test_run_transformer(self):
#         use_case = TransformerThreePhaseRunner(registry=self.registry)

#         PerdasT, Mativa = use_case.run(self.transformer)

#         expected_PerdasT = self.test_responses.get("PerdasT")
#         expected_Mativa = self.test_responses.get("Mativa")

#         self.assertAlmostEqual(
#             first=Mativa,
#             second=expected_Mativa,
#             places=3,
#             msg="Erro na Mativa",
#         )
#         self.assertAlmostEqual(
#             first=PerdasT,
#             second=expected_PerdasT,
#             places=2,
#             msg="Erro na PerdasT",
#         )
