"""
Here we create the data.
"""
import csv
import numpy as np
import sys
sys.path.append('/Users/valerianoaiello/Documents/GitHub/Thompson-knot-theory/src/math_library')
from group_operations import *
from knot_construction import *
from generators_F_3 import *



"""
This function generates all the paths from the identity of F_3 to the elements of radius "radius".
"""
def generate_paths(radius: int) -> np.ndarray:
    v = np.array([i for i in range(-3,4) if i != 0])
    l = np.array([v for i in range(radius)])

    w = np.array(np.meshgrid(*l)).T.reshape(-1, radius)
    return w


"""
The following function checks if a path contains two consecutive entries of opposite sign 
(if this happens the path is not minimal)
"""
def check_reduced_path(path):
    first_entries = path[:-1]
    last_entries = path[1:]
    if np.count_nonzero(first_entries + last_entries) == len(path) -1:
        return True
    else:
        return False

"""
This function takes a path starting from the identity of F_3 and returns the product of all the elements.
The path is described by a vector whose entries are 3, 2, 1, -1, -2, -3 representing x_2^-1, x_1^-1, x_0^-1, x_0, x_1, x_2.  
"""
def multiply_elements_in_path(path_of_tree_diagrams):
  number_of_elements = len(multiply_elements_in_path)
  product = Ternary_tree_diagrams()
  if number_of_elements ==0:
    return product
#  elif number_of_elements == 1:
#    return path_of_tree_diagrams[0]
  else:
    for i in range(len(path_of_tree_diagrams)):
      if path_of_tree_diagrams[i] == 1 :
        product = multiplication_tree_diagrams(product, x_0)
      elif path_of_tree_diagrams[i] == -1 :
       product = multiplication_tree_diagrams(product, x_0inv)
      elif path_of_tree_diagrams[i] == 2:
        product = multiplication_tree_diagrams(product, x_1)
      elif path_of_tree_diagrams[i] == -2:
       product = multiplication_tree_diagrams(product, x_1inv)
      elif path_of_tree_diagrams[i] == 3:
        product = multiplication_tree_diagrams(product, x_2)
      elif path_of_tree_diagrams[i] == -3:
       product = multiplication_tree_diagrams(product, x_2inv)
    return product
    

t = Ternary_tree_diagrams()
x_0.print_tree_diagram()
print(len(generate_paths(3)))
print(type(generate_complete_ternary_tree(3)))
print(type(from_tree_to_graph(x_0)))
print(generate_paths(2).shape)
#for i in range(n):
#    print('i=', i, generate_paths(2)[i][:])
def create_dataset(radius: np.ndarray, csv_path: str) -> None:
    with open(csv_path, 'w') as f:
        writer = csv.writer(f)
        writer.writerow([
            'normal_form',
            'leaves',
            'connected_components',
#            'HOMFLY',
        ])
        for i in range(radius):
            elements = generate_paths(i)
            number_of_elements, _ = elements.shape
            for j in range(number_of_elements):
                if check_reduced_path(elements[j][:]):
                    element = elements[i][:]
                    number_of_leaves = element.get_number_leaves()
                    normal_form_of_element = find_normal_form(element)
                    number_of_connected_components = tree_diagram_to_planar_diagram(element)
                    writer.writerow(
                        [normal_form_of_element] +
                        [number_of_leaves] +
                        [number_of_connected_components]
                    )
create_dataset(2, '/Users/valerianoaiello/Documents/GitHub/Thompson-knot-theory/data.csv')