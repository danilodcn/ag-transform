from typing import Iterable

import numpy as np


def is_dominated(gene1: Iterable, gene2: Iterable):
    gene1 = np.asarray(gene1, dtype=np.float32)
    gene2 = np.asarray(gene2, dtype=np.float32)

    if np.any(gene1 <= gene2):
        return False

    else:
        return True
