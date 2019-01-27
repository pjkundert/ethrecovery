#!/usr/bin/env python3

from __future__ import print_function

# 
# Read a stream of passwords provided on separate lines to stdin, and attempt to unlock the JSON
# keystore file named on the command line.  A number of parallel threads to use can be provided
# after the JSON keystore file name.
# 
# EXAMPLE
# 
# Use 8 threads to attempt to open the JSON file "keystore/*.test"
# 
#     ... | ./attempt.py keystore/*.test 8
# 
import sys
import json
from ethereum.tools.keys import decode_keystore_json
from utils import encode_hex
from joblib import Parallel, delayed

# The base class of string types
type_str_base			= basestring if sys.version_info[0] < 3 else str

class PasswordFoundException(Exception):
    pass

def tryopen(f):
    try:
        assert f
        t = open(f).read()
        try:
            return json.loads(t)
        except:
            raise Exception("Corrupted file: "+f)
    except:
        return None

    
def attempt(w, pw, verbose):
    if not isinstance(pw, type_str_base):
        pw = ''.join(str(i) for i in pw)

    if verbose > 0:
        print (pw)

    try:
        if 'encseed' in w:
            seed = getseed(w['encseed'], pw, w['ethaddr'])
        else:
            seed = decode_keystore_json(w, pw)

        if seed:
            print(
                """\n\nYour seed is:\n%s\n\nYour password is:\n%s\n""" %
                (encode_hex(seed), pw))
            raise PasswordFoundException()

    except ValueError:
        return None

verbose=True

def main():
    w = tryopen( sys.argv[1] )
    print( "account: %s" % json.dumps( w, indent=4 ))

    try:
        if len( sys.argv ) > 2:
            Parallel( n_jobs=int(sys.argv[2]))(
                delayed(attempt)( w, pw.strip(), verbose=verbose )
                for pw in sys.stdin )
        else:
            for pw in sys.stdin:
                attempt( w, pw.strip(), verbose=verbose )
            
        print("None of the passwords worked.")

    except PasswordFoundException as e:
        pass
        
if __name__ == "__main__":
    main()
