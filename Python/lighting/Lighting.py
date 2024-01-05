import numpy as np
from math import sqrt, acos, cos, sin, pi, isnan, exp
from lighting import reflection_angle, reflected_ray_dir, incidence_angle
from functions import clamp
import random
from geometry import Vector_3D
from surface_properties import Colour

# returns second position in list, used for key instead of lambda
def func1(x):
  return x[1]

def phong(obj_colour, light_colour, roughness, N, L, V, n):
  # normalise values
  N = N.normalise()
  L = L.normalise()
  V = V.normalise()
  N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=func1)
  R = 2 * NL_dot * N - L
  RV_dot = R.dot(V)
  

  Id = obj_colour * max(0, NL_dot) * light_colour
  Is = obj_colour * max(0, RV_dot)**n * light_colour
  return Id, Is

#K_a, K_d, K_s = obj_colour
#I_a, I_d, I_s = light_colour

# K_a*i_a + E(K_d*(Dot(L_m, N)*i_d + K_s*(Dot(R_m, V)^2 * i_s))
def blinn_phong(light_colour, roughness, N, L, V, n):
  # normalise values
  N = N.normalise()
  L = L.normalise()
  V = V.normalise()

  H = (L+V).normalise()

  return 
  Is = max(0, N.dot(H))**n

# only used for diffuse
def oren_nayar(obj_colour, light_colour, incidence_ray, N, L, V, roughness):
  N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=func1)
  R = 2 * NL_dot * N - L

  # calculate angle of incidence
  theta_incidence = incidence_angle(incidence_ray, N)

  # calculate angle of reflection
  theta_reflection = reflection_angle(incidence_ray, N)

  # reflection vector

  # calculate angle between view vector and reflection vector
  theta_view_reflection = acos(clamp(R.dot(V), -1, 1))

  std = roughness / sqrt(2)

  A = 1 - 0.5 * (std**2 / (std**2 + 0.57))
  B = 0.45 * (std**2 / (std**2 + 0.09))

  Id = obj_colour * max(0, NL_dot * (A + B * max(0, cos(theta_view_reflection) * sin(roughness) * max(cos(theta_incidence), cos(theta_reflection))))) * light_colour
  return Id


# used for specular
def cook_torrance(obj_colour, light_colour, N, L, V, roughness, n1, n2):
  # normalise
  N = N.normalise()
  L = L.normalise()
  V = V.normalise()
  H = (V+L).to_vector().normalise()
  # N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=func1)
  NL_dot = N.dot(L)
  R = 2 * NL_dot * N - L
  RV_dot = R.dot(V)

  NV_dot = N.dot(V)

  # frensel equations
  F0 = ((n1-n2)**2/(n1+n2)**2)
  F = clamp(F0 + (1 - F0) * (1 - V.dot(H))**5, 0, 1)


  # geometric attenuation
  # G = G1(NL_dot, roughness) * G1(NV_dot, roughness)
  G = cook_torrance_geometric(N,V,L,H)


  # distribution function
  # D = GGX(N.dot(GGX_microfacet_normal(roughness)), roughness)
  D = beckmann(N, H, roughness)

  R = 2 * NL_dot * N - L

  Is = obj_colour * ((F * G * D) / (4 * NV_dot * NL_dot)) * light_colour
  return Is

def cook_torrance_geometric(N,V,L,H):
  return min((1, (2 * N.dot(N) * N.dot(V)) / V.dot(H), (2 * N.dot(H) * N.dot(L)) / V.dot(H)))

def G1(dot, alpha):
  return 2 * dot / (dot + sqrt(alpha**2 + (1 - alpha**2) * dot**2))

# mu is the cosine of the angle between the microfacet normal and surface normal, aka dot product of the 2 vectors
def GGX(mu, alpha):
  return (alpha**2 * mu**2 * (alpha**2 - 1) + 1)**-2

def GGX_microfacet_normal(alpha):
  xi1 = random.random()
  xi2 = random.random()

  theta = acos(sqrt((1 - xi1) / ((alpha**2 - 1) * xi1 + 1)))
  phi = 2 * pi * xi2

  cos_theta = cos(theta)

  sin_theta = sin(theta)
  x = sin_theta * cos(phi)
  y = sin_theta * sin(phi)
  z = cos_theta

  microfacet_normal = Vector_3D(x,y,z)
  return microfacet_normal

def beckmann(N, H, alpha):
  cos_theta_h = N.dot(H)
  cos_theta_h_sq = cos_theta_h**2
  tan_theta_h_sq = (1 - cos_theta_h_sq) / cos_theta_h_sq

  exponent = -tan_theta_h_sq / (alpha * alpha)
  denom = pi * alpha * alpha * cos_theta_h_sq * cos_theta_h_sq

  return exp(exponent) / denom
  
if __name__ == '__main__':
  obj_colour = Colour((50,50,50))

  light_colour = Colour((255,255,255))
  light_intensity = 0.5

  macronormal = Vector_3D(-0.23, 0.23, 0.95)
  light_vector = Vector_3D(-1,1,1).normalise()
  view_vector = Vector_3D(0.21,-0.21,0.96)

  roughness = 0.1

  Is1 = cook_torrance(obj_colour, light_colour * light_intensity, macronormal, light_vector, view_vector, roughness, 1, 1.5)
  Id2, Is2 = phong(obj_colour, light_colour, roughness, macronormal, light_vector, view_vector, 10)
  print(Is1)
  print(Is2)