import pandas as pd

from matplotlib import pyplot as plt


def plot(df: pd.DataFrame):
    Mativa = df["Mativa"]
    PerdasT = df["PerdasT"]

    # g = sns.FacetGrid(df, height=5)
    # g.map(sns.scatterplot, "Mativa", "PerdasT", alpha=.6)
    # g.add_legend()

    _, ax = plt.subplots()

    ax.plot(PerdasT, Mativa, "ko")

    for i, massa, perdas in zip(range(len(Mativa)), Mativa, PerdasT):
        ax.annotate(i, xy=(perdas, massa))

    plt.ioff()
    plt.show()
