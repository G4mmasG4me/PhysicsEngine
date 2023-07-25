import numpy as np
from math import sqrt, acos, cos, sin, pi, isnan
from light_equations import reflection_angle, reflected_ray_dir, incidence_angle
from functions import clamp


def phong(obj_colour, light_colour, roughness, N, V, L, n):
  N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=lambda x: x[1])
  R = 2 * NL_dot * N - L
  RV_dot = R.dot(V)
  

  Id = obj_colour * light_colour * max(0, NL_dot) * roughness
  Is = obj_colour * light_colour * max(0, RV_dot)**n * (1-roughness)
  return Id, Is

# only used for diffuse
def oren_nayar(object_colour, light_colour, incidence_ray, N, L, V, roughness):
  N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=lambda x: x[1])

  # calculate angle of incidence
  theta_incidence = incidence_angle(incidence_ray, N)

  # calculate angle of reflection
  theta_reflection = reflection_angle(incidence_ray, N)

  # reflection vector
  R = 2 * NL_dot * N - L

  # calculate angle between view vector and reflection vector
  theta_view_reflection = acos(clamp(R.dot(V), -1, 1))

  std = roughness / sqrt(2)

  A = 1 - 0.5 * (std**2 / (std**2 + 0.57))
  B = 0.45 * (std**2 / (std**2 + 0.09))

  Id = object_colour * light_colour * max(0, NL_dot * (A + B * max(0, cos(theta_view_reflection) * sin(roughness) * max(cos(theta_incidence), cos(theta_reflection)))))
  return Id


# used for specular
def cook_torrance(object_colour, light_colour, N, L, V, roughness, n1, n2):
  H = (V.normalise() + L.normalise()).to_vector().normalise()
  N, NL_dot = max([[N, N.dot(L)] for N in [N, N.inverse()]], key=lambda x: x[1])
  F0 = ((n1-n2)/(n1+n2))**2

  F = clamp(F0 + (1 - F0) * (1 - NL_dot)**5, 0, 1)

  G = G1(L, N, roughness) * G1(V, N, roughness)

  D = (roughness**2) / (pi * (N.dot(H)**2 * (roughness**2 - 1) + 1)**2)
  Is = object_colour * light_colour * ((F * G * D) / (4 * NL_dot * N.dot(V)))
  return Is

def G1(x, N, alpha):
  Nx_dot = N.dot(x)
  return 2 * Nx_dot / (Nx_dot + sqrt(alpha**2 + (1 - alpha**2) * Nx_dot**2))