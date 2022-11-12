import itertools as it
from typing import List

import numpy as np
import pandas as pd

from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase
from .selection_population_use_case import SelectionPopulationUseCase


class CrossoverPopulationUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population) -> None:
        self.population = population
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.penalized

    def run(self, crossover_population_frac: float):
        selection_use_case = SelectionPopulationUseCase(self.population)

        number_of_fathers = round(
            crossover_population_frac * self.population.props.n_population
        )
        options = dict(number=number_of_fathers, rand_sort=True)

        selection_population: Population = selection_use_case.execute(
            **options
        )

        number = round((1 + (1 + 8 * number_of_fathers) ** 0.5) / 2)
        options = dict(number=number, rand_sort=True, replace=True)
        selection_population_crossover: Population = (
            selection_use_case.execute(**options)
        )

        iterator = zip(
            it.cycle(selection_population.get_data().index),
            it.combinations(
                selection_population_crossover.get_data().index,
                2,
            ),
        )
        count = 0
        new_values: List[pd.Series] = []
        for i, c in iterator:
            count += 1
            if count > number_of_fathers:
                break

            j, k = c
            if j == k:
                continue

            new_values.append(self.crossover(i, j, k))
        new_data = pd.DataFrame(
            new_values,
            index=list(range(len(new_values))),
        )
        population = self.population.copy(update={"data": new_data})
        population.generate_genes()
        population.props.n_population = len(new_data)

        return self.population.join(population)

    def crossover(self, i: int, j: int, k: int) -> pd.Series:
        p_i = self.data.iloc[i]
        p_j = self.data.iloc[j]
        p_k = self.data.iloc[k]
        crossover_probability = self.population.props.crossover_probability
        disturbance_rate = self.population.props.disturbance_rate
        mask = np.random.rand(len(p_i)) < crossover_probability
        # import ipdb; ipdb.set_trace()
        children_1 = disturbance_rate * (p_i - p_j) * 1 * mask

        return children_1 + p_k
