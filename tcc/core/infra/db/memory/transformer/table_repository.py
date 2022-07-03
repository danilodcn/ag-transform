import json
from typing import Dict

from tcc.core.domain.transformer.entities import Table, TableDataType, TableNameEnum
from tcc.core.domain.transformer.table_repository import TableRepository


class TableRepositoryInMemory(TableRepository):
    _tables: Dict[str, TableDataType]

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
            return Table(name=name, data=table)
