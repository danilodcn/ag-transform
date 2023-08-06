from abc import ABC, abstractmethod

from .registry import Registry


class RegistryFactory(ABC):
    @abstractmethod
    def create(self) -> Registry:
        raise NotImplementedError
