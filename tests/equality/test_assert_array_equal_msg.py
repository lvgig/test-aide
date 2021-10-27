import inspect
import pytest

import test_aide.equality as eh

try:

    import numpy as np
    import numpy

    has_numpy = True

except ModuleNotFoundError:

    has_numpy = False


def test_arguments():
    """Test arguments for arguments of function."""

    expected_arguments = ["actual", "expected", "msg_tag", "print_actual_and_expected"]

    expected_default_values = (False,)

    expected_var_keyword_arg = "kwargs"

    arg_spec = inspect.getfullargspec(eh.assert_array_equal_msg)

    arguments = arg_spec.args

    assert len(expected_arguments) == len(
        arguments
    ), f"Incorrect number of arguments -\n  Expected: {len(expected_arguments)}\n  Actual: {len(arguments)}"

    for i, (e, a) in enumerate(zip(expected_arguments, arguments)):
        assert e == a, f"Incorrect arg at index {i} -\n  Expected: {e}\n  Actual: {a}"

    default_values = arg_spec.defaults

    if default_values is None:

        if expected_default_values is not None:
            raise AssertionError(
                f"Incorrect default values -\n  Expected: {expected_default_values}\n  Actual: No default values"
            )

    else:

        if expected_default_values is None:
            raise AssertionError(
                f"Incorrect default values -\n  Expected: No default values\n  Actual: {default_values}"
            )

    if (default_values is not None) and (expected_default_values is not None):

        assert len(expected_default_values) == len(
            default_values
        ), f"Incorrect number of default values -\n  Expected: {len(expected_default_values)}\n  Actual: {len(default_values)}"

        for i, (e, a) in enumerate(zip(expected_default_values, default_values)):
            assert (
                e == a
            ), f"Incorrect default value at index {i} of default values -\n  Expected: {e}\n  Actual: {a}"

    var_keyword_arg = arg_spec.varkw

    assert (
        var_keyword_arg == expected_var_keyword_arg
    ), f"Unexpected keyword arg variable in assert_array_equal_msg -\n  Expected: {expected_var_keyword_arg}\n  Actual: {var_keyword_arg}"


@pytest.mark.skipif(not has_numpy, reason="numpy not installed")
def test_expected_not_array_error():
    """'Test that a TypeError is raised if expected is not a numpy array."""

    with pytest.raises(
        TypeError, match=f"expected should be of type numpy ndarray, but got {type(1)}"
    ):

        eh.assert_array_equal_msg(expected=1, actual=np.array([]), msg_tag="test_msg")


@pytest.mark.skipif(not has_numpy, reason="numpy not installed")
def test_actual_not_array_error():
    """'Test that a TypeError is raised if actual is not a numpy array."""

    with pytest.raises(
        TypeError, match=f"actual should be of type numpy ndarray, but got {type(1)}"
    ):

        eh.assert_array_equal_msg(expected=np.array([]), actual=1, msg_tag="test_msg")


@pytest.mark.skipif(not has_numpy, reason="numpy not installed")
def test_numpy_assert_array_called(mocker):
    """Test the call to pandas.testing.assert_series_equal."""

    srs = np.array([1, 2, 3])
    srs2 = np.array([1, 2, 3])

    spy = mocker.spy(numpy.testing, "assert_array_equal")

    eh.assert_array_equal_msg(expected=srs, actual=srs2, msg_tag="a", verbose=True)

    assert (
        spy.call_count == 1
    ), f"Unexpected number of call to np.testing.assert_array_equal_msg -\n  Expected: 1\n  Actual: {spy.call_count}"

    call_1_args = spy.call_args_list[0]
    call_1_pos_args = call_1_args[0]
    call_1_kwargs = call_1_args[1]

    call_1_expected_kwargs = {"verbose": True}
    call_1_expected_pos_args = (srs, srs2)

    assert len(call_1_expected_kwargs.keys()) == len(
        call_1_kwargs.keys()
    ), f"Unexpected number of kwargs -\n  Expected: {len(call_1_expected_kwargs.keys())}\n  Actual: {len(call_1_kwargs.keys())}"

    assert (
        call_1_expected_kwargs["verbose"] == call_1_kwargs["verbose"]
    ), f"""check_dtype kwarg unexpected -\n  Expected {call_1_expected_kwargs['verbose']}\n  Actual: {call_1_kwargs['verbose']}"""

    assert len(call_1_expected_pos_args) == len(
        call_1_pos_args
    ), f"Unexpected number of kwargs -\n  Expected: {len(call_1_expected_pos_args)}\n  Actual: {len(call_1_pos_args)}"

    np.testing.assert_array_equal(call_1_expected_pos_args[0], call_1_pos_args[0])
    np.testing.assert_array_equal(call_1_expected_pos_args[1], call_1_pos_args[1])


@pytest.mark.skipif(not has_numpy, reason="numpy not installed")
def test_exception_no_print():
    """Test an assert error is raised (with correct info) in case of exception coming from assert_array_equal and
    print_actual_and_expected is False.
    """

    srs = np.array([1, 2, 3])
    srs2 = np.array([1, 2, 4])

    with pytest.raises(AssertionError, match="a"):
        eh.assert_array_equal_msg(
            expected=srs, actual=srs2, msg_tag="a", print_actual_and_expected=False
        )


@pytest.mark.skipif(not has_numpy, reason="numpy not installed")
def test_exception_print():
    """Test an assert error is raised (with correct info) in case of exception coming from assert_series_equal and
    print_actual_and_expected is True.
    """

    srs = np.array([1, 2, 3])
    srs2 = np.array([1, 2, 4])

    with pytest.raises(AssertionError) as exc_info:
        eh.assert_array_equal_msg(
            expected=srs, actual=srs2, msg_tag="a", print_actual_and_expected=True
        )

    assert exc_info.value.args[0] == "a\n" + f"expected:\n{srs}\n" + f"actual:\n{srs2}"
