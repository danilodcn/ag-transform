from typing import Iterable, Type

import numpy as np

from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase


class SelectionPopulationUseCase(PopulationUseCaseBase):
    __ret__ = Type[Population]

    def __init__(self, population: Population) -> None:
        self.population = population

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.fitness_calculated

    def run(
        self,
        number: int | None = None,
        frac: float | None = None,
        weights: Iterable[float] | None = None,
        replace: bool = False,
        rand_sort: float | None = None,
    ) -> Population:
        data = self.population.get_data()
        if frac is not None and number is not None:
            raise ValueError("Cannot use 'number' and 'frac'")

        if weights is None:
            weights = data["fitness"]
        elif weights == 1:
            weights = np.ones(len(data))
        weights = tuple(weights)

        new_data = data.sample(
            n=number,
            frac=frac,
            replace=replace,
            weights=weights,
        )
        if rand_sort:
            new_data = new_data.sample(frac=1)
        population = self.population.copy(update={"data": new_data})
        population.generate_genes()
        return population
