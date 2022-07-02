from enum import Enum
from typing import NamedTuple

from pydantic import BaseModel


class ConnectionEnum(str, Enum):
    delta = "delta"
    triangle = "triangle"


class Connection(NamedTuple):
    primary: ConnectionEnum
    secondary: ConnectionEnum


class Constraint(BaseModel):
    connection: Connection
    Ke: float
    S: float
    Nfases: int
    f: float
    V1: float
    V2: float
    type: str
    Dfe: float
    Dal: float
