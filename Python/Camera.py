import math

from Colour import *
import pickle

import pygame

# Custom Function Packages
import maths as maths
from matrix import xyz_matrix, inverse_matrix

# Custom Classes
from Points import Point_2D, Point_3D, Vector_2D, Vector_3D
from Lines import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D

from PIL import Image, ImageDraw

import random
from tqdm import tqdm
from light_equations import light_intensity_distance
from LightingTreeGen import generate_lighting_tree
from Tree import TreeNode
from LightTreeColour import calc_colour

from multiprocessing import Pool
import os

def process_pixel(pixel):
  px, objects, light_sources, max_light_depth = pixel
  
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

  def render_objects(self, objects, light_sources, max_light_depth, show=False):
    # convert objects to camera space
    objects = [object.camera_space(self) for object in objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in light_sources]
    

    image1 = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    image2 = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    canvas1 = image1.load()
    canvas2 = image2.load()
    lighting_tree_img = [[None for x in range(self.resolution[0])] for y in range(self.resolution[1])]

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
      pixel_dir = Vector_3D(pixel_point[0], pixel_point[1], -self.focal_length)
      main_node = TreeNode({'type':'cam', 'position':Point_3D(0,0,0)})
      node, colour2 = generate_lighting_tree(main_node, pixel_dir, objects, light_sources, max_light_depth)
      colour1 = calc_colour(main_node)
      canvas1[x_pos, y_pos] = tuple(colour1.to_list())
      canvas2[x_pos, y_pos] = tuple(colour2.to_list())
      lighting_tree_img[y_pos][x_pos] = main_node

    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_file_name = ''
    for i in range(16):
      random_file_name += random.choice(chars)

    img_name_1 ='imgs/' + random_file_name + '_1.png'
    img_name_2 ='imgs/' + random_file_name + '_2.png'
    lighting_file_name = 'light_trees/' + random_file_name + '.pkl'

    image1.save(img_name_1)
    image2.save(img_name_2)
    with open(lighting_file_name, 'wb') as file:
      pickle.dump(lighting_tree_img, file)
    
    print(f'Saved Img: {img_name_1}')
    print(f'Saved Img: {img_name_2}')
    print(f'Saved Lighting Tree: {lighting_file_name}')
    return [], image1

  def process_pixel(self, pixel):
    px, objects, light_sources, max_light_depth = pixel
    return self.render_pixel(px, objects, light_sources, max_light_depth)

  def render_objects_multiprocessing(self, objects, light_sources, max_light_depth, show=False, randomize_pixels=True):
    
    # convert objects to camera space
    objects = [object.camera_space(self) for object in objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in light_sources]
    
    image = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    draw = ImageDraw.Draw(image)
    square_size = 10  # Size of each square in the checkerboard
    num_squares_x = self.resolution[0] // square_size
    num_squares_y = self.resolution[1] // square_size

    for i in range(num_squares_x):
      for j in range(num_squares_y):
        x = i * square_size
        y = j * square_size
        if (i + j) % 2 == 0:
          color = "grey"
        else:
          color = "white"
          draw.rectangle([x, y, x + square_size, y + square_size], fill=color)
    canvas = image.load()
    lighting_tree_img = [[None for x in range(self.resolution[0])] for y in range(self.resolution[1])]

    # simple ray tracing, only one intersection
    pixel_positions = self.calculate_pixel_postions()

    pixels = []
    for y_pos, pixel_row in enumerate(pixel_positions):
      for x_pos, pixel_point in enumerate(pixel_row):
        pixels.append([[[x_pos, y_pos], pixel_point], objects, light_sources, max_light_depth])
    if randomize_pixels:
      random.shuffle(pixels)

    
    results = []

    if show:
      os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
      pygame.init()
      display_sizes = pygame.display.get_desktop_sizes()

      display = 0
      screen = pygame.display.set_mode((self.resolution[0], self.resolution[1]), display=0)
      pygame.display.set_caption("Rendering")

      pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
      screen.blit(pygame_image, (0, 0))

    
    with tqdm(total=len(pixels)) as pbar:
      pool = Pool(processes=4)
      for i, result in enumerate(pool.imap(self.process_pixel, pixels)):
        if show:
          for event in pygame.event.get():
            if event.type == pygame.QUIT:
              pygame.quit()
            elif event.type == pygame.VIDEORESIZE:
              # Update the screen dimensions
              screen_width, screen_height = event.w, event.h
              screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
              self.change_resolution([screen_width, screen_height])
            elif event.type == pygame.KEYDOWN:
              if event.key == pygame.K_f:
                # Toggle fullscreen mode
                fullscreen = not fullscreen
                if fullscreen:
                  pygame.quit()
                  pygame.init()
                  screen = pygame.display.set_mode(pygame.display.get_desktop_sizes()[display], pygame.FULLSCREEN, display=0)
                else:
                  screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

        pixel, node, colour = result
        pos, point = pixel
        x_pos, y_pos = pos

        canvas[x_pos, y_pos] = colour.to_tuple()
        lighting_tree_img[y_pos][x_pos] = node
        if show:
          screen.set_at((x_pos, y_pos), colour.to_tuple())
          pygame.display.update()
        pbar.update()

    pool.close()
    pool.join()

    chars = 'abcdefghijklmnopqrstuvwxyz1234567890'
    random_file_name = ''
    for i in range(16):
      random_file_name += random.choice(chars)

    img_name ='imgs/' + random_file_name + '.png'
    lighting_file_name = 'light_trees/' + random_file_name + '.pkl'

    image.save(img_name)
    with open(lighting_file_name, 'wb') as file:
      pickle.dump(lighting_tree_img, file)
    
    print(f'Saved Img: {img_name}')
    print(f'Saved Lighting Tree: {lighting_file_name}')
    return [], image


  def render_pixel(self, pixel, objects, light_sources, max_light_depth):
    pos, pixel_point = pixel
    x_pos, y_pos = pos
    pixel_dir = Vector_3D(pixel_point[0], pixel_point[1], -self.focal_length)
    main_node = TreeNode({'type':'cam', 'position':Point_3D(0,0,0)})
    node, colour = generate_lighting_tree(main_node, pixel_dir, objects, light_sources, max_light_depth)
    return pixel, node, colour
  
  def camera_space_point(self, point):
    # translate
    translated_point = point - self.position

    # rotate and return
    return Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

  def camera_space_vector(self, vector):
    return self.inverse_rotation_matrix.dot(vector)