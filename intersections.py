import math
from geometry import Plane, Point_2D, Point_3D, Segment_2D, Segment_3D, Vector_2D, Vector_3D, Line_2D, Line_3D, Ray_2D, Ray_3D, Plane_Polygon
import numpy as np
from maths import rotate_plane_points

def point_in_plane_polygon(point, polygon):
  # combine polygon points and testing point
  points = polygon.points + [point]
  # rotate the points to get them onto the same plane along the z axis
  points = rotate_plane_points(points, Plane(0,0,1,0))

  # remove the z coordinte, making them 2d
  points = [Point_2D(point.x, point.y) for point in points]

  for point in points:
    print(point.x, point.y)

  # seperate the polygon points and testing point
  polygon_points = points[:-1]
  point = points[-1]
  ray = Ray_2D(point, Vector_2D(1,0))
  print(f'Ray [{ray.p1.x}, {ray.p1.y}], [{ray.dir.x}, {ray.dir.y}]')

  count = 0
  n = len(polygon_points)

  for i in range(len(polygon_points)):
    v1 = polygon_points[i]
    v2 = polygon_points[(i + 1) % n]
    print(f'Segment [{v1.x}, {v1.y}], [{v2.x}, {v2.y}]')

    intersection = ray_segment_intersect_2d(ray, Segment_2D(v1, v2))
    if intersection:
      if ((v1.y > point.y) != (v2.y > point.y)):
        count += 1
  print(count)
  return count % 2 == 1

def ray_sphere_intersection(ray, sphere):
  oc = ray.p1 - sphere.position
  
  a = ray.dir.dot(ray.dir)
  b = 2 * ray.dir.dot(oc)
  c = oc.dot(oc) - sphere.radius ** 2

  discriminant = b ** 2 - 4 * a * c
  if discriminant >= 0:

    sqrt_discriminant = math.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)
    if t1 >= 0:
      # Calculate intersection points
      intersection1 = ray.p1 + ray.dir * t1
      intersection2 = ray.p1 + ray.dir * t2

      return intersection1, t1
  return None


def ray_plane_intersection(ray, plane):
  pass

def ray_polygon_intersection(ray, plane_polygon):
  plane = plane_polygon.plane
  intersection = ray_plane_intersection(ray, plane)
  if intersection:
    if point_in_plane_polygon(intersection, plane_polygon): # intersection inside polygon
      return intersection
    else: # intersection not inside polygon
      return None 
  else: # no intersection with plane, so parallel
    return None

def ray_quad_intersection(ray, quad):
  plane = quad.plane
  intersection = ray_plane_intersection(ray, plane)

def ray_triangle_intersection(ray, triangle):
  pass


def line_plane_intersect(line, plane):
  if np.dot([line.dir.x, line.dir.y, line.dir.z], [plane.a,plane.b,plane.c]):
    t = -(plane.a * line.p1.x + plane.b * line.p1.y + plane.c * line.p1.z + plane.d) / (plane.a * line.dir.x + plane.b * line.dir.y + plane.c * line.dir.z)
    return Point_3D(line.p1.x + t * line.dir.x, line.p1.y + t * line.dir.y, line.p1.z + t * line.dir.z)
  return None


# Line - Line Type Intersections
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
    
    # Calculate the intersection point
    x = x1 + t1 * dx1
    y = y1 + t1 * dy1
    
    return Point_2D(x,y), t1, t2
  return None

def line_segment_intersect_2d(line_1, segment):
  # Line AB
  # Segment CD
  line_2 = Line_2D(segment.p1, segment.p2)
  intersection_output = line_line_intersect_2d(line_1, line_2)
  if intersection_output:
    intercept, t1, t2 = intersection_output
    # calculate if intercept is in segment
    if 0 <= t2 <= 1:
      return intercept
  return None
  # find intersection point
  # check whether its between segment

def ray_segment_intersect_2d(ray, segment):
  line_1 = Line_2D(ray.p1, ray.p2)
  line_2 = Line_2D(segment.p1, segment.p2)
  intersection_output = line_line_intersect_2d(line_1, line_2)
  
  if intersection_output:
    intercept, t1, t2 = intersection_output
    print(intercept.x, intercept.y)
    print(t1, t2)
    if t1 >= 0 and 0 <= t2 <= 1:
      return intercept
  return None


