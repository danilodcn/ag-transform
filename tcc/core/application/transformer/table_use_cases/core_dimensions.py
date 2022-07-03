from tcc.core.domain.transformer.table_repository import TableRepository


class GetCoreDimensions:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, number_of_steps: int):
        TABLE_NAME = "core_dimensions"

        table = self.table_repository.get(TABLE_NAME)
        Ku = table.data["Ku"][number_of_steps]
        L = table.data["core_dimensions"][number_of_steps]

        assert isinstance(Ku, float)
        assert isinstance(L, float)
        return Ku, L
