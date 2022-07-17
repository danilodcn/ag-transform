from pydantic import BaseModel


class BaseModel(BaseModel):
    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias)["properties"].keys())
