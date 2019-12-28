from __future__ import print_function
import sys

from sage.numerical.mip import MIPSolverException
from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend

try:
    b = GurobiBackend()
except MIPSolverException as e:
    if 'NO_LICENSE' in str(e):
        print("Success: sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend() gives exception:", e, "(ok)", file=sys.stderr)
    else:
        raise
else:
    print("Success: sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend() gives {}".format(b),
        file=sys.stderr)
