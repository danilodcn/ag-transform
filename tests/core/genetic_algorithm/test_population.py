import json
import unittest

from tcc.core.domain.genetic_algorithm.gene import Gene
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

        self.variations = self.variation_repository.get()
        self.transformer = Transformer(
            variables=self.variables,
            constraints=self.constraints,
            variations=self.variations,
        )
        self.props = PopulationProps(
            n_population=10,
            disturbance_rate=0.3,
            crossover_probability=0.4,
            penalize_constant=1.4,
        )

    def test_create_population(self):
        population = PopulationBuilder.build(
            props=self.props,
            variations=self.variations,
        )

        self.assertIsInstance(population, Population)

    def test_generate_data(self):
        population = PopulationBuilder.build(
            props=self.props,
            variations=self.variations,
        )
        self.assertIsNone(population.data)

        population.generate_data()

        self.assertIsNotNone(population.data)

    def test_generate_genes(self):
        population = PopulationBuilder.build(
            props=self.props,
            variations=self.variations,
        )
        population.generate_data()

        population.generate_genes()

        self.assertIsNotNone(population.data)
        self.assertEqual(len(population.genes), population.props.n_population)
        for gene in population.genes:
            self.assertIsInstance(gene, Gene)
