from intersections import line_quad_intersection, line_plane_intersect, line_line_intersect_2d, point_in_plane_polygon
from object_intersections import line_sphere_intersection
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D
from Planes import Plane, Plane_Polygon
from light_equations import point_of_reflection, point_of_reflection_dir
from Lights import DirectionalLight, SpotLight, PointLight

from math import asin, atan2, pi
epsilon = 0.1

class Sphere:
  def __init__(self, radius):
    self.radius = radius
  
  # wont work now that spheres contain no position data
  def intersection(self, line):
    
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      intersections = line_sphere_intersection(line, self)
      intersections = [[intersection_point, intersection_point.to_vector()] for intersection_point, _ in intersections] # generate 

      return intersections # intersection point, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None
  
  def one_bounce_intersection(light_pos, intersection_pos):
    return []
  
  def get_uv_pos(self, pos, img_size, texture_scale=1):
    pos = pos.to_vector().normalise()
    u = (0.5 + (atan2(pos.z,pos.x)/(2*pi))) % 1
    v = (0.5 + asin(pos.y)/pi) % 1
    return Point_2D(u, v)
  

  def tesselation(sides):
    pass


class Cuboid:
  def __init__(self, size):
    self.size = size
    
    l, w, h = size
    self.vertices = [
      Point_3D(-l, -w, -h),  # Vertex 1
      Point_3D(-l, -w, h),   # Vertex 2
      Point_3D(-l, w, -h),   # Vertex 3
      Point_3D(-l, w, h),    # Vertex 4
      Point_3D(l, -w, -h),   # Vertex 5
      Point_3D(l, -w, h),    # Vertex 6
      Point_3D(l, w, -h),    # Vertex 7
      Point_3D(l, w, h)      # Vertex 8
    ]

    # faces vertexes must be in certain order, so that the vertex before and after, both connect to it. And its done in clockwise order
    self.faces = [
      Quad(self.vertices[0], self.vertices[2], self.vertices[3], self.vertices[1]),  # Face 1:
      Quad(self.vertices[0], self.vertices[1], self.vertices[5], self.vertices[4]),  # Face 2:
      Quad(self.vertices[0], self.vertices[4], self.vertices[6], self.vertices[2]),  # Face 3:
      Quad(self.vertices[7], self.vertices[6], self.vertices[4], self.vertices[5]),  # Face 4: 
      Quad(self.vertices[7], self.vertices[3], self.vertices[2], self.vertices[6]),  # Face 5:
      Quad(self.vertices[7], self.vertices[5], self.vertices[1], self.vertices[3])   # Face 6:
    ]
    self.normals = [
      Vector_3D(-1,0,0),
      Vector_3D(0,-1,0),
      Vector_3D(0,0,-1),
      Vector_3D(1,0,0),
      Vector_3D(0,1,0),
      Vector_3D(0,0,1)
    ]

  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      # gets intersection as well as normal
      intersections = [[intersection[0], normal] for face, normal in zip(self.faces, self.normals) if (intersection := line_quad_intersection(line, face))]
      return intersections # intersection point, intersection t, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None
  
  def one_bounce_intersection(self, light, intersection_pos):
    reflections = []
    if isinstance(light, DirectionalLight):
      for face in self.faces:
        reflection = point_of_reflection_dir(intersection_pos, light.dir, face.plane_polygon.plane)
        if reflection:
          if point_in_plane_polygon(reflection, face.plane_polygon):
            reflections.append(reflection)

    elif isinstance(light, SpotLight):
      for face in self.faces:
        reflection = point_of_reflection(intersection_pos, light.pos, face.plane_polygon.plane)
        if reflection:
          dir = (reflection - light.position).to_vector()
          if point_in_plane_polygon(reflection, face.plane_polygon) and light.facing_direction(dir):
            reflections.append(reflection)

    elif isinstance(light, PointLight):
      for face in self.faces:
        reflection = point_of_reflection(intersection_pos, light.pos, face.plane_polygon.plane)
        if reflection:
          if point_in_plane_polygon(reflection, face.plane_polygon):
            reflections.append(reflection)
    return reflections

class Infinte_Plane:
  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      intersection = line_plane_intersect(line, Plane(0,0,1,0))
      if intersection:

        intersection = [[intersection[0], Vector_3D(0,0,1)]]
      return intersection # intersection point, intersection t, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None
  
  def one_bounce_intersection(light, intersection_pos):
    reflections = []
    if isinstance(light, DirectionalLight):
      reflection = point_of_reflection_dir(intersection_pos, light.dir, Plane(0,0,1,0))
      if reflection:
        reflections.append(reflection)

    elif isinstance(light, SpotLight):
      reflection = point_of_reflection(intersection_pos, light.pos, Plane(0,0,1,0))
      if reflection:
        dir = (reflection - light.position).to_vector()
        if light.facing_direction(dir):
          reflections.append(reflection)

    elif isinstance(light, PointLight):
      reflection = point_of_reflection(intersection_pos, light.pos, Plane(0,0,1,0))
      if reflection:
        reflections.append(reflection)
    return reflections
  
  def get_uv_pos(self, pos, img_size, texture_scale=1):
    uv = pos * texture_scale / img_size[0] % 1
    return uv

class Quad_Plane_Geometry:
  def __init__(self, size):
    self.size = size
    self.points = [
      Point_3D(-size[0], -size[1], 0),
      Point_3D(-size[0], size[1], 0),
      Point_3D(size[0], -size[1],0),
      Point_3D(size[0],size[1],0)
    ]

  def intersection(self, line, ignore_base_point=True):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      intersection = line_plane_intersect(line, Plane(0,0,1,0))
      if intersections:
        # filter the output
        if ignore_base_point: # use this for shadows
          intersections = [intersection for intersection in intersections if abs(intersection[1]) > epsilon]
        
        if intersections:
          # get lowest intersection
          intersection = min(intersections, key=lambda x: abs(x[1]))

          intersection_point, intersection_t = intersection
          intersection_n = intersection_point.to_vector()
          return [intersection_point, intersection_n] # intersection point, intersection t, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None

class Quad:
  def __init__(self, p1, p2, p3, p4):
    self.points = [p1,p2,p3,p4] # tl, tr, br, bl
    self.plane_polygon = Plane_Polygon(self.points)

class Triangle:
  def __init__(self, p1, p2, p3):
    self.points = [p1,p2,p3]


if __name__ == '__main__':
  my_cube = Cuboid([10,10,10])
  vertices = my_cube.vertices
  plane_polygon = Plane_Polygon([vertices[0], vertices[1], vertices[2], vertices[3]])
  plane = plane_polygon.plane
  my_line = Line_3D(Point_3D(-50,0,0), Vector_3D(1,0,0))
  point, t = line_plane_intersect(my_line, plane)

  ray = Ray_2D(Point_2D(0,0), Vector_2D(1,0))
  segment = Segment_2D(Point_2D(10,10), Point_2D(10,-10))
  intersect = line_line_intersect_2d(ray, segment)
  print(intersect)