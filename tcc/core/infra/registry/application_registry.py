from collections import OrderedDict
from typing import Any

from tcc.core.application.registry.exceptions import (
    DependencyAlreadyExist,
    DependencyNotFound,
)
from tcc.core.application.registry.registry import Registry, empty_register


class ApplicationRegistry(Registry):
    @property
    def dependencies(self) -> dict[str, Any]:
        dependencies: dict[str, Any] | None = getattr(
            self, "__dependencies", None
        )
        if dependencies is None:
            dependencies = OrderedDict()
            setattr(self, "__dependencies", dependencies)

        return dependencies

    def provide(self, name: str, value: Any) -> None:
        if self.dependencies.get(name, empty_register) is not empty_register:
            raise DependencyAlreadyExist(
                "dependência '%s' já registrada" % name
            )

        self.dependencies[name] = value

    def inject(self, name: str) -> Any:
        dependency = self.dependencies.get(name, empty_register)
        if dependency is not empty_register:
            return dependency

        raise DependencyNotFound(f"dependência '{name}' não registrada")
