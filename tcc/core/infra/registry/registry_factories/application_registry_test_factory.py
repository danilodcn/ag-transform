from tcc.core.application.registry import RegistryType
from tcc.core.application.registry.factory_registry import RegistryFactory
from tcc.core.application.transformer.runners.transformer_three_phase_runner import (  # noqa
    TransformerThreePhaseRunner,
)

from ..application_registry import ApplicationRegistry


class ApplicationRegistryTestFactory(RegistryFactory):
    def create(self):
        registry = ApplicationRegistry()

        registry.provide(
            RegistryType.TRANSFORMER_RUNNER,
            TransformerThreePhaseRunner(registry=registry),
        )

        return registry
