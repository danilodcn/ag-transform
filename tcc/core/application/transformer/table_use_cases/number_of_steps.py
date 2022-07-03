from tcc.core.domain.transformer.table_repository import TableRepository


class GetNumberOfSteps:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, area: float):
        TABLE_NAME = "number_of_steps"
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
