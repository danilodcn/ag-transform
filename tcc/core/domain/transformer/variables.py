from pydantic import BaseModel


class Constraint(BaseModel):
    Jbt: float
    Jat: float
    Bm: float
    Ksw: float
    kt: float
    Rjan: float
    rel: float
