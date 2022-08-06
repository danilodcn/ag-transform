import functools
from typing import Any, Optional

import numpy as np
import pandas as pd

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


class Gene(BaseModel):
    data: Optional[pd.Series] = None
    calculated: bool = False
    variables: Variable
    results: Result

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

    @classmethod
    def get_variables_from_data(cls):
        ...

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
    def _(cls, data: Variable, variations: Optional[Variation] = None):

        return data

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        dict = {
            name: np.random.uniform(*value)
            for name, value in variations.dict().items()
        }
        return Variable(**dict)
