from abc import ABC, abstractmethod
from typing import Any

from tcc.core.application.registry import Registry, RegistryType
from tcc.core.domain.repositories.transformer.table_repository import (
    TableRepository,
)


class TableAdapter(ABC):
    def __init__(self, *, registry: Registry) -> None:
        self.table_repository: TableRepository = registry.inject(
            RegistryType.TABLE_REPOSITORY
        )

    @abstractmethod
    def execute(self, /, **kwargs: Any) -> Any:
        raise NotImplementedError
