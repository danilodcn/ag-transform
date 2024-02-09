from math import pi, sqrt

import numpy as np

from tcc.core.application.registry.registry import Registry
from tcc.core.application.transformer.table_facade import TableFacade
from tcc.core.application.transformer.transformer_runner import (
    TransformerRunner,
)
from tcc.core.domain.entities.transformer.transformer import Transformer


class TransformerThreePhaseRunner(TransformerRunner):
    def __init__(self, *, registry: Registry) -> None:
        self.table_facade = TableFacade(registry=registry)

    def run(self, transformer: Transformer):
        constraints = transformer.constraints
        variables = transformer.variables

        Vf1, Vf2 = transformer.get_voltages()

        # é a tensão eficaz por espiras [V/e]
        Et = variables.kt * sqrt(constraints.S)
        N1 = (Vf1 * 1000) / Et
        N2 = (Vf2 * 1000) / Et

        # é a área efetiva da coluna  [mm2]
        Ac = Et / (4.44 * constraints.f * variables.Bm) * 1e6
        Abc = Ac / constraints.Ke

        number_of_steps = self.table_facade.get_number_of_steps(Abc / 1000)
        Ku, __LD = self.table_facade.get_core_dimensions(
            number_of_steps=number_of_steps
        )

        # LD é um vetor que contem todos os valores existentes na tabela 2.4
        LD = np.asarray(__LD, np.float64)

        So = Abc / Ku  # Seção circular circunscrita
        dc = 2 * sqrt(So / pi)  # é o diâmetro da coluna do núcleo

        L = LD * dc
        teta = np.arccos(LD)

        # Calculo da profundidade do núcleo [n]
        e = [np.sin(teta[0]) * dc / 2]
        for i, _ in enumerate(iterable=teta[1:], start=1):
            _prof = np.sin(teta[i]) * dc / 2 - sum(e)
            e.append(_prof)

        Abc = np.sum(L * np.asarray(e, np.float64)) * 2

        # é a profundidade total do núcleo do transformador
        # Prof = np.sum(e) * 2
        k = self.table_facade.get_insulation_type_constant(
            type=constraints.type, number_of_steps=number_of_steps
        )

        d = sqrt(Ac / k)

        # x = (Ac * 4 / pi) ** .5
        # TODO talvez vamos calcular d usando d como o diametro de Ac

        # TODO Kw deveria vir da tabela 2.1.
        # na equação 2.26 usa esse Kw e diz que ele é definido na tabela 2.1
        Kw = variables.Ksw / (30 + Vf2)

        # é a área da janela em [mm²]. Ac esta em [mm²]
        Aw = (
            constraints.S
            / (3.33 * constraints.f * Ac * variables.Bm * Kw * variables.Jbt)
            * 1e9
        )

        # TODO essa equação não está na tese. Olhar a página 50
        ww = sqrt(Aw / variables.Rjan)

        hw = Aw / ww  # é a altura da janela [m]

        # é a maior largura da coluna do núcleo do transformador [m]
        wc: float = L[0]
        # é a distância entre os centros de duas colunas [m]
        D = ww + wc
        W = 2 * D + wc  # é a largura total do núcleo [m]

        # a = (d - wc) / 2
        # Estimativa da corrente de carga
        # Abj = rel * Abc     # é a área bruta da culatra [mm²]
        Aj = variables.rel * Ac  # é a área do jugo ou da culatra [mm²]
        # hy = Abj / Prof     # é a altura da culatra [mm]
        By = variables.Bm / variables.rel  # densidade de fluxo no jugo (yoke)
        # TODO entender o que é isso

        # H = hw + 2 * hy     # é a altura total do núcleo [m]
        Vferc = 3 * hw * Ac  # Volume de ferro no núcleo [mm³]
        Bfe = constraints.Dfe * 1e-9  # Densidade do ferro em [Kg / mm³]
        Mc = Vferc * Bfe  # Massa da culatra  [Kg]

        Pic = self.table_facade.get_core_magnetic_loss(B=variables.Bm)

        Wic = Pic * Mc  # perda específica no núcleo [W]
        Vferj = Aj * W * 2  # é o volume do ferro nas culatras
        Mj = Vferj * Bfe
        MT = Mj + Mc  # Massa total do Trafo [Kg]
        Pij = self.table_facade.get_core_magnetic_loss(B=By)

        Wij = Pij * Mj
        # Perdas totais do ferro no transformador.
        # As perdas totais é a soma da perda nas colunas
        # + as perdas nas culatras (culatras e guarnições)
        Po = (Wic + Wij) * 1.05
        # Componente da corrente ativa Ip da perda no núcleo [A]
        # Ip = Po/(3 * Vf1) * 1e-3

        # atc = self.tables.curva_BH(Bm)
        # atj = self.tables.curva_BH(By)

        # ATj = 2 * W * atj   # A força magnetomotriz na culatra [Ae]
        # ATc = 3 * hw * atc  # A força magnetomotriz na coluna [Ae]

        # ATcj = ATc + ATj        # A força magnetomotriz total [Ae]
        # N1 enrolamento do lado da BT conforme trafo WEG DE 150 KVA
        # Iq = ATcj / N1 * 1e-3

        # Io = sqrt(Ip ** 2 + Iq ** 2) # A corrente a vazio [A]

        I1 = constraints.S / 3 / Vf1  # FIXME S é a potencia total do Trafo
        Fc1 = I1 / variables.Jbt
        Swind1 = Fc1 * N1
        z = (hw * Kw) * 2
        hb = (hw - z) * 1.11
        tbt1 = Swind1 / hb * 1.1  # 10% de folga
        tbt2 = tbt1 * 2

        Dextbt = tbt2 + d  # diametro em mm
        # diâmetro médio na baixa tensão em milímetros
        dmbt = (Dextbt + d) / 2
        Lmbt = pi * dmbt  # Comprimento médio em mm
        Compbt1 = Lmbt * N1  # Comprimento do fio na baixa tensão
        # dfc1 = sqrt(4 * Fc1 / pi)
        VALbt = Compbt1 * Fc1 * 3

        Mbt3 = VALbt * constraints.Dal * 1e-9
        # I2menor = (S / 3 / Vf2)     # corrente no secundário
        # TODO pergutar ao professor se esse valor deve ser dado do usuário
        Vmedio2 = 12
        # tap intermediário para dimensionamento dos condutores
        I2c = constraints.S / 3 / Vmedio2

        Fc2AT = I2c / variables.Jat  # área do condutor em mm2 no secundário
        # dfc2AT  = sqrt(Fc2AT * 4 / pi)  # Diametro do condutor em mm
        SwindAT = Fc2AT * N2  # Area referente a alta tensao
        # dAt = sqrt(SwindAT * 4 / pi)

        tAT1 = SwindAT / hb * 1.1
        # Laxju = hw - hw * Kw / 2

        # tAT2 = tAT1 * 2

        dintAT = Dextbt + 6 * (d - wc) / 2
        DextAT = dintAT + 4 * tAT1

        LmATc = pi * (dintAT + DextAT) / 2  # Comprimento em milímetros
        CompAT = LmATc * N2

        # dfc2 = sqrt(I2c / Jat * 4 / pi)
        VALAT = CompAT * I2c / variables.Jat * 3
        MAT3 = VALAT * constraints.Dal * 1e-9

        # Resistencia do cobre no lado da baixa tesão
        R1 = 0.02857 * Compbt1 / Fc1 * 1e-3
        # Resistencia do cobre no lado da alta tesão
        R2 = 0.02857 * CompAT / Fc2AT * 1e-3

        I2 = constraints.S / 3 / Vf2
        Pj = (R1 * I1**2 + R2 * I2**2) * 3
        PerdasT = Po + Pj
        Mativa = MAT3 + Mbt3 + MT
        return [PerdasT, Mativa]
