import math

import numpy as np
from Colour import *
import pygame

# Custom Function Packages
import maths as maths
from matrix import xyz_matrix, inverse_matrix

# Custom Classes
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D

from PIL import Image

import random
from tqdm import tqdm
from light_equations import light_intensity_distance

epsilon = 0.1
class Camera:
  def __init__(self, resolution, FOV, focal_length, position, rotation, render_distance=100):
    self.resolution = resolution
    self.hFOV = FOV
    self.vFOV = self.calc_vfov()
    self.focal_length = focal_length
    self.position = position
    self.rotation = rotation
    self.rotation_matrix = xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = inverse_matrix(self.rotation_matrix)
    self.direction = maths.euler_to_axis_angle(rotation)
    self.px_size = self.pixel_size()
    self.canvas_size = self.calc_canvas_size()
    self.render_distance = render_distance

  def calc_vfov(self):
    return math.degrees(2 * math.atan(math.tan(math.radians(self.hFOV)/2) * (self.resolution[1] / self.resolution[0])))
  
  def set_rotation(self, rotation):
    self.rotation = rotation
    self.rotation_matrix = xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = inverse_matrix(self.rotation_matrix)
  
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
    

  def canvas_pos_to_screen_pos(self, point):
    point = point / self.px_size
    
    point = point + [self.resolution[0] / 2, -self.resolution[1]/2]
    return point

  def render_objects(self, objects, light_sources):
    light_traces = 1
    n = 100
    
    # convert objects to camera space
    objects = [object.camera_space(self) for object in objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in light_sources]

    image = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    canvas = image.load()

    # simple ray tracing, only one intersection
    pixel_positions = self.calculate_pixel_postions()

    # convert pixel positions to a flattened list that consists of [[x_pos, y_pos], pixel_point]
    pixels = []
    for y_pos, pixel_row in enumerate(pixel_positions):
      for x_pos, pixel_point in enumerate(pixel_row):
        pixels.append([[x_pos, y_pos], pixel_point])
    
    for pixel in tqdm(pixels):
      pos, pixel_point = pixel
      x_pos, y_pos = pos
      ray = Ray_3D(Point_3D(0,0,0), Vector_3D(pixel_point[0], pixel_point[1], -self.focal_length))

      # generate all the intersections 
      intersections = []
      for object in objects: # loop through objects, calculating intersections
        intersection_output = object.intersection(ray) # pos, colour
        intersections += intersection_output

      # collected all object intersections
      if intersections:

        closest_intersection = min(intersections, key=lambda x: x[2])

        obj_intersection, obj_normal, distance, obj_colour, obj_material, obj_refractive_index, intersection_obj = closest_intersection
        normalised_normal = obj_normal.normalise() # Intersection Normal
        normals = [normalised_normal, normalised_normal.inverse()]
        V = obj_intersection.to_vector().inverse().normalise() # Direction From Intersection To Eye

        # split light sources
        sorted_light_sources = {}
        for item in light_sources:
          item_type = type(item).__name__
          if item_type not in sorted_light_sources:
            sorted_light_sources[item_type] = []
          sorted_light_sources[item_type].append(item)

        Ia = Colour((0,0,0))
        Id = Colour((0,0,0))
        Is = Colour((0,0,0))

        
        # ambient light
        if 'AmbientLight' in sorted_light_sources:
          for light in sorted_light_sources['AmbientLight']:
            # calculate ambient light intensity
            Ia += obj_colour * light.colour * light.intensity

        
        if 'PointLight' in sorted_light_sources:
          for light in sorted_light_sources['PointLight']:
            segment = Segment_3D(obj_intersection, light.position)
            # check for object interceptions between light and primary ray interception
            light_intersections = []
            for object in objects:
              light_intersections += object.intersection(segment)

            # returns true if any interceptions, else false
            light_obstructed = any([value is not None for value in light_intersections])
            if not light_obstructed: # if no obstructions in light
              distance = light.position.dist(obj_intersection)
              light_intensity = light_intensity_distance(light.intensity, distance)
              light_intensity = light.intensity
              L =  (light.position - obj_intersection).to_vector().normalise() # towards light vector
              N, NL_dot = max([[N, N.dot(L)] for N in normals], key=lambda x: x[1]) # gets the correct normal for each surface
              NL_dot = N.dot(L)
              R = 2 * NL_dot * N - L
              RV_dot = R.dot(V)
              Id += obj_colour * light.colour * light_intensity * max(0, NL_dot)
              Is += obj_colour * light.colour * light_intensity * max(0, RV_dot)**n

        if 'SpotLight' in sorted_light_sources:
          spotlights = sorted_light_sources['SpotLight']
          
          # create a list of spot lights that shine on the primary ray intersection point
          valid_spotlights = [spotlight for spotlight in spotlights if spotlight.facing_direction(obj_intersection - spotlight.position)]

          for light in valid_spotlights:
            segment = Segment_3D(obj_intersection, light.position)

            light_intersections = []
            for object in objects:
              light_intersections += object.intersection(segment)
            
            # returns true if any interceptions, else false
            light_obstructed = any([value is not None for value in light_intersections])
            if not light_obstructed: # if no obstructions in light
              distance = light.position.dist(obj_intersection)
              light_intensity = light_intensity_distance(light.intensity, distance)
              L =  (light.position - obj_intersection).to_vector().normalise() # towards light vector
              N, NL_dot = max([[N, N.dot(L)] for N in normals], key=lambda x: x[1]) # gets the correct normal for each surface
              R = 2 * NL_dot * N - L
              RV_dot = R.dot(V)
              Id += obj_colour * light.colour * light_intensity * max(0, NL_dot)
              Is += obj_colour * light.colour * light_intensity * max(0, RV_dot)**n

        if 'DirectionalLight' in sorted_light_sources:
          for light in sorted_light_sources['DirectionalLight']:
            ray = Ray_3D(obj_intersection, light.direction.inverse())
            light_intersections = []
            for object in objects:
              light_intersections += object.intersection(ray)


            light_obstructed = any([value is not None for value in light_intersections])
            if not light_obstructed:  
              L = light.direction.inverse() # towards light vector
              N, NL_dot = max([[N, N.dot(L)] for N in normals], key=lambda x: x[1]) # gets the correct normal for each surface
              R = 2 * NL_dot * N - L
              RV_dot = R.dot(V)
              Id += obj_colour * light.colour * light.intensity * max(0, NL_dot)
              Is += obj_colour * light.colour * light.intensity * max(0, RV_dot)**n

        colour = Ia + Id + Is
        # log final colour, as well as light type colours
      
      else:
        colour = Colour((0,0,0))
    
      canvas[x_pos, y_pos] = tuple(colour.to_list())
    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_file_name = 'imgs/'
    for i in range(16):
      random_file_name += random.choice(chars)
    random_file_name += '.png'
    image.save(random_file_name)
    print(f'Saved: {random_file_name}')
    return [], image


  def camera_space_point(self, point):
    # translate
    translated_point = point - self.position

    # rotate and return
    return Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

  def camera_space_vector(self, vector):
    return self.inverse_rotation_matrix.dot(vector)