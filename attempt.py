#!/usr/bin/env python3

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
def __main__():
    w = tryopen( sys.argv[1] )
    print( "account: %s", json.dumps( w, indent=4 ))

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
    __main__()
