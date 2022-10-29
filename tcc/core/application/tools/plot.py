import pandas as pd
from matplotlib import pyplot as plt
from matplotlib._color_data import XKCD_COLORS

COLORS = list(XKCD_COLORS.values())


class Plot:
    # def __init__(self, df: pd.DataFrame) -> None:
    #     self.Mativa = df["Mativa"]
    #     self.PerdasT = df["PerdasT"]
    #     self.rank = df["rank"]
    #     self.df = df

    def __basic_plot(self, title=""):
        fig, ax = plt.subplots()
        ax.set_title(title)
        ax.set_xlabel("Perdas Totais [W]")
        ax.set_ylabel("Massa [Kg]")

        return fig, ax

    def plot(self, df: pd.DataFrame):
        _, ax = self.__basic_plot("")

        PerdasT = df["PerdasT"]
        Mativa = df["Mativa"]

        ax.plot(PerdasT, Mativa, "ko")

        iterator = zip(range(len(Mativa)), Mativa, PerdasT)
        for i, massa, perdas in iterator:
            ax.annotate(str(i), xy=(perdas, massa))

    @staticmethod
    def show():
        plt.show()

    def plot_with_rank(self, title="Points with ranks", penalize=False):
        return
        # print(annotation)
        _, ax = self.__basic_plot(title)

        ranks = self.rank.drop_duplicates()
        ranks = list(ranks)
        ranks.sort()
        PerdasT, Mativa = "PerdasT Mativa".split()
        if penalize:
            PerdasT, Mativa = "PerdasT_P Mativa_P".split()
        for rank in ranks:
            massas = self.df.loc[self.df["rank"] == rank][Mativa]
            perdas = self.df.loc[self.df["rank"] == rank][PerdasT]

            ax.scatter(
                perdas,
                massas,
                marker="o",
                color=COLORS[int(rank % len(COLORS))],
                label=f"rank {rank}",
            )

        plt.legend()
