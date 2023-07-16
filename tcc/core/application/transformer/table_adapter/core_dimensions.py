from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetCoreDimensions(TableAdapter):
    def execute(self, /, **kwargs: int):
        number_of_steps = kwargs["number_of_steps"]
        TABLE_NAME = TableNameEnum.core_dimensions
        number_of_steps -= 1

        table = self.table_repository.get(TABLE_NAME)
        Ku = table.data["Ku"][number_of_steps]
        L = table.data["core_dimensions"][number_of_steps]
        assert isinstance(Ku, float)
        assert isinstance(L, list)
        return Ku, L
