from enum import Enum
from typing import NamedTuple

from tcc.core.domain import BaseModel


class ConnectionEnum(str, Enum):
    delta = "delta"
    star = "star"


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
