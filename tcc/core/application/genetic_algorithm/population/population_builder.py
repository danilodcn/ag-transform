import itertools as it
from typing import Any, List, Optional

import pandas as pd

from tcc.core.application.genetic_algorithm.gene.gene_builder import (
    GeneBuilder,
)
from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationProps,
)
from tcc.core.domain.transformer.entities import Variation
from tcc.core.domain.transformer.transformer import Transformer

__all__ = ["PopulationBuilder"]


class PopulationBuilder:
    @classmethod
    def build(
        cls,
        props: PopulationProps,
        transformer: Transformer,
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
            data=pd.DataFrame(data=data, index=index),
            props=props,
            transformer=transformer,
        )

    @classmethod
    def random_generate(
        cls, n_population: int, variations: Variation
    ) -> List[pd.Series]:
        genes = map(GeneBuilder.build, it.repeat(variations, n_population))
        data = [gene.data for gene in genes]

        return data
