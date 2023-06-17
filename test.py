from Shapes import Sphere
from geometry import Point_3D, Rotation_3D, Ray_3D
from intersections import ray_sphere_intersection

if __name__ == '__main__':
  sphere = Sphere(Point_3D(50,-10,100), Rotation_3D(0,0,0), 10, (0,0,0))
  ray = Ray_3D(Point_3D(0,0,0), Point_3D(5,-1,10))
  intersection = ray_sphere_intersection(ray, sphere)
  if intersection:
    print(f'Intersection 1 | [{intersection[0].x}, {intersection[0].y}, {intersection[0].z}')
    print(f'Intersection 2 | [{intersection[1].x}, {intersection[1].y}, {intersection[1].z}')
    print(f't1: {intersection[2]} | t2: {intersection[3]}')