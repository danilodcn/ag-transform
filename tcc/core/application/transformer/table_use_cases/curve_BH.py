import numpy as np

from tcc.core.domain.transformer.entities import TableNameEnum
from tcc.core.domain.transformer.table_repository import TableRepository


class GetCurveBH:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, B: float) -> float:
        TABLE_NAME = TableNameEnum.curve_BH

        table = self.table_repository.get(TABLE_NAME)
        _B = np.asarray(table.data["B"])
        _H = np.asarray(table.data["H"])

        return float(np.interp(B, _B, _H))
