import json
import unittest

from tcc.core.application.tools.plot import Plot
from tcc.core.domain.genetic_algorithm.population import (
    PopulationBuilder,
    PopulationProps,
)
from tcc.core.domain.transformer.entities import Constraint, Variable
from tcc.core.domain.transformer.transformer import Transformer
from tcc.core.infra.db.memory.transformer.table_repository_in_memory import (
    TableRepositoryInMemory,
)
from tcc.core.infra.db.memory.transformer.variation_repository_in_memory import (
    VariationRepositoryInMemory,
)
from tests.constants import *


class TestCreatePopulation(unittest.TestCase):
    def setUp(self) -> None:
        self.variation_repository = VariationRepositoryInMemory()
        self.table_repository = TableRepositoryInMemory()
        self.table_repository.load_tables(TABLE_FILE_NAME)

        with open(TRANSFORMER_FILE_NAME) as file:
            transformer_data = json.load(file)
            self.variables = Variable(**transformer_data.get("variables", {}))
            self.constraints = Constraint(
                **transformer_data.get("constraints", {})
            )

        variations = self.variation_repository.get()
        self.transformer = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=variations,
        )
        props = PopulationProps(
            n_population=10, disturbance_rate=0.3, crossover_probability=0.4
        )

        self.population = PopulationBuilder.build(
            props=props,
            variations=variations,
        )

    def test_plot(self):
        self.population.generate_data()
        assert self.population.data is not None
        plot = Plot()
        plot.plot(self.population.data, "Jat Jbt".split(), "primeiro")
        plot.plot(self.population.data, "rel Rjan".split(), "segundo")
        Plot.save(
            type="png", suffix="test_population", dir_name="tests", dpi=100
        )
