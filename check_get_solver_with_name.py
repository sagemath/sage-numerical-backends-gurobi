from __future__ import print_function
# Check that the backend can be obtained by passing solver='gurobi' to get_solver.
from sage.numerical.backends.generic_backend import get_solver
from sage_numerical_backends_gurobi.gurobi_backend import GurobiBackend
b = get_solver(solver='gurobi')
assert type(b) == GurobiBackend, "get_solver(solver='gurobi') does not give an instance of sage_numerical_backends_gurobi.gurobi_backend.GurobiBackend"
print("Success: get_solver(solver='gurobi') gives {}".format(b))
