import numpy as np

from tcc.core.domain.entities.transformer.table import TableNameEnum
from tcc.core.domain.repositories.table_repository import TableRepository


class GetCoreMagneticLoss:
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def execute(self, B: float) -> float:
        TABLE_NAME = TableNameEnum.core_magnetic_loss

        table = self.table_repository.get(TABLE_NAME)
        magnetic_induction = np.asarray(table.data["induction"])
        magnetic_loss = np.asarray(table.data["loss"])

        return float(np.interp(B, magnetic_induction, magnetic_loss))
