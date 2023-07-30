from abc import ABC

from tcc.core.domain import BaseModel


class Result(BaseModel, ABC):
    PerdasT: float | None = None
    Mativa: float | None = None
