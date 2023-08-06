import json
import sys
import traceback

import numpy as np  # type: ignore

KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776

DEFAULT_PAGE_SIZE = 50


def human_bytes(B):
    """Return the given bytes as a human friendly KB, MB, GB, or TB string"""
    B = float(B)

    if B < KB:
        return "{0} {1}".format(B, "Bytes" if B > 1 else "Byte")
    elif KB <= B < MB:
        return "{0:.2f} KB".format(B / KB)
    elif MB <= B < GB:
        return "{0:.2f} MB".format(B / MB)
    elif GB <= B < TB:
        return "{0:.2f} GB".format(B / GB)
    elif TB <= B:
        return "{0:.2f} TB".format(B / TB)


def make_multi_dict(row_names, column_names, data, total_row_count, total_column_count):
    """
    column_count and row_count should be values for the whole data structure
    column_names and row_names are values for the possibly abbreviated structure
    """
    if type(column_names) == str:
        column_names = [column_names]
    if type(row_names) == str:
        row_names == [row_names]
    value = {
        "column_count": total_column_count,
        "row_count": total_row_count,
        "column_names": column_names,
        "row_names": row_names,
        "data": data,
    }
    return {"multi_value": value}


def validate_value(value, no_preview=False):
    if value is None and no_preview:
        return None
    if list(value.keys()) == ["single_value"]:
        return {"single_value": str(value["single_value"])}
    elif list(value.keys()) == ["multi_value"]:
        val = value["multi_value"]
        if val["column_names"] is not None:
            val["column_names"] = list(map(str, val["column_names"]))
        if val["row_names"] is not None:
            val["row_names"] = list(map(str, val["row_names"]))
        if val["data"] is not None:
            # double map through the nested arrays in 'data'
            val["data"] = list(map(lambda x: list(map(str, x)), val["data"]))
        return {"multi_value": val}
    else:
        msg = (
            "Value should be single entry dict with a key of "
            "'single_value' or 'multi_value'."
        )
        msg += f" Found keys: {tuple(value.keys())}"
        raise ValueError(msg)


def get_list_var(
    obj,
    name,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    """
    sort_by: expects a list with a single string, ["value"] to sort list by values
    ascending: expects a list with single boolean
    """
    summary = f"Length: {len(obj)}"
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            filter = filters[0]
            if "col" in filter and str(filter["col"]).lower() in [
                "value",
                "values",
                name,
            ]:
                if "search" in filter and isinstance(filter["search"], str):
                    obj_filtered = [
                        x
                        for x in obj_filtered
                        if filter["search"].lower() in str(x).lower()
                    ]
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            len(obj_filtered) > start + page_size if page_size is not None else False
        )
        end = start + page_size if has_next_page else len(obj_filtered)

        if (
            isinstance(sort_by, list)
            and len(sort_by) > 0
            and isinstance(sort_by[0], str)
            and sort_by[0].lower() == "value"
        ):
            if (
                isinstance(ascending, list)
                and len(ascending) > 0
                and isinstance(ascending[0], bool)
            ):
                reverse = not ascending[0]
            else:
                reverse = False

            obj_sorted = sorted(
                obj_filtered, key=lambda x: str(x).lower(), reverse=reverse
            )
        else:
            obj_sorted = obj_filtered

        obj_pre = obj_sorted[start:end]
        data = tuple(map(lambda x: [str(x)], obj_pre))
        row_names = list(range(start, end))
        preview = make_multi_dict(
            row_names,
            name,
            data,
            total_row_count=len(obj_filtered),
            total_column_count=1,
        )
    else:
        preview = make_multi_dict(
            None, None, None, total_row_count=len(obj), total_column_count=1
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_dict_var(
    obj,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=[],
    ascending=[True],
    filters=None,
):
    """
    sort_by: expects a list with a single item, either ["key"] or ["value"]
    ascending: expects a list with single boolean
    """
    summary = f"Length: {len(obj)}"
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            for filter in filters:
                if "col" not in filter:
                    continue

                col = str(filter["col"]).lower()
                if "search" in filter and isinstance(filter["search"], str):
                    search = filter["search"].lower()
                    if col == "value":
                        obj_filtered = {
                            k: v
                            for k, v in obj_filtered.items()
                            if search in str(v).lower()
                        }
                    elif col == "key":
                        obj_filtered = {
                            k: v
                            for k, v in obj_filtered.items()
                            if search in str(k).lower()
                        }
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            len(obj_filtered) > start + page_size if page_size is not None else False
        )
        end = start + page_size if has_next_page else len(obj_filtered)

        if (
            isinstance(sort_by, list)
            and len(sort_by) > 0
            and isinstance(sort_by[0], str)
        ):
            obj_sorted = []

            if (
                isinstance(ascending, list)
                and len(ascending) > 0
                and isinstance(ascending[0], bool)
            ):
                reverse = not ascending[0]
            else:
                reverse = False

            if sort_by[0].lower() == "key":
                obj_sorted = sorted(obj_filtered.items(), reverse=reverse)
            elif sort_by[0].lower() == "value":
                obj_sorted = sorted(
                    obj_filtered.items(),
                    key=lambda item: str(item[1]).lower(),
                    reverse=reverse,
                )
            else:
                obj_sorted = obj_filtered.items()
        else:
            obj_sorted = obj_filtered.items()

        obj_pre = {
            key: val
            for i, (key, val) in enumerate(obj_sorted)
            if i >= start and i < end
        }

        data = tuple(map(lambda x: [str(x[0]), str(x[1])], obj_pre.items()))
        row_names = list(range(start, end))
        preview = make_multi_dict(
            row_names,
            ["Key", "Value"],
            data,
            total_row_count=len(obj_filtered),
            total_column_count=2,
        )
    else:
        preview = make_multi_dict(
            None, None, None, total_row_count=len(obj), total_column_count=2
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_numpy_2d_var(
    obj,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    """
    sort_by: list of indexes (integers) to sort
    ascending: expects a list with single boolean
    """
    summary = f"Size: {obj.shape[0]}x{obj.shape[1]} Memory: {human_bytes(obj.nbytes)}"
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            for filter in filters:
                if "col" not in filter:
                    continue

                col = int(filter["col"])
                if col >= obj_filtered.shape[1] or col < 0:
                    continue

                col_is_numeric = obj_filtered[:, col].dtype.kind in "iufc"

                if "search" in filter and isinstance(filter["search"], str):
                    obj_filtered = obj_filtered[
                        np.char.count(
                            np.char.lower(obj_filtered[:, col].astype("str")),
                            filter["search"],
                        )
                        > 0
                    ]
                if (
                    "min" in filter
                    and isinstance(filter["min"], (int, float))
                    and col_is_numeric
                ):
                    obj_filtered = obj_filtered[obj_filtered[:, col] >= filter["min"]]
                if (
                    "max" in filter
                    and isinstance(filter["max"], (int, float))
                    and col_is_numeric
                ):
                    obj_filtered = obj_filtered[obj_filtered[:, col] <= filter["max"]]
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            obj_filtered.shape[0] > start + page_size
            if page_size is not None
            else False
        )
        end = start + page_size if has_next_page else obj_filtered.shape[0]

        if isinstance(sort_by, list) and len(sort_by) > 0:
            obj_sorted = (
                obj_filtered
                if obj_filtered.dtype != "O"
                else obj_filtered.astype("str")
            )
            params = []

            if (
                isinstance(ascending, list)
                and len(ascending) > 0
                and isinstance(ascending[0], bool)
            ):
                asc_value = ascending[0]
            else:
                asc_value = True

            # Enter the columns in reverse order, because the
            # last index will be the primary sort index (which is backwards from pandas)
            for col in sort_by:
                params.insert(0, obj_sorted[:, col])
            if asc_value:
                obj_sorted = obj_sorted[np.lexsort(params), :]
            else:
                obj_sorted = obj_sorted[np.lexsort(params), :][::-1]
        else:
            obj_sorted = obj_filtered

        obj_pre = obj_sorted[start:end]
        data = obj_pre.tolist()
        row_names = list(range(start, end))
        column_names = list(range(obj_pre.shape[1]))
        preview = make_multi_dict(
            row_names, column_names, data, obj_filtered.shape[0], obj_filtered.shape[1]
        )
    else:
        preview = make_multi_dict(
            None,
            None,
            None,
            total_row_count=obj.shape[0],
            total_column_count=obj.shape[1],
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_numpy_1d_var(
    obj,
    name,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    summary = f"Length: {obj.shape[0]} Memory: {human_bytes(obj.nbytes)}"
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            filter = filters[0]
            if "col" in filter and str(filter["col"]).lower() in [
                "value",
                "values",
                name,
            ]:
                is_numeric = obj_filtered.dtype.kind in "iufc"

            if "search" in filter and isinstance(filter["search"], str):
                obj_filtered = obj_filtered[
                    np.char.count(
                        np.char.lower(obj_filtered.astype("str")), filter["search"]
                    )
                    > 0
                ]
            if (
                "min" in filter
                and isinstance(filter["min"], (int, float))
                and is_numeric
            ):
                obj_filtered = obj_filtered[obj_filtered >= filter["min"]]
            if (
                "max" in filter
                and isinstance(filter["max"], (int, float))
                and is_numeric
            ):
                obj_filtered = obj_filtered[obj_filtered <= filter["max"]]
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            obj_filtered.shape[0] > start + page_size
            if page_size is not None
            else False
        )
        end = start + page_size if has_next_page else obj_filtered.size

        if (
            isinstance(sort_by, list)
            and len(sort_by) > 0
            and isinstance(sort_by[0], str)
        ):
            sort_by_param = sort_by[0].lower()
        elif isinstance(sort_by, str):
            sort_by_param = sort_by.lower()
        else:
            sort_by_param = None

        if sort_by_param:
            if (
                isinstance(ascending, list)
                and len(ascending) > 0
                and isinstance(ascending[0], bool)
            ):
                asc_value = ascending[0]
            elif isinstance(ascending, bool):
                asc_value = ascending
            else:
                asc_value = True

            if sort_by_param in ["value", "values", name]:
                if obj_filtered.dtype == "O":
                    obj_sorted = np.sort(obj_filtered.astype("str"))
                else:
                    obj_sorted = np.sort(obj_filtered)
                if not asc_value:
                    obj_sorted = np.flip(obj_sorted)
            else:
                obj_sorted = obj_filtered
        else:
            obj_sorted = obj_filtered

        obj_pre = obj_sorted[start:end]
        data = tuple(map(lambda x: [str(x)], obj_pre.tolist()))
        row_names = list(range(start, end))
        column_names = name
        preview = make_multi_dict(
            row_names,
            column_names,
            data,
            total_row_count=obj_filtered.shape[0],
            total_column_count=1,
        )
    else:
        preview = make_multi_dict(
            None, None, None, total_row_count=obj.shape[0], total_column_count=1
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_pandas_dataframe_var(
    obj,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    """
    sort_by: list of strings (names of columns to sort), or ["index"] to sort by index
    ascending: list of booleans (must match length of sort_by), or single boolean
    """
    summary = (
        f"Size: {obj.shape[0]}x{obj.shape[1]}"
        + f" Memory: {human_bytes(obj.memory_usage(deep=True).sum())}"
    )
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            for filter in filters:
                if "col" not in filter or filter["col"] not in obj:
                    continue
                col_name = filter["col"]
                col_is_numeric = obj_filtered[col_name].dtype.kind in "iufc"

                if "search" in filter and isinstance(filter["search"], str):
                    obj_filtered = obj_filtered.loc[
                        obj_filtered[col_name]
                        .apply(str)
                        .str.contains(filter["search"], case=False)
                    ]
                if (
                    "min" in filter
                    and isinstance(filter["min"], (int, float))
                    and col_is_numeric
                ):
                    obj_filtered = obj_filtered[obj_filtered[col_name] >= filter["min"]]
                if (
                    "max" in filter
                    and isinstance(filter["max"], (int, float))
                    and col_is_numeric
                ):
                    obj_filtered = obj_filtered[obj_filtered[col_name] <= filter["max"]]
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            obj_filtered.shape[0] > start + page_size
            if page_size is not None
            else False
        )
        end = start + page_size if has_next_page else obj_filtered.shape[0]

        if isinstance(sort_by, list) and len(sort_by) > 0:
            sort_index = len(sort_by) == 1 and sort_by[0].lower() == "index"

            if isinstance(ascending, list) and len(ascending) == len(sort_by):
                asc = ascending
            elif isinstance(ascending, bool):
                asc = ascending
            else:
                asc = True

            if sort_index:
                obj_sorted = obj_filtered.sort_index(ascending=asc, inplace=False)
            else:
                obj_sorted = obj_filtered.sort_values(
                    by=sort_by, ascending=asc, inplace=False
                )
        else:
            obj_sorted = obj_filtered

        obj_pre = obj_sorted.iloc[start:end]

        data = obj_pre.to_numpy().tolist()
        row_names = tuple(map(lambda x: str(x), obj_pre.index.to_list()))
        column_names = obj_pre.columns.to_list()
        preview = make_multi_dict(
            row_names, column_names, data, obj_filtered.shape[0], obj_filtered.shape[1]
        )
    else:
        preview = make_multi_dict(
            None,
            None,
            None,
            total_row_count=obj.shape[0],
            total_column_count=obj.shape[1],
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_pandas_series_var(
    obj,
    name,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    """
    sort_by: list of strings (either "index" or "value")
    ascending: expects a list with a single boolean
    """
    summary = f"Length: {len(obj)} Memory: {human_bytes(obj.memory_usage(deep=True))}"
    has_next_page = False
    preview = None
    if not no_preview:

        if filters and isinstance(filters, list):
            obj_filtered = obj.copy()
            filter = filters[0]
            if "col" in filter and str(filter["col"]).lower() in [
                "value",
                "values",
                name,
            ]:
                is_numeric = obj_filtered.dtype.kind in "iufc"

            if "search" in filter and isinstance(filter["search"], str):
                obj_filtered = obj_filtered.loc[
                    obj_filtered.apply(str).str.contains(filter["search"], case=False)
                ]
            if (
                "min" in filter
                and isinstance(filter["min"], (int, float))
                and is_numeric
            ):
                obj_filtered = obj_filtered[obj_filtered >= filter["min"]]
            if (
                "max" in filter
                and isinstance(filter["max"], (int, float))
                and is_numeric
            ):
                obj_filtered = obj_filtered[obj_filtered <= filter["max"]]
        else:
            obj_filtered = obj

        start = page_size * page if page_size else 0
        has_next_page = (
            obj_filtered.size > start + page_size if page_size is not None else False
        )
        end = start + page_size if has_next_page else obj_filtered.size

        if (
            isinstance(sort_by, list)
            and len(sort_by) > 0
            and isinstance(sort_by[0], str)
        ):
            sort_by_param = sort_by[0].lower()
        elif isinstance(sort_by, str):
            sort_by_param = sort_by.lower()
        else:
            sort_by_param = None

        if sort_by_param:
            if (
                isinstance(ascending, list)
                and len(ascending) > 0
                and isinstance(ascending[0], bool)
            ):
                asc_value = ascending[0]
            elif isinstance(ascending, bool):
                asc_value = ascending
            else:
                asc_value = True

            if sort_by_param in ["value", "values", name]:
                obj_sorted = obj_filtered.sort_values(
                    ascending=asc_value,
                    key=lambda col: col.map(lambda x: str(x).lower()),
                )
            elif sort_by_param == "index":
                obj_sorted = obj_filtered.sort_index(ascending=asc_value)
            else:
                obj_sorted = obj_filtered
        else:
            obj_sorted = obj_filtered

        obj_pre = obj_sorted.iloc[start:end]
        data = tuple(map(lambda x: [str(x)], obj_pre.to_list()))
        row_names = tuple(map(lambda x: str(x), obj_pre.index.to_list()))
        preview = make_multi_dict(
            row_names,
            name,
            data,
            total_row_count=obj_filtered.size,
            total_column_count=1,
        )
    else:
        preview = make_multi_dict(
            None, None, None, total_row_count=obj.size, total_column_count=1
        )
    return (
        summary,
        has_next_page,
        preview,
    )


def get_var_details(
    obj,
    name,
    no_preview=False,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
):
    """
    Get formatted info for a specific var. Pass page_size=None
    to get non-abbreviated variable info. Pass no_preview=True to exclude the
    preview of the var's data
    """
    obj_type = type(obj)
    summary = ""
    value = None
    # Is there a next page available for the variable
    has_next_page = False

    # check custom values (careful not to call summary / value on
    # the Class object, only on the instances)
    if (
        obj_type != type
        and hasattr(obj, "jupyter_d1_summary")
        and callable(getattr(obj, "jupyter_d1_summary"))
    ):
        summary = obj.jupyter_d1_summary()
        if hasattr(obj, "jupyter_d1_value") and callable(
            getattr(obj, "jupyter_d1_value")
        ):
            value = obj.jupyter_d1_value()
        else:
            value = None

    # single valued intrinsics
    elif obj_type.__name__ in ["int", "str", "float", "bool", "complex"]:
        summary = obj
        value = {"single_value": str(obj)}

    # list
    elif obj_type.__name__ == "list" or obj_type.__name__ == "tuple":
        summary, has_next_page, value = get_list_var(
            obj,
            name,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # dictionary
    elif obj_type.__name__ == "dict":
        summary, has_next_page, value = get_dict_var(
            obj,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # numpy 2D array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 2:
        summary, has_next_page, value = get_numpy_2d_var(
            obj,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # numpy 1D array
    elif obj_type.__name__ == "ndarray" and obj.ndim == 1:
        summary, has_next_page, value = get_numpy_1d_var(
            obj,
            name,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # pandas data frame
    elif obj_type.__name__ == "DataFrame":
        summary, has_next_page, value = get_pandas_dataframe_var(
            obj,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # pandas series
    elif obj_type.__name__ == "Series":
        summary, has_next_page, value = get_pandas_series_var(
            obj,
            name,
            no_preview,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )

    # if all else fails, fall back to single value string representation
    else:
        summary = str(obj)
        value = {"single_value": str(obj)}

    return {
        "name": name,
        "type": obj_type.__name__,
        "has_next_page": bool(has_next_page),
        "summary": str(summary)[:140],  # limit summary length
        "value": validate_value(value, no_preview),
    }


def create_exception_var(e):
    exc_type, exc_value, exc_tb = sys.exc_info()
    traceback_lines = traceback.format_exception(exc_type, exc_value, exc_tb)
    return {
        "name": "Introspection Error",
        "type": type(e).__name__,
        "summary": str(e),
        "has_next_page": str(False),
        "value": {
            "multi_value": {
                "column_count": 1,
                "row_count": len(traceback_lines),
                "column_names": "Traceback",
                "row_names": list(range(len(traceback_lines))),
                "data": tuple(map(lambda x: [x], traceback_lines)),
            }
        },
    }


def format_vars(
    vars_output,
    abbrev_len=DEFAULT_PAGE_SIZE,
    no_preview=False,
    **kwargs,
):
    """
    Get string containing json representation of currently defined vars
    (pass the output of `vars()` to this function)

    kwargs currently only serve to make this API a little bit future-proof
    """
    try:
        current_vars = []
        for item in tuple(vars_output.items()):
            name = item[0]
            obj = item[1]
            if name.startswith("__") or name.startswith("@py_assert"):
                continue
            obj_type = type(obj)
            if obj_type.__name__ in ["type", "module", "function"]:
                continue

            var_details = get_var_details(
                obj,
                name,
                no_preview=no_preview,
                page_size=abbrev_len,
            )

            current_vars.append(var_details)

    except Exception as e:
        current_vars = [create_exception_var(e)]

    return json.dumps(current_vars)


def format_var(
    obj,
    name,
    page_size=DEFAULT_PAGE_SIZE,
    page=0,
    sort_by=None,
    ascending=None,
    filters=None,
    **kwargs,
):
    """Get string containing json representation of a var"""
    try:
        var_details = get_var_details(
            obj,
            name,
            page_size=page_size,
            page=page,
            sort_by=sort_by,
            ascending=ascending,
            filters=filters,
        )
        return json.dumps(var_details)
    except Exception as e:
        var_details = create_exception_var(e)

    return json.dumps(var_details)
