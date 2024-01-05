from PIL import Image
from surface_properties import Colour
from geometry import Point_2D

class Texture:
  def __init__(self, img_path, texture_scale=1):
    self.img_path = img_path
    self.img = Image.open(img_path)
    self.img_size = self.img.size
    self.texture_scale = texture_scale # used for Infinite textures. px/m 

  def get_colour(self, pos, type='wrapping'): # either clamping or wrapping
    pos = Point_2D(pos.x, pos.y)
    if type == 'clamping':
      if 0 > pos.x > 1 or 0 > pos.y > 1:
        return Colour((0,0,0))
    elif type == 'wrapping':
      pos = pos % 1
    relative_pos = pos * self.img_size
    return Colour(self.img.getpixel(relative_pos.to_list()), self.img.mode)
  
# texture_scale of 1 | 1m = 1pixel from texture
# texture_scale of 10 | 1m = 10 pixels from texture
default_texture = Texture('textures/default.png', 1)
chessboard_1 = Texture('textures/chessboard_1.png')
chessboard_2 = Texture('textures/chessboard_2.png')
chessboard_3 = Texture('textures/chessboard_3.png')
bricks = Texture('textures/brick.jpg', 100)
sky = Texture('textures/sky.jpg')