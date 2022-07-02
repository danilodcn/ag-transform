from typing import Dict, List

import pandas as pd


def count_restrictions_violated(gene: List[pd.Series], variations: List[List]):
    count = 0
    # TODO implementar a funcionalidade
    # do usuário passar pesos para cada variação
    for value, variation in zip(gene, variations):
        min, max = variation
        if min < value < max:
            continue
        else:
            count += 1

    # import ipdb; ipdb.set_trace()
    return count


def deal_response(data: Dict[str, Dict]):
    # import ipdb; ipdb.set_trace()
    return 0
