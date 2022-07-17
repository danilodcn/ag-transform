import pandas as pd

from tcc.core.domain import BaseModel


class Gene(BaseModel):
    data: pd.Series

    class Config:
        arbitrary_types_allowed = True
