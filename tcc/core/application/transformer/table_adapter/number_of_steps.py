from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetNumberOfSteps(TableAdapter):
    def execute(self, /, **kwargs: float):
        area = kwargs["area"]
        TABLE_NAME = TableNameEnum.number_of_steps
        if area >= 200 or area <= 0:
            raise ValueError("A a area nao pode ser maior 0.2 m² nem menor 0")

        table = self.table_repository.get(TABLE_NAME)
        first_item = table.data.get("1")
        if isinstance(first_item, list) and isinstance(first_item[0], float):
            if area < first_item[0]:
                return 1

            for key, value in table.data.items():
                i, j = value
                assert isinstance(i, float)
                assert isinstance(j, float)

                if i <= area < j:
                    return int(key)

        raise ValueError
