import itertools as it
from abc import ABC, abstractproperty
from typing import Iterable

import numpy as np
import pandas as pd

from tcc.core.domain.entities.genetic_algorithm.population.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase
from .selection_population_use_case import SelectionPopulationUseCase


class IndividualOptimizationUseCase(PopulationUseCaseBase, ABC):
    def __init__(self, population: Population) -> None:
        self.population = population

    @abstractproperty
    def population_frac(self) -> float:
        raise NotImplementedError

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.penalized

    def get_iterator(
        self, selection_population: Population, number: int
    ) -> Iterable:
        raise NotImplementedError

    def run(self, population_frac: float | None = None):
        self.data = self.population.get_data()
        if population_frac is None:
            population_frac = self.population_frac

        selection_use_case = SelectionPopulationUseCase(self.population)

        number_of_fathers = round(
            population_frac * self.population.props.n_population
        )
        options = dict(number=number_of_fathers, rand_sort=True)

        selection_population: Population = selection_use_case.execute(
            **options
        )

        number = round((1 + (1 + 8 * number_of_fathers) ** 0.5) / 2)

        iterator = self.get_iterator(selection_population, number)
        count = 0
        new_values: list[pd.Series] = []
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
        self.population.join(new_data)
        self.population.generate_genes()
        return self.population

    def crossover(self, i: int, j: int, k: int) -> pd.Series:
        p_i = self.data.iloc[i]
        p_j = self.data.iloc[j]
        p_k = self.data.iloc[k]
        crossover_probability = self.population.props.crossover_probability
        disturbance_rate = self.population.props.disturbance_rate
        mask = np.random.rand(len(p_i)) < crossover_probability
        children_1 = disturbance_rate * (p_i - p_j) * 1 * mask

        return children_1 + p_k


class CrossoverPopulationUseCase(IndividualOptimizationUseCase):
    @property
    def population_frac(self) -> float:
        return self.population.props.crossover_population_frac

    def get_iterator(
        self, selection_population: Population, number: int
    ) -> Iterable:
        selection_use_case = SelectionPopulationUseCase(
            population=selection_population
        )
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
        return iterator


class MutationPopulationUseCase(IndividualOptimizationUseCase):
    @property
    def population_frac(self) -> float:
        return self.population.props.mutation_population_frac

    def get_iterator(
        self, selection_population: Population, number: int
    ) -> Iterable:
        iterator = zip(
            np.random.choice(self.data.index, size=number),
            it.combinations(
                selection_population.get_data().index,
                2,
            ),
        )
        return iterator
