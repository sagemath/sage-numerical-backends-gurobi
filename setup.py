#! /usr/bin/env python
## -*- encoding: utf-8 -*-
import os
import sys
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

 # Cython modules
ext_modules = [Extension('sage_numerical_backends_gurobi.gurobi_backend',
                         sources = [os.path.join('sage_numerical_backends_gurobi',
                                     'gurobi_backend.pyx')],
                         include_dirs=sage_include_directories())
    ]

setup(
    name="sage_numerical_backends_gurobi",
    version=readfile("VERSION").strip(),
    description="Gurobi backend for Sage MixedIntegerLinearProgram",
    long_description = readfile("README.md"), # get the long description from the README
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
