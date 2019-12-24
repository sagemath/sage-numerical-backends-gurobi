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
from codecs import open # To open the README file with proper encoding
from sage.env import sage_include_directories

# For the tests
class SageTest(TestCommand):
    def run_tests(self):
        errno = os.system("sage -t --force-lib sage_numerical_backends_gurobi")
        if errno != 0:
            sys.exit(1)

# Get information from separate files (README, VERSION)
def readfile(filename):
    with open(filename, encoding='utf-8') as f:
        return f.read()

gurobi_include_directories = []
gurobi_lib_directories = []
gurobi_libs = []
gurobi_home = os.getenv("GUROBI_HOME")

if not gurobi_home:
    # gurobi.sh might be in PATH.  As of Gurobi 9.0 (on macOS), it is
    # a shell script that sets (but does not export) GUROBI_HOME
    # and then invokes a Python interpreter.
    try:
        gurobi_home = subprocess.check_output(". gurobi.sh -c '' && echo $GUROBI_HOME", shell=True).decode("UTF-8").strip()
        print("Using GUROBI_HOME obtained from gurobi.sh: {}".format(gurobi_home),
              file=sys.stderr)
    except subprocess.CalledProcessError:
        pass

exts = ['so']
if sys.platform == 'darwin':
    exts.insert(0, 'dylib')

if gurobi_home:
    gurobi_include_directories.append(gurobi_home + "/include")
    libdir = gurobi_home + "/lib"
    gurobi_lib_directories.append(libdir)
    from fnmatch import fnmatch
    for file in os.listdir(libdir):
        if any(fnmatch(file, 'libgurobi*.' + ext) for ext in exts):
            gurobi_libs = [os.path.splitext(file)[0][3:]]
            break

if not gurobi_libs:
    print("GUROBI_HOME is not set, or it does not point to a directory with a "
          "Gurobi installation.  Trying to link against -lgurobi", file=sys.stderr)
    gurobi_libs = ['gurobi']
else:
    print("Using gurobi_include_directories={}, libraries={}, library_dirs={}".format(
        gurobi_include_directories, gurobi_libs, gurobi_lib_directories), file=sys.stderr)

 # Cython modules
ext_modules = [Extension('sage_numerical_backends_gurobi.gurobi_backend',
                         sources = [os.path.join('sage_numerical_backends_gurobi',
                                     'gurobi_backend.pyx')],
                         include_dirs=sage_include_directories() + gurobi_include_directories,
                         libraries=gurobi_libs,
                         library_dirs=gurobi_lib_directories)
    ]

setup(
    name="sage_numerical_backends_gurobi",
    version=readfile("VERSION").strip(),
    description="Gurobi backend for Sage MixedIntegerLinearProgram",
    long_description = readfile("README.md"), # get the long description from the README
    long_description_content_type='text/markdown', # https://packaging.python.org/guides/making-a-pypi-friendly-readme/
    url="https://github.com/mkoeppe/sage-numerical-backends-gurobi",
    # Author list obtained by running the following command on sage 9.0.beta9:
    # for f in gurobi_backend.p*; do git blame -w -M -C -C --line-porcelain "$f" | grep -I '^author '; done | sort -f | uniq -ic | sort -n
    # cut off at < 10 lines of attribution.
    author='Nathann Cohen, Martin Albrecht, Matthias Koeppe, John Perry, David Coudert, Jori Mäntysalo, Jeroen Demeyer, Erik M. Bray, Emil R. Vaughan, and others',
    author_email='mkoeppe@math.ucdavis.edu',
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
                 ],
    ext_modules = cythonize(ext_modules, include_path=sys.path),
    cmdclass = {'test': SageTest}, # adding a special setup command for tests
    keywords=['milp', 'linear-programming', 'optimization'],
    packages=['sage_numerical_backends_gurobi'],
    package_dir={'sage_numerical_backends_gurobi': 'sage_numerical_backends_gurobi'},
    package_data={'sage_numerical_backends_gurobi': ['*.pxd']},
    install_requires = ['sage>=8', 'sage-package', 'sphinx'],
)
