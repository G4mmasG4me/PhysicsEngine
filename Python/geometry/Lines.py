from geometry import Point_2D, Point_3D, Vector_2D, Vector_3D


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
  
  def along_line(self, t):
    return True
  
  def output(self):
    print(f'Point: ({self.p1.x}, {self.p1.y}) | Direction: ({self.dir.x}, {self.dir.y})')

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
  
  def along_line(self, t):
    return True
  
  def output(self):
    print(f'Point: ({self.p1.x}, {self.p1.y}, {self.p1.z}) | Direction: ({self.dir.x}, {self.dir.y}, {self.dir.z})')

class Ray_2D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_2D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_2D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd
    
  def along_line(self, t):
    if t >= 0:
      return True
    else:
      return False
    
  def inverse(self):
    return Ray_2D(self.p1, self.dir.inverse())
    
  def output(self):
    print(f'Point: ({self.p1.x}, {self.p1.y}) | Direction: ({self.dir.x}, {self.dir.y})')

class Ray_3D:
  def __init__(self, point1, pd):
    self.p1 = point1
    if isinstance(pd, Point_3D): # if second value is a point
      self.p2 = pd
      self.dir = point_to_vector(pd - point1)
    elif isinstance(pd, Vector_3D): # if second value is a direction
      self.dir = pd
      self.p2 = point1 + pd
    else:
      print(pd)
      raise ValueError('Invalid Input')
      
    
  def along_line(self, t):
    if t >= 0:
      return True
    else:
      return False
    
  def inverse(self):
    return Ray_3D(self.p1, self.dir.inverse())
  
  def __str__(self):
    return f'Ray 3D | Point: ({self.p1.x}, {self.p1.y}, {self.p1.z}) | Direction: ({self.dir.x}, {self.dir.y}, {self.dir.z})'
    
  def output(self):
    print(f'Point: ({self.p1.x}, {self.p1.y}, {self.p1.z}) | Direction: ({self.dir.x}, {self.dir.y}, {self.dir.z})')
  
  def to_line(self):
    return Line_3D(self.p1, self.dir)

  
class Segment_2D:
  def __init__(self, point1, point2):
    self.p1 = point1
    self.p2 = point2
    self.dir = (point2 - point1).to_vector()

  def along_line(self, t):
    if 0 <= t <= 1:
      return True
    else:
      return False
    
  def output(self):
    print(f'Point 1: ({self.p1.x}, {self.p1.y}) | Point 2: ({self.p2.x}, {self.p2.y})')

class Segment_3D:
  def __init__(self, point1, point2):
    self.p1 = point1
    self.p2 = point2
    self.dir = (point2 - point1).to_vector()

  def along_line(self, t):
    if 0 <= t <= 1:
      return True
    else:
      return False
    
  def output(self):
    print(f'Point 1: ({self.p1.x}, {self.p1.y}, {self.p1.z}) | Point 2: ({self.p2.x}, {self.p2.y}, {self.p2.z})')

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