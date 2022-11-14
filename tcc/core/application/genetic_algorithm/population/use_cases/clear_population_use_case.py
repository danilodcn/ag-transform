import numpy as np
import pandas as pd

from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)

from .base_use_case import PopulationUseCaseBase


class ClearPopulationUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population) -> None:
        self.population = population
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.fitness_calculated

    def run(self, n_population: int | None = None):
        if n_population is None:
            n_population = self.population.props.n_population

        all_ranks = list(self.data["rank"].drop_duplicates())
        preserve_ranks = round(len(all_ranks) * 0.4)

        ranks = list(
            self.data[self.data["rank"] <= preserve_ranks][
                "rank"
            ].drop_duplicates()
        )
        ranks.sort(reverse=True)
        removed_index = set(
            self.data[self.data["rank"] > preserve_ranks].index
        )
        n_removed = len(self.data) - n_population
        minimal_distance: float = np.min(self.data["distance"]) * 0.8
        max_distance = np.max(self.data["distance"])
        if minimal_distance <= 0.0:
            minimal_distance = 1e-6
        while True:
            minimal_distance *= 1.3
            for rank in ranks:
                with_rank = self.data[self.data["rank"] == rank]
                remove = with_rank[with_rank["distance"] < minimal_distance]
                removed_index = removed_index.union(list(remove.index))

            if len(removed_index) > n_removed:
                removed_index_choices = np.random.choice(
                    list(removed_index), n_removed, replace=False
                )
                removed_index = set(removed_index_choices)

            if len(removed_index) == n_removed:
                self.data = self.data[~self.data.index.isin(removed_index)]
                self.data.index = pd.RangeIndex(n_population)
                break

            if minimal_distance > max_distance:
                raise OverflowError("Não consegue limpar a população")

        self.population.data = self.data
        self.population.generate_genes()
