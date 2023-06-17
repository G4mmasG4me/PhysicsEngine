import math
import maths
from grid_lines import grid_lines, floor_grid_lines
import matrix
import numpy as np
from colours import *
import pygame
from geometry import Ray_3D, Point_2D, Point_3D, Vector_2D, Vector_3D, Line_2D, Line_3D, Segment_2D, Segment_3D, Plane
from PIL import Image

class Camera:
  def __init__(self, resolution, FOV, focal_length, position, rotation, render_distance=100):
    self.resolution = resolution
    self.hFOV = FOV
    self.vFOV = self.calc_vfov()
    self.focal_length = focal_length
    self.position = Point_3D(*position)
    self.rotation = rotation
    self.rotation_matrix = matrix.xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = matrix.inverse_matrix(self.rotation_matrix)
    self.direction = maths.euler_to_axis_angle(rotation)
    self.px_size = self.pixel_size()
    self.canvas_size = self.calc_canvas_size()
    self.render_distance = render_distance

  def calc_vfov(self):
    return math.degrees(2 * math.atan(math.tan(math.radians(self.hFOV)/2) * (self.resolution[1] / self.resolution[0])))
  
  def set_rotation(self, rotation):
    self.rotation = rotation
    self.rotation_matrix = matrix.xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = matrix.inverse_matrix(self.rotation_matrix)
  
  def calc_canvas_size(self):
    canvas_width =  2 * self.focal_length * math.tan(math.radians(self.hFOV)/2)
    canvas_height =  2 * self.focal_length * math.tan(math.radians(self.vFOV)/2)
    return [canvas_width, canvas_height]

  def pixel_size(self):
    '''
    Calculates Pixel Size
    '''
    canvas_width =  2 * self.focal_length * math.tan(math.radians(self.hFOV)/2)
    return canvas_width / self.resolution[0]
  
  # camera space plane
  def near_plane(self):
    '''
    Standard Near Plaen in Z Axis
    '''
    A = 0
    B = 0
    C = 1
    D = -self.focal_length
    return A, B, C, D

  def far_plane(self):
    '''
    Standard Far Plane in Z Axis
    '''
    A = 0
    B = 0
    C = 1
    D = -self.render_distance
    return A,B,C,D
  
  def calculate_pixel_postions(self):
    '''
    Generates a lis of pixel positions in world space. Ignores z axis as plane is in the z axis
    '''
    pixel_positions = []
    for y in range(round(self.resolution[1]/2), -round(self.resolution[1]/2), -1):
      pixel_row = []
      for x in range(-round(self.resolution[0]/2), round(self.resolution[0]/2)):
        pixel_row.append([x*self.px_size, y*self.px_size])
      pixel_positions.append(pixel_row)
    return pixel_positions

  def change_resolution(self, resolution):
    self.resolution = resolution
    self.vFOV = self.calc_vfov()
    self.px_size = self.pixel_size()

  def change_FOV(self, FOV):
    self.hFOV = FOV
    self.vFOV = self.calc_vfov()

  def change_rotation(self, rotation):
    self.rotation = rotation

  def render_gridlines(self, screen, grid_line_dist, grid_max_dist):
    w, h = self.resolution
    display_bounds = [
      [[0,0],[w,0]], # tl - tr
      [[w,0],[w,h]], # tr - br
      [[w,h],[0,h]], # br - bl
      [[0,h],[0,0]] # bl - tl
    ]
    walls = [Segment_2D(Point_2D(*wall[0]), Point_2D(*wall[1])) for wall in display_bounds]

    # get grid lines
    _, grid_line = floor_grid_lines(grid_line_dist, grid_max_dist)

    # get plane coefficients
    a,b,c,d = self.canvas_plane()

    # convert 3d grid lines to 2d canvas
    # get 2 points on line, and
    for axis in [grid_line]:
      for axis_lines in axis:
        point1, point2 = axis_lines.p1, axis_lines.p2
        # get third point between 2 points
        point3 = maths.between_points_3d(point1, point2)

        # convert points to camera space
        point1 = self.camera_space_point(point1)
        point2 = self.camera_space_point(point2)
        point3 = self.camera_space_point(point3)
        
        # find intersection points between [point, focus point] line and plane
        intersections = [maths.line_plane_intersect(Line_3D(point, self.position), Plane(a,b,c,d)) for point in [point1, point2, point3]]
        # list of not none values
        valid_intersections = [intersect for intersect in intersections if intersect is not None]
        if len(valid_intersections) >= 2:
          p1 = intersections[0]
          p2 = intersections[1]
          # remove extra z axis, since non rotated plane exists along axis, so only 2 axis needed
          p1 = Point_2D(p1.z, p1.y)
          p2 = Point_2D(p2.z, p2.y)
          
          dir = p2 - p1
          dir = Vector_2D(dir.x, dir.y)
          point = self.canvas_pos_to_screen_pos(p1)
          line = Line_2D(point, dir)
          if dir == [0,0]:
            pass
            # draw dot at pos
            screen.set_at(point, BLACK)
          else:
            intersections = []
            for wall in walls:
              intersect = maths.line_segment_intersect_2d(line, wall)
              
              if intersect != None:
                intersections.append(intersect)
            if len(intersections) == 2:
              pygame.draw.line(screen, BLACK, [intersections[0].x, intersections[0].y], [intersections[1].x, intersections[1].y], width=1)
    

  def canvas_pos_to_screen_pos(self, point):
    point = point / self.px_size
    
    point = point + [self.resolution[0] / 2, -self.resolution[1]/2]
    return point

  def render_objects(self, objects, light_sources):
    canvas_px_info = []
    image = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    canvas = image.load()
    # simple ray tracing, only one intersection
    pixel_positions = self.calculate_pixel_postions()
    print(pixel_positions[0][0])
    print(f'Height: {len(pixel_positions)}')
    print(f'Width: {len(pixel_positions[0])}')
    for y_pos, pixel_row in enumerate(pixel_positions):
      canvas_px_info.append([])
      for x_pos, pixel_point in enumerate(pixel_row):
        ray = Ray_3D(Point_3D(0,0,0), Vector_3D(pixel_point[0], pixel_point[1], -self.focal_length))
        intersections = []
        for object in objects:
          intersection = object.intersection(ray) # pos, d, colour 
          if intersection:
            intersections.append(intersection)
        if intersections:
          px_info = min(intersections, key=lambda x: x[1])
        else:
          px_info = (None, None, BLACK)
        canvas_px_info[y_pos].append(px_info)
        canvas[x_pos, y_pos] = px_info[2]
    image.save("output_image.png")
    return canvas_px_info, canvas


  def camera_space_point(self, point):
    # translate
    translated_point = point - self.position

    # rotate and return
    return Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

  def camera_space_vector(self, vector):
    return self.inverse_rotation_matrix.dot(vector)