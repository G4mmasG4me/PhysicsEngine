import math

import pygame
from time import time

from Colour import *

import pickle

from Scene import Scene
import os


if __name__ == '__main__':
  os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,100)
  pygame.init()

  screen_width = 500
  screen_height = 500
  display_sizes = pygame.display.get_desktop_sizes()
  

  display = 0


  clock = pygame.time.Clock()
  max_fps = 60

  fullscreen = False

  running = True
  show_display = False

  if show_display:
    screen = pygame.display.set_mode((screen_width, screen_height), display=0)
    pygame.display.set_caption("Physics Engine")

  scene = input('What scene do you want to use?')
  scene_name = f'scenes/{scene}.pkl'

  with open(scene_name, 'rb') as file:
    scene = pickle.load(file)

  main_camera = scene.camera
  objects = scene.objects
  light_sources = scene.light_sources

  main_camera.change_resolution((screen_width, screen_height))
  while running:
    if show_display:
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          pygame.quit()
        elif event.type == pygame.VIDEORESIZE:
          # Update the screen dimensions
          screen_width, screen_height = event.w, event.h
          screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
          main_camera.change_resolution([screen_width, screen_height])
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

    # reset and update camera
    
    # physics engine camera
    # need to render lines

    # render object
    start = time()
    canvas_px_info, canvas = main_camera.render_objects_multiprocessing(objects, light_sources, 5, True, False)
    print(f'Time To Produce Frame: {time() - start}')
    if show_display:  
      pygame_image = pygame.image.fromstring(canvas.tobytes(), canvas.size, canvas.mode)
      screen.blit(pygame_image, (0, 0))
      clock.tick(max_fps)
      print(f'FPS: {clock.get_fps()}')
      pygame.display.update()
    else:
      quit()