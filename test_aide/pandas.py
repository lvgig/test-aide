"""
This module contains helper functions that create pytest params subsets of input
pandas.DataFrames to repeat tests that transform data more easily on susbsets of
the passed data.

Note, if either pandas or numpy libraries are not installed then this module will
not be available when the package is loaded.

"""

import pytest

try:

    import pandas as pd

except ModuleNotFoundError as err:

    raise ImportError(
        "pandas must be installed to use functionality in pandas module"
    ) from err

try:

    import numpy as np

except ModuleNotFoundError as err:

    raise ImportError(
        "numpy must be installed to use functionality in pandas module"
    ) from err


def _check_dfs_passed(df_1, df_2):
    """Function to check that two pd.DataFrames have equal indexes.

    Parameters
    ----------
    df_1 : pd.DataFrame
        First df to compare

    df_2 : pd.DataFrame
        Second df to compare

    Raises
    ------
    TypeError
        If the first or second positional arg is not a pd.DataFrame

    ValueError
        If the first and second positional args do not have the same number of rows

    ValueError
        If the first and second positonal args do not have equal indexes

    """

    if not type(df_1) is pd.DataFrame:
        raise TypeError(
            f"expecting first positional arg to be a pd.DataFrame but got {type(df_1)}"
        )

    if not type(df_2) is pd.DataFrame:
        raise TypeError(
            f"expecting second positional arg to be a pd.DataFrame but got {type(df_2)}"
        )

    if df_1.shape[0] != df_2.shape[0]:
        raise ValueError(
            f"expecting first positional arg and second positional arg to have equal number of rows but got\n  {df_1.shape[0]}\n  {df_2.shape[0]}"
        )

    if not (df_1.index == df_2.index).all():
        raise ValueError(
            f"expecting indexes for first positional arg and second positional arg to be the same but got\n  {df_1.index}\n  {df_2.index}"
        )


def row_by_row_params(df_1, df_2):
    """Helper function to split input pd.DataFrames pairs into a list of pytest.params of individual row pairs and a final
    pytest.param of the original inputs.

    This function can be used in combination with the pytest.mark.parametrize decorator to easily test that a transformer
    transform method is giving the expected outputs, when called row by row as well as multi row inputs.
    """

    _check_dfs_passed(df_1, df_2)

    params = [
        pytest.param(df_1.loc[[i]].copy(), df_2.loc[[i]].copy(), id=f"index {i}")
        for i in df_1.index
    ]

    params.append(pytest.param(df_1, df_2, id=f"all rows ({df_1.shape[0]})"))

    return params


def index_preserved_params(df_1, df_2, seed=0):
    """Helper function to create copies of input pd.DataFrames pairs in a list of pytest.params where each copy has a different
    index (random, increasing and decreasing), the last item in the list is a pytest.param of the original inputs.

    This function can be used in combination with the pytest.mark.parametrize decorator to easily test that a transformer
    transform method preserves the index of the input.
    """

    _check_dfs_passed(df_1, df_2)

    # create random, increasing and decreasing indexes to set on df args then run func with
    np.random.seed(seed)
    random_index = np.random.randint(low=-99999999, high=100000000, size=df_1.shape[0])
    start_decreasing_index = np.random.randint(low=-99999999, high=100000000, size=1)[0]
    decreasing_index = range(
        start_decreasing_index, start_decreasing_index - df_1.shape[0], -1
    )
    start_increasing_index = np.random.randint(low=-99999999, high=100000000, size=1)[0]
    increasing_index = range(
        start_increasing_index, start_increasing_index + df_1.shape[0], 1
    )

    index_names = ["random", "decreasing", "increasing"]
    indexes = [random_index, decreasing_index, increasing_index]

    params = []

    for index, index_name in zip(indexes, index_names):

        df_1_copy = df_1.copy()
        df_2_copy = df_2.copy()

        df_1_copy.index = index
        df_2_copy.index = index

        params.append(pytest.param(df_1_copy, df_2_copy, id=f"{index_name} index"))

    params.append(pytest.param(df_1, df_2, id="original index"))

    return params


def adjusted_dataframe_params(df_1, df_2, seed=0):
    """Wrapper function to create copies of input pd.DataFrames pairs and adjust
    either the index of the dataframe, or split the dataframe into individual rows.
    The last item in the list is a pytest.param of the original inputs.

    This function can be used in combination with the pytest.mark.parametrize decorator
    to easily test that a transformer transform method preserves the index of the input,
    and gives the expected outputs, when called row by row as well as multi row inputs.
    """

    row_params = row_by_row_params(df_1, df_2)
    index_params = index_preserved_params(df_1, df_2, seed)

    # remove last row param as this is a duplication of the last item of index_params
    return row_params[:-1] + index_params
