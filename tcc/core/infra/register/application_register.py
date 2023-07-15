from typing import Any

from tcc.core.application.register.exceptions import (
    DependencyAlreadyExist,
    DependencyNotFound,
)
from tcc.core.application.register.register import Empty, Register


class ApplicationRegister(Register):
    @property
    def dependencies(self) -> dict[str, Any]:
        dependencies: dict[str, Any] | None = getattr(
            self, "__dependencies", None
        )
        if dependencies is None:
            dependencies = {}
            setattr(self, "__dependencies", dependencies)

        return dependencies

    def provide(self, name: str, value: Any) -> None:
        if self.dependencies.get(name, Empty()) is not Empty():
            raise DependencyAlreadyExist(
                "dependência '%s' já registrada" % name
            )

        self.dependencies[name] = value

    def inject(self, name: str) -> Any:
        dependency = self.dependencies.get(name, Empty())
        if dependency is not Empty():
            return dependency

        raise DependencyNotFound(f"dependência '{name}' não registrada")
