import pytest
import inspect

try:

    import pandas as pd
    import test_aide.pandas as ph

    has_pandas = True

except ModuleNotFoundError:

    has_pandas = False


@pytest.mark.skipif(not has_pandas, reason="pandas not installed")
def test_arguments():
    """Test arguments for arguments of test_aide.pandas._check_dfs_passed."""

    expected_arguments = ["df_1", "df_2"]

    arg_spec = inspect.getfullargspec(ph._check_dfs_passed)

    arguments = arg_spec.args

    assert len(expected_arguments) == len(
        arguments
    ), f"Incorrect number of arguments -\n  Expected: {len(expected_arguments)}\n  Actual: {len(arguments)}"

    assert (
        expected_arguments == arguments
    ), f"Incorrect arguments -\n  Expected: {expected_arguments}\n  Actual: {arguments}"

    default_values = arg_spec.defaults

    assert (
        default_values is None
    ), f"Unexpected default values -\n  Expected: None\n  Actual: {default_values}"


@pytest.mark.skipif(not has_pandas, reason="pandas not installed")
def test_exceptions_raised():
    """Test that the expected exceptions are raised by test_aide.pandas._check_dfs_passed."""

    with pytest.raises(
        TypeError, match=r"expecting first positional arg to be a pd.DataFrame.*"
    ):

        ph._check_dfs_passed(1, pd.DataFrame())

    with pytest.raises(
        TypeError, match=r"expecting second positional arg to be a pd.DataFrame.*"
    ):

        ph._check_dfs_passed(pd.DataFrame(), 1)

    with pytest.raises(
        ValueError,
        match=r"expecting first positional arg and second positional arg to have equal number of rows but got\n  1\n  0",
    ):

        ph._check_dfs_passed(pd.DataFrame({"a": 1}, index=[0]), pd.DataFrame())

    with pytest.raises(
        ValueError,
        match=r"expecting indexes for first positional arg and second positional arg to be the same but got\n  Int64Index\(\[0\], dtype='int64'\)\n  Int64Index\(\[1\], dtype='int64'\)",
    ):

        ph._check_dfs_passed(
            pd.DataFrame({"a": 1}, index=[0]), pd.DataFrame({"a": 1}, index=[1])
        )
