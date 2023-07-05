from Tree import TreeNode
from Points import Point_3D, Vector_3D
from Lines import Ray_3D, Segment_3D
from light_equations import reflected_ray_dir, refracted_ray_dir, ray_inside_outside_detection
import pickle



pixels = []
objects = []
lights = []

air_refractive_index = 1.000293

def generate_lighting_tree(node, direction, objs, lighting, max_depth, current_depth=0, refraction_stack=[]):
  primary_ray = Ray_3D(node.value[1], direction)
  primary_ray.output()
  intersections = [] # position, normal, distance, colour, material, refractive index

  # find all intersections
  for obj in objs:
    intersections += obj.intersection(primary_ray)
  
  if intersections:
    # get closest intersection
    closest_intersection = min(intersections, key=lambda x: x[2])

    obj_intersection, obj_normal, distance, obj_colour, obj_material, obj_refractive_index, intersection_obj = closest_intersection
    obj_node = TreeNode(['obj', obj_intersection, obj_normal, obj_colour, obj_material])
    node.add_child(obj_node)

    # split light sources
    sorted_light_sources = {'AmbientLight':[], 'PointLight':[], 'SpotLight':[], 'DirectionalLight':[]}
    for item in light_sources:
      item_type = type(item).__name__
      sorted_light_sources[item_type].append(item)

    for light in sorted_light_sources['AmbientLight']:
      ambient_light_node = TreeNode(['ambientlight', light.colour, light.intensity])
      obj_node.add_child(ambient_light_node)

    

    for light in sorted_light_sources['PointLight']:
      
      segment = Segment_3D(obj_intersection, light.point)
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(segment)
        light_obstructed = any([value is not None for value in light_intersections])
        if not light_obstructed:
          pointlight_node = TreeNode(['pointlight', light.position, light.colour, light.intensity])
          obj_node.add_child(pointlight_node)

    spotlights = sorted_light_sources['SpotLight']
    valid_spotlights = [spotlight for spotlight in spotlights if spotlight.facing_direction(obj_intersection - spotlight.position)]
    for light in valid_spotlights:
      segment = Segment_3D(obj_intersection, light.point)
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(segment)

      light_obstructed = any([value is not None for value in light_intersections])
      if not light_obstructed:
        spotlight_node = TreeNode(['spotlight', light.position, light.colour, light.intensity])
        obj_node.add_child(spotlight_node)


    for light in sorted_light_sources['DirectionalLight']:
      ray = Ray_3D(obj_intersection, light.direction.inverse())
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(ray)
      
      light_obstructed = any([value is not None for value in light_intersections])
      if not light_obstructed:
        directionallight_node = TreeNode(['directionallight', light.direction, light.colour, light.intensity])
        obj_node.add_child(directionallight_node)

  
    """ for light in sorted_light_sources['DirectionalLight'] + sorted_light_sources['SpotLight'] + sorted_light_sources['PointLight']:
      # indirect illumination
      # 1 bounce
      reflections = []
      for object in objects:

        # check for one bounce reflection
        reflections += object.one_bounce_illumination(light, obj_intersection)

        # loop through reflections
        for reflection in reflections:
          reflection_point, normal, colour = reflection
          light_reflection_segment = Segment_3D(reflection_point, light.position)
          obj_intersection_reflection_segment = Segment_3D(reflection_point, obj_intersection)

          light_intersections = []
          # check for blockages
          for obj in objects:
            light_intersections += obj.intersection(light_reflection_segment, True)
            light_intersections += obj.intersection(obj_intersection_reflection_segment, True)
          light_obstructed = any([value is not None for value in light_intersections])
          if not light_obstructed:
            print('Creating Indirect Reflection Node')
            reflection_tree_node = TreeNode('obj', reflection_point, normal, colour)
            light_tree_node = TreeNode('light', light_point, light_colour, light_intensity)

            # add tree nodes
            reflection_tree_node.add_child(light_tree_node)
            node.add_child(reflection_tree_node) """

    # see if object is entering or leaving object
    if current_depth < max_depth:
      
      # generate_reflecion ray
      if obj_material.smoothness > 0:
        reflected_ray = reflected_ray_dir(primary_ray, obj_normal)
        
        new_node = generate_lighting_tree(obj_node, reflected_ray, objs, lighting, max_depth, current_depth+1, refraction_stack)

      # generate refraction ray
      if obj_material.transparency > 0: # only refracts if transparent
        inside_outside = ray_inside_outside_detection(primary_ray, intersection_obj)
        if inside_outside == 'inside': # ray leaving object
          refractive_index_1 = refraction_stack.pop()
          if refraction_stack:
            refractive_index_2 = refraction_stack[-1]
          else:
            refractive_index_2 = air_refractive_index

        elif inside_outside == 'outside': # ray entering object
          if refraction_stack:
            refractive_index_1 = refraction_stack[-1]
          else:
            refractive_index_1 = air_refractive_index
          refractive_index_2 = obj_refractive_index
          refraction_stack.append(obj_refractive_index)

        refracted_ray = refracted_ray_dir(primary_ray, obj_normal, refractive_index_1, refractive_index_2)
        new_node = generate_lighting_tree(obj_node, refracted_ray, objs, lighting, max_depth, current_depth+1, refraction_stack)
  
  return node


from Object import Object
from Rotation import Rotation_3D, Rotation
from Shapes import Sphere, Cuboid, Infinte_Plane
from Lights import AmbientLight, DirectionalLight
from Colour import Colour
from Material import Material
from Texture import Texture

half_rough = Material(0.5, 0, 0, 0.5)

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
  Object(Sphere(5), Point_3D(0,0,-50), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, chessboard_1, None, 1.2),
  Object(Sphere(5), Point_3D(0,0,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, half_rough, chessboard_1, None, 1.2),
]

white
light_sources = [
  AmbientLight(white, 0.5),
  DirectionalLight(Vector_3D(-1,0,-1), white, 0.5)
]

main_node = TreeNode(['cam', Point_3D(0,0,0)])
main_node = generate_lighting_tree(main_node, Vector_3D(0,0,-1), objects, light_sources, 4)
main_node.output(0)