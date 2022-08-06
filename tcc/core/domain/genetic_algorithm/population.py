import functools
import itertools
from typing import List, Optional, Sequence

import pandas as pd

from tcc.core.domain import BaseModel
from tcc.core.domain.genetic_algorithm.gene import Gene, GeneBuilder
from tcc.core.domain.transformer.entities import Variation

InputData = Optional[List[Gene] | pd.DataFrame]


class PopulationProps(BaseModel):
    n_population: int
    disturbance_rate: float
    crossover_probability: float


class Population(BaseModel):
    data: Optional[pd.DataFrame] = None
    props: PopulationProps
    genes: Sequence[Gene]

    class Config:
        arbitrary_types_allowed = True

    # def get_gene(self, i: int) -> Gene:
    #     assert self.data is not None
    #     data: pd.Series = self.data.iloc[i]

    #     return Gene(data=data)

    def shape(self):
        assert self.data is not None
        return self.data.shape

    def len(self):
        return self.shape()[0]


class PopulationBuilder:
    n_population: int
    variations: Variation

    @classmethod
    def build(
        cls,
        props: PopulationProps,
        variations: Variation,
        data: InputData = None,
    ) -> Population:
        data = cls.get_genes(
            data,
            n_population=props.n_population,
            variations=variations,
        )

        index = pd.Index(data=range(len(data)))
        return Population(
            data=pd.DataFrame(data=data, index=index), props=props, genes=data
        )

    @functools.singledispatchmethod
    @classmethod
    def get_genes(
        cls,
        data: InputData,
        n_population: Optional[int] = None,
        variations: Optional[Variation] = None,
    ) -> List[Gene]:
        assert n_population is not None
        assert variations is not None
        return cls.random_generate(n_population, variations)

    @get_genes.register
    @classmethod
    def _(
        cls,
        data: pd.DataFrame,
        n_population: Optional[int] = None,
        variations: Optional[Variation] = None,
    ):
        raise NotImplementedError

    @get_genes.register(list)
    @classmethod
    def _(
        cls,
        data: List[Gene],
        n_population: Optional[int] = None,
        variations: Optional[Variation] = None,
    ):
        return data

    @classmethod
    def random_generate(
        cls, n_population: int, variations: Variation
    ) -> List[Gene]:
        genes = map(
            GeneBuilder.build, itertools.repeat(variations, n_population)
        )
        data = [gene for gene in genes]

        return data
