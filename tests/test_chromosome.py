from collections import OrderedDict
from unittest import TestCase
from app.genetic_algorithm.chromosome import Chromosome


class TestCromossomeBasics(TestCase):
    def test_crete_chromosome(self):
        chromosome = Chromosome(range(7))
    
    def test_create_random_chromosome(self):
        chromosome = Chromosome()

    def test_change_the_variations(self):
        variations = OrderedDict({
                "Jbt": (12, 14),
                "Jat": (14, 16),
                "Bm": (15, 16),
                "Ksw": (60, 70),
                "kt": (4.5, 5.5),
                "Rjan": (34, 36),
                "rel": (11, 12),
                })
        chromosome_01 = Chromosome()
        chromosome_01.variations = variations
        chromosome_02 = Chromosome()
        self.assertEqual(chromosome_02.variations, variations)