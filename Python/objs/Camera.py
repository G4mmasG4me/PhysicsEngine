import math
from time import time, sleep
import sys

# from tkinter import Tk


from surface_properties import *
import pickle

import pygame
pygame.init()

# Custom Function Packages
import maths as maths
from matrix import xyz_matrix, inverse_matrix

# Custom Classes
from geometry import Point_2D, Point_3D, Vector_2D, Vector_3D
from geometry import Segment_2D, Segment_3D, Ray_2D, Ray_3D, Line_2D, Line_3D

from PIL import Image, ImageDraw

import random
from tqdm import tqdm
# from lighting import light_intensity_distance
from lighting import generate_lighting_tree
from Tree import TreeNode
from lighting import calc_colour
from chunking import chunking

from multiprocessing import Pool
import os

from numba import jit, cuda
from config import epsilon
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

  # calculates the vertical fov
  def calc_vfov(self):
    return math.degrees(2 * math.atan(math.tan(math.radians(self.hFOV)/2) * (self.resolution[1] / self.resolution[0])))
  
  # sets the rotation of the camera
  def change_rotation(self, rotation):
    self.rotation = rotation
    self.rotation_matrix = xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = inverse_matrix(self.rotation_matrix)
  
  # calculates the canvas size using focal length, hFOV and vFOV
  def calc_canvas_size(self):
    canvas_width =  2 * self.focal_length * math.tan(math.radians(self.hFOV)/2)
    canvas_height =  2 * self.focal_length * math.tan(math.radians(self.vFOV)/2)
    return [canvas_width, canvas_height]

  # calcualtes the pixel size given hFOV, resolution and focal length, assumes square pixel
  def pixel_size(self):
    '''
    Calculates Pixel Size
    '''
    canvas_width =  2 * self.focal_length * math.tan(math.radians(self.hFOV)/2)
    return canvas_width / self.resolution[0]
  
  # calculates the near plane, given focal length, in camera space
  def near_plane(self):
    '''
    Standard Near Plaen in Z Axis
    '''
    A = 0
    B = 0
    C = 1
    D = -self.focal_length
    return A, B, C, D

  # calculates the far plane   , given render distance, in camera space
  def far_plane(self):
    '''
    Standard Far Plane in Z Axis

    Parameters:
      self
    
    Returns:
      (float): plane x direction
      (float): plane y direction
      (float): plane z direction
      (float): plane distance from 0
    '''
    A = 0
    B = 0
    C = 1
    D = -self.render_distance
    return A,B,C,D
  
  def calculate_pixel_postions(self):
    '''
    Generates a list of canvas positions in camera space. Ignores z axis as plane is in the z axis
    '''
    pixel_positions = []
    for y in range(round(self.resolution[1]/2), -round(self.resolution[1]/2), -1):
      pixel_row = []
      for x in range(-round(self.resolution[0]/2), round(self.resolution[0]/2)):
        pixel_row.append(Point_3D(x*self.px_size, y*self.px_size, -self.focal_length))
      pixel_positions.append(pixel_row)
    return pixel_positions

  # changes resolution of camera
  def change_resolution(self, resolution):
    print('Now')
    self.resolution = resolution
    self.vFOV = self.calc_vfov()
    self.px_size = self.pixel_size()

  # changes fov of camera
  def change_FOV(self, FOV):
    self.hFOV = FOV
    self.vFOV = self.calc_vfov()

  def pixel_pos_to_canvas_pos(self, point):
    # takes in pixel position
    # returns canvas_pos
    point = [point[0] - self.resolution[0]/2, -(point[1] - self.resolution[1]/2)]
    point = Point_3D(point[0] * self.px_size, point[1] * self.px_size, -self.focal_length)
    return point

  # function used for multiprocessing as you can only pass one value
  def process_pixel(self, pixel):
    # unpacks list and runs through render_pixel function
    px, objects, light_sources, skyboxes, max_light_depth, render_method, split_light = pixel
    output = self.render_pixel(px, objects, light_sources, skyboxes, max_light_depth, render_method, split_light) # returns pixel, node, colour
    return output
  
  def render_individual_pixel(self, render, pixel_pos):
    start = time()
    self.change_resolution(render.resolution)
    print(f'Change Resolution Time: {time() - start}')

    start = time()
    # convert objects to cmaera space
    objects = [object.camera_space(self) for object in render.scene.objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in render.scene.light_sources]

    # convert skyboxes to camera_space
    skyboxes = [skybox.camera_space(self) for skybox in render.scene.skyboxes]
    print(f'Convert Objects Time: {time() - start}')

    start = time()
    pixel_point = self.pixel_pos_to_canvas_pos(pixel_pos)
    print(f'Get Pixel Point: {time() - start}')

    start = time()
    pixel = [[pixel_pos, pixel_point], objects, light_sources, skyboxes, render.max_light_depth, render.quality, render.split_light]
    print(f'Pack Pixel Value: {time() - start}')

    start = time()
    output = self.process_pixel(pixel)
    print(f'Process Pixel: {time() - start}')
    return output

  def render_objects_multiprocessing(self, render, processes, show=False, randomize_pixels=True, chunks=True, light_tree=True):
    fps = 60
    self.change_resolution(render.resolution)

    # convert objects to camera space
    objects = [object.camera_space(self) for object in render.scene.objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in render.scene.light_sources]

    # convert skyboxes to camera_space
    skyboxes = [skybox.camera_space(self) for skybox in render.scene.skyboxes]

    # load images if exists
    if os.path.exists(f'imgs/{render.name}.png'):
      image = Image.open(f'imgs/{render.name}.png')

      canvas = image.load()
      if render.split_light:
        Ia_image = Image.open(f'split_imgs/{render.name}_Ia.png')
        Id_image = Image.open(f'split_imgs/{render.name}_Id.png')
        Is_image = Image.open(f'split_imgs/{render.name}_Is.png')
        Ia_canvas = Ia_image.load()
        Id_canvas = Id_image.load()
        Is_canvas = Is_image.load()
      
    else: # create new images
      image = Image.new("RGB", (self.resolution[0], self.resolution[1]))
      square_size = 10  # Size of each square in the checkerboard
      canvas = image.load()
      if render.split_light:
        Ia_image = image.copy()
        Id_image = image.copy()
        Is_image = image.copy()
        Ia_canvas = Ia_image.load()
        Id_canvas = Id_image.load()
        Is_canvas = Is_image.load()

      for i in range(self.resolution[1]):
        # for every 100 pixels out of the total 500 
        # if its the first 50 pixels
        if (i % (square_size*2)) >= square_size:
          for j in range(self.resolution[0]):
            if (j % (square_size*2)) < square_size:
              canvas[i,j] = (0,0,0)
            else:
              canvas[i,j] = (50,50,50)

        # else its the second 50 pixels         
        else:
          for j in range(self.resolution[0]):
            if (j % (square_size*2)) >= square_size:
              canvas[i,j] = (0,0,0)
            else:
              canvas[i,j] = (50,50,50)
    if light_tree:
      lighting_tree_img = [[None for x in range(render.resolution[0])] for y in range(render.resolution[1])]
    
    # creates the data for each pixel and saves to list to be passed through ray tracing function
    pixel_positions = self.calculate_pixel_postions()
    size_in_bytes = sys.getsizeof(pixel_positions)
    for row in pixel_positions:
      size_in_bytes += sys.getsizeof(row)
      for data in row:
        size_in_bytes += sys.getsizeof(data)
    pixels = []
    for y_pos, pixel_row in enumerate(pixel_positions):
      row = []
      for x_pos, pixel_point in enumerate(pixel_row):
        row.append([[[x_pos, y_pos], pixel_point], objects, light_sources, skyboxes, render.max_light_depth, render.quality, render.split_light])
      pixels.append(row)

    # split into chunks if chunking is on
    pixel_chunks = chunking(pixels, render.chunk_size) if chunks else chunking(pixels, render.resolution)

    # get a list of uncompleted chunks
    pixel_chunks = pixel_chunks[render.completed_chunks:]
    print('showing')
    # create pygame window to show rendering
    if show:
      os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
      pygame.init()
      display_sizes = pygame.display.get_desktop_sizes()

      display_monitor = 0
      print(self.resolution[0], self.resolution[1])
      screen = pygame.display.set_mode((self.resolution[0], self.resolution[1]))
      print('test')
      pygame.display.set_caption("Rendering")

      pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
      screen.blit(pygame_image, (0, 0))

    print('finsihed loading pygame window')
    # calculate number of remaining and completed pixels
    total_pixels_remaining = sum([len(chunk) for chunk in pixel_chunks])
    completed_pixels = self.resolution[0] * self.resolution[1] - total_pixels_remaining

    # create progress bar with max being total amount of pixels
    with tqdm(total=(self.resolution[0] * self.resolution[1]), initial=completed_pixels) as pbar:
      # create pool
      pool = Pool(processes=processes)

      # loop through chunks
      for chunk_num, pixel_chunk in enumerate(pixel_chunks):
        if show and randomize_pixels:
          random.shuffle(pixel_chunk)
        t_last_frame = time()
        for result in pool.imap(self.process_pixel, pixel_chunk):
          
          # retrives results and splits them
          pixel, node, colour = result
          pos, point = pixel
          x_pos, y_pos = pos

          # saves colours to canvases, and nodes to light_trees
          canvas[x_pos, y_pos] = colour[0].to_tuple()
          if render.split_light:
            Ia_canvas[x_pos, y_pos] = colour[1].to_tuple()
            Id_canvas[x_pos, y_pos] = colour[2].to_tuple()
            Is_canvas[x_pos, y_pos] = colour[3].to_tuple()
          if light_tree:
            lighting_tree_img[y_pos][x_pos] = node
            
          # if show is true, then renders each pixel to pygame window
          if show:
            for event in pygame.event.get():
              if event.type == pygame.QUIT:
                    pygame.quit()
            if time() - t_last_frame > 1 / fps:
              t_last_frame = time()
              """screen.set_at((x_pos, y_pos), colour[0].to_tuple())"""
              pygame_image = pygame.image.fromstring(image.tobytes(), image.size, image.mode)
              screen.blit(pygame_image, (0, 0))
              pygame.display.update()

          # updates progress bar
          pbar.update()

        # save images after each chunk
        image.save(f'imgs/{render.name}.png')
        if render.split_light:
          Ia_image.save(f'split_imgs/{render.name}_Ia.png')
          Id_image.save(f'split_imgs/{render.name}_Id.png')
          Is_image.save(f'split_imgs/{render.name}_Is.png')

        if light_tree:
          with open(f'light_trees/{render.name}.pkl', 'wb') as f:
            pickle.dump(lighting_tree_img, f)
        
        # save render obj
        render.completed_chunks += 1
        with open(f'renders/{render.name}.pkl', 'wb') as f:
          pickle.dump(render, f)

      # close pool
      pool.close()
      pool.join()

    return [], image
  
  def render_pixel(self, pixel, objects, light_sources, skyboxes, max_light_depth, render_method, split_light):
    pos, pixel_point = pixel
    x_pos, y_pos = pos
    pixel_dir = pixel_point.to_vector()

    main_node = TreeNode({'type':'cam', 'position':Point_3D(0,0,0)})
    node, colour = generate_lighting_tree(main_node, pixel_dir, objects, light_sources, skyboxes, max_light_depth, render_method, split_light)
    return pixel, node, colour
  
  def camera_space_point(self, point):
    # translate
    translated_point = point - self.position

    # rotate and return
    return Point_3D(*self.inverse_rotation_matrix.dot([translated_point.x, translated_point.y, translated_point.z]))

  def camera_space_vector(self, vector):
    return self.inverse_rotation_matrix.dot(vector)
  
  def change_screen_colour(screen, position, colour):
    screen.set_at((position[0], position[1]), colour[0].to_tuple())

  
  @cuda.jit
  def process_batch_gpu(self, screen, inputs, outputs):
    idx = cuda.grid(1)

    if idx < len(inputs):
      pixel, node, colour = self.process_pixel(inputs[idx])
      outputs[idx] = [pixel, node, colour]
      
      # change screen pixel colour 
      self.change_screen_colour(screen, pixel[0], colour)

  def render_objects_gpu(self, render):
    self.change_resolution(render.resolution)

    # convert objects to camera space
    objects = [object.camera_space(self) for object in render.scene.objects]

    # convert light sources to camera space
    light_sources = [light_source.camera_space(self) for light_source in render.scene.light_sources]

    # convert skyboxes to camera_space
    skyboxes = [skybox.camera_space(self) for skybox in render.scene.skyboxes]

    # calculates the camera space pixel positions in 3d
    pixel_positions = self.calculate_pixel_postions()

    # generate chunks
    pixels = []
    for y_pos, pixel_row in enumerate(pixel_positions):
      row = []
      for x_pos, pixel_point in enumerate(pixel_row):
        row.append([[[x_pos, y_pos], pixel_point], objects, light_sources, skyboxes, render.max_light_depth, render.quality, render.split_light])
      pixels.append(row)

    # split into chunks if chunking is on
    chunks = True
    if chunks:
      pixel_chunks = chunking(pixels, render.chunk_size)
    else:
      pixel_chunks = chunking(pixels, render.resolution)
    pixel_chunks = pixel_chunks[render.completed_chunks:]

    threads_per_block = 128 # max 1024
    for chunk in pixel_chunks:
      outputs = [None for _ in chunk]

      batch_size = len(chunk)
      blocks_per_grid = (batch_size + threads_per_block - 1) // threads_per_block

      d_inputs = cuda.to_device(chunk)
      d_outputs = cuda.to_device(outputs)


      self.process_batch_gpu[blocks_per_grid, threads_per_block](d_inputs, d_outputs)

      d_outputs.copy_to_host(outputs)
    pass


  def render_wireframe(self, render):
    self.change_resolution(render.resolution)

    # convert objects to camera space
    objects = [object.camera_space(self) for object in render.scene.objects]

    # create image
    image = Image.new("RGB", (self.resolution[0], self.resolution[1]))
    draw = ImageDraw.Draw(image)

    for object in objects:
      if hasattr(object.geometry, 'faces') and hasattr(object.geometry, 'vertices'):
        lines = []
        for face in object.geometry.faces:
          lines += face.lines()
        

        for line in lines:
          p1 = object.object_space(line.p1)
          p2 = object.object_space(line.p2)
          # convert each vertex to screen_space
          p1 = self.screen_space_point(p1)
          p2 = self.screen_space_point(p2)
          draw.line(((p1.x, p1.y), (p2.x, p2.y)), fill="green", width=2)
          # print('Drawing From: (%s,%s) To (%s,%s)' % (p1.x, p1.y, p2.x, p2.y))
    return image

  def screen_space_point(self, point):
    x = (point.x / point.z) / math.tan(self.hFOV/2)
    y = (point.y / point.z) / math.tan(self.hFOV/2)
    z = point.z

    screen_x = (x + 1) * self.resolution[0] / 2
    screen_y = (y + 1) * self.resolution[1] / 2
    screen_z = z

    return Point_3D(screen_x,screen_y,screen_z)