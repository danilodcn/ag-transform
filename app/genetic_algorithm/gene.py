import numpy as np
from pandas import Series
from app.utils.classmethod import classproperty
from collections import OrderedDict


class Gene(Series):
    __variations = OrderedDict({
            "Jbt": (1.2, 1.4),
            "Jat": (1.4, 1.6),
            "Bm": (1.5, 1.6),
            "Ksw": (6, 7),
            "kt": (0.45, 0.55),
            "Rjan": (3.4, 3.6),
            "rel": (1.1, 1.2),
            })

    __field_names = ["PerdasT", "Mativa", "rank"]

    def __init__(self, data=[]):
        data = np.asarray(data)
        if data.shape == (0,):
            data = self.random_crete() + [0] * len(self.__field_names)
        super().__init__(data=data, index=self.names + self.__field_names)

    @classproperty
    def variations(cls):
        return cls.__variations

    @variations.setter
    def variations(cls, value):
        cls.__variations = value

    @classproperty
    def names(cls):
        return list(cls.__variations)

    def random_crete(self):
        # import ipdb; ipdb.set_trace()

        genes = [
                np.random.uniform(low, high)
                for low, high
                in self.variations.values()
            ]
        return genes
