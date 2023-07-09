from tcc.core.domain import BaseModel

# tula contendo valor mínimo, máximo e peso usado
VariationTuple = tuple[float, float, float]


class Variation(BaseModel):
    Jbt: VariationTuple
    Jat: VariationTuple
    Bm: VariationTuple
    Ksw: VariationTuple
    kt: VariationTuple
    Rjan: VariationTuple
    rel: VariationTuple
    Mativa: VariationTuple
    PerdasT: VariationTuple
