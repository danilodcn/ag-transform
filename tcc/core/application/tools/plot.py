import io
from collections import defaultdict
from pathlib import Path
from typing import Iterable, Literal, Tuple
from uuid import uuid4

import pandas as pd
from matplotlib import pyplot as plt
from matplotlib._color_data import TABLEAU_COLORS
from matplotlib.backends.backend_pdf import PdfPages

COLORS = list(TABLEAU_COLORS.values())
NUMBER_OF_COLORS = len(COLORS)


class Plot:

    LABEL_NAMES = defaultdict(
        lambda: "",
        **{
            "Mativa": "Massa [Kg]",
            "Mativa_P": "Massa [Kg] (após penalização)",
            "PerdasT": "Perdas Totais [W]",
            "PerdasT_P": "Perdas Totais [W] (após penalização)",
            "Jat": "Indução (alta tensão)",
            "Jbt": "Indução (baixa tensão)",
        },
    )

    def __basic_plot(self, title: str = ""):
        fig, ax = plt.subplots()
        fig.title = title or f"figure-{fig.number}"  # type: ignore
        fig.suptitle(title)
        return fig, ax

    def plot(
        self,
        df: pd.DataFrame,
        field_names: Iterable[str],
        with_ranks=False,
        title="",
        size: Tuple[float, float] = (10, 10),
    ):
        _, ax = self.__basic_plot(title)
        plt.gcf().set_size_inches(*size)
        x_name, y_name = field_names
        x_label = self.LABEL_NAMES[x_name]
        y_label = self.LABEL_NAMES[y_name]

        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)

        x_data = df[x_name]
        y_data = df[y_name]

        dx = max(x_data) - min(x_data)
        dy = max(y_data) - min(y_data)

        kx = dx / 100
        ky = dy * 0
        iterator = zip(range(len(y_data)), y_data, x_data)
        for i, massa, perdas in iterator:
            ax.annotate(str(i), xy=(perdas + kx, massa + ky))
        if with_ranks:
            ranks = list(df["rank"].drop_duplicates())
            ranks.sort()
            for rank in ranks:
                filtered_df = df.loc[df["rank"] == rank]
                x_data = filtered_df[x_name]
                y_data = filtered_df[y_name]
                ax.scatter(
                    x_data,
                    y_data,
                    # marker="o",
                    color=COLORS[int(rank % NUMBER_OF_COLORS)],
                    label=f"rank {rank}",
                )
            ax.legend()
        else:
            ax.plot(x_data, y_data, "ko")

    @staticmethod
    def show():
        plt.show()

    @staticmethod
    def save(
        suffix="",
        dir_name="",
        type: Literal["jpg", "png", "pdf"] = "jpg",
        dpi=100,
    ):
        dir_name = f"/tmp/tcc/images/{dir_name}"
        dir = Path(dir_name)
        dir.mkdir(parents=True, exist_ok=True)
        format = type.lower()
        if format == "pdf":
            Plot.save_pdf(dir, suffix)
        else:
            Plot.save_images(dir, suffix, format, dpi)

    @staticmethod
    def save_images(dir: Path, suffix="", format="jpg", dpi=100):
        figs = [plt.figure(n) for n in plt.get_fignums()]
        for fig in figs:
            with io.BytesIO() as buffer:
                fig.savefig(buffer, format=format, dpi=dpi)
                fig_title: str = f"{fig.title}-{suffix}"  # type: ignore
                fp = dir / f"{fig_title}.{format}"
                fp.write_bytes(buffer.getvalue())

            plt.close(fig)

    @staticmethod
    def save_pdf(dir: Path, suffix=""):
        if not suffix:
            uuid = uuid4()
            suffix = uuid.hex
        figs = [plt.figure(n) for n in plt.get_fignums()]
        pdf = PdfPages(f"{dir}/{suffix}.pdf")
        for fig in figs:
            pdf.savefig(fig)
            plt.close(fig)
        pdf.close()

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
