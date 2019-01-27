#!/usr/bin/env python3

from __future__ import print_function

import sys

from itertools import compress, product, permutations

def combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )


for c in combinations( sys.argv[1:]):
    for p in permutations( c ):
        print( ''.join( p ) )
