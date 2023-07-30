from typing import Any

import numpy as np
import pandas as pd

from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.domain.entities.transformer.variation import Variation

from .gene import Gene
from .gene_result import GeneResult


class GeneBuilder:
    variables_field_names = Variable.get_field_names(alias=True)

    @classmethod
    def build(
        cls,
        variations: Variation | None = None,
        data: "Variable | pd.Series[float] | None" = None,
        random_create: bool = False,
    ) -> Gene:
        # assert data is None and not random_create,
        # "para gerar gene aleatório passe `random_create=True`"

        if isinstance(data, Variable):
            return Gene(variables=data, results=GeneResult())  # type: ignore

        if isinstance(data, pd.Series):
            return cls.from_data(data)

        assert variations is not None
        variables = cls.random_create(variations)
        return Gene(variables=variables, results=GeneResult())

    def __init__(*args: Any, **kwargs: Any) -> None:
        raise ValueError

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        data = {  # type: ignore
            name: np.random.uniform(value[0], value[1])
            for name, value in variations.as_dict().items()
        }
        return Variable(**data)  # type: ignore

    @classmethod
    def from_data(cls, data: "pd.Series[float]"):
        variables_number = len(Variable.get_field_names())

        variables_data = data[0:variables_number]  # type: ignore
        results_data = data[variables_number:]  # type: ignore

        variables = Variable(**variables_data)  # type: ignore
        results = GeneResult(**results_data)  # type: ignore

        return Gene(variables=variables, results=results)
