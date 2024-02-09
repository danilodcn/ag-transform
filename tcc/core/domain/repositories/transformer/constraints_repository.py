from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.constraints import Constraint

from ..repository import EntityError, Repository


class VariationDoesNotExistError(EntityError):
    ...


class VariationRepository(Repository, ABC):
    @property
    def DoesNotExist(self):
        return VariationDoesNotExistError(
            "Constraint not found!",
        )

    @abstractmethod
    def get(self, id: str | None) -> Constraint:
        raise NotImplementedError
