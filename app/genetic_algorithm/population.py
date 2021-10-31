import pandas as pd
from app.genetic_algorithm.gene import Gene
from collections import namedtuple
from app.transformer import Transformer
from app.utils.classmethod import classproperty
from app.utils.sort import is_dominated
# from numba import jit

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

    def sort_pareto_ranks(self):
        no_dominated = list(self.index)
        number = 0
        while len(no_dominated) != 0:
            number += 1
            no_dominated = self.__sort_pareto_ranks(no_dominated, number)

        # import ipdb; ipdb.set_trace()

    def __sort_pareto_ranks(self, no_dominated: list, number):
        dominateds = []
        if len(no_dominated) == 1:
            self.loc[no_dominated[0], "rank"] = number

        for i in no_dominated:
            dominated = False

            for p in no_dominated:
                if i == p:
                    continue
                else:
                    gene_i = self.loc[i, ["PerdasT", "Mativa"]]
                    gene_p = self.loc[p, ["PerdasT", "Mativa"]]

                    # import ipdb; ipdb.set_trace()

                    if is_dominated(gene_i, gene_p):
                        dominated = True
                        dominateds.append(i)
                        # print(gene_i)
                        # print(gene_p)
                        self.loc[i, "rank"] = number + 1
                        break

            if not dominated:
                self.loc[i, "rank"] = number

        # import ipdb; ipdb.set_trace()

        return dominateds
