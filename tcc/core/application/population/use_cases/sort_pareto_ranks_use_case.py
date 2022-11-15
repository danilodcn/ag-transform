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

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.penalized

    def validate(self):
        super().validate()
        data = self.population.get_data()
        assert not all(
            data["PerdasT_P"].isnull()
        ), "garanta que os genes foram penalizados"
        assert not all(
            data["Mativa_P"].isnull()
        ), "garanta que os genes foram penalizados"

    def run(self):
        data = self.population.get_data()
        max_ranks = self.population.props.max_ranks
        data["rank"] = max_ranks
        no_dominated: List[int] = list(data.index)
        number = 1
        data.loc[no_dominated, "rank"] = number
        while len(no_dominated) != 0:
            no_dominated = self.__sort_pareto_ranks(no_dominated, number)
            number += 1
            data.loc[no_dominated, "rank"] = number
            if max_ranks and number >= max_ranks:
                break

        self.population.step = PopulationSteps.ranks_sorted
        return self.population

    def __sort_pareto_ranks(self, no_dominated: List[int], number: int):
        dominates: List[int] = []
        data = self.population.get_data()
        for i in no_dominated:
            for p in no_dominated:
                if i == p:
                    continue
                else:
                    gene_i = data.loc[i, ["PerdasT_P", "Mativa_P"]]
                    gene_p = data.loc[p, ["PerdasT_P", "Mativa_P"]]

                    if is_dominated(gene_i, gene_p):
                        dominates.append(i)
                        # data.loc[i, "rank"] = number + 1
                        break

        return dominates
