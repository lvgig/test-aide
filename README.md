# test-aide

----

`test-aide` is a lightweight package containing helper functions to simplify certain aspects of unit testing. See the [documentation](https://test-aide.readthedocs.io/en/latest/) for the full list of features.

The `equality` module contains helpers that simplfy asserting equality when working with `pandas` or `numpy` types, in particular when working with these types nested in other data structures e.g. a dict containing ``pandas.DataFrame`` object(s).

The `functions` module contains helpers that simplfy asserting that a function was called in a particular way. The functions `assert_function_call` and `assert_function_call_count` are available to be used as context managers to test a function is called in a certain way and called a specific number of times respectively.

## Installation

`test-aide` can be installed from PyPI simply with;

 `pip install test-aide`

## Documentation

Documentation for the package can be found on [readthedocs](https://test-aide.readthedocs.io/en/latest/).

To build the html documentation locally, from the `docs` directory run the following;

```shell
make html
```

## Build and test

The test framework we are using for this project is [pytest](https://docs.pytest.org/en/stable/), to run the tests follow the steps below.

First clone the repo and move to the root directory;

```shell
git clone https://github.com/lvgig/test-aide.git
cd test-aide
```

Then install `test-aide` in editable mode;

```shell
pip install -e . -r requirements-dev.txt
```

Then run the tests simply with `pytest`;

```shell
pytest
```

## Contribute

`test-aide` is under active development, we're super excited if you're interested in contributing! 

See the [CONTRIBUTING](https://github.com/lvgig/test-aide/blob/master/CONTRIBUTING.md) file for the full details of our working practices.

For bugs and feature requests please open an [issue](https://github.com/lvgig/test-aide/issues).
