class DirectionalLight:
  def __init__(self, direction, colour, intensity, attentuation):
    self.direction = direction
    self.colour = colour
    self.intensity = intensity

class SpotLight:
  def __init__(self, position, direction, angle, colour, intensity, attentuation):
    self.position = position
    self.direction = direction
    self.angle = angle # cone angle
    self.colour = colour
    self.intensity = intensity
    self.attentuation = attentuation

class PointLight:
  def __init__(self, position, colour, intensity, attentuation):
    self.position = position
    self.colour = colour
    self.intensity = intensity
    self.attentuation = attentuation

class AmbientLight:
  def __init__(self, colour, intensity):
    self.colour = colour
    self.intensity = intensity