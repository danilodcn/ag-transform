from typing import List

from tcc.core.application.tools.is_dominated import is_dominated
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
        self.data["rank"] = 0
        no_dominated: List[int] = list(self.data.index)
        number = 1
        self.data.loc[no_dominated, "rank"] = number
        while len(no_dominated) != 0:
            no_dominated = self.__sort_pareto_ranks(no_dominated, number)
            number += 1
            self.data.loc[no_dominated, "rank"] = number

    def __sort_pareto_ranks(self, no_dominated: List[int], number: int):
        dominates: List[int] = []
        for i in no_dominated:
            for p in no_dominated:
                if i == p:
                    continue
                else:
                    gene_i = self.data.loc[i, ["PerdasT_P", "Mativa_P"]]
                    gene_p = self.data.loc[p, ["PerdasT_P", "Mativa_P"]]

                    if is_dominated(gene_i, gene_p):
                        dominates.append(i)
                        # self.data.loc[i, "rank"] = number + 1
                        break

        return dominates
