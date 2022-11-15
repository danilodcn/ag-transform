import numpy as np
import pandas as pd
from pydantic import validate_arguments

from tcc.core.application.tools.functions import sum_of_integers
from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)
from tcc.core.domain.transformer.entities import Variation

from .base_use_case import PopulationUseCaseBase

BIG_NUMBER = 1e2


class PopulationFitnessUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population, variations: Variation) -> None:
        self.population = population
        self.variations = variations
        self.niche_radius = population.props.niche_radius
        self.__set_delta_losses_and_mass()

    def __set_delta_losses_and_mass(self):
        min_losses, max_losses, _ = self.variations.PerdasT
        min_mass, max_mass, _ = self.variations.PerdasT
        self.delta_loss = max_losses - min_losses
        self.delta_mass = max_mass - min_mass

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.ranks_sorted

    def run(self):
        # algoritmo definido na página 120 do Lobato
        self.population.data = self.__calcule_fitness()
        self.population.step = PopulationSteps.fitness_calculated
        return self.population

    def __calcule_fitness(self):
        data = self.population.get_data()
        current_n_population = self.population.len()
        columns_names = [
            "meanFitness",
            "sumDistance",
            "distance",
            "sharedFitness",
            "solutions_for_rank",
            "rank",
        ]

        df = pd.DataFrame(
            np.zeros((current_n_population, len(columns_names))),
            columns=columns_names,
        )

        df["rank"] = data["rank"]

        ranks = list(data["rank"].drop_duplicates())
        ranks.sort()

        n_before = current_n_population

        for rank in ranks:
            set: pd.DataFrame = data.loc[data["rank"] == rank][
                ["PerdasT_P", "Mativa_P"]
            ].sort_values(by=["PerdasT_P"])
            losses_set = set["PerdasT_P"]

            df.loc[losses_set.index, "solutions_for_rank"] = losses_set.count()

            number = len(losses_set.index)
            n_current = n_before - number

            df.loc[losses_set.index, "meanFitness"] = sum_of_integers(
                n_current, n_before
            ) / (n_before - n_current)
            n_before = n_current

            loss: pd.Series[float] = set["PerdasT_P"]
            mass: pd.Series[float] = set["Mativa_P"]
            # import ipdb; ipdb.set_trace()
            index_list = list(set.index)
            first_index = index_list[0]
            last_index = index_list[-1]
            for count, i in enumerate(set.index):
                losses_i, mass_i = loss[i], mass[i]
                distance = 1
                if i in [first_index, last_index]:
                    final_distance = BIG_NUMBER
                else:
                    i_0 = set.index[count - 1]
                    i_1 = set.index[count + 1]
                    d0 = self.__distance(
                        losses_i, loss[i_0], mass_i, mass[i_0]  # type: ignore
                    )
                    d1 = self.__distance(
                        losses_i, loss[i_1], mass_i, mass[i_1]  # type: ignore
                    )
                    final_distance = (d0 + d1) / 2

                df.loc[i, "distance"] = final_distance
                count += 1
                for j in set.index:
                    if i == j:
                        continue
                    perda_j, massa_j = loss[j], mass[j]
                    distance_ij = self.__distance(
                        losses_i, perda_j, mass_i, massa_j  # type: ignore
                    )
                    distance += self.__shared_function(distance_ij, 1)

                df.loc[i, "sumDistance"] = distance

        # import ipdb; ipdb.set_trace()
        df["sharedFitness"] = df["meanFitness"] / df["sumDistance"]

        sum_shared_fitness = np.sum(df["sharedFitness"])

        result = (
            df["meanFitness"]
            * df["solutions_for_rank"]
            * (df["sharedFitness"] / sum_shared_fitness)
        )
        data["fitness"] = result / np.sum(result)
        data["distance"] = df["distance"]
        return data

    @validate_arguments
    def __distance(self, l1: float, l2: float, m1: float, m2: float) -> float:
        loss = ((l1 - l2) / self.delta_loss) ** 2
        mass = ((m1 - m2) / self.delta_mass) ** 2

        return (mass + loss) ** 0.5

    @validate_arguments
    def __shared_function(self, distance: float, alfa: float):
        if distance <= self.niche_radius:
            return 1 - (distance / self.niche_radius) ** alfa

        else:
            return 0
