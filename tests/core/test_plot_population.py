# import json
# import unittest

# from tcc.core.application.tools.plot import Plot
# from tcc.core.domain.entities.genetic_algorithm.population.population_builder import (  # noqa
#     PopulationBuilder,
# )
# from tcc.core.domain.entities.genetic_algorithm.population.props import (  # noqa
#     PopulationProps,
# )
# from tcc.core.domain.entities.transformer.constraints import Constraint
# from tcc.core.domain.entities.transformer.transformer import Transformer
# from tcc.core.domain.entities.transformer.variable import Variable
# from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
#     TableRepositoryInMemory,
# )
# from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (  # noqa
#     VariationRepositoryInMemory,
# )
# from tests.constants import TABLE_FILE_NAME, TRANSFORMER_FILE_NAME


# class TestCreatePopulation(unittest.TestCase):
#     def setUp(self) -> None:
#         self.variation_repository = VariationRepositoryInMemory()
#         self.table_repository = TableRepositoryInMemory(TABLE_FILE_NAME)

#         with open(TRANSFORMER_FILE_NAME) as file:
#             transformer_data = json.load(file)
#             self.variables = Variable(**transformer_data.get("variables", {}))
#             self.constraints = Constraint(
#                 **transformer_data.get("constraints", {})
#             )

#         variations = self.variation_repository.get()
#         self.transformer = Transformer(
#             variables=self.variables,
#             constraints=self.constraints,
#             variations=variations,
#         )
#         props = PopulationProps(
#             n_population=10,
#             disturbance_rate=0.3,
#             crossover_probability=0.4,
#             penalize_constant=1.4,
#             niche_radius=0.1,
#             crossover_population_frac=0.4,
#             mutation_population_frac=0.8,
#         )

#         self.population = PopulationBuilder.build(
#             props=props,
#             variations=variations,
#         )

#     def test_plot_simple_using_Plot_instance(self):
#         plot = Plot()
#         plot.plot(self.population.data, "Jat Jbt".split(), title="primeiro")
#         plot.plot(self.population.data, "rel Rjan".split(), title="segundo")
#         Plot.save(
#             type="png", suffix="test_population", dir_name="tests", dpi=100
#         )
