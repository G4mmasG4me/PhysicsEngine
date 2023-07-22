import pickle

from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from tkinter import Tk, Canvas, PhotoImage
from LightTreeColour import calc_colour

def get_pixel_position(event):
  x = event.x // scale_factor
  y = event.y // scale_factor
  pixel = org_img.get(x, y)
  print(f"Pixel position: ({x}, {y})")
  print(f"RGB values: {pixel}")
  img_light_tree[y][x].output(['type', 'position', 'final_colour'])

root = Tk()
light_tree_file = askopenfilename(initialdir='C:/Users/domho/Desktop/Projects/PhysicsEngine/light_trees/')
with open(light_tree_file, 'rb') as file:
  img_light_tree = pickle.load(file)

file_name = light_tree_file.split('/')[-1].split('.')[0]

img_file = 'C:/Users/domho/Desktop/Projects/PhysicsEngine/imgs/' + file_name + '_2.png'

scale_factor = 1  # Adjust this factor as needed

org_img = PhotoImage(file=img_file)

image = org_img.zoom(scale_factor, scale_factor)
canvas = Canvas(root, width=image.width(), height=image.height())
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=image)

canvas.bind("<Button-1>", get_pixel_position)

root.mainloop()