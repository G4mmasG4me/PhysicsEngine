from geometry import Point_3D
from geometry import Plane_Polygon

def load_obj(filename, obj_name=None):
  valid_object = False
  vertices = []
  faces = []
  faces_indices = []

  with open(filename, 'r') as f:
    for line in f:
      line = line.strip()

      if line.startswith('v '):
        vertex = line[2:].split()
        point = Point_3D(float(vertex[0]), float(vertex[1]), float(vertex[2]))
        vertices.append(point)

      if line.startswith('o '):
        if line[2:].strip() == obj_name:
          valid_object = True
        else:
          valid_object = False
      if valid_object or obj_name == None or obj_name == '':
        if line.startswith('f '):
          face_indices = line[2:].split()
          face = []
          for index_set in face_indices:
            vertex_index = int(index_set.split('/')[0])
            face.append(vertex_index)
              
          faces_indices.append(face)

  for face_indices in faces_indices:
    face_points = []
    for pos in face_indices:
      face_points.append(vertices[pos-1])
    faces.append(Plane_Polygon(face_points))
  return vertices, faces

if __name__ == '__main__':
  load_obj('objects/rock.obj', 'Rock')