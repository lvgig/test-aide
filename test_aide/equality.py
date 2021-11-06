"""
This module contains helper functions that simplify asserting equality for types
where it is not possible to simply assert a == b (e.g. pandas.DataFrame) or
nested data structures containing these types.

Note, if pandas or numpy is not available when the module is imported then the
functionality of the assert_equal_dispatch will change - so as not to try and
check types from the libraries that are not available.

"""

try:

    import pandas as pd

    has_pandas = True

except ModuleNotFoundError:

    has_pandas = False

try:

    import numpy as np

    has_numpy = True

except ModuleNotFoundError:

    has_numpy = False


def assert_equal_dispatch(expected, actual, msg):
    """This function is used to call specific assert functions depending on the input types.
    Often we are dealing with pandas.DataFrame or pandas.Series objects when asserting
    equality in this project and these types cannot be compared with the standard ==. This
    function allows these types to be compared appropriately as well as allowing objects
    that may contain these pandas types (e.g. list) to also be compared.

    The first assert is that actual and expected are of the same type. If this passes then
    the following types have specific assert functions;
    - pd.DataFrame
    - pd.Series
    - pd.Index
    - np.NaN
    - np.ndarray

    If the inputs are not of the above types then in the case of the following types;
    - list
    - tuple
    - dict
    recursive calls will be made on the elements of the object, again according to
    their tpyes.

    Finally if on object is passed that is not one of any of the above types then the
    standard assert for equality is used.

    Note, if pandas or numpy are not available then the types from those libraries
    will not be considered i.e. if both are not installed then the function will only
    use the standard equality assertion, while still recursively calling itself
    if a list, tuple or dict is passed.

    Parameters
    ----------
    actual : object
        The expected object.

    expected : object
        The actual object.

    msg : string
        A message to be used in the assert, passed onto the specific assert equality function
        that is called.

    """

    if not type(actual) == type(expected):

        raise TypeError(
            f"expected ({type(expected)}) and actual ({type(actual)}) type mismatch"
        )

    if has_pandas and type(expected) is pd.DataFrame:

        assert_frame_equal_msg(actual, expected, msg)

    elif has_pandas and type(expected) is pd.Series:

        assert_series_equal_msg(actual, expected, msg)

    elif has_pandas and isinstance(expected, pd.Index):

        assert_index_equal_msg(actual, expected, msg)

    elif has_numpy and isinstance(expected, float) and np.isnan(expected):

        assert_np_nan_eqal_msg(actual, expected, msg)

    elif has_numpy and type(expected) is np.ndarray:

        assert_array_equal_msg(actual, expected, msg)

    elif type(expected) in [list, tuple]:

        assert_list_tuple_equal_msg(actual, expected, msg)

    elif isinstance(expected, dict):

        assert_dict_equal_msg(actual, expected, msg)

    else:

        assert_equal_msg(actual, expected, msg)


def assert_equal_msg(actual, expected, msg_tag):
    """Compares actual and expected objects and simply asserts equality (==). Adds msg_tag, actual and expected
    values to AssertionException message.

    Parameters
    ----------
    actual : object
        The expected object.

    expected : object
        The actual object.

    msg_tag : string
        A tag for the AssertionException message. Use this to identify mismatching arguments in test output.

    """

    error_msg = f"{msg_tag} -\n  Expected: {expected}\n  Actual: {actual}"

    assert actual == expected, error_msg


def assert_np_nan_eqal_msg(actual, expected, msg):
    """Function to test that both values are np.NaN.

    Parameters
    ----------
    actual : object
        The expected object. Must be an numeric type for np.isnan to run.

    expected : object
        The actual object. Must be an numeric type for np.isnan to run.

    msg : string
        A tag for the AssertionException message.

    """

    assert np.isnan(actual) and np.isnan(
        expected
    ), f"Both values are not equal to np.NaN -\n  Expected: {expected}\n  Actual: {actual}"


def assert_list_tuple_equal_msg(actual, expected, msg_tag):
    """Compares two actual and expected list or tuple objects and asserts equality between the two.
    Error output will identify location of mismatch in items.

    Checks actual and expected are the same type, then equal length then loops through pariwise eleemnts
    and calls assert_equal_dispatch function.

    Parameters
    ----------
    actual : list or tuple
        The actual list or tuple to compare.

    expected : list or tuple
        The expected list or tuple to compare to actual.

    msg_tag : string
        A tag for the AssertionException message.

    """

    if not type(expected) in [list, tuple]:

        raise TypeError(
            f"expected should be of type list or tuple, but got {type(expected)}"
        )

    if not type(actual) in [list, tuple]:

        raise TypeError(
            f"actual should be of type list or tuple, but got {type(actual)}"
        )

    if not type(actual) == type(expected):

        raise TypeError(
            f"expect ({type(expected)}) and actual ({type(actual)}) type mismatch"
        )

    assert len(expected) == len(
        actual
    ), f"Unequal lengths -\n  Expected: {len(expected)}\n  Actual: {len(actual)}"

    for i, (e, a) in enumerate(zip(expected, actual)):

        assert_equal_dispatch(e, a, f"{msg_tag} index {i}")


def assert_dict_equal_msg(actual, expected, msg_tag):
    """Compares two actual and expected dict objects and asserts equality. Error output
    will identify (first) location of mismatch values.

    Checks actual and expected are both dicts, then same number of keys then loops through pariwise
    values from actual and expected and calls assert_equal_dispatch function on these pairs..

    Parameters
    ----------
    actual : dict
        The actual dict to compare.

    expected : dict
        The expected dict to compare to actual.

    msg_tag : string
        A tag for the AssertionException message.

    """

    if not isinstance(expected, dict):

        raise TypeError(f"expected should be of type dict, but got {type(expected)}")

    if not isinstance(actual, dict):

        raise TypeError(f"actual should be of type dict, but got {type(actual)}")

    assert len(expected.keys()) == len(
        actual.keys()
    ), f"Unequal number of keys -\n  Expected: {len(expected.keys())}\n  Actual: {len(actual.keys())}"

    keys_diff_e_a = set(expected.keys()) - set(actual.keys())

    keys_diff_a_e = set(actual.keys()) - set(expected.keys())

    assert (
        keys_diff_e_a == set()
    ), f"Keys in expected not in actual: {keys_diff_e_a}\nKeys in actual not in expected: {keys_diff_a_e}"

    for k in actual.keys():

        assert_equal_dispatch(expected[k], actual[k], f"{msg_tag} key {k}")


def assert_frame_equal_msg(
    actual, expected, msg_tag, print_actual_and_expected=False, **kwargs
):
    """Compares actual and expected pandas.DataFrames and asserts equality.

    Calls pd.testing.assert_frame_equal but presents msg_tag, and optionally actual and expected
    DataFrames, in addition to any other exception info.

    Parameters
    ----------
    actual : pandas DataFrame
        The expected dataframe.

    expected : pandas DataFrame
        The actual dataframe.

    msg_tag : string
        A tag for the assert error message.

    **kwargs:
        Keyword args passed to pd.testing.assert_frame_equal.

    """

    try:

        pd.testing.assert_frame_equal(expected, actual, **kwargs)

    except Exception as e:

        if print_actual_and_expected:

            error_msg = f"""{msg_tag}\nexpected:\n{expected}\nactual:\n{actual}"""

        else:

            error_msg = msg_tag

        raise AssertionError(error_msg) from e


def assert_series_equal_msg(
    actual, expected, msg_tag, print_actual_and_expected=False, **kwargs
):
    """Compares actual and expected pandas.Series and asserts equality.
    Calls pd.testing.assert_series_equal but presents msg_tag, and optionally actual and expected
    Series, in addition to any other exception info.

    Parameters
    ----------
    actual : pandas Series
        The actual Series.

    expected : pandas Series
        The expected Series.

    msg_tag : string
        A tag for the assert error message.

    print_actual_and_expected : Boolean
        print the actual and expected dataFrame along with error message tag

    **kwargs:
        Keyword args passed to pd.testing.assert_series_equal.

    """

    try:

        pd.testing.assert_series_equal(expected, actual, **kwargs)

    except Exception as e:

        if print_actual_and_expected:

            error_msg = f"""{msg_tag}\nexpected:\n{expected}\nactual:\n{actual}"""

        else:

            error_msg = msg_tag

        raise AssertionError(error_msg) from e


def assert_index_equal_msg(
    actual, expected, msg_tag, print_actual_and_expected=False, **kwargs
):
    """Compares actual and expected pandas.Index objects and asserts equality.
    Calls pd.testing.assert_index_equal but presents msg_tag, and optionally actual and expected
    Series, in addition to any other exception info.

    Parameters
    ----------
    actual : pd.Index
        The actual index.

    expected : pd.Index
        The expected index.

    msg_tag : string
        A tag for the assert error message.

    print_actual_and_expected : Boolean
        print the actual and expected valuess along with error message tag

    **kwargs:
        Keyword args passed to pd.testing.assert_index_equal.

    """

    try:

        pd.testing.assert_index_equal(expected, actual, **kwargs)

    except Exception as e:

        if print_actual_and_expected:

            error_msg = f"""{msg_tag}\nexpected:\n{expected}\nactual:\n{actual}"""

        else:

            error_msg = msg_tag

        raise AssertionError(error_msg) from e


def assert_array_equal_msg(
    actual, expected, msg_tag, print_actual_and_expected=False, **kwargs
):
    """Compares actual and expected np.arrays and asserts equality.
    Calls np.testing.assert_array_equal but presents msg_tag, and optionally actual and expected
    arrays, in addition to any other exception info.

    Parameters
    ----------
    actual : numpy array
        The actual array.

    expected : numpy array
        The expected array.

    msg_tag : string
        A tag for the assert error message.

    print_actual_and_expected : Boolean
        print the actual and expected arrays along with error message tag

    **kwargs:
        Keyword args passed to np.testing.assert_array_equal.
    """
    # If actual or expected is a scalar, numpy will check whether each entry in
    # the other array is equal to the scalar. Therefore need to check type.

    if not isinstance(expected, np.ndarray):

        raise TypeError(
            f"expected should be of type numpy ndarray, but got {type(expected)}"
        )

    if not isinstance(actual, np.ndarray):

        raise TypeError(
            f"actual should be of type numpy ndarray, but got {type(actual)}"
        )

    try:

        np.testing.assert_array_equal(expected, actual, **kwargs)

    except Exception as e:

        if print_actual_and_expected:

            error_msg = f"""{msg_tag}\nexpected:\n{expected}\nactual:\n{actual}"""

        else:

            error_msg = msg_tag

        raise AssertionError(error_msg) from e
