from math import sin, cos, tan, atan, radians
import numpy as np
from geometry import Point_3D

def xyz_matrix(rotation):
  rotation = [radians(angle) for angle in rotation]
  tx,ty,tz = rotation

  sin_tx = sin(tx)
  sin_ty = sin(ty)
  sin_tz = sin(tz)

  cos_tx = cos(tx)
  cos_ty = cos(ty)
  cos_tz = cos(tz)
  
  rotation_matrix = np.array([
    [cos_ty*cos_tz, -cos_ty*sin_tz, sin_ty],
    [cos_tx*sin_tz+sin_tx*sin_tx*cos_tz, cos_tx*cos_tz-sin_tx*sin_ty*sin_tz, -sin_tx*cos_ty],
    [sin_tx*sin_tz-cos_tx*sin_ty*cos_tz, sin_tx*cos_tz+cos_tx*sin_ty*sin_tz, cos_tx*cos_ty]
  ])
  return rotation_matrix

def reverse_xyz_matrix(rotation):
  rotation_matrix = xyz_matrix(rotation)
  return np.linalg.inv(rotation_matrix)

def inverse_matrix(matrix):
  return np.linalg.inv(matrix)

def axis_angle_rotation_matrix(axis, angle):
  c = np.cos(angle)
  s = np.sin(angle)
  t = 1 - c
  x, y, z = axis

  rotation_matrix = np.array([
    [t*x*x + c, t*x*y - z*s, t*x*z + y*s],
    [t*x*y + z*s, t*y*y + c, t*y*z - x*s],
    [t*x*z - y*s, t*y*z + x*s, t*z*z + c]
  ])
  
  return rotation_matrix

def matrix_rotation(rotation_matrix, point, cor=(0,0,0)):
  offset_point = [a - b for a,b in zip(point, cor)]
  rotated_point = rotation_matrix.dot(offset_point)
  final_point = [a + b for a,b in zip(rotated_point, cor)]
  return final_point

def projection_matrix(hFOV, aspect_ratio, near, far):
  vFOV = 2 * atan(tan(hFOV / 2) / aspect_ratio)

  # calculate the frsutum parameters based on the fov
  top = tan(vFOV/2) * near
  bottom = -top

  right = tan(hFOV/2) * near
  # right = aspect_ratio * top
  left = -right

  n, f = near, far
  r, l = right, left
  t, b = top, bottom

  # Construct the projection matrix
  matrix = np.array([
      [(2*n)/(r-l),0,(r+l)/(r-l),0],
      [0,(2*n)/(t-b),(t+b)/(t-b),0],
      [0,0,(f+n)/(n-f),(2*f*n)/(n-f)],
      [0,0,-1,0]
  ])
  return matrix
if __name__ == '__main__':
  matrix = projection_matrix(10, 100)
  point = np.array([0,0,50,1])
  print(np.dot(matrix, point))