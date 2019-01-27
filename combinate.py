#!/usr/bin/env python3

# Generate all combinations and permutations of the words provided on the command-line, with no
# whitespace between them.
# 
# EXAMPLE
# 
# If you know your password was comprised of some of the following words in some order, without
# whitespace:
# 
# ./combinate.py horse stable correct battery mouse | ...
#

from __future__ import print_function

import sys

from itertools import compress, product, permutations

def combinations(items):
    return ( set(compress(items,mask)) for mask in product(*[[0,1]]*len(items)) )

def main():
    for c in combinations( sys.argv[1:]):
        for p in permutations( c ):
            print( ''.join( p ) )

if __name__ == "__main__":
    main()
