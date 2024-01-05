import sys
import os
from pathlib import Path


# add parent directory to path
parent_path = str(Path(__file__).parent.resolve().parent.resolve())
sys.path.insert(0, parent_path)

# import Points
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D

def are_equal(val1, val2):
  return val1 == val2

def add_case(parameters, expected):
  p1, p2 = parameters
  value = p1 + p2
  return are_equal(value, expected), value

# test cases to run
cases = [
  add_case, # add 2D point ints
  add_case, # add 2D points floats
  add_case, # add 2D points negatives
  add_case, # add 3D points ints
  add_case, # add 3D points floats
  add_case, # add 3D points floats
]
parameters = [
  [Point_2D(10,5), Point_2D(5,10)], # ints
  [Point_2D(10,5), Point_2D(-5,-10)], # mixed
  [Point_2D(-1,-4), Point_2D(-4,-2)], # negatives
  [Point_2D(1.1,4.4), Point_2D(4.4,2.2)], # floats
  [Point_2D(-1.1,-4.4), Point_2D(4.4,2.2)], # mixed floats
  [Point_2D(-1.1,-4.4), Point_2D(-4.4,-2.2)], # negative floats
  [Point_2D(0,0), Point_2D(0,0)], # zeros
  [Point_2D(5,0), Point_2D(0,4)], # mixed zeros

]
expecteds = [
  Point_2D(15,15), # ints
  Point_2D(-5,5), # mixed
  Point_2D(-5,-6), # negatives
  Point_2D(5.5,6.6), # floats
  Point_2D(3.3,-2.2), # mixed floats
  Point_2D(-5.5,-6.6), # negative floats
  Point_2D(0,0), # zeros
  Point_2D(5,4), # mixed zeros
]
# name, function, parameters, expected
cases = [
  ['Add 2D Points Positive Ints', add_case, [[Point_2D, (10,5)], [Point_2D, (5,10)]], Point_2D(15,15)],
  ['Add 2D Points Mixed Ints', add_case, [[Point_2D, (10,5)], [Point_2D, (-5,-10)]], Point_2D(5,-5)],
  ['Add 2D Points Negative Ints', add_case, [[Point_2D, (-1,-4)], [Point_2D, (-4,-2)]], Point_2D(-5,-6)],
  ['Add 2D Points Positive Floats', add_case, [[Point_2D, (1.1,4.4)], [Point_2D, (4.4,2.2)]], Point_2D(5.5,6.6)],
  ['Add 2D Points Mixed Floats', add_case, [[Point_2D, (-1.1,-4.4)], [Point_2D, (4.4,2.2)]], Point_2D(3.3,-2.2)],
  ['Add 2D Points Negative Floats', add_case, [[Point_2D, (-1.1,-4.4)], [Point_2D, (-4.4,-2.2)]], Point_2D(-5.5,-6.6)],
  ['Add 2D Points Zeros Ints', add_case, [[Point_2D, (0,0)], [Point_2D, (0,0)]], Point_2D(0,0)],
  ['Add 2D Points Mixed Zeros Ints', add_case, [[Point_2D, (5,0)], [Point_2D, (0,4)]], Point_2D(5,4)],
  ['Add 2D Points String', add_case, [[Point_2D, ('str', 'hello')], [Point_2D, (0,0)]], ValueError]
]

if __name__ == '__main__':
  for idx, (name, case, params, expected) in enumerate(cases):
    try:
      params = [val_class(*vals) for val_class, vals in params]
      has_passed, actual_value = case(params, expected)
    except ValueError:
      actual_value = ValueError
      has_passed = are_equal(actual_value, expected)
      

    if has_passed:
      print(f'Case Num: {idx} | Case Name: {name} | Function Name: {case.__name__} | Pass: {has_passed}')
    else:
      print(f'Case Num: {idx} | {case.__name__} | Pass: {has_passed} | Expected: {expected} | Actual: {actual_value}')