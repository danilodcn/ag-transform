from tcc.core.application.register.register import Register
from tcc.core.application.transformer.table_adapter import (
    core_dimensions,
    core_magnetic_loss,
    curve_BH,
    insulation_type_constant,
    number_of_steps,
)


class TableFacade(object):
    def __init__(self, register: Register) -> None:
        self.register = register

    def get_number_of_steps(self, area: float):
        adapter = number_of_steps.GetNumberOfSteps(self.register)
        return adapter.execute(area=area)

    def get_core_dimensions(self, number_of_steps: int):
        adapter = core_dimensions.GetCoreDimensions(self.register)
        return adapter.execute(number_of_steps=number_of_steps)

    def get_insulation_type_constant(self, type: str, number_of_steps: int):
        adapter = insulation_type_constant.GetInsulationTypeConstraint(
            self.register
        )
        return adapter.execute(type=type, number_of_steps=number_of_steps)

    def get_core_magnetic_loss(self, B: float):
        adapter = core_magnetic_loss.GetCoreMagneticLoss(self.register)
        return adapter.execute(B=B)

    def get_curve_BH(self, B: float):
        adapter = curve_BH.GetCurveBH(self.register)
        return adapter.execute(B=B)
