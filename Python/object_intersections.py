import math

def line_sphere_intersection(line, sphere):
  oc = line.p1
  
  a = line.dir.dot(line.dir) # use non normalised direction, needs direction vector with magnitude between points
  b = 2 * line.dir.dot(oc)
  c = oc.dot(oc) - sphere.radius ** 2

  discriminant = b ** 2 - 4 * a * c
  if discriminant >= 0:

    sqrt_discriminant = math.sqrt(discriminant)
    t1 = (-b - sqrt_discriminant) / (2 * a)
    t2 = (-b + sqrt_discriminant) / (2 * a)
    intersection1 = line.p1 + line.dir * t1
    intersection2 = line.p1 + line.dir * t2
    intersections = [intersection for intersection in [[intersection1,t1],[intersection2,t2]] if line.along_line(intersection[1])]
    if intersections:
      return intersections
  return []

