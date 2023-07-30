from collections import defaultdict
from enum import Enum

import pandas as pd
from typing_extensions import Self

from tcc.core.domain import BaseModel

from ..gene.gene import Gene
from .props import PopulationProps


class PopulationSteps(int, Enum):
    new = 0
    calculated = 1
    penalized = 2
    ranks_sorted = 3
    fitness_calculated = 4


class Population(BaseModel):
    step: PopulationSteps = PopulationSteps.new
    props: PopulationProps
    genes: list[Gene]

    @property
    def data(self) -> pd.DataFrame:
        data = getattr(self, "__data", None)
        if data is None:
            self.__data = self.generate_data()

        return self.__data

    class Config:
        arbitrary_types_allowed = True

    def __add__(self, other: Self) -> Self:
        return self.join(other)

    def join(self, other: Self | pd.DataFrame) -> "Population":
        self_data = self.data
        assert isinstance(
            self_data, pd.DataFrame
        ), "make sure 'self.data' is a Data Frame"

        if isinstance(other, Population):
            other_data = other.data
        else:
            other_data = other

        assert isinstance(
            other_data, pd.DataFrame
        ), "make sure 'other.data' is a Data Frame"

        data = pd.concat(  # type: ignore
            objs=[self_data, other_data],
            ignore_index=True,
        )

        self.__data = data
        self.step = PopulationSteps.new
        return self

    def generate_data(self) -> pd.DataFrame:
        data = pd.DataFrame(  # type: ignore
            gene.data for gene in self.genes  # type: ignore
        )
        return data

    def set_props(self, props: PopulationProps) -> Self:
        self.props = props
        return self

    def set_genes(self, genes: list[Gene]) -> Self:
        self.genes = genes
        return self

    def shape(self):
        assert self.data is not None
        return self.data.shape

    def len(self) -> int:
        return self.shape()[0]

    def add_genes(self, *genes: Gene):
        self.genes.extend(genes)
        rows: dict[int, pd.Series[float]] = {}
        for i, gene in enumerate(genes, start=len(genes)):
            rows[i] = gene.generate_data()

        assert isinstance(self.data, pd.DataFrame)
        objs = [
            self.data,
            pd.DataFrame(rows.values(), index=list(rows.keys())),
        ]

        self.__data = pd.concat(  # type: ignore
            objs=objs,
            ignore_index=True,
        )

    def get_step_display(self, step: int | None = None):
        steps: dict[int, str] = defaultdict(lambda: "-")
        steps.update(
            {
                0: "novo",
                1: "calculado",
                2: "penalizado",
                3: "ranks ordenados",
                4: "fitness calculado",
            }
        )

        if step is None:
            step = self.step
        return steps[step]
