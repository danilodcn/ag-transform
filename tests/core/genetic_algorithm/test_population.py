import json
import os
import unittest

from tcc.core.domain.genetic_algorithm.population import (
    Population,
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

TABLE_FILE_NAME = os.getcwd() + "/tests/core/json/tables.json"
TRANSFORMER_FILE_NAME = os.getcwd() + "/tests/core/json/transformer.json"


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

        self.variations = self.variation_repository.get()
        self.transformer = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=self.variations,
        )

    def test_create_population(self):
        props = PopulationProps(
            n_population=10, disturbance_rate=0.3, crossover_probability=0.4
        )
        population = PopulationBuilder.build(
            props=props,
            variations=self.variations,
        )
        len = population.len()

        self.assertIsInstance(population, Population)
        self.assertEqual(len, props.n_population)
