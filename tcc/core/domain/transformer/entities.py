from enum import Enum
from typing import Dict, List, NamedTuple

from pydantic import BaseModel


class ConnectionEnum(str, Enum):
    delta = "delta"
    triangle = "triangle"


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


TableDataType = Dict[str, List[float] | List[List[float]]]


class Table(BaseModel):
    name: TableNameEnum
    data: TableDataType
