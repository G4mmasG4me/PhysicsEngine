from geometry import Vector_3D, Ray_3D
from math import asin, sin, acos, cos, sqrt

class Light_Ray:
  def __init__(self, ray, colour, intensity, medium):
    self.ray = ray
    self.colour = colour
    self.intensity = intensity
    self.medium = medium

  def change_medium(self, medium):
    self.medium = medium
  
  def reflective_direction(self, surface_normal): # surface contains intersection point, surface normal, colour, surface properties
    return self.ray.direction - 2 * (self.ray.direction.dot(surface_normal)) * surface_normal
  
  def refractive_direction(self, surface_normal, intersection_medium):
    t = self.medium.refractive_index / intersection_medium.refractive_index
    angle_incidence = self.incidence_angle(surface_normal)
    angle_refraction = asin(t * sin(angle_incidence))

    return t * self.ray.direction + (t * cos(angle_incidence)) - sqrt(1 - sin(angle_refraction)**2) * surface_normal
    
  def intersection(self, intersection_medium, transparency, colour, intersection_point, intersection_normal):
    intersection_normal = self.correct_surface_normal(intersection_normal)
    incidence_angle = self.incidence_angle(intersection_normal)
    if transparency == 1: # all light passes through medium, unless incident angle bigger than critical angle
      if incidence_angle < critical_angle: # light can pass through medium
        refractive_intensity = self.intensity * transparency

        refracted_ray = Ray_3D(intersection_point, self.refractive_direction(intersection_normal, intersection_medium))

        reflected_light_ray = None
        refracted_light_ray = Light_Ray(refracted_ray, colour, refractive_intensity, intersection_medium)


      else: # incidence angle bigger or equal to critical angle, light won't pass through medium
        reflective_intensity = 1
        reflected_ray = Ray_3D(intersection_point, self.reflective_direction(intersection_normal))
        reflected_light_ray = Light_Ray(reflected_ray, colour, reflective_intensity, intersection_medium)
        refracted_light_ray = None
      

    elif 0 < transparency < 1: # some transparency, some light will pass through medium
      critical_angle = asin(self.medium.refractive_index /  intersection_medium.refractive_index)
      if incidence_angle < critical_angle: # light can pass through medium
        reflective_intensity = self.intensity * (1-transparency)
        refractive_intensity = self.intensity * transparency

        reflected_ray = Ray_3D(intersection_point, self.reflective_direction(intersection_normal))
        refracted_ray = Ray_3D(intersection_point, self.refractive_direction(intersection_normal, intersection_medium))

        reflected_light_ray = Light_Ray(reflected_ray, colour, reflective_intensity, intersection_medium)
        refracted_light_ray = Light_Ray(refracted_ray, colour, refractive_intensity, intersection_medium)


      else: # incidence angle bigger or equal to critical angle, light won't pass through medium
        reflective_intensity = 1
        reflected_ray = Ray_3D(intersection_point, self.reflective_direction(intersection_normal))
        reflected_light_ray = Light_Ray(reflected_ray, colour, reflective_intensity, intersection_medium)
        refracted_light_ray = None

      
    elif transparency == 0: # no transparency, light won't pass through medium
      reflective_intensity = 1
      reflected_ray = Ray_3D(intersection_point, self.reflective_direction(intersection_normal))
      reflected_light_ray = Light_Ray(reflected_ray, colour, reflective_intensity, intersection_medium)
      refracted_light_ray = None
    return reflected_light_ray, refracted_light_ray

  def incidence_angle(self, surface_normal):
    return acos(self.ray.direction.dot(surface_normal))
  
  def retractive_angle(sefl, t, angle_incidence):
    return asin(t * sin(angle_incidence))

  
  def correct_surface_normal(self, surface_normal):
    return min(self.ray.direction.dot(surface_normal), self.ray.direction.dot(-surface_normal))