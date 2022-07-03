import numpy as np

from tcc.core.domain.transformer.table_repository import TableRepository


class GetCurveBH:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, Bm: float) -> float:
        TABLE_NAME = "curve_BH"

        table = self.table_repository.get(TABLE_NAME)
        B = np.asarray(table.data["B"])
        H = np.asarray(table.data["H"])

        return float(np.interp(Bm, B, H))
