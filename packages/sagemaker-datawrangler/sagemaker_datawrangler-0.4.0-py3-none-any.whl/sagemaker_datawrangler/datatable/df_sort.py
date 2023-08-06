from itertools import chain
from typing import Any, Dict, List

import pandas as pd


def _flatten_dict(outliers: Dict[str, Dict[str, List[Any]]]):
    return {
        col_name: set(chain.from_iterable(outliers[col_name].values()))
        for col_name in outliers
    }


def sort_df_rows_by_cell_highlight_count(df, cell_highlights, keep_sort_key=False):
    """
    Sort dataframe rows by maxium number of outliers in the row. Outliers here are all the values
    that can trigger a data quality issue to be generated
    """

    def _get_row_key(seq: pd.Series, outliers: Dict[str, List]):
        return sum(
            [values in outliers.get(col, set()) for col, values in seq.iteritems()]
        )

    outliers = _flatten_dict(cell_highlights)
    df["sort_key"] = df.apply(lambda row: _get_row_key(row, outliers), axis=1)
    df = df.sort_values(by="sort_key", ascending=False)
    if not keep_sort_key:
        df = df.drop("sort_key", axis=1)
    return df


def sort_df_rows_by_highlight_in_the_column(
    df, cell_highlights, col_name, keep_sort_key=False
):
    """
    Sort dataframe rows by outliers in the column. Outliers here are all the values
    that can trigger a data quality issue to be generated
    """
    outliers = set(_flatten_dict(cell_highlights).get(col_name))
    if outliers:
        df["sort_key"] = df[col_name].map(lambda val: int(val in outliers))
        df = df.sort_values(by="sort_key", ascending=False)
        if not keep_sort_key:
            df = df.drop("sort_key", axis=1)
    return df
