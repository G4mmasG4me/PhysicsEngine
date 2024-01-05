import pickle

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, PhotoImage
from lighting import generate_lighting_tree
from Tree import TreeNode
from geometry import Point_3D
from Scene import Scene


def get_pixel_position(event):
  x = event.x // scale_factor
  y = event.y // scale_factor
  pixel = org_img.get(x, y)
  print(f"Pixel position: ({x}, {y})")
  print(f"RGB values: {pixel}")
  img_light_tree[y][x].output(['type', 'position', 'final_colour', 'colour'])
  print('Lighting Tree Gen For This Pixel')
  ray_dir = img_light_tree[y][x].children[0].value['position'].to_vector().normalise()
  base_node = TreeNode({'type':'cam', 'position':Point_3D(0,0,0)})
  generate_lighting_tree(base_node, ray_dir, objects, light_sources, skyboxes, 5, 'high')

scene = input('What scene do you want to use?')
scene_name = f'scenes/{scene}.pkl'

with open(scene_name, 'rb') as file:
  scene = pickle.load(file)

main_camera = scene.camera
objects = scene.objects
light_sources = scene.light_sources
skyboxes = scene.skyboxes

root = Tk()
light_tree_file = askopenfilename(initialdir='C:/Users/domho/Desktop/PhysicsEngine/light_trees/')
with open(light_tree_file, 'rb') as file:
  img_light_tree = pickle.load(file)

file_name = light_tree_file.split('/')[-1].split('.')[0]

img_file = 'C:/Users/domho/Desktop/PhysicsEngine/imgs/' + file_name + '.png'

scale_factor = 1  # Adjust this factor as needed

org_img = PhotoImage(file=img_file)

image = org_img.zoom(scale_factor, scale_factor)
canvas = Canvas(root, width=image.width(), height=image.height())
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=image)

canvas.bind("<Button-1>", get_pixel_position)

root.mainloop()