import json
import sys
import traceback

import pandas as pd  # type: ignore

from .pandas_statistics import get_single_column_stats

# Return this many of the most common values from a categorical column
DEFAULT_TOP_VALUES = 3


def create_exception_stats(e):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    return {
        "name": "Error getting statistical summary",
        "type": type(e).__name__,
        "summary": str(e),
        "error": tuple(map(lambda x: [x], traceback_lines)),
    }


def get_stat_summary(obj, name, column):
    obj_type = type(obj)
    stats = {}

    # pandas dataframe
    if obj_type.__name__ == "DataFrame":
        if column is None:
            for col_name in obj:
                col = obj[col_name]
                stats[col_name] = get_single_column_stats(col, DEFAULT_TOP_VALUES)
        elif column in obj:
            col = obj[column]
            stats[column] = get_single_column_stats(col, DEFAULT_TOP_VALUES)
    # pandas series
    elif obj_type.__name__ == "Series":
        stats[name] = get_single_column_stats(obj, DEFAULT_TOP_VALUES)

    # numpy 1d array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 1:
        col = pd.Series(obj)
        stats["0"] = get_single_column_stats(col, DEFAULT_TOP_VALUES)

    # numpy 2d array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 2:
        if column is None:
            for col_index in range(0, obj.shape[1]):
                col_name = col_index
                col = pd.Series(obj[:, col_index])
                stats[col_name] = get_single_column_stats(col, DEFAULT_TOP_VALUES)
        else:
            column_int = int(column)
            if column_int >= 0 and column_int < obj.shape[1]:
                col = pd.Series(obj[:, column_int])
                stats[column] = get_single_column_stats(col, DEFAULT_TOP_VALUES)
    # list
    elif obj_type.__name__ == "list" or obj_type.__name__ == "tuple":
        col = pd.Series(obj)
        stats[name] = get_single_column_stats(col, DEFAULT_TOP_VALUES)

    # dictionary
    elif obj_type.__name__ == "dict":
        keys = pd.Series(list(obj.keys()))
        stats["Key"] = get_single_column_stats(keys, DEFAULT_TOP_VALUES)

        values = pd.Series(list(obj.values()))
        stats["Value"] = get_single_column_stats(values, DEFAULT_TOP_VALUES)

    return stats


def get_var_stats(
    obj,
    name,
    column=None,
    **kwargs,
):
    try:
        stats = get_stat_summary(obj, name, column)
    except Exception as e:
        stats = create_exception_stats(e)

    return json.dumps(stats, default=str)
