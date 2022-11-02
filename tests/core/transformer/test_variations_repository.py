import os
import unittest

from tcc.core.domain.transformer.entities import Variation
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
    VariationRepositoryInMemory,
)


class TestTablesRepository(unittest.TestCase):
    def setUp(self) -> None:
        self.repository = VariationRepositoryInMemory()

    def test_should_read_default_variation(self):
        variation = self.repository.get()
        self.assertIsInstance(variation, Variation)

    def test_search_for_not_exist_variation_on_memory(self):
        with self.assertRaises(
            self.repository.DoesNotExist.__class__
        ) as context:
            self.repository.get(id="918253ec-6e12-4226-8f6b-7fbdda5a3b83")
        self.assertIn("not found", str(context.exception))
