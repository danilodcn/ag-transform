import unittest
import pytest

from tcc.core.application.registry.factory_registry import RegistryFactory
from tcc.core.application.registry.registry import Registry


class TestRegistryFactory(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def prepare_fixture(self, test_registry: RegistryFactory):
        self.test_registry = test_registry

    def test_should_create_registry_class(self):
        self.assertIsInstance(self.test_registry, Registry)
