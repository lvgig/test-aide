import pytest
import test_aide.functions as fh


class DummyClass:
    """Dummy class to be used in tests in this script, with it's methods being mocked."""

    def dummy_function_a(self, *args, **kwargs):
        """Function that only calls dummy_function_b."""

        self.dummy_function_b(*args, **kwargs)

    def dummy_function_b(self, *args, **kwargs):
        """Function that does nothing, is called by dummy_function_a."""

        pass


def test_arguments():
    """Test test_aide.functions.assert_function_call_count has expected arguments."""

    # use of contextmanager decorator means we need to use .__wrapped__ to get back to original function
    fh.test_function_arguments(
        func=fh.assert_function_call_count.__wrapped__,
        expected_arguments=["mocker", "target", "attribute", "expected_n_calls"],
        expected_default_values=None,
    )


def test_mocker_arg_not_mocker_fixture_error():
    """Test an exception is raised if mocker is not pytest_mock.plugin.MockerFixture type."""

    with pytest.raises(
        TypeError, match="mocker should be the pytest_mock mocker fixture"
    ):

        x = DummyClass()

        with fh.assert_function_call_count("aaaaaa", DummyClass, "dummy_function_b", 1):

            x.dummy_function_a()


def test_mocker_patch_object_call(mocker):
    """Test the mocker.patch.object call."""

    mocked = mocker.spy(mocker.patch, "object")

    x = DummyClass()

    with fh.assert_function_call_count(
        mocker, DummyClass, "dummy_function_b", 1, return_value=None
    ):

        x.dummy_function_a()

    assert mocked.call_count == 1, "unexpected number of calls to mocker.patch.object"

    mocker_patch_object_call = mocked.call_args_list[0]
    call_pos_args = mocker_patch_object_call[0]
    call_kwargs = mocker_patch_object_call[1]

    assert call_pos_args == (
        DummyClass,
        "dummy_function_b",
    ), "unexpected positional args in mocker.patch.object call"

    assert call_kwargs == {
        "return_value": None
    }, "unexpected kwargs in mocker.patch.object call"


def test_successful_usage(mocker):
    """Test an example of successful run of fh.assert_function_call_count."""

    x = DummyClass()

    with fh.assert_function_call_count(mocker, DummyClass, "dummy_function_b", 1):

        x.dummy_function_a()


def test_exception_raised_more_calls_expected(mocker):
    """Test an exception is raised in the case more calls to a function are expected than happen."""

    with pytest.raises(
        AssertionError,
        match="incorrect number of calls to dummy_function_b, expected 2 but got 1",
    ):

        x = DummyClass()

        with fh.assert_function_call_count(mocker, DummyClass, "dummy_function_b", 2):

            x.dummy_function_a()


def test_exception_raised_more_calls_expected2(mocker):
    """Test an exception is raised in the case more calls to a function are expected than happen."""

    with pytest.raises(
        AssertionError,
        match="incorrect number of calls to dummy_function_b, expected 4 but got 0",
    ):

        with fh.assert_function_call_count(mocker, DummyClass, "dummy_function_b", 4):

            DummyClass()


def test_exception_raised_less_calls_expected(mocker):
    """Test an exception is raised in the case less calls to a function are expected than happen."""

    with pytest.raises(
        AssertionError,
        match="incorrect number of calls to dummy_function_b, expected 1 but got 2",
    ):

        x = DummyClass()

        with fh.assert_function_call_count(mocker, DummyClass, "dummy_function_b", 1):

            x.dummy_function_a()
            x.dummy_function_a()


def test_exception_raised_less_calls_expected2(mocker):
    """Test an exception is raised in the case less calls to a function are expected than happen."""

    with pytest.raises(
        AssertionError,
        match="incorrect number of calls to dummy_function_b, expected 0 but got 1",
    ):

        x = DummyClass()

        with fh.assert_function_call_count(mocker, DummyClass, "dummy_function_b", 0):

            x.dummy_function_a()
