from enum import Enum

from tcc.core.domain import BaseModel

TableDataType = dict[str, list[float] | list[list[float]]]


class TableNameEnum(str, Enum):
    core_dimensions = "core_dimensions"
    core_magnetic_loss = "core_magnetic_loss"
    curve_BH = "curve_BH"
    insulation_type_constant = "insulation_type_constant"
    number_of_steps = "number_of_steps"


class Table(BaseModel):
    name: TableNameEnum
    data: TableDataType
