from collections import namedtuple
from typing import NamedTuple


class NamedTuple:
    def convert_for_tuple(self, lst: list) -> NamedTuple:
        if isinstance(lst, tuple):
            try:
                keys = lst._fields
                e_namedtuple = True
            except Exception:
                e_namedtuple = False

            values = []

            for value in lst:
                if isinstance(value, (list, dict)):
                    value = self.convert_for_tuple(value)
                values.append(value)

            if e_namedtuple:
                Tabela = namedtuple("Tabela", keys)
                return Tabela(*values)
            else:
                return tuple(values)

        if isinstance(lst, list):
            return tuple([self.convert_for_tuple(x) for x in lst])
        elif isinstance(lst, dict):
            return self.to_named_tuple(lst)

        return lst

    def to_named_tuple(self, data: dict):
        values = []
        keys = []

        for key, value in data.items():
            if isinstance(value, dict):
                value = self.to_named_tuple(value)

            elif isinstance(value, list):
                value = tuple(value)
            try:
                int(key)
                key = "a_" + str(key)
            except ValueError:
                ...
            keys.append(key)
            values.append(self.convert_for_tuple(value))

        Tabela = namedtuple("Tabela", keys)
        tabela = Tabela(*values)

        return tabela
