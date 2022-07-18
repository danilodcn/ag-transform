from typing import Dict, Optional, Tuple

from tcc.core.domain.transformer.entities import Variation
from tcc.core.domain.transformer.variation_repository import (
    VariationRepository,
)

VariationRepositoryData = Dict[str, bool | Tuple[float, float]]


class VariationRepositoryInMemory(VariationRepository):
    variations: Dict[int, VariationRepositoryData] = {
        1: {
            "default": True,
            "Jbt": (1.2, 1.4),
            "Jat": (1.4, 1.6),
            "Bm": (1.5, 1.6),
            "Ksw": (6, 7),
            "kt": (0.45, 0.55),
            "Rjan": (3.4, 3.6),
            "rel": (1.1, 1.2),
        }
    }

    def get(self, id: Optional[int] = None) -> Variation:
        for key, value in self.variations.items():
            if key == id or (id is None and value["default"]):
                return Variation(**value)  # type: ignore

        raise KeyError("objeto não encontrado")
