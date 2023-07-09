from math import sqrt

from pydantic import BaseModel

from tcc.core.domain.entities.transformer.constraints import (
    ConnectionEnum,
    Constraint,
)
from tcc.core.domain.entities.transformer.variable import Variable
from tcc.core.domain.entities.transformer.variation import Variation


class Transformer(BaseModel):
    variables: Variable
    variations: Variation
    constraints: Constraint

    def get_voltages(self):
        Vf1, Vf2 = (self.constraints.V1, self.constraints.V2)
        connection = self.constraints.connection

        if self.constraints.NFases == 3:
            if connection.primary == ConnectionEnum.delta:
                Vf1 /= sqrt(3)

            if connection.secondary == ConnectionEnum.delta:
                Vf2 /= sqrt(3)

        return Vf1, Vf2
