import json
from typing import Any

from tcc.core.domain.entities.transformer.table import Table, TableNameEnum
from tcc.core.domain.repositories.table_repository import TableRepository


class TableRepositoryInMemory(TableRepository):
    _tables: Any

    def __init__(self, table_name: str) -> None:
        self.load_tables(table_name)

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

    def load_tables(self, file_name: str) -> None:
        with open(file=file_name, mode="r") as file:
            self._tables = json.load(file)

    def get(self, name: TableNameEnum) -> Table:
        table = self.tables.get(name, None)
        if table is None:
            raise KeyError(f"A tabela '{name}' não existe")
        else:
            return Table(name=name, data=table["data"])

    def insert(self, table: Table) -> None:
        raise NotImplementedError

    def insert_many(self, tables: list[Table]) -> None:
        raise NotImplementedError
