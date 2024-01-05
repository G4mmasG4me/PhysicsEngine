import time

test_amount = 1000

ray_point = (0,0,0)
ray_direction = (1,1,1)
square = [
	(10,10,10),
	(10,10,0),
	(0,10,0),
	(0,10,10)
]
square.reverse()

points = square[:3]
def points_to_plane(points):
	points = points[:3]
	a = [points[1][0] - points[0][0], points[1][1] - points[0][1], points[1][2] - points[0][2]]
	b = [points[2][0] - points[0][0], points[2][1] - points[0][1], points[2][2] - points[0][2]]
	N = [
		a[1]*b[2] - a[2]*b[1],
		a[2]*b[0] - a[0]*b[2],
		a[0]*b[1] - a[1]*b[0]
	]
	A = N[0]
	B = N[1]
	C = N[2]
	D = -(A*points[0][0] + B*points[0][1] + C*points[0][2])
	return A,B,C,D

def ray_plane_intersection(ray_point, ray_direction, plane):
	total_t = plane[0] * ray_direction[0] + plane[1] * ray_direction[1] + plane[2] * ray_direction[2]
	total = plane[0] * ray_point[0] + plane[1] * ray_point[1] * plane[2] * ray_point[2] + plane[3]
	# total_t + total = 0
	# total_t = -total
	t = -total / total_t
	intersection = (
		ray_point[0] + t * ray_direction[0],
		ray_point[1] + t * ray_direction[1],
		ray_point[2] + t * ray_direction[2]
	)
	return intersection
	
def square_intersection(square_points, point):
	sp = square_points
	edge_vectors = [
    [sp[1][0] - sp[0][0], sp[1][1] - sp[0][1], sp[1][2] - sp[0][2]],
    [sp[2][0] - sp[1][0], sp[2][1] - sp[1][1], sp[2][2] - sp[1][2]],
    [sp[3][0] - sp[2][0], sp[3][1] - sp[2][1], sp[3][2] - sp[2][2]],
    [sp[0][0] - sp[3][0], sp[0][1] - sp[3][1], sp[0][2] - sp[3][2]]
	]

	ev = edge_vectors
	point_vertices_vectors = [
    [point[0] - sp[0][0], point[1] - sp[0][1], point[2] - sp[0][2]],
    [point[0] - sp[1][0], point[1] - sp[1][1], point[2] - sp[1][2]],
    [point[0] - sp[2][0], point[1] - sp[2][1], point[2] - sp[2][2]],
    [point[0] - sp[3][0], point[1] - sp[3][1], point[2] - sp[3][2]]
]
	pvv = point_vertices_vectors
	A = ev[0][0]*pvv[0][0] + ev[0][1]*pvv[0][1] + ev[0][2]*pvv[0][2]
	B = ev[1][0]*pvv[1][0] + ev[1][1]*pvv[1][1] + ev[1][2]*pvv[1][2]
	C = ev[2][0]*pvv[2][0] + ev[2][1]*pvv[2][1] + ev[2][2]*pvv[2][2]
	D = ev[3][0]*pvv[3][0] + ev[3][1]*pvv[3][1] + ev[3][2]*pvv[3][2]
	return A,B,C,D

def split_square(square):
	t1 = [
		square[0],
		square[1],
		square[2]
	]
	t2 = [
		square[0],
	  square[2],
		square[3]]

def triangle_intersection():
	pass



if __name__ == '__main__':
	start = time.time()
	for i in range(test_amount):
		plane = points_to_plane(square)
		intersection = ray_plane_intersection(ray_point, ray_direction, plane)
		intersects = square_intersection(square, intersection)
		print(intersects)
		quit()
	end = time.time()
	total = end - start
	print(f'Total Time: {total:.2f} | Time Per Int: {total/test_amount:.2f}')