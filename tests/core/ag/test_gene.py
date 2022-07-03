import os
import unittest

import pandas as pd

from tcc.core.application.transformer.table_use_cases.table_facade import (
    TableFacade,
)
from tcc.core.domain.ag.gene import Gene
from tcc.core.domain.transformer.entities import (
    Table,
    TableNameEnum,
    Variable,
    Variation,
)
from tcc.core.infra.db.memory.transformer.variation_repository import (
    VariationRepositoryInMemory,
)

FILE_NAME = os.getcwd() + "/tests/core/json/tables.json"


class TestCreateGene(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = VariationRepositoryInMemory()

    def test_create_gene(self):
        gene = Gene(self.repository)
        self.assertIsInstance(gene, Gene)

    def teste_data_in_gene_is_Series(self):
        variables = Variable(
            Jbt=1.2, Jat=1.4, Bm=2.3, Ksw=2.5, kt=34, Rjan=2.8, rel=0.7
        )

        gene = Gene(self.repository, variables=variables)
        self.assertIsInstance(gene.data, pd.Series)
