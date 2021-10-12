"""This module contains functions that create simple datasets that are used in the tests."""

import pandas as pd


def create_df_1():
    """Create simple DataFrame with the following...

    6 rows
    2 columns;
    - a integer 1:6
    - b object a:f
    no nulls
    """

    df = pd.DataFrame({"a": [1, 2, 3, 4, 5, 6], "b": ["a", "b", "c", "d", "e", "f"]})

    return df
