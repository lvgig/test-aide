"""
This module contains helper functions that simplify testing functions themselves
e.g. testing a particular function has been called in a particular way.
"""

import inspect
from test_aide.equality import (
    assert_equal_msg,
    assert_list_tuple_equal_msg,
    assert_dict_equal_msg,
)
from contextlib import contextmanager
import pytest_mock


def test_function_arguments(func, expected_arguments, expected_default_values=None):
    """Test that a given function has expected arguments and default values.

    Uses inspect.getfullargspec to get the function argument information. Then loops through
    argument names and default values and uses assert_equal_msg to check actuals are equal to
    expected.

    Parameters
    ----------
    func : method
        Function to check.

    expected_arguments : list
        List of names of expected argument, in order.

    expected_default_values : tuple or None
        A tuple of lenght n of default argument values for the last n positional arguments, or None if
        there are no default values.

    """

    if not type(expected_arguments) is list:

        raise TypeError(
            f"expected_arguments should be a list but got {type(expected_arguments)}"
        )

    if expected_default_values is not None:

        if not type(expected_default_values) is tuple:

            raise TypeError(
                f"expected_default_values should be a tuple but got {type(expected_default_values)}"
            )

    arg_spec = inspect.getfullargspec(func)

    arguments = arg_spec.args

    assert len(expected_arguments) == len(
        arguments
    ), f"Incorrect number of arguments -\n  Expected: {len(expected_arguments)}\n  Actual: {len(arguments)}"

    for i, (e, a) in enumerate(zip(expected_arguments, arguments)):

        assert_equal_msg(a, e, f"Incorrect arg at index {i}")

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

            assert_equal_msg(
                a, e, f"Incorrect default value at index {i} of default values"
            )


@contextmanager
def assert_function_call_count(mocker, target, attribute, expected_n_calls, **kwargs):
    """Assert a function has been called a given number of times. This should be used
    as a context manager, see example below.

    Parameters
    ----------
    mocker : pytest_mock.plugin.MockerFixture
        The mocker fixture from the pytest_mock package.

    target : object
        Object with function to test is called.

    attribute : str
        Name of the method to mock on the target object

    expected_n_calls : int
        Expected number of calls to target.attribute.

    **kwargs : any
        Arbitrary keyword arguments passed on to mocker.patch.object.

    Examples
    --------
    >>> import test_aide as ta
    >>> import random
    >>>
    >>> def test_number_calls_to_function(mocker):
    ...     with ta.functions.assert_function_call_count(mocker, random, "choice", 3):
    ...         random.choice([1, 2, 3])
    ...         random.choice([4, 5, 6])
    ...         random.choice([7, 8, 9])

    """

    if type(mocker) is not pytest_mock.plugin.MockerFixture:

        raise TypeError("mocker should be the pytest_mock mocker fixture")

    mocked_method = mocker.patch.object(target, attribute, **kwargs)

    try:

        yield mocked_method

    finally:

        assert (
            mocked_method.call_count == expected_n_calls
        ), f"incorrect number of calls to {attribute}, expected {expected_n_calls} but got {mocked_method.call_count}"


@contextmanager
def assert_function_call(mocker, target, attribute, expected_calls_args, **kwargs):
    """Assert a function has been called with given arguments. This should be used
    as a context manager, see example below.

    This can be used to check multiple calls to the same function. Both the positional
    and keyword arguments must be specified for any calls to check.

    Parameters
    ----------
    mocker : pytest_mock.plugin.MockerFixture
        The mocker fixture from the pytest_mock package.

    target : object
        Object with function to test is called.

    attribute : str
        Name of the method to mock on the target object

    expected_calls_args : dict
        Expected positional and keyword arguments to specific calls to target.attribute. Keys
        of expected_calls_args must be ints (indexed from 0) indicating the call # of
        interest. The value for each key should be a dict with keys 'args' and 'kwargs'.
        The values for the keys in these sub dicts should be a tuple of expected positional
        arguments and a dict of expected keyword arguments for the given call to target.attribute.
        For example if expected_calls_args = {0: {'args':('a','b'), 'kwargs':{'c': 1}}} this
        indicates that the first call to target.attribute is expected to be called with positional
        args ('a','b') and keyword args {'c': 1}. See the example section below for more examples.

    **kwargs : any
        Arbitrary keyword arguments passed on to mocker.patch.object.

    Examples
    --------
    >>> import test_aide as ta
    >>> import random
    >>>
    >>> def test_number_calls_to_function(mocker):
    ...     expected_call_arguments = {
    ...         0: {
    ...             'args': (
    ...                 [1, 2, 3],
    ...             ),
    ...             'kwargs': {
    ...                 'weights': None
    ...             }
    ...         },
    ...         2: {
    ...             'args': (
    ...                 [1, 2, 3],
    ...             ),
    ...             'kwargs': {}
    ...         },
    ...         3: {
    ...             'args': (),
    ...             'kwargs': {
    ...                 'populaton': [1, 2, 3],
    ...                 'k': 2
    ...              }
    ...         }
    ...     }
    ...     with h.assert_function_call(mocker, random, "choices", expected_call_arguments, return_value=None):
    ...         random.choices([1, 2, 3], weights=None)
    ...         random.choices([1, 2, 3])
    ...         random.choices([1, 2, 3])
    ...         random.choices(population=[1, 2, 3], k=2)
    >>>

    """

    if type(mocker) is not pytest_mock.plugin.MockerFixture:
        raise TypeError("mocker should be the pytest_mock mocker fixture")

    if not type(expected_calls_args) is dict:
        raise TypeError("expected_calls_args should be a dict")

    for call_number, call_n_expected_arguments in expected_calls_args.items():

        if not type(call_number) is int:
            raise TypeError("expected_calls_args keys should be integers")

        if call_number < 0:
            raise ValueError(
                "expected_calls_args keys should be integers greater than or equal to 0"
            )

        if not type(call_n_expected_arguments) is dict:
            raise TypeError("each value in expected_calls_args should be a dict")

        if not sorted(list(call_n_expected_arguments.keys())) == ["args", "kwargs"]:
            raise ValueError(
                """keys of each sub dict in expected_calls_args should be 'args' and 'kwargs' only"""
            )

        if not type(call_n_expected_arguments["args"]) is tuple:
            raise TypeError("args in expected_calls_args should be tuples")

        if not type(call_n_expected_arguments["kwargs"]) is dict:
            raise TypeError("kwargs in expected_calls_args should be dicts")

    max_expected_call = max(expected_calls_args.keys())

    mocked_method = mocker.patch.object(target, attribute, **kwargs)

    try:

        yield mocked_method

    finally:

        assert mocked_method.call_count >= (
            max_expected_call + 1
        ), f"not enough calls to {attribute}, expected at least {max_expected_call+1} but got {mocked_method.call_count}"

        for call_number, call_n_expected_arguments in expected_calls_args.items():

            call_n_arguments = mocked_method.call_args_list[call_number]
            call_n_pos_args = call_n_arguments[0]
            call_n_kwargs = call_n_arguments[1]

            expected_call_n_pos_args = call_n_expected_arguments["args"]
            expected_call_n_kwargs = call_n_expected_arguments["kwargs"]

            assert_list_tuple_equal_msg(
                actual=call_n_pos_args,
                expected=expected_call_n_pos_args,
                msg_tag=f"positional args for call {call_number} not correct",
            )

            assert_dict_equal_msg(
                actual=call_n_kwargs,
                expected=expected_call_n_kwargs,
                msg_tag=f"kwargs for call {call_number} not correct",
            )
