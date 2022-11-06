import json
import unittest

from tcc.core.application.tools.is_dominated import is_dominated


class TestCreatePopulation(unittest.TestCase):
    def test_is_dominated(self):
        gene1 = [40, 20]
        gene2 = [40, 20]
        expected = False

        self.assertEqual(is_dominated(gene1, gene2), expected)

        gene1 = [60, 40]
        gene2 = [40, 20]
        expected = True

        self.assertEqual(is_dominated(gene1, gene2), expected)

        gene1 = [40, 40]
        gene2 = [40, 20]
        expected = False

        self.assertEqual(is_dominated(gene1, gene2), expected)

        gene1 = [20, 20]
        gene2 = [20, 40]
        expected = False

        self.assertEqual(is_dominated(gene1, gene2), expected)

        gene1 = [30, 40]
        gene2 = [20, 40]
        expected = False

        self.assertEqual(is_dominated(gene1, gene2), expected)
