from enum import Enum
from typing import Dict, List, NamedTuple

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


class Table(BaseModel):
    name: str
    data: Dict[str, List[float] | List[List[float]]]
