from tcc.core.domain.entities.transformer.table import TableNameEnum
from tcc.core.domain.repositories.table_repository import TableRepository


class GetCoreDimensions:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, number_of_steps: int):
        TABLE_NAME = TableNameEnum.core_dimensions
        number_of_steps -= 1

        table = self.table_repository.get(TABLE_NAME)
        Ku = table.data["Ku"][number_of_steps]
        L = table.data["core_dimensions"][number_of_steps]
        assert isinstance(Ku, float)
        assert isinstance(L, list)
        return Ku, L
