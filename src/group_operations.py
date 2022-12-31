"""
GROUP OPERATIONS IN THE BROWN-THOMPSON GROUP F_3
"""

import copy
import numpy as np




#import sys
#sys.path.append('/Users/valerianoaiello/Documents/GitHub/Thompson-knot-theory/src/')
#from generators_F_3 import *
"""
GROUP OPERATIONS IN THE BROWN-THOMPSON GROUP F_3
"""

"""
We describe ternary tree diagrams with pairs of ternary words. 

The method inverse_tree_diagram computes the inverse of an element of F_3. The inverse is simply obtained by exchanging the trees in 
the ternary tree diagram.

The method get_number_leaves returns the number of leaves of each ternary tree in the ternary tree diagram.

The method inverse calculates the inverse of an element of F_3
"""

class Ternary_tree_diagrams:
  def __init__(self, top_tree = ["0"], bottom_tree = ["0"]):
    self.top = top_tree
    self.bottom = bottom_tree
  def get_number_leaves(self):
    return len(self.top)
  def inverse_tree_diagram(self):
    return Ternary_tree_diagrams(self.bottom, self.top)
  def print_tree_diagram(self):
    print("top tree", self.top)
    print("bottom tree", self.bottom)



"""
Given a ternary tree diagram (tree_plus, tree_minus), this function returns the image under the right shift homomorphism in the terminology of [AiNa].

References:
V. Aiello, T. Nagnibeda, On the oriented Thompson subgroup F⃗3 and its relatives in higher Brown-Thompson groups, Journal of Algebra and its Applications, 
Volume 21, Issue 07, 2250139, doi: 10.1142/S0219498822501390, preprint arXiv:1912.04730
"""
def right_shift_homomorphism(ternary_tree_diagram):
  tree_plus_deep_cp = copy.deepcopy(ternary_tree_diagram.top)
  tree_minus_deep_cp = copy.deepcopy(ternary_tree_diagram.bottom) 

  for i in range(len(tree_plus_deep_cp)):
      tree_plus_deep_cp[i] = "2"+ tree_plus_deep_cp[i] 
      tree_minus_deep_cp[i] = "2"+ tree_minus_deep_cp[i] 
  tree_plus_deep_cp.insert(0, '1')
  tree_minus_deep_cp.insert(0, '1')
  tree_plus_deep_cp.insert(0, '0')
  tree_minus_deep_cp.insert(0, '0')
  shifted_ternary_tree_diagram = Ternary_tree_diagrams(tree_plus_deep_cp, tree_minus_deep_cp)
  return shifted_ternary_tree_diagram


"""
Given a ternary tree diagram (tree_plus, tree_minus), this function returns the image under the middle shift homomorphism in the terminology of [AiNa].

References:
V. Aiello, T. Nagnibeda, On the oriented Thompson subgroup F⃗3 and its relatives in higher Brown-Thompson groups, Journal of Algebra and its Applications, 
Volume 21, Issue 07, 2250139, doi: 10.1142/S0219498822501390, preprint arXiv:1912.04730
"""
def middle_shift_homomorphism(ternary_tree_diagram):
  tree_plus_deep_cp = copy.deepcopy(ternary_tree_diagram.top)
  tree_minus_deep_cp = copy.deepcopy(ternary_tree_diagram.bottom) 

  for i in range(len(tree_plus_deep_cp)):
      tree_plus_deep_cp[i] = "1"+ tree_plus_deep_cp[i] 
      tree_minus_deep_cp[i] = "1"+ tree_minus_deep_cp[i] 
  tree_plus_deep_cp.insert(0, '0')
  tree_minus_deep_cp.insert(0, '0')
  tree_plus_deep_cp.insert(-1, '2')
  tree_minus_deep_cp.insert(-1, '2')
  shifted_ternary_tree_diagram = Ternary_tree_diagrams(tree_plus_deep_cp, tree_minus_deep_cp)
  return shifted_ternary_tree_diagram


"""
This is the flip automorphism on F_3. It has order 2 and on the level of ternary tree diagrams is obtained by reflecting 
the trees about a vertical line.

References:
V. Aiello, T. Nagnibeda, On the 3-colorable subgroup and maximal subgroups of Thompson’s group F
"""
def flip_automorphism(ternary_tree_diagram):
  
  tree_plus_deep_cp = copy.deepcopy(ternary_tree_diagram.top)
  tree_minus_deep_cp = copy.deepcopy(ternary_tree_diagram.bottom) 

  for i in range(len(tree_plus_deep_cp)):
      for j in range(len(tree_plus_deep_cp[i])):
        if tree_plus_deep_cp[i][j] == '0':
          tree_plus_deep_cp[i] = tree_plus_deep_cp[i][:j] + '2' + tree_plus_deep_cp[i][j+1:]
        elif tree_plus_deep_cp[i][j] == '2':
          tree_plus_deep_cp[i] = tree_plus_deep_cp[i][:j] + '0' + tree_plus_deep_cp[i][j+1:]
      for j in range(len(tree_minus_deep_cp[i])):
        if tree_minus_deep_cp[i][j] == '0':
          tree_minus_deep_cp[i] = tree_minus_deep_cp[i][:j] + '2' + tree_minus_deep_cp[i][j+1:]
        elif tree_minus_deep_cp[i][j] == '2':
          tree_minus_deep_cp[i] = tree_minus_deep_cp[i][:j] + '0' + tree_minus_deep_cp[i][j+1:]
  tree_plus_deep_cp.sort()
  tree_minus_deep_cp.sort()
  return Ternary_tree_diagrams(tree_plus_deep_cp, tree_minus_deep_cp)

"""
This function returns the words representing a complete ternary tree, that is it produces the labels of its leaves (these are words in the letters {0, 1, 2}).
The heigth of the tree must be at least 1.
"""
def generate_complete_ternary_tree(height):
  if height == 0:
    return [""]
  elif height == 1:
    return ["0", "1", "2"]
  else:
    return ["0" + i for i in generate_complete_ternary_tree(height-1)]+ ["1" + i for i in generate_complete_ternary_tree(height-1)]+ ["2" + i for i in generate_complete_ternary_tree(height-1)] 




"""
This function makes flattens a list.
It is used in find_common_tree.
"""
def flatten_list(outer_list):
    flat_list = []
    for element in outer_list:
        if type(element) is list:
            for item in element:
                flat_list.append(item)
        else:
            flat_list.append(element)
    return flat_list



"""
Create the graph for the bottom tree. 
The keys are the sources, the values are the targets.
"""

def from_tree_to_graph(ternary_tree_diagram):

# Create graph for top tree.
  graph_plus = {}
  tree_plus = copy.deepcopy(ternary_tree_diagram.top)
  for word in tree_plus:
    for i in range(1,len(word)):
      if '+'+word[:i] not in graph_plus:  
        graph_plus['+'+word[:i]] = ['+' + word[:i+1]]        
        graph_plus['+'+word[:i+1]] = [] 
      elif '+'+word[:i] in graph_plus:  
        graph_plus['+'+word[:i]].append('+' + word[:i+1])        
        graph_plus['+'+word[:i+1]] = []


  if len(graph_plus)>1:
    graph_plus['+']=['+0','+1','+2']
  else:
    graph_plus['+']=['+0']



# graph for bottom tree
  tree_minus = copy.deepcopy(ternary_tree_diagram.bottom)



# Create graph for bottom tree.
  
  for word in tree_minus:
    for i in range(len(word),1,-1):
      if '-'+word[:i] not in tree_minus:  
        graph_plus['-'+word[:i]] = ['-' + word[:i-1]]        
        graph_plus['-'+word[:i-1]] = [] 
      elif '-'+word[:i] in tree_minus: 
        graph_plus['-'+word[:i]].append('-' +  word[:i-1])        
        graph_plus['-'+word[:i-1]] = []


  
 # Add edges to root of bottom tree 
  if len(graph_plus)>1:
    graph_plus['-0']=['-']
    graph_plus['-1']=['-']
    graph_plus['-2']=['-']
  else:
    graph_plus['-0']=['-']

# Connect the leaves of the top tree with those of the bottom tree
  for i in range(len(tree_plus)):
    graph_plus['+'+tree_plus[i]] = ['-'+tree_minus[i], 'leaf']
  return graph_plus






"""
Tree_plus and tree_minus are lists containing ternary words, that is with digits in {0, 1, 2},
each reprententing a ternary tree. Both trees have the same number of leaves. 
The function reduce_tree_diagram takes two ternary trees and applies a reduction move if it can be performed.
The function returns a pair of ternary tree diagrams.
"""
def reduce_tree_diagram(tree_diagram):
  
  tree_plus = copy.deepcopy(tree_diagram.top)
  tree_minus = copy.deepcopy(tree_diagram.bottom)

  for i in range(len(tree_plus)-3,-1,-1):
    if i+2<len(tree_plus) and (tree_plus[i][:-1] == tree_plus[i+1][:-1] == tree_plus[i+2][:-1])and (tree_minus[i][:-1] == tree_minus[i+1][:-1] == tree_minus[i+2][:-1])and (tree_plus[i][-1] == tree_minus[i][-1] == '0') and (tree_plus[i+1][-1] == tree_minus[i+1][-1] == '1') and (tree_plus[i+2][-1] == tree_minus[i+2][-1] == '2'):
        tree_plus[i] = tree_plus[i][:-1]
        tree_minus[i] = tree_minus[i][:-1]
        del tree_plus[i+2]
        del tree_plus[i+1]
        del tree_minus[i+2]
        del tree_minus[i+1]
  tree_diagram_reduced =  Ternary_tree_diagrams(tree_plus, tree_minus)
  return tree_diagram_reduced


 
"""
This function takes two ternary tree diagrams as an input (tree_plus, tree_minus), (tree_plus_prime, tree_minus_prime) and finds 
representative such that the second tree of the first tree diagram is equal to first tree of the second tree diagram.
This will allow us to multiply easily the elements.
"""
def find_common_tree(tree_diagram_one, tree_diagram_two):
  
  tree_plus = copy.deepcopy(tree_diagram_one.top)
  tree_minus = copy.deepcopy(tree_diagram_one.bottom)
  tree_plus_prime = copy.deepcopy(tree_diagram_two.top)
  tree_minus_prime = copy.deepcopy(tree_diagram_two.bottom)

  if tree_minus == tree_plus_prime:
    return tree_plus, tree_minus, tree_plus_prime, tree_minus_prime
  else:
    max_length = max(len(max(tree_minus, key=len)), len(max(tree_plus_prime, key=len)))
    for i in range(len(tree_plus)):
      if len(tree_minus[i])<max_length:
          temp = tree_plus[i]
          temp_completion = generate_complete_ternary_tree(max_length-len(tree_minus[i]))
          tree_plus[i]= [temp + word for word in temp_completion] 
    for i in range(len(tree_minus_prime)):
      if len(tree_plus_prime[i])<max_length:
          temp_2 = tree_minus_prime[i]
          temp_completion_2 = generate_complete_ternary_tree(max_length-len(tree_plus_prime[i]))
          tree_minus_prime[i]= [temp_2 + word for word in temp_completion_2]
  tree_minus = generate_complete_ternary_tree(max_length)    
  tree_plus_prime = generate_complete_ternary_tree(max_length)    

  tree_plus = flatten_list(tree_plus)
  tree_minus_prime = flatten_list(tree_minus_prime)
  tree_diagram_one_mod = Ternary_tree_diagrams(tree_plus, tree_minus)
  tree_diagram_two_mod = Ternary_tree_diagrams(tree_plus_prime, tree_minus_prime)

  return tree_diagram_one_mod, tree_diagram_two_mod



"""
This function calculate the power of an element of F_3.
The element is in the variable "tree_diagram", while "exponent" is an integer
"""
def power_tree_diagram(tree_diagram, exponent):
  result = Ternary_tree_diagrams()
  if exponent == 0:
    return result
  elif exponent >= 0:
    result = multiplication_tree_diagrams(tree_diagram, power_tree_diagram(tree_diagram, exponent-1)) 
    return result
  elif exponent < 0:
    result = multiplication_tree_diagrams(tree_diagram, power_tree_diagram(tree_diagram, exponent+1)) 
    return result
  return result


"""
This function multiplies several elements of F_3.
The input is a list whose elements are ternary tree diagrams
"""
def multiply_many_tree_diagrams(collection_of_tree_diagram):
  number_of_elements = len(collection_of_tree_diagram)
  product = Ternary_tree_diagrams()
  if number_of_elements ==0:
    return product
  elif number_of_elements == 1:
    return collection_of_tree_diagram[0]
  else:
    for i in range(len(collection_of_tree_diagram)):
      product = multiplication_tree_diagrams(product, collection_of_tree_diagram[i])
    return product
  return product  




"""
The following function takes a ternary tree diagram and returns its normal form in terms of two numpy arrays,
one for the positive part, one for the negative one. 
The positive part is described by a vector of the form [a_0, ..., a_n], 
the negative part is described by a vector of the form [b_0, ..., b_n],
where a_0, ..., a_n, b_0, ..., b_n are all non-negative integers. 
This function finds the gives the vectors with the smallest n such that at least one between a_n and b_n is non-zero.
"""
def find_normal_form2(tree_diagram):
  length = tree_diagram.get_number_leaves()

  positive_part = np.zeros(length)
  negative_part = np.zeros(length)

  top_tree = tree_diagram.top
  bottom_tree = tree_diagram.bottom

  right_side = '2'*length


  positive_part[0] = len(top_tree[0])-1
  negative_part[0] = len(bottom_tree[0])-1
  for i in range(1, length):
    if top_tree[i][-1] == '0' and top_tree[i].rstrip('0') in right_side:
      positive_part[i] = len(top_tree[i])-len(top_tree[i].rstrip('0'))-1
    elif top_tree[i][-1] == '0':
      positive_part[i] = len(top_tree[i])-len(top_tree[i].rstrip('0'))
    if bottom_tree[i][-1] == '0' and bottom_tree[i].rstrip('0') in right_side:
      negative_part[i] = len(bottom_tree[i])-len(bottom_tree[i].rstrip('0'))-1
    else:
      negative_part[i] = len(bottom_tree[i])-len(bottom_tree[i].rstrip('0'))

  return positive_part, negative_part


def find_normal_form(tree_diagram):
  length = tree_diagram.get_number_leaves()

  positive_part = np.zeros(length)
  negative_part = np.zeros(length)

  top_tree = tree_diagram.top
  bottom_tree = tree_diagram.bottom

  right_side = '2'*length


  positive_part[0] = len(top_tree[0])-1
  negative_part[0] = len(bottom_tree[0])-1
  for i in range(1, length):
    if top_tree[i][-1] == '0' and top_tree[i].rstrip('0') in right_side:
      positive_part[i] = len(top_tree[i])-len(top_tree[i].rstrip('0'))-1
    elif top_tree[i][-1] == '0':
      positive_part[i] = len(top_tree[i])-len(top_tree[i].rstrip('0'))
    if bottom_tree[i][-1] == '0' and bottom_tree[i].rstrip('0') in right_side:
      negative_part[i] = len(bottom_tree[i])-len(bottom_tree[i].rstrip('0'))-1
    else:
      negative_part[i] = len(bottom_tree[i])-len(bottom_tree[i].rstrip('0'))
  
  nonzero_indices_positive_part = np.nonzero(positive_part)[-1]
  nonzero_indices_negative_part = np.nonzero(negative_part)[-1] 
  if len(nonzero_indices_positive_part)>0:
    length_positive_part = nonzero_indices_positive_part[-1] + 1
  else:
    length_positive_part = 0

  if len(nonzero_indices_negative_part)>0:
    length_negative_part = nonzero_indices_negative_part[-1] + 1
  else:
    length_negative_part = 0

  if length_positive_part + length_negative_part >0:
    max_length = max(length_positive_part, length_negative_part)
    positive_part = positive_part[:max_length + 1]
    negative_part = negative_part[:max_length + 1]
  else:   
    positive_part = np.array([])
    negative_part = np.array([])

  return positive_part, negative_part





"""
The function takes two tree diagrams (described by two pairs of ternary words) finds a representative of their product
(prod_tree_plus_temp, prod_tree_minus_temp) which is then turned into its reduced form by means of the function 
reduce_tree_diagram and do-while
"""
def multiplication_tree_diagrams(tree_diagram_one, tree_diagram_two):
  if tree_diagram_one.get_number_leaves() == 1:
    return tree_diagram_two
  elif tree_diagram_two.get_number_leaves() == 1:
    return tree_diagram_one
  elif tree_diagram_one.top == tree_diagram_two.bottom and tree_diagram_one.bottom == tree_diagram_two.top:
    return Ternary_tree_diagrams()
  else:
    tree_plus = copy.deepcopy(tree_diagram_one.top)
    tree_minus = copy.deepcopy(tree_diagram_one.bottom)
    tree_plus_prime = copy.deepcopy(tree_diagram_two.top)
    tree_minus_prime = copy.deepcopy(tree_diagram_two.bottom)

    tuple_containing_unreduced_tree_diagrams  = find_common_tree(Ternary_tree_diagrams(tree_plus, tree_minus), Ternary_tree_diagrams(tree_plus_prime, tree_minus_prime)) 
    tree_diagram_one_prime = tuple_containing_unreduced_tree_diagrams[0]
    tree_diagram_two_prime = tuple_containing_unreduced_tree_diagrams[1]
    prod_tree_plus_temp = copy.deepcopy(tree_diagram_one_prime.top) 
    prod_tree_minus_temp = copy.deepcopy(tree_diagram_two_prime.bottom)

    tree_diagram_prod = Ternary_tree_diagrams(prod_tree_plus_temp, prod_tree_minus_temp)
    while True:
        lenght_tree_plus = len(tree_diagram_prod.top)
        tree_diagram_prod = reduce_tree_diagram(tree_diagram_prod)
        if lenght_tree_plus == len(tree_diagram_prod.top):
            break
  return tree_diagram_prod



"""
This function takes two ternary tree diagrams as an input (tree_plus, tree_minus), (tree_plus_prime, tree_minus_prime) and finds 
representative such that the second tree of the first tree diagram is equal to first tree of the second tree diagram.
This will allow us to multiply easily the elements.
"""
def find_common_tree(tree_diagram_one, tree_diagram_two):
  
  tree_plus = copy.deepcopy(tree_diagram_one.top)
  tree_minus = copy.deepcopy(tree_diagram_one.bottom)
  tree_plus_prime = copy.deepcopy(tree_diagram_two.top)
  tree_minus_prime = copy.deepcopy(tree_diagram_two.bottom)

  if tree_minus == tree_plus_prime:
    return tree_diagram_one, tree_diagram_two
  else:
    max_length = max(len(max(tree_minus, key=len)), len(max(tree_plus_prime, key=len)))
    for i in range(len(tree_plus)):
      if len(tree_minus[i])<max_length:
          temp = tree_plus[i]
          temp_completion = generate_complete_ternary_tree(max_length-len(tree_minus[i]))
          tree_plus[i]= [temp + word for word in temp_completion] 
    for i in range(len(tree_minus_prime)):
      if len(tree_plus_prime[i])<max_length:
          temp_2 = tree_minus_prime[i]
          temp_completion_2 = generate_complete_ternary_tree(max_length-len(tree_plus_prime[i]))
          tree_minus_prime[i]= [temp_2 + word for word in temp_completion_2]
  tree_minus = generate_complete_ternary_tree(max_length)    
  tree_plus_prime = generate_complete_ternary_tree(max_length)    

  tree_plus = flatten_list(tree_plus)
  tree_minus_prime = flatten_list(tree_minus_prime)
  tree_diagram_one_mod = Ternary_tree_diagrams(tree_plus, tree_minus)
  tree_diagram_two_mod = Ternary_tree_diagrams(tree_plus_prime, tree_minus_prime)
  return tree_diagram_one_mod, tree_diagram_two_mod




if __name__ == '__main__':
  x_0 = Ternary_tree_diagrams(['00', '01', '02', '1', '2'], ['0', '1', '20', '21', '22'])
  x_1 = Ternary_tree_diagrams(['0', '10', '11', '12', '2'], ['0', '1', '20', '21', '22'])
  x_2 = right_shift_homomorphism(x_0)

  x_0inv = x_0.inverse_tree_diagram()
  x_1inv = x_1.inverse_tree_diagram()
  x_2inv = x_2.inverse_tree_diagram()

  product = multiplication_tree_diagrams(x_0, x_2)
  print("product")
  product.print_tree_diagram()
  print("normal form:", find_normal_form(x_0))
  print("normal form:", find_normal_form(x_0inv))
  print("normal form:", find_normal_form(x_1))
  print("normal form:", find_normal_form(x_1inv))
  print("normal form:", find_normal_form(x_2))
  print("normal form:", find_normal_form(x_2inv))

"""
if __name__ == '__main__':
  x_0
  print(from_tree_to_graph(x_0))
  x_0.print_tree_diagram()
"""