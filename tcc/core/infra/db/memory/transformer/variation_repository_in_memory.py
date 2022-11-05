from typing import Dict, List, Tuple
from uuid import UUID

from tcc.core.domain.transformer.entities import Variation
from tcc.core.domain.transformer.variation_repository import (
    VariationRepository,
)


class VariationRepositoryInMemory(VariationRepository):
    __name__ = Variation.__name__
    items: List[Dict[str, bool | str | Tuple[float, float, float]]] = [
        {
            "id": "b572eabc-88f5-4f80-9df7-09b8b15ec50a",
            "default": True,
            "Jbt": (1.2, 1.4, 0.03),
            "Jat": (1.4, 1.6, 0.02),
            "Bm": (1.5, 1.6, 0.03),
            "Ksw": (6, 7, 0.04),
            "kt": (0.45, 0.55, 0.03),
            "Rjan": (3.4, 3.6, 0.02),
            "rel": (1.1, 1.2, 0.03),
            "Mativa": (0, 600, 0.0456),
            "PerdasT": (0, 2000, 0.0567),
        }
    ]

    def get(self, id: UUID | str | None = None) -> Variation:
        if id is None:
            filtered = filter(lambda x: x["default"], self.items)
        else:
            filtered = filter(lambda x: x["id"] == id, self.items)

        try:
            value = next(filtered)
            return Variation(**value)  # type: ignore
        except Exception as error:
            raise self.DoesNotExist from error
