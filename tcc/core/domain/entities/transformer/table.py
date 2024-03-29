import uuid
from enum import Enum

from pydantic import Field

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


class Tables(BaseModel):
    tables: list[Table]
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
