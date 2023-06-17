from intersections import ray_quad_intersection, ray_sphere_intersection

class Sphere:
  def __init__(self, position, rotation, radius, colour):
    self.position = position
    self.rotation = rotation
    self.radius = radius
    self.colour = colour # need to swap out for texture

  def intersection(self, ray):
    intersection_output =  ray_sphere_intersection(ray, self)
    if intersection_output:
      return intersection_output[0], intersection_output[1], self.colour
    
    return None
  

class Cuboid:
  def __init__(self, position, rotation, size):
    self.position = position
    self.rotation = rotation
    self.size = size
    l, w, h = size

    self.vertices = [
      [-l/2, -w/2, -h/2],  # Vertex 1
      [-l/2, -w/2, h/2],   # Vertex 2
      [-l/2, w/2, -h/2],   # Vertex 3
      [-l/2, w/2, h/2],    # Vertex 4
      [l/2, -w/2, -h/2],   # Vertex 5
      [l/2, -w/2, h/2],    # Vertex 6
      [l/2, w/2, -h/2],    # Vertex 7
      [l/2, w/2, h/2]      # Vertex 8
    ]

    self.faces = [
      Quad(self.vertices[0], self.vertices[1], self.vertices[2], self.vertices[3]),  # Face 1: Front face
      Quad(self.vertices[0], self.vertices[1], self.vertices[4], self.vertices[5]),  # Face 2: Bottom face
      Quad(self.vertices[0], self.vertices[2], self.vertices[4], self.vertices[6]),  # Face 3: Left face
      Quad(self.vertices[1], self.vertices[3], self.vertices[5], self.vertices[7]),  # Face 4: Right face
      Quad(self.vertices[2], self.vertices[3], self.vertices[6], self.vertices[7]),  # Face 5: Back face
      Quad(self.vertices[4], self.vertices[5], self.vertices[6], self.vertices[7])   # Face 6: Top face
    ] 

  def intersect(self, ray):
    # gets list of distances and intersections
    intersections = [ray_quad_intersection(ray, face) for face in self.faces]
    # sort based on distance
    sorted_intersections = sorted(intersections, key=lambda x: x[1])

    # closest intersection
    closest_intersection = sorted_intersections[0]



class Quad:
  def __init__(self, p1, p2, p3, p4):
    self.points = [p1,p2,p3,p4] # tl, tr, br, bl

class Triangle:
  def __init__(self, p1, p2, p3):
    self.points = [p1,p2,p3]