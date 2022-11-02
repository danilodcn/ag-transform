import pandas as pd

from tcc.core.application.transformer.run_transformer_use_case import (
    RunTransformerUseCase,
)
from tcc.core.domain.genetic_algorithm.population import Population
from tcc.core.domain.transformer.entities import (
    Constraint,
    Variable,
    Variation,
)
from tcc.core.domain.transformer.table_repository import TableRepository
from tcc.core.domain.transformer.transformer import Transformer


class PopulationCalculator:
    def __init__(
        self,
        population: Population,
        table_repository: TableRepository,
        constraints: Constraint,
        variations: Variation,
    ) -> None:
        self.population = population

        self.use_case = RunTransformerUseCase(
            table_repository=table_repository
        )
        self.constraints = constraints
        self.variations = variations

    def execute(self):
        transformer = Transformer(
            variables=Variable(Jbt=0, Jat=0, Bm=0, Ksw=0, kt=0, Rjan=0, rel=0),
            constraints=self.constraints,
            variations=self.variations,
        )
        result = []
        for gene in self.population.genes:
            transformer.variables = gene.variables
            result.append(self.use_case.execute(transformer))

        if self.population.data is not None:
            index = self.population.data.index
        else:
            index = pd.Index(range(self.population.props.n_population))

        pd_result = pd.DataFrame(
            result,
            index=index,
            columns=["PerdasT", "Mativa"],
        )

        self.population.generate_data()
        assert self.population.data is not None
        self.population.data.update(pd_result)
        self.population.generate_genes()
