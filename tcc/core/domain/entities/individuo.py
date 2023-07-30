from abc import ABC, abstractmethod
from functools import cached_property
from typing import Any

import pandas as pd
from typing_extensions import Self

from tcc.core.domain import BaseModel
from tcc.core.domain.entities.result import Result
from tcc.core.domain.entities.transformer.variable import Variable


class Individuo(BaseModel, ABC):
    variables: Variable
    results: Result

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
