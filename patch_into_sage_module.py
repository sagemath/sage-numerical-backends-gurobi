from __future__ import print_function
import os
import sage.numerical.backends as dm
import sage_numerical_backends_coin.coin_backend as sm
s = sm.__file__
f = os.path.basename(s)
d = os.path.join(dm.__path__[0], f)
try:
    os.remove(d)
except Exception:
    pass
os.symlink(s, d)
print("Success: Patched in the module as sage.numerical.backends.coin_backend")
