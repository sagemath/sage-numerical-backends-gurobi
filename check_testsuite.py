import os
import sys

errno = os.system(r'sage -c "load(\"check_license.py\")"')
if errno >> 8 == 42:
    print("The module seems to work but the license is missing. Skipping the test suite.",
          file=sys.stderr)
    sys.exit(0)
elif errno != 0:
    print("check_license.py returned error {}".format(errno))
    sys.exit(1)

# Passing optional=sage avoids using sage.misc.package.list_packages,
# which gives an error on Debian unstable as of 2019-12-27:
# FileNotFoundError: [Errno 2] No such file or directory: '/usr/share/sagemath/build/pkgs'

errno = os.system("sage -t --force-lib --optional=sage,gurobi sage_numerical_backends_gurobi")
if errno != 0:
    sys.exit(1)
