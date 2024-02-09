import pandas as pd

from tcc.core.application.registry.registry import Registry
from tcc.core.application.registry.registry_type import RegistryType
from tcc.core.application.transformer.transformer_runner import (
    TransformerRunner,
)
from tcc.core.domain.entities.genetic_algorithm.population.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase


class PopulationCalculatorUseCase(PopulationUseCaseBase):
    def __init__(
        self,
        *,
        population: Population,
        registry: Registry,
    ) -> None:
        self.population = population

        self.transformer_runner: TransformerRunner = registry.inject(
            RegistryType.TRANSFORMER_RUNNER
        )

    @property
    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.new

    def run(self, **_):
        result: list[list[float]] = []
        for gene in self.population.genes:
            result.append(self.transformer_runner.run(gene.transformer))

        index = self.population.data.index

        pd_result = pd.DataFrame(
            result,
            index=index,
            columns=["PerdasT", "Mativa"],
        )

        self.population.data.update(other=pd_result)  # type: ignore
        self.population.generate_data()

        self.population.step = PopulationSteps.calculated

        return self.population
