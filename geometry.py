import math

class Plane_Polygon:
  def __init__(self, points):
    self.points = points
    self.plane = Plane(*points)



class Plane:
  def __init__(self, *elements):
    if len(elements) == 4 and all(isinstance(value, (int, float)) for value in elements): 
      self.a, self.b, self.c, self.d = elements

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

      # normalize coefficients
      mag = math.sqrt(normal_vector[0]**2 + normal_vector[1]**2 + normal_vector[2]**2)
      self.a = normal_vector[0] / mag
      self.b = normal_vector[1] / mag
      self.c = normal_vector[2] / mag
      self.d = d / mag

  def normals_list(self):
    return [self.a, self.b, self.c]
  
  def line_intersect(line):
    pass

class Ray_2D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_2D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_2D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd

class Ray_3D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_3D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_3D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd
# Point Objects
class Point_2D:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x + value.x, self.y + value.y)
    elif isinstance(value, list):
      return Point_2D(self.x + value[0], self.y + value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x + value, self.y + value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x - value.x, self.y - value.y)
    elif isinstance(value, list):
      return Point_2D(self.x - value[0], self.y - value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x - value, self.y - value)
  
  def __mul__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x * value.x, self.y * value.y)
    elif isinstance(value, list):
      return Point_2D(self.x * value[0], self.y * value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x * value, self.y * value)
  
  def __truediv__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x / value.x, self.y / value.y)
    elif isinstance(value, list):
      return Point_2D(self.x / value[0], self.y / value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x / value, self.y / value)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y
    
  def to_list(self):
    return [self.x,self.y]


class Point_3D:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x + value.x, self.y + value.y, self.z + value.z)
    elif isinstance(value, list):
      return Point_3D(self.x + value[0], self.y + value[1], self.z + value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x + value, self.y + value, self.z + value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x - value.x, self.y - value.y, self.z - value.z)
    elif isinstance(value, list):
      return Point_3D(self.x - value[0], self.y - value[1], self.z - value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x - value, self.y - value, self.z - value)
  
  def __mul__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x * value.x, self.y * value.y, self.z * value.z)
    elif isinstance(value, list):
      return Point_3D(self.x * value[0], self.y * value[1], self.z * value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x * value, self.y * value, self.z * value)
    
  def __truediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x / value.x, self.y / value.y, self.z / value.z)
    elif isinstance(value, list):
      return Point_3D(self.x / value[0], self.y / value[1], self.z / value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x / value, self.y / value, self.z / value)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y + self.z * other.z
  
  def dist(self, other):
    return math.sqrt((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)*2)
    
  def to_list(self):
    return [self.x,self.y,self.z]



# Vector Objects
class Vector_2D:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    mag = math.sqrt(x**2 + y**2)
    if mag:
      self.x_norm = x / mag
      self.y_norm = y / mag
    else:
      self.x_norm = 0
      self.y_norm = 0
    
  def __add__(self, value): # method to add points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x + value.x, self.y + value.y)
    elif isinstance(value, list):
      return Point_2D(self.x + value[0], self.y + value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x + value, self.y + value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x - value.x, self.y - value.y)
    elif isinstance(value, list):
      return Point_2D(self.x - value[0], self.y - value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x - value, self.y - value)
  
  def __mul__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x * value.x, self.y * value.y)
    elif isinstance(value, list):
      return Point_2D(self.x * value[0], self.y * value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x * value, self.y * value)
  
  def __truediv__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x / value.x, self.y / value.y)
    elif isinstance(value, list):
      return Point_2D(self.x / value[0], self.y / value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x / value, self.y / value)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y
  
  def to_list(self):
    return [self.x,self.y]
  
  def norm_to_list(self):
    return [self.x_norm, self.y_norm]

class Vector_3D:
  def __init__(self, x, y, z):
    mag = math.sqrt(x**2 + y**2 + z**2)
    if mag:
      self.x = x / mag
      self.y = y / mag
      self.z = z / mag
    else:
      self.x = 0
      self.y = 0
      self.z = 0

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x + value.x, self.y + value.y, self.z + value.z)
    elif isinstance(value, list):
      return Point_3D(self.x + value[0], self.y + value[1], self.z + value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x + value, self.y + value, self.z + value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x - value.x, self.y - value.y, self.z - value.z)
    elif isinstance(value, list):
      return Point_3D(self.x - value[0], self.y - value[1], self.z - value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x - value, self.y - value, self.z - value)
  
  def __mul__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x * value.x, self.y * value.y, self.z * value.z)
    elif isinstance(value, list):
      return Point_3D(self.x * value[0], self.y * value[1], self.z * value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x * value, self.y * value, self.z * value)
    
  def __truediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x / value.x, self.y / value.y, self.z / value.z)
    elif isinstance(value, list):
      return Point_3D(self.x / value[0], self.y / value[1], self.z / value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x / value, self.y / value, self.z / value)
  def dot(self, other):
    return self.x * other.x + self.y * other.y + self.z * other.z
  
  def to_list(self):
    return [self.x,self.y,self.z]
  
class Line_2D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_2D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_2D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd
    self.A = self.p1.y - self.p2.y
    self.B = self.p1.x - self.p2.x
    self.C = -(self.p1.x * self.p2.y - self.p2.x * self.p1.y)

class Line_3D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_3D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_3D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd
    self.A = self.p1.y - self.p2.y
    self.B = self.p1.x - self.p2.x
    self.C = self.p1.z
    self.C = -(self.p1.x * self.p2.y - self.p2.x * self.p1.y)

class Segment_2D:
  def __init__(self, point1, point2):
    self.p1 = point1
    self.p2 = point2
    self.dir = point2 - point1

class Segment_3D:
  def __init__(self, point1, point2):
    self.p1 = point1
    self.p2 = point2
    self.dir = Vector_3D(*point2 - point1)

def point_to_vector(point):
  if isinstance(point, Point_2D):
    return Vector_2D(point.x, point.y)
  elif isinstance(point, Point_3D):
    return Vector_3D(point.x, point.y, point.z)

def vector_to_point(vector):
  if isinstance(vector, Vector_2D):
    return Point_2D(vector.x, vector.y)
  elif isinstance(vector, Vector_3D):
    return Point_3D(vector.x, vector.y, vector.z)

class Rotation_3D:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

class Rotation:
  def __init__(self, angle, unit='rad'):
    if unit in ['deg', 'degree', 'degrees']:
      self.angle = angle * (math.pi / 180) # measured in radians
    elif unit in ['rad', 'radian', 'radians']:
      self.angle = angle
    
    self.deg, self.degrees = self.degree, self.degree
    self.rad, self.radians = self.radian, self.radian
  def degree(self):
    return self.angle * (180 / math.pi)
  def radian(self):
    return self.angle
  
  def __add__(self, angle):
    return Rotation(self.angle + angle.angle, unit='rad')
  def __sub__(self, angle):
    return Rotation(self.angle - angle.angle, unit='rad')

  