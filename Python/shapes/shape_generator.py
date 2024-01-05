from geometry import Point_3D
from geometry import Plane_Polygon

def Cuboid(size):
  l, w, h = size # diameters

  # radiuses
  hl = l/2
  hw = w/2
  hh = h/2
  vertices = [
    Point_3D(-hl, -hw, -hh),  # Vertex 1
    Point_3D(-hl, -hw, hh),   # Vertex 2
    Point_3D(-hl, hw, -hh),   # Vertex 3
    Point_3D(-hl, hw, hh),    # Vertex 4
    Point_3D(hl, -hw, -hh),   # Vertex 5
    Point_3D(hl, -hw, hh),    # Vertex 6
    Point_3D(hl, hw, -hh),    # Vertex 7
    Point_3D(hl, hw, hh)      # Vertex 8
  ]
  faces = [
    Plane_Polygon([vertices[0], vertices[2], vertices[3], vertices[1]]),  # Face 1:
    Plane_Polygon([vertices[0], vertices[1], vertices[5], vertices[4]]),  # Face 2:
    Plane_Polygon([vertices[0], vertices[4], vertices[6], vertices[2]]),  # Face 3:
    Plane_Polygon([vertices[7], vertices[6], vertices[4], vertices[5]]),  # Face 4: 
    Plane_Polygon([vertices[7], vertices[3], vertices[2], vertices[6]]),  # Face 5:
    Plane_Polygon([vertices[7], vertices[5], vertices[1], vertices[3]])   # Face 6:
  ]
  return vertices, faces

def Pyramid(base_width, height):
  hbw = base_width/2
  hh = height/2
  vertices = [
    Point_3D(0,hh, 0), # top
    Point_3D(hbw, -hh, hbw), 
    Point_3D(hbw, -hh, -hbw),
    Point_3D(-hbw, -hh, hbw),
    Point_3D(-hbw, -hh, -hbw)
  ]
  faces = [
    Plane_Polygon([vertices[1], vertices[2], vertices[3], vertices[4]]), # bottom
    Plane_Polygon([vertices[0], vertices[1], vertices[2]]),
    Plane_Polygon([vertices[0], vertices[1], vertices[3]]),
    Plane_Polygon([vertices[0], vertices[4], vertices[3]]),
    Plane_Polygon([vertices[0], vertices[4], vertices[2]])
  ]
  return vertices, faces
