from tcc.core.domain.entities.transformer.variation import Variation
from tcc.core.domain.repositories.transformer.variation_repository import (
    VariationRepository,
)


class VariationRepositoryInMemory(VariationRepository):
    __name__ = Variation.__name__
    items: list[dict[str, bool | str | tuple[float, float, float]]] = [
        {
            "id": "b572eabc-88f5-4f80-9df7-09b8b15ec50a",
            "default": True,
            "Jbt": (1.2, 1.4, 0.001),
            "Jat": (1.4, 1.6, 0.001),
            "Bm": (1.5, 1.6, 0.001),
            "Ksw": (6, 7, 0.001),
            "kt": (0.45, 0.55, 0.001),
            "Rjan": (3.4, 3.6, 0.001),
            "rel": (1.1, 1.2, 0.001),
            "Mativa": (0, 600, 0.02),
            "PerdasT": (0, 2000, 0.02),
        }
    ]

    def get(self, id: str | None = None) -> Variation:
        if id is None:
            filtered = filter(lambda x: x["default"], self.items)
        else:
            filtered = filter(lambda x: x["id"] == id, self.items)

        try:
            value = next(filtered)
            return Variation(**value)  # type: ignore
        except Exception as error:
            raise self.DoesNotExist from error

    def insert(self, variation: Variation) -> None:
        raise NotImplementedError

    def insert_many(self, variations: list[Variation]) -> None:
        raise NotImplementedError
