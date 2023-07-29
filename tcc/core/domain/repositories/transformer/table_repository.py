from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.table import Table, TableNameEnum

from ..repository import EntityDoesNotExist, Repository


class TableDoesNotExist(EntityDoesNotExist):
    ...


class TableRepository(Repository, ABC):
    @property
    def DoesNotExist(self) -> EntityDoesNotExist:
        return TableDoesNotExist("Table does not exists")

    @abstractmethod
    def get(self, name: TableNameEnum) -> Table:
        raise NotImplementedError

    @abstractmethod
    def insert(self, table: Table) -> None:
        raise NotImplementedError

    @abstractmethod
    def insert_many(self, tables: list[Table]) -> None:
        raise NotImplementedError
