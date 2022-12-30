"""
Here we create the data.
"""

import sys
from sage.all import *

import csv
import numpy as np
import sys
sys.path.append('/afs/cern.ch/work/v/vaiello/private/Thompson-knot-theory/src/')
from group_operations import *
from knot_construction import *



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
  global x_0
  global x_0inv
  global x_1
  global x_1inv
  global x_2
  global x_2inv

  x_0 = Ternary_tree_diagrams(['00', '01', '02', '1', '2'], ['0', '1', '20', '21', '22'])
  x_1 = Ternary_tree_diagrams(['0', '10', '11', '12', '2'], ['0', '1', '20', '21', '22'])
  x_2 = right_shift_homomorphism(x_0)

  x_0inv = x_0.inverse_tree_diagram()
  x_1inv = x_1.inverse_tree_diagram()
  x_2inv = x_2.inverse_tree_diagram()

  number_of_elements = len(path_of_tree_diagrams)
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
    

def create_dataset(radius: np.ndarray, csv_path: str) -> None:

  with open(csv_path, 'w') as f:
      writer = csv.writer(f)
      writer.writerow([
          'word',
          'normal_form',
          'leaves',
          'connected_components',
          'HOMFLY',
      ])
      for i in range(1, radius + 1):
        paths_from_identity = generate_paths(i)
        number_of_elements, _ = paths_from_identity.shape
        for j in range(number_of_elements):
          if check_reduced_path(paths_from_identity[j][:]):
            single_path = paths_from_identity[j][:]
            element = multiply_elements_in_path(paths_from_identity[j][:])
            number_of_leaves = element.get_number_leaves()
            normal_form_of_element = find_normal_form(element)
            normal_form_of_element_listed = [list(normal_form_of_element[0]), list(normal_form_of_element[1])]
            planar_diagram = tree_diagram_to_planar_diagram(element)
            number_of_connected_components = len(planar_diagram)
            link = Link(planar_diagram)
            homfly_polynomial  = link.homfly_polynomial()
#            print('qui', normal_form_of_element)
#            print(number_of_leaves, normal_form_of_element, type(element)) 
            element.print_tree_diagram()
            writer.writerow(
                  [single_path] +
                  [normal_form_of_element_listed] +
                  [number_of_leaves] +
                  [number_of_connected_components] +
                  [homfly_polynomial]
              )

if __name__ == '__main__':
  create_dataset(1, '/afs/cern.ch/work/v/vaiello/private/Thompson-knot-theory/src/data.csv')
  
"""
t = Ternary_tree_diagrams(['0', '1', '20', '21', '220', '221', '2220', '2221', '2222'], ['0', '1', '2000', '2001', '2002', '201', '202', '21', '22'])
  print(find_normal_form(t))





  paths_from_identity = generate_paths(2)  
#  print(paths_from_identity)  

  number_of_elements, _ = paths_from_identity.shape
  for j in range(number_of_elements):
      if check_reduced_path(paths_from_identity[j][:]):
          single_path = paths_from_identity[j][:]
  element = multiply_elements_in_path(paths_from_identity[0][:])
  print(paths_from_identity[0][:])
  print(type(element))
  print(element.top)
  print(element.bottom)
  print("normal form:", find_normal_form(element))
"""
