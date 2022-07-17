from typing import Any, List, Optional

import numpy as np
import pandas as pd

from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.transformer.entities import Variable
from tcc.core.domain.transformer.variation_repository import (
    VariationRepository,
)
from tcc.core.domain.types import DictStrAny


class GeneBuilder:
    variables_field_names = Variable.get_field_names(alias=True)
    result_field_names = [
        "PerdasT",
        "Mativa",
        "PerdasT_P",
        "Mativa_P",
        "rank",
        "crowlingDistance",
        "fitness",
    ]

    repository: VariationRepository

    @classmethod
    def build(
        cls,
        variation_repository: VariationRepository,
        variables: Optional[Variable] = None,
    ) -> Gene:
        cls.repository = variation_repository
        if variables is not None:
            data = list(variables.dict().values())
        else:
            data = cls.random_crete()

        data += [0] * len(cls.result_field_names)
        serie = pd.Series(data=data, index=cls.get_index_names())

        return Gene(data=serie)

    def __init__(*args: Any, **kwargs: DictStrAny) -> None:
        raise ValueError

    @classmethod
    def get_index_names(cls) -> List[str]:
        return cls.variables_field_names + cls.result_field_names

    @classmethod
    def random_crete(cls, id: Optional[int] = None):
        variation = cls.repository.get(id=id)

        genes = [
            np.random.uniform(min, max)
            for min, max in variation.dict().values()
        ]

        return genes
