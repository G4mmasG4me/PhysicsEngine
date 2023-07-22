from Tree import TreeNode
from Points import Point_3D, Vector_3D
from Lines import Ray_3D, Segment_3D
from light_equations import reflected_ray_dir, refracted_ray_dir, ray_inside_outside_detection
import pickle
from Shapes import Infinte_Plane, Quad_Plane_Geometry
from Colour import Colour

air_refractive_index = 1.000293

def generate_lighting_tree(node, direction, objects, light_sources, max_depth, current_depth=0, refraction_stack=[]):
  primary_ray = Ray_3D(node.value['position'], direction)
  intersections = [] # position, normal, distance, colour, material, refractive index
  
  Ia = Colour((0,0,0))
  Id = Colour((0,0,0))
  Is = Colour((0,0,0))

  # find all intersections
  for obj in objects:
    intersections += obj.intersection(primary_ray)
  
  # if there is an intersection with an object
  if intersections:
    # get closest intersection
    closest_intersection = min(intersections, key=lambda x: x[2])

    # unpacks all values from the closest intersection
    obj_intersection, obj_normal, distance, obj_colour, obj_material, obj_refractive_index, intersection_obj = closest_intersection

    # creates an object node
    obj_node = TreeNode({'type':'obj', 'position':obj_intersection, 'normal':obj_normal, 'colour':obj_colour, 'material':obj_material, 'intensity':obj_material.transparency})

    # adds the object node to original node
    node.add_child(obj_node)

    # creates the direction to the view/position of previous node, used for diffuse and specular light. 
    V = node.value['position'] - obj_intersection
    

    ########## refraction / reflection rays ##########
    if current_depth < max_depth:
      
      # generate_reflecion ray
      if obj_material.smoothness: # must be smooth to generate reflection
        reflected_ray = reflected_ray_dir(primary_ray, obj_normal)
        L = reflected_ray.normalise() # direction towards light
        N, NL_dot = max([[N, N.dot(L)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])
        R = 2 * NL_dot * N - L
        RV_dot = R.dot(V)

        new_node, colour = generate_lighting_tree(obj_node, reflected_ray, objects, light_sources, max_depth, current_depth+1, refraction_stack)

        colour = obj_colour * colour * (1-obj_material.transparency)
        Id += colour * max(0, NL_dot) * (1-obj_material.smoothness)
        Is += colour * max(0, RV_dot)**obj_material.shininess * obj_material.smoothness
        

      # generate refraction ray
      if obj_material.transparency: # must be transparent to refract
        if isinstance(intersection_obj.geometry, (Infinte_Plane, Quad_Plane_Geometry)): # not interior on plane types
          refractive_index_1 = refraction_stack[-1] if refraction_stack else air_refractive_index
          refractive_index_2 = obj_refractive_index
        else:
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
        L = refracted_ray.normalise() # direction towards light
        N, NL_dot = max([[N, N.dot(L)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])
        R = 2 * NL_dot * N - L
        RV_dot = R.dot(V)
        new_node, colour = generate_lighting_tree(obj_node, refracted_ray, objects, light_sources, max_depth, current_depth+1, refraction_stack)
        colour = obj_colour * colour * obj_material.transparency

        Id += colour * max(0, NL_dot) * (1-obj_material.smoothness)
        Is += colour * max(0, RV_dot)**obj_material.shininess * obj_material.smoothness



    ########## shadow rays ##########
    # need to implemenet a special condition for objects with plane geometry, as shadows will be casted from the previous side, because it doesn't have an interior
    # split light sources
    sorted_light_sources = {'AmbientLight':[], 'PointLight':[], 'SpotLight':[], 'DirectionalLight':[]}
    for item in light_sources:
      item_type = type(item).__name__
      sorted_light_sources[item_type].append(item)

    for light in sorted_light_sources['AmbientLight']:
      ambient_light_node = TreeNode({'type': 'ambientlight', 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
      Ia += obj_colour * light.colour * light.intensity
      obj_node.add_child(ambient_light_node)


    ##### PointLights #####
    valid_pointlights = sorted_light_sources['PointLight']
    # for planes makes sure the light is shining on the right side of the plane
    if isinstance(intersection_obj.geometry, (Infinte_Plane, Quad_Plane_Geometry)):
      pointlights = []
      for pointlight in valid_pointlights:
        if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0] == max([[N, N.dot(pointlight.point - obj_intersection)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0]:
          pointlights.append(pointlight)
      valid_pointlights = pointlights

    for light in valid_pointlights:
      
      segment = Segment_3D(obj_intersection, light.point)
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(segment)
        light_obstructed = any([value is not None for value in light_intersections])
        if not light_obstructed:
          L = (light.position - obj_intersection).to_vector().normalise() # direction towards light
          N, NL_dot = max([[N, N.dot(L)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])
          R = 2 * NL_dot * N - L
          RV_dot = R.dot(V)

          colour = obj_colour * light.colour * light.intensity * (1-obj_material.transparency) # light only affects as reflections not refractions
          Id += colour * max(0, NL_dot) * (1-obj_material.smoothness)
          Is += colour * max(0, RV_dot)**obj_material.shininess * obj_material.smoothness

          pointlight_node = TreeNode({'type': 'pointlight', 'position':light.position, 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
          obj_node.add_child(pointlight_node)


    ##### SpotLights #####
    spotlights = sorted_light_sources['SpotLight']
    valid_spotlights = [spotlight for spotlight in spotlights if spotlight.facing_direction(obj_intersection - spotlight.position)]
    
    # for planes makes sure the light is shining on the right side of the plane
    if isinstance(intersection_obj.geometry, (Infinte_Plane, Quad_Plane_Geometry)):
      spotlights = []
      for spotlight in valid_spotlights:
        if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0] == max([[N, N.dot(spotlight.point - obj_intersection)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0]:
          spotlights.append(spotlight)
      valid_spotlights = spotlights

    for light in valid_spotlights:
      segment = Segment_3D(obj_intersection, light.point)
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(segment)
      light_obstructed = any([value is not None for value in light_intersections])
      if not light_obstructed:
        L = (light.position - obj_intersection).to_vector().normalise() # direction towards light
        N, NL_dot = max([[N, N.dot(L)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1]) # N = towards plane normal
        R = 2 * NL_dot * N - L
        RV_dot = R.dot(V)

        colour = obj_colour * light.colour * light.intensity * (1-obj_material.transparency) # light only affects as reflections not refractions
        Id += colour * max(0, NL_dot) * (1-obj_material.smoothness)
        Is += colour * max(0, RV_dot)**obj_material.shininess * obj_material.smoothness

        spotlight_node = TreeNode({'type':'spotlight', 'position':light.position, 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
        obj_node.add_child(spotlight_node)

    ##### DirectionalLights ######
    valid_directionallights = sorted_light_sources['DirectionalLight']
    # for planes makes sure the light is shining on the right side of the plane
    """ if isinstance(intersection_obj.geometry, (Infinte_Plane, Quad_Plane_Geometry)):
      directionallights = []
      for directionallight in valid_directionallights:
        if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0] == max([[N, N.dot(directionallight.direction.inverse())] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])[0]:
          directionallights.append(directionallight)
      valid_directionallights = directionallights """


    for light in valid_directionallights:
      ray = Ray_3D(obj_intersection, light.direction.inverse())
      light_intersections = []
      for object in objects:
        light_intersections += object.intersection(ray)
      
      light_obstructed = any([value is not None for value in light_intersections])
      if not light_obstructed:
        L = light.direction.inverse()
        N, NL_dot = max([[N, N.dot(L)] for N in [obj_normal, obj_normal.inverse()]], key=lambda x: x[1])
        NL_dot = max(0, NL_dot)
        R = 2 * NL_dot * N - L
        RV_dot = R.dot(V)
        RV_dot = max(0, RV_dot)

        
        colour = obj_colour * light.colour * light.intensity * (1-obj_material.transparency)
        Id += colour * NL_dot * (1-obj_material.smoothness)
        
        Is += colour * RV_dot**obj_material.shininess * obj_material.smoothness

        directionallight_node = TreeNode({'type':'directionallight', 'direction':light.direction, 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
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
  
  final_colour = Ia + Id + Is
  node.value['final_colour'] = final_colour
  
  return node, final_colour