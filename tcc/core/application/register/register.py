from abc import ABC, abstractmethod, abstractproperty
from typing import Any

from tcc.core.application.singleton.singleton import SingletonMeta


class Empty(metaclass=SingletonMeta):
    ...


class Register(ABC):
    @abstractproperty
    def dependencies(self) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    def provide(self, name: str, value: Any) -> None:
        raise NotImplementedError

    def inject(self, name: str) -> Any:
        raise NotImplementedError
