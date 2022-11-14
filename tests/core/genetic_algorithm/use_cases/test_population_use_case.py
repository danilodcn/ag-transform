import json
import unittest
from typing import Callable, Iterable

import numpy as np

from tcc.core.application.genetic_algorithm.population.use_cases import (
    ClearPopulationUseCase,
    CrossoverPopulationUseCase,
    MutationPopulationUseCase,
    PopulationCalculatorUseCase,
    PopulationFitnessUseCase,
    PopulationPenalizeUseCase,
    SelectionPopulationUseCase,
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
            niche_radius=0.1,
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
                is_none = element is None or np.isnan(element)
                self.assertTrue(
                    is_none,
                    f"Antes da operação deve ser igual a 'None'.\n{elements}",
                )

        func(*args, **kwargs)

        for name in test_field_names:
            elements = self.population.data[name]
            for element in elements:
                is_none = element is not None or not np.isnan(element)
                self.assertTrue(
                    is_none,
                    f"Após a operação deve ser diferente de 'None'.\n{elements}",
                )

    def calcule_all(self, population=None):
        if population is None:
            population = self.population
        calculator = PopulationCalculatorUseCase(
            population,
            self.table_repository,
            self.constraints,
            self.variations,
        )
        self.population.generate_data()
        calculator.execute()

    def penalize_population(self, **options):
        use_case = PopulationPenalizeUseCase(self.population, self.variations)
        use_case.execute(**options)

    def sort_pareto_ranks(self):
        use_case = SortParetoRanksUseCase(self.population)
        use_case.execute()

    def calcule_fitness(self):
        use_case = PopulationFitnessUseCase(
            population=self.population, variations=self.variations
        )
        use_case.execute()

    def crossover_population(self, population_frac):
        use_case = CrossoverPopulationUseCase(self.population)
        population: Population = use_case.execute(
            population_frac=population_frac
        )
        self.calcule_all(population)
        self.population = population

    def mutation_population(self, population_frac):
        use_case = MutationPopulationUseCase(self.population)
        population: Population = use_case.execute(
            population_frac=population_frac
        )
        self.calcule_all(population)
        self.population = population

    def clear_population(self, n_population: int | None = None):
        use_case = ClearPopulationUseCase(self.population)
        use_case.execute(n_population=n_population)

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

    def test_sort_pareto_ranks(self):
        self.calcule_all()
        self.penalize_population(type="weigh")
        assert self.population.data is not None

        self.assertPopulationChangeValue(self.sort_pareto_ranks, ["rank"])

    def test_calcule_fitness(self):
        self.calcule_all()
        self.penalize_population()
        self.sort_pareto_ranks()

        self.assertPopulationChangeValue(self.calcule_fitness, ["fitness"])

    def test_selection_use_case(self):
        self.calcule_all()
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()
        expected_n_population = 3
        use_case: SelectionPopulationUseCase = SelectionPopulationUseCase(
            self.population
        )
        population: Population = use_case.execute(number=expected_n_population)

        assert population.data is not None

        self.assertIsInstance(population, Population)
        self.assertEqual(population.len(), expected_n_population)
        self.assertEqual(len(population.data), expected_n_population)
        self.assertEqual(len(population.genes), expected_n_population)

    def test_crossover_population(self):
        self.calcule_all()
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()
        self.crossover_population(population_frac=0.9)

    def test_mutation_population(self):
        self.calcule_all()
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()
        frac = 0.46
        self.mutation_population(population_frac=frac)

    def test_clear_population(self):
        self.calcule_all()
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()

        frac = 0.46

        self.crossover_population(population_frac=frac)
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()

        self.mutation_population(population_frac=frac)
        self.penalize_population()
        self.sort_pareto_ranks()
        self.calcule_fitness()
        n_population = self.population.props.n_population - 4

        self.clear_population(n_population=n_population)

        self.assertIsInstance(self.population, Population)
        self.assertEqual(len(self.population.get_data()), n_population)
        self.assertEqual(len(self.population.genes), n_population)

    def test_plot_after_calculation(self):
        self.calcule_all()
        self.penalize_population(type="weigh")
        self.sort_pareto_ranks()
        plot = Plot()
        assert self.population.data is not None
        fields_names = "PerdasT Mativa".split()
        plot.plot(self.population.data, fields_names, title="Primeira Geração")
        fields_names = "PerdasT_P Mativa_P".split()
        plot.plot(self.population.data, fields_names, title="Com penalização")
        fields_names = "PerdasT Mativa".split()
        plot.plot(
            self.population.data,
            fields_names,
            with_ranks=True,
            title="Com ranks",
        )
        # import ipdb; ipdb.set_trace()
        # self.calcule_fitness()
        # plot.save(suffix="plot_after_calculation", type="pdf", dpi=500)
        # return
        fields_names = "PerdasT_P Mativa_P".split()
        plot.plot(
            self.population.data,
            fields_names,
            with_ranks=True,
            title="Com ranks (Valores penalizados)",
        )

        self.calcule_fitness()
        self.crossover_population(population_frac=0.9)
        self.penalize_population()
        self.sort_pareto_ranks()
        fields_names = "PerdasT_P Mativa_P".split()
        plot.plot(
            self.population.data,
            fields_names,
            with_ranks=True,
            title="Após crossover",
        )
        self.calcule_fitness()
        self.mutation_population(population_frac=0.9)
        self.penalize_population()
        self.sort_pareto_ranks()
        fields_names = "PerdasT_P Mativa_P".split()
        plot.plot(
            self.population.data,
            fields_names,
            with_ranks=True,
            title="Após mutação",
        )

        plot.save(suffix="plot_after_calculation", type="pdf", dpi=500)
