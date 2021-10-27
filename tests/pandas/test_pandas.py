import pytest
import test_aide

try:

    import pandas as pd  # noqa

    has_pandas = True

except ModuleNotFoundError:

    has_pandas = False


@pytest.mark.skipif(has_pandas, reason="pandas installed")
def test_no_pandas_module_if_not_installed():
    """Test that test_aide has not pandas module if the library is not installed."""

    assert "pandas" not in dir(
        test_aide
    ), "pandas module is available in test_aide when pandas is not installed"
