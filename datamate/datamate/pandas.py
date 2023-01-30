from typing import Collection

from pandas.api.types import union_categoricals
import pandas


__all__ = [
    "concat_preserving_categorical",
]


def concat_preserving_categorical(
    dfs: Collection[pandas.DataFrame],
    *args,
    **kwargs,
) -> pandas.DataFrame:
    """Concatenate while preserving categorical columns.
    From https://stackoverflow.com/a/57809778.
    """
    adjusted_dfs = [df.copy() for df in dfs]
    for column in set.intersection(
        *[set(df.select_dtypes(include="category").columns) for df in adjusted_dfs]
    ):
        # Generate the union category across dfs for this column
        uc = union_categoricals([df[column] for df in adjusted_dfs])
        # Change to union category for all dataframes
        for index, df in enumerate(adjusted_dfs):
            adjusted_dfs[index] = df.assign(
                **{
                    column: lambda x: pandas.Categorical(
                        x[column].values, categories=uc.categories
                    )
                }
            )
    return pandas.concat(adjusted_dfs, *args, **kwargs)
