import numpy as np
from numpy import dot

class Phong:
  def calc(obj_colour, light_intensity, distance_attenuation, reflectiveness, N, R, V, L, n):
    k_ambient, k_specular, k_diffuse = obj_colour, obj_colour, obj_colour

    I_light = light_intensity
    k_light = distance_attenuation

    I_ambient = k_ambient * I_light * k_light * reflectiveness
    I_diffuse = k_diffuse * dot(N,L) * I_light * k_light * (1 - reflectiveness)



# for reflective material, there light comes solely from specular
# for non reflectiv material there light comes from diffuse