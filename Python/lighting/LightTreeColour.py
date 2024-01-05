from surface_properties import Colour

# recursively calculate the colour of a lighting tree

# returns second position in list, used for key instead of lambda
def func1(x):
  return x[1]

def calc_colour(node, parent=None):
  Ia = Colour((0,0,0))
  Id = Colour((0,0,0))
  Is = Colour((0,0,0))

  for child in node.children: # only objects can have children, so child is assumed to be an obj class, object has to have a parent obj, so node is also obj (other than starting node)
    
    obj_light_colour = calc_colour(child, node)
    if parent == None: # if at start
      return obj_light_colour
    colour = node.value['colour']
    N = node.value['normal']
    normals = [N, N.inverse()]
    V = parent.value['position'] - node.value['position']
    
    if child.value['type'] == 'ambientlight':
      # multiply colour
      Ia += colour * child.value['colour'] * child.value['intensity']
      # print(f'Ia: {Ia.to_list()}')

    elif child.value['type'] in ['directionallight','pointlight','spotlight']:
      if child.value['type'] == 'directionallight':
        L = child.value['direction'].inverse()
      else:
        L = (child.value['position'] - node.value['position']).to_vector()
      N, NL_dot = max([[N, N.dot(L)] for N in normals], key=func1) # gets the correct normal for each surface
      R = 2 * NL_dot * N - L
      RV_dot = R.dot(V)

      light_total_colour = colour * child.value['colour'] * child.value['intensity'] * node.value['intensity']

      Id += light_total_colour * max(0, NL_dot) * (1-node.value['material'].smoothness) # the smoother the surface, the less diffusion light
      Is += light_total_colour * max(0, RV_dot)**node.value['material'].shininess * node.value['material'].smoothness # RV_dot is causing weird shadows

    elif child.value['type'] == 'obj':
      L = (child.value['position'] - node.value['position']).to_vector() # direction towards light
      N, NL_dot = max([[N, N.dot(L)] for N in normals], key=func1) # gets the correct normal for each surface
      R = 2 * NL_dot * N - L
      RV_dot = R.dot(V)


      # if this light is a reflecton, then intensity value is (1-transparency), if its refraction then its * transparency

      light_total_colour = colour * child.value['colour'] * node.value['intensity']


      Id += light_total_colour * max(0, NL_dot) * (1-node.value['material'].smoothness)
      Is += light_total_colour * max(0, RV_dot)**node.value['material'].shininess * node.value['material'].smoothness
      # print(f'Id: {Id.to_list()}')
      # print(f'Is: {Is.to_list()}')
    
  colour = Ia + Id + Is

  return colour


# color of transparent material
# object_colour * object_transparency * light_colour * light_intensity