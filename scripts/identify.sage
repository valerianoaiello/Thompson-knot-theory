# Identification of the knots found by run.py with KnotInfo and SnapPy, in parallel on all the cores.
# The code is in identify_lib.py (a plain Python module, so that the 'spawn' worker processes can
# import it); see its docstring.
#
# usage (from F_index/):   sage scripts/identify.sage [max_crossing_number_in_output] [F|F3] [processes]
import os, sys
sys.path.insert(0, os.path.join(os.getcwd(), 'scripts'))
import identify_lib

if __name__ == '__main__':
    identify_lib.main(sys.argv[1:])
