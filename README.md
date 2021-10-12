# test-aide

----

`test-aide` includes helper functions to simplify unit tests.


## Installation

test-aide can be installed from PyPI simply with;

 `pip install test-aide`

## Documentation

To build local documentation, specify the environment variable $SPHINX_BUILD_DIR$, and then
run from the `docs/` directory

```shell
make apidoc
make html
```

## Examples

To help get started there are example notebooks in the [examples](https://github.com/lvgig/test-aide/tree/master/examples) folder that show how to use each transformer as well as an example of putting several together in a Pipeline.

## Build and test

The test framework we are using for this project is [pytest](https://docs.pytest.org/en/stable/), to run the tests follow the steps below.

First clone the repo and move to the root directory;

```shell
git clone https://github.com/lvgig/test-aide.git
cd test-aide
```

Then install test-aide in editable mode;

```shell
pip install -e . -r requirements-dev.txt
```

Then run the tests simply with pytest

```shell
pytest
```

## Contribute

`test-aide` is under active development, we're super excited if you're interested in contributing! See the `CONTRIBUTING.md` for the full details of our working practices.

For bugs and feature requests please open an [issue](https://github.com/lvgig/test-aide/issues).
