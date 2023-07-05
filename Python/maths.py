import math
import numpy as np
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from Planes import Plane, Plane_Polygon
import matrix as matrix

def rotation_matrix_to_axis_angle(R):
  # Convert the rotation matrix to axis-angle representation
  alpha = np.arccos((np.trace(R) - 1) / 2)
  r = 1 / (2 * np.sin(alpha)) * np.array([R[2, 1] - R[1, 2],
                                            R[0, 2] - R[2, 0],
                                            R[1, 0] - R[0, 1]])
  return r, alpha

def euler_to_axis_angle(angle):
  phi, theta, psi = angle.to_list()
  R_x = np.array([[1, 0, 0],
                  [0, np.cos(phi), -np.sin(phi)],
                  [0, np.sin(phi), np.cos(phi)]])

  R_y = np.array([[np.cos(theta), 0, np.sin(theta)],
                  [0, 1, 0],
                  [-np.sin(theta), 0, np.cos(theta)]])

  R_z = np.array([[np.cos(psi), -np.sin(psi), 0],
                  [np.sin(psi), np.cos(psi), 0],
                  [0, 0, 1]])
  
  r = np.dot([1,0,0], np.dot(R_z, np.dot(R_y, R_x)))

  return r



def between_points_2d(point1, point2):
  return Point_2D((point1.x + point2.x)/2, (point1.y + point2.y)/2)


def between_points_3d(point1, point2):
  return Point_3D((point1.x + point2.x)/2, (point1.y + point2.y)/2, (point1.z + point2.z)/2)

def list_type(my_list):
  objs = [] # objects in list
  for i in my_list:
    list_obj = type(i).__name__
    if list_obj not in objs:
      objs.append(list_obj)
  
  # sort list and return
  return sorted(objs, key=str.lower)




def rotate_plane_points(points, target_plane):
  points_plane = Plane(*points)
  # Calculate the rotation axis
  rotation_axis = np.cross(points_plane.normals_list(), target_plane.normals_list())
  if not all(element == 0 for element in rotation_axis):
    
    rotation_axis /= np.linalg.norm(rotation_axis)

    # Calculate the rotation angle
    rotation_angle = np.arccos(np.dot(points_plane.normals_list(), target_plane.normals_list()))
    # Generate the rotation matrix
    rotation_matrix = matrix.axis_angle_rotation_matrix(rotation_axis, rotation_angle)

    # Rotate the points
    points = np.array([point.to_list() for point in points])
    rotated_points = [Point_3D(*rotation_matrix.dot(point)) for point in points]

    return rotated_points
  else:
    return points
