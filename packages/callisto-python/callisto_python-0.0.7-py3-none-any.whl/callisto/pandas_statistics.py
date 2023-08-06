import pandas as pd  # type: ignore
from pandas.api.types import is_categorical_dtype  # type: ignore
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype


def get_single_column_stats(col, n_top_values):
    series_stats = {}
    series_stats["na_count"] = int(col.isna().sum())

    if is_numeric_dtype(col):
        series_stats["type"] = "numeric"
        series_stats["min"] = col.min()
        series_stats["max"] = col.max()
        series_stats["mean"] = col.mean()

    elif is_categorical_dtype(col) or (
        is_string_series(col) and is_series_categorical(col)
    ):
        series_stats["type"] = "category"
        series_stats["top_values"] = get_most_common_values(col, n_top_values)
        series_stats["unique_count"] = col.nunique()

    elif is_datetime64_any_dtype(col):
        series_stats["type"] = "date"
        series_stats["min"] = col.min()
        series_stats["max"] = col.max()
        series_stats["unique_count"] = col.nunique()

    else:
        series_stats["type"] = "misc"
        series_stats["unique_count"] = col.nunique()

    return series_stats


def get_most_common_values(col, n_top_values):
    top_3 = (
        col.value_counts()
        .nlargest(n_top_values, keep="all")
        .sort_index()
        .sort_values(ascending=False)
    )

    length = n_top_values if top_3.size >= n_top_values else top_3.size
    return {top_3.index[i]: int(top_3.values[i]) for i in range(0, length)}


def is_series_categorical(col):
    # If a string column has more than 5% repeating values,
    # Consider it to be a categorical dataset
    size = col.count()
    n_unique = col.nunique(dropna=False)
    return (size - n_unique) / size > 0.05


def is_string_series(col):
    if isinstance(col.dtype, pd.StringDtype):
        return True
    elif col.dtype == "object":
        # Object series, check each value
        return all((v is None) or isinstance(v, str) for v in col)
    else:
        return False
