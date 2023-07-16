from abc import ABC, abstractmethod
from typing import Any

from tcc.core.application.register import Register, RegisterType
from tcc.core.domain.repositories.table_repository import TableRepository


class TableAdapter(ABC):
    def __init__(self, register: Register) -> None:
        self.table_repository: TableRepository = register.inject(
            RegisterType.TABLE_REPOSITORY
        )

    @abstractmethod
    def execute(self, /, **kwargs: Any) -> Any:
        raise NotImplementedError
