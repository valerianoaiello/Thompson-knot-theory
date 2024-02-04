
#from src.math_library import group_operations
#from .math_library import group_operations
#import sys
#sys.path.insert(1, '/Users/valerianoaiello/Documents/GitHub/Thompson-knot-theory/src')
#from Users.valerianoaiello.Documents.GitHub.Thompson-knot-theory.src.group_operations import *


import sys
sys.path.append('/afs/cern.ch/work/v/vaiello/private/Thompson-knot-theory/src/')
from group_operations import *



"""
This part contains the generators of F_3: x_0, x_1, x_2 and their inverses.
"""

x_0 = Ternary_tree_diagrams(['00', '01', '02', '1', '2'], ['0', '1', '20', '21', '22'])
x_1 = Ternary_tree_diagrams(['0', '10', '11', '12', '2'], ['0', '1', '20', '21', '22'])
x_2 = right_shift_homomorphism(x_0)

x_0inv = x_0.inverse_tree_diagram()
x_1inv = x_1.inverse_tree_diagram()
x_2inv = x_2.inverse_tree_diagram()

"""
if __name__ == '__main__':
  x_0 = Ternary_tree_diagrams(['00', '01', '02', '1', '2'], ['0', '1', '20', '21', '22'])
  x_0.print_tree_diagram()
#  t = multiplication_tree_diagrams(x_0,x_0)
  print('hello')
"""