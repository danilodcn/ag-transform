import pandas as pd

from tcc.core.domain import BaseModel
from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.transformer.transformer import Transformer


class PopulationProps(BaseModel):
    n_population: int
    disturbance_rate: float
    crossover_probability: float


class Population(BaseModel):
    props: PopulationProps
    data: pd.DataFrame
    transformer: Transformer

    class Config:
        arbitrary_types_allowed = True

    def get_gene(self, i: int) -> Gene:
        data: pd.Series = self.data.iloc[i]

        return Gene(data=data)

    def shape(self):
        return self.data.shape

    def len(self):
        return self.shape()[0]
