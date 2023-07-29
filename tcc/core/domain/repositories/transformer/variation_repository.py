from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.variation import Variation

from ..repository import EntityDoesNotExist, Repository


class VariationDoesNotExistError(EntityDoesNotExist):
    ...


class VariationRepository(Repository, ABC):
    @property
    def DoesNotExist(self):
        return VariationDoesNotExistError(
            "Variation not found!",
        )

    @abstractmethod
    def get(self, id: str | None) -> Variation:
        raise NotImplementedError

    @abstractmethod
    def insert(self, variation: Variation) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, variations: list[Variation]) -> None:
        raise NotImplementedError
