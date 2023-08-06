import pytest
from tcc.core.infra.registry.registry_factories.application_registry_test_factory import ApplicationRegistryTestFactory # noqa


@pytest.fixture(scope="module")
def test_registry():
    factory = ApplicationRegistryTestFactory()
    yield factory.create()
