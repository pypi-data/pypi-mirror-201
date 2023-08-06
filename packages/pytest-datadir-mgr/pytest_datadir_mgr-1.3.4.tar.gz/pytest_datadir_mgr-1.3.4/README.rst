=============================
datadir-mgr plugin for pytest
=============================
.. badges-begin

| |pypi| |Python Version| |repo| |downloads| |dlrate|
| |license|  |build| |coverage| |codacy| |issues|

.. |pypi| image:: https://img.shields.io/pypi/v/pytest-datadir-mgr.svg
    :target: https://pypi.python.org/pypi/pytest-datadir-mgr
    :alt: Python package

.. |Python Version| image:: https://img.shields.io/pypi/pyversions/pytest-datadir-mgr
   :target: https://pypi.python.org/pypi/pytest-datadir-mgr
   :alt: Supported Python Versions

.. |repo| image:: https://img.shields.io/github/last-commit/joelb123/pytest-datadir-mgr
    :target: https://github.com/joelb123/pytest-datadir-mgr
    :alt: GitHub repository

.. |downloads| image:: https://pepy.tech/badge/pytest-datadir-mgr
     :target: https://pepy.tech/project/pytest_datadir_mgr
     :alt: Download stats

.. |dlrate| image:: https://img.shields.io/pypi/dm/pytest-datadir-mgr
   :target: https://github.com/joelb123/pytest-datadir-mgr
   :alt: PYPI download rate

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
    :target: https://github.com/joelb123/pytest-datadir-mgr/blob/master/LICENSE.txt
    :alt: License terms

.. |build| image:: https://github.com/joelb123/pytest-datadir-mgr/workflows/tests/badge.svg
    :target:  https://github.com/joelb123/pytest-datadir-mgr.actions
    :alt: GitHub Actions

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/f306c40d604f4e62b8731ada896d8eb2
    :target: https://www.codacy.com/gh/joelb123/pytest-datadir-mgr?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=joelb123/pytest-datadir-mgr&amp;utm_campaign=Badge_Grade
    :alt: Codacy.io grade

.. |coverage| image:: https://codecov.io/gh/joelb123/pytest-datadir-mgr/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/joelb123/pytest-datadir-mgr
    :alt: Codecov.io test coverage

.. |issues| image:: https://img.shields.io/github/issues/joelb123/pytest-datadir-mgr.svg
    :target:  https://github.com/joelb123/pytest-datadir-mgr/issues
    :alt: Issues reported

.. badges-end

.. image:: https://raw.githubusercontent.com/joelb123/pytest-datadir-mgr/main/docs/_static/logo.png
   :target: https://raw.githubusercontent.com/joelb123/pytest-datadir-mgr/main/LICENSE.artwork.txt
   :alt: Logo credit Jørgen Stamp, published under a Creative Commons Attribution 2.5 Denmark License.

The ``datadir-mgr`` plugin for pytest_ provides the ``datadir_mgr`` fixture which
allow test functions to easily download data files and cache generated data files
in data directories in a manner that allows for overlaying of results. ``datadir-mgr``
is pathlib-based, so complete paths to data files are handled,
not just filenames.



This plugin behaves like a limited dictionary, with ``datadir_mgr[item]`` returning a path
with the most specific scope (out of ``global, module, [class], [function]`` that matches
the string or path specified by ``item``.  In addition to serving data files already stored
in the data directory, the fixture provides five methods useful for adding to the test data
stored in the repository:

- The ``download`` method allows downloading data files into data directories, with
  option MD5 checksum checks, un-gzipping, and a progressbar.
- The ``savepath`` fixture lets an arbitrary path relative to the current working
  directory to be saved at a particular scope in the data directories.
- The ``add_scope`` method lets one add directories from scopes different from
  the present request to be added to the search path.  This lets the results
  of previous cached steps to be used in scopes other than global.
- The ``in_tmp_dir`` method creates a context in a temporary directory with
  a list of request file paths copied in.  Optionally, all output file paths
  can be saved at a particular scope at cleanup with an optional exclusion
  filter pattern (e.g., for excluding log files).  Note that files in directories
  that begin with ``test_`` or end with ``_test`` could be confused with
  scope directories and cannnot be saved.  If ``progressbar`` is set to "True",
  then the progress of file copying will be shown, which is helpful in some long-running
  pytest jobs, e.g. on Travis.
- The ``paths_from_scope`` returns a list of all paths to files from a specified scope.


Prerequisites
-------------
Python 3.6 or greater is required.  This package is tested under Linux, MacOS, and Windows
using Python 3.9.

.. _pytest: http://pytest.org/
