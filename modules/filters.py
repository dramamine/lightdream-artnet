from math import ceil
import numpy as np

class Filters:
  def __init__(self, default_brightness = 0.2):
    self.dynamic_filters_list = []
    self.set_brightness(default_brightness)

  def set_brightness(self, brightness):
    self.brightness_filter = np.vectorize(lambda x: ceil(x*brightness))
  
  def another_brightness(self, frame):
    return np.multiply(frame, 0.7)
    
  def divider_brightness(self, frame):
    return np.floor_divide(frame, 2)

  def apply_filters_numpy(self, frame):
    # print("before:", frame[0][0], frame[0][1], frame[0][2])
    frame = self.another_brightness(frame)
    frame = frame.astype(np.uint8)
    # print("after:", frame[0][0], frame[0][1], frame[0][2])
    return frame
