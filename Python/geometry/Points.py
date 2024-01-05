from math import sqrt

# Point Objects
class Point_2D:
  def __init__(self, x, y):
    self.x = round(x, 16)
    self.y = round(y, 16)

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x + value.x, self.y + value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x + value[0], self.y + value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x + value, self.y + value)
    
  def __radd__(self, value):
    return self.__add__(value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x - value.x, self.y - value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x - value[0], self.y - value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x - value, self.y - value)
    
  def __rsub__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
        return Point_2D(value.x - self.x, value.y - self.y)
    elif isinstance(value, (list, tuple)):
        return Point_2D(value[0] - self.x, value[1] - self.y)
    elif isinstance(value, (float, int)):
        return Point_2D(value - self.x, value - self.y)
  
  def __mul__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x * value.x, self.y * value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x * value[0], self.y * value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x * value, self.y * value)
    
  def __rmul__(self, value):
    return self.__mul__(value)
  
  def __truediv__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x / value.x, self.y / value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x / value[0], self.y / value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x / value, self.y / value)
    
  def __rtruediv__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
        return Point_2D(value.x / self.x, value.y / self.y)
    elif isinstance(value, (list, tuple)):
        return Point_2D(value[0] / self.x, value[1] / self.y)
    elif isinstance(value, (float, int)):
        return Point_2D(value / self.x, value / self.y)
    
  def __mod__(self, other):
    return Point_2D(self.x % other, self.y % other)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y
    
  def to_list(self):
    return (self.x,self.y)
  
  def to_vector(self):
    return Vector_2D(self.x, self.y)
  
  def output(self):
    print(f'Point 2D : ({self.x}, {self.y})')
  
  def __str__(self):
    return f'({self.x}, {self.y})'


class Point_3D:
  def __init__(self, x, y, z):
    self.x = round(x, 16)
    self.y = round(y, 16)
    self.z = round(z, 16)

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x + value.x, self.y + value.y, self.z + value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x + value[0], self.y + value[1], self.z + value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x + value, self.y + value, self.z + value)
    
  def __radd__(self, value):
    return self.__radd__(value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x - value.x, self.y - value.y, self.z - value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x - value[0], self.y - value[1], self.z - value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x - value, self.y - value, self.z - value)
    
  def __rsub__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(value.x - self.x, value.y - self.y, value.z - self.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(value[0] - self.x, value[1] - self.y, value[2] - self.z)
    elif isinstance(value, (float, int)):
      return Point_3D(value - self.x, value - self.y, value - self.z)
  
  def __mul__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x * value.x, self.y * value.y, self.z * value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x * value[0], self.y * value[1], self.z * value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x * value, self.y * value, self.z * value)

  def __rmul__(self, value):
    return self.__mul__(value)
    
  def __truediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x / value.x, self.y / value.y, self.z / value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x / value[0], self.y / value[1], self.z / value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x / value, self.y / value, self.z / value)
    
  def __rtruediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(value.x / self.x, value.y / self.y, value.z / self.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(value[0] / self.x, value[1] / self.y, value[2] / self.z)
    elif isinstance(value, (float, int)):
      return Point_3D(value / self.x, value / self.y, value / self.z)
    
  def __mod__(self, other):
    return Point_3D(self.x % other, self.y % other, self.z % other)
  
  def __repr__(self):
    return f'({round(self.x,2)}, {round(self.y,2)}, {round(self.z,2)})'
  def __str__(self):
    return f'({round(self.x,2)}, {round(self.y,2)}, {round(self.z,2)})'
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y + self.z * other.z
  
  def dist(self, other):
    return sqrt(abs((self.x-other.x)**2 + (self.y-other.y)**2 + (self.z-other.z)**2))
    
  def to_list(self):
    return (self.x,self.y,self.z)
  
  def to_vector(self):
    return Vector_3D(self.x, self.y, self.z)
  
  def output(self):
    print(f'Point 3D : ({self.x}, {self.y}, {self.z})')
  
  def __str__(self):
    return f'({self.x}, {self.y}, {self.z})' 

  



# Vector Objects
class Vector_2D:
  def __init__(self, x, y):
    self.x = round(x, 16)
    self.y = round(y, 16)
  
  def normalise(self):
    mag = sqrt(self.x**2 + self.y**2)
    if mag:
      return Vector_2D(self.x / mag, self.y / mag)
    else:
      return Vector_2D(0,0,0)
    
  def __add__(self, value): # method to add points
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x + value.x, self.y + value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x + value[0], self.y + value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x + value, self.y + value)
    
  def __radd__(self, value):
    return self.__add__(value)

  def __rsub__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
        return Point_2D(value.x - self.x, value.y - self.y)
    elif isinstance(value, (list, tuple)):
        return Point_2D(value[0] - self.x, value[1] - self.y)
    elif isinstance(value, (float, int)):
        return Point_2D(value - self.x, value - self.y)
  
  def __mul__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x * value.x, self.y * value.y)
    elif isinstance(value, (list, tuple)):
      return Point_2D(self.x * value[0], self.y * value[1])
    elif isinstance(value, (float, int)):
      return Point_2D(self.x * value, self.y * value)
    
  def __rmul__(self, value):
    return self.__mul__(value)
  
  def __rtruediv__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
        return Point_2D(value.x / self.x, value.y / self.y)
    elif isinstance(value, (list, tuple)):
        return Point_2D(value[0] / self.x, value[1] / self.y)
    elif isinstance(value, (float, int)):
        return Point_2D(value / self.x, value / self.y)
    
  def __mod__(self, other):
    return Vector_2D(self.x % other, self.y % other)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y
  
  def to_list(self):
    return (self.x,self.y)
  
  def norm_to_list(self):
    return (self.x_norm,self.y_norm)
  
  def inverse(self):
    return [-self.x,-self.y]
  
  def output(self):
    print(f'Vector 2D : ({self.x}, {self.y})')
  def __str__(self):
    return f'({self.x}, {self.y})'

class Vector_3D:
  def __init__(self, x, y, z):
    self.x = round(x, 16)
    self.y = round(y, 16)
    self.z = round(z, 16)

  def normalise(self):
    mag = sqrt(self.x**2 + self.y**2 + self.z**2)
    if mag:
      return Vector_3D(self.x / mag, self.y / mag, self.z / mag)
    else:
      return Vector_3D(0,0,0)

  def __add__(self, value): # method to add points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x + value.x, self.y + value.y, self.z + value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x + value[0], self.y + value[1], self.z + value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x + value, self.y + value, self.z + value)
    
  def __radd__(self, value):
    return self.__add__(value)

  def __sub__(self, value): # method to subtract points
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x - value.x, self.y - value.y, self.z - value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x - value[0], self.y - value[1], self.z - value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x - value, self.y - value, self.z - value)
    
  def __rsub__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(value.x - self.x, value.y - self.y, value.z - self.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(value[0] - self.x, value[1] - self.y, value[2] - self.z)
    elif isinstance(value, (float, int)):
      return Point_3D(value - self.x, value - self.y, value - self.z)
  
  def __mul__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x * value.x, self.y * value.y, self.z * value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x * value[0], self.y * value[1], self.z * value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x * value, self.y * value, self.z * value)
    
  def __rmul__(self, value):
    return self.__mul__(value)
    
  def __truediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(self.x / value.x, self.y / value.y, self.z / value.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(self.x / value[0], self.y / value[1], self.z / value[2])
    elif isinstance(value, (float, int)):
      return Point_3D(self.x / value, self.y / value, self.z / value)
  
  def __rtruediv__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
      return Point_3D(value.x / self.x, value.y / self.y, value.z / self.z)
    elif isinstance(value, (list, tuple)):
      return Point_3D(value[0] / self.x, value[1] / self.y, value[2] / self.z)
    elif isinstance(value, (float, int)):
      return Point_3D(value / self.x, value / self.y, value / self.z)
    
  def __mod__(self, other):
    return Vector_2D(self.x % other, self.y % other, self.z % other)
    
  def dot(self, other):
    return self.x * other.x + self.y * other.y + self.z * other.z
  
  def to_list(self):
    return (self.x,self.y,self.z)
  
  def inverse(self):
    return Vector_3D(-self.x,-self.y,-self.z)
  
  def output(self):
    print(f'Vector 3D : ({self.x}, {self.y}, {self.z})')

  def __str__(self):
    return f'({self.x}, {self.y}, {self.z})'