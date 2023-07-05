import math
from geometry import Line_3D, Point_3D

def grid_lines(grid_line_dist, grid_max_dist):

  # simple grid generation in a cube
  # define max distance around camera
  lines = math.floor(grid_max_dist * 2 / grid_line_dist) + 1
  points = [-grid_max_dist + i*grid_line_dist for i in range(lines)]

  # x axis
  x_lines = []
  y_lines = []
  z_lines = []
  for point_1 in points:
    for point_2 in points:
      x_lines.append(Line_3D(Point_3D(-grid_max_dist, point_1, point_2), Point_3D(grid_max_dist, point_1, point_2)))
      y_lines.append(Line_3D(Point_3D(point_1, -grid_max_dist, point_2), Point_3D(point_1, grid_max_dist, point_2)))
      z_lines.append(Line_3D(Point_3D(point_1, point_2, -grid_max_dist), Point_3D(point_1, point_2, grid_max_dist)))

  return x_lines, y_lines, z_lines

def floor_grid_lines(grid_line_dist, grid_max_dist):
  lines = lines = math.floor(grid_max_dist * 2 / grid_line_dist) + 1
  points = [-grid_max_dist + i*grid_line_dist for i in range(lines)]

  x_lines = []
  z_lines = []
  for point_1 in points:
    x_lines.append(Line_3D(Point_3D(-grid_max_dist, 0, point_1), Point_3D(grid_max_dist, 0, point_1)))
    z_lines.append(Line_3D(Point_3D(point_1, 0, -grid_max_dist), Point_3D(point_1, 0, grid_max_dist)))
  return x_lines, z_lines