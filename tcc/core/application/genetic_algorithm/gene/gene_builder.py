from typing import Any, Optional

import numpy as np

from tcc.core.domain.genetic_algorithm.gene import Gene, Result
from tcc.core.domain.transformer.entities import Variable, Variation
from tcc.core.domain.types import DictStrAny


class GeneBuilder:
    variables_field_names = Variable.get_field_names(alias=True)

    # @functools.singledispatch
    @classmethod
    def build(
        cls,
        variations: Variation,
        variables: Optional[Variable] = None,
    ) -> Gene:
        if variables is None:
            variables = cls.random_create(variations=variations)

        results = Result()
        return Gene(results=results, variables=variables)

    def __init__(*args: Any, **kwargs: DictStrAny) -> None:
        raise ValueError

    @classmethod
    def random_create(cls, variations: Variation) -> Variable:
        dict = {
            name: np.random.uniform(*value)
            for name, value in variations.dict().items()
        }
        return Variable(**dict)
