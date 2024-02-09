from typing import Any

import numpy as np

from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetCurveBH(TableAdapter):
    def execute(self, /, **kwargs: Any) -> float:
        B = kwargs["B"]
        TABLE_NAME = TableNameEnum.curve_BH

        table = self.table_repository.get(
            name=TABLE_NAME, table_id=kwargs.get("table_id")
        )
        _B = np.asarray(table.data["B"])
        _H = np.asarray(table.data["H"])

        return float(np.interp(B, _B, _H))
