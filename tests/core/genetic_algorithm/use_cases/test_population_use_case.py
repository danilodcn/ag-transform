import json
import unittest
from typing import Callable, Iterable

from tcc.core.application.genetic_algorithm.population.use_cases.calcule_all_use_case import (
    PopulationCalculatorUseCase,
)
from tcc.core.application.genetic_algorithm.population.use_cases.penalize_use_case import (
    PopulationPenalizeUseCase,
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
            n_population=10,
            disturbance_rate=0.3,
            crossover_probability=0.4,
            penalize_constant=1.4,
        )

        self.population = PopulationBuilder.build(
            props=props,
            variations=self.variations,
        )

    def assertPopulationChangeValue(
        self, func: Callable, test_field_names: Iterable[str], *args, **kwargs
    ):
        assert self.population.data is not None
        for name in test_field_names:
            elements = self.population.data[name]
            for element in elements:
                self.assertEqual(
                    element,
                    None,
                    f"Antes da operação deve ser igual a 'None'.\n{elements}",
                )

        func(*args, **kwargs)

        for name in test_field_names:
            elements = self.population.data[name]
            for element in elements:
                self.assertNotEqual(
                    element,
                    None,
                    f"Após a operação deve ser diferente de 'None'.\n{elements}",
                )

    def calcule_all(self):
        calculator = PopulationCalculatorUseCase(
            self.population,
            self.table_repository,
            self.constraints,
            self.variations,
        )
        self.population.generate_data()
        calculator.execute()

    def penalize_population(self, **options):
        use_case = PopulationPenalizeUseCase(self.population, self.variations)
        use_case.execute(**options)

    def test_calcule_all_in_population(self):
        self.population.generate_data()
        assert self.population.data is not None
        test_field_names = ["Mativa", "PerdasT"]

        self.assertPopulationChangeValue(self.calcule_all, test_field_names)

    def test_penalize_population(self):
        self.calcule_all()

        assert self.population.data is not None
        test_field_names = ["Mativa_P", "PerdasT_P"]

        self.assertPopulationChangeValue(
            self.penalize_population, test_field_names
        )

    def sort_pareto_ranks(self):
        use_case = SortParetoRanksUseCase(self.population)
        use_case.execute()

    def test_sort_pareto_ranks(self):
        self.calcule_all()
        self.penalize_population(type="weigh")
        assert self.population.data is not None

        self.assertPopulationChangeValue(self.sort_pareto_ranks, ["rank"])

    def test_plot_after_calculation(self):
        self.calcule_all()
        self.penalize_population(type="weigh")
        plot = Plot()
        assert self.population.data is not None
        fields_names = "PerdasT Mativa".split()
        plot.plot(self.population.data, fields_names)
        fields_names = "PerdasT_P Mativa_P".split()
        plot.plot(self.population.data, fields_names)
        plot.save(suffix="plot_after_calculation", type="pdf", dpi=500)
