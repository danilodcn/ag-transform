import numpy as np
import pandas as pd
from app.genetic_algorithm.gene import Gene
from collections import namedtuple
from app.transformer import Transformer


PopulationProps = namedtuple("PopulationProps", field_names=["n_population"])


class Population(pd.DataFrame):
    props = PopulationProps(0)

    def __init__(self, n_population, constraints, tables, data=[]) -> None:
        # import ipdb; ipdb.set_trace()

        self.props = self.props._replace(n_population=n_population)
        self.transformer = Transformer(constraints, tables)

        if not data:
            data = [Gene() for _ in range(n_population)]
        index = list(range(len(data)))
        super().__init__(data=data, index=index)

    def calculate_all(self):
        # import ipdb; ipdb.set_trace()
        np
