from PIL import Image

class Material_Map:
  """
  Contains the mapping of a certain material
  """
  def __init__(self, uv_maps, materials, scale):
    self.uv_map_path = uv_maps # list of uv map paths
    self.uv_maps = [Image.open(uv_map_path) for uv_map_path in uv_maps]
    uv_map_sizes = [uv_map.size for uv_map in self.uv_maps]
    if uv_map_sizes.count(uv_map_sizes[0]) == len(uv_map_sizes):
      self.uv_map_size = uv_map_sizes[0]
    else:
      raise ValueError('UV Maps differ in resolution | All UV maps must be the same resolution')
    if len(self.uv_maps) != len(materials):
      raise ValueError('Number of UV maps and materials differ | Num of UV maps and materials must be the same')
    self.materials = materials # list of materials
    self.material_scale = scale

  def get_material(self, uv):
    if self.uv_maps and self.materials:
      for uv_map in self.uv_maps:
        uv_map.getpixel(uv.to_list())
    else:
      return default_material


class Material:
  """
  A material object with 4 values, roughness, shininess, emission and transparency
  """
  def __init__(self, roughness, shininess, emission, transparency):
    """
    Initialize Material Object
    
    Paramters:
      roughness: float value between 0 and 1
      shininess: float value between 0 and 1
      emission: float value between 0 and 1
      transparency: float value between 0 and 1
    """
    self.roughness = roughness # to do with reflectiveness
    self.shininess = shininess # specular reflection coefficient
    self.emission = emission # glow
    self.transparency = transparency

default_material = Material(0.5, 0, 0, 0)
glass = Material(0.1,0,0,0.9)
mirror = Material(0.1,0,0,0)
normal = Material(0.5,0,0,0)
rough = Material(0.9,0,0,0)
very_rough = Material(0.95,0,0,0)