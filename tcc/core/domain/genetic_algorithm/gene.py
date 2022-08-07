import functools
from typing import Any, Optional

import numpy as np
import pandas as pd
from typing_extensions import Self

from tcc.core.domain import BaseModel
from tcc.core.domain.transformer.entities import Variable, Variation
from tcc.core.domain.types import DictStrAny

InputData = Optional[Variable | pd.Series]


class Result(BaseModel):
    PerdasT: Optional[float] = None
    Mativa: Optional[float] = None
    PerdasT_P: Optional[float] = None
    Mativa_P: Optional[float] = None
    rank: Optional[float] = None
    crowlingDistance: Optional[float] = None
    fitness: Optional[float] = None
    calculated: float = False


class Gene(BaseModel):
    data: Optional[pd.Series] = None
    variables: Variable
    results: Result

    def set_data(self, data: pd.Series) -> Self:
        self.data = data
        return self

    def set_variables(self, variables: Variable) -> Self:
        self.variables = variables
        return self

    def set_results(self, results: Result) -> Self:
        self.results = results
        return self

    def generate_data(self) -> None:
        variables = self.variables.dict()
        results = self.results.dict()

        data = list(variables.values()) + list(results.values())
        index = list(variables) + list(results)
        series = pd.Series(
            data=data,
            index=index,
        )
        self.data = series

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
        variations: Variation,
        data: InputData = None,
        # variables: Optional[Variable] = None,
    ) -> Gene:
        # if variables is None:
        #     variables = cls.random_create(variations=variations)
        variables = cls.get_variable(data, variations=variations)
        results = Result()
        return Gene(results=results, variables=variables)

    def __init__(*args: Any, **kwargs: DictStrAny) -> None:
        raise ValueError

    @functools.singledispatchmethod
    @classmethod
    def get_variable(
        cls, data: None = None, variations: Optional[Variation] = None
    ) -> Variable:
        assert variations is not None

        return cls.random_create(variations)

    @get_variable.register
    @classmethod
    def _(cls, data: Variable, **_):

        return data

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        dict = {
            name: np.random.uniform(*value)
            for name, value in variations.dict().items()
        }
        return Variable(**dict)
