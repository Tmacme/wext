#!/usr/bin/env python

# Load required modules
import numpy as np
from constants import *
from exact import exact_test
import cpoibin
from saddlepoint import saddlepoint
from comet_exact_test import comet_exact_test
import warnings

# Perform the weighted-row exclusivity test (WR-test) using the given method.
# Note that EXACT refers to the WR-exclusivity recursive formula, and computes
# the p-value _exactly_.
def wre_test(t, x, p, method=EXACT, verbose=0):
    # Check we're using an appropriate method
    assert( method in METHODS )
    # Check for equal numbers of genes.
    assert(len(x)==len(p))
    # Check for equal numbers of samples.
    assert(min(len(a) for a in p)==max(len(a) for a in p))
    # Check that the probabilities are in (0, 1].
    assert(all(0<b<= 1 for a in p for b in a))
    # Check that the number of mutations in each gene is not greater than the number of samples.
    assert(all(a<=len(b) for a, b in zip(x, p)))
    # Check that the number of mutually exclusive mutations is not greater than the total number of mutations.
    assert(t<=sum(x))
    #Check that we've implemented the given set size with the exact test
    if method == EXACT:
        assert( len(x) in WRE_EXACT_SET_SIZES_IMPLEMENTED )

    p = [ list(p_g) for p_g in p ]

    if method == EXACT:
        p_value = exact_test( t, x, p, verbose )
    if method == SADDLEPOINT:
        # Ignore warnings
        with warnings.catch_warnings() as e:
            warnings.simplefilter("ignore")
            p_value = saddlepoint( t, x, p, verbose )

    return p_value

# Perform the row-exclusivity test (RE-test) using the given method.
# Note that EXACT refers to the CoMEt tail enumeration scheme, and computes
# the p-value _exactly_.
def re_test(t, x, tbl, method=EXACT, verbose=0):
    N = sum(tbl)
    if method == SADDLEPOINT:
        p = [ [ float(x_i)/N ] * N for x_i in x ]
        # Ignore warnings
        with warnings.catch_warnings() as e:
            warnings.simplefilter("ignore")
            p_value = saddlepoint( t, x, p )

    elif method == EXACT:
        k = len(x)
        assert( tbl and len(tbl) == 2**k )
        p_value, mid_p_value = comet_exact_test( k, N, tbl, 1.1 )

    return p_value
