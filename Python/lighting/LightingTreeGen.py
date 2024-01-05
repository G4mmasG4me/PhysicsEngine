from Tree import TreeNode
from shapes import Infinite_Plane
from geometry import Point_3D, Vector_3D
from geometry import Ray_3D, Segment_3D
from lighting import reflected_ray_dir, refracted_ray_dir, ray_inside_outside_detection
import pickle
from shapes import Quad_Plane_Geometry, SkyBox
from surface_properties import Colour

from lighting import oren_nayar, cook_torrance, phong

from config import epsilon

# returns second position in list, used for key instead of lambda
def func1(x):
  return x[1]

# returns third position in list, used for key instead of lambda
def func2(x):
  return x['distance']
air_refractive_index = 1.000293

def generate_lighting_tree(node, direction, objects, light_sources, skyboxes, max_depth, render_method, current_depth=0, refraction_stack=[]):
  primary_ray = Ray_3D(node.value['position'], direction)
  intersections = [] # position, normal, distance, colour, material, refractive index
  
  Ia = Colour((0,0,0))
  Id = Colour((0,0,0))
  Is = Colour((0,0,0))
  obj_colour = Colour((0,0,0))

  # find all intersections
  for obj in objects:
    intersections += obj.intersection(primary_ray)

  for skybox_obj in skyboxes:
    intersections += skybox_obj.intersection(primary_ray)

  
  # if there is an intersection with an object
  if intersections:
    # get closest intersection
    closest_intersection = min(intersections, key=func2)
    if isinstance(closest_intersection['obj'], SkyBox):
      Ia = closest_intersection['colour']
      skybox_node = TreeNode({'type':'SkyBox', 'position':closest_intersection['intersection'], 'normal':closest_intersection['normal'], 'final_colour':closest_intersection['colour']})
      node.add_child(skybox_node)
    else:


      # unpacks dictionary
      obj_intersection = closest_intersection['intersection']
      obj_normal = closest_intersection['normal']
      obj_colour = closest_intersection['colour']
      obj_material = closest_intersection['material']
      obj_refractive_index = closest_intersection['refractive index']
      intersection_obj = closest_intersection['obj']

      # creates an object node
      obj_node = TreeNode({'type':'obj', 'position':obj_intersection, 'normal':obj_normal, 'colour':obj_colour, 'material':obj_material, 'intensity':obj_material.transparency})

      # adds the object node to original node
      node.add_child(obj_node)

      # creates the direction to the view/position of previous node, used for diffuse and specular light. 
      V = (node.value['position'] - obj_intersection).to_vector().normalise()
      
      ########## refraction / reflection rays ##########
      if current_depth < max_depth:
        
        # generate_reflecion ray
        if obj_material.roughness: # must be smooth to generate reflection
          n1 = refraction_stack[-1] if refraction_stack else air_refractive_index
          n2 = obj_refractive_index
          reflected_ray = reflected_ray_dir(primary_ray, obj_normal)
          # phong lighting method
          L = reflected_ray.normalise() # direction towards light
          new_node, colour = generate_lighting_tree(obj_node, reflected_ray, objects, light_sources, skyboxes, max_depth, render_method, current_depth+1, refraction_stack)
          light_colour = colour[0] * (1-obj_material.transparency)
          if render_method.lower() == 'low':
            Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
            Id += Id_add
            Is += Is_add

          # oren nayar and cook torrance lighting method
          elif render_method.lower() == 'high':
            Id += oren_nayar(obj_colour, light_colour, primary_ray, obj_normal, L, V, obj_material.roughness)
            if obj_material.transparency == 0:
              if abs(L.dot(V)) > epsilon:
                Is += cook_torrance(obj_colour, light_colour, obj_normal, L, V, obj_material.roughness, n1, n2)
            else:
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Is += Is_add
          else:
            raise 'Error: Invalid Render Method'
          

        # generate refraction ray
        if obj_material.transparency: # must be transparent to refract
          if isinstance(intersection_obj.geometry, (Infinite_Plane, Quad_Plane_Geometry)): # not interior on plane types
            n1 = refraction_stack[-1] if refraction_stack else air_refractive_index
            n2 = obj_refractive_index
          else:
            inside_outside = ray_inside_outside_detection(primary_ray, intersection_obj)
            if inside_outside == 'inside': # ray leaving object
              n1 = refraction_stack.pop()
              if refraction_stack:
                n2 = refraction_stack[-1]
              else:
                n2 = air_refractive_index

            elif inside_outside == 'outside': # ray entering object
              if refraction_stack:
                n1 = refraction_stack[-1]
              else:
                n1 = air_refractive_index
              n2 = obj_refractive_index
              refraction_stack.append(obj_refractive_index)

          refracted_ray = refracted_ray_dir(primary_ray, obj_normal, n1, n2)
          if refracted_ray:
            L = refracted_ray.normalise() # direction towards light
            new_node, colour = generate_lighting_tree(obj_node, refracted_ray, objects, light_sources, skyboxes, max_depth, render_method, current_depth+1, refraction_stack)
            light_colour = colour[0] * obj_material.transparency
            if render_method.lower() == 'low':
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Id += Id_add
              Is += Is_add

            # oren nayar and cook torrance lighting method
            elif render_method.lower() == 'high':
              Id += oren_nayar(obj_colour, light_colour, primary_ray, obj_normal, L, V, obj_material.roughness)
              if obj_material.transparency == 0:
                if abs(L.dot(V)) > epsilon:
                  Is += cook_torrance(obj_colour, light_colour, obj_normal, L, V, obj_material.roughness, n1, n2)
              else:
                Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
                Is += Is_add
            else:
              raise 'Error: Invalid Render Method'



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

      n1 = air_refractive_index
      n2 = obj_refractive_index
      ##### PointLights #####
      valid_pointlights = sorted_light_sources['PointLight']
      # for planes makes sure the light is shining on the right side of the plane
      if isinstance(intersection_obj.geometry, (Infinite_Plane, Quad_Plane_Geometry)):
        pointlights = []
        for pointlight in valid_pointlights:
          if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0] == max([[N, N.dot(pointlight.position - obj_intersection)] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0]:
            pointlights.append(pointlight)
        valid_pointlights = pointlights

      for light in valid_pointlights:
        
        segment = Segment_3D(obj_intersection, light.position)
        light_intersections = []
        for object in objects:
          light_intersections += object.intersection(segment)
          light_obstructed = any([value is not None for value in light_intersections])
          if not light_obstructed:
            L = (light.position - obj_intersection).to_vector().normalise() # direction towards light
            light_colour = light.colour * light.intensity * (1-obj_material.transparency) # light only affects as reflections not refractions
            if render_method.lower() == 'low':
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Id += Id_add
              Is += Is_add

            # oren nayar and cook torrance lighting method
            elif render_method.lower() == 'high':
              Id += oren_nayar(obj_colour, light_colour, segment, obj_normal, L, V, obj_material.roughness)
              if obj_material.transparency == 0:
                if abs(L.dot(V)) > epsilon:
                  Is += cook_torrance(obj_colour, light_colour, obj_normal, L, V, obj_material.roughness, n1, n2)
              else:
                Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
                Is += Is_add
                
            else:
              raise 'Error: Invalid Render Method'

            pointlight_node = TreeNode({'type': 'pointlight', 'position':light.position, 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
            obj_node.add_child(pointlight_node)


      ##### SpotLights #####
      spotlights = sorted_light_sources['SpotLight']
      valid_spotlights = [spotlight for spotlight in spotlights if spotlight.facing_direction(obj_intersection - spotlight.position)]
      
      # for planes makes sure the light is shining on the right side of the plane
      if isinstance(intersection_obj.geometry, (Infinite_Plane, Quad_Plane_Geometry)):
        spotlights = []
        for spotlight in valid_spotlights:
          if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0] == max([[N, N.dot(spotlight.position - obj_intersection)] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0]:
            spotlights.append(spotlight)
        valid_spotlights = spotlights

      for light in valid_spotlights:
        segment = Segment_3D(obj_intersection, light.position)
        light_intersections = []
        for object in objects:
          light_intersections += object.intersection(segment)
        light_obstructed = any([value is not None for value in light_intersections])
        if not light_obstructed:
          L = (light.position - obj_intersection).to_vector().normalise() # direction towards light
          light_colour = light.colour * light.intensity * (1-obj_material.transparency) # light only affects as reflections not refractions
          if render_method.lower() == 'low':
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Id += Id_add
              Is += Is_add

          # oren nayar and cook torrance lighting method
          elif render_method.lower() == 'high':
            Id += oren_nayar(obj_colour, light_colour, segment, obj_normal, L, V, obj_material.roughness)
            if obj_material.transparency == 0:
              if abs(L.dot(V)) > epsilon:
                Is += cook_torrance(obj_colour, light_colour, obj_normal, L, V, obj_material.roughness, n1, n2)
            else:
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Is += Is_add
          else:
            raise 'Error: Invalid Render Method'

          spotlight_node = TreeNode({'type':'spotlight', 'position':light.position, 'colour':light.colour, 'intensity':light.intensity, 'final_colour':light.colour*light.intensity})
          obj_node.add_child(spotlight_node)

      ##### DirectionalLights ######
      valid_directionallights = sorted_light_sources['DirectionalLight']
      # for planes makes sure the light is shining on the right side of the plane
      """ if isinstance(intersection_obj.geometry, (Infinite_Plane, Quad_Plane_Geometry)):
        directionallights = []
        for directionallight in valid_directionallights:
          if max([[N, N.dot(V)] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0] == max([[N, N.dot(directionallight.direction.inverse())] for N in [obj_normal, obj_normal.inverse()]], key=func1)[0]:
            directionallights.append(directionallight)
        valid_directionallights = directionallights """


      for light in valid_directionallights:
        ray = Ray_3D(obj_intersection, light.direction.inverse())
        light_intersections = []
        for object in objects:
          light_intersections += object.intersection(ray)
        
        light_obstructed = any([value is not None for value in light_intersections])

        L = light.direction.inverse()
        if not light_obstructed and obj_normal.dot(L): # check not obstructed and not perpendicular
          
          light_colour = light.colour * light.intensity * (1-obj_material.transparency)
          if render_method.lower() == 'low':
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Id += Id_add
              Is += Is_add

            # oren nayar and cook torrance lighting method
          elif render_method.lower() == 'high':
            Id += oren_nayar(obj_colour, light_colour, ray, obj_normal, L, V, obj_material.roughness)
            if obj_material.transparency == 0:
              # print(f'Normal: {obj_normal}')
              if abs(L.dot(V)) > epsilon:
                Is += cook_torrance(obj_colour, light_colour, obj_normal, L, V, obj_material.roughness, n1, n2)
            else:
              Id_add, Is_add = phong(obj_colour, light_colour, obj_material.roughness, obj_normal, L, V, obj_material.shininess)
              Is += Is_add
          else:
            raise 'Error: Invalid Render Method'

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
  node.value['Ia'] = Ia
  node.value['Id'] = Id
  node.value['Is'] = Is
  node.value['final_colour'] = final_colour


    
  
  
  
  
  return node, (final_colour, Ia, Id, Is)