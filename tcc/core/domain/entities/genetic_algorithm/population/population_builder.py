import itertools

import pandas as pd

from tcc.core.domain.entities.transformer.variation import Variation

from ..gene.gene import Gene
from ..gene.gene_builder import GeneBuilder
from ..population.props import PopulationProps
from .population import Population


class PopulationBuilder:
    n_population: int
    variations: Variation

    @classmethod
    def build(
        cls,
        props: PopulationProps,
        variations: Variation,
        data: list[Gene] | None = None,
        random_create: float = False,
    ) -> Population:
        if data is None or random_create:
            data = cls.random_generate(
                n_population=props.n_population,
                variations=variations,
            )

        return Population(props=props, genes=data)

    @classmethod
    def random_generate(
        cls, n_population: int, variations: Variation
    ) -> list[Gene]:
        genes = map(
            GeneBuilder.build, itertools.repeat(variations, n_population)
        )
        data = [gene for gene in genes]

        return data

    @classmethod
    def from_data(cls, data: "pd.DataFrame"):
        genes: "pd.Series[Gene]" = data.apply(  # type: ignore
            lambda d: GeneBuilder.build(data=d),  # type: ignore
            axis=1,
        )
        genes = list(genes)  # type: ignore
        return genes
