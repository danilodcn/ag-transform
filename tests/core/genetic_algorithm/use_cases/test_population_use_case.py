import json
import unittest

from tcc.core.application.genetic_algorithm.population.use_cases.calcule_all_use_case import (
    PopulationCalculatorUseCase,
)
from tcc.core.application.genetic_algorithm.population.use_cases.sort_pareto_ranks_use_case import (
    SortParetoRanksUseCase,
)
from tcc.core.application.tools.plot import Plot
from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationBuilder,
    PopulationProps,
)
from tcc.core.domain.transformer.entities import Constraint, Variable
from tcc.core.domain.transformer.transformer import Transformer
from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
    TableRepositoryInMemory,
)
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
    VariationRepositoryInMemory,
)
from tests.constants import *


class TestUseCaseCalculeAll(unittest.TestCase):
    def setUp(self) -> None:
        self.variation_repository = VariationRepositoryInMemory()
        self.table_repository = TableRepositoryInMemory()
        self.table_repository.load_tables(TABLE_FILE_NAME)

        with open(TRANSFORMER_FILE_NAME) as file:
            transformer_data = json.load(file)
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
        props = PopulationProps(
            n_population=10, disturbance_rate=0.3, crossover_probability=0.4
        )

        self.population = PopulationBuilder.build(
            props=props,
            variations=self.variations,
        )

    def test_calcule_all_in_population(self):
        calculator = PopulationCalculatorUseCase(
            self.population,
            self.table_repository,
            self.constraints,
            self.variations,
        )
        self.population.generate_data()
        assert self.population.data is not None
        test_field_names = ["Mativa", "PerdasT"]

        for name in test_field_names:
            for element in self.population.data[name]:
                self.assertIs(None, element)

        calculator.execute()

        for name in test_field_names:
            self.assertNotIn(None, self.population.data[name])

    def test_sort_pareto_ranks(self):
        self.test_calcule_all_in_population()
        use_case = SortParetoRanksUseCase(self.population)
        use_case.execute()

    def test_plot_after_calculation(self):
        self.test_calcule_all_in_population()
        plot = Plot()
        assert self.population.data is not None
        fields_names = "PerdasT Mativa".split()
        plot.plot(self.population.data, fields_names)
        plot.save(suffix="plot_after_calculation", type="pdf", dpi=500)
