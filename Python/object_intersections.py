import math
from geometry import Point_3D

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

def line_cylinder_intersection(line, cylinder):
  # Unpack the point and direction coordinates
  Px, Py, Pz = line.p1.to_list()
  Dx, Dy, Dz = line.dir.normalise().to_list()

  # Calculate the coefficients of the quadratic equation for t
  A = Dx**2 + Dz**2
  B = 2 * (Px * Dx + Pz * Dz)
  C = Px**2 + Pz**2 - cylinder.radius**2

  # Calculate the discriminant to determine the number of intersections
  discriminant = B**2 - 4 * A * C

  # side intersection
  intersections = []
  if discriminant >= 0:
    # Calculate the two solutions for t
    t1 = (-B + math.sqrt(discriminant)) / (2 * A)
    t2 = (-B - math.sqrt(discriminant)) / (2 * A)

    # Calculate the y-coordinates of the intersection points
    y1 = Py + t1 * Dy
    y2 = Py + t2 * Dy

    # Check if the intersection points are within the height of the cylinder
    if -cylinder.half_height <= y1 <= cylinder.half_height:
        x1 = Px + t1 * Dx
        z1 = Pz + t1 * Dz
        intersections.append([Point_3D(x1, y1, z1), t1])
    if -cylinder.half_height <= y2 <= cylinder.half_height:
        x2 = Px + t2 * Dx
        z2 = Pz + t2 * Dz
        intersections.append([Point_3D(x2, y2, z2), t2])

  if Dy != 0:
    # Calculate the t value where the line intersects the top circular base
    t_top = (cylinder.half_height - Py) / Dy
    x_top = Px + t_top * Dx
    z_top = Pz + t_top * Dz
    if x_top**2 + z_top**2 <= cylinder.radius**2:
      intersections.append([Point_3D(x_top, cylinder.half_height, z_top), t_top])

    # Calculate the t value where the line intersects the bottom circular base
    t_bottom = (-cylinder.half_height - Py) / Dy
    x_bottom = Px + t_bottom * Dx
    z_bottom = Pz + t_bottom * Dz
    if x_bottom**2 + z_bottom**2 <= cylinder.radius**2:
      intersections.append([Point_3D(x_bottom, -cylinder.half_height, z_bottom), t_bottom])

  intersections = [intersection for intersection in intersections if line.along_line(intersection[1])]
  return intersections
