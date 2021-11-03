import pandas as pd
import numpy as np
import itertools as it

from collections import OrderedDict
from app.genetic_algorithm.gene import Gene
from collections import namedtuple
from app.transformer import Transformer
from app.utils.classmethod import classproperty
from app.utils.functions import count_restrictions_violated
from app.utils.sort import is_dominated
from dataclasses import dataclass
# from app.utils.plot import Plot, plt
# from numba import jit

PopulationProps = namedtuple("PopulationProps", field_names=["n_population", ])


@dataclass
class PopulationProps:
    n_population: int = 0
    # FIXME taxa de perturbação e probalidade de crossover
    # foram achados na página 147 do livro do Lobato
    disturbance_rate: float = .8        # deve esta entre 0.2 e 2
    crossover_probability: float = .3   # deve esta entre 0.1 e 1

    tables = 0
    constraints = 0


def sum_of_integers(n1, n2):
    return int((n2 - n1 + 1) * (n1 + n2) / 2)


class Population(pd.DataFrame):

    # props = PopulationProps(0)
    props = PopulationProps()
    __transformer = ...
    __variations = OrderedDict({
        "PerdasT": [0, 2000],
        "Mativa": [0, 600]
    })

    crowlingDistancePartinner = float("inf")
    niche_ray = 0.01

    def __init__(self, n_population, constraints, tables, data=[]) -> None:
        # import ipdb; ipdb.set_trace()

        # self.props = self.props._replace(n_population=n_population)
        self.props.n_population = n_population
        self.props.constraints = constraints
        self.props.tables = tables
        self.transformer = Transformer(constraints, tables)

        if isinstance(data, (pd.DataFrame, pd.Series)):
            pass

        elif not data:
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

    def calcule_all(self):
        # import ipdb; ipdb.set_trace()
        PerdasT, Mativa = "PerdasT", "Mativa"

        result = pd.DataFrame([
            self.transfomer.run(values[1:8]) for values in self.itertuples()
        ], index=self.index, columns=(PerdasT, Mativa))
        # import ipdb; ipdb.set_trace()
        # self[PerdasT] = result[PerdasT]
        # self[Mativa] = result[Mativa]
        self.update(result)
        self["PerdasT_P"] = self[PerdasT]
        self["Mativa_P"] = self[Mativa]

        # print(res[0])
        # return result

    def penalize(self):
        # print(self)
        variations = (
            list(Gene.variations.values()) + list(self.variations.values())
        )
        counts = self.apply(
            count_restrictions_violated,
            args=(variations, ),
            axis=1
        )
        perdas, massas = self.variations.values()
        k = 1.4
        vector_params = pd.DataFrame(
            np.asarray([
                np.ones((self.index.__len__())) * perdas[1] * counts,
                np.ones((self.index.__len__())) * massas[1] * counts
            ]).transpose() * k,

            columns=[
                "PerdasT_P", "Mativa_P",
            ]
        ) + self[["PerdasT_P", "Mativa_P"]]

        # import ipdb; ipdb.set_trace()
        self.update(vector_params)
        # vector_params.dot(vector_params)

    def sort_pareto_ranks(self):
        self["rank"] *= 0
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
                    gene_i = self.loc[i, ["PerdasT_P", "Mativa_P"]]
                    gene_p = self.loc[p, ["PerdasT_P", "Mativa_P"]]

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
            np.zeros((self.index.__len__(), 5)),
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
            set = self.loc[self["rank"] == rank][["PerdasT_P", "Mativa_P"]]
            perdas_set = set.sort_values(by=["PerdasT_P"])["PerdasT_P"]

            # import ipdb; ipdb.set_trace()

            df["solutions_for_rank"].iloc[
                perdas_set.index
            ] = perdas_set.count()

            # massas_set = set.sort_values(by=["Mativa"])["Mativa"]
            number = perdas_set.index.__len__()
            n_current = n_before - number

            df["meanFitness"].loc[perdas_set.index] = (
                3 * sum_of_integers(n_current, n_before) / (
                    n_before - n_current
                    )
            )
            n_before = n_current
            # import ipdb; ipdb.set_trace()

            # iterator = it.permutations(set.index, 2)
            for i in set.index:
                perda_i, massa_i = set["PerdasT_P"][i], set["Mativa_P"][i]
                distance = 1
                for j in set.index:
                    if i == j:
                        continue
                    perda_j, massa_j = set["PerdasT_P"][j], set["Mativa_P"][j]
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

        result = df["meanFitness"] * df["solutions_for_rank"] * (
                df["sharedFitness"] / sum_shared_fitness
            )
        self["fitness"] = result / np.sum(result)
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

    def sample(
            self, n=None, frac=None, weights=None, axis=None, replace=False
            ) -> pd.DataFrame:
        # import ipdb; ipdb.set_trace()
        if weights is None:
            weights = self["fitness"]
        elif weights == 1:
            weights = [1] * self.count()

        return super().sample(
            n, frac=frac, replace=replace, weights=weights, axis=axis
        )

    def add_gene(self, gene: Gene):
        # self.index += 1
        self.loc[self["rank"].count()] = gene
        # self.props.n_population += 1
        # import ipdb; ipdb.set_trace()

    def crossover(self):
        father: pd.DataFrame = self.sample(frac=.9, weights=None)
        father = father.sample(frac=1)

        k = .8
        father_1: pd.DataFrame = father.sample(
            frac=k, weights=None
            ).sample(frac=1)

        n = 1 + (1 + 8 * 1 * self.index.__len__()) ** .5
        n = int(n / 2 + .5)
        father_2: pd.DataFrame = father.sample(
            n=n, weights=None
            ).sample(frac=1)

        iterator = zip(
            it.cycle(father_1.index),
            it.combinations(father_2.index, 2)
            # father_2.index,
            # father_3.index
        )
        # import ipdb; ipdb.set_trace()
        m = 0
        for k, values in iterator:
            i, j = values
            m += 1
            if i == j:
                continue

            self.__crossover(
                self.iloc[i],
                self.iloc[j],
                self.iloc[k],
            )
            # import ipdb; ipdb.set_trace()

        # import ipdb; ipdb.set_trace()

    def __crossover(self, p1: Gene, p2: Gene, p3: Gene):
        # p0 = self.sample(n=1, weights=None)
        mask = np.random.rand(p1.count()) < self.props.crossover_probability
        p0 = self.props.disturbance_rate * (p1 - p2) * 1 * mask

        children = p0 + p3
        self.add_gene(children)
        # import ipdb; ipdb.set_trace()

    def mutation(self, n):
        n = 1 + (1 + 8 * n) ** .5
        n = int(n / 2) + 1
        father: pd.DataFrame = self.sample(n=n, weights=None).sample(frac=1)
        index = self.index
        weights = self["fitness"]
        iterator = zip(
            range(n),
            it.combinations(father.index, 2)
        )
        # import ipdb; ipdb.set_trace()
        for _, value in iterator:
            i, j = value

            self.__crossover(
                self.iloc[i],
                self.iloc[j],
                self.loc[np.random.choice(index, p=weights)]
            )

    def clean(self):
        print("Começo")
        weights = self["fitness"]
        if (weights < 0).any():
            self.calcule_all()
            self.sort_pareto_ranks()
            self.penalize()
            self.calcule_fitness()

        rank_1 = self.loc[self["rank"] == 1]
        index = list(rank_1.index)

        # import ipdb; ipdb.set_trace()

        if len(index) > self.props.n_population:
            index = np.random.choice(
                self.index,
                self.props.n_population,
                p=list(rank_1["fitness"])
            )
            index = list(index)

        else:
            bad_index = self.index.isin(index)
            # res = self.iloc[~bad_index],
            fitness = self["fitness"].iloc[~bad_index]
            p = fitness / np.sum(fitness)

            res_index = np.random.choice(
                fitness.index,
                self.props.n_population - index.__len__(),
                p=p
            )
            index = list(index)
            index.extend(list(res_index))
            # del index[-1]

        # _index = self.index.isin(index)
        data: pd.DataFrame = self.iloc[index]
        data.index = list(range(self.props.n_population))

        self = Population(
            self.props.n_population,
            self.props.constraints,
            self.props.tables,
            data=data
        )
        # import ipdb; ipdb.set_trace()
        return self
