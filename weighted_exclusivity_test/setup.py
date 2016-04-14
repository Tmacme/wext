#!/usr/bin/env python

"""Compiles the C modules used by the weighted enrichment test."""

# Load required modules
from distutils.core import setup, Extension
import subprocess, numpy, os

thisDir = os.path.dirname(os.path.realpath(__file__))

# Compile the Poisson-Binomial module
srcs = ['/src/c/poibinmodule.c']
module = Extension('cpoibin', include_dirs=[numpy.get_include()],
    sources = [ thisDir + s for s in srcs ],
    extra_compile_args = ['-g', '-O0'])
setup(name='poibin', version='0.0.1',  ext_modules=[module],
      description='Module for analyzing the Poisson-Binomial distribution.')

# Compile the weighted enrichment module
srcs = ['/src/c/exact_test.c']
module = Extension('cexact_test', include_dirs=[numpy.get_include()],
    sources = [ thisDir + s for s in srcs ],
    extra_compile_args = ['-g', '-O0'])
setup(name='cexact_test', version='0.0.1',  ext_modules=[module],
      description='Exact test implementation of Weighted enrichment test.')