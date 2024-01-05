from load_object import load_obj

from geometry import Line_3D, Ray_3D, Segment_3D
from intersections import line_polygon_intersection

class Custom_Shape:
  def __init__(self, vertices_faces):
    self.vertices = vertices_faces[0]
    self.faces = vertices_faces[1]

  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      # gets intersection as well as normal
      intersections = [[intersection[0], face.plane.normal] for face in self.faces if (intersection := line_polygon_intersection(line, face))]
      return intersections # intersection point, intersection t, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None

# custom shape takes list of vertices and faces, specifically used from shape creator function


class Custom:
  def __init__(self, filename, obj_name=None):
    self.vertices, self.faces = load_obj(filename, obj_name)

  def intersection(self, line):
    if isinstance(line, (Line_3D, Ray_3D, Segment_3D)):
      # gets intersection as well as normal
      intersections = [[intersection[0], face.plane.normal] for face in self.faces if (intersection := line_polygon_intersection(line, face))]
      return intersections # intersection point, intersection t, normal | in a sphere the intersection point is the normal when the sphere is located at (0,0,0)
    return None
  

if __name__ == '__main__':
  shape = Custom('objects/rock.obj')
  print(shape.faces[0].points)