import math

class Camera:
  def __init__(self, position, rotation, resolution, FOV, focal_length, render_distance):
    self.position = position
    self.rotation = rotation
    self.rotation_matrix = xyz_matrix
    self.inverse_rotation_matrix = inverse_matrix(self.rotation_matrix)
    self.resolution = resolution
    self.FOV = FOV # stored in radians
    self.focal_length = focal_length
    self.render_distance = render_distance

  def calculate_pixel_positions(self, rotation):
    self.rotation = rotation
    self.rotation_matrix = xyz_matrix(self.rotation)
    self.inverse_rotation_matrix = inverse_rotation_matrix(self.roation_matrix)

  def calc_canvas_size(self):
    canvas_width = 2 * self.focal_length * math.tan(self.hFOV)/2
    canvas_height = 2 * self.focal_length * math.tan(self.vFOV)/2
    return [canvas_width, canvas_height]
    
  def pixel_size(self):
    canvas_width = 2 * self.focal_length * math.tan(self.hFOV/2)
    return canvas_width / self.resolution[0]

  def calculate_canvas_pixel_positions(self):
    canvas_pixel_positions = []
    for y in range(round(self.resolution[1]/2), -round(self.resolution[1]/2), -1):
      canvas_pixel_row = []
      for x in range(-round(self.resolution[0]/2), round(self.resoltuion[0]/2)):
        canvas_pixel_row.append([x*self.px_size, y*self.px_size])
      canvas_pixel_positions.append(canvas_pixel_row)
    return canvas_pixel_positions
  
  def change_FOV(self, FOV):
    self.hFOV = FOV
    self.vFOV = self.calc_vfov(FOV)

  def calc_vFOV(self):
    return 2 * math.atan(math.tan(self.hFOV/2) * (self.resolution[1] / self.resoltuion[0]))
# things that have to be done for the camera when rendering

# only change canvas position if resolution, fov or focal_length change
# pixel positions are relative to camera