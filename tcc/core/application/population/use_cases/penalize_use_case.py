from typing import Literal

import numpy as np
import pandas as pd

from tcc.core.application.tools.restrict_violated import (
    count_restrictions_violated,
)
from tcc.core.domain.entities.genetic_algorithm.population.population import (
    Population,
    PopulationSteps,
)
from tcc.core.domain.entities.transformer.variation import Variation

from .base_use_case import PopulationUseCaseBase


class PopulationPenalizeUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population, variations: Variation) -> None:
        self.variations = variations
        self.population = population

    @property
    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.calculated

    def run(self, type: Literal["count", "weigh"] = "weigh"):
        data = self.population.data
        assert isinstance(
            data, pd.DataFrame
        ), "population.data não pode está vazio"
        counts = data.apply(
            count_restrictions_violated,  # type: ignore
            args=(self.variations,),
            axis=1,
            result_type="expand",  # type: ignore
        )
        counts_list = counts[type]
        max_losses: float = np.max(
            data["PerdasT"][data["PerdasT"] <= self.variations.PerdasT[1]]
        )
        max_active_mass: float = np.max(
            data["Mativa"][data["Mativa"] <= self.variations.Mativa[1]]
        )
        population_len = self.population.len()
        penalize_constant = self.population.props.penalize_constant

        result = np.asarray(
            (
                np.ones(population_len) * max_losses * counts_list,
                np.ones(population_len) * max_active_mass * counts_list,
            )
        ).transpose()

        data[["PerdasT_P", "Mativa_P"]] = data[["PerdasT", "Mativa"]]
        vector_params = (
            pd.DataFrame(
                result * penalize_constant,
                columns=[
                    "PerdasT_P",
                    "Mativa_P",
                ],
            )
            + data[["PerdasT_P", "Mativa_P"]]
        )

        assert len(vector_params.keys()) == 2

        data.update(vector_params)
        self.population.step = PopulationSteps.penalized
        return self.population
