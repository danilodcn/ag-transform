from typing import List, Optional

import numpy as np
import pandas as pd

from tcc.core.domain.transformer.entities import Variable
from tcc.core.domain.transformer.variation_repository import (
    VariationRepository,
)


class Gene:
    data: pd.Series
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

    def __init__(
        self,
        variation_repository: VariationRepository,
        variables: Optional[Variable] = None,
    ) -> None:
        self.variation_repository = variation_repository

        if variables is not None:
            data = list(variables.dict().values())
        else:
            data = self.random_crete()

        data += [0] * len(self.result_field_names)

        self.data = pd.Series(data=data, index=self.get_index_names())

    def get_index_names(self) -> List[str]:
        return self.variables_field_names + self.result_field_names

    def random_crete(self, id: Optional[int] = None):
        variation = self.variation_repository.get(id=id)

        genes = [
            np.random.uniform(min, max)
            for min, max in variation.dict().values()
        ]

        return genes
