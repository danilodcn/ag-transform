# import json
# import unittest

# from tcc.core.application.genetic_algorithm.use_case import (
#     DataOutput,
#     RunAGUseCase,
# )
# from tcc.core.application.tools.plot import Plot
# from tcc.core.domain.entities.genetic_algorithm.population.population_builder import (  # noqa
#     PopulationBuilder,
#     PopulationProps,
# )
# from tcc.core.domain.entities.transformer.constraints import Constraint
# from tcc.core.domain.entities.transformer.transformer import Transformer
# from tcc.core.domain.entities.transformer.variable import Variable
# from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
#     TableRepositoryInMemory,
# )

# from tests.constants import TABLE_FILE_NAME, TRANSFORMER_FILE_NAME


# class TestUseCaseCalculeAll(unittest.TestCase):
#     def setUp(self) -> None:
#         self.variation_repository = VariationRepositoryInMemory()
#         self.table_repository = TableRepositoryInMemory(TABLE_FILE_NAME)

#         with open(TRANSFORMER_FILE_NAME) as file:
#             transformer_data = json.load(file)
#             self.variables = Variable(**transformer_data.get("variables", {}))
#             self.constraints = Constraint(
#                 **transformer_data.get("constraints", {})
#             )

#         self.variations = self.variation_repository.get()
#         self.transformer = Transformer(
#             variables=self.variables,
#             constraints=self.constraints,
#             variations=self.variations,
#         )
#         props = PopulationProps(
#             n_population=10,
#             disturbance_rate=0.3,
#             crossover_probability=0.4,
#             penalize_constant=1.4,
#             niche_radius=0.01,
#             crossover_population_frac=0.1,
#             mutation_population_frac=0.1,
#             max_ranks=2,
#         )

#         self.population = PopulationBuilder.build(
#             props=props,
#             variations=self.variations,
#         )

#         self.ag_use_case = RunAGUseCase(
#             self.population,
#             self.table_repository,
#             self.constraints,
#             self.variations,
#         )

#     def test_creation_ag_use_case(self):
#         self.assertIsInstance(self.ag_use_case, RunAGUseCase)

#     def test_execute_AG(self):
#         g = 0

#         def handle(out: DataOutput | None):
#             if out:
#                 print("Dentro do handler", out.index)
#                 plot.plot(
#                     df=out.data,
#                     field_names="Mativa PerdasT".split(),
#                     title=f"{out.step} - {out.index} - geração {g}",
#                 )
#             else:
#                 print("recebeu sinal de saída!")

#         plot = Plot()
#         for i in range(1):
#             self.ag_use_case.execute(
#                 consumer_callback=handle,
#             )
#         plot.plot(
#             df=self.population.get_data(),
#             field_names="Mativa PerdasT".split(),
#             title="Depois",
#             with_ranks=True,
#         )
#         plot.save(suffix="antes", dir_name="ag", type="pdf")
#         print("saiu")
