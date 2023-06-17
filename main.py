import math
import pygame
import Camera
from colours import *
from Shapes import Sphere
from geometry import Point_3D, Rotation, Rotation_3D
from Lights import AmbientLight
pygame.init()

screen_width = 960
screen_height = 540
display_sizes = pygame.display.get_desktop_sizes()

display = 0

screen = pygame.display.set_mode((screen_width, screen_height), display=0)
pygame.display.set_caption("Physics Engine")

clock = pygame.time.Clock()
max_fps = 60

fullscreen = False

running = True

main_camera = Camera.Camera((960,540), 90, 10, (0,0,0), (0,0,0))

objects = [
  Sphere(Point_3D(50,50,-100), Rotation_3D(Rotation(0),Rotation(0),Rotation(0)), 10, RED)
]

light_sources = [
  AmbientLight((255,255,255), 1)
]
while running:
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
  canvas_px_info, canvas = main_camera.render_objects(objects, light_sources)
  quit()
  screen.blit(image_surface, (0, 0))

  clock.tick(max_fps)
  pygame.display.update()