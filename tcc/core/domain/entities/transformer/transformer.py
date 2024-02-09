from abc import abstractmethod
from functools import cached_property
from math import sqrt
from typing import Any

import pandas as pd
from pydantic import BaseModel
from typing_extensions import Self

from tcc.core.domain.entities.transformer.constraints import (
    ConnectionEnum,
    Constraint,
)
from tcc.core.domain.entities.transformer.result import Result
from tcc.core.domain.entities.transformer.variable import Variable


class Transformer(BaseModel):
    variables: Variable
    constraints: Constraint
    results: Result

    def get_voltages(self):
        Vf1, Vf2 = (self.constraints.V1, self.constraints.V2)
        connection = self.constraints.connection

        if self.constraints.NFases == 3:
            if connection.primary == ConnectionEnum.delta:
                Vf1 /= sqrt(3)

            if connection.secondary == ConnectionEnum.delta:
                Vf2 /= sqrt(3)

        return Vf1, Vf2

    @cached_property
    def data(self) -> "pd.Series[Any]":
        return self.generate_data()

    @abstractmethod
    def generate_data(self) -> "pd.Series[Any]":
        raise NotImplementedError

    def __eq__(self, other: Self) -> bool:
        assert isinstance(
            other, self.__class__
        ), f"precisa ser {self.__class__}"

        return (
            self.results == other.results and self.variables == other.variables
        )
