from ...result import Result


class GeneResult(Result):
    PerdasT: float | None = None
    Mativa: float | None = None
    PerdasT_P: float | None = None
    Mativa_P: float | None = None
    rank: float | None = None
    crowlingDistance: float | None = None
    fitness: float | None = None
    distance: float | None = None
