import math
import numpy as np

def numpy_mixer(frame_a, frame_b, mix):
  return frame_a * (1-mix) + frame_b * mix

# ex. [255, 0, 0] becomes a 510-size vector
def make_rgb_frame(rgb):
  return np.tile(rgb, 170)

# frame input should be 512x80 from video or image from cv2
# output should be 510x30
def remove_unused_pixels_from_frame(frame):
  frame = np.minimum.reduce(
    np.array(frame, dtype=np.uint8), 2
  )
  
  # remove empties
  mask = np.zeros(len(frame), dtype=bool)
  mask[[0,1,2,3,4,5, 16,17,18,19,20,21, 32,33,34,35,36,37, 48,49,50,51,52,53, 64,65,66,67,68,69]] = True
  frame = frame[mask,...]

  frame = np.delete(frame, (510, 511), axis=1)

  # should be 30, 510
  assert(len(frame) == 30)
  assert(len(frame[0]) == 510)
  return frame

# convert to polar coordinate, assuming center is (0.5, 0.5)
def to_polar(point):
  x = point[0] - 0.5
  y = point[1] - 0.5
  r = (x ** 2 + y ** 2) ** .5
  theta = math.degrees(math.atan2(y,x)) % 360
  return r, theta

def scale_to(val, old_range, new_range):
  (old_range_min, old_range_max) = old_range
  normalized_val = (val - old_range_min) / (old_range_max - old_range_min)
  (new_range_min, new_range_max) = new_range
  return normalized_val * (new_range_max - new_range_min) + new_range_min

# all blacks
nullframe = np.zeros((30,510), dtype=np.uint8)