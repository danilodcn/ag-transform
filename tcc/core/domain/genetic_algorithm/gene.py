import functools
from typing import Any

import numpy as np
import pandas as pd
from typing_extensions import Self

from tcc.core.domain import BaseModel
from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.domain.entities.transformer.variation import Variation
from tcc.core.domain.types import DictStrAny

InputData = Variable | pd.Series | None


class Result(BaseModel):
    PerdasT: float | None = None
    Mativa: float | None = None
    PerdasT_P: float | None = None
    Mativa_P: float | None = None
    rank: float | None = None
    crowlingDistance: float | None = None
    fitness: float | None = None
    distance: float | None = None


class Gene(BaseModel):
    data: pd.Series | None = None
    variables: Variable
    results: Result

    def __eq__(self, other: Self) -> bool:
        assert isinstance(other, Gene), "precisa ser gene"
        return (
            self.results == other.results and self.variables == other.variables
        )

    def set_data(self, data: pd.Series) -> Self:
        self.data = data
        return self

    def set_variables(self, variables: Variable) -> Self:
        self.variables = variables
        return self

    def set_results(self, results: Result) -> Self:
        self.results = results
        return self

    def generate_data(self) -> "pd.Series[float]":
        variables = self.variables.dict()
        results = self.results.dict()

        data = list(variables.values()) + list(results.values())
        index = list(variables) + list(results)
        series = pd.Series(
            data=data,
            index=index,
        )
        self.data = series
        return series

    def process_data(self):
        variables_number = len(Variable.get_field_names())

        assert self.data is not None

        variables_data = self.data[0:variables_number]
        results_data = self.data[variables_number:]

        self.set_variables(Variable(**variables_data))  # type: ignore
        self.set_results(Result(**results_data))  # type: ignore

    class Config:
        arbitrary_types_allowed = True


class GeneBuilder:
    variables_field_names = Variable.get_field_names(alias=True)

    @classmethod
    def build(
        cls,
        variations: Variation | None = None,
        data: InputData = None,
    ) -> Gene:
        # if variables is None:
        #     variables = cls.random_create(variations=variations)
        gene = cls.create_gene(data, variations=variations)
        return gene

    def __init__(*args: Any, **kwargs: DictStrAny) -> None:
        raise ValueError

    @functools.singledispatchmethod
    @classmethod
    def create_gene(cls, data, variations: Variation | None = None) -> Gene:
        # assert variations is not None

        # return cls.random_create(variations)
        ...

    @create_gene.register
    @classmethod
    def _(cls, data: Variable, **_):
        results = Result()
        return Gene(variables=data, results=results)

    @create_gene.register
    @classmethod
    def _(cls, data: None, variations: Variation | None = None):
        assert variations is not None
        variables = cls.random_create(variations)
        results = Result()
        return Gene(variables=variables, results=results)

    @create_gene.register
    @classmethod
    def _(cls, data: pd.Series, **_):
        variables_number = len(Variable.get_field_names())

        variables_data = data[0:variables_number]
        results_data = data[variables_number:]

        variables = Variable(**variables_data)  # type: ignore
        results = Result(**results_data)  # type: ignore

        return Gene(variables=variables, results=results, data=data)

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        dict = {
            name: np.random.uniform(value[0], value[1])
            for name, value in variations.dict().items()
        }
        return Variable(**dict)
