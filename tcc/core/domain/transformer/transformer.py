from math import sqrt

from pydantic import BaseModel

from .entities import ConnectionEnum, Constraint, Variable


class Transformer(BaseModel):
    variables: Variable
    constraints: Constraint

    def get_voltages(self):

        Vf1, Vf2 = (self.constraints.V1, self.constraints.V2)
        connection = self.constraints.connection
        if self.constraints.NFases == 3:
            if connection.primary == ConnectionEnum.triangle:
                Vf1 /= sqrt(3)

            if connection.secondary == ConnectionEnum.triangle:
                Vf2 /= sqrt(3)

        return Vf1, Vf2
