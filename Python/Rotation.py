from math import pi

class Rotation_3D:
  def __init__(self, x, y, z):
    self.x = x
    self.y = y
    self.z = z

  def to_list(self):
    return [self.x.angle, self.y.angle, self.z.angle]
  
  def __sub__(self, other):
    return Rotation_3D(self.x - other.x, self.y - other.y, self.z - other.z)


class Rotation:
  def __init__(self, angle, unit='rad'):
    # stores angle in radians
    if unit in ['deg', 'degree', 'degrees']:
      self.angle = angle * (pi / 180) # measured in radians
    elif unit in ['rad', 'radian', 'radians']:
      self.angle = angle
    
    self.deg, self.degrees = self.degree, self.degree
    self.rad, self.radians = self.radian, self.radian
  def degree(self):
    return self.angle * (180 / pi)
  def radian(self):
    return self.angle
  
  def __add__(self, angle):
    return Rotation(self.angle + angle.angle, unit='rad')
  def __sub__(self, angle):
    return Rotation(self.angle - angle.angle, unit='rad')

  