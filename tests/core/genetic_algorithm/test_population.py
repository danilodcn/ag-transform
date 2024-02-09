# import json
# import unittest

# import numpy as np

# from tcc.core.application.registry.registry_type import RegistryType
# from tcc.core.application.transformer.runners.transformer_three_phase_runner import (  # noqa
#     TransformerThreePhaseRunner,
# )
# from tcc.core.domain.entities.genetic_algorithm.gene.gene import Gene
# from tcc.core.domain.entities.genetic_algorithm.population.population_builder import (  # noqa
#     Population,
#     PopulationBuilder,
#     PopulationProps,
# )
# from tcc.core.domain.entities.transformer.constraints import Constraint
# from tcc.core.domain.entities.transformer.transformer import Transformer
# from tcc.core.domain.entities.transformer.variable import Variable
# from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
#     TableRepositoryInMemory,
# )

# from tcc.core.infra.registry.application_registry import ApplicationRegistry
# from tests.constants import TABLE_FILE_NAME, TRANSFORMER_FILE_NAME


# class TestCreatePopulation(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         cls.variation_repository = VariationRepositoryInMemory()
#         cls.table_repository = TableRepositoryInMemory(TABLE_FILE_NAME)

#         registry = ApplicationRegistry()
#         registry.provide(RegistryType.TABLE_REPOSITORY, cls.table_repository)
#         registry.provide(
#             RegistryType.VARIATION_REPOSITORY, cls.variation_repository
#         )
#         registry.provide(
#             RegistryType.TRANSFORMER_RUNNER,
#             TransformerThreePhaseRunner(
#                 registry=registry,
#             ),
#         )
#         cls.registry = registry
#         with open(TRANSFORMER_FILE_NAME) as file:
#             transformer_data = json.load(file)
#             cls.variables = Variable(**transformer_data.get("variables", {}))
#             cls.constraints = Constraint(
#                 **transformer_data.get("constraints", {})
#             )

#         cls.variations = cls.variation_repository.get()
#         cls.transformer = Transformer(
#             variables=cls.variables,
#             constraints=cls.constraints,
#             variations=cls.variations,
#         )
#         cls.props = PopulationProps(
#             n_population=10,
#             disturbance_rate=0.3,
#             crossover_probability=0.4,
#             penalize_constant=1.4,
#             niche_radius=0.1,
#             crossover_population_frac=0.4,
#             mutation_population_frac=0.8,
#         )

#     def test_create_population(self):
#         population = PopulationBuilder.build(
#             props=self.props, variations=self.variations, random_create=True
#         )

#         self.assertIsInstance(population, Population)

#     def test_generate_data(self):
#         population = PopulationBuilder.build(
#             props=self.props, variations=self.variations, random_create=True
#         )

#         self.assertIsNotNone(population.data)

#     def test_generate_genes(self):
#         population = PopulationBuilder.build(
#             props=self.props, variations=self.variations, random_create=True
#         )

#         self.assertIsNotNone(population.data)
#         self.assertEqual(len(population.genes), population.props.n_population)
#         for gene in population.genes:
#             self.assertIsInstance(gene, Gene)

#     def test_add_genes(self):
#         population_1 = PopulationBuilder.build(
#             props=self.props, variations=self.variations, random_create=True
#         )

#         population_2 = PopulationBuilder.build(
#             props=self.props, variations=self.variations, random_create=True
#         )

#         assert population_1.data is not None
#         assert population_2.data is not None
#         N = 4
#         genes_for_add_ids = np.random.choice(
#             list(population_2.data.index), N, replace=False
#         )
#         genes_for_add_ids.sort()
#         genes_for_add: list[Gene] = []
#         for i, gene in enumerate(population_2.genes):
#             if i in genes_for_add_ids:
#                 genes_for_add.append(gene)
#         population_1.add_genes(*genes_for_add)
#         for gene_1, gene_2 in zip(genes_for_add, population_1.genes[-N:]):
#             try:
#                 self.assertEqual(gene_1, gene_2)
#             except ValueError as error:
#                 self.assertIn(
#                     "The truth value of a Series is ambiguous", str(error)
#                 )

#         selected_1 = population_1.data[-N:]
#         selected_2 = population_2.data.iloc[genes_for_add_ids]
#         selected_2.index = selected_1.index
#         for key_1 in selected_1.index:  # type: ignore
#             value_1: list[float] = selected_1.loc[key_1]  # type: ignore
#             value_2: list[float] = selected_2.loc[key_1]  # type: ignore

#             for i, j in zip(value_1, value_2):  # type: ignore
#                 is_equal = i == j or (np.isnan(i) and np.isnan(j))
#                 self.assertTrue(is_equal, f"deve ser igual: {i} != {j}")
