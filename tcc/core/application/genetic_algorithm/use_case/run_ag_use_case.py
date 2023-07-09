import dataclasses
import logging
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor
from queue import Queue

import pandas as pd

from tcc.core.application.population.use_cases import (
    ClearPopulationUseCase,
    CrossoverPopulationUseCase,
    MutationPopulationUseCase,
    PopulationCalculatorUseCase,
    PopulationFitnessUseCase,
    PopulationPenalizeUseCase,
    SortParetoRanksUseCase,
)
from tcc.core.domain.entities.transformer.constraints import Constraint
from tcc.core.domain.entities.transformer.variation import Variation
from tcc.core.domain.genetic_algorithm.population import Population
from tcc.core.domain.repositories.table_repository import TableRepository

logger = logging.getLogger(__name__)


STEPS = {
    0: "inicial",
    1: "fitness calculado",
    2: "reprodução",
    3: "mutação",
    4: "limpo",
}


@dataclasses.dataclass
class DataOutput:
    step: str
    data: pd.DataFrame
    index: int | None = None


class RunAGUseCase:
    def __init__(
        self,
        population: Population,
        table_repository: TableRepository,
        constraints: Constraint,
        variations: Variation,
    ) -> None:
        self.population = population
        self.constraints = constraints
        self.variations = variations
        self.table_repository = table_repository

        self.population.generate_data()
        self.on_init()

    def get_data(self, i) -> DataOutput:
        data = DataOutput(STEPS[i], self.population.get_data().copy())
        return data

    def run(self):
        assert isinstance(self.population.data, pd.DataFrame)
        yield self.get_data(0)
        self.calculate_penalize_pareto_ranks_and_fitness()
        yield self.get_data(1)
        self.crossover_population()
        yield self.get_data(2)
        self.calculate_penalize_pareto_ranks_and_fitness()
        yield self.get_data(2)
        self.mutation_population()
        yield self.get_data(3)
        self.calculate_penalize_pareto_ranks_and_fitness()
        yield self.get_data(2)
        self.clear_population()
        yield self.get_data(4)

    def execute(
        self,
        producer_callback: Callable | None = None,
        consumer_callback: Callable | None = None,
    ):
        with ThreadPoolExecutor(2) as executor:
            queue = Queue()

            executor.submit(self.consume, q=queue, callback=consumer_callback)
            executor.submit(self.produce, q=queue, callback=producer_callback)

    def consume(
        self, q: Queue[DataOutput | None], callback: Callable | None = None
    ):
        while True:
            print("[2 - CONSUMER] esperando mensagem")
            value = q.get(block=True, timeout=10)
            if value is None:
                return
            if callable(callback):
                callback(value)

    def produce(
        self, q: Queue[DataOutput | None], callback: Callable | None = None
    ):
        print("[1 - PRODUCER] dentro da função")
        for i, value in enumerate(self.run()):
            value.index = i
            if callable(callback):
                callback(value)
            q.put(value)

        q.put(None)

    def calculate_penalize_pareto_ranks_and_fitness(self):
        print("calcular")
        self.calcule_all()
        print("penalizar")
        self.penalize()
        print("ordenar")
        self.sort_pareto_ranks()
        print("calcular fitness")
        self.calcule_fitness()

    def calcule_all(self):
        self.population = self.population_calculator_use_case.execute()

    def penalize(self):
        self.population = self.penalize_use_case.execute(type="weigh")

    def sort_pareto_ranks(self):
        self.population = self.sort_pareto_ranks_use_case.execute()

    def calcule_fitness(self):
        self.population = self.fitness_calculator_use_case.execute()

    def crossover_population(self):
        self.population = self.crossover_population_use_case.execute()

    def mutation_population(self):
        self.population = self.mutation_population_use_case.execute()

    def clear_population(self):
        self.population = self.clear_population_use_case.execute()

    def on_init(self):
        self.population_calculator_use_case = PopulationCalculatorUseCase(
            self.population,
            self.table_repository,
            self.constraints,
            self.variations,
        )
        self.penalize_use_case = PopulationPenalizeUseCase(
            self.population, self.variations
        )
        self.sort_pareto_ranks_use_case = SortParetoRanksUseCase(
            self.population
        )
        self.fitness_calculator_use_case = PopulationFitnessUseCase(
            population=self.population, variations=self.variations
        )

        self.crossover_population_use_case = CrossoverPopulationUseCase(
            self.population
        )
        self.mutation_population_use_case = MutationPopulationUseCase(
            self.population
        )
        self.clear_population_use_case = ClearPopulationUseCase(
            self.population
        )
