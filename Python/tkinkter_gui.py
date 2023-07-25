import tkinter as tk
from tkinter import Button, Label, Entry
from tkinter import filedialog as fd

from Material import Material
import pickle

class Widget:
  def __init__(self, id, type, value, pos):
    self.id = id
    self.type = type
    self.value = value
    self.pos = pos

widgets = []

m = tk.Tk()

def material_save():
  file_name = f'materials/{material_name.get()}.pkl'
  mat = Material(float(material_roughness.get()), float(material_shininess.get()), float(material_emission.get()), float(material_transparency.get()))
  with open(file_name, 'wb') as f:
    pickle.dump(mat, f)

def material_load():
  file_name = fd.askopenfilename()
  with open(file_name, 'rb') as f:
    mat = pickle.load(f)
  mat_name = file_name.split('/')[-1].split('.')[0]
  material_name.insert(0, mat_name)
  material_roughness.insert(0, mat.roughness)
  material_shininess.insert(0, mat.shininess)
  material_emission.insert(0, mat.emission)
  material_transparency.insert(0, mat.transparency)



def add_object():
  objects_widgets.append(Widget('geometry_name_1'))

camera_widgets = []
objects_widgets = []
lights_widgets = []
materials_widgets = []

# camera widgets
resolution_text = Label(m, text='Resolution')
camera_section.append([resolution_text, [1,0]])

resolution_x = Label(m, text='x')
camera_section.append([resolution_x, [1,2]])

resolution_width = Entry(width=10)
camera_section.append([resolution_width, [1,1]])

resolution_height = Entry(width=10)
camera_section.append([resolution_height, [1,3]])


# objects widget
add_object_button = Button(m, 'Add Object', width=10, command=add_object)







# materials widgets
material_name_text = Label(text='Name', width=10)
materials_section.append([material_name_text, [2,0]])

material_name = Entry(width=10)
materials_section.append([material_name, [2,1]])

material_roughness_text = Label(text="Roughness", width=10)
materials_section.append([material_roughness_text, [3,0]])

material_roughness = Entry(width=10)
materials_section.append([material_roughness, [3,1]])

material_shininess_text = Label(text="Shininess", width=10)
materials_section.append([material_shininess_text, [4,0]])

material_shininess = Entry(width=10)
materials_section.append([material_shininess, [4,1]])

material_emission_text = Label(text="Emission", width=10)
materials_section.append([material_emission_text, [5,0]])

material_emission = Entry(width=10)
materials_section.append([material_emission, [5,1]])

material_transparency_text = Label(text="Transparency", width=10)
materials_section.append([material_transparency_text, [6,0]])

material_transparency = Entry(width=10)
materials_section.append([material_transparency, [6,1]])

material_save_button = Button(m, text='Save', width=10, command=material_save)
materials_section.append([material_save_button, [1,0]])

material_load_button = Button(m, text='Load', width=10, command=material_load)
materials_section.append([material_load_button, [1,1]])

def open_camera():
  # hide all other objects
  for obj in objects_section + lights_section + materials_section:
    if obj[0].grid_info():
      obj[0].grid_forget()
  # show all camera objs
  for obj in camera_section:
    obj[0].grid(row=obj[1][0], column=obj[1][1])

def open_objects():
  for obj in camera_section + lights_section + materials_section:
    if obj[0].grid_info():
      obj[0].grid_forget()
  # show all object objs
  for obj in objects_section:
    obj[0].grid(row=obj[1][0], column=obj[1][1])

def open_lights():
  for obj in camera_section + objects_section + materials_section:
    if obj[0].grid_info():
      obj[0].grid_forget()
  # show all lights objs
  for obj in lights_section:
    obj[0].grid(row=obj[1][0], column=obj[1][1])

def open_materials():
  for obj in camera_section + objects_section + lights_section:
    if obj[0].grid_info():
      obj[0].grid_forget()
  # show all materials objs
  for obj in materials_section:
    obj[0].grid(row=obj[1][0], column=obj[1][1])


m.title('Material Creator')

camera_button = Button(m, text='Camera', width=10, command=open_camera)
objects_button = Button(m, text='Objects', width=10, command=open_objects)
lights_buttons = Button(m, text='Light', width=10, command=open_lights)
materials_button = Button(m, text='Materials', width=10, command=open_materials)
camera_button.grid(row=0, column=0)
objects_button.grid(row=0, column=1)
lights_buttons.grid(row=0, column=2)
materials_button.grid(row=0, column=3)


open_materials()
m.mainloop()