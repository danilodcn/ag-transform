from tcc.core.domain.entities.transformer.table import TableNameEnum

from .table_adapter import TableAdapter


class GetInsulationTypeConstraint(TableAdapter):
    def execute(self, /, **kwargs: int | str):
        type = kwargs["type"]
        number_of_steps = kwargs["number_of_steps"]
        assert isinstance(type, str)
        assert isinstance(number_of_steps, int)

        TABLE_NAME = TableNameEnum.insulation_type_constant
        table = self.table_repository.get(TABLE_NAME)

        number_of_steps -= 1
        if number_of_steps > 4:
            number_of_steps = 4

        try:
            insulation_constraint = table.data[type][number_of_steps]
            if isinstance(insulation_constraint, float):
                return insulation_constraint

        except Exception:
            txt = f'O tipo de transformador "{type}" não é suportado.'

            msg = "Os tipos suportados sao: [{}]"
            msg.format(", ".join([f'"{i}"' for i in table.data.keys()]))
            txt += msg
            raise KeyError(txt)

        raise ValueError("A constante de insolação deve ser do tipo 'float'.")
