from abc import ABC, abstractmethod
from typing import List, Optional

from tcc.core.domain.entities.transformer.variation import Variation


class VariationDoesNotExistError(Exception):
    ...


class VariationRepository(ABC):
    DoesNotExist = VariationDoesNotExistError(
        "Variation not found!",
    )

    @abstractmethod
    def get(self, id: Optional[int]) -> Variation:
        raise NotImplementedError

    @abstractmethod
    def insert(self, variation: Variation) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, variations: List[Variation]) -> None:
        raise NotImplementedError
