import uuid

from tcc.core.application.registry.registry import Registry

from .transformer import Transformer


class TransformerBuilder:
    @classmethod
    def build(cls, registry: Registry, id: uuid.UUID) -> Transformer:
        ...

    def __init__(self) -> None:
        raise NotImplementedError
