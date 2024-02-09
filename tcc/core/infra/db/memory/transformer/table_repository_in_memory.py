import json
import uuid
from typing import Any, Callable

from tcc.core.domain.entities.transformer.table import Table, TableNameEnum
from tcc.core.domain.repositories.transformer.table_repository import (  # noqa
    TableRepository,
)

SearchFunc = Callable[[dict[str, Any]], bool]


class TableRepositoryInMemory(TableRepository):
    _tables: list[dict[str, Any]]

    def __init__(self, table_name: str) -> None:
        self.__load_tables(table_name)

    @property
    def tables(self):
        if getattr(self, "_tables", None) is None:
            raise ValueError(
                """
                Voce deve inicializar as tabelas usando
                o método repository.load_tables(name)
                """
            )
        return self._tables

    def __load_tables(self, file_name: str) -> None:
        with open(file=file_name, mode="r") as file:
            self._tables = json.load(file)

    def get(
        self, *, name: TableNameEnum, table_id: uuid.UUID | None = None
    ) -> Table:
        if table_id is None:
            filtered_func: SearchFunc = lambda i: i["default"]
        else:
            filtered_func: SearchFunc = lambda i: i["id"]

        tables = filter(filtered_func, self.tables)

        try:
            return Table(**next(tables)[name])
        except Exception as error:
            raise self.DoesNotExist from error

    def insert(self, table: Table) -> None:
        raise NotImplementedError

    def insert_many(self, tables: list[Table]) -> None:
        raise NotImplementedError
