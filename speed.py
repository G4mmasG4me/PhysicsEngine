import random
import time

def test_1():
  unit = random.choice(['deg', 'degree', 'degrees', 'rad', 'radian', 'radians'])
  if unit == 'deg' or unit == 'degree' or unit == 'degrees':
    pass
  elif unit == 'rad' or unit == 'radian' or unit == 'radians':
    pass

def test_2():
  unit = random.choice(['deg', 'degree', 'degrees', 'rad', 'radian', 'radians'])
  if unit in ['deg', 'degree', 'degrees']:
    pass
  elif unit in ['rad', 'radian', 'radians']:
    pass

runs = 10000000

start = time.time()
for run in range(runs):
  test_1()
print(time.time() - start)

start = time.time()
for run in range(runs):
  test_2()
print(time.time() - start)