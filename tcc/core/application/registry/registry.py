from abc import ABC, abstractmethod
from typing import Any

from tcc.core.application.singleton.singleton import SingletonMeta


class Empty(metaclass=SingletonMeta):
    ...


empty_register: Empty = Empty()


class Registry(ABC):
    @abstractmethod
    def provide(self, name: str, value: Any) -> None:
        ...

    def inject(self, name: str) -> Any:
        ...

    @abstractmethod
    def remove(self, name: str) -> None:
        ...
