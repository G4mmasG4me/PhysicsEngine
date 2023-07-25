import math

def clamp(n, minn, maxn):
  try:
    return max(min(maxn, n), minn)
  except Exception as e:
    print(f'Error: {e}')
    print(f'N: {n}')
    print(f'Is NaN: {math.isnan(n)}')
    quit()