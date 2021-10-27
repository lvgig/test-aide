"""
This module contains helper functions that deal with classes and the methods and
attributes of objects.
"""

import inspect
from test_aide.equality import assert_equal_dispatch


def check_is_class(class_to_check):
    """Raises type error if class_to_check is not a class.

    Uses inspect.isclass.

    Parameters
    ----------
    class_to_check : object
        The object to be inspected.

    """

    if inspect.isclass(class_to_check) is False:

        raise TypeError(f"{class_to_check} is not a valid class")


def assert_inheritance(obj, cls):
    """Asserts whether an object inherits from a particular class.

    Uses isinstance.

    Parameters
    ----------
    obj : object
        The object to test.

    cls : Class
        Class to check obj is an instance of.

    """

    check_is_class(cls)

    assert isinstance(
        obj, cls
    ), f"Incorrect inheritance - passed obj of class {obj.__class__.__name__} is not an instance of {cls}"


def test_object_method(obj, expected_method, msg):
    """Test that a particular object has a given method and the (method) attribute is callable.

    Uses hasattr to check the method attribute exists, then callable(getattr()) to check the method
    is callable.

    Parameters
    ----------
    obj : object
        The object to test.

    expected_method : str
        Name of expected method on obj.

    """

    if not type(expected_method) is str:

        raise TypeError(
            f"expected_method should be a str but got {type(expected_method)}"
        )

    assert hasattr(
        obj, expected_method
    ), f"obj does not have attribute {expected_method}"

    assert callable(
        getattr(obj, expected_method)
    ), f"{expected_method} on obj is not callable"


def test_object_attributes(obj, expected_attributes, msg):
    """Check a particular object has given attributes.

    Function loops through key, value pairs in expected_attributes dict and checks
    there is an attribute with the name of each key is on obj then calls assert_equal_dispatch
    to check the expected value and actual value are equal.

    Parameters
    ----------
    obj : object
        Object to test attributes of.

    expected_attributes : dict
        Dict of expected attributes and their values.

    msg : str
        Message tag passed onto assert_equal_dispatch.

    """

    if not type(expected_attributes) is dict:

        raise TypeError(
            f"expected_attributes should be a dict but got {type(expected_attributes)}"
        )

    for attribute_name, expected in expected_attributes.items():

        assert hasattr(obj, attribute_name), f"obj has not attribute {attribute_name}"

        actual = getattr(obj, attribute_name)

        assert_equal_dispatch(
            expected=expected, actual=actual, msg=f"{attribute_name} {msg}"
        )
