from collections import OrderedDict
from typing import Any

from tcc.core.application.registry.exceptions import (
    DependencyAlreadyExist,
    DependencyNotFound,
)
from tcc.core.application.registry.registry import Registry, empty_register


class ApplicationRegistry(Registry):
    @property
    def __dependencies(self) -> dict[str, Any]:
        dependencies: dict[str, Any] | None = getattr(
            self, "__internal_dependencies", None
        )
        if dependencies is None:
            dependencies = OrderedDict()
            setattr(self, "__internal_dependencies", dependencies)

        return dependencies

    @property
    def count(self):
        return len(self.__dependencies)

    def provide(self, name: str, value: Any) -> None:
        if self.__dependencies.get(name, empty_register) is not empty_register:
            raise DependencyAlreadyExist(
                "dependência '%s' já registrada" % name
            )

        self.__dependencies[name] = value

    def inject(self, name: str) -> Any:
        dependency = self.__dependencies.get(name, empty_register)
        if dependency is not empty_register:
            return dependency

        raise DependencyNotFound(f"dependência '{name}' não registrada")

    def remove(self, name: str) -> Any:
        dependency = self.__dependencies.pop(name, empty_register)

        if dependency is empty_register:
            raise DependencyNotFound(
                f"dependência '{name}' não registrada. Impossível apagar"
            )

        return dependency
