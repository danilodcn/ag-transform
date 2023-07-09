from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.variation import Variation


class VariationDoesNotExistError(Exception):
    ...


class VariationRepository(ABC):
    DoesNotExist = VariationDoesNotExistError(
        "Variation not found!",
    )

    @abstractmethod
    def get(self, id: int) -> Variation:
        raise NotImplementedError

    @abstractmethod
    def insert(self, variation: Variation) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, variations: list[Variation]) -> None:
        raise NotImplementedError
