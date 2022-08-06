from typing import Optional

import pandas as pd

from tcc.core.domain import BaseModel
from tcc.core.domain.transformer.entities import Variable


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
