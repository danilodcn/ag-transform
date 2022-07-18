import os
import unittest

import pandas as pd

from tcc.core.application.genetic_algorithm.gene.gene_builder import (
    GeneBuilder,
)
from tcc.core.domain.genetic_algorithm.gene import Gene
from tcc.core.domain.transformer.entities import Variable
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
    VariationRepositoryInMemory,
)


class TestCreateGene(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = VariationRepositoryInMemory()
        self.variations = self.repository.get()

    def test_create_gene(self):
        gene = GeneBuilder.build(variations=self.variations)
        self.assertIsInstance(gene, Gene)

    def teste_data_in_gene_is_Series(self):
        variables = Variable(
            Jbt=1.2, Jat=1.4, Bm=2.3, Ksw=2.5, kt=34, Rjan=2.8, rel=0.7
        )

        gene = GeneBuilder.build(
            variations=self.variations, variables=variables
        )

        self.assertIsInstance(gene.data, pd.Series)
