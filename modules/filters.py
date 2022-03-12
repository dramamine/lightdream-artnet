from math import ceil
import numpy as np

class Filters:
  def __init__(self, brightness = 0.5):
    self.dynamic_filters_list = []
    self.set_brightness(brightness)

  def set_brightness(self, brightness):
    assert(brightness >= 0.0)
    assert(brightness <= 1.0)
    self.brightness = brightness
  
  def apply_brightness(self, frame):
    return np.multiply(frame, self.brightness)

  # note that 'frame' could be dtype uint8 or float64 at this point.
  # but output has gotta be uint8 so we can convert to bytearray later.
  def apply_filters(self, frame):
    # print("before:", frame[0][0], frame[0][1], frame[0][2])
    frame = self.apply_brightness(frame)
    frame = np.minimum(frame, 255)
    frame = np.maximum(frame, 0)
    frame = frame.astype(np.uint8)
    # print("after:", frame[0][0], frame[0][1], frame[0][2])
    return frame
