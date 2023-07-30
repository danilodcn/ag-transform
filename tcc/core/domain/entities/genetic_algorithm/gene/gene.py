from typing import Any

import pandas as pd
from typing_extensions import Self

from tcc.core.domain.entities.individuo import Individuo
from tcc.core.domain.entities.transformer.variable import Variable

from .gene_result import GeneResult


class Gene(Individuo):
    def set_variables(self, variables: Variable) -> Self:
        self.variables = variables
        return self

    def set_results(self, results: GeneResult) -> Self:
        self.results = results
        return self

    def generate_data(self) -> "pd.Series[Any]":
        variables = self.variables.as_dict()
        results = self.results.as_dict()

        data = list(variables.values()) + list(results.values())
        index = list(variables) + list(results)
        series = pd.Series(
            data=data,
            index=index,
        )

        return series  # type: ignore
