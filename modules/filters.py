from math import ceil
import numpy as np

class Filters:
  def __init__(self, default_brightness = 0.2):
    self.dynamic_filters_list = []
    self.set_brightness(default_brightness)

  def set_brightness(self, brightness):
    self.brightness_filter = np.vectorize(lambda x: ceil(x*brightness))

  def apply_filters_numpy(self, frame):
    return frame * 0.2
