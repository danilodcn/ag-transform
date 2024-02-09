import uuid
from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.table import Table, TableNameEnum

from ..repository import EntityError, Repository


class TableDoesNotExist(EntityError):
    ...


class TableRepository(Repository, ABC):
    @property
    def DoesNotExist(self) -> EntityError:
        return TableDoesNotExist("Table does not exists")

    @abstractmethod
    def get(
        self, *, name: TableNameEnum, table_id: uuid.UUID | None = None
    ) -> Table:
        raise NotImplementedError

    @abstractmethod
    def insert(self, table: Table) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, tables: list[Table]) -> None:
        raise NotImplementedError
