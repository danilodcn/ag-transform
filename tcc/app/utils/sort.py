import numpy as np


def is_dominated(gene1: tuple, gene2: tuple):
    gene1 = np.asarray(gene1)
    gene2 = np.asarray(gene2)
    # import ipdb; ipdb.set_trace()

    # if np.all(gene1 == gene2):
    #     return False

    if np.all(gene1 <= gene2):
        return False

    if np.any(gene1 <= gene2):
        return False

    else:
        return True
