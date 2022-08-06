import itertools as it
from typing import Any, List, Optional

import pandas as pd

from tcc.core.application.genetic_algorithm.gene.gene_builder import (
    GeneBuilder,
)
from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationProps,
)
from tcc.core.domain.transformer.entities import Variation

__all__ = ["PopulationBuilder"]


class PopulationBuilder:
    @classmethod
    def build(
        cls,
        props: PopulationProps,
        variations: Variation,
        data: Optional[List[Any] | pd.DataFrame] = None,
    ) -> Population:
        if data is None:
            data = cls.random_generate(
                n_population=props.n_population,
                variations=variations,
            )

        index = pd.Index(data=range(len(data)))
        return Population(
            data=pd.DataFrame(data=data, index=index), props=props
        )

    @classmethod
    def random_generate(
        cls, n_population: int, variations: Variation
    ) -> List[Gene]:
        genes = map(GeneBuilder.build, it.repeat(variations, n_population))
        data = [gene for gene in genes]

        return data
