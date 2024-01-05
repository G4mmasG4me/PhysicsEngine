import pickle
from objs import Camera

from surface_properties import Material, glass, mirror, normal, rough, very_rough

from objs import Object
from shapes import Sphere, Cuboid, Infinite_Plane, Quad_Plane_Geometry, Cylinder, Pyramid, SkyBox
from objs import Custom_Shape, Custom

from geometry import Point_3D, Vector_3D
from geometry import Rotation_3D, Rotation

from objs import DirectionalLight, SpotLight, PointLight, AmbientLight
from colours import *

from surface_properties import Texture, default_texture, chessboard_1, chessboard_2, chessboard_3, bricks, sky

class Scene:
  def __init__(self, name, camera, objects, light_sources, skyboxes):
    self.name = name
    self.file_name = name + '.pkl'

    self.camera = camera
    self.objects = objects
    self.light_sources = light_sources
    self.skyboxes = skyboxes

if __name__ == '__main__':                             # x = pitch, positive is up | y = roll, positive is anti clockwise | z = yaw, positive is right  
  cam = Camera((1000,1000), 90, 10, Point_3D(0,-5,-5), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')))

  objects = [
    Object('floor', Infinite_Plane(), Point_3D(0,-20,0), Rotation_3D(Rotation(90, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_3, None, 1),
    Object('rock', Custom('objects/rock.obj', 'Rock'), Point_3D(10,-10,-10), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, rough, GRAY, None, 1),
    Object('wall', Quad_Plane_Geometry((20,20)), Point_3D(10,0,-25), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, rough, bricks, None, 1),
    Object('glass wall', Quad_Plane_Geometry((20,20)), Point_3D(-10,0,-25), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, glass, WHITE, None, 0.995),
    Object('sphere', Sphere(5), Point_3D(-10,0,-50), Rotation_3D(Rotation(0), Rotation(0), Rotation(0)), [1,1,1], 0, 0, 0, normal, MAGENTA, None, 1)
  ]

  light_sources = [
    # AmbientLight(WHITE, 0.2),
    PointLight(Point_3D(10, 0, 0), RED, 0.4, 0),
    DirectionalLight(Vector_3D(-1,0,-1), WHITE, 0.4)
  ]
  
  skyboxes = [
    SkyBox(Point_3D(0,0,0), 250, sky)
  ]

  name = input('Whats the Scene Name:')
  my_scene = Scene(name, cam, objects, light_sources, skyboxes)
  path = 'scenes/' + my_scene.file_name
  with open(path, 'wb') as file:
    pickle.dump(my_scene, file)