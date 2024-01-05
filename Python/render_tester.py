from Render import Render
from Scene import Scene
from geometry import Ray_3D
from geometry import Point_3D, Vector_3D

from tkinter.filedialog import askopenfilename
import pickle
import time
# pixel tester

# pixel
pixel = [464, 464]


# load render
render_file = askopenfilename(initialdir='C:/Users/domho/Desktop/PhysicsEngine/renders/')

with open(render_file, 'rb') as f:
  render = pickle.load(f)

print(render.completed_chunks)
start = time.time()
print(render.scene.camera.render_individual_pixel(render, pixel))
print(time.time() - start)