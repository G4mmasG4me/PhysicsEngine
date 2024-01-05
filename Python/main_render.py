from time import time
import multiprocessing

from surface_properties import Colour

import pickle
from tkinter.filedialog import askopenfilename
from tkinter import Tk
root = Tk()
from Scene import Scene
from Render import Render
import pygame
pygame.init()



import cProfile
processes = 8 # set the number of simulataneous processes
resolution = (500,500) # set resolution in pixels

max_light_depth = 4 # set max light depth
quality = 'high' # set render method
split_light = False # if true creates 4 seperate images for combined, ambient, diffusion and specular light
chunk_size = (50,50) # set chunk size
show = True
profiler = False

if __name__ == '__main__':
  # select and load the scene or render
  scene_render_file = askopenfilename(initialdir='/renders/')
  with open(scene_render_file, 'rb') as f:
    scene_render = pickle.load(f)
  
  # if the file is a Scene class, then create a scene out of it and save
  if isinstance(scene_render, Scene):
    name = input('Choose Name:')
    scene_render = Render(name, resolution, scene_render, max_light_depth, quality, split_light, chunk_size, 0)
    with open(f'renders/{scene_render.name}.pkl', 'wb') as f:
      pickle.dump(scene_render, f)

  start = time()
  # start rendering
  scene_render.change_show(show)
  if profiler:
    cProfile.runctx('g(x)', {'g': scene_render.start_rendering, 'x': processes}, {})
  else:
    scene_render.start_rendering(processes)
  print(f'Time To Produce Frame: {time() - start}')