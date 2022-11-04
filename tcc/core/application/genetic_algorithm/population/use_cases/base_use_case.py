from abc import ABC, abstractmethod, abstractproperty

import pandas as pd

from tcc.core.domain.genetic_algorithm.population import (
    Population,
    PopulationSteps,
)


class PopulationUseCaseBase(ABC):
    population: Population

    @abstractproperty
    def minimal_step(self) -> PopulationSteps:
        raise NotImplementedError

    @abstractmethod
    def run(self):
        ...

    def execute(self):
        self.validate()
        self.run()

    def validate(self):
        minimal_step_method = getattr(self, "minimal_step", None)
        minimal_step = minimal_step_method
        if callable(minimal_step_method):
            minimal_step = minimal_step_method()

        class_name = self.__class__.__name__
        base_message = """
        "garanta que a classe '{class_name}' possua a propriedade '{property}'"
        """

        assert isinstance(minimal_step, PopulationSteps), base_message.format(
            property=".minimal_step", class_name=class_name
        )

        population: Population | None = getattr(self, "population", None)
        assert isinstance(population, Population), base_message.format(
            property=".population", class_name=class_name
        )

        message = "passo deve ser no mínimo '{}'. Atualmente é '{}'".format(
            population.get_step_display(minimal_step),
            population.get_step_display(),
        )

        assert population.step >= minimal_step, message

        data = population.data
        assert isinstance(
            data, pd.DataFrame
        ), "garanta que '.data' seja uma instância de 'pd.DataFrame'"
