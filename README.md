# sage-numerical-backends-gurobi: Gurobi mixed integer linear programming backend for SageMath

[![PyPI](https://img.shields.io/pypi/v/sage-numerical-backends-gurobi)](https://pypi.org/project/sage-numerical-backends-gurobi/ "PyPI: sage-numerical-backends-gurobi")

`GurobiBackend` has previously been available as part of the [SageMath](http://www.sagemath.org/) source tree,
from which it is built as an "optional extension" if the proprietary Gurobi library and header files have been symlinked into `$SAGE_LOCAL` manually.

Because of the proprietary nature of the Gurobi software, `GurobiBackend` is not available in any binary distributions of SageMath.

The present standalone Python package `sage-numerical-backends-gurobi` has been created from the SageMath sources, version 9.0.beta10; the in-tree version of `GurobiBackend` has been removed in [Sage ticket #28175](https://trac.sagemath.org/ticket/28175).  SageMath 9.1 and later makes the package available as an optional Sage package (SPKG).

The current version of this package can also be installed on top of various Sage installations using pip.
(Your installation of Sage must be based on Python 3; if your SageMath is version 9.2 or newer, it is.)

## Installation of Gurobi

Install Gurobi according to the instructions on the website,
which includes obtaining a license key.

- On a Linux system, after unpacking the Gurobi archive in the desired location,
  such as `/opt`, set the environment variable `GUROBI_HOME` to the directory containing the subdirectories `bin`, `lib`, ...:

        $ export GUROBI_HOME=/opt/gurobi900/linux64

  Then adjust your `PATH` (or create symbolic links) so that the interactive Gurobi shell `gurobi.sh` can be found from your `PATH`:

        $ export PATH="$GUROBI_HOME/bin:$PATH"

- On macOS, the Gurobi installer should make the interactive Gurobi shell ``gurobi.sh`` available in `/usr/local/bin` and therefore from your ``PATH``.

Verify this by typing the shell command ``gurobi.sh``::

    $ gurobi.sh
    Python 3.7.4 (default, Aug 27 2019, 11:27:39)
    ...
    Gurobi Interactive Shell (mac64), Version 9.0.0
    Copyright (c) 2019, Gurobi Optimization, LLC
    Type "help()" for help
    gurobi>

If this does not work, adjust your ``PATH`` (or create symbolic links) so
that ``gurobi.sh`` is found.

## Installation of this package

This package finds the Gurobi installation using the `GUROBI_HOME` environment variable.  (On macOS, it suffices to have `gurobi.sh` in your ``PATH``.)
An alternative method of build configuration is to set compiler/linker flags appropriately.

In [SageMath 9.1 and newer](https://wiki.sagemath.org/ReleaseTours/sage-9.1#Easier_installation_of_optional_linear_and_mixed_integer_linear_optimization_backends), this package is available as an optional SPKG and can be installed using

    $ sage -i sage_numerical_backends_gurobi

Alternatively, you can install this package from PyPI using

    $ sage -pip install sage-numerical-backends-gurobi

or from a checked out source tree using

    $ sage -pip install .

or from GitHub using

    $ sage -pip install git+https://github.com/sagemath/sage-numerical-backends-gurobi

(See [`build.yml` in the related package sage-numerical-backends-coin package](https://github.com/sagemath/sage-numerical-backends-coin/blob/master/.github/workflows/build.yml) for details about package prerequisites on various systems.)

## Using this package

After a successful installation, Sage will automatically make this new backend
the default MIP solver.

To select the `'Gurobi'` solver explicitly as the default MIP backend, additionally use the following command.

    sage: default_mip_solver('Gurobi')

To make these settings permanent, add the above 2 + 1 commands to your `~/.sage/init.sage` file.
Note that this setting will not affect doctesting (`sage -t`) because this file is ignored in doctesting mode.

## Running doctests

To run the (limited) testsuite of this package, use:

    $ sage setup.py test

If no Gurobi license is available, the testing is skipped without error.

To run the Sage testsuite with the default MIP solver set to the backend provided by this package, use:

    $ sage setup.py check_sage_testsuite

If no Gurobi license is available, the testing is skipped without error.

## Running tests with tox

The doctests can also be invoked using `tox`:

    $ tox -e local
    $ tox -e local check_sage_testsuite.py

Testing multiple installed Gurobi versions in parallel (see `tox.ini`):

    $ tox -p auto
