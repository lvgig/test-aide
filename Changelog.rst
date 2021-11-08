Changelog
=========

This changelog follows the great advice from https://keepachangelog.com/.

Each section will have a title of the format ``X.Y.Z (YYYY-MM-DD)`` giving the version of the package and the date of release of that version. Unreleased changes i.e. those that have been merged into `main` (e.g. with a .dev suffix) but which are not yet in a new release (on PyPI) are added to the changelog but with the title ``X.Y.Z (unreleased)``. Unreleased sections can be combined when they are released and the date of release added to the title.

Subsections for each version can be one of the following;

- ``Added`` for new features.
- ``Changed`` for changes in existing functionality.
- ``Deprecated`` for soon-to-be removed features.
- ``Removed`` for now removed features.
- ``Fixed`` for any bug fixes.
- ``Security`` in case of vulnerabilities.

Each individual change should have a link to the pull request after the description of the change.

0.1.1 (2021-11-08)
------------------

Removed
^^^^^^^

- Remove ``np.float`` from ``equality`` module after it has been deprecated in `numpy 1.20 <https://numpy.org/doc/stable/release/1.20.0-notes.html#deprecations>`_ `#8 <https://github.com/lvgig/test-aide/pull/8>`_

0.1.0 (2021-10-27)
------------------

Added
^^^^^

- Initial version of the code for open source release after separating from `tubular <https://github.com/lvgig/tubular>`_
- Set up documentation for  `readthedocs <https://test-aide.readthedocs.io/en/latest/index.html>`_
