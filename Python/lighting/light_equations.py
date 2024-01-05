from math import sin, asin, cos, acos, pi, sqrt
from geometry import Point_2D, Point_3D, Vector_2D, Vector_3D
from geometry import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from geometry import Plane
import numpy as np
from intersections import line_plane_intersect, line_polygon_intersection

def incidence_angle(incidence_ray, normal):
  incidence_direction = incidence_ray.dir.normalise()
  surface_normal_direction = normal.normalise()
  incidence_angle = acos(incidence_direction.dot(surface_normal_direction))
  return incidence_angle

def refracted_ray_dir(incidence_ray, surface_normal, refractive_index_1, refractive_index_2):
  incidence_direction = incidence_ray.dir.normalise()
  surface_normal_direction = surface_normal.normalise()

  normals = [surface_normal_direction, surface_normal_direction.inverse()]
  dot_prods = [incidence_direction.dot(normal) for normal in normals]
  normal_dots = zip(normals,dot_prods)

  # returns second position in list, used for key instead of lambda
  def func1(x):
    return x[1]
  surface_normal, dot_prod = min(normal_dots, key=func1)

  ratio = refractive_index_1 / refractive_index_2
  D = 1 - (ratio**2) * (1 - (dot_prod**2))
  if D >= 0: # if refraction, if lower than 0 there is no pass through

    refracted_direction = (ratio * incidence_direction) - (surface_normal * (ratio * dot_prod + sqrt(D)))
    return refracted_direction.to_vector()
  return None

def reflection_angle(incidence_ray, surface_normal):
  incidence_direction = incidence_ray.dir.normalise()
  surface_normal_direction = surface_normal.normalise()
  reflection_angle = acos(incidence_direction.dot(surface_normal_direction))
  return reflection_angle

# returns reflection direction
def reflected_ray_dir(incidence_ray, surface_normal):
  incidence_direction = incidence_ray.dir.normalise()
  surface_normal_direction = surface_normal.normalise()

  normals = [surface_normal_direction, surface_normal_direction.inverse()]
  dot_prods = [incidence_direction.dot(normal) for normal in normals]
  normal_dots = zip(normals,dot_prods)

  def func(x):
    return x[1]
  surface_normal, dot_prod = min(normal_dots, key=func)

  reflection_direction = incidence_direction - 2 * incidence_direction.dot(surface_normal) * surface_normal
  return reflection_direction.to_vector()

def refraction_angle(incidence_ray, surface_normal, refractive_index_1, refractive_index_2):
  incidence_direction = incidence_ray.dir.normalise()
  surface_normal_direction = surface_normal.normalise()
  incidence_angle = acos(incidence_direction.dot(surface_normal_direction))
  refraction_angle = asin((refractive_index_1 / refractive_index_2) * sin(incidence_angle))
  return refraction_angle

def light_intensity_distance(intensity, distance):
  return intensity / (distance ** 2)


# gets the reflection point, when trying to reflect from a point off a plane type to another point
# |  o
# | /
# |< 
# | \
# |  o
def point_of_reflection(point1, point2, plane):
  # get reflected point 2 in plane
  reflected_point2 = reflect_point_plane(point2, plane)
  
  # create segment between point1 and reflected point
  segment = Segment_3D(point1, reflected_point2)

  # check the intersection between the segment and plane
  intersection_output = line_plane_intersect(segment, plane)
  if intersection_output:
    intersection, t = intersection_output
    return intersection
  return None



# gets the reflection point, when trying to reflect from a direction off a plane_type to a point
# |  o
# | /
# |< 
# | \
# |  \
def point_of_reflection_dir(point, direction, plane):
  reflected_point = reflect_point_plane(point, plane)
  ray = Ray_3D(reflected_point, direction.inverse())

  intersection_output = line_plane_intersect(ray, plane)
  if intersection_output:
    intersection, t = intersection_output
    return intersection
  return None


# reflects a point in a plane
def reflect_point_plane(point, plane):
  Px,Py,Pz = point.to_list()
  A,B,C,D = plane.to_list()

  k = (A*Px + B*Py + C*Pz + D) / (A**2 + B**2 + C**2)
  

  reflect_point =  point - 2 * k * plane.normal
  return reflect_point

def ray_inside_outside_detection(ray, object):
  intersections = object.intersection(ray)
  if len(intersections) % 1 == 0: # even | outside object entering
    return 'outside'
  else: # odd | inside object leaving
    return 'inside'

  
if __name__ == '__main__':
  ray = Ray_3D(Point_3D(0,0,0), Point_3D(2.56,15.75,-45.77))
  plane = Vector_3D(2.56,0.75,4.23)
  # reflect = reflect_point(point1, point2, plane)
  refracted_ray = refracted_ray_dir(ray, plane, 1, 1)
  refracted_ray.output()




# Kd - Diffuse Reflection Coefficient
# Ks - Specular Reflection Coefficient
# Ke - Emission Colour
# Ka - Ambient Reflection Coefficient

# Ia_global = Ambient Intensity
# Id_light = Diffuse Intensity
# Is_light = Specular Intensity

# Ambient Light: Ia = Ka * Ia_global
# Diffuse Light: Id = Kd * Id_light * (N.L)
# Specular Light: Is = Ks * Is_light * (R.V)^n
# Emissive Light: Ie = Ke

# Light Colour = [0.8,0.4,0.6]
# Intensity = 0.5
# Light Intensity = [0.4,0.2,0.3]

# Light intensity distance
# IO = Light Intensity
# I = Inteisty at distance
# d = distance
# I = I0 / (d^2)