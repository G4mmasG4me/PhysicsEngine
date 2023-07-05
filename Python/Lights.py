import numpy as np
from math import cos
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D

class DirectionalLight:
  def __init__(self, direction, colour, intensity):
    self.direction = direction
    self.colour = colour
    self.intensity = intensity

  def camera_space(self, camera):

    # rotate position
    rotated_direction = Vector_3D(*camera.inverse_rotation_matrix.dot([self.direction.x, self.direction.y, self.direction.z]))

    return DirectionalLight(rotated_direction, self.colour, self.intensity)

class SpotLight:
  def __init__(self, position, direction, angle, colour, intensity, attentuation):
    self.position = position
    self.direction = direction
    self.angle = angle # cone angle
    self.colour = colour
    self.intensity = intensity
    self.attentuation = attentuation

  def facing_direction(self, direction):
    dot_prod = np.dot(self.direction.norm_to_list(), direction.norm_to_list())
    cos_angle = cos(self.angle.radian())
    if dot_prod >= cos_angle:
      return True
    else:
      return False
    
  def camera_space(self, camera):
    # translate position
    translated_position = self.position - camera.position

    # rotate position
    rotated_position = Point_3D(*camera.inverse_rotation_matrix.dot([translated_position.x, translated_position.y, translated_position.z]))

    # rotate rotation
    rotated_direction = Vector_3D(*camera.inverse_rotation_matrix.dot([self.direction.x, self.direction.y, self.direction.z]))

    return SpotLight(rotated_position, rotated_direction, self.angle, self.colour, self.intensity, self.attentuation)

class PointLight:
  def __init__(self, position, colour, intensity, attentuation):
    self.position = position
    self.colour = colour
    self.intensity = intensity
    self.attentuation = attentuation

  def camera_space(self, camera):
    # translate position
    translated_position = self.position - camera.position

    # rotate position
    rotated_position = Point_3D(*camera.inverse_rotation_matrix.dot([translated_position.x, translated_position.y, translated_position.z]))

    return PointLight(rotated_position, self.colour, self.intensity, self.attentuation)

class AmbientLight:
  def __init__(self, colour, intensity):
    self.colour = colour
    self.intensity = intensity

  def camera_space(self, camera):
    return self