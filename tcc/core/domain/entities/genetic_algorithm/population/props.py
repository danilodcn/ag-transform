from pydantic import validator

from tcc.core.domain import BaseModel


class PopulationProps(BaseModel):
    n_population: int
    disturbance_rate: float
    crossover_probability: float
    penalize_constant: float
    niche_radius: float
    crossover_population_frac: float
    mutation_population_frac: float
    max_ranks: int | None = None

    @validator(
        "crossover_population_frac",
        "mutation_population_frac",
        allow_reuse=True,
    )
    def value_must_be_a_valid_percentage(cls, v: float):
        if 0 < v < 1:
            return v

        else:
            raise ValueError(f"{v} is not a valid percentage")
