from __future__ import print_function
# Check that the backend can be obtained by passing solver='coin' to get_solver.
from sage.numerical.backends.generic_backend import get_solver
from sage_numerical_backends_coin.coin_backend import CoinBackend
b = get_solver(solver='coin')
assert type(b) == CoinBackend, "get_solver(solver='coin') does not give an instance of sage_numerical_backends_coin.coin_backend.CoinBackend"
print("Success: get_solver(solver='coin') gives {}".format(b))
