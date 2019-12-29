# sage-numerical-backends-gurobi: Gurobi mixed integer linear programming backend for SageMath

[![PyPI](https://img.shields.io/pypi/v/sage-numerical-backends-gurobi)](https://pypi.org/project/sage-numerical-backends-gurobi/ "PyPI: sage-numerical-backends-gurobi")

`GurobiBackend` has previously been available as part of the [SageMath](http://www.sagemath.org/) source tree,
from which it is built as an "optional extension" if the proprietary Gurobi library and header files have been symlinked into `$SAGE_LOCAL` manually.

Because of the proprietary nature of the Gurobi software, `GurobiBackend` is not available in any binary distributions of SageMath.

The present standalone Python package `sage-numerical-backends-gurobi` has been created from the SageMath sources, version 9.0.beta10.  It can be installed on top of various Sage installations using pip, including older versions of Sage such as 8.1 (as shipped by Ubuntu bionic 18.04LTS).

## Installation

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

This package finds the Gurobi installation using the `GUROBI_HOME` environment variable.  (On macOS, it suffices to have `gurobi.sh` in your ``PATH``.)
An alternative method of build configuration is to set compiler/linker flags appropriately.

Install this package from PyPI using

    $ sage -python -m pip install sage-numerical-backends-gurobi

or from a checked out source tree using

    $ sage -python -m pip install .

or from GitHub using

    $ sage -python -m pip install git+https://github.com/mkoeppe/sage-numerical-backends-gurobi

(See [`build.yml` in the related package sage-numerical-backends-coin package](https://github.com/mkoeppe/sage-numerical-backends-coin/blob/master/.github/workflows/build.yml) for details about package prerequisites on various systems.)

## Using this package

To obtain a solver (backend) instance:

    sage: from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
    sage: GurobiBackend()
    <sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend object at 0x7fb72c2c7528>

Equivalently:

    sage: from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
    sage: from sage.numerical.backends.generic_backend import get_solver
    sage: get_solver(solver=GurobiBackend)
    <sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend object at 0x7fe21ffbe2b8>

To use this solver (backend) with [`MixedIntegerLinearProgram`](http://doc.sagemath.org/html/en/reference/numerical/sage/numerical/mip.html):

    sage: from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
    sage: M = MixedIntegerLinearProgram(solver=GurobiBackend)
    sage: M.get_backend()
    <sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend object at 0x7fb72c2c7868>

Setting it as the default backend for `MixedIntegerLinearProgram`, as of SageMath 9.0.beta10, requires some trickery:

    sage: import sage_numerical_backends_gurobi.gurobi_backend as gurobi_backend, sage.numerical.backends as backends, sys
    sage: sys.modules['sage.numerical.backends.gurobi_backend'] = backends.gurobi_backend = gurobi_backend
    sage: default_mip_solver('Gurobi')

To patch this in permanently (at your own risk):

    $ sage -c 'import os; import sage.numerical.backends as dm; import sage_numerical_backends_gurobi.gurobi_backend as sm; s = sm.__file__; f = os.path.basename(s); d = os.path.join(dm.__path__[0], f); (os.path.exists(d) or os.path.lexists(d)) and os.remove(d); os.symlink(s, d);'

Or use the script [`patch_into_sage_module.py`](patch_into_sage_module.py) in the source distribution that does the same:

    $ sage -c 'load("patch_into_sage_module.py")'
    Success: Patched in the module as sage.numerical.backends.gurobi_backend

Verify with [`check_get_solver_with_name.py`](check_get_solver_with_name.py) that the patching script has worked:

    $ sage -c 'load("check_get_solver_with_name.py")'
    Success: get_solver(solver='gurobi') gives <sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend object at 0x7f8f20218528>
