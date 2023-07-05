import math
from geometry import Line_3D, Point_3D

class Grid_Lines:
  def __init__(self, distance, colour):
    self.distance = distance
    self.colour = colour # either singular colour, or list of colours for indidivudal axis, in xyz
class Floor_Grid_Lines:
  def __init__(self, distance, colour):
    self.distance = distance
    self.colour = colour # either singular colour, or list of colours for individual axis in xz