from typing import Any

import numpy as np
import pandas as pd

from tcc.core.domain.entities.transformer.constraints import Constraint
from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.domain.entities.transformer.variation import Variation

from .gene import Gene
from .gene_result import GeneResult


class GeneBuilder:
    @classmethod
    def build(
        cls,
        constraints: Constraint,
        variations: Variation,
        data: "Variable | pd.Series[float] | None" = None,
        random_create: bool = False,
    ) -> Gene:
        # assert data is None and not random_create,
        # "para gerar gene aleatório passe `random_create=True`"
        results = GeneResult()

        if isinstance(data, Variable):
            return Gene(
                variables=data,
                variations=variations,
                constraints=constraints,
                results=results,
            )

        if isinstance(data, pd.Series):
            return cls.from_data(
                data, variations=variations, constraints=constraints
            )

        assert variations is not None
        variables = cls.random_create(variations)
        return Gene(variables=variables, results=GeneResult())

    def __init__(*args: Any, **kwargs: Any) -> None:
        raise NotImplementedError(
            "classe builder nao pode nao pode ser instanciada"
        )

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        data = {  # type: ignore
            name: np.random.uniform(value[0], value[1])
            for name, value in variations.as_dict().items()
        }
        return Variable(**data)  # type: ignore

    @classmethod
    def from_data(
        cls,
        data: "pd.Series[float]",
        constraints: Constraint,
        variations: Variation,
    ) -> Gene:
        variables_number = len(Variable.get_field_names())

        variables_data = data[0:variables_number]  # type: ignore
        results_data = data[variables_number:]  # type: ignore

        variables = Variable(**variables_data)  # type: ignore
        results = GeneResult(**results_data)  # type: ignore

        return Gene(
            variables=variables,
            results=results,
            variations=variations,
            constraints=constraints,
        )
