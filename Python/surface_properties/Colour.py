from functions import clamp

# opportunity to add mode to img
class Colour:
  """
  Colour object
  """
  def __init__(self, colour, type='rgb'):
    """
    Initialise colour object
    
    Parameters:
      self
      colour (list, tuple): colour in list format
      type (string): type of colour e.g. 'rgb', 'rgba'
    """
    if type.lower() == 'rgb' or type.lower() == 'rgba':
      self.r = colour[0]
      self.g = colour[1]
      self.b = colour[2]

  def to_list(self):
    """
    Outputs colour object as list
    
    Paramters:
      self
    
    Returns:
      (list): 'rgb' colour in list format between 0 and 255, e.g. [r,g,b] 
    """
    return [self.r,self.g,self.b]
  
  def to_tuple(self):
    """
    Outputs colour object as list
    
    Paramters:
      self
    
    Returns:
      (list): 'rgb' colour in list format between 0 and 255, e.g. (r,g,b)
    """
    return (self.r,self.g,self.b)
  
  def fp_to_list(self):
    """
    Outputs colour object as list
    
    Paramters:
      self
    
    Returns:
      (list): 'rgb' colour in list format between 0 and 1, e.g. [r,g,b] 
    """
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

  def __str__(self):
    return f'({self.r}, {self.g}, {self.b})'
    
  def __rsub__(self, other):
    if isinstance(other, Colour):
      r = int(clamp(round(other.r - self.r), 0, 255))
      g = int(clamp(round(other.g - self.g), 0, 255))
      b = int(clamp(round(other.b - self.b), 0, 255))
      return Colour((r,g,b))
    else:
      return None
    
  def __repr__(self):
    return f'(self.r, self.g, self.b)'
  def __str__(self):
    return f'({self.r}, {self.g}, {self.b})'
    
BLACK = Colour((0,0,0))
WHITE = Colour((255,255,255))
RED = Colour((255,0,0))
GREEN = Colour((0,255,0))
BLUE = Colour((0,0,255))
GREY = Colour((50,50,50))