from typing import Any, Optional

import numpy as np
import pandas as pd

from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.transformer.entities import Variable, Variation
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

    @classmethod
    def build(
        cls,
        variations: Variation,
        variables: Optional[Variable] = None,
    ) -> Gene:
        if variables is not None:
            data = list(variables.dict().values())
        else:
            data = cls.random_crete(variations=variations)

        data += [0] * len(cls.result_field_names)
        serie = pd.Series(data=data, index=cls.get_index_names())

        return Gene(data=serie)

    def __init__(*args: Any, **kwargs: DictStrAny) -> None:
        raise ValueError

    @classmethod
    def get_index_names(cls):
        return cls.variables_field_names + cls.result_field_names

    @classmethod
    def random_crete(cls, variations: Variation):
        genes = [
            np.random.uniform(min, max)
            for min, max in variations.dict().values()
        ]

        return genes
