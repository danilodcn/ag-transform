import pandas as pd
import numpy as np

from collections import OrderedDict
from app.genetic_algorithm.gene import Gene
from collections import namedtuple
from app.transformer import Transformer
from app.utils.classmethod import classproperty
from app.utils.sort import is_dominated
# from app.utils.plot import Plot, plt
# from numba import jit

PopulationProps = namedtuple("PopulationProps", field_names=["n_population"])


def sum_of_integers(n1, n2):
    return int((n2 - n1 + 1) * (n1 + n2) / 2)


class Population(pd.DataFrame):

    props = PopulationProps(0)
    __transformer = ...
    __variations = OrderedDict({
        "PerdasT": [0, 2000],
        "Mativa": [300, 610]
    })

    crowlingDistancePartinner = float("inf")
    niche_ray = 0.01

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

    @classproperty
    def variations(cls):
        return cls.__variations

    @variations.setter
    def variations(cls, value):
        cls.__variations = value

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

    def calculate_crowding_distance(self):
        self.__calculate_crowling_distance("Mativa")
        self.__calculate_crowling_distance("PerdasT")
        # import ipdb; ipdb.set_trace()

    def __calculate_crowling_distance(self, objetive: str):
        fmin, fmax = self.variations.get(objetive)
        delta = fmax - fmin

        ranks = list(self["rank"].drop_duplicates())

        ranks.sort()
        for rank in ranks:
            solution_set = self.loc[
                self["rank"] == rank
                ].sort_values(by=[objetive])[objetive]

            if solution_set.count() < 3:
                self["crowlingDistance"].iloc[
                    solution_set.index
                    ] = self.crowlingDistancePartinner
                continue

            else:
                ind = solution_set.index
                # import ipdb; ipdb.set_trace()
                self["crowlingDistance"].iloc[
                    [ind[0], ind[-1]]
                    ] = self.crowlingDistancePartinner

            iterator = zip(
                solution_set[:-2],
                solution_set.index[1:-1],
                solution_set[2:],
            )
            for f_left, index, f_right, in iterator:
                self["crowlingDistance"].iloc[
                    index
                    ] += (f_right - f_left) / delta

        # import ipdb; ipdb.set_trace()

    def calcule_fitness(self):
        self.__calcule_fitness()

        # import ipdb; ipdb.set_trace()

    def __calcule_fitness(self):

        # import ipdb; ipdb.set_trace()
        lst_rank = list(self["rank"])
        df = pd.DataFrame(
            np.zeros((self.props.n_population, 5)),
            columns=[
                "meanFitness", "sumDistance",
                "sharedFitness", "solutions_for_rank", "rank"
            ]
        )

        df["rank"] = lst_rank

        # df = df[df["solutions_for_rank"].notnull()].copy()

        ranks = list(self["rank"].drop_duplicates())
        ranks.sort()
        n_before = self.index.__len__()
        for rank in ranks:
            set = self.loc[self["rank"] == rank][["PerdasT", "Mativa"]]
            perdas_set = set.sort_values(by=["PerdasT"])["PerdasT"]

            # import ipdb; ipdb.set_trace()

            df["solutions_for_rank"].iloc[
                perdas_set.index
            ] = perdas_set.count()

            # massas_set = set.sort_values(by=["Mativa"])["Mativa"]
            number = perdas_set.index.__len__()
            n_current = n_before - number

            df["meanFitness"].loc[perdas_set.index] = (
                sum_of_integers(n_current, n_before) / (n_before - n_current)
            )
            n_before = n_current

            # iterator = it.permutations(set.index, 2)
            for i in set.index:
                perda_i, massa_i = set["Mativa"][i], set["Mativa"][i]
                distance = 1
                for j in set.index:
                    if i == j:
                        continue
                    perda_j, massa_j = set["Mativa"][j], set["Mativa"][j]
                    distance_ij = self.__distance(
                        perda_i, perda_j, massa_i, massa_j
                    )
                    distance += self.__shared_function(distance_ij, 1)

                df["sumDistance"].iloc[i] = distance

            # self.__distances(set.sort_values(by=["PerdasT"]))
            # continuação do algoritmo
            # niche_ray = 32

        df["sharedFitness"] = df["meanFitness"] / df["sumDistance"]

        sum_shared_fitness = np.sum(df["sharedFitness"])

        self["fitness"] = df["meanFitness"] * df["solutions_for_rank"] * (
                df["sharedFitness"] / sum_shared_fitness
            )

        # import ipdb; ipdb.set_trace()

    def __shared_function(self, distance: float, alfa: float):
        if distance <= self.niche_ray:
            return 1 - (distance / self.niche_ray) ** alfa

        else:
            return 0

    def __distance(self, p1, p2, m1, m2):
        fmin, fmax = self.variations.get("Mativa")
        delta_massas = fmax - fmin

        fmin, fmax = self.variations.get("PerdasT")
        delta_perdas = fmax - fmin

        massas = ((m1 - m2) / delta_massas) ** 2
        perdas = ((p1 - p2) / delta_perdas) ** 2

        return (massas + perdas) ** .5

    def 
