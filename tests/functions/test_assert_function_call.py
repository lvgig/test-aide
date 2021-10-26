import pytest
import test_aide
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
    """Test test_aide.functions.assert_function_call has expected arguments."""

    # use of contextmanager decorator means we need to use .__wrapped__ to get back to original function
    fh.test_function_arguments(
        func=fh.assert_function_call.__wrapped__,
        expected_arguments=["mocker", "target", "attribute", "expected_calls_args"],
        expected_default_values=None,
    )


def test_mocker_arg_not_mocker_fixture_error():
    """Test an exception is raised if mocker is not pytest_mock.plugin.MockerFixture type."""

    with pytest.raises(
        TypeError, match="mocker should be the pytest_mock mocker fixture"
    ):

        x = DummyClass()

        with fh.assert_function_call(
            "aaaaaa", DummyClass, "dummy_function_b", {0: {"args": (), "kwargs": {}}}
        ):

            x.dummy_function_a()


def test_expected_calls_args_checks(mocker):
    """Test that the checks on the expected_calls_args parameter raise exceptions."""

    with pytest.raises(TypeError, match="expected_calls_args should be a dict"):

        with fh.assert_function_call(mocker, DummyClass, "dummy_function_b", ()):

            DummyClass()

    with pytest.raises(TypeError, match="expected_calls_args keys should be integers"):

        with fh.assert_function_call(
            mocker,
            DummyClass,
            "dummy_function_b",
            {"a": {"args": (), "kwargs": {"columns": "a"}}},
        ):

            DummyClass()

    with pytest.raises(
        ValueError,
        match="expected_calls_args keys should be integers greater than or equal to 0",
    ):

        with fh.assert_function_call(
            mocker,
            DummyClass,
            "dummy_function_b",
            {-1: {"args": (), "kwargs": {"columns": "a"}}},
        ):

            DummyClass()

    with pytest.raises(
        TypeError, match="each value in expected_calls_args should be a dict"
    ):

        with fh.assert_function_call(
            mocker, DummyClass, "dummy_function_b", {0: ((), {"columns": "a"})}
        ):

            DummyClass()

    with pytest.raises(
        ValueError,
        match="""keys of each sub dict in expected_calls_args should be 'args' and 'kwargs' only""",
    ):

        with fh.assert_function_call(
            mocker,
            DummyClass,
            "dummy_function_b",
            {0: {"argz": (), "kwargs": {"columns": "a"}}},
        ):

            DummyClass()

    with pytest.raises(TypeError, match="args in expected_calls_args should be tuples"):

        with fh.assert_function_call(
            mocker,
            DummyClass,
            "dummy_function_b",
            {0: {"args": {}, "kwargs": {"columns": "a"}}},
        ):

            DummyClass()

    with pytest.raises(
        TypeError, match="kwargs in expected_calls_args should be dicts"
    ):

        with fh.assert_function_call(
            mocker, DummyClass, "dummy_function_b", {0: {"args": (), "kwargs": ["a"]}}
        ):

            DummyClass()


def test_mocker_patch_object_call(mocker):
    """Test the mocker.patch.object call."""

    mocked = mocker.spy(mocker.patch, "object")

    expected_call_arguments = {0: {"args": ("a",), "kwargs": {"other": 1}}}

    x = DummyClass()

    with fh.assert_function_call(
        mocker,
        DummyClass,
        "dummy_function_b",
        expected_call_arguments,
        return_value=None,
    ):

        x.dummy_function_a("a", other=1)

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


def test_successful_function_call(mocker):
    """Test a successful function call with the correct arguments specified."""

    expected_call_arguments = {
        0: {"args": ("a",), "kwargs": {"other": 1}},
        2: {"args": (["a", "b"],), "kwargs": {}},
        3: {"args": (), "kwargs": {"columns": ["a", "b"]}},
    }

    x = DummyClass()

    with fh.assert_function_call(
        mocker,
        DummyClass,
        "dummy_function_b",
        expected_call_arguments,
        return_value=None,
    ):

        x.dummy_function_a("a", other=1)
        x.dummy_function_a(1, columns=["a"])
        x.dummy_function_a(["a", "b"])
        x.dummy_function_a(columns=["a", "b"])


def test_not_enough_function_calls_exception(mocker):
    """Test an exception is raised if the mocked function is not called enough time for the number of expected_call_arguments items."""

    expected_call_arguments = {
        2: {"args": (["a", "b"],), "kwargs": {}},
        5: {"args": (), "kwargs": {"columns": ["a", "b"]}},
    }

    x = DummyClass()

    with pytest.raises(
        AssertionError,
        match="not enough calls to dummy_function_b, expected at least 6 but got 4",
    ):

        with fh.assert_function_call(
            mocker,
            DummyClass,
            "dummy_function_b",
            expected_call_arguments,
            return_value=None,
        ):

            x.dummy_function_a("a", other=1)
            x.dummy_function_a(1, columns=["a"])
            x.dummy_function_a(["a", "b"])
            x.dummy_function_a(columns=["a", "b"])


@pytest.mark.parametrize(
    "expected_args",
    [
        {
            1: {"args": (1,), "kwargs": {}},
            3: {"args": (), "kwargs": {"columns": ["a", "b"]}},
        },
        {
            1: {"args": (), "kwargs": {"columns": ["a"]}},
            3: {"args": (), "kwargs": {"columns": ["a", "b"]}},
        },
        {
            1: {"args": (), "kwargs": {}},
            3: {"args": (1,), "kwargs": {"columns": ["a", "b"]}},
        },
        {
            1: {"args": (), "kwargs": {}},
            3: {"args": (1,), "kwargs": {"columns": ["a"]}},
        },
        {2: {"args": (), "kwargs": {}}},
        {0: {"args": ("a",), "kwargs": {"other": 2}}},
    ],
)
def test_incorrect_call_args_exception(mocker, expected_args):
    """Test an exception is raised if the mocked function is not called with expected arguments."""

    x = DummyClass()

    with pytest.raises(AssertionError):

        with fh.assert_function_call(
            mocker, DummyClass, "dummy_function_b", expected_args, return_value=None
        ):

            x.dummy_function_a("a", other=1)
            x.dummy_function_a()
            x.dummy_function_a(["a", "b"])
            x.dummy_function_a(columns=["a", "b"])


def test_assert_dict_equal_msg_call(mocker):
    """Test the calls to assert_dict_equal_msg."""

    # this is patched so it will not cause errors below when expected_args do not match
    mocked_dict_assert = mocker.patch.object(
        test_aide.functions, "assert_dict_equal_msg"
    )

    expected_args = {
        0: {"args": ("a",), "kwargs": {"other": 1}},
        1: {"args": (), "kwargs": {}},
        2: {"args": (["a", "b"],), "kwargs": {}},
        3: {"args": (), "kwargs": {"columns": ["a", "c"]}},
    }

    x = DummyClass()

    with fh.assert_function_call(
        mocker, DummyClass, "dummy_function_b", expected_args, return_value=None
    ):

        x.dummy_function_a("a", other=1)
        x.dummy_function_a()
        x.dummy_function_a(["a", "b"])
        x.dummy_function_a(columns=["a", "b"])

    assert (
        mocked_dict_assert.call_count == 4
    ), "unexpected number of calls to test_aide.functions.assert_dict_equal_msg"

    call_n_args = mocked_dict_assert.call_args_list[0]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert call_n_pos_args == (), "unexpected pos args in assert_dict_equal_msg call 1"

    assert call_n_kwargs == {
        "actual": {"other": 1},
        "expected": {"other": 1},
        "msg_tag": "kwargs for call 0 not correct",
    }, "unexpected kwargs in assert_dict_equal_msg call 1"

    call_n_args = mocked_dict_assert.call_args_list[1]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert call_n_pos_args == (), "unexpected pos args in assert_dict_equal_msg call 2"

    assert call_n_kwargs == {
        "actual": {},
        "expected": {},
        "msg_tag": "kwargs for call 1 not correct",
    }, "unexpected kwargs in assert_dict_equal_msg call 2"

    call_n_args = mocked_dict_assert.call_args_list[2]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert call_n_pos_args == (), "unexpected pos args in assert_dict_equal_msg call 3"

    assert call_n_kwargs == {
        "actual": {},
        "expected": {},
        "msg_tag": "kwargs for call 2 not correct",
    }, "unexpected kwargs in assert_dict_equal_msg call 3"

    call_n_args = mocked_dict_assert.call_args_list[3]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert call_n_pos_args == (), "unexpected pos args in assert_dict_equal_msg call 4"

    assert call_n_kwargs == {
        "actual": {"columns": ["a", "b"]},
        "expected": expected_args[3]["kwargs"],
        "msg_tag": "kwargs for call 3 not correct",
    }, "unexpected kwargs in assert_dict_equal_msg call 4"


def test_assert_list_tuple_equal_msg_call(mocker):
    """Test the calls to assert_list_tuple_equal_msg."""

    # this is patched so it will not cause errors below when expected_args do not match
    mocked_dict_assert = mocker.patch.object(
        test_aide.functions, "assert_list_tuple_equal_msg"
    )

    expected_args = {
        0: {"args": ("a",), "kwargs": {"other": 1}},
        1: {"args": (), "kwargs": {}},
        2: {"args": (["a", "c"],), "kwargs": {}},
        3: {"args": (), "kwargs": {"columns": "a"}},
    }

    x = DummyClass()

    with fh.assert_function_call(
        mocker, DummyClass, "dummy_function_b", expected_args, return_value=None
    ):

        x.dummy_function_a("a", other=1)
        x.dummy_function_a()
        x.dummy_function_a(["a", "b"])
        x.dummy_function_a(columns="a")

    assert (
        mocked_dict_assert.call_count == 4
    ), "unexpected number of calls to test_aide.functions.assert_list_tuple_equal_msg"

    call_n_args = mocked_dict_assert.call_args_list[0]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert (
        call_n_pos_args == ()
    ), "unexpected pos args in assert_list_tuple_equal_msg call 1"

    assert call_n_kwargs == {
        "actual": ("a",),
        "expected": ("a",),
        "msg_tag": "positional args for call 0 not correct",
    }, "unexpected pos args in assert_list_tuple_equal_msg call 1"

    call_n_args = mocked_dict_assert.call_args_list[1]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert (
        call_n_pos_args == ()
    ), "unexpected pos args in assert_list_tuple_equal_msg call 2"

    assert call_n_kwargs == {
        "actual": (),
        "expected": (),
        "msg_tag": "positional args for call 1 not correct",
    }, "unexpected pos args in assert_list_tuple_equal_msg call 2"

    call_n_args = mocked_dict_assert.call_args_list[2]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert (
        call_n_pos_args == ()
    ), "unexpected pos args in assert_list_tuple_equal_msg call 3"

    assert call_n_kwargs == {
        "actual": (["a", "b"],),
        "expected": expected_args[2]["args"],
        "msg_tag": "positional args for call 2 not correct",
    }, "unexpected pos args in assert_list_tuple_equal_msg call 3"

    call_n_args = mocked_dict_assert.call_args_list[3]
    call_n_pos_args = call_n_args[0]
    call_n_kwargs = call_n_args[1]

    assert (
        call_n_pos_args == ()
    ), "unexpected pos args in assert_list_tuple_equal_msg call 4"

    assert call_n_kwargs == {
        "actual": (),
        "expected": (),
        "msg_tag": "positional args for call 3 not correct",
    }, "unexpected pos args in assert_list_tuple_equal_msg call 4"
