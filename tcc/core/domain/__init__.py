from pydantic import BaseModel as PydanticBaseModel


class BaseModel(PydanticBaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        return list(map(str, cls.schema(alias)["properties"].keys()))
