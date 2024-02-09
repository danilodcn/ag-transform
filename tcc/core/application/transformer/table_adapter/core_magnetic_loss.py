from typing import Any

import numpy as np

from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetCoreMagneticLoss(TableAdapter):
    def execute(self, /, **kwargs: Any) -> float:
        B = kwargs["B"]
        TABLE_NAME = TableNameEnum.core_magnetic_loss

        table = self.table_repository.get(
            name=TABLE_NAME, table_id=kwargs.get("table_id")
        )
        magnetic_induction = np.asarray(table.data["induction"])
        magnetic_loss = np.asarray(table.data["loss"])

        return float(np.interp(B, magnetic_induction, magnetic_loss))
