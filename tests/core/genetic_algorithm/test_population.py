import json
import unittest
from typing import List

import numpy as np

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
            niche_radius=0.1,
            crossover_population_frac=0.4,
            mutation_population_frac=0.8,
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

    def test_add_genes(self):
        population_1 = PopulationBuilder.build(
            props=self.props,
            variations=self.variations,
        )

        population_2 = PopulationBuilder.build(
            props=self.props,
            variations=self.variations,
        )

        population_1.generate_data()
        population_2.generate_data()
        assert population_1.data is not None
        assert population_2.data is not None
        N = 4
        genes_for_add_ids = np.random.choice(
            list(population_2.data.index), N, replace=False
        )
        genes_for_add_ids.sort()
        genes_for_add: List[Gene] = []
        for i, gene in enumerate(population_2.genes):
            if i in genes_for_add_ids:
                genes_for_add.append(gene)
        population_1.add_genes(*genes_for_add)
        for gene_1, gene_2 in zip(genes_for_add, population_1.genes[-N:]):
            try:
                self.assertEqual(gene_1, gene_2)
            except ValueError as error:
                self.assertIn(
                    "The truth value of a Series is ambiguous", str(error)
                )

        selected_1 = population_1.data[-N:]
        selected_2 = population_2.data.iloc[genes_for_add_ids]
        selected_2.index = selected_1.index
        for key_1 in selected_1.index:
            value_1 = selected_1.loc[key_1]
            value_2 = selected_2.loc[key_1]

            for i, j in zip(value_1, value_2):
                is_equal = i == j or (np.isnan(i) and np.isnan(j))
                self.assertTrue(is_equal, f"deve ser igual: {i} != {j}")
