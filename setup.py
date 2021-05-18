#! /usr/bin/env python
## -*- encoding: utf-8 -*-

from __future__ import print_function

import os
import sys
import subprocess
from setuptools import setup
from setuptools import Extension
from setuptools.command.test import test as TestCommand # for tests
from Cython.Build import cythonize
from Cython.Compiler.Errors import CompileError
from codecs import open # To open the README file with proper encoding
from sage.env import sage_include_directories

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("PYTHONPATH=`pwd` sage check_license.py")
        if errno >> 8 == 42:
            print("The module seems to work but the license is missing. Skipping the test suite.",
                  file=sys.stderr)
            sys.exit(0)
        elif errno != 0:
            print("check_license.py returned error {}".format(errno))
            sys.exit(1)
        self._actually_run_tests()

    def _actually_run_tests(self):
        # Passing optional=sage avoids using sage.misc.package.list_packages,
        # which gives an error on Debian unstable as of 2019-12-27:
        # FileNotFoundError: [Errno 2] No such file or directory: '/usr/share/sagemath/build/pkgs'
        errno = os.system("PYTHONPATH=`pwd` sage -t --force-lib --optional=sage,gurobi sage_numerical_backends_gurobi")
        if errno != 0:
            sys.exit(1)

class SageTestSage(SageTest):
    def _actually_run_tests(self):
        errno = os.system("PYTHONPATH=`pwd` sage -c 'load(\"check_sage_testsuite.py\")'")
        if errno != 0:
            sys.exit(1)

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

gurobi_include_directories = []
gurobi_lib_directories = []
gurobi_lib_files = []
gurobi_libs = []
gurobi_home = os.getenv("GUROBI_HOME")

if not gurobi_home:
    # gurobi.sh might be in PATH.  As of Gurobi 9.0 (on macOS), it is
    # a shell script that sets (but does not export) GUROBI_HOME
    # and then invokes a Python interpreter.
    # Gurobi 8.0.1 and 8.1.1 (on macOS) do not set GUROBI_HOME
    # but set PYTHONPATH.
    try:
        gurobi_home = subprocess.check_output(
            '. gurobi.sh -c "" '
            '&& if [ -n "$GUROBI_HOME" ]; then echo $GUROBI_HOME; else dirname $PYTHONPATH; fi',
            shell=True).decode("UTF-8").strip()
        print("Using GUROBI_HOME obtained from gurobi.sh: {}".format(gurobi_home),
              file=sys.stderr)
    except subprocess.CalledProcessError:
        pass

exts = ['so']
if sys.platform == 'darwin':
    exts.insert(0, 'dylib')

use_rpath = True

if gurobi_home:
    gurobi_include_directories.append(gurobi_home + "/include")
    libdir = gurobi_home + "/lib"
    gurobi_lib_directories.append(libdir)
    from fnmatch import fnmatch
    for file in os.listdir(libdir):
        # Avoid libgurobi81_light.dylib, which causes runtime
        if any(fnmatch(file, 'libgurobi*.' + ext) for ext in exts) and not fnmatch(file, 'libgurobi*light*.*'):
            gurobi_libs = [os.path.splitext(file)[0][3:]]
            gurobi_lib_files = [os.path.join(libdir, file)]
            break

if not gurobi_libs:
    print("GUROBI_HOME is not set, or it does not point to a directory with a "
          "Gurobi installation.  Trying to link against -lgurobi", file=sys.stderr)
    gurobi_libs = ['gurobi']
else:
    print("Using gurobi_include_directories={}, libraries={}, library_dirs={}".format(
        gurobi_include_directories, gurobi_libs, gurobi_lib_directories), file=sys.stderr)

if use_rpath:
    lib_args = dict(libraries=gurobi_libs,
                    library_dirs=gurobi_lib_directories,
                    runtime_library_dirs=gurobi_lib_directories)
else:
    lib_args = dict(extra_link_args=gurobi_lib_files)

 # Cython modules
ext_modules = [Extension('sage_numerical_backends_gurobi.gurobi_backend',
                         sources = [os.path.join('sage_numerical_backends_gurobi',
                                     'gurobi_backend.pyx')],
                         include_dirs=sage_include_directories() + gurobi_include_directories,
                         **lib_args)
    ]


## SageMath 8.1 (included in Ubuntu bionic 18.04 LTS) does not have sage.cpython.string;
## it was introduced in 8.2.
compile_time_env = {'HAVE_SAGE_CPYTHON_STRING': False,
                    'HAVE_ADD_COL_UNTYPED_ARGS': False}

print("Checking whether HAVE_SAGE_CPYTHON_STRING...", file=sys.stderr)
try:
    import sage.cpython.string
    compile_time_env['HAVE_SAGE_CPYTHON_STRING'] = True
except ImportError:
    pass

## SageMath 8.7 changed the signature of add_col.
print("Checking whether HAVE_ADD_COL_UNTYPED_ARGS...", file=sys.stderr)
try:
    cythonize(Extension('check_add_col_untyped_args',
                        sources=['check_add_col_untyped_args.pyx'],
                        include_dirs=sage_include_directories()),
              quiet=True,
              include_path=sys.path)
    compile_time_env['HAVE_ADD_COL_UNTYPED_ARGS'] = True
except CompileError:
    pass

print("Using compile_time_env: {}".format(compile_time_env), file=sys.stderr)

setup(
    name="sage_numerical_backends_gurobi",
    version=readfile("VERSION").strip(),
    description="Gurobi backend for Sage MixedIntegerLinearProgram",
    long_description = readfile("README.md"), # get the long description from the README
    long_description_content_type='text/markdown', # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    url="https://github.com/sagemath/sage-numerical-backends-gurobi",
    # Author list obtained by running the following command on sage 9.0.beta9:
    # for f in gurobi_backend.p*; do git blame -w -M -C -C --line-porcelain "$f" | grep -I '^author '; done | sort -f | uniq -ic | sort -n
    # cut off at < 10 lines of attribution.
    author='Nathann Cohen, Martin Albrecht, Matthias Koeppe, John Perry, David Coudert, Jori Mäntysalo, Jeroen Demeyer, Erik M. Bray, Emil R. Vaughan, and others',
    author_email='sage-support@googlegroups.com',
    license='GPLv2+', # This should be consistent with the LICENCE file
    classifiers=['Development Status :: 5 - Production/Stable',
                 "Intended Audience :: Science/Research",
                 'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2",
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.4',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9',
                 ],
    ext_modules = cythonize(ext_modules, include_path=sys.path,
                            compile_time_env=compile_time_env),
    cmdclass = {'test': SageTest, 'check_sage_testsuite': SageTestSage}, # adding a special setup command for tests
    keywords=['milp', 'linear-programming', 'optimization'],
    packages=['sage_numerical_backends_gurobi'],
    package_dir={'sage_numerical_backends_gurobi': 'sage_numerical_backends_gurobi'},
    package_data={'sage_numerical_backends_gurobi': ['*.pxd']},
    install_requires = [# 'sage>=8',    ### On too many distributions, sage is actually not known as a pip package
                        'sphinx'],
)
