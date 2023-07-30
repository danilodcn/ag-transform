import unittest

import pandas as pd

from tcc.core.domain.entities.genetic_algorithm.gene.gene_builder import (
    Gene,
    GeneBuilder,
    GeneResult,
)
from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (  # noqa
    VariationRepositoryInMemory,
)


class TestCreateGene(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = VariationRepositoryInMemory()
        self.variations = self.repository.get()

        self.variables = Variable(
            Jbt=1.2, Jat=1.4, Bm=2.3, Ksw=2.5, kt=34, Rjan=2.8, rel=0.7
        )

    def test_create_gene(self):
        gene = GeneBuilder.build(
            variations=self.variations, random_create=True
        )

        self.assertIsInstance(gene, Gene)

    def test_data_in_gene_is_cached(self):
        assert self.variables
        gene = GeneBuilder.build(
            variations=self.variations, data=self.variables
        )

        id_first = id(gene.data)
        id_second = id(gene.data)

        self.assertEqual(id_first, id_second)

    def test_data_is_Serie_when_execute_generate_data(self):
        gene = GeneBuilder.build(
            variations=self.variations, random_create=True
        )

        self.assertIsInstance(gene.data, pd.Series)

    def test_change_variation_and_result_on_handle_data(self):
        gene = GeneBuilder.build(
            variations=self.variations, random_create=True
        )
        Jat = 3
        Mativa = 800
        data = gene.generate_data()

        data["Jat"] = Jat
        data["Mativa"] = Mativa

        new_gene = GeneBuilder.from_data(data)

        self.assertEqual(new_gene.variables.Jat, Jat)
        self.assertEqual(new_gene.results.Mativa, Mativa)

    def test_index_of_gene_is_list_titles_of_variables_and_results(self):
        gene = GeneBuilder.build(variations=self.variations)
        gene.generate_data()
        assert gene.data is not None

        expected_index = (
            Variable.get_field_names() + GeneResult.get_field_names()
        )
        expected_number = len(expected_index)
        number = len(gene.data)
        index = gene.data.index

        equal_all = all([x == y for x, y in zip(index, expected_index)])

        self.assertEqual(number, expected_number)
        self.assertTrue(equal_all, f"\n{index=}\n{expected_index=}")
        self.assertIsInstance(gene, Gene)
