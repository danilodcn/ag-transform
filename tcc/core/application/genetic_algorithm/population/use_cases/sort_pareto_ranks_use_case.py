from typing import List

from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)
from tcc.utils.sort import is_dominated

from .base_use_case import PopulationUseCaseBase


class SortParetoRanksUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population) -> None:
        self.population = population
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.calculated

    def run(self):
        self.data["rank"] = 0
        no_dominated: List[int] = list(self.data.index)
        # import ipdb; ipdb.set_trace()
        number = 0
        while len(no_dominated) != 0:
            number += 1
            no_dominated = no_dominated[: len(no_dominated) - 1]
            # no_dominated = self.__sort_pareto_ranks(no_dominated, number)
        # import ipdb; ipdb.set_trace()

    def __sort_pareto_ranks(self, no_dominated: list, number):
        dominates = []
        if len(no_dominated) == 1:
            self.data.loc[no_dominated[0], "rank"] = number

        for i in no_dominated:
            dominated = False

            for p in no_dominated:
                if i == p:
                    continue
                else:
                    gene_i = self.data.loc[i, ["PerdasT_P", "Mativa_P"]]
                    gene_p = self.data.loc[p, ["PerdasT_P", "Mativa_P"]]

                    import ipdb

                    ipdb.set_trace()

                    if is_dominated(gene_i, gene_p):
                        dominated = True
                        dominates.append(i)
                        # print(gene_i)
                        # print(gene_p)
                        self.data.loc[i, "rank"] = number + 1
                        break

            if not dominated:
                self.data.loc[i, "rank"] = number

        # import ipdb; ipdb.set_trace()

        return dominates
