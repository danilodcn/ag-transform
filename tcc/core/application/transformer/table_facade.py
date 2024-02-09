from tcc.core.application.registry.registry import Registry
from tcc.core.application.transformer.table_adapter import (
    core_dimensions,
    core_magnetic_loss,
    curve_BH,
    insulation_type_constant,
    number_of_steps,
)


class TableFacade(object):
    def __init__(self, *, registry: Registry) -> None:
        assert isinstance(
            registry, Registry
        ), f"deve ser instancia de {Registry}, em vez disso é instancia de {registry.__class__.__name__}"  # noqa
        self.registry = registry

    def get_number_of_steps(self, area: float):
        adapter = number_of_steps.GetNumberOfSteps(registry=self.registry)
        return adapter.execute(area=area)

    def get_core_dimensions(self, number_of_steps: int):
        adapter = core_dimensions.GetCoreDimensions(registry=self.registry)
        return adapter.execute(number_of_steps=number_of_steps)

    def get_insulation_type_constant(self, type: str, number_of_steps: int):
        adapter = insulation_type_constant.GetInsulationTypeConstraint(
            registry=self.registry
        )
        return adapter.execute(type=type, number_of_steps=number_of_steps)

    def get_core_magnetic_loss(self, B: float):
        adapter = core_magnetic_loss.GetCoreMagneticLoss(
            registry=self.registry
        )
        return adapter.execute(B=B)

    def get_curve_BH(self, B: float):
        adapter = curve_BH.GetCurveBH(registry=self.registry)
        return adapter.execute(B=B)
