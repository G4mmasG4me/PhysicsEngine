from tkinter import Tk
root = Tk()

from time import time

from surface_properties import Colour

import pickle
from tkinter.filedialog import askopenfilename

from Scene import Scene
from Render import Render

import pygame
from geometry import Point_3D
from geometry import Rotation
pygame.init()



processes = 8
resolution = (1000,1000) # set resolution

max_light_depth = 4
quality = 'high'
split_light = True
chunk_size = (100,100)

scripts = []
running = True

display = pygame.display.set_mode(resolution)

current_mouse_pos = None
previous_mouse_pos = None
if __name__ == '__main__':

  scene_render_file = askopenfilename(initialdir='C:/Users/domho/Desktop/PhysicsEngine/scenes/')

  with open(scene_render_file, 'rb') as f:
    scene_render = pickle.load(f)
  
  if isinstance(scene_render, Scene):
    scene_render = Render('game', resolution, scene_render, max_light_depth, quality, split_light, chunk_size, 0)
  
  while running:
    for event in pygame.event.get():
      if event.type == pygame.quit:
        running = False
      elif event.type == pygame.KEYDOWN:
        if event.key == pygame.K_w:
          scene_render.scene.camera.position += Point_3D(0,1,0)
        if event.key == pygame.K_s:
          scene_render.scene.camera.position += Point_3D(0,-1,0)
        if event.key == pygame.K_d:
          scene_render.scene.camera.position += Point_3D(-1,0,0)
        if event.key == pygame.K_a:
          scene_render.scene.camera.position += Point_3D(1,0,0)
    
    current_mouse_pos = pygame.mouse.get_pos()
    if previous_mouse_pos:
      mouse_pos_change = (current_mouse_pos[0] - previous_mouse_pos[0], current_mouse_pos[1] - previous_mouse_pos[1])
      scene_render.scene.camera.rotation.x += Rotation(mouse_pos_change[1]/10, 'deg')
      scene_render.scene.camera.rotation.y += Rotation(-mouse_pos_change[0]/10, 'deg')
    previous_mouse_pos = current_mouse_pos
    display.fill('WHITE')

    image = scene_render.scene.camera.render_wireframe(scene_render)
    image_str = image.tobytes('raw', image.mode)
    pygame_image = pygame.image.fromstring(image_str, image.size, image.mode)
    display.blit(pygame_image, (0,0))
    pygame.display.update()
  pygame.quit()