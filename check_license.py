from __future__ import print_function
import sys

from sage.numerical.mip import MIPSolverException
import sage_numerical_backends_gurobi.gurobi_backend as gurobi_backend
from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
print("Success: Imported GurobiBackend from {}".format(gurobi_backend.__file__), file=sys.stderr)

try:
    b = GurobiBackend()
except MIPSolverException as e:
    if 'NO_LICENSE' in str(e):
        print("No license: sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend() gives exception:", e, "(ok)", file=sys.stderr)
        sys.exit(42)
    else:
        raise
else:
    print("Success: sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend() gives {}".format(b),
        file=sys.stderr)
