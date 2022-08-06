from typing import Optional

import pandas as pd

from tcc.core.domain import BaseModel
from tcc.core.domain.genetic_algorithm.gene import Gene


class PopulationProps(BaseModel):
    n_population: int
    disturbance_rate: float
    crossover_probability: float


class Population(BaseModel):
    data: Optional[pd.DataFrame] = None
    props: PopulationProps

    class Config:
        arbitrary_types_allowed = True

    def get_gene(self, i: int) -> Gene:
        assert self.data is not None
        data: pd.Series = self.data.iloc[i]

        return Gene(data=data)

    def shape(self):
        assert self.data is not None
        return self.data.shape

    def len(self):
        return self.shape()[0]
