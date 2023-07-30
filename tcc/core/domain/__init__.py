from typing import Any

from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    @classmethod
    def get_field_names(cls, alias: bool = False):
        return list(
            map(str, cls.model_json_schema(alias)["properties"].keys())
        )

    def as_dict(self) -> dict[str, Any]:
        return self.model_dump()
