from enum import Enum
from typing import Dict, List, NamedTuple, Tuple

from tcc.core.domain import BaseModel


class ConnectionEnum(str, Enum):
    delta = "delta"
    star = "star"


class TableNameEnum(str, Enum):
    core_dimensions = "core_dimensions"
    core_magnetic_loss = "core_magnetic_loss"
    curve_BH = "curve_BH"
    insulation_type_constant = "insulation_type_constant"
    number_of_steps = "number_of_steps"


class Connection(NamedTuple):
    primary: ConnectionEnum
    secondary: ConnectionEnum


class Constraint(BaseModel):
    connection: Connection
    Ke: float
    S: float
    NFases: int
    f: float
    V1: float
    V2: float
    type: str
    Dfe: float
    Dal: float


class Variable(BaseModel):
    Jbt: float
    Jat: float
    Bm: float
    Ksw: float
    kt: float
    Rjan: float
    rel: float


VariationTuple = Tuple[float, float, int]


class Variation(BaseModel):
    Jbt: VariationTuple
    Jat: VariationTuple
    Bm: VariationTuple
    Ksw: VariationTuple
    kt: VariationTuple
    Rjan: VariationTuple
    rel: VariationTuple


TableDataType = Dict[str, List[float] | List[List[float]]]


class Table(BaseModel):
    name: TableNameEnum
    data: TableDataType
