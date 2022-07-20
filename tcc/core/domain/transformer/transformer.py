from math import sqrt
from typing import Type, TypeVar
from uuid import uuid4

from pydantic import UUID4, BaseModel, Field

from tcc.core.domain.transformer.entities import (
    ConnectionEnum,
    Constraint,
    Variable,
    Variation,
)

Model = TypeVar("Model", bound="Transformer")


class Transformer(BaseModel):
    uuid: UUID4 = Field(default_factory=uuid4)
    variables: Variable
    variations: Variation
    constraints: Constraint

    def __eq__(self, other: Type["Model"]) -> bool:
        return self.uuid == other.uuid

    def get_voltages(self):

        Vf1, Vf2 = (self.constraints.V1, self.constraints.V2)
        connection = self.constraints.connection

        if self.constraints.NFases == 3:
            if connection.primary == ConnectionEnum.delta:
                Vf1 /= sqrt(3)

            if connection.secondary == ConnectionEnum.delta:
                Vf2 /= sqrt(3)

        return Vf1, Vf2
