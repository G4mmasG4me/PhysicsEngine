from geometry import Point_3D, Vector_3D, Point_2D
from geometry import Line_3D, Ray_3D, Segment_3D
from surface_properties import Colour
from surface_properties import Texture, default_texture
from math import pi, atan2, asin
from object_intersections import line_sphere_intersection
from functions import clamp

from config import epsilon
class SkyBox:
  def __init__(self, center, radius, texture):
    self.center = center
    self.radius = radius
    self.texture = texture

  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)): # Line intersection
      # convert line to object space
      line = self.object_space(line)
      intersections = line_sphere_intersection(line, self)
      intersection_output = [[intersection_point, intersection_point.to_vector()] for intersection_point, _ in intersections] # generate 
      intersections = []
      for intersection_point, intersection_normal in intersection_output:
        distance = line.p1.dist(intersection_point)
        world_intersection_point = self.world_space(intersection_point)
        world_intersection_normal = self.world_space(intersection_normal).normalise()
        # gets colour
        if isinstance(self.texture, Colour):
          colour = self.texture
        elif isinstance(self.texture, Texture):
          uv = self.get_uv_pos(intersection_point)
          colour = self.texture.get_colour(uv)

        elif isinstance(self.texture, None): # returns default
          uv = self.get_uv_pos(intersection_point, default_texture.img_size, default_texture.texture_scale)

        intersections.append({'intersection':world_intersection_point, 'normal':world_intersection_normal, 'distance':distance, 'colour':colour, 'obj':self})
      return intersections # even if no intersections returns empty list, as it automatically gets added anyway
    return None
  
  def get_uv_pos(self, pos):
    pos = pos.to_vector().normalise()
    u = clamp((atan2(pos.z,pos.x)/(pi) + 1) * 0.5, 0, 1)
    v = clamp(0.5 - asin(pos.y)/pi, 0, 1)
    return Point_2D(u, 1-v) # flip y, as image measures from top down, whereas env is bottom up


  def object_space(self, obj):
    if isinstance(obj, Point_3D):
      # translate
      translated_point = obj - self.center
      return translated_point

    elif isinstance(obj, Vector_3D):
      # rotate direction
      return obj
    
    elif isinstance(obj, Line_3D):
      # translate point
      translated_point = obj.p1 - self.center

      # return object space line
      return Line_3D(translated_point, obj.dir)

    elif isinstance(obj, Ray_3D):
      # translate point
      translated_point = obj.p1 - self.center

      # return object space line
      return Ray_3D(translated_point, obj.dir)

    elif isinstance(obj, Segment_3D):
      # translate points
      translated_point_1 = obj.p1 - self.center
      translated_point_2 = obj.p2 - self.center

      # return object space line
      return Segment_3D(translated_point_1, translated_point_2)
  
  # convert a point, vector or line from object space back to world space
  def world_space(self, obj):
    if isinstance(obj, Point_3D):
      # translate
      final_point = obj + self.center
      return final_point

    elif isinstance(obj, Vector_3D):
      return obj
    
    elif isinstance(obj, Line_3D):
      # translate
      final_point = obj.p1 + self.center

      # return object space line
      return Line_3D(final_point, obj.dir)

    elif isinstance(obj, Ray_3D):
      # translated point
      final_point = obj.p1 + self.center

      # return object space line
      return Ray_3D(final_point, obj.dir)

    elif isinstance(obj, Segment_3D):
      # translate point
      final_point_1 = obj.p1 + self.center
      final_point_2 = obj.p2 + self.center

      # return object space line
      return Segment_3D(final_point_1, final_point_2)
    
  def camera_space(self, camera):
      # translate position
      translated_position = self.center - camera.position

      return SkyBox(translated_position, self.radius, self.texture)