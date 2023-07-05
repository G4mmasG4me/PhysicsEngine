from functions import clamp

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# opportunity to add mode to img
class Colour:
  def __init__(self, colour, type='rgb'):
    if type.lower() == 'rgb' or type.lower() == 'rgba':
      self.r = colour[0]
      self.g = colour[1]
      self.b = colour[2]

  def to_list(self):
    return [self.r,self.g,self.b]
  
  def fp_to_list(self):
    return [self.r/255,self.g/255,self.b/255]
  
  def __mul__(self, other):
    if isinstance(other, Colour):
      r = int(clamp(round(self.r * other.r / 255), 0, 255))
      g = int(clamp(round(self.g * other.g / 255), 0, 255))
      b = int(clamp(round(self.b * other.b / 255), 0, 255))
      return Colour((r,g,b))
    elif isinstance(other, (float, int)): # multiply by between 0 and 1
      r = int(clamp(round(self.r * other), 0, 255))
      g = int(clamp(round(self.g * other), 0, 255))
      b = int(clamp(round(self.b * other), 0, 255))
      return Colour((r,g,b))
    else:
      return None
    
  def __rmul__(self, other):
    return self.__mul__(other)
  
  def __add__(self, other):
    if isinstance(other, Colour):
      r = int(clamp(round(self.r + other.r), 0, 255))
      g = int(clamp(round(self.g + other.g), 0, 255))
      b = int(clamp(round(self.b + other.b), 0, 255))
      return Colour((r,g,b))
    else:
      return None
  
  def __radd__(self, other):
    return self.__add__(other)
    
  def __sub__(self, other):
    if isinstance(other, Colour):
      r = int(clamp(round(self.r - other.r), 0, 255))
      g = int(clamp(round(self.g - other.g), 0, 255))
      b = int(clamp(round(self.b - other.b), 0, 255))
      return Colour((r,g,b))
    else:
      return None
    
  def __rsub__(self, other):
    if isinstance(other, Colour):
      r = int(clamp(round(other.r - self.r), 0, 255))
      g = int(clamp(round(other.g - self.g), 0, 255))
      b = int(clamp(round(other.b - self.b), 0, 255))
      return Colour((r,g,b))
    else:
      return None