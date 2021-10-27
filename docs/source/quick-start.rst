Quick Start
====================

Welcome to the quick start guide for ``test-aide``!

Installation
--------------------

The easiest way to get ``test-aide`` is to install directly from ``pip``;

   .. code::

     pip install test-aide

Summary
--------------------

The ``test-aide`` package contains four modules to assist with pretty specific areas of testing. The functionality was originally part of the `tubular <https://github.com/lvgig/tubular>`_ library so a lot of the package assists with testing in the context of a data science workflow and with using `pandas <https://pandas.pydata.org/>`_ or `numpy <https://numpy.org/>`_.

We have found ourselves using these helpers across multiple projects and hence decided to create a standalone package.

The different modules are described below.

Class helpers
--------------------

The ``classes`` module contains simple helpers to assist with testing classes and objects. 

There are functions to test an object is a class, an object inherits from a particular class and an object has a particular method or attributes.

Equality helpers
--------------------

The ``equality`` module contains helpers to assist with asserting equality when working with ``pandas`` or ``numpy`` data structures e.g. `pandas.DataFrame <https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html>`_. 

For example if you have a dict containing differnt but equal ``pd.DataFrame`` objects you can no longer use the simple ``assert`` statement to check the dicts are equal. The helpers in the ``equality`` module make it easier to assert equality in situations like this.

The following ``pandas`` or ``numpy`` data types are supported for easier comparison;

- pd.DataFrame
- pd.Series
- pd.Index
- np.float
- np.NaN
- np.ndarray

As well as wrappers for asserting equality for the following data structures, in case they contain any of the above types;

- list
- tuple
- dict

There is also an ``assert_equal_dispatch`` wrapper function to automatically call the correct assertion function from the module given the input types.

Functions helpers
--------------------

The ``functions`` module contains helpers to assist with testing functions.

There is a simple function to test the arguments of a function as well as helpers when testing a function has been called in a specific way or specific number of times when mocking.

Pandas helpers
--------------------

The ``pandas`` module contains helpers that create pytest params subsets of input ``pd.DataFrame`` objects, in order to repeat tests more easily on subsets and transformations of the passed data.

You can see examples of their usage in the `tubular tests <https://github.com/lvgig/tubular/tree/master/tests>`_ for the ``transform`` method for pretty much any transformer in the package. The helpers are called within the `pytest.mark.parametrize` decorator to generate the pytest params that will define the different tests - running on different subsets of the data.
