import pickle
import os
from objs import Camera

class Render:
  def __init__(self, name, resolution, scene, max_light_depth, quality, split_light, chunk_size, completed_chunks):
    self.name = name
    self.resolution = resolution
    self.scene = scene
    self.max_light_depth = max_light_depth
    self.quality = quality
    self.split_light = split_light
    self.chunk_size = chunk_size
    self.completed_chunks = completed_chunks
    self.show = True

  def save(self):
    with open(f'renders/{self.name}.pkl', 'wb') as f:
      pickle.dump(self, f)

  def validate(self):
    if not os.path.exists(f'imgs/{self.name}.png'):
      return False
    
    if self.split_lights:
      if not os.path.exists(f'split_imgs/{self.name}_Ia.png') or not os.path.exists(f'split_imgs/{self.name}_Is.png') or not os.path.exists(f'split_imgs/{self.name}_Id.png'):
        return False
    return True
  
  def change_show(self, show):
    self.show = show

  def start_rendering(self, processes):
    print('Starting Rendering')
    self.scene.camera.render_objects_multiprocessing(self, processes, self.show, True, True, False)