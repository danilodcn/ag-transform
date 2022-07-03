from tcc.core.domain.transformer.table_repository import TableRepository

from .core_dimensions import GetCoreDimensions
from .core_magnetic_loss import GetCoreMagneticLoss
from .curve_BH import GetCurveBH
from .insulation_type_constant import GetInsulationTypeConstraint
from .number_of_steps import GetNumberOfSteps


class TableFacade(object):
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def get_number_of_steps(self, area: float):
        use_case = GetNumberOfSteps(self.table_repository)
        return use_case.execute(area)

    def get_core_dimensions(self, number_of_steps: int):
        use_case = GetCoreDimensions(self.table_repository)
        return use_case.execute(number_of_steps)

    def get_insulation_type_constant(self, type: str, number_of_steps: int):
        use_case = GetInsulationTypeConstraint(self.table_repository)
        return use_case.execute(type, number_of_steps)

    def get_core_magnetic_loss(self, B: float):
        use_case = GetCoreMagneticLoss(self.table_repository)
        return use_case.execute(B=B)

    def get_curve_BH(self, Bm: float):
        use_case = GetCurveBH(self.table_repository)
        return use_case.execute(Bm)
