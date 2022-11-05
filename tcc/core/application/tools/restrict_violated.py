from collections.abc import ItemsView

import pandas as pd

from tcc.core.domain.transformer.entities import Variation, VariationTuple


def count_restrictions_violated(genes: pd.Series, variations: Variation):
    count = 0
    weigh_sum = 0.0
    variation_items: ItemsView[str, VariationTuple] = variations.dict().items()

    for name, variation in variation_items:
        min, max, weigh = variation
        value = genes[name]
        if min < value < max:
            continue
        else:
            # print(f"{min=}, {max=}, {weigh=}, {value=}, {name=}")
            count += 1
            weigh_sum += weigh

    return {"count": count, "weigh": weigh_sum}
