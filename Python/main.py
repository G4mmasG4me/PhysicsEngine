import math
import pygame
from time import time

# Custom Packages
import Camera

from Object import Object

from Lights import AmbientLight, SpotLight, PointLight, DirectionalLight
from Shapes import Sphere, Cuboid, Infinte_Plane
from Material import Material
from Texture import Texture, default_texture

from Points import Point_3D, Vector_3D
from Rotation import Rotation_3D, Rotation

from Colour import Colour


pygame.init()

screen_width = 250
screen_height = 250
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

main_camera = Camera.Camera((screen_width,screen_height), 90, 10, Point_3D(0,0,0), Rotation_3D(Rotation(0),Rotation(0),Rotation(0)))

half_rough = Material(0.5, 0, 0, 0)

red = Colour((255,0,0))
blue = Colour((0,0,255))
green = Colour((0,255,0))
light_green = Colour((0,200,0))
white = Colour((255,255,255))
grey = Colour((100,100,100))
purple = Colour((255,0,255))

chessboard_1 = Texture('textures/chessboard_1.png')
chessboard_2 = Texture('textures/chessboard_2.png')
chessboard_3 = Texture('textures/chessboard_3.png')

default_texture_2 = Texture('textures/default.png', 2)
default_texture_3 = Texture('textures/default.png', 0.1)

objects = [
  Object(Sphere(5), Point_3D(0,15,-50), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, chessboard_2, None, 1),
  Object(Cuboid([5,5,5]), Point_3D(0,10,-50), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, red, None, 1),
  Object(Sphere(5), Point_3D(0,5,-50), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, chessboard_1, None, 1),
  Object(Infinte_Plane(), Point_3D(0,-10,0), Rotation_3D(Rotation(90, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, default_texture_2, None, 1)
]

light_sources = [
  AmbientLight(white, 0.5),
  DirectionalLight(Vector_3D(-1,0,-1), white, 0.5)
]

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
  canvas_px_info, canvas = main_camera.render_objects(objects, light_sources)
  print(f'Time To Produce Frame: {time() - start}')
  if show_display:  
    pygame_image = pygame.image.fromstring(canvas.tobytes(), canvas.size, canvas.mode)
    screen.blit(pygame_image, (0, 0))
    clock.tick(max_fps)
    print(f'FPS: {clock.get_fps()}')
    pygame.display.update()
  else:
    quit()