from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from Texture import Texture, default_texture
from Material import Material, Material_Map, default_material

from Colour import Colour
from matrix import xyz_matrix, inverse_matrix

epsilon = 0.01
class Object:
  def __init__(self, geometry, position, rotation, scale, velocity, angular_velocity, mass, material, texture, collider, refractive_index):
    self.geometry = geometry
    self.position = position
    self.rotation = rotation
    self.scale = scale
    self.velocity = velocity
    self.angular_velocity = angular_velocity
    self.mass = mass
    
    self.material = material # either material object, or uv map material object
    self.texture = texture # either colour object or uv map colour object
    self.collider = collider
    self.refractive_index = 1.1

    self.rotation_matrix = xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = inverse_matrix(self.rotation_matrix)


  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)): # Line intersection
      # convert line to object space
      line = self.object_space(line)
      intersection_output = self.geometry.intersection(line)
      intersections = []
      for intersection_point, intersection_normal in intersection_output:
        distance = line.p1.dist(intersection_point)
        if distance > epsilon:
          world_intersection_point = self.world_space(intersection_point)
          world_intersection_normal = self.world_space(intersection_normal).normalise()
          
          # gets colour
          if isinstance(self.texture, Colour):
            colour = self.texture
          elif isinstance(self.texture, Texture):
            
            uv = self.geometry.get_uv_pos(intersection_point, self.texture.img_size, self.texture.texture_scale)
            
            colour = self.texture.get_colour(uv)
          elif isinstance(self.texture, None): # returns default
            uv = self.geometry.get_uv_pos(intersection_point, default_texture.img_size, default_texture.texture_scale)
           
          if isinstance(self.material, Material):
            material = self.material
          elif isinstance(self.material, Material_Map):
             uv = self.geometry.get_uv_pos(intersection_point, self.material.uv_map_size, self.material.material_scale)
             material = self.material.get_material(uv)
          elif isinstance(self.material, None): # returns default
            material = default_material

          intersections.append([world_intersection_point, world_intersection_normal, distance, colour, material, self.refractive_index, self])
      return intersections # even if no intersections returns empty list, as it automatically gets added anyway
    return None
  
  # also need to check for material as material at certain points will or wont allow reflections
  def one_bounce_intersection(self, light, object_intersection):
    light_pos = self.object_space(light.position)
    intersection_pos = self.object_space(object_intersection)
    reflection_positions = self.geometry.one_bounce_intersetion(light_pos, intersection_pos)

    # check that no intersections segment between light pos and reflection pos and segment between intersection and reflection pos
    # segment between light pos and reflection pos
    reflection_positions = [reflection_pos for reflection_pos in reflection_positions if (not self.intersection(Segment_3D(reflection_pos, light_pos)) and not self.intersection(Segment_3D(reflection_pos, intersection_pos)))]
    return reflection_positions
    
  # convert a point, vector or line into object space
  def object_space(self, obj):
    if isinstance(obj, Point_3D):
      # translate
      translated_point = obj - self.position

      # rotate and return
      return Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

    elif isinstance(obj, Vector_3D):
      # rotate direction
      return Vector_3D(*self.inverse_rotation_matrix.dot([obj.x, obj.y, obj.z]))
    
    elif isinstance(obj, Line_3D):
      # translate point
      translated_point = obj.p1 - self.position
      
      # rotate point
      final_point = Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

      # rotate direction
      final_direction = Vector_3D(*self.inverse_rotation_matrix.dot([obj.dir.x, obj.dir.y, obj.dir.z]))

      # return object space line
      return Line_3D(final_point, final_direction)

    elif isinstance(obj, Ray_3D):
      # translate point
      translated_point = obj.p1 - self.position
      
      # rotate point
      final_point = Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

      # rotate direction
      final_direction = Vector_3D(*self.inverse_rotation_matrix.dot([obj.dir.x, obj.dir.y, obj.dir.z]))

      # return object space line
      return Ray_3D(final_point, final_direction)

    elif isinstance(obj, Segment_3D):
      # translate points
      translated_point_1 = obj.p1 - self.position
      translated_point_2 = obj.p2 - self.position
      
      # rotate points
      final_point_1 = Point_3D(*self.inverse_rotation_matrix.dot([translated_point_1.x, translated_point_1.y, translated_point_1.z]))
      final_point_2 = Point_3D(*self.inverse_rotation_matrix.dot([translated_point_2.x, translated_point_2.y, translated_point_2.z]))

      # return object space line
      return Segment_3D(final_point_1, final_point_2)
  
  # convert a point, vector or line from object space back to world space
  def world_space(self, obj):
    if isinstance(obj, Point_3D):
      # rotate
      rotated_point = Point_3D(*self.rotation_matrix.dot([obj.x, obj.y, obj.z]))

      # translate
      final_point = rotated_point + self.position

      return final_point


    elif isinstance(obj, Vector_3D):
      return Vector_3D(*self.rotation_matrix.dot([obj.x, obj.y, obj.z]))
    elif isinstance(obj, Line_3D):
      # rotate point
      rotated_point = Point_3D(*self.rotation_matrix.dot([obj.p1.x, obj.p1.y, obj.p1.z]))

      # translate
      final_point = rotated_point + self.position

      # rotate direction
      final_direction = Vector_3D(*self.rotation_matrix.dot([obj.dir.x, obj.dir.y, obj.dir.z]))

      # return object space line
      return Line_3D(final_point, final_direction)

    elif isinstance(obj, Ray_3D):
      # rotate point
      rotated_point = Point_3D(*self.rotation_matrix.dot([obj.p1.x, obj.p1.y, obj.p1.z]))

      # translated point
      final_point = rotated_point + self.position

      # rotate direction
      final_direction = Vector_3D(*self.rotation_matrix.dot([obj.dir.x, obj.dir.y, obj.dir.z]))

      # return object space line
      return Ray_3D(final_point, final_direction)

    elif isinstance(obj, Segment_3D):
      

      # rotate points
      rotated_point_1 = Point_3D(*self.rotation_matrix.dot([obj.p1.x, obj.p1.y, obj.p1.z]))
      rotated_point_2 = Point_3D(*self.rotation_matrix.dot([obj.p2.x, obj.p2.y, obj.p2.z]))

      # translate point
      final_point_1 = rotated_point_1 + self.position
      final_point_2 = rotated_point_2 + self.position

      # return object space line
      return Segment_3D(final_point_1, final_point_2)

  # convert a point, vector or line from its space to camera space
  def camera_space(self, camera):
    # translate position
    translated_position = self.position - camera.position


    # rotate position
    rotated_position = Point_3D(*camera.inverse_rotation_matrix.dot([translated_position.x, translated_position.y, translated_position.z]))


    # rotate rotation
    rotate_rotation = self.rotation - camera.rotation

    return Object(self.geometry, rotated_position, rotate_rotation, self.scale, self.velocity, self.angular_velocity, self.mass, self.material, self.texture, self.collider, self.refractive_index)