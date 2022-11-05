import functools
import itertools
from collections import defaultdict
from enum import Enum
from typing import Dict, List, Optional

import pandas as pd
from typing_extensions import Self

from tcc.core.domain import BaseModel
from tcc.core.domain.genetic_algorithm.gene import Gene, GeneBuilder
from tcc.core.domain.transformer.entities import Variation

InputData = Optional[List[Gene] | pd.DataFrame]


class PopulationProps(BaseModel):
    n_population: int
    disturbance_rate: float
    crossover_probability: float
    penalize_constant: float


class PopulationSteps(int, Enum):
    new = 0
    calculated = 1
    penalized = 2
    ranks_sorted = 3


class Population(BaseModel):
    step = PopulationSteps.new
    data: pd.DataFrame | None = None
    props: PopulationProps
    genes: List[Gene]

    class Config:
        arbitrary_types_allowed = True

    def set_data(self, data: pd.DataFrame) -> Self:
        self.data = data
        self.generate_genes()
        return self

    def set_props(self, props: PopulationProps) -> Self:
        self.props = props
        return self

    def set_genes(self, genes: List[Gene]) -> Self:
        self.genes = genes
        return self

    # def get_gene(self, i: int) -> Gene:
    #     assert self.data is not None
    #     data: pd.Series = self.data.iloc[i]

    #     return Gene(data=data)

    def shape(self):
        assert self.data is not None
        return self.data.shape

    def len(self):
        return self.shape()[0]

    def generate_data(self):
        data = [gene.generate_data() for gene in self.genes]
        self.data = pd.DataFrame(data)

        return self.data

    def generate_genes(self):
        assert self.data is not None
        data = self.data.apply(
            lambda data_gene: GeneBuilder.build(data=data_gene), axis=1
        )
        genes: List[Gene] = list(data)  # type: ignore
        self.genes = genes
        return self.genes

    def add_genes(self, *genes: Gene):
        self.genes.extend(genes)
        rows: Dict[int, pd.Series[float]] = {}
        for i, gene in enumerate(genes, start=len(genes)):
            rows[i] = gene.generate_data()

        assert self.data is not None
        objs = [
            self.data,
            pd.DataFrame(rows.values(), index=list(rows.keys())),
        ]

        self.data = pd.concat(
            objs=objs,
            ignore_index=True,
        )

    def get_step_display(self, step=None):
        steps = defaultdict(lambda: "-")
        steps.update(
            {
                0: "novo",
                1: "calculado",
                2: "penalizado",
                3: "ranks ordenados",
            }
        )

        if step is None:
            step = self.step
        return steps[step]


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

        return Population(props=props, genes=data)

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
    def _(cls, data: pd.DataFrame, **_):
        raise NotImplementedError

    @get_genes.register(list)
    @classmethod
    def _(cls, data: List[Gene], **_):
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
