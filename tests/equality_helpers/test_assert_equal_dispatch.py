import inspect
import pytest
import test_aide.equality as eh
from collections import defaultdict
import pandas as pd
import numpy as np
from unittest.mock import _get_target


# potential functions that test_aide.equality.assert_equal_dispatch can call
potential_assert_functions = [
    "test_aide.equality.assert_frame_equal_msg",
    "test_aide.equality.assert_series_equal_msg",
    "test_aide.equality.assert_index_equal_msg",
    "test_aide.equality.assert_list_tuple_equal_msg",
    "test_aide.equality.assert_dict_equal_msg",
    "test_aide.equality.assert_equal_msg",
    "test_aide.equality.assert_np_nan_eqal_msg",
    "test_aide.equality.assert_array_equal_msg",
]


def test_arguments():
    """Test arguments for arguments of test_aide.equality.assert_equal_dispatch."""

    expected_arguments = ["expected", "actual", "msg"]

    arg_spec = inspect.getfullargspec(eh.assert_equal_dispatch)

    arguments = arg_spec.args

    assert len(expected_arguments) == len(
        arguments
    ), f"Incorrect number of arguments -\n  Expected: {len(expected_arguments)}\n  Actual: {len(arguments)}"

    for i, (e, a) in enumerate(zip(expected_arguments, arguments)):

        assert e == a, f"Incorrect arg at index {i} -\n  Expected: {e}\n  Actual: {a}"

    default_values = arg_spec.defaults

    assert (
        default_values is None
    ), f"Unexpected default values -\n  Expected: None\n  Actual: {default_values}"


def test_different_types_error():
    """Test that an exception is raised if expected and actual are different types."""

    with pytest.raises(TypeError, match="type mismatch"):

        eh.assert_equal_dispatch(expected=1, actual=1.0, msg="test_msg")


@pytest.mark.parametrize(
    "test_function_call, expected_value, pd_testing_function",
    [
        (
            "test_aide.equality.assert_frame_equal_msg",
            pd.DataFrame({"a": [1, 2]}),
            pd.testing.assert_frame_equal,
        ),
        (
            "test_aide.equality.assert_series_equal_msg",
            pd.Series([1, 2]),
            pd.testing.assert_series_equal,
        ),
        (
            "test_aide.equality.assert_index_equal_msg",
            pd.Index([1, 2]),
            pd.testing.assert_index_equal,
        ),
    ],
)
def test_pd_types_correct_function_call(
    mocker, test_function_call, expected_value, pd_testing_function
):
    """Test that the correct 'sub' assert function is called if expected for the given input type - and none
    of the other functions are called.
    """

    # test_function_call is the function to check has been called
    # expected_value is the dummy value to use when calling eh.assert_equal_dispatch, so test_function_call will be called
    # pd_testing_function is the specific pd.testing function that should be used to compare that type

    # patch all the potential functions that can be called by test_aide.equality.assert_equal_dispatch
    for x in potential_assert_functions:

        mocker.patch(x)

    actual_value = expected_value
    msg_value = "test_msg"

    eh.assert_equal_dispatch(
        expected=expected_value, actual=actual_value, msg=msg_value
    )

    getter, attribute = _get_target(test_function_call)

    mocked_function_call = getattr(getter(), attribute)

    assert (
        mocked_function_call.call_count == 1
    ), f"Unexpected number of calls to {test_function_call} -\n  Expected:  1\n  Actual:  {mocked_function_call.call_count}"

    call_1_args = mocked_function_call.call_args_list[0]
    call_1_pos_args = call_1_args[0]
    call_1_kwargs = call_1_args[1]

    call_1_expected_pos_arg = (expected_value, actual_value, msg_value)

    assert len(call_1_pos_args) == len(
        call_1_expected_pos_arg
    ), f"Unexpected number of positional args in call to {test_function_call} -\n  Expected: {len(call_1_expected_pos_arg)}\n  Actual:  {len(call_1_pos_args)}"

    pd_testing_function(call_1_expected_pos_arg[0], call_1_pos_args[0])
    pd_testing_function(call_1_expected_pos_arg[1], call_1_pos_args[1])

    e = call_1_expected_pos_arg[2]
    a = call_1_pos_args[2]

    assert (
        e == a
    ), f"Unexpected last positional arg in call to {test_function_call} -\n  Expected: {e}\n  Actual: {a}"

    assert (
        call_1_kwargs == {}
    ), f"Unexpected keyword args in call to {test_function_call} -\n  Expected: None\n  Actual:  {call_1_kwargs}"

    # get functions that should not have been called
    test_functions_not_call = list(
        set(potential_assert_functions) - set([test_function_call])
    )

    # loop through each one and test it has not been called
    for test_function_not_call in test_functions_not_call:

        getter, attribute = _get_target(test_function_not_call)

        mocked_function_not_call = getattr(getter(), attribute)

        assert (
            mocked_function_not_call.call_count == 0
        ), f"Unexpected number of calls to {test_function_not_call} -\n  Expected:  0\n  Actual:  {mocked_function_not_call.call_count}"


@pytest.mark.parametrize(
    "expected_value",
    [
        np.array([]),
        np.array([0, 1, 2]),
        np.array([[1, 2], [3, 4]]),
        np.array([np.nan, np.nan]),
    ],
)
def test_np_array_correct_function_call(mocker, expected_value):
    """Test that assert_array_equal_msg called correctly when expected is a numpy array"""

    # function to check has been called
    test_function_call = "test_aide.equality.assert_array_equal_msg"

    # patch all the potential functions that can be called by test_aide.equality.assert_equal_dispatch
    for x in potential_assert_functions:

        mocker.patch(x)

    actual_value = expected_value
    msg_value = "test_msg"

    eh.assert_equal_dispatch(
        expected=expected_value, actual=actual_value, msg=msg_value
    )

    getter, attribute = _get_target(test_function_call)

    mocked_function_call = getattr(getter(), attribute)

    assert (
        mocked_function_call.call_count == 1
    ), f"Unexpected number of calls to {test_function_call} with {expected_value} -\n  Expected:  1\n  Actual:  {mocked_function_call.call_count}"

    call_1_args = mocked_function_call.call_args_list[0]
    call_1_pos_args = call_1_args[0]
    call_1_kwargs = call_1_args[1]

    call_1_expected_pos_arg = (expected_value, actual_value, msg_value)

    assert len(call_1_pos_args) == len(
        call_1_expected_pos_arg
    ), f"Unexpected number of positional args in call to {test_function_call} -\n  Expected: {len(call_1_expected_pos_arg)}\n  Actual:  {len(call_1_pos_args)}"

    np.testing.assert_array_equal(call_1_expected_pos_arg[0], call_1_pos_args[0])
    np.testing.assert_array_equal(call_1_expected_pos_arg[1], call_1_pos_args[1])

    e = call_1_expected_pos_arg[2]
    a = call_1_pos_args[2]

    assert (
        e == a
    ), f"Unexpected last positional arg in call to {test_function_call} -\n  Expected: {e}\n  Actual: {a}"

    assert (
        call_1_kwargs == {}
    ), f"Unexpected keyword args in call to {test_function_call} -\n  Expected: None\n  Actual:  {call_1_kwargs}"

    # get functions that should not have been called
    test_functions_not_call = list(
        set(potential_assert_functions) - set([test_function_call])
    )

    # loop through each one and test it has not been called
    for test_function_not_call in test_functions_not_call:

        getter, attribute = _get_target(test_function_not_call)

        mocked_function_not_call = getattr(getter(), attribute)

        assert (
            mocked_function_not_call.call_count == 0
        ), f"Unexpected number of calls to {test_function_not_call} -\n  Expected:  0\n  Actual:  {mocked_function_not_call.call_count}"


@pytest.mark.parametrize(
    "expected_function_called, value_to_pass",
    [
        ("test_aide.equality.assert_list_tuple_equal_msg", [1, 2]),
        ("test_aide.equality.assert_list_tuple_equal_msg", (1, 2)),
        ("test_aide.equality.assert_dict_equal_msg", {"a": 1}),
        ("test_aide.equality.assert_dict_equal_msg", defaultdict(None, {"a": 1})),
        ("test_aide.equality.assert_equal_msg", 1),
        ("test_aide.equality.assert_equal_msg", 1.0),
        ("test_aide.equality.assert_equal_msg", "a"),
        ("test_aide.equality.assert_equal_msg", False),
        ("test_aide.equality.assert_equal_msg", None),
        ("test_aide.equality.assert_equal_msg", np.float64(1)),
        ("test_aide.equality.assert_equal_msg", np.int64(1)),
        ("test_aide.equality.assert_np_nan_eqal_msg", np.NaN),
        ("test_aide.equality.assert_np_nan_eqal_msg", np.float64(np.NaN)),
    ],
)
def test_non_dataframe_correct_function_call(
    mocker, expected_function_called, value_to_pass
):
    """Test that the correct 'sub' assert function is called if expected for the given input type - and none
    of the other functions are called.
    """

    # function to check has been called
    test_function_call = expected_function_called

    # patch all the potential functions that can be called by test_aide.equality.assert_equal_dispatch
    for x in potential_assert_functions:

        mocker.patch(x)

    expected_value = value_to_pass
    actual_value = expected_value
    msg_value = "test_msg"

    eh.assert_equal_dispatch(
        expected=expected_value, actual=actual_value, msg=msg_value
    )

    getter, attribute = _get_target(test_function_call)

    mocked_function_call = getattr(getter(), attribute)

    assert (
        mocked_function_call.call_count == 1
    ), f"Unexpected number of calls to {test_function_call} with {value_to_pass} -\n  Expected:  1\n  Actual:  {mocked_function_call.call_count}"

    call_1_args = mocked_function_call.call_args_list[0]
    call_1_pos_args = call_1_args[0]
    call_1_kwargs = call_1_args[1]

    call_1_expected_pos_arg = (expected_value, actual_value, msg_value)

    assert len(call_1_pos_args) == len(
        call_1_expected_pos_arg
    ), f"Unexpected number of positional args in call to {test_function_call} -\n  Expected: {len(call_1_expected_pos_arg)}\n  Actual:  {len(call_1_pos_args)}"

    for i, (e, a) in enumerate(zip(call_1_expected_pos_arg, call_1_pos_args)):

        # logic to handle np.NaNs o/w they will not pass e == a
        if (type(e) is float and np.isnan(e)) or (
            isinstance(e, np.float) and np.isnan(e)
        ):

            assert np.isnan(e) and np.isnan(
                a
            ), f"Unexpected positional arg in index {i} in call to {test_function_call} -\n  Expected: {e}\n  Actual: {a}"

        else:

            assert (
                e == a
            ), f"Unexpected positional arg in index {i} in call to {test_function_call} -\n  Expected: {e}\n  Actual: {a}"

    assert (
        call_1_kwargs == {}
    ), f"Unexpected keyword args in call to {test_function_call} -\n  Expected: None\n  Actual:  {call_1_kwargs}"

    # get functions that should not have been called
    test_functions_not_call = list(
        set(potential_assert_functions) - set([test_function_call])
    )

    # loop through each one and test it has not been called
    for test_function_not_call in test_functions_not_call:

        getter, attribute = _get_target(test_function_not_call)

        mocked_function_not_call = getattr(getter(), attribute)

        assert (
            mocked_function_not_call.call_count == 0
        ), f"Unexpected number of calls to {test_function_not_call} -\n  Expected:  0\n  Actual:  {mocked_function_not_call.call_count}"


def test_other_type_equality_checked():
    """Test if types not directly checked for in assert_equal_dispatch are passed then they are compared using ==."""

    try:

        eh.assert_equal_dispatch(
            expected=set(["a"]), actual=set(["a"]), msg="test message b"
        )

    except Exception as err:

        pytest.fail(
            f"eh.assert_equal_dispatch failed for equal sets call with error; {err}"
        )

    with pytest.raises(AssertionError, match="test message"):

        eh.assert_equal_dispatch(
            expected=set(["a"]), actual=set(["a", "b"]), msg="test message"
        )
