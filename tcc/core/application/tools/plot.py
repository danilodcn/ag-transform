import io
from pathlib import Path

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

    def __basic_plot(self, title: str = ""):
        fig, ax = plt.subplots()
        # ax.set_title(title)
        fig.suptitle(title)
        ax.set_xlabel("Perdas Totais [W]")
        ax.set_ylabel("Massa [Kg]")

        return fig, ax

    def plot(self, df: pd.DataFrame, title=""):
        _, ax = self.__basic_plot(title)

        PerdasT = df["PerdasT"]
        Mativa = df["Mativa"]
        Mativa = df["Jat"]
        PerdasT = df["Jbt"]

        ax.plot(PerdasT, Mativa, "ko")

        dx = max(PerdasT) - min(PerdasT)
        dy = max(Mativa) - min(Mativa)

        kx = dx / 100
        ky = dy * 0
        iterator = zip(range(len(Mativa)), Mativa, PerdasT)
        for i, massa, perdas in iterator:
            ax.annotate(str(i), xy=(perdas + kx, massa + ky))

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(dpi=100):
        dir_name = "/tmp/tcc/images"
        dir = Path(dir_name)
        dir.mkdir(parents=True, exist_ok=True)
        figs = [plt.figure(n) for n in plt.get_fignums()]
        for fig in figs:
            fig.get_axes()
            with io.BytesIO() as buffer:
                fig.savefig(buffer, format="jpg", dpi=dpi)
                fig_title: str = fig.texts[0].get_text()  # type: ignore
                fp = dir / f"{fig_title}.jpg"
                fp.write_bytes(buffer.getvalue())

    def plot_with_rank(self, title="Points with ranks", penalize=False):
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
