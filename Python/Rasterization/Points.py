point_precision = 8 # 16 decimal places

class Point_2D:
  def __init__(self, x, y):
    if isinstance(x, (int, float)) and isinstance(y, (int, float)):

      self.x = round(x, point_precision)
      self.y = round(y, point_precision)
    else:
      raise ValueError()

  def to_list(self):
    return [self.x, self.y]
  
  def to_tuple(self):
    return (self.x, self.y)
  
  def __add__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return Point_2D(self.x + value.x, self.y + value.y)
    elif isinstance(value, (list, tuple)):
      if len(value) == 2:
        return Point_2D(self.x + value[0], self.y + value[1])
      else:
        raise ValueError()
    elif isinstance(value, (float, int)):
      return Point_2D(self.x + value, self.y + value)
    else:
      raise ValueError()
    
  def __eq__(self, value):
    if isinstance(value, (Point_2D, Vector_2D)):
      return self.to_tuple() == value.to_tuple()
    elif isinstance(value, list):
      return self.to_list() == value
    elif isinstance(value, tuple):
      return self.to_tuple() == value
    else:
      raise ValueError()
    
  def __str__(self):
    return f'Point_2D: {self.to_tuple()}'


class Point_3D:
  def __init__(self, x,y,z):
    self.x = round(x, point_precision)
    self.y = (y, point_precision)
    self.z = (z, point_precision)
  def __add__(self, value):
    if isinstance(value, (Point_3D, Vector_3D)):
        return Point_3D(self.x + value.x, self.y + value.y, self.z + value.z)
    elif isinstance(value, (list, tuple)):
      if len(value) == 3:
        return Point_3D(self.x + value[0], self.y + value[1], self.z + value[2])
      else:
        raise ValueError()
    elif isinstance(value, (float, int)):
      return Point_3D(self.x + value, self.y + value, self.z + value)
    else:
      raise ValueError()


class Vector_2D:
  def __init__(self, x, y):
    self.x = round(x, point_precision)
    self.y = round(y, point_precision)

class Vector_3D:
  def __init__(self, x, y, z):
    self.x = round(x, point_precision)
    self.y = round(y, point_precision)
    self.z = round(z, point_precision)