import numpy as np

from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetCurveBH(TableAdapter):
    def execute(self, /, **kwargs: float) -> float:
        B = kwargs["B"]
        TABLE_NAME = TableNameEnum.curve_BH

        table = self.table_repository.get(TABLE_NAME)
        _B = np.asarray(table.data["B"])
        _H = np.asarray(table.data["H"])

        return float(np.interp(B, _B, _H))
