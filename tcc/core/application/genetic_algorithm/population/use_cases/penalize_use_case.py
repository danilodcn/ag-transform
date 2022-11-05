from typing import Literal

import numpy as np
import pandas as pd

from tcc.core.application.tools.restrict_violated import (
    count_restrictions_violated,
)
from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)
from tcc.core.domain.transformer.entities import Variation

from .base_use_case import PopulationUseCaseBase


class PopulationPenalizeUseCase(PopulationUseCaseBase):
    def __init__(self, population: Population, variations: Variation) -> None:
        self.variations = variations
        self.population = population
        assert self.population.data is not None, "data não existe!"
        self.data = self.population.data

    def minimal_step(self) -> PopulationSteps:
        return PopulationSteps.calculated

    def run(self, type: Literal["count", "weigh"] = "count"):
        counts = self.data.apply(
            count_restrictions_violated,
            args=(self.variations,),
            axis=1,
            result_type="expand",
        )
        counts_list = counts[type]
        max_losses = self.variations.PerdasT[1]
        max_active_mass = self.variations.Mativa[1]
        n_population = self.population.props.n_population
        penalize_constant = self.population.props.penalize_constant
        # import ipdb; ipdb.set_trace()
        result = np.asarray(
            (
                np.ones(n_population) * max_losses * counts_list,
                np.ones(n_population) * max_active_mass * counts_list,
            )
        ).transpose()
        self.data[["PerdasT_P", "Mativa_P"]] = self.data[["PerdasT", "Mativa"]]
        vector_params = (
            pd.DataFrame(
                result * penalize_constant,
                columns=[
                    "PerdasT_P",
                    "Mativa_P",
                ],
            )
            + self.data[["PerdasT_P", "Mativa_P"]]
        )

        assert len(vector_params.keys()) == 2
        self.data.update(vector_params)
        self.population.step = PopulationSteps.penalized
