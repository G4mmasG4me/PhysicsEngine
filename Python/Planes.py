from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from math import sqrt

class Plane_Polygon:
  def __init__(self, points):
    self.points = points
    self.plane = Plane(*points)


class Plane:
  def __init__(self, *elements):
    if len(elements) == 4 and all(isinstance(value, (int, float)) for value in elements): 
      self.a, self.b, self.c, self.d = elements
      self.normal = Vector_3D(self.a,self.b,self.c)

    elif len(elements) >= 3 and all(isinstance(value, Point_3D) for value in elements):
      
      self.bounds = elements
      v1 = [elements[1].x - elements[0].x, elements[1].y - elements[0].y, elements[1].z - elements[0].z]
      v2 = [elements[2].x - elements[0].x, elements[2].y - elements[0].y, elements[2].z - elements[0].z]

      # Calculate the cross product of v1 and v2 to get the normal vector
      normal_vector = [
          (v1[1] * v2[2]) - (v1[2] * v2[1]),
          (v1[2] * v2[0]) - (v1[0] * v2[2]),
          (v1[0] * v2[1]) - (v1[1] * v2[0])
      ]

      # Calculate the value of d
      d = -(normal_vector[0] * elements[0].x + normal_vector[1] * elements[0].y + normal_vector[2] * elements[0].z)

      # normalise coefficients
      mag = sqrt(normal_vector[0]**2 + normal_vector[1]**2 + normal_vector[2]**2)
      self.a = normal_vector[0] / mag
      self.b = normal_vector[1] / mag
      self.c = normal_vector[2] / mag
      self.normal = Vector_3D(self.a,self.b,self.c)
      self.d = d / mag

  def normals_list(self):
    return [self.a, self.b, self.c]
  
  def line_intersect(line):
    pass

  def to_list(self):
    return [self.a,self.b,self.c,self.d]

  def inverse(self):
    return Plane(-self.a, -self.b, -self.c, -self.d)