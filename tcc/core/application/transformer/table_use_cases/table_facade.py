from tcc.core.application.transformer.table_use_cases import (
    core_dimensions,
    core_magnetic_loss,
    curve_BH,
    insulation_type_constant,
    number_of_steps,
)
from tcc.core.domain.transformer.table_repository import TableRepository


class TableFacade(object):
    def __init__(self, table_repository: TableRepository) -> None:
        self.table_repository = table_repository

    def get_number_of_steps(self, area: float):
        use_case = number_of_steps.GetNumberOfSteps(self.table_repository)
        return use_case.execute(area)

    def get_core_dimensions(self, number_of_steps: int):
        use_case = core_dimensions.GetCoreDimensions(self.table_repository)
        return use_case.execute(number_of_steps)

    def get_insulation_type_constant(self, type: str, number_of_steps: int):
        use_case = insulation_type_constant.GetInsulationTypeConstraint(
            self.table_repository
        )
        return use_case.execute(type, number_of_steps)

    def get_core_magnetic_loss(self, B: float):
        use_case = core_magnetic_loss.GetCoreMagneticLoss(
            self.table_repository
        )
        return use_case.execute(B=B)

    def get_curve_BH(self, B: float):
        use_case = curve_BH.GetCurveBH(self.table_repository)
        return use_case.execute(B=B)
