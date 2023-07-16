from abc import ABC, abstractmethod

from tcc.core.domain.entities.transformer.transformer import Transformer


class TransformerRunner(ABC):
    @abstractmethod
    def run(self, transformer: Transformer) -> list[float]:
        raise NotImplementedError
