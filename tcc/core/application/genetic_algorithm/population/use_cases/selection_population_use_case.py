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
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.fitness_calculated

    def run(
        self,
        number: int | None = None,
        frac: float | None = None,
        weights: Iterable[float] | None = None,
    ) -> Population:
        if frac is not None and number is not None:
            raise ValueError("Cannot use 'number' and 'frac'")

        if weights is None:
            weights = self.data["fitness"]
        elif weights == 1:
            weights = np.ones(len(self.data))
        weights = tuple(weights)

        new_data = self.data.sample(
            n=number,
            frac=frac,
            replace=False,
            weights=weights,
        )
        population = self.population.copy(update={"data": new_data})
        population.generate_genes()
        population.props.n_population = len(new_data)
        return population
