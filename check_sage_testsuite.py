from __future__ import print_function

"""
Check portions of the sage test suite, with default mip solver set to ours.

    sage: M = MixedIntegerLinearProgram()
    sage: M.get_backend()
    <...sage_numerical_backends_gurobi...>
"""

import sage_numerical_backends_gurobi.gurobi_backend as gurobi_backend, sage.numerical.backends as backends, sys
sys.modules['sage.numerical.backends.gurobi_backend'] = backends.gurobi_backend = gurobi_backend

from sage.numerical.backends.generic_backend import default_mip_solver
default_mip_solver('Gurobi')

try:
    from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
    b = GurobiBackend()
except MIPSolverException as e:
    if 'NO_LICENSE' in str(e):
        print("No license: sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend() gives exception:", e, "(ok)", file=sys.stderr)
        print("The module seems to work but the license is missing. Skipping the test suite.", file=sys.stderr)
        sys.exit(0)

from sage.doctest.control import DocTestController, DocTestDefaults
options = DocTestDefaults(nthreads=0, long=False, optional="sage,gurobi", force_lib=True, abspath=True)

import os, sage.env, glob, sys
abs_file = os.path.abspath("check_sage_testsuite.py")
os.chdir(os.path.join(sage.env.SAGE_LIB, 'sage'))
files = ["coding",
         "combinat/designs", "combinat/integer_vector.py", "combinat/posets/",
         "game_theory/",
         "geometry/polyhedron/base.py", "geometry/cone.py",
         "graphs/",
         "homology/simplicial_complex.py",
         "knots/",
         "matroids/",
         "sat/"]

files += glob.glob("numerical/*.py") + glob.glob("numerical/*.pyx")

# First verify that we installed the default backend
DC = DocTestController(options, [abs_file])
err = DC.run()
if err != 0:
    print("Error: Setting the default solver did not work", file=sys.stderr)
    sys.exit(2)

# from $SAGE_SRC/bin/sage-runtests
DC = DocTestController(options, files)
err = DC.run()
if err != 0:
    sys.exit(1)

sys.exit(0)
