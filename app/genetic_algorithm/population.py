import pandas as pd
from app.genetic_algorithm.gene import Gene
from collections import namedtuple
from app.transformer import Transformer
from app.utils.classmethod import classproperty


PopulationProps = namedtuple("PopulationProps", field_names=["n_population"])


class Population(pd.DataFrame):
    props = PopulationProps(0)
    __transformer = ...

    def __init__(self, n_population, constraints, tables, data=[]) -> None:
        # import ipdb; ipdb.set_trace()

        self.props = self.props._replace(n_population=n_population)
        self.transformer = Transformer(constraints, tables)

        if not data:
            data = [Gene() for _ in range(n_population)]
        index = list(range(len(data)))
        super().__init__(data=data, index=index)

    @classproperty
    def transformer(cls):
        return cls.__transformer

    @transformer.setter
    def transfomer(cls, new_value):
        cls.__transformer = new_value

    def calculate_all(self):
        # import ipdb; ipdb.set_trace()
        PerdasT, Mativa = "PerdasT", "Mativa"

        result = pd.DataFrame([
            self.transfomer.run(values[1:8]) for values in self.itertuples()
        ], index=range(self.props.n_population), columns=(PerdasT, Mativa))
        self[PerdasT] = result[PerdasT]
        self[Mativa] = result[Mativa]

        # print(res[0])
        return result
