import pickle
from Camera import Camera

from Material import Material, glass, mirror, normal, rough

from Object import Object
from Shapes import Sphere, Cuboid, Infinte_Plane, Quad_Plane_Geometry, Cylinder

from Points import Point_3D, Vector_3D
from Rotation import Rotation_3D, Rotation

from Lights import DirectionalLight, SpotLight, PointLight, AmbientLight
from Colour import *

from Texture import Texture, default_texture, chessboard_1, chessboard_2, chessboard_3

class Scene:
  def __init__(self, name, camera, objects, light_sources):
    self.name = name
    self.file_name = name + '.pkl'

    self.camera = camera
    self.objects = objects
    self.light_sources = light_sources

if __name__ == '__main__':
  cam = Camera((1000,1000), 90, 10, Point_3D(0,0,0), Rotation_3D(Rotation(0),Rotation(0),Rotation(0)))

  objects = [
    Object(Infinte_Plane(), Point_3D(0,-20,0), Rotation_3D(Rotation(90, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_3, None, 1),
    Object(Sphere(10), Point_3D(-15,10,-40), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_2, None, 1),
    Object(Cuboid((10,10,10)), Point_3D(-15,0,-40), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, rough, RED, None, 1),
    Object(Sphere(10), Point_3D(-15,-10,-40), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_1, None, 1),
    Object(Sphere(10), Point_3D(15,10,-80), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_1, None, 1),
    Object(Cylinder(10,10), Point_3D(15,20,-80), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, BLUE, None, 1),
    Object(Sphere(10), Point_3D(15,30,-80), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, normal, chessboard_2, None, 1),
    Object(Quad_Plane_Geometry((40,40)), Point_3D(-40,0,-20), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, glass, WHITE, None, 1.2),
    Object(Quad_Plane_Geometry((40,40)), Point_3D(40,0,-60), Rotation_3D(Rotation(0, unit='deg'),Rotation(90, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, mirror, WHITE, None, 1),
  ]

  objects = [
    Object(Infinte_Plane(), Point_3D(0,-20,0), Rotation_3D(Rotation(90, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.1,1,0,0), chessboard_3, None, 1),
    Object(Sphere(10), Point_3D(-50,10,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.2,10,0,0), BLUE, None, 1),
    Object(Sphere(10), Point_3D(-25,10,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.4,10,0,0), BLUE, None, 1),
    Object(Sphere(10), Point_3D(0,10,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.6,10,0,0), BLUE, None, 1),
    Object(Sphere(10), Point_3D(25,10,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.8,10,0,0), BLUE, None, 1),
    Object(Sphere(10), Point_3D(50,10,-75), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(1,10,0,0), BLUE, None, 1),
  ]
  objects = [
    Object(Sphere(10), Point_3D(0,0,-25), Rotation_3D(Rotation(0, unit='deg'),Rotation(0, unit='deg'),Rotation(0, unit='deg')), [1,1,1], 0, 0, 0, Material(0.1,1,0,0), BLUE, None, 1),
  ]

  light_sources = [
    AmbientLight(WHITE, 0.2),
    DirectionalLight(Vector_3D(-1,0,-1), WHITE, 0.5)
  ]

  name = input('Whats the Scene Name:')
  my_scene = Scene(name, cam, objects, light_sources)
  path = 'scenes/' + my_scene.file_name
  with open(path, 'wb') as file:
    pickle.dump(my_scene, file)