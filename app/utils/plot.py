import pandas as pd

from matplotlib import pyplot as plt
from matplotlib import colors


COLORS = list(colors.TABLEAU_COLORS.values())


class Plot:
    def __init__(self, df) -> None:
        self.Mativa = df["Mativa"]
        self.PerdasT = df["PerdasT"]
        self.rank = df["rank"]

    def __basic_plot(self, title=""):
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel("Perdas Totais [W]")
        ax.set_ylabel("Massa [Kg]")

        return fig, ax

    def plot(self, df: pd.DataFrame):
        _, ax = self.__basic_plot("")

        ax.plot(self.PerdasT, self.Mativa, "ko")

        iterator = zip(
            range(len(self.Mativa)),
            self.Mativa,
            self.PerdasT
        )
        for i, massa, perdas in iterator:
            ax.annotate(i, xy=(perdas, massa))

    def plot_with_rank(self):
        # print(annotation)
        _, ax = self.__basic_plot("Points with ranks")
        iterator = zip(
            range(len(self.Mativa)),
            self.Mativa, self.PerdasT,
            self.rank
        )

        for i, massa, perdas, rank in iterator:
            ax.plot(
                perdas, massa, marker="o",
                color=COLORS[int(rank % len(COLORS))]
            )
