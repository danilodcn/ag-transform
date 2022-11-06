from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase


class SortParetoRanksUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population) -> None:
        self.population = population
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.penalized

    def run(self):
        raise NotImplementedError
