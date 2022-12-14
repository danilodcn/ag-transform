from abc import ABC, abstractmethod
from typing import List

from tcc.core.domain.transformer.entities import Table, TableNameEnum


class TableRepository(ABC):
    @abstractmethod
    def get(self, name: TableNameEnum) -> Table:
        raise NotImplementedError

    def insert(self, table: Table) -> None:
        raise NotImplementedError

    def insert_many(self, tables: List[Table]) -> None:
        raise NotImplementedError
