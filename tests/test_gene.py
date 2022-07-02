from collections import OrderedDict
from unittest import TestCase
from app.genetic_algorithm.gene import Gene


class TestGeneBasics(TestCase):
    def test_crete_gene(self):
        gene = Gene(range(14))
        gene.abs

    def test_create_random_gene(self):
        gene = Gene()
        gene.abs

    def test_change_the_variations(self):
        variations = OrderedDict(
            {
                "Jbt": (12, 14),
                "Jat": (14, 16),
                "Bm": (15, 16),
                "Ksw": (60, 70),
                "kt": (4.5, 5.5),
                "Rjan": (34, 36),
                "rel": (11, 12),
            }
        )
        gene_01 = Gene()
        gene_01.variations = variations
        gene_02 = Gene()

        self.assertEqual(gene_02.variations, variations)
