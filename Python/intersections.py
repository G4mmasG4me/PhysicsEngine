import math
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from Planes import Plane

import numpy as np
from maths import rotate_plane_points

def point_in_plane_polygon(point, polygon):
  # combine polygon points and testing point
  points = polygon.points + [point]
  # rotate the points to get them onto the same plane along the z axis
  points = rotate_plane_points(points, Plane(0,0,1,0))

  # remove the z coordinte, making them 2d
  points = [Point_2D(point.x, point.y) for point in points]

  # seperate the polygon points and testing point
  polygon_points = points[:-1]
  point = points[-1]
  ray = Ray_2D(point, Vector_2D(1,0))

  count = 0
  n = len(polygon_points)

  for i in range(len(polygon_points)):
    v1 = polygon_points[i]
    v2 = polygon_points[(i + 1) % n]

    intersection = line_line_intersect_2d(ray, Segment_2D(v1, v2))
    if intersection:
      if ((v1.y > point.y) != (v2.y > point.y)):
        count += 1
  return count % 2 == 1


def line_polygon_intersection(ray, plane_polygon):
  plane = plane_polygon.plane
  intersection_output = line_plane_intersect(ray, plane)
  if intersection_output:
    intersection, t = intersection_output
    if point_in_plane_polygon(intersection, plane_polygon): # intersection inside polygon
      return intersection_output
    else: # intersection not inside polygon
      return None 
  else: # no intersection with plane, so parallel
    return None

def line_quad_intersection(ray, quad):
  plane_polygon = quad.plane_polygon
  intersection = line_polygon_intersection(ray, plane_polygon)
  return intersection


# Line Type - Plane Intersections
def line_plane_intersect(line, plane):
  if np.dot([line.dir.x, line.dir.y, line.dir.z], [plane.a,plane.b,plane.c]):
    t = -(plane.a * line.p1.x + plane.b * line.p1.y + plane.c * line.p1.z + plane.d) / (plane.a * line.dir.x + plane.b * line.dir.y + plane.c * line.dir.z)
    if line.along_line(t):
      point = line.p1 + t * line.dir
      return point, t
  return []


# Line Type - Line Type Intersections
def line_line_intersect_2d(line_1, line_2):
  x1, y1 = line_1.p1.to_list()
  dx1, dy1 = line_1.dir.to_list()
  x2, y2 = line_2.p1.to_list()
  dx2, dy2 = line_2.dir.to_list()

  cross_product = (dx1 * dy2 - dx2 * dy1)
  if cross_product:
    # Solve the system of equations
    t1 = (dy2 * (x2 - x1) + dx2 * (y1 - y2)) / cross_product
    t2 = (dx1 * (y1 - y2) + dy1 * (x2 - x1)) / cross_product

    
    # check if in the bounds of either line
    if line_1.along_line(t1) and line_2.along_line(t2):
      # Calculate the intersection point
      point = line_1.p1 + t1 * line_1.dir
      return point
      
  return None

