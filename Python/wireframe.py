class Camera:
  def __init__(self, position, rotation, resolution):
    self.position = position
    self.rotation = rotation
    self.resolution = resolution


def render(object):
  # load object

  # get list of lines
  lines = []
  for face in object.faces:
    for point_pos in range(len(face)):
      lines.append([face[point_pos], face[(point_pos+1) % len(face)]])

  # create a list of unique lines between vertexes
  unique_lines = [list(x) for x in list(set(frozenset(x) for x in lines))]


  # for each vertex
  for vertex in object.vertexes:

    # convert to screen space
    # add to ilst
  # for each unique line
    # draw line between 2 screen space points